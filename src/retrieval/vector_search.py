"""Qdrant vector search implementation"""

import sys
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

from src.config.settings import settings
from src.observability.logger import get_logger
from src.llm.embeddings import embedding_service

logger = get_logger("vector_search")


class VectorSearchProvider:
    """Qdrant vector database provider"""
    
    def __init__(self):
        self.client = AsyncQdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
            https=settings.qdrant_https,
            check_compatibility=False  # Suppress version mismatch warning
        )
        self.collection_name = settings.qdrant_collection
        
    async def ensure_collection(self):
        """Ensure the vector collection exists"""
        try:
            collections = await self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating Qdrant collection: {self.collection_name}")
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.embedding_dimension,
                        distance=Distance.COSINE
                    )
                )
                
                # Create payload indexes
                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.document_id",
                    field_schema="keyword"
                )
                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata.source",
                    field_schema="keyword"
                )
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")
            raise

    async def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector database"""
        try:
            texts = [doc["text"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            ids = [doc.get("id") for doc in documents]
            
            logger.info(f"Generating embeddings for {len(texts)} documents")
            embeddings = await embedding_service.embed_documents(texts)
            
            points = [
                models.PointStruct(
                    id=idx if not ids[i] else ids[i],
                    vector=embeddings[i],
                    payload={
                        "text": texts[i],
                        "metadata": metadatas[i]
                    }
                )
                for i, idx in enumerate(range(len(documents)))
            ]
            
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Successfully added {len(points)} documents to Qdrant")
            
        except Exception as e:
            logger.error(f"Error adding documents to Qdrant: {e}")
            raise

    async def search(
        self, 
        query: str, 
        top_k: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            logger.info(f"Searching for: {query}")
            query_vector = await embedding_service.embed_query(query)
            
            # Construct Qdrant filters if provided
            query_filter = None
            if filters:
                must_conditions = []
                for key, value in filters.items():
                    must_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )
                if must_conditions:
                    query_filter = models.Filter(must=must_conditions)
            
            # Use query_points (new API in qdrant-client >= 1.12)
            results = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=top_k
            )
            
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "text": hit.payload.get("text"),
                    "metadata": hit.payload.get("metadata")
                }
                for hit in results.points
            ]
            
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            raise

# Global vector search provider
vector_search = VectorSearchProvider()
