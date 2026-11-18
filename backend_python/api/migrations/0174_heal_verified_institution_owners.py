"""Link every verified institution account to its Institution row (adds or links only, deletes nothing)."""
import logging

from django.db import migrations

log = logging.getLogger(__name__)


def heal(apps, schema_editor):
    try:
        from api.institutions import heal_owner
        from api.models import User
        done = 0
        for user in User.objects.filter(role='institution', institution_verified=True).iterator():
            try:
                if heal_owner(user):
                    done += 1
            except Exception:
                log.exception('heal_owner failed for %s', user.pk)
        log.info('verified institution accounts linked: %s', done)
    except Exception:
        log.exception('heal_verified_institution_owners skipped')


class Migration(migrations.Migration):
    dependencies = [('api', '0173_user_cover_art')]
    operations = [migrations.RunPython(heal, migrations.RunPython.noop)]
