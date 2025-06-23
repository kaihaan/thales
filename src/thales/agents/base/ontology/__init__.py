"""Agent Ontology Package"""

from .identity import AgentIdentity, AgentType, CommunicationStyle, DecisionStyle
from .goalsClasses import Goal, GoalType, GoalStatus, TimeConstraint
from .tasksClasses import Task, TaskType, TaskStatus, RetryPolicy
from .ontology import AgentOntology

__all__ = [
    # Identity
    "AgentIdentity",
    "AgentType", 
    "CommunicationStyle",
    "DecisionStyle",
    
    # Goals
    "Goal",
    "GoalType",
    "GoalStatus", 
    "TimeConstraint",
    
    # Tasks
    "Task",
    "TaskType",
    "TaskStatus",
    "RetryPolicy",
    
    # Main ontology
    "AgentOntology",
]
