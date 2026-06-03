from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_rename_user_auth_t_user_id_e4923b_idx_user_auth_t_user_id_a801f0_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArenaChatSession',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('arena_session_id', models.CharField(db_index=True, max_length=64)),
                ('arena_token_id', models.CharField(blank=True, default='', max_length=64)),
                ('model_id', models.CharField(max_length=64)),
                ('model_code', models.CharField(blank=True, default='', max_length=100)),
                ('model_display_name', models.CharField(blank=True, default='', max_length=200)),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('message_count', models.PositiveIntegerField(default=0)),
                ('last_message_at', models.BigIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('updated_at', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arena_sessions', to='api.user')),
            ],
            options={
                'db_table': 'arena_chat_sessions',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.AddIndex(
            model_name='arenachatsession',
            index=models.Index(fields=['user', '-updated_at'], name='arena_chat_user_update_idx'),
        ),
        migrations.AddIndex(
            model_name='arenachatsession',
            index=models.Index(fields=['user', 'is_active'], name='arena_chat_user_activ_idx'),
        ),
        migrations.CreateModel(
            name='ArenaChatMessage',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], max_length=10)),
                ('content', models.TextField(blank=True, default='')),
                ('parent_id', models.CharField(blank=True, default='', max_length=36)),
                ('arena_message_id', models.CharField(blank=True, default='', max_length=64)),
                ('finish_reason', models.CharField(blank=True, default='', max_length=20)),
                ('error', models.CharField(blank=True, default='', max_length=200)),
                ('duration_ms', models.PositiveIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.arenachatsession')),
            ],
            options={
                'db_table': 'arena_chat_messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='arenachatmessage',
            index=models.Index(fields=['session', 'created_at'], name='arena_msg_session_created_idx'),
        ),
    ]
