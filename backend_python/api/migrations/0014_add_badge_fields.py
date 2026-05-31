from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_backfill_user_counters'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_level',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='moderator_level',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='achievement_badges',
            field=models.TextField(blank=True, default=''),
        ),
    ]