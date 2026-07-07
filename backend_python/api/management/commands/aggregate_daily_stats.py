"""
Management command: aggregate_daily_stats

Computes and stores DailyStat records from raw PageView data.
Run daily via cron: python manage.py aggregate_daily_stats
"""
import time
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db.models import Count
from api.models import PageView, DailyStat, User, Post, Reply, Resource


class Command(BaseCommand):
    help = 'Aggregate raw page views into DailyStat records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=7,
            help='Number of past days to aggregate (default: 7)'
        )
        parser.add_argument(
            '--all', action='store_true',
            help='Re-aggregate all dates with data'
        )

    def handle(self, *args, **options):
        today = date.today()
        days = options['days']
        redo_all = options['all']
        now_ms = int(time.time() * 1000)

        if redo_all:
            first = PageView.objects.order_by('created_at').first()
            if first is None:
                self.stdout.write(self.style.WARNING('No page views found.'))
                return
            first_date = date.fromtimestamp(first.created_at / 1000)
            delta = (today - first_date).days
            days = delta + 1

        aggregated = 0
        for i in range(days):
            target_date = today - timedelta(days=i)

            day_start_ms = int(time.mktime(target_date.timetuple()) * 1000)
            day_end_ms = day_start_ms + 86400000

            qs = PageView.objects.filter(
                created_at__gte=day_start_ms,
                created_at__lt=day_end_ms,
            )

            total = qs.count()
            if total == 0 and not redo_all:
                continue

            unique_v = qs.values('session_key').distinct().count()
            new_users = User.objects.filter(
                created_at__gte=day_start_ms,
                created_at__lt=day_end_ms,
            ).count()
            web_v = qs.filter(source='web').count()
            app_v = qs.filter(source='app').count()
            direct_v = qs.filter(referrer_type='direct').count()
            search_v = qs.filter(referrer_type='search').count()
            social_v = qs.filter(referrer_type='social').count()
            referral_v = qs.filter(referrer_type='referral').count()
            internal_v = qs.filter(referrer_type='internal').count()
            new_posts = Post.objects.filter(
                created_at__gte=day_start_ms,
                created_at__lt=day_end_ms,
            ).count()
            new_resources = Resource.objects.filter(
                added_at__gte=day_start_ms,
                added_at__lt=day_end_ms,
            ).count()
            new_replies = Reply.objects.filter(
                created_at__gte=day_start_ms,
                created_at__lt=day_end_ms,
            ).count()

            DailyStat.objects.update_or_create(
                date=target_date,
                defaults={
                    'total_visits': total,
                    'unique_visitors': unique_v,
                    'new_users': new_users,
                    'web_visits': web_v,
                    'app_visits': app_v,
                    'direct_visits': direct_v,
                    'search_visits': search_v,
                    'social_visits': social_v,
                    'referral_visits': referral_v,
                    'internal_visits': internal_v,
                    'new_posts': new_posts,
                    'new_resources': new_resources,
                    'new_replies': new_replies,
                    'created_at': now_ms,
                }
            )
            aggregated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Aggregated {aggregated} daily stat records.'
        ))
