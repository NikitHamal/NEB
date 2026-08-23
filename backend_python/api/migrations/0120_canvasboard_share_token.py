from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_rename_ai_fb_surf_created_idx_ai_feedback_surface_223784_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvasboard',
            name='share_token',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='canvasboard',
            name='shared_at',
            field=models.BigIntegerField(default=0),
        ),
    ]
