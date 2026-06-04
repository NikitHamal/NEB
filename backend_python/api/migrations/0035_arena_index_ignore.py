# Arena index name normalization - state-only, no DB changes.
# Django's auto-naming detected mismatches between local SQLite and what
# the model Meta.indexes would generate. These are cosmetic renames that
# should NOT touch the production DB (the indexes already exist under
# different names). We use SeparateDatabaseAndState to update Django's
# internal state without running ALTER INDEX on MariaDB.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_botconfig_cleanup'),
    ]

    operations = [
        # These rename operations only update Django's migration state.
        # The actual indexes on MariaDB may have different names (or may
        # not exist at all). We skip the database side entirely.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameIndex(
                    model_name='arenachatmessage',
                    new_name='arena_chat__session_5d4fbf_idx',
                    old_name='arena_msg_session_created_idx',
                ),
                migrations.RenameIndex(
                    model_name='arenachatsession',
                    new_name='arena_chat__user_id_89d2d5_idx',
                    old_name='arena_chat_user_update_idx',
                ),
                migrations.RenameIndex(
                    model_name='arenachatsession',
                    new_name='arena_chat__user_id_98366e_idx',
                    old_name='arena_chat_user_activ_idx',
                ),
            ],
            database_operations=[],
        ),
    ]