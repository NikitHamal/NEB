from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_composite_indexes_user_email_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botconfig',
            name='provider',
            field=models.CharField(choices=[('qwen', 'Qwen (chat.qwen.ai)'), ('ai4bharat', 'AI4Bharat Arena (Indic LLM Arena)'), ('egov', 'eGov Chat AI (Philippines)'), ('deepai', 'DeepAI (deepai.org)'), ('eqing', 'EQing / EasyChat (chat3.eqing.tech)'), ('freegpt', 'FreeGPT (standalone.freegpt.win:3001)'), ('deepseekai', 'DeepSeek AI (deep-seek.ai)'), ('surfsense', 'SurfSense (surfsense.com)'), ('custom', 'Custom OpenAI-compatible endpoint')], default='qwen', max_length=20),
        ),
        migrations.AlterField(
            model_name='arenachatsession',
            name='provider',
            field=models.CharField(choices=[('ai4bharat', 'AI4Bharat Arena'), ('qwen', 'Qwen (chat.qwen.ai)'), ('egov', 'eGov Chat AI (Philippines)'), ('deepai', 'DeepAI (deepai.org)'), ('eqing', 'EQing / EasyChat (chat3.eqing.tech)'), ('freegpt', 'FreeGPT (standalone.freegpt.win:3001)'), ('deepseekai', 'DeepSeek AI (deep-seek.ai)'), ('surfsense', 'SurfSense (surfsense.com)')], default='ai4bharat', max_length=20),
        ),
    ]