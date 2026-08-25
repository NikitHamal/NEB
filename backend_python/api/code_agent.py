from __future__ import annotations

import json
import logging
import re

from django.conf import settings

from api import code_realtime as rt
from api.code_agent_prompt import history_prompt, system_prompt
from api.code_agent_providers import CodeProviderAdapter, CodeProviderError
from api.code_agent_tools import result_preview, run_tool, sanitize_args, tool_label
from api.models import CodeMessage, CodeSession

logger = logging.getLogger(__name__)

FINISH_RE = re.compile(r'FINISH:\s*(.+?)\s*$', re.DOTALL | re.IGNORECASE)
THINK_RE = re.compile(r'<think>.*?</think>', re.DOTALL | re.IGNORECASE)
_TOOL_CALL_RE = re.compile(r'<\s*tool_call\s*>(.*?)<\s*/\s*tool_call\s*>', re.I | re.S)
_INVOKE_RE = re.compile(r'<\s*invoke\s+name=["\']([^"\']+)["\']\s*>(.*?)</\s*invoke\s*>', re.I | re.S)
_PARAM_RE = re.compile(r'<\s*parameter\s+name=["\']([^"\']+)["\']\s*>(.*?)</\s*parameter\s*>', re.I | re.S)
_JSON_FENCE_RE = re.compile(r'```(?:json|tool)?\s*\n([\s\S]*?)```', re.IGNORECASE)
_QWEN_FN_RE = re.compile(r'✿FUNCTION✿\s*:\s*([A-Za-z_][\w\-]*)\s*✿ARGS✿\s*:\s*(.*?)(?=✿FUNCTION✿|$)', re.S)

REFUSAL_PATTERNS = [
    r"no\s+filesystem",
    r"can(?:'t|not)\s+(?:directly\s+)?(?:browse|inspect|access|read|view)\s+(?:your|the)?\s*(?:local|repo|workspace|files|code)",
    r"looking\s+at\s+my\s+available\s+tools",
    r"reality\s+check\s+on\s+my\s+access",
    r"don(?:'t|not)\s+(?:actually\s+)?see\s+the\s+local",
    r"paste\s+(?:the|your)\s+code",
    r"share\s+(?:the|your)\s+snippets",
    r"i(?:'ve| have)\s+got\s*:\s*web_search",
    r"only\s+have\s+access\s+to\s+web",
    r"no\s+worries\s+though\s*[—–-]\s*here\s+are\s+your\s+options",
]
REFUSAL_RE = re.compile('|'.join(REFUSAL_PATTERNS), re.IGNORECASE)


class CancelledError(Exception):
    pass


def _load_json_loose(raw: str):
    raw = (raw or '').strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        pass
    try:
        return json.loads(re.sub(r',\s*([\]}])', r'\1', raw))
    except Exception:
        pass
    start = raw.find('{')
    end = raw.rfind('}')
    if start >= 0 and end > start:
        try:
            return json.loads(raw[start:end + 1])
        except Exception:
            pass
    start = raw.find('[')
    end = raw.rfind(']')
    if start >= 0 and end > start:
        try:
            return json.loads(raw[start:end + 1])
        except Exception:
            pass
    return None


def parse_tool_calls(text: str) -> list[tuple[str, dict]]:
    from api.code_agent_tools import normalize_tool_and_args
    calls = []
    text = str(text or '')

    # 1. Hermes / Nous XML: <tool_call>{"name": ..., "arguments": ...}</tool_call>
    for match in _TOOL_CALL_RE.finditer(text):
        raw = match.group(1).strip()
        data = _load_json_loose(raw)
        if isinstance(data, dict):
            name = data.get('name') or data.get('tool') or data.get('action') or data.get('function')
            args = data.get('arguments') or data.get('args') or data.get('parameters') or data.get('input') or {}
            if isinstance(args, str):
                args = _load_json_loose(args) or {}
            if name:
                calls.append(normalize_tool_and_args(str(name), args if isinstance(args, dict) else {}))
    if calls:
        return calls

    # 2. Markdown fences: ```json ... ``` or ```tool ... ```
    for match in _JSON_FENCE_RE.finditer(text):
        raw = match.group(1).strip()
        data = _load_json_loose(raw)
        if isinstance(data, dict):
            data = [data]
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                name = item.get('tool') or item.get('name') or item.get('action') or item.get('function')
                args = item.get('args') or item.get('arguments') or item.get('parameters') or item.get('input') or {}
                if isinstance(args, str):
                    args = _load_json_loose(args) or {}
                if name:
                    calls.append(normalize_tool_and_args(str(name), args if isinstance(args, dict) else {}))
    if calls:
        return calls

    # 3. Claude/Anthropic XML: <invoke name="...">...</invoke>
    for match in _INVOKE_RE.finditer(text):
        name = match.group(1).strip()
        body = match.group(2)
        params = {m.group(1): m.group(2).strip() for m in _PARAM_RE.finditer(body)}
        if not params:
            loose = _load_json_loose(body)
            if isinstance(loose, dict):
                params = loose
        calls.append(normalize_tool_and_args(name, params))
    if calls:
        return calls

    # 4. Qwen function calls: ✿FUNCTION✿: name ✿ARGS✿: {...}
    for match in _QWEN_FN_RE.finditer(text):
        name = match.group(1).strip()
        raw_args = match.group(2).strip()
        args = _load_json_loose(raw_args) or {}
        calls.append(normalize_tool_and_args(name, args if isinstance(args, dict) else {}))
    if calls:
        return calls

    # 5. Standalone loose JSON anywhere in text
    loose = _load_json_loose(text)
    if isinstance(loose, dict) and any(k in loose for k in ('tool', 'name', 'action', 'function')):
        name = loose.get('tool') or loose.get('name') or loose.get('action') or loose.get('function')
        args = loose.get('args') or loose.get('arguments') or loose.get('parameters') or loose.get('input') or {}
        if name:
            calls.append(normalize_tool_and_args(str(name), args if isinstance(args, dict) else {}))

    return calls


def strip_tool_fences(text: str) -> str:
    text = str(text or '')
    text = _TOOL_CALL_RE.sub('', text)
    text = _JSON_FENCE_RE.sub('', text)
    text = _INVOKE_RE.sub('', text)
    text = _QWEN_FN_RE.sub('', text)
    return text.strip()


class CodeAgent:
    def __init__(self, session_id: str):
        self.session = CodeSession.objects.get(pk=session_id)
        self.user_id = str(self.session.user_id)
        self.mode = (getattr(self.session, 'mode', '') or 'agent').strip().lower()
        if self.mode not in ('agent', 'ask', 'plan'):
            self.mode = 'agent'
        self.provider = CodeProviderAdapter(
            self.session,
            on_retry=self._provider_retry,
            cancelled=self.cancelled,
        )
        self.tool_count = 0
        self.iteration = 0
        self.last_provider = ''
        self.last_context_pct = 0
        self.last_action_signature = ''
        self.action_repeat_count = 0

    def push(self, event: str, data: dict):
        rt.push_ui(self.session.id, event, data)

    def push_delta(self, text: str):
        if text:
            self.push('delta', {'kind': 'text', 'text': text})

    def cancelled(self) -> bool:
        if not self.session.pk:
            return True
        return bool(CodeSession.objects.only('cancel_flag').get(pk=self.session.id).cancel_flag)

    def save_msg(self, role: str, content: str = '', meta=None) -> int:
        now = rt.now_ms()
        msg = CodeMessage.objects.create(
            session=self.session,
            role=role,
            content=content,
            meta=meta or None,
            created_at=now,
        )
        CodeSession.objects.filter(pk=self.session.id).update(updated_at=now)
        return msg.pk

    def persist_event(self, etype: str, **meta):
        meta['type'] = etype
        return self.save_msg('event', '', meta)

    def _provider_retry(self, slug: str, error: str):
        self.push('status', {'phase': 'retrying', 'provider': slug, 'detail': error})

    def _history(self):
        row_cap = max(100, min(int(getattr(settings, 'CODE_AGENT_HISTORY_ROWS', 1200)), 5000))
        return list(
            CodeMessage.objects.filter(session=self.session)
            .order_by('-created_at', '-id')
            .values('role', 'content', 'meta', 'created_at')[:row_cap]
        )[::-1]

    def _build_prompt(self) -> tuple[str, int, int]:
        context_window = max(16000, self.provider.estimated_context_window())
        reserved_tokens = max(4000, min(24000, int(context_window * 0.15)))
        input_tokens = max(8000, context_window - reserved_tokens)
        char_budget = min(700000, max(32000, input_tokens * 3))
        prompt, used_chars = history_prompt(self._history(), char_budget)
        approx_tokens = max(1, used_chars // 4)
        pct = max(0, min(99, round((approx_tokens / context_window) * 100)))
        self.last_context_pct = pct
        self.push('context', {
            'percent': pct,
            'approx_tokens': approx_tokens,
            'context_window': context_window,
        })
        return prompt, approx_tokens, context_window

    def _execute_calls(self, calls: list[tuple[str, dict]]):
        signature = json.dumps([(tool, sanitize_args(args)) for tool, args in calls], sort_keys=True, ensure_ascii=False)
        if signature == self.last_action_signature:
            self.action_repeat_count += 1
        else:
            self.last_action_signature = signature
            self.action_repeat_count = 0
        if self.action_repeat_count >= 2:
            self.persist_event('loop_guard', message='Repeated identical tool batch; model must change approach')
            self.save_msg('event', '', {
                'type': 'tool_result',
                'call_id': 'loop-guard',
                'summary': 'The identical tool batch has repeated. Do not repeat it again; inspect the failure and change approach.',
                'preview': '',
            })
            self.push('status', {'phase': 'thinking', 'detail': 'Changing approach after repeated tool batch'})
            return

        for index, (tool, args) in enumerate(calls):
            if self.cancelled():
                raise CancelledError()
            self.tool_count += 1
            call_id = f'i{self.iteration}t{self.tool_count}-{index}'
            label = tool_label(tool, args)
            clean_args = sanitize_args(args)
            self.push('tool_call', {
                'call_id': call_id,
                'tool': tool,
                'args': clean_args,
                'label': label,
                'tool_count': self.tool_count,
            })
            event_meta = {'call_id': call_id, 'tool': tool, 'args': clean_args, 'label': label}
            if tool in ('write_file', 'append_file'):
                event_meta['lines'] = str(args.get('content') or '').count('\n') + 1
            self.persist_event('tool_call', **event_meta)

            outcome = run_tool(self.user_id, self.session.id, tool, args, self.mode)
            if self.cancelled():
                raise CancelledError()
            raw = outcome.get('raw') or {}
            ok = bool(raw.get('ok'))
            preview = result_preview(raw)
            result_data = {
                'call_id': call_id,
                'tool': tool,
                'ok': ok,
                'summary': outcome.get('summary') or '',
                'error': raw.get('error') or '',
                'duration_ms': outcome.get('duration_ms') or 0,
            }
            self.push('tool_result', result_data)
            self.persist_event('tool_result', preview=preview, **result_data)

            if tool == 'update_plan' and ok:
                data = raw.get('data') or {}
                plan_meta = {
                    'todos': data.get('todos') or [],
                    'explanation': data.get('explanation') or '',
                }
                self.persist_event('plan', **plan_meta)
                self.push('plan', plan_meta)

    def run(self, user_message_id=None):
        self._start_session()
        final_text = ''
        error_text = ''
        try:
            while True:
                if self.cancelled():
                    raise CancelledError()
                self.iteration += 1
                max_steps = int(getattr(settings, 'CODE_AGENT_MAX_STEPS', 0) or 0)
                if max_steps > 0 and self.iteration > max_steps:
                    raise RuntimeError('Configured CODE_AGENT_MAX_STEPS was reached')

                prompt, approx_tokens, context_window = self._build_prompt()
                if self.iteration > 1:
                    prompt += '\n\nContinue from the latest tool results. Do not repeat successful work. Use tools if needed or finish with FINISH:.'
                self.push('status', {
                    'phase': 'thinking',
                    'iteration': self.iteration,
                    'tool_count': self.tool_count,
                    'provider': self.last_provider,
                })
                result = self.provider.call(system_prompt(rt.get_presence(self.user_id), self.mode), prompt)
                self.last_provider = f'{result.provider} · {result.model}'
                self.push('model', {
                    'provider': result.provider,
                    'model': result.model,
                    'elapsed_ms': result.elapsed_ms,
                    'context_window': result.context_window,
                })
                clean = THINK_RE.sub('', result.text or '').strip()
                calls = parse_tool_calls(clean)
                finish = FINISH_RE.search(clean)
                prose = strip_tool_fences(clean)
                if finish:
                    prose = FINISH_RE.sub('', prose).strip()

                if calls:
                    if prose:
                        self.save_msg('assistant', prose)
                        self.push_delta(prose + '\n\n')
                    self._execute_calls(calls)
                    continue

                if REFUSAL_RE.search(clean):
                    logger.info('CodeAgent intercepted model refusal; executing workspace inspection bootstrap')
                    self.push_delta('*Inspecting local workspace structure...*\n\n')
                    self._execute_calls([('list_dir', {'path': '.'}), ('git_status', {})])
                    continue

                final_text = prose
                if finish:
                    final_text = final_text or finish.group(1).strip()
                    break
                if self.mode in ('ask', 'plan'):
                    break
                if final_text:
                    break
                self.save_msg('event', '', {
                    'type': 'tool_result', 'call_id': 'format-repair',
                    'summary': 'No tool calls or final answer were produced. Continue with valid tool JSON or FINISH:.',
                    'preview': '',
                })
        except CancelledError:
            error_text = 'Cancelled'
        except CodeProviderError as exc:
            logger.warning('CodeAgent provider error: %s', exc)
            error_text = str(exc)[:4000]
        except Exception as exc:
            logger.exception('CodeAgent unexpected error: %s', exc)
            error_text = str(exc)[:4000]
        self._finish_session(final_text, error_text, user_message_id)

    def _start_session(self):
        self.session.status = 'running'
        self.session.error = ''
        self.session.cancel_flag = False
        self.session.save(update_fields=['status', 'error', 'cancel_flag', 'updated_at'])
        self.push('status', {'phase': 'starting', 'iteration': 0, 'tool_count': 0})

    def _finish_session(self, final_text: str, error_text: str, user_message_id):
        if final_text:
            self.save_msg('assistant', final_text, {'final': True})
            self.push_delta(final_text)
        status = 'idle'
        if error_text and error_text != 'Cancelled':
            status = 'error'
            self.save_msg('event', error_text, {'type': 'error'})
        self.session.status = status
        self.session.error = error_text
        self.session.save(update_fields=['status', 'error', 'updated_at'])
        self.push('done', {
            'status': status,
            'message_id': user_message_id,
            'error': error_text,
            'finish': final_text[-500:] if final_text else '',
            'iterations': self.iteration,
            'tool_count': self.tool_count,
            'context_percent': self.last_context_pct,
            'provider': self.last_provider,
        })


def run_session(session_id: str):
    CodeAgent(session_id).run()
