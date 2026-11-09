"""One level vocabulary: canonical values on write, tolerant matching on read."""
import time

from django.test import Client, TestCase

from api.education_catalog import canonical_level, level_match_values
from api.models import Resource, User

NOW = int(time.time() * 1000)


def _user(name, **kw):
    kw.setdefault('class_level', '11')
    return User.objects.create(id=name, username=name, email=f'{name}@x.com', created_at=1,
                               email_verified=True, **kw)


def _res(rid, grade, **kw):
    return Resource.objects.create(id=rid, title=f'Book {rid}', subject='Physics', grade_level=grade,
                                   type='PDF', approval_status='approved', is_lead=True,
                                   added_at=NOW, **kw)


class CanonicalLevelTests(TestCase):
    def test_spellings_fold_onto_the_catalog_value(self):
        cases = {'Class 11': '11', 'grade 12': '12', '11th': '11', 'Bachelor': 'Bachelors',
                 "Bachelor's": 'Bachelors', 'bachelor': 'Bachelors', 'SEE': 'Class 10 / SEE',
                 'Class 10': 'Class 10 / SEE', 'Passout': '+2 Passout', 'grade 8': 'Class 8',
                 'Bachelors': 'Bachelors', 'Masters': 'Masters', 'Entrance Prep': 'Entrance Prep'}
        for raw, canon in cases.items():
            self.assertEqual(canonical_level(raw), canon, raw)

    def test_unknown_and_empty_values_survive(self):
        self.assertEqual(canonical_level(''), '')
        self.assertEqual(canonical_level('Some School Board'), 'Some School Board')

    def test_match_values_cover_both_sides(self):
        values = level_match_values('Class 11')
        self.assertEqual(values[0], '11')
        self.assertIn('class 11', values)
        self.assertIn('11', level_match_values('11'))
        self.assertEqual(level_match_values(''), [])


class TolerantFilterTests(TestCase):
    def setUp(self):
        _user('u1')
        _res('canon11', '11')
        _res('legacy11', 'Class 11')
        _res('canon12', '12')
        _res('bag', 'Bachelors')
        _res('oldbag', 'Bachelor')

    def test_web_filter_finds_both_spellings(self):
        c = Client()
        for term in ('11', 'Class 11'):
            html = c.get('/app/library/', {'grade': term}).content.decode()
            self.assertIn('Book canon11', html, term)
            self.assertIn('Book legacy11', html, term)
            self.assertNotIn('Book canon12', html, term)

    def test_web_filter_folds_bachelor_into_bachelors(self):
        for term in ('Bachelors', 'Bachelor'):
            html = Client().get('/app/library/', {'grade': term}).content.decode()
            self.assertIn('Book bag', html, term)
            self.assertIn('Book oldbag', html, term)

    def test_api_filter_finds_both_spellings(self):
        r = Client().get('/api/resources/', {'grade': 'Class 12'})
        ids = {row['id'] for row in r.json()['results']}
        self.assertEqual(ids, {'canon12'})

    def test_upload_stores_the_canonical_value(self):
        user = User.objects.get(pk='u1')
        from api.security import issue_auth_token
        token = issue_auth_token(user)
        r = Client().post('/api/resources/upload/', {
            'title': 'New Book', 'subject': 'Physics', 'grade_level': 'Class 12',
            'description': 'x', 'type': 'PDF', 'file_url': 'https://example.com/a.pdf',
        }, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertIn(r.status_code, (200, 201), r.content[:200])
        self.assertEqual(Resource.objects.get(title='New Book').grade_level, '12')

    def test_profile_save_stores_the_canonical_value(self):
        user = User.objects.get(pk='u1')
        from api.security import issue_auth_token
        token = issue_auth_token(user)
        r = Client().post('/api/users/profile/', {
            'username': 'u1', 'dob': '2008-01-15', 'displayName': 'Student One',
            'gender': 'Male', 'classLevel': 'Class 10 / SEE',
        }, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertIn(r.status_code, (200, 204), r.content[:200])
        user.refresh_from_db()
        self.assertEqual(user.class_level, 'Class 10 / SEE')

    def test_chip_list_is_one_entry_per_level(self):
        html = Client().get('/app/library/').content.decode()
        self.assertEqual(html.count('data-filter="grade" data-value="11"'), 1)
        self.assertEqual(html.count('data-filter="grade" data-value="Class 11"'), 0)
        self.assertIn('>Class 11<', html)