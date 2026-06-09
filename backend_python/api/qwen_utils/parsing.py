"""
Response parsing utilities for Qwen AI output.

Handles JSON array/object extraction, code fence stripping,
AI preamble removal, and LaTeX formula normalization.
Re-usable from any view, management command, or future service.
"""
import json
import logging
import re

logger = logging.getLogger(__name__)


def strip_code_fence(text: str) -> str:
    """Remove markdown code fences from AI response text."""
    if not text:
        return ''
    stripped = text.strip()
    if stripped.startswith('```'):
        stripped = re.sub(r'^```[a-zA-Z0-9_-]*\s*', '', stripped)
        stripped = re.sub(r'\s*```$', '', stripped).strip()
    return stripped


def clean_ai_markdown(text: str) -> str:
    """Remove common AI preambles and code fences while preserving markdown."""
    if not text:
        return ''
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```[a-zA-Z0-9_-]*\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned).strip()
    preamble_re = re.compile(
        r"^(?:\s*(?:sure[,!\s]*)?)?(?:#+\s*)?(?:here(?:'s| is)|below is|this is|i have prepared|i've prepared)\b[^\n]{0,240}\n+",
        re.IGNORECASE,
    )
    for _ in range(3):
        new = preamble_re.sub('', cleaned).strip()
        if new == cleaned:
            break
        cleaned = new
    return cleaned


def normalize_formulas(text: str) -> str:
    """Post-process AI output to ensure formulas are KaTeX-compatible LaTeX.

    - Wraps lone \\ce{...} in $...$ so KaTeX auto-render catches them.
    - Ensures $$ display math is on its own line.
    """
    if not text:
        return text
    text = re.sub(r'(?<!\$)\\ce\{([^}]*)\}', r'$\\ce{\1}$', text)
    text = re.sub(r'(?<!\n)\$\$(.+?)\$\$(?!\n)', r'\n$$\1$$', text)
    return text


def parse_json_response(text: str) -> list:
    """Extract a JSON array from Qwen's response text."""
    if not text:
        return []
    stripped = strip_code_fence(text)
    try:
        parsed = json.loads(stripped)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', stripped, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                pass
    logger.warning('Failed to parse Qwen JSON array response: %s...', text[:200])
    return []


def parse_json_object_response(text: str) -> dict | None:
    """Extract a JSON object from Qwen's response text."""
    if not text:
        return None
    stripped = strip_code_fence(text)
    try:
        parsed = json.loads(stripped)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', stripped, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                pass
    logger.warning('Failed to parse Qwen JSON object response: %s...', text[:200])
    return None


def dedupe_questions(items: list, existing_normalized: set | list) -> list:
    """Remove duplicate quiz questions based on normalized question text."""
    seen = set(existing_normalized) if isinstance(existing_normalized, (set, list)) else set(existing_normalized)
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        q = (item.get('question') or '').strip()
        options = item.get('options') or []
        if not q or len(options) < 4:
            continue
        key = q.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def dedupe_flashcards(items: list, existing_normalized: set | list) -> list:
    """Remove duplicate flashcards based on normalized front+back text."""
    seen = set(existing_normalized) if isinstance(existing_normalized, (set, list)) else set(existing_normalized)
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        front = (item.get('front') or '').strip()
        back = (item.get('back') or '').strip()
        if not front or not back:
            continue
        key = f'{front} — {back}'.lower()
        if key in seen or front.lower() in seen:
            continue
        seen.add(key)
        out.append(item)
    return out