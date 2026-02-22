"""Configuration settings using Pydantic"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    
    # LLM Providers
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    cohere_api_key: str = Field(default="", env="COHERE_API_KEY")
    
    # Vector Database
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_api_key: str = Field(default="", env="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="decision_intelligence", env="QDRANT_COLLECTION")
    qdrant_https: bool = Field(default=False, env="QDRANT_HTTPS")
    
    # Cache
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: str = Field(default="", env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_cache_ttl: int = Field(default=86400, env="REDIS_CACHE_TTL")
    
    # Database
    database_url: str = Field(default="sqlite:///./decision_intelligence.db", env="DATABASE_URL")
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    
    # Observability
    langsmith_api_key: str = Field(default="", env="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="decision-intelligence", env="LANGSMITH_PROJECT")
    langsmith_endpoint: str = Field(default="https://api.smith.langchain.com", env="LANGSMITH_ENDPOINT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Security
    jwt_secret_key: str = Field(default="demo-secret-key-change-in-production", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    
    # Rate Limiting
    rate_limit_per_user: int = Field(default=100, env="RATE_LIMIT_PER_USER")
    rate_limit_window_hours: int = Field(default=1, env="RATE_LIMIT_WINDOW_HOURS")
    rate_limit_global: int = Field(default=1000, env="RATE_LIMIT_GLOBAL")
    
    # Retrieval Configuration
    embedding_model: str = Field(default="text-embedding-3-large", env="EMBEDDING_MODEL")
    embedding_dimension: int = Field(default=3072, env="EMBEDDING_DIMENSION")
    vector_top_k: int = Field(default=20, env="VECTOR_TOP_K")
    bm25_top_k: int = Field(default=20, env="BM25_TOP_K")
    rerank_top_n: int = Field(default=10, env="RERANK_TOP_N")
    enable_local_reranking: bool = Field(default=False, env="ENABLE_LOCAL_RERANKING")
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    
    # Agent Configuration
    classifier_model: str = Field(default="gpt-4o-mini", env="CLASSIFIER_MODEL")
    research_model: str = Field(default="gpt-4o", env="RESEARCH_MODEL")
    risk_model: str = Field(default="gpt-4o", env="RISK_MODEL")
    financial_model: str = Field(default="gpt-4o", env="FINANCIAL_MODEL")
    fact_check_model: str = Field(default="claude-3-5-sonnet-20241022", env="FACT_CHECK_MODEL")
    summary_model: str = Field(default="gpt-4o", env="SUMMARY_MODEL")
    
    # Evaluation
    ragas_enabled: bool = Field(default=True, env="RAGAS_ENABLED")
    ragas_sample_rate: float = Field(default=0.1, env="RAGAS_SAMPLE_RATE")
    
    # Cost Tracking
    cost_tracking_enabled: bool = Field(default=True, env="COST_TRACKING_ENABLED")
    cost_alert_threshold_usd: float = Field(default=10.0, env="COST_ALERT_THRESHOLD_USD")
    
    # Performance
    max_concurrent_agents: int = Field(default=5, env="MAX_CONCURRENT_AGENTS")
    agent_timeout_seconds: int = Field(default=60, env="AGENT_TIMEOUT_SECONDS")
    retrieval_timeout_seconds: int = Field(default=10, env="RETRIEVAL_TIMEOUT_SECONDS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore unknown env vars (e.g. LANGCHAIN_TRACING_V2)


# Global settings instance
settings = Settings()
