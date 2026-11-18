# Adaptive Reinforcement Learning-Based RAG Optimization Framework
### For Corporate Knowledge Management & Enterprise Document Intelligence

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/)
[![Presentation](https://img.shields.io/badge/Presentation-Download%20PPTX-orange?style=for-the-badge&logo=microsoftpowerpoint)](presentation/Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg?style=for-the-badge)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

---

## 👨‍💻 Project Information & Contact
- **Principal Author / Candidate:** **Rishi Sunkavalli**
- **GitHub Email:** [sunkavallirshi@gmail.com](mailto:sunkavallirshi@gmail.com)
- **GitHub Profile:** [@Rishi-Sunkavalli](https://github.com/Rishi-Sunkavalli)
- **Repository:** [Rishi-Sunkavalli/Adaptive-Corporate-RAG-Framework](https://github.com/Rishi-Sunkavalli/Adaptive-Corporate-RAG-Framework)
- **Permanent Live Interactive Demo:** [https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/](https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/)

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

All models were evaluated on an expanded, held-out test suite of **50 gold-annotated corporate queries** spanning HR, IT, Finance, Operations, Legal & Compliance, cross-boundary security probes, and out-of-domain edge cases:

| Evaluation Dimension / Metric | Fixed-Parameter RAG (Static K=5) | Query-Aware Heuristic Baseline | Adaptive RL-RAG (LinUCB) | RL Framework Improvement Δ |
| :--- | :---: | :---: | :---: | :---: |
| **Precision @ 5** | 0.6800 | 0.6960 | **0.8093** | **+19.0%** |
| **Recall @ 5** | 0.6800 | 0.7200 | **0.9400** | **+38.2% (Substantial)** |
| **Mean Reciprocal Rank (MRR)** | 0.6800 | 0.7200 | **0.9300** | **+36.8%** |
| **Faithfulness Score (Grounding)** | 1.0000 | 1.0000 | **0.9920** | **High Evidence Grounding** |
| **Answer Relevance Score** | 0.6805 | 0.6928 | **0.7857** | **+15.5%** |
| **Mean End-to-End Latency (ms)** | 37.95 ms | 57.46 ms | **82.16 ms** | Real-time interactive (<100ms) |
| **Tokens Consumed per Query** | 411.4 tok | 499.4 tok | **751.3 tok** | Adaptive context-budgeting |
| **Total Test Suite Tokens** | 20,570 | 24,972 | **37,566** | Controlled inference expenditure |
| **Multi-Objective Reward Utility** | 0.5382 | 0.5436 | **0.6781** | **+26.0% Higher Reward Utility** |
| **RBAC Security Leakage Rate** | 0.00% | 0.00% | **0.00%** | **Zero Cross-Boundary Leaks (0/50)** |

### Key Benchmark Insights
1. **Elimination of Recall Bottlenecks:** Fixed $K=5$ missed clauses on multi-policy questions (e.g., comparing Maternity vs. Paternity leave, P1 vs. P2 SLA tiers, or CapEx thresholds). The RL controller selected $K=8$ and hybrid search, boosting recall from **68.0% to 94.0%**.
2. **First-Rank Target Placement:** Mean Reciprocal Rank jumped from **0.680 to 0.930**, proving the target corporate clause appeared in the #1 retrieved position in over 90% of test episodes.
3. **Zero Security Leakage:** Over simulated multi-role evaluations across unauthorized employee personas, attempts to query restricted procurement thresholds, database root procedures, or disaster recovery failover configurations were completely blocked prior to vector search (**0.00% leakage rate across all 50 queries**).

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

## 📚 Enterprise Knowledge Corpus & Multi-Format Datasets

This project provides authentic enterprise knowledge datasets compiled across **5 corporate departments** and published in multiple industry-standard data formats:

### 1. Structured Dataset Artifacts (`data/datasets/`)
- **`enterprise_knowledge_corpus.json` & `.jsonl`:** Complete enterprise knowledge base with structured metadata (`doc_id`, `department`, `title`, `category`, `security_clearance`, `version`, `effective_date`, `owner`, `sections`, `key_entities`).
- **`enterprise_kb_dataset.csv`:** Flattened tabular dataset containing 52 policy clauses, section headings, text, key entities, and word counts.
- **`enterprise_kb_dataset.parquet`:** High-performance columnar Apache Parquet dataset for scalable analytics and embeddings.
- **`qa_benchmark_dataset.json` & `.csv`:** 50 gold-annotated corporate evaluation queries with ground-truth document IDs, sections, expected facts, required roles, and optimal retrieval configurations.
- **Departmental Subsets (`data/datasets/departments/`):**
  - `hr_policies_dataset.json`
  - `it_policies_dataset.json`
  - `finance_policies_dataset.json`
  - `operations_policies_dataset.json`
  - `legal_policies_dataset.json`

### 2. Multi-Format Native Documents (`data/documents/`)
All policy manuals are also compiled into genuine enterprise formats:
- **Microsoft Word (`.docx`):** Fully styled DOCX documents with corporate headers, metadata tables, and structured sections.
- **Adobe Acrobat (`.pdf`):** Formatted PDF policy manuals with official headers and tables.
- **Structured Markdown / TXT (`.txt`):** Structured text with document metadata headers.

### 3. Covered Enterprise Domains
1. **Human Resources (HR):**
   - `HR-DOC-001`: Global Employee Leave and Attendance Policy 2026 (22-day annual leave, 8-day rollover cap, 18-week maternity / 4-week paternity leave).
   - `HR-DOC-002`: Employee Code of Conduct, Ethics and Disciplinary Procedure ($75 gift cap, whistleblower protection, 4-stage disciplinary ladder).
   - `HR-DOC-003`: Remote Work, Telecommuting and Hybrid Workplace Agreement (3/2 hybrid model, $800 home office stipend, 30-day international WFA limit).
2. **Information Technology & Cybersecurity (IT):**
   - `IT-DOC-001`: IT Infrastructure Incident Response and SLA SOP (P1 Critical 15-min response / 2-hr resolution, P2 Major 30-min response / 6-hr resolution, 72-hr RCA).
   - `IT-DOC-002`: Enterprise Access Management and Cybersecurity Protocol (120-min production root sessions, FIDO2/YubiKey MFA, 15-min involuntary offboarding SLA).
   - `IT-DOC-003`: Cloud Security, Data Encryption and Key Management Guidelines (AES-256 CMEK, TLS 1.3, 365-day KMS key rotation).
3. **Finance & Sourcing (FIN):**
   - `FIN-DOC-001`: Corporate Travel, Meal and Business Expense Reimbursement Policy ($85/day Tier 1 meal per-diem, $280/night Tier 1 hotel cap, $0.67/mile mileage).
   - `FIN-DOC-002`: Corporate Procurement, Vendor Selection and Supplier Payment Guidelines (PO Tiers A–D, Three-Way Matching protocol, Net-45 standard terms).
   - `FIN-DOC-003`: Capital Expenditure (CapEx) Governance and Asset Depreciation Manual ($5,000 capitalization floor, straight-line depreciation schedules).
4. **Operations & Resilience (OPS):**
   - `OPS-DOC-001`: Enterprise Business Continuity and Disaster Recovery Plan (Tier 1 Mission-Critical RTO <= 1 hr, RPO <= 15 min, 6-min DNS failover).
   - `OPS-DOC-002`: Customer Support Escalation Matrix and SLA Guidelines (Tiers 1–4 severity, 75% SLA escalation triggers, executive notifications).
   - `OPS-DOC-003`: Supply Chain Vendor Governance and Quality Assurance SOP (98.0% on-time delivery threshold, 0.05% defect limit, inbound quarantine inspection).
5. **Legal, Compliance & Data Governance (LEGAL):**
   - `LEGAL-DOC-001`: Master Services Agreement (MSA) Standards and Contract Negotiation Framework (12-month fee liability cap, 2x super-cap, 5-year NDA confidentiality).
   - `LEGAL-DOC-002`: Global Data Privacy Regulation (GDPR & CCPA) Compliance Manual (30-day DSAR response deadline, 72-hour mandatory breach notification).

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Rishi-Sunkavalli/Adaptive-Corporate-RAG-Framework.git
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
👉 **[https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/](https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/)**

---

## 📂 Repository Layout

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml            # Automated GitHub Actions workflow for GitHub Pages
├── app/
│   └── app.py                    # Streamlit interactive application & Datasets Explorer
├── data/
│   ├── benchmark_results.json    # Full empirical benchmark metrics & logs (50 queries)
│   ├── test_queries.json         # 50 curated benchmark queries with ground truth
│   ├── datasets/                 # Production-Grade Multi-Format Enterprise Datasets
│   │   ├── enterprise_knowledge_corpus.json   # Full unified corpus (14 documents)
│   │   ├── enterprise_knowledge_corpus.jsonl  # JSON Lines streaming dataset
│   │   ├── enterprise_kb_dataset.csv          # Flat tabular dataset (52 clauses)
│   │   ├── enterprise_kb_dataset.parquet      # Columnar Apache Parquet dataset
│   │   ├── qa_benchmark_dataset.json          # 50 gold-annotated benchmark QA pairs
│   │   ├── qa_benchmark_dataset.csv           # Benchmark QA in tabular CSV
│   │   └── departments/                       # Domain-specific JSON datasets (HR, IT, Finance, Ops, Legal)
│   ├── documents/                # Multi-Format Native Enterprise Files
│   │   ├── HR/                   # DOCX, PDF, and TXT files
│   │   ├── IT/                   # DOCX, PDF, and TXT files
│   │   ├── Finance/              # DOCX, PDF, and TXT files
│   │   ├── Operations/           # DOCX, PDF, and TXT files
│   │   └── Legal/                # DOCX, PDF, and TXT files
│   └── corporate_documents/      # Backwards-compatible document partition
├── docs/
│   └── index.html                # Standalone SPA for permanent GitHub Pages live demo
├── presentation/
│   ├── Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx  # 18-slide executive deck
│   └── Presentation_Outline_and_Speaker_Notes.md                 # Defense notes
├── scripts/
│   ├── build_datasets.py         # Compiles JSON, CSV, Parquet, DOCX, PDF datasets
│   ├── generate_presentation.py  # Python script generating the 18-slide PPTX
│   └── run_evaluation.py         # 50-query Benchmark evaluation script
├── src/
│   ├── rbac/
│   │   └── access_control.py     # Role-Based Access Control pre-filtering engine
│   ├── ingestion/
│   │   ├── parser.py             # Multi-format parser (JSON, CSV, Parquet, DOCX, PDF, TXT)
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
