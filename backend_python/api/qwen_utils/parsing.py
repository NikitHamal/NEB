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



def _match_brace_end(text: str, open_idx: int) -> int:
    """Given the index of a '{' in ``text``, return the index just past its
    matching '}' (handling nested braces and backslash escapes), or -1."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def normalize_formulas(text: str) -> str:
    """Post-process AI output to ensure formulas are KaTeX-compatible LaTeX.

    - Wraps lone \\ce{...} in $...$ so KaTeX auto-render catches them.
      Handles nested braces (e.g. \\ce{^{235}U}) and does NOT double-wrap
      occurrences that are already inside $...$ or $$...$$ math.
    - Ensures $$ display math starts on its own line.
    - Heals bare unit/orbital LaTeX that leaked outside math (e.g.
      ``kJ mol^{-1}`` or ``2p^3``) by wrapping in $...$ and stripping stray
      escapes (e.g. ``\\^{-1\\}`` → ``^{-1}``).
    """
    if not text:
        return text

    # Heal the common broken split: "kJ mol$^{-1}$" → "$kJ mol^{-1}$"
    text = re.sub(r'kJ\s+mol\s*\$\s*\^\s*\{-1\}\s*\$', r'$kJ mol^{-1}$', text)
    text = re.sub(r'kJ\s+mol\s*\\\$\s*\\\^\s*\\?\{?\s*-1\s*\\?\}?\s*\\\$', r'$kJ mol^{-1}$', text)

    _BARE_ORBITAL_RE = re.compile(r'[1-6][spdf]\s*\^\s*(?:\{\s*\d+\s*\}|\d+)')
    _BARE_UNIT_RE = re.compile(r'(?:kJ\s+)?mol\s*\\?\^\s*\\?\{?\s*-1\s*\\?\}?', re.IGNORECASE)

    out = []
    i = 0
    n = len(text)
    in_inline = False   # inside $...$
    in_display = False  # inside $$...$$
    while i < n:
        if text.startswith('$$', i):
            in_display = not in_display
            out.append('$$')
            i += 2
            continue
        if text[i] == '$' and not in_display:
            in_inline = not in_inline
            out.append('$')
            i += 1
            continue
        if not in_inline and not in_display:
            m = _BARE_ORBITAL_RE.match(text, i)
            if m:
                raw = m.group(0)
                clean = re.sub(r'\\([{}^])', r'\1', raw)
                out.append('$' + clean.strip() + '$')
                i = m.end()
                continue
            m = _BARE_UNIT_RE.match(text, i)
            if m:
                raw = m.group(0)
                # Only wrap if it actually contains ^ (plain kJ/mol stays plain)
                if '^' in raw or '\\^' in raw:
                    clean = re.sub(r'\\([{}^])', r'\1', raw)
                    # Normalize "kJ mol^{-1}" → keep as is inside $
                    out.append('$' + clean.strip() + '$')
                    i = m.end()
                    continue
        if text[i] == '\\' and i + 1 < n:
            if (not in_inline and not in_display) and text.startswith('\\ce', i):
                j = i + 3
                if j < n and text[j] == '{':
                    end = _match_brace_end(text, j)
                    if end != -1:
                        out.append('$' + text[i:end] + '$')
                        i = end
                        continue
            # Copy the escape pair verbatim so '\\$' never toggles math state.
            out.append(text[i:i + 2])
            i += 2
            continue
        out.append(text[i])
        i += 1

    result = ''.join(out)
    result = re.sub(r'(?<!\n)\$\$(.+?)\$\$(?!\n)', r'\n$$\1$$', result)
    return result


# A backslash followed by anything that is NOT a valid JSON escape character.
_INVALID_JSON_ESCAPE_RE = re.compile(r'\\(?!["\\/bfnrtu])')


def _repair_json_escapes(text: str) -> str:
    """Double any backslash that does not start a valid JSON escape.

    AI models often emit raw LaTeX like ``"\\ce{H2O}"`` inside JSON strings,
    which is invalid JSON (``\\c`` is not a recognised escape). Doubling the
    backslash turns it into a valid escaped backslash.
    """
    if not text:
        return text
    return _INVALID_JSON_ESCAPE_RE.sub(r'\\\\', text)


def _extract_balanced(text: str, open_ch: str, close_ch: str) -> str | None:
    """Return the first balanced ``open_ch...close_ch`` block in ``text``.

    Uses a small stack-based scanner that respects JSON string literals and
    backslash escapes, unlike a greedy regex.
    """
    if not text:
        return None
    start = text.find(open_ch)
    if start == -1:
        return None
    depth = 0
    in_str = False
    escaped = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def _try_json_loads(candidate: str, expect_type: type):
    """Try to parse ``candidate`` as JSON, with a LaTeX-escape repair pass."""
    for attempt in (candidate, _repair_json_escapes(candidate)):
        try:
            parsed = json.loads(attempt)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(parsed, expect_type):
            return parsed
    return None


def parse_json_response(text: str) -> list:
    """Extract a JSON array from Qwen's response text."""
    if not text:
        return []
    stripped = strip_code_fence(text)
    parsed = _try_json_loads(stripped, list)
    if parsed is not None:
        return parsed
    extracted = _extract_balanced(stripped, '[', ']')
    if extracted:
        parsed = _try_json_loads(extracted, list)
        if parsed is not None:
            return parsed
    logger.warning('Failed to parse Qwen JSON array response: %s...', text[:200])
    return []


def parse_json_object_response(text: str) -> dict | None:
    """Extract a JSON object from Qwen's response text."""
    if not text:
        return None
    stripped = strip_code_fence(text)
    parsed = _try_json_loads(stripped, dict)
    if parsed is not None:
        return parsed
    extracted = _extract_balanced(stripped, '{', '}')
    if extracted:
        parsed = _try_json_loads(extracted, dict)
        if parsed is not None:
            return parsed
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