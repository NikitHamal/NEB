"""Auto-fix watcher daemon - REMOVED (Sep 2026 security audit).

Kept as a no-op so existing cron entries fail closed with a clear message
instead of crashing. Remove the cron entry at will.
"""
from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Disabled: the CI auto-fix watcher was removed for security reasons.'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=120)
        parser.add_argument('--once', action='store_true')
        parser.add_argument('--max-sessions', type=int, default=3)

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'autofix watcher has been removed and does nothing. '
            'You can safely delete its cron entry.'
        ))
