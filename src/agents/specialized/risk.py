"""Risk Agent Implementation"""

import json
from typing import Dict, Any

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.risk import risk_prompt


class RiskAgent(BaseAgent):
    """Agent responsible for risk assessment"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.RISK,
            model_name=settings.risk_model,
            temperature=0.0
        )
        self.chain = risk_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute risk analysis logic"""
        query = state["query"]
        
        # Get research results from state
        # The Research Agent should have ideally run before this
        research_results = state.get("agent_results", {}).get(AgentName.RESEARCH, {})
        
        # If no research results, we might need to do a quick retrieval or fail
        if not research_results:
             self.logger.warning("No research results found for Risk Agent. Running purely on internal knowledge.")
             research_context = "No specific research documents provided."
        else:
             research_context = json.dumps(research_results, indent=2)

        # Invoke LLM
        response = await self.chain.ainvoke({
            "query": query,
            "research_results": research_context
        })
        
        # Parse Output
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            analysis = json.loads(content)
        except Exception as e:
            self.logger.error(f"Failed to parse risk JSON: {e}")
            analysis = {
                "risks": [],
                "overall_risk_score": 0.0,
                "summary": "Failed to generate risk analysis."
            }

        # Create Trace
        trace = self.log_trace(
            action="risk_assessment",
            details={
                "risks_identified": len(analysis.get("risks", [])),
                "risk_score": analysis.get("overall_risk_score")
            }
        )
        
        return {
            "agent_results": {AgentName.RISK: analysis},
            "reasoning_trace": [trace]
        }


# Global risk agent
risk_agent = RiskAgent()
