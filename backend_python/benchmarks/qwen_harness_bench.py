#!/usr/bin/env python3
"""Offline Qwen harness benchmark: parse recall, observation tokens, edit ACI.

Run from backend_python/:

    DEBUG=1 DB_ENGINE=sqlite python benchmarks/qwen_harness_bench.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
os.environ.setdefault('DEBUG', '1')
os.environ.setdefault('DB_ENGINE', 'sqlite')

import django

django.setup()

from api.background_agent.protocol import parse_model_response
from api.background_agent.qwen_harness.observe import compact_tool_content, estimate_tokens
from api.background_agent.qwen_harness.prompt import build_system_prompt


CORPUS = [
    ('json_fence', True, '```json\n{"thought":"x","actions":[{"tool":"list_files","arguments":{}}],"summary":"s"}\n```'),
    ('json_raw', True, '{"thought":"edit","actions":[{"tool":"write_file","arguments":{"path":"a.py","content":"x"}}],"summary":"n"}'),
    ('hermes_single', True, '<tool_call>\n{"name":"read_file","arguments":{"path":"a.py"}}\n</tool_call>'),
    ('hermes_parallel', True, '<tool_call>{"name":"glob_files","arguments":{"pattern":"**/*.py"}}</tool_call>\n<tool_call>{"name":"search_text","arguments":{"query":"foo"}}</tool_call>'),
    ('hermes_done', True, '<tool_call>{"name":"done","arguments":{"summary":"shipped"}}</tool_call>'),
    ('hermes_think', True, '<think>plan</think><tool_call>{"name":"git_status","arguments":{}}</tool_call>'),
    ('qwen_fn', True, '✿FUNCTION✿: list_files\n✿ARGS✿: {"path":"."}'),
    ('fence', True, '```tool\nname: edit_file\nargs:\n  path: a.py\n  old_text: a\n  new_text: b\n```'),
    ('ask', True, '<tool_call>{"name":"ask_user","arguments":{"question":"which?"}}</tool_call>'),
    ('prose', False, 'I changed everything successfully.'),
    ('trailing_comma', True, '{"thought":"e","actions":[{"tool":"list_files","arguments":{},}],"summary":"s",}'),
    ('incomplete', True, '<tool_call>\n{"name": "git_log", "arguments": {"limit": 5}}'),
]


def _legacy_json_only(raw: str) -> bool:
    text = raw.strip()
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end <= start:
        return False
    try:
        payload = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        try:
            payload = json.loads(__import__('re').sub(r',\s*([}\]])', r'\1', text[start:end + 1]))
        except json.JSONDecodeError:
            return False
    return isinstance(payload, dict) and ('actions' in payload or 'thought' in payload)


def main():
    started = time.perf_counter()
    new_hits = 0
    old_hits = 0
    rows = []
    for name, expect_ok, raw in CORPUS:
        parsed = parse_model_response(raw)
        ok = bool(parsed.parse_ok) if expect_ok else (not parsed.parse_ok and not parsed.actions)
        new_hits += int(ok)
        old_ok = _legacy_json_only(raw) if expect_ok else (not _legacy_json_only(raw))
        old_hits += int(old_ok)
        rows.append((name, 'ok' if ok else 'MISS', parsed.protocol, len(parsed.actions), 'yes' if old_ok else 'no'))

    bulky_lines = [{'line': i, 'text': f'payload_line_{i}'} for i in range(1, 201)]
    bulky = json.dumps({'ok': True, 'tool': 'read_file', 'result': {'path': 'mod.py', 'lines': bulky_lines, 'totalLines': 200}})
    compact = compact_tool_content(bulky)
    ratio = len(compact) / max(1, len(bulky))

    prompt = build_system_prompt('Qwen 3.8 Max')
    elapsed = (time.perf_counter() - started) * 1000
    print('Qwen harness offline bench')
    print(f'{"case":<18} {"new":<6} {"proto":<10} {"acts":<5} {"old-json"}')
    for row in rows:
        print(f'{row[0]:<18} {row[1]:<6} {row[2]:<10} {row[3]:<5} {row[4]}')
    print()
    print(f'parse recall          new {new_hits}/{len(CORPUS)}  legacy-json {old_hits}/{len(CORPUS)}')
    print(f'observation tokens    bulky {estimate_tokens(bulky)}  compact {estimate_tokens(compact)}  ratio {ratio:.2f}')
    print(f'system prompt tokens  {estimate_tokens(prompt)}  ({len(prompt)} chars)')
    print(f'elapsed               {elapsed:.1f} ms')
    if new_hits < len(CORPUS):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
