from __future__ import annotations

import fnmatch
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

IGNORED_DIRS = {
    '.git', '.hg', '.svn', '.idea', '.vscode', '.venv', 'venv', 'env',
    '__pycache__', 'node_modules', '.next', '.nuxt', '.cache', 'dist', 'build',
    'coverage', '.pytest_cache', '.mypy_cache', '.ruff_cache',
}
MAX_TREE_ENTRIES = 12000
MAX_SEARCH_MATCHES = 1200
MAX_FIND_FILES = 5000
MAX_READ_BYTES = 2_000_000


class WorkspaceError(RuntimeError):
    pass


class Workspace:
    def __init__(self, root: str | os.PathLike):
        self.root = Path(root).expanduser().resolve()
        if not self.root.is_dir():
            raise WorkspaceError(f'Workspace does not exist: {self.root}')

    def rel(self, path: str | os.PathLike = '.') -> Path:
        raw = str(path or '.').replace('\\', '/')
        candidate = (self.root / raw).resolve(strict=False)
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise WorkspaceError('Path is outside the workspace') from exc
        return candidate

    def display(self, path: Path) -> str:
        try:
            rel = path.resolve(strict=False).relative_to(self.root)
            return rel.as_posix() or '.'
        except ValueError:
            return str(path)

    def list_dir(self, path='.', include_hidden=True):
        target = self.rel(path)
        if not target.is_dir():
            raise WorkspaceError(f'Not a directory: {path}')
        entries = []
        for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            if not include_hidden and item.name.startswith('.'):
                continue
            stat = item.stat()
            entries.append({
                'name': item.name,
                'path': self.display(item),
                'type': 'dir' if item.is_dir() else 'file',
                'size': 0 if item.is_dir() else stat.st_size,
                'modified_ns': stat.st_mtime_ns,
            })
        return {'path': self.display(target), 'entries': entries}

    def tree(self, path='.', depth=4, include_hidden=False):
        start = self.rel(path)
        if not start.is_dir():
            raise WorkspaceError(f'Not a directory: {path}')
        depth = max(0, min(int(depth or 4), 12))
        entries = []

        def walk(folder: Path, level: int):
            if level > depth or len(entries) >= MAX_TREE_ENTRIES:
                return
            try:
                children = sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
            except OSError:
                return
            for item in children:
                if len(entries) >= MAX_TREE_ENTRIES:
                    return
                if item.name in IGNORED_DIRS:
                    continue
                if not include_hidden and item.name.startswith('.'):
                    continue
                try:
                    is_dir = item.is_dir()
                    size = 0 if is_dir else item.stat().st_size
                except OSError:
                    continue
                entries.append({
                    'name': item.name,
                    'path': self.display(item),
                    'type': 'dir' if is_dir else 'file',
                    'depth': level,
                    'size': size,
                })
                if is_dir:
                    walk(item, level + 1)

        walk(start, 0)
        return {'path': self.display(start), 'entries': entries, 'truncated': len(entries) >= MAX_TREE_ENTRIES}

    def read_file(self, path, start_line=1, end_line=0):
        target = self.rel(path)
        if not target.is_file():
            raise WorkspaceError(f'File not found: {path}')
        if target.stat().st_size > MAX_READ_BYTES:
            raise WorkspaceError(f'File is larger than {MAX_READ_BYTES} bytes')
        raw = target.read_bytes()
        if b'\x00' in raw[:8192]:
            raise WorkspaceError('Binary files cannot be opened in the text editor')
        text = raw.decode('utf-8', errors='replace')
        lines = text.splitlines(keepends=True)
        total = len(lines)
        start = max(1, int(start_line or 1))
        end = int(end_line or 0)
        end = total if end <= 0 else min(total, max(start, end))
        content = ''.join(lines[start - 1:end])
        return {
            'path': self.display(target),
            'content': content,
            'line_count': total,
            'start_line': start,
            'end_line': end,
            'size': len(raw),
        }

    def info(self, path):
        target = self.rel(path)
        if not target.exists():
            return {'path': self.display(target), 'exists': False}
        stat = target.stat()
        return {
            'path': self.display(target),
            'exists': True,
            'type': 'dir' if target.is_dir() else 'file',
            'size': 0 if target.is_dir() else stat.st_size,
            'modified_ns': stat.st_mtime_ns,
            'readonly': not os.access(target, os.W_OK),
        }

    def find_files(self, pattern='*', path='.', max_results=1000):
        start = self.rel(path)
        pattern = str(pattern or '*')
        cap = max(1, min(int(max_results or 1000), MAX_FIND_FILES))
        files = []
        for root, dirs, names in os.walk(start):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for name in names:
                full = Path(root) / name
                rel = self.display(full)
                if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern):
                    files.append(rel)
                    if len(files) >= cap:
                        return {'files': files, 'truncated': True}
        return {'files': files, 'truncated': False}

    def search_files(self, query, path='.', glob='*', regex=False, case_sensitive=False, max_results=400):
        query = str(query or '')
        if not query:
            raise WorkspaceError('Search query is required')
        start = self.rel(path)
        cap = max(1, min(int(max_results or 400), MAX_SEARCH_MATCHES))
        flags = 0 if case_sensitive else re.IGNORECASE
        rx = re.compile(query if regex else re.escape(query), flags)
        matches = []
        for root, dirs, names in os.walk(start):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for name in names:
                full = Path(root) / name
                rel = self.display(full)
                if glob and not (fnmatch.fnmatch(name, glob) or fnmatch.fnmatch(rel, glob)):
                    continue
                try:
                    if full.stat().st_size > MAX_READ_BYTES:
                        continue
                    raw = full.read_bytes()
                    if b'\x00' in raw[:8192]:
                        continue
                    text = raw.decode('utf-8', errors='replace')
                except OSError:
                    continue
                for line_no, line in enumerate(text.splitlines(), 1):
                    if rx.search(line):
                        matches.append({'path': rel, 'line': line_no, 'text': line[:1200]})
                        if len(matches) >= cap:
                            return {'matches': matches, 'truncated': True}
        return {'matches': matches, 'truncated': False}

    def write_file(self, path, content, create_parents=True):
        target = self.rel(path)
        if create_parents:
            target.parent.mkdir(parents=True, exist_ok=True)
        existed = target.exists()
        text = str(content or '')
        fd, temp_name = tempfile.mkstemp(prefix='.neby-', dir=str(target.parent))
        try:
            with os.fdopen(fd, 'w', encoding='utf-8', newline='') as stream:
                stream.write(text)
            os.replace(temp_name, target)
        except Exception:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise
        return {
            'path': self.display(target),
            'bytes': len(text.encode('utf-8')),
            'created': not existed,
            'summary': f'Wrote {self.display(target)}',
        }

    def append_file(self, path, content, create_parents=True):
        target = self.rel(path)
        if create_parents:
            target.parent.mkdir(parents=True, exist_ok=True)
        text = str(content or '')
        with target.open('a', encoding='utf-8', newline='') as stream:
            stream.write(text)
        return {'path': self.display(target), 'bytes': len(text.encode('utf-8')), 'summary': f'Appended {self.display(target)}'}

    def edit_file(self, path, old_text, new_text, replace_all=False):
        target = self.rel(path)
        if not target.is_file():
            raise WorkspaceError(f'File not found: {path}')
        text = target.read_text(encoding='utf-8')
        old = str(old_text or '')
        new = str(new_text or '')
        if not old:
            raise WorkspaceError('old_text is required')
        count = text.count(old)
        if count == 0:
            raise WorkspaceError('old_text was not found')
        if count > 1 and not replace_all:
            raise WorkspaceError(f'old_text matched {count} places; provide a more specific match or set replace_all')
        updated = text.replace(old, new, -1 if replace_all else 1)
        self.write_file(path, updated)
        changed = count if replace_all else 1
        return {'path': self.display(target), 'replacements': changed, 'summary': f'Edited {self.display(target)} ({changed} replacement{'' if changed == 1 else 's'})'}

    def apply_patch(self, patch):
        text = str(patch or '')
        if not text.strip():
            raise WorkspaceError('patch is required')
        proc = subprocess.run(
            ['git', 'apply', '--whitespace=nowarn', '-'],
            cwd=self.root,
            input=text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=90,
        )
        if proc.returncode != 0:
            raise WorkspaceError((proc.stderr or proc.stdout or 'git apply failed').strip()[:4000])
        return {'summary': 'Patch applied', 'stdout': proc.stdout[-4000:]}

    def mkdir(self, path):
        target = self.rel(path)
        target.mkdir(parents=True, exist_ok=True)
        return {'path': self.display(target), 'summary': f'Created {self.display(target)}'}

    def move(self, source, destination, overwrite=False):
        src = self.rel(source)
        dst = self.rel(destination)
        if not src.exists():
            raise WorkspaceError(f'Path not found: {source}')
        if dst.exists() and not overwrite:
            raise WorkspaceError(f'Destination already exists: {destination}')
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and overwrite:
            self.delete(destination, recursive=True)
        shutil.move(str(src), str(dst))
        return {'source': self.display(src), 'destination': self.display(dst), 'summary': f'Moved {source} to {destination}'}

    def delete(self, path, recursive=False):
        target = self.rel(path)
        if target == self.root:
            raise WorkspaceError('Cannot delete the workspace root')
        if not target.exists():
            return {'path': self.display(target), 'deleted': False, 'summary': f'{path} did not exist'}
        if target.is_dir():
            if recursive:
                shutil.rmtree(target)
            else:
                target.rmdir()
        else:
            target.unlink()
        return {'path': self.display(target), 'deleted': True, 'summary': f'Deleted {path}'}

    def git_status(self):
        text = self._git(['status', '--porcelain=v1', '--branch'])
        lines = text.splitlines()
        branch = ''
        changes = []
        for line in lines:
            if line.startswith('## '):
                branch = line[3:].split('...')[0].strip()
                continue
            if len(line) < 3:
                continue
            xy = line[:2]
            path = line[3:]
            if ' -> ' in path:
                path = path.split(' -> ', 1)[1]
            changes.append({'path': path, 'status': xy, 'kind': self._status_kind(xy)})
        return {'branch': branch, 'changes': changes, 'status_text': text}

    def git_diff(self, path='', staged=False, context=3):
        args = ['diff', f'--unified={max(0, min(int(context or 3), 20))}']
        if staged:
            args.append('--cached')
        if path:
            self.rel(path)
            args.extend(['--', path])
        patch = self._git(args, allow_exit=(0, 1))
        if path and not patch:
            info = self.git_status()
            item = next((x for x in info['changes'] if x['path'] == path), None)
            if item and '?' in item['status']:
                patch = self._git(['diff', '--no-index', '--', '/dev/null', path], allow_exit=(0, 1), windows_null=True)
        return {'path': path, 'patch': patch, 'staged': bool(staged)}

    def git_log(self, limit=30):
        cap = max(1, min(int(limit or 30), 200))
        text = self._git(['log', f'-{cap}', '--date=iso-strict', '--pretty=format:%h%x09%an%x09%ad%x09%s'])
        commits = []
        for line in text.splitlines():
            parts = line.split('\t', 3)
            if len(parts) == 4:
                commits.append({'hash': parts[0], 'author': parts[1], 'date': parts[2], 'subject': parts[3]})
        return {'commits': commits, 'log_text': text}

    def git_snapshot(self):
        try:
            root = self._git(['rev-parse', '--show-toplevel']).strip()
            branch = self._git(['branch', '--show-current']).strip()
            return {'git_root': root, 'git_branch': branch}
        except Exception:
            return {'git_root': '', 'git_branch': ''}

    def _git(self, args, allow_exit=(0,), windows_null=False):
        command = ['git', *args]
        if windows_null and os.name == 'nt':
            command = ['git', *[('NUL' if arg == '/dev/null' else arg) for arg in args]]
        proc = subprocess.run(
            command,
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60,
        )
        if proc.returncode not in allow_exit:
            raise WorkspaceError((proc.stderr or proc.stdout or 'git command failed').strip()[:4000])
        return proc.stdout

    @staticmethod
    def _status_kind(status):
        if '?' in status or 'A' in status:
            return 'new'
        if 'D' in status:
            return 'delete'
        if 'R' in status:
            return 'rename'
        return 'edit'
