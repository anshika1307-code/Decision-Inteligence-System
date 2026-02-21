"""BM25 keyword search implementation"""

from typing import List, Dict, Any, Optional
import numpy as np
from rank_bm25 import BM25Okapi
from src.observability.logger import get_logger

logger = get_logger("bm25_search")


class BM25SearchProvider:
    """BM25 keyword search provider"""
    
    def __init__(self):
        self.bm25: Optional[BM25Okapi] = None
        self.documents: List[Dict[str, Any]] = []
        self.tokenized_docs: List[List[str]] = []
        
    def fit(self, documents: List[Dict[str, Any]]):
        """Build BM25 index from documents"""
        try:
            self.documents = documents
            # Simple tokenization by splitting on whitespace
            # In production, use a proper tokenizer (e.g., NLTK or spaCy)
            self.tokenized_docs = [
                doc["text"].lower().split() 
                for doc in documents
            ]
            
            logger.info(f"Building BM25 index for {len(documents)} documents")
            self.bm25 = BM25Okapi(self.tokenized_docs)
            logger.info("BM25 index built successfully")
            
        except Exception as e:
            logger.error(f"Error building BM25 index: {e}")
            raise

    def search(
        self, 
        query: str, 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for documents using BM25"""
        if not self.bm25:
            logger.warning("BM25 index not initialized")
            return []
            
        try:
            tokenized_query = query.lower().split()
            scores = self.bm25.get_scores(tokenized_query)
            
            # Get top indices
            # argsort sorts in ascending order, so we reverse it
            top_indices = np.argsort(scores)[::-1]
            
            results = []
            count = 0
            
            for idx in top_indices:
                if count >= top_k:
                    break
                    
                doc = self.documents[idx]
                score = float(scores[idx])
                
                # Apply filters if provided
                if filters:
                    matches = True
                    for key, value in filters.items():
                        if doc["metadata"].get(key) != value:
                            matches = False
                            break
                    if not matches:
                        continue
                
                if score > 0:
                    results.append({
                        "id": doc.get("id"),
                        "score": score,
                        "text": doc["text"],
                        "metadata": doc["metadata"]
                    })
                    count += 1
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing BM25 search: {e}")
            return []


# Global BM25 provider
bm25_search = BM25SearchProvider()
