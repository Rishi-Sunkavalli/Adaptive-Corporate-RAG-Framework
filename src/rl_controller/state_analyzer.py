"""
Query State Analyzer & Feature Extraction for the RL Retrieval Controller.
Extracts query intent, length bin, complexity, and department signals.
"""

import re
from typing import Dict, Any, List

class QueryStateAnalyzer:
    DEPARTMENT_KEYWORDS = {
        "HR": ["leave", "vacation", "holiday", "sick", "maternity", "paternity", "parental", "bereavement", "conduct", "benefits", "insurance", "401k", "stipend", "bonus", "appraisal", "onboarding", "attendance"],
        "IT": ["vpn", "mfa", "password", "login", "incident", "p1", "p2", "outage", "dr", "failover", "rto", "rpo", "teleport", "cyberark", "ciso", "iam", "credential", "security", "encryption"],
        "Finance": ["expense", "reimbursement", "travel", "flight", "hotel", "per-diem", "meal", "receipt", "po", "purchase order", "procurement", "invoice", "vendor", "net-30", "cfo", "budget"],
        "Operations": ["sop", "escalation", "ticket", "tier 1", "tier 2", "sla", "bcp", "business continuity", "customer", "support", "downtime", "crisis", "outage", "incident commander"]
    }

    INTENT_PATTERNS = [
        (r"\b(compare|difference between|versus|vs|how does .* differ)\b", "comparative"),
        (r"\b(how do i|steps to|process for|procedure|ladder|approval workflow|what to do)\b", "procedural"),
        (r"\b(is it allowed|can i|permitted|policy on|mandatory|compulsory|forbidden|prohibited)\b", "policy_verification"),
        (r"\b(what is|how many|how much|when|who|where|amount|rate|percentage|limit|cap)\b", "factual"),
    ]

    @classmethod
    def analyze_query(cls, query: str) -> Dict[str, Any]:
        words = re.findall(r"\b[a-zA-Z0-9_\-\$]+\b", query.lower())
        word_count = len(words)

        # 1. Length binning
        if word_count < 10:
            length_bin = "short"
            length_score = 0.2
        elif word_count <= 22:
            length_bin = "medium"
            length_score = 0.6
        else:
            length_bin = "long"
            length_score = 1.0

        # 2. Intent Detection
        detected_intent = "factual"
        q_lower = query.lower()
        for pattern, intent in cls.INTENT_PATTERNS:
            if re.search(pattern, q_lower):
                detected_intent = intent
                break

        # 3. Department Classification
        dept_scores = {"HR": 0, "IT": 0, "Finance": 0, "Operations": 0}
        for dept, kws in cls.DEPARTMENT_KEYWORDS.items():
            for kw in kws:
                if kw in q_lower:
                    dept_scores[dept] += 1
        
        top_dept = max(dept_scores, key=dept_scores.get)
        if dept_scores[top_dept] == 0:
            detected_dept = "General"
        else:
            detected_dept = top_dept

        # 4. Complexity Estimation
        complexity_score = 0
        if detected_intent in ["comparative", "procedural"]:
            complexity_score += 2
        if word_count > 15:
            complexity_score += 1
        if any(w in q_lower for w in ["versus", "compare", "protocol", "disaster", "escalation", "three-way", "rto", "rpo"]):
            complexity_score += 1

        if complexity_score <= 1:
            complexity = "low"
            comp_numeric = 0.2
        elif complexity_score == 2:
            complexity = "medium"
            comp_numeric = 0.6
        else:
            complexity = "high"
            comp_numeric = 1.0

        state_key = f"{detected_intent}_{complexity}_{length_bin}_{detected_dept}"

        # Numerical feature vector for LinUCB / Contextual Bandit (dim = 6)
        intent_map = {"factual": 0.2, "policy_verification": 0.4, "procedural": 0.7, "comparative": 1.0}
        feature_vector = [
            1.0,  # Bias
            intent_map.get(detected_intent, 0.5),
            comp_numeric,
            length_score,
            min(word_count / 30.0, 1.0),
            1.0 if detected_dept != "General" else 0.0
        ]

        return {
            "query": query,
            "word_count": word_count,
            "length_bin": length_bin,
            "intent": detected_intent,
            "department": detected_dept,
            "complexity": complexity,
            "state_key": state_key,
            "feature_vector": feature_vector
        }
