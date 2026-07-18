"""Parser for tool calls embedded in LLM responses.

The agent runs in *prompted tool-call* mode: the LLM is told to emit fenced
code blocks (see constants.TOOL_CALL_FENCE_OPEN) of a simple ``name: / args:``
shape, and this module extracts them and converts them into structured Python
values.

Why handled in Python (not as native tool_calls):
  Several reverse-engineered providers used by NEBians (chat.qwen.ai,
  AI4Bharat Arena, eGov, DeepAI free tier) do not honor OpenAI's tool_calls
  JSON Schema path. They drop the `tools` field entirely or refuse to produce
  structured outputs reliably. Coercing them to use prompt-defined tool
  blocks is far more portable, deterministic and cheaper.

Tolerant parsing:
  · Trailing/leading whitespace inside the fence is ignored.
  · ``name: foo`` and ``name=foo`` both work.
  · ``args`` may be absent (tools that take no arguments).
  · Block-scalar values (`key: |2 ...`, `key: | ...`) are collected until
    indentation drops back to the args-section indent.
  · JSON values for lists/dicts/numbers/bools/None are detected inline.

The parser returns ToolCall dataclass objects — they pass cleanly into the
tool registry for execution.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .constants import TOOL_CALL_FENCE_CLOSE, TOOL_CALL_FENCE_OPEN

_NAME_LINE_RE = re.compile(r'^\s*name\s*[=:]\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*$')
_KV_LINE_RE = re.compile(r'^(\s*)([^:\s][^:]*?)\s*[=:]\s*(.*)$')

_BOOL_TRUE = {'true', 'yes'}
_BOOL_FALSE = {'false', 'no'}
_NULL_VALUES = {'null', 'none', '~'}


@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any] = field(default_factory=dict)
    raw: str = ''
    start: int = 0
    end: int = 0


def strip_fences(text: str) -> str:
    return text.replace(TOOL_CALL_FENCE_OPEN, '').replace(TOOL_CALL_FENCE_CLOSE, '')


def find_tool_blocks(text: str) -> List[Tuple[int, int]]:
    """Return list of (start, end) character offsets for every ```tool block.

    ``start`` is the character index of the opening backticks; ``end`` is the
    character index just past the closing backticks.
    """
    blocks: List[Tuple[int, int]] = []
    i = 0
    open_token = TOOL_CALL_FENCE_OPEN
    close_token = TOOL_CALL_FENCE_CLOSE
    while True:
        s = text.find(open_token, i)
        if s == -1:
            break
        e = text.find(close_token, s + len(open_token))
        if e == -1:
            break
        blocks.append((s, e + len(close_token)))
        i = e + len(close_token)
    return blocks


def _parse_yamlish_block(body: str) -> Tuple[str, Dict[str, Any]]:
    """Parse a small YAML-ish body that begins with ``name: <tool>`` followed by
    an optional ``args:`` section with ``key: value`` lines and block-scalars.

    Block scalars (lines starting with a key followed by ``|`` or ``|2``) are
    gathered until the next line whose indent is at-or-below the key's own
    indent. Indent baseline = first non-empty content line indent. Extra
    leading spaces on the first line of a scalar body are preserved.
    """
    lines = body.splitlines()
    name: Optional[str] = None
    args: Dict[str, Any] = {}
    i = 0
    n = len(lines)

    while i < n and not lines[i].strip():
        i += 1
    if i >= n:
        return '', {}

    m = _NAME_LINE_RE.match(lines[i])
    if m:
        name = m.group(1)
        i += 1

    while i < n and not lines[i].strip():
        i += 1

    if i >= n or not lines[i].lstrip().startswith(('args', 'arguments')):
        return name or '', args

    args_indent = len(lines[i]) - len(lines[i].lstrip())
    i += 1

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= args_indent:
            break
        raw = line[indent:]
        if not raw:
            i += 1
            continue
        m = _KV_LINE_RE.match(line)
        if not m:
            i += 1
            continue
        key = m.group(2).strip()
        rest = m.group(3)
        if rest == '':
            scalar_start = i + 1
            try:
                block_indent_arg = _collect_block_scalar(lines, scalar_start, args_indent)
                if block_indent_arg is not None:
                    text_val, next_i, indent_extra = block_indent_arg
                    args[key] = _maybe_json(text_val, indent_extra=indent_extra)
                    i = next_i
                    continue
            except _BadBlockScalar:
                pass
            args[key] = ''
            i += 1
            continue
        if rest.strip().startswith('|') or rest.strip().startswith('>'):
            ch = rest.strip()[0]
            marker = rest.strip()[1:] or '-1'
            try:
                block_chomp = int(marker) if marker.lstrip('-').isdigit() else -1
            except Exception:
                block_chomp = -1
            block_indent_arg = _collect_block_scalar(lines, i + 1, indent)
            if block_indent_arg is None:
                args[key] = ''
                i += 1
                continue
            text_val, next_i, indent_extra = block_indent_arg
            if ch == '>':
                text_val = _folded_to_plain(text_val)
            if block_chomp >= 0:
                text_val = text_val.rstrip('\n')
            else:
                text_val = text_val.rstrip('\n') + '\n'
            args[key] = _maybe_json(text_val, indent_extra=indent_extra)
            i = next_i
            continue
        args[key] = _maybe_json(rest.strip())
        i += 1

    return name or '', args


def _maybe_json(text: str, indent_extra: int = 0):
    if indent_extra > 0:
        return text
    s = text.strip()
    if not s:
        return ''
    if s in _NULL_VALUES:
        return None
    low = s.lower()
    if low in _BOOL_TRUE:
        return True
    if low in _BOOL_FALSE:
        return False
    if (s.startswith('{') and s.endswith('}')) or (s.startswith('[') and s.endswith(']')):
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            pass
    if re.match(r'^-?\d+(\.\d+)?$', s):
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except ValueError:
            pass
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        try:
            return json.loads(s.replace("'", '"'))
        except json.JSONDecodeError:
            return s[1:-1]
    return s


def _collect_block_scalar(lines: List[str], start: int, parent_indent: int) -> Optional[Tuple[str, int, int]]:
    """Collect a block scalar starting at ``lines[start]`` until indentation
    drops back to ``parent_indent``. Returns (value, next_line_index,
    indent_extra). ``indent_extra`` is the number of spaces the first content
    line is indented BEYOND ``parent_indent - 1`` — caller must prepend those
    spaces to every collected line.
    """
    n = len(lines)
    j = start
    first = None
    while j < n:
        line = lines[j]
        if line.strip() == '':
            j += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= parent_indent:
            return None
        first = (j, indent)
        break
    if first is None:
        return None
    first_j, first_indent = first
    baseline = first_indent
    collected_lines: List[str] = []
    j = first_j
    while j < n:
        line = lines[j]
        if line.strip() == '':
            collected_lines.append('')
            j += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent < baseline:
            break
        if indent >= baseline:
            collected_lines.append(line[baseline:])
        else:
            break
        j += 1
    indent_extra = first_indent - baseline
    value = '\n'.join(collected_lines)
    if value and indent_extra > 0:
        value = (' ' * indent_extra) + value
    return value, j, indent_extra


def _folded_to_plain(text: str) -> str:
    out_lines: List[str] = []
    paragraph: List[str] = []
    for line in text.split('\n'):
        if line.strip() == '':
            if paragraph:
                out_lines.append(' '.join(paragraph))
                paragraph = []
            out_lines.append('')
            continue
        paragraph.append(line.strip())
    if paragraph:
        out_lines.append(' '.join(paragraph))
    return '\n'.join(out_lines)


class _BadBlockScalar(Exception):
    pass


def parse(text: str) -> Tuple[str, List[ToolCall]]:
    """Parse tool calls out of ``text``.

    Returns ``(clean_text, calls)`` where ``clean_text`` is the response with
    every well-formed `````tool`` block removed, and ``calls`` is the list of
    extracted ToolCall objects.
    """
    blocks = find_tool_blocks(text)
    calls: List[ToolCall] = []
    if not blocks:
        return text, []

    clean = []
    last = 0
    for s, e in blocks:
        clean.append(text[last:s])
        body = text[s + len(TOOL_CALL_FENCE_OPEN):e - len(TOOL_CALL_FENCE_CLOSE)].strip('\n')
        last = e
        name, args = _parse_yamlish_block(body)
        if not name:
            continue
        calls.append(ToolCall(name=name, args=args, raw=body, start=s, end=e))
    clean.append(text[last:])
    return ''.join(clean), calls


def looks_like_done_call(call: ToolCall) -> bool:
    return call.name == 'done'


def merge_calls_with_assistant(text: str) -> Tuple[str, List[ToolCall]]:
    """Convenience: returns (assistant_text_without_tool_fences, calls)."""
    return parse(text)
