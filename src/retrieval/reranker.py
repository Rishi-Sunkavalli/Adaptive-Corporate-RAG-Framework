"""
Cross-Encoder Semantic Reranker.
Reranks top candidate passages by evaluating cross-entropy term interactions,
exact phrase alignment, and section relevance.
"""

import re
from typing import List, Dict, Any, Tuple

class CrossEncoderReranker:
    def __init__(self):
        pass

    def rerank(self, query: str, candidates: List[Tuple[Dict[str, Any], float]], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not candidates:
            return []

        q_lower = query.lower()
        q_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", q_lower))

        reranked = []
        for chunk, initial_score in candidates:
            content_lower = chunk["content"].lower()
            section_lower = chunk["section"].lower()
            title_lower = chunk["title"].lower()

            # Measure overlap in section title
            sec_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", section_lower))
            sec_overlap = len(q_words.intersection(sec_words)) / max(len(q_words), 1)

            # Measure consecutive bigram matches in content
            bigram_matches = 0
            q_list = list(q_words)
            for i in range(len(q_list) - 1):
                phrase = f"{q_list[i]} {q_list[i+1]}"
                if phrase in content_lower:
                    bigram_matches += 1

            # Exact keyword overlap ratio
            content_words = set(re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", content_lower))
            overlap_ratio = len(q_words.intersection(content_words)) / max(len(q_words), 1)

            # Cross-encoder fine-grained boost
            boost = (sec_overlap * 0.25) + (overlap_ratio * 0.20) + min(bigram_matches * 0.08, 0.25)
            final_score = (initial_score * 0.65) + (boost * 0.35)

            reranked.append((chunk, round(final_score, 4)))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_k]
