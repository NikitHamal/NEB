"""Iterative coding-agent harness for providers without native tool calls."""
from __future__ import annotations

import json
import logging
import re
import time
import traceback

from django.conf import settings

from api.background_agent.attachments import mark_qwen_files_sent, qwen_files_for_iteration
from api.background_agent.context import build_snapshot, compact_if_needed, compact_now
from api.background_agent.events import add_message, emit, store_prompt
from api.background_agent.labels import tool_label
from api.background_agent.protocol import MAX_ACTIONS_PER_TURN, ParsedResponse, parse_model_response
from api.background_agent.qwen_harness import (
    action_signature,
    build_system_prompt,
    build_user_prompt,
    format_repair_prompt,
    heal_note,
    json_repair_prompt,
    needs_format_repair,
    render_hermes_transcript,
    run_action_batches,
    thought_signature,
)
from api.background_agent.workspace import GitWorkspace, ToolExecutor, WorkspaceError
from api.models import BackgroundAgentSession
from api import qwen_proxy
from api.llm.client import LLMError
from api.llm.runtime import call_session_provider, call_session_provider_stream, resolve_session_provider
from api.utils import now_ms

logger = logging.getLogger(__name__)

_MAX_ACTIONS_PER_TURN = MAX_ACTIONS_PER_TURN

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
    {"tool": "update_plan", "arguments": {"todos": [{"content": "single concrete step", "status": "pending|in_progress|completed"}], "explanation": "optional note for the operator"}},
    {"tool": "git_status", "arguments": {}},
    {"tool": "git_diff", "arguments": {}},
    {"tool": "git_log", "arguments": {"limit": 20}},
    {"tool": "git_pull", "arguments": {}},
    {"tool": "git_restore", "arguments": {"paths": ["src/app.py"], "staged": false}},
    {"tool": "git_stage", "arguments": {"paths": ["src/app.py"]}},
    {"tool": "git_commit", "arguments": {"message": "concise conventional commit message"}},
    {"tool": "git_push", "arguments": {"branch": "task-branch-name"}},
    {"tool": "deploy_live_hotfix", "arguments": {"reason": "Fix 500 error in resource upload"}}
  ],
  "final": "set ONLY when the goal is genuinely complete; summarize the implementation and validation",
  "needs_input": false,
  "summary": "compact durable state for the next turn (what is done, what remains, key decisions)"
}

How to edit code (in order of preference):
1. edit_file / multi_edit — the most reliable. Provide old_text copied verbatim from read_file, with enough surrounding lines to be unique. It tolerates incidental whitespace drift and tells you the closest line if it cannot match. For large batches (5+ edits) use "best_effort": true so a single mismatch doesn't discard all other edits.
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

Planning (update_plan):
- For any goal that needs more than ~3 steps, call update_plan as your FIRST action with the full step list, then keep it live: exactly one item marked "in_progress", items flipped to "completed" as soon as they are done, and an updated update_plan call whenever the plan changes.
- Every plan item must be "completed" before you set "final".

Git policy:
- Write your own commits as you work: after completing a meaningful unit of work, call git_commit with a clear, descriptive message (conventional style, e.g. "fix: refresh token after expiry"). Multiple commits per task are allowed and expected. Never use vague messages like "update" or "changes" — say what changed and why. git_commit stages and commits the current changes for you.
- Call git_push exactly ONCE per task, only when the work is finished and validated. If you set "final" in the same response, place git_push in actions AND still set "final" — both are honored. The server also pushes automatically when you finish, so a final push is guaranteed.
- If you catch yourself repeating the same analysis or the same action sequence without new information, stop: either change your approach materially or set needs_input so the operator can unblock you.
- The task branch is generated for you before you start (shown in the TASK header). Never switch, merge, reset, rebase, force-push or modify the source/default branch.
'''.strip()

BRANCH_NAME_SYSTEM_PROMPT = r'''
You are naming a short git branch for an autonomous coding task. Respond with exactly one JSON object and nothing else:

{"branch": "...", "description": "..."}

Branch rules:
- Short: 3-6 words, 5-40 characters, all lowercase, hyphen-separated, no spaces.
- No slashes, no prefixes like "nebians-agent/" or "feature/", no generic words like "system", "task", "fix".
- Name describes the concrete outcome of the goal (e.g. "oauth-token-refresh", "pdf-zoom-sync", "exam-countdown-widget").
- Use the task title and goal below as the source of the name; if the goal names a module, bug or feature, use that.

Description rules:
- One sentence, max 120 characters, plain English, describing what this branch does.
'''.strip()


class AgentPaused(Exception):
    pass


class AgentStopped(Exception):
    pass


class BackgroundAgentRunner:
    def __init__(self, session: BackgroundAgentSession):
        self.session = session
        self.workspace = GitWorkspace(session.project, session)
        self.tools = ToolExecutor(self.workspace)
        # Official-API provider resolution (None = legacy Qwen web path).
        # Lazy: resolved on the first provider call so keys saved after a
        # session was queued still apply.
        self._llm_resolved = None
        self._llm_resolved_once = False
        self._call_announced = False
        self._pending_reasoning = ''
        # Actual model response time from the upstream API (milliseconds),
        # vs wall-clock from Python-side timer which includes Qwen pool
        # queue, file uploads, and format-retry overhead.
        self._last_model_response_ms = 0
        # Anti-loop guard: count consecutive identical reasoning / action blocks.
        self._last_signature = ''
        self._signature_repeats = 0
        self._last_action_sig = ''
        self._action_repeats = 0
        self._pending_heal = []
        # Live-stream pub/sub client (lazy; None when Redis is unavailable).
        self._stream_redis_client = None

    def run(self):
        try:
            self._set_status('preparing', 5, 'Naming the task branch')
            emit(self.session, 'session.preparing', 'Naming the task branch and syncing the repository')
            self._check_control()
            self._generate_branch_name()
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

    _BRANCH_RE = re.compile(r'^[a-z0-9][a-z0-9-]{2,58}[a-z0-9]$')

    def _generate_branch_name(self):
        """Ask the LLM for a short, task-specific branch name before the
        worktree is created. Falls back to the deterministic generator when
        the model call fails or returns something unusable."""
        if self.session.work_branch:
            return
        title = (self.session.title or '').strip()
        goal = (self.session.goal or '').strip()
        prompt = (
            f'Task title: {title or "(untitled)"}\n'
            f'User goal: {goal}\n'
        )
        fallback = None
        try:
            from api.background_agent.workspace import build_branch_name
            fallback = build_branch_name(goal, str(self.session.id))
        except Exception:
            pass
        try:
            raw = self._call_provider(
                prompt,
                system_prompt=BRANCH_NAME_SYSTEM_PROMPT,
                max_tokens=400,
            )
            branch, description = self._parse_branch_response(raw, fallback)
        except Exception as exc:
            logger.exception('Branch-name generation failed for session %s', self.session.id)
            emit(self.session, 'branch.fallback', f'Branch-name generation failed ({str(exc)[:200]}); using a generated name')
            branch, description = fallback or 'task-branch', ''
        if not branch or branch in ('main', 'master'):
            branch = fallback or 'task-branch'
        try:
            state = json.loads(self.session.agent_state or '{}')
        except (TypeError, json.JSONDecodeError):
            state = {}
        state['branchDescription'] = description
        self.session.work_branch = branch
        self.session.agent_state = json.dumps(state, ensure_ascii=False)
        self.session.save(update_fields=['work_branch', 'agent_state', 'updated_at'])
        emit(self.session, 'branch.named', f'Task branch: {branch}', {
            'branch': branch, 'description': description,
        })

    @classmethod
    def _parse_branch_response(cls, raw: str, fallback: str):
        text = re.sub(r'```(?:json)?', '', raw or '').replace('```', '').strip()
        start, end = text.find('{'), text.rfind('}')
        if start < 0 or end <= start:
            raise ValueError('no JSON object in branch-name response')
        payload = json.loads(text[start:end + 1])
        branch = cls._sanitize_branch_name(payload.get('branch') or '')
        if not cls._BRANCH_RE.match(branch or '') or branch in ('main', 'master'):
            raise ValueError(f'invalid branch name: {branch!r}')
        description = str(payload.get('description') or '').strip()[:120]
        return branch, description

    @staticmethod
    def _sanitize_branch_name(name: str) -> str:
        cleaned = re.sub(r'[^a-z0-9]+', '-', (name or '').strip().lower()).strip('-')
        cleaned = re.sub(r'-{2,}', '-', cleaned)
        return cleaned[:60].rstrip('-')

    def _loop(self):
        # No iteration cap: the agent works until it reports completion, asks for
        # input, is paused/stopped, or hits an unrecoverable error.
        while True:
            self._check_control()
            self.session.refresh_from_db(fields=['control_state', 'status', 'iteration', 'compact_requested_at'])
            iteration = self.session.iteration + 1
            prompt = self._build_prompt(iteration)
            file_paths, qwen_attachments = qwen_files_for_iteration(self.session)
            self._heartbeat(progress=min(92, 12 + iteration * 2), label=f'Agent iteration {iteration}')

            # Log full prompt for export/debug
            store_prompt(self.session, prompt, iteration)

            call_label = self._llm_label()
            resolved_now = self._llm_selection()
            # Announce the model ONCE per run — a per-iteration "Calling X for
            # iteration N" line is pure noise in the conversation timeline.
            if not self._call_announced:
                self._call_announced = True
                emit(self.session, 'model.started', f'Running with {call_label}', {
                    'model': resolved_now.model if resolved_now is not None else self._community_model(),
                    'provider': self.session.llm_provider or 'qwen',
                    'attachmentCount': len(file_paths),
                })
            model_started = time.monotonic()
            raw = self._call_provider(prompt, file_paths=file_paths)
            mark_qwen_files_sent(qwen_attachments, iteration)
            parsed = parse_model_response(raw, extra_thought=self._pending_reasoning)
            format_retries_allowed = max(0, min(int(getattr(settings, 'BACKGROUND_AGENT_FORMAT_RETRIES', 2)), 3))
            format_retries_used = 0
            for retry_index in range(format_retries_allowed):
                if not needs_format_repair(parsed):
                    break
                format_retries_used += 1
                emit(self.session, 'model.format_retry', 'Provider output was not a valid tool protocol; requesting a schema repair', {
                    'iteration': iteration, 'retry': retry_index + 1,
                    'protocol': getattr(parsed, 'protocol', 'none'),
                })
                if self._uses_qwen_harness():
                    repair_prompt = format_repair_prompt(prompt, raw)
                else:
                    repair_prompt = json_repair_prompt(prompt, raw)
                raw = self._call_provider(repair_prompt)
                parsed = parse_model_response(raw, extra_thought=self._pending_reasoning)
            response_ms = self._last_model_response_ms or int((time.monotonic() - model_started) * 1000)
            self._record_messages(parsed, iteration, raw, file_paths, format_retries_used, response_ms)

            signature = thought_signature(parsed.thought)
            if signature and signature == self._last_signature:
                self._signature_repeats += 1
            elif signature:
                self._signature_repeats = 0
                self._last_signature = signature
            act_sig = action_signature(parsed.actions)
            if act_sig and act_sig == self._last_action_sig:
                self._action_repeats += 1
            elif act_sig:
                self._action_repeats = 0
                self._last_action_sig = act_sig

            self.session.iteration = iteration
            state = {}
            try:
                prior = json.loads(self.session.agent_state or '{}')
                if prior.get('branchDescription'):
                    state['branchDescription'] = prior['branchDescription']
            except (TypeError, json.JSONDecodeError):
                pass
            state.update({
                'summary': parsed.summary,
                'lastThought': parsed.thought,
                'lastIteration': iteration,
            })
            self.session.agent_state = json.dumps(state, ensure_ascii=False)
            self.session.updated_at = now_ms()
            self.session.save(update_fields=['iteration', 'agent_state', 'updated_at'])

            if parsed.actions:
                self._run_actions(parsed.actions[:_MAX_ACTIONS_PER_TURN], iteration)

            # A response may carry BOTH actions and "final" (e.g. "commit, push,
            # done") — always honor final after the actions instead of looping.
            if parsed.final:
                self._complete(parsed.final)
                return

            if self._signature_repeats >= 3 or self._action_repeats >= 3:
                self._set_status('waiting', self.session.progress, 'Paused — repeated reasoning detected')
                emit(
                    self.session,
                    'session.waiting',
                    'The agent repeated the same reasoning or tool sequence several times without new information. '
                    'Send a clarifying message (or /compact) to unblock it.',
                )
                return

            if parsed.actions:
                continue

            self._set_status('waiting', self.session.progress, 'Waiting for clarification')
            emit(self.session, 'session.waiting', parsed.thought or 'The agent needs additional direction')
            return

    def _record_messages(self, parsed: ParsedResponse, iteration: int, raw: str, file_paths, format_retries_used: int, duration_ms: int):
        """Store the model turn: reasoning as a collapsible thought, the answer separately."""
        base = {
            'iteration': iteration,
            'raw': raw[:500000],
            'summary': parsed.summary,
            'needsInput': parsed.needs_input,
            'filePaths': file_paths or [],
            'formatRetries': format_retries_used,
            'durationMs': duration_ms,
        }
        if parsed.thought:
            add_message(self.session, 'assistant', parsed.thought, {**base, 'kind': 'thought'})
            if parsed.final:
                add_message(self.session, 'assistant', parsed.final, {'iteration': iteration, 'kind': 'final'})
        elif parsed.final:
            add_message(self.session, 'assistant', parsed.final, {**base, 'kind': 'final'})
        else:
            add_message(self.session, 'assistant', 'Agent response received', {**base, 'kind': 'assistant'})

    def _run_actions(self, actions, iteration):
        def execute_one(action):
            self._check_control()
            tool_name = (action.get('tool') or 'unknown').strip()
            arguments = action.get('arguments') or {}
            if tool_name == 'update_plan':
                result = self._update_plan(arguments)
            else:
                result = self.tools.execute(action)
            return action, result

        executed = run_action_batches(actions, execute_one)
        for index, (action, result) in enumerate(executed, 1):
            tool_name = (action.get('tool') or 'unknown').strip()
            arguments = action.get('arguments') or {}
            ok = bool(result.get('ok', False))
            label = result.pop('label', None) or tool_label(tool_name, arguments, ok=ok)
            compact = self._compact_result(result)
            add_message(self.session, 'tool', compact, {
                'iteration': iteration,
                'index': index,
                'tool': tool_name,
                'label': label,
                'ok': ok,
                'args': arguments,
            })
            note = heal_note(tool_name, result)
            if note:
                self._pending_heal.append(note)
            emit(
                self.session,
                'tool.executed' if ok else 'tool.failed',
                label,
                {'iteration': iteration, 'index': index, 'tool': tool_name, 'label': label, 'ok': ok,
                 'error': result.get('error', '')[:1000]},
            )

    # ------------------------------------------------------------------
    # Delivery: the model writes its own commits; push is guaranteed at the end.
    # ------------------------------------------------------------------

    def _ensure_final_push(self):
        """Best-effort final push so completed work always reaches the remote,
        even when the model never called git_push. workspace.push() commits any
        remaining uncommitted changes first, then pushes the task branch."""
        try:
            result = self.workspace.push()
            ok = bool(result and result.ok)
            emit(self.session, 'git.pushed', f'Pushed {self.session.work_branch}' if ok else 'Push reported no changes', {
                'branch': self.session.work_branch,
                'ok': ok,
                'detail': (result.get('stdout', '') if result else '')[-500:],
            })
        except Exception as exc:
            logger.exception('Final push failed for session %s', self.session.id)
            emit(self.session, 'git.push_failed', f'Automatic push failed: {str(exc)[:300]}')

    # ------------------------------------------------------------------
    # Live task planning.
    # ------------------------------------------------------------------

    _TODO_STATUSES = ('pending', 'in_progress', 'completed')

    def _update_plan(self, arguments):
        raw_todos = (arguments or {}).get('todos')
        if not isinstance(raw_todos, list):
            return {'ok': False, 'tool': 'update_plan', 'error': 'update_plan requires a "todos" array'}
        todos = []
        for item in raw_todos[:24]:
            if not isinstance(item, dict):
                continue
            content = str(item.get('content') or '').strip()[:220]
            if not content:
                continue
            status = str(item.get('status') or 'pending').strip().lower()
            if status not in self._TODO_STATUSES:
                status = 'pending'
            todos.append({'content': content, 'status': status})
        if not todos:
            return {'ok': False, 'tool': 'update_plan', 'error': 'The todos array was empty after normalization'}
        done = sum(1 for item in todos if item['status'] == 'completed')
        self.session.todos_json = json.dumps(todos, ensure_ascii=False)
        self.session.updated_at = now_ms()
        self.session.save(update_fields=['todos_json', 'updated_at'])
        explanation = str((arguments or {}).get('explanation') or '').strip()[:400]
        emit(self.session, 'plan.updated', f'Plan updated — {done} of {len(todos)} done', {
            'todos': todos, 'completed': done, 'total': len(todos), 'explanation': explanation,
        })
        if done == len(todos):
            hint = 'Every plan item is complete. Validate the work, call git_push once to deliver, then set "final".'
        else:
            next_step = next((item['content'] for item in todos if item['status'] != 'completed'), '')
            hint = f'Continue with: {next_step}' if next_step else ''
        return {
            'ok': True,
            'tool': 'update_plan',
            'label': f'Plan · {done}/{len(todos)} done',
            'result': {'todos': todos, 'completed': done, 'total': len(todos), 'hint': hint},
        }

    @staticmethod
    def _compact_result(result):
        """Serialise a tool result for the transcript / expandable UI panel."""
        try:
            encoded = json.dumps(result, ensure_ascii=False)
        except (TypeError, ValueError):
            encoded = str(result)
        if len(encoded) > 500000:
            encoded = encoded[:500000] + '\n[tool result truncated in conversation log]'
        return encoded

    def _llm_selection(self):
        """Resolve the session's LLM once per run. Returns None for the
        legacy community model path, or an api.llm ResolvedProvider."""
        if not self._llm_resolved_once:
            self._llm_resolved = resolve_session_provider(self.session)
            self._llm_resolved_once = True
            slug = (self.session.llm_provider or '').strip().lower()
            if slug and self._llm_resolved is None:
                from api.llm.registry import is_official_slug
                if is_official_slug(slug) or slug == 'custom':
                    # The picker selected an official provider that can no
                    # longer be served (key removed/disabled). Fall back to
                    # the shared default transparently instead of failing.
                    emit(self.session, 'model.fallback', f'Selected model is unavailable; using the default {self._llm_label_community_fallback()} instead', {
                        'requestedProvider': self.session.llm_provider,
                        'requestedModel': self.session.llm_model,
                    })
        return self._llm_resolved

    def _llm_label_community_fallback(self) -> str:
        try:
            from api.llm.runtime import model_display_label
            return model_display_label(self._community_slug(), self._community_model())
        except Exception:
            return f'Qwen ({self._community_model()})'

    def _community_slug(self) -> str:
        slug = (self.session.llm_provider or '').strip().lower()
        if slug in ('qwen', 'k2think', 'poolside', 'motiftech', 'metaai'):
            return slug
        return 'qwen'

    def _community_model(self) -> str:
        """Selected community model — Qwen web model, else the preset default
        for k2think/poolside/motiftech/metaai, else qwen3.8-max."""
        slug = (self.session.llm_provider or '').strip().lower()
        model = (self.session.llm_model or '').strip()
        if model:
            return model
        if slug == 'k2think':
            return 'MBZUAI-IFM/K2-Think-v2'
        if slug == 'poolside':
            return 'laguna-s-2.1'
        if slug == 'motiftech':
            return 'motif-102b'
        if slug == 'metaai':
            return 'metaai-instant'
        try:
            from api.qwen_utils.models import get_default_model
            return get_default_model() or 'qwen3.8-max'
        except Exception:
            return 'qwen3.8-max'

    def _llm_label(self) -> str:
        resolved = self._llm_selection()
        if resolved is not None:
            return f'{resolved.label} · {resolved.model}'
        try:
            from api.llm.runtime import model_display_label
            return model_display_label(self._community_slug(), self._community_model())
        except Exception:
            return f'Qwen ({self._community_model()})'

    def _uses_qwen_harness(self) -> bool:
        if not getattr(settings, 'BACKGROUND_AGENT_QWEN_HARNESS', True):
            return False
        if self._llm_selection() is not None:
            return False
        return self._community_slug() == 'qwen'

    def _system_prompt_for_run(self) -> str:
        if self._uses_qwen_harness():
            return build_system_prompt(self._llm_label())
        try:
            return SYSTEM_PROMPT.replace(
                'You are running through Qwen 3.7 Plus.',
                f'You are running through {self._llm_label()}.',
            )
        except Exception:
            return SYSTEM_PROMPT

    def _call_provider(self, prompt: str, *, system_prompt: str = None, file_paths=None, max_tokens=None) -> str:
        if system_prompt is None:
            system_prompt = self._system_prompt_for_run()
        self._pending_reasoning = ''
        primary_error = None
        try:
            resolved = self._llm_selection()
            if resolved is not None:
                return self._call_official_provider_stream(
                    resolved, prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens,
                )
            slug = (self.session.llm_provider or '').strip().lower()
            if slug in ('k2think', 'poolside', 'motiftech', 'metaai'):
                return self._call_community_proxy(
                    slug, prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens,
                )
            return self._call_qwen_legacy(prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens)
        except (AgentPaused, AgentStopped):
            raise
        except WorkspaceError as exc:
            primary_error = exc
        chain = self._bot_fallback_chain()
        if not chain:
            raise primary_error
        last_error = primary_error
        for entry in chain:
            self._check_control()
            label = self._fallback_entry_label(entry)
            try:
                emit(self.session, 'model.fallback', f'Primary provider failed; trying fallback: {label}', {
                    'provider': entry.get('provider'), 'model': entry.get('model') or '',
                    'error': str(last_error)[:1000],
                })
                return self._call_fallback_entry(entry, prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens)
            except (AgentPaused, AgentStopped):
                raise
            except WorkspaceError as exc:
                last_error = exc
                emit(self.session, 'model.fallback', f'Fallback {label} failed; next: {str(exc)[:400]}', {
                    'provider': entry.get('provider'), 'model': entry.get('model') or '',
                    'error': str(exc)[:1000],
                })
                continue
        raise WorkspaceError(
            f'All providers failed ({1 + len(chain)} tried, last: {last_error})'
        ) from last_error

    def _bot_fallback_chain(self) -> list:
        """Ordered fallback provider entries from the session's BotConfig."""
        try:
            bot = self.session.bot_config
        except Exception:
            bot = None
        if bot is None:
            return []
        return bot.get_fallback_chain()

    @staticmethod
    def _fallback_entry_label(entry: dict) -> str:
        slug = (entry.get('provider') or '').strip().lower()
        model = (entry.get('model') or '').strip()
        if slug == 'custom':
            return 'Custom endpoint' + (f' ({model})' if model else '')
        return f'{slug} {model}'.strip()

    def _call_fallback_entry(self, entry: dict, prompt: str, *, system_prompt: str, file_paths=None, max_tokens=None) -> str:
        """Run a single fallback-chain entry: official preset, community
        scraper, or a custom OpenAI-compatible endpoint."""
        slug = (entry.get('provider') or '').strip().lower()
        model = (entry.get('model') or '').strip()
        api_url = (entry.get('api_url') or '').strip()
        api_key = (entry.get('api_key') or '').strip()
        from api.llm.registry import is_official_slug
        if slug == 'qwen':
            return self._call_qwen_legacy(
                prompt, system_prompt=system_prompt, file_paths=file_paths,
                max_tokens=max_tokens, model_override=model or None,
            )
        if slug in ('k2think', 'poolside', 'motiftech', 'metaai'):
            return self._call_community_proxy(
                slug, prompt, system_prompt=system_prompt, file_paths=file_paths,
                max_tokens=max_tokens, model_override=model or None,
            )
        if slug in ('egov', 'deepai', 'inception'):
            return self._call_scraper_proxy(
                slug, prompt, system_prompt=system_prompt, file_paths=file_paths,
                max_tokens=max_tokens, model_override=model or None,
            )
        if slug == 'custom':
            if not api_url:
                raise WorkspaceError('Custom fallback entry requires an api_url')
            from api.llm.credentials import ResolvedProvider
            resolved = ResolvedProvider(
                slug='custom', label='Custom fallback', format='openai',
                base_url=api_url, api_key=api_key, model=model or '',
                context_window=131072, max_output_tokens=4096,
                source='bot', official=True,
            )
            return self._call_official_provider_stream(
                resolved, prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens,
            )
        if not is_official_slug(slug):
            raise WorkspaceError(f'Fallback provider {slug} is not supported by the agent runner')
        from api.llm.credentials import resolve as llm_resolve
        resolved = llm_resolve(self.session.admin_user, slug, model=model)
        if resolved is None:
            raise WorkspaceError(f'Fallback provider {slug} is not configured (no API key/URL)')
        if api_url:
            resolved.base_url = api_url
        if api_key:
            resolved.api_key = api_key
        return self._call_official_provider_stream(
            resolved, prompt, system_prompt=system_prompt, file_paths=file_paths, max_tokens=max_tokens,
        )

    # ------------------------------------------------------------------
    # Live streaming: official providers publish incremental deltas to
    # Redis pub/sub on `ba:stream:<session_id>`; the admin panel's SSE
    # endpoint relays them to the page. Fully best-effort — when Redis is
    # down the call still completes and the UI falls back to polling.
    # ------------------------------------------------------------------

    def _stream_redis(self):
        if self._stream_redis_client is None:
            client = None
            try:
                import redis
                url = (getattr(settings, 'BACKGROUND_AGENT_STREAM_REDIS', '') or '').strip() \
                    or (getattr(settings, 'CACHE_LOCATION', '') or '').strip()
                client = redis.Redis.from_url(url, socket_connect_timeout=2, socket_timeout=2, decode_responses=True) if url \
                    else redis.Redis(host='127.0.0.1', port=6379, db=0, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)
                client.ping()
            except Exception:
                client = None
            self._stream_redis_client = client
        return self._stream_redis_client

    def _publish_stream(self, kind: str, payload: dict):
        try:
            client = self._stream_redis()
            if client is None:
                return
            message = dict(payload or {})
            message['kind'] = kind
            client.publish(f'ba:stream:{self.session.id}', json.dumps(message, ensure_ascii=False))
        except Exception:
            pass

    def _call_community_proxy(self, slug: str, prompt: str, *, system_prompt: str, file_paths=None, max_tokens=None, model_override: str = None) -> str:
        """Community web proxies (k2think / poolside / motiftech / metaai) — no keys, no
        native file upload; new upload contents are inlined into the prompt."""
        if slug == 'k2think':
            from api import k2think_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'MBZUAI-IFM/K2-Think-v2'
            label = 'K2 Think'
            fn = k2think_proxy.simple_chat
        elif slug == 'motiftech':
            from api import motiftech_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'motif-102b'
            label = 'Motif'
            fn = motiftech_proxy.simple_chat
        elif slug == 'metaai':
            from api import metaai_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'metaai-instant'
            label = 'Meta AI'
            fn = metaai_proxy.simple_chat
        else:
            from api import poolside_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'laguna-s-2.1'
            label = 'Poolside'
            fn = poolside_proxy.simple_chat
        if file_paths:
            inline_files = self._attachments_inline_text(file_paths)
            if inline_files:
                prompt = prompt + '\n\n' + inline_files
        output_tokens = int(max_tokens or getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                t0 = time.monotonic()
                response = fn(
                    user_message=prompt,
                    model=model,
                    system_prompt=system_prompt,
                    max_tokens=output_tokens,
                )
                if t0:
                    self._last_model_response_ms = int((time.monotonic() - t0) * 1000)
                if response:
                    return str(response)
                raise WorkspaceError(f'{label} {model} returned an empty response')
            except (AgentPaused, AgentStopped):
                raise
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        raise WorkspaceError(
            f'{label} {model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    def _call_scraper_proxy(self, slug: str, prompt: str, *, system_prompt: str, file_paths=None, max_tokens=None, model_override: str = None) -> str:
        """Scraper proxies (egov / deepai / inception) — no keys, no native
        file upload; new upload contents are inlined into the prompt."""
        output_tokens = int(max_tokens or getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        if slug == 'egov':
            from api import egov_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'AI1'
            label = 'eGov'
            fn = lambda **kw: egov_proxy.simple_chat(max_tokens=output_tokens, **kw)
        elif slug == 'deepai':
            from api import deepai_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'standard'
            label = 'DeepAI'
            fn = deepai_proxy.simple_chat
        else:
            from api import inception_proxy
            model = model_override or (self.session.llm_model or '').strip() or 'mercury-2'
            label = 'Inception'
            fn = lambda **kw: inception_proxy.simple_chat(reasoning_effort='high', **kw)
        if file_paths:
            inline_files = self._attachments_inline_text(file_paths)
            if inline_files:
                prompt = prompt + '\n\n' + inline_files
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                t0 = time.monotonic()
                response = fn(
                    user_message=prompt,
                    model=model,
                    system_prompt=system_prompt,
                )
                if t0:
                    self._last_model_response_ms = int((time.monotonic() - t0) * 1000)
                if response:
                    return str(response)
                raise WorkspaceError(f'{label} {model} returned an empty response')
            except (AgentPaused, AgentStopped):
                raise
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        raise WorkspaceError(
            f'{label} {model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    def _call_official_provider_stream(self, resolved, prompt: str, *, system_prompt: str, file_paths=None, max_tokens=None) -> str:
        """Official API providers with live streaming: every reasoning/text
        delta is published to Redis pub/sub (`ba:stream:<session_id>`) so the
        admin panel renders the turn as it happens instead of after the fact.

        Same retry contract as the one-shot path; on success returns the full
        text exactly like `_call_official_provider`."""
        model = resolved.model
        label = resolved.label
        output_tokens = int(max_tokens or getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        output_tokens = min(output_tokens, resolved.max_output_tokens or output_tokens)
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        inline_files = self._attachments_inline_text(file_paths) if file_paths else ''
        if inline_files:
            prompt = prompt + '\n\n' + inline_files
        timeout = int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_TIMEOUT', 300))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                t0 = time.monotonic()
                text_parts: list = []
                reasoning_parts: list = []
                stream_meta: dict = {}
                for chunk in call_session_provider_stream(
                        self.session, resolved,
                        system_prompt=system_prompt, user_prompt=prompt,
                        max_tokens=output_tokens, timeout=timeout):
                    ctype = chunk.get('type')
                    if ctype == 'reasoning':
                        part = chunk.get('content') or ''
                        reasoning_parts.append(part)
                        self._publish_stream('thought', {'content': part})
                    elif ctype == 'text':
                        part = chunk.get('content') or ''
                        text_parts.append(part)
                        self._publish_stream('text', {'content': part})
                    elif ctype == 'done':
                        stream_meta = chunk
                text = ''.join(text_parts).strip()
                reasoning = ''.join(reasoning_parts).strip()
                if text:
                    self._pending_reasoning = reasoning
                    self._last_model_response_ms = int((time.monotonic() - t0) * 1000)
                    self._publish_stream('done', {
                        'model': stream_meta.get('model') or model,
                        'durationMs': self._last_model_response_ms,
                        'tokensIn': stream_meta.get('input_tokens') or 0,
                        'tokensOut': stream_meta.get('output_tokens') or 0,
                    })
                    return text
                raise WorkspaceError(f'{label} {model} returned an empty response')
            except (AgentPaused, AgentStopped):
                self._publish_stream('error', {'message': 'Agent paused mid-generation'})
                raise
            except LLMError as exc:
                last_error = exc
                if attempt >= attempts or not exc.retryable:
                    break
                delay = min(30, 2 ** attempt)
                self._publish_stream('error', {'message': f'{label} attempt {attempt} failed; retrying in {delay}s'})
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': resolved.slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': resolved.slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        self._publish_stream('error', {'message': f'{label} {model} failed after {attempts} attempt(s): {last_error}', 'fatal': True})
        raise WorkspaceError(
            f'{label} {model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    def _call_official_provider(self, resolved, prompt: str, *, system_prompt: str, file_paths=None, max_tokens=None) -> str:
        """Official API providers (Agnes, OpenAI, Claude, Gemini, DeepSeek,
        custom BYOK) — real request formats, real auth, no scraping.

        File attachments cannot be uploaded through these endpoints, so new
        upload contents are inlined into the prompt (Qwen keeps its native
        upload path on the legacy branch)."""
        model = resolved.model
        label = resolved.label
        output_tokens = int(max_tokens or getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        output_tokens = min(output_tokens, resolved.max_output_tokens or output_tokens)
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        inline_files = self._attachments_inline_text(file_paths) if file_paths else ''
        if inline_files:
            prompt = prompt + '\n\n' + inline_files
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                result = call_session_provider(
                    self.session, resolved,
                    system_prompt=system_prompt, user_prompt=prompt,
                    max_tokens=output_tokens,
                    timeout=int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_TIMEOUT', 300)),
                )
                self._last_model_response_ms = result.duration_ms
                if result and result.text:
                    self._pending_reasoning = (getattr(result, 'reasoning', '') or '').strip()
                    return result.text
                raise WorkspaceError(f'{label} {model} returned an empty response')
            except (AgentPaused, AgentStopped):
                raise
            except LLMError as exc:
                last_error = exc
                if attempt >= attempts or not exc.retryable:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': resolved.slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    break
                delay = min(30, 2 ** attempt)
                emit(self.session, 'model.retrying', f'{label} attempt {attempt} failed; retrying in {delay}s', {
                    'provider': resolved.slug, 'model': model,
                    'error': str(exc)[:1000], 'attempt': attempt,
                })
                for _ in range(delay):
                    time.sleep(1)
                    self._check_control()
        raise WorkspaceError(
            f'{label} {model} failed after {attempts} attempt(s): {last_error}'
        ) from last_error

    @staticmethod
    def _attachments_inline_text(file_paths, per_file_cap=12000, total_cap=60000) -> str:
        """Render newly uploaded files as fenced prompt text for providers
        without native upload. Returns '' when nothing readable is attached."""
        from pathlib import Path
        chunks = []
        total = 0
        for raw in file_paths or []:
            try:
                path = Path(str(raw))
                text = path.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            snippet = text[:per_file_cap]
            if len(text) > per_file_cap:
                snippet += f'\n[... truncated {len(text) - per_file_cap} chars ...]'
            block = f'═══ Attached file: {path.name} ═══\n{snippet}'
            if total + len(block) > total_cap:
                chunks.append('[... remaining attachments omitted this iteration ...]')
                break
            chunks.append(block)
            total += len(block)
        if not chunks:
            return ''
        return 'ATTACHED FILES (inline — this provider has no file upload)\n' + '\n\n'.join(chunks)

    def _call_qwen_legacy(self, prompt: str, *, system_prompt: str = SYSTEM_PROMPT, file_paths=None, max_tokens=None, model_override: str = None) -> str:
        model = model_override or self._community_model()
        thinking_mode = (self.session.llm_thinking_mode or 'auto').strip().lower()
        if thinking_mode not in ('auto', 'thinking', 'fast'):
            thinking_mode = 'auto'
        default_tokens = int(getattr(settings, 'BACKGROUND_AGENT_MODEL_MAX_TOKENS', 6000))
        if self._uses_qwen_harness():
            default_tokens = max(default_tokens, int(getattr(settings, 'BACKGROUND_AGENT_QWEN_MAX_TOKENS', 8192)))
        output_tokens = int(max_tokens or default_tokens)
        attempts = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_PROVIDER_ATTEMPTS', 3)), 6))
        last_error = None
        for attempt in range(1, attempts + 1):
            self._check_control()
            try:
                t0 = time.monotonic()
                response = qwen_proxy.call_qwen(
                    system_prompt=system_prompt,
                    user_message=prompt,
                    model=model,
                    max_tokens=output_tokens,
                    file_paths=file_paths or None,
                    thinking_mode=thinking_mode,
                )
                if t0:
                    self._last_model_response_ms = int((time.monotonic() - t0) * 1000)
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
Model: {self._llm_label()}

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
        try:
            state['todos'] = json.loads(self.session.todos_json or '[]')
        except (TypeError, json.JSONDecodeError):
            state['todos'] = []
        tree = ''
        if iteration == 1:
            tree_result = self.tools.list_files('.', depth=3, limit=600)
            tree = '\n'.join(tree_result['entries'])
        status = self.workspace.status()
        fixed = self._fixed_prompt(iteration, state, tree, status)
        if self.session.compact_requested_at:
            # Operator typed /compact — run the anchored compaction immediately,
            # regardless of the automatic threshold.
            compact_now(self.session, fixed, self._compact_call, manual=True)
            self.session.compact_requested_at = 0
            self.session.save(update_fields=['compact_requested_at'])
            try:
                state = json.loads(self.session.agent_state or '{}')
                state['todos'] = json.loads(self.session.todos_json or '[]')
            except (TypeError, json.JSONDecodeError):
                pass
        compact_if_needed(self.session, fixed, self._compact_call)
        qwen = self._uses_qwen_harness()
        snapshot = build_snapshot(
            self.session,
            fixed,
            format_message=render_hermes_transcript if qwen else None,
            rows_as_transcript=qwen,
        )
        self.session.context_tokens_estimate = snapshot.estimated_tokens
        self.session.context_window_tokens = snapshot.window_tokens
        self.session.save(update_fields=['context_tokens_estimate', 'context_window_tokens'])
        threshold_percent = round(snapshot.threshold_tokens * 100 / snapshot.window_tokens)
        accounting = (
            f'Estimated input: {snapshot.estimated_tokens} / {snapshot.window_tokens} tokens '
            f'({snapshot.percent}%).\nAutomatic anchored compaction runs at {threshold_percent}%.'
        )
        heal = '\n'.join(self._pending_heal)
        self._pending_heal = []
        if qwen:
            return build_user_prompt(fixed, snapshot.transcript, accounting, heal=heal)
        closer = (
            'Decide the next smallest set of high-value actions. Prefer edit_file/multi_edit over apply_patch. '
            'Return exactly one JSON object matching the required schema.'
        )
        if heal:
            closer = f'RECOVERY\n{heal}\n\n{closer}'
        return f"""{fixed}

ANCHORED CONTEXT AND RECENT CONVERSATION
{snapshot.transcript or '(none)'}

CONTEXT ACCOUNTING
{accounting}

{closer}
""".strip()

    def _complete(self, final: str):
        self._check_control()
        self._heartbeat(95, 'Building diff and downloadable artifacts')
        self._ensure_final_push()
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
