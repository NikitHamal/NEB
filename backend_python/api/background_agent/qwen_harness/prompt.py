"""Qwen-native system and turn prompts (official Nous / Hermes template)."""
from __future__ import annotations

import json

from api.background_agent.qwen_harness.catalog import tools_xml
from api.background_agent.qwen_harness.observe import compact_tool_content, wrap_tool_call, wrap_tool_response

FN_CALL_TEMPLATE = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tool_descs}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{{"name": <function-name>, "arguments": <args-json-object>}}
</tool_call>"""

ENGINEERING_RULES = """You are NEBians Background Agent, a senior autonomous software engineer in a real Git repository.
You do not have native API function calling. Use the <tool_call> protocol below — never invent a different envelope.

How to work:
- Inspect before you edit (list_files / glob_files / read_file / search_text). Preserve architecture, style, security and UX.
- Prefer edit_file / multi_edit. Copy old_text verbatim from read_file, with enough surrounding lines to be unique. write_file is for new files or full rewrites. Avoid apply_patch unless you must.
- Independent read-only tools in one turn run in parallel — batch reads and searches.
- Work only on the supplied task branch. Never switch, merge, reset, rebase, force-push or edit the default branch.
- Never read or expose secrets, .env files, credentials, SSH material, or paths outside the workspace.
- run_command takes an argv array only — no shell operators, pipes, redirection or substitution.
- Run the relevant tests / linters / type checks before calling done. Do not fabricate results.
- There is no iteration budget. Keep going until the goal is truly done, then call done. If you are blocked on a human decision, call ask_user with one question.
- For goals with more than ~3 steps, call update_plan first and keep exactly one item in_progress.
- Commit after each meaningful unit of work (conventional messages). Call git_push at most once, when finished.
- You may also call copy_file, move_file, create_directory, apply_patch, git_stage, git_pull or git_restore if needed. They are not listed above but are implemented.
- If a tool fails, change approach with the error in mind. Do not repeat the same failing call."""


def build_system_prompt(model_label: str = 'Qwen') -> str:
    identity = f'You are running through {model_label}.'
    return f'{ENGINEERING_RULES}\n\n{identity}\n\n{FN_CALL_TEMPLATE.format(tool_descs=tools_xml())}'.strip()


def _meta(message) -> dict:
    raw = getattr(message, 'metadata', None) or ''
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw or '{}')
    except (TypeError, json.JSONDecodeError):
        return {}


def render_hermes_transcript(rows, per_message_chars: int = 24000) -> str:
    blocks = []
    for message in rows:
        role = (getattr(message, 'role', '') or '').lower()
        content = getattr(message, 'content', '') or ''
        meta = _meta(message)
        if meta.get('kind') == 'model_prompt':
            continue
        if role == 'tool':
            name = meta.get('tool') or 'tool'
            arguments = meta.get('args') if isinstance(meta.get('args'), dict) else {}
            body = compact_tool_content(content, cap=min(per_message_chars, 8000))
            blocks.append(
                'ASSISTANT:\n' + wrap_tool_call(name, arguments)
                + '\nUSER:\n' + wrap_tool_response(body)
            )
            continue
        if len(content) > per_message_chars:
            content = content[:per_message_chars] + '\n[message truncated for context]'
        label = 'USER' if role == 'user' else 'ASSISTANT' if role == 'assistant' else role.upper()
        if role == 'system':
            continue
        blocks.append(f'{label}:\n{content}')
    return '\n\n'.join(blocks)


def build_user_prompt(fixed: str, transcript: str, accounting: str, heal: str = '') -> str:
    parts = [
        fixed.strip(),
        '',
        'ANCHORED CONTEXT AND RECENT CONVERSATION',
        transcript.strip() or '(none)',
        '',
        'CONTEXT ACCOUNTING',
        accounting.strip(),
    ]
    if heal.strip():
        parts.extend(['', 'RECOVERY', heal.strip()])
    parts.extend([
        '',
        'Decide the next smallest set of high-value actions. Prefer edit_file/multi_edit. '
        'Emit one or more <tool_call> blocks, or call done if the goal is complete. '
        'Do not wrap the tool calls in markdown fences. Do not emit a JSON envelope.',
    ])
    return '\n'.join(parts).strip()


def format_repair_prompt(original_prompt: str, prior_output: str) -> str:
    return f'''{original_prompt}

FORMAT REPAIR
Your prior response was not valid tool-call XML. Do not continue the task yet.
Convert the intended next step into one or more <tool_call> blocks using this exact shape:
<tool_call>
{{"name": "tool_name", "arguments": {{}}}}
</tool_call>
If the task is already complete, call done. If you need a human, call ask_user.
No markdown fences. No JSON envelope. No prose outside the tool calls.

PRIOR OUTPUT
{(prior_output or "")[:12000]}
'''


def json_repair_prompt(original_prompt: str, prior_output: str) -> str:
    return f'''{original_prompt}

FORMAT REPAIR
Your prior response did not match the required JSON protocol. Do not continue the task yet.
Convert the intended next step below into exactly one valid JSON object matching the system schema.
Do not use markdown fences or any text outside the JSON object.

PRIOR OUTPUT
{(prior_output or "")[:12000]}
'''
