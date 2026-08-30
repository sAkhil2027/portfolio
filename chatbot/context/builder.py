"""
Context Builder module.
Formats Phase 3 search results into grounded prompt context, citation metadata, and related project lists.
Includes zero-latency near-duplicate text content filtering.
"""

import re
from typing import List, Tuple
from rag.models.document import SearchResult
from chatbot.models.response import Citation


class ContextBuilder:
    """
    Transforms retrieved Phase 3 SearchResult chunks into structured LLM context blocks.
    Deduplicates project IDs and near-duplicate text blocks.
    """

    def build_context(self, search_results: List[SearchResult], similarity_threshold: float = 0.75) -> Tuple[str, List[Citation], List[str]]:
        """
        Formats retrieved SearchResult chunks into a grounded text context, citation list, and related projects list.
        Filters out near-duplicate text content (similarity > threshold).
        Returns: (formatted_context, citations, related_projects)
        """
        if not search_results:
            return "NO RELEVANT KNOWLEDGE CONTEXT FOUND.", [], []

        context_blocks = []
        citations = []
        related_projects = []
        seen_texts = []

        for idx, res in enumerate(search_results, start=1):
            chunk = res.chunk
            text_content = chunk.text.strip()
            
            # Extract metadata attributes cleanly
            title = "Document"
            if isinstance(chunk.metadata, dict):
                title = chunk.metadata.get("title") or chunk.metadata.get("source") or chunk.source
            elif hasattr(chunk.metadata, "title"):
                title = getattr(chunk.metadata, "title", chunk.source)

            source_type = chunk.source_type or "general"
            section_name = chunk.section or "General"
            
            # Extract related project ID if present
            if chunk.project_id and chunk.project_id not in related_projects:
                related_projects.append(chunk.project_id)

            # Build deep link URL if project or section is present
            url = None
            if chunk.project_id:
                url = f"/projects/{chunk.project_id}"
            elif source_type == "project":
                url = "/projects"
            elif source_type == "experience":
                url = "/#experience"
            elif source_type == "education":
                url = "/#education"

            # Create citation model (citations always record source reference)
            citation = Citation(
                citation_id=idx,
                chunk_id=chunk.id,
                title=str(title),
                source=chunk.source,
                section=section_name,
                source_type=source_type,
                url=url,
                score=round(float(res.score), 4)
            )
            citations.append(citation)

            # Near-duplicate text content filtering
            if self._is_near_duplicate(text_content, seen_texts, threshold=similarity_threshold):
                continue

            seen_texts.append(text_content)

            # Build context text block with explicit numbered anchor
            block = (
                f"[Source {idx}] ({citation.title} | {section_name} | {source_type.upper()})\n"
                f"Content: {text_content}\n"
            )
            context_blocks.append(block)

        formatted_context = "\n---\n".join(context_blocks) if context_blocks else "NO RELEVANT KNOWLEDGE CONTEXT FOUND."
        return formatted_context, citations, related_projects

    def _is_near_duplicate(self, new_text: str, seen_texts: List[str], threshold: float = 0.75) -> bool:
        """
        Calculates word-set Jaccard overlap between new_text and previously accepted texts.
        """
        new_words = set(re.findall(r"\w+", new_text.lower()))
        if not new_words:
            return False

        for text in seen_texts:
            seen_words = set(re.findall(r"\w+", text.lower()))
            if not seen_words:
                continue

            intersection = new_words.intersection(seen_words)
            union = new_words.union(seen_words)

            similarity = len(intersection) / max(len(union), 1)
            if similarity >= threshold:
                return True

        return False
