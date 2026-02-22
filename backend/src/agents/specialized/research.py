"""Research Agent Implementation"""

import json
from typing import Dict, Any, List

from src.agents.base.agent import BaseAgent
from src.agents.base.state import DecisionState
from src.config.settings import settings
from src.config.constants import AgentName
from src.llm.prompts.research import research_prompt


class ResearchAgent(BaseAgent):
    """Agent responsible for market research and data synthesis"""
    
    def __init__(self):
        super().__init__(
            name=AgentName.RESEARCH,
            model_name=settings.research_model,
            temperature=0.0
        )
        self.chain = research_prompt | self.llm

    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Execute research logic"""
        query = state["query"]
        
        # 1. Retrieve documents (if not already retrieved or if we need specific research docs)
        # For simplicity, we assume the supervisor or a previous step might have triggered retrieval,
        # but the research agent should probably ensure it has relevant docs.
        # Here we'll perform a fresh retrieval for the specific research context.
        
        filters = None
        if state.get("classification"):
             # Optional: Add filters based on classification entities
             pass
             
        docs = await self.retriever.retrieve(query, filters=filters)
        
        # Format documents for prompt
        doc_context = "\n\n".join([
            f"Source: {d.get('metadata', {}).get('source', 'Unknown')}\nContent: {d.get('text', '')}"
            for d in docs
        ])
        
        # 2. Analyze with LLM
        response = await self.chain.ainvoke({
            "query": query,
            "documents": doc_context[:50000] # Truncate to avoid context limit (approx 12k tokens)
        })
        
        # 3. Parse Output
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(content)
        except Exception as e:
            self.logger.error(f"Failed to parse research JSON: {e}")
            analysis = {
                "market_overview": "Failed to generate analysis.",
                "key_statistics": [],
                "trends": [],
                "data_gaps": ["Error processing results"]
            }

        # 4. Create Trace
        trace = self.log_trace(
            action="market_research",
            details={
                "documents_found": len(docs),
                "stats_extracted": len(analysis.get("key_statistics", [])),
                "trends_identified": len(analysis.get("trends", []))
            }
        )
        
        return {
            "agent_results": {AgentName.RESEARCH: analysis},
            "retrieved_docs": docs,
            "reasoning_trace": [trace]
        }


# Global research agent
research_agent = ResearchAgent()
