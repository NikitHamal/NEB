from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0104_restore_studydoc_space_column'),
        ('api', '0103_alter_resourcecomment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundagentsession',
            name='llm_thinking_mode',
            field=models.CharField(blank=True, default='auto', max_length=12),
        ),
    ]