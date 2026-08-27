import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_canvas_neby_runs'),
    ]

    operations = [
        migrations.CreateModel(
            name='LazyDocSession',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='New chat', max_length=200)),
                ('doc_title', models.CharField(blank=True, default='', max_length=200)),
                ('doc_html', models.TextField(blank=True, default='')),
                ('meta', models.TextField(blank=True, default='{}')),
                ('message_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='lazy_sessions', to='api.user')),
            ],
            options={
                'db_table': 'lazy_doc_sessions',
                'ordering': ['-updated_at'],
                'indexes': [models.Index(fields=['user', '-updated_at'], name='lazy_doc_user_updated_idx')],
            },
        ),
        migrations.CreateModel(
            name='LazyDocMessage',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, default='')),
                ('meta', models.TextField(blank=True, default='{}')),
                ('created_at', models.BigIntegerField(default=0)),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant')], max_length=12)),
                ('session', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.lazydocsession')),
            ],
            options={
                'db_table': 'lazy_doc_messages',
                'ordering': ['created_at', 'id'],
                'indexes': [models.Index(fields=['session', 'created_at'], name='lazy_msg_session_created_idx')],
            },
        ),
    ]
