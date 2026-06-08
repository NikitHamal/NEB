from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_arena_chat_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='arenachatsession',
            name='provider',
            field=models.CharField(choices=[('ai4bharat', 'AI4Bharat Arena'), ('qwen', 'Qwen (chat.qwen.ai)')], default='ai4bharat', max_length=20),
        ),
        migrations.AddField(
            model_name='arenachatsession',
            name='qwen_chat_id',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]