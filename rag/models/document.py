"""
Document, Chunk, and SearchResult data models for RAG pipeline.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from knowledge.schemas import DocumentMetadata, RAGDocument


class Document(BaseModel):
    """
    Represents a unified document ingested into the RAG system.
    """
    doc_id: str
    content: str
    metadata: DocumentMetadata = Field(default_factory=lambda: DocumentMetadata(source="unknown"))
    extra: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_rag_document(cls, rag_doc: RAGDocument, doc_id: Optional[str] = None) -> "Document":
        id_val = doc_id or rag_doc.metadata.doc_id or rag_doc.metadata.source
        return cls(
            doc_id=id_val,
            content=rag_doc.content,
            metadata=rag_doc.metadata
        )


class DocumentChunk(BaseModel):
    """
    Unified common document chunk object for BM25 and Vector Search.
    """
    id: str
    text: str
    source: str
    source_type: str = "general"
    category: str = "general"
    project_id: Optional[str] = None
    experience_id: Optional[str] = None
    education_id: Optional[str] = None
    entity_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def chunk_id(self) -> str:
        return self.id

    @property
    def doc_id(self) -> str:
        return self.source

    @property
    def content(self) -> str:
        return self.text

    @property
    def technologies(self) -> List[str]:
        return self.metadata.get("technologies", [])

    @property
    def section(self) -> str:
        return self.metadata.get("section", "General")



class Chunk(DocumentChunk):
    """
    Subclass of DocumentChunk maintained for backward compatibility.
    """
    def __init__(self, **data: Any):
        if "chunk_id" in data and "id" not in data:
            data["id"] = data.pop("chunk_id")
        if "content" in data and "text" not in data:
            data["text"] = data.pop("content")
        if "doc_id" in data and "source" not in data:
            data["source"] = data.pop("doc_id")
        if "metadata" in data and hasattr(data["metadata"], "model_dump"):
            meta_obj = data["metadata"]
            meta_dict = meta_obj.model_dump()
            data["metadata"] = meta_dict
            if "source_type" in meta_dict and "source_type" not in data:
                data["source_type"] = meta_dict["source_type"]
            if "category" in meta_dict and "category" not in data and meta_dict["category"]:
                data["category"] = meta_dict["category"]
        super().__init__(**data)


class SearchResult(BaseModel):
    """
    Represents a single retrieval match for a query.
    """
    chunk: DocumentChunk
    score: float
    retrieval_method: str = "bm25"

