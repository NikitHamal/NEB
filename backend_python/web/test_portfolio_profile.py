"""Portfolio on the profile page: visible to everyone, editable only by the owner, hidden when private."""
import json
import time
import uuid

from django.test import Client, TestCase

from api.models import ProfileEntry, User
from api.security import issue_auth_token
from api.serializers import UserSerializer


def _make(**kw):
    d = {'id': str(uuid.uuid4()), 'username': f'p_{uuid.uuid4().hex[:8]}', 'email': f'{uuid.uuid4().hex[:8]}@t.com',
         'created_at': int(time.time() * 1000), 'email_verified': True, 'display_name': 'Pat', 'gender': 'Other',
         'dob': '2002-02-02', 'role': 'student', 'class_level': 'Bachelors', 'edu_status': 'dropped_out',
         'edu_program': 'BSc CSIT', 'edu_term': 'Year 1', 'edu_completed': '+2 Passout',
         'bio': 'Building things my own way', 'skills': 'Python,Design', 'open_to': 'collab,mentoring'}
    d.update(kw)
    return User.objects.create(**d)


def _sign_in(client, user):
    s = client.session
    s['auth_token'] = issue_auth_token(user)
    s['user_data'] = dict(UserSerializer(user).data)
    s.save()


class ProfilePortfolioTests(TestCase):
    def setUp(self):
        self.owner = _make()
        ProfileEntry.objects.create(user=self.owner, kind='project', title='Notes app', org='Side project', start='2025-03', is_current=True)

    def test_visitor_sees_story_but_no_edit_controls(self):
        html = Client().get(f'/app/profile/{self.owner.username}/').content.decode()
        for needle in ('Building things my own way', 'BSc CSIT', 'Dropped out', 'Finished +2', 'Notes app', 'Python', 'Project collab'):
            self.assertIn(needle, html, needle)
        self.assertNotIn('pf-entry-sheet', html)
        self.assertNotIn('data-folio-edit', html)

    def test_owner_gets_the_editor(self):
        c = Client()
        _sign_in(c, self.owner)
        html = c.get(f'/app/profile/{self.owner.username}/').content.decode()
        self.assertIn('pf-entry-sheet', html)
        self.assertIn('data-folio-edit', html)

    def test_private_profile_hides_the_portfolio(self):
        self.owner.is_locked = True
        self.owner.save()
        html = Client().get(f'/app/profile/{self.owner.username}/').content.decode()
        self.assertNotIn('Notes app', html)

    def test_owner_can_save_and_delete_over_session(self):
        c = Client()
        _sign_in(c, self.owner)
        r = c.post('/ajax/portfolio/save/', json.dumps({'kind': 'certificate', 'title': 'Python basics', 'start': '2025-01'}), content_type='application/json')
        self.assertEqual(r.status_code, 200, r.content)
        eid = r.json()['entry']['id']
        r = c.post('/ajax/portfolio/delete/', json.dumps({'id': eid}), content_type='application/json')
        self.assertTrue(r.json()['ok'])
        self.assertFalse(ProfileEntry.objects.filter(pk=eid).exists())

    def test_stranger_cannot_edit_or_delete_anothers_entry(self):
        stranger = _make()
        c = Client()
        _sign_in(c, stranger)
        entry = ProfileEntry.objects.filter(user=self.owner).first()
        r = c.post('/ajax/portfolio/save/', json.dumps({'id': entry.id, 'kind': 'project', 'title': 'Hacked'}), content_type='application/json')
        self.assertEqual(r.status_code, 404)
        c.post('/ajax/portfolio/delete/', json.dumps({'id': entry.id}), content_type='application/json')
        self.assertTrue(ProfileEntry.objects.filter(pk=entry.id).exists())
        self.assertEqual(Client().post('/ajax/portfolio/save/', '{}', content_type='application/json').status_code, 401)


class ProfileSheetsTests(TestCase):
    """The profile's dialogs are NebUI sheets: no native <dialog>, no native month fields, no stroke on a photo."""

    def _read(self, *parts):
        import os
        base = os.path.join(os.path.dirname(__file__), 'static', 'web')
        with open(os.path.join(base, *parts), encoding='utf-8') as fh:
            return fh.read()

    def test_entry_editor_is_a_sheet_with_month_and_year_selects(self):
        import os
        path = os.path.join(os.path.dirname(__file__), 'templates', 'web', 'profile', '_portfolio.html')
        html = open(path, encoding='utf-8').read()
        self.assertIn('neb-scrim', html)
        self.assertNotIn('<dialog', html)
        self.assertNotIn('type="month"', html)
        self.assertIn('pf-entry-start-m', html)
        js = self._read('js', 'portfolio.js')
        self.assertIn('NebUI.open', js)
        self.assertIn("'-' + (month.value || '01')", js)

    def test_follow_and_photo_modals_are_sheets(self):
        import os
        path = os.path.join(os.path.dirname(__file__), 'templates', 'web', 'profile', '_follow_modal.html')
        html = open(path, encoding='utf-8').read()
        self.assertNotIn('modal-overlay', html)
        self.assertNotIn('style="', html)
        self.assertIn('id="followModal"', html)
        self.assertIn('id="photoHistoryModal"', html)

    def test_photo_thumbs_carry_no_stroke(self):
        css = self._read('css', 'm3x', 'app-profile.css')
        i = css.index('.photo-thumb.active')
        self.assertNotIn('outline', css[i:i + 120])
        self.assertNotIn('border: 2px', css[i:i + 120])
