from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_merge_0108_leaves'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username_changed_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='username_change_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]