"""Education situation + portfolio: the dropout case, validation, privacy."""
import time
import uuid

from django.test import Client, TestCase

from api import education_catalog as cat
from api.models import ProfileEntry, User
from api.security import issue_auth_token


def _user(**kw):
    d = {'id': str(uuid.uuid4()), 'username': f'u_{uuid.uuid4().hex[:8]}',
         'email': f'{uuid.uuid4().hex[:8]}@t.com', 'created_at': int(time.time() * 1000),
         'email_verified': True, 'display_name': 'Test', 'gender': 'Other',
         'dob': '2003-01-01', 'role': 'student', 'class_level': 'Bachelors'}
    d.update(kw)
    return User.objects.create(**d)


class CatalogTests(TestCase):
    def test_catalog_is_consistent(self):
        values = [lv['value'] for lv in cat.LEVELS]
        self.assertEqual(len(values), len(set(values)), 'duplicate level value')
        for old in ('Class 8', 'Class 9', 'Class 10 / SEE', '11', '12', '+2 Passout',
                    'Diploma', 'Bachelors', 'Masters', 'PhD', 'Other'):
            self.assertIn(old, values)
        self.assertIn('BSc CSIT', cat.LEVEL_BY_VALUE['Bachelors']['programs'])
        self.assertIn('Dropped out', [s['label'] for s in cat.STATUSES])
        self.assertGreaterEqual(len(cat.LEVEL_BY_VALUE['Bachelors']['programs']), 60)

    def test_catalog_endpoint_is_public(self):
        r = Client().get('/api/education/catalog/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('levels', r.json())


class EducationSaveTests(TestCase):
    def setUp(self):
        self.user = _user()
        self.h = {'HTTP_AUTHORIZATION': f'Bearer {issue_auth_token(self.user)}'}

    def _save(self, **extra):
        body = {'username': self.user.username, 'dob': '2003-01-01'}
        body.update(extra)
        return Client().post('/api/users/profile/', body, content_type='application/json', **self.h)

    def test_dropout_after_one_year_of_bsc_csit(self):
        r = self._save(classLevel='Bachelors', eduStatus='dropped_out', eduProgram='BSc CSIT',
                       eduTerm='Year 1', eduCompleted='+2 Passout')
        self.assertEqual(r.status_code, 200, r.content)
        self.user.refresh_from_db()
        self.assertEqual(
            (self.user.class_level, self.user.edu_status, self.user.edu_program,
             self.user.edu_term, self.user.edu_completed),
            ('Bachelors', 'dropped_out', 'BSc CSIT', 'Year 1', '+2 Passout'))

    def test_bad_status_is_rejected_and_old_clients_keep_new_fields(self):
        self.assertEqual(self._save(eduStatus='nonsense').status_code, 400)
        self._save(classLevel='Bachelors', eduStatus='studying', eduProgram='BCA')
        self._save(classLevel='Bachelors')  # an older client that knows no new field
        self.user.refresh_from_db()
        self.assertEqual((self.user.edu_status, self.user.edu_program), ('studying', 'BCA'))

    def test_completed_only_kept_when_it_applies(self):
        self._save(classLevel='Bachelors', eduStatus='studying', eduCompleted='+2 Passout')
        self.user.refresh_from_db()
        self.assertEqual(self.user.edu_completed, '')

    def test_open_to_and_skills_are_cleaned(self):
        self._save(openTo='mentoring,hax,mentoring,tutoring', skills=' Python ,python,Design')
        self.user.refresh_from_db()
        self.assertEqual(self.user.open_to, 'mentoring,tutoring')
        self.assertEqual(self.user.skills, 'Python,Design')

    def test_global_user_rules(self):
        from api.view_helpers import is_global_user
        self.user.class_level, self.user.edu_status = 'Class 9', 'dropped_out'
        self.assertTrue(is_global_user(self.user))
        self.user.edu_status = 'studying'
        self.assertFalse(is_global_user(self.user))
        self.user.class_level = 'Self Learner'
        self.assertTrue(is_global_user(self.user))


class EntryApiTests(TestCase):
    def setUp(self):
        self.user = _user()
        self.h = {'HTTP_AUTHORIZATION': f'Bearer {issue_auth_token(self.user)}'}

    def test_crud_and_validation(self):
        c = Client()
        r = c.post('/api/profile/entries/', {'kind': 'project', 'title': 'Notes app',
                                              'url': 'github.com/x/y', 'start': '2025-03'},
                   content_type='application/json', **self.h)
        self.assertEqual(r.status_code, 201, r.content)
        eid = r.json()['entry']['id']
        self.assertTrue(r.json()['entry']['url'].startswith('https://'))
        bad = c.post('/api/profile/entries/', {'kind': 'nope', 'title': 'x'},
                     content_type='application/json', **self.h)
        self.assertEqual(bad.status_code, 400)
        backwards = c.post('/api/profile/entries/', {'kind': 'experience', 'title': 'Intern',
                                                      'start': '2025-05', 'end': '2024-01'},
                           content_type='application/json', **self.h)
        self.assertEqual(backwards.status_code, 400)
        p = c.patch(f'/api/profile/entries/{eid}/', {'title': 'Notes app v2'},
                    content_type='application/json', **self.h)
        self.assertEqual(p.json()['entry']['title'], 'Notes app v2')
        self.assertEqual(c.delete(f'/api/profile/entries/{eid}/', **self.h).status_code, 200)
        self.assertFalse(ProfileEntry.objects.filter(pk=eid).exists())

    def test_cannot_touch_someone_elses_entry(self):
        other = _user()
        e = ProfileEntry.objects.create(user=other, kind='project', title='Mine')
        r = Client().delete(f'/api/profile/entries/{e.id}/', **self.h)
        self.assertEqual(r.status_code, 404)

    def test_public_portfolio_hides_private_profiles(self):
        ProfileEntry.objects.create(user=self.user, kind='achievement', title='Gold medal')
        self.assertEqual(len(Client().get(f'/api/users/profile/{self.user.username}/portfolio/')
                             .json()['sections']), 1)
        self.user.is_locked = True
        self.user.save()
        self.assertEqual(Client().get(f'/api/users/profile/{self.user.username}/portfolio/')
                         .json()['sections'], [])
