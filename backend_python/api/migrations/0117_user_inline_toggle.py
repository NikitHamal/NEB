from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_content_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enable_inline_images',
            field=models.BooleanField(default=True),
        ),
    ]
