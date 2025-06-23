""" Anthropic LLM Adapter """

# from typing import Dict, Any
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock, ToolUseBlock, ServerToolUseBlock,  WebSearchToolResultBlock, ThinkingBlock, RedactedThinkingBlock
from thales.llm.client.base import LLMClient, LLMResponse, LLMError

class AnthropicClient(LLMClient):
    """ Anthropic LLM Adapter Class """
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    async def generate_text(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> LLMResponse:
        try:
            completion = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            res = ""
            if completion.content and len(completion.content) > 0:
                block = completion.content[0]
                match block:
                    case TextBlock(text=text):
                        # textblock
                        res = text
                    case ToolUseBlock():
                        # It's a ToolUseBlock, handle it accordingly
                        res = "" # or some other default value or handling
                    case ServerToolUseBlock():
                        # It's a ServerToolUseBlock, handle it accordingly
                        res = "" # or some other default value or handling
                    case WebSearchToolResultBlock():
                        # It's a WebSearchToolResultBlock, handle it accordingly
                        res = "" # or some other default value or handling
                    case ThinkingBlock():
                        # It's a ThinkingBlock, handle it accordingly
                        res = "" # or some other default value or handling
                    case RedactedThinkingBlock():
                        # It's a RedactedThinkingBlock, handle it accordingly
                        res = "" # or some other default value or handling
                    case _:
                        # It's an unknown type, handle it accordingly
                        res = "" # or some other default value or handling

            return LLMResponse(content=[res], metadata={"model": self.model})
        
        except Exception as e:
            return LLMResponse(content=[], error=LLMError(message=str(e)))

    async def get_model_list(self) -> LLMResponse:
        try:
            models = await self.client.models.list()
            model_names = [model.display_name for model in models.data if hasattr(model, 'display_name')]
            return LLMResponse(content=model_names)
        
        except Exception as e:
            return LLMResponse(content=[], error=LLMError(message=str(e)))
