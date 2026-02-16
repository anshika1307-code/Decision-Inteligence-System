"""Agent state definition"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator


class DecisionState(TypedDict):
    """
    LangGraph state for the decision intelligence workflow.
    
    Attributes:
        query: The original user query
        classification: Query classification results
        workflow_plan: List of agents to execute
        agent_results: Results from each agent execution
        retrieved_docs: Documents retrieved by agents
        reasoning_trace: Step-by-step reasoning log
        final_report: The final constructed report
        metadata: Execution metadata (time, cost, etc.)
    """
    query: str
    classification: Optional[Dict[str, Any]]
    workflow_plan: List[str]
    agent_results: Annotated[Dict[str, Any], operator.or_]  # Merge dicts
    retrieved_docs: Annotated[List[Dict[str, Any]], operator.add]  # Append lists
    reasoning_trace: Annotated[List[Dict[str, Any]], operator.add]  # Append lists
    final_report: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
    next_step: Optional[str]
    retry_count: int
