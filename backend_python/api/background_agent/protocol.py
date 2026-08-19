"""Multi-format tool-call parser for providers without native function calling.

Qwen (and most reverse-engineered web proxies) drop OpenAI `tools`. The models
are still trained on Hermes/Nous XML (`<tool_call>…</tool_call>`). This parser
accepts that native format first, then the legacy JSON envelope, then a few
common Qwen-Agent / fence variants so a single turn almost never dies on
format.
"""
from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field

_MAX_ACTIONS_PER_TURN = 12

_THINK_BLOCK_RE = re.compile(r'<\s*think\s*>(.*?)<\s*/\s*think\s*>', re.I | re.S)
_TOOL_CALL_RE = re.compile(r'<\s*tool_call\s*>(.*?)<\s*/\s*tool_call\s*>', re.I | re.S)
_TOOL_CALL_OPEN_RE = re.compile(r'<\s*tool_call\s*>', re.I)
_FENCE_TOOL_RE = re.compile(r'```tool[^\n]*\n(.*?)```', re.I | re.S)
_QWEN_FN_RE = re.compile(
    r'✿FUNCTION✿\s*:\s*([A-Za-z_][\w\-]*)\s*✿ARGS✿\s*:\s*(.*?)(?=✿FUNCTION✿|$)',
    re.S,
)
_INVOKE_RE = re.compile(r'<\s*invoke\s+name=["\']([^"\']+)["\']\s*>(.*?)</\s*invoke\s*>', re.I | re.S)
_PARAM_RE = re.compile(r'<\s*parameter\s+name=["\']([^"\']+)["\']\s*>(.*?)</\s*parameter\s*>', re.I | re.S)
_FUNCTION_EQ_RE = re.compile(
    r'<\s*function\s*=\s*([A-Za-z_][\w\-]*)\s*>(.*?)</\s*function\s*>',
    re.I | re.S,
)
_NAME_LINE_RE = re.compile(r'^\s*(?:name|tool)\s*[=:]\s*([A-Za-z_][\w\-]*)\s*$', re.I)

_DONE_ALIASES = frozenset({'done', 'finish', 'submit', 'complete'})
_ASK_ALIASES = frozenset({'ask_user', 'ask', 'needs_input'})
_NON_JSON_SUMMARY = 'Provider returned non-JSON output; waiting for administrator guidance.'


@dataclass
class ParsedResponse:
    thought: str
    actions: list
    final: str
    needs_input: bool
    summary: str
    protocol: str = 'none'
    parse_ok: bool = False
    control: dict = field(default_factory=dict)


def _balanced_json_candidates(text: str):
    for start, char in enumerate(text):
        if char != '{':
            continue
        depth = 0
        quoted = False
        escaped = False
        for index in range(start, len(text)):
            current = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif current == '\\':
                    escaped = True
                elif current == '"':
                    quoted = False
                continue
            if current == '"':
                quoted = True
            elif current == '{':
                depth += 1
            elif current == '}':
                depth -= 1
                if depth == 0:
                    yield text[start:index + 1]
                    break


def _decode_protocol_object(candidate: str):
    variants = [candidate, re.sub(r',\s*([}\]])', r'\1', candidate)]
    for variant in variants:
        try:
            value = json.loads(variant)
        except json.JSONDecodeError:
            try:
                value = ast.literal_eval(variant)
            except (ValueError, SyntaxError):
                continue
        if isinstance(value, dict):
            return value
    return None


def _decode_loose(text: str):
    text = (text or '').strip()
    if not text:
        return None
    obj = _decode_protocol_object(text)
    if obj is not None:
        return obj
    start, end = text.find('{'), text.rfind('}')
    if start >= 0 and end > start:
        return _decode_protocol_object(text[start:end + 1])
    return None


def _normalize_tool_name(name: str) -> str:
    cleaned = re.sub(r'[\s\-]+', '_', (name or '').strip()).strip('_').lower()
    if cleaned in _DONE_ALIASES:
        return 'done'
    if cleaned in _ASK_ALIASES:
        return 'ask_user'
    return cleaned


def _coerce_arguments(value) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = _decode_loose(value)
        if isinstance(parsed, dict):
            return parsed
        if value.strip():
            return {'value': value}
    return {}


def _action(name: str, arguments) -> dict | None:
    tool = _normalize_tool_name(name)
    if not tool or not re.match(r'^[a-z_][a-z0-9_]*$', tool):
        return None
    return {'tool': tool, 'arguments': _coerce_arguments(arguments)}


def _action_from_mapping(payload: dict) -> dict | None:
    name = payload.get('name') or payload.get('tool') or payload.get('function')
    if isinstance(name, dict):
        name = name.get('name')
    if not isinstance(name, str):
        return None
    arguments = (
        payload.get('arguments')
        if 'arguments' in payload
        else payload.get('parameters')
        if 'parameters' in payload
        else payload.get('args')
        if 'args' in payload
        else {k: v for k, v in payload.items() if k not in ('name', 'tool', 'function', 'thought')}
    )
    return _action(name, arguments)


def _parse_tool_call_body(body: str) -> dict | None:
    text = (body or '').strip()
    if not text:
        return None
    payload = _decode_loose(text)
    if isinstance(payload, dict):
        action = _action_from_mapping(payload)
        if action:
            return action
    invoke = _INVOKE_RE.search(text)
    if invoke:
        params = {m.group(1): m.group(2).strip() for m in _PARAM_RE.finditer(invoke.group(2))}
        return _action(invoke.group(1), params)
    fn_eq = _FUNCTION_EQ_RE.search(text)
    if fn_eq:
        params = {m.group(1): m.group(2).strip() for m in _PARAM_RE.finditer(fn_eq.group(2))}
        if not params:
            nested = _decode_loose(fn_eq.group(2))
            if isinstance(nested, dict):
                params = nested
        return _action(fn_eq.group(1), params)
    lines = [line for line in text.splitlines() if line.strip()]
    if lines:
        named = _NAME_LINE_RE.match(lines[0])
        if named:
            rest = '\n'.join(lines[1:]).strip()
            args = _decode_loose(rest) if rest else {}
            if args is None:
                args = {}
            return _action(named.group(1), args)
        if len(lines) >= 2 and re.match(r'^[A-Za-z_][\w\-]*$', lines[0].strip()):
            args = _decode_loose('\n'.join(lines[1:])) or {}
            return _action(lines[0].strip(), args)
    return None


def _extract_hermes_actions(text: str) -> list[dict]:
    actions = []
    for body in _TOOL_CALL_RE.findall(text):
        action = _parse_tool_call_body(body)
        if action:
            actions.append(action)
    if actions:
        return actions
    opens = list(_TOOL_CALL_OPEN_RE.finditer(text))
    if len(opens) != 1:
        return actions
    tail = text[opens[0].end():]
    if '</tool_call>' in tail.lower():
        return actions
    action = _parse_tool_call_body(tail)
    if action:
        actions.append(action)
    return actions


def _extract_qwen_fn_actions(text: str) -> list[dict]:
    actions = []
    for name, raw_args in _QWEN_FN_RE.findall(text):
        action = _action(name, raw_args)
        if action:
            actions.append(action)
    return actions


def _extract_fence_actions(text: str) -> list[dict]:
    actions = []
    for body in _FENCE_TOOL_RE.findall(text):
        parsed = _yamlish_tool(body)
        if parsed and parsed.get('arguments'):
            actions.append(parsed)
            continue
        action = _parse_tool_call_body(body)
        if action:
            actions.append(action)
            continue
        if parsed:
            actions.append(parsed)
    return actions


def _yamlish_tool(body: str) -> dict | None:
    name = ''
    args: dict = {}
    in_args = False
    current_key = ''
    block_lines: list[str] = []
    block_indent = None
    for raw in body.splitlines():
        if block_indent is not None:
            indent = len(raw) - len(raw.lstrip(' '))
            if raw.strip() and indent <= block_indent:
                args[current_key] = '\n'.join(block_lines).rstrip('\n') + '\n'
                block_indent = None
                block_lines = []
            else:
                block_lines.append(raw[block_indent:] if len(raw) >= block_indent else raw.lstrip())
                continue
        match = _NAME_LINE_RE.match(raw)
        if match and not in_args:
            name = match.group(1)
            continue
        stripped = raw.strip()
        if re.match(r'^(args|arguments)\s*:', stripped, re.I):
            in_args = True
            continue
        if not in_args or not stripped:
            continue
        kv = re.match(r'^(\s*)([^:\s][^:]*?)\s*:\s*(.*)$', raw)
        if not kv:
            continue
        key = kv.group(2).strip()
        rest = kv.group(3)
        if rest.strip() in ('|', '|2', '|-', '>'):
            current_key = key
            block_indent = len(kv.group(1))
            block_lines = []
            continue
        args[key] = rest
    if block_indent is not None and current_key:
        args[current_key] = '\n'.join(block_lines).rstrip('\n') + '\n'
    if not name:
        return None
    coerced = {}
    for key, value in args.items():
        if isinstance(value, str):
            parsed = _decode_loose(value)
            coerced[key] = parsed if parsed is not None and value.strip()[:1] in '{["tfn-0123456789' else value
        else:
            coerced[key] = value
    return _action(name, coerced)


def _extract_json_envelope(text: str):
    candidates = [text]
    candidates.extend(re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', text, flags=re.I | re.S))
    candidates.extend(_balanced_json_candidates(text))
    seen = set()
    best = None
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        payload = _decode_protocol_object(candidate)
        if payload is None:
            continue
        if any(key in payload for key in ('actions', 'thought', 'final', 'needs_input', 'summary')):
            return payload
        if best is None and ('tool' in payload or 'name' in payload):
            best = payload
    return best


def _normalize_json_actions(payload: dict) -> list[dict]:
    actions = payload.get('actions')
    if isinstance(actions, dict):
        actions = [actions]
    if not isinstance(actions, list):
        single = _action_from_mapping(payload)
        return [single] if single else []
    normalized = []
    for action in actions:
        if not isinstance(action, dict):
            continue
        item = _action_from_mapping(action)
        if item:
            normalized.append(item)
    return normalized


def split_control(actions: list[dict]) -> tuple[list[dict], dict]:
    work = []
    final = ''
    needs_input = False
    question = ''
    for action in actions or []:
        tool = (action.get('tool') or '').strip()
        arguments = action.get('arguments') or {}
        if tool == 'done':
            final = (
                str(arguments.get('summary') or arguments.get('final') or arguments.get('message') or '')
            ).strip()
            continue
        if tool == 'ask_user':
            needs_input = True
            question = str(arguments.get('question') or arguments.get('message') or '').strip()
            continue
        work.append(action)
    return work, {'final': final, 'needs_input': needs_input, 'question': question}


def parse_model_response(raw: str, extra_thought: str = '') -> ParsedResponse:
    text = (raw or '').strip()
    think_bits = [bit.strip() for bit in _THINK_BLOCK_RE.findall(text) if bit and bit.strip()]
    if think_bits:
        text = _THINK_BLOCK_RE.sub('\n', text).strip()
    upstream = ' · '.join(bit for bit in [extra_thought.strip() if extra_thought else ''] if bit)
    prefix = '\n\n'.join(part for part in [upstream, '\n\n'.join(think_bits)] if part).strip()

    def _thought(value: str, limit: int) -> str:
        combined = '\n\n'.join(part for part in [prefix, (value or '').strip()] if part).strip()
        return combined[:limit]

    hermes = _extract_hermes_actions(text)
    qwen_fn = _extract_qwen_fn_actions(text) if not hermes else []
    fences = _extract_fence_actions(text) if not hermes and not qwen_fn else []
    payload = _extract_json_envelope(text)
    json_actions = _normalize_json_actions(payload) if isinstance(payload, dict) else []

    protocol = 'none'
    actions: list[dict] = []
    if hermes:
        protocol = 'hermes'
        actions = hermes
    elif qwen_fn:
        protocol = 'qwen_fn'
        actions = qwen_fn
    elif fences:
        protocol = 'fence'
        actions = fences
    elif json_actions:
        protocol = 'json'
        actions = json_actions
    elif isinstance(payload, dict) and any(key in payload for key in ('thought', 'final', 'needs_input', 'summary')):
        protocol = 'json'

    thought = ''
    final = ''
    needs_input = False
    summary = ''
    if isinstance(payload, dict) and protocol in ('json', 'hermes', 'qwen_fn', 'fence'):
        thought = str(payload.get('thought') or '')
        final = str(payload.get('final') or '')
        needs_input = bool(payload.get('needs_input', False))
        summary = str(payload.get('summary') or '')

    work, control = split_control(actions)
    if control['final'] and not final:
        final = control['final']
    if control['needs_input']:
        needs_input = True
        if control['question'] and not thought:
            thought = control['question']

    parse_ok = protocol != 'none' or bool(work) or bool(final)
    if not parse_ok:
        return ParsedResponse(
            thought=_thought(text, 12000),
            actions=[],
            final='',
            needs_input=True,
            summary=_NON_JSON_SUMMARY,
            protocol='none',
            parse_ok=False,
            control=control,
        )
    if not thought and protocol != 'json':
        cleaned = _TOOL_CALL_RE.sub('\n', text)
        cleaned = _FENCE_TOOL_RE.sub('\n', cleaned)
        cleaned = _QWEN_FN_RE.sub('\n', cleaned)
        thought = cleaned.strip()
    return ParsedResponse(
        thought=_thought(thought, 20000),
        actions=work[:_MAX_ACTIONS_PER_TURN],
        final=final[:30000],
        needs_input=needs_input,
        summary=(summary or control.get('final') or '')[:12000],
        protocol=protocol,
        parse_ok=True,
        control=control,
    )


MAX_ACTIONS_PER_TURN = _MAX_ACTIONS_PER_TURN
NON_JSON_SUMMARY = _NON_JSON_SUMMARY
