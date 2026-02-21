"""Seed data for the showcase"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.vector_search import vector_search
from src.retrieval.bm25_search import bm25_search
from src.observability.logger import get_logger

logger = get_logger("seed_data")

# Sample documents allowing us to test "Should we expand to UAE?" query
SAMPLE_DOCUMENTS = [
    {
        "text": "The UAE software market is projected to grow at 12% CAGR through 2028, driven by government digitization initiatives like Vision 2030.",
        "metadata": {"source": "Market Report 2025", "category": "market", "date": "2025-01-10"}
    },
    {
        "text": "Dubai Internet City offers 100% foreign ownership and 50-year tax exemption for tech companies.",
        "metadata": {"source": "Government Portal", "category": "policy", "date": "2024-12-01"}
    },
    {
        "text": "Operating costs in Dubai are 40% higher than Bangalore, with average office rent at $50/sqft.",
        "metadata": {"source": "Real Estate Index", "category": "financial", "date": "2025-02-01"}
    },
    {
        "text": "New data privacy laws in UAE (PDPL) require strict data localization for financial data.",
        "metadata": {"source": "Legal Brief", "category": "regulatory", "date": "2024-11-15"}
    },
    {
        "text": "Cloud adoption in the GCC region is lagging behind Europe but accelerating due to AWS and Azure local regions.",
        "metadata": {"source": "Tech Trends", "category": "technology", "date": "2025-01-20"}
    },
    {
        "text": "There is a shortage of senior AI engineers in the MENA region, driving up salaries by 25% YoY.",
        "metadata": {"source": "HR Annual Report", "category": "operational", "date": "2025-01-05"}
    }
]

async def seed_data():
    """Seed the vector database and BM25 index"""
    logger.info("Starting data seeding...")
    
    # 1. Setup Qdrant
    await vector_search.ensure_collection()
    
    # 2. Add Documents to Qdrant
    logger.info(f"Adding {len(SAMPLE_DOCUMENTS)} documents to Vector DB...")
    await vector_search.add_documents(SAMPLE_DOCUMENTS)
    
    # 3. Fit BM25 (In memory - for this script only, normally handled by a service)
    # Note: In a real app, BM25 index needs to be persisted or rebuilt on startup.
    # For this MVP showcase script, we just show it works.
    bm25_search.fit(SAMPLE_DOCUMENTS)
    logger.info("BM25 index built.")
    
    logger.info("✅ Data seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
