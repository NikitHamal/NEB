# Generated: live plan/todo tracking + manual (/compact) compaction requests.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_background_agent_autofix'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundagentsession',
            name='compact_requested_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='backgroundagentsession',
            name='todos_json',
            field=models.TextField(blank=True, default='[]'),
        ),
    ]
