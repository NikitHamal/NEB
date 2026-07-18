from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_background_agent_mobile_and_archive'),
    ]

    operations = [
        # On MySQL/MariaDB, alter TEXT columns to MEDIUMTEXT so we can store
        # raw model responses, full prompts, tool results, and event payloads
        # without truncation.
        migrations.RunSQL(
            sql="""
                ALTER TABLE background_agent_messages
                MODIFY content MEDIUMTEXT,
                MODIFY metadata MEDIUMTEXT;
            """,
            reverse_sql="""
                ALTER TABLE background_agent_messages
                MODIFY content TEXT,
                MODIFY metadata TEXT;
            """,
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE background_agent_events
                MODIFY payload MEDIUMTEXT;
            """,
            reverse_sql="""
                ALTER TABLE background_agent_events
                MODIFY payload TEXT;
            """,
        ),
    ]
