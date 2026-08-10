from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_neby_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='thumbnail_url',
            field=models.TextField(blank=True, default=''),
        ),
    ]
