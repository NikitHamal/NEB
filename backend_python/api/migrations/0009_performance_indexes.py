from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_banner_url_and_reports'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['user_id', '-created_at'], name='api_post_user_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['category'], name='api_post_category_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_archived', '-created_at'], name='api_post_archived_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-thumbs_up_count'], name='api_post_thumbs_idx'),
        ),
        migrations.AddIndex(
            model_name='reply',
            index=models.Index(fields=['post_id', 'created_at'], name='api_reply_post_created_idx'),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(fields=['subject'], name='api_resource_subject_idx'),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(fields=['grade_level'], name='api_resource_grade_idx'),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(fields=['type'], name='api_resource_type_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['following_id'], name='api_follow_following_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['follower_id'], name='api_follow_follower_idx'),
        ),
        migrations.AddIndex(
            model_name='fcmtoken',
            index=models.Index(fields=['user_id'], name='api_fcmtoken_user_idx'),
        ),
        migrations.AddIndex(
            model_name='userphoto',
            index=models.Index(fields=['user_id'], name='api_userphoto_user_idx'),
        ),
        migrations.AddIndex(
            model_name='edithistory',
            index=models.Index(fields=['target_type', 'target_id'], name='api_edithistory_target_idx'),
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['status', '-created_at'], name='api_report_status_created_idx'),
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['target_type', 'target_id'], name='api_report_target_idx'),
        ),
    ]