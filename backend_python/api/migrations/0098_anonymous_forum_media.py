# Anonymous posting/commenting flags, forum media attachments, and
# notification actor masking — Pass 12 feature drop.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_alter_userllmprovider_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reply',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='actor_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('kind', models.CharField(choices=[('video', 'Video'), ('audio', 'Audio'), ('file', 'File')], default='file', max_length=10)),
                ('url', models.TextField()),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('mime_type', models.CharField(blank=True, default='', max_length=120)),
                ('size_bytes', models.BigIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='api.post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='api.reply')),
            ],
            options={
                'db_table': 'post_media',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='postmedia',
            index=models.Index(fields=['post_id', 'order'], name='post_media_post_order_idx'),
        ),
        migrations.AddIndex(
            model_name='postmedia',
            index=models.Index(fields=['reply_id', 'order'], name='post_media_reply_order_idx'),
        ),
    ]
