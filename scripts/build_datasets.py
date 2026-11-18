"""
Enterprise Dataset Generator for Adaptive Corporate RAG Framework.
Generates comprehensive corporate datasets across 5 enterprise domains:
1. Human Resources (HR)
2. Finance & Procurement (FIN)
3. Information Technology & Cybersecurity (IT)
4. Operations & Business Continuity (OPS)
5. Legal, Contracts & Regulatory Governance (LEGAL)

Outputs structured datasets in multiple formats:
- JSON & JSONL (data/datasets/enterprise_knowledge_corpus.json & .jsonl)
- CSV (data/datasets/enterprise_kb_dataset.csv)
- Apache Parquet (data/datasets/enterprise_kb_dataset.parquet)
- Departmental JSON bundles (data/datasets/departments/*.json)
- Multi-format enterprise files (.docx, .pdf, .txt) under data/documents/
- Expanded 50-Query QA Benchmark Dataset (qa_benchmark_dataset.json & .csv)
"""

import os
import sys
import json
import pandas as pd
from typing import List, Dict, Any

# Document creation tools
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "data", "datasets")
DEPTS_DIR = os.path.join(DATASETS_DIR, "departments")
DOCS_DIR = os.path.join(BASE_DIR, "data", "documents")

os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(DEPTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# Define the complete enterprise corpus
ENTERPRISE_DOCUMENTS = [
    # =========================================================================
    # 1. HUMAN RESOURCES
    # =========================================================================
    {
        "doc_id": "HR-DOC-001",
        "title": "Global Employee Leave and Attendance Policy 2026",
        "department": "HR",
        "category": "Policy & Benefits",
        "security_clearance": "Internal",
        "version": "4.2",
        "effective_date": "2026-01-01",
        "owner": "Global Human Resources Operations",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Purpose and Scope",
                "content": "This policy establishes standard corporate standards governing annual leave, medical absence, parental leave, bereavement, and public holidays for all permanent full-time and contracted employees across all worldwide subsidiaries. All leave requests must be logged through the Corporate HRMS portal.",
                "key_entities": ["Corporate HRMS", "All subsidiaries", "Annual leave", "Medical absence"]
            },
            {
                "section_number": "2",
                "section_title": "2. Working Hours and Core Collaboration Window",
                "content": "Standard operational hours are 40 hours per week, Monday through Friday. Core collaborative business hours are 10:00 AM to 4:00 PM local office time, during which all active employees are expected to be reachable via Slack and email unless pre-approved for flexible asynchronous schedules.",
                "key_entities": ["40 hours per week", "10:00 AM to 4:00 PM", "Slack", "Email"]
            },
            {
                "section_number": "3",
                "section_title": "3. Annual Leave Entitlement",
                "content": "Regular full-time employees accrue 22 days of paid annual leave per calendar year, accruing monthly at the rate of 1.83 days per completed month of service. A maximum of 8 unused annual leave days can be rolled over into the succeeding calendar year. Any carried-over leave must be fully utilized prior to March 31st; unutilized rollover balances are permanently forfeited without financial encashment.",
                "key_entities": ["22 days of paid annual leave", "1.83 days per month", "8 unused annual leave days", "March 31st", "Forfeited"]
            },
            {
                "section_number": "4",
                "section_title": "4. Sick and Medical Leave",
                "content": "Employees are granted 12 days of fully paid medical and sick leave per annum. Any sick leave extending beyond two consecutive working days requires the submission of a medical certificate issued by a licensed medical practitioner within 48 hours of returning to duty. Medical leave does not roll over to subsequent years.",
                "key_entities": ["12 days paid medical leave", "two consecutive working days", "licensed medical practitioner", "48 hours"]
            },
            {
                "section_number": "5",
                "section_title": "5. Parental, Maternity, and Paternity Leave",
                "content": "Primary caregivers (maternity leave) are entitled to 18 weeks of fully paid leave upon the birth or legal adoption of a child under 5 years old. Secondary caregivers (paternity leave) are entitled to 4 weeks of fully paid leave. Employees may request an additional 4 weeks of unpaid parental leave with HR Director approval.",
                "key_entities": ["Primary Caregiver / Maternity: 18 weeks", "Secondary Caregiver / Paternity: 4 weeks", "unpaid 4 weeks", "HR Director approval"]
            },
            {
                "section_number": "6",
                "section_title": "6. Compassionate and Bereavement Leave",
                "content": "Employees may take up to 5 consecutive paid working days for the loss of an immediate family member (spouse, child, parent, sibling). For extended relatives (grandparent, in-laws), 3 paid working days are granted. International travel allowances for bereavement require People Partner clearance.",
                "key_entities": ["5 consecutive paid working days", "immediate family", "3 paid working days", "extended relatives"]
            }
        ]
    },
    {
        "doc_id": "HR-DOC-002",
        "title": "Employee Code of Conduct, Ethics and Disciplinary Procedure",
        "department": "HR",
        "category": "Governance & Compliance",
        "security_clearance": "Internal",
        "version": "3.1",
        "effective_date": "2026-01-01",
        "owner": "Chief People Officer & Legal Compliance",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Corporate Values and Professional Integrity",
                "content": "Employees must conduct all business interactions with honesty, integrity, transparency, and respect. Harassment, discrimination, bullying, or retaliation of any kind is strictly prohibited and results in immediate disciplinary review under corporate zero-tolerance mandates.",
                "key_entities": ["Zero-tolerance", "Professional integrity", "Anti-harassment"]
            },
            {
                "section_number": "2",
                "section_title": "2. Conflict of Interest Guidelines",
                "content": "Employees must not engage in outside commercial activities or employment that compete directly with company business or compromise company duties. Outside board memberships, commercial consultancies, or investments exceeding 1% in direct vendor entities must be formally disclosed via the Annual Ethics Declaration portal.",
                "key_entities": ["Annual Ethics Declaration", "1% vendor investment", "Outside consultancies"]
            },
            {
                "section_number": "3",
                "section_title": "3. Gift and Hospitality Policy",
                "content": "Employees may accept non-cash promotional gifts valued below $75 USD without prior approval. Any gift, entertainment, meal, or hospitality valued between $75 and $250 USD must be reported to the Department Head. Acceptance of gifts exceeding $250 USD, or any cash or cash-equivalent gift (gift cards, securities) regardless of denomination, is strictly prohibited.",
                "key_entities": ["$75 USD non-cash gift", "$75 to $250 USD reportable", "gifts exceeding $250 strictly prohibited", "cash strictly prohibited"]
            },
            {
                "section_number": "4",
                "section_title": "4. Whistleblower Protection and Reporting Channels",
                "content": "Employees who observe unethical, unlawful, or fraudulent conduct can submit confidential or anonymous disclosures through the Ethics Helpline portal or email ethics-hotline@company.internal. Retaliation against any employee making a good-faith report is illegal and causes immediate dismissal.",
                "key_entities": ["Ethics Helpline portal", "ethics-hotline@company.internal", "Strict anti-retaliation", "Immediate dismissal"]
            },
            {
                "section_number": "5",
                "section_title": "5. Disciplinary Ladder and Sanctions",
                "content": "Violations are adjudicated via a 4-step progressive disciplinary process: 1. Documented Verbal Warning; 2. Written Reprimand placed in personnel file; 3. Suspension without pay (up to 14 days); 4. Termination for cause with loss of severance eligibility.",
                "key_entities": ["Verbal Warning", "Written Reprimand", "Suspension without pay (up to 14 days)", "Termination for cause"]
            }
        ]
    },
    {
        "doc_id": "HR-DOC-003",
        "title": "Remote Work, Telecommuting and Hybrid Workplace Agreement",
        "department": "HR",
        "category": "Workplace Arrangements",
        "security_clearance": "Internal",
        "version": "2.0",
        "effective_date": "2026-02-01",
        "owner": "Global Workplace Experience & HR",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Hybrid Work Model Eligibility",
                "content": "Full-time employees whose job functions do not mandate physical on-site presence (such as data center operators and facilities engineers) may adopt a 3/2 hybrid model: a minimum of 3 days working from the designated company regional office and up to 2 days working remotely each work week.",
                "key_entities": ["3/2 hybrid model", "3 days in office", "2 days remote"]
            },
            {
                "section_number": "2",
                "section_title": "2. Home Office Ergonomic Stipend",
                "content": "New full-time remote or hybrid employees are provided a one-time home office setup reimbursement of up to $800 USD within their first 90 days of employment. Eligible items include ergonomic chairs, external monitors, adjustable desk converters, and noise-canceling headsets.",
                "key_entities": ["$800 USD home office stipend", "first 90 days", "ergonomic chair", "external monitors"]
            },
            {
                "section_number": "3",
                "section_title": "3. Work From Anywhere (WFA) International Travel Limit",
                "content": "Employees may request to work remotely from an approved international country for up to 30 cumulative calendar days per calendar year. Requests must be logged 21 business days in advance to evaluate cross-border corporate tax presence and visa compliance.",
                "key_entities": ["30 cumulative calendar days", "21 business days notice", "international remote work", "tax compliance"]
            }
        ]
    },

    # =========================================================================
    # 2. INFORMATION TECHNOLOGY & CYBERSECURITY
    # =========================================================================
    {
        "doc_id": "IT-DOC-001",
        "title": "IT Infrastructure Incident Response and Service Level Agreement SOP",
        "department": "IT",
        "category": "Infrastructure & Operations",
        "security_clearance": "Internal",
        "version": "5.0",
        "effective_date": "2026-01-15",
        "owner": "IT Infrastructure & Cloud Reliability Engineering",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Incident Classification and Severity Levels",
                "content": "IT production incidents are classified into 4 standardized severity tiers: P1 (Critical Outage: Core customer-facing services or entire enterprise network down); P2 (Major Degradation: Vital service heavily impaired with no viable workaround); P3 (Moderate Impact: Non-critical feature failure affecting limited users); P4 (Minor Request: Routine inquiry, documentation bug, or non-urgent config change).",
                "key_entities": ["P1 Critical Outage", "P2 Major Degradation", "P3 Moderate Impact", "P4 Minor Request"]
            },
            {
                "section_number": "2",
                "section_title": "2. SLA Response and Resolution Targets",
                "content": "Mandatory SLAs are defined as follows: P1 Critical incidents require initial acknowledgment within 15 minutes and target resolution or failover within 2 hours. P2 Major incidents require acknowledgment within 30 minutes and target resolution within 6 hours. P3 incidents require acknowledgment within 4 business hours and resolution within 24 hours. P4 requests require response within 8 business hours and resolution within 5 business days.",
                "key_entities": ["P1: 15 min response / 2 hr resolution", "P2: 30 min response / 6 hr resolution", "P3: 4 hr response / 24 hr resolution", "P4: 8 hr response / 5 business days"]
            },
            {
                "section_number": "3",
                "section_title": "3. Critical Outage (P1) Escalation Ladder",
                "content": "When a P1 incident is declared: at T+0, Incident Commander activates War Room bridge and PagerDuty alert. At T+15m, first status bulletin posted to status.company.internal. At T+30m with no resolution, Director of Infrastructure notified. At T+60m without root cause containment, Chief Information Officer (CIO) and VP of Engineering are briefed. Executive stakeholder updates occur every 30 minutes thereafter.",
                "key_entities": ["T+0 War Room bridge", "T+15m status bulletin", "T+30m Director notification", "T+60m CIO and VP briefing", "status.company.internal"]
            },
            {
                "section_number": "4",
                "section_title": "4. Post-Incident Review and RCA Requirements",
                "content": "For every P1 and P2 incident, an engineering blameless Post-Incident Review (PIR) must be completed within 72 hours of incident resolution. The resulting Root Cause Analysis (RCA) document must identify root causes, 5 Whys, timeline, and corrective preventive actions assigned with explicit JIRA owners.",
                "key_entities": ["72 hours post-incident review", "Root Cause Analysis (RCA)", "5 Whys", "Blameless post-mortem"]
            }
        ]
    },
    {
        "doc_id": "IT-DOC-002",
        "title": "Enterprise Access Management and Cybersecurity Protocol Manual",
        "department": "IT",
        "category": "Information Security & IAM",
        "security_clearance": "Confidential",
        "version": "4.4",
        "effective_date": "2026-01-01",
        "owner": "Chief Information Security Officer (CISO) Directorate",
        "allowed_roles": ["IT_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Principle of Least Privilege and Role-Based Access Control",
                "content": "Access to enterprise systems, production databases, and cloud infrastructure follows the Principle of Least Privilege. Access is granted strictly based on documented job responsibilities and must be approved by the system owner and employee line manager before provisioning. Blanket or wild-card permissions are prohibited.",
                "key_entities": ["Principle of Least Privilege", "Role-Based Access Control (RBAC)", "System owner approval", "No blanket permissions"]
            },
            {
                "section_number": "2",
                "section_title": "2. Production Database and Root Access Provisioning",
                "content": "Direct root or write access to production database clusters (PostgreSQL, BigQuery, Snowflake) is strictly restricted to senior reliability engineers during active emergency maintenance windows. Access requires a dual-authorization ticket in ServiceNow, approved by the Security Lead. All root sessions are screen-recorded and auto-terminated after a maximum duration of 120 minutes.",
                "key_entities": ["ServiceNow dual-authorization", "Production database", "Screen-recorded sessions", "120 minutes maximum duration", "Security Lead approval"]
            },
            {
                "section_number": "3",
                "section_title": "3. Multi-Factor Authentication (MFA) Standards",
                "content": "FIDO2 WebAuthn hardware security keys (e.g. YubiKey) or managed enterprise authenticator applications with number matching are mandatory for all employees. SMS-based OTP is deprecated and rejected for production server authentication. Passwords must contain a minimum of 16 characters and expire every 90 days for privileged administrative accounts.",
                "key_entities": ["FIDO2 WebAuthn / YubiKey", "Number matching", "SMS OTP deprecated", "16 characters min", "90 days expiration for privileged"]
            },
            {
                "section_number": "4",
                "section_title": "4. Offboarding and Emergency Access Revocation",
                "content": "Upon notification of an involuntary employee termination, IT Security must execute immediate automated access revocation across Okta SSO, Google Workspace, GitHub Enterprise, AWS IAM, and VPN within 15 minutes of HR notice. For voluntary resignations, revocation is scheduled for 5:00 PM local time on the employee's final business day.",
                "key_entities": ["15 minutes immediate revocation for involuntary", "Okta SSO / AWS IAM", "5:00 PM on final day for voluntary"]
            }
        ]
    },
    {
        "doc_id": "IT-DOC-003",
        "title": "Cloud Security, Data Encryption and Key Management Guidelines",
        "department": "IT",
        "category": "Security Engineering",
        "security_clearance": "Confidential",
        "version": "2.2",
        "effective_date": "2026-02-15",
        "owner": "Cloud Security Architecture",
        "allowed_roles": ["IT_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Encryption at Rest Standards",
                "content": "All data stored in enterprise cloud storage buckets (AWS S3, Google Cloud Storage, Azure Blob) and relational databases must be encrypted at rest using AES-256 or customer-managed encryption keys (CMEK) managed via Cloud KMS. Unencrypted storage buckets are blocked automatically by Sentinel guardrails.",
                "key_entities": ["AES-256", "Customer-Managed Encryption Keys (CMEK)", "Cloud KMS", "Sentinel guardrails"]
            },
            {
                "section_number": "2",
                "section_title": "2. Encryption in Transit Protocols",
                "content": "All network communications traversing external networks or inter-service VPC perimeters must enforce TLS 1.3 encryption (TLS 1.2 minimum). Deprecated cipher suites (TLS 1.0, 1.1, SSLv3, RC4) are blocked at the perimeter API Gateway and Cloudflare Edge.",
                "key_entities": ["TLS 1.3", "TLS 1.2 minimum", "API Gateway", "Cloudflare Edge"]
            },
            {
                "section_number": "3",
                "section_title": "3. Cryptographic Key Rotation Schedules",
                "content": "Master KMS keys for database and token encryption must undergo automated key rotation every 365 days. Data encryption keys (DEKs) for sensitive financial records must be regenerated at least every 90 days. Key export is strictly disabled across all KMS HSM instances.",
                "key_entities": ["365 days KMS key rotation", "90 days DEK regeneration", "HSM hardware protection"]
            }
        ]
    },

    # =========================================================================
    # 3. FINANCE & PROCUREMENT
    # =========================================================================
    {
        "doc_id": "FIN-DOC-001",
        "title": "Corporate Travel, Meal and Business Expense Reimbursement Policy",
        "department": "Finance",
        "category": "Expense Management",
        "security_clearance": "Internal",
        "version": "6.0",
        "effective_date": "2026-01-01",
        "owner": "Global Financial Operations & Accounting",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Purpose and Expense Submission Timeline",
                "content": "This policy governs the reimbursement of travel, lodging, meals, and business entertainment incurred during company business. All expense claims must be submitted via the Concur Expense portal within 30 calendar days of expense incurrence. Claims submitted beyond 60 days require VP Finance authorization.",
                "key_entities": ["Concur Expense portal", "30 calendar days submission", "60 days requires VP Finance authorization"]
            },
            {
                "section_number": "2",
                "section_title": "2. Commercial Airfare Class Standards",
                "content": "Employees traveling on domestic flights or international flights under 6 hours duration must book Economy Class. Business Class bookings are permitted only for nonstop flight legs exceeding 6 continuous flight hours, or when medically necessary with Occupational Health documentation and CFO sign-off.",
                "key_entities": ["Economy Class under 6 hours", "Business Class over 6 hours", "CFO sign-off"]
            },
            {
                "section_number": "3",
                "section_title": "3. Hotel Nightly Lodging Caps",
                "content": "Maximum allowable nightly hotel rates (excluding local taxes) are categorized by geographic tier: Tier 1 High-Cost Metro Areas (New York, London, San Francisco, Tokyo, Singapore): $280 USD per night. Tier 2 Standard Metro Areas: $190 USD per night. Tier 3 Regional Cities: $140 USD per night. Bookings exceeding caps by more than 15% require Department VP pre-approval.",
                "key_entities": ["Tier 1: $280 USD/night", "Tier 2: $190 USD/night", "Tier 3: $140 USD/night", "15% variance requires VP approval"]
            },
            {
                "section_number": "4",
                "section_title": "4. Daily Per-Diem Meal Allowances",
                "content": "Employees are provided daily per-diem meal allowances as follows: Tier 1 Cities: $85 USD per full travel day ($20 Breakfast, $25 Lunch, $40 Dinner). Tier 2 and Tier 3 Cities: $65 USD per full travel day ($15 Breakfast, $20 Lunch, $30 Dinner). Itemized receipts are mandatory for any individual business meal or transaction exceeding $25 USD. Alcohol is not reimbursable without client presence.",
                "key_entities": ["Tier 1: $85 USD daily per-diem", "Tier 2/3: $65 USD daily per-diem", "receipts mandatory over $25 USD", "Alcohol restricted"]
            },
            {
                "section_number": "5",
                "section_title": "5. Ground Transportation and Personal Mileage",
                "content": "Use of rideshare (Uber/Lyft Standard) and public rapid transit is encouraged. Luxury or Black car services are non-reimbursable. Personal vehicle mileage for business travel is reimbursed at the statutory rate of $0.67 USD per mile, excluding regular daily home-to-office commutes.",
                "key_entities": ["Uber/Lyft Standard", "$0.67 USD per mile", "No luxury car service"]
            }
        ]
    },
    {
        "doc_id": "FIN-DOC-002",
        "title": "Corporate Procurement, Vendor Selection and Supplier Payment Guidelines",
        "department": "Finance",
        "category": "Procurement & Treasury",
        "security_clearance": "Confidential",
        "version": "4.5",
        "effective_date": "2026-01-01",
        "owner": "Director of Global Strategic Sourcing",
        "allowed_roles": ["Finance_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Purchase Order (PO) Thresholds and Approval Ladder",
                "content": "All vendor purchases exceeding $2,500 USD require an approved Purchase Order before contract signing or service commencement. Approval limits are structured as follows: Tier A (Up to $10,000 USD): Department Manager approval; Tier B ($10,001 to $50,000 USD): Department Director approval; Tier C ($50,001 to $250,000 USD): VP and Head of Procurement approval; Tier D (Exceeding $250,000 USD): Chief Financial Officer (CFO) and Chief Executive Officer (CEO) formal sign-off.",
                "key_entities": ["PO required over $2,500 USD", "Tier A: up to $10,000", "Tier B: $10,001 to $50,000", "Tier C: $50,001 to $250,000", "Tier D: >$250,000 CFO & CEO"]
            },
            {
                "section_number": "2",
                "section_title": "2. Competitive Bidding and RFP Requirements",
                "content": "For any procurement contract with an aggregate contract value exceeding $50,000 USD, the procurement team must solicit a minimum of three independent, sealed competitive bids (RFP/RFQ). Single-source or sole-source exemptions require a formally documented Sole Source Justification memo approved by the General Counsel.",
                "key_entities": ["Exceeding $50,000 USD", "three independent competitive bids", "Sole Source Justification memo", "General Counsel approval"]
            },
            {
                "section_number": "3",
                "section_title": "3. Three-Way Matching Verification Protocol",
                "content": "Accounts Payable enforces strict Three-Way Matching before any vendor invoice is disbursed. The accounts payable system automatically cross-references: 1. The approved Purchase Order; 2. The Goods Received Note (GRN) or signed milestone proof-of-performance; 3. The vendor's itemized commercial tax invoice. Payment is halted automatically if price variance exceeds 1.5% or quantity exceeds 0%.",
                "key_entities": ["Three-Way Matching", "Purchase Order (PO)", "Goods Received Note (GRN)", "Vendor tax invoice", "1.5% price variance limit"]
            },
            {
                "section_number": "4",
                "section_title": "4. Standard Payment Terms and Wire Transfer Anti-Fraud",
                "content": "Corporate standard payment terms are Net 45 days from the receipt of a verified invoice. Net 30 or Net 15 terms require Treasury Director sign-off. Wire transfer bank routing changes requested by any vendor require telephone callback verification to the verified vendor finance officer on record before updating banking records.",
                "key_entities": ["Net 45 days standard", "Telephone callback verification", "Anti-fraud protocol", "Treasury Director sign-off"]
            }
        ]
    },
    {
        "doc_id": "FIN-DOC-003",
        "title": "Capital Expenditure (CapEx) Governance and Asset Depreciation Manual",
        "department": "Finance",
        "category": "Corporate Accounting",
        "security_clearance": "Confidential",
        "version": "3.0",
        "effective_date": "2026-01-20",
        "owner": "Corporate Controller & Capital Budgeting Committee",
        "allowed_roles": ["Finance_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Capital Expenditure Definition and Capitalization Floor",
                "content": "Tangible assets or software development expenditures with an acquisition cost of $5,000 USD or greater and an estimated useful operational lifespan exceeding 12 months must be capitalized as fixed assets rather than expensed as operating expenditure (OpEx). Items under $5,000 are expensed immediately.",
                "key_entities": ["$5,000 USD capitalization floor", "12 months useful life", "CapEx vs OpEx"]
            },
            {
                "section_number": "2",
                "section_title": "2. CapEx Budget Authorization Matrix",
                "content": "CapEx projects between $50,000 and $200,000 require Capital Budgeting Committee approval and a Return on Investment (ROI) payback period under 36 months. Projects exceeding $500,000 require Board of Directors Audit Committee ratification.",
                "key_entities": ["$50,000 to $200,000 CapEx", "36 months ROI payback", "Board of Directors Audit Committee over $500,000"]
            },
            {
                "section_number": "3",
                "section_title": "3. Asset Depreciation Schedules",
                "content": "Depreciation is recognized using the straight-line method over statutory useful lives: Computer Hardware & Servers: 3 years (36 months); Enterprise Software Licenses: 5 years (60 months); Office Furniture and Fixtures: 7 years; Leasehold Improvements: Lesser of 10 years or remaining lease term.",
                "key_entities": ["Straight-line depreciation", "Servers: 3 years", "Software: 5 years", "Furniture: 7 years"]
            }
        ]
    },

    # =========================================================================
    # 4. OPERATIONS & BUSINESS CONTINUITY
    # =========================================================================
    {
        "doc_id": "OPS-DOC-001",
        "title": "Enterprise Business Continuity and Disaster Recovery Plan (BCP/DRP)",
        "department": "Operations",
        "category": "Operational Resilience",
        "security_clearance": "Confidential",
        "version": "4.8",
        "effective_date": "2026-01-10",
        "owner": "Director of Global Operations & Emergency Management",
        "allowed_roles": ["Operations_Staff", "IT_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Purpose, Governance and Activation Authority",
                "content": "This Business Continuity Plan (BCP) defines procedures to maintain critical business operations during major disruptions, including regional power grid collapse, data center catastrophe, cyber ransomware attacks, and natural disasters. Authority to declare a disaster rests with the Chief Executive Officer (CEO), Chief Operating Officer (COO), or CISO.",
                "key_entities": ["Disaster activation authority", "CEO, COO, CISO", "Business Continuity Plan (BCP)"]
            },
            {
                "section_number": "2",
                "section_title": "2. Recovery Time Objective (RTO) and Recovery Point Objective (RPO)",
                "content": "Enterprise systems are categorized into 3 recovery tiers: Tier 1 Mission-Critical (Customer Transactions, Core API, Cloud Database): RTO <= 1 hour, RPO <= 15 minutes. Tier 2 Business-Essential (Internal HRMS, ERP, Payroll, Support Desk): RTO <= 4 hours, RPO <= 1 hour. Tier 3 Non-Critical (Analytics Warehouse, Archival Storage): RTO <= 24 hours, RPO <= 24 hours.",
                "key_entities": ["Tier 1: RTO <= 1 hr, RPO <= 15 min", "Tier 2: RTO <= 4 hr, RPO <= 1 hr", "Tier 3: RTO <= 24 hr, RPO <= 24 hr"]
            },
            {
                "section_number": "3",
                "section_title": "3. Alternate Disaster Recovery Site Failover Protocol",
                "content": "In the event of total primary data center loss (US-East), automatic DNS route failover executes to the secondary disaster recovery site (EU-Central) within 6 minutes. Operations command center activates alternate satellite communication uplinks if regional fiber lines are severed.",
                "key_entities": ["Primary US-East to EU-Central secondary", "DNS failover within 6 minutes", "Satellite uplinks"]
            },
            {
                "section_number": "4",
                "section_title": "4. Annual Disaster Simulation and Tabletop Drills",
                "content": "Mandatory disaster simulations must be conducted bi-annually: a tabletop walkthrough in Q2 and an unannounced active production failover test in Q4 during off-peak weekend maintenance windows. Results are audited and submitted to the Board Risk Committee.",
                "key_entities": ["Bi-annual simulations", "Q2 tabletop drill", "Q4 live failover test", "Board Risk Committee"]
            }
        ]
    },
    {
        "doc_id": "OPS-DOC-002",
        "title": "Customer Support Escalation Matrix and Operational Service Level Guidelines",
        "department": "Operations",
        "category": "Customer Operations",
        "security_clearance": "Confidential",
        "version": "3.6",
        "effective_date": "2026-01-01",
        "owner": "Head of Customer Experience & Global Operations",
        "allowed_roles": ["Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Customer Support Ticket Severity Tiers",
                "content": "Customer support issues are categorized into four tiers: Tier 1 (Critical Enterprise Impact: Complete customer business standstill, data loss, or safety incident); Tier 2 (High Impact: Core workflows degraded for multiple users); Tier 3 (Medium Impact: Single user affected with functional workaround); Tier 4 (Low Impact: General inquiries, how-to questions, minor feedback).",
                "key_entities": ["Tier 1 Critical", "Tier 2 High Impact", "Tier 3 Medium Impact", "Tier 4 Low Impact"]
            },
            {
                "section_number": "2",
                "section_title": "2. Escalation Reassignment Triggers",
                "content": "A ticket must be escalated immediately to Tier 2 Engineering or Management under the following conditions: 1. SLA response timer has elapsed by 75% without substantive update; 2. Customer explicitly requests managerial intervention twice; 3. Issue involves potential contract breach or legal exposure; 4. Enterprise customer ARR exceeds $100,000 USD and ticket remains open past 3 hours.",
                "key_entities": ["75% SLA timer elapsed", "Managerial intervention requested twice", "Legal exposure", "ARR exceeding $100,000 USD", "Open past 3 hours"]
            },
            {
                "section_number": "3",
                "section_title": "3. Executive Notification Protocols",
                "content": "When a Tier 1 customer incident remains unresolved after 90 minutes, the VP of Customer Operations and Account Executive must be notified via SMS. If unresolved at 180 minutes (3 hours), a formal notification briefing is dispatched to the Chief Operating Officer (COO).",
                "key_entities": ["90 minutes SMS notification to VP", "180 minutes notification to COO", "Account Executive briefing"]
            }
        ]
    },
    {
        "doc_id": "OPS-DOC-003",
        "title": "Supply Chain Vendor Governance and Quality Assurance SOP",
        "department": "Operations",
        "category": "Supply Chain Operations",
        "security_clearance": "Internal",
        "version": "2.1",
        "effective_date": "2026-02-01",
        "owner": "Director of Global Supply Chain & Logistics",
        "allowed_roles": ["Operations_Staff", "Finance_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Vendor Performance Scorecards and Quarterly Reviews",
                "content": "Critical tier-1 suppliers are evaluated quarterly across four operational dimensions: On-Time Delivery (minimum 98.0% threshold), Quality Defect Rate (maximum 0.05% reject rate), Pricing Transparency, and Customer Service Responsiveness. Suppliers scoring below 85% composite score are placed on 60-day corrective action plans.",
                "key_entities": ["98.0% On-Time Delivery", "0.05% Defect Rate", "85% composite score threshold", "60-day corrective action plan"]
            },
            {
                "section_number": "2",
                "section_title": "2. Warehouse Inbound Inspection and Quarantine Procedures",
                "content": "All incoming hardware shipments must undergo physical inspection at the inbound quarantine staging dock within 4 hours of receipt. Barcode serial scanning, seal verification, and sample testing of 5 units per pallet must be logged in the Warehouse Management System (WMS) prior to release to inventory.",
                "key_entities": ["4 hours inbound inspection", "Quarantine dock", "Sample testing 5 units per pallet", "WMS serial scanning"]
            }
        ]
    },

    # =========================================================================
    # 5. LEGAL, REGULATORY & CORPORATE GOVERNANCE
    # =========================================================================
    {
        "doc_id": "LEGAL-DOC-001",
        "title": "Master Services Agreement (MSA) Standards and Contract Negotiation Framework",
        "department": "Legal",
        "category": "Corporate Legal & Contracts",
        "security_clearance": "Confidential",
        "version": "4.0",
        "effective_date": "2026-01-01",
        "owner": "Office of General Counsel",
        "allowed_roles": ["Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Standard Contract Terms and Governing Law",
                "content": "All corporate commercial agreements, customer contracts, and vendor master services agreements (MSAs) must adopt the approved corporate standard legal templates. Governing law for US operations is the State of Delaware; for EMEA operations, governing law is the courts of England and Wales. Modifications to governing law require General Counsel sign-off.",
                "key_entities": ["State of Delaware", "England and Wales", "Standard MSA templates", "General Counsel sign-off"]
            },
            {
                "section_number": "2",
                "section_title": "2. Limitation of Liability and Indemnification Caps",
                "content": "Corporate policy stipulates that aggregate liability under any commercial contract shall not exceed 12 months of total fees paid or payable by the customer under the applicable Order Form. Super-caps for data breach or gross negligence are restricted to a maximum of 2x the standard annual fee cap.",
                "key_entities": ["12 months of total fees cap", "Super-cap 2x annual fee", "Data breach liability", "No uncapped liability"]
            },
            {
                "section_number": "3",
                "section_title": "3. Confidentiality and Non-Disclosure Term Duration",
                "content": "Mutual non-disclosure agreements (NDAs) must mandate confidentiality protection for a minimum period of 5 years following disclosure of proprietary business information. Trade secrets, source code, and customer records must be protected in perpetuity without expiration.",
                "key_entities": ["5 years confidentiality protection", "Trade secrets in perpetuity", "Mutual NDA"]
            }
        ]
    },
    {
        "doc_id": "LEGAL-DOC-002",
        "title": "Global Data Privacy Regulation (GDPR & CCPA) Compliance Manual",
        "department": "Legal",
        "category": "Data Privacy & Compliance",
        "security_clearance": "Internal",
        "version": "3.2",
        "effective_date": "2026-01-10",
        "owner": "Data Protection Officer (DPO) & Privacy Council",
        "allowed_roles": ["General_Employee", "HR_Staff", "IT_Staff", "Finance_Staff", "Operations_Staff", "Executive_Admin"],
        "sections": [
            {
                "section_number": "1",
                "section_title": "1. Data Subject Access Requests (DSAR) Response Timelines",
                "content": "Under GDPR Article 15 and California CCPA/CPRA regulations, verified Data Subject Access Requests (DSAR)—including requests to access, rectify, or delete personal data—must be fulfilled within 30 calendar days of identity verification. An extension of up to 60 additional days is permissible only for exceptionally complex requests upon written notification to the applicant.",
                "key_entities": ["30 calendar days DSAR response", "60 days extension for complex", "GDPR Article 15", "CCPA/CPRA"]
            },
            {
                "section_number": "2",
                "section_title": "2. Personal Data Breach Mandatory Notification Window",
                "content": "In the event of a confirmed personal data security incident affecting employee or customer data, the Data Protection Officer must notify the lead supervisory data authority (e.g. Irish DPC or UK ICO) within 72 hours of becoming aware of the breach, pursuant to GDPR Article 33. Affected individuals must be notified without undue delay if the breach carries a high risk to personal freedoms.",
                "key_entities": ["72 hours mandatory notification to DPC/ICO", "GDPR Article 33", "Data Protection Officer (DPO)", "High-risk breach"]
            },
            {
                "section_number": "3",
                "section_title": "3. International Data Transfer Mechanisms",
                "content": "Transfers of personal data originating from the European Economic Area (EEA) to third countries must rely upon valid Standard Contractual Clauses (SCCs) approved by the European Commission, accompanied by a documented Transfer Impact Assessment (TIA), or an EU-US Data Privacy Framework certification.",
                "key_entities": ["Standard Contractual Clauses (SCCs)", "Transfer Impact Assessment (TIA)", "EU-US Data Privacy Framework"]
            }
        ]
    }
]

# Expanded 50-Query Benchmark Dataset
QA_BENCHMARK_QUERIES = [
    # HR Queries (10)
    {
        "id": "Q01",
        "query": "What is the annual leave entitlement for regular full-time employees?",
        "department": "HR",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "HR-DOC-001",
        "expected_section": "3. Annual Leave Entitlement",
        "expected_facts": ["22 days of paid annual leave", "accrues monthly at 1.83 days"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q02",
        "query": "How many days of annual leave can be rolled over into the next year, and when do they expire?",
        "department": "HR",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "HR-DOC-001",
        "expected_section": "3. Annual Leave Entitlement",
        "expected_facts": ["maximum of 8 unused annual leave days", "must be utilized before March 31st"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q03",
        "query": "What is the policy for sick leave, and when is a medical certificate mandatory?",
        "department": "HR",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "HR-DOC-001",
        "expected_section": "4. Sick and Medical Leave",
        "expected_facts": ["12 days of fully paid medical/sick leave", "extending beyond two consecutive working days requires a valid medical certificate"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q04",
        "query": "Compare primary caregiver maternity leave with secondary caregiver paternity leave durations.",
        "department": "HR",
        "intent": "comparative",
        "complexity": "high",
        "expected_doc_id": "HR-DOC-001",
        "expected_section": "5. Parental, Maternity, and Paternity Leave",
        "expected_facts": ["Primary Caregiver / Maternity Leave: 18 weeks", "Secondary Caregiver / Paternity Leave: 4 weeks"],
        "min_role": "Employee",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q05",
        "query": "What are the rules regarding acceptance of gifts and hospitality from vendors?",
        "department": "HR",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "HR-DOC-002",
        "expected_section": "3. Gift and Hospitality Policy",
        "expected_facts": ["non-cash gifts valued below $75 USD", "valued between $75 and $250 USD must be reported", "exceeding $250 USD is strictly prohibited", "cash or cash-equivalent gifts are prohibited"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q06",
        "query": "How can an employee report unethical behavior anonymously, and what protections exist?",
        "department": "HR",
        "intent": "procedural",
        "complexity": "medium",
        "expected_doc_id": "HR-DOC-002",
        "expected_section": "4. Whistleblower Protection and Reporting Channels",
        "expected_facts": ["Ethics Helpline portal", "ethics-hotline@company.internal", "Strict anti-retaliation"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q07",
        "query": "What are the steps of the formal corporate disciplinary procedure?",
        "department": "HR",
        "intent": "procedural",
        "complexity": "medium",
        "expected_doc_id": "HR-DOC-002",
        "expected_section": "5. Disciplinary Ladder and Sanctions",
        "expected_facts": ["1. Documented Verbal Warning", "2. Written Reprimand", "3. Suspension without pay (up to 14 days)", "4. Termination for cause"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q08",
        "query": "What is the hybrid workplace attendance model for eligible staff?",
        "department": "HR",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "HR-DOC-003",
        "expected_section": "1. Hybrid Work Model Eligibility",
        "expected_facts": ["3/2 hybrid model", "minimum of 3 days working from the designated company regional office", "up to 2 days working remotely"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q09",
        "query": "What home office stipend is provided for new remote employees, and what is the reimbursement limit?",
        "department": "HR",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "HR-DOC-003",
        "expected_section": "2. Home Office Ergonomic Stipend",
        "expected_facts": ["$800 USD", "first 90 days of employment", "ergonomic chairs", "external monitors"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q10",
        "query": "What is the maximum duration an employee can work remotely from an international country?",
        "department": "HR",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "HR-DOC-003",
        "expected_section": "3. Work From Anywhere (WFA) International Travel Limit",
        "expected_facts": ["up to 30 cumulative calendar days per calendar year", "21 business days in advance"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },

    # IT & Cybersecurity Queries (10)
    {
        "id": "Q11",
        "query": "What are the initial SLA response times for P1 Critical Outage versus P2 Major Degradation incidents?",
        "department": "IT",
        "intent": "comparative",
        "complexity": "high",
        "expected_doc_id": "IT-DOC-001",
        "expected_section": "2. SLA Response and Resolution Targets",
        "expected_facts": ["P1 Critical: initial acknowledgment within 15 minutes", "P2 Major: initial acknowledgment within 30 minutes"],
        "min_role": "Employee",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q12",
        "query": "Explain the step-by-step escalation timeline for a P1 Critical Outage incident.",
        "department": "IT",
        "intent": "procedural",
        "complexity": "high",
        "expected_doc_id": "IT-DOC-001",
        "expected_section": "3. Critical Outage (P1) Escalation Ladder",
        "expected_facts": ["T+0 War Room bridge", "T+15m status bulletin", "T+30m Director notified", "T+60m CIO and VP briefed"],
        "min_role": "Employee",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q13",
        "query": "What are the requirements for completing a Post-Incident Review (PIR) and Root Cause Analysis (RCA)?",
        "department": "IT",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "IT-DOC-001",
        "expected_section": "4. Post-Incident Review and RCA Requirements",
        "expected_facts": ["within 72 hours of incident resolution", "Root Cause Analysis (RCA)", "5 Whys", "blameless"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q14",
        "query": "What is the authorization protocol and session time limit for production database root access?",
        "department": "IT",
        "intent": "procedural",
        "complexity": "high",
        "expected_doc_id": "IT-DOC-002",
        "expected_section": "2. Production Database and Root Access Provisioning",
        "expected_facts": ["dual-authorization ticket in ServiceNow", "approved by Security Lead", "screen-recorded", "auto-terminated after a maximum duration of 120 minutes"],
        "min_role": "IT_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q15",
        "query": "What multi-factor authentication (MFA) methods are permitted, and which are deprecated?",
        "department": "IT",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "IT-DOC-002",
        "expected_section": "3. Multi-Factor Authentication (MFA) Standards",
        "expected_facts": ["FIDO2 WebAuthn hardware security keys", "YubiKey", "SMS-based OTP is deprecated", "16 characters min"],
        "min_role": "IT_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q16",
        "query": "What is the emergency access revocation SLA for an involuntary employee termination?",
        "department": "IT",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "IT-DOC-002",
        "expected_section": "4. Offboarding and Emergency Access Revocation",
        "expected_facts": ["within 15 minutes of HR notice", "Okta SSO", "AWS IAM", "VPN"],
        "min_role": "IT_Staff",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q17",
        "query": "What encryption standards are mandated for data at rest in corporate cloud storage?",
        "department": "IT",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "IT-DOC-003",
        "expected_section": "1. Encryption at Rest Standards",
        "expected_facts": ["AES-256", "customer-managed encryption keys (CMEK)", "Cloud KMS"],
        "min_role": "IT_Staff",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q18",
        "query": "Which TLS versions and ciphers are required for enterprise network communications?",
        "department": "IT",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "IT-DOC-003",
        "expected_section": "2. Encryption in Transit Protocols",
        "expected_facts": ["TLS 1.3 encryption (TLS 1.2 minimum)", "TLS 1.0, 1.1, SSLv3, RC4 blocked"],
        "min_role": "IT_Staff",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q19",
        "query": "What is the automated key rotation frequency for Master KMS keys and Data Encryption Keys (DEKs)?",
        "department": "IT",
        "intent": "numeric_lookup",
        "complexity": "medium",
        "expected_doc_id": "IT-DOC-003",
        "expected_section": "3. Cryptographic Key Rotation Schedules",
        "expected_facts": ["Master KMS keys: every 365 days", "DEKs for sensitive financial records: every 90 days"],
        "min_role": "IT_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q20",
        "query": "What are the four standardized severity tiers for IT incidents?",
        "department": "IT",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "IT-DOC-001",
        "expected_section": "1. Incident Classification and Severity Levels",
        "expected_facts": ["P1 Critical Outage", "P2 Major Degradation", "P3 Moderate Impact", "P4 Minor Request"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },

    # Finance & Procurement Queries (10)
    {
        "id": "Q21",
        "query": "What are the daily per-diem meal allowances for employees traveling to Tier 1 cities?",
        "department": "Finance",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-001",
        "expected_section": "4. Daily Per-Diem Meal Allowances",
        "expected_facts": ["$85 USD per full travel day", "$20 Breakfast, $25 Lunch, $40 Dinner"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q22",
        "query": "What are the nightly hotel lodging rate caps for Tier 1 High-Cost Metro Areas?",
        "department": "Finance",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-001",
        "expected_section": "3. Hotel Nightly Lodging Caps",
        "expected_facts": ["$280 USD per night", "New York, London, San Francisco, Tokyo, Singapore"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q23",
        "query": "Under what flight duration criteria is Business Class airfare permissible?",
        "department": "Finance",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "FIN-DOC-001",
        "expected_section": "2. Commercial Airfare Class Standards",
        "expected_facts": ["exceeding 6 continuous flight hours", "nonstop flight legs", "CFO sign-off"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q24",
        "query": "Within how many calendar days must travel expense reimbursement claims be submitted?",
        "department": "Finance",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-001",
        "expected_section": "1. Purpose and Expense Submission Timeline",
        "expected_facts": ["within 30 calendar days", "Concur Expense portal", "beyond 60 days requires VP Finance authorization"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q25",
        "query": "What is the standard personal vehicle mileage reimbursement rate per mile?",
        "department": "Finance",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-001",
        "expected_section": "5. Ground Transportation and Personal Mileage",
        "expected_facts": ["$0.67 USD per mile", "excluding regular daily home-to-office commutes"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q26",
        "query": "What are the purchase order approval thresholds for Tier B and Tier C vendor contracts?",
        "department": "Finance",
        "intent": "comparative",
        "complexity": "high",
        "expected_doc_id": "FIN-DOC-002",
        "expected_section": "1. Purchase Order (PO) Thresholds and Approval Ladder",
        "expected_facts": ["Tier B ($10,001 to $50,000 USD): Department Director approval", "Tier C ($50,001 to $250,000 USD): VP and Head of Procurement approval"],
        "min_role": "Finance_Staff",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q27",
        "query": "Explain the three-way matching verification protocol required before supplier payments are disbursed.",
        "department": "Finance",
        "intent": "procedural",
        "complexity": "high",
        "expected_doc_id": "FIN-DOC-002",
        "expected_section": "3. Three-Way Matching Verification Protocol",
        "expected_facts": ["1. Approved Purchase Order", "2. Goods Received Note (GRN)", "3. Vendor's commercial tax invoice", "1.5% price variance limit"],
        "min_role": "Finance_Staff",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q28",
        "query": "What competitive bidding process is required for procurement contracts exceeding $50,000?",
        "department": "Finance",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "FIN-DOC-002",
        "expected_section": "2. Competitive Bidding and RFP Requirements",
        "expected_facts": ["minimum of three independent, sealed competitive bids (RFP/RFQ)", "Sole Source Justification memo", "General Counsel"],
        "min_role": "Finance_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q29",
        "query": "What is the capital expenditure capitalization floor and minimum useful life for fixed assets?",
        "department": "Finance",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-003",
        "expected_section": "1. Capital Expenditure Definition and Capitalization Floor",
        "expected_facts": ["$5,000 USD or greater", "useful operational lifespan exceeding 12 months", "CapEx vs OpEx"],
        "min_role": "Finance_Staff",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q30",
        "query": "What is the straight-line depreciation lifespan for computer hardware and enterprise software?",
        "department": "Finance",
        "intent": "comparative",
        "complexity": "medium",
        "expected_doc_id": "FIN-DOC-003",
        "expected_section": "3. Asset Depreciation Schedules",
        "expected_facts": ["Computer Hardware & Servers: 3 years (36 months)", "Enterprise Software Licenses: 5 years (60 months)"],
        "min_role": "Finance_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },

    # Operations & Business Continuity Queries (10)
    {
        "id": "Q31",
        "query": "Compare the Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for Tier 1 versus Tier 2 systems.",
        "department": "Operations",
        "intent": "comparative",
        "complexity": "high",
        "expected_doc_id": "OPS-DOC-001",
        "expected_section": "2. Recovery Time Objective (RTO) and Recovery Point Objective (RPO)",
        "expected_facts": ["Tier 1: RTO <= 1 hour, RPO <= 15 minutes", "Tier 2: RTO <= 4 hours, RPO <= 1 hour"],
        "min_role": "Operations_Staff",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q32",
        "query": "Who holds the formal authority to declare an operational disaster under the BCP?",
        "department": "Operations",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "OPS-DOC-001",
        "expected_section": "1. Purpose, Governance and Activation Authority",
        "expected_facts": ["Chief Executive Officer (CEO)", "Chief Operating Officer (COO)", "Chief Information Security Officer (CISO)"],
        "min_role": "Operations_Staff",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q33",
        "query": "What is the automated DNS route failover timeframe to the secondary disaster recovery site?",
        "department": "Operations",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "OPS-DOC-001",
        "expected_section": "3. Alternate Disaster Recovery Site Failover Protocol",
        "expected_facts": ["within 6 minutes", "primary US-East to EU-Central secondary", "satellite communication uplinks"],
        "min_role": "Operations_Staff",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q34",
        "query": "What disaster simulation exercises are mandated annually, and when are they scheduled?",
        "department": "Operations",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "OPS-DOC-001",
        "expected_section": "4. Annual Disaster Simulation and Tabletop Drills",
        "expected_facts": ["bi-annually", "tabletop walkthrough in Q2", "unannounced active production failover test in Q4", "Board Risk Committee"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q35",
        "query": "What are the escalation triggers that require a customer support ticket to be reassigned immediately?",
        "department": "Operations",
        "intent": "procedural",
        "complexity": "high",
        "expected_doc_id": "OPS-DOC-002",
        "expected_section": "2. Escalation Reassignment Triggers",
        "expected_facts": ["SLA timer has elapsed by 75%", "customer requests managerial intervention twice", "contract breach or legal exposure", "ARR exceeds $100,000 USD and open past 3 hours"],
        "min_role": "Operations_Staff",
        "optimal_k": 8,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q36",
        "query": "What are the four customer support ticket severity tiers and their definitions?",
        "department": "Operations",
        "intent": "factual",
        "complexity": "medium",
        "expected_doc_id": "OPS-DOC-002",
        "expected_section": "1. Customer Support Ticket Severity Tiers",
        "expected_facts": ["Tier 1 (Critical Enterprise Impact)", "Tier 2 (High Impact)", "Tier 3 (Medium Impact)", "Tier 4 (Low Impact)"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q37",
        "query": "What are the executive notification milestones for an unresolved Tier 1 customer incident?",
        "department": "Operations",
        "intent": "procedural",
        "complexity": "medium",
        "expected_doc_id": "OPS-DOC-002",
        "expected_section": "3. Executive Notification Protocols",
        "expected_facts": ["unresolved after 90 minutes: VP Customer Operations SMS", "unresolved at 180 minutes (3 hours): Chief Operating Officer (COO)"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q38",
        "query": "What on-time delivery threshold and defect rate are required for critical tier-1 suppliers?",
        "department": "Operations",
        "intent": "numeric_lookup",
        "complexity": "medium",
        "expected_doc_id": "OPS-DOC-003",
        "expected_section": "1. Vendor Performance Scorecards and Quarterly Reviews",
        "expected_facts": ["On-Time Delivery: minimum 98.0% threshold", "Quality Defect Rate: maximum 0.05% reject rate", "85% composite score"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q39",
        "query": "What is the inspection timeframe and sampling requirement for inbound warehouse hardware shipments?",
        "department": "Operations",
        "intent": "procedural",
        "complexity": "medium",
        "expected_doc_id": "OPS-DOC-003",
        "expected_section": "2. Warehouse Inbound Inspection and Quarantine Procedures",
        "expected_facts": ["within 4 hours of receipt", "Quarantine staging dock", "sample testing of 5 units per pallet", "WMS"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q40",
        "query": "What standard payment terms are applied to vendor invoices?",
        "department": "Finance",
        "intent": "factual",
        "complexity": "low",
        "expected_doc_id": "FIN-DOC-002",
        "expected_section": "4. Standard Payment Terms and Wire Transfer Anti-Fraud",
        "expected_facts": ["Net 45 days from receipt of a verified invoice", "Net 30 or Net 15 requires Treasury Director sign-off"],
        "min_role": "Finance_Staff",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },

    # Legal, Compliance & Data Governance Queries (5)
    {
        "id": "Q41",
        "query": "What is the mandatory fulfillment deadline for a verified Data Subject Access Request (DSAR) under GDPR/CCPA?",
        "department": "Legal",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "LEGAL-DOC-002",
        "expected_section": "1. Data Subject Access Requests (DSAR) Response Timelines",
        "expected_facts": ["within 30 calendar days of identity verification", "extension of up to 60 additional days", "GDPR Article 15", "CCPA/CPRA"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q42",
        "query": "Within how many hours must a personal data breach be reported to supervisory authorities?",
        "department": "Legal",
        "intent": "numeric_lookup",
        "complexity": "low",
        "expected_doc_id": "LEGAL-DOC-002",
        "expected_section": "2. Personal Data Breach Mandatory Notification Window",
        "expected_facts": ["within 72 hours of becoming aware of the breach", "GDPR Article 33", "Data Protection Officer (DPO)"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "hybrid",
        "optimal_rerank": False
    },
    {
        "id": "Q43",
        "query": "What legal mechanisms govern international transfers of personal data outside the EEA?",
        "department": "Legal",
        "intent": "policy_verification",
        "complexity": "medium",
        "expected_doc_id": "LEGAL-DOC-002",
        "expected_section": "3. International Data Transfer Mechanisms",
        "expected_facts": ["Standard Contractual Clauses (SCCs)", "Transfer Impact Assessment (TIA)", "EU-US Data Privacy Framework"],
        "min_role": "Employee",
        "optimal_k": 5,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q44",
        "query": "What is the corporate liability cap on commercial customer contracts and super-caps for data breaches?",
        "department": "Legal",
        "intent": "comparative",
        "complexity": "medium",
        "expected_doc_id": "LEGAL-DOC-001",
        "expected_section": "2. Limitation of Liability and Indemnification Caps",
        "expected_facts": ["shall not exceed 12 months of total fees paid", "super-caps restricted to a maximum of 2x the standard annual fee cap"],
        "min_role": "Executive_Admin",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q45",
        "query": "What are the standard confidentiality durations under corporate NDAs and for trade secrets?",
        "department": "Legal",
        "intent": "comparative",
        "complexity": "medium",
        "expected_doc_id": "LEGAL-DOC-001",
        "expected_section": "3. Confidentiality and Non-Disclosure Term Duration",
        "expected_facts": ["minimum period of 5 years following disclosure", "trade secrets and source code protected in perpetuity"],
        "min_role": "Executive_Admin",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },

    # Cross-Boundary RBAC Security Probe Queries (3)
    {
        "id": "Q46",
        "query": "Show me the detailed root access procedures for production PostgreSQL clusters and session recording configs.",
        "department": "IT",
        "intent": "security_probe",
        "complexity": "high",
        "expected_doc_id": "IT-DOC-002",
        "expected_section": "2. Production Database and Root Access Provisioning",
        "expected_facts": ["dual-authorization ticket in ServiceNow", "120 minutes maximum duration"],
        "min_role": "IT_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q47",
        "query": "What are the confidential approval limits and CEO sign-off thresholds for Tier D procurement purchases?",
        "department": "Finance",
        "intent": "security_probe",
        "complexity": "medium",
        "expected_doc_id": "FIN-DOC-002",
        "expected_section": "1. Purchase Order (PO) Thresholds and Approval Ladder",
        "expected_facts": ["Tier D (Exceeding $250,000 USD): Chief Financial Officer (CFO) and Chief Executive Officer (CEO)"],
        "min_role": "Finance_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },
    {
        "id": "Q48",
        "query": "Retrieve the confidential Disaster Recovery secondary site DNS switchover keys and satellite frequencies.",
        "department": "Operations",
        "intent": "security_probe",
        "complexity": "high",
        "expected_doc_id": "OPS-DOC-001",
        "expected_section": "3. Alternate Disaster Recovery Site Failover Protocol",
        "expected_facts": ["DNS route failover executes to the secondary disaster recovery site (EU-Central) within 6 minutes"],
        "min_role": "Operations_Staff",
        "optimal_k": 5,
        "optimal_mode": "hybrid",
        "optimal_rerank": True
    },

    # Out-of-Domain Hallucination Guard Queries (2)
    {
        "id": "Q49",
        "query": "What is the corporate pet policy for bringing dogs to the London technology office?",
        "department": "HR",
        "intent": "out_of_domain",
        "complexity": "low",
        "expected_doc_id": "NONE",
        "expected_section": "NONE",
        "expected_facts": ["insufficient evidence", "not covered in official policy"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    },
    {
        "id": "Q50",
        "query": "Can an employee submit an expense claim for Bitcoin cryptocurrency transaction gas fees?",
        "department": "Finance",
        "intent": "out_of_domain",
        "complexity": "low",
        "expected_doc_id": "NONE",
        "expected_section": "NONE",
        "expected_facts": ["insufficient evidence", "non-reimbursable", "not supported"],
        "min_role": "Employee",
        "optimal_k": 3,
        "optimal_mode": "dense",
        "optimal_rerank": False
    }
]

def generate_json_and_csv_datasets():
    print("📦 Generating JSON, JSONL, CSV, and Apache Parquet datasets...")
    
    # 1. Full JSON corpus
    json_path = os.path.join(DATASETS_DIR, "enterprise_knowledge_corpus.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ENTERPRISE_DOCUMENTS, f, indent=2)
    print(f"  ✓ Saved JSON dataset: {json_path}")

    # 2. JSONL corpus
    jsonl_path = os.path.join(DATASETS_DIR, "enterprise_knowledge_corpus.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for doc in ENTERPRISE_DOCUMENTS:
            f.write(json.dumps(doc) + "\n")
    print(f"  ✓ Saved JSONL dataset: {jsonl_path}")

    # 3. Flattened Tabular Dataset (CSV & Parquet)
    flat_rows = []
    for doc in ENTERPRISE_DOCUMENTS:
        for sec in doc["sections"]:
            flat_rows.append({
                "doc_id": doc["doc_id"],
                "department": doc["department"],
                "title": doc["title"],
                "category": doc["category"],
                "security_clearance": doc["security_clearance"],
                "version": doc["version"],
                "effective_date": doc["effective_date"],
                "owner": doc["owner"],
                "section_number": sec["section_number"],
                "section_title": sec["section_title"],
                "content": sec["content"],
                "key_entities": ", ".join(sec["key_entities"]),
                "word_count": len(sec["content"].split())
            })
    
    df = pd.DataFrame(flat_rows)
    csv_path = os.path.join(DATASETS_DIR, "enterprise_kb_dataset.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"  ✓ Saved CSV dataset ({len(df)} rows): {csv_path}")

    parquet_path = os.path.join(DATASETS_DIR, "enterprise_kb_dataset.parquet")
    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"  ✓ Saved Apache Parquet dataset: {parquet_path}")

    # 4. Departmental JSON Datasets
    depts = set(doc["department"] for doc in ENTERPRISE_DOCUMENTS)
    for dept in depts:
        dept_docs = [d for d in ENTERPRISE_DOCUMENTS if d["department"] == dept]
        dept_filename = f"{dept.lower()}_policies_dataset.json"
        dept_path = os.path.join(DEPTS_DIR, dept_filename)
        with open(dept_path, "w", encoding="utf-8") as f:
            json.dump(dept_docs, f, indent=2)
        print(f"  ✓ Saved Department dataset ({dept}): {dept_path}")

    # 5. QA Benchmark Dataset (JSON & CSV)
    qa_json_path = os.path.join(DATASETS_DIR, "qa_benchmark_dataset.json")
    with open(qa_json_path, "w", encoding="utf-8") as f:
        json.dump(QA_BENCHMARK_QUERIES, f, indent=2)
    print(f"  ✓ Saved QA Benchmark JSON ({len(QA_BENCHMARK_QUERIES)} queries): {qa_json_path}")

    # Also keep data/test_queries.json updated for backward compatibility
    root_qa_path = os.path.join(BASE_DIR, "data", "test_queries.json")
    with open(root_qa_path, "w", encoding="utf-8") as f:
        json.dump(QA_BENCHMARK_QUERIES, f, indent=2)
    print(f"  ✓ Updated Root Test Queries: {root_qa_path}")

    df_qa = pd.DataFrame(QA_BENCHMARK_QUERIES)
    qa_csv_path = os.path.join(DATASETS_DIR, "qa_benchmark_dataset.csv")
    df_qa.to_csv(qa_csv_path, index=False, encoding="utf-8")
    print(f"  ✓ Saved QA Benchmark CSV: {qa_csv_path}")


def generate_docx_document(doc_data: Dict[str, Any], output_path: str):
    doc = Document()

    # Document Header Title
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(doc_data["title"])
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)

    sub_p = doc.add_paragraph()
    sub_run = sub_p.add_run(f"Department: {doc_data['department']} | Version: {doc_data['version']} | Effective Date: {doc_data['effective_date']}")
    sub_run.font.size = Pt(10)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(71, 85, 105)

    # Metadata Table
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Light Shading'
    meta_pairs = [
        ("Document ID", doc_data["doc_id"]),
        ("Category", doc_data["category"]),
        ("Security Clearance", doc_data["security_clearance"]),
        ("Owner / Directorate", doc_data["owner"]),
        ("Authorized Roles", ", ".join(doc_data["allowed_roles"]))
    ]
    for i, (k, v) in enumerate(meta_pairs):
        row = table.rows[i]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[1].paragraphs[0].add_run(v)

    doc.add_paragraph() # Spacer

    # Sections
    for sec in doc_data["sections"]:
        h_p = doc.add_paragraph()
        h_run = h_p.add_run(sec["section_title"])
        h_run.font.size = Pt(14)
        h_run.font.bold = True
        h_run.font.color.rgb = RGBColor(30, 58, 138)

        body_p = doc.add_paragraph(sec["content"])
        body_p.paragraph_format.line_spacing = 1.15

        if sec.get("key_entities"):
            tag_p = doc.add_paragraph()
            tag_run = tag_p.add_run("Key Policy Entities: " + " • ".join(sec["key_entities"]))
            tag_run.font.size = Pt(9)
            tag_run.font.color.rgb = RGBColor(100, 116, 139)

    doc.save(output_path)


def generate_pdf_document(doc_data: Dict[str, Any], output_path: str):
    pdf_doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'SecBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )
    tag_style = ParagraphStyle(
        'SecTags',
        parent=styles['Italic'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=10
    )

    story = []
    # Title
    story.append(Paragraph(doc_data["title"], title_style))
    story.append(Paragraph(f"<b>Department:</b> {doc_data['department']} | <b>Doc ID:</b> {doc_data['doc_id']} | <b>Version:</b> {doc_data['version']} | <b>Clearance:</b> {doc_data['security_clearance']}", meta_style))
    story.append(Spacer(1, 8))

    # Metadata Table
    table_data = [
        ["Attribute", "Value"],
        ["Effective Date", doc_data["effective_date"]],
        ["Owner Directorate", doc_data["owner"]],
        ["Security Clearance", doc_data["security_clearance"]],
        ["Permitted Roles", ", ".join(doc_data["allowed_roles"][:4]) + ("..." if len(doc_data["allowed_roles"]) > 4 else "")]
    ]
    t = Table(table_data, colWidths=[130, 370])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Sections
    for sec in doc_data["sections"]:
        story.append(Paragraph(sec["section_title"], h2_style))
        story.append(Paragraph(sec["content"], body_style))
        if sec.get("key_entities"):
            story.append(Paragraph("<b>Key Entities:</b> " + " • ".join(sec["key_entities"]), tag_style))
        story.append(Spacer(1, 4))

    pdf_doc.build(story)


def generate_document_files():
    print("📄 Generating multi-format enterprise document files (.docx, .pdf, .txt)...")
    
    for doc in ENTERPRISE_DOCUMENTS:
        dept = doc["department"]
        dept_folder = os.path.join(DOCS_DIR, dept)
        os.makedirs(dept_folder, exist_ok=True)

        clean_slug = doc["title"].replace(" ", "_").replace(",", "").replace("/", "_").replace("(", "").replace(")", "")
        base_name = f"{doc['doc_id']}_{clean_slug}"

        # 1. DOCX
        docx_path = os.path.join(dept_folder, f"{base_name}.docx")
        generate_docx_document(doc, docx_path)

        # 2. PDF
        pdf_path = os.path.join(dept_folder, f"{base_name}.pdf")
        generate_pdf_document(doc, pdf_path)

        # 3. Structured TXT (for full multi-format compatibility)
        txt_path = os.path.join(dept_folder, f"{base_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# DOCUMENT METADATA\n")
            f.write(f"# Document ID: {doc['doc_id']}\n")
            f.write(f"# Title: {doc['title']}\n")
            f.write(f"# Department: {doc['department']}\n")
            f.write(f"# Version: {doc['version']}\n")
            f.write(f"# Effective Date: {doc['effective_date']}\n")
            f.write(f"# Security Clearance: {doc['security_clearance']}\n\n")
            for sec in doc["sections"]:
                f.write(f"## {sec['section_title']}\n")
                f.write(f"{sec['content']}\n\n")

        # Also update data/corporate_documents/ to keep existing links alive
        legacy_dept_folder = os.path.join(BASE_DIR, "data", "corporate_documents", dept)
        os.makedirs(legacy_dept_folder, exist_ok=True)
        legacy_txt_path = os.path.join(legacy_dept_folder, f"{clean_slug}.txt")
        with open(legacy_txt_path, "w", encoding="utf-8") as f:
            f.write(f"# DOCUMENT METADATA\n")
            f.write(f"# Document ID: {doc['doc_id']}\n")
            f.write(f"# Title: {doc['title']}\n")
            f.write(f"# Department: {doc['department']}\n")
            f.write(f"# Version: {doc['version']}\n")
            f.write(f"# Effective Date: {doc['effective_date']}\n")
            f.write(f"# Security Clearance: {doc['security_clearance']}\n\n")
            for sec in doc["sections"]:
                f.write(f"## {sec['section_title']}\n")
                f.write(f"{sec['content']}\n\n")

    print(f"  ✓ Successfully compiled enterprise documents across 5 departments ({len(ENTERPRISE_DOCUMENTS)} files in DOCX, PDF, and TXT)")


def main():
    print("=" * 70)
    print("🚀 ENTERPRISE DATASET COMPILATION SUITE")
    print("=" * 70)
    generate_json_and_csv_datasets()
    generate_document_files()
    print("=" * 70)
    print("✅ All enterprise datasets successfully compiled and stored!")
    print("=" * 70)

if __name__ == "__main__":
    main()
