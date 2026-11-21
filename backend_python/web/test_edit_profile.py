"""The profile editor shares the welcome flow's controls and saves the education story."""

from django.test import Client, TestCase

from web.test_onboarding import _make, _sign_in


class EditProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _make(display_name='Nik', dob='2007-02-27', gender='Male', role='student',
                          class_level='Bachelors', edu_program='BCA')
        _sign_in(self.client, self.user)

    def _html(self):
        r = self.client.get('/app/profile/edit/')
        self.assertEqual(r.status_code, 200)
        return r.content.decode()

    def test_date_and_gender_are_the_shared_controls_and_stack(self):
        html = self._html()
        for needle in ('id="dob-field"', 'id="gender-field"', 'id="dob-sheet"', 'neb-dob-field.js', 'neb-edu.js'):
            self.assertIn(needle, html)
        self.assertNotIn('type="date"', html)
        # No row wrapper holds the two side by side any more.
        dob_at, gender_at = html.index('id="dob-field"'), html.index('id="gender-field"')
        between = html[dob_at:gender_at]
        self.assertNotIn('form-row', between)
        self.assertLess(dob_at, gender_at)

    def test_no_taglines_left_in_the_editor(self):
        html = self._html()
        for gone in ('This is what other NEBians see', 'Kept off your profile', 'JPG, PNG or WebP',
                     'Explorers have nothing else'):
            self.assertNotIn(gone, html)

    def test_old_class_select_is_gone_and_picker_inputs_exist(self):
        html = self._html()
        self.assertNotIn('class_level_picker_trigger', html)
        self.assertNotIn('name="headline"', html)
        for name in ('class_level', 'edu_status', 'edu_program', 'edu_term', 'edu_completed',
                     'skills', 'open_to'):
            self.assertRegex(html, r'name="%s"' % name)
        self.assertIn('id="epf-boot"', html)

    def test_post_saves_education_headline_skills_and_open_to(self):
        post = {'username': self.user.username, 'dob': '2007-02-27', 'display_name': 'Nik H',
                'gender': 'Male', 'role': 'student', 'class_level': 'Bachelors',
                'edu_status': 'studying', 'edu_program': 'BSc CSIT', 'edu_term': 'Semester 3',
                'edu_completed': '', 'bio': 'Building things', 'skills': 'Python,Design',
                'open_to': 'collab,mentoring', 'email': self.user.email}
        r = self.client.post('/app/profile/edit/', post)
        self.assertIn(r.status_code, (200, 302), r.content[:300])
        self.user.refresh_from_db()
        self.assertEqual((self.user.edu_program, self.user.edu_term, self.user.edu_status),
                         ('BSc CSIT', 'Semester 3', 'studying'))
        self.assertEqual(self.user.bio, 'Building things')
        self.assertEqual(self.user.skills, 'Python,Design')
        self.assertEqual(self.user.open_to, 'collab,mentoring')

    def test_post_without_the_new_fields_leaves_them_alone(self):
        self.user.skills = 'Python,Design'
        self.user.save()
        post = {'username': self.user.username, 'dob': '2007-02-27', 'display_name': 'Nik',
                'gender': 'Male', 'role': 'student', 'class_level': 'Bachelors'}
        self.client.post('/app/profile/edit/', post)
        self.user.refresh_from_db()
        self.assertEqual(self.user.skills, 'Python,Design')

    def test_bad_status_is_refused(self):
        post = {'username': self.user.username, 'dob': '2007-02-27', 'display_name': 'Nik',
                'gender': 'Male', 'role': 'student', 'class_level': 'Bachelors',
                'edu_status': 'nonsense'}
        r = self.client.post('/app/profile/edit/', post)
        self.assertEqual(r.status_code, 200)
        self.assertIn('Choose one of the listed situations', r.content.decode())
