"""Regression tests for the NEBians security hardening pass.

Run locally with, for example:
SECRET_KEY=test DEBUG=True DB_ENGINE=sqlite python manage.py test api
"""
import hashlib
import uuid

from django.test import Client, TestCase

from .models import Resource, User
from .security import (
    generate_numeric_code,
    hash_password,
    hash_verification_code,
    make_internal_admin_signature,
    validate_profile_photo_url,
    verify_password,
    verify_verification_code,
)


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
        with self.assertRaises(Exception):
            validate_profile_photo_url('http://127.0.0.1/private.png')
        with self.assertRaises(Exception):
            validate_profile_photo_url('https://localhost/private.png')


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
        response = self.client.get('/api/resources/?page=1&page_size=2')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 2)
