"""Helpers for structured, interactive syllabus content.

The rich syllabus format is deliberately small and JSON-friendly so it can be
produced from uploaded learning resources, edited by admins, returned to native
clients, and rendered progressively on the website without replacing the
existing Markdown syllabus fields.
"""
from __future__ import annotations

import re
from typing import Any


ALLOWED_BLOCK_TYPES = {"section", "formula", "interactive", "callout"}


def _string(value: Any) -> str:
    return str(value or "").strip()


def _page_label(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        clean = [str(v).strip() for v in value if str(v).strip()]
        return ", ".join(clean)
    return str(value).strip()


def _first_page(value: Any) -> str:
    label = _page_label(value)
    match = re.search(r"\d+", label)
    return match.group(0) if match else ""


def _flatten(value: Any) -> list[str]:
    """Collect human-searchable strings from nested JSON without indexing keys."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (int, float, bool)):
        return [str(value)]
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(_flatten(item))
        return out
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        for item in value:
            out.extend(_flatten(item))
        return out
    return []


def syllabus_search_text(entry) -> str:
    parts = [
        getattr(entry, "chapter_title", "") or "",
        getattr(entry, "chapter_id", "") or "",
        getattr(entry, "text_content", "") or "",
        getattr(entry, "question_answers", "") or "",
    ]
    parts.extend(_flatten(getattr(entry, "rich_content", {}) or {}))
    return " ".join(parts).lower()


def prepare_rich_content(entry) -> dict[str, Any]:
    """Return a template-friendly normalized rich-content dictionary.

    Unknown block types are ignored rather than rendered as arbitrary markup.
    The raw JSON stays available through the API separately.
    """
    raw = getattr(entry, "rich_content", {}) or {}
    if not isinstance(raw, dict):
        raw = {}

    topics = raw.get("topics") if isinstance(raw.get("topics"), list) else []
    objectives = raw.get("learning_objectives") if isinstance(raw.get("learning_objectives"), list) else []
    source = raw.get("source") if isinstance(raw.get("source"), dict) else {}
    blocks_raw = raw.get("blocks") if isinstance(raw.get("blocks"), list) else []

    chapter_id = _string(getattr(entry, "chapter_id", "chapter")) or "chapter"
    chapter_title = _string(getattr(entry, "chapter_title", "Chapter")) or "Chapter"
    source_resource_id = _string(getattr(entry, "source_resource_id", ""))
    source_label = _string(getattr(entry, "source_label", "")) or _string(source.get("label"))

    blocks: list[dict[str, Any]] = []
    for idx, item in enumerate(blocks_raw):
        if not isinstance(item, dict):
            continue
        block_type = _string(item.get("type")).lower()
        if block_type not in ALLOWED_BLOCK_TYPES:
            continue

        title = _string(item.get("title"))
        markdown = _string(item.get("markdown"))
        latex = _string(item.get("latex"))
        kind = _string(item.get("kind"))
        config = item.get("config") if isinstance(item.get("config"), dict) else {}
        variables = item.get("variables") if isinstance(item.get("variables"), list) else []
        source_pages = _page_label(item.get("source_pages"))
        dom_id = f"rich-{chapter_id}-{idx}"
        prompt_subject = title or kind.replace("-", " ") or block_type
        ai_prompt = _string(item.get("ai_prompt")) or (
            f"Explain {prompt_subject} from {chapter_title}. Keep the explanation tied to the syllabus source, "
            "define the symbols, and show the reasoning step by step where useful."
        )

        blocks.append({
            "type": block_type,
            "title": title,
            "markdown": markdown,
            "latex": latex,
            "kind": kind,
            "config": config,
            "variables": variables,
            "source_pages": source_pages,
            "source_page_start": _first_page(item.get("source_pages")),
            "dom_id": dom_id,
            "ai_prompt": ai_prompt,
            "search_text": " ".join(_flatten(item)).lower(),
        })

    return {
        "version": raw.get("version", 1),
        "topics": [str(x) for x in topics if str(x).strip()],
        "learning_objectives": [str(x) for x in objectives if str(x).strip()],
        "source": source,
        "source_label": source_label,
        "source_resource_id": source_resource_id,
        "blocks": blocks,
        "has_blocks": bool(blocks),
    }
