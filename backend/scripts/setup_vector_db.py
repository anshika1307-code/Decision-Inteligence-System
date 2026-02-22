"""Scripts to setup Qdrant vector database"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.vector_search import vector_search
from src.observability.logger import get_logger

logger = get_logger("setup_vector_db")


async def main():
    """Initialize Qdrant collection"""
    logger.info("Starting Qdrant setup...")
    try:
        await vector_search.ensure_collection()
        logger.info("✅ Qdrant collection setup complete")
    except Exception as e:
        logger.error(f"❌ Failed to setup Qdrant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
