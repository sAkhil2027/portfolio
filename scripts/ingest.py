"""
Data & Knowledge Ingestion Script for Akhil Portfolio.
Loads structured JSON data and markdown documents from knowledge/
and validates structured datasets & document metadata into Pydantic models.
"""

import json
import os
import sys

# Ensure root workspace is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from knowledge.schemas import (
    ProfileSchema,
    Project,
    Experience,
    SkillCategory,
    Education,
    CertificationSchema,
    AchievementSchema,
    DocumentMetadata,
    RAGDocument,
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
STRUCTURED_DIR = os.path.join(KNOWLEDGE_DIR, "structured")
DOCUMENTS_DIR = os.path.join(KNOWLEDGE_DIR, "documents")

def load_json_file(directory, filename):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def load_markdown_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return None

def ingest_all_knowledge():
    """
    Ingests all structured datasets and document files into a validated knowledge repository with RAG metadata.
    """
    print("Ingesting and validating structured knowledge datasets with Pydantic...")

    profile_raw = load_json_file(STRUCTURED_DIR, "profile.json")
    projects_raw = load_json_file(STRUCTURED_DIR, "projects.json")
    experience_raw = load_json_file(STRUCTURED_DIR, "experience.json")
    skills_raw = load_json_file(STRUCTURED_DIR, "skills.json")
    education_raw = load_json_file(STRUCTURED_DIR, "education.json")
    achievements_raw = load_json_file(STRUCTURED_DIR, "achievements.json")
    certifications_raw = load_json_file(STRUCTURED_DIR, "certifications.json")

    structured_knowledge = {
        "profile": ProfileSchema(**profile_raw) if profile_raw else None,
        "projects": [Project(**p) for p in projects_raw] if projects_raw else [],
        "experience": [Experience(**e) for e in experience_raw] if experience_raw else [],
        "skills": [SkillCategory(**s) for s in skills_raw] if skills_raw else [],
        "education": [Education(**e) for e in education_raw] if education_raw else [],
        "achievements": [AchievementSchema(**a) for a in achievements_raw] if achievements_raw else [],
        "certifications": [CertificationSchema(**c) for c in certifications_raw] if certifications_raw else [],
    }

    print("Ingesting document files and attaching RAG DocumentMetadata...")
    metadata_map = load_json_file(DOCUMENTS_DIR, "metadata.json") or {}
    rag_documents = []

    # Recursively scan DOCUMENTS_DIR for all .md files
    for root, _, files in os.walk(DOCUMENTS_DIR):
        for fname in sorted(files):
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, DOCUMENTS_DIR).replace("\\", "/")
                content = load_markdown_file(fpath)
                if content and rel_path in metadata_map:
                    meta = DocumentMetadata(**metadata_map[rel_path])
                    rag_documents.append(RAGDocument(content=content, metadata=meta))

    print(f"Ingestion Complete: Validated {len(structured_knowledge)} structured datasets and {len(rag_documents)} RAG documents with rich metadata.")
    return {
        "structured": structured_knowledge,
        "rag_documents": rag_documents
    }

if __name__ == "__main__":
    knowledge_base = ingest_all_knowledge()
