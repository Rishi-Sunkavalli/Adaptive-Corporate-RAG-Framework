"""
BM25 (Okapi) Lexical Keyword Retriever.
Provides term-frequency / inverse-document-frequency ranking for corporate search.
"""

import math
import re
from typing import List, Dict, Any, Tuple
from src.rbac.access_control import UserContext, filter_authorized_documents

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "can", "did", "do", "does", "doing", "don", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
    "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "you", "your", "yours", "yourself", "yourselves"
}

def tokenize(text: str) -> List[str]:
    tokens = re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS]

class BM25Retriever:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: List[Dict[str, Any]] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_lens: List[int] = []
        self.avg_dl: float = 0.0
        self.idf: Dict[str, float] = {}

    def index_chunks(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.doc_tokens = []
        self.doc_lens = []

        total_words = 0
        df: Dict[str, int] = {}

        for chunk in chunks:
            full_text = f"{chunk['title']} {chunk['section']} {chunk['content']}"
            toks = tokenize(full_text)
            self.doc_tokens.append(toks)
            length = len(toks)
            self.doc_lens.append(length)
            total_words += length

            unique_toks = set(toks)
            for ut in unique_toks:
                df[ut] = df.get(ut, 0) + 1

        n_docs = len(chunks)
        self.avg_dl = (total_words / n_docs) if n_docs > 0 else 1.0

        # Calculate IDF
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log((n_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def search(self, query: str, user: UserContext, top_k: int = 5, threshold: float = 0.1) -> List[Tuple[Dict[str, Any], float]]:
        # RBAC pre-filter
        authorized_chunks = filter_authorized_documents(self.chunks, user)
        if not authorized_chunks:
            return []

        q_toks = tokenize(query)
        if not q_toks:
            return []

        authorized_ids = {c["chunk_id"] for c in authorized_chunks}
        scores = []

        for idx, chunk in enumerate(self.chunks):
            if chunk["chunk_id"] not in authorized_ids:
                continue

            doc_toks = self.doc_tokens[idx]
            d_len = self.doc_lens[idx]
            score = 0.0

            tf: Dict[str, int] = {}
            for t in doc_toks:
                tf[t] = tf.get(t, 0) + 1

            for q_term in q_toks:
                if q_term not in tf:
                    continue
                term_tf = tf[q_term]
                idf_val = self.idf.get(q_term, 0.1)
                denom = term_tf + self.k1 * (1.0 - self.b + self.b * (d_len / self.avg_dl))
                score += idf_val * (term_tf * (self.k1 + 1.0)) / (denom if denom > 0 else 1.0)

            if score >= threshold:
                scores.append((chunk, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
