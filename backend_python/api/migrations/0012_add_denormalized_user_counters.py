from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_reply_count_and_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contribution_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='follower_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='likes_given_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='likes_received_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='post_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='reply_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]