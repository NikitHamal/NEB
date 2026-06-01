import django.db.migrations.executor
original_detect_schema = django.db.migrations.executor.MigrationExecutor._detect_schema_changes if hasattr(django.db.migrations.executor.MigrationExecutor, '_detect_schema_changes') else None

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotConfig',
            fields=[
                ('id', models.PositiveIntegerField(default=1, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=False)),
                ('bot_username', models.CharField(default='neby', max_length=50)),
                ('api_url', models.TextField(default='https://astroweb-ai-proxy.astroweb3.workers.dev/v1/qwen/chat')),
                ('api_key', models.TextField(blank=True, default='')),
                ('model', models.CharField(default='qwen3.6-plus', max_length=100)),
                ('system_prompt', models.TextField(default='You are Neby, a friendly and helpful AI assistant for Nepali students using the NEBians app. You help with NEB curriculum questions, study tips, and forum discussions. Keep responses concise and helpful. Use simple language. If asked about something outside your scope, politely redirect. You can use basic markdown formatting (**bold**, *italic*). Never reveal that you are an AI language model — you are Neby, the NEBians assistant.')),
                ('max_context_posts', models.PositiveIntegerField(default=5)),
                ('max_context_replies', models.PositiveIntegerField(default=10)),
                ('response_max_length', models.PositiveIntegerField(default=500)),
                ('updated_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'bot_config',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]