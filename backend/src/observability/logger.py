"""Logging configuration using Loguru"""

import sys
from loguru import logger
from src.config.settings import settings


def setup_logging():
    """Configure loguru logger"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File handler with rotation
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level=settings.log_level,
        serialize=settings.log_format == "json",
    )
    
    return logger


def get_logger(name: str):
    """Get a logger instance for a module"""
    return logger.bind(name=name)
