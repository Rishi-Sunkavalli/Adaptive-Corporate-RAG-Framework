# Adaptive Corporate RAG Framework
## Final Year Project Presentation: Outline & Speaker Notes
**Author:** Rishi Sunkavalli  
**Contact Email:** sunkavallirshi@gmail.com  
**GitHub Repository:** [Adaptive-Corporate-RAG-Framework](https://github.com/Rishi-Sunkavalli/Adaptive-Corporate-RAG-Framework)  
**Live Web Deployment:** [Permanent GitHub Pages Demo](https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/)  
**Presentation File:** `presentation/Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx` (18 Slides, 16:9 Widescreen)

---

### Slide 1: Title Slide & Project Identification
- **Title:** Adaptive Reinforcement Learning-Based RAG Optimization Framework for Corporate Knowledge Management
- **Subtitle:** Enterprise Document Intelligence, Dynamic Contextual Bandit Optimization, and Grounded Generation
- **Presenter:** Rishi Sunkavalli (`sunkavallirshi@gmail.com`)
- **Key Talking Points:**
  - Welcome the committee and stakeholders.
  - Introduce the core vision: moving beyond brittle, static retrieval parameters in enterprise AI assistants by formulating retrieval configuration selection as an online Reinforcement Learning problem.

---

### Slide 2: Executive Summary & Project Motivation
- **Corporate Knowledge Silos:** Organizations maintain vast, unstructured repositories across HR, IT, Finance, and Operations.
- **Search Latency & Lost Productivity:** Employees spend roughly 20-25% of their working hours searching for accurate corporate policies.
- **Why RAG Needs Adaptivity:** Fixed Top-K and static similarity cutoffs lead to either missing critical clauses or stuffing unnecessary noise into the prompt.

---

### Slide 3: Enhanced Problem Statement
- **Distributed & Overlapping Policies:** Corporate rules evolve rapidly across versions, creating conflicting interpretations.
- **The Pitfall of Uniform Retrieval:** Factual questions require minimal focused context, whereas comparative and workflow queries require broad, multi-document synthesis.
- **Token Inflation & Hallucination Risk:** Excess chunks drive up inference costs and distract LLMs; missing evidence triggers hallucinations unless rigorous refusal guards are established.
- **Security Boundaries:** Unrestricted enterprise search risks exposing confidential executive, financial, or disaster recovery data to unprivileged staff.

---

### Slide 4: Limitations of Conventional Fixed-Parameter RAG
- **Static Top-K (K=5):** Fixed depth fails to adapt to query variance.
- **Static Similarity Thresholds:** Fixed cutoff (e.g. 0.50) admits noise on broad queries or excludes vital passages on specific vocabulary.
- **Dense-Only Search Blindspots:** Dense vector embeddings struggle with exact alphanumeric codes, policy numbers, and financial tiers.
- **Proposed Adaptive Framework:** Query-aware dynamic K ∈ {3, 5, 8}, adaptive similarity thresholds, hybrid BM25 + dense search, and cross-encoder reranking.

---

### Slide 5: Research Aim & Specific Objectives
- **Aim:** To design, implement, and evaluate an adaptive corporate knowledge assistant that uses Reinforcement Learning to optimize RAG retrieval configurations, improving relevance, grounding, and computational efficiency.
- **8 Objectives:** Ingestion pipeline, vector/lexical indexing, RBAC security, state feature extraction, discrete action space, multi-objective reward formulation, grounded generation with citations, and empirical benchmarking.

---

### Slide 6: End-to-End System Architecture
- **Step 1:** Employee submits query & RBAC pre-filter restricts searchable documents.
- **Step 2:** Query State Analyzer extracts intent, length bin, complexity, and department.
- **Step 3:** LinUCB RL Controller selects action tuple `(Top-K, threshold, search_mode, rerank)`.
- **Step 4:** Hybrid Retriever executes vector search + BM25 with Reciprocal Rank Fusion (RRF).
- **Step 5:** Grounded LLM synthesizes response with verified citations and evaluates multi-objective reward to update bandit weights.

---

### Slide 7: Enterprise Knowledge Corpus & Multi-Format Datasets
- **5 Departments & 14 Policies:**
  - **HR:** Global Leave Policy, Code of Conduct & Ethics, Remote Work & Ergonomic Stipend.
  - **IT:** Infrastructure Incident Response SOP, Access Management & Root Protocol, Cloud Encryption & KMS Key Rotation.
  - **Finance:** Travel Expense Reimbursement, Procurement & 3-Way Matching, CapEx Asset Depreciation.
  - **Operations:** Business Continuity Plan, Customer Support Escalation Matrix, Supply Chain Vendor Quality SOP.
  - **Legal & Governance:** Master Services Agreement (MSA) Standards, GDPR & CCPA Data Privacy Manual.
- **Multi-Format Datasets:** Provided in JSON, JSONL, CSV, Apache Parquet, Word DOCX, and Adobe PDF.
- **RBAC Matrix:** Pre-retrieval role filtration ensures general staff cannot query restricted financial procurement, infrastructure root access, or disaster recovery documents.

---

### Slide 8: Multi-Format Ingestion & Hybrid Retrieval Engine
- **Multi-Format Parsing:** Native parsers for structured datasets (JSON, CSV, Parquet) and document binaries (Word DOCX, Adobe PDF, and TXT).
- **Semantic Chunking:** 180 words per chunk with 30-word overlap, preserving section headings, table entities, and document breadcrumbs.
- **Hybrid Retrieval:** Dense 384-d semantic vectors combined with BM25 Okapi lexical scoring via Reciprocal Rank Fusion (RRF constant k=60).
- **Cross-Encoder Reranker:** Evaluates term proximity, bigram overlap, and section affinity for complex comparative queries.

---

### Slide 9: Query Analysis & State Representation
- **State Features (d=6):**
  - Intent: Factual, Numeric/Lookup, Procedural, Comparative, Policy Verification, Security Probes, and Refusal Guards.
  - Length Bins: Short (<10 words), Medium (10-22 words), Long (>22 words).
  - Complexity: Low, Medium, High.
  - Department signals: HR, IT, Finance, Operations, Legal, General.
- **Feature Vector:** `x = [1.0, intent_norm, complexity_norm, length_norm, scaled_words, domain_flag]^T`.

---

### Slide 10: Reinforcement Learning Controller: LinUCB Formulation
- **Action Space:** 24 discrete action combinations across Top-K ∈ {3, 5, 8}, threshold ∈ {0.35, 0.50, 0.65}, search mode ∈ {dense, hybrid}, reranking ∈ {off, on}.
- **Decision Rule:** $a^* = \arg\max_a \left[ \theta_a^T x + \alpha \sqrt{x^T A_a^{-1} x} \right]$.
- **Exploration Parameter:** $\alpha = 0.60$ for optimal exploration-exploitation balance.

---

### Slide 11: Multi-Objective Reward Function Formulation
- **Formula:**
  $$\text{Reward} = w_1 \cdot \text{Relevance} + w_2 \cdot \text{Faithfulness} + w_3 \cdot \text{AnswerRelevance} - w_4 \cdot \frac{\text{Latency}}{1200\text{ms}} - w_5 \cdot \frac{\text{Tokens}}{2000}$$
- **Weights:** $w_1 = 0.35, w_2 = 0.35, w_3 = 0.15, w_4 = 0.08, w_5 = 0.07$.

---

### Slide 12: Evidence-Grounded Answer Generation & Citation Engine
- **Strict Grounding:** Generates answers solely from authorized retrieved chunks.
- **Insufficient Evidence Refusal:** If confidence < 0.28, system outputs explicit disclaimer rather than hallucinating unapproved internal guidance.
- **In-Text Citations:** Traceable references including Document ID, Title, Section, Version, and Effective Date.

---

### Slide 13: Experimental Design & Comparative Methodology
- **Held-Out Test Queries:** 50 gold-annotated corporate questions covering factual, comparative, procedural, numeric/lookup, RBAC security probes, and out-of-domain edge cases.
- **Evaluated Baselines:**
  1. Fixed-Parameter RAG (Static K=5, threshold=0.50, dense search).
  2. Query-Aware Heuristic Baseline (Rule-based switching).
  3. Proposed Adaptive RL-RAG (LinUCB Contextual Bandit).

---

### Slide 14: Empirical Benchmark Results (50 Test Queries)
| Metric / Dimension | Fixed RAG (K=5) | Heuristic Baseline | Adaptive RL-RAG | RL Improvement Δ |
| :--- | :--- | :--- | :--- | :--- |
| **Precision @ 5** | 0.6800 | 0.6960 | **0.8093** | **+19.0%** |
| **Recall @ 5** | 0.6800 | 0.7200 | **0.9400** | **+38.2% (Substantial)** |
| **Mean Reciprocal Rank (MRR)** | 0.6800 | 0.7200 | **0.9300** | **+36.8%** |
| **Faithfulness Score** | 1.0000 | 1.0000 | **0.9920** | **High Evidence Grounding** |
| **Answer Relevance** | 0.6805 | 0.6928 | **0.7857** | **+15.5%** |
| **Mean Latency (ms)** | 37.95 ms | 57.46 ms | **82.16 ms** | Real-time interactive (<100ms) |
| **Multi-Objective Reward** | 0.5382 | 0.5436 | **0.6781** | **+26.0% Higher Utility** |
| **RBAC Security Leakage** | 0.00% | 0.00% | **0.00%** | **Zero Security Leaks (0/50)** |

---

### Slide 15: Security & Role-Based Access Control (RBAC) Validation
- **Pre-Retrieval Isolation:** Unauthorized chunks are purged prior to similarity scoring.
- **Empirical Security Probe:** Simulated unauthorized queries across general staff and departmental personas confirmed a **0.00% cross-boundary leakage rate** across 60 trials.

---

### Slide 16: Key Findings, Trade-Offs & Discussion
- **Hybrid Search Superiority:** BM25 lexical search is essential for alphanumeric codes, SLA names, and currency numbers.
- **Recall vs. Cost Trade-Off:** The controller selectively expands Top-K to 8 only for complex multi-policy comparisons, keeping overall latency under 110ms.
- **Selective Reranking:** The bandit avoids activating cross-encoders for simple factual lookups, saving significant compute.

---

### Slide 17: Future Research & Enterprise Roadmap
- **Deep RL:** Transitioning from linear bandits to Deep Q-Networks (DQN) for multi-turn stateful dialogue.
- **Implicit Feedback:** Leveraging employee dwell time, copy actions, and feedback ratings.
- **Multimodal Documents:** Parsing tables, architecture diagrams, and workflow charts.
- **Scale:** Distributed vector indexing for 100k+ enterprise manuals.

---

### Slide 18: Summary of Deliverables & Conclusion
- **Complete Python Codebase:** Ingestion, vector store, BM25, hybrid retrieval, LinUCB bandit, grounded generator, benchmark evaluation, and Streamlit app.
- **Permanent Live Demo:** Hosted on GitHub Pages at `https://rishi-sunkavalli.github.io/Adaptive-Corporate-RAG-Framework/`.
- **PowerPoint Presentation:** `Adaptive_Corporate_RAG_Framework_Final_Presentation.pptx` uploaded to the repository.
