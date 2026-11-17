"""Profile strength card and the institution portfolio editor on the web profile."""
import json

from django.test import Client, TestCase

from api import institution_profile as ip

from api.models_institutions import Institution
from api.profile_strength import person_strength
from web.test_portfolio_profile import _make, _sign_in


class StrengthTests(TestCase):
    def test_person_score_grows_with_what_is_filled(self):
        empty = _make(headline='', skills='', open_to='', class_level='', edu_program='', school='', bio='')
        self.assertEqual(person_strength(empty)['percent'], 0)
        full = _make()
        self.assertGreater(person_strength(full)['percent'], 0)
        self.assertNotIn('Skills', person_strength(full)['steps'])

    def test_teacher_uses_teaching_weights(self):
        t = _make(role='teacher', school='Demo School', teaching_subjects='Physics', experience_years=4)
        out = person_strength(t)
        self.assertIn('Levels', out['steps'])
        self.assertNotIn('Subjects', out['steps'])


class InstitutionFolioTests(TestCase):
    def setUp(self):
        self.owner = _make(role='institution', gender='', dob='', username='demo_inst')
        self.inst = Institution.objects.create(slug='demo-college', name='Demo College', kind='college',
                                               district='Kaski', claimed_by=self.owner, verified=True)

    def _save(self, client, **data):
        data['slug'] = self.inst.slug
        return client.post('/ajax/institution/portfolio/save/', json.dumps(data), content_type='application/json')

    def test_owner_saves_one_section_at_a_time(self):
        c = Client()
        _sign_in(c, self.owner)
        r = self._save(c, levels=['plus_two'], about='Hello')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])
        r = self._save(c, students='1200')
        self.assertTrue(r.json()['ok'])
        d = ip.get(self.inst)
        self.assertEqual(d['levels'], ['plus_two'])
        self.assertEqual(d['students'], 1200)

    def test_stranger_cannot_save(self):
        other = _make(role='student')
        c = Client()
        _sign_in(c, other)
        self.assertEqual(self._save(c, about='x').status_code, 403)
        self.assertEqual(self._save(Client(), about='x').status_code, 401)

    def test_profile_shows_strength_to_owner_only(self):
        ip.save(self.inst, {'about': 'We teach.', 'levels': ['plus_two'], 'feeMin': '90000'})
        c = Client()
        _sign_in(c, self.owner)
        html = c.get('/app/profile/demo_inst/').content.decode()
        self.assertIn('Portfolio strength', html)
        self.assertIn('data-inst-edit="facilities"', html)
        visitor = Client().get('/app/profile/demo_inst/').content.decode()
        self.assertNotIn('Portfolio strength', visitor)
        self.assertIn('Levels offered', visitor)
        self.assertNotIn('data-inst-edit', visitor)
