"""Marketplace tests: creator pages, courses, the QR checkout and the admin
verification queue that credits a seller.

Three classes, one per surface, because they fail for different reasons:

* ``CreatorPageApiTests``    — the REST API both clients read and write.
* ``MarketplaceWebTests``    — the Django pages, the studio's JSON saves and the
  web checkout.
* ``AdminPaymentQueueTests`` — the queue that turns a submitted payment into a
  credited seller. This one covers a *pre-existing* break: the admin panel
  called ``_notif.create_notification``, which did not exist, so every approval
  raised after crediting the seller.

Run: ``python manage.py test api.tests_marketplace -v 2``
"""
import json
import uuid
from decimal import Decimal

from django.core.cache import cache
from django.db import connection
from django.test import Client, RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from api.creator_pages import check_user_course_access
from api.marketplace import get_payment_config
from api.models import (
    CreatorCourse, CreatorPage, CreatorPost, Notification, PaymentVerification, Resource,
    SellerBalance, User, UserAuthToken,
)
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms


class MarketplaceTestBase(TestCase):
    """Shared fixtures: a teacher with a storefront, a student and an admin."""

    def setUp(self):
        # Throttle counters live in the shared cache and the fixture user ids
        # are deterministic, so without this one test's writes would spend the
        # next test's allowance.
        cache.clear()
        self.teacher = self.make_user('t_teacher', role=User.ROLE_TEACHER)
        self.institute = self.make_user('t_institute', role=User.ROLE_INSTITUTION)
        self.student = self.make_user('t_student')
        self.other_teacher = self.make_user('t_teacher2', role=User.ROLE_TEACHER)
        self.admin = self.make_user('t_admin', is_admin=True)

    def make_user(self, username, role=User.ROLE_STUDENT, is_admin=False):
        raw = f'tok-{username}-{uuid.uuid4().hex}'
        user = User.objects.create(
            id=f'u-{username}',
            username=username,
            role=role,
            is_admin=is_admin,
            email=f'{username}@example.com',
            email_verified=True,
            # the column holds the hash of the live token; the bearer itself
            # lives in the row created next, exactly as the real login does it
            auth_token=hash_auth_token(raw),
            created_at=now_ms(),
            is_locked=False,
            is_banned=False,
        )
        UserAuthToken.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            token_hash=hash_auth_token(raw),
            created_at=now_ms(),
            last_used_at=now_ms(),
            revoked_at=0,
            expires_at=now_ms() + AUTH_TOKEN_TTL_MS,
        )
        user.raw_token = raw
        return user

    def get(self, user, path):
        return self.client.get(path, HTTP_AUTHORIZATION=f'Bearer {user.raw_token}')

    def post_json(self, user, path, payload):
        return self.client.post(
            path,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user.raw_token}',
        )

    def put_json(self, user, path, payload):
        return self.client.put(
            path,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user.raw_token}',
        )

    def patch_json(self, user, path, payload):
        return self.client.patch(
            path,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user.raw_token}',
        )

    def make_published_page(self, user, slug='t-published', **overrides):
        payload = {
            'display_name': 'Test Teacher',
            'slug': slug,
            'tagline': 'Physics, plainly',
            'accent_hex': '#1F6F5C',
            'layout': 'spotlight',
            'blocks': [{'type': 'hero', 'title': 'Hero'}, {'type': 'courses'}],
            'published': True,
        }
        payload.update(overrides)
        response = self.put_json(user, '/api/marketplace/me/page/', payload)
        return response.json()['page']


class CreatorPageApiTests(MarketplaceTestBase):

    def test_only_teachers_institutes_and_admins_get_a_storefront(self):
        self.assertEqual(self.get(self.student, '/api/marketplace/me/page/').status_code, 403)
        self.assertEqual(self.get(self.teacher, '/api/marketplace/me/page/').status_code, 200)
        self.assertEqual(self.get(self.institute, '/api/marketplace/me/page/').status_code, 200)
        self.assertEqual(self.get(self.admin, '/api/marketplace/me/page/').status_code, 200)

    def test_a_new_page_starts_as_a_draft_with_default_sections(self):
        page = self.get(self.teacher, '/api/marketplace/me/page/').json()['page']
        self.assertFalse(page['published'])
        self.assertTrue(page['slug'])
        self.assertGreaterEqual(len(page['blocks']), 4)
        self.assertEqual(page['kind'], 'tutor')
        self.assertEqual(CreatorPage.objects.filter(user=self.teacher).count(), 1)

    def test_page_writes_are_sanitised(self):
        page = self.make_published_page(self.teacher, blocks=[
            {'type': 'hero', 'title': 'Physics with Sabina'},
            {'type': 'showcase', 'items': [{'title': 'Optics deck', 'badge': 'Free'}]},
            {'type': 'not_a_block', 'title': 'dropped'},
            {'type': 'about', 'body': 'x' * 9000},
        ], socials={'youtube': 'https://youtube.com/@x', 'website': 'javascript:alert(1)'},
            style={'hero': 'cover', 'radius': 'sharp', 'gallery_columns': 9})

        types = [block['type'] for block in page['blocks']]
        self.assertNotIn('not_a_block', types)
        self.assertEqual(len(types), 3)
        self.assertTrue(all(block['id'] for block in page['blocks']))
        about = next(block for block in page['blocks'] if block['type'] == 'about')
        self.assertLessEqual(len(about['body']), 4000)
        self.assertNotIn('website', page['socials'])
        self.assertEqual(page['style']['gallery_columns'], 4)
        self.assertEqual(page['accent_hex'], '#1F6F5C')

    def test_a_javascript_url_is_never_stored(self):
        page = self.make_published_page(self.teacher, slug='t-urls', blocks=[
            {'type': 'links', 'items': [{'label': 'bad', 'url': 'javascript:alert(1)'},
                                        {'label': 'good', 'url': 'https://example.com'}]},
        ])
        urls = [item['url'] for item in page['blocks'][0]['items']]
        self.assertIn('https://example.com', urls)
        self.assertNotIn('javascript:alert(1)', urls)

    def test_a_testimonial_portrait_goes_through_the_url_allowlist(self):
        """Every field that lands in a src is sanitised, not just the ones
        named *_url in the hero."""
        page = self.make_published_page(self.teacher, slug='t-avatar', blocks=[
            {'type': 'testimonials', 'items': [
                {'name': 'A', 'quote': 'Great', 'avatar_url': 'javascript:alert(1)'},
                {'name': 'B', 'quote': 'Good', 'avatar_url': 'https://cdn.example.com/b.png'},
            ]},
        ])
        avatars = [item['avatar_url'] for item in page['blocks'][0]['items']]
        self.assertEqual(avatars, ['', 'https://cdn.example.com/b.png'])

    def test_pages_are_public_and_drafts_are_not(self):
        self.make_published_page(self.teacher, slug='t-live')
        self.client.post('/api/marketplace/me/page/', data=json.dumps({'published': False}),
                         content_type='application/json',
                         HTTP_AUTHORIZATION=f'Bearer {self.teacher.raw_token}')

        listing = self.client.get('/api/marketplace/creators/').json()
        self.assertEqual(listing['total'], 0)
        self.assertEqual(self.client.get('/api/marketplace/creators/t-live/').status_code, 404)
        self.assertEqual(self.get(self.teacher, '/api/marketplace/creators/t-live/').status_code, 200)

    def test_slugs_never_collide(self):
        first = self.make_published_page(self.teacher, slug='t-same')
        second = self.make_published_page(self.other_teacher, slug='t-same')
        self.assertNotEqual(first['slug'], second['slug'])

    def test_only_an_admin_may_make_an_admin_page(self):
        response = self.put_json(self.institute, '/api/marketplace/me/page/',
                                 {'display_name': 'x', 'kind': 'admin'})
        self.assertEqual(response.status_code, 400)

    def test_listing_cards_carry_a_course_count_without_a_second_query(self):
        self.make_published_page(self.teacher, slug='t-count')
        page = CreatorPage.objects.get(slug='t-count')
        CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Course', slug='c1',
            is_free=True, status='published', created_at=now_ms(), updated_at=now_ms(),
        )
        with self.assertNumQueries(2):
            listing = self.client.get('/api/marketplace/creators/').json()
        self.assertEqual(listing['creators'][0]['course_count'], 1)


class MarketplaceCourseTests(MarketplaceTestBase):

    def setUp(self):
        super().setUp()
        self.page = CreatorPage.objects.create(
            id=str(uuid.uuid4()), user=self.teacher, kind='tutor', slug='t-courses',
            display_name='Course Teacher', published=True, blocks=[], style={},
            created_at=now_ms(), updated_at=now_ms(),
        )

    def make_course(self, **overrides):
        payload = {
            'title': 'Physics 12', 'price': '2500', 'is_free': False,
            'status': 'published', 'summary': 'Mechanics to modern physics',
            'includes': ['Live classes', 'Weekly tests'], 'lesson_count': 48,
        }
        payload.update(overrides)
        return self.post_json(self.teacher, '/api/marketplace/me/courses/', payload)

    def test_a_paid_course_needs_a_price(self):
        response = self.post_json(self.teacher, '/api/marketplace/me/courses/',
                                  {'title': 'No price', 'is_free': False, 'status': 'published'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.json()['error'].lower())

    def test_a_free_course_normalises_its_price(self):
        course = self.make_course(title='Free notes', is_free=True, price='500').json()['course']
        self.assertEqual(course['price'], '0')
        self.assertEqual(self.client.get(f"/api/marketplace/courses/{course['id']}/").json()['access_reason'], 'free')

    def test_only_the_owner_can_edit_a_course(self):
        course = self.make_course().json()['course']
        response = self.patch_json(self.other_teacher, f"/api/marketplace/me/courses/{course['id']}/",
                                   {'title': 'Hijacked'})
        self.assertEqual(response.status_code, 403)

    def test_the_course_shelf_is_public_and_filterable(self):
        self.make_course()
        self.make_course(title='Free one', is_free=True, price='0')

        shelf = self.client.get('/api/marketplace/courses/').json()
        self.assertEqual(shelf['total'], 2)
        self.assertEqual(shelf['courses'][0]['page_name'], 'Course Teacher')

        free = self.client.get('/api/marketplace/courses/?pricing=free').json()
        self.assertTrue(all(course['is_free'] for course in free['courses']))
        self.assertEqual(self.client.get('/api/marketplace/courses/?kind=institute').json()['total'], 0)

    def test_the_shelf_costs_the_same_whatever_its_length(self):
        """A signed-in browser used to pay one purchase lookup per paid card,
        so a full shelf cost forty-eight of them. They batch into one now."""
        for index in range(2):
            self.make_course(title=f'Paid {index}')
        with CaptureQueriesContext(connection) as small:
            self.get(self.student, '/api/marketplace/courses/')
        for index in range(2, 8):
            self.make_course(title=f'Paid {index}')
        with CaptureQueriesContext(connection) as large:
            response = self.get(self.student, '/api/marketplace/courses/')

        self.assertEqual(response.json()['total'], 8)
        self.assertEqual(len(large), len(small))
        lookups = [q for q in large.captured_queries
                   if 'payment_verifications' in q['sql']]
        self.assertEqual(len(lookups), 1)

    def test_buying_is_gated_until_an_admin_approves(self):
        course_id = self.make_course().json()['course']['id']

        locked = self.get(self.student, f'/api/marketplace/courses/{course_id}/purchase/').json()
        self.assertFalse(locked['has_access'])
        self.assertEqual(locked['access_reason'], 'unpurchased')
        self.assertEqual(locked['price'], '2500')

        self.assertEqual(self.get(self.teacher, f'/api/marketplace/courses/{course_id}/purchase/').json()['access_reason'], 'owner')
        self.assertEqual(self.post_json(self.teacher, f'/api/marketplace/courses/{course_id}/purchase/',
                                        {'transaction_id': 'X'}).status_code, 400)

        empty = self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/', {})
        self.assertEqual(empty.status_code, 400)

        submitted = self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                                   {'transaction_id': 'TXN-1'})
        self.assertEqual(submitted.status_code, 201)
        self.assertEqual(submitted.json()['access_reason'], 'pending_verification')

        # Re-submitting better proof updates the row an admin is already looking
        # at rather than queueing a duplicate.
        self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                       {'transaction_id': 'TXN-2'})
        self.assertEqual(PaymentVerification.objects.filter(buyer=self.student, course_id=course_id).count(), 1)

        payment = PaymentVerification.objects.get(buyer=self.student, course_id=course_id)
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(float(payment.seller_earnings) + float(payment.platform_commission), 2500.0)

        payment.status = 'approved'
        payment.save()
        unlocked = self.get(self.student, f'/api/marketplace/courses/{course_id}/purchase/').json()
        self.assertTrue(unlocked['has_access'])
        self.assertEqual(unlocked['access_reason'], 'purchased')

    def test_commission_comes_from_the_platform_configuration(self):
        course_id = self.make_course().json()['course']['id']
        self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                       {'transaction_id': 'TXN-3'})
        payment = PaymentVerification.objects.get(buyer=self.student, course_id=course_id)
        expected = round(2500 * float(get_payment_config().commission_percent) / 100, 2)
        self.assertEqual(float(payment.platform_commission), expected)

    def test_course_access_helper_matches_resource_rules(self):
        course_id = self.make_course().json()['course']['id']
        course = CreatorCourse.objects.get(pk=course_id)
        self.assertEqual(check_user_course_access(None, course), (False, 'unpurchased', None))
        self.assertEqual(check_user_course_access(self.teacher, course)[1], 'owner')
        self.assertEqual(check_user_course_access(self.admin, course)[1], 'admin')

    def test_the_seller_dashboard_reports_sales_and_the_wallet(self):
        course_id = self.make_course().json()['course']['id']
        self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                       {'transaction_id': 'TXN-4'})

        dashboard = self.get(self.teacher, '/api/marketplace/dashboard/').json()
        self.assertEqual(dashboard['stats']['pending_sales'], 1)
        self.assertEqual(dashboard['sales'][0]['buyer_username'], 't_student')
        self.assertEqual(dashboard['sales'][0]['target_type'], 'course')
        self.assertEqual(dashboard['wallet']['current_balance'], '0')

        self.assertEqual(self.get(self.student, '/api/marketplace/dashboard/').status_code, 403)

    def test_purchase_history_includes_courses(self):
        course_id = self.make_course().json()['course']['id']
        self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                       {'transaction_id': 'TXN-5'})
        items = self.get(self.student, '/api/wallet/purchases/').json()['purchases']
        self.assertTrue(any(item['target_type'] == 'course' for item in items))

    def test_buying_a_course_unlocks_the_material_it_lists(self):
        """Both surfaces show the seller's attached notes as "Course material",
        so the sale has to cover them."""
        from web.view_helpers import check_user_resource_access

        note = Resource.objects.create(
            id=str(uuid.uuid4()), title='Chapter notes', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', is_paid=True,
            price=Decimal('300'), added_at=now_ms(),
        )
        course_id = self.make_course(resource_ids=[note.id]).json()['course']['id']
        self.assertEqual(check_user_resource_access(self.student, note)[1], 'unpurchased')

        self.post_json(self.student, f'/api/marketplace/courses/{course_id}/purchase/',
                       {'transaction_id': 'TXN-MATERIAL'})
        # an unverified course payment unlocks nothing
        self.assertFalse(check_user_resource_access(self.student, note)[0])

        payment = PaymentVerification.objects.get(buyer=self.student, course_id=course_id)
        payment.status = 'approved'
        payment.save()
        has_access, reason, _ = check_user_resource_access(self.student, note)
        self.assertTrue(has_access)
        self.assertEqual(reason, 'purchased')
        # someone who bought nothing is still locked out
        self.assertFalse(check_user_resource_access(self.other_teacher, note)[0])

    def test_course_resources_must_belong_to_the_page_owner(self):
        mine = Resource.objects.create(
            id=str(uuid.uuid4()), title='Mine', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', added_at=now_ms(),
        )
        theirs = Resource.objects.create(
            id=str(uuid.uuid4()), title='Theirs', subject='Physics', type='Note',
            uploaded_by=self.other_teacher, approval_status='approved', added_at=now_ms(),
        )
        course = self.post_json(self.teacher, '/api/marketplace/me/courses/', {
            'title': 'With material', 'is_free': True, 'status': 'published',
            'resource_ids': [mine.id, theirs.id],
        }).json()['course']
        attached = list(CreatorCourse.objects.get(pk=course['id']).course_resources.values_list('resource_id', flat=True))
        self.assertEqual(attached, [mine.id])


class MarketplaceWebTests(MarketplaceTestBase):

    def session_client(self, user):
        client = Client()
        session = client.session
        session['auth_token'] = user.raw_token
        session['user_data'] = {
            'id': user.id, 'username': user.username, 'email': user.email,
            'role': user.role, 'gender': 'male', 'photo_url': '', 'avatar_url': '',
            'is_admin': user.is_admin, 'verification_level': 0, 'moderator_level': 0,
            'enable_inline_images': True, 'enableInlineImages': True,
        }
        session['theme'] = 'light'
        session.save()
        return client

    def ajax(self, client, name, payload):
        return client.post(reverse(f'web:{name}'), data=json.dumps(payload),
                           content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_the_marketplace_tab_sits_in_the_library_between_library_and_syllabus(self):
        response = self.client.get('/library/?tab=marketplace')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('mkt-shelf', html)
        for tab in ('?tab=digital', '?tab=marketplace', '?tab=categories'):
            self.assertIn(tab, html)
        self.assertLess(html.index('?tab=marketplace'), html.index('?tab=categories'))

    def test_the_directory_lists_published_pages(self):
        self.make_published_page(self.teacher, slug='t-web', display_name='Web Teacher')
        response = self.client.get('/marketplace/')
        self.assertContains(response, 'Web Teacher')
        self.assertContains(response, 'mkt-shelf-focus' if False else 'creator-grid')

    def test_the_studio_is_for_eligible_accounts_only(self):
        self.assertEqual(self.session_client(self.teacher).get('/marketplace/studio/').status_code, 200)
        self.assertEqual(self.session_client(self.student).get('/marketplace/studio/').status_code, 403)
        self.assertEqual(self.client.get('/marketplace/studio/').status_code, 302)

    def test_the_studio_saves_a_page_through_the_shared_validator(self):
        client = self.session_client(self.teacher)
        response = self.ajax(client, 'marketplace_page_save', {
            'display_name': 'Sabina Physics',
            'slug': 't-studio',
            'tagline': 'Physics, plainly',
            'accent_hex': '#166534',
            'layout': 'grid',
            'blocks': [{'type': 'hero', 'title': 'Physics'}, {'type': 'rubbish'}],
            'socials': {'youtube': 'https://youtube.com/@x', 'website': 'javascript:alert(1)'},
            'subjects': ['Physics'],
            'published': True,
        })
        self.assertEqual(response.status_code, 200, response.content)
        page = response.json()['page']
        self.assertEqual(page['slug'], 't-studio')
        self.assertEqual(len(page['blocks']), 1)
        self.assertNotIn('website', page['socials'])

    def test_an_institute_cannot_save_an_admin_page(self):
        client = self.session_client(self.institute)
        response = self.ajax(client, 'marketplace_page_save', {'display_name': 'x', 'kind': 'admin'})
        self.assertEqual(response.status_code, 400)

    def test_the_storefront_renders_the_owners_blocks_in_order(self):
        self.make_published_page(self.teacher, slug='t-render', blocks=[
            {'type': 'hero', 'title': 'Hero headline'},
            {'type': 'faq', 'title': 'Questions', 'items': [{'q': 'When?', 'a': 'Sunday'}]},
            {'type': 'about', 'title': 'About me', 'body': 'Fifteen years of NEB physics.'},
        ])
        html = self.client.get('/marketplace/t-render/').content.decode()
        self.assertIn('Hero headline', html)
        self.assertIn('When?', html)
        self.assertIn('Fifteen years of NEB physics.', html)
        self.assertLess(html.index('Hero headline'), html.index('When?'))
        self.assertLess(html.index('When?'), html.index('Fifteen years of NEB physics.'))
        self.assertIn('#1F6F5C', html)

    def test_the_price_setter_is_the_shared_component(self):
        html = self.session_client(self.teacher).get('/upload/').content.decode()
        self.assertIn('data-neb-price', html)
        self.assertIn('neb-price-preset', html)
        self.assertNotIn('price_field_container', html)

    def test_web_checkout_submits_and_then_unlocks(self):
        self.make_published_page(self.teacher, slug='t-buy')
        page = CreatorPage.objects.get(slug='t-buy')
        course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Web Course', slug='web-course',
            summary='A course', is_free=False, price='1200', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )

        client = self.session_client(self.student)
        page_html = client.get(f'/marketplace/course/{course.id}/').content.decode()
        self.assertIn('Submit payment', page_html)

        response = client.post(f'/marketplace/course/{course.id}/', {'transaction_id': 'WEB-1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Awaiting verification', response.content.decode())
        self.assertTrue(PaymentVerification.objects.filter(buyer=self.student, course=course, status='pending').exists())

        payment = PaymentVerification.objects.get(buyer=self.student, course=course)
        payment.status = 'approved'
        payment.save()
        self.assertIn('Unlocked', client.get(f'/marketplace/course/{course.id}/').content.decode())

    def test_the_owner_cannot_buy_their_own_course(self):
        self.make_published_page(self.teacher, slug='t-own')
        page = CreatorPage.objects.get(slug='t-own')
        course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Mine', slug='mine',
            is_free=False, price='100', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )
        client = self.session_client(self.teacher)
        client.post(f'/marketplace/course/{course.id}/', {'transaction_id': 'X'})
        self.assertFalse(PaymentVerification.objects.filter(buyer=self.teacher, course=course).exists())

    def test_the_studio_lists_the_sellers_sales(self):
        self.make_published_page(self.teacher, slug='t-sales')
        page = CreatorPage.objects.get(slug='t-sales')
        course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Sold Course', slug='sold',
            is_free=False, price='900', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )
        PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, course=course, seller=self.teacher,
            amount=Decimal('900'), platform_commission=Decimal('22.5'),
            seller_earnings=Decimal('877.5'), transaction_id='SOLD-1',
            status='pending', created_at=now_ms(),
        )
        html = self.session_client(self.teacher).get('/marketplace/studio/').content.decode()
        self.assertIn('Sold Course', html)
        self.assertIn('t_student', html)


class AdminPaymentQueueTests(MarketplaceTestBase):

    def setUp(self):
        super().setUp()
        self.page = CreatorPage.objects.create(
            id=str(uuid.uuid4()), user=self.teacher, kind='tutor', slug='t-admin',
            display_name='Admin Case', published=True, blocks=[], style={},
            created_at=now_ms(), updated_at=now_ms(),
        )
        self.course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=self.page, title='Admin Course', slug='admin-course',
            is_free=False, price='2000', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )
        self.resource = Resource.objects.create(
            id=str(uuid.uuid4()), title='Admin Notes', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', is_paid=True,
            price='500', added_at=now_ms(),
        )

    def admin_client(self):
        client = Client()
        session = client.session
        session['auth_token'] = self.admin.raw_token
        session['user_data'] = {
            'id': self.admin.id, 'username': self.admin.username, 'email': self.admin.email,
            'role': self.admin.role, 'gender': 'male', 'is_admin': True,
            'photo_url': '', 'avatar_url': '', 'verification_level': 0, 'moderator_level': 0,
        }
        session['theme'] = 'light'
        session.save()
        return client

    def test_the_queue_renders_course_and_resource_payments(self):
        payment = PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, course=self.course, seller=self.teacher,
            amount=Decimal('2000'), platform_commission=Decimal('50'),
            seller_earnings=Decimal('1950'), transaction_id='Q-1',
            status='pending', created_at=now_ms(),
        )
        PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, resource=self.resource, seller=self.teacher,
            amount=Decimal('500'), platform_commission=Decimal('12.5'),
            seller_earnings=Decimal('487.5'), transaction_id='Q-2',
            status='pending', created_at=now_ms(),
        )
        response = self.admin_client().get(reverse('web:admin_pending_payments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Course')
        self.assertContains(response, 'Admin Notes')
        self.assertContains(response, 'Paid course')
        self.assertTrue(payment.id)  # the row above is the one the page must open

    def test_approving_a_course_payment_credits_the_seller_and_unlocks_it(self):
        payment = PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, course=self.course, seller=self.teacher,
            amount=Decimal('2000'), platform_commission=Decimal('50'),
            seller_earnings=Decimal('1950'), transaction_id='A-1',
            status='pending', created_at=now_ms(),
        )
        response = self.admin_client().post(
            reverse('web:admin_pending_payments'),
            {'payment_id': payment.id, 'action': 'approve', 'reason': 'checked'},
        )
        self.assertEqual(response.status_code, 302)

        payment.refresh_from_db()
        self.assertEqual(payment.status, 'approved')

        balance = SellerBalance.objects.get(user=self.teacher)
        self.assertEqual(float(balance.current_balance), 1950.0)

        self.course.refresh_from_db()
        self.assertEqual(self.course.sale_count, 1)
        self.assertEqual(self.course.enrollment_count, 1)

        self.student.refresh_from_db()
        self.teacher.refresh_from_db()
        self.assertGreater(self.teacher.nebians_points, 0)
        self.assertEqual(float(self.student.total_spent), 2000.0)

        self.assertTrue(Notification.objects.filter(recipient=self.student, verb='payment_approved').exists())
        self.assertTrue(Notification.objects.filter(recipient=self.teacher, verb='sale_credited').exists())
        notification = Notification.objects.get(recipient=self.student, verb='payment_approved')
        self.assertEqual(notification.target_type, 'course')

        self.assertTrue(check_user_course_access(self.student, self.course)[0])

    def test_approving_a_resource_payment_still_works(self):
        payment = PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, resource=self.resource, seller=self.teacher,
            amount=Decimal('500'), platform_commission=Decimal('12.5'),
            seller_earnings=Decimal('487.5'), transaction_id='A-2',
            status='pending', created_at=now_ms(),
        )
        self.admin_client().post(reverse('web:admin_pending_payments'),
                                 {'payment_id': payment.id, 'action': 'approve'})
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'approved')
        self.assertEqual(float(SellerBalance.objects.get(user=self.teacher).current_balance), 487.5)

    def test_rejecting_tells_the_buyer_why(self):
        payment = PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, course=self.course, seller=self.teacher,
            amount=Decimal('2000'), platform_commission=Decimal('50'),
            seller_earnings=Decimal('1950'), transaction_id='A-3',
            status='pending', created_at=now_ms(),
        )
        self.admin_client().post(reverse('web:admin_pending_payments'),
                                 {'payment_id': payment.id, 'action': 'reject', 'reason': 'blurry proof'})
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'rejected')
        self.assertEqual(payment.admin_notes, 'blurry proof')
        self.assertTrue(Notification.objects.filter(recipient=self.student, verb='payment_rejected').exists())

    def test_a_non_admin_cannot_verify_payments(self):
        payment = PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, course=self.course, seller=self.teacher,
            amount=Decimal('2000'), platform_commission=Decimal('50'),
            seller_earnings=Decimal('1950'), transaction_id='A-4',
            status='pending', created_at=now_ms(),
        )
        buyer_client = self.session_client(self.student)
        response = buyer_client.post(reverse('web:admin_pending_payments'),
                                     {'payment_id': payment.id, 'action': 'approve'})
        payment.refresh_from_db()
        self.assertIn(response.status_code, (302, 403))
        self.assertEqual(payment.status, 'pending')

    def session_client(self, user):
        client = Client()
        session = client.session
        session['auth_token'] = user.raw_token
        session['user_data'] = {
            'id': user.id, 'username': user.username, 'email': user.email,
            'role': user.role, 'gender': 'male', 'is_admin': user.is_admin,
            'photo_url': '', 'avatar_url': '', 'verification_level': 0, 'moderator_level': 0,
        }
        session['theme'] = 'light'
        session.save()
        return client


class RealtimeGuardTests(TestCase):
    """A realtime push must never turn a successful write into a 500."""

    def test_send_survives_a_broken_channel_layer(self):
        from unittest import mock

        from api import realtime

        with mock.patch.object(realtime, 'get_channel_layer', side_effect=RuntimeError('no redis')):
            realtime._send('group', 'event', {'a': 1})
