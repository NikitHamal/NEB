"""Format repair, self-heal notes, and anti-loop signatures."""
from __future__ import annotations

import json
import re

from api.background_agent.protocol import ParsedResponse

_EDIT_TOOLS = frozenset({'edit_file', 'multi_edit', 'apply_patch'})


def needs_format_repair(parsed: ParsedResponse) -> bool:
    return not bool(getattr(parsed, 'parse_ok', False))


def action_signature(actions) -> str:
    parts = []
    for action in actions or []:
        if not isinstance(action, dict):
            continue
        tool = (action.get('tool') or '').strip()
        arguments = action.get('arguments') if isinstance(action.get('arguments'), dict) else {}
        keys = []
        for key in ('path', 'query', 'pattern', 'source', 'destination', 'message'):
            if arguments.get(key):
                keys.append(f'{key}={str(arguments[key])[:80]}')
        if tool == 'run_command':
            argv = arguments.get('argv') or []
            keys.append('argv=' + ' '.join(str(part) for part in argv)[:120])
        if tool == 'edit_file':
            keys.append('old=' + re.sub(r'\s+', ' ', str(arguments.get('old_text') or ''))[:80])
        parts.append(tool + ':' + ','.join(keys))
    return '|'.join(parts)[:1500]


def heal_note(tool: str, result: dict) -> str:
    if not result or result.get('ok', False):
        return ''
    name = (tool or result.get('tool') or 'tool').strip()
    error = str(result.get('error') or '')[:800]
    if name in _EDIT_TOOLS:
        return (
            f'The last {name} failed. {error}\n'
            'Re-read the target file, copy the exact current bytes into old_text '
            '(including indentation and blank lines), and retry a smaller unique block.'
        )
    if name == 'run_command':
        return f'The last command failed. Inspect stdout/stderr and fix the cause before repeating it.\n{error}'
    if error:
        return f'The last {name} failed: {error}'
    return ''


def thought_signature(thought: str) -> str:
    return re.sub(r'\s+', ' ', (thought or '').strip().lower())[:1500]


def dump_actions(actions) -> str:
    try:
        return json.dumps(actions or [], ensure_ascii=False)[:4000]
    except (TypeError, ValueError):
        return str(actions)[:4000]
