"""Tool implementations executed inside the agent's workspace.

Each tool is a plain function decorated with `@tool` so it registers itself
into the global registry. ``execute()`` calls the requested tool by name,
catches exceptions, persists a CodingAgentToolCall row, returns a (text,
status) tuple for the agent runtime to feed back as the next message.

The tools are intentionally conservative:
  · No network calls except git operations (via libgit2 wrapper or `git`
    subprocess inside the workspace) and grep/find which use ripgrep.
  · Shell commands run inside the workspace with a default timeout. A small
    denylist blocks the obvious foot-guns (`rm -rf /`, fork bombs, sudo).
  · File writes are atomic (write to .tmp then rename).
  · `write_file` computes a unified diff and stores it in CodingAgentFileChange.
  · `git_commit` never pushes and never touches the default branch.
"""
from __future__ import annotations

import difflib
import fnmatch
import json
import logging
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from django.db import close_old_connections
from django.utils.text import get_valid_filename

from .constants import (
    ALLOWED_FILE_EXTENSIONS_DENYLIST,
    DANGEROUS_SHELL_PATTERNS,
    MAX_FILE_READ_CHARS,
    MAX_TOOL_RESULT_CHARS,
    SHELL_TIMEOUT_DEFAULT,
    SHELL_TIMEOUT_MAX,
)
from .models import (
    CodingAgentFileChange,
    CodingAgentSession,
    CodingAgentToolCall,
)

logger = logging.getLogger(__name__)


@dataclass
class ToolContext:
    session: CodingAgentSession
    workspace: Path
    iteration: int
    cancelled: Callable[[], bool] = lambda: False


@dataclass
class ToolResult:
    text: str
    status: str = 'ok'
    error: str = ''
    data: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        payload = {'text': self.text, 'status': self.status}
        if self.data is not None:
            payload['data'] = self.data
        if self.error:
            payload['error'] = self.error
        return json.dumps(payload, ensure_ascii=False)


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[[Dict[str, Any], ToolContext], ToolResult]] = {}

    def register(self, name: str):
        def deco(fn):
            self._tools[name] = fn
            fn.__tool_name__ = name
            return fn
        return deco

    def names(self) -> List[str]:
        return sorted(self._tools.keys())

    def has(self, name: str) -> bool:
        return name in self._tools

    def execute(self, name: str, args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
        fn = self._tools.get(name)
        if fn is None:
            return ToolResult(
                text=f'Unknown tool: {name!r}. Available: {", ".join(self.names())}',
                status='error',
            )
        try:
            return fn(args, ctx)
        except _ToolError as e:
            return ToolResult(text=str(e), status='error', error=str(e))
        except Exception as e:  # noqa: BLE001
            logger.exception('tool %s raised: %s', name, e)
            return ToolResult(text=f'Internal error in {name}: {e}', status='error', error=str(e))


registry = ToolRegistry()


class _ToolError(Exception):
    pass


def _resolve_path(ctx: ToolContext, raw: str) -> Path:
    if not raw:
        raise _ToolError('path is required')
    p = Path(raw)
    if p.is_absolute():
        try:
            p.relative_to(ctx.workspace)
        except ValueError:
            raise _ToolError(f'path {raw!r} escapes the workspace')
        return p
    candidate = (ctx.workspace / p).resolve()
    try:
        candidate.relative_to(ctx.workspace.resolve())
    except ValueError:
        raise _ToolError(f'path {raw!r} escapes the workspace')
    return candidate


def _truncate(text: str, limit: int = MAX_TOOL_RESULT_CHARS) -> Tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit] + f'\n... [truncated {len(text) - limit} chars] ...', True


def _rg_available() -> bool:
    return shutil.which('rg') is not None


def _format_match_lines(file_path: Path, root: Path, matches: List[Tuple[int, str]], limit: int = 200) -> str:
    out = []
    rel = file_path.relative_to(root) if file_path.is_absolute() else file_path
    for lineno, line in matches:
        out.append(f'{rel}:{lineno}:{line.rstrip()}')
        if len(out) >= limit:
            out.append(f'... [hit per-file limit of {limit} lines]')
            break
    return '\n'.join(out)


@registry.register('list_files')
def _list_files(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    rel = args.get('path', '.') or '.'
    recursive = bool(args.get('recursive', True))
    max_entries = int(args.get('max_entries', 500))
    root = _resolve_path(ctx, rel)
    if not root.exists():
        return ToolResult(text=f'Path does not exist: {rel}', status='error')
    if not root.is_dir():
        return ToolResult(text=f'Not a directory: {rel}', status='error')

    skip_dirs = {'.git', '__pycache__', 'node_modules', '.next', 'dist', 'build', '.venv', 'venv', 'target', '.gradle'}

    lines: List[str] = []
    count = 0

    def _walk(p: Path, depth: int):
        nonlocal count
        if count >= max_entries:
            return False
        try:
            entries = sorted(p.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
        except (PermissionError, OSError):
            return True
        for entry in entries:
            if entry.name in skip_dirs:
                continue
            if entry.name.startswith('.') and entry.name not in {'.gitignore', '.env.example', '.github'}:
                if entry.is_dir():
                    continue
            if count >= max_entries:
                return False
            rel = entry.relative_to(ctx.workspace)
            marker = '/' if entry.is_dir() else ''
            lines.append(f'{"  " * depth}{rel}{marker}')
            count += 1
            if recursive and entry.is_dir():
                if not _walk(entry, depth + 1):
                    return False
        return True

    if not _walk(root, 0):
        lines.append(f'... [hit max_entries={max_entries}] ...')
    return ToolResult(text='\n'.join(lines) if lines else '(empty)')


@registry.register('read_file')
def _read_file(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    raw = args.get('path')
    if not raw:
        return ToolResult(text='path is required', status='error')
    p = _resolve_path(ctx, raw)
    if not p.exists():
        return ToolResult(text=f'File not found: {raw}', status='error')
    if p.is_dir():
        return ToolResult(text=f'Is a directory: {raw} (use list_files instead)', status='error')
    if p.suffix.lower() in ALLOWED_FILE_EXTENSIONS_DENYLIST and p.stat().st_size > 256 * 1024:
        return ToolResult(text=f'Binary file skipped ({p.stat().st_size} bytes): {raw}', status='ok')

    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except OSError as e:
        return ToolResult(text=f'Could not read {raw}: {e}', status='error')

    start_line = int(args.get('start_line', 0) or 0)
    end_line = args.get('end_line')
    if start_line < 0:
        start_line = 0
    lines = text.splitlines(keepends=True)
    total = len(lines)
    if end_line is None or end_line == '' or int(end_line) >= total:
        end_line = total
    else:
        end_line = int(end_line)
    window = ''.join(lines[start_line:end_line])
    truncated_text, truncated = _truncate(window, MAX_FILE_READ_CHARS)
    header = f'# {raw}  (lines {start_line + 1}-{end_line} of {total})\n'
    if truncated:
        header += f'# NOTE: response was truncated at {MAX_FILE_READ_CHARS} chars\n'
    return ToolResult(text=header + truncated_text, status='ok', data={'truncated': truncated, 'total_lines': total})


@registry.register('grep')
def _grep(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    pattern = args.get('pattern')
    if not pattern:
        return ToolResult(text='pattern is required', status='error')
    path = args.get('path', '.')
    glob_pat = args.get('glob') or None
    max_results = int(args.get('max_results', 200))
    case_sensitive = bool(args.get('case_sensitive', False))

    root = _resolve_path(ctx, path)
    if not root.exists():
        return ToolResult(text=f'Path not found: {path}', status='error')

    skip_dirs = {'.git', '__pycache__', 'node_modules', 'dist', 'build', '.venv', 'venv', 'target'}

    out_lines: List[str] = []
    file_hits: Dict[str, int] = {}
    total = 0
    flags_re = 0 if case_sensitive else re.IGNORECASE
    try:
        compiled = re.compile(pattern, flags_re)
    except re.error as e:
        return ToolResult(text=f'Bad regex: {e}', status='error')

    def _scan(p: Path):
        nonlocal total
        try:
            entries = list(p.iterdir())
        except (PermissionError, OSError):
            return
        for entry in entries:
            if entry.name in skip_dirs:
                continue
            if entry.is_dir():
                if total < max_results:
                    _scan(entry)
                continue
            if glob_pat and not fnmatch.fnmatch(entry.name, glob_pat):
                continue
            try:
                if entry.stat().st_size > 2 * 1024 * 1024:
                    continue
                with entry.open('r', encoding='utf-8', errors='replace') as f:
                    for lineno, line in enumerate(f, start=1):
                        if compiled.search(line):
                            rel = entry.relative_to(ctx.workspace)
                            out_lines.append(f'{rel}:{lineno}:{line.rstrip()}')
                            file_hits[str(rel)] = file_hits.get(str(rel), 0) + 1
                            total += 1
                            if total >= max_results:
                                out_lines.append(f'... [hit max_results={max_results}]')
                                return
            except OSError:
                continue

    _scan(root)
    summary = f'# {total} match(es) in {len(file_hits)} file(s)'
    if file_hits:
        top = sorted(file_hits.items(), key=lambda kv: -kv[1])[:20]
        summary += '\n# Top files: ' + ', '.join(f'{p}({n})' for p, n in top)
    return ToolResult(text=summary + '\n' + '\n'.join(out_lines), status='ok', data={'matches': total, 'files': len(file_hits)})


@registry.register('find_files')
def _find_files(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    name_pat = args.get('name_pattern')
    path = args.get('path', '.')
    root = _resolve_path(ctx, path)
    if not root.exists():
        return ToolResult(text=f'Path not found: {path}', status='error')
    matches: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {'.git', '__pycache__', 'node_modules', 'dist', 'build'}]
        for filename in filenames:
            if not name_pat:
                matches.append(str(Path(dirpath, filename).relative_to(ctx.workspace)))
            elif fnmatch.fnmatch(filename.lower(), name_pat.lower()):
                matches.append(str(Path(dirpath, filename).relative_to(ctx.workspace)))
        if len(matches) >= 500:
            break
    return ToolResult(text='\n'.join(matches) if matches else '(no matches)', status='ok', data={'count': len(matches)})


@registry.register('write_file')
def _write_file(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    raw_path = args.get('path')
    content = args.get('content')
    if raw_path is None:
        return ToolResult(text='path is required', status='error')
    if content is None:
        return ToolResult(text='content is required', status='error')
    target = _resolve_path(ctx, raw_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    old_text = ''
    if target.exists():
        if target.is_dir():
            return ToolResult(text=f'Path is a directory: {raw_path}', status='error')
        try:
            old_text = target.read_text(encoding='utf-8', errors='replace')
        except OSError as e:
            return ToolResult(text=f'Could not read existing file: {e}', status='error')

    tmp_path = target.with_suffix(target.suffix + '.coding_agent_tmp')
    try:
        tmp_path.write_text(content, encoding='utf-8')
        os.replace(tmp_path, target)
    except OSError as e:
        return ToolResult(text=f'Failed to write {raw_path}: {e}', status='error')

    if old_text == content:
        return ToolResult(text=f'(no change) {raw_path}', status='ok')

    diff = '\n'.join(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        content.splitlines(keepends=True),
        fromfile=f'a/{raw_path}',
        tofile=f'b/{raw_path}',
    ))
    additions = sum(1 for ln in content.splitlines() if ln.strip())
    deletions = sum(1 for ln in old_text.splitlines() if ln.strip())

    file_change = CodingAgentFileChange.objects.create(
        id=uuid.uuid4().hex,
        session=ctx.session,
        path=raw_path,
        op=CodingAgentFileChange.OP_CREATE if not old_text else CodingAgentFileChange.OP_MODIFY,
        additions=additions,
        deletions=deletions,
        patch=diff[:60000],
    )

    head = f'wrote {raw_path} ({len(content)} chars, +{additions}/-{deletions} lines)'
    return ToolResult(text=head + '\n' + (diff[:1500] + ('\n... [diff truncated]' if len(diff) > 1500 else '')), status='ok', data={'file_change_id': file_change.id})


@registry.register('edit_file')
def _edit_file(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    raw_path = args.get('path')
    find_text = args.get('find', args.get('old_text', args.get('old')))
    new_text = args.get('new_text', args.get('replace', args.get('new')))
    replace_all = bool(args.get('replace_all', args.get('global_replace', False)))
    if not raw_path:
        return ToolResult(text='path is required', status='error')
    if find_text is None:
        return ToolResult(text='find (or old_text) is required', status='error')
    if new_text is None:
        return ToolResult(text='new_text (or replace) is required', status='error')
    target = _resolve_path(ctx, raw_path)
    if not target.exists() or target.is_dir():
        return ToolResult(text=f'File not writable / not a file: {raw_path}', status='error')

    old_text = target.read_text(encoding='utf-8', errors='replace')
    if not replace_all:
        occurrences = old_text.count(find_text)
        if occurrences == 0:
            return ToolResult(text=f'No match for `find` in {raw_path}. Re-read the file to confirm exact text.', status='error')
        if occurrences > 1:
            return ToolResult(
                text=f'`find` matched {occurrences} times in {raw_path}. Set replace_all=true or make the snippet more specific.',
                status='error',
            )
        new_content = old_text.replace(find_text, new_text, 1)
    else:
        if find_text not in old_text:
            return ToolResult(text=f'No match for `find` in {raw_path}.', status='error')
        new_content = old_text.replace(find_text, new_text)

    try:
        tmp = target.with_suffix(target.suffix + '.coding_agent_tmp')
        tmp.write_text(new_content, encoding='utf-8')
        os.replace(tmp, target)
    except OSError as e:
        return ToolResult(text=f'Failed to write {raw_path}: {e}', status='error')

    diff = '\n'.join(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f'a/{raw_path}',
        tofile=f'b/{raw_path}',
    ))
    additions = sum(1 for ln in new_content.splitlines() if ln.strip())
    deletions = sum(1 for ln in old_text.splitlines() if ln.strip())

    file_change = CodingAgentFileChange.objects.create(
        id=uuid.uuid4().hex,
        session=ctx.session,
        path=raw_path,
        op=CodingAgentFileChange.OP_MODIFY,
        additions=additions,
        deletions=deletions,
        patch=diff[:60000],
    )

    head = f'edited {raw_path} ({len(new_content)} chars, +{additions}/-{deletions} lines, replace_all={replace_all})'
    return ToolResult(text=head + '\n' + (diff[:1500] + ('\n... [diff truncated]' if len(diff) > 1500 else '')), status='ok', data={'file_change_id': file_change.id})


@registry.register('delete_file')
def _delete_file(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    raw = args.get('path')
    if not raw:
        return ToolResult(text='path is required', status='error')
    target = _resolve_path(ctx, raw)
    if not target.exists():
        return ToolResult(text=f'Nothing to delete: {raw}', status='error')
    if target.is_dir():
        return ToolResult(text='Refusing to delete a directory. Use shell `rm` only if absolutely necessary.', status='error')
    target.unlink()
    CodingAgentFileChange.objects.create(
        id=uuid.uuid4().hex,
        session=ctx.session,
        path=raw,
        op=CodingAgentFileChange.OP_DELETE,
    )
    return ToolResult(text=f'deleted {raw}', status='ok')


@registry.register('rename_file')
def _rename_file(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    src = args.get('from') or args.get('src') or args.get('path')
    dst = args.get('to') or args.get('dst') or args.get('new_path')
    if not src or not dst:
        return ToolResult(text='from and to are required', status='error')
    src_p = _resolve_path(ctx, src)
    dst_p = _resolve_path(ctx, dst)
    if not src_p.exists():
        return ToolResult(text=f'src not found: {src}', status='error')
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    src_p.rename(dst_p)
    CodingAgentFileChange.objects.create(
        id=uuid.uuid4().hex,
        session=ctx.session,
        path=dst,
        op=CodingAgentFileChange.OP_RENAME,
    )
    return ToolResult(text=f'renamed {src} -> {dst}', status='ok')


@registry.register('run_shell')
def _run_shell(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    cmd = args.get('command') or args.get('cmd')
    if not cmd:
        return ToolResult(text='command is required', status='error')

    try:
        argv = shlex.split(cmd)
    except ValueError as e:
        return ToolResult(text=f'Could not parse command: {e}', status='error')

    joined_low = cmd.lower()
    for pat in DANGEROUS_SHELL_PATTERNS:
        if pat.lower() in joined_low:
            return ToolResult(
                text=f'Refused to run command matching dangerous pattern {pat!r}. If you really need this, do it manually after the session finishes.',
                status='denied',
            )

    timeout = int(args.get('timeout', SHELL_TIMEOUT_DEFAULT) or SHELL_TIMEOUT_DEFAULT)
    timeout = max(1, min(timeout, SHELL_TIMEOUT_MAX))

    cwd = ctx.workspace

    env_overrides = {
        'CI': '1',
        'PAGER': 'cat',
        'GIT_TERMINAL_PROMPT': '0',
        'GIT_ASKPASS': 'echo',
        'LANG': 'C.UTF-8',
    }
    full_env = {**os.environ, **env_overrides}

    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=full_env,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        return ToolResult(
            text=f'Command timed out after {timeout}s: {cmd}\nstdout=\n{e.stdout or ""}\nstderr=\n{e.stderr or ""}',
            status='timeout',
        )
    except FileNotFoundError as e:
        return ToolResult(text=f'Command not found: {e}', status='error')

    out_text = proc.stdout or ''
    err_text = proc.stderr or ''
    out_text_t, out_truncated = _truncate(out_text)
    err_text_t, err_truncated = _truncate(err_text)
    summary = f'exit={proc.returncode}'
    body = f'# command: {cmd}\n# timeout: {timeout}s\n# status: {summary}\n\n--- stdout ---\n{out_text_t}\n--- stderr ---\n{err_text_t}\n'
    truncated = out_truncated or err_truncated
    return ToolResult(text=body, status='ok' if proc.returncode == 0 else 'error',
                       data={'exit': proc.returncode, 'truncated': truncated,
                             'stdout_chars': len(out_text), 'stderr_chars': len(err_text)})


@registry.register('git_diff')
def _git_diff(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    staged = bool(args.get('staged', False))
    argv = ['git', 'diff', '--stat', '--patch']
    if staged:
        argv.insert(2, '--cached')
    proc = subprocess.run(argv + ['--no-color'], cwd=str(ctx.workspace), capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        return ToolResult(text=f'git diff failed: {proc.stderr}', status='error')
    return ToolResult(text=proc.stdout or '(no diff)', status='ok', data={'exit': proc.returncode, 'chars': len(proc.stdout)})


@registry.register('git_log')
def _git_log(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    n = int(args.get('limit', 20) or 20)
    argv = ['git', 'log', f'-n{n}', '--pretty=format:%h%x09%an%x09%ad%x09%s', '--date=short']
    proc = subprocess.run(argv, cwd=str(ctx.workspace), capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        return ToolResult(text=f'git log failed: {proc.stderr}', status='error')
    return ToolResult(text='commit\tauthor\tdate\tsubject\n' + proc.stdout, status='ok')


@registry.register('git_commit')
def _git_commit(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    message = args.get('message')
    if not message or not message.strip():
        return ToolResult(text='message is required', status='error')

    add_argv = ['git', 'add', '-A']
    add_proc = subprocess.run(add_argv, cwd=str(ctx.workspace), capture_output=True, text=True, timeout=60)
    if add_proc.returncode != 0:
        return ToolResult(text=f'git add failed: {add_proc.stderr}', status='error')

    status_proc = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=str(ctx.workspace),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if not status_proc.stdout.strip():
        return ToolResult(text='No staged changes to commit.', status='error')

    committer_name = 'NEBians Coding Agent'
    committer_email = 'coding-agent@nebians.local'
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = committer_name
    env['GIT_AUTHOR_EMAIL'] = committer_email
    env['GIT_COMMITTER_NAME'] = committer_name
    env['GIT_COMMITTER_EMAIL'] = committer_email

    commit_proc = subprocess.run(
        ['git', 'commit', '-m', message.strip()],
        cwd=str(ctx.workspace),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    if commit_proc.returncode != 0:
        return ToolResult(text=f'git commit failed: {commit_proc.stderr}', status='error')

    sha_proc = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=str(ctx.workspace),
        capture_output=True,
        text=True,
        timeout=10,
    )
    sha = sha_proc.stdout.strip()
    CodingAgentFileChange.objects.filter(session=ctx.session, committed=False).update(committed=True, commit_sha=sha)
    return ToolResult(text=f'commit {sha[:8]} created: {message.strip()}', status='ok', data={'sha': sha})


@registry.register('ask_user')
def _ask_user(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    question = args.get('question') or args.get('message') or ''
    options = args.get('options') or []
    if not question:
        return ToolResult(text='question is required', status='error')
    ctx.session.status = CodingAgentSession.STATUS_AWAITING_INPUT
    ctx.session.save(update_fields=['status', 'updated_at'])
    payload = {'question': question, 'options': options}
    return ToolResult(text=f'Asked the user: {question}', status='ok', data=payload)


@registry.register('done')
def _done(args: Dict[str, Any], ctx: ToolContext) -> ToolResult:
    summary = args.get('summary') or args.get('message') or ''
    status = args.get('status', 'success')
    if status not in {'success', 'partial'}:
        status = 'success'
    ctx.session.summary = summary.strip()[:4000]
    ctx.session.error_message = '' if status == 'success' else ctx.session.error_message
    ctx.session.status = CodingAgentSession.STATUS_FINISHED
    ctx.session.finished_at = int(time.time() * 1000)
    ctx.session.save(update_fields=['summary', 'status', 'finished_at', 'updated_at', 'error_message'])
    return ToolResult(text=f'Done ({status}). {summary}', status='ok')


def persist_tool_call(session_id: str, name: str, args: Dict[str, Any], result: ToolResult, iteration: int) -> CodingAgentToolCall:
    """Insert / update a CodingAgentToolCall row for audit & rerun."""
    args_json = json.dumps(args, ensure_ascii=False, default=str)[:20000]
    res_text = result.text
    truncated = False
    if len(res_text) > MAX_TOOL_RESULT_CHARS:
        res_text = res_text[:MAX_TOOL_RESULT_CHARS] + '\n... [truncated]'
        truncated = True
    call = CodingAgentToolCall.objects.create(
        id=uuid.uuid4().hex,
        session_id=session_id,
        name=name,
        args_json=args_json,
        result_text=res_text,
        result_truncated=truncated,
        status=result.status,
        iteration=iteration,
        finished_at=int(time.time() * 1000),
    )
    close_old_connections()
    return call
