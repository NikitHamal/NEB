"""Per-run workspace and restricted code execution.

There is no Docker on this host, so containment is process-level: an import
hook blocks networking and dangerous modules, filesystem writes are confined
to the run's own directory, and a parent-side watchdog enforces wall-clock and
memory ceilings before killing the whole process tree.

This is a meaningful reduction in blast radius, not a security boundary. It is
appropriate for a public product where the agent runs model-generated code, but
it should be replaced by a container when the host supports one.
"""

import os
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time

from django.conf import settings

MAX_TIMEOUT = 120
DEFAULT_TIMEOUT = 30
DEFAULT_MEMORY_MB = 512
MAX_OUTPUT_CHARS = 12000
MAX_FILE_CHARS = 200000

# Networking, process spawning and low-level memory access. Deliberately NOT
# blocked: os, shutil, sys, importlib, platform — libraries legitimately import
# these, so they are confined at the call level instead (see _GUARD).
BLOCKED_MODULES = {
    'socket', 'ssl', 'urllib', 'urllib2', 'urllib3', 'http', 'httplib',
    'http.client', 'ftplib', 'smtplib', 'telnetlib', 'xmlrpc', 'requests',
    'curl_cffi', 'subprocess', 'multiprocessing', 'ctypes', 'webbrowser',
    'pty', 'pexpect', 'getpass', 'antigravity',
}

SHELL_ALLOWLIST = {
    'python': [sys.executable, '-I', '-B'],
    'python3': [sys.executable, '-I', '-B'],
    'node': ['node'],
    'npm': ['npm'],
    'pip': [sys.executable, '-m', 'pip'],
}

_DISALLOWED_SHELL_CHARS = re.compile(r'[|&;<>$`(){}!*?\[\]\\\'"]')


class SandboxError(Exception):
    """Raised for path escapes, blocked operations and execution failures."""


# --------------------------------------------------------------------------
# Workspace
# --------------------------------------------------------------------------

def workspace_root():
    return os.path.join(str(settings.MEDIA_ROOT), 'lazy_runs')


def workspace_path(run_id, create=True):
    root = workspace_root()
    path = os.path.abspath(os.path.join(root, str(run_id)))
    if create:
        os.makedirs(path, exist_ok=True)
    return path


def resolve_path(run_id, rel_path, must_exist=False):
    """Resolve a user/agent-supplied relative path inside the run workspace.

    Absolute paths, drive letters, `..` traversal and symlinks that escape the
    workspace are all rejected rather than clamped — a silent rewrite would hide
    the agent's mistake and let it believe a write landed somewhere it did not.
    """
    rel = str(rel_path or '').strip().replace('\\', '/')
    while rel.startswith('./'):
        rel = rel[2:]
    rel = rel.lstrip('/')
    if not rel:
        raise SandboxError('path is empty')
    if os.path.isabs(rel) or re.match(r'^[A-Za-z]:', rel):
        raise SandboxError('absolute paths are not allowed')
    if '..' in rel.split('/'):
        raise SandboxError('path traversal ("..") is not allowed')

    base = workspace_path(run_id)
    full = os.path.abspath(os.path.join(base, rel))
    if full != base and not full.startswith(base + os.sep):
        raise SandboxError('path escapes the run workspace')
    if os.path.islink(full):
        real = os.path.realpath(full)
        if real != base and not real.startswith(base + os.sep):
            raise SandboxError('symlink escapes the run workspace')
    if must_exist and not os.path.exists(full):
        raise SandboxError(f'no such file: {rel}')
    return full


def write_file(run_id, rel_path, content, mode='w'):
    full = resolve_path(run_id, rel_path)
    os.makedirs(os.path.dirname(full) or workspace_path(run_id), exist_ok=True)
    if isinstance(content, str):
        content = content.encode('utf-8')
    with open(full, 'wb') as handle:
        handle.write(content)
    return {'path': _rel(run_id, full), 'size': os.path.getsize(full)}


def read_file(run_id, rel_path, max_chars=MAX_FILE_CHARS):
    full = resolve_path(run_id, rel_path, must_exist=True)
    if os.path.getsize(full) > 4 * 1024 * 1024:
        raise SandboxError('file too large to read (>4MB)')
    try:
        with open(full, 'r', encoding='utf-8', errors='replace') as handle:
            text = handle.read(max_chars)
    except UnicodeDecodeError:
        raise SandboxError('binary file — cannot read as text')
    truncated = len(text) >= max_chars
    return {'path': _rel(run_id, full), 'text': text, 'truncated': truncated}


def list_files(run_id, prefix='', limit=200):
    base = workspace_path(run_id)
    scan = os.path.join(base, str(prefix or '').strip('/\\')) if prefix else base
    if not os.path.isdir(scan):
        raise SandboxError(f'not a directory: {prefix}')
    entries = []
    for root, dirs, files in os.walk(scan):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules')]
        for name in files:
            full = os.path.join(root, name)
            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0
            entries.append({'path': _rel(run_id, full), 'size': size})
            if len(entries) >= limit:
                return {'files': entries, 'truncated': True}
    entries.sort(key=lambda e: e['path'])
    return {'files': entries, 'truncated': False}


def delete_path(run_id, rel_path):
    full = resolve_path(run_id, rel_path, must_exist=True)
    if os.path.isdir(full):
        if full == workspace_path(run_id):
            raise SandboxError('refusing to delete the workspace root')
        import shutil
        shutil.rmtree(full)
    else:
        os.remove(full)
    return {'deleted': _rel(run_id, full)}


def _rel(run_id, full):
    return os.path.relpath(full, workspace_path(run_id)).replace('\\', '/')


# --------------------------------------------------------------------------
# Execution guard
# --------------------------------------------------------------------------

_GUARD = '''
import builtins as _b, os as _os, sys as _sys, importlib.abc as _abc

_ROOT = _os.path.abspath(_os.getcwd())
_BLOCKED = {mods!r}


class _Blocker(_abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in _BLOCKED:
            raise ImportError(
                'Blocked in the Lazy sandbox: %r is unavailable (networking, process '
                'spawning and low-level access are disabled).' % fullname.split('.')[0]
            )
        return None


_sys.meta_path.insert(0, _Blocker())


def _inside(p):
    p = _os.path.abspath(str(p))
    return p == _ROOT or p.startswith(_ROOT + _os.sep)


_real_open = _b.open


def _confined_open(file, mode='r', *a, **kw):
    m = str(mode)
    if any(ch in m for ch in ('w', 'a', 'x', '+')):
        if not _inside(file):
            raise PermissionError('Lazy sandbox: writes must stay inside the run workspace')
    return _real_open(file, mode, *a, **kw)


_b.open = _confined_open


def _confined(fn, label):
    def wrapper(p, *a, **kw):
        if not _inside(p):
            raise PermissionError('Lazy sandbox: %s escapes the run workspace' % label)
        return fn(p, *a, **kw)
    return wrapper


_os.remove = _confined(_os.remove, 'remove')
_os.rmdir = _confined(_os.rmdir, 'rmdir')
_os.rename = _confined(_os.rename, 'rename')
_os.mkdir = _confined(_os.mkdir, 'mkdir')
_os.makedirs = _confined(_os.makedirs, 'makedirs')

_real_chdir = _os.chdir


def _confined_chdir(p):
    if not _inside(p):
        raise PermissionError('Lazy sandbox: chdir escapes the run workspace')
    return _real_chdir(p)


_os.chdir = _confined_chdir

try:
    import shutil as _shutil

    def _confined_rmtree(p, *a, **kw):
        if not _inside(p):
            raise PermissionError('Lazy sandbox: rmtree escapes the run workspace')
        return _shutil._real_rmtree(p, *a, **kw)

    _shutil._real_rmtree = _shutil.rmtree
    _shutil.rmtree = _confined_rmtree
except Exception:
    pass
'''


def _guard_source():
    return _GUARD.format(mods=sorted(BLOCKED_MODULES))


def _kill_tree(proc):
    try:
        import psutil
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            try:
                child.kill()
            except Exception:
                pass
        parent.kill()
        return
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


def _enforce_limits(proc, timeout, memory_mb, state):
    """Parent-side watchdog: kills on wall-clock overrun or memory ceiling."""
    deadline = time.time() + timeout
    try:
        import psutil
        handle = psutil.Process(proc.pid)
    except Exception:
        handle = None

    while time.time() < deadline:
        if proc.poll() is not None:
            return
        if handle is not None:
            try:
                rss = 0
                for child in [handle] + handle.children(recursive=True):
                    try:
                        rss += child.memory_info().rss
                    except Exception:
                        pass
                if rss > memory_mb * 1024 * 1024:
                    state['reason'] = f'memory limit exceeded ({rss // (1024 * 1024)}MB > {memory_mb}MB)'
                    _kill_tree(proc)
                    return
            except Exception:
                pass
        time.sleep(0.25)

    if proc.poll() is None:
        state['reason'] = f'time limit exceeded ({timeout}s)'
        _kill_tree(proc)


def run_python(run_id, code, timeout=DEFAULT_TIMEOUT, memory_mb=DEFAULT_MEMORY_MB, filename='_snippet.py'):
    """Execute agent-authored Python inside the guarded workspace."""
    code = code or ''
    if not code.strip():
        raise SandboxError('no code provided')

    try:
        timeout = max(1, min(MAX_TIMEOUT, int(timeout)))
    except Exception:
        timeout = DEFAULT_TIMEOUT
    try:
        memory_mb = max(64, min(2048, int(memory_mb)))
    except Exception:
        memory_mb = DEFAULT_MEMORY_MB

    base = workspace_path(run_id)
    script_path = os.path.join(base, filename.lstrip('/\\') or '_snippet.py')
    with open(script_path, 'w', encoding='utf-8') as handle:
        handle.write(_guard_source() + '\n' + code)

    env = dict(os.environ)
    for key in list(env):
        if key.lower().startswith(('http_proxy', 'https_proxy', 'all_proxy', 'no_proxy')):
            env.pop(key, None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONHASHSEED'] = '0'
    env['MPLBACKEND'] = 'Agg'
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONSTARTUP', None)

    started = time.time()
    state = {'reason': ''}
    try:
        proc = subprocess.Popen(
            [sys.executable, '-I', '-B', script_path],
            cwd=base, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True, encoding='utf-8', errors='replace',
        )
    except Exception as exc:
        raise SandboxError(f'could not start interpreter: {exc}')

    watcher = threading.Thread(
        target=_enforce_limits, args=(proc, timeout, memory_mb, state), daemon=True,
    )
    watcher.start()
    try:
        out, err = proc.communicate(timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        out, err = '', 'execution watchdog terminated the process'
    finally:
        watcher.join(timeout=2)

    elapsed = int((time.time() - started) * 1000)
    out = (out or '')[:MAX_OUTPUT_CHARS]
    err = (err or '')[:MAX_OUTPUT_CHARS]
    if state['reason']:
        err = (err + f"\n[{state['reason']}]").strip()

    # Surface the traceback line the agent actually needs, relative to its code.
    if err and 'Traceback' in err:
        err = err.replace(script_path, filename)

    return {
        'ok': proc.returncode == 0 and not state['reason'],
        'exitCode': proc.returncode,
        'stdout': out,
        'stderr': err,
        'elapsedMs': elapsed,
        'timedOut': bool(state['reason']),
    }


def run_shell(run_id, command, timeout=DEFAULT_TIMEOUT, memory_mb=DEFAULT_MEMORY_MB):
    """Run an allowlisted command. No shell interpreter is ever involved."""
    command = (command or '').strip()
    if not command:
        raise SandboxError('no command provided')
    if _DISALLOWED_SHELL_CHARS.search(command):
        raise SandboxError(
            'shell metacharacters are not allowed; use run_python for anything complex'
        )

    try:
        argv = shlex.split(command)
    except ValueError as exc:
        raise SandboxError(f'unparseable command: {exc}')

    program = os.path.basename(argv[0]).lower()
    if program.endswith('.exe'):
        program = program[:-4]
    prefix = SHELL_ALLOWLIST.get(program)
    if not prefix:
        raise SandboxError(
            f'command {program!r} is not allowed; permitted: {", ".join(sorted(SHELL_ALLOWLIST))}'
        )

    rest = argv[1:]
    if program == 'python':
        # Route python back through the guarded runner so limits still apply.
        paths = [a for a in rest if not a.startswith('-')]
        if paths:
            source = resolve_path(run_id, paths[0], must_exist=True)
            with open(source, 'r', encoding='utf-8', errors='replace') as handle:
                return run_python(run_id, handle.read(), timeout=timeout, memory_mb=memory_mb)
        raise SandboxError('python needs a script file to run')

    try:
        timeout = max(1, min(MAX_TIMEOUT, int(timeout)))
    except Exception:
        timeout = DEFAULT_TIMEOUT

    base = workspace_path(run_id)
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env.pop('PYTHONPATH', None)

    started = time.time()
    try:
        proc = subprocess.Popen(
            prefix + rest, cwd=base, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True, encoding='utf-8', errors='replace',
        )
    except FileNotFoundError:
        raise SandboxError(f'{program} is not installed on this server')
    except Exception as exc:
        raise SandboxError(f'could not start {program}: {exc}')

    state = {'reason': ''}
    watcher = threading.Thread(
        target=_enforce_limits, args=(proc, timeout, memory_mb, state), daemon=True,
    )
    watcher.start()
    try:
        out, err = proc.communicate(timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        out, err = '', f'time limit exceeded ({timeout}s)'
    finally:
        watcher.join(timeout=2)

    if state['reason']:
        err = (err or '') + f"\n[{state['reason']}]"

    return {
        'ok': proc.returncode == 0,
        'exitCode': proc.returncode,
        'stdout': (out or '')[:MAX_OUTPUT_CHARS],
        'stderr': (err or '')[:MAX_OUTPUT_CHARS],
        'elapsedMs': int((time.time() - started) * 1000),
    }


def export_bundle(run_id, paths=None, name='bundle'):
    """Zip part or all of the workspace into a downloadable archive."""
    import zipfile
    base = workspace_path(run_id)
    safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', str(name or 'bundle'))[:60] or 'bundle'
    out_path = os.path.join(base, f'{safe_name}.zip')

    if paths:
        targets = [resolve_path(run_id, p, must_exist=True) for p in paths]
    else:
        targets = [base]

    count = 0
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for target in targets:
            if os.path.isfile(target):
                zf.write(target, os.path.relpath(target, base))
                count += 1
                continue
            for root, dirs, files in os.walk(target):
                dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules')]
                for fname in files:
                    full = os.path.join(root, fname)
                    if full == out_path:
                        continue
                    zf.write(full, os.path.relpath(full, base))
                    count += 1
    return {'path': f'{safe_name}.zip', 'files': count, 'size': os.path.getsize(out_path)}
