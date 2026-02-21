"""Hybrid retrieval implementation with RRF"""

from typing import List, Dict, Any, Optional
from collections import defaultdict

from src.config.settings import settings
from src.observability.logger import get_logger
from src.observability.metrics import metrics
from src.retrieval.vector_search import vector_search
from src.retrieval.bm25_search import bm25_search
from src.retrieval.reranker import reranker

logger = get_logger("hybrid_retriever")


class HybridRetriever:
    """Hybrid retrieval engine combining Vector Search and BM25"""
    
    def __init__(self):
        self.vector_weight = 0.5
        self.bm25_weight = 0.5
        self.rrf_k = 60
        
    async def retrieve(
        self, 
        query: str, 
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = getattr(settings, 'vector_top_k', 20)
    ) -> List[Dict[str, Any]]:
        """
        Execute hybrid retrieval pipeline:
        1. Parallel Vector + BM25 search
        2. Reciprocal Rank Fusion (RRF)
        3. Metadata filtering (applied during search where possible)
        4. Reranking
        """
        try:
            logger.info(f"Executing hybrid retrieval for: {query}")
            metrics.retrieval_count.inc()
            
            # 1. Execute searches
            # Note: We await sequentially here for simplicity, 
            # in full async production we'd use asyncio.gather
            vector_results = await vector_search.search(
                query, top_k=top_k, filters=filters
            )
            
            try:
                bm25_results = bm25_search.search(
                    query, top_k=top_k, filters=filters
                )
            except Exception as e:
                logger.warning(f"BM25 search failed (index might be empty): {e}")
                bm25_results = []
            
            # 2. Fuse results with RRF
            fused_results = self._reciprocal_rank_fusion(
                vector_results, bm25_results
            )
            
            logger.info(f"Fused {len(fused_results)} documents from Vector + BM25")
            
            # 3. Rerank
            rerank_top_n = getattr(settings, 'rerank_top_n', 10)
            final_results = await reranker.rerank(
                query, fused_results, top_n=rerank_top_n
            )
            
            metrics.documents_retrieved.observe(len(final_results))
            return final_results
            
        except Exception as e:
            logger.error(f"Error in hybrid retrieval: {e}")
            # Fallback to empty list to check for gracefulness
            return []

    def _reciprocal_rank_fusion(
        self, 
        results_a: List[Dict[str, Any]], 
        results_b: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Combine two ranked lists using Reciprocal Rank Fusion (RRF).
        Score = 1 / (rank + k)
        """
        scores = defaultdict(float)
        doc_map = {}
        
        # Process list A (Vector)
        for rank, doc in enumerate(results_a):
            doc_id = doc.get("id")
            if not doc_id:
                continue
            scores[doc_id] += 1 / (rank + self.rrf_k)
            doc_map[doc_id] = doc
            
        # Process list B (BM25)
        for rank, doc in enumerate(results_b):
            doc_id = doc.get("id")
            if not doc_id:
                continue
            scores[doc_id] += 1 / (rank + self.rrf_k)
            # Prefer vector doc if exists (contains embedding-based metadata often)
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
        
        # Sort by score descending
        sorted_doc_ids = sorted(
            scores.keys(), 
            key=lambda x: scores[x], 
            reverse=True
        )
        
        # Return docs with RRF score
        fused_docs = []
        for doc_id in sorted_doc_ids:
            doc = doc_map[doc_id]
            doc["rrf_score"] = scores[doc_id]
            fused_docs.append(doc)
            
        return fused_docs


# Global hybrid retriever
hybrid_retriever = HybridRetriever()
