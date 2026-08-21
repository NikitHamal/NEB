"""Management command to clean up stale data.

Removes:
- Expired verification codes (clears the code + resets attempts)
- Stale FCM tokens older than --fcm-days days (default 90)
- Abandoned Django sessions older than --session-days days (default 30)
- Unverified email accounts older than --unverified-days days (default 365)

Usage:
    python manage.py cleanup_stale_data
    python manage.py cleanup_stale_data --fcm-days 60 --session-days 7
"""
import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import User, FCMToken


class Command(BaseCommand):
    help = 'Remove expired verification codes, stale FCM tokens, old sessions, and abandoned unverified accounts.'

    def add_arguments(self, parser):
        parser.add_argument('--fcm-days', type=int, default=90, help='Remove FCM tokens older than this many days.')
        parser.add_argument('--session-days', type=int, default=30, help='Remove Django sessions older than this many days.')
        parser.add_argument('--unverified-days', type=int, default=365, help='Remove unverified accounts older than this many days.')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting.')

    def handle(self, *args, **options):
        now_ms = int(time.time() * 1000)
        dry_run = options['dry_run']
        prefix = '[DRY RUN] ' if dry_run else ''

        # 1. Clear expired verification codes
        expired_codes = User.objects.filter(
            verification_code_expires__gt=0,
            verification_code_expires__lt=now_ms,
        )
        count = expired_codes.count()
        self.stdout.write(f'{prefix}Clearing {count} expired verification codes.')
        if not dry_run:
            expired_codes.update(
                verification_code=None,
                verification_code_expires=0,
                verification_code_purpose='',
                verification_code_attempts=0,
            )

        # 2. Remove stale FCM tokens
        fcm_cutoff = now_ms - (options['fcm_days'] * 86400 * 1000)
        stale_tokens = FCMToken.objects.filter(created_at__lt=fcm_cutoff)
        count = stale_tokens.count()
        self.stdout.write(f'{prefix}Removing {count} stale FCM tokens (older than {options["fcm_days"]} days).')
        if not dry_run:
            stale_tokens.delete()

        # 3. Clear abandoned Django sessions
        from django.contrib.sessions.models import Session
        session_cutoff = timezone.now() - timezone.timedelta(days=options['session_days'])
        old_sessions = Session.objects.filter(expire_date__lt=session_cutoff)
        count = old_sessions.count()
        self.stdout.write(f'{prefix}Removing {count} expired Django sessions (older than {options["session_days"]} days).')
        if not dry_run:
            old_sessions.delete()

        # 4. Remove long-abandoned unverified accounts
        unverified_cutoff = now_ms - (options['unverified_days'] * 86400 * 1000)
        abandoned = User.objects.filter(
            email_verified=False,
            created_at__gt=0,
            created_at__lt=unverified_cutoff,
        )
        count = abandoned.count()
        self.stdout.write(f'{prefix}Removing {count} abandoned unverified accounts (older than {options["unverified_days"]} days).')
        if not dry_run:
            abandoned.delete()

        # 5. Remove unused inline content images (orphan uploads, 48h old)
        cutoff_48h = now_ms - 48 * 3600 * 1000
        try:
            from api.models import ContentImage
            from api.content_images import delete_files
            stale = ContentImage.objects.filter(used=False, created_at__lt=cutoff_48h)
            count = stale.count()
            self.stdout.write(f'{prefix}Removing {count} unused inline images (older than 48h).')
            if not dry_run:
                for row in stale[:500]:
                    delete_files(row)
                stale.delete()
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f'Skipped inline-image cleanup: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'{prefix}Cleanup complete.'))