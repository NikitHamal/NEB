# Hand-written migration: composite indexes for hot query paths + User.email index.
#
# - Resource: (approval_status, is_lead, -added_at) and
#             (approval_status, is_lead, -view_count) — cover the home/library
#             "approved lead resources" listings sorted by recency/popularity.
# - Post:     (category, is_archived, -created_at) — covers the forum category
#             listing filtered to non-archived posts sorted by recency.
# - User.email: db_index=True for OAuth/email-login lookups.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_study_space_learning_plan'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(
                fields=['approval_status', 'is_lead', '-added_at'],
                name='res_appr_lead_added_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(
                fields=['approval_status', 'is_lead', '-view_count'],
                name='res_appr_lead_views_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(
                fields=['category', 'is_archived', '-created_at'],
                name='post_cat_arch_created_idx',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, db_index=True, max_length=254, null=True),
        ),
    ]
