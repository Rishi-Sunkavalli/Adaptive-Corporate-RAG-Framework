"""
Enterprise Document & Dataset Ingestion Engine.
Extracts document metadata and structured text from:
- Structured Datasets: JSON, JSONL, CSV, and Apache Parquet (.parquet)
- Enterprise Document Formats: DOCX (Word), PDF (Acrobat), and Markdown/TXT.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
import pandas as pd

# Safe optional imports for document parsing
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class CorporateDocumentParser:
    """
    Unified multi-format parser for enterprise knowledge repositories and datasets.
    """

    @staticmethod
    def parse_txt_document(filepath: str) -> Dict[str, Any]:
        """
        Parses a corporate TXT document with structured metadata comments at the top.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = {
            "doc_id": "UNKNOWN",
            "title": os.path.basename(filepath).replace(".txt", "").replace("_", " "),
            "department": "General",
            "version": "1.0",
            "effective_date": "2026-01-01",
            "security_clearance": "Internal",
            "filepath": filepath,
            "format": "txt"
        }

        # Extract metadata from header lines
        header_match = re.search(r"# DOCUMENT METADATA\n(.*?)(?=\n##|\n[A-Z0-9]|\n\n[^\#])", content, re.DOTALL)
        if header_match:
            header_text = header_match.group(1)
            for line in header_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip().lower().replace("#", "").replace(" ", "_")
                    val = val.strip()
                    if "document_id" in key or "doc_id" in key:
                        metadata["doc_id"] = val
                    elif "title" in key:
                        metadata["title"] = val
                    elif "department" in key:
                        metadata["department"] = val
                    elif "version" in key:
                        metadata["version"] = val
                    elif "effective_date" in key:
                        metadata["effective_date"] = val
                    elif "security_clearance" in key:
                        metadata["security_clearance"] = val

        # Clean body text
        body_text = re.sub(r"# DOCUMENT METADATA.*?(?=\n## |\n# )", "", content, flags=re.DOTALL).strip()
        if not body_text:
            body_text = content.strip()

        return {
            "metadata": metadata,
            "raw_text": body_text
        }

    @staticmethod
    def parse_json_dataset(filepath: str) -> List[Dict[str, Any]]:
        """
        Parses an enterprise knowledge JSON dataset file (e.g. enterprise_knowledge_corpus.json).
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

        parsed_docs = []
        for item in data:
            doc_id = item.get("doc_id", "UNKNOWN")
            title = item.get("title", "Untitled Policy")
            department = item.get("department", "General")
            version = str(item.get("version", "1.0"))
            effective_date = item.get("effective_date", "2026-01-01")
            security_clearance = item.get("security_clearance", "Internal")

            sections = item.get("sections", [])
            body_parts = []
            for sec in sections:
                sec_title = sec.get("section_title", "Section")
                sec_content = sec.get("content", "")
                entities = sec.get("key_entities", [])
                ent_str = f"\n*Key Terms: {', '.join(entities)}*" if entities else ""
                body_parts.append(f"## {sec_title}\n{sec_content}{ent_str}")

            raw_text = "\n\n".join(body_parts) if body_parts else item.get("content", "")

            parsed_docs.append({
                "metadata": {
                    "doc_id": doc_id,
                    "title": title,
                    "department": department,
                    "version": version,
                    "effective_date": effective_date,
                    "security_clearance": security_clearance,
                    "category": item.get("category", "Enterprise Policy"),
                    "owner": item.get("owner", "Corporate Operations"),
                    "allowed_roles": item.get("allowed_roles", []),
                    "filepath": filepath,
                    "format": "json"
                },
                "raw_text": raw_text
            })
        return parsed_docs

    @staticmethod
    def parse_jsonl_dataset(filepath: str) -> List[Dict[str, Any]]:
        """
        Parses a JSON Lines dataset file.
        """
        parsed_docs = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                doc_id = item.get("doc_id", "UNKNOWN")
                title = item.get("title", "Untitled Policy")
                department = item.get("department", "General")
                version = str(item.get("version", "1.0"))
                effective_date = item.get("effective_date", "2026-01-01")
                security_clearance = item.get("security_clearance", "Internal")

                sections = item.get("sections", [])
                body_parts = []
                for sec in sections:
                    sec_title = sec.get("section_title", "Section")
                    sec_content = sec.get("content", "")
                    body_parts.append(f"## {sec_title}\n{sec_content}")

                raw_text = "\n\n".join(body_parts) if body_parts else item.get("content", "")

                parsed_docs.append({
                    "metadata": {
                        "doc_id": doc_id,
                        "title": title,
                        "department": department,
                        "version": version,
                        "effective_date": effective_date,
                        "security_clearance": security_clearance,
                        "category": item.get("category", "Enterprise Policy"),
                        "owner": item.get("owner", "Corporate Operations"),
                        "allowed_roles": item.get("allowed_roles", []),
                        "filepath": filepath,
                        "format": "jsonl"
                    },
                    "raw_text": raw_text
                })
        return parsed_docs

    @staticmethod
    def parse_csv_dataset(filepath: str) -> List[Dict[str, Any]]:
        """
        Parses a tabular CSV dataset of enterprise knowledge (e.g. enterprise_kb_dataset.csv).
        """
        df = pd.read_csv(filepath)
        grouped = df.groupby("doc_id")
        parsed_docs = []

        for doc_id, group in grouped:
            first_row = group.iloc[0]
            title = str(first_row.get("title", "Untitled Policy"))
            department = str(first_row.get("department", "General"))
            version = str(first_row.get("version", "1.0"))
            effective_date = str(first_row.get("effective_date", "2026-01-01"))
            security_clearance = str(first_row.get("security_clearance", "Internal"))
            category = str(first_row.get("category", "Enterprise Policy"))
            owner = str(first_row.get("owner", "Corporate Directorate"))

            body_parts = []
            for _, row in group.iterrows():
                sec_title = str(row.get("section_title", "Section"))
                content = str(row.get("content", ""))
                body_parts.append(f"## {sec_title}\n{content}")

            parsed_docs.append({
                "metadata": {
                    "doc_id": str(doc_id),
                    "title": title,
                    "department": department,
                    "version": version,
                    "effective_date": effective_date,
                    "security_clearance": security_clearance,
                    "category": category,
                    "owner": owner,
                    "filepath": filepath,
                    "format": "csv"
                },
                "raw_text": "\n\n".join(body_parts)
            })
        return parsed_docs

    @staticmethod
    def parse_parquet_dataset(filepath: str) -> List[Dict[str, Any]]:
        """
        Parses an Apache Parquet dataset file.
        """
        df = pd.read_parquet(filepath)
        grouped = df.groupby("doc_id")
        parsed_docs = []

        for doc_id, group in grouped:
            first_row = group.iloc[0]
            title = str(first_row.get("title", "Untitled Policy"))
            department = str(first_row.get("department", "General"))
            version = str(first_row.get("version", "1.0"))
            effective_date = str(first_row.get("effective_date", "2026-01-01"))
            security_clearance = str(first_row.get("security_clearance", "Internal"))

            body_parts = []
            for _, row in group.iterrows():
                sec_title = str(row.get("section_title", "Section"))
                content = str(row.get("content", ""))
                body_parts.append(f"## {sec_title}\n{content}")

            parsed_docs.append({
                "metadata": {
                    "doc_id": str(doc_id),
                    "title": title,
                    "department": department,
                    "version": version,
                    "effective_date": effective_date,
                    "security_clearance": security_clearance,
                    "filepath": filepath,
                    "format": "parquet"
                },
                "raw_text": "\n\n".join(body_parts)
            })
        return parsed_docs

    @staticmethod
    def parse_docx_document(filepath: str) -> Dict[str, Any]:
        """
        Parses a Microsoft Word (.docx) document file.
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required to parse .docx files")

        doc = Document(filepath)
        filename = os.path.basename(filepath)
        
        # Deduce doc_id and department from filename if present
        doc_id = "UNKNOWN"
        match = re.search(r"(HR|IT|FIN|OPS|LEGAL)-DOC-\d+", filename)
        if match:
            doc_id = match.group(0)

        metadata = {
            "doc_id": doc_id,
            "title": filename.replace(".docx", "").replace("_", " "),
            "department": "General",
            "version": "1.0",
            "effective_date": "2026-01-01",
            "security_clearance": "Internal",
            "filepath": filepath,
            "format": "docx"
        }

        # Check metadata table if first element
        for table in doc.tables:
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells]
                if len(cells) >= 2:
                    k, v = cells[0].lower(), cells[1]
                    if "document id" in k or "doc id" in k:
                        metadata["doc_id"] = v
                    elif "department" in k:
                        metadata["department"] = v
                    elif "security clearance" in k:
                        metadata["security_clearance"] = v
                    elif "version" in k:
                        metadata["version"] = v
                    elif "effective date" in k:
                        metadata["effective_date"] = v

        # Extract paragraphs
        body_lines = []
        for p in doc.paragraphs:
            text = p.text.strip()
            if not text:
                continue
            if p.style.name.startswith("Heading 1") or (len(text) < 80 and re.match(r"^\d+\.\s+[A-Z]", text)):
                body_lines.append(f"## {text}")
            else:
                body_lines.append(text)

        raw_text = "\n\n".join(body_lines)
        return {"metadata": metadata, "raw_text": raw_text}

    @staticmethod
    def parse_pdf_document(filepath: str) -> Dict[str, Any]:
        """
        Parses an Adobe PDF (.pdf) document file using pypdf.
        """
        if not PDF_AVAILABLE:
            raise ImportError("pypdf is required to parse .pdf files")

        reader = PdfReader(filepath)
        filename = os.path.basename(filepath)
        
        doc_id = "UNKNOWN"
        match = re.search(r"(HR|IT|FIN|OPS|LEGAL)-DOC-\d+", filename)
        if match:
            doc_id = match.group(0)

        metadata = {
            "doc_id": doc_id,
            "title": filename.replace(".pdf", "").replace("_", " "),
            "department": "General",
            "version": "1.0",
            "effective_date": "2026-01-01",
            "security_clearance": "Internal",
            "filepath": filepath,
            "format": "pdf"
        }

        full_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                full_text.append(t)

        raw_content = "\n".join(full_text)

        # Look for Doc ID in text if UNKNOWN
        id_match = re.search(r"(HR|IT|FIN|OPS|LEGAL)-DOC-\d+", raw_content)
        if id_match and metadata["doc_id"] == "UNKNOWN":
            metadata["doc_id"] = id_match.group(0)

        # Format sections with ##
        cleaned_lines = []
        for line in raw_content.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            if re.match(r"^\d+\.\s+[A-Z]", line_str):
                cleaned_lines.append(f"\n## {line_str}")
            else:
                cleaned_lines.append(line_str)

        raw_text = "\n".join(cleaned_lines)
        return {"metadata": metadata, "raw_text": raw_text}

    @classmethod
    def load_dataset_or_directory(cls, path: str) -> List[Dict[str, Any]]:
        """
        Intelligently loads documents from either a dataset file (.json, .jsonl, .csv, .parquet)
        or a directory of enterprise documents (.json, .csv, .docx, .pdf, .txt).
        Applies deduplication by doc_id to ensure single source of truth.
        """
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext == ".json":
                return cls.parse_json_dataset(path)
            elif ext == ".jsonl":
                return cls.parse_jsonl_dataset(path)
            elif ext == ".csv":
                return cls.parse_csv_dataset(path)
            elif ext == ".parquet":
                return cls.parse_parquet_dataset(path)
            elif ext == ".docx":
                return [cls.parse_docx_document(path)]
            elif ext == ".pdf":
                return [cls.parse_pdf_document(path)]
            elif ext in [".txt", ".md"]:
                return [cls.parse_txt_document(path)]

        # If it's a directory:
        parsed_by_doc_id: Dict[str, Dict[str, Any]] = {}
        
        # Check if an enterprise JSON dataset exists inside or nearby
        primary_json = os.path.join(path, "datasets", "enterprise_knowledge_corpus.json")
        if not os.path.exists(primary_json):
            # Check data/datasets/ relative to path
            base = os.path.dirname(path) if not path.endswith("data") else path
            candidate = os.path.join(base, "datasets", "enterprise_knowledge_corpus.json")
            if os.path.exists(candidate):
                primary_json = candidate

        if os.path.exists(primary_json):
            docs = cls.parse_json_dataset(primary_json)
            for d in docs:
                parsed_by_doc_id[d["metadata"]["doc_id"]] = d
            return list(parsed_by_doc_id.values())

        # Fallback recursive scan over directory
        for root, _, files in os.walk(path):
            for file in sorted(files):
                full_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                try:
                    if ext == ".json" and not file.startswith("test_") and not file.startswith("benchmark_"):
                        docs = cls.parse_json_dataset(full_path)
                        for d in docs:
                            parsed_by_doc_id[d["metadata"]["doc_id"]] = d
                    elif ext == ".csv" and "kb" in file.lower():
                        docs = cls.parse_csv_dataset(full_path)
                        for d in docs:
                            parsed_by_doc_id[d["metadata"]["doc_id"]] = d
                    elif ext == ".docx" and DOCX_AVAILABLE:
                        doc = cls.parse_docx_document(full_path)
                        if doc["metadata"]["doc_id"] not in parsed_by_doc_id:
                            parsed_by_doc_id[doc["metadata"]["doc_id"]] = doc
                    elif ext == ".pdf" and PDF_AVAILABLE:
                        doc = cls.parse_pdf_document(full_path)
                        if doc["metadata"]["doc_id"] not in parsed_by_doc_id:
                            parsed_by_doc_id[doc["metadata"]["doc_id"]] = doc
                    elif ext == ".txt":
                        doc = cls.parse_txt_document(full_path)
                        if doc["metadata"]["doc_id"] not in parsed_by_doc_id:
                            parsed_by_doc_id[doc["metadata"]["doc_id"]] = doc
                except Exception as e:
                    # Non-fatal error on corrupted individual file
                    continue

        return list(parsed_by_doc_id.values())

    @classmethod
    def load_directory(cls, dir_path: str) -> List[Dict[str, Any]]:
        """
        Maintains strict backward compatibility with existing pipeline call sites.
        """
        return cls.load_dataset_or_directory(dir_path)
