"""
Django models for Background Coding Agent (GitHub integration).
Similar to Google Jules, Cursor Agent, Tembo AI - works with GitHub repos directly.
"""
import uuid
from django.db import models
from api.models import User


class GitHubConnection(models.Model):
    """
    Stores OAuth connection to GitHub for a user.
    Similar to how Tembo AI, Cursor connect to GitHub.
    """
    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='github_connections')
    github_user_id = models.CharField(max_length=50, db_index=True)
    github_username = models.CharField(max_length=100)
    access_token = models.TextField()  # Encrypted in production
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.BigIntegerField(default=0)
    installed = models.BooleanField(default=False)  # Whether app is installed on user's repos
    permissions = models.TextField(blank=True, default='')  # JSON list of granted permissions
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'github_connections'
        unique_together = ('user', 'github_user_id')
        indexes = [
            models.Index(fields=['github_user_id']),
            models.Index(fields=['user', 'installed']),
        ]

    def __str__(self):
        return f"{self.github_username} (user {self.user_id})"


class CodebaseProject(models.Model):
    """
    Represents a cloned repository/codebase environment.
    Each project has its own isolated environment like Google Jules.
    """
    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    github_connection = models.ForeignKey(GitHubConnection, on_delete=models.CASCADE, related_name='projects')
    repo_owner = models.CharField(max_length=100)  # GitHub owner/org
    repo_name = models.CharField(max_length=100)
    repo_full_name = models.CharField(max_length=200, db_index=True)  # owner/repo
    clone_url = models.TextField()
    base_branch = models.CharField(max_length=100, default='main')
    local_path = models.TextField()  # Path where repo is cloned on server
    environment_setup = models.TextField(blank=True, default='')  # Setup commands/env vars as JSON
    last_synced_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'codebase_projects'
        unique_together = ('github_connection', 'repo_full_name')
        indexes = [
            models.Index(fields=['repo_full_name']),
            models.Index(fields=['github_connection', 'repo_owner', 'repo_name']),
        ]

    def __str__(self):
        return self.repo_full_name


class CodingSession(models.Model):
    """
    A session represents a coding task/agent run.
    Like Google Jules sessions - each task uses its own branch.
    Users can stop, pause, resume, chat/interrupt/followup.
    """
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('cloning', 'Cloning Repository'),
        ('setting_up', 'Setting Up Environment'),
        ('running', 'Running Agent'),
        ('paused', 'Paused'),
        ('waiting_input', 'Waiting for User Input'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    project = models.ForeignKey(CodebaseProject, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coding_sessions')
    
    # Task details
    title = models.CharField(max_length=200)
    description = models.TextField()  # The main goal/task for the agent
    instructions = models.TextField(blank=True, default='')  # Additional context/instructions
    
    # Branch management - NEVER use main branch
    session_branch = models.CharField(max_length=100)  # Unique branch for this session
    base_commit = models.CharField(max_length=64, blank=True, default='')  # SHA of commit we branched from
    
    # Execution state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued', db_index=True)
    current_step = models.TextField(blank=True, default='')  # What the agent is currently doing
    progress_percent = models.PositiveSmallIntegerField(default=0)
    
    # Model/provider selection (uses Neby AI providers)
    provider = models.CharField(max_length=50, default='qwen')  # qwen, deepai, custom_provider, etc.
    model_name = models.CharField(max_length=100, default='qwen-coder')
    model_params = models.TextField(blank=True, default='')  # JSON: temperature, max_tokens, etc.
    
    # Results
    pr_number = models.IntegerField(null=True, blank=True)  # GitHub PR number if opened
    pr_url = models.TextField(blank=True, default='')
    diff_summary = models.TextField(blank=True, default='')  # Summary of all changes
    
    # Timing
    started_at = models.BigIntegerField(default=0)
    paused_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['project', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['session_branch']),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"


class SessionMessage(models.Model):
    """
    Chat messages between user and agent within a session.
    Users can interrupt, followup, give additional instructions.
    """
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_SYSTEM = 'system'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ASSISTANT, 'Assistant'),
        (ROLE_SYSTEM, 'System'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    session = models.ForeignKey(CodingSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    content = models.TextField()
    
    # For assistant messages - track what actions were taken
    action_type = models.CharField(max_length=50, blank=True, default='')  # e.g., 'file_read', 'file_write', 'command_run', 'search'
    action_data = models.TextField(blank=True, default='')  # JSON with details about the action
    
    # Attachments (screenshots, file snippets, etc.)
    attachments = models.TextField(blank=True, default='')  # JSON array of attachment URLs
    
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'session_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['session', 'role']),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class FileChange(models.Model):
    """
    Tracks individual file changes made by the agent.
    Allows users to review, download as zip, or push to GitHub.
    """
    CHANGE_TYPE_CHOICES = [
        ('created', 'Created'),
        ('modified', 'Modified'),
        ('deleted', 'Deleted'),
        ('renamed', 'Renamed'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    session = models.ForeignKey(CodingSession, on_delete=models.CASCADE, related_name='file_changes')
    file_path = models.TextField()  # Relative path in repo
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    
    # Content tracking
    old_content = models.TextField(blank=True, default='')  # For modified/deleted files
    new_content = models.TextField(blank=True, default='')  # For created/modified files
    diff_patch = models.TextField(blank=True, default='')  # Unified diff
    
    # Metadata
    line_added = models.PositiveIntegerField(default=0)
    line_removed = models.PositiveIntegerField(default=0)
    
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'file_changes'
        ordering = ['file_path']
        indexes = [
            models.Index(fields=['session', 'file_path']),
        ]

    def __str__(self):
        return f"{self.change_type}: {self.file_path}"


class CommandExecution(models.Model):
    """
    Tracks commands executed by the agent in the background.
    For transparency and debugging.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    session = models.ForeignKey(CodingSession, on_delete=models.CASCADE, related_name='commands')
    command = models.TextField()  # The shell command
    working_directory = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    exit_code = models.IntegerField(null=True, blank=True)
    stdout = models.TextField(blank=True, default='')
    stderr = models.TextField(blank=True, default='')
    duration_ms = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'command_executions'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', '-created_at']),
        ]

    def __str__(self):
        return f"{self.command[:50]}... ({self.status})"


class AgentTask(models.Model):
    """
    Individual subtasks within a session.
    The agent breaks down the main goal into these tasks.
    Similar to how Cursor Agent plans and executes.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    session = models.ForeignKey(CodingSession, on_delete=models.CASCADE, related_name='tasks')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subtasks', null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Planning
    plan = models.TextField(blank=True, default='')  # How the agent plans to accomplish this
    result_summary = models.TextField(blank=True, default='')  # What was actually done
    
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'agent_tasks'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['session', 'status']),
            models.Index(fields=['parent_task']),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"


class DownloadPackage(models.Model):
    """
    Zip packages of changes that users can download.
    """
    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
    session = models.ForeignKey(CodingSession, on_delete=models.CASCADE, related_name='download_packages')
    package_type = models.CharField(max_length=50)  # 'full_diff', 'new_files_only', 'specific_paths'
    filter_paths = models.TextField(blank=True, default='')  # JSON array of paths if filtered
    file_path = models.TextField()  # Path to the generated zip file
    file_size = models.BigIntegerField(default=0)
    expires_at = models.BigIntegerField(default=0)  # Auto-cleanup after some time
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'download_packages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', '-created_at']),
        ]

    def __str__(self):
        return f"Package for {self.session_id} ({self.package_type})"
