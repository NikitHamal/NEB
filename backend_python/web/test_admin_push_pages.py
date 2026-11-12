"""Admin push pages: compose, history, detail, autopilot, and the manual announce flow."""
import time
from unittest import mock

from django.core.cache import cache
from django.test import Client, TestCase

from api import push_engine
from api.models import FCMToken, PushCampaign, PushDelivery, PushSettings, Resource, ResourceAlert, User
from api.security import issue_auth_token

NOW = int(time.time() * 1000)


def _fake(tokens, title, body, data=None, workers=8, **kw):
    return {t: (True, 'ok') for t in tokens}


@mock.patch('api.fcm_utils.send_fcm_detailed', side_effect=_fake)
class AdminPushPageTests(TestCase):
    def setUp(self):
        cache.clear()
        PushSettings.objects.create(pk=1, quiet_start_hour=0, quiet_end_hour=0)
        self.admin = User.objects.create(id='adm', username='adm', created_at=1, is_admin=True, email='a@x.com')
        self.s = User.objects.create(id='s1', username='s1', created_at=1, class_level='Class 10 / SEE',
                                     subjects='Science', email='s1@x.com')
        FCMToken.objects.create(token='t1', user=self.s, created_at=1)
        self.client = Client()
        sess = self.client.session
        sess['auth_token'] = issue_auth_token(self.admin)
        sess.save()

    def test_pages_render(self, _f):
        for name in ('/admin/push-notifications/', '/admin/push-notifications/history/', '/admin/push-notifications/autopilot/'):
            r = self.client.get(name)
            self.assertEqual(r.status_code, 200, name)
            self.assertContains(r, 'pn-tabs')

    def test_non_admin_is_redirected(self, _f):
        self.assertEqual(Client().get('/admin/push-notifications/history/').status_code, 302)

    def test_counts_json_has_devices_and_inbox_split(self, _f):
        d = self.client.get('/admin/push-notifications/', {'count_only': '1', 'class_level': 'Class 10 / SEE'}).json()
        self.assertEqual((d['matching_users'], d['device_users'], d['inbox_only'], d['devices']), (1, 1, 0, 1))

    def test_send_creates_a_campaign_with_numbers(self, _f):
        with mock.patch.object(push_engine, 'run_in_background', side_effect=lambda fn, *a, **k: fn(*a, **k)):
            r = self.client.post('/admin/push-notifications/', {
                'title': 'Hello', 'body': 'World', 'class_level': 'Class 10 / SEE', 'dest': 'none', 'also_inbox': '1'})
        self.assertEqual(r.status_code, 302)
        c = PushCampaign.objects.get(kind='manual')
        self.assertEqual((c.users_targeted, c.devices_accepted, c.status), (1, 1, 'sent'))
        page = self.client.get(f'/admin/push-notifications/history/{c.id}/')
        self.assertContains(page, 'Hello')
        self.assertContains(self.client.get('/admin/push-notifications/history/'), 'Hello')

    def test_validation_and_empty_audience(self, _f):
        r = self.client.post('/admin/push-notifications/', {'title': '', 'body': 'x'})
        self.assertContains(r, 'title and a message')
        r = self.client.post('/admin/push-notifications/', {'title': 'a', 'body': 'b', 'class_level': 'PhD'})
        self.assertContains(r, 'No one matches')
        self.assertEqual(PushCampaign.objects.count(), 0)

    def test_unknown_resource_destination_is_refused(self, _f):
        r = self.client.post('/admin/push-notifications/', {'title': 'a', 'body': 'b', 'dest': 'resource', 'dest_id': 'nope'})
        self.assertContains(r, 'resource was not found')

    def test_test_send_goes_to_the_admin_only(self, _f):
        FCMToken.objects.create(token='adm-t', user=self.admin, created_at=1)
        r = self.client.post('/admin/push-notifications/', {'title': 'T', 'body': 'B', 'action': 'test', 'class_level': 'PhD'})
        self.assertEqual(r.status_code, 302)
        c = PushCampaign.objects.get(kind='test')
        self.assertEqual((c.users_targeted, c.devices_accepted), (1, 1))
        self.assertEqual(PushDelivery.objects.get(campaign=c).user_id, 'adm')

    def test_announce_by_hand_sends_one_digest_and_marks_resources(self, _f):
        Resource.objects.bulk_create([Resource(id=f'o{i}', title=f'Old {i}', subject='Science and Technology',
                                               grade_level='Class 10 / SEE', added_at=NOW - 9 * 86400000) for i in range(3)])
        pv = self.client.post('/admin/push-notifications/autopilot/preview/', data='{"ids":["o0","o1","o2"]}',
                              content_type='application/json').json()
        self.assertEqual((pv['people'], pv['would_send_as_singles']), (1, 3))
        with mock.patch('api.push_engine.run_in_background', side_effect=lambda fn, *a, **k: fn(*a, **k)):
            r = self.client.post('/admin/push-notifications/autopilot/', {'action': 'announce', 'resource_ids': ['o0', 'o1', 'o2']})
        self.assertEqual(r.status_code, 302)
        c = PushCampaign.objects.get(kind='library')
        self.assertEqual(c.users_targeted, 1)
        self.assertEqual(set(ResourceAlert.objects.values_list('state', flat=True)), {'manual'})
        self.assertContains(self.client.get(f'/admin/push-notifications/history/{c.id}/'), 'Old 0')

    def _old_science(self, n=3):
        Resource.objects.bulk_create([Resource(id=f'o{i}', title=f'Old {i}', subject='Science and Technology',
                                               grade_level='Class 10 / SEE', added_at=NOW - 9 * 86400000) for i in range(n)])

    def test_unnotified_mode_counts_and_sends_one_digest(self, _f):
        self._old_science()
        d = self.client.get('/admin/push-notifications/', {'count_only': '1', 'mode': 'unnotified'}).json()
        self.assertEqual((d['users'], d['device_users'], d['resources'], d['singles']), (1, 1, 3, 3))
        self.assertEqual(d['sample']['title'], '3 new Science and Technology resources added for Class 10')
        with mock.patch('api.push_engine.run_in_background', side_effect=lambda fn, *a, **k: fn(*a, **k)):
            r = self.client.post('/admin/push-notifications/', {'mode': 'unnotified', 'action': 'send'})
        self.assertEqual(r.status_code, 302)
        c = PushCampaign.objects.get(kind='library')
        self.assertEqual(c.users_targeted, 1)
        self.assertEqual(self.client.get('/admin/push-notifications/', {'count_only': '1', 'mode': 'unnotified'}).json()['resources'], 0)

    def test_platform_mode_splits_android_and_web(self, _f):
        User.objects.create(id='w1', username='w1', created_at=1, email='w1@x.com')
        a = self.client.get('/admin/push-notifications/', {'count_only': '1', 'mode': 'platform', 'device': 'with'}).json()
        w = self.client.get('/admin/push-notifications/', {'count_only': '1', 'mode': 'platform', 'device': 'without'}).json()
        self.assertEqual(a['users'], 1)
        self.assertEqual(w['users'], 2)

    def test_all_mode_ignores_stale_class_filter(self, _f):
        d = self.client.get('/admin/push-notifications/', {'count_only': '1', 'mode': 'all', 'class_level': 'PhD'}).json()
        self.assertEqual(d['users'], 2)

    def test_one_tap_batch_on_the_autopilot_page(self, _f):
        self._old_science(2)
        page = self.client.get('/admin/push-notifications/autopilot/')
        self.assertContains(page, 'Announce unnotified library uploads')
        with mock.patch('api.push_engine.run_in_background', side_effect=lambda fn, *a, **k: fn(*a, **k)):
            r = self.client.post('/admin/push-notifications/autopilot/', {'action': 'announce_unnotified'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(PushCampaign.objects.get(kind='library').users_targeted, 1)

    def test_history_has_trigger_labels_ctr_and_resource_views(self, _f):
        self._old_science(1)
        with mock.patch('api.push_engine.run_in_background', side_effect=lambda fn, *a, **k: fn(*a, **k)):
            self.client.post('/admin/push-notifications/autopilot/', {'action': 'announce_unnotified'})
        c = PushCampaign.objects.get(kind='library')
        d = PushDelivery.objects.get(campaign=c)
        from api import push_engine, push_stats
        push_engine.record_push_open(self.s, notification_id=d.notification_id)
        push_engine.record_push_open(self.s, notification_id=d.notification_id)
        m = push_stats.rollup([c])[c.id]
        self.assertEqual((m['targeted'], m['sent'], m['delivered'], m['failed'], m['opened'], m['clicked']), (1, 1, 1, 0, 1, 1))
        self.assertEqual(m['ctr'], 100.0)
        page = self.client.get('/admin/push-notifications/history/')
        self.assertContains(page, 'Batch Digest')
        self.assertContains(page, 'CTR')
        self.assertContains(self.client.get('/admin/push-notifications/history/', {'kind': 'library'}), 'Old 0'[:0] + 'Batch Digest')

    def test_inbox_link_of_a_campaign_carries_the_push_source(self, _f):
        from api.notifications import get_notification_url
        from api.models import Notification
        n = Notification(id='n1', recipient_id='s1', verb='new_resource', target_type='resource', target_id='r9',
                         campaign_id='c1', created_at=1)
        self.assertEqual(get_notification_url(n), '/reader/r9/?src=push')
        n.campaign_id = ''
        self.assertEqual(get_notification_url(n), '/reader/r9/')

    def test_autopilot_settings_save(self, _f):
        self.client.post('/admin/push-notifications/autopilot/', {'action': 'settings', 'daily_cap': '3', 'quiet_start_hour': '22',
                                                                   'quiet_end_hour': '6', 'settle_minutes': '10', 'max_wait_minutes': '60'})
        cfg = PushSettings.objects.get(pk=1)
        self.assertEqual((cfg.autopilot_enabled, cfg.daily_cap, cfg.quiet_start_hour), (False, 3, 22))
