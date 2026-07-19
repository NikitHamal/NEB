import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_blog_comment_likes_and_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundagentproject',
            name='autofix_enabled',
            field=models.BooleanField(
                default=True,
                help_text='When a GitHub Actions run fails for this repo, queue an agent session with the failing job log.',
            ),
        ),
        migrations.CreateModel(
            name='BackgroundAgentAutofixRun',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('run_id', models.BigIntegerField(default=0)),
                ('head_sha', models.CharField(blank=True, default='', max_length=64)),
                ('branch', models.CharField(blank=True, default='', max_length=255)),
                ('workflow_name', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.BigIntegerField(default=0)),
                (
                    'project',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='autofix_runs',
                        to='api.backgroundagentproject',
                    ),
                ),
                (
                    'session',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='autofix_origin',
                        to='api.backgroundagentsession',
                    ),
                ),
            ],
            options={
                'db_table': 'background_agent_autofix_runs',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['project', '-created_at'], name='bg_autofix_project_created_idx'),
                    models.Index(fields=['project', 'head_sha'], name='bg_autofix_project_sha_idx'),
                ],
                'constraints': [
                    models.UniqueConstraint(fields=('project', 'run_id'), name='uniq_bg_autofix_project_run'),
                ],
            },
        ),
    ]
