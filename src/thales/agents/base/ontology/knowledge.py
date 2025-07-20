"""
Defines AI Agent knowledge base, enabling persistent
memory and dynamic tool use.

Expects Agent with LLM to use as part of its Ontology.

Local Data Classes
    - `Message`: Single conversational turn
    - `Session`: Continuous interaction.

Imported Data Classes
    - MCP Tool

Main Class (`Knowledge`):
    - Central orchestrator for all knowledge-related operations.
    - SQLite DB for persistent knowledge storage.
    - Methods
        - init args db_path, thales_multi_server_client
        - session
            - start / stop
            - list_all_sessions
            - find session
            - add messages to session x
            - list messages in session x
        - knowledge tools
            - list_knowledge_tools
            - select_for_use
            - use_knwolede_tool

Expected Usage:
1. Agent creator will Create Knowledge instance with
    - Agent ID
    - Thales Multi Server Client
    - DB location
2. Knowledge will...
    - Open DB Connection, with context manager
    - Check if Agent has previously been created:
        - Already exists: restore Knowledge
        - First time: Find and select relevant Knowledge Tools (e.g. Web Search)
3. Agent creator will
    - Add knowledge to AgentOntology
    - With intentions, style & imeratives
4. Agent will then...
    - Session Start:
        - New Session
            - Start new sessions.
            - Add messages to the session
        - Continue Session
            - Retrieve conversation history.
            - Add messages to the session
5. Context manager will close DB.
"""

import aiosqlite
import json
from dataclasses import dataclass
from mcp.types import Tool
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, NewType
from uuid import uuid4
from thales.mcp.client import EnhancedMCPClient


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    AGENT = "agent"


# Strongly-typed alias (helps mypy/pyright catch mix-ups)
SessionID = NewType("SessionID", str)
ActorID = NewType("ActorID", str)


@dataclass(slots=True)
class MessageRecord:
    message_id: int
    session_id: SessionID
    role: MessageRole
    content: str
    actor_id: ActorID | None= None

@dataclass(slots=True)
class SessionRecord:
    """ can be multi-agent session """
    session_id: SessionID
    start_time: datetime
    metadata: Dict[str, Any] | None = None

@dataclass(slots=True)
class LLMMsg:
    """ messages loaded into memory from DB """
    role: str
    content: Any

class _Knowledge:
    """
    Central hub for an agent's knowledge, with persistent knowledge store and a dynamic registry for knowledge-retrieval tools.
    """

    innate: dict[str, Any] | None = None
    _db_conn: aiosqlite.Connection | None = None

    def __init__(self, db_path: str, actor_id: str, mcp: EnhancedMCPClient) -> None:
        self.db_path: str = db_path
        self.actor_id: str = actor_id
        self.mcp: EnhancedMCPClient = mcp
        self.tools: Dict[str, Tool] = {}
        self.sessions: Dict[SessionID, SessionRecord] = {}
        self.messages: Dict[SessionID, List[LLMMsg]] = {}


    @classmethod
    async def create(cls, db_path: str, actor_id: str, mcp: EnhancedMCPClient) -> "_Knowledge":
        """Asynchronous factory constructor."""
        instance = cls(db_path, actor_id, mcp)
        await instance._initialize_db()

        if instance._db_conn:
            instance._db_conn.row_factory = aiosqlite.Row
            # First, get all unique session IDs for the actor
            get_sessions_query = "SELECT DISTINCT session_id FROM messages WHERE actor_id = ?"
            async with instance._db_conn.execute(get_sessions_query, (actor_id,)) as cursor:
                session_rows = await cursor.fetchall()
                session_ids = [SessionID(row["session_id"]) for row in session_rows]

            # For each session, load the session details and all messages
            for session_id in session_ids:
                # Load session record
                get_session_details_query = "SELECT * FROM sessions WHERE session_id = ?"
                async with instance._db_conn.execute(get_session_details_query, (session_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        instance.sessions[session_id] = SessionRecord(
                            session_id=SessionID(row["session_id"]),
                            start_time=datetime.fromisoformat(row["start_time"]),
                            metadata=json.loads(row["metadata"]) if row["metadata"] else None,
                        )

                # Load messages for the session
                get_messages_query = "SELECT role, content FROM messages WHERE session_id = ? ORDER BY message_id ASC"
                async with instance._db_conn.execute(get_messages_query, (session_id,)) as cursor:
                    message_rows = await cursor.fetchall()
                    instance.messages[session_id] = [
                        LLMMsg(role=row["role"], content=row["content"]) for row in message_rows
                    ]
        return instance

    async def _initialize_db(self) -> None:
        """Connects to the database and creates tables if they don't exist."""
        self._db_conn = await aiosqlite.connect(self.db_path)
        await self._db_conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                metadata TEXT
            )
            """
        )
        await self._db_conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES sessions (session_id),
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                actor_id TEXT
            )
            """
        )
        await self._db_conn.commit()

    async def close(self) -> None:
        """Closes the database connection gracefully."""
        if self._db_conn:
            await self._db_conn.close()

    async def start_session(
        self,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SessionID:
        """Creates and stores a new session, returning its ID."""
        if self._db_conn is None:
            raise ConnectionError("Database connection not initialized. Call create() to instantiate.")

        session_id = session_id or str(uuid4())
        start_time = datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata or {})

        await self._db_conn.execute(
            "INSERT INTO sessions (session_id, start_time, metadata) VALUES (?, ?, ?)",
            (session_id, start_time, metadata_json),
        )
        await self._db_conn.commit()
        return SessionID(session_id)

    async def add_message(
        self, session_id: SessionID, role: MessageRole, content: str, actor_id: ActorID
    ) -> MessageRecord:
        """Adds a message to a session, stores it in the database, and updates the in-memory cache."""
        if self._db_conn is None:
            raise ConnectionError("Database connection not initialized. Call create() to instantiate.")

        # Add to database
        await self._db_conn.execute(
            "INSERT INTO messages (session_id, role, content, actor_id) VALUES (?, ?, ?, ?)",
            (session_id, role.value, content, actor_id),
        )
        await self._db_conn.commit()

        # Retrieve the new message ID
        async with self._db_conn.execute("SELECT last_insert_rowid()") as cursor:
            row = await cursor.fetchone()
            if not row:
                raise RuntimeError("Failed to retrieve last inserted message ID.")
            message_id = row[0]

        # Update in-memory cache
        if session_id not in self.messages:
            self.messages[session_id] = []
        self.messages[session_id].append(LLMMsg(role=role.value, content=content))

        return MessageRecord(
            message_id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            actor_id=actor_id,
        )

    def get_history(self, session_id: SessionID) -> List[LLMMsg]:
        """Retrieves the full message history for a given session from the in-memory cache."""
        return self.messages.get(session_id, [])

    def register_tool(self, tool: Tool) -> None:
        """Registers a knowledge tool for the agent to use."""
        if tool.name in self.tools:
            # Consider logging a warning here
            pass
        self.tools[tool.name] = tool

    # TODO make this search for a 'knowledge tools' set - managed by MCPServerManager
    def get_knowledge_tools(self) -> None:
        """Uses the MCP client to find and register tools relevant to a query."""
        knowledge_tools = self.mcp.get_tool_set("knowledge")
        # TODO guard against tools being entered twice
        if knowledge_tools and knowledge_tools.tools:
            for tool in knowledge_tools.tools:
                self.register_tool(tool)


async def main()->None:
    """ test _Knowledge """
    # from thales.mcp.client import EnhancedMCPClient

    mcp = EnhancedMCPClient()
    kb =await _Knowledge.create("kb", "Agent_Caller", mcp)
    session_id = await kb.start_session()
    print(f"Session ID {session_id}")
    msg = await kb.add_message(session_id, MessageRole.USER, "Hello World", ActorID("User_Caller"))
    msg = await kb.add_message(session_id, MessageRole.AGENT, "What do you want?", ActorID("Agent_Caller"))
    hist = kb.get_history(SessionID(session_id))
    print(hist)
    await kb.close()



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
