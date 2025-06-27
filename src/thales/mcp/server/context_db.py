"""
SQLITE AI Agent Context Database 
Stores
- MCP:
    - Prompts
        {
            name: string;              // Unique identifier for the prompt
            description?: string;      // Human-readable description
            arguments?: [              // Optional list of arguments
                {
                name: string;          // Argument identifier
                description?: string;  // Argument description
                required?: boolean;    // Whether argument is required
                }
            ]
        }
    - Resources
        - Text resources
            - docs
        - Binary
            - images
            - videos
            - pdfs
            - audio
- Agent Framework
    - Goals & Tasks
    - Agent Ontology
        - identity
        - interactions
        - policies
        - 

TODO Create Pydantic/Dataclass model for each
    - Goals / Tasks / AgentOntology from AgentOntology
    - Prompts / 
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any, TypeGuard

DB_PATH = "context.db"

class ContextDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Create tables for identities, goals, tasks
            c.execute("""
                CREATE TABLE IF NOT EXISTS identities (
                    agent_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    goal_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()

    def store_identity(self, agent_id: str, identity_data: Dict[str, Any]) -> None:
        data_json = json.dumps(identity_data)
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO identities (agent_id, data) VALUES (?, ?)
            """, (agent_id, data_json))
            conn.commit()

    def _identity_type(self, v: Any) -> TypeGuard[dict[str, Any]]:
        return isinstance(v, dict)

    def get_identity(self, agent_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT data FROM identities WHERE agent_id = ?", (agent_id,))
            row = c.fetchone()
            raw = json.loads(row[0])
            if not self._identity_type(raw):
                raise ValueError("Not JSON Object for Identity") 
            return None

    def store_goal(self, goal_id: str, goal_data: Dict[str, Any]) -> None:
        data_json = json.dumps(goal_data)
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO goals (goal_id, data) VALUES (?, ?)
            """, (goal_id, data_json))
            conn.commit()

    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT data FROM goals WHERE goal_id = ?", (goal_id,))
            row = c.fetchone()
            raw = json.loads(row[0])
            if not self._identity_type(raw):
                raise ValueError("Not JSON Object for Goal") 
            return None

    def store_task(self, task_id: str, task_data: Dict[str, Any]) -> None:
        data_json = json.dumps(task_data)
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO tasks (task_id, data) VALUES (?, ?)
            """, (task_id, data_json))
            conn.commit()

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT data FROM tasks WHERE task_id = ?", (task_id,))
            row = c.fetchone()
            raw = json.loads(row[0])
            if not self._identity_type(raw):
                raise ValueError("Not JSON Object for Task") 
            return None

    def find_components(self, component_type: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Basic search by filtering JSON data in Python after fetching all rows.
        component_type: 'identities', 'goals', or 'tasks'
        query: dict of key-value pairs to match inside the JSON data
        """
        if component_type not in ('identities', 'goals', 'tasks'):
            raise ValueError("Invalid component_type. Must be 'identities', 'goals', or 'tasks'.")

        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f"SELECT data FROM {component_type}")
            rows = c.fetchall()

        results = []
        for (data_json,) in rows:
            data = json.loads(data_json)
            if all(data.get(k) == v for k, v in query.items()):
                results.append(data)
        return results
