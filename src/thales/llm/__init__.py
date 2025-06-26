"""
LLM Abstraction Layer for Thales Agent Framework
Provides unified interface for multiple LLM providers
"""

from .client.base import LLMClient, LLMResponse, LLMError
from .client.openai_client import OpenAIClient
from .client.anthropic_client import AnthropicClient
from .prompts.goal_decomposition import GoalDecompositionPrompts
from .models import DecomposedTasks

__all__ = [
    "LLMClient",
    "LLMResponse",
    "LLMError",
    "OpenAIClient",
    "AnthropicClient",
    "GoalDecompositionPrompts",
    "DecomposedTasks"
]
