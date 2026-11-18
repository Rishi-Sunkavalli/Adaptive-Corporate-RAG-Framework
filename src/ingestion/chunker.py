"""
Section-Aware Semantic Chunker for Corporate Documents.
Splits document body into searchable, context-preserved chunks.
"""

import re
from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, chunk_size_words: int = 200, overlap_words: int = 40):
        self.chunk_size_words = chunk_size_words
        self.overlap_words = overlap_words

    def chunk_document(self, parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        metadata = parsed_doc["metadata"]
        raw_text = parsed_doc["raw_text"]
        chunks = []

        # Split text into major sections by Markdown headings (## or #)
        sections = re.split(r"\n(?=## |\n# )", raw_text)
        chunk_idx = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Identify section heading
            heading_match = re.match(r"^#+\s*(.*?)\n", section)
            section_title = heading_match.group(1).strip() if heading_match else "General Overview"
            
            # Words in this section
            words = section.split()
            if len(words) <= self.chunk_size_words:
                chunk_id = f"{metadata['doc_id']}_c{chunk_idx:03d}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "doc_id": metadata["doc_id"],
                    "title": metadata["title"],
                    "department": metadata["department"],
                    "version": metadata["version"],
                    "effective_date": metadata["effective_date"],
                    "security_clearance": metadata["security_clearance"],
                    "section": section_title,
                    "breadcrumb": f"{metadata['title']} > {section_title}",
                    "content": section,
                    "word_count": len(words)
                })
                chunk_idx += 1
            else:
                # Sliding window chunking
                step = self.chunk_size_words - self.overlap_words
                for i in range(0, len(words), step):
                    window = words[i:i + self.chunk_size_words]
                    if len(window) < 25 and len(chunks) > 0:
                        # Skip tiny trailing fragments
                        continue
                    
                    window_text = " ".join(window)
                    # Re-prepend section heading if not already starting with it
                    if not window_text.startswith("#"):
                        window_text = f"## {section_title} (cont.)\n" + window_text

                    chunk_id = f"{metadata['doc_id']}_c{chunk_idx:03d}"
                    chunks.append({
                        "chunk_id": chunk_id,
                        "doc_id": metadata["doc_id"],
                        "title": metadata["title"],
                        "department": metadata["department"],
                        "version": metadata["version"],
                        "effective_date": metadata["effective_date"],
                        "security_clearance": metadata["security_clearance"],
                        "section": section_title,
                        "breadcrumb": f"{metadata['title']} > {section_title}",
                        "content": window_text,
                        "word_count": len(window)
                    })
                    chunk_idx += 1

        return chunks

    def chunk_all(self, parsed_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_chunks = []
        for doc in parsed_docs:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks
