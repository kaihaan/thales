"""An Agent Ontology
Describes everything the agent needs to know to operate
SQLAlchemy for persistance
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
from mcp import Tool

from thales.utils.logger import get_logger

logger = get_logger(__name__)

from .capacities import Identity, Goal, GoalStatus, Task, TaskStatus, TaskType, Memory, Imperatives


@dataclass
class AgentOntology:
    """Complete agent ontological framework"""

    identity: Identity = field(default_factory=lambda: Identity("DefaultAgent"))
    memory: Memory = field(default_factory=lambda: Memory())
    imperatives: Imperatives = field(default_factory=lambda: Imperatives())
    goals: dict[str, Goal] = field(default_factory=dict)
    tasks: dict[str, Task] = field(default_factory=dict)
    tools: dict[str, Tool] = field(default_factory=dict)

    def add_goal(self, goal: Goal) -> None:
        """Add a new goal to the agent"""
        found = self.goals.get(goal.goal_id)
        if not found:
            self.goals[goal.goal_id] = goal
            self.last_updated = datetime.now()
        else:
            logger.debug("Attempting to add goal - but goal already exists")

    def add_task(self, task: Task) -> None:
        """Add a new task to the agent"""
        if task.task_id in self.tasks:
            logger.debug("Adding task but it already exists")
            return
        self.tasks[task.task_id] = task
        self.last_updated = datetime.now()

    def get_active_goals(self) -> List[Goal]:
        """Get all active goals"""
        return [g for g in self.goals.values() if g.status == GoalStatus.IN_PROGRESS]

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]

    def get_ontology_summary(self) -> Dict[str, Any]:
        """Get summary of agent's ontological state"""
        return {
            "identity": {"name": self.identity.name, "type": self.identity.agent_type.value},
            "goals": {"active": len(self.goals), "completed": len(self.goals)},
            "tasks": {
                "active": len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
                "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            },
            "last_updated": self.last_updated.isoformat(),
        }
