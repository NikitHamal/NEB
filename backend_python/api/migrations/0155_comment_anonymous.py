from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0154_merge_forum_categories_and_agent_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='resourcecomment',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
