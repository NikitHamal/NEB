# Generated manually for NEBians security hardening.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_email_auth_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code_purpose',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code_attempts',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code_last_sent_at',
            field=models.BigIntegerField(default=0),
        ),
    ]
