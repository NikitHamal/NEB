# Re-points the background agent ownership fields from Django's auth.User to the
# platform account model (api.User) so admins sign in with their NEBians account
# and the GitHub credential travels with that account across devices.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_background_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundagentcredential',
            name='admin_user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='background_agent_credential',
                to='api.user',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentproject',
            name='admin_user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='background_agent_projects',
                to='api.user',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentsession',
            name='admin_user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='background_agent_sessions',
                to='api.user',
            ),
        ),
        migrations.AlterField(
            model_name='backgroundagentaction',
            name='requested_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='background_agent_actions',
                to='api.user',
            ),
        ),
    ]
