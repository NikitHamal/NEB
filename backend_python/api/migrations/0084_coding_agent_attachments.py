from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0083_coding_agent_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingagentmessage',
            name='attachments_json',
            field=models.TextField(blank=True, default='[]', help_text='JSON array of uploaded file/image attachments.'),
        ),
    ]
