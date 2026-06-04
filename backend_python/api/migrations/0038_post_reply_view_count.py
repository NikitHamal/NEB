from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_resource_is_lead_resource_upload_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-view_count'], name='api_post_view_co_idx'),
        ),
    ]