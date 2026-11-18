"""
Vector Store & Dense Semantic Search for Corporate Knowledge Management.
Supports dense vector embedding, indexing, cosine similarity ranking,
and strict pre-retrieval RBAC filtering.
"""

import math
import re
from typing import List, Dict, Any, Tuple
from src.rbac.access_control import UserContext, filter_authorized_documents

class SemanticVectorizer:
    """
    Lightweight, highly performant character n-gram & word hashing embedding generator.
    Produces stable 384-dimensional dense vectors with cosine similarity without external heavyweight dependencies.
    """
    def __init__(self, dim: int = 384):
        self.dim = dim

    def _hash_token(self, token: str) -> int:
        h = 2166136261
        for ch in token:
            h = (h ^ ord(ch)) * 16777619
        return h & 0x7FFFFFFF

    def embed_text(self, text: str) -> List[float]:
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", text.lower())
        vec = [0.0] * self.dim
        if not tokens:
            return vec

        # Bag of words + subword character n-grams
        for tok in tokens:
            idx = self._hash_token(tok) % self.dim
            vec[idx] += 1.0

            # 3-char subwords
            if len(tok) >= 3:
                for i in range(len(tok) - 2):
                    sub = tok[i:i+3]
                    s_idx = self._hash_token(sub) % self.dim
                    vec[s_idx] += 0.4

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 1e-9:
            vec = [x / norm for x in vec]
        return vec

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    return max(0.0, min(1.0, dot))


class CorporateVectorStore:
    def __init__(self, vectorizer: SemanticVectorizer = None):
        self.vectorizer = vectorizer or SemanticVectorizer(dim=384)
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []

    def index_chunks(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        texts = [f"{c['title']} {c['section']} {c['content']}" for c in chunks]
        self.embeddings = self.vectorizer.embed_batch(texts)
        for i, c in enumerate(self.chunks):
            c["_embedding_idx"] = i

    def search(self, query: str, user: UserContext, top_k: int = 5, threshold: float = 0.35) -> List[Tuple[Dict[str, Any], float]]:
        """
        Dense vector search with RBAC pre-retrieval filtering.
        """
        # Step 1: Pre-retrieval RBAC Filter
        authorized_chunks = filter_authorized_documents(self.chunks, user)
        if not authorized_chunks:
            return []

        # Step 2: Query Embedding
        q_emb = self.vectorizer.embed_text(query)

        # Step 3: Compute Similarities
        scored_results = []
        for chunk in authorized_chunks:
            idx = chunk["_embedding_idx"]
            c_emb = self.embeddings[idx]
            sim = cosine_similarity(q_emb, c_emb)
            if sim >= threshold:
                scored_results.append((chunk, sim))

        # Step 4: Sort descending by similarity
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]
