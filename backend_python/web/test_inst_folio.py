"""Profile strength card and the institution portfolio editor on the web profile."""
import json

from django.test import Client, TestCase

from api import institution_profile as ip

from api.models_institutions import Institution
from api.profile_strength import person_strength
from web.test_portfolio_profile import _make, _sign_in


class StrengthTests(TestCase):
    def test_person_score_grows_with_what_is_filled(self):
        empty = _make(skills='', open_to='', class_level='', edu_program='', school='', bio='')
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


class TeacherSchoolsCardTests(TestCase):
    def test_current_and_past_schools_share_one_card(self):
        from django.test import Client
        from api.models import ProfileEntry
        t = _make(role='teacher', school='Himalaya Secondary School', teaching_subjects='Physics', experience_years=9)
        ProfileEntry.objects.create(user=t, kind='past_school', title='Teacher', org='Sunrise English School', start='2016-01', end='2021-01')
        html = Client().get(f'/app/profile/{t.username}/').content.decode()
        self.assertIn('pf-folio-schools', html)
        self.assertIn('Himalaya Secondary School', html)
        self.assertIn('Sunrise English School', html)
        self.assertNotIn('data-kind="past_school"', html)
        self.assertNotIn('Current school', html)


class TeacherEditorTests(TestCase):
    def setUp(self):
        self.t = _make(role='teacher', school='Old School', teaching_subjects='Physics')

    def _post(self, client, **data):
        return client.post('/ajax/teacher/profile/save/', json.dumps(data), content_type='application/json')

    def test_teacher_saves_one_section_at_a_time(self):
        c = Client()
        _sign_in(c, self.t)
        r = self._post(c, teaching_subjects='Physics, Maths, physics', teach_levels=['plus_two', 'bogus'])
        self.assertTrue(r.json()['ok'])
        self.t.refresh_from_db()
        self.assertEqual(self.t.teaching_subjects, 'Physics,Maths')
        self.assertEqual(self.t.teach_levels, 'plus_two')
        self.assertEqual(self.t.school, 'Old School')
        r = self._post(c, school='Himalaya Secondary School', employment='full_time', experience_years='9')
        self.assertTrue(r.json()['ok'])
        self.t.refresh_from_db()
        self.assertEqual((self.t.school, self.t.employment, self.t.experience_years), ('Himalaya Secondary School', 'full_time', 9))

    def test_guest_and_non_teacher_are_refused(self):
        self.assertEqual(self._post(Client(), school='X').status_code, 401)
        s = _make(role='student')
        c = Client()
        _sign_in(c, s)
        self.assertEqual(self._post(c, school='X').status_code, 403)

    def test_owner_sees_edit_hooks_visitor_does_not(self):
        c = Client()
        _sign_in(c, self.t)
        own = c.get(f'/app/profile/{self.t.username}/').content.decode()
        self.assertIn('data-tf-edit="teach"', own)
        self.assertIn('tf-boot', own)
        other = Client().get(f'/app/profile/{self.t.username}/').content.decode()
        self.assertNotIn('data-tf-edit', other)
