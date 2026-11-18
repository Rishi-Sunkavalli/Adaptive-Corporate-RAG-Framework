"""
Contextual Bandit and Q-Learning Agent for Adaptive RAG Retrieval Optimization.
Implements LinUCB (Linear Upper Confidence Bound) and Tabular Q-Learning.
"""

import math
import random
import json
import os
from typing import Dict, Any, List, Optional
from src.rl_controller.action_space import ActionSpace

class LinUCBAgent:
    """
    Disjoint Linear Upper Confidence Bound (LinUCB) contextual bandit.
    Learns linear relationship between query context features and retrieval configuration rewards.
    """
    def __init__(self, action_space: ActionSpace, feature_dim: int = 6, alpha: float = 0.8):
        self.action_space = action_space
        self.num_actions = len(action_space)
        self.dim = feature_dim
        self.alpha = alpha

        # For each action a: A_a is d x d identity, b_a is d x 1 zero vector
        self.A = [self._identity_matrix(self.dim) for _ in range(self.num_actions)]
        self.b = [[0.0] * self.dim for _ in range(self.num_actions)]
        self.action_counts = [0] * self.num_actions
        self.history = []

    def _identity_matrix(self, d: int) -> List[List[float]]:
        return [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]

    def _invert_matrix(self, A: List[List[float]]) -> List[List[float]]:
        """
        Gauss-Jordan inversion for small d (d=6).
        """
        n = len(A)
        # Augment with identity
        aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
        for i in range(n):
            # Pivot
            pivot = aug[i][i]
            if abs(pivot) < 1e-9:
                pivot = 1e-9
            for j in range(2 * n):
                aug[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(2 * n):
                        aug[k][j] -= factor * aug[i][j]
        return [row[n:] for row in aug]

    def _mat_vec_mul(self, M: List[List[float]], v: List[float]) -> List[float]:
        return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

    def _dot(self, v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def select_action(self, feature_vector: List[float], explore: bool = True) -> Dict[str, Any]:
        best_action_id = 0
        max_p = -float("inf")
        action_scores = {}

        x = feature_vector
        for a in range(self.num_actions):
            A_inv = self._invert_matrix(self.A[a])
            theta = self._mat_vec_mul(A_inv, self.b[a])
            expected_r = self._dot(theta, x)

            if explore:
                A_inv_x = self._mat_vec_mul(A_inv, x)
                var = math.sqrt(max(0.0, self._dot(x, A_inv_x)))
                p = expected_r + self.alpha * var
            else:
                p = expected_r

            action_scores[a] = round(p, 4)
            if p > max_p:
                max_p = p
                best_action_id = a

        chosen_action = self.action_space.get_action(best_action_id).copy()
        chosen_action["ucb_score"] = round(max_p, 4)
        chosen_action["confidence"] = min(1.0, max(0.1, 1.0 / (1.0 + math.exp(-max_p))))
        return chosen_action

    def update(self, action_id: int, feature_vector: List[float], reward: float):
        """
        Ridge regression update: A_a += x x^T, b_a += r x
        """
        x = feature_vector
        for i in range(self.dim):
            self.b[action_id][i] += reward * x[i]
            for j in range(self.dim):
                self.A[action_id][i][j] += x[i] * x[j]
        self.action_counts[action_id] += 1
        self.history.append({"action_id": action_id, "reward": reward})

    def save(self, filepath: str):
        data = {
            "dim": self.dim,
            "alpha": self.alpha,
            "A": self.A,
            "b": self.b,
            "action_counts": self.action_counts,
            "history_length": len(self.history)
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.dim = data["dim"]
            self.alpha = data["alpha"]
            self.A = data["A"]
            self.b = data["b"]
            self.action_counts = data["action_counts"]
