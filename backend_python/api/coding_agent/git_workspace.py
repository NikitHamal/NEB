"""GitHub + git workspace helpers for the coding agent.

Responsibilities:
  · Clone the connected GitHub repo into a per-session workspace directory
    (or reuse the project workspace cache when a session starts).
  · Create the session branch from the project's default branch, push to it
    when the user approves.
  · Push the branch to the user's GitHub via HTTPS + Basic auth with the
    project's OAuth `repo` scope token. We don't use SSH to avoid managing
    server keys.
  · Open a PR via the GitHub REST API.

This module deliberately avoids the `git` CLI's interactive prompts so it can
be invoked from a non-interactive cron worker. `GIT_TERMINAL_PROMPT=0` is set
in the shell environment (see tools.py).
"""
from __future__ import annotations

import logging
import os
import re
import subprocess
import threading
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .constants import WORKSPACE_ROOT_DEFAULT, WORKSPACE_ROOT_ENV
from .models import CodingAgentProject, CodingAgentSession

logger = logging.getLogger(__name__)

_WORKSPACE_LOCKS: Dict[str, threading.Lock] = {}
_WORKSPACE_LOCKS_LOCK = threading.Lock()


def workspace_root() -> Path:
    raw = os.environ.get(WORKSPACE_ROOT_ENV, WORKSPACE_ROOT_DEFAULT)
    p = Path(raw)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _lock_for(path: Path) -> threading.Lock:
    key = str(path.resolve())
    with _WORKSPACE_LOCKS_LOCK:
        lock = _WORKSPACE_LOCKS.get(key)
        if lock is None:
            lock = threading.Lock()
            _WORKSPACE_LOCKS[key] = lock
        return lock


def safe_branch_name(task: str) -> str:
    """Convert a session task into a valid git branch name.

    Lower-case, dashes for spaces, strips characters Git refuses. Adds a
    short ts suffix so two sessions with identical tasks don't collide.
    """
    base = re.sub(r'[^A-Za-z0-9._/-]+', '-', task.strip().lower())[:40].strip('-')
    if not base:
        base = 'task'
    return f'agent/{base}-{int(time.time())}'[:200]


def slugify(value: str) -> str:
    return re.sub(r'[^a-z0-9-]+', '-', value.lower()).strip('-')


def project_repo_dir(project: CodingAgentProject) -> Path:
    safe_owner = re.sub(r'[^a-zA-Z0-9._-]+', '-', project.repo_owner)
    safe_name = re.sub(r'[^a-zA-Z0-9._-]+', '-', project.repo_name)
    return workspace_root() / f'{safe_owner}__{safe_name}'


def project_auth_url(project: CodingAgentProject) -> str:
    token = urllib.parse.quote(project.access_token or '', safe='')
    return f'https://x-access-token:{token}@github.com/{project.repo_owner}/{project.repo_name}.git'


def is_clone_present(project: CodingAgentProject) -> bool:
    p = project_repo_dir(project)
    return p.exists() and (p / '.git').is_dir()


def fetch_default_branch(project: CodingAgentProject) -> str:
    """Read repo info via GitHub API to learn its default branch."""
    import requests

    url = f'https://api.github.com/repos/{project.repo_owner}/{project.repo_name}'
    headers = {
        'Authorization': f'Bearer {project.access_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code >= 300:
        raise RuntimeError(f'GitHub repo fetch failed: HTTP {resp.status_code} {resp.text[:300]}')
    data = resp.json()
    default_branch = data.get('default_branch') or project.default_branch or 'main'
    project.default_branch = default_branch
    project.repo_description = (data.get('description') or '')[:1000]
    project.repo_url = data.get('html_url') or project.repo_url
    project.is_private = bool(data.get('private'))
    project.github_user_login = data.get('owner', {}).get('login') or project.github_user_login
    project.save(update_fields=['default_branch', 'repo_description', 'repo_url', 'is_private', 'github_user_login', 'updated_at'])
    return default_branch


def ensure_clone(project: CodingAgentProject, refresh: bool = False) -> Path:
    target = project_repo_dir(project)
    auth_url = project_auth_url(project)
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'
    env['GIT_ASKPASS'] = 'echo'

    lock = _lock_for(target)
    with lock:
        if refresh and target.exists():
            shutil_rmtree(target)

        if target.exists() and (target / '.git').is_dir():
            try:
                remote_proc = subprocess.run(
                    ['git', '-C', str(target), 'remote', 'set-url', 'origin', auth_url],
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=30,
                )
                if remote_proc.returncode != 0:
                    logger.warning('set-url failed (no remote configured yet): %s', remote_proc.stderr.strip())
            except Exception:  # noqa: BLE001
                logger.warning('set-url exception (likely no remote)', exc_info=False)
            try:
                fetch_proc = subprocess.run(
                    ['git', '-C', str(target), 'fetch', '--prune', '--tags', 'origin'],
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=600,
                )
                if fetch_proc.returncode != 0:
                    logger.warning('git fetch failed (will retry on branch creation): %s', fetch_proc.stderr[:300])
            except Exception:  # noqa: BLE001
                logger.warning('git fetch exception (will retry on branch creation)', exc_info=False)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            clone_proc = subprocess.run(
                ['git', 'clone', '--quiet', auth_url, str(target)],
                capture_output=True,
                text=True,
                env=env,
                timeout=900,
            )
            if clone_proc.returncode != 0:
                raise RuntimeError(f'git clone failed: {clone_proc.stderr[:1000]}')
    return target


def create_session_branch(project: CodingAgentProject, session: CodingAgentSession, branch_name: str) -> str:
    """Create (or check out) the session branch from the project's default branch.

    Returns the base SHA the session branched from.
    """
    repo_path = project_repo_dir(project)
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'

    has_remote = subprocess.run(
        ['git', '-C', str(repo_path), 'remote', 'get-url', 'origin'],
        capture_output=True, text=True, env=env, timeout=10,
    )

    if has_remote.returncode == 0 and has_remote.stdout.strip():
        fetch_proc = subprocess.run(
            ['git', '-C', str(repo_path), 'fetch', '--quiet', 'origin', project.default_branch],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
        )
        if fetch_proc.returncode != 0:
            raise RuntimeError(f'git fetch origin/{project.default_branch} failed: {fetch_proc.stderr[:600]}')

        hard_reset_proc = subprocess.run(
            ['git', '-C', str(repo_path), 'reset', '--hard', f'origin/{project.default_branch}'],
            capture_output=True,
            text=True,
            env=env,
            timeout=60,
        )
        if hard_reset_proc.returncode != 0:
            raise RuntimeError(f'git reset hard failed: {hard_reset_proc.stderr[:600]}')
    elif has_remote.returncode != 0:
        logger.info('create_session_branch: no remote configured for %s, using local HEAD as base', repo_path)

    clean_proc = subprocess.run(
        ['git', '-C', str(repo_path), 'clean', '-fdx'],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    if clean_proc.returncode != 0:
        logger.warning('git clean failed (non-fatal): %s', clean_proc.stderr)

    branch_proc = subprocess.run(
        ['git', '-C', str(repo_path), 'checkout', '-B', branch_name],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    if branch_proc.returncode != 0:
        raise RuntimeError(f'git checkout -B failed: {branch_proc.stderr[:600]}')

    sha_proc = subprocess.run(
        ['git', '-C', str(repo_path), 'rev-parse', 'HEAD'],
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )
    if sha_proc.returncode != 0:
        raise RuntimeError(f'git rev-parse failed: {sha_proc.stderr[:300]}')
    sha = sha_proc.stdout.strip()
    session.base_ref = sha
    session.branch = branch_name
    session.workspace_path = str(repo_path)
    session.save(update_fields=['base_ref', 'branch', 'workspace_path', 'updated_at'])
    return sha


def push_branch(project: CodingAgentProject, session: CodingAgentSession) -> Dict[str, Any]:
    repo_path = Path(session.workspace_path or project_repo_dir(project))
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'

    fetch_local = subprocess.run(
        ['git', '-C', str(repo_path), 'fetch', '--quiet', 'origin', session.branch],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    if fetch_local.returncode == 0:
        subprocess.run(
            ['git', '-C', str(repo_path), 'reset', '--hard', f'origin/{session.branch}'],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )

    push_proc = subprocess.run(
        ['git', '-C', str(repo_path), 'push', '-u', 'origin', session.branch],
        capture_output=True,
        text=True,
        env=env,
        timeout=600,
    )
    if push_proc.returncode != 0:
        raise RuntimeError(f'git push failed: {(push_proc.stdout or '')[:200]} {(push_proc.stderr or '')[:800]}')

    remote_proc = subprocess.run(
        ['git', '-C', str(repo_path), 'rev-parse', f'origin/{session.branch}'],
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )
    if remote_proc.returncode != 0:
        raise RuntimeError(f'git rev-parse after push failed: {remote_proc.stderr[:300]}')

    return {
        'remote_sha': remote_proc.stdout.strip(),
        'stdout': push_proc.stdout[:400],
        'stderr': push_proc.stderr[:400],
    }


def open_pull_request(project: CodingAgentProject, session: CodingAgentSession, title: str, body: str) -> Dict[str, Any]:
    import requests

    head = f'{project.repo_owner}:{session.branch}'
    base = project.default_branch
    url = f'https://api.github.com/repos/{project.repo_owner}/{project.repo_name}/pulls'
    headers = {
        'Authorization': f'Bearer {project.access_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    payload = {
        'title': title,
        'body': body,
        'head': head,
        'base': base,
        'maintainer_can_modify': True,
        'draft': False,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code >= 300:
        raise RuntimeError(f'GitHub PR creation failed: {resp.status_code} {resp.text[:500]}')
    data = resp.json()
    return {
        'url': data.get('html_url'),
        'number': data.get('number'),
        'node_id': data.get('node_id'),
        'state': data.get('state'),
    }


def list_user_repos(project_owner_user, access_token: str, refresh: bool = False) -> List[Dict[str, Any]]:
    """List GitHub repos the authenticated user / installation can see."""
    import requests
    from django.core.cache import cache

    cache_key = f'coding_agent:gh_repos:{project_owner_user.id}'
    if not refresh:
        cached = cache.get(cache_key)
        if cached:
            return cached

    repos: List[Dict[str, Any]] = []
    page = 1
    while page < 6:
        resp = requests.get(
            'https://api.github.com/user/repos',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
            },
            params={'per_page': 100, 'page': page, 'sort': 'updated', 'affiliation': 'owner,collaborator,organization_member'},
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(f'GitHub list repos failed: HTTP {resp.status_code}')
        batch = resp.json() or []
        if not batch:
            break
        for r in batch:
            repos.append({
                'id': r.get('id'),
                'full_name': r.get('full_name'),
                'name': r.get('name'),
                'owner': (r.get('owner') or {}).get('login'),
                'description': r.get('description') or '',
                'private': bool(r.get('private')),
                'default_branch': r.get('default_branch') or 'main',
                'html_url': r.get('html_url'),
                'updated_at': r.get('updated_at'),
                'stargazers_count': r.get('stargazers_count') or 0,
                'forks_count': r.get('forks_count') or 0,
                'language': r.get('language') or '',
            })
        if len(batch) < 100:
            break
        page += 1

    cache.set(cache_key, repos, 120)
    return repos


def search_repos(access_token: str, query: str) -> List[Dict[str, Any]]:
    import requests

    if not query:
        return []
    resp = requests.get(
        'https://api.github.com/search/repositories',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        params={'q': query, 'per_page': 25, 'sort': 'updated'},
        timeout=30,
    )
    if resp.status_code != 200:
        return []
    data = resp.json() or {}
    out: List[Dict[str, Any]] = []
    for r in data.get('items') or []:
        out.append({
            'id': r.get('id'),
            'full_name': r.get('full_name'),
            'name': r.get('name'),
            'owner': (r.get('owner') or {}).get('login'),
            'description': r.get('description') or '',
            'private': bool(r.get('private')),
            'default_branch': r.get('default_branch') or 'main',
            'html_url': r.get('html_url'),
            'updated_at': r.get('updated_at'),
            'stargazers_count': r.get('stargazers_count') or 0,
            'forks_count': r.get('forks_count') or 0,
            'language': r.get('language') or '',
        })
    return out


def github_oauth_authorize(client_id: str, redirect_uri: str, state: str, scope: str = 'repo read:user user:email') -> str:
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': scope,
        'allow_signup': 'true',
    }
    return 'https://github.com/login/oauth/authorize?' + urllib.parse.urlencode(params)


def github_exchange_code(client_id: str, client_secret: str, code: str, redirect_uri: str) -> Dict[str, Any]:
    import requests

    resp = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        },
        timeout=20,
    )
    if resp.status_code != 200:
        raise RuntimeError(f'GitHub token exchange failed: HTTP {resp.status_code}')
    data = resp.json() or {}
    if 'error' in data:
        raise RuntimeError(f'GitHub OAuth error: {data.get("error_description") or data.get("error")}')
    if 'access_token' not in data:
        raise RuntimeError('GitHub OAuth response missing access_token')
    return data


def github_user(access_token: str) -> Dict[str, Any]:
    import requests

    resp = requests.get(
        'https://api.github.com/user',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        timeout=20,
    )
    if resp.status_code != 200:
        raise RuntimeError(f'GitHub user fetch failed: HTTP {resp.status_code}')
    return resp.json()


def shutil_rmtree(path: Path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)
