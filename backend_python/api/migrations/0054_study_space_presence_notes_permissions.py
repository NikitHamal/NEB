"""Add StudySpace presence, shared notes, metadata, and permission columns.

Uses defensive raw SQL to match the existing StudySpace migration style and to be
safe on retried production deployments.
"""
from django.db import migrations
import django.db.migrations.operations as mops


def _table_columns(cursor, table):
    vendor = cursor.db.vendor
    if vendor == 'sqlite':
        cursor.execute(f"PRAGMA table_info({table})")
        return {row[1] for row in cursor.fetchall()}
    cursor.execute(f"SHOW COLUMNS FROM `{table}`")
    return {row[0] for row in cursor.fetchall()}


def _table_exists(cursor, table):
    vendor = cursor.db.vendor
    if vendor == 'sqlite':
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=%s", [table])
        return cursor.fetchone() is not None
    cursor.execute("SHOW TABLES LIKE %s", [table])
    return cursor.fetchone() is not None


def _add_column_if_missing(cursor, table, column, sql):
    if column in _table_columns(cursor, table):
        return
    cursor.execute(sql)


def _safe_exec(cursor, sql):
    try:
        cursor.execute(sql)
    except Exception:
        pass


def forwards(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    vendor = schema_editor.connection.vendor
    if not _table_exists(cursor, 'study_spaces'):
        return

    cols = [
        ('study_level', "varchar(80) NOT NULL DEFAULT ''"),
        ('subject', "varchar(120) NOT NULL DEFAULT ''"),
        ('exam', "varchar(120) NOT NULL DEFAULT ''"),
        ('generate_min_role', "varchar(20) NOT NULL DEFAULT 'moderator'"),
        ('upload_min_role', "varchar(20) NOT NULL DEFAULT 'member'"),
        ('invite_min_role', "varchar(20) NOT NULL DEFAULT 'admin'"),
        ('moderate_min_role', "varchar(20) NOT NULL DEFAULT 'moderator'"),
        ('publish_min_role', "varchar(20) NOT NULL DEFAULT 'owner'"),
    ]
    for name, spec in cols:
        if vendor == 'sqlite':
            _add_column_if_missing(cursor, 'study_spaces', name, f"ALTER TABLE study_spaces ADD COLUMN {name} {spec}")
        else:
            _add_column_if_missing(cursor, 'study_spaces', name, f"ALTER TABLE `study_spaces` ADD COLUMN `{name}` {spec}")

    if vendor == 'sqlite':
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS study_space_notes ("
            "id varchar(36) NOT NULL PRIMARY KEY, "
            "space_id varchar(36) NOT NULL UNIQUE, "
            "content text NOT NULL DEFAULT '', "
            "updated_by_id varchar(36) NULL, "
            "version integer NOT NULL DEFAULT 1, "
            "created_at bigint NOT NULL DEFAULT 0, "
            "updated_at bigint NOT NULL DEFAULT 0)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS study_space_presence ("
            "id varchar(36) NOT NULL PRIMARY KEY, "
            "space_id varchar(36) NOT NULL, "
            "user_id varchar(36) NOT NULL, "
            "status varchar(20) NOT NULL DEFAULT 'inside', "
            "current_tab varchar(40) NOT NULL DEFAULT '', "
            "current_document_id varchar(36) NOT NULL DEFAULT '', "
            "detail varchar(120) NOT NULL DEFAULT '', "
            "is_typing bool NOT NULL DEFAULT 0, "
            "session_id varchar(64) NOT NULL DEFAULT '', "
            "last_seen_at bigint NOT NULL DEFAULT 0, "
            "updated_at bigint NOT NULL DEFAULT 0, "
            "UNIQUE(space_id, user_id))"
        )
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_space_presence_space_seen_idx ON study_space_presence(space_id, last_seen_at DESC)")
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_space_presence_user_seen_idx ON study_space_presence(user_id, last_seen_at DESC)")
    else:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `study_space_notes` ("
            "`id` varchar(36) NOT NULL PRIMARY KEY, "
            "`space_id` varchar(36) NOT NULL UNIQUE, "
            "`content` longtext NOT NULL, "
            "`updated_by_id` varchar(36) NULL, "
            "`version` int NOT NULL DEFAULT 1, "
            "`created_at` bigint NOT NULL DEFAULT 0, "
            "`updated_at` bigint NOT NULL DEFAULT 0"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `study_space_presence` ("
            "`id` varchar(36) NOT NULL PRIMARY KEY, "
            "`space_id` varchar(36) NOT NULL, "
            "`user_id` varchar(36) NOT NULL, "
            "`status` varchar(20) NOT NULL DEFAULT 'inside', "
            "`current_tab` varchar(40) NOT NULL DEFAULT '', "
            "`current_document_id` varchar(36) NOT NULL DEFAULT '', "
            "`detail` varchar(120) NOT NULL DEFAULT '', "
            "`is_typing` tinyint(1) NOT NULL DEFAULT 0, "
            "`session_id` varchar(64) NOT NULL DEFAULT '', "
            "`last_seen_at` bigint NOT NULL DEFAULT 0, "
            "`updated_at` bigint NOT NULL DEFAULT 0, "
            "UNIQUE KEY `study_space_presence_space_user_uniq` (`space_id`, `user_id`), "
            "KEY `study_space_presence_space_seen_idx` (`space_id`, `last_seen_at` DESC), "
            "KEY `study_space_presence_user_seen_idx` (`user_id`, `last_seen_at` DESC)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        _safe_exec(cursor, "ALTER TABLE `study_space_notes` ADD CONSTRAINT `study_space_notes_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE")
        _safe_exec(cursor, "ALTER TABLE `study_space_notes` ADD CONSTRAINT `study_space_notes_updated_by_fk` FOREIGN KEY (`updated_by_id`) REFERENCES `users`(`id`) ON DELETE SET NULL")
        _safe_exec(cursor, "ALTER TABLE `study_space_presence` ADD CONSTRAINT `study_space_presence_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE")
        _safe_exec(cursor, "ALTER TABLE `study_space_presence` ADD CONSTRAINT `study_space_presence_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE")


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0053_study_space_collaboration'),
    ]

    operations = [
        mops.RunPython(forwards, backwards),
    ]
