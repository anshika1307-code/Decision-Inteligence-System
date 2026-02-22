"""API Response Models"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Classification(BaseModel):
    primary_category: str
    confidence: float
    entities: Dict[str, Any]


class ReasonStep(BaseModel):
    agent: str
    action: str
    timestamp: float
    details: Dict[str, Any]


class AnalyzeResponse(BaseModel):
    """Response model for analysis endpoint"""
    query: str
    classification: Optional[Classification]
    executive_summary: Optional[str]
    detailed_analysis: Optional[Dict[str, Any]]
    risk_summary: Optional[str]
    financial_overview: Optional[str]
    recommendations: Optional[List[str]]
    confidence_score: Optional[float]
    reasoning_trace: Optional[List[ReasonStep]]
    metadata: Dict[str, Any]
    error: Optional[str] = None
