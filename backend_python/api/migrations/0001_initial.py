import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('auth_token', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('photo_url', models.TextField(blank=True, null=True)),
                ('display_name', models.CharField(blank=True, max_length=150, null=True)),
                ('dob', models.CharField(default='', max_length=20)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('class_level', models.CharField(blank=True, db_column='class', max_length=10, null=True)),
                ('subjects', models.TextField(blank=True, null=True)),
                ('pradesh', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('school', models.CharField(blank=True, max_length=200, null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('grade_level', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=50)),
                ('file_url', models.TextField()),
                ('thumbnail_url', models.TextField(blank=True, null=True)),
                ('file_size', models.BigIntegerField(default=0)),
                ('added_at', models.BigIntegerField()),
                ('view_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'resources',
                'ordering': ['-added_at'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('thumbs_up_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='api.user')),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='api.user')),
            ],
            options={
                'db_table': 'post_likes',
                'unique_together': {('post', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('thumbs_up_count', models.IntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('parent_reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.reply')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='api.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='api.user')),
            ],
            options={
                'db_table': 'replies',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReplyLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.reply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to='api.user')),
            ],
            options={
                'db_table': 'reply_likes',
                'unique_together': {('reply', 'user')},
            },
        ),
        migrations.CreateModel(
            name='FCMToken',
            fields=[
                ('token', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('created_at', models.BigIntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fcm_tokens', to='api.user')),
            ],
            options={
                'db_table': 'fcm_tokens',
            },
        ),
    ]