"""Admin analytics: rules, tracking pipeline, report maths, views, backfill."""
import io
import os
import time
from unittest import mock

from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase
from django.urls import NoReverseMatch, reverse

from api.models import PageView, Post, User
from api.security import issue_auth_token
from nebians.analytics import events, report, rules, writer
from nebians.analytics.rules import MS_DAY

OWN = {'nebians.consica.com.np'}
CHROME_ANDROID = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36'
CHROME_DESKTOP = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'


class RulesTests(TestCase):
    def test_bots(self):
        self.assertTrue(rules.is_bot(''))
        self.assertTrue(rules.is_bot('Mozilla/5.0 (compatible; Googlebot/2.1)'))
        self.assertTrue(rules.is_bot('facebookexternalhit/1.1'))
        self.assertTrue(rules.is_bot('python-requests/2.31'))
        self.assertFalse(rules.is_bot(CHROME_ANDROID))
        self.assertFalse(rules.is_bot('okhttp/4.12', is_app=True))

    def test_referrers_use_whole_hosts(self):
        def c(url, **kw):
            return rules.classify_referrer(url, OWN, **kw)

        self.assertEqual(c('https://www.google.com/').channel, 'search')
        self.assertEqual(c('https://www.google.com.np/').name, 'Google')
        self.assertEqual(c('https://classroom.google.com/').channel, 'referral')
        self.assertEqual(c('android-app://com.google.android.gm').channel, 'email')
        self.assertEqual(c('android-app://org.telegram.messenger').name, 'Telegram')
        self.assertEqual(c('https://l.facebook.com/l.php?u=x').name, 'Facebook')
        self.assertEqual(c('https://chatgpt.com/').channel, 'ai')
        self.assertEqual(c('https://box.com/').channel, 'referral')  # was matched as X
        self.assertEqual(c('https://nebians.consica.com.np/app/').channel, 'internal')
        self.assertEqual(c('http://localhost:8000/').channel, 'internal')
        self.assertEqual(c('https://accounts.google.com/o/oauth2').channel, 'internal')
        self.assertEqual(c('').channel, 'direct')

    def test_utm_without_referrer(self):
        r = rules.classify_referrer('', OWN, utm_source='newsletter', utm_medium='email')
        self.assertEqual((r.channel, r.name), ('email', 'newsletter'))
        r = rules.classify_referrer('', OWN, utm_source='poster', utm_medium='qr')
        self.assertEqual(r.channel, 'campaign')

    def test_pages_collapse_to_routes(self):
        a = rules.classify_page('/avatar/prashantchataut/')
        b = rules.classify_page('/avatar/bAdhikarii/')
        self.assertEqual(a.key, b.key)
        self.assertEqual(a.section, 'Profiles')
        self.assertEqual(rules.classify_page('/app/forum/post/123/').label, 'Forum thread')
        self.assertEqual(rules.classify_page('/app/forum/post/123/?x=1').key, '/app/forum/post/*/')
        self.assertEqual(rules.classify_page('/').section, 'Landing')
        self.assertEqual(rules.classify_page('/app/library/').section, 'Library')

    def test_visitor_ids(self):
        a = rules.anon_visitor_id('k', '2026-01-01', '1.2.3.4', 'UA')
        self.assertEqual(a, rules.anon_visitor_id('k', '2026-01-01', '1.2.3.4', 'UA'))
        self.assertNotEqual(a, rules.anon_visitor_id('k', '2026-01-02', '1.2.3.4', 'UA'))
        self.assertNotIn('1.2.3.4', a)
        self.assertEqual(rules.user_visitor_id('k', '7'), rules.user_visitor_id('k', '7'))

    def test_country_codes(self):
        self.assertEqual(rules.country_from_code('np'), 'Nepal')
        self.assertEqual(rules.country_from_code('XX'), '')
        self.assertEqual(rules.country_from_code('T1'), '')

    def test_device_os_browser(self):
        self.assertEqual(rules.device_class(CHROME_ANDROID), 'mobile')
        self.assertEqual(rules.device_class(CHROME_DESKTOP), 'desktop')
        self.assertEqual(rules.detect_platform(CHROME_ANDROID), 'android')
        self.assertEqual(rules.browser_name(CHROME_DESKTOP), 'Chrome')
        self.assertEqual(rules.browser_name('Mozilla/5.0 (iPhone) AppleWebKit Mobile FBAV/400'), 'Facebook app')


class TrackingTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT=CHROME_DESKTOP)

    def _hit(self, path, **extra):
        with mock.patch('nebians.analytics.submit') as submit:
            self.client.get(path, **extra)
        return [c.args[0] for c in submit.call_args_list]

    def test_human_page_view_is_recorded_without_pii(self):
        evs = self._hit('/login/', HTTP_REFERER='https://www.google.com/search?q=secret', REMOTE_ADDR='203.0.113.9')
        self.assertEqual(len(evs), 1)
        ev = evs[0]
        self.assertEqual(ev['referrer_type'], 'search')
        self.assertEqual(ev['referrer'], 'www.google.com/search')  # no query string
        self.assertEqual(ev['device_class'], 'desktop')
        self.assertEqual(ev['page_key'], '/login/')
        self.assertTrue(ev['visitor_id'].startswith('a'))
        for banned in ('ip_address', 'user_agent', 'full_url'):
            self.assertNotIn(banned, ev)

    def test_bots_assets_and_fragments_are_not_page_views(self):
        self.assertEqual(self._hit('/login/', HTTP_USER_AGENT='Googlebot/2.1'), [])
        self.assertEqual(self._hit('/og/page/home.png'), [])
        self.assertEqual(self._hit('/login/', HTTP_HX_REQUEST='true'), [])
        self.assertEqual(self._hit('/login/', HTTP_SEC_PURPOSE='prefetch'), [])

    def test_staff_browsing_is_not_counted(self):
        admin = User.objects.create(id='1', username='boss', created_at=1, is_admin=True)
        member = User.objects.create(id='2', username='kid', created_at=1)
        req = RequestFactory().get('/app/', HTTP_USER_AGENT=CHROME_DESKTOP)
        self.assertIsNone(events.event_from_request(req, user=admin))
        ev = events.event_from_request(req, user=member)
        self.assertEqual(ev['user_identifier'], '2')
        self.assertTrue(ev['visitor_id'].startswith('u'))

    def test_signed_in_members_are_identified_from_the_session_token(self):
        """request.user is always anonymous here; identity is the session token."""
        member = User.objects.create(id='42', username='student', created_at=1)
        s = self.client.session
        s['auth_token'] = issue_auth_token(member)
        s.save()
        evs = self._hit('/privacy/')
        self.assertTrue(evs)
        self.assertEqual(evs[0]['user_identifier'], '42')

    def test_cached_anonymous_hits_are_still_counted(self):
        """The anonymous page cache answers repeat hits on `/`; those are real
        visits and must not vanish from the numbers."""
        from django.core.cache import cache

        cache.clear()
        first = self._hit('/')
        second = self._hit('/')
        third = self._hit('/')
        self.assertEqual((len(first), len(second), len(third)), (1, 1, 1))

    def test_online_now_is_gone(self):
        for name in ('admin_analytics_online_users', 'admin_analytics_refresh'):
            with self.assertRaises(NoReverseMatch):
                reverse(f'web:{name}')
        self.assertEqual(Client().post('/api/presence/heartbeat/').status_code, 404)

    def test_app_track_endpoint_uses_same_pipeline(self):
        with mock.patch('nebians.analytics.submit') as submit:
            r = Client().post('/api/analytics/track/', {'path': '/app/library/', 'platform': 'android'},
                              content_type='application/json')
            self.assertEqual(r.status_code, 200)
            ev = submit.call_args.args[0]
            self.assertEqual((ev['source'], ev['platform'], ev['page_key']), ('app', 'android', '/app/library/'))
            submit.reset_mock()
            Client().post('/api/analytics/track/', {'path': '/api/secret/'}, content_type='application/json')
            Client().post('/api/analytics/track/', {'path': 'no-slash'}, content_type='application/json')
            submit.assert_not_called()


class WriterTests(TestCase):
    def _event(self, visitor, at, **kw):
        base = {
            'path': '/app/', 'page_key': '/app/', 'referrer': '', 'referrer_domain': '', 'referrer_type': 'direct',
            'referrer_name': 'Direct', 'utm_source': '', 'utm_medium': '', 'utm_campaign': '', 'source': 'web',
            'platform': 'windows', 'device_class': 'desktop', 'browser': 'Chrome', 'visitor_id': visitor,
            'user_identifier': '', 'country': '', 'city': '', 'created_at': at, '_touch_user': '', '_ip': '1.1.1.1',
        }
        base.update(kw)
        return base

    def test_sessions_follow_the_30_minute_rule(self):
        t = int(time.time() * 1000)
        v = f'a-test-{t}'
        writer._write(self._event(v, t))
        writer._write(self._event(v, t + 5 * 60_000))
        writer._write(self._event(v, t + 50 * 60_000))
        rows = list(PageView.objects.filter(visitor_id=v).order_by('created_at'))
        self.assertEqual([r.is_entry for r in rows], [True, False, True])
        self.assertEqual(rows[0].session_id, rows[1].session_id)
        self.assertNotEqual(rows[1].session_id, rows[2].session_id)
        self.assertIsNone(rows[0].ip_address)  # raw IP is never stored

    def test_forked_child_gets_its_own_worker_and_queue(self):
        """LSAPI forks per request. The child inherits the Thread object (still
        `is_alive()`) but not the OS thread, so the writer must notice the pid
        change and rebuild both, or events pile up with no consumer."""
        class Ghost:  # what a forked child sees: an "alive" thread that is not running
            def is_alive(self):
                return True

        old_q, old_w, old_pid = writer._queue, writer._worker, writer._owner_pid
        try:
            writer._worker = Ghost()
            writer._owner_pid = old_pid + 1  # pretend we were forked from another pid
            writer._ensure_worker()
            self.assertIsNot(writer._worker, None)
            self.assertNotIsInstance(writer._worker, Ghost)
            self.assertTrue(writer._worker.is_alive())
            self.assertIsNot(writer._queue, old_q)
            self.assertEqual(writer._owner_pid, os.getpid())
            # and the rebuilt worker really drains the rebuilt queue
            writer._queue.put_nowait(self._event(f'a-fork-{time.time()}', int(time.time() * 1000)))
            writer._queue.join()
        finally:
            writer._queue, writer._worker, writer._owner_pid = old_q, old_w, old_pid

    def test_remote_geo_is_off_by_default(self):
        with mock.patch.object(writer, '_geo_remote') as remote:
            writer._write(self._event(f'a-geo-{time.time()}', int(time.time() * 1000)))
        remote.assert_not_called()


def _pv(visitor, session, at, entry=False, **kw):
    d = dict(path='/app/', page_key='/app/', visitor_id=visitor, session_id=session, is_entry=entry,
             created_at=at, referrer_type='direct', referrer_name='Direct', source='web',
             device_class='desktop', platform='windows', browser='Chrome')
    d.update(kw)
    return PageView(**d)


class ReportTests(TestCase):
    def setUp(self):
        self.rng = report.resolve_range({'range': '7d'})
        mid = self.rng['start'] + 2 * MS_DAY + 12 * 3_600_000  # noon, two days in
        PageView.objects.bulk_create([
            # visitor A: a bounce, from Google
            _pv('a1', 's1', mid, True, referrer_type='search', referrer_name='Google', page_key='/'),
            # visitor B: two pages 90 seconds apart, from Telegram, in the app
            _pv('a2', 's2', mid, True, referrer_type='social', referrer_name='Telegram', source='app',
                device_class='mobile', platform='android', page_key='/app/forum/post/*/', path='/app/forum/post/9/'),
            _pv('a2', 's2', mid + 90_000, False, source='app', page_key='/app/library/', path='/app/library/'),
            # a signed-in member who came back after an idle gap
            _pv('u1', 's3', mid, True, user_identifier='10', referrer_type='internal', page_key='/app/'),
            # noise that must never count
            _pv('a9', 's9', mid, True, is_bot=True),
            _pv('', '', mid, True),  # legacy row, not yet backfilled
        ])
        User.objects.create(id='10', username='m', created_at=mid, class_level='11', gender='female')
        Post.objects.create(id='9', user_id='10', title='Newton laws help', created_at=mid)

    def test_headline_numbers(self):
        r = report.build_report(self.rng, use_cache=False)
        t = r['totals']
        self.assertEqual(t['pageviews'], 4)  # bot and legacy rows excluded
        self.assertEqual(t['visitors'], 3)
        self.assertEqual(t['sessions'], 3)
        self.assertEqual(t['bounces'], 2)
        self.assertEqual(t['bounce_rate'], 66.7)
        self.assertEqual(t['avg_duration'], 90.0)
        self.assertEqual(t['members'], 1)
        self.assertEqual(t['new_accounts'], 1)
        self.assertTrue(r['needs_backfill'])

    def test_channels_ignore_internal_navigation(self):
        r = report.build_report(self.rng, use_cache=False)
        by = {c['key']: c['count'] for c in r['channels']}
        self.assertEqual(by, {'search': 1, 'social': 1, 'direct': 1})  # the internal entry folds into direct
        self.assertEqual(sorted(s['name'] for s in r['sources']), ['Google', 'Telegram'])

    def test_source_filter(self):
        r = report.build_report(self.rng, 'app', use_cache=False)
        self.assertEqual(r['totals']['pageviews'], 2)
        self.assertEqual(r['audience']['devices'][0]['name'], 'Mobile')

    def test_series_are_aligned_and_complete(self):
        r = report.build_report(self.rng, use_cache=False)
        tr = r['trend']
        self.assertEqual(len(tr['labels']), 7)
        self.assertEqual(len(tr['pageviews']), 7)
        self.assertEqual(len(tr['prev']['pageviews']), 7)
        self.assertEqual(sum(tr['pageviews']), 4)
        self.assertEqual(sum(tr['visitors']), 3)
        today = report.build_report(report.resolve_range({'range': 'today'}), use_cache=False)
        self.assertEqual(len(today['trend']['labels']), 24)

    def test_heatmap_and_content(self):
        r = report.build_report(self.rng, use_cache=False)
        self.assertEqual(sum(c['v'] for row in r['heatmap']['rows'] for c in row['cells']), 4)
        self.assertEqual(r['heatmap']['peak']['hour'], 12)
        names = [p['name'] for p in r['content']['pages']]
        self.assertIn('Forum thread', names)
        self.assertEqual(r['content']['threads'][0]['name'], 'Newton laws help')

    def test_demographics_and_funnel(self):
        r = report.build_report(self.rng, use_cache=False)
        self.assertEqual(r['demographics']['classes'][0]['name'], '11')
        self.assertEqual(r['demographics']['gender'][0]['name'], 'Female')
        self.assertEqual(r['funnel'][0]['name'], 'Visits')
        self.assertEqual(r['funnel'][1]['count'], 2)  # two of three sessions went past the landing page

    def test_deltas(self):
        self.assertEqual(report.delta(150, 100)['text'], '+50.0%')
        self.assertEqual(report.delta(5, 0)['text'], 'new')
        self.assertEqual(report.delta(0, 0)['dir'], 'flat')
        d = report.delta(40.0, 50.0, rate=True, lower_is_better=True)
        self.assertEqual((d['text'], d['good']), ('−10.0 pts', True))

    def test_custom_range_and_clamping(self):
        r = report.resolve_range({'from': '2026-01-10', 'to': '2026-01-01'})
        self.assertEqual((r['key'], r['days']), ('custom', 10))
        self.assertEqual(report.resolve_range({'range': 'nonsense'})['key'], '7d')
        self.assertEqual(report.resolve_range({'from': 'x', 'to': 'y'})['key'], '7d')
        far = report.resolve_range({'from': '2000-01-01', 'to': '2100-01-01'})
        self.assertLessEqual(far['days'], 366)

    def test_days_are_cut_at_nepal_midnight(self):
        r = report.resolve_range({'range': 'today'})
        self.assertEqual((r['start'] + r['off']) % MS_DAY, 0)
        self.assertEqual(r['off'], 5 * 3_600_000 + 45 * 60_000)


class AdminViewTests(TestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()  # reports are cached for 60s; tests must not see each other's
        admin = User.objects.create(id='u_admin', username='admin_test', created_at=1, is_admin=True)
        self.client = Client()
        s = self.client.session
        s['auth_token'] = issue_auth_token(admin)
        s.save()

    def test_requires_admin(self):
        self.assertEqual(Client().get('/admin/analytics/').status_code, 302)
        self.assertEqual(Client().get('/admin/analytics/export/csv/').status_code, 302)

    def test_empty_state_renders(self):
        r = self.client.get('/admin/analytics/')
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'Online now')
        self.assertNotContains(r, 'Auto-refresh')

    def test_page_renders_every_range_with_data(self):
        now = int(time.time() * 1000)
        PageView.objects.bulk_create([
            _pv('a1', 's1', now - 3600_000, True, referrer_type='search', referrer_name='Google', country='Nepal'),
            _pv('a1', 's1', now - 3500_000, False, page_key='/app/library/', path='/app/library/'),
            _pv('u1', 's2', now - 7200_000, True, user_identifier='5', page_key='/app/forum/'),
        ])
        for q in ('', '?range=today', '?range=30d&source=web', '?range=90d&source=app',
                  '?from=2026-01-01&to=2026-01-31'):
            r = self.client.get('/admin/analytics/' + q)
            self.assertEqual(r.status_code, 200, q)
        r = self.client.get('/admin/analytics/')
        for needle in ('Visitors', 'Bounce rate', 'Acquisition', 'Audience', 'Content', 'Google'):
            self.assertContains(r, needle)

    def test_csv_export_matches_report(self):
        now = int(time.time() * 1000)
        PageView.objects.bulk_create([_pv('a1', 's1', now - 1000, True), _pv('a1', 's1', now - 500)])
        r = self.client.get('/admin/analytics/export/csv/?range=7d')
        self.assertEqual(r.status_code, 200)
        lines = r.content.decode().strip().splitlines()
        self.assertEqual(lines[0], 'period,visitors,visits,pageviews,new_accounts,threads,resources,replies')
        self.assertEqual(len(lines), 8)
        self.assertEqual(sum(int(line.split(',')[3]) for line in lines[1:]), 2)


class BackfillTests(TestCase):
    def test_legacy_rows_are_migrated_and_scrubbed(self):
        t = int(time.time() * 1000) - 5 * MS_DAY
        legacy = dict(visitor_id='', session_key='', ip_address='198.51.100.7', user_agent=CHROME_DESKTOP,
                      full_url='https://nebians.consica.com.np/app/?token=abc', source='web')
        PageView.objects.create(path='/avatar/prashantchataut/', referrer='https://www.google.com/',
                                referrer_domain='google.com', referrer_type='search', created_at=t, **legacy)
        PageView.objects.create(path='/avatar/other/', referrer='https://nebians.consica.com.np/',
                                referrer_domain='nebians.consica.com.np', referrer_type='internal',
                                created_at=t + 60_000, **legacy)
        PageView.objects.create(path='/app/', created_at=t, **{**legacy, 'user_agent': 'Googlebot/2.1'})
        call_command('backfill_analytics', stdout=io.StringIO())
        rows = list(PageView.objects.order_by('created_at', 'id'))
        self.assertTrue(all(r.visitor_id for r in rows))
        first, bot, second = [r for r in rows if not r.is_bot][0], [r for r in rows if r.is_bot][0], \
            [r for r in rows if not r.is_bot][1]
        self.assertTrue(bot.is_bot)
        self.assertEqual(first.page_key, '/avatar/*/')
        self.assertEqual((first.referrer_type, first.referrer_name), ('search', 'Google'))
        self.assertEqual(second.referrer_type, 'internal')
        self.assertEqual(first.session_id, second.session_id)
        self.assertTrue(first.is_entry and not second.is_entry)
        for r in rows:
            self.assertIsNone(r.ip_address)
            self.assertEqual((r.user_agent, r.full_url), ('', ''))
        out = io.StringIO()
        call_command('backfill_analytics', stdout=out)  # idempotent
        self.assertIn('Backfilled 0', out.getvalue())
