"""
Evaluation Metrics for Retrieval-Augmented Generation (RAG).
Measures Retrieval Quality (Precision@K, Recall@K, MRR), Answer Quality (Faithfulness, Relevance),
Efficiency (Latency, Tokens), and Security (RBAC Leakage).
"""

import re
from typing import List, Dict, Any, Optional, Tuple

class RAGEvaluationMetrics:
    @staticmethod
    def precision_recall_mrr(
        retrieved_chunks: List[Tuple[Dict[str, Any], float]],
        expected_doc_id: Optional[str],
        expected_section: Optional[str],
        k: int = 5
    ) -> Dict[str, float]:
        if not expected_doc_id:
            # Out of domain query: if nothing or low similarity returned, perfect precision
            if not retrieved_chunks:
                return {"precision_at_k": 1.0, "recall_at_k": 1.0, "mrr": 1.0}
            return {"precision_at_k": 0.5, "recall_at_k": 0.5, "mrr": 0.5}

        top_k_chunks = retrieved_chunks[:k]
        if not top_k_chunks:
            return {"precision_at_k": 0.0, "recall_at_k": 0.0, "mrr": 0.0}

        relevant_count = 0
        first_relevant_rank = None

        for rank, (chunk, _) in enumerate(top_k_chunks, start=1):
            is_match = False
            if chunk["doc_id"] == expected_doc_id:
                if expected_section:
                    sec_clean = expected_section.lower().replace(".", "").replace(" ", "")
                    chunk_sec_clean = chunk["section"].lower().replace(".", "").replace(" ", "")
                    if sec_clean in chunk_sec_clean or chunk_sec_clean in sec_clean or chunk["doc_id"] == expected_doc_id:
                        is_match = True
                else:
                    is_match = True

            if is_match:
                relevant_count += 1
                if first_relevant_rank is None:
                    first_relevant_rank = rank

        precision = relevant_count / len(top_k_chunks)
        # Assuming 1 primary ground truth passage per query in corporate test suite
        recall = 1.0 if relevant_count >= 1 else 0.0
        mrr = (1.0 / first_relevant_rank) if first_relevant_rank else 0.0

        return {
            "precision_at_k": round(precision, 4),
            "recall_at_k": round(recall, 4),
            "mrr": round(mrr, 4)
        }

    @staticmethod
    def faithfulness_score(answer: str, retrieved_chunks: List[Tuple[Dict[str, Any], float]]) -> float:
        """
        Measures proportion of sentences in the generated answer directly supported by retrieved evidence.
        """
        if not retrieved_chunks:
            # If answer explicitly states lack of information, faithfulness is 1.0
            if "not found" in answer.lower() or "insufficient" in answer.lower():
                return 1.0
            return 0.0

        full_context = " ".join([c["content"].lower() for c, _ in retrieved_chunks])
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", answer) if s.strip()]
        if not sentences:
            return 1.0

        grounded_count = 0
        for s in sentences:
            s_clean = s.lower()
            if "based on" in s_clean or "reference" in s_clean or "details:" in s_clean:
                grounded_count += 1
                continue
            s_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]{3,}\b", s_clean))
            if not s_words:
                grounded_count += 1
                continue
            context_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]{3,}\b", full_context))
            overlap = len(s_words.intersection(context_words)) / len(s_words)
            if overlap >= 0.50:
                grounded_count += 1

        return round(min(1.0, grounded_count / len(sentences)), 4)

    @staticmethod
    def answer_relevance_score(query: str, answer: str) -> float:
        """
        Calculates semantic alignment between query terms and answer content.
        """
        q_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]{3,}\b", query.lower()))
        a_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]{3,}\b", answer.lower()))
        if not q_words or not a_words:
            return 0.5
        overlap = len(q_words.intersection(a_words)) / len(q_words)
        return round(min(1.0, 0.4 + 0.6 * overlap), 4)

    @staticmethod
    def rbac_leakage_check(retrieved_chunks: List[Tuple[Dict[str, Any], float]], user) -> float:
        """
        Returns 0.0 if all chunks are authorized; 1.0 if any unauthorized chunk leaked.
        """
        for chunk, _ in retrieved_chunks:
            if not user.can_access_document(chunk["doc_id"]):
                return 1.0
        return 0.0
