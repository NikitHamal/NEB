"""H2/H3 (Sep 2026 security fixes).

Schema:
- User.is_banned (admin ban; distinct from the is_locked privacy toggle).
- UserAuthToken.expires_at (ms epoch; 0 = expired, fail closed).

Data backfill (idempotent): expires_at = created_at + 30d for rows where
it is 0 (ancient rows get now + 7d grace).

Note: the CodingAgentProject table was dropped by migration 0089 and does
not exist in production, so there are no plaintext GitHub tokens to
backfill. New tokens are encrypted by api/coding_agent/crypto.py at write
time whenever the table exists again.
"""

import time

from django.db import migrations, models


TOKEN_TTL_MS = 30 * 24 * 3600 * 1000
GRACE_MS = 7 * 24 * 3600 * 1000


def backfill_expires_at(apps, schema_editor):
    UserAuthToken = apps.get_model('api', 'UserAuthToken')
    now = int(time.time() * 1000)
    for row in UserAuthToken.objects.filter(expires_at=0).only('id', 'created_at', 'revoked_at'):
        if row.revoked_at:
            continue
        base = row.created_at or now
        row.expires_at = base + TOKEN_TTL_MS
        if row.expires_at <= now:
            row.expires_at = now + GRACE_MS
        row.save(update_fields=['expires_at'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0140_alter_arenachatsession_provider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userauthtoken',
            name='expires_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.RunPython(backfill_expires_at, migrations.RunPython.noop),
    ]
