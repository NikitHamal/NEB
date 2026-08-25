from __future__ import annotations

import re
import time

from django.conf import settings

from api import code_realtime as rt
from api.code_agent_prompt import READ_ONLY_TOOLS

TOOL_OUTPUT_CAP = int(getattr(settings, 'CODE_AGENT_TOOL_OUTPUT_CHARS', 12000))

TOOL_ACTIONS = {
    'list_dir': ('fs.list', 30),
    'read_file': ('fs.read', 30),
    'file_info': ('fs.info', 20),
    'find_files': ('fs.find', 45),
    'search_files': ('fs.search', 60),
    'write_file': ('fs.write', 60),
    'edit_file': ('fs.edit', 60),
    'append_file': ('fs.append', 60),
    'apply_patch': ('fs.patch', 90),
    'make_dirs': ('fs.mkdir', 30),
    'move_path': ('fs.move', 45),
    'delete_path': ('fs.delete', 45),
    'git_status': ('git.status', 30),
    'git_diff': ('git.diff', 45),
    'git_log': ('git.log', 30),
    'run_command': ('term.run', int(getattr(settings, 'CODE_AGENT_COMMAND_TIMEOUT', 1800))),
}

TOOL_ALIASES = {
    'list_files': 'list_dir',
    'ls': 'list_dir',
    'dir': 'list_dir',
    'list_directory': 'list_dir',
    'view_file': 'read_file',
    'cat': 'read_file',
    'open_file': 'read_file',
    'read': 'read_file',
    'get_file': 'read_file',
    'create_file': 'write_file',
    'save_file': 'write_file',
    'write': 'write_file',
    'str_replace': 'edit_file',
    'replace_file_content': 'edit_file',
    'multi_edit': 'edit_file',
    'modify_file': 'edit_file',
    'replace': 'edit_file',
    'edit': 'edit_file',
    'grep': 'search_files',
    'search_text': 'search_files',
    'find_text': 'search_files',
    'search': 'search_files',
    'grep_search': 'search_files',
    'glob_files': 'find_files',
    'glob': 'find_files',
    'locate_files': 'find_files',
    'find': 'find_files',
    'bash': 'run_command',
    'terminal': 'run_command',
    'execute_command': 'run_command',
    'exec': 'run_command',
    'sh': 'run_command',
    'cmd': 'run_command',
    'run': 'run_command',
    'diff': 'git_diff',
    'status': 'git_status',
    'log': 'git_log',
    'mkdir': 'make_dirs',
    'move': 'move_path',
    'rename': 'move_path',
    'delete': 'delete_path',
    'remove': 'delete_path',
    'rm': 'delete_path',
}

MUTATING_TOOLS = set(TOOL_ACTIONS) - READ_ONLY_TOOLS


def normalize_tool_and_args(tool: str, args: dict) -> tuple[str, dict]:
    raw_name = re.sub(r'[\s\-]+', '_', (tool or '').strip()).strip('_').lower()
    canonical_tool = TOOL_ALIASES.get(raw_name, raw_name)
    raw_args = dict(args if isinstance(args, dict) else {})
    clean_args = {}

    path_val = raw_args.get('path') or raw_args.get('file_path') or raw_args.get('filepath') or raw_args.get('target_file') or raw_args.get('file') or raw_args.get('directory') or raw_args.get('dir')
    if path_val is not None:
        clean_args['path'] = str(path_val)

    content_val = raw_args.get('content') or raw_args.get('text') or raw_args.get('code') or raw_args.get('body')
    if content_val is not None:
        clean_args['content'] = str(content_val)

    old_val = raw_args.get('old_text') or raw_args.get('old_str') or raw_args.get('target_content') or raw_args.get('find') or raw_args.get('target')
    if old_val is not None:
        clean_args['old_text'] = str(old_val)
    new_val = raw_args.get('new_text') or raw_args.get('new_str') or raw_args.get('replacement_content') or raw_args.get('replace') or raw_args.get('replacement')
    if new_val is not None:
        clean_args['new_text'] = str(new_val)

    cmd_val = raw_args.get('command') or raw_args.get('cmd') or raw_args.get('script')
    if cmd_val is None and 'argv' in raw_args:
        argv = raw_args['argv']
        cmd_val = ' '.join(str(x) for x in argv) if isinstance(argv, list) else str(argv)
    if cmd_val is not None:
        clean_args['command'] = str(cmd_val)

    query_val = raw_args.get('query') or raw_args.get('search') or raw_args.get('pattern') or raw_args.get('regex')
    if query_val is not None:
        if canonical_tool == 'find_files':
            clean_args['pattern'] = str(query_val)
        else:
            clean_args['query'] = str(query_val)

    for k, v in raw_args.items():
        if k not in clean_args and k not in ('tool', 'name', 'action', 'function'):
            clean_args[k] = v

    return canonical_tool, clean_args


def tool_allowed(tool: str, mode: str) -> bool:
    mode = (mode or 'agent').strip().lower()
    if mode == 'agent':
        return True
    return tool in READ_ONLY_TOOLS


def run_tool(user_id: str, session_id: str, tool: str, args: dict, mode: str) -> dict:
    tool, args = normalize_tool_and_args(tool, args)
    if tool == 'update_plan':
        return _plan_result(args)
    if not tool_allowed(tool, mode):
        return {
            'raw': {'ok': False, 'error': f'{tool} is disabled in {mode} mode'},
            'summary': f'{tool} skipped: {mode} mode is read-only',
            'duration_ms': 0,
        }
    spec = TOOL_ACTIONS.get(tool)
    if not spec:
        return {
            'raw': {'ok': False, 'error': f'unknown tool {tool}'},
            'summary': f'Unknown tool: {tool}',
            'duration_ms': 0,
        }
    action, timeout = spec
    args = dict(args or {})
    if tool == 'run_command':
        requested = int(args.get('timeout_sec') or 0)
        if requested > 0:
            timeout = min(max(requested + 15, 30), int(getattr(settings, 'CODE_AGENT_COMMAND_TIMEOUT', 1800)))
    started = time.monotonic()
    raw = rt.call_daemon(user_id, action, args, timeout=timeout, session_id=session_id)
    duration_ms = int((time.monotonic() - started) * 1000)
    return {
        'raw': raw,
        'summary': summarize_result(tool, args, raw, duration_ms),
        'duration_ms': duration_ms,
    }


def _plan_result(args: dict) -> dict:
    todos = []
    for item in (args.get('todos') or [])[:40]:
        if not isinstance(item, dict):
            continue
        content = str(item.get('content') or '').strip()[:400]
        if not content:
            continue
        status = str(item.get('status') or 'pending').strip().lower()
        if status not in ('pending', 'in_progress', 'completed'):
            status = 'pending'
        todos.append({'content': content, 'status': status})
    if not todos:
        return {'raw': {'ok': False, 'error': 'todos are required'}, 'summary': 'Plan update failed: no todos', 'duration_ms': 0}
    return {
        'raw': {'ok': True, 'data': {'todos': todos, 'explanation': str(args.get('explanation') or '')[:1000]}},
        'summary': f'Plan updated: {sum(1 for t in todos if t["status"] == "completed")}/{len(todos)} complete',
        'duration_ms': 0,
    }


def sanitize_args(args: dict) -> dict:
    clean = {}
    for key, value in (args or {}).items():
        if key in ('content', 'patch', 'old_text', 'new_text'):
            text = str(value)
            clean[key] = text[:4000] + ('…' if len(text) > 4000 else '')
        else:
            try:
                encoded = json.dumps(value, ensure_ascii=False)
                clean[key] = json.loads(encoded) if len(encoded) <= 4000 else encoded[:4000] + '…'
            except Exception:
                clean[key] = str(value)[:4000]
    return clean


def tool_label(tool: str, args: dict) -> str:
    target = (
        args.get('path') or args.get('source') or args.get('command') or
        args.get('query') or args.get('pattern') or ''
    )
    target = str(target)
    if len(target) > 72:
        target = target[:69] + '…'
    verbs = {
        'update_plan': 'Updating plan', 'list_dir': 'Listing', 'read_file': 'Reading',
        'file_info': 'Inspecting', 'find_files': 'Finding', 'search_files': 'Searching',
        'write_file': 'Writing', 'edit_file': 'Editing', 'append_file': 'Appending',
        'apply_patch': 'Applying patch', 'make_dirs': 'Creating', 'move_path': 'Moving',
        'delete_path': 'Deleting', 'git_status': 'Checking git status',
        'git_diff': 'Reading git diff', 'git_log': 'Reading git history',
        'run_command': 'Running',
    }
    base = verbs.get(tool, tool)
    return f'{base} {target}'.strip()


def result_preview(res: dict) -> str:
    if not isinstance(res, dict):
        return ''
    data = res.get('data')
    if isinstance(data, str):
        return data[:TOOL_OUTPUT_CAP]
    if not isinstance(data, dict):
        return ''
    for key in (
        'content', 'patch', 'output_tail', 'stdout_tail', 'stderr_tail',
        'matches_text', 'entries_text', 'status_text', 'log_text',
    ):
        value = data.get(key)
        if isinstance(value, str) and value:
            return value[:TOOL_OUTPUT_CAP]
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)[:TOOL_OUTPUT_CAP]
    except Exception:
        return str(data)[:TOOL_OUTPUT_CAP]


def summarize_result(tool: str, args: dict, res: dict, duration_ms: int) -> str:
    if not isinstance(res, dict) or not res.get('ok'):
        return f'{tool} failed: {(res or {}).get("error") or "unknown error"}'
    data = res.get('data') or {}
    if tool == 'run_command':
        if data.get('started'):
            return f'command started; streaming output to the terminal ({duration_ms}ms dispatch)'
        code = data.get('exit_code')
        tail = str(data.get('stdout_tail') or data.get('stderr_tail') or '').strip()
        return f'exit={code}, {duration_ms}ms' + (f'\n{tail[:1000]}' if tail else '')
    if tool == 'read_file':
        return f'read {data.get("line_count", len(str(data.get("content", "")).splitlines()))} lines from {args.get("path")}'
    if tool == 'list_dir':
        return f'{len(data.get("entries") or [])} entries in {args.get("path") or "."}'
    if tool in ('write_file', 'edit_file', 'append_file', 'apply_patch'):
        return str(data.get('summary') or f'{tool} completed')
    if tool == 'search_files':
        return f'{len(data.get("matches") or [])} matches'
    if tool == 'find_files':
        return f'{len(data.get("files") or [])} files found'
    if tool == 'git_status':
        return f'{len(data.get("changes") or [])} working tree changes'
    if tool == 'git_diff':
        return f'git diff returned {len(str(data.get("patch") or ""))} chars'
    return str(data.get('summary') or f'{tool} completed')
