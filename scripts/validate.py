"""
Data & Structure Validation Script for Akhil Portfolio.
Ensures structural consistency and performs Pydantic schema validation.
"""

import json
import os
import sys
from pydantic import ValidationError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from knowledge.schemas import (
    ProfileSchema,
    Project,
    Experience,
    SkillCategory,
    Education,
    CertificationSchema,
    AchievementSchema,
    DocumentMetadata,
)

REQUIRED_DATA_FILES = [
    "data/profile.py",
    "data/projects.py",
    "data/skills.py",
    "data/experience.py",
    "data/education.py",
]

REQUIRED_STRUCTURED_JSONS = [
    ("knowledge/structured/profile.json", ProfileSchema, False),
    ("knowledge/structured/projects.json", Project, True),
    ("knowledge/structured/experience.json", Experience, True),
    ("knowledge/structured/skills.json", SkillCategory, True),
    ("knowledge/structured/education.json", Education, True),
    ("knowledge/structured/achievements.json", AchievementSchema, True),
    ("knowledge/structured/certifications.json", CertificationSchema, True),
]

REQUIRED_DOCUMENTS = [
    "knowledge/documents/resume.md",
    "knowledge/documents/resumes/resume_ai_ml_engineer.md",
    "knowledge/documents/resumes/resume_data_scientist.md",
    "knowledge/documents/resumes/resume_data_analyst.md",
    "knowledge/documents/linkedin/about.md",
    "knowledge/documents/linkedin/experience.md",
    "knowledge/documents/linkedin/education.md",
    "knowledge/documents/linkedin/skills.md",
    "knowledge/documents/linkedin/achievements.md",
    "knowledge/documents/experience.md",
    "knowledge/documents/skills.md",
    "knowledge/documents/education.md",
    "knowledge/documents/projects/customer-churn-prediction-ml.md",
    "knowledge/documents/projects/youtube-ai-rag-chatbot.md",
    "knowledge/documents/projects/laptop-price-prediction.md",
    "knowledge/documents/projects/multi-utility-rag-chatbot.md",
    "knowledge/documents/projects/diwali-sales-analysis.md",
    "knowledge/documents/projects/iphone-ecommerce-sales-analysis.md",
]

def validate_portfolio_structure():
    all_passed = True
    print("--- Starting Portfolio Structure & Pydantic Schema Validation ---")

    # 1. Check Data Python Files
    for rel_path in REQUIRED_DATA_FILES:
        abs_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(abs_path):
            print(f"[OK] Python Module: {rel_path}")
        else:
            print(f"[FAIL] Missing Python Module: {rel_path}")
            all_passed = False

    # 2. Check Structured JSON Files & Validate with Pydantic Schemas
    for rel_path, schema_cls, is_list in REQUIRED_STRUCTURED_JSONS:
        abs_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(abs_path):
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if is_list:
                    validated = [schema_cls(**item) for item in data]
                    print(f"[OK] Pydantic Validated JSON ({len(validated)} items): {rel_path}")
                else:
                    validated = schema_cls(**data)
                    print(f"[OK] Pydantic Validated JSON (Single Object): {rel_path}")

            except ValidationError as ve:
                print(f"[FAIL] Pydantic Schema Error in {rel_path}:\n{ve}")
                all_passed = False
            except Exception as e:
                print(f"[FAIL] JSON error in {rel_path}: {e}")
                all_passed = False
        else:
            print(f"[FAIL] Missing Structured JSON: {rel_path}")
            all_passed = False

    # 3. Check Document Files & Metadata Map
    metadata_file = os.path.join(BASE_DIR, "knowledge/documents/metadata.json")
    metadata_map = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata_map = json.load(f)
        print(f"[OK] Document Metadata Sidecar ({len(metadata_map)} document keys): knowledge/documents/metadata.json")
    else:
        print("[FAIL] Missing Document Metadata Sidecar: knowledge/documents/metadata.json")
        all_passed = False

    for rel_path in REQUIRED_DOCUMENTS:
        abs_path = os.path.join(BASE_DIR, rel_path)
        doc_key = rel_path.replace("knowledge/documents/", "")
        if os.path.exists(abs_path):
            size = os.path.getsize(abs_path)
            if doc_key in metadata_map:
                try:
                    meta = DocumentMetadata(**metadata_map[doc_key])
                    print(f"[OK] Document & Pydantic Metadata ({size} bytes, source='{meta.source}'): {rel_path}")
                except ValidationError as ve:
                    print(f"[FAIL] Invalid Metadata Schema for {rel_path}:\n{ve}")
                    all_passed = False
            else:
                print(f"[FAIL] Missing Metadata Key for Document: {doc_key}")
                all_passed = False
        else:
            print(f"[FAIL] Missing Document File: {rel_path}")
            all_passed = False

    print("-----------------------------------------------------")
    if all_passed:
        print("[SUCCESS] All structure and Pydantic schema validation checks passed!")
    else:
        print("[FAILURE] Validation detected missing or invalid schemas.")
    return all_passed

if __name__ == "__main__":
    success = validate_portfolio_structure()
    sys.exit(0 if success else 1)
