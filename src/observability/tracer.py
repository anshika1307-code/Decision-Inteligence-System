"""Tracing configuration using LangSmith"""

import os
from functools import wraps
from typing import Optional, Any
from langsmith import Client
from langsmith.run_helpers import traceable
from loguru import logger
from src.config.settings import settings


class Tracer:
    """LangSmith tracer wrapper"""
    
    def __init__(self):
        self.enabled = bool(settings.langsmith_api_key)
        self.client = None
        
        if self.enabled:
            try:
                self.client = Client(
                    api_key=settings.langsmith_api_key,
                    api_url=settings.langsmith_endpoint
                )
                logger.info(f"LangSmith tracing enabled for project: {settings.langsmith_project}")
            except Exception as e:
                logger.warning(f"Failed to initialize LangSmith client: {e}")
                self.enabled = False
    
    def trace_agent(self, name: str):
        """Decorator to trace agent execution"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.enabled:
                    return await func(*args, **kwargs)
                
                # Use LangSmith's @traceable if enabled
                # We prioritize using the official decorator functionality dynamically
                # or simplified manual wrapping if needed.
                # For this implementation, we use the standard @traceable behavior
                return await traceable(
                    run_type="chain",
                    name=name,
                    project_name=settings.langsmith_project
                )(func)(*args, **kwargs)
            return wrapper
        return decorator


# Global tracer instance
tracer = Tracer()
