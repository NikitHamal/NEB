"""Push engine and library autopilot: who is told, how often, and what is measured."""
import time
from unittest import mock

from django.test import TestCase

from api import push_engine, resource_alerts
from api.models import (FCMToken, Notification, PushCampaign, PushDelivery, PushSettings, Resource,
                        ResourceAlert, User)

NOW = int(time.time() * 1000)


def _user(name, **kw):
    kw.setdefault('class_level', 'Class 10 / SEE')
    kw.setdefault('subjects', 'Science, Mathematics')
    return User.objects.create(id=name, username=name, email=f'{name}@x.com', created_at=1,
                               email_verified=True, **kw)


def _res(rid, **kw):
    kw.setdefault('title', f'Title {rid}')
    kw.setdefault('subject', 'Science and Technology')
    kw.setdefault('grade_level', 'Class 10 / SEE')
    kw.setdefault('added_at', NOW)
    r = Resource(id=rid, **kw)
    r.save()
    return r


def _fake_send(tokens, title, body, data=None, workers=8):
    return {t: (not t.startswith('bad'), 'ok' if not t.startswith('bad') else 'unregistered') for t in tokens}


class MatchingTests(TestCase):
    def test_levels_are_one_vocabulary(self):
        n = resource_alerts.norm_level
        self.assertEqual(n('Class 10 / SEE'), n('Class 10'))
        self.assertEqual(n('11'), n('Class 11'))
        self.assertNotEqual(n('Bachelors'), n('11'))

    def test_subject_matching(self):
        m = resource_alerts.subject_matches
        self.assertTrue(m('Science', 'Science and Technology'))
        self.assertTrue(m('Mathematics', 'Mathematics II'))
        self.assertFalse(m('Mathematics', 'Optional Mathematics'))
        self.assertTrue(m('English', 'Compulsory English'))
        self.assertFalse(m('Physics', 'Chemistry'))

    def test_audience_is_class_and_subject_and_optin(self):
        _user('yes')
        _user('wrong_subject', subjects='Social')
        _user('wrong_class', class_level='11')
        _user('optout', notify_new_resources=False)
        _user('nosubjects', subjects='')
        up = _user('uploader')
        r = _res('r1', uploaded_by=up, source_type='user')
        self.assertEqual(resource_alerts.audience_for(r), ['yes'])

    def test_programme_match_reaches_a_member_without_the_subject(self):
        _user('bca', class_level='Bachelors', subjects='', edu_program='BCA')
        r = _res('b1', grade_level='Bachelors', subject='Web Technology I', program='BCA')
        self.assertEqual(resource_alerts.audience_for(r), ['bca'])


@mock.patch('api.fcm_utils.send_fcm_detailed', side_effect=_fake_send)
class AutopilotTests(TestCase):
    def setUp(self):
        self.cfg = PushSettings.objects.create(pk=1, quiet_start_hour=0, quiet_end_hour=0)  # quiet hours off
        self.a, self.b = _user('a'), _user('b', subjects='Mathematics')
        FCMToken.objects.create(token='tok-a', user=self.a, created_at=1)
        FCMToken.objects.create(token='bad-b', user=self.b, created_at=1)

    def test_saving_an_approved_resource_queues_one_alert(self, _s):
        r = _res('r1')
        self.assertEqual(ResourceAlert.objects.get(resource=r).state, 'pending')
        r.title = 'Edited'
        r.save()
        self.assertEqual(ResourceAlert.objects.count(), 1)

    def test_pending_review_is_silent_until_approved(self, _s):
        r = _res('r1', approval_status='pending')
        self.assertEqual(ResourceAlert.objects.count(), 0)
        r.approval_status = 'approved'
        r.save()
        self.assertEqual(ResourceAlert.objects.get(resource=r).state, 'pending')

    def test_non_lead_files_do_not_alert(self, _s):
        _res('r1', is_lead=False)
        self.assertEqual(ResourceAlert.objects.count(), 0)

    def test_round_waits_for_uploads_to_settle(self, _s):
        _res('r1')
        self.assertIsNone(resource_alerts.flush_pending())
        self.assertEqual(ResourceAlert.objects.get().state, 'pending')

    def test_bulk_upload_is_one_digest_per_person(self, _s):
        for i in range(6):
            _res(f'r{i}', subject='Science and Technology')
        c = resource_alerts.flush_pending(force=True)
        self.assertEqual(c.kind, 'autopilot')
        self.assertEqual(c.users_targeted, 1)                      # only `a` studies Science
        self.assertEqual(Notification.objects.filter(recipient=self.a, campaign_id=c.id).count(), 1)
        n = Notification.objects.get(recipient=self.a)
        self.assertTrue(n.message.startswith('6 new Science and Technology resources'))
        self.assertEqual(c.devices_accepted, 1)
        self.assertEqual(set(ResourceAlert.objects.values_list('state', flat=True)), {'sent'})

    def test_optout_gets_nothing_and_unmatched_resource_is_skipped(self, _s):
        User.objects.filter(pk='a').update(notify_new_resources=False)
        _res('r1')
        self.assertIsNone(resource_alerts.flush_pending(force=True))
        al = ResourceAlert.objects.get()
        self.assertEqual((al.state, al.reason), ('skipped', 'no_audience'))
        self.assertFalse(Notification.objects.exists())

    def test_daily_cap_keeps_the_inbox_but_stops_the_buzz(self, _s):
        self.cfg.daily_cap = 1
        self.cfg.save()
        _res('r1')
        first = resource_alerts.flush_pending(force=True)
        self.assertEqual(first.users_pushed, 1)
        _res('r2')
        second = resource_alerts.flush_pending(force=True)
        self.assertEqual(second.users_pushed, 0)
        self.assertEqual(second.users_suppressed, 1)
        self.assertEqual(PushDelivery.objects.get(campaign=second).status, 'capped')
        self.assertEqual(Notification.objects.filter(recipient=self.a).count(), 2)

    def test_quiet_hours_hold_the_round(self, _s):
        self.cfg.quiet_start_hour, self.cfg.quiet_end_hour = 0, 24 % 24 or 23
        self.cfg.save()
        with mock.patch.object(resource_alerts, 'in_quiet_hours', return_value=True):
            _res('r1')
            old = push_engine.now_ms() - 3600000
            ResourceAlert.objects.update(queued_at=old)
            self.assertIsNone(resource_alerts.flush_pending())
        self.assertEqual(ResourceAlert.objects.get().state, 'pending')

    def test_autopilot_off_skips_with_a_reason(self, _s):
        self.cfg.autopilot_enabled = False
        self.cfg.save()
        _res('r1')
        al = ResourceAlert.objects.get()
        self.assertEqual((al.state, al.reason), ('skipped', 'autopilot_off'))

    def test_paid_resources_are_not_announced_by_default(self, _s):
        _res('r1', is_paid=True)
        self.assertEqual(ResourceAlert.objects.get().reason, 'paid')

    def test_uploader_is_never_told_about_their_own_upload(self, _s):
        _res('r1', uploaded_by=self.a, source_type='user')
        self.assertIsNone(resource_alerts.flush_pending(force=True))

    def test_the_backlog_is_never_announced_by_itself(self, _s):
        Resource.objects.bulk_create([Resource(id='old', title='Old', subject='Science', grade_level='Class 10 / SEE', added_at=NOW)])
        self.assertEqual(ResourceAlert.objects.count(), 0)
        self.assertIsNone(resource_alerts.flush_pending(force=True))

    def test_manual_announce_of_the_backlog_is_a_digest(self, _s):
        Resource.objects.bulk_create([Resource(id=f'old{i}', title=f'Old {i}', subject='Science and Technology',
                                               grade_level='Class 10 / SEE', added_at=NOW - 9 * 86400000) for i in range(4)])
        pv = resource_alerts.preview([f'old{i}' for i in range(4)])
        self.assertEqual((pv['people'], pv['would_send_as_singles']), (1, 4))
        c = resource_alerts.announce([f'old{i}' for i in range(4)], sync=True)
        self.assertEqual((c.kind, c.users_targeted, c.users_pushed), ('library', 1, 1))
        self.assertEqual(set(ResourceAlert.objects.values_list('state', flat=True)), {'manual'})


@mock.patch('api.fcm_utils.send_fcm_detailed', side_effect=_fake_send)
class CampaignMeasurementTests(TestCase):
    def setUp(self):
        self.u = _user('u')
        self.v = _user('v')
        FCMToken.objects.create(token='tok-u', user=self.u, created_at=1)
        FCMToken.objects.create(token='bad-u2', user=self.u, created_at=2)

    def test_broadcast_counts_devices_failures_and_inbox_only(self, _s):
        c = push_engine.send_manual(title='Hello', body='World', sync=True)
        self.assertEqual((c.users_targeted, c.users_pushed, c.users_inbox_only), (2, 1, 1))
        self.assertEqual((c.devices_targeted, c.devices_accepted, c.devices_failed), (2, 1, 1))
        self.assertEqual(c.errors, {'unregistered': 1})
        self.assertEqual(c.status, 'sent')
        self.assertEqual(User.objects.get(pk='v').unread_notification_count, 1)

    def test_open_is_counted_once_from_inbox_and_from_push(self, _s):
        c = push_engine.send_manual(title='Hello', body='World', sync=True)
        nid = Notification.objects.get(recipient=self.u).id
        self.assertEqual(push_engine.mark_opened([nid], 'inbox'), 1)
        self.assertEqual(push_engine.mark_opened([nid], 'inbox'), 0)
        d = PushDelivery.objects.get(campaign=c, user=self.u)
        self.assertEqual(d.opened_via, 'inbox')
        self.assertTrue(push_engine.record_push_open(self.v, notification_id=Notification.objects.get(recipient=self.v).id))
        self.assertEqual(PushDelivery.objects.filter(campaign=c).exclude(opened_at=0).count(), 2)

    def test_scheduled_campaign_waits_then_runs(self, _s):
        c = push_engine.send_manual(title='Later', body='x', scheduled_at=push_engine.now_ms() + 600000, sync=True)
        self.assertEqual(c.status, 'scheduled')
        self.assertEqual(push_engine.run_due_scheduled(), 0)
        PushCampaign.objects.filter(pk=c.pk).update(scheduled_at=push_engine.now_ms() - 1)
        self.assertEqual(push_engine.run_due_scheduled(), 1)
        self.assertEqual(PushCampaign.objects.get(pk=c.pk).status, 'sent')
