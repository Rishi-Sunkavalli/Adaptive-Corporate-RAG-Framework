# Adaptive Reinforcement Learning-Based RAG Optimization Framework
### For Corporate Knowledge Management & Enterprise Document Intelligence

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://michanagatlayaswanth.github.io/Adaptive-Corporate-RAG-Framework/)
[![Presentation](https://img.shields.io/badge/Presentation-Download%20PPTX-orange?style=for-the-badge&logo=microsoftpowerpoint)](presentation/Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg?style=for-the-badge)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

---

## 👨‍💻 Project Information & Contact
- **Principal Author / Candidate:** **Rishi Sunkavalli**
- **GitHub Email:** [sunkavallirshi@gmail.com](mailto:sunkavallirshi@gmail.com)
- **GitHub Profile:** [@Rishi-Sunkavalli](https://github.com/Rishi-Sunkavalli)
- **Repository:** [MICHANAGATLAYASWANTH/Adaptive-Corporate-RAG-Framework](https://github.com/MICHANAGATLAYASWANTH/Adaptive-Corporate-RAG-Framework)
- **Permanent Live Interactive Demo:** [https://michanagatlayaswanth.github.io/Adaptive-Corporate-RAG-Framework/](https://michanagatlayaswanth.github.io/Adaptive-Corporate-RAG-Framework/)

---

## 📖 Executive Summary & Abstract
Organizations generate and maintain vast amounts of operational knowledge across departments—distributed among HR policies, employee handbooks, IT manuals, travel expense rules, compliance guidelines, standard operating procedures (SOPs), and business continuity plans. Employees routinely spend upwards of 20% of their working hours searching for authoritative guidance.

Conventional Retrieval-Augmented Generation (RAG) frameworks make enterprise files searchable through natural language, but rely on **fixed retrieval parameters**—such as a static Top-K (e.g., $K=5$), fixed similarity thresholds, and a single retriever mode. In practice, enterprise inquiries are highly heterogeneous:
1. **Short factual lookups** (e.g., *"What is the annual leave entitlement?"*) get overwhelmed by unnecessary chunks, driving up latency and token expense.
2. **Complex comparative audits** (e.g., *"Compare P1 Outage vs P2 Degradation SLA response times and escalation ladders"*) miss critical policy clauses due to insufficient retrieval depth.
3. **Alphanumeric lookups** (e.g., *"Tier B $50,000 procurement threshold"*) fail when relying solely on dense vector search.

This project implements an **Adaptive Reinforcement Learning-Based RAG Optimization Framework** that dynamically selects optimal retrieval configurations (Top-K, similarity cutoff, dense vs. hybrid search, and cross-encoder reranking) based on query context features. Evaluated against conventional fixed-parameter RAG and a heuristic baseline across multi-department corporate queries, the proposed RL-driven framework achieves **+39.3% higher Recall@5**, a **0.975 Mean Reciprocal Rank (MRR)**, **100% evidence faithfulness**, and a **+26.1% increase in multi-objective reward utility** while strictly preserving a **0.00% cross-boundary RBAC security leakage rate**.

---

## 🏗️ System Architecture & Workflow

```
+----------------------------------------------------------------------------------------------------+
|                                    ENTERPRISE USER INTERFACE                                       |
|               (Role-Based Personas: General Staff, HR Specialist, IT DevOps, Finance, Ops)        |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                           1. PRE-RETRIEVAL ROLE-BASED ACCESS CONTROL (RBAC)                        |
|   Strict identity & clearance filter: unpermitted departmental manuals are purged before search.   |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                2. QUERY UNDERSTANDING & STATE ANALYZER                             |
|  Extracts query intent (factual, comparative, procedural), complexity, length bin, and department.  |
|  Constructs feature vector: x = [ 1.0, intent_norm, complexity_norm, length_norm, words, dept ]^T  |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                         3. REINFORCEMENT LEARNING CONTROLLER (LinUCB BANDIT)                       |
|   Dynamically selects action: a* = argmax_a [ θ_a^T x + α √(x^T A_a^(-1) x) ]                      |
|   • Top-K ∈ {3, 5, 8}      • Threshold ∈ {0.35, 0.50, 0.65}                                        |
|   • Mode: Dense vs Hybrid   • Cross-Encoder Reranker: On vs Off                                    |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                         4. DUAL-STAGE AUTHORIZED HYBRID RETRIEVAL ENGINE                           |
|   • Dense Vector Search: 384-d semantic embeddings with Cosine similarity                          |
|   • Lexical Search: BM25 Okapi for exact financial/SLA acronyms and policy codes                   |
|   • Reciprocal Rank Fusion (RRF): Score(d) = ∑ w_m / (60 + rank_m(d))                              |
|   • Optional Cross-Encoder Reranker: Joint phrase & section affinity scoring                       |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                         5. GROUNDED GENERATION & CITATION PROVENANCE ENGINE                        |
|   • Refusal Guard: If max similarity < 0.28, outputs explicit insufficient evidence notice.        |
|   • Grounded In-Context Prompting: Restricts answer generation solely to retrieved passages.       |
|   • Verified In-Text Citations: [Document Title | Section Heading | Version | Effective Date]       |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
|                         6. MULTI-OBJECTIVE REWARD EVALUATION & POLICY UPDATE                       |
|   Reward = w1*Relevance + w2*Faithfulness + w3*AnswerRel - w4*(Latency/1.2s) - w5*(Tokens/2k)      |
|   Online updates: A_a ← A_a + x x^T,  b_a ← b_a + r x                                              |
+────────────────────────────────────────────────────────────────────────────────────────────────----+
```

---

## 📊 Empirical Benchmark Evaluation Results

All models were evaluated on a held-out test suite of 20 representative corporate queries spanning HR, IT, Finance, Operations, and out-of-domain edge cases:

| Evaluation Dimension / Metric | Fixed-Parameter RAG (Static K=5) | Query-Aware Heuristic Baseline | Adaptive RL-RAG (LinUCB) | RL Framework Improvement Δ |
| :--- | :---: | :---: | :---: | :---: |
| **Precision @ 5** | 0.7000 | 0.6600 | **0.7625** | **+8.9%** |
| **Recall @ 5** | 0.7000 | 0.7000 | **0.9750** | **+39.3% (Substantial)** |
| **Mean Reciprocal Rank (MRR)** | 0.7000 | 0.7000 | **0.9750** | **+39.3%** |
| **Faithfulness Score (Grounding)** | 1.0000 | 1.0000 | **1.0000** | **100% Grounded** |
| **Answer Relevance Score** | 0.7030 | 0.7160 | **0.8057** | **+14.6%** |
| **Mean End-to-End Latency (ms)** | 39.30 ms | 76.22 ms | **107.82 ms** | Real-time interactive (<150ms) |
| **Tokens Consumed per Query** | 471.8 tok | 599.6 tok | **901.3 tok** | Context-Rich for Comparative Queries |
| **Total Test Suite Tokens** | 9,436 | 11,992 | **18,026** | Controlled inference cost |
| **Multi-Objective Reward Utility** | 0.5550 | 0.5507 | **0.6999** | **+26.1% Higher Reward Utility** |
| **RBAC Security Leakage Rate** | 0.00% | 0.00% | **0.00%** | **Zero Cross-Boundary Leaks** |

### Key Benchmark Insights
1. **Elimination of Recall Bottlenecks:** Fixed $K=5$ missed clauses on multi-policy questions (e.g., comparing Maternity vs. Paternity leave or P1 vs. P2 SLA tiers). The RL controller selected $K=8$ and hybrid search, boosting recall from **70.0% to 97.5%**.
2. **First-Rank Target Placement:** Mean Reciprocal Rank jumped from **0.700 to 0.975**, proving the target corporate clause appeared in the #1 retrieved position in 95% of test episodes.
3. **Zero Security Leakage:** Over 60 simulated multi-role evaluations, unprivileged staff attempts to query restricted procurement thresholds or disaster recovery credentials were completely neutralized prior to vector search (**0.00% leakage rate**).

---

## 🎯 Reinforcement Learning Formulation

### 1. State Space ($s \in \mathcal{S}$)
A 6-dimensional normalized query context vector:
$$x = \begin{bmatrix} 1.0 & \text{Intent}_{\text{norm}} & \text{Complexity}_{\text{norm}} & \text{Length}_{\text{norm}} & \frac{\text{WordCount}}{30} & \text{Domain}_{\text{flag}} \end{bmatrix}^T$$

- **Intent:** Factual (0.2), Policy Verification (0.4), Procedural (0.7), Comparative (1.0).
- **Complexity:** Low (0.2), Medium (0.6), High (1.0).
- **Length Bins:** Short (<10 words), Medium (10-22 words), Long (>22 words).

### 2. Action Space ($a \in \mathcal{A}$)
Combinatorial discrete action space with 24 candidate tuples:
- **Top-K ($K$):** $\{3, 5, 8\}$
- **Similarity Threshold ($\theta$):** $\{0.35, 0.50, 0.65\}$
- **Retrieval Strategy:** $\{\text{Dense Vector}, \text{Hybrid RRF}\}$
- **Reranker:** $\{\text{Disabled}, \text{Cross-Encoder Enabled}\}$

### 3. Multi-Objective Reward Function ($R$)
Balances evidence quality against operational resource consumption:
$$R = w_1 \cdot \text{Relevance} + w_2 \cdot \text{Faithfulness} + w_3 \cdot \text{AnswerRelevance} - w_4 \cdot \left(\frac{\text{Latency}}{1200\text{ms}}\right) - w_5 \cdot \left(\frac{\text{Tokens}}{2000}\right)$$
Calibrated weights: $w_1 = 0.35, w_2 = 0.35, w_3 = 0.15, w_4 = 0.08, w_5 = 0.07$.

### 4. LinUCB Learning Algorithm
For each action $a$, the controller estimates expected reward $\hat{\theta}_a = A_a^{-1} b_a$ and chooses:
$$a^* = \arg\max_{a \in \mathcal{A}} \left( \hat{\theta}_a^T x + \alpha \sqrt{x^T A_a^{-1} x} \right)$$
with online updates:
$$A_a \leftarrow A_a + x x^T, \quad b_a \leftarrow b_a + r x$$

---

## 📚 Corporate Knowledge Base Corpus

The repository includes 8 comprehensive, real-world corporate policy manuals:
- **Human Resources (HR):**
  - `HR_Global_Leave_Attendance_Policy_2026.txt`: Vacation entitlement, sick leave, 18-week maternity / 4-week paternity leave, 8-day rollover cap.
  - `HR_Employee_Code_of_Conduct_Benefits.txt`: Whistleblower protections, medical insurance tiers, dollar-for-dollar 401(k) match up to 5%, remote work stipends.
- **Information Technology (IT):**
  - `IT_Access_Management_Security_Manual.txt`: FIDO2 MFA keys, GlobalProtect VPN, 16-character passwords, 90-day rotation, data classifications (Levels 1–4).
  - `IT_Infrastructure_Incident_Response_SOP.txt`: P1 Critical (15-min SLA), P2 Major (30-min SLA), blameless PIR within 72 hours, 4-hour RTO and 15-minute RPO.
- **Finance & Sourcing:**
  - `Finance_Travel_Expense_Reimbursement_Policy.txt`: Domestic coach vs. transcontinental business flights (>6 hours), per-diem rates ($85/day Tier 1), $300 hotel caps.
  - `Finance_Procurement_Vendor_Payment_Guidelines.txt`: PO tiers (<$5k single quote, $5k–$50k three quotes, >$50k RFP), three-way matching, Net-45 payment terms.
- **Operations & Governance:**
  - `Operations_SOP_Customer_Escalation_Matrix.txt`: Tiers 1–4 support hierarchy, SLA breach triggers, executive notification ladders.
  - `Operations_Business_Continuity_Plan.txt`: Mission-critical Tier 0 systems, crisis command tree, regional remote failover drills.

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/MICHANAGATLAYASWANTH/Adaptive-Corporate-RAG-Framework.git
cd Adaptive-Corporate-RAG-Framework
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Evaluation Benchmark
Executes the side-by-side benchmark comparing Fixed RAG, Heuristic RAG, and Adaptive RL-RAG:
```bash
python scripts/run_evaluation.py
```

### 4. Launch the Interactive Local Application
```bash
streamlit run app/app.py
```
Open your browser at `http://localhost:8501` to test role-based access, inspect RL decisions, and query corporate documents.

### 5. Access the Permanent Live Demo
Visit the GitHub Pages deployment directly in any browser:
👉 **[https://michanagatlayaswanth.github.io/Adaptive-Corporate-RAG-Framework/](https://michanagatlayaswanth.github.io/Adaptive-Corporate-RAG-Framework/)**

---

## 📂 Repository Layout

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml            # Automated GitHub Actions workflow for GitHub Pages
├── app/
│   └── app.py                    # Streamlit interactive application & diagnostics
├── data/
│   ├── benchmark_results.json    # Full empirical benchmark metrics & logs
│   ├── test_queries.json         # 20 curated benchmark queries with ground truth
│   └── corporate_documents/      # Multi-department policy manuals
│       ├── HR/                   # Leave policy & Code of Conduct
│       ├── IT/                   # Access management & Incident Response SOP
│       ├── Finance/              # Travel expense & Procurement guidelines
│       └── Operations/           # Escalation matrix & Business continuity plan
├── docs/
│   └── index.html                # Standalone SPA for permanent GitHub Pages live demo
├── presentation/
│   ├── Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx  # 18-slide executive deck
│   └── Presentation_Outline_and_Speaker_Notes.md                 # Defense notes
├── scripts/
│   ├── generate_presentation.py  # Python script generating the 18-slide PPTX
│   └── run_evaluation.py         # Benchmark execution script
├── src/
│   ├── rbac/
│   │   └── access_control.py     # Role-Based Access Control pre-filtering engine
│   ├── ingestion/
│   │   ├── parser.py             # Metadata and text extractor
│   │   └── chunker.py            # Section-preserving semantic chunker
│   ├── retrieval/
│   │   ├── vector_store.py       # Dense vector index with cosine similarity
│   │   ├── bm25_search.py        # BM25 Okapi lexical retriever
│   │   ├── hybrid_retriever.py   # Dense + BM25 Reciprocal Rank Fusion (RRF)
│   │   └── reranker.py           # Cross-encoder semantic reranker
│   ├── rl_controller/
│   │   ├── state_analyzer.py     # Query feature extraction & state builder
│   │   ├── action_space.py       # Discrete 24-action configuration space
│   │   ├── reward_engine.py      # Multi-objective scalar reward calculator
│   │   └── bandit_agent.py       # LinUCB Contextual Bandit implementation
│   ├── generation/
│   │   └── grounded_generator.py # Strict evidence grounding & in-text citations
│   └── evaluation/
│       ├── metrics.py            # Precision@K, Recall@K, MRR, Faithfulness, RBAC leakage
│       └── benchmark.py          # Comparative evaluation harness
├── index.html                    # Root live demo file for GitHub Pages
├── requirements.txt              # Python library dependencies
├── LICENSE                       # MIT License
└── README.md                     # Comprehensive project documentation
```

---

## 📑 Presentation & Slide Deck
An executive-ready, 18-slide widescreen (16:9) PowerPoint presentation is included directly in this repository:
- **File:** [`presentation/Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx`](presentation/Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx)
- **Speaker Notes & Transcript:** [`presentation/Presentation_Outline_and_Speaker_Notes.md`](presentation/Presentation_Outline_and_Speaker_Notes.md)

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✉️ Author
**Rishi Sunkavalli**  
Email: [sunkavallirshi@gmail.com](mailto:sunkavallirshi@gmail.com)  
GitHub: [Rishi-Sunkavalli](https://github.com/Rishi-Sunkavalli)
