from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_arena_chat_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='botconfig',
            name='provider',
            field=models.CharField(
                choices=[
                    ('qwen', 'Qwen (chat.qwen.ai)'),
                    ('ai4bharat', 'AI4Bharat Arena (Indic LLM Arena)'),
                    ('custom', 'Custom OpenAI-compatible endpoint'),
                ],
                default='qwen',
                max_length=20,
            ),
        ),
        # Backfill: any existing rows without a provider default to qwen
        migrations.RunSQL(
            sql=("UPDATE bot_config SET provider = 'qwen' WHERE provider IS NULL OR provider = '';",),
            reverse_sql=("UPDATE bot_config SET provider = 'qwen';",),
        ),
        # Widen the model column so AI4Bharat UUIDs + long custom model names fit
        migrations.AlterField(
            model_name='botconfig',
            name='model',
            field=models.CharField(default='qwen3.6-plus', max_length=200),
        ),
    ]
