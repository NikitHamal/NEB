"""Database models for the background coding agent."""
from django.db import models

from api.models import User
from api.utils import now_ms, uuid_str


class CodingAgentProject(models.Model):
    """A connected GitHub project. Holds the OAuth access token that gives the
    agent write access to the linked repo. Each project corresponds to one
    repo (e.g. owner/name) that sessions can be created against.
    """
    SCOPE_REPO = 'repo'
    SCOPE_PUBLIC = 'public_repo'

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coding_agent_projects')
    repo_owner = models.CharField(max_length=200, help_text='GitHub owner/org login (e.g. NikitHamal)')
    repo_name = models.CharField(max_length=200, help_text='Repository name (e.g. NEB)')
    repo_full_name = models.CharField(max_length=400)
    repo_description = models.TextField(blank=True, default='')
    default_branch = models.CharField(max_length=120, default='main')
    repo_url = models.CharField(max_length=500, default='')
    is_private = models.BooleanField(default=False)
    access_token = models.TextField(help_text='GitHub OAuth access token (server-only).')
    token_scope = models.CharField(max_length=40, default='repo')
    github_user_login = models.CharField(max_length=120, blank=True, default='')
    system_prompt = models.TextField(
        blank=True,
        default='',
        help_text='Optional override system prompt prepended to every session.',
    )
    agent_provider = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text='Optional override AI provider (qwen/inception/...).',
    )
    agent_model = models.CharField(max_length=200, blank=True, default='')
    max_iterations = models.PositiveIntegerField(default=80, help_text='Safety cap per session.')
    is_archived = models.BooleanField(default=False)
    last_used_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_projects'
        unique_together = (('owner_user', 'repo_full_name'),)
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner_user', '-updated_at']),
            models.Index(fields=['repo_full_name']),
        ]

    def save(self, *args, **kwargs):
        now = now_ms()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        if not self.repo_full_name:
            self.repo_full_name = f'{self.repo_owner}/{self.repo_name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repo_full_name


class CodingAgentSession(models.Model):
    """One task / session against a project.

    Each session works on its own branch (never the default branch of the
    cloned repo). When the agent reaches a stopping point it commits and
    pushes the branch and can open a PR.
    """
    STATUS_QUEUED = 'queued'
    STATUS_SETUP = 'setup'
    STATUS_RUNNING = 'running'
    STATUS_PAUSED = 'paused'
    STATUS_AWAITING_INPUT = 'awaiting_input'
    STATUS_FINISHED = 'finished'
    STATUS_FAILED = 'failed'
    STATUS_STOPPED = 'stopped'
    STATUS_PR_OPENED = 'pr_opened'
    STATUS_CHOICES = [
        (STATUS_QUEUED, 'Queued'),
        (STATUS_SETUP, 'Setting up'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_PAUSED, 'Paused'),
        (STATUS_AWAITING_INPUT, 'Awaiting input'),
        (STATUS_FINISHED, 'Finished'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_STOPPED, 'Stopped'),
        (STATUS_PR_OPENED, 'PR opened'),
    ]

    PRIORITY_NORMAL = 'normal'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [(PRIORITY_NORMAL, 'Normal'), (PRIORITY_HIGH, 'High')]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    project = models.ForeignKey(CodingAgentProject, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=255, default='', help_text='Short human label for the session.')
    task = models.TextField(help_text='The task / goal the agent is asked to accomplish.')
    branch = models.CharField(max_length=200, default='', help_text='Branch name the agent creates and works on.')
    base_ref = models.CharField(max_length=120, default='', help_text='Commit SHA the session branched from.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED, db_index=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_coding_sessions')

    provider = models.CharField(max_length=20, default='', help_text='Resolved AI provider used for this session.')
    model = models.CharField(max_length=200, default='')

    iterations = models.PositiveIntegerField(default=0)
    tool_calls_count = models.PositiveIntegerField(default=0)
    input_tokens_estimate = models.PositiveIntegerField(default=0)
    output_tokens_estimate = models.PositiveIntegerField(default=0)

    workspace_path = models.CharField(max_length=500, default='', help_text='On-disk path of the cloned workspace.')
    last_message_id = models.CharField(max_length=36, blank=True, default='')
    summary = models.TextField(blank=True, default='', help_text='Final summary written by the agent when finishing.')
    pr_url = models.CharField(max_length=500, blank=True, default='')
    pr_number = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True, default='')
    push_state = models.CharField(max_length=20, blank=True, default='', help_text='local_only / pushed / push_failed')

    paused_at = models.BigIntegerField(default=0)
    stopped_at = models.BigIntegerField(default=0)
    finished_at = models.BigIntegerField(default=0)
    last_activity_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-priority', 'created_at'], name='ca_sess_queue_idx'),
            models.Index(fields=['project', '-created_at'], name='ca_sess_proj_idx'),
            models.Index(fields=['assigned_to', '-created_at'], name='ca_sess_user_idx'),
        ]

    def save(self, *args, **kwargs):
        now = now_ms()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.repo_full_name} #{self.pk[:8]}'

    def is_terminal(self):
        return self.status in {self.STATUS_FINISHED, self.STATUS_FAILED, self.STATUS_STOPPED, self.STATUS_PR_OPENED}

    def is_active(self):
        return self.status in {self.STATUS_RUNNING, self.STATUS_SETUP, self.STATUS_PAUSED, self.STATUS_AWAITING_INPUT}


class CodingAgentMessage(models.Model):
    """A single message in a session conversation.

    Roles:
      system   - usually only the synthetic system prompt at the start
      user     - human message — the initial task or a follow-up ("interrupt")
      assistant - text the model produced
      tool     - tool call or result attributed to a tool name (kind=call/result)
    """
    ROLE_SYSTEM = 'system'
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_TOOL = 'tool'
    ROLE_CHOICES = [
        (ROLE_SYSTEM, 'System'),
        (ROLE_USER, 'User'),
        (ROLE_ASSISTANT, 'Assistant'),
        (ROLE_TOOL, 'Tool'),
    ]

    KIND_MESSAGE = 'message'
    KIND_TOOL_CALL = 'tool_call'
    KIND_TOOL_RESULT = 'tool_result'
    KIND_NOTE = 'note'
    KIND_CHOICES = [
        (KIND_MESSAGE, 'Message'),
        (KIND_TOOL_CALL, 'Tool call'),
        (KIND_TOOL_RESULT, 'Tool result'),
        (KIND_NOTE, 'Note'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    session = models.ForeignKey(CodingAgentSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=KIND_MESSAGE)
    content = models.TextField(blank=True, default='')
    tool_name = models.CharField(max_length=60, blank=True, default='')
    tool_args_json = models.TextField(blank=True, default='', help_text='JSON of the tool args.')
    tool_result_json = models.TextField(blank=True, default='', help_text='JSON of the tool result.')
    tool_status = models.CharField(max_length=20, blank=True, default='', help_text='ok / error / pending')
    attachments_json = models.TextField(blank=True, default='[]', help_text='JSON array of uploaded file/image attachments.')
    is_visible = models.BooleanField(default=True, help_text='Whether the message is rendered to humans (system spam is hidden).')
    iteration = models.PositiveIntegerField(default=0)
    sequence = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_messages'
        ordering = ['sequence', 'created_at']
        indexes = [
            models.Index(fields=['session', 'sequence'], name='ca_msg_seq_idx'),
            models.Index(fields=['session', '-created_at'], name='ca_msg_session_created_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        super().save(*args, **kwargs)


class CodingAgentToolCall(models.Model):
    """One tool invocation executed during a session. Persisted for audit,
    re-run, and download-as-zip purposes.
    """
    STATUS_PENDING = 'pending'
    STATUS_OK = 'ok'
    STATUS_ERROR = 'error'
    STATUS_DENIED = 'denied'
    STATUS_TIMEOUT = 'timeout'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_OK, 'OK'),
        (STATUS_ERROR, 'Error'),
        (STATUS_DENIED, 'Denied'),
        (STATUS_TIMEOUT, 'Timeout'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    session = models.ForeignKey(CodingAgentSession, on_delete=models.CASCADE, related_name='tool_calls')
    name = models.CharField(max_length=60, db_index=True)
    args_json = models.TextField(blank=True, default='')
    result_text = models.TextField(blank=True, default='')
    result_truncated = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    duration_ms = models.PositiveIntegerField(default=0)
    iteration = models.PositiveIntegerField(default=0)
    message_id = models.CharField(max_length=36, blank=True, default='')
    error_text = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    finished_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_tool_calls'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at'], name='ca_tool_session_idx'),
            models.Index(fields=['name', '-created_at'], name='ca_tool_name_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        super().save(*args, **kwargs)


class CodingAgentFileChange(models.Model):
    """Files touched by the agent. Used for diff rendering, ZIP packaging,
    and PR description generation.
    """
    OP_CREATE = 'create'
    OP_MODIFY = 'modify'
    OP_DELETE = 'delete'
    OP_RENAME = 'rename'
    OP_CHOICES = [
        (OP_CREATE, 'Create'),
        (OP_MODIFY, 'Modify'),
        (OP_DELETE, 'Delete'),
        (OP_RENAME, 'Rename'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    session = models.ForeignKey(CodingAgentSession, on_delete=models.CASCADE, related_name='file_changes')
    path = models.CharField(max_length=500, db_index=True)
    op = models.CharField(max_length=10, choices=OP_CHOICES, default=OP_MODIFY)
    additions = models.PositiveIntegerField(default=0)
    deletions = models.PositiveIntegerField(default=0)
    patch = models.TextField(blank=True, default='', help_text='Unified diff for this file (may be empty for big files).')
    committed = models.BooleanField(default=False)
    commit_sha = models.CharField(max_length=64, blank=True, default='')
    tool_call_id = models.CharField(max_length=36, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_file_changes'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', '-created_at'], name='ca_file_session_idx'),
            models.Index(fields=['session', 'path'], name='ca_file_path_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        super().save(*args, **kwargs)


class CodingAgentEvent(models.Model):
    """Audit / timeline events for a session (status changes, push, PR open).

    Distinct from messages because events are millisecond-low-overhead records
    used by the UI timeline and broadcast fan-out.
    """
    EVENT_STATUS = 'status'
    EVENT_TOOL = 'tool'
    EVENT_LOG = 'log'
    EVENT_PUSH = 'push'
    EVENT_PR = 'pr'
    EVENT_INTERRUPT = 'interrupt'
    EVENT_CHOICES = [
        (EVENT_STATUS, 'Status'),
        (EVENT_TOOL, 'Tool'),
        (EVENT_LOG, 'Log'),
        (EVENT_PUSH, 'Push'),
        (EVENT_PR, 'PR'),
        (EVENT_INTERRUPT, 'Interrupt'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    session = models.ForeignKey(CodingAgentSession, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES, default=EVENT_LOG)
    summary = models.CharField(max_length=255)
    detail = models.TextField(blank=True, default='')
    payload_json = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', '-created_at'], name='ca_event_session_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        super().save(*args, **kwargs)


class CodingAgentKnowledgeItem(models.Model):
    """Server-side Long-Term Memory & Knowledge Base item for background agent sessions."""
    TYPE_CODING_RULE = 'CODING_RULE'
    TYPE_PROJECT_ARCHITECTURE = 'PROJECT_ARCHITECTURE'
    TYPE_USER_PREFERENCE = 'USER_PREFERENCE'
    TYPE_SNIPPET = 'SNIPPET'
    TYPE_DOCUMENT_CHUNK = 'DOCUMENT_CHUNK'
    TYPE_SESSION_SUMMARY = 'SESSION_SUMMARY'

    TYPE_CHOICES = [
        (TYPE_CODING_RULE, 'Coding Rule'),
        (TYPE_PROJECT_ARCHITECTURE, 'Project Architecture'),
        (TYPE_USER_PREFERENCE, 'User Preference'),
        (TYPE_SNIPPET, 'Snippet'),
        (TYPE_DOCUMENT_CHUNK, 'Document Chunk'),
        (TYPE_SESSION_SUMMARY, 'Session Summary'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coding_agent_knowledge_items')
    project = models.ForeignKey(CodingAgentProject, on_delete=models.CASCADE, null=True, blank=True, related_name='knowledge_items')
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=40, choices=TYPE_CHOICES, default=TYPE_CODING_RULE)
    tags = models.CharField(max_length=500, blank=True, default='')
    repository = models.CharField(max_length=400, blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'coding_agent_knowledge_items'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner_user', '-updated_at'], name='ca_kb_user_idx'),
            models.Index(fields=['project', '-updated_at'], name='ca_kb_proj_idx'),
            models.Index(fields=['repository'], name='ca_kb_repo_idx'),
        ]

    def save(self, *args, **kwargs):
        now = now_ms()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.type}] {self.title}'

