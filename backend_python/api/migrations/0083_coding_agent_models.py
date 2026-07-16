"""Migration for background coding agent models."""
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_post_view_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodingProject',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('repo_full_name', models.CharField(help_text='e.g. NikitHamal/NEB', max_length=255)),
                ('repo_url', models.URLField(max_length=500)),
                ('default_branch', models.CharField(default='main', max_length=100)),
                ('github_token', models.TextField(blank=True, default='', help_text='Encrypted GitHub access token with repo scope')),
                ('workspace_dir', models.CharField(blank=True, default='', max_length=500)),
                ('clone_status', models.CharField(default='pending', help_text='pending/ready/failed', max_length=20)),
                ('clone_error', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], db_index=True, default='active', max_length=20)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('owner', models.ForeignKey(db_index=True, on_delete=models.deletion.CASCADE, related_name='coding_projects', to='api.user')),
            ],
            options={
                'db_table': 'coding_projects',
                'ordering': ['-updated_at'],
                'indexes': [
                    models.Index(fields=['owner', '-updated_at'], name='coding_proj_owner_i_8e6f3f_idx'),
                    models.Index(fields=['status'], name='coding_proj_status_208be5_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='CodingTask',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('goal', models.TextField(help_text='The coding task description/goal for the AI agent')),
                ('branch_name', models.CharField(help_text='Branch the agent works on (never main)', max_length=200)),
                ('status', models.CharField(choices=[('queued', 'Queued'), ('running', 'Running'), ('paused', 'Paused'), ('completed', 'Completed'), ('failed', 'Failed'), ('stopped', 'Stopped')], db_index=True, default='queued', max_length=20)),
                ('provider', models.CharField(default='ai4bharat', help_text='AI provider: ai4bharat/qwen/deepai/egov', max_length=50)),
                ('model_id', models.CharField(blank=True, default='', max_length=100)),
                ('iteration', models.IntegerField(default=0, help_text='How many AI turns have been completed')),
                ('max_iterations', models.IntegerField(default=50)),
                ('last_thought', models.TextField(blank=True, default='')),
                ('pr_url', models.URLField(blank=True, default='', max_length=500)),
                ('pr_number', models.IntegerField(blank=True, null=True)),
                ('created_at', models.BigIntegerField(default=0)),
                ('started_at', models.BigIntegerField(default=0)),
                ('completed_at', models.BigIntegerField(default=0)),
                ('paused_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('project', models.ForeignKey(db_index=True, on_delete=models.deletion.CASCADE, related_name='tasks', to='api.codingproject')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='coding_tasks', to='api.user')),
            ],
            options={
                'db_table': 'coding_tasks',
                'ordering': ['-updated_at'],
                'indexes': [
                    models.Index(fields=['status'], name='coding_task_status_fecfe8_idx'),
                    models.Index(fields=['project', '-updated_at'], name='coding_task_project_b1d33d_idx'),
                    models.Index(fields=['created_by', '-created_at'], name='coding_task_created_88d6f8_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='CodingTaskMessage',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System'), ('tool_result', 'Tool Result')], db_index=True, max_length=20)),
                ('content', models.TextField(blank=True, default='')),
                ('tool_actions', models.TextField(blank=True, default='', help_text='JSON array of tool calls the AI made')),
                ('tool_results', models.TextField(blank=True, default='', help_text='JSON array of tool execution results')),
                ('thoughts', models.TextField(blank=True, default='', help_text='AI reasoning/thinking text')),
                ('status_flag', models.CharField(blank=True, default='', help_text='working/done/need_input/error', max_length=20)),
                ('created_at', models.BigIntegerField(default=0)),
                ('task', models.ForeignKey(db_index=True, on_delete=models.deletion.CASCADE, related_name='messages', to='api.codingtask')),
            ],
            options={
                'db_table': 'coding_task_messages',
                'ordering': ['created_at'],
                'indexes': [
                    models.Index(fields=['task', 'created_at'], name='coding_task_task_id_3a09b0_idx'),
                    models.Index(fields=['role'], name='coding_task_role_3f2a49_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='CodingActionLog',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('iteration', models.IntegerField(default=0)),
                ('action_type', models.CharField(choices=[('read', 'Read File'), ('write', 'Write File'), ('list', 'List Files'), ('search', 'Search'), ('command', 'Run Command'), ('git', 'Git Operation'), ('status', 'Status Update')], db_index=True, max_length=20)),
                ('description', models.TextField(blank=True, default='')),
                ('file_path', models.CharField(blank=True, default='', max_length=500)),
                ('content_diff', models.TextField(blank=True, default='')),
                ('status', models.CharField(default='ok', help_text='ok/error', max_length=20)),
                ('created_at', models.BigIntegerField(default=0)),
                ('task', models.ForeignKey(db_index=True, on_delete=models.deletion.CASCADE, related_name='action_logs', to='api.codingtask')),
            ],
            options={
                'db_table': 'coding_action_logs',
                'ordering': ['created_at'],
                'indexes': [
                    models.Index(fields=['task', 'created_at'], name='coding_acti_task_id_8b0e25_idx'),
                    models.Index(fields=['action_type'], name='coding_acti_action__937f11_idx'),
                ],
            },
        ),
    ]
