from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_api_edithistory_target_idx_edit_histor_target__ea3ea5_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='reply_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name='reply',
            index=models.Index(fields=['parent_reply_id', 'created_at'], name='replies_parent__7d68d0_idx'),
        ),
    ]