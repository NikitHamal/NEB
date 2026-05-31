from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_bookmarks_and_reply_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unread_notification_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('verb', models.CharField(choices=[('like_post', 'Liked your post'), ('like_reply', 'Liked your reply'), ('reply', 'Replied to your post'), ('reply_reply', 'Replied to your comment'), ('follow', 'Started following you'), ('mention', 'Mentioned you'), ('system', 'System notification')], max_length=20)),
                ('target_type', models.CharField(choices=[('post', 'Post'), ('reply', 'Reply'), ('user', 'User'), ('system', 'System')], max_length=10)),
                ('target_id', models.CharField(max_length=36)),
                ('reference_type', models.CharField(default='', max_length=10, blank=True)),
                ('reference_id', models.CharField(default='', max_length=36, blank=True)),
                ('message', models.TextField(blank=True, default='')),
                ('is_read', models.BooleanField(default=False, db_index=True)),
                ('created_at', models.BigIntegerField()),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_sent', to='api.user')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='api.user')),
            ],
            options={
                'db_table': 'notifications',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['recipient_id', '-created_at'], name='notif_recip_time_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['recipient_id', 'is_read', '-created_at'], name='notif_recip_unread_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['target_type', 'target_id'], name='notif_target_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['recipient_id', 'actor_id', 'verb', 'target_type', 'target_id'], name='notif_dedup_idx'),
        ),
    ]