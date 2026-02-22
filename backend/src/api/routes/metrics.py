"""Metrics Route"""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from src.observability.metrics import metrics

router = APIRouter()

@router.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    """Expose Prometheus metrics"""
    return metrics.get_latest()
