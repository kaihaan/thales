# src/thales/llm/models.py
from pydantic import BaseModel, Field
from typing import List
from thales.agents.base.ontology.intentions.tasksClasses import TaskType # Import TaskType

class TaskOutput(BaseModel):
    """Pydantic model for a single decomposed task from LLM."""
    action: str = Field(..., description="A concise verb phrase describing the task action.")
    description: str = Field(..., description="A detailed description of the task.")
    task_type: TaskType = Field(TaskType.EXECUTION, description="The type of task (e.g., INFORMATION_GATHERING, EXECUTION). Defaults to EXECUTION.")

class DecomposedTasks(BaseModel):
    """Pydantic model for a list of decomposed tasks from LLM."""
    tasks: List[TaskOutput] = Field(..., description="A list of decomposed tasks.")
