import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .parser import parse_tool_calls
from .providers import stream_chat
from .session import Session
from .tools import execute_tool_call
from .ui import console

SUBAGENT_ROLES: Dict[str, Dict[str, Any]] = {
    "researcher": {
        "title": "Codebase Researcher",
        "description": "Explores codebase, searches symbols, inspects files, and summarizes architecture without modifying code.",
        "allowed_tools": ["read_file", "list_dir", "grep_search", "find_files", "done"],
        "max_steps": 8,
        "system_prompt": (
            "You are Neby Subagent: Researcher.\n"
            "Your objective is to thoroughly investigate and understand the codebase for the assigned task.\n"
            "Rules:\n"
            "- Use read_file, list_dir, grep_search, and find_files to gather facts.\n"
            "- NEVER edit or write files.\n"
            "- When you have enough context, call done(summary='...') with a complete, structured summary.\n"
        ),
    },
    "coder": {
        "title": "Precise Software Coder",
        "description": "Applies targeted code changes, creates new modules, and edits existing files accurately.",
        "allowed_tools": ["read_file", "write_file", "edit_file", "list_dir", "grep_search", "done"],
        "max_steps": 8,
        "system_prompt": (
            "You are Neby Subagent: Coder.\n"
            "Your objective is to implement the requested code changes accurately.\n"
            "Rules:\n"
            "- Always read existing files before editing.\n"
            "- Use edit_file for existing files (exact string replacements).\n"
            "- Use write_file only for new files.\n"
            "- Call done(summary='...') when modifications are complete.\n"
        ),
    },
    "reviewer": {
        "title": "Code Reviewer & Auditor",
        "description": "Audits git diffs and code files for bugs, security risks, regressions, and style issues.",
        "allowed_tools": ["read_file", "git_diff", "grep_search", "done"],
        "max_steps": 6,
        "system_prompt": (
            "You are Neby Subagent: Reviewer.\n"
            "Your objective is to inspect git diffs and modified code to verify correctness, security, and edge cases.\n"
            "Rules:\n"
            "- Check for syntax errors, unintended removals, and security issues.\n"
            "- Call done(summary='...') with your structured audit findings.\n"
        ),
    },
    "tester": {
        "title": "Test & Execution Runner",
        "description": "Runs test suites, linters, and verification commands, then reports test results.",
        "allowed_tools": ["run_command", "read_file", "done"],
        "max_steps": 6,
        "system_prompt": (
            "You are Neby Subagent: Tester.\n"
            "Your objective is to execute test commands and check runtime output.\n"
            "Rules:\n"
            "- Run relevant pytest, lint, or build commands using run_command.\n"
            "- If failures occur, inspect the error output and report clear diagnostic steps.\n"
            "- Call done(summary='...') when testing is complete.\n"
        ),
    },
    "planner": {
        "title": "System Architect & Planner",
        "description": "Breaks down complex requirements into sequenced implementation steps.",
        "allowed_tools": ["read_file", "list_dir", "grep_search", "done"],
        "max_steps": 5,
        "system_prompt": (
            "You are Neby Subagent: Planner.\n"
            "Your objective is to analyze requirements and generate a detailed, phased execution plan.\n"
            "Rules:\n"
            "- Explore existing code structure to ground the plan in reality.\n"
            "- Call done(summary='...') with numbered phases, dependencies, and risks.\n"
        ),
    },
}


def get_available_roles() -> List[Dict[str, str]]:
    return [
        {"role": k, "title": v["title"], "description": v["description"]}
        for k, v in SUBAGENT_ROLES.items()
    ]


def run_subagent(
    role: str,
    task: str,
    context: Optional[str] = None,
    parent_session: Optional[Session] = None,
    ui: Any = None,
    on_progress: Optional[Callable[[str], None]] = None,
) -> str:
    role = (role or "researcher").strip().lower()
    role_cfg = SUBAGENT_ROLES.get(role, SUBAGENT_ROLES["researcher"])

    cwd = parent_session.cwd if parent_session else "."
    provider = parent_session.provider if parent_session else "metaai"
    model = parent_session.model if parent_session else None

    sub_session = Session(provider=provider, model=model, cwd=cwd)

    tools_doc = "\n".join(f"- {t}" for t in role_cfg["allowed_tools"])
    sys_content = (
        f"{role_cfg['system_prompt']}\n"
        f"Workspace: {cwd}\n"
        f"Available Tools:\n{tools_doc}\n\n"
        f"Tool Format (YAML):\n"
        f"```tool\nname: <tool_name>\nargs:\n  <param>: <value>\n```\n"
    )
    sub_session.messages = [{"role": "system", "content": sys_content}]

    user_prompt = f"Task: {task}"
    if context:
        user_prompt += f"\n\nContext:\n{context}"
    sub_session.add_user_message(user_prompt)

    header_msg = f"[bold cyan]🤖 Subagent [{role.upper()}][/bold cyan] [dim]{task[:60]}[/dim]"
    if ui:
        ui.append_history(header_msg)
    elif on_progress:
        on_progress(header_msg)
    else:
        console.print(f"\n{header_msg}")

    max_steps = role_cfg["max_steps"]
    step = 0
    final_summary = ""
    start_time = time.time()

    while step < max_steps:
        step += 1
        accumulated_text = ""

        try:
            for chunk in stream_chat(
                sub_session.get_trimmed_messages(),
                provider=sub_session.provider,
                model=sub_session.model,
            ):
                ct = chunk.get("type")
                if ct == "text":
                    accumulated_text += chunk.get("content", "")
                elif ct == "error":
                    err = chunk.get("error", "Subagent stream error")
                    return f"Subagent error ({role}): {err}"
        except Exception as exc:
            return f"Subagent exception ({role}): {exc}"

        if not accumulated_text.strip():
            break

        clean_text, tool_calls = parse_tool_calls(accumulated_text)
        sub_session.add_assistant_message(accumulated_text)

        if not tool_calls:
            final_summary = clean_text or accumulated_text
            break

        is_done = False
        for call in tool_calls:
            tool_name = call.name.strip().lower()
            if tool_name not in role_cfg["allowed_tools"]:
                res = f"Error: Tool '{tool_name}' is not allowed for role '{role}'."
            elif tool_name == "done":
                final_summary = call.args.get("summary") or call.args.get("result") or clean_text
                is_done = True
                res = f"Subagent completed: {final_summary}"
            else:
                t0 = time.time()
                res = execute_tool_call(tool_name, call.args)
                td = time.time() - t0

                step_info = f"  [dim]└──[/dim] [cyan]{tool_name}[/cyan] [dim]({td:.1f}s)[/dim]"
                if ui:
                    ui.append_history(step_info)
                elif on_progress:
                    on_progress(step_info)
                else:
                    console.print(step_info)

            sub_session.add_tool_result(call.name, res)

        if is_done:
            break

    elapsed = time.time() - start_time
    if not final_summary:
        final_summary = clean_text.strip() or "Subagent completed assigned steps."

    finish_msg = f"[dim green]✓ Subagent [{role}] finished in {elapsed:.1f}s[/dim green]"
    if ui:
        ui.append_history(finish_msg)
    elif on_progress:
        on_progress(finish_msg)
    else:
        console.print(finish_msg)

    return f"[{role.upper()} RESULTS]\n{final_summary}"
