"""Enhanced Goal System for Agent Ontology"""

from dataclasses import dataclass, field
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class GoalType(Enum):
    ACHIEVEMENT = "achievement"      # Accomplish something
    MAINTENANCE = "maintenance"      # Keep something running
    AVOIDANCE = "avoidance"         # Prevent something
    EXPLORATION = "exploration"      # Discover/learn something

class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

@dataclass
class TimeConstraint:
    """Time-based constraints for goals"""
    deadline: Optional[datetime] = None
    estimated_duration: Optional[timedelta] = None
    max_duration: Optional[timedelta] = None
    preferred_start_time: Optional[datetime] = None

@dataclass
class Goal:
    """Enhanced goal with full ontological context"""
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    goal_type: GoalType = GoalType.ACHIEVEMENT
    priority: int = 5  # 0 (highest) to 10 (lowest)
            
    time_constraints: Optional[TimeConstraint] = None
    
    # Lifecycle tracking
    status: GoalStatus = GoalStatus.PENDING
    progress: float = 0.0  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Learning and adaptation
    attempts: int = 0
    failure_reasons: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    
    
    def is_overdue(self) -> bool:
        """Check if goal is overdue"""
        if not self.time_constraints or not self.time_constraints.deadline:
            return False
        return datetime.now() > self.time_constraints.deadline
    

