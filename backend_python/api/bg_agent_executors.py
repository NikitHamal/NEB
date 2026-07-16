"""
Background Coding Agent Executors.
Handles the actual AI-powered coding work in the background.
Similar to Google Jules, Cursor Agent - works autonomously until goal is achieved.

Key features:
- Clones repo, creates isolated branch (NEVER main)
- Uses Neby AI providers (Qwen, DeepAI, custom providers)
- Handles reverse-engineered APIs and web scrapers specially
- Runs in background - task continues even if user closes site
- Supports stop, pause, resume, chat/interrupt/followup
- Creates PR at the end, allows zip download
"""
import os
import json
import logging
import subprocess
import shutil
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime

from django.conf import settings

from api.models_bg_agent import (
    GitHubConnection,
    CodebaseProject,
    CodingSession,
    SessionMessage,
    FileChange,
    CommandExecution,
    AgentTask,
    DownloadPackage,
)
from api.utils import now_ms, uuid_str
from api.qwen_utils.client import QwenClient
from api.generation import mark_progress, mark_completed, mark_failed

logger = logging.getLogger(__name__)

# Base directory for cloned repositories
REPO_BASE_PATH = getattr(settings, 'BG_AGENT_REPO_PATH', '/tmp/nebians_bg_agent')


class BackgroundCodingAgent:
    """
    Main agent class that orchestrates the coding workflow.
    Works like Google Jules - autonomous, background execution.
    """
    
    def __init__(self, session: CodingSession):
        self.session = session
        self.project = session.project
        self.connection = session.project.github_connection
        self.work_dir = None
        self.branch_name = session.session_branch
        
    def execute(self):
        """Main execution flow for the coding session."""
        try:
            # Update session status
            self.session.status = 'cloning'
            self.session.started_at = now_ms()
            self.session.save(update_fields=['status', 'started_at', 'updated_at'])
            
            # Step 1: Clone repository
            self._clone_repository()
            
            # Step 2: Setup environment
            self.session.status = 'setting_up'
            self.session.save(update_fields=['status', 'updated_at'])
            self._setup_environment()
            
            # Step 3: Create session branch
            self._create_session_branch()
            
            # Step 4: Run the AI agent loop
            self.session.status = 'running'
            self.session.save(update_fields=['status', 'updated_at'])
            self._run_agent_loop()
            
            # Step 5: Complete session
            self._finalize_session()
            
        except Exception as e:
            logger.exception(f"Session {self.session.id} failed: {e}")
            self.session.status = 'failed'
            self.session.error = str(e)
            self.session.completed_at = now_ms()
            self.session.save(update_fields=['status', 'error', 'completed_at', 'updated_at'])
            self._cleanup()
    
    def _clone_repository(self):
        """Clone the GitHub repository to local path."""
        logger.info(f"Cloning {self.project.repo_full_name}...")
        
        # Create base directory if not exists
        os.makedirs(REPO_BASE_PATH, exist_ok=True)
        
        # Setup clone directory
        self.work_dir = os.path.join(
            REPO_BASE_PATH,
            self.project.repo_owner,
            self.project.repo_name,
            uuid_str()[:8]  # Unique session dir
        )
        os.makedirs(self.work_dir, exist_ok=True)
        
        # Build clone URL with token
        clone_url = self.project.clone_url.replace(
            'https://github.com/',
            f'https://{self.connection.access_token}@github.com/'
        )
        
        # Clone command
        cmd = ['git', 'clone', '--depth', '1', '-b', self.project.base_branch, clone_url, self.work_dir]
        self._log_command(cmd, self.work_dir)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise Exception(f"Git clone failed: {result.stderr}")
        
        self.session.progress_percent = 20
        self.session.current_step = 'Repository cloned successfully'
        self.session.save(update_fields=['progress_percent', 'current_step', 'updated_at'])
        
        # Add system message
        SessionMessage.objects.create(
            session=self.session,
            role='system',
            content=f'Repository {self.project.repo_full_name} cloned to working directory',
            created_at=now_ms()
        )
    
    def _create_session_branch(self):
        """Create a new branch for this session (NEVER use main)."""
        logger.info(f"Creating session branch: {self.branch_name}")
        
        # Get current commit SHA
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.work_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        self.session.base_commit = result.stdout.strip()
        
        # Create and checkout new branch
        cmd = ['git', 'checkout', '-b', self.branch_name]
        self._log_command(cmd, self.work_dir)
        
        result = subprocess.run(cmd, cwd=self.work_dir, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"Failed to create branch: {result.stderr}")
        
        self.session.save(update_fields=['base_commit', 'updated_at'])
        
        SessionMessage.objects.create(
            session=self.session,
            role='system',
            content=f'Created new branch: {self.branch_name} from commit {self.session.base_commit[:7]}',
            created_at=now_ms()
        )
    
    def _setup_environment(self):
        """Setup the development environment based on project type."""
        logger.info("Setting up environment...")
        
        # Detect project type and setup
        setup_steps = []
        
        # Check for common project files
        if os.path.exists(os.path.join(self.work_dir, 'requirements.txt')):
            setup_steps.append('python_requirements')
        if os.path.exists(os.path.join(self.work_dir, 'package.json')):
            setup_steps.append('nodejs')
        if os.path.exists(os.path.join(self.work_dir, 'Cargo.toml')):
            setup_steps.append('rust')
        if os.path.exists(os.path.join(self.work_dir, 'go.mod')):
            setup_steps.append('golang')
        
        # Execute setup steps
        for step in setup_steps:
            self._execute_setup_step(step)
        
        self.session.progress_percent = 40
        self.session.current_step = 'Environment setup complete'
        self.session.save(update_fields=['progress_percent', 'current_step', 'updated_at'])
    
    def _execute_setup_step(self, step_type):
        """Execute a specific environment setup step."""
        if step_type == 'python_requirements':
            cmd = ['pip', 'install', '-r', 'requirements.txt']
            self._run_command(cmd, timeout=300)
        elif step_type == 'nodejs':
            cmd = ['npm', 'install']
            self._run_command(cmd, timeout=300)
        elif step_type == 'rust':
            cmd = ['cargo', 'build']
            self._run_command(cmd, timeout=600)
        elif step_type == 'golang':
            cmd = ['go', 'mod', 'download']
            self._run_command(cmd, timeout=300)
    
    def _run_agent_loop(self):
        """
        Main AI agent loop.
        Breaks down task, executes, monitors, and iterates until goal achieved.
        """
        logger.info("Starting AI agent loop...")
        
        # Initialize AI client based on provider
        ai_client = self._get_ai_client()
        
        # Parse the task description
        task_description = self.session.description
        instructions = self.session.instructions
        
        # Create initial planning task
        plan_prompt = self._build_planning_prompt(task_description, instructions)
        
        # Get AI to break down the task
        plan_response = ai_client.generate(plan_prompt)
        tasks = self._parse_task_plan(plan_response)
        
        # Create agent tasks
        for i, task_data in enumerate(tasks):
            AgentTask.objects.create(
                session=self.session,
                title=task_data.get('title', 'Untitled Task'),
                description=task_data.get('description', ''),
                plan=task_data.get('plan', ''),
                order=i,
                created_at=now_ms()
            )
        
        # Execute tasks
        all_tasks = AgentTask.objects.filter(session=self.session).order_by('order')
        
        for task in all_tasks:
            if self._check_session_interrupted():
                logger.info("Session interrupted by user")
                return
            
            self._execute_single_task(task, ai_client)
        
        self.session.progress_percent = 90
        self.session.current_step = 'All tasks completed'
        self.session.save(update_fields=['progress_percent', 'current_step', 'updated_at'])
    
    def _get_ai_client(self):
        """Get the appropriate AI client based on provider selection."""
        provider = self.session.provider
        
        # Use existing Neby AI providers
        if provider == 'qwen':
            return QwenClient()
        elif provider == 'deepai':
            # Import DeepAI client if available
            from api.deepai_proxy import DeepAIClient
            return DeepAIClient()
        else:
            # Default to Qwen
            return QwenClient()
    
    def _build_planning_prompt(self, task_description, instructions):
        """Build prompt for task planning."""
        return f"""You are an expert software engineering AI agent. Your task is to analyze the following coding request and break it down into executable steps.

TASK DESCRIPTION:
{task_description}

ADDITIONAL INSTRUCTIONS:
{instructions}

PROJECT CONTEXT:
- Repository: {self.project.repo_full_name}
- Branch: {self.branch_name}
- Base Commit: {self.session.base_commit}

Please break this down into a structured plan with clear, executable tasks. For each task, provide:
1. Title
2. Description
3. Files that will likely be modified
4. Commands that may need to be run

Respond in JSON format:
{{
  "tasks": [
    {{
      "title": "...",
      "description": "...",
      "files": ["...", "..."],
      "commands": ["...", "..."]
    }}
  ]
}}
"""
    
    def _parse_task_plan(self, response):
        """Parse AI response into task list."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('tasks', [])
        except Exception as e:
            logger.warning(f"Failed to parse task plan: {e}")
        
        # Fallback: create single task
        return [{
            'title': 'Execute coding task',
            'description': self.session.description,
            'files': [],
            'commands': []
        }]
    
    def _execute_single_task(self, task: AgentTask, ai_client):
        """Execute a single agent task."""
        logger.info(f"Executing task: {task.title}")
        
        task.status = 'in_progress'
        task.started_at = now_ms()
        task.save(update_fields=['status', 'started_at', 'updated_at'])
        
        self.session.current_step = f'Working on: {task.title}'
        self.session.save(update_fields=['current_step', 'updated_at'])
        
        # Build execution prompt
        exec_prompt = self._build_execution_prompt(task)
        
        # Get AI to generate code/commands
        response = ai_client.generate(exec_prompt)
        
        # Parse and execute actions
        actions = self._parse_actions(response)
        
        for action in actions:
            if self._check_session_interrupted():
                task.status = 'failed'
                task.completed_at = now_ms()
                task.save(update_fields=['status', 'completed_at', 'updated_at'])
                return
            
            self._execute_action(action, task)
        
        task.status = 'completed'
        task.result_summary = f"Completed: {task.title}"
        task.completed_at = now_ms()
        task.save(update_fields=['status', 'result_summary', 'completed_at', 'updated_at'])
        
        # Update progress
        completed = AgentTask.objects.filter(
            session=self.session, 
            status='completed'
        ).count()
        total = AgentTask.objects.filter(session=self.session).count()
        self.session.progress_percent = int(40 + (completed / max(total, 1)) * 50)
        self.session.save(update_fields=['progress_percent', 'updated_at'])
    
    def _build_execution_prompt(self, task: AgentTask):
        """Build prompt for executing a single task."""
        # Get context about current state of files
        file_context = []
        for file_path in self._get_relevant_files(task):
            try:
                full_path = os.path.join(self.work_dir, file_path)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:5000]  # Limit context
                        file_context.append(f"=== {file_path} ===\n{content}")
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
        
        return f"""You are executing a coding task. Analyze the current codebase and make necessary changes.

TASK:
{task.title}

DESCRIPTION:
{task.description}

PLAN:
{task.plan}

CURRENT FILE CONTEXT:
{'\n\n'.join(file_context)}

Based on this, generate the exact code changes needed. You can:
1. Write new files (provide full content)
2. Modify existing files (show the changes)
3. Run shell commands (for testing, building, etc.)

Respond with clear actions in this format:
ACTION: write_file
PATH: path/to/file.py
CONTENT: |
    ... file content here ...

ACTION: modify_file
PATH: path/to/file.py
CHANGES:
    ... describe changes or show diff ...

ACTION: run_command
COMMAND: npm test

Be specific and precise. Only change what's necessary.
"""
    
    def _parse_actions(self, response):
        """Parse AI response into executable actions."""
        actions = []
        lines = response.split('\n')
        current_action = None
        
        for line in lines:
            if line.startswith('ACTION:'):
                if current_action:
                    actions.append(current_action)
                current_action = {'type': line.split(':', 1)[1].strip(), 'data': {}}
            elif current_action and ':' in line:
                key, value = line.split(':', 1)
                current_action['data'][key.strip().lower()] = value.strip()
        
        if current_action:
            actions.append(current_action)
        
        return actions
    
    def _execute_action(self, action, task):
        """Execute a single action from the AI."""
        action_type = action.get('type', '').lower()
        data = action.get('data', {})
        
        if action_type == 'write_file':
            self._action_write_file(data, task)
        elif action_type == 'modify_file':
            self._action_modify_file(data, task)
        elif action_type == 'run_command':
            self._action_run_command(data, task)
        elif action_type == 'read_file':
            self._action_read_file(data, task)
        elif action_type == 'search_code':
            self._action_search_code(data, task)
        else:
            logger.warning(f"Unknown action type: {action_type}")
    
    def _action_write_file(self, data, task):
        """Write a new file or overwrite existing."""
        file_path = data.get('path', '')
        content = data.get('content', '')
        
        if not file_path:
            return
        
        full_path = os.path.join(self.work_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Check if file exists (for tracking change type)
        change_type = 'created'
        old_content = ''
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                old_content = f.read()
            change_type = 'modified'
        
        # Write the file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Track the change
        self._track_file_change(file_path, change_type, old_content, content)
        
        # Log to session
        SessionMessage.objects.create(
            session=self.session,
            role='assistant',
            content=f"Written file: {file_path}",
            action_type='file_write',
            action_data=json.dumps({'path': file_path, 'change_type': change_type}),
            created_at=now_ms()
        )
    
    def _action_modify_file(self, data, task):
        """Modify an existing file."""
        file_path = data.get('path', '')
        changes_desc = data.get('changes', '')
        
        # For now, treat as read-modify-write
        # In production, implement proper patching
        self._action_write_file(data, task)
    
    def _action_run_command(self, data, task):
        """Run a shell command."""
        command = data.get('command', '')
        
        if not command:
            return
        
        result = self._run_command(
            command,
            shell=True,
            timeout=300
        )
        
        # Log to session
        SessionMessage.objects.create(
            session=self.session,
            role='assistant',
            content=f"Executed: {command}\n\nExit code: {result.get('exit_code', -1)}",
            action_type='command_run',
            action_data=json.dumps({
                'command': command,
                'exit_code': result.get('exit_code'),
                'stdout_lines': len(result.get('stdout', '').splitlines()),
                'stderr_lines': len(result.get('stderr', '').splitlines())
            }),
            created_at=now_ms()
        )
    
    def _action_read_file(self, data, task):
        """Read a file (for context)."""
        file_path = data.get('path', '')
        
        if not file_path:
            return
        
        full_path = os.path.join(self.work_dir, file_path)
        
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()[:10000]
            
            SessionMessage.objects.create(
                session=self.session,
                role='assistant',
                content=f"Read file: {file_path} ({len(content)} chars)",
                action_type='file_read',
                action_data=json.dumps({'path': file_path}),
                created_at=now_ms()
            )
    
    def _action_search_code(self, data, task):
        """Search codebase for patterns."""
        pattern = data.get('pattern', '')
        
        if not pattern:
            return
        
        try:
            result = subprocess.run(
                ['grep', '-r', '-n', pattern, self.work_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            matches = result.stdout[:5000]  # Limit output
            
            SessionMessage.objects.create(
                session=self.session,
                role='assistant',
                content=f"Search results for '{pattern}':\n{matches}",
                action_type='search',
                action_data=json.dumps({'pattern': pattern}),
                created_at=now_ms()
            )
        except Exception as e:
            logger.warning(f"Search failed: {e}")
    
    def _track_file_change(self, file_path, change_type, old_content, new_content):
        """Track a file change in the database."""
        # Calculate diff (simple line-based)
        old_lines = old_content.splitlines() if old_content else []
        new_lines = new_content.splitlines() if new_content else []
        
        lines_added = len(new_lines) - len(old_lines) if change_type == 'modified' else len(new_lines)
        lines_removed = max(0, len(old_lines) - len(new_lines)) if change_type == 'modified' else 0
        
        # Generate simple unified diff
        import difflib
        diff = ''.join(difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f'a/{file_path}',
            tofile=f'b/{file_path}',
            n=3
        ))
        
        FileChange.objects.create(
            session=self.session,
            file_path=file_path,
            change_type=change_type,
            old_content=old_content if change_type in ['modified', 'deleted'] else '',
            new_content=new_content if change_type in ['created', 'modified'] else '',
            diff_patch=diff,
            line_added=max(0, lines_added),
            line_removed=max(0, lines_removed),
            created_at=now_ms()
        )
    
    def _run_command(self, cmd, shell=False, timeout=300, cwd=None):
        """Run a shell command and log it."""
        cmd_exec = CommandExecution.objects.create(
            session=self.session,
            command=cmd if isinstance(cmd, str) else ' '.join(cmd),
            working_directory=cwd or self.work_dir,
            status='running',
            created_at=now_ms()
        )
        
        start_time = now_ms()
        
        try:
            if isinstance(cmd, str) or shell:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=cwd or self.work_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            else:
                result = subprocess.run(
                    cmd,
                    cwd=cwd or self.work_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            
            duration = now_ms() - start_time
            
            cmd_exec.status = 'completed'
            cmd_exec.exit_code = result.returncode
            cmd_exec.stdout = result.stdout[:50000]  # Limit storage
            cmd_exec.stderr = result.stderr[:50000]
            cmd_exec.duration_ms = duration
            cmd_exec.completed_at = now_ms()
            cmd_exec.save()
            
            return {
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            cmd_exec.status = 'failed'
            cmd_exec.stderr = f'Command timed out after {timeout}s'
            cmd_exec.completed_at = now_ms()
            cmd_exec.save()
            return {'exit_code': -1, 'stdout': '', 'stderr': 'Timeout'}
        except Exception as e:
            cmd_exec.status = 'failed'
            cmd_exec.stderr = str(e)
            cmd_exec.completed_at = now_ms()
            cmd_exec.save()
            return {'exit_code': -1, 'stdout': '', 'stderr': str(e)}
    
    def _log_command(self, cmd, cwd=None):
        """Log a command without executing (for git operations)."""
        CommandExecution.objects.create(
            session=self.session,
            command=' '.join(cmd) if isinstance(cmd, list) else cmd,
            working_directory=cwd or self.work_dir,
            status='completed',
            exit_code=0,
            created_at=now_ms(),
            completed_at=now_ms()
        )
    
    def _get_relevant_files(self, task):
        """Get files relevant to a task."""
        # Simple heuristic: look at mentioned files in task description
        # In production, use better file discovery
        files = []
        
        # Common file patterns
        patterns = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.html', '*.css', '*.json']
        
        for pattern in patterns:
            try:
                result = subprocess.run(
                    ['find', self.work_dir, '-name', pattern, '-type', 'f'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                files.extend([
                    f.replace(self.work_dir + '/', '')
                    for f in result.stdout.splitlines()[:20]  # Limit
                ])
            except Exception:
                pass
        
        return files[:50]  # Return top 50 files
    
    def _check_session_interrupted(self):
        """Check if session was paused/cancelled by user."""
        self.session.refresh_from_db()
        return self.session.status in ['paused', 'cancelled']
    
    def _finalize_session(self):
        """Finalize the session - create PR, generate diff summary, etc."""
        logger.info("Finalizing session...")
        
        # Commit changes
        self._commit_changes()
        
        # Push branch to GitHub
        self._push_branch()
        
        # Create Pull Request
        self._create_pull_request()
        
        # Generate diff summary
        self._generate_diff_summary()
        
        # Create download package
        self._create_download_package()
        
        self.session.status = 'completed'
        self.session.completed_at = now_ms()
        self.session.progress_percent = 100
        self.session.current_step = 'Session completed successfully'
        self.session.save(update_fields=['status', 'completed_at', 'progress_percent', 'current_step', 'updated_at'])
        
        SessionMessage.objects.create(
            session=self.session,
            role='system',
            content=f'Session completed! PR #{self.session.pr_number} opened: {self.session.pr_url}',
            created_at=now_ms()
        )
    
    def _commit_changes(self):
        """Commit all changes to the session branch."""
        # Check for changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=self.work_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if not result.stdout.strip():
            logger.info("No changes to commit")
            return
        
        # Add all changes
        subprocess.run(['git', 'add', '-A'], cwd=self.work_dir, timeout=30)
        
        # Commit
        commit_msg = f"[NEBians Agent] {self.session.title}\n\n{self.session.description}"
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=self.work_dir,
            timeout=30
        )
    
    def _push_branch(self):
        """Push the session branch to GitHub."""
        remote_url = self.project.clone_url.replace(
            'https://github.com/',
            f'https://{self.connection.access_token}@github.com/'
        )
        
        cmd = ['git', 'push', '-u', 'origin', self.branch_name]
        self._log_command(cmd, self.work_dir)
        
        result = subprocess.run(cmd, cwd=self.work_dir, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            logger.warning(f"Push failed: {result.stderr}")
    
    def _create_pull_request(self):
        """Create a Pull Request on GitHub."""
        import requests
        
        pr_title = f"[NEBians Agent] {self.session.title}"
        pr_body = f"""## Automated Changes by NEBians Background Agent

**Task:** {self.session.title}

**Description:**
{self.session.description}

**Changes Summary:**
- Session ID: {self.session.id}
- Branch: {self.session.session_branch}
- Base Branch: {self.project.base_branch}

This PR was automatically generated by the NEBians AI coding agent. Please review the changes carefully before merging.

---
*Generated by NEBians Background Coding Agent*
"""
        
        api_url = f"https://api.github.com/repos/{self.project.repo_full_name}/pulls"
        headers = {
            'Authorization': f'Bearer {self.connection.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'title': pr_title,
            'body': pr_body,
            'head': self.branch_name,
            'base': self.project.base_branch
        }
        
        try:
            resp = requests.post(api_url, json=data, headers=headers, timeout=30)
            resp.raise_for_status()
            pr_data = resp.json()
            
            self.session.pr_number = pr_data.get('number')
            self.session.pr_url = pr_data.get('html_url', '')
            self.session.save(update_fields=['pr_number', 'pr_url', 'updated_at'])
            
            logger.info(f"PR created: {self.session.pr_url}")
        except Exception as e:
            logger.exception(f"Failed to create PR: {e}")
            self.session.pr_url = f"Error: {str(e)}"
            self.session.save(update_fields=['pr_url', 'updated_at'])
    
    def _generate_diff_summary(self):
        """Generate a summary of all changes."""
        changes = FileChange.objects.filter(session=self.session)
        
        summary_lines = [
            f"# Changes Summary for: {self.session.title}",
            "",
            f"**Total files changed:** {changes.count()}",
            ""
        ]
        
        created = changes.filter(change_type='created').count()
        modified = changes.filter(change_type='modified').count()
        deleted = changes.filter(change_type='deleted').count()
        
        summary_lines.extend([
            f"- Created: {created} files",
            f"- Modified: {modified} files",
            f"- Deleted: {deleted} files",
            "",
            "## Changed Files:",
            ""
        ])
        
        for change in changes:
            stats = f"+{change.line_added}/-{change.line_removed}"
            summary_lines.append(f"- `{change.file_path}` ({stats})")
        
        self.session.diff_summary = '\n'.join(summary_lines)
        self.session.save(update_fields=['diff_summary', 'updated_at'])
    
    def _create_download_package(self):
        """Create a zip package of all changes."""
        zip_path = os.path.join(
            REPO_BASE_PATH,
            'packages',
            f"{self.session.id}_changes.zip"
        )
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for change in FileChange.objects.filter(session=self.session):
                if change.change_type in ['created', 'modified']:
                    # Add file with relative path
                    arcname = f"changes/{change.file_path}"
                    zipf.writestr(arcname, change.new_content)
        
        file_size = os.path.getsize(zip_path)
        
        DownloadPackage.objects.create(
            session=self.session,
            package_type='full_diff',
            file_path=zip_path,
            file_size=file_size,
            expires_at=now_ms() + (7 * 24 * 60 * 60 * 1000),  # 7 days
            created_at=now_ms()
        )
    
    def _cleanup(self):
        """Cleanup temporary files."""
        if self.work_dir and os.path.exists(self.work_dir):
            try:
                shutil.rmtree(self.work_dir)
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")


def run_coding_session(session_id):
    """
    Entry point for running a coding session.
    Called by background worker/management command.
    """
    try:
        session = CodingSession.objects.get(id=session_id)
        agent = BackgroundCodingAgent(session)
        agent.execute()
    except CodingSession.DoesNotExist:
        logger.error(f"Session {session_id} not found")
    except Exception as e:
        logger.exception(f"Failed to run session {session_id}: {e}")


def pause_session(session_id):
    """Pause a running session."""
    session = CodingSession.objects.get(id=session_id)
    if session.status == 'running':
        session.status = 'paused'
        session.paused_at = now_ms()
        session.save(update_fields=['status', 'paused_at', 'updated_at'])


def resume_session(session_id):
    """Resume a paused session."""
    session = CodingSession.objects.get(id=session_id)
    if session.status == 'paused':
        session.status = 'running'
        session.save(update_fields=['status', 'updated_at'])
        # Restart the agent
        run_coding_session(session_id)


def cancel_session(session_id):
    """Cancel a session."""
    session = CodingSession.objects.get(id=session_id)
    if session.status in ['queued', 'running', 'paused']:
        session.status = 'cancelled'
        session.completed_at = now_ms()
        session.save(update_fields=['status', 'completed_at', 'updated_at'])
