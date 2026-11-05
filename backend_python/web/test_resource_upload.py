from decimal import Decimal
from unittest import mock

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from api.models import Resource, User
from api.security import issue_auth_token
from api.utils import now_ms

BASE = {'title': 'Optics notes', 'subject': 'Physics', 'grade_level': 'Class 12'}


def _user(user_id, **extra):
    return User.objects.create(
        id=user_id, username=user_id, role=User.ROLE_STUDENT, email=f'{user_id}@example.com',
        email_verified=True, created_at=now_ms(), is_locked=False, is_banned=False, **extra,
    )


def _login(client, user):
    session = client.session
    session['auth_token'] = issue_auth_token(user)
    session.save()


def _fake_save(request, file_obj):
    return f'resources/{file_obj.name}', 10, None


def _pdf(name):
    return SimpleUploadedFile(name, b'%PDF-1.4', content_type='application/pdf')


class _UploadCase(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        patcher = mock.patch('web.resource_upload.validate_and_save_resource_file', side_effect=_fake_save)
        self.save_file = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('api.resource_form.default_storage')
        self.storage = patcher.start()
        self.addCleanup(patcher.stop)


class PublicUploadTests(_UploadCase):
    URL = '/app/upload/'

    def test_signed_in_url_upload_is_pending_and_owned(self):
        owner = _user('owner')
        _login(self.client, owner)
        response = self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'tags': ' mcq '})
        self.assertEqual(response.status_code, 200)
        row = Resource.objects.get()
        self.assertEqual((row.approval_status, row.source_type, row.uploaded_by_id), ('pending', 'user', 'owner'))
        self.assertEqual((row.tags, row.type, row.is_lead, row.upload_group_id), ('mcq', 'PDF', True, ''))

    def test_anonymous_upload_has_no_owner(self):
        self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf'})
        row = Resource.objects.get()
        self.assertEqual((row.source_type, row.uploaded_by_id), ('anonymous', None))

    def test_several_files_make_one_group_with_a_lead(self):
        self.client.post(self.URL, {**BASE, 'file': [_pdf('one.pdf'), _pdf('two.pdf')]})
        rows = list(Resource.objects.order_by('added_at'))
        self.assertEqual([r.title for r in rows], ['Optics notes', 'Optics notes - two'])
        self.assertEqual([r.is_lead for r in rows], [True, False])
        self.assertEqual(len({r.upload_group_id for r in rows}), 1)
        self.assertNotEqual(rows[0].upload_group_id, '')

    def test_paid_resource_needs_a_price(self):
        response = self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'is_paid': 'on', 'price': '0'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn('valid price', response.json()['errors'][0])
        self.assertEqual(Resource.objects.count(), 0)

    def test_price_is_kept_only_when_paid(self):
        self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'price': '50'})
        self.client.post(self.URL, {**BASE, 'title': 'Paid', 'file_url': 'https://example.com/b.pdf', 'is_paid': 'on', 'price': '50'})
        self.assertEqual(Resource.objects.get(title='Optics notes').price, Decimal('0.00'))
        self.assertEqual(Resource.objects.get(title='Paid').price, Decimal('50'))

    def test_rejected_form_deletes_files_it_already_saved(self):
        response = self.client.post(self.URL, {'subject': 'Physics', 'file': _pdf('lost.pdf')}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.storage.delete.assert_called_once_with('resources/lost.pdf')
        self.assertEqual(Resource.objects.count(), 0)

    def test_bad_thumbnail_url_also_deletes_saved_files(self):
        self.client.post(self.URL, {**BASE, 'file': _pdf('lost.pdf'), 'thumbnail_url': 'javascript:alert(1)'})
        self.storage.delete.assert_called_once_with('resources/lost.pdf')
        self.assertEqual(Resource.objects.count(), 0)

    def test_more_than_five_files_is_an_error(self):
        response = self.client.post(self.URL, {**BASE, 'file': [_pdf(f'{i}.pdf') for i in range(6)]},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn('at most 5', response.json()['errors'][0])


class AdminCreateTests(_UploadCase):
    URL = '/admin/resources/new/'

    def setUp(self):
        super().setUp()
        self.admin = _user('boss', is_admin=True)
        _login(self.client, self.admin)

    def test_defaults_to_approved_and_reviewed_by_the_admin(self):
        self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'view_count': '7'})
        row = Resource.objects.get()
        self.assertEqual((row.approval_status, row.source_type, row.uploaded_by_id, row.reviewed_by_id, row.view_count),
                         ('approved', 'admin', 'boss', 'boss', 7))
        self.assertIsNotNone(row.reviewed_at)

    def test_on_behalf_of_a_user_marks_the_row_as_theirs_and_pending_has_no_reviewer(self):
        _user('student')
        self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'behalf_username': '@Student',
                                    'approval_status': 'pending'})
        row = Resource.objects.get()
        self.assertEqual((row.uploaded_by_id, row.source_type, row.reviewed_by_id, row.reviewed_at), ('student', 'user', None, 0))

    def test_unknown_behalf_user_is_an_error(self):
        response = self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'behalf_username': 'ghost'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn('@ghost', response.json()['errors'][0])

    def test_unknown_status_and_source_fall_back(self):
        self.client.post(self.URL, {**BASE, 'file_url': 'https://example.com/a.pdf', 'approval_status': 'x', 'source_type': 'y'})
        row = Resource.objects.get()
        self.assertEqual((row.approval_status, row.source_type), ('approved', 'admin'))

    def test_missing_title_and_file_report_both(self):
        response = self.client.post(self.URL, {'subject': 'Physics'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json()['errors'], ['Title is required.', 'Please upload a file or provide a file URL.'])

    def test_files_make_a_group(self):
        self.client.post(self.URL, {**BASE, 'file': [_pdf('a.pdf'), _pdf('b.pdf')]})
        self.assertEqual(Resource.objects.filter(is_lead=True).count(), 1)
        self.assertEqual(Resource.objects.exclude(upload_group_id='').count(), 2)


class OwnerEditTests(_UploadCase):
    def setUp(self):
        super().setUp()
        self.owner = _user('owner')
        _login(self.client, self.owner)
        self.row = Resource.objects.create(id='r1', title='Old', subject='Physics', uploaded_by=self.owner,
                                           added_at=now_ms(), approval_status='approved')

    def test_edit_keeps_blank_title_and_toggles_price_with_paid(self):
        self.client.post(f'/app/resource/{self.row.id}/edit/', {'title': '', 'subject': 'Chemistry', 'is_paid': 'on', 'price': '-5'})
        self.row.refresh_from_db()
        self.assertEqual((self.row.title, self.row.subject, self.row.is_paid, self.row.price),
                         ('Old', 'Chemistry', True, Decimal('0.00')))
