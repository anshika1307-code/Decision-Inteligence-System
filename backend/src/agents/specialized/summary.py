"""Summary Agent Implementation"""

import json
from typing import Dict, Any

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.summary import summary_prompt


class SummaryAgent(BaseAgent):
    """Agent responsible for generating final report"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.SUMMARY,
            model_name=settings.summary_model,
            temperature=0.0
        )
        self.chain = summary_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute summary generation logic"""
        query = state["query"]
        agent_results = state.get("agent_results", {})
        
        # Serialize results
        results_context = json.dumps(agent_results, indent=2)

        # Invoke LLM
        response = await self.chain.ainvoke({
            "query": query,
            "agent_results": results_context[:50000] # Truncate if necessary
        })
        
        # Parse Output
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            report = json.loads(content)
        except Exception as e:
            self.logger.error(f"Failed to parse summary JSON: {e}")
            report = {
                "executive_summary": "Failed to generate report.",
                "detailed_analysis": {},
                "recommendations": [],
                "error": str(e)
            }

        # Create Trace
        trace = self.log_trace(
            action="generate_report",
            details={
                "recommendations_count": len(report.get("recommendations", [])),
                "confidence": report.get("confidence_score")
            }
        )
        
        return {
            "final_report": report,
            "reasoning_trace": [trace]
        }


# Global summary agent
summary_agent = SummaryAgent()
