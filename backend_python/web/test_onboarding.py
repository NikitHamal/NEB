"""The welcome flow: role is saved as chosen, education situations round-trip, bad input is refused."""
import json
import time
import uuid

from django.test import Client, TestCase

from api.models import User
from api.security import issue_auth_token
from api.serializers import UserSerializer


def _make(**kw):
    d = {'id': str(uuid.uuid4()), 'username': f'u_{uuid.uuid4().hex[:8]}',
         'email': f'{uuid.uuid4().hex[:8]}@t.com', 'created_at': int(time.time() * 1000),
         'email_verified': True}
    d.update(kw)
    return User.objects.create(**d)


def _sign_in(client, user):
    s = client.session
    s['auth_token'] = issue_auth_token(user)
    s['user_data'] = dict(UserSerializer(user).data)
    s.save()


GOOD = {'role': 'student', 'displayName': 'Asha Rai', 'dob': '2004-04-12', 'gender': 'Female',
        'status': 'studying', 'level': '11', 'program': 'Science (Physical)'}


class OnboardingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _make()  # a social sign-up: model default role is student, nothing else set
        _sign_in(self.client, self.user)

    def _save(self, **over):
        body = {**GOOD, **over}
        return self.client.post('/welcome/save/', json.dumps(body), content_type='application/json')

    def test_anonymous_is_sent_to_login(self):
        r = Client().get('/welcome/')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login/', r['Location'])

    def test_page_preselects_nothing_for_an_unfinished_profile(self):
        r = self.client.get('/welcome/')
        self.assertEqual(r.status_code, 200)
        boot = r.context['boot']
        self.assertEqual(boot['initial']['role'], '')
        self.assertIn('Dropped out', json.dumps(boot['catalog']['statuses']))

    def test_choosing_teacher_actually_saves_teacher(self):
        r = self._save(role='teacher', teachingSubjects='Physics, Mathematics', level='Masters',
                       status='completed', program='MSc Physics')
        self.assertEqual(r.status_code, 200, r.content)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'teacher')
        self.assertEqual(self.user.teaching_subjects, 'Physics,Mathematics')
        self.assertEqual(self.client.session['user_data']['role'], 'teacher')

    def test_dropout_story_round_trips(self):
        r = self._save(status='dropped_out', level='Bachelors', program='BSc CSIT', term='Year 1',
                       completed='+2 Passout', headline='Learning to code my own way',
                       skills='Python,Design', openTo='collab,mentoring', district='Kathmandu', pradesh='3')
        self.assertEqual(r.status_code, 200, r.content)
        self.user.refresh_from_db()
        self.assertEqual((self.user.edu_status, self.user.class_level, self.user.edu_program,
                          self.user.edu_term, self.user.edu_completed),
                         ('dropped_out', 'Bachelors', 'BSc CSIT', 'Year 1', '+2 Passout'))
        self.assertEqual(self.user.open_to, 'collab,mentoring')
        self.assertEqual(self.user.headline, 'Learning to code my own way')

    def test_validation(self):
        for over, field in [({'role': 'wizard'}, 'role'), ({'displayName': ' '}, 'displayName'),
                            ({'dob': '2099-01-01'}, 'dob'), ({'gender': 'x'}, 'gender'),
                            ({'level': ''}, 'level'), ({'level': 'Class 99'}, 'level'),
                            ({'role': 'teacher', 'teachingSubjects': ''}, 'teachingSubjects'),
                            ({'role': 'institution', 'school': ''}, 'school'),
                            ({'status': 'nonsense'}, 'status')]:
            r = self._save(**over)
            self.assertEqual(r.status_code, 400, over)
            self.assertEqual(r.json()['field'], field, over)

    def test_auto_username_can_be_claimed_once_and_conflicts_are_refused(self):
        _make(username='taken_name')
        self.assertEqual(self._save(username='taken_name').status_code, 400)
        r = self._save(username='asha_rai')
        self.assertEqual(r.status_code, 200, r.content)
        self.assertTrue(r.json()['profileUrl'].endswith('/asha_rai/'))

    def test_next_is_only_followed_when_local(self):
        r = self.client.post('/welcome/save/?next=//evil.example', json.dumps(GOOD), content_type='application/json')
        self.assertEqual(r.json()['next'], '')
        r = self.client.post('/welcome/save/?next=/app/library/', json.dumps(GOOD), content_type='application/json')
        self.assertEqual(r.json()['next'], '/app/library/')

    def test_anonymous_cannot_save(self):
        r = Client().post('/welcome/save/', json.dumps(GOOD), content_type='application/json')
        self.assertEqual(r.status_code, 401)

    def test_new_oauth_users_land_in_onboarding(self):
        from django.urls import reverse
        self.assertEqual(reverse('web:onboarding'), '/welcome/')
