"""Iterative coding-agent harness for providers without native tool calls."""
from __future__ import annotations

import json
import logging
import re
import time
import traceback
from dataclasses import dataclass

from django.conf import settings

from api.background_agent.events import add_message, emit
from api.background_agent.workspace import GitWorkspace, ToolExecutor, WorkspaceError
from api.models import BackgroundAgentSession, BotConfig
from api.neby import call_ai_api
from api.utils import now_ms

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = r'''
You are NEBians Background Agent, a senior autonomous software engineer operating in a real Git repository.
You do not have native function calling. Every response MUST be one valid JSON object and nothing else.

Response schema:
{
  "thought": "brief engineering reasoning safe to show in the activity log",
  "actions": [
    {"tool": "list_files", "arguments": {"path": ".", "depth": 3}},
    {"tool": "read_file", "arguments": {"path": "path/to/file", "start_line": 1, "end_line": 400}},
    {"tool": "search_text", "arguments": {"query": "needle", "path": "."}},
    {"tool": "write_file", "arguments": {"path": "path/to/file", "content": "complete file content"}},
    {"tool": "apply_patch", "arguments": {"patch": "unified git patch"}},
    {"tool": "delete_file", "arguments": {"path": "path/to/file"}},
    {"tool": "run_command", "arguments": {"argv": ["python", "-m", "pytest"], "cwd": ".", "timeout": 300}},
    {"tool": "git_status", "arguments": {}},
    {"tool": "git_diff", "arguments": {}}
  ],
  "final": "only set when the requested goal is complete; summarize implementation and tests",
  "needs_input": false,
  "summary": "compact durable state for the next iteration"
}

Rules:
- Inspect before editing. Preserve the repository's existing architecture, style, security boundaries, and UX.
- Work only in the supplied task branch. Never switch, merge, reset, rebase, force-push, or modify the source/default branch.
- Never read or expose secrets, .env files, credentials, SSH material, browser profiles, or paths outside the workspace.
- Prefer precise patches over rewriting large files. Do not modify .git.
- Use run_command with an argv array; never depend on shell operators, pipes, redirection, or command substitution.
- Use the dedicated git_status and git_diff tools for Git inspection. Git history and repository credentials are not exposed inside command sandboxes.
- Run relevant tests, linters, type checks, or builds before declaring completion.
- Do not fabricate successful test results. When a command fails, inspect and fix it or report the exact limitation.
- Keep each response focused: at most 8 actions. Continue iteratively until the goal is genuinely complete.
- If the user interrupts with a follow-up, treat the newest user message as a higher-priority refinement unless it conflicts with safety.
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
        while self.session.iteration < self.session.max_iterations:
            self._check_control()
            self.session.refresh_from_db(fields=['control_state', 'status', 'iteration', 'max_iterations'])
            iteration = self.session.iteration + 1
            prompt = self._build_prompt(iteration)
            self._heartbeat(progress=min(88, 12 + iteration * 3), label=f'Agent iteration {iteration}')
            emit(self.session, 'model.requested', f'Calling AI provider for iteration {iteration}')
            raw = self._call_provider(prompt)
            parsed = parse_model_response(raw)
            format_retries = max(0, min(int(getattr(settings, 'BACKGROUND_AGENT_FORMAT_RETRIES', 1)), 3))
            for retry_index in range(format_retries):
                if parsed.summary != 'Provider returned non-JSON output; waiting for administrator guidance.':
                    break
                emit(self.session, 'model.format_retry', 'Provider output was not valid JSON; requesting a schema repair', {
                    'iteration': iteration,
                    'retry': retry_index + 1,
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
                for index, action in enumerate(parsed.actions[:8], 1):
                    self._check_control()
                    tool_name = action.get('tool') or 'unknown'
                    emit(self.session, 'tool.started', f'{tool_name}', {'iteration': iteration, 'index': index})
                    result = self.tools.execute(action)
                    serialized_result = json.dumps(result, ensure_ascii=False)
                    if len(serialized_result) > 120000:
                        serialized_result = serialized_result[:120000] + '\n[tool result truncated in conversation log]'
                    add_message(self.session, 'tool', serialized_result, {
                        'iteration': iteration,
                        'tool': tool_name,
                        'ok': result.get('ok', False),
                    })
                    emit(self.session, 'tool.completed' if result.get('ok') else 'tool.failed', tool_name, result)
                continue

            if parsed.final:
                self._complete(parsed.final)
                return

            self._set_status('waiting', self.session.progress, 'Waiting for clarification')
            emit(self.session, 'session.waiting', parsed.thought or 'The agent needs additional direction')
            return

        self._set_status('waiting', self.session.progress, 'Iteration limit reached')
        emit(self.session, 'session.waiting', 'Iteration limit reached. Send guidance and resume to continue.')

    def _call_provider(self, prompt: str) -> str:
        config = self.session.bot_config or BotConfig.objects.filter(enabled=True).first()
        if not config:
            raise WorkspaceError('No enabled AI bot/provider configuration is available')
        original_max = config.response_max_length
        config.response_max_length = max(
            int(original_max or 0),
            int(getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000)),
        )
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                response = call_ai_api(SYSTEM_PROMPT, prompt, config=config)
                if response:
                    return str(response)
                raise WorkspaceError(f'AI provider {config.provider}/{config.model} returned an empty response')
            except (AgentPaused, AgentStopped):
                raise
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'Provider attempt {attempt} failed; retrying in {delay}s', {
                    'provider': config.provider,
                    'model': config.model,
                    'error': str(exc)[:1000],
                    'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        raise WorkspaceError(
            f'AI provider {config.provider}/{config.model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    def _build_prompt(self, iteration: int) -> str:
        state = {}
        try:
            state = json.loads(self.session.agent_state or '{}')
        except (TypeError, json.JSONDecodeError):
            state = {}
        messages = list(self.session.messages.order_by('-created_at')[:20])
        messages.reverse()
        transcript = []
        total = 0
        for message in messages:
            content = message.content
            if len(content) > 12000:
                content = content[:12000] + '\n[message truncated]'
            row = f'{message.role.upper()}: {content}'
            total += len(row)
            if total > 60000:
                break
            transcript.append(row)
        tree = ''
        if iteration == 1:
            tree_result = self.tools.list_files('.', depth=3, limit=600)
            tree = '\n'.join(tree_result['entries'])
        status = self.workspace.status()
        return f'''
TASK
Repository: {self.session.project.repo_full_name}
Source branch (read-only base): {self.session.source_branch}
Task branch: {self.session.work_branch}
Goal: {self.session.goal}
Iteration: {iteration}/{self.session.max_iterations}

DURABLE STATE
{json.dumps(state, ensure_ascii=False)}

CURRENT GIT STATUS
{status or '(clean)'}

INITIAL REPOSITORY MAP
{tree or '(already supplied or request list_files for a focused path)'}

RECENT CONVERSATION AND TOOL RESULTS
{chr(10).join(transcript) or '(none)'}

Decide the next smallest set of high-value actions. Return exactly one JSON object matching the required schema.
'''.strip()

    def _complete(self, final: str):
        self._check_control()
        self._heartbeat(92, 'Building diff and downloadable artifacts')
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
            'changedFiles': changed,
            'artifacts': artifacts,
        })

    def _test_summary(self):
        rows = []
        for message in self.session.messages.filter(role='tool').order_by('-created_at')[:100]:
            try:
                payload = json.loads(message.content)
            except (TypeError, json.JSONDecodeError):
                continue
            if payload.get('tool') != 'run_command':
                continue
            result = payload.get('result') or {}
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


def parse_model_response(raw: str) -> ParsedResponse:
    text = (raw or '').strip()
    candidates = [text]
    fenced = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', text, flags=re.I | re.S)
    candidates.extend(fenced)
    first, last = text.find('{'), text.rfind('}')
    if first >= 0 and last > first:
        candidates.append(text[first:last + 1])
    payload = None
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                payload = obj
                break
        except json.JSONDecodeError:
            continue
    if payload is None:
        # A provider that ignores formatting still gets a safe waiting state,
        # preserving its response for the administrator instead of executing it.
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
    normalized = [a for a in actions if isinstance(a, dict) and isinstance(a.get('tool'), str)]
    return ParsedResponse(
        thought=str(payload.get('thought') or '')[:20000],
        actions=normalized[:8],
        final=str(payload.get('final') or '')[:30000],
        needs_input=bool(payload.get('needs_input', False)),
        summary=str(payload.get('summary') or '')[:12000],
    )
