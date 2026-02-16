"""API Request Models"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from src.config.constants import AnalysisDepth


class QueryOptions(BaseModel):
    """Configuration options for query analysis"""
    depth: AnalysisDepth = Field(default=AnalysisDepth.STANDARD, description="Depth of analysis")
    include_reasoning: bool = Field(default=True, description="Include detailed reasoning trace")
    max_sources: int = Field(default=20, ge=1, le=50, description="Maximum number of sources to retrieve")
    force_refresh: bool = Field(default=False, description="Bypass cache")


class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint"""
    query: str = Field(..., min_length=10, max_length=2000, description="The decision query")
    options: Optional[QueryOptions] = Field(default_factory=QueryOptions)

    @field_validator("query")
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()
