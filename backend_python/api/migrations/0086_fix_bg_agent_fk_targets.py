"""Fix background agent FK targets from auth.User to api.User."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0085_fix_bg_agent_user_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundagentcredential',
            name='admin_user',
            field=models.OneToOneField(
                on_delete=models.CASCADE,
                related_name='background_agent_credential',
                to='api.User',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentproject',
            name='admin_user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='background_agent_projects',
                to='api.User',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentsession',
            name='admin_user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='background_agent_sessions',
                to='api.User',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentaction',
            name='requested_by',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='background_agent_actions',
                to='api.User',
            ),
        ),
    ]
