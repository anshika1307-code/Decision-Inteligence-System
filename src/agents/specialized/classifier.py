"""Query Classifier Agent"""

import json
from typing import Dict, Any

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.classifier import classifier_prompt


class ClassifierAgent(BaseAgent):
    """Agent responsible for classifying queries and extracting entities"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.CLASSIFIER,
            model_name=settings.classifier_model,  # Uses gpt-4o-mini (cheap)
            temperature=0.0
        )
        self.chain = classifier_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute classification logic using LLM"""
        query = state["query"]
        
        # Invoke LLM
        response = await self.chain.ainvoke({"query": query})
        
        # Parse JSON output
        try:
            content = response.content
            # Clean up markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            classification = json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse classification JSON: {response.content}")
            # Fallback
            classification = {
                "primary_category": "RESEARCH",
                "confidence": 0.5,
                "depth": "STANDARD",
                "entities": {},
                "reasoning": "JSON parse error, fallback to default"
            }

        # Create trace
        trace = self.log_trace(
            action="classify_query",
            details={
                "category": classification.get("primary_category"),
                "confidence": classification.get("confidence"),
                "entities": classification.get("entities")
            }
        )
        
        return {
            "classification": classification,
            "reasoning_trace": [trace]
        }


# Global classifier instance
classifier_agent = ClassifierAgent()
