import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0091_alter_backgroundagentaction_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundagentsession',
            name='archived_at',
            field=models.BigIntegerField(db_index=True, default=0),
        ),
        migrations.CreateModel(
            name='BackgroundAgentDevicePairing',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('device_code_hash', models.CharField(max_length=64, unique=True)),
                ('user_code', models.CharField(db_index=True, max_length=12, unique=True)),
                ('device_name', models.CharField(blank=True, default='Zeus', max_length=120)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('consumed', 'Consumed'), ('expired', 'Expired'), ('denied', 'Denied')], db_index=True, default='pending', max_length=20)),
                ('created_at', models.BigIntegerField(default=0)),
                ('expires_at', models.BigIntegerField(db_index=True, default=0)),
                ('approved_at', models.BigIntegerField(default=0)),
                ('consumed_at', models.BigIntegerField(default=0)),
                ('last_polled_at', models.BigIntegerField(default=0)),
                ('poll_count', models.PositiveIntegerField(default=0)),
                ('admin_user', models.ForeignKey(blank=True, null=True, db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='background_agent_pairings', to='api.user')),
            ],
            options={
                'db_table': 'background_agent_device_pairings',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['status', 'expires_at'], name='bg_pair_status_expiry_idx')],
            },
        ),
        migrations.CreateModel(
            name='BackgroundAgentDeviceToken',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('token_hash', models.CharField(db_index=True, max_length=64, unique=True)),
                ('device_name', models.CharField(blank=True, default='Zeus', max_length=120)),
                ('scopes', models.CharField(default='agent:read,agent:write,repo:read,artifact:read', max_length=255)),
                ('created_at', models.BigIntegerField(default=0)),
                ('last_used_at', models.BigIntegerField(default=0)),
                ('expires_at', models.BigIntegerField(db_index=True, default=0)),
                ('revoked_at', models.BigIntegerField(db_index=True, default=0)),
                ('admin_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='background_agent_device_tokens', to='api.user')),
            ],
            options={
                'db_table': 'background_agent_device_tokens',
                'ordering': ['-last_used_at', '-created_at'],
                'indexes': [models.Index(fields=['admin_user', '-last_used_at'], name='bg_device_admin_used_idx')],
            },
        ),
    ]
