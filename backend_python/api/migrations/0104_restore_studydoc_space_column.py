"""Repair study_documents.space_id for SQLite test databases.

Migration 0052 added the `space_id` column to `study_documents` with raw SQL
(not part of Django's model state at the time). On SQLite, the AddField
migrations in 0055 rebuild the table and drop columns that are not in the
model state, leaving the `studydoc_space_status_idx` index (created in 0066)
referencing a missing column. SQLite re-validates the whole schema on any DDL,
so later migrations (e.g. 0080's DROP COLUMN) fail with
"error in index studydoc_space_status_idx after drop column: no such column:
space_id".

This migration re-creates the column when it is missing. MariaDB production
already has it (raw SQL there succeeded), so this is a no-op on non-SQLite
vendors.
"""
from django.db import migrations


def restore_space_column(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    if schema_editor.connection.vendor == 'sqlite':
        columns = [row[1] for row in cursor.execute('PRAGMA table_info(study_documents)')]
        if 'space_id' not in columns:
            cursor.execute('ALTER TABLE study_documents ADD COLUMN space_id varchar(36) NULL')
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'study_documents' "
            "AND COLUMN_NAME = 'space_id'"
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute('ALTER TABLE `study_documents` ADD COLUMN `space_id` varchar(36) NULL')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_remove_g4f_freegpt_deepseekai_surfsense_eqing'),
    ]

    operations = [
        migrations.RunPython(restore_space_column, noop),
    ]
