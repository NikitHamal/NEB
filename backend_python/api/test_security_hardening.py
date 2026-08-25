"""Regression and integration tests for NEBians backend.

Run locally with:
    SECRET_KEY=test DEBUG=True DB_ENGINE=sqlite python manage.py test api
"""
import hashlib
import uuid
import time
from unittest.mock import patch

from django.test import Client, TestCase
from django.core.exceptions import ValidationError

from .models import Resource, User, Post, Reply, FCMToken, Report
from .security import (
    generate_numeric_code,
    hash_password,
    hash_verification_code,
    make_internal_admin_signature,
    validate_profile_photo_url,
    validate_external_https_url,
    verify_password,
    verify_verification_code,
)
from .mobile_oauth import issue_mobile_oauth_code


def _create_user(**kwargs):
    defaults = {
        'id': str(uuid.uuid4()),
        'auth_token': uuid.uuid4().hex + uuid.uuid4().hex,
        'username': f'testuser_{uuid.uuid4().hex[:8]}',
        'email': f'{uuid.uuid4().hex[:8]}@test.com',
        'created_at': int(time.time() * 1000),
    }
    defaults.update(kwargs)
    return User.objects.create(**defaults)


class PasswordAndCodeSecurityTests(TestCase):
    def test_django_hashes_and_legacy_sha256_migration_flag(self):
        password = 'CorrectHorseBatteryStaple42!'
        modern_hash = hash_password(password)
        self.assertNotEqual(modern_hash, password)
        self.assertTrue(verify_password(password, modern_hash)[0])
        self.assertFalse(verify_password(password, modern_hash)[1])

        legacy_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(verify_password(password, legacy_hash), (True, True))
        self.assertEqual(verify_password('wrong-password', legacy_hash), (False, True))

    def test_verification_codes_are_random_numeric_and_hashed(self):
        code = generate_numeric_code()
        self.assertRegex(code, r'^\d{6}$')
        code_hash = hash_verification_code(code)
        self.assertNotEqual(code_hash, code)
        self.assertTrue(verify_verification_code(code, code_hash))
        self.assertFalse(verify_verification_code('000000', code_hash))

    def test_external_profile_photo_urls_block_local_hosts(self):
        with self.assertRaises(ValidationError):
            validate_profile_photo_url('http://127.0.0.1/private.png')
        with self.assertRaises(ValidationError):
            validate_profile_photo_url('https://localhost/private.png')

    def test_url_validation_blocks_private_networks(self):
        with self.assertRaises(ValidationError):
            validate_external_https_url('https://192.168.1.1/file.pdf')
        with self.assertRaises(ValidationError):
            validate_external_https_url('https://10.0.0.1/file.pdf')
        with self.assertRaises(ValidationError):
            validate_external_https_url('https://172.16.0.1/file.pdf')

    def test_url_validation_allows_public_https(self):
        url = validate_external_https_url('https://example.com/file.pdf')
        self.assertEqual(url, 'https://example.com/file.pdf')

    def test_url_validation_rejects_http_by_default(self):
        with self.assertRaises(ValidationError):
            validate_external_https_url('http://example.com/file.pdf')

    def test_url_validation_rejects_credentials_in_url(self):
        with self.assertRaises(ValidationError):
            validate_external_https_url('https://user:pass@example.com/file.pdf')


class MobileOAuthExchangeTests(TestCase):
    def test_exchange_code_returns_token_once(self):
        code = issue_mobile_oauth_code('raw-token', True, 'new-user')

        response = self.client.post(
            '/api/auth/mobile/exchange/',
            {'code': code},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['authToken'], 'raw-token')
        self.assertTrue(response.json()['isNewUser'])
        self.assertEqual(response.json()['username'], 'new-user')

        replay = self.client.post(
            '/api/auth/mobile/exchange/',
            {'code': code},
            content_type='application/json',
        )
        self.assertEqual(replay.status_code, 400)

    def test_exchange_rejects_missing_code(self):
        response = self.client.post(
            '/api/auth/mobile/exchange/',
            {},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)


class AdminAndPrivacyRegressionTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_legacy_admin_username_and_bearer_token_do_not_grant_admin_api_access(self):
        User.objects.create(
            id='legacy-admin-profile',
            username='admin',
            email='admin@example.test',
            auth_token='legacy-static-token',
            created_at=1,
        )
        response = self.client.get(
            '/api/admin/stats/',
            HTTP_AUTHORIZATION='Bearer legacy-static-token',
        )
        self.assertEqual(response.status_code, 403)

    def test_signed_internal_admin_header_allows_server_side_admin_api_call(self):
        response = self.client.get(
            '/api/admin/stats/',
            HTTP_X_INTERNAL_ADMIN_SIGNATURE=make_internal_admin_signature(),
        )
        self.assertEqual(response.status_code, 200)

    def test_locked_profile_returns_public_serializer_to_anonymous_user(self):
        User.objects.create(
            id='private-user',
            username='lockedstudent',
            email='locked@example.test',
            display_name='Locked Student',
            dob='2006-01-01',
            class_level='12',
            subjects='Physics, Chemistry',
            is_locked=True,
            created_at=1,
        )
        response = self.client.get('/api/users/profile/lockedstudent/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'lockedstudent')
        self.assertNotIn('email', data)
        self.assertNotIn('dob', data)
        self.assertNotIn('subjects', data)

    def test_public_lists_are_paginated(self):
        user = _create_user()
        auth_header = {'HTTP_AUTHORIZATION': f'Bearer {user.auth_token}'}
        for i in range(3):
            Resource.objects.create(
                id=str(uuid.uuid4()),
                title=f'Resource {i}',
                description='Test resource',
                subject='Physics',
                grade_level='12',
                type='PDF',
                file_url='https://example.com/resource.pdf',
                added_at=i,
            )
        response = self.client.get('/api/resources/?page=1&page_size=2', **auth_header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 2)


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user(
            display_name='Test',
            gender='Other',
            class_level='12',
            email_verified=True,
        )
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.auth_token}'}

    def test_profile_update_requires_auth(self):
        response = self.client.post('/api/users/profile/', {'username': 'newname'}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_profile_update_with_valid_auth(self):
        response = self.client.post(
            '/api/users/profile/',
            {'username': self.user.username, 'dob': '2005-06-15'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')

    def test_profile_update_rejects_invalid_photo_url(self):
        response = self.client.post(
            '/api/users/profile/',
            {'username': self.user.username, 'dob': '2005-06-15', 'photoUrl': 'http://evil.com/photo.jpg'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 400)

    def test_profile_update_rejects_invalid_banner_url(self):
        response = self.client.post(
            '/api/users/profile/',
            {'username': self.user.username, 'dob': '2005-06-15', 'bannerUrl': 'http://evil.com/banner.jpg'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 400)

    def test_profile_update_rejects_unverified_email_change(self):
        response = self.client.post(
            '/api/users/profile/',
            {
                'username': self.user.username,
                'dob': '2005-06-15',
                'email': 'replacement@example.test',
            },
            content_type='application/json',
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Email changes require verification')
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'replacement@example.test')

    def test_username_conflict_returns_409(self):
        other_user = _create_user(username='takenname')
        response = self.client.post(
            '/api/users/profile/',
            {'username': 'takenname', 'dob': '2005-06-15'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 409)

    def test_check_username_available(self):
        response = self.client.get('/api/users/check-username/?username=newuniqueuser')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['available'])

    def test_check_username_taken(self):
        response = self.client.get(f'/api/users/check-username/?username={self.user.username}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['available'])


class PostAndReplyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user(display_name='Poster', gender='Other', class_level='12')
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.auth_token}'}

    def test_create_post_requires_auth(self):
        response = self.client.post('/api/posts/', {'title': 'Test', 'content': 'Body', 'category': 'General'}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_and_fetch_post(self):
        response = self.client.post(
            '/api/posts/',
            {'title': 'Test Post', 'content': 'Test content', 'category': 'General'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 201)
        post_id = response.json()['id']

        response = self.client.get(f'/api/posts/{post_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Post')

    def test_create_post_missing_fields(self):
        response = self.client.post(
            '/api/posts/',
            {'title': 'Test'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 400)

    def test_archived_posts_hidden_from_listings(self):
        Post.objects.create(
            id=str(uuid.uuid4()), user=self.user, title='Archived', content='Hidden',
            category='General', thumbs_up_count=0, reply_count=0, created_at=int(time.time() * 1000),
            is_archived=True,
        )
        Post.objects.create(
            id=str(uuid.uuid4()), user=self.user, title='Active', content='Visible',
            category='General', thumbs_up_count=0, reply_count=0, created_at=int(time.time() * 1000),
            is_archived=False,
        )
        response = self.client.get('/api/posts/', **self.auth_header)
        data = response.json()
        titles = [p['title'] for p in data['results']]
        self.assertNotIn('Archived', titles)
        self.assertIn('Active', titles)

    def test_create_reply(self):
        post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.user, title='Test', content='Body',
            category='General', thumbs_up_count=0, reply_count=0, created_at=int(time.time() * 1000),
        )
        response = self.client.post(
            f'/api/posts/{post.id}/replies/',
            {'content': 'Test reply'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['content'], 'Test reply')


class FollowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = _create_user(display_name='User A', gender='Other', class_level='12')
        self.user_b = _create_user(display_name='User B', gender='Other', class_level='12')
        self.auth_a = {'HTTP_AUTHORIZATION': f'Bearer {self.user_a.auth_token}'}

    def test_follow_toggle(self):
        response = self.client.post(f'/api/users/{self.user_b.id}/follow/', **self.auth_a)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_following'])

        response = self.client.post(f'/api/users/{self.user_b.id}/follow/', **self.auth_a)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['is_following'])

    def test_cannot_follow_self(self):
        response = self.client.post(f'/api/users/{self.user_a.id}/follow/', **self.auth_a)
        self.assertEqual(response.status_code, 400)


class FCMTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.auth_token}'}

    def test_fcm_register_requires_token(self):
        response = self.client.post('/api/fcm/register/', {}, content_type='application/json', **self.auth_header)
        self.assertEqual(response.status_code, 400)

    def test_fcm_register_rejects_short_token(self):
        response = self.client.post('/api/fcm/register/', {'token': 'abc'}, content_type='application/json', **self.auth_header)
        self.assertEqual(response.status_code, 400)

    def test_fcm_register_valid_token(self):
        token = 'a' * 100
        response = self.client.post('/api/fcm/register/', {'token': token}, content_type='application/json', **self.auth_header)
        self.assertEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_empty_query(self):
        response = self.client.get('/api/search/?q=')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['resources'], [])
        self.assertEqual(data['posts'], [])

    def test_search_returns_matching_resources(self):
        Resource.objects.create(
            id=str(uuid.uuid4()), title='Physics Grade 12',
            description='Complete notes', subject='Physics',
            grade_level='12', type='PDF',
            file_url='https://example.com/phys.pdf', added_at=1,
        )
        response = self.client.get('/api/search/?q=Physics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['resources']), 1)


class ReportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user(display_name='Reporter', gender='Other', class_level='12')
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.auth_token}'}

    def test_create_report_requires_auth(self):
        response = self.client.post('/api/reports/', {'target_type': 'post', 'target_id': '123'}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_report_invalid_target_type(self):
        response = self.client.post(
            '/api/reports/',
            {'target_type': 'invalid', 'target_id': '123'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 400)

    def test_create_report_success(self):
        response = self.client.post(
            '/api/reports/',
            {'target_type': 'post', 'target_id': 'abc-123', 'reason': 'spam', 'description': 'Test report'},
            content_type='application/json',
            **self.auth_header,
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['target_type'], 'post')
        self.assertEqual(data['reason'], 'spam')
        self.assertEqual(data['status'], 'open')

    def test_admin_can_list_reports(self):
        Report.objects.create(
            id=str(uuid.uuid4()), reporter=self.user, target_type='post',
            target_id='abc-123', reason='spam', status='open',
            created_at=int(time.time() * 1000),
        )
        response = self.client.get(
            '/api/admin/reports/',
            HTTP_X_INTERNAL_ADMIN_SIGNATURE=make_internal_admin_signature(),
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_can_update_report_status(self):
        report = Report.objects.create(
            id=str(uuid.uuid4()), reporter=self.user, target_type='post',
            target_id='abc-123', reason='spam', status='open',
            created_at=int(time.time() * 1000),
        )
        response = self.client.patch(
            f'/api/admin/reports/{report.id}/',
            {'status': 'resolved'},
            content_type='application/json',
            HTTP_X_INTERNAL_ADMIN_SIGNATURE=make_internal_admin_signature(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'resolved')


class EmailAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_requires_all_fields(self):
        response = self.client.post('/api/auth/email/signup/', {'email': 'test@test.com'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_password_too_short(self):
        response = self.client.post(
            '/api/auth/email/signup/',
            {'email': 'test@test.com', 'password': 'abc', 'username': 'testuser123'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_creates_user(self):
        response = self.client.post(
            '/api/auth/email/signup/',
            {'email': 'new@test.com', 'password': 'StrongPass123!', 'username': 'newuser123'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('userId', data)

    def test_login_unverified_returns_403(self):
        from api.security import hash_password
        user = User.objects.create(
            id=str(uuid.uuid4()), username='unverified_user', email='unverified@test.com',
            password_hash=hash_password('TestPass123!'),
            email_verified=False, created_at=int(time.time() * 1000),
            auth_token=uuid.uuid4().hex + uuid.uuid4().hex,
        )
        response = self.client.post(
            '/api/auth/email/login/',
            {'email': 'unverified@test.com', 'password': 'TestPass123!'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)


class ResultCheckerAPITests(TestCase):
    def setUp(self):
        from django.test import Client
        self.client = Client()

    @patch('services.result_scraper.check_result')
    def test_ajax_check_result_see_no_dob(self, mock_check):
        mock_check.return_value = {
            'success': True,
            'data': {
                'symbol': '71234567',
                'student_name': 'TEST STUDENT',
                'gpa': '3.90',
                'subjects': []
            },
            'cached': False
        }
        
        # Test SEE: dob is not required!
        response = self.client.post(
            '/ajax/results/check/',
            {'exam': 'see', 'symbol': '71234567', 'batch': '2080'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        mock_check.assert_called_with('see', '71234567', '', batch='2080')

    @patch('services.result_scraper.check_result')
    def test_ajax_check_result_neb_requires_dob(self, mock_check):
        # Test NEB: dob is required!
        response = self.client.post(
            '/ajax/results/check/',
            {'exam': 'neb', 'symbol': '21234567', 'batch': '2080'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('Date of birth is required', response.json()['error'])
        mock_check.assert_not_called()