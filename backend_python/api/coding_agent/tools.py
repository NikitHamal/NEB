"""File system and shell tools for the background coding agent.

Each tool function takes the workspace path and args dict, executes the
operation, and returns a result string. All tools are sandboxed to the
workspace directory — paths cannot escape it.
"""
import fnmatch
import os
import re
import subprocess
import logging

logger = logging.getLogger(__name__)

MAX_FILE_READ = 50000
MAX_FILE_WRITE = 200000
MAX_COMMAND_OUTPUT = 8000
MAX_LIST_ENTRIES = 200
MAX_SEARCH_RESULTS = 50
COMMAND_TIMEOUT = 120

SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    '.next', 'dist', 'build', '.tox', '.eggs', '.mypy_cache',
    '.pytest_cache', '.gradle', 'target', '.idea', '.vscode',
}
SKIP_EXTENSIONS = {
    '.pyc', '.pyo', '.so', '.dll', '.dylib', '.class',
    '.o', '.a', '.lib', '.exe', '.bin',
}
MAX_FILE_SIZE_LIST = 5 * 1024 * 1024


def _safe_path(workspace, relative_path):
    """Resolve a relative path within the workspace, preventing escape."""
    if not relative_path:
        relative_path = '.'
    relative_path = relative_path.lstrip('/')
    full = os.path.normpath(os.path.join(workspace, relative_path))
    workspace_norm = os.path.normpath(workspace)
    if not (full == workspace_norm or full.startswith(workspace_norm + os.sep)):
        return None
    return full


def tool_list_files(workspace, args):
    """List files and directories at a path."""
    path = args.get('path', '.')
    full = _safe_path(workspace, path)
    if full is None:
        return 'Error: path escapes workspace'
    if not os.path.exists(full):
        return f'Error: path does not exist: {path}'
    if not os.path.isdir(full):
        return f'Error: not a directory: {path}'
    
    entries = []
    try:
        for name in sorted(os.listdir(full)):
            if name in SKIP_DIRS:
                continue
            full_path = os.path.join(full, name)
            if os.path.isdir(full_path):
                entries.append(f'  {name}/')
            else:
                ext = os.path.splitext(name)[1]
                if ext in SKIP_EXTENSIONS:
                    continue
                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    size = 0
                if size > MAX_FILE_SIZE_LIST:
                    entries.append(f'  {name}  ({size // 1024}KB)')
                else:
                    entries.append(f'  {name}')
            if len(entries) >= MAX_LIST_ENTRIES:
                entries.append(f'  ... (truncated at {MAX_LIST_ENTRIES} entries)')
                break
    except PermissionError:
        return f'Error: permission denied: {path}'
    
    if not entries:
        return f'(empty directory: {path})'
    return f'Directory: {path}\n' + '\n'.join(entries)


def tool_read_file(workspace, args):
    """Read the content of a file."""
    path = args.get('path', '')
    if not path:
        return 'Error: path is required'
    full = _safe_path(workspace, path)
    if full is None:
        return 'Error: path escapes workspace'
    if not os.path.exists(full):
        return f'Error: file not found: {path}'
    if not os.path.isfile(full):
        return f'Error: not a file: {path}'
    try:
        size = os.path.getsize(full)
    except OSError:
        size = 0
    if size > MAX_FILE_READ:
        return f'Error: file too large ({size} bytes, max {MAX_FILE_READ}). Use search_files to find specific content.'
    try:
        with open(full, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        if len(content) > MAX_FILE_READ:
            content = content[:MAX_FILE_READ] + f'\n... (truncated at {MAX_FILE_READ} chars)'
        return f'File: {path} ({len(content)} chars)\n```\n{content}\n```'
    except Exception as e:
        return f'Error reading file: {e}'


def tool_write_file(workspace, args):
    """Write content to a file (creates or overwrites)."""
    path = args.get('path', '')
    content = args.get('content', '')
    if not path:
        return 'Error: path is required'
    full = _safe_path(workspace, path)
    if full is None:
        return 'Error: path escapes workspace'
    if len(content) > MAX_FILE_WRITE:
        return f'Error: content too large ({len(content)} chars, max {MAX_FILE_WRITE})'
    if os.path.basename(path) in SKIP_DIRS:
        return f'Error: cannot write to protected path: {path}'
    parent = os.path.dirname(full)
    if parent and not os.path.exists(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError as e:
            return f'Error creating directories: {e}'
    try:
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'File written: {path} ({len(content)} chars)'
    except Exception as e:
        return f'Error writing file: {e}'


def tool_edit_file(workspace, args):
    """Apply a targeted edit to an existing file."""
    path = args.get('path', '')
    old_string = args.get('old_string', '')
    new_string = args.get('new_string', '')
    if not path:
        return 'Error: path is required'
    if not old_string:
        return 'Error: old_string is required'
    full = _safe_path(workspace, path)
    if full is None:
        return 'Error: path escapes workspace'
    if not os.path.exists(full):
        return f'Error: file not found: {path}'
    try:
        with open(full, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return f'Error reading file: {e}'
    
    count = content.count(old_string)
    if count == 0:
        return f'Error: old_string not found in {path}. Make sure the string matches exactly.'
    if count > 1:
        return f'Error: old_string found {count} times in {path}. Provide more context to make it unique.'
    
    new_content = content.replace(old_string, new_string, 1)
    try:
        with open(full, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return f'File edited: {path} (replaced {len(old_string)} chars with {len(new_string)} chars)'
    except Exception as e:
        return f'Error writing file: {e}'


def tool_search_files(workspace, args):
    """Search for a pattern across files using regex."""
    pattern = args.get('pattern', '')
    search_path = args.get('path', '.')
    include_glob = args.get('include', '')
    if not pattern:
        return 'Error: pattern is required'
    full = _safe_path(workspace, search_path)
    if full is None:
        return 'Error: path escapes workspace'
    if not os.path.exists(full):
        return f'Error: path does not exist: {search_path}'
    
    try:
        regex = re.compile(pattern)
    except re.error as e:
        return f'Error: invalid regex: {e}'
    
    results = []
    file_count = 0
    for root, dirs, files in os.walk(full):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            ext = os.path.splitext(fname)[1]
            if ext in SKIP_EXTENSIONS:
                continue
            if include_glob and not fnmatch.fnmatch(fname, include_glob):
                continue
            fpath = os.path.join(root, fname)
            try:
                if os.path.getsize(fpath) > MAX_FILE_SIZE_LIST:
                    continue
            except OSError:
                continue
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            rel = os.path.relpath(fpath, workspace)
                            results.append(f'{rel}:{line_num}: {line.rstrip()[:200]}')
                            if len(results) >= MAX_SEARCH_RESULTS:
                                results.append(f'... (truncated at {MAX_SEARCH_RESULTS} results)')
                                return '\n'.join(results)
            except (OSError, UnicodeDecodeError):
                continue
            file_count += 1
            if file_count > 500:
                break
    
    if not results:
        return f'No matches found for pattern: {pattern}'
    return '\n'.join(results)


def tool_run_command(workspace, args):
    """Run a shell command in the workspace root."""
    command = args.get('command', '')
    timeout = min(args.get('timeout', COMMAND_TIMEOUT), COMMAND_TIMEOUT)
    if not command:
        return 'Error: command is required'
    
    dangerous = ['rm -rf /', 'mkfs', 'dd if=', '> /dev/sd', ':(){:|:&};:']
    for d in dangerous:
        if d in command:
            return f'Error: potentially dangerous command blocked: {d}'
    
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, 'CI': 'true'},
        )
        output = ''
        if proc.stdout:
            output += proc.stdout
        if proc.stderr:
            if output:
                output += '\n--- stderr ---\n'
            output += proc.stderr
        if len(output) > MAX_COMMAND_OUTPUT:
            output = output[:MAX_COMMAND_OUTPUT] + f'\n... (truncated at {MAX_COMMAND_OUTPUT} chars, exit code {proc.returncode})'
        prefix = f'Command: {command}\nExit code: {proc.returncode}\n'
        return prefix + (output or '(no output)')
    except subprocess.TimeoutExpired:
        return f'Command timed out after {timeout}s: {command}'
    except Exception as e:
        return f'Error running command: {e}'


def tool_git_diff(workspace, args):
    """Show git diff."""
    staged = args.get('staged', False)
    cmd = ['git', 'diff']
    if staged:
        cmd.append('--staged')
    try:
        proc = subprocess.run(
            cmd,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = proc.stdout or '(no changes)'
        if len(output) > MAX_COMMAND_OUTPUT:
            output = output[:MAX_COMMAND_OUTPUT] + f'\n... (truncated at {MAX_COMMAND_OUTPUT} chars)'
        return output
    except Exception as e:
        return f'Error: {e}'


def tool_git_status(workspace, args):
    """Show git status."""
    try:
        proc = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = proc.stdout.strip()
        if not output:
            return 'Working tree clean (no changes)'
        return output
    except Exception as e:
        return f'Error: {e}'


TOOL_FUNCTIONS = {
    'list_files': tool_list_files,
    'read_file': tool_read_file,
    'write_file': tool_write_file,
    'edit_file': tool_edit_file,
    'search_files': tool_search_files,
    'run_command': tool_run_command,
    'git_diff': tool_git_diff,
    'git_status': tool_git_status,
}

ACTION_TYPE_MAP = {
    'list_files': 'list',
    'read_file': 'read',
    'write_file': 'write',
    'edit_file': 'write',
    'search_files': 'search',
    'run_command': 'command',
    'git_diff': 'git',
    'git_status': 'git',
    'finish': 'status',
    'need_input': 'status',
}


def execute_tool(workspace, tool_name, args):
    """Execute a single tool and return (result_string, action_type, file_path, diff)."""
    if tool_name in ('finish', 'need_input'):
        return None, 'status', '', ''
    
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return f'Error: unknown tool: {tool_name}', 'status', '', ''
    
    if not isinstance(args, dict):
        args = {}
    
    file_path = ''
    diff = ''
    if tool_name in ('write_file', 'edit_file'):
        file_path = args.get('path', '')
    elif tool_name == 'read_file':
        file_path = args.get('path', '')
    elif tool_name == 'search_files':
        file_path = args.get('path', '')
    
    try:
        result = func(workspace, args)
        if tool_name == 'write_file' and file_path:
            try:
                proc = subprocess.run(
                    ['git', 'diff', '--stat', '--', file_path],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                diff = proc.stdout.strip()[:500]
            except Exception:
                pass
        elif tool_name == 'edit_file' and file_path:
            try:
                proc = subprocess.run(
                    ['git', 'diff', '--', file_path],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                diff = proc.stdout.strip()[:2000]
            except Exception:
                pass
        return result, ACTION_TYPE_MAP.get(tool_name, 'status'), file_path, diff
    except Exception as e:
        logger.exception('Tool %s failed: %s', tool_name, e)
        return f'Error: {e}', 'status', file_path, ''
