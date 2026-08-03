from django.db import migrations


def to_mediumtext(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    if schema_editor.connection.vendor == 'sqlite':
        return
    cursor.execute(
        "ALTER TABLE background_agent_messages "
        "MODIFY content MEDIUMTEXT, MODIFY metadata MEDIUMTEXT;"
    )
    cursor.execute(
        "ALTER TABLE background_agent_events "
        "MODIFY payload MEDIUMTEXT;"
    )


def to_text(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    if schema_editor.connection.vendor == 'sqlite':
        return
    cursor.execute(
        "ALTER TABLE background_agent_messages "
        "MODIFY content TEXT, MODIFY metadata TEXT;"
    )
    cursor.execute(
        "ALTER TABLE background_agent_events "
        "MODIFY payload TEXT;"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_background_agent_mobile_and_archive'),
    ]

    operations = [
        # On MySQL/MariaDB, alter TEXT columns to MEDIUMTEXT so we can store
        # raw model responses, full prompts, tool results, and event payloads
        # without truncation. No-op on SQLite, which has no MEDIUMTEXT.
        migrations.RunPython(to_mediumtext, to_text),
    ]
