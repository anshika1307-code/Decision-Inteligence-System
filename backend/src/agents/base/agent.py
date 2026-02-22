"""Base agent implementation"""

from abc import ABC, abstractmethod
import time
from typing import Dict, Any, Optional

from src.agents.base.state import DecisionState
from src.retrieval.hybrid_retriever import hybrid_retriever
from src.llm.factory import llm_factory
from src.observability.logger import get_logger
from src.observability.tracer import tracer
from src.observability.metrics import metrics

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(
        self, 
        name: str, 
        model_name: str, 
        temperature: float = 0.0
    ):
        self.name = name
        self.logger = get_logger(name)
        self.llm = llm_factory.create(model_name, temperature)
        self.retriever = hybrid_retriever
        
    @tracer.trace_agent(name="agent_execution")
    async def execute(self, state: DecisionState) -> Dict[str, Any]:
        """
        Execute agent logic with monitoring and error handling.
        This wrapper handles metrics and logging.
        """
        start_time = time.time()
        try:
            self.logger.info(f"Starting execution for agent: {self.name}")
            
            result = await self._execute_impl(state)
            
            duration = time.time() - start_time
            metrics.agent_execution_time.labels(agent_name=self.name).observe(duration)
            
            self.logger.info(f"Agent {self.name} completed in {duration:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in agent {self.name}: {e}")
            metrics.agent_errors.labels(agent_name=self.name, error_type=type(e).__name__).inc()
            raise

    @abstractmethod
    async def _execute_impl(self, state: DecisionState) -> Dict[str, Any]:
        """Implementation of agent specific logic"""
        pass
    
    def log_trace(self, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Create a reasoning trace entry"""
        return {
            "agent": self.name,
            "timestamp": time.time(),
            "action": action,
            "details": details
        }
