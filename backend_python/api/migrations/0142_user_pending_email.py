"""Adds User.pending_email for the confirmed email-change flow.

The address a user types into Settings > Account security is parked here
until a code sent to it comes back verified; only then does `email` move.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_token_expiry_ban_and_coding_token_crypto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pending_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
