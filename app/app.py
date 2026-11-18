"""
Interactive Streamlit Application for Adaptive Corporate RAG.
Provides live query interface, role-based access testing, RL decision inspection,
and comparative benchmark dashboards.
"""

import streamlit as st
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rbac.access_control import DEFAULT_USERS, Role
from src.evaluation.benchmark import CorporateRAGPipeline
from src.rl_controller.state_analyzer import QueryStateAnalyzer

st.set_page_config(
    page_title="Adaptive Corporate RAG Framework",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_pipeline():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(base_dir, "data", "corporate_documents")
    return CorporateRAGPipeline(docs_dir)

pipeline = load_pipeline()

# Sidebar: User & RBAC Configuration
st.sidebar.title("🔐 Corporate Identity & RBAC")
user_key = st.sidebar.selectbox(
    "Active Corporate User Profile:",
    options=list(DEFAULT_USERS.keys()),
    format_func=lambda k: f"{DEFAULT_USERS[k].name} [{DEFAULT_USERS[k].department}]"
)
current_user = DEFAULT_USERS[user_key]

st.sidebar.markdown(f"""
**Employee Name:** {current_user.name}  
**Department:** {current_user.department}  
**Role:** `{current_user.role.value}`  
""")

st.sidebar.divider()
st.sidebar.subheader("⚙️ Retrieval Architecture")
rag_mode = st.sidebar.radio(
    "Select RAG Pipeline:",
    options=["adaptive", "heuristic", "fixed"],
    format_func=lambda x: {
        "adaptive": "🧠 Adaptive RL-RAG (Contextual Bandit)",
        "heuristic": "📏 Query-Aware Heuristic Baseline",
        "fixed": "🔒 Fixed-Parameter RAG (Static K=5)"
    }[x]
)

st.title("🏢 Adaptive Corporate RAG Framework")
st.caption("Reinforcement Learning-Optimized Retrieval-Augmented Generation for Enterprise Knowledge Intelligence")

tab_chat, tab_bench, tab_kb = st.tabs(["💬 Knowledge Assistant", "📊 Benchmark & Evaluation", "📚 Corporate Knowledge Base"])

with tab_chat:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("Submit Corporate Query")
        sample_queries = [
            "What is the annual leave entitlement for regular full-time employees?",
            "How many days of annual leave can be rolled over into the next year?",
            "Compare primary caregiver maternity leave with secondary caregiver paternity leave durations.",
            "What are the initial SLA response times for P1 Critical Outage versus P2 Major Degradation incidents?",
            "What are the daily per-diem meal allowances for employees traveling to Tier 1 cities?",
            "Explain the three-way matching verification protocol required before supplier payments are disbursed.",
            "What are the escalation triggers that require a customer support ticket to be reassigned immediately?",
            "What is the corporate pet policy for bringing dogs to the London technology office? (Out of domain test)"
        ]
        selected_sample = st.selectbox("Or choose a benchmark query:", ["-- Custom Query --"] + sample_queries)
        default_query = "" if selected_sample == "-- Custom Query --" else selected_sample
        user_query = st.text_input("Enter natural-language question:", value=default_query)

        run_btn = st.button("🚀 Execute Grounded Retrieval", type="primary")

    if run_btn and user_query:
        with st.spinner("Analyzing state and executing retrieval..."):
            out = pipeline.execute_query(user_query, current_user, mode=rag_mode, train_rl=False)
            gen = out["generation"]

        with col1:
            st.markdown("### 📝 Grounded Response")
            if gen["insufficient_evidence"]:
                st.warning(gen["answer"])
            else:
                st.info(gen["answer"])

            if gen["citations"]:
                st.markdown("#### 📑 Verified Source Citations")
                for cit in gen["citations"]:
                    st.markdown(f"- **{cit['title']}** | *{cit['section']}* (v{cit['version']}, {cit['effective_date']}) — Score: `{cit['relevance_score']}`")

        with col2:
            st.markdown("### 🧠 RL Controller Diagnostics")
            state = out["state"]
            action = out["action"]
            reward = out["reward"]

            st.json({
                "Detected Intent": state["intent"],
                "Estimated Complexity": state["complexity"],
                "Query Length Bin": state["length_bin"],
                "Target Department": state["department"]
            })

            st.markdown(f"""
            **Selected Action Configuration:**
            - **Top-K Chunks:** `{action.get('top_k', 5)}`
            - **Similarity Threshold:** `{action.get('threshold', 0.50)}`
            - **Search Strategy:** `{action.get('mode', 'dense').upper()}`
            - **Reranker Applied:** `{'Yes' if action.get('rerank') else 'No'}`
            """)

            st.metric("Latency", f"{out['latency_ms']} ms")
            st.metric("Tokens Consumed", f"{out['tokens']} tokens")
            st.metric("Multi-Objective Reward", f"{reward['scalar_reward']}")

with tab_bench:
    st.subheader("Comparative Benchmark: Fixed vs Heuristic vs RL-Adaptive")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bench_path = os.path.join(base_dir, "data", "benchmark_results.json")
    if os.path.exists(bench_path):
        with open(bench_path, "r") as f:
            bdata = json.load(f)
        summary = bdata["metrics_summary"]
        st.dataframe(summary)
    else:
        st.info("Run scripts/run_evaluation.py to generate benchmark results.")

with tab_kb:
    st.subheader("Ingested Corporate Knowledge Base")
    st.write(f"Total chunks indexed: **{len(pipeline.chunks)}**")
    for c in pipeline.chunks[:8]:
        with st.expander(f"[{c['department']}] {c['title']} - {c['section']}"):
            st.markdown(f"**Security Clearance:** `{c['security_clearance']}` | **Version:** `{c['version']}`")
            st.text(c["content"])
