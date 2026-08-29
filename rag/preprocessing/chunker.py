import re
from typing import List, Dict, Any, Tuple
from rag.models.document import Document, DocumentChunk, Chunk


class TextChunker:
    """
    Splits Document content into manageable DocumentChunk objects using section-based splitting and sliding window fallback.
    """

    def __init__(self, chunk_size: int = 650, chunk_overlap: int = 130):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _split_into_sections(self, text: str) -> List[Tuple[str, str]]:
        """
        Splits markdown text by headers (#, ##, ###) into (section_title, section_text) tuples.
        """
        pattern = r'(?m)^(#{1,6}\s+.+)$'
        parts = re.split(pattern, text)
        sections: List[Tuple[str, str]] = []

        if not parts:
            return [("General", text)]

        current_title = "Overview"
        current_content = parts[0].strip()

        if current_content:
            sections.append((current_title, current_content))

        for i in range(1, len(parts), 2):
            header = parts[i].strip()
            content = parts[i+1].strip() if (i + 1) < len(parts) else ""
            title_text = re.sub(r'^#+\s+', '', header).strip()
            section_full_text = f"{header}\n{content}".strip() if content else header
            sections.append((title_text, section_full_text))

        return sections

    def _sliding_window(self, text: str, document: Document, source_val: str, source_type_val: str, category_val: str, meta_dict: Dict[str, Any], section_title: str, start_idx: int) -> Tuple[List[DocumentChunk], int]:
        chunks = []
        start = 0
        text_len = len(text)
        chunk_idx = start_idx

        while start < text_len:
            end = start + self.chunk_size

            if end < text_len:
                break_point = text.rfind("\n", start, end)
                if break_point == -1 or break_point <= start:
                    break_point = text.rfind(" ", start, end)

                if break_point > start:
                    end = break_point

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = f"{document.doc_id}_chunk_{chunk_idx}"
                chunk_meta = dict(meta_dict)
                chunk_meta["chunk_index"] = chunk_idx
                chunk_meta["doc_id"] = document.doc_id
                chunk_meta["section"] = section_title

                chunks.append(DocumentChunk(
                    id=chunk_id,
                    text=chunk_text,
                    source=source_val,
                    source_type=source_type_val,
                    category=category_val,
                    project_id=chunk_meta.get("project_id"),
                    experience_id=chunk_meta.get("experience_id"),
                    education_id=chunk_meta.get("education_id"),
                    entity_id=chunk_meta.get("entity_id"),
                    metadata=chunk_meta
                ))
                chunk_idx += 1

            if end >= text_len:
                break

            start = max(start + 1, end - self.chunk_overlap)

        return chunks, chunk_idx

    def chunk_document(self, document: Document) -> List[DocumentChunk]:
        """
        Chunks a single Document into section-based DocumentChunk objects.
        """
        text = document.content
        if not text:
            return []

        # Extract metadata fields
        meta_dict: Dict[str, Any] = {}
        source_val = document.doc_id
        source_type_val = "document"
        category_val = "general"

        if hasattr(document.metadata, "model_dump"):
            meta_dict = document.metadata.model_dump()
            if document.metadata.category:
                category_val = document.metadata.category

        if document.extra:
            meta_dict.update(document.extra)
            if "source_type" in document.extra:
                source_type_val = str(document.extra["source_type"])
            if "category" in document.extra:
                category_val = str(document.extra["category"])

        sections = self._split_into_sections(text)
        all_chunks: List[DocumentChunk] = []
        chunk_counter = 0

        # If document has no section headers, fall back directly to sliding window
        if len(sections) <= 1 and not re.search(r'(?m)^#{1,6}\s+', text):
            sub_chunks, _ = self._sliding_window(text, document, source_val, source_type_val, category_val, meta_dict, "General", 0)
            return sub_chunks

        for sec_title, sec_text in sections:
            if not sec_text:
                continue

            # If section fits within 1.5x chunk_size, keep section whole
            if len(sec_text) <= self.chunk_size * 1.5:
                chunk_id = f"{document.doc_id}_chunk_{chunk_counter}"
                chunk_meta = dict(meta_dict)
                chunk_meta["chunk_index"] = chunk_counter
                chunk_meta["doc_id"] = document.doc_id
                chunk_meta["section"] = sec_title

                all_chunks.append(DocumentChunk(
                    id=chunk_id,
                    text=sec_text,
                    source=source_val,
                    source_type=source_type_val,
                    category=category_val,
                    project_id=chunk_meta.get("project_id"),
                    experience_id=chunk_meta.get("experience_id"),
                    education_id=chunk_meta.get("education_id"),
                    entity_id=chunk_meta.get("entity_id"),
                    metadata=chunk_meta
                ))
                chunk_counter += 1
            else:
                # If section exceeds limit, split section via sliding window
                sec_chunks, chunk_counter = self._sliding_window(
                    sec_text, document, source_val, source_type_val, category_val, meta_dict, sec_title, chunk_counter
                )
                all_chunks.extend(sec_chunks)

        return all_chunks

    def chunk_documents(self, documents: List[Document]) -> List[DocumentChunk]:
        """
        Chunks a list of Document objects.
        """
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks


