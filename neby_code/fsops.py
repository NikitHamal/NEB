"""Safe filesystem operations, confined to the workspace root."""
import fnmatch
import json
import os
import re
import shutil
import sys

IGNORED_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.idea',
                '.gradle', 'build', 'dist', '.next', '.cache', 'vendor'}
MAX_READ = 400000
TEXT_EXTS = {'.txt', '.md', '.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.json',
             '.css', '.scss', '.html', '.xml', '.yml', '.yaml', '.toml', '.ini', '.cfg',
             '.sh', '.bat', '.ps1', '.java', '.kt', '.kts', '.c', '.h', '.cpp', '.hpp',
             '.cs', '.go', '.rs', '.rb', '.php', '.sql', '.env', '.gitignore', '.csv'}
BINARY_CAP = 200000


class FsError(Exception):
    pass


class Workspace:
    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        if not os.path.isdir(self.root):
            raise FsError(f'workspace does not exist: {self.root}')

    def resolve(self, rel: str) -> str:
        if not rel or str(rel).strip() in ('.', '', '/'):
            return self.root
        p = os.path.abspath(os.path.join(self.root, str(rel)))
        if not (p == self.root or p.startswith(self.root + os.sep)):
            raise FsError(f'path escapes workspace: {rel}')
        return p

    # ---------------------------------------------------------------- read ops

    def list_dir(self, rel: str = '.') -> dict:
        path = self.resolve(rel)
        if not os.path.isdir(path):
            raise FsError(f'not a directory: {rel}')
        entries = []
        try:
            names = sorted(os.listdir(path), key=lambda n: (not os.path.isdir(os.path.join(path, n)), n.lower()))
        except PermissionError:
            raise FsError(f'permission denied: {rel}')
        for name in names[:500]:
            full = os.path.join(path, name)
            try:
                st = os.stat(full)
                entries.append({
                    'name': name,
                    'is_dir': os.path.isdir(full),
                    'size': st.st_size if os.path.isfile(full) else 0,
                    'modified_ms': int(st.st_mtime * 1000),
                })
            except OSError:  # noqa: PERF203
                continue
        return {'entries': entries}

    def tree(self, depth: int = 3) -> dict:
        return {'tree': self._tree('.', max(1, min(int(depth), 4)))}

    def _tree(self, rel: str, depth: int) -> list:
        if depth <= 0:
            return []
        out = []
        try:
            entries = self.list_dir(rel)['entries']
        except FsError:
            return out
        for e in entries[:80]:
            node = {'name': e['name'], 'path': f"{rel}/{e['name']}".replace('\\', '/'),
                    'is_dir': e['is_dir']}
            if e['is_dir']:
                if e['name'] in IGNORED_DIRS:
                    continue
                node['children'] = self._tree(node['path'], depth - 1)
            out.append(node)
        return out

    def read_file(self, rel: str, start_line=None, end_line=None) -> dict:
        path = self.resolve(rel)
        if not os.path.isfile(path):
            raise FsError(f'not a file: {rel}')
        size = os.path.getsize(path)
        ext = os.path.splitext(path)[1].lower()
        if size > MAX_READ * 3 and ext not in TEXT_EXTS:
            raise FsError(f'file too large / binary: {rel} ({size} bytes)')
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read(MAX_READ + BINARY_CAP)
        truncated = len(content) >= MAX_READ + BINARY_CAP
        lines = None
        if start_line is not None or end_line is not None:
            all_lines = content.splitlines()
            s = max(1, int(start_line or 1))
            e = min(len(all_lines), int(end_line or len(all_lines)))
            content = '\n'.join(all_lines[s - 1:e])
            lines = [s, e]
        return {'content': content, 'size': size, 'truncated': truncated, 'range': lines}

    def search_files(self, query: str, rel: str = '.', max_results: int = 60) -> dict:
        pattern = re.compile(re.escape(query), re.IGNORECASE) if query else None
        if pattern is None:
            raise FsError('empty query')
        base = self.resolve(rel)
        matches = []
        scanned = 0
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
            for fname in filenames:
                if len(matches) >= max_results:
                    break
                full = os.path.join(dirpath, fname)
                ext = os.path.splitext(fname)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
                           '.jar', '.exe', '.dll', '.so', '.dylib', '.woff', '.woff2'):
                    continue
                if os.path.getsize(full) > BINARY_CAP:
                    continue
                try:
                    with open(full, 'r', encoding='utf-8', errors='ignore') as fh:
                        for lineno, line in enumerate(fh, 1):
                            scanned += 1
                            if pattern.search(line):
                                matches.append({
                                    'path': os.path.relpath(full, self.root).replace('\\', '/'),
                                    'line': lineno,
                                    'text': line.strip()[:240],
                                })
                                if len(matches) >= max_results:
                                    break
                except OSError:
                    continue
                if len(matches) >= max_results:
                    break
        return {'matches': matches, 'scanned_lines': scanned}

    # ---------------------------------------------------------------- write ops

    def write_file(self, rel: str, content: str = '') -> dict:
        path = self.resolve(rel)
        os.makedirs(os.path.dirname(path) or self.root, exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(str(content or ''))
        return {'written': len(str(content or '')), 'path': rel}

    def append_file(self, rel: str, content: str = '') -> dict:
        path = self.resolve(rel)
        with open(path, 'a', encoding='utf-8') as fh:
            fh.write(str(content or ''))
        return {'appended': len(str(content or ''))}

    def delete_path(self, rel: str) -> dict:
        path = self.resolve(rel)
        if path == self.root:
            raise FsError('refusing to delete workspace root')
        if os.path.isdir(path):
            shutil.rmtree(path)
            return {'deleted_dir': rel}
        os.remove(path)
        return {'deleted_file': rel}

    def make_dirs(self, rel: str) -> dict:
        path = self.resolve(rel)
        os.makedirs(path, exist_ok=True)
        return {'created': rel}


def env_snapshot(root: str) -> dict:
    info = {
        'platform': f'{sys.platform} ({os.name})',
        'python': sys.version.split()[0],
        'cwd': root,
    }
    git_head = os.path.join(root, '.git', 'HEAD')
    if os.path.isfile(git_head):
        try:
            with open(git_head, 'r', encoding='utf-8', errors='replace') as fh:
                head = fh.read().strip()
            if head.startswith('ref:'):
                info['git_branch'] = head.split('/')[-1]
        except OSError:
            pass
    return info


def dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)
