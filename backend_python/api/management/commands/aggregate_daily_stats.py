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

            # ── New session analytics ──
            session_data = list(
                qs.values('session_key')
                  .annotate(pages=Count('id'))
                  .order_by()
            )
            total_sessions = len(session_data)
            bounce_count = sum(1 for s in session_data if s['pages'] == 1) if session_data else 0
            pages_per_session = round(total / total_sessions, 1) if total_sessions else 0.0

            # ── Peak hour ──
            peak_hour = 0
            peak_hour_max = 0
            for h in range(24):
                hs = day_start_ms + h * 3600000
                he = hs + 3600000
                h_count = qs.filter(created_at__gte=hs, created_at__lt=he).count()
                if h_count > peak_hour_max:
                    peak_hour_max = h_count
                    peak_hour = h

            # ── Avg session duration ──
            avg_session_duration = 0.0
            if total_sessions > 0:
                # For each session, compute duration from first to last page view
                durations = []
                for key_info in session_data[:50]:  # limit to 50 sessions for performance
                    skey = key_info['session_key']
                    times = list(
                        qs.filter(session_key=skey)
                          .values_list('created_at', flat=True)
                          .order_by('created_at')[:2]
                    )
                    if len(times) >= 2:
                        durations.append((times[-1] - times[0]) / 1000.0)
                if durations:
                    avg_session_duration = round(sum(durations) / len(durations), 1)

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
                    'total_sessions': total_sessions,
                    'bounce_count': bounce_count,
                    'pages_per_session': pages_per_session,
                    'peak_hour': peak_hour,
                    'avg_session_duration': avg_session_duration,
                    'created_at': now_ms,
                }
            )
            aggregated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Aggregated {aggregated} daily stat records.'
        ))
