# Attachments on resource comments (voice notes / audio / video / files) —
# mirrors PostMedia from 0098_anonymous_forum_media for forum content.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_anonymous_forum_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceCommentMedia',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('kind', models.CharField(choices=[('video', 'Video'), ('audio', 'Audio'), ('file', 'File')], default='file', max_length=10)),
                ('url', models.TextField()),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('mime_type', models.CharField(blank=True, default='', max_length=120)),
                ('size_bytes', models.BigIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='api.resourcecomment')),
            ],
            options={
                'db_table': 'resource_comment_media',
                'ordering': ['order', 'created_at'],
                'indexes': [models.Index(fields=['comment_id', 'order'], name='resource_co_comment_2f3f1a_idx')],
            },
        ),
    ]
