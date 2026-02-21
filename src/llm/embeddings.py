"""Embedding service interface"""

from typing import List
from langchain_openai import OpenAIEmbeddings
from src.config.settings import settings
from src.observability.logger import get_logger

logger = get_logger("embeddings")


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
            dimensions=settings.embedding_dimension
        )
        logger.info(f"Initialized embeddings with model: {settings.embedding_model}")

    async def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query string"""
        try:
            return await self.embeddings.aembed_query(text)
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents"""
        try:
            return await self.embeddings.aembed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating document embeddings: {e}")
            raise


# Global embedding service
embedding_service = EmbeddingService()
