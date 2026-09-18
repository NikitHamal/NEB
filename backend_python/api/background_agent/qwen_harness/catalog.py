"""Qwen-native tool catalog (Hermes / Nous function schemas).

Alibaba's own guidance: keep the live tool set under ~20 and describe each
tool the way Qwen-Agent does — JSON Schema inside `<tools>`. Extra workspace
tools stay executable if the model names them, but they are not advertised.
"""
from __future__ import annotations

import json

READONLY_TOOLS = frozenset({
    'list_files', 'glob_files', 'read_file', 'search_text',
    'git_status', 'git_diff', 'git_log',
})

CONTROL_TOOLS = frozenset({'done', 'ask_user'})

HIDDEN_TOOLS = frozenset({
    'apply_patch', 'copy_file', 'move_file', 'create_directory',
    'git_stage', 'git_pull', 'git_restore', 'web_extractor',
})

_TOOLS: list[dict] = [
    {
        'name': 'list_files',
        'description': 'List files and directories under path. Prefer this for a first look at a folder.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string', 'description': 'Directory relative to the repo root. Default ".".'},
                'depth': {'type': 'integer', 'description': 'Max walk depth (1-8). Default 3.'},
                'limit': {'type': 'integer', 'description': 'Max entries to return. Default 500.'},
            },
        },
    },
    {
        'name': 'glob_files',
        'description': 'Find files by glob pattern (e.g. "**/*.py", "src/**/*.js"). Faster than listing everything.',
        'parameters': {
            'type': 'object',
            'properties': {
                'pattern': {'type': 'string', 'description': 'fnmatch-style pattern. ** matches across directories.'},
                'path': {'type': 'string', 'description': 'Directory to search from. Default ".".'},
                'limit': {'type': 'integer', 'description': 'Max matches. Default 200.'},
            },
            'required': ['pattern'],
        },
    },
    {
        'name': 'read_file',
        'description': 'Read a text file as numbered lines. Always read before editing. Use start_line/end_line for large files (windows of ~80-200 lines work best).',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string', 'description': 'File path relative to the repo root.'},
                'start_line': {'type': 'integer', 'description': '1-based start line. Default 1.'},
                'end_line': {'type': 'integer', 'description': '1-based inclusive end line. Default start+399.'},
            },
            'required': ['path'],
        },
    },
    {
        'name': 'search_text',
        'description': 'Search file contents. Default is a literal substring. Set regex=true for a Python regex. Optional glob limits which files are scanned.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'Literal text or regex.'},
                'path': {'type': 'string', 'description': 'File or directory to search. Default ".".'},
                'regex': {'type': 'boolean', 'description': 'Treat query as a regex. Default false.'},
                'glob': {'type': 'string', 'description': 'Optional file-name glob, e.g. "*.py".'},
                'limit': {'type': 'integer', 'description': 'Max matches. Default 100.'},
            },
            'required': ['query'],
        },
    },
    {
        'name': 'edit_file',
        'description': 'Surgical search-and-replace. old_text MUST be copied verbatim from read_file (including indentation). Prefer this over write_file and apply_patch.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'},
                'old_text': {'type': 'string', 'description': 'Exact existing block, unique in the file.'},
                'new_text': {'type': 'string', 'description': 'Replacement block.'},
                'replace_all': {'type': 'boolean', 'description': 'Replace every match. Default false.'},
            },
            'required': ['path', 'old_text', 'new_text'],
        },
    },
    {
        'name': 'multi_edit',
        'description': 'Apply several sequential old_text/new_text edits to one file. Use best_effort=true for large batches so one miss does not discard the rest.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'},
                'edits': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'old_text': {'type': 'string'},
                            'new_text': {'type': 'string'},
                            'replace_all': {'type': 'boolean'},
                        },
                        'required': ['old_text', 'new_text'],
                    },
                },
                'best_effort': {'type': 'boolean'},
            },
            'required': ['path', 'edits'],
        },
    },
    {
        'name': 'write_file',
        'description': 'Create a new file or fully rewrite an existing one. Do not use this to change a few lines — use edit_file.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'},
                'content': {'type': 'string', 'description': 'Complete file contents.'},
            },
            'required': ['path', 'content'],
        },
    },
    {
        'name': 'delete_file',
        'description': 'Delete a file or an empty directory. Never delete unless the task requires it.',
        'parameters': {
            'type': 'object',
            'properties': {'path': {'type': 'string'}},
            'required': ['path'],
        },
    },
    {
        'name': 'run_command',
        'description': 'Run a process as an argv array (no shell, no pipes, no redirection). Use for tests, linters, builds, compilers.',
        'parameters': {
            'type': 'object',
            'properties': {
                'argv': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Example: ["python", "-m", "pytest", "-q"]',
                },
                'cwd': {'type': 'string', 'description': 'Working directory. Default ".".'},
                'timeout': {'type': 'integer', 'description': 'Seconds. Default 300.'},
            },
            'required': ['argv'],
        },
    },
    {
        'name': 'update_plan',
        'description': 'Publish or refresh the live todo list. For any goal with more than ~3 steps, call this first. Exactly one item should be in_progress.',
        'parameters': {
            'type': 'object',
            'properties': {
                'todos': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'content': {'type': 'string'},
                            'status': {'type': 'string', 'enum': ['pending', 'in_progress', 'completed']},
                        },
                        'required': ['content', 'status'],
                    },
                },
                'explanation': {'type': 'string'},
            },
            'required': ['todos'],
        },
    },
    {
        'name': 'git_status',
        'description': 'Show branch and working-tree status.',
        'parameters': {'type': 'object', 'properties': {}},
    },
    {
        'name': 'git_diff',
        'description': 'Show the current task-branch diff against the base commit.',
        'parameters': {'type': 'object', 'properties': {}},
    },
    {
        'name': 'git_log',
        'description': 'Recent commits on the task branch.',
        'parameters': {
            'type': 'object',
            'properties': {'limit': {'type': 'integer', 'description': 'Default 20.'}},
        },
    },
    {
        'name': 'git_commit',
        'description': 'Stage safe changes and create a commit. Use a conventional message (fix:/feat:/refactor:). Call after each meaningful unit of work.',
        'parameters': {
            'type': 'object',
            'properties': {'message': {'type': 'string'}},
            'required': ['message'],
        },
    },
    {
        'name': 'git_push',
        'description': 'Push the task branch once, when the work is finished and validated. The server also pushes automatically on done.',
        'parameters': {
            'type': 'object',
            'properties': {'branch': {'type': 'string', 'description': 'Defaults to the task branch.'}},
        },
    },
    {
        'name': 'done',
        'description': 'Call only when the goal is genuinely complete and validated. Provide a concise summary of what changed and how you checked it.',
        'parameters': {
            'type': 'object',
            'properties': {
                'summary': {'type': 'string', 'description': 'What shipped and how it was validated.'},
            },
            'required': ['summary'],
        },
    },
    {
        'name': 'ask_user',
        'description': 'Pause and ask the operator a single blocking question. Use only when you cannot proceed safely.',
        'parameters': {
            'type': 'object',
            'properties': {'question': {'type': 'string'}},
            'required': ['question'],
        },
    },
]


def advertised_tools() -> list[dict]:
    return list(_TOOLS)


def tools_xml() -> str:
    lines = []
    for tool in _TOOLS:
        lines.append(json.dumps({
            'type': 'function',
            'function': {
                'name': tool['name'],
                'description': tool['description'],
                'parameters': tool.get('parameters') or {'type': 'object', 'properties': {}},
            },
        }, ensure_ascii=False))
    return '\n'.join(lines)


def is_readonly(tool: str) -> bool:
    return (tool or '').strip() in READONLY_TOOLS


def is_control(tool: str) -> bool:
    return (tool or '').strip() in CONTROL_TOOLS
