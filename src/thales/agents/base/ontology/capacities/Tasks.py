"""Enhanced Task System for Agent Ontology"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class TaskType(Enum):
    INFORMATION_GATHERING = "information_gathering"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    EXECUTION = "execution"
    COMMUNICATION = "communication"
    VALIDATION = "validation"
    PLANNING = "planning"
    MONITORING = "monitoring"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class RetryPolicy:
    """Retry configuration for tasks"""

    max_retries: int = 3
    retry_delay: timedelta = field(default_factory=lambda: timedelta(seconds=1))
    backoff_multiplier: float = 2.0
    retry_on_failure_types: List[str] = field(default_factory=lambda: ["timeout", "connection_error"])


@dataclass
class Task:
    """Enhanced task with full execution context"""

    task_id: str
    action: str
    task_type: TaskType
    description: str = ""

    # Lifecycle tracking
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[timedelta] = None

    # Task relationships
    parent_goal: str = ""

    # Quality and validation
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)

    # Results and feedback
    result: Optional[Any] = None
    error_messages: List[str] = field(default_factory=list)

    # Tool tracking
    tool_used: Optional[str] = None

    # Learning and adaptation
    attempts: int = 0
    failure_reasons: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

    def start(self) -> None:
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.attempts += 1

    def mark_complete(self, result: Any) -> None:
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

        if self.started_at:
            self.duration = self.completed_at - self.started_at

    def mark_failed(self, error_message: str) -> None:
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.error_messages.append(f"{datetime.now()}: {error_message}")

        if self.started_at:
            self.duration = datetime.now() - self.started_at

    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.attempts < self.retry_policy.max_retries and self.status == TaskStatus.FAILED

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of task execution"""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "attempts": self.attempts,
            "duration": str(self.duration) if self.duration else None,
            "success": self.status == TaskStatus.COMPLETED,
        }
