from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_study_space_presence_notes_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydocument',
            name='parse_status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='parsed_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='parsed_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='parse_error',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='qwen_file_id',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]