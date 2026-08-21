import fnmatch
import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

MAX_FILE_READ_CHARS = 50000
MAX_OUTPUT_CHARS = 15000


def read_file(path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    path = path.strip().strip("'\"")
    if not os.path.exists(path):
        return f"Error: File '{path}' does not exist."
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        if start_line is not None or end_line is not None:
            try:
                s = max(1, int(start_line or 1)) - 1
                e = min(total_lines, int(end_line or total_lines))
            except Exception:
                s, e = 0, total_lines
            selected = lines[s:e]
            content = "".join(f"{i+s+1:4d} | {line}" for i, line in enumerate(selected))
            return f"File '{path}' (lines {s+1}-{e} of {total_lines}):\n{content}"
        
        full_text = "".join(lines)
        if len(full_text) > MAX_FILE_READ_CHARS:
            preview = "".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines[:300]))
            return f"File '{path}' ({total_lines} lines, showing first 300 lines due to length limit):\n{preview}\n... [file truncated, use start_line/end_line to read more]"
        
        content = "".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines))
        return f"File '{path}' ({total_lines} lines):\n{content}"
    except Exception as exc:
        return f"Error reading file '{path}': {exc}"


def write_file(path: str, content: str) -> str:
    path = path.strip().strip("'\"")
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        lines = len(content.splitlines())
        return f"Successfully wrote {len(content)} characters ({lines} lines) to '{path}'."
    except Exception as exc:
        return f"Error writing to file '{path}': {exc}"


def edit_file(path: str, old_str: str, new_str: str) -> str:
    path = path.strip().strip("'\"")
    if not os.path.exists(path):
        return f"Error: File '{path}' does not exist."
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        
        if old_str not in content:
            return f"Error: The target text to replace was not found in '{path}'. Please ensure exact matching including whitespace."
        
        occurrences = content.count(old_str)
        if occurrences > 1:
            return f"Warning: The target text occurs {occurrences} times in '{path}'. Please provide more surrounding context to make the match unique."
        
        updated = content.replace(old_str, new_str, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return f"Successfully updated '{path}' (replaced 1 occurrence)."
    except Exception as exc:
        return f"Error editing file '{path}': {exc}"


def list_dir(path: str = ".", max_depth: int = 2) -> str:
    path = path.strip().strip("'\"") or "."
    if not os.path.exists(path):
        return f"Error: Directory '{path}' does not exist."
    try:
        entries = []
        base_depth = len(os.path.abspath(path).split(os.sep))
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git", "build", "dist")]
            current_depth = len(os.path.abspath(root).split(os.sep)) - base_depth
            if current_depth > max_depth:
                continue
            indent = "  " * current_depth
            rel = os.path.relpath(root, path)
            if rel != ".":
                entries.append(f"{indent}{os.path.basename(root)}/")
            for f in sorted(files):
                if not f.startswith("."):
                    entries.append(f"{indent}  {f}")
            if len(entries) > 100:
                entries.append(f"... (truncated at 100 entries)")
                break
        return f"Directory listing for '{path}':\n" + "\n".join(entries) if entries else f"Directory '{path}' is empty."
    except Exception as exc:
        return f"Error listing directory '{path}': {exc}"


def grep_search(query: str, path: str = ".") -> str:
    query = query.strip()
    path = path.strip().strip("'\"") or "."
    matches = []
    try:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git", "build", "dist")]
            for f in files:
                if f.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".json", ".md", ".toml", ".yml", ".yaml", ".sh", ".ps1")):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                            for line_no, line in enumerate(file, 1):
                                if pattern.search(line):
                                    matches.append(f"{fpath}:{line_no}: {line.strip()[:150]}")
                                    if len(matches) >= 30:
                                        matches.append("... [results capped at 30 matches]")
                                        return "\n".join(matches)
                    except Exception:
                        pass
        return "\n".join(matches) if matches else f"No matches found for '{query}' in '{path}'."
    except Exception as exc:
        return f"Error performing grep search: {exc}"


def find_files(pattern: str, path: str = ".") -> str:
    pattern = pattern.strip()
    path = path.strip().strip("'\"") or "."
    results = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git", "build", "dist")]
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                results.append(os.path.join(root, f))
                if len(results) >= 50:
                    results.append("... [results capped at 50 files]")
                    return "\n".join(results)
    return "\n".join(results) if results else f"No files matching pattern '{pattern}' found."


def run_command(command: str, timeout: int = 60) -> str:
    command = command.strip()
    try:
        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        out = (res.stdout or "").strip()
        err = (res.stderr or "").strip()
        code = res.returncode
        result = []
        if out:
            result.append(f"STDOUT:\n{out}")
        if err:
            result.append(f"STDERR:\n{err}")
        result.append(f"(Exit code: {code})")
        full = "\n".join(result)
        if len(full) > MAX_OUTPUT_CHARS:
            full = full[:MAX_OUTPUT_CHARS] + "\n... [output truncated]"
        return full
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds."
    except Exception as exc:
        return f"Error executing command: {exc}"


def git_diff() -> str:
    return run_command("git diff", timeout=20)


TOOL_DEFINITIONS = """\
Available Tools:
1. read_file(path: str, start_line: Optional[int], end_line: Optional[int])
   Read contents of a file with line numbers.
2. write_file(path: str, content: str)
   Write/overwrite a full file.
3. edit_file(path: str, old_str: str, new_str: str)
   Replace exact text occurrence in a file.
4. list_dir(path: str = '.')
   List directory hierarchy.
5. grep_search(query: str, path: str = '.')
   Search for a pattern across code files.
6. find_files(pattern: str, path: str = '.')
   Find files matching glob pattern (e.g. '*.py').
7. run_command(command: str)
   Run a shell command (e.g. tests, linters, git).
8. ask_user(question: str, options: List[str], allow_custom: bool = True)
   Ask the user a multiple-choice question to confirm an action or resolve ambiguity.
9. spawn_subagent(role: str, task: str, context: Optional[str] = None)
   Delegate a subtask to a specialized subagent (roles: 'researcher', 'coder', 'reviewer', 'tester', 'planner').
10. inspect_image(path: str)
    Inspect image metadata, dimensions, and terminal preview.
11. done(summary: str)
    Mark task complete and summarize changes.
"""


def execute_tool_call(
    name: str,
    args: Dict[str, Any],
    session: Any = None,
    ui: Any = None,
) -> str:
    name = (name or "").strip().lower()
    if name == "read_file":
        return read_file(args.get("path", ""), args.get("start_line"), args.get("end_line"))
    elif name == "write_file":
        return write_file(args.get("path", ""), args.get("content", ""))
    elif name == "edit_file":
        return edit_file(args.get("path", ""), args.get("old_str", ""), args.get("new_str", ""))
    elif name == "list_dir":
        return list_dir(args.get("path", "."))
    elif name == "grep_search":
        return grep_search(args.get("query", ""), args.get("path", "."))
    elif name == "find_files":
        return find_files(args.get("pattern", "*"), args.get("path", "."))
    elif name == "run_command":
        return run_command(args.get("command", ""))
    elif name == "git_diff":
        return git_diff()
    elif name in ("ask_user", "ask_question"):
        from .interactive import ask_question_interactive
        question = args.get("question") or args.get("prompt") or "Please select an option:"
        options = args.get("options") or ["Yes", "No"]
        allow_custom = args.get("allow_custom", True)
        is_multi = args.get("is_multi_select", False)
        return ask_question_interactive(question, options, allow_custom, is_multi, ui=ui)
    elif name in ("spawn_subagent", "delegate_task", "invoke_subagent"):
        from .subagents import run_subagent
        role = args.get("role") or "researcher"
        task = args.get("task") or args.get("instruction") or ""
        ctx = args.get("context") or ""
        return run_subagent(role, task, ctx, parent_session=session, ui=ui)
    elif name in ("inspect_image", "read_image"):
        from .images import load_image_from_path, render_ascii_preview, format_image_description
        path = args.get("path") or args.get("file_path") or ""
        ok, msg, info = load_image_from_path(path)
        if not ok:
            return msg
        desc = format_image_description(info)
        preview = render_ascii_preview(info["path"])
        return f"{desc}\n{preview}"
    elif name in ("get_clipboard_image", "paste_clipboard_image"):
        from .images import grab_clipboard_image, format_image_description, render_ascii_preview
        ok, msg, info = grab_clipboard_image()
        if not ok:
            return msg
        if session and hasattr(session, "attach_image"):
            session.attach_image(info)
        desc = format_image_description(info)
        preview = render_ascii_preview(info["path"])
        return f"{desc}\n{preview}\n(Image attached to session context)"
    elif name == "done":
        return f"Task completed: {args.get('summary', 'Done')}"
    return f"Error: Tool '{name}' is not recognized."
