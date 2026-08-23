"""Read and summarize recent Git commits for blog post generation."""
import logging
import os
import subprocess
from typing import List, Dict

logger = logging.getLogger(__name__)

# Patterns to filter out non-user-facing commits
IGNORE_PREFIXES = (
    'merge ',
    'merge branch',
    'chore(ci)',
    'chore(deploy)',
    'chore: deploy',
    'deploy:',
    'bump ',
    'lint:',
    'cleanup:',
    'wip:',
)


def get_recent_commits(limit: int = 35, repo_dir: str = None) -> List[Dict[str, str]]:
    """Retrieve recent commits from the git repository formatted cleanly."""
    if not repo_dir:
        # Default to repo root (2 levels above backend_python/api/agent_blog)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            repo_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

    try:
        cmd = ['git', 'log', f'-n {limit}', '--pretty=format:%h|||%s|||%b|||%an|||%ad', '--date=short']
        result = subprocess.run(
            cmd,
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace',
        )
        if result.returncode != 0:
            logger.warning('git_reader: git log failed with returncode %s', result.returncode)
            return []

        commits = []
        raw_lines = result.stdout.strip().split('\n')
        for line in raw_lines:
            if not line.strip():
                continue
            parts = line.split('|||')
            if len(parts) < 2:
                continue
            hash_code = parts[0].strip()
            subject = parts[1].strip()
            body = parts[2].strip() if len(parts) > 2 else ''
            author = parts[3].strip() if len(parts) > 3 else ''
            date = parts[4].strip() if len(parts) > 4 else ''

            # Skip noise
            lower_sub = subject.lower()
            if any(lower_sub.startswith(p) for p in IGNORE_PREFIXES):
                continue
            if 'merge ' in lower_sub or 'checkpoint' in lower_sub:
                continue

            commits.append({
                'hash': hash_code,
                'subject': subject,
                'body': body,
                'author': author,
                'date': date,
            })
        return commits
    except Exception as e:
        logger.warning('git_reader: failed to read git commits: %s', e)
        return []


def format_commits_for_prompt(commits: List[Dict[str, str]], max_items: int = 15) -> str:
    """Format commits into a human-readable list for LLM context."""
    if not commits:
        return (
            "- Neby Canvas: Living knowledge maps, interactive concept reasoning, and markdown notes.\n"
            "- Interactive 3D Labs: Physics mechanics, Optics, and Biology 3D simulations.\n"
            "- Smart PDF Viewer: In-book highlighting, bookmarks, and offline study materials.\n"
            "- Study Spaces & Focus Timers: Pomodoro sessions and peer collaborative rooms.\n"
            "- Cosmetics Store: Dynamic Material 3 themes, animated profile banners, and subject badges."
        )

    lines = []
    for c in commits[:max_items]:
        line = f"- {c['subject']} ({c.get('date', '')})"
        lines.append(line)
    return "\n".join(lines)
