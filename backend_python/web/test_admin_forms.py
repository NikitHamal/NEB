from django.core.cache import cache
from django.test import Client, TestCase

from api.models import Resource, SyllabusContent, User
from api.resource_catalog import DEFAULT_SUBJECTS, EDUCATION_LEVELS, upload_form_options
from api.security import issue_auth_token
from api.utils import now_ms

FORM_KEYS = {'subjects', 'education_levels', 'exam_types', 'pradesh_options', 'resource_types', 'common_tags'}


def _user(user_id, **extra):
    return User.objects.create(
        id=user_id, username=user_id, role=User.ROLE_STUDENT, email=f'{user_id}@example.com',
        email_verified=True, created_at=now_ms(), is_locked=False, is_banned=False, **extra,
    )


def _login(client, user):
    session = client.session
    session['auth_token'] = issue_auth_token(user)
    session.save()


class SyllabusFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        _login(self.client, _user('boss', is_admin=True))

    def _post(self, url, **overrides):
        data = {'grade_level': 'Class 11', 'subject': 'Physics', 'chapter_title': 'Units',
                'chapter_id': 'units', 'order': '2', 'text_content': ' body '}
        data.update(overrides)
        return self.client.post(url, data)

    def test_create_saves_and_redirects(self):
        response = self._post('/admin/syllabus/new/')
        self.assertEqual(response.status_code, 302)
        row = SyllabusContent.objects.get(chapter_id='units')
        self.assertEqual((row.grade_level, row.order, row.text_content), ('Class 11', 2, 'body'))
        self.assertEqual(row.created_at, row.updated_at)

    def test_create_rejects_duplicate_chapter_id(self):
        self._post('/admin/syllabus/new/')
        response = self._post('/admin/syllabus/new/', chapter_title='Other')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')
        self.assertEqual(SyllabusContent.objects.count(), 1)

    def test_bad_rich_json_and_missing_fields_re_render(self):
        self.assertContains(self._post('/admin/syllabus/new/', rich_content_json='{'), 'Interactive content JSON is invalid')
        self.assertContains(self._post('/admin/syllabus/new/', subject=''), 'must be filled')
        self.assertEqual(SyllabusContent.objects.count(), 0)

    def test_edit_updates_in_place_and_may_keep_its_own_chapter_id(self):
        self._post('/admin/syllabus/new/')
        row = SyllabusContent.objects.get(chapter_id='units')
        response = self._post(f'/admin/syllabus/{row.id}/edit/', chapter_title='Units 2', order='x')
        self.assertEqual(response.status_code, 302)
        row.refresh_from_db()
        self.assertEqual((row.chapter_title, row.order), ('Units 2', 0))

    def test_edit_rejects_another_rows_chapter_id(self):
        self._post('/admin/syllabus/new/')
        self._post('/admin/syllabus/new/', chapter_id='second')
        row = SyllabusContent.objects.get(chapter_id='second')
        response = self._post(f'/admin/syllabus/{row.id}/edit/', chapter_id='units')
        self.assertContains(response, 'already exists')

    def test_edit_of_missing_row_goes_back_to_the_list(self):
        self.assertEqual(self.client.get('/admin/syllabus/nope/edit/').status_code, 302)

    def test_anonymous_cannot_open_the_form(self):
        self.assertEqual(Client().get('/admin/syllabus/new/').status_code, 302)


class UploadCatalogTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_subjects_merge_defaults_with_stored_subjects_once_each(self):
        Resource.objects.create(id='r1', title='t', subject='Physics, Astro Lore', added_at=now_ms())
        options = upload_form_options()
        self.assertEqual(set(options), FORM_KEYS)
        self.assertIn('Astro Lore', options['subjects'])
        self.assertEqual(options['subjects'].count('Physics'), 1)
        self.assertEqual(options['subjects'], sorted(options['subjects']))
        self.assertTrue(set(DEFAULT_SUBJECTS) <= set(options['subjects']))

    def test_every_upload_form_gets_the_same_options(self):
        admin = _user('boss', is_admin=True)
        owner = _user('owner')
        Resource.objects.create(id='r2', title='mine', subject='Physics', uploaded_by=owner, added_at=now_ms())
        client = Client()
        _login(client, admin)
        for url in ('/admin/resources/new/', '/admin/resources/r2/'):
            response = client.get(url)
            self.assertEqual(response.status_code, 200, url)
            for key in FORM_KEYS:
                self.assertIn(key, response.context, (url, key))
            self.assertEqual(response.context['education_levels'], EDUCATION_LEVELS)
