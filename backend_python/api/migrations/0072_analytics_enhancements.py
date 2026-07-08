from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_merge_20260707_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_active',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pageview',
            name='user_identifier',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='avg_session_duration',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='bounce_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='total_sessions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='pages_per_session',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dailystat',
            name='peak_hour',
            field=models.IntegerField(default=0),
        ),
        # Indexes already exist from 0070 migration — model now has matching
        # explicit names, so no AlterIndex/AddIndex needed.
    ]
