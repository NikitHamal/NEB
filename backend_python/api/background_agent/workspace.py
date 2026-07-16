"""Git mirror/worktree management and bounded command execution."""
from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import os
import re
try:
    import resource
except ImportError:  # pragma: no cover - Windows development only
    resource = None
import shlex
import shutil
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path

from django.conf import settings

from api.background_agent.crypto import decrypt_secret
from api.models import BackgroundAgentArtifact
from api.utils import now_ms, uuid_str

logger = logging.getLogger(__name__)


class WorkspaceError(RuntimeError):
    pass


class CommandResult(dict):
    @property
    def ok(self):
        return self.get('returncode') == 0


class GitWorkspace:
    SENSITIVE_DIR_NAMES = {
        '.ssh', '.aws', '.azure', '.gcloud', '.gnupg', '.kube', '.secrets',
    }
    SENSITIVE_FILE_NAMES = {
        '.env', '.netrc', '.npmrc', '.pypirc', '.git-credentials',
        'credentials.json', 'secrets.json', 'secrets.yaml', 'secrets.yml',
        'firebase-service-account.json', 'service-account.json',
        'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    }
    SENSITIVE_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.jks', '.keystore'}
    SAFE_ENV_TEMPLATES = {'.env.example', '.env.sample', '.env.template'}

    def __init__(self, project, session=None):
        self.project = project
        self.session = session
        self.root = Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()
        self.project_root = self.root / 'projects' / str(project.id)
        self.mirror_path = self.project_root / 'repo.git'
        self.session_root = self.root / 'sessions' / str(session.id) if session else None
        self.worktree = self.session_root / 'repo' if self.session_root else None
        self.artifact_root = self.session_root / 'artifacts' if self.session_root else None

    @property
    def token(self) -> str:
        return decrypt_secret(self.project.credential.encrypted_access_token)

    def ensure_dirs(self):
        self.project_root.mkdir(parents=True, exist_ok=True)
        if self.session_root:
            self.session_root.mkdir(parents=True, exist_ok=True)
            self.artifact_root.mkdir(parents=True, exist_ok=True)

    @contextlib.contextmanager
    def _project_lock(self):
        """Serialize mirror mutations across worker processes.

        Git handles normal object reads concurrently, but fetch/worktree/branch
        metadata updates can collide when multiple workers start tasks for the
        same repository at once. The persisted lock lives beside the mirror.
        """
        self.project_root.mkdir(parents=True, exist_ok=True)
        lock_path = self.project_root / '.workspace.lock'
        handle = lock_path.open('a+b')
        try:
            if os.name == 'posix':
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            elif os.name == 'nt':  # pragma: no cover - production is Linux
                import msvcrt
                handle.seek(0)
                if handle.tell() == 0:
                    handle.write(b'0')
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            yield
        finally:
            try:
                if os.name == 'posix':
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                elif os.name == 'nt':  # pragma: no cover
                    import msvcrt
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            finally:
                handle.close()

    @contextlib.contextmanager
    def _auth_env(self):
        token = self.token
        if not token:
            raise WorkspaceError('GitHub credential is not connected')
        self.ensure_dirs()
        askpass_dir = Path(tempfile.mkdtemp(prefix='askpass-', dir=str(self.root)))
        script = askpass_dir / 'askpass.sh'
        script.write_text(
            '#!/bin/sh\n'
            'case "$1" in\n'
            '  *Username*) printf "%s\\n" "x-access-token" ;;\n'
            '  *) printf "%s\\n" "$NEBIANS_GITHUB_TOKEN" ;;\n'
            'esac\n'
        )
        script.chmod(0o700)
        env = self._clean_env()
        env.update({
            'GIT_ASKPASS': str(script),
            'GIT_TERMINAL_PROMPT': '0',
            'NEBIANS_GITHUB_TOKEN': token,
        })
        try:
            yield env
        finally:
            shutil.rmtree(askpass_dir, ignore_errors=True)

    @staticmethod
    def _clean_env():
        allowed = ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR', 'TEMP', 'TMP', 'SYSTEMROOT', 'COMSPEC')
        env = {k: v for k, v in os.environ.items() if k in allowed}
        env.setdefault('LANG', 'C.UTF-8')
        env['GIT_CONFIG_NOSYSTEM'] = '1'
        env['GIT_LFS_SKIP_SMUDGE'] = '1'
        return env

    def _run(self, args, *, cwd=None, env=None, timeout=None, check=True, stdout_limit=200000, stderr_limit=50000) -> CommandResult:
        timeout = timeout or int(getattr(settings, 'BACKGROUND_AGENT_COMMAND_TIMEOUT', 300))
        started = time.monotonic()
        try:
            completed = subprocess.run(
                [str(a) for a in args],
                cwd=str(cwd) if cwd else None,
                env=env or self._clean_env(),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise WorkspaceError(f'Command timed out after {timeout}s: {shlex.join(map(str, args))}') from exc
        result = CommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout if stdout_limit is None else completed.stdout[-stdout_limit:],
            stderr=completed.stderr if stderr_limit is None else completed.stderr[-stderr_limit:],
            duration=round(time.monotonic() - started, 3),
            command=[str(a) for a in args],
        )
        if check and completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or 'unknown error')[-4000:]
            raise WorkspaceError(f"Command failed ({completed.returncode}): {detail}")
        return result

    def ensure_mirror(self):
        self.ensure_dirs()
        with self._project_lock():
            self._ensure_mirror_locked()

    def _ensure_mirror_locked(self):
        self.project.status = 'syncing'
        self.project.last_error = ''
        self.project.updated_at = now_ms()
        self.project.save(update_fields=['status', 'last_error', 'updated_at'])
        try:
            self._sync_mirror_repository()
        except Exception as exc:
            self.project.status = 'error'
            self.project.last_error = str(exc)[:8000]
            self.project.updated_at = now_ms()
            self.project.save(update_fields=['status', 'last_error', 'updated_at'])
            raise
        self.project.mirror_path = str(self.mirror_path)
        self.project.status = 'ready'
        self.project.last_error = ''
        self.project.last_synced_at = now_ms()
        self.project.updated_at = now_ms()
        self.project.save(update_fields=['mirror_path', 'status', 'last_error', 'last_synced_at', 'updated_at'])

    def _sync_mirror_repository(self):
        clone_url = self.project.clone_url
        with self._auth_env() as env:
            if not self.mirror_path.exists():
                tmp = self.project_root / 'repo.git.tmp'
                shutil.rmtree(tmp, ignore_errors=True)
                self._run(['git', 'init', '--bare', str(tmp)], env=env)
                self._run(['git', '--git-dir', str(tmp), 'remote', 'add', 'origin', clone_url], env=env)
                self._run(
                    ['git', '--git-dir', str(tmp), 'fetch', '--prune', 'origin',
                     '+refs/heads/*:refs/remotes/origin/*', '+refs/tags/*:refs/tags/*'],
                    env=env,
                    timeout=900,
                )
                tmp.replace(self.mirror_path)
            else:
                self._run(['git', '--git-dir', str(self.mirror_path), 'remote', 'set-url', 'origin', clone_url], env=env)
                self._run(
                    ['git', '--git-dir', str(self.mirror_path), 'fetch', '--prune', 'origin',
                     '+refs/heads/*:refs/remotes/origin/*', '+refs/tags/*:refs/tags/*'],
                    env=env,
                    timeout=900,
                )

    def prepare_session(self):
        if not self.session:
            raise WorkspaceError('Session is required')
        self.ensure_dirs()
        if self.worktree.exists() and (self.worktree / '.git').exists():
            return
        with self._project_lock():
            self._ensure_mirror_locked()
            if self.worktree.exists():
                shutil.rmtree(self.worktree, ignore_errors=True)
            source_branch = (self.session.source_branch or '').strip()
            valid_source = self._run(['git', 'check-ref-format', '--branch', source_branch], check=False)
            if not valid_source.ok:
                raise WorkspaceError(f'Invalid source branch: {source_branch}')
            source_ref = f'refs/remotes/origin/{source_branch}'
            exists = self._run(['git', '--git-dir', str(self.mirror_path), 'show-ref', '--verify', '--quiet', source_ref], check=False)
            if not exists.ok:
                raise WorkspaceError(f'Source branch does not exist: {source_branch}')
            if not self.session.work_branch:
                self.session.work_branch = build_branch_name(self.session.goal, str(self.session.id))
            valid_work = self._run(['git', 'check-ref-format', '--branch', self.session.work_branch], check=False)
            if not valid_work.ok:
                raise WorkspaceError('Generated task branch is invalid')
            # A stale branch from a failed preparation should not block a retry.
            self._run(['git', '--git-dir', str(self.mirror_path), 'branch', '-D', self.session.work_branch], check=False)
            self._run([
                'git', '--git-dir', str(self.mirror_path), 'worktree', 'add', '--force', '-b',
                self.session.work_branch, str(self.worktree), source_ref,
            ], timeout=300)
        self._run(['git', 'config', 'user.name', 'NEBians Background Agent'], cwd=self.worktree)
        self._run(['git', 'config', 'user.email', 'background-agent@nebians.local'], cwd=self.worktree)
        base_sha = self._run(['git', 'rev-parse', 'HEAD'], cwd=self.worktree).get('stdout', '').strip()
        self.session.base_sha = base_sha
        self.session.head_sha = base_sha
        self.session.workspace_path = str(self.worktree)
        self.session.save(update_fields=['work_branch', 'base_sha', 'head_sha', 'workspace_path'])

    def git(self, *args, check=True, timeout=None, stdout_limit=200000):
        if not self.worktree:
            raise WorkspaceError('Session worktree is unavailable')
        return self._run(
            ['git', *args], cwd=self.worktree, check=check, timeout=timeout,
            stdout_limit=stdout_limit,
        )

    def status(self) -> str:
        return self.git('status', '--short', '--branch').get('stdout', '')

    def diff(self, *, max_chars=500000) -> str:
        base = self.session.base_sha or 'HEAD'
        files = self.changed_files()
        if not files:
            return ''
        untracked = self._safe_untracked_files()
        # Intent-to-add makes safe untracked files visible in the diff without
        # staging content. Sensitive files are never added or sent to a model.
        if untracked:
            self.git('add', '-N', '--', *untracked, check=False)
        capture_limit = None if max_chars is None else max_chars + 1
        out = self.git(
            'diff', '--no-ext-diff', '--find-renames', '--find-copies', '--binary',
            base, '--', *files, stdout_limit=capture_limit,
        ).get('stdout', '')
        if max_chars is not None and len(out) > max_chars:
            return out[:max_chars] + '\n\n[diff truncated by server]\n'
        return out

    def write_patch(self, path: Path):
        """Stream the complete safe diff to disk without response truncation."""
        files = self.changed_files()
        untracked = self._safe_untracked_files()
        if untracked:
            self.git('add', '-N', '--', *untracked, check=False)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not files:
            path.write_bytes(b'')
            return path
        command = [
            'git', 'diff', '--no-ext-diff', '--find-renames', '--find-copies',
            '--binary', self.session.base_sha or 'HEAD', '--', *files,
        ]
        try:
            with path.open('wb') as output:
                completed = subprocess.run(
                    command,
                    cwd=str(self.worktree),
                    env=self._clean_env(),
                    stdout=output,
                    stderr=subprocess.PIPE,
                    timeout=int(getattr(settings, 'BACKGROUND_AGENT_PATCH_TIMEOUT', 900)),
                    check=False,
                )
        except subprocess.TimeoutExpired as exc:
            path.unlink(missing_ok=True)
            raise WorkspaceError('Generating the complete patch timed out') from exc
        if completed.returncode != 0:
            path.unlink(missing_ok=True)
            raise WorkspaceError((completed.stderr or b'git diff failed')[-4000:].decode('utf-8', errors='replace'))
        return path

    def changed_files(self) -> list[str]:
        base = self.session.base_sha or 'HEAD'
        tracked = self.git('diff', '--name-only', '-z', base, '--').get('stdout', '')
        untracked = '\0'.join(self._safe_untracked_files())
        if untracked:
            untracked += '\0'
        files = []
        seen = set()
        for path in [p for p in (tracked + untracked).split('\0') if p]:
            if path not in seen and self.safe_path(path, must_exist=False):
                seen.add(path)
                files.append(path)
        return files

    def _safe_untracked_files(self) -> list[str]:
        raw = self.git('ls-files', '--others', '--exclude-standard', '-z').get('stdout', '')
        return [
            path for path in raw.split('\0')
            if path and self.safe_path(path, must_exist=False)
        ]

    @classmethod
    def is_sensitive_relative(cls, relative: str | Path) -> bool:
        path = Path(str(relative))
        parts = [part.lower() for part in path.parts if part not in ('', '.')]
        if any(part in cls.SENSITIVE_DIR_NAMES for part in parts):
            return True
        if not parts:
            return False
        name = parts[-1]
        if name in cls.SAFE_ENV_TEMPLATES:
            return False
        if name == '.env' or name.startswith('.env.'):
            return True
        if name in cls.SENSITIVE_FILE_NAMES:
            return True
        if ('service-account' in name or 'service_account' in name) and name.endswith('.json'):
            return True
        return Path(name).suffix.lower() in cls.SENSITIVE_SUFFIXES

    def safe_path(self, relative: str, *, must_exist=False) -> Path | None:
        if not self.worktree:
            return None
        if not relative or '\x00' in relative:
            return None
        logical = Path(relative)
        if self.is_sensitive_relative(logical):
            return None
        candidate = (self.worktree / logical).resolve()
        root = self.worktree.resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            return None
        resolved_relative = candidate.relative_to(root)
        if '.git' in resolved_relative.parts or self.is_sensitive_relative(resolved_relative):
            return None
        if must_exist and not candidate.exists():
            return None
        return candidate

    def commit(self, message: str):
        files = self.changed_files()
        if not files:
            return ''
        self.git('add', '-A', '--', *files)
        result = self.git('commit', '-m', (message or 'Apply background agent changes')[:240], check=False)
        if not result.ok and 'nothing to commit' not in (result.stdout + result.stderr).lower():
            raise WorkspaceError(result.stderr or result.stdout)
        sha = self.git('rev-parse', 'HEAD').get('stdout', '').strip()
        self.session.head_sha = sha
        self.session.save(update_fields=['head_sha'])
        return sha

    def push(self):
        self.commit(self.session.title or self.session.goal[:120])
        with self._auth_env() as env:
            result = self._run(
                ['git', 'push', '--set-upstream', 'origin', f'HEAD:refs/heads/{self.session.work_branch}'],
                cwd=self.worktree,
                env=env,
                timeout=900,
            )
        return result

    def build_artifacts(self):
        if not self.session:
            raise WorkspaceError('Session is required')
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        changed = self.changed_files()
        patch_path = self.artifact_root / f'{self.session.id}.patch'
        self.write_patch(patch_path)
        zip_path = self.artifact_root / f'{self.session.id}-changed-files.zip'
        manifest = {
            'sessionId': str(self.session.id),
            'repository': self.project.repo_full_name,
            'sourceBranch': self.session.source_branch,
            'workBranch': self.session.work_branch,
            'baseSha': self.session.base_sha,
            'headSha': self.session.head_sha,
            'changedFiles': changed,
            'generatedAt': now_ms(),
        }
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            zf.writestr('BACKGROUND_AGENT_MANIFEST.json', json.dumps(manifest, indent=2, ensure_ascii=False))
            zf.write(patch_path, 'changes.patch')
            for relative in changed:
                path = self.safe_path(relative, must_exist=True)
                if path and path.is_file():
                    zf.write(path, relative)
        self._record_artifact('patch', patch_path, f'{self.session.id}.patch')
        self._record_artifact('changes_zip', zip_path, f'{self.project.repo_full_name.replace("/", "-")}-{self.session.id}.zip')
        return {'changedFiles': changed, 'patchPath': str(patch_path), 'zipPath': str(zip_path)}

    def _record_artifact(self, kind, path: Path, file_name: str):
        hasher = hashlib.sha256()
        with path.open('rb') as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                hasher.update(chunk)
        digest = hasher.hexdigest()
        artifact, created = BackgroundAgentArtifact.objects.get_or_create(
            session=self.session,
            kind=kind,
            defaults={'id': uuid_str(), 'file_path': str(path), 'file_name': file_name},
        )
        artifact.file_path = str(path)
        artifact.file_name = file_name
        artifact.size_bytes = path.stat().st_size
        artifact.sha256 = digest
        artifact.created_at = now_ms()
        artifact.save(update_fields=['file_path', 'file_name', 'size_bytes', 'sha256', 'created_at'])


class ToolExecutor:
    """Workspace-jail file tools plus a bounded command runner.

    Local execution is intentionally constrained and can be replaced with a
    Docker backend through settings. It never invokes a shell for model-issued
    commands. The model must provide an argv array.
    """

    DEFAULT_ALLOWED = {
        'python', 'python3', 'pytest', 'node', 'npm', 'npx', 'pnpm', 'yarn',
        'java', 'javac', 'gradle', 'mvn', 'go', 'cargo', 'rustc', 'make', 'cmake',
        'php', 'composer', 'ruby', 'bundle',
    }

    def __init__(self, workspace: GitWorkspace):
        self.workspace = workspace

    def execute(self, action: dict) -> dict:
        tool = (action.get('tool') or '').strip()
        arguments = action.get('arguments') or {}
        handlers = {
            'list_files': self.list_files,
            'read_file': self.read_file,
            'search_text': self.search_text,
            'write_file': self.write_file,
            'apply_patch': self.apply_patch,
            'delete_file': self.delete_file,
            'run_command': self.run_command,
            'git_status': self.git_status,
            'git_diff': self.git_diff,
        }
        handler = handlers.get(tool)
        if not handler:
            return {'ok': False, 'error': f'Unknown tool: {tool}'}
        try:
            return {'ok': True, 'tool': tool, 'result': handler(**arguments)}
        except Exception as exc:
            logger.exception('Background agent tool failed: %s', tool)
            return {'ok': False, 'tool': tool, 'error': str(exc)[:4000]}

    def list_files(self, path='.', depth=3, limit=500):
        base = self.workspace.safe_path(path, must_exist=True)
        if not base or not base.is_dir():
            raise WorkspaceError('Directory not found or outside workspace')
        depth = max(0, min(int(depth), 8))
        limit = max(1, min(int(limit), 2000))
        root_depth = len(base.parts)
        rows = []
        ignored = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.gradle', 'build', 'dist', 'target'}
        for current, dirs, files in os.walk(base):
            current_path = Path(current)
            if len(current_path.parts) - root_depth >= depth:
                dirs[:] = []
            safe_dirs = []
            for name in dirs:
                rel = (current_path / name).relative_to(self.workspace.worktree)
                if name not in ignored and not self.workspace.is_sensitive_relative(rel):
                    safe_dirs.append(name)
            dirs[:] = safe_dirs
            safe_files = [
                name for name in files
                if not self.workspace.is_sensitive_relative((current_path / name).relative_to(self.workspace.worktree))
            ]
            for name in sorted(dirs + safe_files):
                p = current_path / name
                rel = p.relative_to(self.workspace.worktree).as_posix()
                rows.append(rel + ('/' if p.is_dir() else ''))
                if len(rows) >= limit:
                    return {'entries': rows, 'truncated': True}
        return {'entries': rows, 'truncated': False}

    def read_file(self, path, start_line=1, end_line=400):
        target = self.workspace.safe_path(path, must_exist=True)
        if not target or not target.is_file():
            raise WorkspaceError('File not found or outside workspace')
        max_bytes = int(getattr(settings, 'BACKGROUND_AGENT_MAX_FILE_READ_BYTES', 500000))
        data = target.read_bytes()
        if len(data) > max_bytes:
            data = data[:max_bytes]
        if b'\x00' in data:
            return {'path': path, 'binary': True, 'size': target.stat().st_size}
        text = data.decode('utf-8', errors='replace').splitlines()
        start = max(1, int(start_line))
        end = max(start, min(int(end_line), start + 2000))
        lines = [{'line': i + 1, 'text': text[i]} for i in range(start - 1, min(end, len(text)))]
        return {'path': path, 'lines': lines, 'totalLines': len(text), 'truncatedBytes': target.stat().st_size > len(data)}

    def search_text(self, query, path='.', limit=100):
        if not query or len(query) > 500:
            raise WorkspaceError('Search query is required and must be under 500 characters')
        base = self.workspace.safe_path(path, must_exist=True)
        if not base:
            raise WorkspaceError('Search path is outside workspace')
        limit = max(1, min(int(limit), 500))
        matches = []
        scanned_bytes = 0
        max_scan_bytes = int(getattr(settings, 'BACKGROUND_AGENT_MAX_SEARCH_BYTES', 25_000_000))
        ignored = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.gradle', 'build', 'dist', 'target'}
        roots = [base] if base.is_file() else None
        iterator = []
        if roots:
            iterator = [(str(base.parent), [], [base.name])]
        else:
            iterator = os.walk(base, followlinks=False)
        truncated = False
        for current, dirs, files in iterator:
            current_path = Path(current)
            dirs[:] = [
                name for name in dirs
                if name not in ignored and not self.workspace.is_sensitive_relative(
                    (current_path / name).relative_to(self.workspace.worktree)
                )
            ]
            for name in files:
                candidate = current_path / name
                relative = candidate.relative_to(self.workspace.worktree)
                safe = self.workspace.safe_path(relative.as_posix(), must_exist=True)
                if not safe or not safe.is_file():
                    continue
                try:
                    size = safe.stat().st_size
                except OSError:
                    continue
                if size > 2_000_000 or scanned_bytes + size > max_scan_bytes:
                    truncated = True
                    continue
                scanned_bytes += size
                try:
                    data = safe.read_bytes()
                except OSError:
                    continue
                if b'\x00' in data:
                    continue
                for line_number, line in enumerate(data.decode('utf-8', errors='replace').splitlines(), 1):
                    if query in line:
                        matches.append(f'{relative.as_posix()}:{line_number}:{line[:2000]}')
                        if len(matches) >= limit:
                            return {'matches': matches, 'truncated': True, 'scannedBytes': scanned_bytes}
        return {'matches': matches, 'truncated': truncated, 'scannedBytes': scanned_bytes}

    def write_file(self, path, content, create_parents=True):
        target = self.workspace.safe_path(path, must_exist=False)
        if not target:
            raise WorkspaceError('Write path is outside workspace')
        max_bytes = int(getattr(settings, 'BACKGROUND_AGENT_MAX_WRITE_BYTES', 2_000_000))
        encoded = str(content).encode('utf-8')
        if len(encoded) > max_bytes:
            raise WorkspaceError(f'Write exceeds {max_bytes} bytes')
        if create_parents:
            target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)
        return {'path': path, 'bytes': len(encoded)}

    def apply_patch(self, patch):
        if not isinstance(patch, str) or len(patch) > 2_000_000:
            raise WorkspaceError('Patch is missing or too large')
        patch_paths = self._validate_patch_paths(patch)
        if not patch_paths:
            raise WorkspaceError('Patch does not contain any file changes')
        completed = subprocess.run(
            ['git', 'apply', '--whitespace=nowarn', '-'],
            cwd=str(self.workspace.worktree),
            input=patch,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            env=self.workspace._clean_env(),
        )
        if completed.returncode != 0:
            raise WorkspaceError(completed.stderr[-4000:] or 'git apply failed')
        return {'applied': True}

    def _validate_patch_paths(self, patch):
        paths = set()
        for line in patch.splitlines():
            candidates = []
            if line.startswith('diff --git '):
                try:
                    parts = shlex.split(line)
                except ValueError as exc:
                    raise WorkspaceError('Patch contains an invalid diff header') from exc
                if len(parts) >= 4:
                    candidates.extend(parts[2:4])
            elif line.startswith('--- ') or line.startswith('+++ '):
                value = line[4:].split('\t', 1)[0].strip()
                candidates.append(value)
            for value in candidates:
                if value == '/dev/null':
                    continue
                if value.startswith(('a/', 'b/')):
                    value = value[2:]
                if not value or not self.workspace.safe_path(value, must_exist=False):
                    raise WorkspaceError(f'Patch targets a protected or invalid path: {value or "(empty)"}')
                paths.add(value)
        return sorted(paths)

    def delete_file(self, path):
        target = self.workspace.safe_path(path, must_exist=True)
        if not target:
            raise WorkspaceError('Delete path is outside workspace')
        if target.is_dir():
            if any(target.iterdir()):
                raise WorkspaceError('Refusing to recursively delete a non-empty directory')
            target.rmdir()
        else:
            target.unlink()
        return {'path': path, 'deleted': True}

    def run_command(self, argv, cwd='.', timeout=300):
        if not isinstance(argv, list) or not argv or not all(isinstance(v, str) for v in argv):
            raise WorkspaceError('run_command requires a non-empty argv string array')
        executable = Path(argv[0]).name
        configured = getattr(settings, 'BACKGROUND_AGENT_ALLOWED_COMMANDS', '')
        allowed = {x.strip() for x in configured.split(',') if x.strip()} or self.DEFAULT_ALLOWED
        if executable not in allowed and not argv[0].startswith('./'):
            raise WorkspaceError(f'Command is not allowed: {executable}')
        command_cwd = self.workspace.safe_path(cwd, must_exist=True)
        if not command_cwd or not command_cwd.is_dir():
            raise WorkspaceError('Command working directory is outside workspace')
        timeout = max(1, min(int(timeout), int(getattr(settings, 'BACKGROUND_AGENT_MAX_COMMAND_TIMEOUT', 1200))))
        backend = getattr(settings, 'BACKGROUND_AGENT_EXECUTION_BACKEND', 'auto').lower()
        if backend in ('docker', 'auto') and shutil.which('docker') and getattr(settings, 'BACKGROUND_AGENT_DOCKER_IMAGE', ''):
            result = self._run_docker(argv, command_cwd, timeout)
            result.update({'argv': argv, 'cwd': cwd, 'backend': 'docker'})
            return result
        if backend == 'docker':
            raise WorkspaceError('Docker execution was requested but Docker or BACKGROUND_AGENT_DOCKER_IMAGE is unavailable')
        if not getattr(settings, 'BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION', False):
            raise WorkspaceError('Local command execution is disabled. Configure the Docker sandbox or explicitly enable local execution for development.')
        result = self._run_local(argv, command_cwd, timeout)
        result.update({'argv': argv, 'cwd': cwd, 'backend': 'local'})
        return result

    def _run_local(self, argv, cwd, timeout):
        def limits():
            try:
                if resource is None:
                    return
                resource.setrlimit(resource.RLIMIT_CPU, (timeout + 5, timeout + 5))
                max_file = int(getattr(settings, 'BACKGROUND_AGENT_MAX_OUTPUT_FILE_BYTES', 250_000_000))
                resource.setrlimit(resource.RLIMIT_FSIZE, (max_file, max_file))
                resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
                resource.setrlimit(resource.RLIMIT_NPROC, (128, 128))
            except Exception:
                pass
        started = time.monotonic()
        completed = subprocess.run(
            argv,
            cwd=str(cwd),
            env=self.workspace._clean_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            preexec_fn=limits if os.name == 'posix' else None,
        )
        return {
            'returncode': completed.returncode,
            'stdout': completed.stdout[-100000:],
            'stderr': completed.stderr[-50000:],
            'duration': round(time.monotonic() - started, 3),
        }

    def _run_docker(self, argv, cwd, timeout):
        image = getattr(settings, 'BACKGROUND_AGENT_DOCKER_IMAGE')
        network = getattr(settings, 'BACKGROUND_AGENT_DOCKER_NETWORK', 'none')
        rel_cwd = cwd.relative_to(self.workspace.worktree).as_posix()
        container_cwd = '/workspace' if rel_cwd == '.' else f'/workspace/{rel_cwd}'
        command = [
            'docker', 'run', '--rm', '--init', '--network', network,
            '--cpus', str(getattr(settings, 'BACKGROUND_AGENT_DOCKER_CPUS', '2')),
            '--memory', str(getattr(settings, 'BACKGROUND_AGENT_DOCKER_MEMORY', '4g')),
            '--pids-limit', str(getattr(settings, 'BACKGROUND_AGENT_DOCKER_PIDS', '256')),
            '--cap-drop', 'ALL', '--read-only',
            '--security-opt', 'no-new-privileges',
            '--tmpfs', '/tmp:rw,nosuid,nodev,size=1g',
            '--user', f'{os.getuid()}:{os.getgid()}' if hasattr(os, 'getuid') else '65534:65534',
            '-e', 'HOME=/tmp', '-e', 'CI=1',
            '-v', f'{self.workspace.worktree}:/workspace:rw',
            '-w', container_cwd,
        ]
        command.extend(self._docker_secret_masks('/workspace'))
        command.extend([image, *argv])
        return self.workspace._run(command, timeout=timeout, check=False)

    def _docker_secret_masks(self, container_root):
        """Hide repository credentials from model-issued container commands."""
        mask_root = self.workspace.session_root / '.sandbox-masks'
        empty_file = mask_root / 'empty-file'
        empty_dir = mask_root / 'empty-dir'
        empty_dir.mkdir(parents=True, exist_ok=True)
        empty_file.touch(exist_ok=True)
        mounts = ['-v', f'{empty_file}:{container_root}/.git:ro']
        for current, dirs, files in os.walk(self.workspace.worktree, followlinks=False):
            current_path = Path(current)
            kept_dirs = []
            for name in dirs:
                path = current_path / name
                relative = path.relative_to(self.workspace.worktree)
                if self.workspace.is_sensitive_relative(relative):
                    mounts.extend(['-v', f'{empty_dir}:{container_root}/{relative.as_posix()}:ro'])
                else:
                    kept_dirs.append(name)
            dirs[:] = kept_dirs
            for name in files:
                path = current_path / name
                relative = path.relative_to(self.workspace.worktree)
                if self.workspace.is_sensitive_relative(relative):
                    mounts.extend(['-v', f'{empty_file}:{container_root}/{relative.as_posix()}:ro'])
        return mounts

    def git_status(self):
        return {'status': self.workspace.status()}

    def git_diff(self):
        return {'diff': self.workspace.diff()}


def build_branch_name(goal: str, session_id: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', (goal or '').lower()).strip('-')[:42] or 'task'
    suffix = re.sub(r'[^a-f0-9]', '', session_id.lower())[:8] or str(int(time.time()))
    return f'nebians-agent/{slug}-{suffix}'
