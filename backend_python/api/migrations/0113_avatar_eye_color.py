from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_avatar_color_pickers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_eye_color',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
    ]