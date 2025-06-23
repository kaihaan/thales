""" Open AI Client Adapter """

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionToolParam, ChatCompletionToolChoiceOptionParam
from thales.llm.client.base import LLMClient, LLMResponse, LLMError, T
from typing import Type, Optional, cast
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel 
from thales.utils import get_logger 

logger = get_logger(__name__) # Initialize logger
load_dotenv()  # loads from .env by default

api_key = os.environ.get("OPENAI_API_KEY")

class OpenAIClient(LLMClient):
    """ OpenAI Client Adapter Class """
    def __init__(self, model: str = "gpt-4"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_text(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> LLMResponse:
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            res = completion.choices[0].message.content
            if res is None:
                res = ""
            return LLMResponse(content=[res], metadata={"model": self.model})
        
        except Exception as e:
            return LLMResponse(content=[], error=LLMError(message=str(e)))

    async def get_model_list(self) -> LLMResponse:
        try:
            models = await self.client.models.list()
            model_names = [model.id for model in models.data]
            return LLMResponse(content=model_names)
        
        except Exception as e:
            return LLMResponse(content=[], error=LLMError(message=str(e)))

    async def generate_structured_output(self, prompt: str, output_type: Type[T], max_tokens: int = 500, temperature: float = 0.7) -> Optional[T]:

        # Ensure the output_type is a Pydantic BaseModel
        if not issubclass(output_type, BaseModel):
            logger.error(f"Output type {output_type.__name__} must be a Pydantic BaseModel for structured output.")
            raise ValueError("output_type must be a Pydantic BaseModel.")

        # Generate JSON schema from the Pydantic model
        # Pydantic v2 uses model_json_schema()
        tool_parameters = output_type.model_json_schema()

        tool_schema: ChatCompletionToolParam  = {
            "type": "function",
            "function": {
                "name": "return_structured_data",
                "description": f"Returns data structured as a {output_type.__name__} object.",
                "parameters": tool_parameters,
            },
        }


        # Explicitly type the tool_choice using ChatCompletionToolChoiceParam
        tool_choice: ChatCompletionToolChoiceOptionParam  = {"type": "function", "function": {"name": "return_structured_data"}}


        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ],
                tools=[tool_schema],
                tool_choice={"type": "function", "function": {"name": "return_structured_data"}},
                max_tokens=max_tokens,
                temperature=temperature,
                # response_format={"type": "json_object"} # This is not needed when using tool_choice
            )

            tool_calls = response.choices[0].message.tool_calls
            if tool_calls and tool_calls[0].function.name == "return_structured_data":
                json_output = json.loads(tool_calls[0].function.arguments)
                # Use Pydantic's parse_obj or model_validate for robust parsing
                return cast(T, output_type.model_validate(json_output)) # For Pydantic v2+
            else:
                logger.warning("LLM did not return structured data as expected.")
                return None

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating structured output: {e}")
            return None