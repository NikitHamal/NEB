from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_performance_indexes'),
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