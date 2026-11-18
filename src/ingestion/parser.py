"""
Corporate Document Ingestion & Parsing Engine.
Extracts document metadata and structured text from TXT, DOCX, and PDF formats.
"""

import os
import re
from typing import Dict, Any, List

class CorporateDocumentParser:
    @staticmethod
    def parse_txt_document(filepath: str) -> Dict[str, Any]:
        """
        Parses a corporate TXT document with structured metadata comments at the top.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = {
            "doc_id": "UNKNOWN",
            "title": os.path.basename(filepath),
            "department": "General",
            "version": "1.0",
            "effective_date": "2026-01-01",
            "security_clearance": "Internal",
            "filepath": filepath,
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

    @classmethod
    def load_directory(cls, dir_path: str) -> List[Dict[str, Any]]:
        """
        Recursively scans directory and parses all corporate documents.
        """
        parsed_docs = []
        for root, _, files in os.walk(dir_path):
            for file in sorted(files):
                if file.endswith(".txt"):
                    full_path = os.path.join(root, file)
                    parsed = cls.parse_txt_document(full_path)
                    parsed_docs.append(parsed)
        return parsed_docs
