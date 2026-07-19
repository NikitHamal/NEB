# Generated: user-switchable LLM providers (BYOK + official APIs incl. Agnes).
from django.conf import settings as dj_settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_background_agent_plan_compact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botconfig',
            name='provider',
            field=models.CharField(choices=[
                ('qwen', 'Qwen (chat.qwen.ai)'),
                ('ai4bharat', 'AI4Bharat Arena (Indic LLM Arena)'),
                ('egov', 'eGov Chat AI (Philippines)'),
                ('deepai', 'DeepAI (deepai.org)'),
                ('inception', 'Inception Labs (Mercury 2)'),
                ('custom', 'Custom OpenAI-compatible endpoint'),
                ('agnes', 'Agnes 2.0 Flash (Sapiens AI — official API, currently free)'),
                ('openai', 'OpenAI (ChatGPT official API)'),
                ('anthropic', 'Anthropic (Claude official API)'),
                ('gemini', 'Google Gemini (official API)'),
                ('deepseek', 'DeepSeek (official API)'),
            ], default='qwen', max_length=20),
        ),
        migrations.AddField(
            model_name='backgroundagentsession',
            name='llm_provider',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='backgroundagentsession',
            name='llm_model',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='backgroundagentsession',
            name='llm_provider_id',
            field=models.CharField(blank=True, default='', max_length=36),
        ),
        migrations.CreateModel(
            name='UserLLMProvider',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('provider', models.CharField(db_index=True, max_length=40)),
                ('api_format', models.CharField(choices=[
                    ('openai', 'OpenAI-compatible (chat completions)'),
                    ('anthropic', 'Anthropic Messages API'),
                    ('gemini', 'Google Gemini API'),
                ], default='openai', max_length=20)),
                ('base_url', models.TextField(blank=True, default='')),
                ('api_key', models.TextField(blank=True, default='')),
                ('models_json', models.TextField(blank=True, default='[]')),
                ('default_model', models.CharField(blank=True, default='', max_length=200)),
                ('context_window', models.PositiveIntegerField(default=131072)),
                ('max_output_tokens', models.PositiveIntegerField(default=4096)),
                ('enabled', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='llm_providers',
                    to=dj_settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'user_llm_providers',
                'ordering': ['-updated_at'],
                'indexes': [models.Index(fields=['user', 'provider', 'enabled'], name='llmprov_user_slug_idx')],
            },
        ),
    ]
