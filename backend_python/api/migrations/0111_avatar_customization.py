from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0110_username_change_cooldown'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_bg',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_hue',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_tone',
            field=models.FloatField(default=-1.0),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_anim',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]