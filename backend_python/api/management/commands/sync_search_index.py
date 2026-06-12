"""Sync database content to Meilisearch for full-text search."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sync database content to Meilisearch. Creates indexes and bulk-syncs resources, posts, and users.'

    def add_arguments(self, parser):
        parser.add_argument('--resources-only', action='store_true', help='Only sync resources')
        parser.add_argument('--posts-only', action='store_true', help='Only sync posts')
        parser.add_argument('--users-only', action='store_true', help='Only sync users')
        parser.add_argument('--ensure-indexes', action='store_true', help='Only create/update index settings, no data sync')

    def handle(self, *args, **options):
        from api.search import is_enabled, sync_all, sync_resources, sync_posts, sync_users, _ensure_indexes

        if not is_enabled():
            self.stderr.write(self.style.ERROR('Meilisearch is not configured. Set MEILISEARCH_URL in settings/.env.'))
            return

        if options['ensure_indexes']:
            _ensure_indexes()
            self.stdout.write(self.style.SUCCESS('Index settings updated.'))
            return

        if options['resources_only']:
            count = sync_resources()
            self.stdout.write(self.style.SUCCESS(f'Synced {count} resources.'))
            return

        if options['posts_only']:
            count = sync_posts()
            self.stdout.write(self.style.SUCCESS(f'Synced {count} posts.'))
            return

        if options['users_only']:
            count = sync_users()
            self.stdout.write(self.style.SUCCESS(f'Synced {count} users.'))
            return

        total = sync_all()
        self.stdout.write(self.style.SUCCESS(f'Synced all content (total documents: {total}).'))