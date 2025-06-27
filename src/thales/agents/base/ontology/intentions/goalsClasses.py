"""Enhanced Goal System for Agent Ontology"""

from dataclasses import dataclass, field
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
    goal_id: str
    description: str
    goal_type: GoalType = GoalType.ACHIEVEMENT
    priority: int = 1  # 1 (highest) to 10 (lowest)
    urgency: int = 5   # 1 (low) to 10 (critical)
    
    # Goal relationships
    parent_goal: Optional[str] = None
    sub_goals: List[str] = field(default_factory=list)
    related_goals: List[str] = field(default_factory=list)
    
    # Success criteria
    success_criteria: List[str] = field(default_factory=list)
    success_metrics: Dict[str, Any] = field(default_factory=dict)
    completion_threshold: float = 1.0  # 0.0 to 1.0
    
    # Context and constraints
    context_requirements: Dict[str, Any] = field(default_factory=dict)
    resource_requirements: List[str] = field(default_factory=list)
    time_constraints: Optional[TimeConstraint] = None
    dependencies: List[str] = field(default_factory=list)
    
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
    
    def update_progress(self, progress: float, notes: str = "") -> None:
        """Update goal progress"""
        self.progress = max(0.0, min(1.0, progress))
        self.updated_at = datetime.now()
        if notes:
            self.lessons_learned.append(f"{datetime.now()}: {notes}")
        
        # Auto-complete if threshold reached
        if self.progress >= self.completion_threshold:
            self.status = GoalStatus.COMPLETED
            self.completed_at = datetime.now()
    
    def add_failure_reason(self, reason: str) -> None:
        """Record failure reason"""
        self.failure_reasons.append(f"{datetime.now()}: {reason}")
        self.attempts += 1
    
    def is_overdue(self) -> bool:
        """Check if goal is overdue"""
        if not self.time_constraints or not self.time_constraints.deadline:
            return False
        return datetime.now() > self.time_constraints.deadline
    
    def get_priority_score(self) -> float:
        """Calculate combined priority score"""
        # Combine priority and urgency (lower priority number = higher importance)
        priority_score = (11 - self.priority) / 10.0  # Invert and normalize
        urgency_score = self.urgency / 10.0
        return (priority_score + urgency_score) / 2.0
