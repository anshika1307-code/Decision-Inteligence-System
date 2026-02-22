"""Logging Middleware"""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.observability.logger import get_logger

logger = get_logger("middleware.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown"
            }
        )
        
        try:
            response = await call_next(request)
            
            duration = time.time() - start_time
            logger.info(
                f"Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2)
                }
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2)
                }
            )
            raise
