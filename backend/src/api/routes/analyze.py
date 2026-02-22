"""Analyze route implementation"""

import time
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from src.api.models.request import AnalyzeRequest
from src.api.models.response import AnalyzeResponse
from src.agents.supervisor import supervisor
from src.observability.logger import get_logger
from src.observability.metrics import metrics

router = APIRouter()
logger = get_logger("api.analyze")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_query(request: AnalyzeRequest):
    """
    Process a decision query through the multi-agent system.
    """
    start_time = time.time()
    metrics.request_count.labels(method="POST", endpoint="/analyze", status="200").inc()
    
    try:
        logger.info(f"Received query: {request.query[:50]}...")
        
        # Execute workflow
        result = await supervisor.execute(
            query=request.query,
            metadata={"source": "api", "options": request.options.model_dump()}
        )
        
        # Extract report
        report = result.get("final_report", {})
        if not report:
             # If report generation failed but we have partial data
             report = {}
        
        response = AnalyzeResponse(
            query=request.query,
            classification=result.get("classification"),
            executive_summary=report.get("executive_summary"),
            detailed_analysis=report.get("detailed_analysis"),
            risk_summary=report.get("risk_summary"),
            financial_overview=report.get("financial_overview"),
            recommendations=report.get("recommendations"),
            confidence_score=report.get("confidence_score"),
            reasoning_trace=result.get("reasoning_trace") if request.options.include_reasoning else None,
            metadata={
                "processing_time": time.time() - start_time,
                "agent_plan": result.get("workflow_plan"),
                **result.get("metadata", {})
            }
        )
        
        metrics.request_latency.labels(method="POST", endpoint="/analyze").observe(time.time() - start_time)
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        metrics.request_count.labels(method="POST", endpoint="/analyze", status="500").inc()
        raise HTTPException(status_code=500, detail=str(e))
