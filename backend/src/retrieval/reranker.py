"""Reranking service implementation"""

from typing import List, Dict, Any, Optional

from src.config.settings import settings
from src.observability.logger import get_logger

logger = get_logger("reranker")

# Lazy import flag
_CROSS_ENCODER_AVAILABLE = None

def _check_cross_encoder() -> bool:
    """Check if sentence_transformers/torch is available (lazy check)."""
    global _CROSS_ENCODER_AVAILABLE
    if _CROSS_ENCODER_AVAILABLE is None:
        try:
            import torch  # noqa: F401
            from sentence_transformers import CrossEncoder  # noqa: F401
            _CROSS_ENCODER_AVAILABLE = True
        except ImportError:
            logger.warning(
                "torch/sentence_transformers not available (Python 3.14 not yet supported). "
                "Falling back to score-passthrough reranking. "
                "To enable local reranking, use Python 3.11 or set COHERE_API_KEY."
            )
            _CROSS_ENCODER_AVAILABLE = False
    return _CROSS_ENCODER_AVAILABLE


class RerankerService:
    """Service for reranking retrieved documents"""
    
    def __init__(self):
        self.use_cohere = bool(settings.cohere_api_key)
        self.cohere_client = None
        self._cross_encoder = None  # Lazy loaded
        
        if self.use_cohere:
            try:
                import cohere
                self.cohere_client = cohere.Client(settings.cohere_api_key)
                logger.info("Initialized Cohere Rerank API")
            except Exception as e:
                logger.warning(f"Failed to initialize Cohere client: {e}, falling back to local CrossEncoder")
                self.use_cohere = False
        
        if not self.use_cohere:
            if _check_cross_encoder():
                try:
                    from sentence_transformers import CrossEncoder
                    model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
                    logger.info(f"Loading local CrossEncoder model: {model_name}")
                    self._cross_encoder = CrossEncoder(model_name)
                    logger.info("Initialized local CrossEncoder")
                except Exception as e:
                    logger.warning(f"Failed to load CrossEncoder model: {e}. Using passthrough reranking.")
            else:
                logger.info("Using passthrough reranking (no torch/CrossEncoder available)")

    async def rerank(
        self, 
        query: str, 
        documents: List[Dict[str, Any]], 
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """Rerank a list of documents based on query relevance"""
        
        if not documents:
            return []
            
        try:
            if self.use_cohere and self.cohere_client:
                return await self._rerank_cohere(query, documents, top_n)
            elif self._cross_encoder:
                return await self._rerank_local(query, documents, top_n)
            else:
                # Passthrough: return top_n documents as-is (no reranking)
                return documents[:top_n]
                
        except Exception as e:
            logger.error(f"Error during reranking: {e}")
            return documents[:top_n]

    async def _rerank_cohere(
        self, 
        query: str, 
        documents: List[Dict[str, Any]], 
        top_n: int
    ) -> List[Dict[str, Any]]:
        """Rerank using Cohere API"""
        docs_text = [doc["text"] for doc in documents]
        
        results = self.cohere_client.rerank(
            query=query,
            documents=docs_text,
            top_n=top_n,
            model="rerank-english-v3.0"
        )
        
        reranked = []
        for hit in results.results:
            original_doc = documents[hit.index]
            original_doc["rerank_score"] = hit.relevance_score
            reranked.append(original_doc)
            
        return reranked

    async def _rerank_local(
        self, 
        query: str, 
        documents: List[Dict[str, Any]], 
        top_n: int
    ) -> List[Dict[str, Any]]:
        """Rerank using local CrossEncoder"""
        pairs = [[query, doc["text"]] for doc in documents]
        scores = self._cross_encoder.predict(pairs)
        
        for i, doc in enumerate(documents):
            doc["rerank_score"] = float(scores[i])
            
        sorted_docs = sorted(
            documents, 
            key=lambda x: x["rerank_score"], 
            reverse=True
        )
        
        return sorted_docs[:top_n]


# Global reranker service
reranker = RerankerService()
