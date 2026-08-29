import json
import os
from typing import List, Dict, Any
from rag.models.document import Document
from knowledge.schemas import DocumentMetadata


def format_json_to_markdown(data: Any, item_title: str = "") -> str:
    """
    Recursively converts JSON dictionaries and lists into section-structured Markdown.
    """
    if isinstance(data, str):
        return data
    if isinstance(data, (int, float, bool)):
        return str(data)

    lines = []
    if item_title:
        lines.append(f"# {item_title}")

    if isinstance(data, dict):
        for k, v in data.items():
            if v is None or v == "" or v == []:
                continue
            heading = k.replace("_", " ").title()
            if isinstance(v, list):
                lines.append(f"## {heading}")
                for elem in v:
                    if isinstance(elem, dict):
                        sub_title = elem.get("name") or elem.get("label") or elem.get("title") or ""
                        lines.append(format_json_to_markdown(elem, item_title=sub_title))
                    else:
                        lines.append(f"- {elem}")
            elif isinstance(v, dict):
                lines.append(f"## {heading}")
                lines.append(format_json_to_markdown(v))
            else:
                lines.append(f"## {heading}\n{v}")
            lines.append("")

    elif isinstance(data, list):
        for elem in data:
            lines.append(format_json_to_markdown(elem))
            lines.append("")

    return "\n".join(lines).strip()


class JSONLoader:
    """
    Loader for structured JSON datasets (profile, projects, experience, skills, etc.).
    Emits entity-level Document objects with section headers for section-based chunking.
    """

    def __init__(self, structured_dir: str):
        self.structured_dir = structured_dir

    def load_documents(self) -> List[Document]:
        documents = []
        if not os.path.exists(self.structured_dir):
            return documents

        for fname in sorted(os.listdir(self.structured_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(self.structured_dir, fname)
                category = fname.replace(".json", "")
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    if isinstance(data, list):
                        for idx, item in enumerate(data):
                            item_title = ""
                            if isinstance(item, dict):
                                item_title = item.get("name") or item.get("title") or item.get("company") or item.get("degree") or f"{category.capitalize()} #{idx+1}"
                            else:
                                item_title = f"{category.capitalize()} #{idx+1}"

                            content_str = format_json_to_markdown(item, item_title=item_title)
                            if not content_str:
                                content_str = json.dumps(item, indent=2)

                            # Map category to singular source_type
                            source_type_map = {
                                "projects": "project",
                                "experience": "experience",
                                "education": "education",
                                "achievements": "achievement",
                                "certifications": "certification",
                                "skills": "skill",
                                "profile": "profile"
                            }
                            stype = source_type_map.get(category, category)

                            extra_data: Dict[str, Any] = {"source_type": stype, "item_index": idx}
                            if isinstance(item, dict):
                                if "technologies" in item:
                                    extra_data["technologies"] = item["technologies"]
                                if stype == "project":
                                    extra_data["project_id"] = str(item.get("slug") or item.get("id") or item.get("name") or doc_id)
                                    extra_data["entity_id"] = extra_data["project_id"]
                                elif stype == "experience":
                                    extra_data["experience_id"] = str(item.get("company") or doc_id)
                                    extra_data["entity_id"] = extra_data["experience_id"]
                                elif stype == "education":
                                    extra_data["education_id"] = str(item.get("degree") or item.get("institution") or doc_id)
                                    extra_data["entity_id"] = extra_data["education_id"]

                            doc_id = f"json_{category}_{idx}"
                            metadata = DocumentMetadata(
                                source=f"structured/{fname}",
                                doc_id=doc_id,
                                category=category,
                                title=item_title,
                                technologies=extra_data.get("technologies", [])
                            )
                            documents.append(Document(
                                doc_id=doc_id,
                                content=content_str,
                                metadata=metadata,
                                extra=extra_data
                            ))
                    else:
                        item_title = data.get("name") or f"Structured Data: {category.capitalize()}" if isinstance(data, dict) else f"Structured Data: {category.capitalize()}"
                        content_str = format_json_to_markdown(data, item_title=item_title)
                        if not content_str:
                            content_str = json.dumps(data, indent=2)

                        source_type_map = {
                            "projects": "project",
                            "experience": "experience",
                            "education": "education",
                            "achievements": "achievement",
                            "certifications": "certification",
                            "skills": "skill",
                            "profile": "profile"
                        }
                        stype = source_type_map.get(category, category)
                        extra_data = {"source_type": stype}
                        if isinstance(data, dict) and "technologies" in data:
                            extra_data["technologies"] = data["technologies"]

                        doc_id = f"json_{category}"
                        metadata = DocumentMetadata(
                            source=f"structured/{fname}",
                            doc_id=doc_id,
                            category=category,
                            title=item_title,
                            technologies=extra_data.get("technologies", [])
                        )
                        documents.append(Document(
                            doc_id=doc_id,
                            content=content_str,
                            metadata=metadata,
                            extra=extra_data
                        ))
                except Exception as e:
                    print(f"[JSONLoader] Warning: Failed to load {fpath}: {e}")

        return documents

