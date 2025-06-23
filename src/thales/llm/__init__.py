"""
LLM Abstraction Layer for Thales Agent Framework
Provides unified interface for multiple LLM providers
"""

from .client.base import LLMClient, LLMResponse, LLMError
from .client.openai_client import OpenAIClient
from .prompts.goal_decomposition import GoalDecompositionPrompts

__all__ = [
    "LLMClient",
    "LLMResponse", 
    "LLMError",
    "OpenAIClient",
    "GoalDecompositionPrompts"
]
