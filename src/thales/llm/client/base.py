"""
Abstract class definitions for LLM interface
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Type
from dataclasses import dataclass

# Define a TypeVar for the dataclass type
T = TypeVar('T')

@dataclass
class LLMError:
    """ LLM Error response """
    message: str

@dataclass
class LLMResponse:
    """ LLM response """
    content: List[str]
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[LLMError] = None
    cost: Optional[float] = None
    tokens: Optional[int] = None

class LLMClient(ABC):
    """ LLM Client """
    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> LLMResponse:
        """
        Generates text based on the given prompt.
        """
        pass

    @abstractmethod
    async def get_model_list(self) -> LLMResponse:
        """
        Returns a list of available models.
        """
        pass

    @abstractmethod
    async def generate_structured_output(self, prompt: str, output_type: Type[T], max_tokens: int = 500, temperature: float = 0.7) -> Optional[T]:
        """
        Generates structured output (JSON) based on the given prompt and parses it into the specified dataclass type.

        Args:
            prompt (str): The prompt to send to the LLM, instructing it to return JSON.
            output_type (Type[T]): The dataclass type to parse the JSON response into.
            max_tokens (int): The maximum number of tokens to generate.
            temperature (float): The sampling temperature for generation.

        Returns:
            Optional[T]: An instance of the output_type dataclass if successful, otherwise None.
        """
        pass