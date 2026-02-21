"""Financial Agent Implementation"""

import json
from typing import Dict, Any

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.financial import financial_prompt


class FinancialAgent(BaseAgent):
    """Agent responsible for financial projections"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.FINANCIAL,
            model_name=settings.financial_model,
            temperature=0.0
        )
        self.chain = financial_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute financial analysis logic"""
        query = state["query"]
        
        # Get context
        research_results = state.get("agent_results", {}).get(AgentName.RESEARCH, {})
        risk_results = state.get("agent_results", {}).get(AgentName.RISK, {})
        
        # Serialize context
        research_context = json.dumps(research_results, indent=2) if research_results else "No research data."
        risk_context = json.dumps(risk_results, indent=2) if risk_results else "No risk data."

        # Invoke LLM
        response = await self.chain.ainvoke({
            "query": query,
            "research_results": research_context[:20000],
            "risk_results": risk_context[:5000]
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
            self.logger.error(f"Failed to parse financial JSON: {e}")
            analysis = {
                "initial_investment": {},
                "revenue_projections": {},
                "error": "Failed to generate financial analysis"
            }

        # Create Trace
        trace = self.log_trace(
            action="financial_analysis",
            details={
                "roi_projected": analysis.get("roi_3_year"),
                "break_even": analysis.get("break_even_months")
            }
        )
        
        return {
            "agent_results": {AgentName.FINANCIAL: analysis},
            "reasoning_trace": [trace]
        }


# Global financial agent
financial_agent = FinancialAgent()
