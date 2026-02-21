"""Fact-Check Agent Implementation"""

import json
from typing import Dict, Any

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.fact_check import fact_check_prompt


class FactCheckAgent(BaseAgent):
    """Agent responsible for validating claims"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.FACT_CHECK,
            model_name=settings.fact_check_model, # Uses Claude (or strong model)
            temperature=0.0
        )
        self.chain = fact_check_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute fact checking logic"""
        # Gather outputs from all previous agents
        agent_results = state.get("agent_results", {})
        
        # Gather retrieved docs
        docs = state.get("retrieved_docs", [])
        doc_context = "\n\n".join([
            f"[{i}] {d.get('text', '')[:1000]}..." 
            for i, d in enumerate(docs)
        ])
        
        # Serialize agent outputs
        outputs_context = json.dumps(agent_results, indent=2)

        # Invoke LLM
        response = await self.chain.ainvoke({
            "agent_outputs": outputs_context[:30000], # Truncate to fit context
            "documents": doc_context[:40000]
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
            self.logger.error(f"Failed to parse fact-check JSON: {e}")
            analysis = {
                "verified_claims": [],
                "contradictions": [],
                "verification_score": 0.0,
                "error": "Failed to parse verification results"
            }

        # Create Trace
        trace = self.log_trace(
            action="fact_check",
            details={
                "verified_count": len(analysis.get("verified_claims", [])),
                "contradictions": len(analysis.get("contradictions", [])),
                "score": analysis.get("verification_score")
            }
        )
        
        return {
            "agent_results": {AgentName.FACT_CHECK: analysis},
            "reasoning_trace": [trace]
        }


# Global fact-check agent
fact_check_agent = FactCheckAgent()
