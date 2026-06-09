"""Add StudySpace model and related models for multi-file study spaces.

- StudySpace: container for up to 5 documents, with share settings and linked generation
- StudySpaceShare: per-user access grants for space-level sharing
- StudySpaceQuiz/Question/Attempt: quizzes generated across all files in a space
- StudySpaceFlashcard/Review: flashcards generated across all files in a space
- StudyDocument.space: FK to StudySpace (nullable for backward compat)
- StudyDocument: removed per-document share fields (share_token, share_mode, shared_at) and legacy summary field
"""
from django.db import migrations
import django.db.migrations.operations as mops


def create_tables(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    charset = 'utf8mb4'
    collation = 'utf8mb4_unicode_ci'

    tables_sql = [
        f"""CREATE TABLE IF NOT EXISTS `study_spaces` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `user_id` varchar(36) NOT NULL,
            `title` varchar(200) NOT NULL DEFAULT '',
            `description` longtext NOT NULL,
            `share_token` varchar(64) NOT NULL,
            `share_mode` varchar(20) NOT NULL DEFAULT 'private',
            `shared_at` bigint NOT NULL DEFAULT 0,
            `link_summary_compact` longtext NOT NULL,
            `link_summary_detailed` longtext NOT NULL,
            `link_summary_generated_at` bigint NOT NULL DEFAULT 0,
            `link_mindmap_json` longtext NOT NULL,
            `link_mindmap_generated_at` bigint NOT NULL DEFAULT 0,
            `created_at` bigint NOT NULL DEFAULT 0,
            `updated_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_shares` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `space_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `granted_by_id` varchar(36) NOT NULL,
            `created_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_quizzes` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `space_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `title` varchar(500) NOT NULL DEFAULT '',
            `question_count` int unsigned NOT NULL DEFAULT 0,
            `created_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_quiz_questions` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `quiz_id` varchar(36) NOT NULL,
            `question_number` int unsigned NOT NULL DEFAULT 0,
            `question_text` longtext NOT NULL,
            `option_a` longtext NOT NULL DEFAULT '',
            `option_b` longtext NOT NULL DEFAULT '',
            `option_c` longtext NOT NULL DEFAULT '',
            `option_d` longtext NOT NULL DEFAULT '',
            `correct_answer` varchar(1) NOT NULL DEFAULT 'A',
            `explanation` longtext NOT NULL DEFAULT ''
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_quiz_attempts` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `quiz_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `score` int unsigned NOT NULL DEFAULT 0,
            `total_questions` int unsigned NOT NULL DEFAULT 0,
            `answers` longtext NOT NULL DEFAULT '',
            `xp_earned` int unsigned NOT NULL DEFAULT 0,
            `completed_at` bigint NOT NULL DEFAULT 0,
            `created_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_flashcards` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `space_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `front` longtext NOT NULL,
            `back` longtext NOT NULL,
            `card_number` int unsigned NOT NULL DEFAULT 0,
            `created_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
        f"""CREATE TABLE IF NOT EXISTS `study_space_flashcard_reviews` (
            `id` varchar(36) NOT NULL PRIMARY KEY,
            `flashcard_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `confidence` varchar(10) NOT NULL DEFAULT 'medium',
            `review_count` int unsigned NOT NULL DEFAULT 0,
            `last_reviewed_at` bigint NOT NULL DEFAULT 0,
            `next_review_at` bigint NOT NULL DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation}""",
    ]

    for sql in tables_sql:
        cursor.execute(sql)

    indexes_sql = [
        'CREATE INDEX IF NOT EXISTS `study_spaces_user_updated` ON `study_spaces` (`user_id`, `updated_at` DESC)',
        'CREATE INDEX IF NOT EXISTS `study_space_shares_space_user` ON `study_space_shares` (`space_id`, `user_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_shares_user_created` ON `study_space_shares` (`user_id`, `created_at` DESC)',
        'CREATE INDEX IF NOT EXISTS `study_space_quizzes_space` ON `study_space_quizzes` (`space_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_quizzes_user` ON `study_space_quizzes` (`user_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_quiz_questions_quiz` ON `study_space_quiz_questions` (`quiz_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_quiz_attempts_quiz` ON `study_space_quiz_attempts` (`quiz_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_quiz_attempts_user` ON `study_space_quiz_attempts` (`user_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_flashcards_space` ON `study_space_flashcards` (`space_id`)',
        'CREATE INDEX IF NOT EXISTS `study_space_flashcard_reviews_user_flash` ON `study_space_flashcard_reviews` (`user_id`, `flashcard_id`)',
    ]
    for sql in indexes_sql:
        try:
            cursor.execute(sql)
        except Exception:
            pass

    fk_sql = [
        """ALTER TABLE `study_space_shares`
            ADD CONSTRAINT `study_space_shares_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_shares_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_shares_granted_by_fk` FOREIGN KEY (`granted_by_id`) REFERENCES `users`(`id`) ON DELETE CASCADE""",
        """ALTER TABLE `study_space_quizzes`
            ADD CONSTRAINT `study_space_quizzes_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_quizzes_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE""",
        """ALTER TABLE `study_space_quiz_questions`
            ADD CONSTRAINT `study_space_quiz_questions_quiz_fk` FOREIGN KEY (`quiz_id`) REFERENCES `study_space_quizzes`(`id`) ON DELETE CASCADE""",
        """ALTER TABLE `study_space_quiz_attempts`
            ADD CONSTRAINT `study_space_quiz_attempts_quiz_fk` FOREIGN KEY (`quiz_id`) REFERENCES `study_space_quizzes`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_quiz_attempts_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE""",
        """ALTER TABLE `study_space_flashcards`
            ADD CONSTRAINT `study_space_flashcards_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_flashcards_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE""",
        """ALTER TABLE `study_space_flashcard_reviews`
            ADD CONSTRAINT `study_space_flashcard_reviews_flashcard_fk` FOREIGN KEY (`flashcard_id`) REFERENCES `study_space_flashcards`(`id`) ON DELETE CASCADE,
            ADD CONSTRAINT `study_space_flashcard_reviews_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE""",
    ]
    for sql in fk_sql:
        try:
            cursor.execute(sql)
        except Exception:
            pass

    try:
        cursor.execute("ALTER TABLE `study_documents` ADD COLUMN `space_id` varchar(36) NULL")
    except Exception:
        pass
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS `study_documents_space_updated` ON `study_documents` (`space_id`, `updated_at` DESC)")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE `study_documents` ADD CONSTRAINT `study_documents_space_fk` FOREIGN KEY (`space_id`) REFERENCES `study_spaces`(`id`) ON DELETE CASCADE")
    except Exception:
        pass


def reverse_tables(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0051_study_document_sharing'),
    ]

    operations = [
        mops.RunPython(create_tables, reverse_tables),
    ]