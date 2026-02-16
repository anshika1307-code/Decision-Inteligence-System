"""LLM Factory for model instantiation"""

from typing import Union
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.config.settings import settings
from src.config.constants import MODEL_COSTS

class LLMFactory:
    """Factory to create LLM instances based on configuration"""

    @staticmethod
    def create(model_name: str, temperature: float = 0.0) -> Union[ChatOpenAI, ChatAnthropic]:
        """Create an LLM instance"""
        
        if "gpt" in model_name:
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=settings.openai_api_key
            )
        elif "claude" in model_name:
            if not settings.anthropic_api_key:
                # Fallback to GPT-4o-mini if Anthropic key is missing
                return ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=temperature,
                    openai_api_key=settings.openai_api_key
                )
            return ChatAnthropic(
                model=model_name,
                temperature=temperature,
                anthropic_api_key=settings.anthropic_api_key
            )
        else:
            # Default fallback
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=temperature,
                openai_api_key=settings.openai_api_key
            )

    @staticmethod
    def get_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate estimated cost for a request"""
        rates = MODEL_COSTS.get(model_name)
        if not rates:
            # Fallback to GPT-4o-mini rates if unknown
            rates = MODEL_COSTS["gpt-4o-mini"]
            
        input_cost = (input_tokens / 1_000_000) * rates["input"]
        output_cost = (output_tokens / 1_000_000) * rates["output"]
        
        return input_cost + output_cost

# Global factory instance
llm_factory = LLMFactory()
