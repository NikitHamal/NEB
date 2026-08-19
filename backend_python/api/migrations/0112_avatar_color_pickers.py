from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0111_avatar_customization'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_shape',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_expression',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_color',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_bg_color',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
    ]