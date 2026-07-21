# Generated for voice-note/media attachments on blog comments

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0099_resource_comment_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCommentMedia',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('kind', models.CharField(choices=[('video', 'Video'), ('audio', 'Audio'), ('file', 'File')], default='file', max_length=10)),
                ('url', models.TextField()),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('mime_type', models.CharField(blank=True, default='', max_length=120)),
                ('size_bytes', models.BigIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='api.blogcomment')),
            ],
            options={
                'db_table': 'blog_comment_media',
                'ordering': ['order', 'created_at'],
                'indexes': [models.Index(fields=['comment_id', 'order'], name='blog_commen_comment_f1ab0f_idx')],
            },
        ),
    ]
