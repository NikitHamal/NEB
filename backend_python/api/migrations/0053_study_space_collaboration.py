"""Future-proof StudySpace sharing, invite codes, public spaces, and member roles.

The StudySpace tables were created with raw SQL in 0052, so this migration also
uses defensive raw SQL instead of Django state-dependent AddField/CreateModel
operations. It is intentionally idempotent for cPanel/LiteSpeed deployments where
migrations may be retried.
"""
from django.db import migrations
import django.db.migrations.operations as mops
import random
import string


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


def _new_code(existing):
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(alphabet) for _ in range(8))
        if code not in existing:
            existing.add(code)
            return code


def forwards(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    vendor = schema_editor.connection.vendor

    if not _table_exists(cursor, 'study_spaces'):
        return

    if vendor == 'sqlite':
        _add_column_if_missing(cursor, 'study_spaces', 'invite_code', "ALTER TABLE study_spaces ADD COLUMN invite_code varchar(12) NOT NULL DEFAULT ''")
        _add_column_if_missing(cursor, 'study_spaces', 'visibility', "ALTER TABLE study_spaces ADD COLUMN visibility varchar(20) NOT NULL DEFAULT 'private'")
        _add_column_if_missing(cursor, 'study_spaces', 'allow_join_by_code', "ALTER TABLE study_spaces ADD COLUMN allow_join_by_code bool NOT NULL DEFAULT 1")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS study_space_members ("
            "id varchar(36) NOT NULL PRIMARY KEY, "
            "space_id varchar(36) NOT NULL, "
            "user_id varchar(36) NOT NULL, "
            "role varchar(20) NOT NULL DEFAULT 'member', "
            "invited_by_id varchar(36) NULL, "
            "joined_at bigint NOT NULL DEFAULT 0, "
            "updated_at bigint NOT NULL DEFAULT 0, "
            "UNIQUE(space_id, user_id))"
        )
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_spaces_invite_code_idx ON study_spaces(invite_code)")
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_spaces_visibility_idx ON study_spaces(visibility)")
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_space_members_space_role_idx ON study_space_members(space_id, role)")
        _safe_exec(cursor, "CREATE INDEX IF NOT EXISTS study_space_members_user_joined_idx ON study_space_members(user_id, joined_at DESC)")
    else:
        _add_column_if_missing(cursor, 'study_spaces', 'invite_code', "ALTER TABLE `study_spaces` ADD COLUMN `invite_code` varchar(12) NOT NULL DEFAULT ''")
        _add_column_if_missing(cursor, 'study_spaces', 'visibility', "ALTER TABLE `study_spaces` ADD COLUMN `visibility` varchar(20) NOT NULL DEFAULT 'private'")
        _add_column_if_missing(cursor, 'study_spaces', 'allow_join_by_code', "ALTER TABLE `study_spaces` ADD COLUMN `allow_join_by_code` tinyint(1) NOT NULL DEFAULT 1")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `study_space_members` ("
            "`id` varchar(36) NOT NULL PRIMARY KEY, "
            "`space_id` varchar(36) NOT NULL, "
            "`user_id` varchar(36) NOT NULL, "
            "`role` varchar(20) NOT NULL DEFAULT 'member', "
            "`invited_by_id` varchar(36) NULL, "
            "`joined_at` bigint NOT NULL DEFAULT 0, "
            "`updated_at` bigint NOT NULL DEFAULT 0, "
            "UNIQUE KEY `study_space_members_space_user_uniq` (`space_id`, `user_id`), "
            "KEY `study_space_members_space_role_idx` (`space_id`, `role`), "
            "KEY `study_space_members_user_joined_idx` (`user_id`, `joined_at` DESC)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        _safe_exec(cursor, "CREATE UNIQUE INDEX `study_spaces_invite_code_uniq` ON `study_spaces` (`invite_code`)")
        _safe_exec(cursor, "CREATE INDEX `study_spaces_visibility_idx` ON `study_spaces` (`visibility`)")
        _safe_exec(cursor, "ALTER TABLE `study_space_members` ADD CONSTRAINT `study_space_members_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE")
        _safe_exec(cursor, "ALTER TABLE `study_space_members` ADD CONSTRAINT `study_space_members_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE")
        _safe_exec(cursor, "ALTER TABLE `study_space_members` ADD CONSTRAINT `study_space_members_invited_by_fk` FOREIGN KEY (`invited_by_id`) REFERENCES `users`(`id`) ON DELETE SET NULL")

    # Backfill stable invite codes and owner memberships.
    cursor.execute("SELECT id, user_id, created_at FROM study_spaces")
    rows = cursor.fetchall()
    cursor.execute("SELECT invite_code FROM study_spaces WHERE invite_code <> ''")
    existing_codes = {r[0] for r in cursor.fetchall() if r[0]}
    for sid, uid, created_at in rows:
        if not sid or not uid:
            continue
        cursor.execute("SELECT invite_code FROM study_spaces WHERE id=%s", [sid])
        current_code = (cursor.fetchone() or [''])[0]
        if not current_code:
            code = _new_code(existing_codes)
            cursor.execute("UPDATE study_spaces SET invite_code=%s WHERE id=%s", [code, sid])
        cursor.execute("SELECT id FROM study_space_members WHERE space_id=%s AND user_id=%s", [sid, uid])
        if cursor.fetchone() is None:
            mid = f"owner-{sid}"[:36]
            stamp = created_at or 0
            cursor.execute(
                "INSERT INTO study_space_members (id, space_id, user_id, role, invited_by_id, joined_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                [mid, sid, uid, 'owner', None, stamp, stamp],
            )

    if vendor == 'sqlite':
        _safe_exec(cursor, "CREATE UNIQUE INDEX IF NOT EXISTS study_spaces_invite_code_uniq ON study_spaces(invite_code) WHERE invite_code <> ''")
    else:
        _safe_exec(cursor, "CREATE UNIQUE INDEX `study_spaces_invite_code_uniq` ON `study_spaces` (`invite_code`)")


def backwards(apps, schema_editor):
    # Keep data on rollback; this is safer for production and matches 0052 style.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0052_study_spaces'),
    ]

    operations = [
        mops.RunPython(forwards, backwards),
    ]
