"""Library reach: one view per viewer per day, push taps close the push funnel, insights stay private."""
import json
import time

from django.core.cache import cache
from django.test import Client, TestCase

from api import resource_insights, resource_reach
from api.models import (PushCampaign, PushDelivery, Resource, ResourceAlert, ResourceImpression, ResourceReach,
                        User)
from api.security import issue_auth_token

NOW = int(time.time() * 1000)
UA = {'HTTP_USER_AGENT': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36'}


def _login(user, client=None):
    c = client or Client(**UA)
    sess = c.session
    sess['auth_token'] = issue_auth_token(user)
    sess.save()
    return c


def _bearer(user):
    return {'HTTP_AUTHORIZATION': f'Bearer {issue_auth_token(user)}'}


def _user(name, **kw):
    return User.objects.create(id=name, username=name, email=f'{name}@x.com', created_at=1, email_verified=True, **kw)


class ReachTests(TestCase):
    def setUp(self):
        cache.clear()
        self.up = _user('up')
        self.stu = _user('stu', class_level='Class 10 / SEE', subjects='Science')
        self.res = Resource.objects.create(id='r1', title='Science notes', subject='Science', grade_level='Class 10 / SEE',
                                           added_at=NOW, uploaded_by=self.up, source_type='user')

    def test_view_counts_once_per_viewer_per_day(self):
        c = _login(self.stu)
        for _ in range(3):
            c.post('/api/resources/r1/view/', data=json.dumps({'surface': 'library'}), content_type='application/json')
        self.res.refresh_from_db()
        self.assertEqual(self.res.view_count, 1)
        row = ResourceReach.objects.get()
        self.assertEqual((row.hits, row.surface, row.class_level), (3, 'library', 'Class 10 / SEE'))

    def test_uploader_and_bots_do_not_inflate(self):
        _login(self.up).post('/api/resources/r1/view/', content_type='application/json')
        Client(HTTP_USER_AGENT='Googlebot/2.1').post('/api/resources/r1/view/', content_type='application/json')
        self.res.refresh_from_db()
        self.assertEqual(self.res.view_count, 0)
        self.assertEqual(ResourceReach.objects.filter(is_owner=False).count(), 0)

    def test_dwell_and_actions(self):
        c = _login(self.stu)
        c.post('/api/resources/r1/view/', data=json.dumps({'dwell_ms': 42000}), content_type='application/json')
        c.post('/api/resources/r1/action/', data=json.dumps({'action': 'read'}), content_type='application/json')
        c.post('/api/resources/r1/action/', data=json.dumps({'action': 'download'}), content_type='application/json')
        c.post('/api/resources/r1/action/', data=json.dumps({'action': 'download'}), content_type='application/json')
        bad = c.post('/api/resources/r1/action/', data=json.dumps({'action': 'nuke'}), content_type='application/json')
        self.assertEqual(bad.status_code, 400)
        row = ResourceReach.objects.get()
        self.assertEqual((row.dwell_ms, row.read, row.downloaded, row.shared), (42000, True, True, False))
        self.res.refresh_from_db()
        self.assertEqual(self.res.download_count, 1)   # a second tap the same day is not a second download

    def test_impressions_ignore_unknown_ids(self):
        c = _login(self.stu)
        r = c.post('/api/resources/impressions/', data=json.dumps({'ids': ['r1', 'nope', 'r1']}),
                   content_type='application/json')
        self.assertEqual(r.json()['recorded'], 1)
        self.assertEqual(ResourceImpression.objects.get().count, 1)

    def test_page_visit_and_push_tap_close_the_funnel(self):
        camp = PushCampaign.objects.create(id='c1', kind='autopilot', title='New', created_at=NOW)
        PushDelivery.objects.create(campaign=camp, user=self.stu, status='sent', created_at=NOW)
        ResourceAlert.objects.update_or_create(resource=self.res, defaults=dict(state='sent', campaign_id='c1', audience_size=1, queued_at=NOW))
        c = _login(self.stu)
        self.assertEqual(c.get('/app/reader/r1/?src=push').status_code, 200)
        d = PushDelivery.objects.get()
        self.assertTrue(d.clicked_at and d.opened_at)
        self.assertEqual(ResourceReach.objects.get().surface, 'notification')
        self.res.refresh_from_db()
        self.assertEqual(self.res.view_count, 1)
        c.get('/app/reader/r1/')   # refresh: still one view
        self.res.refresh_from_db()
        self.assertEqual(self.res.view_count, 1)

    def test_pending_resource_is_not_counted(self):
        Resource.objects.filter(pk='r1').update(approval_status='pending')
        _login(self.stu).post('/api/resources/r1/view/', content_type='application/json')
        self.res.refresh_from_db()
        self.assertEqual(self.res.view_count, 0)


class InsightsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.up, self.other = _user('up'), _user('other')
        self.adm = _user('adm', is_admin=True)
        self.res = Resource.objects.create(id='r1', title='Notes', subject='Science', grade_level='Class 10 / SEE',
                                           added_at=NOW, uploaded_by=self.up, source_type='user')
        for i, n in enumerate(('s1', 's2', 's3')):
            u = _user(n, class_level='Class 10 / SEE')
            c = _login(u)
            c.post('/api/resources/r1/view/', data=json.dumps({'surface': 'notification' if i == 0 else 'library'}),
                   content_type='application/json')
            if i < 2:
                c.post('/api/resources/r1/action/', data=json.dumps({'action': 'read'}), content_type='application/json')
        Client(**UA).post('/api/resources/impressions/', data=json.dumps({'ids': ['r1']}), content_type='application/json')

    def test_build_numbers(self):
        d = resource_insights.build(Resource.objects.get(pk='r1'), 30)
        self.assertEqual(d['kpis']['views']['value'], 3)
        self.assertEqual(d['kpis']['reads']['value'], 2)
        self.assertEqual(d['kpis']['impressions']['value'], 1)
        self.assertEqual(d['push']['views'], 1)
        self.assertEqual(d['classes'][0]['label'], 'Class 10 / SEE')
        self.assertEqual(d['funnel'][1]['count'], 3)
        self.assertTrue(d['hasData'])
        self.assertNotIn('viewer', json.dumps(d))   # aggregates only

    def test_overview_for_uploader(self):
        d = resource_insights.overview(self.up, 30)
        self.assertEqual(d['totals']['resources'], 1)
        self.assertEqual(d['resources'][0]['views'], 3)
        self.assertIn('posts', d)

    def test_access(self):
        self.assertIn(Client().get('/api/resources/r1/insights/').status_code, (401, 403))
        api = Client(**UA)
        self.assertEqual(api.get('/api/resources/r1/insights/', **_bearer(self.other)).status_code, 403)
        self.assertEqual(api.get('/api/resources/r1/insights/?days=7', **_bearer(self.up)).status_code, 200)
        self.assertEqual(api.get('/api/resources/r1/insights/', **_bearer(self.adm)).status_code, 200)
        self.assertEqual(api.get('/api/uploads/insights/', **_bearer(self.up)).json()['totals']['resources'], 1)
        self.assertEqual(_login(self.up).get('/ajax/resource/r1/insights/').status_code, 200)
        self.assertEqual(_login(self.other).get('/ajax/resource/r1/insights/').status_code, 403)
        self.assertEqual(_login(self.up).get('/ajax/uploads/insights/').json()['totals']['resources'], 1)

    def test_detail_page_shows_insights_button_only_to_uploader(self):
        self.assertContains(_login(self.up).get('/app/reader/r1/'), 'open-resource-insights')
        self.assertNotContains(_login(self.other).get('/app/reader/r1/'), 'open-resource-insights')
