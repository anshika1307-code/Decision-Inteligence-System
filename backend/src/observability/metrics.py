"""Prometheus metrics configuration"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from src.config.constants import AgentName


class Metrics:
    """Application metrics"""
    
    def __init__(self):
        # Request metrics
        self.request_count = Counter(
            "request_total", 
            "Total number of API requests",
            ["method", "endpoint", "status"]
        )
        self.request_latency = Histogram(
            "request_latency_seconds",
            "API request latency",
            ["method", "endpoint"]
        )
        
        # Query metrics
        self.query_total = Counter(
            "query_total",
            "Total number of queries processed",
            ["category", "status"]
        )
        self.query_duration = Histogram(
            "query_duration_seconds",
            "End-to-end query processing duration"
        )
        self.query_cost = Histogram(
            "query_cost_usd",
            "Total cost per query in USD"
        )
        
        # Agent metrics
        self.agent_execution_time = Histogram(
            "agent_execution_seconds",
            "Agent execution time",
            ["agent_name"]
        )
        self.agent_errors = Counter(
            "agent_errors_total",
            "Total errors in agent execution",
            ["agent_name", "error_type"]
        )
        
        # Retrieval metrics
        self.retrieval_count = Counter(
            "retrieval_total",
            "Total number of retrieval operations"
        )
        self.cache_hits = Counter(
            "cache_hits_total",
            "Total number of cache hits"
        )
        self.documents_retrieved = Histogram(
            "documents_retrieved_count",
            "Number of documents retrieved per query"
        )
        
        # Evaluation metrics (Gauge as they are set per query)
        self.faithfulness_score = Gauge(
            "eval_faithfulness_score",
            "RAGAS faithfulness score (last query)"
        )
        self.relevancy_score = Gauge(
            "eval_relevancy_score",
            "RAGAS answer relevancy score (last query)"
        )
        
    def get_latest(self):
        """Get latest metrics in Prometheus format"""
        return generate_latest()


# Global metrics instance
metrics = Metrics()
