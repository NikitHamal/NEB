from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arenachatsession',
            name='provider',
            field=models.CharField(choices=[('ai4bharat', 'AI4Bharat Arena'), ('qwen', 'Qwen (chat.qwen.ai)'), ('egov', 'eGov Chat AI (Philippines)'), ('deepai', 'DeepAI (deepai.org)'), ('eqing', 'EQing / EasyChat (chat3.eqing.tech)'), ('freegpt', 'FreeGPT (standalone.freegpt.win:3001)'), ('deepseekai', 'DeepSeek AI (deep-seek.ai)'), ('surfsense', 'SurfSense (surfsense.com)'), ('g4f', 'G4F (g4f.space / Pollinations AI)'), ('custom', 'Custom OpenAI-compatible endpoint')], default='qwen', max_length=20),
        ),
        migrations.AlterField(
            model_name='botconfig',
            name='provider',
            field=models.CharField(choices=[('qwen', 'Qwen (chat.qwen.ai)'), ('ai4bharat', 'AI4Bharat Arena (Indic LLM Arena)'), ('egov', 'eGov Chat AI (Philippines)'), ('deepai', 'DeepAI (deepai.org)'), ('eqing', 'EQing / EasyChat (chat3.eqing.tech)'), ('freegpt', 'FreeGPT (standalone.freegpt.win:3001)'), ('deepseekai', 'DeepSeek AI (deep-seek.ai)'), ('surfsense', 'SurfSense (surfsense.com)'), ('g4f', 'G4F (g4f.space / Pollinations AI)'), ('custom', 'Custom OpenAI-compatible endpoint')], default='qwen', max_length=20),
        ),
    ]
