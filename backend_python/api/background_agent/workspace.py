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

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


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
        self.worktree = self.project_root / 'reusable_workspace'
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
        with self._project_lock():
            self._ensure_mirror_locked()
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

            # Single reusable workspace: clone/add worktree once, otherwise fetch & checkout clean
            if not self.worktree.exists() or not (self.worktree / '.git').exists():
                if self.worktree.exists():
                    shutil.rmtree(self.worktree, ignore_errors=True)
                self._run([
                    'git', '--git-dir', str(self.mirror_path), 'worktree', 'add', '--force', '-b',
                    self.session.work_branch, str(self.worktree), source_ref,
                ], timeout=300)
            else:
                self._run(['git', 'reset', '--hard'], cwd=self.worktree, check=False)
                self._run(['git', 'clean', '-fd'], cwd=self.worktree, check=False)
                with self._auth_env() as env:
                    self._run(['git', 'fetch', '--prune', 'origin'], cwd=self.worktree, env=env, check=False)
                self._run(['git', 'checkout', '-B', self.session.work_branch, source_ref], cwd=self.worktree, check=False)

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

    def push(self, branch: str = ''):
        """Commit safe changes and push the task branch to origin."""
        if not self.session.title:
            # Ensure there is something to push even if the agent never committed.
            self.commit(self.session.goal[:120])
        else:
            self.commit(self.session.title or self.session.goal[:120])
        target = branch or self.session.work_branch
        with self._auth_env() as env:
            result = self._run(
                ['git', 'push', '--set-upstream', 'origin', f'HEAD:refs/heads/{target}'],
                cwd=self.worktree,
                env=env,
                timeout=900,
            )
        return result

    def stage(self, paths=None):
        targets = [p for p in (paths or []) if self.safe_path(p, must_exist=False)]
        if targets:
            self.git('add', '--', *targets, check=False)
        else:
            self.git('add', '-A', check=False)
        return self.git('status', '--short').get('stdout', '')

    def restore(self, paths=None, *, staged=False):
        """Discard working-tree edits for the given safe paths.

        With ``staged=True`` the paths are unstaged instead (``git restore --staged``).
        Omitting ``paths`` restores the whole workspace.
        """
        targets = [p for p in (paths or []) if self.safe_path(p, must_exist=False)]
        args = ['restore']
        if staged:
            args.append('--staged')
        if targets:
            args.extend(['--'] + targets)
        else:
            if not staged:
                args.append('.')
            else:
                return self.git('reset', '--mixed', 'HEAD', check=False).get('stdout', '')
        return self.git(*args, check=False).get('stdout', '')

    def log(self, limit: int = 30):
        limit = max(1, min(int(limit), 200))
        return self.git(
            'log', f'-{limit}', '--pretty=format:%h|%an|%ar|%s', check=False
        ).get('stdout', '')

    def pull(self, branch: str = ''):
        """Fetch and fast-forward merge the upstream of the current task branch."""
        target = branch or self.session.work_branch
        with self._auth_env() as env:
            self._run(
                ['git', 'fetch', 'origin', f'refs/heads/{target}:refs/remotes/origin/{target}'],
                cwd=self.worktree, env=env, timeout=900, check=False,
            )
            result = self.git('merge', '--no-edit', '--ff-only', f'origin/{target}', check=False)
        return result.get('stdout', '') + result.get('stderr', '')

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
        'grep', 'rg', 'find', 'sort', 'wc', 'head', 'tail', 'diff', 'cat', 'cut',
        'uniq', 'tee', 'echo', 'printf', 'env', 'which', 'dirname', 'basename',
        'mkdir', 'cp', 'mv', 'ln',
    }

    def __init__(self, workspace: GitWorkspace):
        self.workspace = workspace

    def execute(self, action: dict) -> dict:
        tool = (action.get('tool') or '').strip()
        arguments = action.get('arguments') or {}
        handlers = {
            'list_files': self.list_files,
            'glob_files': self.glob_files,
            'read_file': self.read_file,
            'search_text': self.search_text,
            'write_file': self.write_file,
            'edit_file': self.edit_file,
            'multi_edit': self.multi_edit,
            'apply_patch': self.apply_patch,
            'delete_file': self.delete_file,
            'copy_file': self.copy_file,
            'move_file': self.move_file,
            'create_directory': self.create_directory,
            'run_command': self.run_command,
            'web_extractor': self.web_extractor,
            'git_status': self.git_status,
            'git_diff': self.git_diff,
            'git_log': self.git_log,
            'git_stage': self.git_stage,
            'git_commit': self.git_commit,
            'git_push': self.git_push,
            'git_pull': self.git_pull,
            'git_restore': self.git_restore,
            'deploy_live_hotfix': self.deploy_live_hotfix,
        }
        handler = handlers.get(tool)
        if not handler:
            return {'ok': False, 'error': f'Unknown tool: {tool}'}
        try:
            return {'ok': True, 'tool': tool, 'result': handler(**arguments)}
        except Exception as exc:
            logger.exception('Background agent tool failed: %s', tool)
            return {'ok': False, 'tool': tool, 'error': str(exc)[:4000]}

    def glob_files(self, pattern, path='.', limit=200):
        import fnmatch
        if not pattern or not isinstance(pattern, str) or len(pattern) > 260:
            raise WorkspaceError('glob_files requires a pattern under 260 characters')
        base = self.workspace.safe_path(path, must_exist=True)
        if not base or not base.is_dir():
            raise WorkspaceError('Directory not found or outside workspace')
        limit = max(1, min(int(limit or 200), 2000))
        ignored = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.gradle', 'build', 'dist', 'target'}
        matches = []
        for current, dirs, files in os.walk(base):
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
                if self.workspace.is_sensitive_relative(relative):
                    continue
                rel = relative.as_posix()
                if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(name, pattern):
                    matches.append(rel)
                    if len(matches) >= limit:
                        return {'matches': matches, 'truncated': True, 'pattern': pattern}
        return {'matches': matches, 'truncated': False, 'pattern': pattern}

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
        width = max(4, len(str(min(end, len(text)))))
        view = '\n'.join(f'{item["line"]:>{width}}|{item["text"]}' for item in lines)
        return {
            'path': path,
            'lines': lines,
            'view': view,
            'totalLines': len(text),
            'truncatedBytes': target.stat().st_size > len(data),
        }

    def search_text(self, query, path='.', limit=100, regex=False, glob=''):
        if not query or len(query) > 500:
            raise WorkspaceError('Search query is required and must be under 500 characters')
        base = self.workspace.safe_path(path, must_exist=True)
        if not base:
            raise WorkspaceError('Search path is outside workspace')
        limit = max(1, min(int(limit), 500))
        use_regex = str(regex).strip().lower() in ('1', 'true', 'yes', 'on')
        matcher = None
        if use_regex:
            try:
                matcher = re.compile(query)
            except re.error as exc:
                raise WorkspaceError(f'Invalid regex: {exc}') from exc
        file_glob = (glob or '').strip()
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
                if file_glob and not __import__('fnmatch').fnmatch(name, file_glob):
                    continue
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
                    hit = bool(matcher.search(line)) if matcher is not None else query in line
                    if hit:
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
        error = self._apply_patch_robust(patch)
        if error:
            raise WorkspaceError(error)
        return {'applied': True, 'files': patch_paths}

    def _apply_patch_robust(self, patch: str) -> str:
        """Apply a unified patch using progressively more forgiving strategies.

        ``git apply`` requires exact context, which is why naive patches "almost
        always fail" when a model drifts on whitespace. We try, in order:
          1. ``git apply --3way``   – three-way merge against stored blobs;
          2. ``git apply`` with whitespace/recount tolerance;
          3. GNU ``patch --merge --fuzz`` as a last resort.
        Returns an empty string on success or a compact error otherwise.
        """
        env = self.workspace._clean_env()
        cwd = str(self.workspace.worktree)

        def run(args, stdin=patch):
            return subprocess.run(
                args, cwd=cwd, env=env, input=stdin, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
            )

        # 1) Three-way merge is the most forgiving and produces real conflicts.
        r = run(['git', 'apply', '--3way', '--whitespace=nowarn', '-'])
        if r.returncode == 0:
            return ''
        attempt_3way = (r.stderr or r.stdout or '').strip()

        # 2) Whitespace-tolerant + recount (lets models with slightly off counts apply).
        r = run(['git', 'apply', '--recount', '--whitespace=fix', '-'])
        if r.returncode == 0:
            return ''

        # 3) GNU patch with fuzzy matching and merge conflict markers.
        patch_bin = shutil.which('patch')
        if patch_bin:
            r = run([patch_bin, '-p1', '--merge', '--fuzz=3', '--no-backup-if-mismatch'])
            if r.returncode == 0:
                return ''
            # patch returns non-zero when some hunks applied and some failed; treat
            # a fully-applied state (clean tree minus expected) as success.
            if 'FAILED' not in (r.stdout or '') and 'FAILED' not in (r.stderr or ''):
                return ''

        return (
            'The patch could not be applied cleanly. '
            'Use edit_file with exact old_text/new_text instead, or fix the context.\n'
            + attempt_3way[-3000:]
        )

    # ---- Search-and-replace editing (the reliable alternative to raw patches) ----

    def edit_file(self, path, old_text, new_text, replace_all=False):
        """Replace ``old_text`` with ``new_text`` inside a file.

        Robust to line-ending and incidental whitespace drift: tries an exact
        match first, then a whitespace-normalised match. Raises a helpful error
        (with the closest line numbers) when the block cannot be located so the
        agent can re-read and retry.
        """
        target = self.workspace.safe_path(path, must_exist=True)
        if not target or not target.is_file():
            raise WorkspaceError('File not found or outside workspace')
        original = target.read_bytes()
        if b'\x00' in original:
            raise WorkspaceError('Cannot edit a binary file')
        text = original.decode('utf-8')
        old = '' if old_text is None else str(old_text)
        new = '' if new_text is None else str(new_text)
        if old == new:
            raise WorkspaceError('old_text and new_text are identical')
        new_text_out, count = self._str_replace(text, old, new, replace_all)
        if count == 0:
            hint = self._closest_match_hint(text, old)
            raise WorkspaceError(
                'old_text was not found in the file. '
                'Re-read the file and copy the exact bytes (including indentation).'
                + (f'\nClosest region:\n{hint}' if hint else '')
            )
        encoded = new_text_out.encode('utf-8')
        max_bytes = int(getattr(settings, 'BACKGROUND_AGENT_MAX_WRITE_BYTES', 2_000_000))
        if len(encoded) > max_bytes:
            raise WorkspaceError(f'Edited file would exceed {max_bytes} bytes')
        target.write_bytes(encoded)
        return {'path': path, 'replacements': count}

    def multi_edit(self, path, edits, best_effort=False):
        """Apply several sequential old_text→new_text edits to one file.

        When *best_effort* is true, failing edits are skipped and the
        response reports which succeeded and which failed (with the closest
        hint).  Default (false) raises on the first failure so no partial
        changes are ever written — the caller can retry the whole batch."""
        if not isinstance(edits, list) or not edits:
            raise WorkspaceError('edits must be a non-empty array of {old_text, new_text}')
        target = self.workspace.safe_path(path, must_exist=True)
        if not target or not target.is_file():
            raise WorkspaceError('File not found or outside workspace')
        original = target.read_bytes()
        if b'\x00' in original:
            raise WorkspaceError('Cannot edit a binary file')
        text = original.decode('utf-8')
        applied = 0
        skipped = []
        for index, edit in enumerate(edits, 1):
            if not isinstance(edit, dict):
                if best_effort:
                    skipped.append({'index': index, 'reason': 'edit must be an object'})
                    continue
                raise WorkspaceError(f'edit #{index} must be an object')
            old = '' if edit.get('old_text') is None else str(edit.get('old_text'))
            new = '' if edit.get('new_text') is None else str(edit.get('new_text'))
            if old == new:
                if best_effort:
                    skipped.append({'index': index, 'reason': 'old_text and new_text are identical'})
                    continue
                raise WorkspaceError(f'edit #{index}: old_text and new_text are identical')
            text, count = self._str_replace(text, old, new, bool(edit.get('replace_all')))
            if count == 0:
                hint = self._closest_match_hint(text, old)
                if best_effort:
                    skipped.append({
                        'index': index,
                        'reason': 'old_text not found',
                        'hint': hint or '',
                    })
                    continue
                raise WorkspaceError(
                    f'edit #{index}: old_text was not found.'
                    + (f'\nClosest region:\n{hint}' if hint else '')
                )
            applied += count
        encoded = text.encode('utf-8')
        max_bytes = int(getattr(settings, 'BACKGROUND_AGENT_MAX_WRITE_BYTES', 2_000_000))
        if len(encoded) > max_bytes:
            raise WorkspaceError(f'Edited file would exceed {max_bytes} bytes')
        target.write_bytes(encoded)
        result = {'path': path, 'replacements': applied}
        if skipped:
            result['skipped'] = skipped
        return result

    @staticmethod
    def _str_replace(text: str, old: str, new: str, replace_all: bool):
        if not old:
            return text, 0
        # Exact count first.
        exact_count = text.count(old)
        if exact_count:
            if replace_all:
                return text.replace(old, new), exact_count
            if exact_count == 1:
                return text.replace(old, new), 1
            raise WorkspaceError(
                f'old_text matches {exact_count} locations. '
                'Add more surrounding context to make it unique, or set replace_all=true.'
            )
        # Fallback: whitespace-normalised match (collapse internal whitespace runs).
        def norm(s):
            return re.sub(r'[ \t]+', ' ', s).replace('\r\n', '\n')

        norm_text, norm_old = norm(text), norm(old)
        if norm_old and norm_old in norm_text:
            occurrences = norm_text.count(norm_old)
            if not replace_all and occurrences > 1:
                raise WorkspaceError(
                    f'old_text matches {occurrences} locations after normalising whitespace. '
                    'Add more context or set replace_all=true.'
                )
            # Reconstruct by replacing the normalised span in the original text.
            rebuilt = []
            i = 0
            replaced = 0
            while True:
                idx = norm_text.find(norm_old, i)
                if idx < 0:
                    break
                # Map the normalised index back to the original text by scanning.
                orig_start = _denorm_index(text, norm_text, idx)
                orig_end = _denorm_index(text, norm_text, idx + len(norm_old))
                rebuilt.append(text[i:orig_start])
                rebuilt.append(new)
                i = orig_end
                replaced += 1
                if not replace_all:
                    break
            rebuilt.append(text[i:])
            return ''.join(rebuilt), replaced
        return text, 0

    @staticmethod
    def _closest_match_hint(text: str, old: str, window: int = 6):
        """Return a small snippet around the line that best resembles ``old``."""
        if not old:
            return ''
        lines = text.splitlines()
        first = old.strip().splitlines()[0][:80] if old.strip() else old[:80]
        best_idx, best_score = -1, 0
        for idx, line in enumerate(lines):
            score = _sequence_similarity(first, line.strip())
            if score > best_score:
                best_score = score
                best_idx = idx
        if best_idx < 0 or best_score < 0.34:
            return ''
        start = max(0, best_idx - 2)
        end = min(len(lines), best_idx + window)
        return '\n'.join(f'{start + n + 1}: {lines[start + n]}' for n in range(end - start))

    # ---- Additional filesystem tools ----

    def copy_file(self, source, destination):
        src = self.workspace.safe_path(source, must_exist=True)
        dst = self.workspace.safe_path(destination, must_exist=False)
        if not src or not src.exists():
            raise WorkspaceError('Source not found or outside workspace')
        if not dst:
            raise WorkspaceError('Destination is outside workspace')
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return {'source': source, 'destination': destination}

    def move_file(self, source, destination):
        src = self.workspace.safe_path(source, must_exist=True)
        dst = self.workspace.safe_path(destination, must_exist=False)
        if not src or not src.exists():
            raise WorkspaceError('Source not found or outside workspace')
        if not dst:
            raise WorkspaceError('Destination is outside workspace')
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return {'source': source, 'destination': destination}

    def create_directory(self, path):
        target = self.workspace.safe_path(path, must_exist=False)
        if not target:
            raise WorkspaceError('Path is outside workspace')
        target.mkdir(parents=True, exist_ok=True)
        return {'path': path}

    # ---- Git tools exposed to the agent ----

    def git_stage(self, paths=None):
        return {'status': self.workspace.stage(paths)}

    def git_commit(self, message):
        msg = (message or 'Background agent changes').strip() or 'Background agent changes'
        sha = self.workspace.commit(msg[:240])
        return {'sha': sha} if sha else {'sha': '', 'note': 'Nothing to commit'}

    def git_push(self, branch=''):
        result = self.workspace.push(branch)
        return {'stdout': result.get('stdout', '')[-4000:], 'branch': branch or self.workspace.session.work_branch}

    def git_pull(self, branch=''):
        return {'output': self.workspace.pull(branch)[-4000:]}

    def git_log(self, limit=30):
        return {'log': self.workspace.log(limit)}

    def git_restore(self, paths=None, staged=False):
        return {'status': self.workspace.restore(paths, staged=staged)}

    def deploy_live_hotfix(self, reason=''):
        """Deploys verified changes from the workspace directly to the live server
        and restarts the application (LiteSpeed/Passenger) without needing SSH keys."""
        import shutil
        from django.conf import settings
        
        live_root = Path(getattr(settings, 'BASE_DIR', '.'))
        ws_repo = self.workspace.worktree
        
        if not ws_repo or not ws_repo.exists():
            return {'ok': False, 'error': 'Workspace repository is unavailable'}

        copied_files = []
        changed = self.workspace.changed_files()
        for rel_file in changed:
            src = ws_repo / rel_file
            if rel_file.startswith('backend_python/'):
                target_rel = rel_file[len('backend_python/'):]
            else:
                target_rel = rel_file
                
            dst = live_root / target_rel
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied_files.append(str(target_rel))

        # Restart LiteSpeed / WSGI by touching restart.txt
        tmp_dir = live_root / 'tmp'
        tmp_dir.mkdir(parents=True, exist_ok=True)
        restart_file = tmp_dir / 'restart.txt'
        restart_file.touch()

        return {
            'ok': True,
            'message': f'Live hotfix deployed ({len(copied_files)} files updated on live server)',
            'copied_files': copied_files,
            'restarted': True,
            'reason': reason or 'Autonomous hotfix by background agent'
        }

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

    def web_extractor(self, url='', **kwargs):
        return {
            'url': url,
            'available': False,
            'error': 'Web extraction is not available in this environment. '
                     'Use search_text, grep, or read_file on locally available files instead.',
        }

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


def _denorm_index(original: str, normalized: str, norm_pos: int) -> int:
    """Map an index in a whitespace-normalised string back to ``original``.

    Walks both strings together, advancing through runs of whitespace so the
    position lines up with the original source text.
    """
    oi = ni = 0
    olen, nlen = len(original), len(normalized)
    ws = ' \t\r\n'
    while ni < norm_pos and ni < nlen and oi < olen:
        if normalized[ni] == original[oi]:
            oi += 1
            ni += 1
        elif original[oi] in ws:
            oi += 1
        else:  # normalised collapsed a whitespace run
            ni += 1
    return oi


def _sequence_similarity(a: str, b: str) -> float:
    """Cheap normalised similarity in [0, 1] using a subsequence ratio."""
    if not a or not b:
        return 0.0
    la, lb = len(a), len(b)
    i = j = matches = 0
    while i < la and j < lb:
        if a[i] == b[j]:
            matches += 1
            i += 1
            j += 1
        elif la - i >= lb - j:
            i += 1
        else:
            j += 1
    return matches / max(la, lb)


def build_branch_name(goal: str, session_id: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', (goal or '').lower()).strip('-')[:42] or 'task'
    suffix = re.sub(r'[^a-f0-9]', '', session_id.lower())[:8] or str(int(time.time()))
    return f'nebians-agent/{slug}-{suffix}'
