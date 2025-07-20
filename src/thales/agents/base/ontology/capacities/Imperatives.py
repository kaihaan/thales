"""
AI Agent Behavior Choices (Imperatives)
"""

from uuid import UUID, uuid4
from dataclasses import dataclass, field

@dataclass
class Imperatives:
    """defines imperative instructions for an AI Agent
    tags to assist with autonomous searching"""
    interactive: bool = False
    reflection_prompts: list[str] = field(default_factory=list)
