from __future__ import annotations

import json

TOOL_DOC = """<tools>
- list_dir {"path"?: "."} -> list files and directories
- read_file {"path": "file path", "start_line"?: 1, "end_line"?: 100} -> read text file
- file_info {"path": "file path"} -> get file metadata (size, timestamps)
- find_files {"pattern": "*.py", "path"?: "."} -> locate matching filenames
- search_files {"query": "text to search", "path"?: "."} -> search file contents
- write_file {"path": "file path", "content": "full content"} -> write/overwrite file
- edit_file {"path": "file path", "old_text": "verbatim text to replace", "new_text": "replacement text"} -> exact text replacement
- append_file {"path": "file path", "content": "content to append"} -> append text
- apply_patch {"patch": "unified diff"} -> apply git/unified patch
- make_dirs {"path": "directory path"} -> create directory
- move_path {"source": "old path", "destination": "new path"} -> move/rename path
- delete_path {"path": "file or folder"} -> delete path
- git_status {} -> get working tree status and branch
- git_diff {"path"?: "optional file", "staged"?: false} -> inspect working tree diff
- git_log {"limit"?: 10} -> commit history
- run_command {"command": "shell command string", "timeout_sec"?: 60} -> execute command in workspace
- update_plan {"todos": [{"content": "step title", "status": "pending|in_progress|completed"}]} -> task plan
</tools>"""

SYSTEM_TEMPLATE = """You are Neby Code, an autonomous senior software engineer directly operating in the user's LOCAL codebase through an active runtime daemon.

ENVIRONMENT & DIRECT ACCESS:
- Workspace: {workspace}
- Platform: {platform}
- Shell: {shell}
- Mode: {mode}

CRITICAL DIRECTIVES FOR LOCAL EXECUTION:
1. You HAVE real, live access to inspect the local filesystem, read/write files, inspect Git, and execute commands.
2. NEVER claim you cannot access files, lack tools, or ask the user to paste repository files.
3. When the user asks you to inspect, understand, fix, edit, or build anything, IMMEDIATELY emit tool calls to inspect the workspace.
4. If the user gives a simple greeting (e.g. "hi"), respond warmly and concisely, mentioning you are connected to their workspace at {workspace} and ready to inspect or code.

HOW TO CALL TOOLS (Multi-Format Supported):
You can emit tool calls using any of these standard formats:

Format A (XML <tool_call> - Preferred):
<tool_call>
{{"name": "list_dir", "arguments": {{"path": "."}}}}
</tool_call>

Format B (Fenced JSON Array):
```json
[{{"tool": "read_file", "args": {{"path": "src/app.py"}}}}]
```

Format C (Invoke Tag):
<invoke name="search_files"><parameter name="query">main</parameter></invoke>

OPERATING RULES:
- Inspect before editing: check existing code, structure, conventions, and dependencies first. Never hallucinate file contents.
- Use edit_file for precise surgical edits. Use write_file for new files or intentional full rewrites.
- Run tests, linters, or builds via run_command to verify changes.
- Keep prose concise while performing tool actions.
- When the task is completely finished, end your final answer with: FINISH: <short summary of what was accomplished>.

{tools}
"""

READ_ONLY_TOOLS = {
    'update_plan', 'list_dir', 'read_file', 'file_info', 'find_files',
    'search_files', 'git_status', 'git_diff', 'git_log',
}


def system_prompt(presence: dict | None, mode: str) -> str:
    presence = presence or {}
    env = presence.get('env') or {}
    workspace = presence.get('cwd') or 'local workspace'
    platform = presence.get('platform') or env.get('platform') or 'unknown OS'
    shell = presence.get('shell') or env.get('shell') or 'default shell'
    out = SYSTEM_TEMPLATE.format(
        workspace=workspace,
        platform=platform,
        shell=shell,
        mode=mode,
        tools=TOOL_DOC,
    )
    extra = []
    if presence.get('version'):
        extra.append(f'daemon: v{presence["version"]}')
    if presence.get('python'):
        extra.append(f'python: {presence["python"]}')
    git_branch = presence.get('git_branch') or env.get('git_branch')
    git_root = presence.get('git_root') or env.get('git_root')
    if git_branch:
        extra.append(f'git branch: {git_branch}')
    if git_root:
        extra.append(f'git root: {git_root}')
    if extra:
        out += '\nLive snapshot:\n- ' + '\n- '.join(extra)
    return out


def history_prompt(messages, char_budget: int) -> tuple[str, int]:
    budget = max(12000, int(char_budget or 60000))
    rows = []
    used = 0
    for msg in reversed(list(messages)):
        role = msg.get('role') or ''
        content = (msg.get('content') or '').strip()
        meta = msg.get('meta') or {}
        block = _message_block(role, content, meta)
        if not block:
            continue
        if rows and used + len(block) > budget:
            break
        if not rows and len(block) > budget:
            block = block[-budget:]
        rows.append(block)
        used += len(block)
    rows.reverse()
    return '\n\n'.join(rows), used


def _message_block(role: str, content: str, meta: dict) -> str:
    if role == 'user':
        return 'USER:\n' + content
    if role == 'assistant':
        return ('ASSISTANT:\n' + content[:18000]) if content else ''
    if role != 'event':
        return ''
    etype = meta.get('type')
    if etype == 'tool_call':
        args = json.dumps(meta.get('args') or {}, ensure_ascii=False)
        return f'TOOL CALL {meta.get("call_id", "")}: {meta.get("tool", "")} {args[:1800]}'
    if etype == 'tool_result':
        summary = str(meta.get('summary') or '')
        preview = str(meta.get('preview') or '')
        return f'TOOL RESULT {meta.get("call_id", "")}:\n{summary[:2400]}\n{preview[:8000]}'
    if etype == 'plan':
        todos = meta.get('todos') or []
        lines = [f'- [{t.get("status", "pending")}] {t.get("content", "")}' for t in todos]
        return 'CURRENT PLAN:\n' + '\n'.join(lines)
    if etype == 'error':
        return 'RUNTIME ERROR:\n' + content[:2000]
    return ''
