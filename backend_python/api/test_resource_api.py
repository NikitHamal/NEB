import uuid
from unittest import mock

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from api.models import Resource, ResourceRequest, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms

FILE_URL = 'https://example.com/a.pdf'


def _member(username, **extra):
    raw = f'tok-{username}-{uuid.uuid4().hex}'
    user = User.objects.create(
        id=f'u-{username}', username=username, email=f'{username}@example.com', email_verified=True,
        auth_token=hash_auth_token(raw), created_at=now_ms(), **extra,
    )
    UserAuthToken.objects.create(
        id=str(uuid.uuid4()), user=user, token_hash=hash_auth_token(raw), created_at=now_ms(),
        last_used_at=now_ms(), revoked_at=0, expires_at=now_ms() + AUTH_TOKEN_TTL_MS,
    )
    user.bearer = {'HTTP_AUTHORIZATION': f'Bearer {raw}'}
    return user


def _resource(title, **extra):
    return Resource.objects.create(
        id=str(uuid.uuid4()), title=title, subject=extra.pop('subject', 'Physics'), added_at=extra.pop('added_at', now_ms()),
        approval_status='approved', is_lead=True, **extra,
    )


class _ApiCase(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()


class UploadTests(_ApiCase):
    def test_signed_in_upload_is_pending_owned_and_may_be_paid(self):
        owner = _member('owner')
        response = self.client.post(
            '/api/resources/upload/',
            {'title': ' Notes ', 'subject': 'Physics', 'file_url': FILE_URL, 'is_paid': 'true', 'price': '40', 'tags': ' mcq '},
            **owner.bearer,
        )
        self.assertEqual(response.status_code, 201)
        row = Resource.objects.get()
        self.assertEqual((row.title, row.tags, row.type), ('Notes', 'mcq', 'PDF'))
        self.assertEqual((row.approval_status, row.source_type, row.uploaded_by_id), ('pending', 'user', owner.id))
        self.assertEqual((row.is_paid, int(row.price)), (True, 40))

    def test_signed_out_upload_to_the_member_route_is_refused(self):
        response = self.client.post('/api/resources/upload/', {'title': 'x', 'subject': 'y', 'file_url': FILE_URL})
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Resource.objects.exists())

    def test_anonymous_upload_has_no_owner_and_cannot_be_paid(self):
        response = self.client.post('/api/resources/upload/anonymous/', {
            'title': 'Notes', 'subject': 'Physics', 'file_url': FILE_URL, 'is_paid': 'true', 'price': '40',
            'requester_name': 'n' * 150, 'author_name': 'ignored',
        })
        self.assertEqual(response.status_code, 201)
        row = Resource.objects.get()
        self.assertEqual((row.approval_status, row.source_type, row.uploaded_by_id), ('pending', 'anonymous', None))
        self.assertEqual((row.author_name, row.is_paid), ('n' * 100, False))

    def test_missing_title_subject_or_file_is_refused(self):
        for body in ({'subject': 'Physics', 'file_url': FILE_URL}, {'title': 'x', 'file_url': FILE_URL}, {'title': 'x', 'subject': 'y'}):
            response = self.client.post('/api/resources/upload/anonymous/', body)
            self.assertEqual(response.status_code, 400, body)
        self.assertFalse(Resource.objects.exists())

    def test_unsafe_links_are_refused(self):
        for key in ('file_url', 'source_url', 'thumbnail_url'):
            body = {'title': 'x', 'subject': 'y', 'file_url': FILE_URL, key: 'javascript:alert(1)'}
            response = self.client.post('/api/resources/upload/anonymous/', body)
            self.assertEqual(response.status_code, 400, key)
        self.assertFalse(Resource.objects.exists())

    def test_uploaded_file_is_stored_and_linked(self):
        with mock.patch('api.views_resources.validate_and_save_resource_file', return_value=('resources/a.pdf', 8, None)):
            response = self.client.post('/api/resources/upload/anonymous/', {
                'title': 'x', 'subject': 'y', 'file': SimpleUploadedFile('a.pdf', b'%PDF-1.4'),
            })
        self.assertEqual(response.status_code, 201)
        row = Resource.objects.get()
        self.assertEqual((row.file.name, row.file_size), ('resources/a.pdf', 8))
        self.assertTrue(row.file_url.endswith('/resources/a.pdf'))

    def test_file_saved_before_a_bad_cover_is_deleted(self):
        with mock.patch('api.views_resources.validate_and_save_resource_file', return_value=('resources/a.pdf', 8, None)), \
                mock.patch('api.resource_form.default_storage') as storage:
            response = self.client.post('/api/resources/upload/anonymous/', {
                'title': 'x', 'subject': 'y', 'file': SimpleUploadedFile('a.pdf', b'%PDF-1.4'),
                'thumbnail_url': 'javascript:alert(1)',
            })
        self.assertEqual(response.status_code, 400)
        storage.delete.assert_called_once_with('resources/a.pdf')
        self.assertFalse(Resource.objects.exists())


class OwnerEditTests(_ApiCase):
    def test_owner_edit_changes_fields_clears_cover_and_returns_to_review(self):
        owner = _member('owner')
        row = _resource('Old', uploaded_by=owner, thumbnail_url='https://example.com/c.png', tags='a')
        response = self.client.put(
            f'/api/resources/{row.id}/', {'title': ' New ', 'thumbnail_url': '', 'is_paid': 'true', 'price': '25'},
            content_type='application/json', **owner.bearer,
        )
        self.assertEqual(response.status_code, 200, response.content)
        row.refresh_from_db()
        self.assertEqual((row.title, row.tags, row.thumbnail_url), ('New', 'a', ''))
        self.assertEqual((row.approval_status, row.is_paid, int(row.price)), ('pending', True, 25))

    def test_edit_without_a_cover_field_keeps_the_cover(self):
        owner = _member('owner')
        row = _resource('Old', uploaded_by=owner, thumbnail_url='https://example.com/c.png')
        self.client.patch(f'/api/resources/{row.id}/', {'description': 'd'}, content_type='application/json', **owner.bearer)
        row.refresh_from_db()
        self.assertEqual((row.description, row.thumbnail_url), ('d', 'https://example.com/c.png'))

    def test_only_the_owner_edits_and_blank_title_is_refused(self):
        owner, other = _member('owner'), _member('other')
        row = _resource('Old', uploaded_by=owner)
        denied = self.client.put(f'/api/resources/{row.id}/', {'title': 'x'}, content_type='application/json', **other.bearer)
        blank = self.client.put(f'/api/resources/{row.id}/', {'title': ' '}, content_type='application/json', **owner.bearer)
        self.assertEqual((denied.status_code, blank.status_code), (403, 400))

    def test_bad_link_on_edit_is_refused_and_nothing_changes(self):
        owner = _member('owner')
        row = _resource('Old', uploaded_by=owner)
        response = self.client.put(
            f'/api/resources/{row.id}/', {'title': 'New', 'file_url': 'javascript:alert(1)'},
            content_type='application/json', **owner.bearer,
        )
        self.assertEqual(response.status_code, 400)
        row.refresh_from_db()
        self.assertEqual(row.title, 'Old')


class ListOrderTests(_ApiCase):
    def titles(self, query='', **headers):
        response = self.client.get(f'/api/resources/?{query}', **headers)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        return [r['title'] for r in (body['results'] if isinstance(body, dict) else body)]

    def setUp(self):
        super().setUp()
        _resource('old-popular', added_at=1, like_count=9, view_count=1, subject='Chemistry')
        _resource('mid', added_at=2, like_count=1, view_count=9, subject='Physics')
        _resource('new', added_at=3, like_count=0, view_count=0, subject='Biology')

    def test_each_sort(self):
        self.assertEqual(self.titles('sort=newest'), ['new', 'mid', 'old-popular'])
        self.assertEqual(self.titles('sort=oldest'), ['old-popular', 'mid', 'new'])
        self.assertEqual(self.titles('sort=liked'), ['old-popular', 'mid', 'new'])
        self.assertEqual(self.titles('sort=trending'), ['mid', 'old-popular', 'new'])
        self.assertEqual(self.titles('sort=anything'), ['new', 'mid', 'old-popular'])
        self.assertEqual(self.titles(), ['new', 'mid', 'old-popular'])

    def test_a_members_subjects_float_matches_first(self):
        member = _member('reader', subjects='Chemistry')
        self.assertEqual(self.titles('sort=newest', **member.bearer), ['old-popular', 'new', 'mid'])
        self.assertEqual(self.titles('sort=oldest', **member.bearer), ['old-popular', 'mid', 'new'])


class RequestTests(_ApiCase):
    def test_signed_in_request_is_owned(self):
        member = _member('asker')
        response = self.client.post('/api/resource-requests/create/', {'title': ' Past papers ', 'subject': 'Physics'}, **member.bearer)
        self.assertEqual(response.status_code, 201)
        row = ResourceRequest.objects.get()
        self.assertEqual((row.title, row.subject, row.requested_by_id), ('Past papers', 'Physics', member.id))

    def test_anonymous_request_keeps_contact_details(self):
        response = self.client.post('/api/resource-requests/anonymous/', {
            'title': 'Past papers', 'requester_name': 'n' * 150, 'requester_email': ' a@b.co ',
        })
        self.assertEqual(response.status_code, 201)
        row = ResourceRequest.objects.get()
        self.assertEqual((row.requested_by_id, row.requester_name, row.requester_email), (None, 'n' * 100, 'a@b.co'))

    def test_title_is_required_and_members_must_sign_in(self):
        self.assertEqual(self.client.post('/api/resource-requests/anonymous/', {'title': ' '}).status_code, 400)
        self.assertEqual(self.client.post('/api/resource-requests/create/', {'title': 'x'}).status_code, 401)
        self.assertFalse(ResourceRequest.objects.exists())
