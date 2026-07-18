"""Iterative coding-agent harness for providers without native tool calls."""
from __future__ import annotations

import ast
import json
import logging
import re
import time
import traceback
from dataclasses import dataclass

from django.conf import settings

from api.background_agent.attachments import mark_qwen_files_sent, qwen_files_for_iteration
from api.background_agent.context import build_snapshot, compact_if_needed
from api.background_agent.events import add_message, emit
from api.background_agent.labels import tool_label
from api.background_agent.workspace import GitWorkspace, ToolExecutor, WorkspaceError
from api.models import BackgroundAgentSession
from api import qwen_proxy
from api.utils import now_ms

logger = logging.getLogger(__name__)

# A turn may carry several tool calls, but keep each step focused.
_MAX_ACTIONS_PER_TURN = 12

SYSTEM_PROMPT = r'''
You are NEBians Background Agent, a senior autonomous software engineer operating in a real Git repository.
You do not have native function calling. Every response MUST be one valid JSON object and nothing else.

Response schema:
{
  "thought": "brief engineering reasoning shown in the activity log",
  "actions": [
    {"tool": "list_files", "arguments": {"path": ".", "depth": 3}},
    {"tool": "read_file", "arguments": {"path": "path/to/file", "start_line": 1, "end_line": 400}},
    {"tool": "search_text", "arguments": {"query": "needle", "path": "."}},
    {"tool": "edit_file", "arguments": {"path": "path/to/file", "old_text": "exact existing block", "new_text": "replacement block", "replace_all": false}},
    {"tool": "multi_edit", "arguments": {"path": "path/to/file", "edits": [{"old_text": "...", "new_text": "..."}]}},
    {"tool": "write_file", "arguments": {"path": "path/to/file", "content": "complete file content"}},
    {"tool": "apply_patch", "arguments": {"patch": "unified git diff"}},
    {"tool": "delete_file", "arguments": {"path": "path/to/file"}},
    {"tool": "copy_file", "arguments": {"source": "a", "destination": "b"}},
    {"tool": "move_file", "arguments": {"source": "a", "destination": "b"}},
    {"tool": "create_directory", "arguments": {"path": "lib/util"}},
    {"tool": "run_command", "arguments": {"argv": ["python", "-m", "pytest"], "cwd": ".", "timeout": 300}},
    {"tool": "git_status", "arguments": {}},
    {"tool": "git_diff", "arguments": {}},
    {"tool": "git_log", "arguments": {"limit": 20}},
    {"tool": "git_stage", "arguments": {"paths": ["src/app.py"]}},
    {"tool": "git_commit", "arguments": {"message": "concise conventional message"}},
    {"tool": "git_push", "arguments": {"branch": "nebians-agent/..."}},
    {"tool": "git_pull", "arguments": {}},
    {"tool": "git_restore", "arguments": {"paths": ["src/app.py"], "staged": false}}
  ],
  "final": "set ONLY when the goal is genuinely complete; summarize the implementation and validation",
  "needs_input": false,
  "summary": "compact durable state for the next turn (what is done, what remains, key decisions)"
}

How to edit code (in order of preference):
1. edit_file / multi_edit — the most reliable. Provide old_text copied verbatim from read_file, with enough surrounding lines to be unique. It tolerates incidental whitespace drift and tells you the closest line if it cannot match.
2. write_file — for brand-new files or full rewrites.
3. apply_patch — unified diff. Use only for bulk changes; it is less forgiving than edit_file.

Rules:
- Inspect before editing (list_files / read_file / search_text). Preserve the repository's architecture, style, conventions, security boundaries and UX.
- Work only in the supplied task branch. Never switch, merge, reset, rebase, force-push or modify the source/default branch.
- Never read or expose secrets, .env files, credentials, SSH material, or paths outside the workspace.
- run_command takes an argv array only — no shell operators, pipes, redirection or substitution.
- Run relevant tests, linters, type checks or builds before declaring completion. Do not fabricate results; when a command fails, inspect and fix it, or report the exact limitation.
- There is no iteration budget. Work iteratively until the goal is truly complete, then set "final". If you genuinely need a decision from the operator, set "needs_input": true with no actions.
- If the user interrupts with a follow-up, treat the newest user message as a higher-priority refinement unless it conflicts with repository security.
- You are running through Qwen 3.7 Plus. Use the supplied attachments and anchored context as authoritative inputs.
'''.strip()


@dataclass
class ParsedResponse:
    thought: str
    actions: list[dict]
    final: str
    needs_input: bool
    summary: str


class AgentPaused(Exception):
    pass


class AgentStopped(Exception):
    pass


class BackgroundAgentRunner:
    def __init__(self, session: BackgroundAgentSession):
        self.session = session
        self.workspace = GitWorkspace(session.project, session)
        self.tools = ToolExecutor(self.workspace)

    def run(self):
        try:
            self._set_status('preparing', 5, 'Preparing isolated worktree')
            emit(self.session, 'session.preparing', 'Syncing repository and creating the task branch')
            self._check_control()
            self.workspace.prepare_session()
            emit(self.session, 'workspace.ready', f'Working on {self.session.work_branch}', {
                'sourceBranch': self.session.source_branch,
                'workBranch': self.session.work_branch,
                'baseSha': self.session.base_sha,
            })
            self._set_status('running', 12, 'Agent is inspecting the repository')
            self._loop()
        except AgentPaused:
            self._set_status('paused', self.session.progress, 'Paused')
            emit(self.session, 'session.paused', 'Agent paused at a safe checkpoint')
        except AgentStopped:
            self._set_status('cancelled', self.session.progress, 'Stopped', completed=True)
            emit(self.session, 'session.cancelled', 'Agent stopped by an administrator')
        except Exception as exc:
            logger.exception('Background agent session %s failed', self.session.id)
            self.session.status = 'failed'
            self.session.last_error = str(exc)[:8000]
            self.session.progress_label = 'Failed'
            self.session.completed_at = now_ms()
            self.session.updated_at = now_ms()
            self.session.save(update_fields=['status', 'last_error', 'progress_label', 'completed_at', 'updated_at'])
            emit(self.session, 'session.failed', str(exc)[:1000], {'trace': traceback.format_exc()[-6000:]})

    def _loop(self):
        # No iteration cap: the agent works until it reports completion, asks for
        # input, is paused/stopped, or hits an unrecoverable error.
        while True:
            self._check_control()
            self.session.refresh_from_db(fields=['control_state', 'status', 'iteration'])
            iteration = self.session.iteration + 1
            prompt = self._build_prompt(iteration)
            file_paths, qwen_attachments = qwen_files_for_iteration(self.session)
            self._heartbeat(progress=min(92, 12 + iteration * 2), label=f'Agent iteration {iteration}')
            emit(self.session, 'model.requested', f'Calling Qwen 3.7 Plus for iteration {iteration}', {
                'model': 'qwen3.7-plus', 'attachmentCount': len(file_paths),
            })
            raw = self._call_provider(prompt, file_paths=file_paths)
            mark_qwen_files_sent(qwen_attachments, iteration)
            parsed = parse_model_response(raw)
            format_retries = max(0, min(int(getattr(settings, 'BACKGROUND_AGENT_FORMAT_RETRIES', 1)), 3))
            for retry_index in range(format_retries):
                if parsed.summary != 'Provider returned non-JSON output; waiting for administrator guidance.':
                    break
                emit(self.session, 'model.format_retry', 'Provider output was not valid JSON; requesting a schema repair', {
                    'iteration': iteration, 'retry': retry_index + 1,
                })
                repair_prompt = f'''{prompt}

FORMAT REPAIR
Your prior response did not match the required JSON protocol. Do not continue the task yet.
Convert the intended next step below into exactly one valid JSON object matching the system schema.
Do not use markdown fences or any text outside the JSON object.

PRIOR OUTPUT
{raw[:12000]}
'''
                raw = self._call_provider(repair_prompt)
                parsed = parse_model_response(raw)
            add_message(self.session, 'assistant', parsed.thought or parsed.final or 'Agent response received', {
                'iteration': iteration,
                'raw': raw[:30000],
                'summary': parsed.summary,
                'needsInput': parsed.needs_input,
            })
            self.session.iteration = iteration
            self.session.agent_state = json.dumps({
                'summary': parsed.summary,
                'lastThought': parsed.thought,
                'lastIteration': iteration,
            }, ensure_ascii=False)
            self.session.updated_at = now_ms()
            self.session.save(update_fields=['iteration', 'agent_state', 'updated_at'])

            if parsed.actions:
                self._run_actions(parsed.actions[:_MAX_ACTIONS_PER_TURN], iteration)
                continue

            if parsed.final:
                self._complete(parsed.final)
                return

            self._set_status('waiting', self.session.progress, 'Waiting for clarification')
            emit(self.session, 'session.waiting', parsed.thought or 'The agent needs additional direction')
            return

    def _run_actions(self, actions, iteration):
        for index, action in enumerate(actions, 1):
            self._check_control()
            tool_name = (action.get('tool') or 'unknown').strip()
            arguments = action.get('arguments') or {}
            result = self.tools.execute(action)
            ok = bool(result.get('ok', False))
            label = tool_label(tool_name, arguments, ok=ok)
            compact = self._compact_result(result)
            add_message(self.session, 'tool', compact, {
                'iteration': iteration,
                'index': index,
                'tool': tool_name,
                'label': label,
                'ok': ok,
            })
            emit(
                self.session,
                'tool.executed' if ok else 'tool.failed',
                label,
                {'iteration': iteration, 'index': index, 'tool': tool_name, 'label': label, 'ok': ok,
                 'error': result.get('error', '')[:1000]},
            )

    @staticmethod
    def _compact_result(result):
        """Serialise a tool result for the transcript / expandable UI panel."""
        try:
            encoded = json.dumps(result, ensure_ascii=False)
        except (TypeError, ValueError):
            encoded = str(result)
        if len(encoded) > 120000:
            encoded = encoded[:120000] + '\n[tool result truncated in conversation log]'
        return encoded

    def _call_provider(self, prompt: str, *, system_prompt: str = SYSTEM_PROMPT, file_paths=None, max_tokens=None) -> str:
        model = 'qwen3.7-plus'
        output_tokens = int(max_tokens or getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                response = qwen_proxy.call_qwen(
                    system_prompt=system_prompt,
                    user_message=prompt,
                    model=model,
                    max_tokens=output_tokens,
                    file_paths=file_paths or None,
                )
                if response:
                    return str(response)
                raise WorkspaceError(f'Qwen {model} returned an empty response')
            except (AgentPaused, AgentStopped):
                raise
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'Qwen attempt {attempt} failed; retrying in {delay}s', {
                    'provider': 'qwen', 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        raise WorkspaceError(
            f'Qwen {model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    def _compact_call(self, system_prompt: str, prompt: str) -> str:
        return self._call_provider(
            prompt,
            system_prompt=system_prompt,
            max_tokens=int(getattr(settings, 'BACKGROUND_AGENT_COMPACTION_MAX_TOKENS', 5000)),
        )

    def _fixed_prompt(self, iteration: int, state: dict, tree: str, status: str) -> str:
        return f"""TASK
Repository: {self.session.project.repo_full_name}
Source branch (read-only base): {self.session.source_branch}
Task branch: {self.session.work_branch}
Goal: {self.session.goal}
Iteration: {iteration} (no cap - keep going until the goal is complete)
Model: Qwen 3.7 Plus

DURABLE STATE
{json.dumps(state, ensure_ascii=False)}

CURRENT GIT STATUS
{status or '(clean)'}

INITIAL REPOSITORY MAP
{tree or '(already supplied or request list_files for a focused path)'}"""

    def _build_prompt(self, iteration: int) -> str:
        try:
            state = json.loads(self.session.agent_state or '{}')
        except (TypeError, json.JSONDecodeError):
            state = {}
        tree = ''
        if iteration == 1:
            tree_result = self.tools.list_files('.', depth=3, limit=600)
            tree = '\n'.join(tree_result['entries'])
        status = self.workspace.status()
        fixed = self._fixed_prompt(iteration, state, tree, status)
        compact_if_needed(self.session, fixed, self._compact_call)
        snapshot = build_snapshot(self.session, fixed)
        self.session.context_tokens_estimate = snapshot.estimated_tokens
        self.session.context_window_tokens = snapshot.window_tokens
        self.session.save(update_fields=['context_tokens_estimate', 'context_window_tokens'])
        threshold_percent = round(snapshot.threshold_tokens * 100 / snapshot.window_tokens)
        return f"""{fixed}

ANCHORED CONTEXT AND RECENT CONVERSATION
{snapshot.transcript or '(none)'}

CONTEXT ACCOUNTING
Estimated input: {snapshot.estimated_tokens} / {snapshot.window_tokens} tokens ({snapshot.percent}%).
Automatic anchored compaction runs at {threshold_percent}%.

Decide the next smallest set of high-value actions. Prefer edit_file/multi_edit over apply_patch. Return exactly one JSON object matching the required schema.
""".strip()

    def _complete(self, final: str):
        self._check_control()
        self._heartbeat(95, 'Building diff and downloadable artifacts')
        diff = self.workspace.diff(max_chars=1_000_000)
        changed = self.workspace.changed_files()
        artifacts = self.workspace.build_artifacts()
        head = self.workspace.git('rev-parse', 'HEAD').get('stdout', '').strip()
        self.session.status = 'completed'
        self.session.progress = 100
        self.session.progress_label = 'Completed'
        self.session.summary = final
        self.session.final_diff = diff
        self.session.changed_files = json.dumps(changed, ensure_ascii=False)
        self.session.test_summary = self._test_summary()
        self.session.head_sha = head
        self.session.control_state = ''
        self.session.completed_at = now_ms()
        self.session.updated_at = now_ms()
        self.session.last_heartbeat_at = now_ms()
        self.session.save(update_fields=[
            'status', 'progress', 'progress_label', 'summary', 'final_diff',
            'changed_files', 'test_summary', 'head_sha', 'control_state', 'completed_at',
            'updated_at', 'last_heartbeat_at',
        ])
        emit(self.session, 'session.completed', final[:1000], {
            'changedFiles': changed, 'artifacts': artifacts,
        })

    def _test_summary(self):
        rows = []
        for message in self.session.messages.filter(role='tool').order_by('-created_at')[:100]:
            try:
                payload = json.loads(message.content)
            except (TypeError, json.JSONDecodeError):
                continue
            tool = payload.get('tool')
            result = payload.get('result') or payload
            if tool != 'run_command':
                continue
            argv = result.get('argv') or []
            command = ' '.join(str(part) for part in argv)
            returncode = result.get('returncode')
            duration = result.get('duration')
            status = 'passed' if returncode == 0 else f'failed ({returncode})'
            suffix = f' in {duration}s' if duration is not None else ''
            rows.append(f'- `{command}` — {status}{suffix}')
            if len(rows) >= 20:
                break
        rows.reverse()
        return '\n'.join(rows) or 'No validation command was recorded.'

    def _check_control(self):
        self.session.refresh_from_db(fields=['control_state', 'status'])
        if self.session.control_state == 'pause':
            self.session.control_state = ''
            self.session.save(update_fields=['control_state'])
            raise AgentPaused()
        if self.session.control_state == 'stop':
            self.session.control_state = ''
            self.session.save(update_fields=['control_state'])
            raise AgentStopped()

    def _heartbeat(self, progress=None, label=None):
        fields = ['last_heartbeat_at', 'updated_at']
        self.session.last_heartbeat_at = now_ms()
        self.session.updated_at = now_ms()
        if progress is not None:
            self.session.progress = max(0, min(int(progress), 100))
            fields.append('progress')
        if label is not None:
            self.session.progress_label = label[:255]
            fields.append('progress_label')
        self.session.save(update_fields=fields)

    def _set_status(self, status, progress, label, completed=False):
        self.session.status = status
        self.session.progress = max(0, min(int(progress or 0), 100))
        self.session.progress_label = label[:255]
        self.session.updated_at = now_ms()
        self.session.last_heartbeat_at = now_ms()
        fields = ['status', 'progress', 'progress_label', 'updated_at', 'last_heartbeat_at']
        if not self.session.started_at and status in ('preparing', 'running'):
            self.session.started_at = now_ms()
            fields.append('started_at')
        if completed:
            self.session.completed_at = now_ms()
            fields.append('completed_at')
        self.session.save(update_fields=fields)


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


def parse_model_response(raw: str) -> ParsedResponse:
    text = (raw or '').strip()
    candidates = [text]
    candidates.extend(re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', text, flags=re.I | re.S))
    candidates.extend(_balanced_json_candidates(text))
    payload = None
    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        payload = _decode_protocol_object(candidate)
        if payload is not None:
            break
    if payload is None:
        return ParsedResponse(
            thought=text[:12000],
            actions=[],
            final='',
            needs_input=True,
            summary='Provider returned non-JSON output; waiting for administrator guidance.',
        )
    actions = payload.get('actions')
    if not isinstance(actions, list):
        actions = []
    normalized = []
    for action in actions:
        if not isinstance(action, dict) or not isinstance(action.get('tool'), str):
            continue
        arguments = action.get('arguments')
        normalized.append({
            'tool': action['tool'].strip(),
            'arguments': arguments if isinstance(arguments, dict) else {},
        })
    return ParsedResponse(
        thought=str(payload.get('thought') or '')[:20000],
        actions=normalized[:_MAX_ACTIONS_PER_TURN],
        final=str(payload.get('final') or '')[:30000],
        needs_input=bool(payload.get('needs_input', False)),
        summary=str(payload.get('summary') or '')[:12000],
    )
