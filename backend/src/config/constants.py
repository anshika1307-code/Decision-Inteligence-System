"""Application constants"""

from enum import Enum


class QueryCategory(str, Enum):
    """Query classification categories"""
    RESEARCH = "research"
    POLICY = "policy"
    MARKET = "market"
    RISK = "risk"
    COMPARISON = "comparison"
    GENERIC = "generic"


class AnalysisDepth(str, Enum):
    """Analysis depth levels"""
    QUICK = "quick"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class AgentName(str, Enum):
    """Agent identifiers"""
    CLASSIFIER = "classifier"
    RESEARCH = "research"
    RISK = "risk"
    FINANCIAL = "financial"
    FACT_CHECK = "fact_check"
    SUMMARY = "summary"
    SUPERVISOR = "supervisor"


class RiskSeverity(str, Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class VerificationStatus(str, Enum):
    """Fact-check verification status"""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    CONTRADICTED = "contradicted"


# Retrieval Constants
DEFAULT_TOP_K = 20
DEFAULT_RERANK_N = 10
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# Model Costs (per 1M tokens)
MODEL_COSTS = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
}

# Agent Timeout (seconds)
AGENT_TIMEOUT = 60
RETRIEVAL_TIMEOUT = 10

# Cache TTL (seconds)
CACHE_TTL = 86400  # 24 hours
