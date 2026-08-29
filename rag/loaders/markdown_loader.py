"""
Markdown Knowledge Loader module.
Loads document markdown files from knowledge/documents/ into Document models.
"""

import json
import os
from typing import List
from rag.models.document import Document
from knowledge.schemas import DocumentMetadata


class MarkdownLoader:
    """
    Loader for markdown documents stored in knowledge/documents/.
    Reads metadata.json to map file paths to DocumentMetadata.
    """

    def __init__(self, documents_dir: str):
        self.documents_dir = documents_dir

    def load_documents(self) -> List[Document]:
        documents = []
        if not os.path.exists(self.documents_dir):
            return documents

        metadata_map_path = os.path.join(self.documents_dir, "metadata.json")
        metadata_map = {}
        if os.path.exists(metadata_map_path):
            try:
                with open(metadata_map_path, "r", encoding="utf-8") as f:
                    metadata_map = json.load(f)
            except Exception as e:
                print(f"[MarkdownLoader] Warning: Failed to load metadata.json: {e}")

        for root, _, files in os.walk(self.documents_dir):
            for fname in sorted(files):
                if fname.endswith(".md"):
                    fpath = os.path.join(root, fname)
                    rel_path = os.path.relpath(fpath, self.documents_dir).replace("\\", "/")
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()

                        if rel_path in metadata_map:
                            meta = DocumentMetadata(**metadata_map[rel_path])
                        else:
                            meta = DocumentMetadata(
                                source=f"documents/{rel_path}",
                                doc_id=rel_path,
                                title=os.path.basename(rel_path).replace(".md", "").replace("_", " ").title()
                            )

                        doc_id = meta.doc_id or rel_path.replace(".md", "")
                        category_val = meta.category or (rel_path.split("/")[0] if "/" in rel_path else "general")
                        
                        # Infer source_type from category or path
                        stype = "project" if ("project" in rel_path.lower() or category_val == "projects") else (
                            "experience" if "experience" in rel_path.lower() else (
                                "education" if "education" in rel_path.lower() else "document"
                            )
                        )

                        extra_data = {
                            "source_type": stype,
                            "category": category_val,
                            "technologies": meta.technologies,
                            "github": meta.github,
                            "demo": meta.demo
                        }
                        if stype == "project":
                            extra_data["project_id"] = doc_id
                            extra_data["entity_id"] = doc_id
                        elif stype == "experience":
                            extra_data["experience_id"] = doc_id
                            extra_data["entity_id"] = doc_id

                        documents.append(Document(
                            doc_id=doc_id,
                            content=content,
                            metadata=meta,
                            extra=extra_data
                        ))
                    except Exception as e:
                        print(f"[MarkdownLoader] Warning: Failed to load {fpath}: {e}")

        return documents
