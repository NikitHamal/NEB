"""Runtime — the agent loop.

Architecture:
  · `AgentRuntime` is initialised with a CodingAgentSession.
  · `step()` advances the session by exactly one LLM round-trip plus optional
    tool calls. It is idempotent and short-lived; the worker daemon calls it
    in a poll loop.
  · The runtime never holds open file handles or DB transactions across
    LLM calls. That is intentional — the worker is allowed to be killed
    between steps and resume from the database state.

Stop / pause / interrupt semantics:
  · `pause` is recorded by setting status='paused' on the session. The worker
    reads status before every step and refuses to advance when paused.
  · `stop`  sets status='stopped'. The runtime stops after the current
    tool call is persisted (or before it starts).
  · `interrupt` (a user follow-up message) is just a new CodingAgentMessage
    with role='user'. The runtime injects it into the LLM's input next step.

Per-iteration lifecycle:
  1. Build the model input from the session message history (system + user +
     assistant + tool messages). The system prompt is the bootstrap; the
     rest comes directly from CodingAgentMessage rows so the model sees the
     full conversation history including tool calls/results.
  2. Call `provider_adapter.call_for_agent`. May raise ProviderError.
  3. Persist the assistant message and parse tool calls out of the response.
  4. If no tool calls: write a wrapping event and let the loop exit (worker
     decides what to do — typically mark the session 'awaiting_input').
  5. Otherwise: execute each tool call, persist the result, advance iteration.
"""
from __future__ import annotations

import logging
import threading
import time
import traceback
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from django.utils.text import get_valid_filename

from .constants import (
    AGENT_DEFAULT_SYSTEM_PROMPT,
    MAX_TOOL_RESULT_CHARS,
    USER_TOOL_GUIDANCE_PROMPT,
    merge_system_prompts,
)
from .git_workspace import ensure_clone, create_session_branch, project_repo_dir
from .models import (
    CodingAgentEvent,
    CodingAgentFileChange,
    CodingAgentMessage,
    CodingAgentProject,
    CodingAgentSession,
    CodingAgentToolCall,
)
from .provider_adapter import ProviderCompletion, ProviderError, call_for_agent
from .tools import ToolContext, ToolResult, persist_tool_call, registry
from . import tool_parser

logger = logging.getLogger(__name__)


@dataclass
class StepResult:
    finished: bool
    status: str
    message: str = ''


class AgentRuntime:
    """Stateless around a session — every step reads/writes the DB."""

    def __init__(
        self,
        session: CodingAgentSession,
        *,
        cancelled: Optional[Callable[[], bool]] = None,
        on_event: Optional[Callable[[CodingAgentEvent], None]] = None,
    ):
        self.session = session
        self.cancelled = cancelled or (lambda: False)
        self.on_event = on_event or (lambda e: None)
        self._stop_flag = threading.Event()

    def stop(self) -> None:
        self._stop_flag.set()

    def _check_stop(self) -> None:
        self.session.refresh_from_db(fields=['status', 'updated_at'])
        if self.session.status in {CodingAgentSession.STATUS_STOPPED, CodingAgentSession.STATUS_PAUSED}:
            raise _AgentStopped('session is ' + self.session.status)
        if self.cancelled():
            raise _AgentStopped('runtime cancelled')

    def ensure_workspace(self) -> Path:
        project = self.session.project
        repo_path = Path(self.session.workspace_path) if self.session.workspace_path else project_repo_dir(project)
        project.last_used_at = int(time.time() * 1000)
        project.save(update_fields=['last_used_at'])
        if not self.session.workspace_path:
            ensure_clone(project)
            self.session.workspace_path = str(repo_path)
            self.session.save(update_fields=['workspace_path', 'updated_at'])
        return repo_path

    def bootstrap(self) -> StepResult:
        """One-time setup: clone, branch, write system message, enqueue the task."""
        session = self.session
        session.refresh_from_db()
        if session.status in {CodingAgentSession.STATUS_FINISHED, CodingAgentSession.STATUS_FAILED, CodingAgentSession.STATUS_STOPPED, CodingAgentSession.STATUS_PR_OPENED}:
            return StepResult(finished=True, status=session.status, message='already terminal')

        project = session.project
        session.status = CodingAgentSession.STATUS_SETUP
        session.started_at = session.started_at or int(time.time() * 1000)
        session.last_activity_at = int(time.time() * 1000)
        session.save(update_fields=['status', 'started_at', 'last_activity_at', 'updated_at'])
        self.emit(CodingAgentEvent.EVENT_STATUS, 'Setup: cloning repo and preparing branch', '')

        try:
            ensure_clone(project)
            if not session.branch:
                session.branch = 'agent/' + (get_valid_filename(session.title or session.task[:30]) or 'task').replace('_', '-').lower()[:80].strip('-') + '-' + uuid.uuid4().hex[:6]
            create_session_branch(project, session, session.branch)
        except Exception as e:  # noqa: BLE001
            logger.exception('session setup failed: %s', e)
            session.status = CodingAgentSession.STATUS_FAILED
            session.error_message = ('Setup failed: ' + str(e))[:4000]
            session.finished_at = int(time.time() * 1000)
            session.save(update_fields=['status', 'error_message', 'finished_at', 'updated_at'])
            self.emit(CodingAgentEvent.EVENT_STATUS, 'Setup failed', str(e))
            return StepResult(finished=True, status=session.status, message=str(e))

        system_prompt = merge_system_prompts(AGENT_DEFAULT_SYSTEM_PROMPT, project.system_prompt)
        
        # Inject project and user long-term memory / knowledge base context
        try:
            from django.db.models import Q
            from .models import CodingAgentKnowledgeItem
            kb_items = CodingAgentKnowledgeItem.objects.filter(
                Q(owner_user=project.owner_user) &
                (Q(project=project) | Q(repository=project.repo_full_name) | Q(repository=''))
            ).order_by('-updated_at')[:10]
            if kb_items:
                kb_lines = ['\n\n## Project & User Knowledge Base (Long-Term Memory)']
                for kb in kb_items:
                    kb_lines.append(f'### [{kb.type}] {kb.title}\n{kb.content}\n')
                system_prompt += '\n'.join(kb_lines)
        except Exception as kb_err:
            logger.warning('Failed to query knowledge base for session %s: %s', session.id, kb_err)

        CodingAgentMessage.objects.get_or_create(
            session=session,
            role=CodingAgentMessage.ROLE_SYSTEM,
            kind=CodingAgentMessage.KIND_MESSAGE,
            content=system_prompt,
            defaults={'id': uuid.uuid4().hex, 'created_at': int(time.time() * 1000)},
        )

        CodingAgentMessage.objects.get_or_create(
            session=session,
            role=CodingAgentMessage.ROLE_USER,
            kind=CodingAgentMessage.KIND_MESSAGE,
            content=session.task.strip(),
            defaults={'id': uuid.uuid4().hex, 'created_at': int(time.time() * 1000) + 1},
        )

        if not session.provider:
            session.provider = project.agent_provider or _pick_default_provider()
        if not session.model:
            session.model = project.agent_model or ''
        if not session.model:
            from .constants import PROVIDER_DEFAULT_MODEL
            session.model = PROVIDER_DEFAULT_MODEL.get(session.provider, '')
        session.status = CodingAgentSession.STATUS_RUNNING
        session.save(update_fields=['provider', 'model', 'status', 'updated_at'])
        self.emit(CodingAgentEvent.EVENT_STATUS, 'Session is now running', 'provider=%s model=%s' % (session.provider, session.model))
        return StepResult(finished=False, status=session.status, message='setup complete')

    def step(self) -> StepResult:
        self._check_stop()
        session = self.session
        session.refresh_from_db()
        if session.status in {CodingAgentSession.STATUS_FINISHED, CodingAgentSession.STATUS_FAILED, CodingAgentSession.STATUS_STOPPED, CodingAgentSession.STATUS_PR_OPENED}:
            return StepResult(finished=True, status=session.status)
        if session.status != CodingAgentSession.STATUS_RUNNING:
            session.status = CodingAgentSession.STATUS_RUNNING
            session.save(update_fields=['status', 'updated_at'])

        if session.iterations >= (session.project.max_iterations or 80):
            session.status = CodingAgentSession.STATUS_AWAITING_INPUT
            session.error_message = ('Hit max_iterations cap (%d). Awaiting human follow-up.' % session.iterations)[:4000]
            session.save(update_fields=['status', 'error_message', 'updated_at'])
            return StepResult(finished=True, status=session.status, message='iteration cap reached')

        messages = _build_messages_for_provider(session)
        try:
            completion = call_for_agent(
                provider=session.provider,
                model=session.model,
                messages=messages,
                api_url=getattr(session.project, 'agent_api_url', '') or '',
                api_key=getattr(session.project, 'agent_api_key', '') or '',
            )
        except ProviderError as e:
            logger.warning('provider error: %s', e)
            session.iterations += 1
            session.error_message = ('Provider error (will retry next worker cycle): ' + str(e))[:4000]
            session.save(update_fields=['iterations', 'error_message', 'updated_at'])
            self.emit(CodingAgentEvent.EVENT_LOG, 'Provider error', str(e))
            return StepResult(finished=False, status=session.status, message='provider error')

        assistant_text, calls = tool_parser.parse(completion.text)
        session.iterations += 1
        session.input_tokens_estimate += completion.input_tokens or 0
        session.output_tokens_estimate += completion.output_tokens or 0
        session.last_activity_at = int(time.time() * 1000)

        seq = _next_sequence(session)
        assistant_msg = CodingAgentMessage.objects.create(
            id=uuid.uuid4().hex,
            session=session,
            role=CodingAgentMessage.ROLE_ASSISTANT,
            kind=CodingAgentMessage.KIND_MESSAGE,
            content=assistant_text.strip(),
            iteration=session.iterations,
            sequence=seq,
        )
        session.last_message_id = assistant_msg.id

        if calls:
            for call in calls:
                _emit_assistant_tool_call(call, session, assistant_msg.id, session.iterations)

        if not calls:
            session.tool_calls_count = session.tool_calls_count
            session._meta_has_assistant_text_without_tools = True
            session.save(update_fields=[
                'iterations', 'input_tokens_estimate', 'output_tokens_estimate',
                'last_activity_at', 'last_message_id', 'updated_at',
            ])
            self.emit(CodingAgentEvent.EVENT_LOG, 'Assistant turn (no tools)', (assistant_text or '')[:300])
            return StepResult(finished=False, status=session.status, message='no tool calls')

        return self._execute_calls(calls, session, assistant_msg.id, session.iterations)

    def _execute_calls(self, calls, session: CodingAgentSession, parent_message_id: str, iteration: int) -> StepResult:
        workspace = Path(session.workspace_path)
        ctx = ToolContext(
            session=session,
            workspace=workspace,
            iteration=iteration,
            cancelled=lambda: self._stop_flag.is_set(),
        )
        finished = False
        status_final = session.status
        for call in calls:
            try:
                self._check_stop()
            except _AgentStopped as e:
                self.emit(CodingAgentEvent.EVENT_INTERRUPT, 'Interrupted before tool execution', str(e))
                break

            t0 = time.time()
            result = registry.execute(call.name, call.args, ctx)
            duration = int((time.time() - t0) * 1000)
            tc = persist_tool_call(session.id, call.name, call.args, result, iteration)
            tc.duration_ms = duration
            tc.message_id = parent_message_id
            tc.save(update_fields=['duration_ms', 'message_id'])

            _persist_tool_result_message(session, call, result, parent_message_id, iteration)

            if call.name == 'done':
                finished = True
                session.status = CodingAgentSession.STATUS_FINISHED
                session.finished_at = int(time.time() * 1000)
                session.summary = result.data.get('summary', '') if isinstance(result.data, dict) else (call.args.get('summary') or '')
                session.save(update_fields=['status', 'finished_at', 'summary', 'updated_at'])
                self.emit(CodingAgentEvent.EVENT_STATUS, 'Agent finished', session.summary)
                status_final = session.status
                break

            if result.status == 'denied':
                self.emit(CodingAgentEvent.EVENT_INTERRUPT, 'Tool denied: ' + call.name, result.text[:300])
            else:
                self.emit(CodingAgentEvent.EVENT_TOOL, 'Tool %s — %s' % (call.name, result.status), result.text[:300])

            session.refresh_from_db()
            if session.status in {CodingAgentSession.STATUS_STOPPED, CodingAgentSession.STATUS_PAUSED, CodingAgentSession.STATUS_AWAITING_INPUT}:
                status_final = session.status
                break

        if not finished and session.status == CodingAgentSession.STATUS_RUNNING:
            session.save(update_fields=['updated_at'])

        return StepResult(finished=finished, status=status_final)

    def emit(self, event_type: str, summary: str, detail: str = '', payload: Optional[Dict[str, Any]] = None):
        ev = CodingAgentEvent.objects.create(
            id=uuid.uuid4().hex,
            session=self.session,
            event_type=event_type,
            summary=summary[:240],
            detail=detail[:6000],
            payload_json=_safe_json(payload),
        )
        try:
            self.on_event(ev)
        except Exception:  # noqa: BLE001
            logger.exception('on_event callback failed')
        return ev


class _AgentStopped(Exception):
    pass


def _safe_json(payload: Optional[Dict[str, Any]]) -> str:
    if not payload:
        return ''
    try:
        import json
        return json.dumps(payload, ensure_ascii=False, default=str)[:6000]
    except Exception:  # noqa: BLE001
        return ''


def _emit_assistant_tool_call(call, session: CodingAgentSession, parent_message_id: str, iteration: int) -> CodingAgentMessage:
    import json
    return CodingAgentMessage.objects.create(
        id=uuid.uuid4().hex,
        session=session,
        role=CodingAgentMessage.ROLE_ASSISTANT,
        kind=CodingAgentMessage.KIND_TOOL_CALL,
        content='',
        tool_name=call.name,
        tool_args_json=json.dumps(call.args, ensure_ascii=False, default=str)[:20000],
        tool_status='pending',
        iteration=iteration,
        sequence=_next_sequence(session),
    )


def _persist_tool_result_message(session: CodingAgentSession, call, result, parent_message_id: str, iteration: int) -> CodingAgentMessage:
    return CodingAgentMessage.objects.create(
        id=uuid.uuid4().hex,
        session=session,
        role=CodingAgentMessage.ROLE_TOOL,
        kind=CodingAgentMessage.KIND_TOOL_RESULT,
        content=result.text if result.text else '',
        tool_name=call.name,
        tool_result_json=result.to_json(),
        tool_status=result.status,
        iteration=iteration,
        sequence=_next_sequence(session),
    )


def _next_sequence(session: CodingAgentSession) -> int:
    last = CodingAgentMessage.objects.filter(session=session).order_by('-sequence').values_list('sequence', flat=True).first()
    return int(last or 0) + 1


def _build_messages_for_provider(session: CodingAgentSession) -> List[Dict[str, str]]:
    messages_qs = list(
        CodingAgentMessage.objects.filter(session=session, is_visible=True)
        .order_by('sequence', 'created_at')
        .values('role', 'kind', 'content', 'tool_name', 'tool_args_json', 'tool_result_json', 'tool_status', 'attachments_json')
    )
    out: List[Dict[str, str]] = []
    pending_tool: Optional[str] = None
    for m in messages_qs:
        role = m['role']
        kind = m['kind']
        if role == CodingAgentMessage.ROLE_SYSTEM and kind == CodingAgentMessage.KIND_MESSAGE:
            out.append({'role': 'system', 'content': m['content']})
            continue
        if role == CodingAgentMessage.ROLE_USER and kind == CodingAgentMessage.KIND_MESSAGE:
            msg_item = {'role': 'user', 'content': m['content']}
            att_raw = m.get('attachments_json') or ''
            if att_raw:
                try:
                    import json
                    atts = json.loads(att_raw)
                    if isinstance(atts, list) and atts:
                        msg_item['attachments'] = atts
                except Exception:
                    pass
            out.append(msg_item)
            continue
        if role == CodingAgentMessage.ROLE_ASSISTANT and kind == CodingAgentMessage.KIND_MESSAGE:
            txt = m['content']
            if not txt.strip():
                continue
            out.append({'role': 'assistant', 'content': txt})
            continue
        if role == CodingAgentMessage.ROLE_ASSISTANT and kind == CodingAgentMessage.KIND_TOOL_CALL:
            out.append({'role': 'assistant', 'content': _format_tool_call_for_model(m)})
            continue
        if role == CodingAgentMessage.ROLE_TOOL and kind == CodingAgentMessage.KIND_TOOL_RESULT:
            out.append({'role': 'user', 'content': _format_tool_result_for_model(m)})
            continue
    return _truncate_messages_for_provider(out, char_budget=120_000)


def _format_tool_call_for_model(m: Dict[str, Any]) -> str:
    args = m.get('tool_args_json') or ''
    if args:
        try:
            import json
            args_obj = json.loads(args)
        except Exception:
            args_obj = {'_raw': args}
    else:
        args_obj = {}
    args_yaml = _yamlify_args(args_obj)
    return '```tool\nname: ' + m['tool_name'] + '\nargs:\n' + args_yaml + '\n```'


def _yamlify_args(obj: Any, indent: int = 2) -> str:
    if isinstance(obj, dict):
        if not obj:
            return ''
        lines = []
        pad = ' ' * indent
        for k, v in obj.items():
            if isinstance(v, str):
                if '\n' in v:
                    lines.append(pad + str(k) + ': |2')
                    for ln in v.splitlines():
                        lines.append(pad + '  ' + ln)
                    lines.append('')
                else:
                    esc = v.replace('\\', '\\\\').replace('"', '\\"')
                    lines.append(pad + str(k) + ': "' + esc + '"')
            elif isinstance(v, (int, float, bool)) or v is None:
                lines.append(pad + str(k) + ': ' + _scalar_yaml(v))
            elif isinstance(v, (list, dict)):
                import json
                lines.append(pad + str(k) + ': ' + json.dumps(v, ensure_ascii=False))
            else:
                lines.append(pad + str(k) + ': "' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"')
        return '\n'.join(lines)
    return _scalar_yaml(obj) if obj is not None else ''


def _scalar_yaml(v: Any) -> str:
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    return str(v)


def _format_tool_result_for_model(m: Dict[str, Any]) -> str:
    import json
    status = m.get('tool_status') or 'ok'
    raw = m.get('tool_result_json') or ''
    if raw:
        try:
            obj = json.loads(raw)
            text = obj.get('text') if isinstance(obj, dict) else ''
            data = obj.get('data') if isinstance(obj, dict) else None
        except Exception:
            text = raw
            data = None
    else:
        text = m.get('content') or ''
        data = None
    header = 'Tool `%s` returned status="%s":\n' % (m.get('tool_name', '?'), status)
    if data:
        try:
            data_str = json.dumps(data, ensure_ascii=False, default=str)
        except Exception:
            data_str = str(data)
    else:
        data_str = ''
    if text and data_str:
        return header + '\n' + text + '\n\n(Structured data): ' + data_str + '\n'
    if text:
        return header + '\n' + text + '\n'
    return header + '(no output)\n'


def _truncate_messages_for_provider(messages: List[Dict[str, str]], char_budget: int = 120_000) -> List[Dict[str, str]]:
    if not messages:
        return messages
    total = sum(len(m.get('content') or '') for m in messages)
    if total <= char_budget:
        return messages
    budget = char_budget
    sys = next((m for m in messages if m['role'] == 'system'), None)
    other = [m for m in messages if m is not sys]
    out: List[Dict[str, str]] = []
    if sys:
        out.append(sys)
        budget -= len(sys['content'])
    used = 0
    head = []
    tail: List[Dict[str, str]] = []
    for m in other:
        c = len(m['content'])
        if used + c <= budget // 2 and len(head) < 6:
            head.append(m)
            used += c
        else:
            tail.append(m)
    summary = '[... elided middle turns to fit context budget ...]'
    out.extend(head)
    out.append({'role': 'system', 'content': summary})
    out.extend(tail[-30:])
    return out


def _pick_default_provider() -> str:
    try:
        from api.models import BotConfig
        cfg = BotConfig.objects.filter(enabled=True).first()
        if cfg:
            return cfg.provider or 'qwen'
    except Exception:  # noqa: BLE001
        pass
    return 'qwen'


def derive_session_title(task: str) -> str:
    task = task.strip()
    return task[:60] + ('...' if len(task) > 60 else '')
