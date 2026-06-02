import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_resourcerequest_resourcerequestupvote_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resources/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='file_url',
            field=models.TextField(blank=True, default=''),
        ),
    ]