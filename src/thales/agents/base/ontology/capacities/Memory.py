"""
Defines AI Agent knowledge base, enabling persistent
memory. Excludes knowledge of tools.

Local Data Classes
    - `Message`: Single conversational turn
    - `Session`: Continuous interaction.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, NewType
from uuid import UUID, uuid4


class CallerRole(Enum):
    SYSTEM = "system"
    USER = "user"
    AGENT = "agent"


# Strongly-typed alias (helps mypy/pyright catch mix-ups)
SessionID = NewType("SessionID", str)
ActorID = NewType("ActorID", str)


@dataclass(slots=True)
class MessageRecord:
    session_id: SessionID
    role: CallerRole
    content: str
    actor_id: ActorID | None = None


@dataclass(slots=True)
class SessionMeta:
    """can be multi-agent session"""

    session_id: SessionID
    start_time: str
    metadata: Dict[str, Any] | None = None


@dataclass(slots=True)
class LLMMsg:
    """messages loaded into memory from DB"""

    role: str
    content: Any


@dataclass
class Memory:
    """
    Central hub for an agent's knowledge, with persistent knowledge store. Excludes tool 'knowledge'
    """

    sessions: Dict[SessionID, SessionMeta] = field(default_factory=dict)
    messages: Dict[SessionID, List[LLMMsg]] = field(default_factory=dict)

    def start_session(
        self,
        session_id: Optional[SessionID] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SessionID:
        """Creates and stores a new session, returning its ID."""

        session_id = session_id or SessionID(str(uuid4()))
        start_time = datetime.now(timezone.utc).isoformat()

        self.sessions[session_id] = SessionMeta(
            session_id=session_id,
            start_time=start_time,
            metadata=metadata,
        )

        return SessionID(session_id)

    def add_message(self, session_id: SessionID, role: CallerRole, content: str, actor_id: ActorID) -> MessageRecord:
        """Adds a message to the session."""

        # Update in-memory cache
        if session_id not in self.messages:
            self.messages[session_id] = []
        self.messages[session_id].append(LLMMsg(role=role.value, content=content))

        return MessageRecord(
            session_id=session_id,
            role=role,
            content=content,
            actor_id=actor_id,
        )

    def get_history(self, session_id: SessionID) -> List[LLMMsg]:
        """Retrieves the full message history for a given session from the in-memory cache."""
        return self.messages.get(session_id, [])


async def main() -> None:
    """test _Knowledge"""

    kb = Memory()
    session_id = kb.start_session()
    print(f"Session ID {session_id}")
    kb.add_message(session_id, CallerRole.USER, "Hello World", ActorID("User_Caller"))
    kb.add_message(session_id, CallerRole.AGENT, "What do you want?", ActorID("Agent_Caller"))
    hist = kb.get_history(SessionID(session_id))
    print(hist)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
