# src/thales/llm/prompts/goal_decomposition.py
import json
from thales.llm.models import DecomposedTasks # Import the Pydantic model
from thales.agents.base.ontology.tasksClasses import TaskType

class GoalDecompositionPrompts:
    def __init__(self) -> None:
        pass

    def get_prompt(self, goal: str) -> str:
        # Dynamically get the JSON schema from the Pydantic model
        schema = json.dumps(DecomposedTasks.model_json_schema(), indent=2)

        return f"""
        Decompose the following high-level goal into a list of atomic, actionable tasks.
        Each task should be a JSON object with 'action', 'description', and 'task_type' fields.
        The 'action' should be a concise verb phrase.
        The 'description' should provide enough detail for another agent to understand and execute the task.
        The 'task_type' should be one of the following: {", ".join([t.value for t in TaskType])}.
        If not specified, default 'task_type' to 'execution'.

        Return the response as a JSON object matching the following schema:
        {schema}

        Goal: {goal}

        JSON Response:
        """
