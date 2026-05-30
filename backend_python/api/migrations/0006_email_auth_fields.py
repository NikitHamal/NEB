# Generated migration for email auth fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_add_edit_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_hash',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(max_length=6, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code_expires',
            field=models.BigIntegerField(default=0),
        ),
    ]