"""Merge 0083_background_agent and 0083_coding_agent_models."""
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0083_background_agent'),
        ('api', '0083_coding_agent_models'),
    ]
    operations = []
