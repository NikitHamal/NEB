"""Fix background agent FK targets (auth.User -> api.User)."""
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0084_merge_0083_background_agent_0083_coding_agent_models'),
    ]
    operations = []
