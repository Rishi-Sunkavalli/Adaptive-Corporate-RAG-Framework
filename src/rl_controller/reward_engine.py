"""
Multi-Objective Reward Function Engine for RL-Based RAG Controller.
Balances retrieval evidence relevance, answer faithfulness, and question relevance
against operational latency and token consumption penalties.
"""

from typing import Dict, Any

class RewardEngine:
    def __init__(
        self,
        w_relevance: float = 0.35,
        w_faithfulness: float = 0.35,
        w_answer_relevance: float = 0.15,
        w_latency: float = 0.08,
        w_cost: float = 0.07,
        max_target_latency_ms: float = 1200.0,
        max_target_tokens: float = 2000.0
    ):
        self.w1 = w_relevance
        self.w2 = w_faithfulness
        self.w3 = w_answer_relevance
        self.w4 = w_latency
        self.w5 = w_cost
        self.max_target_latency_ms = max_target_latency_ms
        self.max_target_tokens = max_target_tokens

    def compute_reward(
        self,
        retrieval_relevance: float,
        faithfulness: float,
        answer_relevance: float,
        latency_ms: float,
        tokens_used: int
    ) -> Dict[str, Any]:
        """
        Calculates scalar reward in range [-1.0, 1.0] and component logs.
        """
        # Normalize cost metrics into [0.0, 1.5]
        norm_latency = min(latency_ms / self.max_target_latency_ms, 1.5)
        norm_tokens = min(tokens_used / self.max_target_tokens, 1.5)

        # Multi-objective weighted sum
        positive_term = (
            self.w1 * max(0.0, min(1.0, retrieval_relevance)) +
            self.w2 * max(0.0, min(1.0, faithfulness)) +
            self.w3 * max(0.0, min(1.0, answer_relevance))
        )
        penalty_term = (
            self.w4 * norm_latency +
            self.w5 * norm_tokens
        )

        scalar_reward = positive_term - penalty_term
        scalar_reward = max(-1.0, min(1.0, round(scalar_reward, 4)))

        return {
            "scalar_reward": scalar_reward,
            "components": {
                "retrieval_relevance": round(retrieval_relevance, 4),
                "faithfulness": round(faithfulness, 4),
                "answer_relevance": round(answer_relevance, 4),
                "normalized_latency": round(norm_latency, 4),
                "normalized_tokens": round(norm_tokens, 4),
                "positive_gain": round(positive_term, 4),
                "cost_penalty": round(penalty_term, 4)
            },
            "weights": {
                "w_relevance": self.w1,
                "w_faithfulness": self.w2,
                "w_answer_relevance": self.w3,
                "w_latency": self.w4,
                "w_cost": self.w5
            }
        }
