"""Supervisor Agent (LangGraph Orchestrator)"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.agents.base.state import DecisionState
from src.agents.specialized.classifier import classifier_agent
from src.agents.specialized.research import research_agent
from src.agents.specialized.risk import risk_agent
from src.agents.specialized.financial import financial_agent
from src.agents.specialized.fact_check import fact_check_agent
from src.agents.specialized.summary import summary_agent
from src.config.constants import AgentName, QueryCategory
from src.observability.logger import get_logger

logger = get_logger("supervisor")


class SupervisorAgent:
    """Orchestrator for the multi-agent workflow"""
    
    def __init__(self):
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(DecisionState)
        
        # Add Nodes
        workflow.add_node("classify", self._classifier_node)
        workflow.add_node("plan", self._planner_node)
        workflow.add_node("research", self._research_node)
        workflow.add_node("risk", self._risk_node)
        workflow.add_node("financial", self._financial_node)
        workflow.add_node("fact_check", self._fact_check_node)
        workflow.add_node("summarize", self._summary_node)
        
        # Set Entry Point
        workflow.set_entry_point("classify")
        
        # Add Edges
        workflow.add_edge("classify", "plan")
        
        # Conditional Routing from Plan
        workflow.add_conditional_edges(
            "plan",
            self._route_parallel_agents,
            ["research", "risk", "financial"]
        )
        
        # Re-convergence logic
        # In LangGraph, parallel branches need to converge. 
        # We can make them all point to fact_check.
        workflow.add_edge("research", "fact_check")
        workflow.add_edge("risk", "fact_check")
        workflow.add_edge("financial", "fact_check")
        
        workflow.add_edge("fact_check", "summarize")
        workflow.add_edge("summarize", END)
        
        return workflow.compile()

    # Node wrappers
    async def _classifier_node(self, state: DecisionState) -> Dict[str, Any]:
        return await classifier_agent.execute(state)

    async def _planner_node(self, state: DecisionState) -> Dict[str, Any]:
        """Determine which agents to run based on classification"""
        classification = state.get("classification", {})
        category = classification.get("primary_category", "RESEARCH")
        
        plan = [AgentName.RESEARCH] # Always research
        
        if category in [QueryCategory.RISK, QueryCategory.MARKET, QueryCategory.COMPARISON]:
             plan.append(AgentName.RISK)
             
        if category in [QueryCategory.MARKET, QueryCategory.COMPARISON]:
             plan.append(AgentName.FINANCIAL)
             
        # Normalize plan
        plan = list(set(plan))
        logger.info(f"Planned workflow: {plan} for category {category}")
        
        return {"workflow_plan": plan}

    async def _research_node(self, state: DecisionState) -> Dict[str, Any]:
        return await research_agent.execute(state)

    async def _risk_node(self, state: DecisionState) -> Dict[str, Any]:
        return await risk_agent.execute(state)

    async def _financial_node(self, state: DecisionState) -> Dict[str, Any]:
        return await financial_agent.execute(state)

    async def _fact_check_node(self, state: DecisionState) -> Dict[str, Any]:
        return await fact_check_agent.execute(state)

    async def _summary_node(self, state: DecisionState) -> Dict[str, Any]:
        return await summary_agent.execute(state)

    # Routing logic
    def _route_parallel_agents(self, state: DecisionState) -> List[str]:
        """Route to parallel agents based on plan"""
        plan = state.get("workflow_plan", [])
        next_nodes = []
        
        if AgentName.RESEARCH in plan:
            next_nodes.append("research")
        if AgentName.RISK in plan:
            next_nodes.append("risk")
        if AgentName.FINANCIAL in plan:
            next_nodes.append("financial")
            
        return next_nodes

    async def execute(self, query: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the workflow for a given query"""
        initial_state = {
            "query": query,
            "classification": None,
            "workflow_plan": [],
            "agent_results": {},
            "retrieved_docs": [],
            "reasoning_trace": [],
            "final_report": None,
            "metadata": metadata or {},
            "next_step": None,
            "retry_count": 0
        }
        
        result = await self.workflow.ainvoke(initial_state)
        return result


# Global supervisor instance
supervisor = SupervisorAgent()
