"""Institution portfolio, teacher fields, and institution accounts without gender or date of birth."""
from django.test import Client, TestCase

from api import institution_profile as prof
from api import institutions as svc
from api.models import User
from api.models_institutions import Institution
from api.security import issue_auth_token


def _owner(role='institution'):
    u = User.objects.create(id='u_' + role, username='owner_' + role, created_at=1, role=role,
                            email='o@example.com', email_verified=True, display_name='Owner')
    return u


def _client(user):
    c = Client()
    s = c.session
    s['auth_token'] = issue_auth_token(user)
    s.save()
    return c, {'HTTP_AUTHORIZATION': 'Bearer ' + issue_auth_token(user)}


class PortfolioTests(TestCase):
    def setUp(self):
        self.inst = Institution.objects.create(slug='demo-college', name='Demo College', kind='college',
                                               district='Kaski')

    def test_clean_checks_each_field(self):
        out, est, err = prof.clean({'est': '2045', 'teachers': '42', 'levels': ['plus_two', 'bogus'],
                                    'facilities': 'library,wifi,nope', 'feeMin': '1,50,000'})
        self.assertIsNone(err)
        self.assertEqual(est, '2045')
        self.assertEqual(out['levels'], ['plus_two'])
        self.assertEqual(out['facilities'], ['library', 'wifi'])
        self.assertEqual(out['teachers'], 42)
        self.assertEqual(out['feeMin'], 150000)

    def test_bad_values_are_refused(self):
        self.assertIsNotNone(prof.clean({'est': '20x5'})[2])
        self.assertIsNotNone(prof.clean({'feeMin': 9000, 'feeMax': 100})[2])
        self.assertIsNotNone(prof.clean({'socials': {'facebook': 'not a url'}})[2])

    def test_partial_save_keeps_the_rest_and_scores(self):
        payload, err = prof.save(self.inst, {'about': 'A college in Pokhara.', 'est': '2050'})
        self.assertIsNone(err)
        first = payload['completeness']
        payload, err = prof.save(self.inst, {'levels': ['bachelor'], 'phone': '061-000000'})
        self.assertEqual(payload['details']['about'], 'A college in Pokhara.')
        self.assertGreater(payload['completeness'], first)
        self.inst.refresh_from_db()
        self.assertEqual(self.inst.est, '2050')
        self.assertNotIn('about', payload['missing'])

    def test_fuller_portfolios_list_first_among_claimed(self):
        other = Institution.objects.create(slug='other-college', name='Aaa Other College', kind='college')
        for i in (self.inst, other):
            i.verified = True
            i.save()
        prof.save(self.inst, {'about': 'x' * 20, 'levels': ['plus_two'], 'est': '2060'})
        rows, _, _ = svc.search('college', verified_only=True)
        self.assertEqual(rows[0].pk, self.inst.pk)
        self.assertGreater(svc.serialize(rows[0])['completeness'], 0)

    def test_only_the_verified_owner_can_edit(self):
        owner = _owner()
        client, auth = _client(owner)
        url = '/api/institutions/demo-college/profile/'
        r = client.patch(url, {'about': 'Hi'}, content_type='application/json', **auth)
        self.assertEqual(r.status_code, 403)
        self.inst.claimed_by, self.inst.verified = owner, True
        self.inst.save()
        r = client.patch(url, {'about': 'Hi', 'teachers': 12}, content_type='application/json', **auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['portfolio']['details']['teachers'], 12)
        detail = client.get('/api/institutions/demo-college/', **auth).json()
        self.assertTrue(detail['canEdit'])
        self.assertEqual(detail['portfolio']['details']['about'], 'Hi')
        mine = client.get('/api/institutions/mine/', **auth).json()
        self.assertEqual(mine['institution']['slug'], 'demo-college')
        self.assertEqual(Client().get('/api/institutions/schema/').json()['levels'][0]['value'], 'preprimary')

    def test_claim_needs_an_institution_account_and_a_document(self):
        teacher = _owner('teacher')
        client, auth = _client(teacher)
        r = client.post('/api/institutions/demo-college/claim/', {}, **auth)
        self.assertEqual(r.status_code, 403)
        inst_user = User.objects.create(id='u_i2', username='inst2', created_at=1, role='institution',
                                        email='i2@example.com', email_verified=True)
        client, auth = _client(inst_user)
        r = client.post('/api/institutions/demo-college/claim/', {'name': 'Demo College'}, **auth)
        self.assertEqual(r.status_code, 400)


class AccountRuleTests(TestCase):
    def test_institution_needs_no_gender_or_dob(self):
        from api.view_helpers import _profile_incomplete
        inst = User(role='institution', display_name='X', school='X School', gender='')
        self.assertFalse(_profile_incomplete(inst))
        self.assertTrue(_profile_incomplete(User(role='student', display_name='X', gender='', class_level='Class 9')))

    def test_teacher_fields_are_saved_and_cleaned(self):
        from api.profile_education import apply_education
        t = User(role='teacher')
        err = apply_education(t, {'teachLevels': 'plus_two,bachelor,zzz', 'experienceYears': '7', 'employment': 'tutor'})
        self.assertIsNone(err)
        self.assertEqual(t.teach_levels, 'plus_two,bachelor')
        self.assertEqual((t.experience_years, t.employment), (7, 'tutor'))
        t2 = User(role='teacher')
        apply_education(t2, {'employment': 'pirate'})
        self.assertEqual(t2.employment, '')


class PathwaysOnNebTests(TestCase):
    def test_lists_only_claimed_institutions_with_a_portfolio(self):
        a = Institution.objects.create(slug='a-col', name='A College', kind='college', verified=True)
        Institution.objects.create(slug='b-col', name='B College', kind='college', verified=True)
        prof.save(a, {'about': 'About us', 'levels': ['bachelor']})
        data = Client().get('/api/pathways/on-neb/').json()
        self.assertEqual([i['slug'] for i in data['items']], ['a-col'])
        self.assertIn('matches', data)
