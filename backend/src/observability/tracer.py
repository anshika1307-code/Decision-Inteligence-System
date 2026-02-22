"""Tracing configuration using LangSmith"""

import os
from functools import wraps
from loguru import logger
from src.config.settings import settings


def _is_real_key(key: str) -> bool:
    key = (key or "").strip()
    return bool(key) and "your" not in key.lower() and len(key) > 10


class Tracer:
    """LangSmith tracer wrapper"""

    def __init__(self):
        self.enabled = False
        self.client = None

        key = settings.langsmith_api_key or ""
        # Only enable if there's a real key AND tracing isn't explicitly disabled
        tracing_disabled = os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() == "false"

        if _is_real_key(key) and not tracing_disabled:
            self._try_init_langsmith(key)
        else:
            logger.info("LangSmith tracing disabled")

    def _try_init_langsmith(self, key: str):
        """Lazy-import and initialise LangSmith client."""
        try:
            from langsmith import Client  # lazy import avoids network hang on Python 3.14
            self.client = Client(
                api_key=key,
                api_url=settings.langsmith_endpoint,
            )
            self.enabled = True
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
                try:
                    from langsmith.run_helpers import traceable  # lazy
                    return await traceable(
                        run_type="chain",
                        name=name,
                        project_name=settings.langsmith_project,
                    )(func)(*args, **kwargs)
                except Exception:
                    return await func(*args, **kwargs)
            return wrapper
        return decorator


# Global tracer instance
tracer = Tracer()
