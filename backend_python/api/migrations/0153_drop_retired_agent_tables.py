from django.db import connection, migrations

# The background coding agent, the Neby Code IDE and the Lazy agentic workspace
# were removed from the codebase. These are their models and their tables.
#
# SeparateDatabaseAndState is used rather than plain DeleteModel because these
# tables were created before the users table was converted to utf8mb4, so
# MariaDB refuses a plain DROP TABLE chain while child foreign keys still
# point at a parent. MySQL therefore needs FOREIGN_KEY_CHECKS off for the
# duration; SQLite (what the test runner uses) rejects that statement outright,
# so the drop branches on the backend.
#
# A full DB backup was taken before this migration was written.

DELETE_MODELS = [
    'BackgroundAgentAction',
    'BackgroundAgentArtifact',
    'BackgroundAgentAttachment',
    'BackgroundAgentAutofixRun',
    'BackgroundAgentCredential',
    'BackgroundAgentDevicePairing',
    'BackgroundAgentDeviceToken',
    'BackgroundAgentEvent',
    'BackgroundAgentMessage',
    'BackgroundAgentProject',
    'BackgroundAgentSession',
    'BackgroundAgentWorker',
    'CodeMessage',
    'CodeSession',
    'LazyAgentRun',
    'LazyAgentStep',
    'LazyArtifact',
    'LazyDocMessage',
    'LazyDocSession',
]

DROP_TABLES = [
    'background_agent_actions',
    'background_agent_artifacts',
    'background_agent_attachments',
    'background_agent_autofix_runs',
    'background_agent_credentials',
    'background_agent_device_pairings',
    'background_agent_device_tokens',
    'background_agent_events',
    'background_agent_messages',
    'background_agent_projects',
    'background_agent_sessions',
    'background_agent_workers',
    'code_messages',
    'code_sessions',
    'lazy_agent_runs',
    'lazy_agent_steps',
    'lazy_artifacts',
    'lazy_doc_messages',
    'lazy_doc_sessions',
]


def drop_retired_agent_tables(apps, schema_editor):
    is_mysql = connection.vendor == 'mysql'
    quote = '`%s`' if is_mysql else '"%s"'
    with connection.cursor() as cursor:
        if is_mysql:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0')
        try:
            for table in DROP_TABLES:
                cursor.execute('DROP TABLE IF EXISTS ' + (quote % table))
        finally:
            if is_mysql:
                cursor.execute('SET FOREIGN_KEY_CHECKS=1')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0151_keep_deleted_user_content'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name=name) for name in DELETE_MODELS
            ],
            database_operations=[
                migrations.RunPython(drop_retired_agent_tables, migrations.RunPython.noop),
            ],
        ),
    ]
