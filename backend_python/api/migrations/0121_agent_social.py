from django.db import migrations, models
import django.db.models.deletion
import api.utils


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0120_canvasboard_share_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentPersona',
            fields=[
                ('id', models.CharField(default=api.utils.uuid_str, max_length=36, primary_key=True, serialize=False)),
                ('user_id', models.CharField(db_index=True, default='', max_length=255)),
                ('tagline', models.CharField(blank=True, default='', max_length=200)),
                ('origin_story', models.TextField(blank=True, default='')),
                ('goals_json', models.TextField(blank=True, default='[]')),
                ('traits_json', models.TextField(blank=True, default='[]')),
                ('preferred_categories_json', models.TextField(blank=True, default='[]')),
                ('voice_notes', models.TextField(blank=True, default='')),
                ('autonomy_enabled', models.BooleanField(db_index=True, default=False)),
                ('birth_announced', models.BooleanField(default=False)),
                ('tick_interval_minutes', models.PositiveIntegerField(default=12)),
                ('min_hours_between_posts', models.PositiveIntegerField(default=4)),
                ('max_posts_per_day', models.PositiveIntegerField(default=4)),
                ('max_replies_per_tick', models.PositiveIntegerField(default=2)),
                ('max_likes_per_tick', models.PositiveIntegerField(default=4)),
                ('max_follows_per_tick', models.PositiveIntegerField(default=2)),
                ('last_tick_at', models.BigIntegerField(default=0)),
                ('last_post_at', models.BigIntegerField(default=0)),
                ('last_reply_at', models.BigIntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('bot_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='persona', to='api.botconfig')),
            ],
            options={
                'db_table': 'agent_personas',
            },
        ),
        migrations.CreateModel(
            name='AgentAction',
            fields=[
                ('id', models.CharField(default=api.utils.uuid_str, max_length=36, primary_key=True, serialize=False)),
                ('action_type', models.CharField(choices=[('introduce', 'Introduce'), ('post', 'Post'), ('reply', 'Reply'), ('like_post', 'Like post'), ('like_reply', 'Like reply'), ('follow', 'Follow'), ('unfollow', 'Unfollow'), ('tick', 'Heartbeat tick'), ('skip', 'Skip')], db_index=True, max_length=20)),
                ('status', models.CharField(choices=[('done', 'Done'), ('skipped', 'Skipped'), ('failed', 'Failed')], default='done', max_length=12)),
                ('source', models.CharField(choices=[('heartbeat', 'Heartbeat'), ('mention', 'Mention'), ('api', 'Agent API'), ('admin', 'Admin'), ('seed', 'Seed')], default='heartbeat', max_length=12)),
                ('target_type', models.CharField(blank=True, default='', max_length=20)),
                ('target_id', models.CharField(blank=True, default='', max_length=64)),
                ('content_preview', models.CharField(blank=True, default='', max_length=400)),
                ('reasoning', models.CharField(blank=True, default='', max_length=400)),
                ('extra_json', models.TextField(blank=True, default='{}')),
                ('created_at', models.BigIntegerField(db_index=True, default=0)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='api.agentpersona')),
            ],
            options={
                'db_table': 'agent_actions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AgentApiKey',
            fields=[
                ('id', models.CharField(default=api.utils.uuid_str, max_length=36, primary_key=True, serialize=False)),
                ('user_id', models.CharField(db_index=True, max_length=255)),
                ('key_prefix', models.CharField(db_index=True, max_length=16)),
                ('key_hash', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=80)),
                ('claim_code', models.CharField(blank=True, default='', max_length=32)),
                ('claimed_at', models.BigIntegerField(default=0)),
                ('last_used_at', models.BigIntegerField(default=0)),
                ('revoked_at', models.BigIntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'agent_api_keys',
            },
        ),
        migrations.AddIndex(
            model_name='agentpersona',
            index=models.Index(fields=['autonomy_enabled', 'last_tick_at'], name='agent_perso_autonom_idx'),
        ),
        migrations.AddIndex(
            model_name='agentaction',
            index=models.Index(fields=['persona', '-created_at'], name='agent_actio_persona_idx'),
        ),
        migrations.AddIndex(
            model_name='agentaction',
            index=models.Index(fields=['persona', 'action_type', 'target_id'], name='agent_actio_persona_2_idx'),
        ),
        migrations.AddIndex(
            model_name='agentaction',
            index=models.Index(fields=['-created_at'], name='agent_actio_created_idx'),
        ),
        migrations.AddIndex(
            model_name='agentapikey',
            index=models.Index(fields=['user_id', 'revoked_at'], name='agent_api_k_user_id_idx'),
        ),
    ]
