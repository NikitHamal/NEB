"""Bring page views written before the analytics rebuild up to the new model.

    python manage.py backfill_analytics              # derive + scrub
    python manage.py backfill_analytics --keep-raw   # derive, keep ip/user agent/full url
    python manage.py backfill_analytics --delete-bots

For every legacy row (visitor_id == '') this derives, in time order:
  * is_bot, device_class, browser, platform  (from the stored user agent)
  * referrer channel + friendly source name  (re-classified with the fixed rules)
  * page_key                                 (/avatar/x/ -> /avatar/*/)
  * visitor_id (daily-rotating hash of ip + user agent, or the account)
  * session_id / is_entry                    (30 minute inactivity gap)
and then, unless --keep-raw, drops the raw IP, user agent and full URL.
Safe to re-run: rows that already have a visitor_id are skipped. Interrupting it
loses nothing: every batch is committed on its own.
"""
import time
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import PageView
from nebians.analytics import rules
from nebians.analytics.rules import SESSION_GAP_MS

FIELDS = [
    'is_bot', 'device_class', 'browser', 'platform', 'referrer', 'referrer_domain',
    'referrer_type', 'referrer_name', 'page_key', 'visitor_id', 'session_id', 'is_entry',
    'user_identifier',
]


class Command(BaseCommand):
    help = 'Derive visitor/session/channel fields for legacy page views and scrub raw identifiers'

    def add_arguments(self, parser):
        parser.add_argument('--batch', type=int, default=2000)
        parser.add_argument('--keep-raw', action='store_true',
                            help='keep ip_address, user_agent and full_url on migrated rows')
        parser.add_argument('--delete-bots', action='store_true',
                            help='delete rows identified as bots once migrated')

    def handle(self, *args, **opts):
        batch = max(100, opts['batch'])
        secret = settings.SECRET_KEY
        extra_hosts = {h.lstrip('.').lower() for h in settings.ALLOWED_HOSTS if h and '*' not in h}
        state: dict[str, tuple[str, int]] = {}  # visitor_id -> (session_id, last_ms)
        done = bots = 0
        started = time.time()

        while True:
            rows = list(PageView.objects.filter(visitor_id='').order_by('created_at', 'id')[:batch])
            if not rows:
                break
            for row in rows:
                self._derive(row, secret, extra_hosts, state)
                if not opts['keep_raw']:
                    row.ip_address, row.user_agent, row.full_url = None, '', ''
                bots += 1 if row.is_bot else 0
            with transaction.atomic():
                scrub = [] if opts['keep_raw'] else ['ip_address', 'user_agent', 'full_url']
                PageView.objects.bulk_update(rows, FIELDS + scrub, batch_size=500)
            done += len(rows)
            # Visitors idle for longer than a session gap can never be continued.
            horizon = rows[-1].created_at - SESSION_GAP_MS
            state = {k: v for k, v in state.items() if v[1] >= horizon}
            self.stdout.write(f'  {done} rows migrated')

        if opts['delete_bots']:
            deleted, _ = PageView.objects.filter(is_bot=True).delete()
            self.stdout.write(f'Deleted {deleted} bot rows.')
        self.stdout.write(self.style.SUCCESS(
            f'Backfilled {done} page views ({bots} flagged as bots) in {time.time() - started:.1f}s.'
        ))

    @staticmethod
    def _derive(row, secret, extra_hosts, state):
        ua = row.user_agent or ''
        is_app = row.source == 'app'
        row.is_bot = rules.is_bot(ua, is_app=is_app)
        row.device_class = rules.device_class(ua) if ua else ('mobile' if is_app else 'other')
        row.browser = rules.browser_name(ua)
        if not row.platform:
            row.platform = rules.detect_platform(ua)

        own = set(extra_hosts)
        if row.full_url:
            try:
                own.add((urlparse(row.full_url).hostname or '').lower())
            except ValueError:
                pass
        # Old rows kept the whole referrer URL; fall back to the stored domain.
        ref_url = row.referrer or (f'https://{row.referrer_domain}/' if row.referrer_domain else '')
        ref = rules.classify_referrer(ref_url, own, row.utm_source, row.utm_medium)
        row.referrer = rules.referrer_label(ref_url)
        row.referrer_domain = ref.host[:255]
        row.referrer_type = ref.channel
        row.referrer_name = ref.name[:80]
        row.page_key = rules.classify_page(row.path).key[:200]

        uid = row.user_identifier or (str(row.user_id) if row.user_id else '')
        row.user_identifier = uid[:255]
        if uid:
            row.visitor_id = rules.user_visitor_id(secret, uid)
        else:
            day = time.strftime('%Y-%m-%d', time.localtime(row.created_at / 1000))
            row.visitor_id = rules.anon_visitor_id(secret, day, row.ip_address or '', ua)

        cur = state.get(row.visitor_id)
        if cur and 0 <= row.created_at - cur[1] <= SESSION_GAP_MS:
            row.session_id, row.is_entry = cur[0], False
        else:
            row.session_id = f'b{row.id:x}'[:24]
            row.is_entry = True
        state[row.visitor_id] = (row.session_id, row.created_at)
