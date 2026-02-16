"""Main application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.api.routes import analyze, metrics
from src.api.middleware.auth import AuthMiddleware
from src.api.middleware.rate_limit import RateLimitMiddleware
from src.api.middleware.logging import RequestLoggingMiddleware
from src.observability.logger import setup_logging

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events"""
    logger.info("Starting up Decision Intelligence System...")
    # Initialize DB connections if needed here
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Multi-Agent Decision Intelligence System",
    description="Production-ready decision intelligence platform",
    version="0.1.0",
    lifespan=lifespan
)

# Middleware (Order matters!)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Observability"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app", 
        host=settings.api_host, 
        port=settings.api_port, 
        reload=True
    )
