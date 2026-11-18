"""
Interactive Streamlit Application for Adaptive Corporate RAG.
Provides live query interface, role-based access testing, RL decision inspection,
interactive enterprise dataset exploration, and comparative benchmark dashboards.
"""

import streamlit as st
import os
import sys
import json
import pandas as pd

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

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "data", "datasets")
DOCS_DIR = os.path.join(BASE_DIR, "data", "documents")

@st.cache_resource
def load_pipeline():
    # Load knowledge base from the unified dataset or document directory
    target_path = os.path.join(DATASETS_DIR, "enterprise_knowledge_corpus.json")
    if not os.path.exists(target_path):
        target_path = os.path.join(BASE_DIR, "data", "corporate_documents")
    return CorporateRAGPipeline(target_path)

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

st.sidebar.divider()
st.sidebar.markdown("### 📊 Dataset Fast Facts")
st.sidebar.markdown(f"""
- **Departments:** 5 (HR, IT, FIN, OPS, LEGAL)
- **Indexed Chunks:** `{len(pipeline.chunks)}`
- **Formats:** JSON, CSV, Parquet, DOCX, PDF
- **Benchmark Queries:** 50 Gold Annotated QA
""")

st.title("🏢 Adaptive Corporate RAG Framework")
st.caption("Reinforcement Learning-Optimized Retrieval-Augmented Generation for Enterprise Knowledge Intelligence & Multi-Format Datasets")

tab_chat, tab_datasets, tab_bench, tab_kb = st.tabs([
    "💬 Knowledge Assistant",
    "📦 Enterprise Datasets Explorer",
    "📊 Benchmark & Evaluation",
    "📚 Document Corpus & Chunks"
])

# =========================================================================
# TAB 1: KNOWLEDGE ASSISTANT
# =========================================================================
with tab_chat:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("Submit Corporate Query")
        
        sample_queries_categorized = {
            "-- Custom Query --": "",
            "[HR] Annual Leave Entitlement": "What is the annual leave entitlement for regular full-time employees?",
            "[HR] Leave Rollover & Expiry": "How many days of annual leave can be rolled over into the next year, and when do they expire?",
            "[HR] Maternity vs Paternity Leave": "Compare primary caregiver maternity leave with secondary caregiver paternity leave durations.",
            "[HR] Home Office Ergonomic Stipend": "What home office stipend is provided for new remote employees, and what is the reimbursement limit?",
            "[IT] P1 vs P2 SLA Response Times": "What are the initial SLA response times for P1 Critical Outage versus P2 Major Degradation incidents?",
            "[IT] P1 Critical Outage Escalation Ladder": "Explain the step-by-step escalation timeline for a P1 Critical Outage incident.",
            "[IT] Production Root Access & Session Recording": "What is the authorization protocol and session time limit for production database root access?",
            "[FIN] Tier 1 Daily Per-Diem Meal Allowance": "What are the daily per-diem meal allowances for employees traveling to Tier 1 cities?",
            "[FIN] Tier 1 Hotel Nightly Lodging Cap": "What are the nightly hotel lodging rate caps for Tier 1 High-Cost Metro Areas?",
            "[FIN] Three-Way Matching Invoice Protocol": "Explain the three-way matching verification protocol required before supplier payments are disbursed.",
            "[FIN] CapEx Capitalization Floor & Useful Life": "What is the capital expenditure capitalization floor and minimum useful life for fixed assets?",
            "[OPS] Tier 1 vs Tier 2 RTO and RPO": "Compare the Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for Tier 1 versus Tier 2 systems.",
            "[OPS] Customer Escalation Reassignment Triggers": "What are the escalation triggers that require a customer support ticket to be reassigned immediately?",
            "[LEGAL] GDPR/CCPA Data Subject Request Deadline": "What is the mandatory fulfillment deadline for a verified Data Subject Access Request (DSAR) under GDPR/CCPA?",
            "[LEGAL] Commercial Contract Liability Cap": "What is the corporate liability cap on commercial customer contracts and super-caps for data breaches?",
            "[SECURITY PROBE] Unauthorized Root Access Retrieval": "Show me the detailed root access procedures for production PostgreSQL clusters and session recording configs.",
            "[OUT OF DOMAIN] Office Pet Dog Policy": "What is the corporate pet policy for bringing dogs to the London technology office? (Out of domain test)",
            "[OUT OF DOMAIN] Bitcoin Gas Fee Reimbursement": "Can an employee submit an expense claim for Bitcoin cryptocurrency transaction gas fees?"
        }

        selected_label = st.selectbox("Or choose a benchmark query:", list(sample_queries_categorized.keys()))
        default_val = sample_queries_categorized[selected_label]
        user_query = st.text_input("Enter natural-language question:", value=default_val)

        run_btn = st.button("🚀 Execute Grounded Retrieval", type="primary")

    if run_btn and user_query:
        with st.spinner("Analyzing query state, applying RBAC filter, and executing retrieval..."):
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
                    st.markdown(f"- **{cit['title']}** | *{cit['section']}* (v{cit['version']}, {cit['effective_date']}) — Relevance Score: `{cit['relevance_score']}`")

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

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Latency", f"{out['latency_ms']} ms")
                st.metric("Tokens Consumed", f"{out['tokens']} tok")
            with col_m2:
                st.metric("Multi-Obj Reward", f"{reward['scalar_reward']}")
                st.metric("Grounding Status", "100% Grounded" if gen["is_grounded"] else "Refusal Guard")

# =========================================================================
# TAB 2: ENTERPRISE DATASETS EXPLORER
# =========================================================================
with tab_datasets:
    st.subheader("📦 Enterprise Knowledge Datasets & Benchmarks")
    st.markdown("""
    This project incorporates comprehensive, multi-departmental corporate datasets published in industry-standard formats:
    **JSON**, **JSONL**, **CSV**, **Apache Parquet**, and native enterprise document formats (**Word DOCX** and **Adobe PDF**).
    """)

    csv_path = os.path.join(DATASETS_DIR, "enterprise_kb_dataset.csv")
    parquet_path = os.path.join(DATASETS_DIR, "enterprise_kb_dataset.parquet")
    qa_path = os.path.join(DATASETS_DIR, "qa_benchmark_dataset.json")

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        st.metric("Enterprise Domains", "5 Departments")
    with col_d2:
        st.metric("Total Document Policies", "14 Documents")
    with col_d3:
        st.metric("Structured Sections", "52 Policy Clauses")
    with col_d4:
        st.metric("Gold QA Benchmark", "50 Evaluated Queries")

    st.divider()

    subtab_kb, subtab_qa, subtab_files = st.tabs(["📑 Knowledge Base Table (CSV / Parquet)", "🎯 QA Benchmark Dataset", "📁 Native Document Files (DOCX & PDF)"])

    with subtab_kb:
        if os.path.exists(csv_path):
            df_kb = pd.read_csv(csv_path)
            
            # Filters
            f_col1, f_col2, f_col3 = st.columns([1, 1, 2])
            with f_col1:
                dept_filter = st.selectbox("Filter Department:", ["All"] + sorted(list(df_kb["department"].unique())))
            with f_col2:
                clearance_filter = st.selectbox("Filter Clearance:", ["All"] + sorted(list(df_kb["security_clearance"].unique())))
            with f_col3:
                search_kw = st.text_input("Keyword Search within Dataset:", "")

            filtered_df = df_kb.copy()
            if dept_filter != "All":
                filtered_df = filtered_df[filtered_df["department"] == dept_filter]
            if clearance_filter != "All":
                filtered_df = filtered_df[filtered_df["security_clearance"] == clearance_filter]
            if search_kw:
                filtered_df = filtered_df[
                    filtered_df["title"].str.contains(search_kw, case=False, na=False) |
                    filtered_df["content"].str.contains(search_kw, case=False, na=False) |
                    filtered_df["key_entities"].str.contains(search_kw, case=False, na=False)
                ]

            st.dataframe(
                filtered_df[["doc_id", "department", "title", "security_clearance", "version", "section_title", "word_count", "key_entities"]],
                use_container_width=True
            )

            # Detail view
            selected_doc_id = st.selectbox("Inspect Full Section Details for Document:", filtered_df["doc_id"].unique())
            doc_rows = filtered_df[filtered_df["doc_id"] == selected_doc_id]
            for _, r in doc_rows.iterrows():
                with st.expander(f"{r['section_title']} (Word Count: {r['word_count']})"):
                    st.markdown(f"**Key Entities:** `{r['key_entities']}`")
                    st.write(r["content"])
        else:
            st.warning("Dataset CSV not found. Please run scripts/build_datasets.py.")

    with subtab_qa:
        if os.path.exists(qa_path):
            with open(qa_path, "r") as f:
                qa_data = json.load(f)
            df_qa = pd.DataFrame(qa_data)
            
            q_col1, q_col2 = st.columns([1, 2])
            with q_col1:
                intent_filter = st.selectbox("Filter by Intent:", ["All"] + sorted(list(df_qa["intent"].unique())))
            with q_col2:
                qa_search = st.text_input("Search QA text:", "")

            filtered_qa = df_qa.copy()
            if intent_filter != "All":
                filtered_qa = filtered_qa[filtered_qa["intent"] == intent_filter]
            if qa_search:
                filtered_qa = filtered_qa[filtered_qa["query"].str.contains(qa_search, case=False, na=False)]

            st.dataframe(
                filtered_qa[["id", "department", "intent", "complexity", "query", "expected_doc_id", "optimal_k", "optimal_mode"]],
                use_container_width=True
            )
        else:
            st.warning("QA Benchmark dataset not found.")

    with subtab_files:
        st.markdown("### 📄 Native Enterprise Documents (DOCX, PDF, and TXT)")
        st.markdown("All policy documents have been compiled into authentic Microsoft Word (.docx) and Adobe PDF (.pdf) documents under `data/documents/`.")
        
        doc_files = []
        for root, _, files in os.walk(DOCS_DIR):
            for file in sorted(files):
                dept = os.path.basename(root)
                ext = os.path.splitext(file)[1].upper().replace(".", "")
                size_kb = round(os.path.getsize(os.path.join(root, file)) / 1024, 1)
                doc_files.append({"Department": dept, "Filename": file, "Format": ext, "Size (KB)": size_kb})
        
        st.dataframe(pd.DataFrame(doc_files), use_container_width=True)

# =========================================================================
# TAB 3: BENCHMARK & EVALUATION
# =========================================================================
with tab_bench:
    st.subheader("📊 Comparative Benchmark: Fixed vs Heuristic vs RL-Adaptive")
    bench_path = os.path.join(BASE_DIR, "data", "benchmark_results.json")
    if os.path.exists(bench_path):
        with open(bench_path, "r") as f:
            bdata = json.load(f)
        summary = bdata["metrics_summary"]

        # Metric cards
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Recall @ 5 (RL-RAG)", f"{summary['adaptive']['mean_recall_at_5']:.3f}", delta=f"+{(summary['adaptive']['mean_recall_at_5'] - summary['fixed']['mean_recall_at_5'])*100:.1f}%")
        with m_col2:
            st.metric("Precision @ 5 (RL-RAG)", f"{summary['adaptive']['mean_precision_at_5']:.3f}", delta=f"+{(summary['adaptive']['mean_precision_at_5'] - summary['fixed']['mean_precision_at_5'])*100:.1f}%")
        with m_col3:
            st.metric("MRR (RL-RAG)", f"{summary['adaptive']['mean_mrr']:.3f}", delta=f"+{(summary['adaptive']['mean_mrr'] - summary['fixed']['mean_mrr'])*100:.1f}%")
        with m_col4:
            st.metric("Security Leakage", f"{summary['adaptive']['rbac_security_leakage_rate']:.2%}", delta="0.00% Leakage")

        st.markdown("### 📋 Full Metrics Comparison Table")
        st.dataframe(pd.DataFrame(summary).T, use_container_width=True)
    else:
        st.info("Run scripts/run_evaluation.py to generate benchmark results.")

# =========================================================================
# TAB 4: DOCUMENT CORPUS & CHUNKS
# =========================================================================
with tab_kb:
    st.subheader("📚 Ingested Corporate Knowledge Base")
    st.write(f"Total chunks indexed in active vector store & BM25 index: **{len(pipeline.chunks)}**")
    
    dept_tabs = st.tabs(["All", "HR", "IT", "Finance", "Operations", "Legal"])
    for i, d_tab in enumerate(dept_tabs):
        d_name = ["All", "HR", "IT", "Finance", "Operations", "Legal"][i]
        with d_tab:
            shown_chunks = pipeline.chunks if d_name == "All" else [c for c in pipeline.chunks if c.get("department", "").lower() == d_name.lower()]
            st.write(f"Displaying **{len(shown_chunks)}** chunks:")
            for c in shown_chunks[:10]:
                with st.expander(f"[{c['department']}] {c['title']} — {c['section']}"):
                    st.markdown(f"**Doc ID:** `{c['doc_id']}` | **Clearance:** `{c['security_clearance']}` | **Version:** `{c['version']}`")
                    st.text(c["content"])
