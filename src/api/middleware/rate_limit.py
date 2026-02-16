"""Rate Limiting Middleware"""

import time
import redis
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.config.settings import settings
from src.observability.logger import get_logger

logger = get_logger("middleware.ratelimit")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Redis-backed Rate Limiting Middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.enabled = bool(settings.redis_host)
        self.redis = None
        
        if self.enabled:
            try:
                self.redis = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    password=settings.redis_password,
                    db=settings.redis_db,
                    decode_responses=True
                )
            except Exception as e:
                logger.warning(f"Failed to connect to Redis for rate limiting: {e}")
                self.enabled = False

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)
            
        # Skip rate limit for non-API endpoints
        if not request.url.path.startswith("/api/v1"):
            return await call_next(request)

        user_id = getattr(request.state, "user_id", "anonymous")
        key = f"ratelimit:{user_id}"
        
        try:
            # Simple window counter
            current = self.redis.get(key)
            
            if current and int(current) >= settings.rate_limit_per_user:
                logger.warning(f"Rate limit exceeded for user: {user_id}")
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )
                
            pipe = self.redis.pipeline()
            pipe.incr(key)
            if not current:
                pipe.expire(key, 3600)  # 1 hour window
            pipe.execute()
            
        except Exception as e:
            # Fail open if Redis is down
            logger.error(f"Rate limiting error: {e}")

        return await call_next(request)
