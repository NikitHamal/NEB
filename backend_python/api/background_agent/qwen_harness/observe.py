"""Token-efficient Agent-Computer Interface observations.

SWE-agent showed that numbered file views and truncated, labelled tool output
move solve-rate more than extra prompt prose. We keep the stored tool message
as JSON (the session UI parses it) and render this compact view only when the
next model turn is built.
"""
from __future__ import annotations

import json
import re

_DEFAULT_CAP = 8000
_LINE_RE = re.compile(r'^\s*(\d+)\s*[|:]\s?(.*)$')


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def numbered_view(text: str, start_line: int = 1, end_line: int | None = None) -> str:
    lines = (text or '').splitlines()
    start = max(1, int(start_line or 1))
    end = len(lines) if end_line is None else max(start, int(end_line))
    width = max(4, len(str(min(end, len(lines)))))
    out = []
    for index in range(start - 1, min(end, len(lines))):
        out.append(f'{index + 1:>{width}}|{lines[index]}')
    return '\n'.join(out)


def _as_dict(content: str):
    text = (content or '').strip()
    if not text:
        return None
    if text[0] not in '{[':
        return None
    try:
        value = json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _result_payload(payload: dict) -> dict:
    result = payload.get('result')
    if isinstance(result, dict):
        return result
    return payload


def _clip(text: str, cap: int) -> str:
    if len(text) <= cap:
        return text
    return text[:cap].rstrip() + f'\n[truncated {len(text) - cap} chars — request a narrower window or path]'


def _render_read(result: dict) -> str:
    path = result.get('path') or ''
    total = result.get('totalLines')
    view = result.get('view')
    if not view:
        lines = result.get('lines') or []
        chunks = []
        for item in lines:
            if isinstance(item, dict):
                number = item.get('line')
                chunks.append(f'{number:>6}|{item.get("text", "")}' if number is not None else str(item.get('text', '')))
            else:
                chunks.append(str(item))
        view = '\n'.join(chunks)
    header = f'path: {path}'
    if total:
        shown = view.count('\n') + 1 if view else 0
        header += f' ({total} lines, showing {shown})'
        if result.get('truncatedBytes') or (total and shown < total):
            header += ' — use start_line/end_line to page'
    if result.get('binary'):
        return f'{header}\nbinary: true\nsize: {result.get("size", "?")}'
    return f'{header}\n{view}'.rstrip()


def _render_search(result: dict) -> str:
    matches = result.get('matches') or []
    truncated = result.get('truncated')
    body = '\n'.join(str(item) for item in matches[:200])
    header = f'matches: {len(matches)}'
    if truncated:
        header += ' (truncated — narrow path/glob or raise specificity)'
    return f'{header}\n{body}'.rstrip()


def _render_list(result: dict) -> str:
    entries = result.get('entries') or []
    truncated = result.get('truncated')
    header = f'entries: {len(entries)}'
    if truncated:
        header += ' (truncated)'
    return f'{header}\n' + '\n'.join(str(item) for item in entries)


def _render_command(result: dict) -> str:
    argv = result.get('argv') or []
    parts = [
        f'argv: {" ".join(str(part) for part in argv)}' if argv else '',
        f'cwd: {result["cwd"]}' if result.get('cwd') else '',
        f'exit: {result.get("returncode")}',
    ]
    if result.get('duration') is not None:
        parts.append(f'duration: {result["duration"]}s')
    stdout = (result.get('stdout') or '').rstrip()
    stderr = (result.get('stderr') or '').rstrip()
    if stdout:
        parts.append('stdout:\n' + stdout[-6000:])
    if stderr:
        parts.append('stderr:\n' + stderr[-3000:])
    return '\n'.join(part for part in parts if part)


def render_tool_body(payload: dict, cap: int = _DEFAULT_CAP) -> str:
    ok = bool(payload.get('ok', True))
    tool = payload.get('tool') or ''
    error = payload.get('error') or ''
    result = _result_payload(payload)
    lines = [f'ok: {"true" if ok else "false"}']
    if tool:
        lines.insert(0, f'name: {tool}')
    if not ok:
        lines.append(f'error: {error or "tool failed"}')
        hint = ''
        if isinstance(result, dict):
            hint = str(result.get('hint') or '')
        if 'Closest region' in (error or ''):
            lines.append(error)
        elif hint:
            lines.append(hint)
        if tool in ('edit_file', 'multi_edit', 'apply_patch'):
            lines.append('heal: re-read the file and copy old_text verbatim (including indentation), then retry.')
        return _clip('\n'.join(lines), cap)
    renderer = {
        'read_file': _render_read,
        'search_text': _render_search,
        'list_files': _render_list,
        'glob_files': lambda r: _render_list({'entries': r.get('matches') or r.get('entries') or [], 'truncated': r.get('truncated')}),
        'run_command': _render_command,
    }.get(tool)
    if renderer:
        lines.append(renderer(result if isinstance(result, dict) else {}))
    elif isinstance(result, dict):
        interesting = {k: v for k, v in result.items() if k not in ('ok', 'tool') and v not in (None, '', [], {})}
        if interesting:
            try:
                lines.append(json.dumps(interesting, ensure_ascii=False, indent=2)[:cap])
            except (TypeError, ValueError):
                lines.append(str(interesting)[:cap])
    elif result not in (None, '', payload):
        lines.append(str(result)[:cap])
    return _clip('\n'.join(part for part in lines if part), cap)


def compact_tool_content(content: str, cap: int = _DEFAULT_CAP) -> str:
    payload = _as_dict(content)
    if payload is None:
        text = content or ''
        return _clip(text, cap)
    return render_tool_body(payload, cap=cap)


def wrap_tool_response(body: str) -> str:
    return f'<tool_response>\n{body.rstrip()}\n</tool_response>'


def wrap_tool_call(name: str, arguments: dict) -> str:
    payload = {'name': name, 'arguments': arguments or {}}
    return '<tool_call>\n' + json.dumps(payload, ensure_ascii=False) + '\n</tool_call>'


def format_tool_turn(name: str, arguments: dict, content: str, *, hermes: bool = True) -> str:
    body = compact_tool_content(content)
    if not hermes:
        return f'TOOL {name}: {body}'
    return wrap_tool_call(name, arguments) + '\n' + wrap_tool_response(body)
