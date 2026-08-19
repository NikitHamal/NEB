from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0114_botconfig_fallback_chain'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_use_pp',
            field=models.BooleanField(default=False),
        ),
    ]
