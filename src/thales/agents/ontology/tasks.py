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
    
    # Task relationships
    parent_goal: str = ""
    parent_task: Optional[str] = None
    sub_tasks: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # Execution requirements
    required_capabilities: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    required_knowledge: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Quality and validation
    validation_criteria: List[str] = field(default_factory=list)
    quality_threshold: float = 0.8
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    
    # Results and feedback
    result: Optional[Any] = None
    confidence: float = 0.0
    quality_score: float = 0.0
    feedback: List[str] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    
    # Lifecycle tracking
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[timedelta] = None
    
    # Execution tracking
    attempts: int = 0
    max_attempts: int = 3
    last_error: Optional[str] = None
    
    def start_execution(self):
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.attempts += 1
    
    def complete_task(self, result: Any, confidence: float = 1.0, quality_score: float = 1.0):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        self.confidence = confidence
        self.quality_score = quality_score
        
        if self.started_at:
            self.duration = self.completed_at - self.started_at
    
    def fail_task(self, error_message: str):
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.last_error = error_message
        self.error_messages.append(f"{datetime.now()}: {error_message}")
        
        if self.started_at:
            self.duration = datetime.now() - self.started_at
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.attempts < self.max_attempts and self.status == TaskStatus.FAILED
    
    def add_feedback(self, feedback: str):
        """Add feedback to task"""
        self.feedback.append(f"{datetime.now()}: {feedback}")
    
    def meets_quality_threshold(self) -> bool:
        """Check if task meets quality requirements"""
        return self.quality_score >= self.quality_threshold
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of task execution"""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "attempts": self.attempts,
            "duration": str(self.duration) if self.duration else None,
            "confidence": self.confidence,
            "quality_score": self.quality_score,
            "success": self.status == TaskStatus.COMPLETED
        }
