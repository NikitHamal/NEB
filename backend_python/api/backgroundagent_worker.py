import os
import subprocess
import logging
import re
import urllib.parse
from django.conf import settings
from api.models import BackgroundAgentSession, BackgroundAgentMessage
from api.utils import now_ms, uuid_str
from api.neby import call_ai_api

logger = logging.getLogger(__name__)

def get_repo_dir(session_id):
    return f"/tmp/nebians_agent_{session_id}"

def execute_git_command(command, cwd):
    try:
        result = subprocess.run(
            command, cwd=cwd, text=True, capture_output=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")
        raise Exception(f"Git error: {e.stderr}")

def setup_repo(session):
    repo_dir = get_repo_dir(session.id)
    if os.path.exists(repo_dir):
        return # Already cloned

    repo_url = session.repo_url

    # If the user has a linked github token, we could inject it here.
    # For now, if they provided a private repo URL, they should include the token.
    # We will assume public or token-embedded URL.

    logger.info(f"Cloning {repo_url} into {repo_dir} for session {session.id}")

    # Update status
    _add_message(session, "agent", "Cloning repository...")

    os.makedirs(repo_dir, exist_ok=True)
    try:
        execute_git_command(["git", "clone", repo_url, "."], cwd=repo_dir)

        # Create new branch
        execute_git_command(["git", "checkout", "-b", session.branch_name], cwd=repo_dir)

        _add_message(session, "agent", f"Repository cloned and checked out to branch `{session.branch_name}`.")

    except Exception as e:
        _add_message(session, "agent", f"Failed to setup repository: {str(e)}")
        session.status = 'failed'
        session.save(update_fields=['status'])
        raise e

def push_and_create_pr(session):
    repo_dir = get_repo_dir(session.id)
    _add_message(session, "agent", "Committing and pushing changes...")
    try:
        execute_git_command(["git", "add", "."], cwd=repo_dir)
        # Check if there are changes
        status = execute_git_command(["git", "status", "--porcelain"], cwd=repo_dir)
        if not status.strip():
            _add_message(session, "agent", "No changes to commit.")
            session.status = 'done'
            session.save(update_fields=['status'])
            return

        commit_msg = f"Agent changes for session {session.id}\n\nGoal: {session.goal}"
        # We need to configure git user for the commit
        execute_git_command(["git", "config", "user.email", "agent@nebians.com"], cwd=repo_dir)
        execute_git_command(["git", "config", "user.name", "NEBians Agent"], cwd=repo_dir)

        execute_git_command(["git", "commit", "-m", commit_msg], cwd=repo_dir)

        # Push
        execute_git_command(["git", "push", "-u", "origin", session.branch_name], cwd=repo_dir)

        # In a real scenario, use GitHub API to open a PR. For now, just print the URL.
        # Assuming github.com URL:
        if "github.com" in session.repo_url:
            base_url = session.repo_url
            if base_url.endswith(".git"):
                base_url = base_url[:-4]
            pr_url = f"{base_url}/pull/new/{session.branch_name}"
            _add_message(session, "agent", f"Changes pushed! Open a PR here: {pr_url}")
        else:
            _add_message(session, "agent", f"Changes pushed to branch {session.branch_name}.")

        session.status = 'done'
        session.save(update_fields=['status'])

    except Exception as e:
        _add_message(session, "agent", f"Failed to push/PR: {str(e)}")
        session.status = 'failed'
        session.save(update_fields=['status'])

def _add_message(session, role, content):
    BackgroundAgentMessage.objects.create(
        id=uuid_str(),
        session=session,
        role=role,
        content=content,
        created_at=now_ms()
    )

def list_project_files(repo_dir):
    files = []
    for root, dirnames, filenames in os.walk(repo_dir):
        if '.git' in dirnames:
            dirnames.remove('.git')
        if 'node_modules' in dirnames:
            dirnames.remove('node_modules')
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, repo_dir)
            files.append(rel_path)
    return files

def read_file_content(repo_dir, file_path):
    full_path = os.path.join(repo_dir, file_path)
    if not os.path.exists(full_path):
        return None
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def write_file_content(repo_dir, file_path, content):
    # Prevent path traversal
    clean_path = os.path.normpath(file_path).lstrip('/')
    if ".." in clean_path.split(os.sep):
        raise ValueError("Invalid file path")
    full_path = os.path.join(repo_dir, clean_path)
    # Ensure it's inside repo_dir
    if not os.path.abspath(full_path).startswith(os.path.abspath(repo_dir)):
        raise ValueError("Invalid file path")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def apply_code_changes(session, response_text):
    repo_dir = get_repo_dir(session.id)

    # We expect the AI to output blocks like:
    # FILE: path/to/file.py
    # ```python
    # ... content ...
    # ```

    file_blocks = re.split(r'FILE:\s*([^\n]+)', response_text)
    if len(file_blocks) < 2:
        return False

    changes_made = 0
    # file_blocks[0] is preamble.
    # file_blocks[1] is file1 path, file_blocks[2] is file1 content, etc.
    for i in range(1, len(file_blocks), 2):
        file_path = file_blocks[i].strip()
        block_content = file_blocks[i+1]

        # Extract code inside ```...```
        code_match = re.search(r'```[a-zA-Z]*\n(.*?)\n```', block_content, re.DOTALL)
        if code_match:
            new_code = code_match.group(1)
            write_file_content(repo_dir, file_path, new_code)
            changes_made += 1

    return changes_made > 0


def execute_agent_step(session):
    repo_dir = get_repo_dir(session.id)

    if not os.path.exists(repo_dir):
        setup_repo(session)
        if session.status == 'failed': return

    # Get conversation history
    messages = session.messages.all().order_by('created_at')

    # Build prompt
    prompt = "You are a background coding agent.\n"
    prompt += f"The user's goal is: {session.goal}\n\n"

    # Provide file list context
    files = list_project_files(repo_dir)
    prompt += "Here are the files in the project:\n"
    prompt += "\n".join(files[:100]) # Limit to 100 for brevity
    prompt += "\n\n"

    # If there's a specific file mentioned in conversation, we could read it, but for simplicity:
    prompt += "To make changes, output the full file content in the following format exactly:\n"
    prompt += "FILE: path/to/file.py\n```python\n[full file content here]\n```\n\n"

    prompt += "Conversation history:\n"
    for m in messages:
        prompt += f"{m.role}: {m.content}\n"

    prompt += "\nagent: "

    _add_message(session, "agent", "Thinking and generating code changes...")

    try:
        response_text = call_ai_api(None, prompt) # use default config
        if not response_text:
            _add_message(session, "agent", "Failed to get response from AI.")
            session.status = 'failed'
            session.save(update_fields=['status'])
            return

        _add_message(session, "agent", response_text)

        # Apply changes
        if apply_code_changes(session, response_text):
            _add_message(session, "agent", "Code changes applied to the local repository.")
        else:
            _add_message(session, "agent", "No valid code blocks found to apply.")

        # Pause after a step to allow user to review
        session.status = 'paused'
        session.updated_at = now_ms()
        session.save(update_fields=['status', 'updated_at'])

    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        _add_message(session, "agent", f"Error during execution: {str(e)}")
        session.status = 'failed'
        session.save(update_fields=['status'])

def process_pending_sessions():
    sessions = BackgroundAgentSession.objects.filter(status='running')
    for session in sessions:
        try:
            execute_agent_step(session)
        except Exception as e:
            logger.error(f"Failed to process session {session.id}: {e}")
            session.status = 'failed'
            session.save(update_fields=['status'])

    # Also handle push requests
    push_sessions = BackgroundAgentSession.objects.filter(status='pushing')
    for session in push_sessions:
        try:
            push_and_create_pr(session)
        except Exception as e:
            logger.error(f"Failed to push session {session.id}: {e}")
