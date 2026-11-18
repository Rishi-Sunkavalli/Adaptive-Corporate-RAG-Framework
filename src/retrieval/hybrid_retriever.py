"""
Hybrid Retriever combining Dense Semantic Search and BM25 Lexical Search
via Reciprocal Rank Fusion (RRF).
"""

from typing import List, Dict, Any, Tuple
from src.rbac.access_control import UserContext
from src.retrieval.vector_store import CorporateVectorStore
from src.retrieval.bm25_search import BM25Retriever

class HybridRetriever:
    def __init__(self, vector_store: CorporateVectorStore, bm25_retriever: BM25Retriever, rrf_k: int = 60):
        self.vector_store = vector_store
        self.bm25 = bm25_retriever
        self.rrf_k = rrf_k

    def search(
        self,
        query: str,
        user: UserContext,
        top_k: int = 5,
        threshold: float = 0.35,
        dense_weight: float = 0.6,
        bm25_weight: float = 0.4
    ) -> List[Tuple[Dict[str, Any], float]]:
        # Fetch candidate pools from both retrievers (with larger candidate pool for fusion)
        fetch_k = max(top_k * 2, 10)
        dense_results = self.vector_store.search(query, user, top_k=fetch_k, threshold=threshold * 0.7)
        bm25_results = self.bm25.search(query, user, top_k=fetch_k, threshold=0.05)

        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}
        raw_dense_sims: Dict[str, float] = {}

        # Dense rank fusion
        for rank, (chunk, sim) in enumerate(dense_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            raw_dense_sims[cid] = sim
            score = dense_weight * (1.0 / (self.rrf_k + rank + 1))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score

        # BM25 rank fusion
        for rank, (chunk, bm_score) in enumerate(bm25_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            score = bm25_weight * (1.0 / (self.rrf_k + rank + 1))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score

        # Filter by threshold on scaled score
        fused = []
        for cid, rrf_score in rrf_scores.items():
            # Normalized score approximation combining dense similarity and RRF
            sim = raw_dense_sims.get(cid, 0.35)
            combined_score = 0.5 * sim + 0.5 * (rrf_score * (self.rrf_k + 1))
            if combined_score >= threshold:
                fused.append((chunk_map[cid], combined_score))

        fused.sort(key=lambda x: x[1], reverse=True)
        return fused[:top_k]
