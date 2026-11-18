"""
Script to execute the complete RAG evaluation benchmark and output comparative results.
"""

import sys
import os
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.evaluation.benchmark import run_benchmark

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(base_dir, "data", "corporate_documents")
    queries_path = os.path.join(base_dir, "data", "test_queries.json")
    output_path = os.path.join(base_dir, "data", "benchmark_results.json")

    print(f"🚀 Running Corporate RAG Benchmark across Fixed, Heuristic, and RL-Adaptive models...")
    results = run_benchmark(docs_dir, queries_path, output_path)

    print("\n" + "="*80)
    print("🏆 CORPORATE RAG EVALUATION BENCHMARK RESULTS")
    print("="*80)
    summary = results["metrics_summary"]
    header = f"{'Metric':<30} | {'Fixed RAG':<14} | {'Heuristic':<14} | {'Adaptive RL-RAG':<14}"
    print(header)
    print("-" * len(header))

    metric_names = [
        ("mean_precision_at_5", "Precision @ 5"),
        ("mean_recall_at_5", "Recall @ 5"),
        ("mean_mrr", "Mean Reciprocal Rank (MRR)"),
        ("mean_faithfulness", "Faithfulness (Grounding)"),
        ("mean_answer_relevance", "Answer Relevance"),
        ("mean_latency_ms", "Latency (ms)"),
        ("mean_tokens_per_query", "Tokens / Query"),
        ("total_tokens_consumed", "Total Tokens Consumed"),
        ("mean_reward", "Mean Multi-Objective Reward"),
        ("rbac_security_leakage_rate", "RBAC Security Leakage Rate")
    ]

    for key, label in metric_names:
        f_val = str(summary['fixed'][key])
        h_val = str(summary['heuristic'][key])
        a_val = str(summary['adaptive'][key])
        print(f"{label:<30} | {f_val:<14} | {h_val:<14} | {a_val:<14}")
    print("="*80)
    print(f"✅ Full benchmark data saved to: {output_path}")

if __name__ == "__main__":
    main()
