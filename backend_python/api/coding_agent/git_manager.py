"""Git operations manager for the background coding agent.

Handles cloning repos, creating branches, committing changes, pushing,
and creating pull requests via the GitHub API.
"""
import logging
import os
import subprocess

import requests

logger = logging.getLogger(__name__)

GITHUB_API = 'https://api.github.com'


def _run_git(workspace, args, timeout=60):
    """Run a git command in the workspace and return (stdout, stderr, returncode)."""
    try:
        proc = subprocess.run(
            ['git'] + args,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        return '', f'git command timed out after {timeout}s', -1
    except Exception as e:
        return '', str(e), -1


def clone_repo(workspace_parent, repo_url, token, branch=None, depth=1):
    """Clone a repo into the workspace. Returns (workspace_path, error)."""
    repo_name = repo_url.rstrip('/').split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]
    workspace = os.path.join(workspace_parent, repo_name)
    
    if os.path.exists(workspace):
        return workspace, None
    
    clone_url = repo_url
    if token:
        if clone_url.startswith('https://github.com/'):
            clone_url = clone_url.replace(
                'https://github.com/',
                f'https://x-access-token:{token}@github.com/'
            )
    
    cmd = ['git', 'clone', '--depth', str(depth)]
    if branch:
        cmd.extend(['--branch', branch])
    cmd.extend([clone_url, workspace])
    
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            return None, proc.stderr.strip() or 'git clone failed'
        return workspace, None
    except subprocess.TimeoutExpired:
        return None, 'git clone timed out after 120s'
    except Exception as e:
        return None, str(e)


def create_branch(workspace, branch_name, base_branch='main'):
    """Create and checkout a new branch from the base branch."""
    stdout, stderr, rc = _run_git(workspace, ['checkout', base_branch], timeout=30)
    if rc != 0:
        stdout2, stderr2, rc2 = _run_git(workspace, ['checkout', '-b', branch_name], timeout=30)
        if rc2 != 0:
            return False, f'Failed to checkout base branch: {stderr}; {stderr2}'
        return True, f'Created and checked out new branch: {branch_name}'
    
    _run_git(workspace, ['pull', '--ff-only', 'origin', base_branch], timeout=30)
    
    stdout, stderr, rc = _run_git(workspace, ['checkout', '-b', branch_name], timeout=30)
    if rc != 0:
        stdout, stderr, rc = _run_git(workspace, ['checkout', branch_name], timeout=30)
        if rc != 0:
            return False, f'Failed to create/checkout branch {branch_name}: {stderr}'
        return True, f'Checked out existing branch: {branch_name}'
    return True, f'Created and checked out new branch: {branch_name}'


def get_default_branch(workspace):
    """Get the default branch of the repo."""
    stdout, stderr, rc = _run_git(workspace, ['symbolic-ref', '--short', 'refs/remotes/origin/HEAD'], timeout=15)
    if rc == 0 and stdout:
        return stdout.replace('origin/', '').strip()
    stdout, stderr, rc = _run_git(workspace, ['rev-parse', '--abbrev-ref', 'HEAD'], timeout=15)
    if rc == 0 and stdout:
        return stdout.strip()
    return 'main'


def commit_all(workspace, message):
    """Stage all changes and commit."""
    _run_git(workspace, ['add', '-A'], timeout=30)
    
    stdout, stderr, rc = _run_git(workspace, ['status', '--porcelain'], timeout=15)
    if not stdout:
        return False, 'No changes to commit'
    
    stdout, stderr, rc = _run_git(workspace, ['commit', '-m', message], timeout=30)
    if rc != 0:
        return False, f'Commit failed: {stderr}'
    return True, f'Committed: {message}'


def push_branch(workspace, branch_name, token, remote_url):
    """Push the branch to the remote."""
    push_url = remote_url
    if token and push_url.startswith('https://github.com/'):
        push_url = push_url.replace(
            'https://github.com/',
            f'https://x-access-token:{token}@github.com/'
        )
    
    stdout, stderr, rc = _run_git(
        workspace,
        ['push', '-u', push_url, branch_name],
        timeout=60,
    )
    if rc != 0:
        return False, f'Push failed: {stderr}'
    return True, f'Pushed branch: {branch_name}'


def create_pull_request(token, repo_full_name, branch_name, base_branch, title, body):
    """Create a pull request via the GitHub API. Returns (pr_url, pr_number, error)."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    data = {
        'title': title,
        'body': body,
        'head': branch_name,
        'base': base_branch,
    }
    try:
        resp = requests.post(
            f'{GITHUB_API}/repos/{repo_full_name}/pulls',
            json=data,
            headers=headers,
            timeout=30,
        )
        if resp.status_code == 201:
            pr_data = resp.json()
            return pr_data.get('html_url', ''), pr_data.get('number'), None
        elif resp.status_code == 422:
            error_msg = resp.json().get('message', 'PR creation failed')
            errors = resp.json().get('errors', [])
            if errors:
                error_msg += ': ' + ', '.join(e.get('message', '') for e in errors)
            return '', None, error_msg
        else:
            return '', None, f'GitHub API error {resp.status_code}: {resp.text[:200]}'
    except Exception as e:
        return '', None, str(e)


def get_changed_files(workspace):
    """Get list of changed files compared to the base branch."""
    stdout, stderr, rc = _run_git(workspace, ['diff', '--name-only', 'HEAD~1'], timeout=15)
    if rc == 0 and stdout:
        return stdout.split('\n')
    
    stdout, stderr, rc = _run_git(workspace, ['diff', '--name-only', '--staged'], timeout=15)
    if rc == 0 and stdout:
        return stdout.split('\n')
    
    stdout, stderr, rc = _run_git(workspace, ['status', '--porcelain'], timeout=15)
    if rc == 0 and stdout:
        return [line[3:].strip() for line in stdout.split('\n') if line.strip()]
    return []


def get_diff_summary(workspace, max_files=20):
    """Get a summary of all changes (file stats + truncated diffs)."""
    stdout, stderr, rc = _run_git(workspace, ['diff', '--stat'], timeout=15)
    if not stdout:
        stdout, stderr, rc = _run_git(workspace, ['diff', '--staged', '--stat'], timeout=15)
    return stdout or '(no changes)'


def get_full_diff(workspace, max_chars=50000):
    """Get the full diff of all uncommitted changes."""
    stdout, stderr, rc = _run_git(workspace, ['diff', 'HEAD'], timeout=30)
    if not stdout:
        stdout, stderr, rc = _run_git(workspace, ['diff', '--staged'], timeout=30)
    if not stdout:
        stdout, stderr, rc = _run_git(workspace, ['diff'], timeout=30)
    diff = stdout or '(no changes)'
    if len(diff) > max_chars:
        diff = diff[:max_chars] + f'\n... (truncated at {max_chars} chars)'
    return diff


def generate_branch_name(task_title, task_id):
    """Generate a safe branch name from a task title and ID."""
    import re
    safe = re.sub(r'[^a-zA-Z0-9\s_-]', '', task_title.lower())[:50]
    safe = re.sub(r'[\s_]+', '-', safe.strip('-'))
    if not safe:
        safe = 'task'
    return f'coding-agent/{safe}-{task_id[:8]}'


def create_zip_archive(workspace, output_path):
    """Create a zip archive of the workspace (excluding .git)."""
    import zipfile
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(workspace):
            dirs[:] = [d for d in dirs if d != '.git']
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, workspace)
                zf.write(file_path, arcname)
    return output_path
