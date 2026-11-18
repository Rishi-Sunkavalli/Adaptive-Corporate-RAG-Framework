"""
Action Space Definition for Adaptive RAG Retrieval Controller.
Defines discrete candidate configurations for Top-K, Similarity Threshold,
Search Mode (Dense vs Hybrid), and Reranking.
"""

from typing import List, Dict, Any

class ActionSpace:
    CANDIDATE_TOP_K = [3, 5, 8]
    CANDIDATE_THRESHOLDS = [0.35, 0.50, 0.65]
    CANDIDATE_MODES = ["dense", "hybrid"]
    CANDIDATE_RERANK = [False, True]

    def __init__(self):
        self.actions: List[Dict[str, Any]] = []
        action_id = 0
        for top_k in self.CANDIDATE_TOP_K:
            for thresh in self.CANDIDATE_THRESHOLDS:
                for mode in self.CANDIDATE_MODES:
                    for rerank in self.CANDIDATE_RERANK:
                        self.actions.append({
                            "action_id": action_id,
                            "top_k": top_k,
                            "threshold": thresh,
                            "mode": mode,
                            "rerank": rerank,
                            "description": f"K={top_k}, Thresh={thresh}, Mode={mode}, Rerank={rerank}"
                        })
                        action_id += 1

    def __len__(self):
        return len(self.actions)

    def get_action(self, action_id: int) -> Dict[str, Any]:
        return self.actions[action_id % len(self.actions)]

    def get_fixed_baseline_action(self) -> Dict[str, Any]:
        """
        Conventional Fixed RAG: K=5, Threshold=0.50, Dense, No Reranking.
        """
        return {
            "action_id": -1,
            "top_k": 5,
            "threshold": 0.50,
            "mode": "dense",
            "rerank": False,
            "description": "Baseline: Fixed K=5, Thresh=0.50, Dense, Rerank=False"
        }

    def get_heuristic_action(self, state_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query-Aware Heuristic Baseline: Rules based on query length and complexity.
        """
        complexity = state_info["complexity"]
        length_bin = state_info["length_bin"]
        intent = state_info["intent"]

        if complexity == "high" or intent == "comparative":
            top_k = 8
            threshold = 0.35
            mode = "hybrid"
            rerank = True
        elif complexity == "medium" or intent == "procedural":
            top_k = 5
            threshold = 0.50
            mode = "hybrid" if length_bin == "long" else "dense"
            rerank = False
        else:
            top_k = 3
            threshold = 0.50
            mode = "dense"
            rerank = False

        return {
            "action_id": -2,
            "top_k": top_k,
            "threshold": threshold,
            "mode": mode,
            "rerank": rerank,
            "description": f"Heuristic: K={top_k}, Thresh={threshold}, Mode={mode}, Rerank={rerank}"
        }
