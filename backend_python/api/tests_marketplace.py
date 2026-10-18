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
import re
import uuid
from decimal import Decimal
from pathlib import Path

from django.conf import settings

from django.core.cache import cache
from django.db import connection
from django.test import Client, RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from api.creator_pages import (
    BLOCK_FIELDS, PALETTES, TEMPLATES_BY_ID, apply_template, check_user_course_access,
    editor_schema, palette, template_list,
)
from api.marketplace import get_payment_config
from api.models import (
    CreatorCourse, CreatorPage, CreatorPost, Notification, PaymentVerification, Resource,
    SellerBalance, User, UserAuthToken,
)
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms
from web.templatetags.web_extras import video_embed


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

    def delete(self, user, path):
        return self.client.delete(path, HTTP_AUTHORIZATION=f'Bearer {user.raw_token}')

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

    def test_a_draft_may_still_be_priceless(self):
        """Half-written is a normal state for a course: the price rule only
        bites when the creator actually puts it on the shelf."""
        draft = self.post_json(self.teacher, '/api/marketplace/me/courses/',
                               {'title': 'Still thinking', 'is_free': False, 'status': 'draft'})
        self.assertEqual(draft.status_code, 201)
        course_id = draft.json()['course']['id']
        listing = self.patch_json(self.teacher, f'/api/marketplace/me/courses/{course_id}/',
                                  {'status': 'published'})
        self.assertEqual(listing.status_code, 400)

    def test_dropping_the_price_cannot_leave_a_paid_course_free(self):
        """PATCHing price alone used to leave a listed course priced at Rs. 0
        while still marked paid -- the shelf and the access check then
        disagreed about whether anyone had to pay for it."""
        course = self.make_course().json()['course']
        response = self.patch_json(self.teacher, f"/api/marketplace/me/courses/{course['id']}/",
                                   {'price': '0'})
        self.assertEqual(response.status_code, 400)

    def test_a_price_keeps_its_paisa_and_never_goes_scientific(self):
        """'%g' formatting dropped the cents past six significant digits and
        rendered a big price as 1.23457e+06."""
        cheap = self.make_course(title='Paisa', price='1499.50').json()['course']
        self.assertEqual(cheap['price'], '1499.50')
        dear = self.make_course(title='Big', price='999999.99').json()['course']
        self.assertEqual(dear['price'], '999999.99')
        self.assertEqual(self.make_course(title='Round', price='2500').json()['course']['price'], '2500')

    def test_a_sold_course_is_archived_not_deleted(self):
        """The purchase row points at the course with SET_NULL, so deleting a
        sold offering would strip the buyer's access and the seller's sale."""
        course = self.make_course(title='Sold out').json()['course']
        PaymentVerification.objects.create(
            id=str(uuid.uuid4()), buyer=self.student, seller=self.teacher,
            course_id=course['id'], amount=Decimal('2500'), status='approved',
            created_at=now_ms(),
        )
        response = self.delete(self.teacher, f"/api/marketplace/me/courses/{course['id']}/")
        self.assertEqual(response.status_code, 409)
        self.assertIn('archive', response.json()['error'].lower())
        self.assertTrue(CreatorCourse.objects.filter(pk=course['id']).exists())

        archived = self.patch_json(self.teacher, f"/api/marketplace/me/courses/{course['id']}/",
                                   {'status': 'archived'})
        self.assertEqual(archived.status_code, 200)
        has_access, reason, _ = check_user_course_access(self.student,
                                                        CreatorCourse.objects.get(pk=course['id']))
        self.assertTrue(has_access)
        self.assertEqual(reason, 'purchased')

    def test_an_unsold_course_can_be_deleted(self):
        course = self.make_course(title='Nobody bought this').json()['course']
        self.assertEqual(self.delete(self.teacher, f"/api/marketplace/me/courses/{course['id']}/").status_code, 200)
        self.assertFalse(CreatorCourse.objects.filter(pk=course['id']).exists())

    def test_a_double_submit_queues_one_payment_not_two(self):
        """Both taps see no open row and both insert; the database keeps one."""
        course = self.make_course(title='Raced').json()['course']
        for _ in range(2):
            response = self.post_json(self.student, f"/api/marketplace/courses/{course['id']}/purchase/",
                                      {'transaction_id': 'TXN-1'})
            self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(PaymentVerification.objects.filter(
            buyer=self.student, course_id=course['id'], status='pending').count(), 1)

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

    def test_the_owners_own_course_payload_carries_its_attachments(self):
        """An editor that cannot see the current attachments will save an empty
        list over them, so every studio round trip has to carry them."""
        note = Resource.objects.create(
            id=str(uuid.uuid4()), title='Attached note', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', added_at=now_ms(),
        )
        created = self.make_course(resource_ids=[note.id]).json()['course']
        self.assertEqual(created['resource_ids'], [note.id])

        course_id = created['id']
        self.assertEqual(
            self.get(self.teacher, f'/api/marketplace/me/courses/{course_id}/').json()['course']['resource_ids'],
            [note.id],
        )
        listed = self.get(self.teacher, '/api/marketplace/me/courses/').json()['courses']
        self.assertEqual(next(c for c in listed if c['id'] == course_id)['resource_ids'], [note.id])
        mine = self.get(self.teacher, '/api/marketplace/me/page/').json()['page']
        self.assertEqual(next(c for c in mine['courses'] if c['id'] == course_id)['resource_ids'], [note.id])

    def test_a_buyer_never_sees_which_notes_a_course_wraps(self):
        note = Resource.objects.create(
            id=str(uuid.uuid4()), title='Attached note', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', added_at=now_ms(),
        )
        course_id = self.make_course(resource_ids=[note.id]).json()['course']['id']
        payload = self.get(self.student, f'/api/marketplace/courses/{course_id}/').json()
        self.assertNotIn('resource_ids', payload)

    def test_editing_a_course_without_touching_its_notes_keeps_them(self):
        """`resource_ids` absent means "leave the attachments alone" -- only an
        explicit empty list detaches."""
        note = Resource.objects.create(
            id=str(uuid.uuid4()), title='Attached note', subject='Physics', type='Note',
            uploaded_by=self.teacher, approval_status='approved', added_at=now_ms(),
        )
        course_id = self.make_course(resource_ids=[note.id]).json()['course']['id']

        renamed = self.patch_json(self.teacher, f'/api/marketplace/me/courses/{course_id}/',
                                  {'title': 'Renamed'})
        self.assertEqual(renamed.status_code, 200)
        self.assertEqual(renamed.json()['course']['resource_ids'], [note.id])

        detached = self.patch_json(self.teacher, f'/api/marketplace/me/courses/{course_id}/',
                                   {'resource_ids': []})
        self.assertEqual(detached.json()['course']['resource_ids'], [])

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
        response = self.client.get('/app/library/?tab=marketplace')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('mkt-shelf', html)
        for tab in ('?tab=digital', '?tab=marketplace', '?tab=categories'):
            self.assertIn(tab, html)
        self.assertLess(html.index('?tab=marketplace'), html.index('?tab=categories'))

    def test_the_directory_lists_published_pages(self):
        self.make_published_page(self.teacher, slug='t-web', display_name='Web Teacher')
        response = self.client.get('/app/marketplace/')
        self.assertContains(response, 'Web Teacher')
        self.assertContains(response, 'mkt-shelf-focus' if False else 'creator-grid')

    def test_the_studio_is_for_eligible_accounts_only(self):
        self.assertEqual(self.session_client(self.teacher).get('/app/marketplace/studio/').status_code, 200)
        self.assertEqual(self.session_client(self.student).get('/app/marketplace/studio/').status_code, 403)
        self.assertEqual(self.client.get('/app/marketplace/studio/').status_code, 302)

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
        html = self.client.get('/app/marketplace/t-render/').content.decode()
        self.assertIn('Hero headline', html)
        self.assertIn('When?', html)
        self.assertIn('Fifteen years of NEB physics.', html)
        self.assertLess(html.index('Hero headline'), html.index('When?'))
        self.assertLess(html.index('When?'), html.index('Fifteen years of NEB physics.'))
        self.assertIn('#1F6F5C', html)

    def test_the_hero_choice_never_lands_on_the_page_container(self):
        """`mkt-hero-art` is the art layer, so the page cannot also wear it.

        The modifier used to be `mkt-hero-{{ style.hero }}`, which on the default
        hero gave the whole page `position: absolute; inset: 0; opacity: 0.5`
        from the art layer's own rule.
        """
        self.make_published_page(self.teacher, slug='t-hero')
        html = self.client.get('/app/marketplace/t-hero/').content.decode()
        container = html[html.index('class="mkt-page'):]
        container = container[:container.index('>')]
        self.assertIn('mkt-hero-mode-art', container)
        self.assertNotIn('mkt-hero-art', container)

    def test_the_verified_badge_and_the_contact_rows_follow_the_creators_choice(self):
        self.make_published_page(self.teacher, slug='t-flags', blocks=[
            {'type': 'hero', 'title': 'Hero'},
            {'type': 'contact', 'title': 'Get in touch'},
        ], contact_email='sabina@example.com', style={
            'hero': 'art', 'show_verified': False, 'show_contact': False, 'show_stats': True,
        })
        CreatorPage.objects.filter(slug='t-flags').update(verified=True, view_count=1200)
        html = self.client.get('/app/marketplace/t-flags/').content.decode()
        self.assertNotIn('mkt-verified', html)
        self.assertNotIn('sabina@example.com', html)
        # show_stats on: the platform numbers sit under the name
        self.assertIn('mkt-hero-stats', html)
        self.assertIn('followers', html)

    def test_the_badge_and_the_contact_rows_are_on_by_default(self):
        self.make_published_page(self.teacher, slug='t-flags-on', blocks=[
            {'type': 'hero', 'title': 'Hero'},
            {'type': 'contact', 'title': 'Get in touch'},
        ], contact_email='sabina@example.com')
        CreatorPage.objects.filter(slug='t-flags-on').update(verified=True)
        html = self.client.get('/app/marketplace/t-flags-on/').content.decode()
        self.assertIn('mkt-verified', html)
        self.assertIn('sabina@example.com', html)
        self.assertNotIn('mkt-hero-stats', html)

    def test_a_stats_section_keeps_its_own_heading(self):
        self.make_published_page(self.teacher, slug='t-stats', blocks=[
            {'type': 'stats', 'title': 'By the numbers',
             'items': [{'label': 'Students', 'value': '400'}]},
        ])
        html = self.client.get('/app/marketplace/t-stats/').content.decode()
        self.assertIn('By the numbers', html)
        self.assertIn('400', html)

    def test_the_price_setter_is_the_shared_component(self):
        html = self.session_client(self.teacher).get('/app/upload/').content.decode()
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
        page_html = client.get(f'/app/marketplace/course/{course.id}/').content.decode()
        self.assertIn('Submit payment', page_html)

        response = client.post(f'/app/marketplace/course/{course.id}/', {'transaction_id': 'WEB-1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Awaiting verification', response.content.decode())
        self.assertTrue(PaymentVerification.objects.filter(buyer=self.student, course=course, status='pending').exists())

        payment = PaymentVerification.objects.get(buyer=self.student, course=course)
        payment.status = 'approved'
        payment.save()
        self.assertIn('Unlocked', client.get(f'/app/marketplace/course/{course.id}/').content.decode())

    def test_the_owner_cannot_buy_their_own_course(self):
        self.make_published_page(self.teacher, slug='t-own')
        page = CreatorPage.objects.get(slug='t-own')
        course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Mine', slug='mine',
            is_free=False, price='100', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )
        client = self.session_client(self.teacher)
        client.post(f'/app/marketplace/course/{course.id}/', {'transaction_id': 'X'})
        self.assertFalse(PaymentVerification.objects.filter(buyer=self.teacher, course=course).exists())

    def selected_option(self, html, attr, value):
        """The value the studio's `<select ... {attr}="{value}">` opens on."""
        start = html.index(f'{attr}="{value}"')
        block = html[start:html.index('</select>', start)]
        match = re.search(r'<option value="([^"]+)"\s+selected', block)
        return match.group(1) if match else None

    def hidden_style(self, html, key):
        """The value behind a segmented or swatch control.

        Palette, scheme and hero are picked by eye rather than from a list, so
        what gets saved lives in a hidden input the buttons write into.
        """
        match = re.search(
            r'<input type="hidden" data-mkt-style="' + key + r'" value="([^"]*)"', html)
        return match.group(1) if match else None

    def pressed_choice(self, html, key):
        """The segment drawn as chosen, which has to agree with the hidden input
        or the studio opens showing one thing and saves another."""
        for match in re.finditer(
                r'data-mkt-choice="' + key + r'" data-value="([^"]+)"[^>]*aria-checked="(\w+)"', html):
            if match.group(2) == 'true':
                return match.group(1)
        return None

    def test_the_look_tab_opens_on_what_the_creator_saved(self):
        """The Look tab used to render against an undefined `style`.

        Every `{% if style.X %}` was false, so the tab showed the defaults, and
        the first save sent those defaults back -- `style` is replaced wholesale,
        so a creator who touched the Content tab lost their whole look.
        """
        self.make_published_page(self.teacher, slug='t-look', style={
            'hero': 'plain', 'radius': 'sharp', 'density': 'compact',
            'gallery_columns': 4, 'show_stats': True, 'show_verified': False,
        })
        html = self.session_client(self.teacher).get('/app/marketplace/studio/').content.decode()
        self.assertEqual(self.hidden_style(html, 'hero'), 'plain')
        self.assertEqual(self.pressed_choice(html, 'hero'), 'plain')
        self.assertEqual(self.selected_option(html, 'data-mkt-style', 'radius'), 'sharp')
        self.assertEqual(self.selected_option(html, 'data-mkt-style', 'density'), 'compact')
        self.assertEqual(self.selected_option(html, 'data-mkt-style', 'gallery_columns'), '4')
        stats = html[html.index('data-mkt-style-bool="show_stats"'):]
        self.assertIn('checked', stats[:stats.index('>')])
        verified = html[html.index('data-mkt-style-bool="show_verified"'):]
        self.assertNotIn('checked', verified[:verified.index('>')])

    def test_the_studio_opens_on_a_gallery_not_a_blank_canvas(self):
        """A first page should be a choice between finished ones.

        Twenty-five section names and an empty list is how a creator abandons a
        storefront half-built, so the studio leads with templates -- each card
        painted in the template's own resolved colours, because the colours are
        the thing being chosen.
        """
        client = self.session_client(self.teacher)
        html = client.get('/app/marketplace/studio/').content.decode()
        entries = template_list('tutor')
        self.assertGreaterEqual(len(entries), 5, 'a gallery of one is not a gallery')
        for entry in entries:
            self.assertIn(f'data-mkt-template="{entry["id"]}"', html)
            self.assertIn(f'--t-accent: {entry["colors"]["accent"]}', html)
        self.assertIn('data-mkt-preview-frame', html)
        self.assertIn('data-mkt-preview-size="phone"', html)

    def test_every_section_can_be_reached_from_the_picker(self):
        """A section the server knows about and the picker does not is a section
        no creator can ever add."""
        html = self.session_client(self.teacher).get('/app/marketplace/studio/').content.decode()
        for entry in editor_schema()['blocks']:
            self.assertIn(f'data-mkt-add-block="{entry["type"]}"', html)

    def test_a_template_applied_from_the_studio_takes(self):
        self.make_published_page(self.teacher, slug='t-apply')
        client = self.session_client(self.teacher)
        response = self.ajax(client, 'marketplace_template_apply',
                             {'template': template_list('tutor')[0]['id'], 'mode': 'page'})
        self.assertEqual(response.status_code, 200, response.content)
        page = CreatorPage.objects.get(slug='t-apply')
        template = TEMPLATES_BY_ID[template_list('tutor')[0]['id']]
        self.assertEqual([b['type'] for b in page.blocks], [b['type'] for b in template['blocks']])
        self.assertEqual(page.style['palette'], template['style']['palette'])

    def test_a_template_cannot_be_applied_to_somebody_elses_page(self):
        self.make_published_page(self.teacher, slug='t-mine')
        response = self.ajax(self.session_client(self.student), 'marketplace_template_apply',
                             {'template': template_list()[0]['id']})
        self.assertIn(response.status_code, (403, 404))
        self.assertEqual(CreatorPage.objects.get(slug='t-mine').blocks[0]['type'], 'hero')

    def test_a_sections_own_look_survives_a_studio_save(self):
        """The per-section controls write into `settings`, which the sanitizer
        keeps only when it differs from the default -- so a page that never
        touches them stays exactly as small on the wire as it was."""
        self.make_published_page(self.teacher, slug='t-settings')
        response = self.ajax(self.session_client(self.teacher), 'marketplace_page_save', {
            'blocks': [
                {'type': 'hero', 'title': 'Loud', 'settings': {'tone': 'accent', 'align': 'center'}},
                {'type': 'about', 'title': 'Quiet', 'settings': {'tone': 'plain', 'align': 'start'}},
            ],
        })
        self.assertEqual(response.status_code, 200, response.content)
        blocks = CreatorPage.objects.get(slug='t-settings').blocks
        self.assertEqual(blocks[0]['settings'], {'align': 'center', 'tone': 'accent'})
        self.assertNotIn('settings', blocks[1])

    def test_a_course_on_an_unpublished_page_is_not_reachable(self):
        """Unpublishing has to take the offerings with it.

        The storefront 404s for a stranger, but the course page did not, so every
        course link -- QR checkout included -- stayed live after the creator
        pulled the page down.
        """
        self.make_published_page(self.teacher, slug='t-hidden')
        page = CreatorPage.objects.get(slug='t-hidden')
        course = CreatorCourse.objects.create(
            id=str(uuid.uuid4()), page=page, title='Hidden Course', slug='hidden',
            is_free=False, price='500', status='published',
            created_at=now_ms(), updated_at=now_ms(),
        )
        student = self.session_client(self.student)
        self.assertEqual(student.get(f'/app/marketplace/course/{course.id}/').status_code, 200)

        CreatorPage.objects.filter(id=page.id).update(published=False)
        self.assertEqual(student.get(f'/app/marketplace/course/{course.id}/').status_code, 404)
        self.assertEqual(self.client.get(f'/app/marketplace/course/{course.id}/').status_code, 404)
        # its owner still needs the preview, and an admin still needs to moderate it
        self.assertEqual(self.session_client(self.teacher).get(f'/app/marketplace/course/{course.id}/').status_code, 200)
        self.assertEqual(self.session_client(self.admin).get(f'/app/marketplace/course/{course.id}/').status_code, 200)

    def test_an_empty_section_does_not_render_a_bare_heading(self):
        """A section a creator added but never filled stays invisible.

        Otherwise the page reads as broken: a "Gallery" heading with nothing
        under it, then "What students say" with nothing under that.
        """
        self.make_published_page(self.teacher, slug='t-empty', blocks=[
            {'type': 'hero', 'title': 'Hero'},
            {'type': 'gallery', 'title': 'My gallery', 'images': []},
            {'type': 'testimonials', 'title': 'What students say', 'items': []},
            {'type': 'faq', 'title': 'Common queries', 'items': []},
            {'type': 'showcase', 'title': 'My work', 'items': []},
        ])
        html = self.client.get('/app/marketplace/t-empty/').content.decode()
        for heading in ('My gallery', 'What students say', 'Common queries', 'My work'):
            self.assertNotIn(heading, html)

        # ...and the moment one has something in it, it comes back
        self.make_published_page(self.teacher, slug='t-empty', blocks=[
            {'type': 'hero', 'title': 'Hero'},
            {'type': 'gallery', 'title': 'My gallery',
             'images': ['https://cdn.example.com/1.jpg']},
        ])
        html = self.client.get('/app/marketplace/t-empty/').content.decode()
        self.assertIn('My gallery', html)

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
        html = self.session_client(self.teacher).get('/app/marketplace/studio/').content.decode()
        self.assertIn('Sold Course', html)
        self.assertIn('t_student', html)


class CreatorThemeTests(MarketplaceTestBase):
    """Templates, palettes and the per-section overrides.

    These exist because the theme layer is the one part of the marketplace with
    no obvious failure mode: a page with a broken palette still returns 200, it
    just looks wrong, and nobody notices until a creator does.
    """

    def test_every_starter_template_renders_in_every_scheme(self):
        """Ten templates x two schemes x four card styles, all 200.

        The real value here is the template *engine*: a section type that a
        starter template uses but `marketplace_page.html` has no branch for
        renders as nothing at all, silently, and this catches it by size.
        """
        for index, template_id in enumerate(TEMPLATES_BY_ID):
            user = self.make_user(f't_tpl{index}', role=User.ROLE_TEACHER)
            page = CreatorPage.objects.create(
                id=f'cp-tpl-{index}', user=user, slug=f'tpl-{template_id}',
                display_name='Sunrise Tuition', kind='tutor', published=True,
                subjects='Physics,Maths', tagline='Board physics, small batches',
                about='Ten years of it.', contact_email='hello@example.com',
                created_at=now_ms(), updated_at=now_ms())
            page, error = apply_template(page, template_id, mode='page')
            self.assertIsNone(error, template_id)
            self.assertTrue(page.blocks, f'{template_id} has no sections')
            page.save()

            url = reverse('web:marketplace_creator', kwargs={'slug': page.slug})
            for scheme in ('light', 'dark'):
                for card in ('elevated', 'outlined', 'flat', 'glass'):
                    page.style = dict(page.style, scheme=scheme, card=card)
                    page.save(update_fields=['style'])
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200,
                                     f'{template_id} / {scheme} / {card}')
            html = response.content.decode()
            self.assertIn('--creator-accent', html)
            self.assertIn('mkt-card-glass', html)

    def test_every_section_type_has_somewhere_to_render(self):
        """No block type may exist in the schema without a branch on the page.

        A type the server accepts and the page ignores is the worst kind of
        bug here: the studio saves it, tells the creator it worked, and the
        section is simply absent when they go and look.
        """
        markup = (Path(settings.BASE_DIR) / 'web' / 'templates' / 'web'
                  / 'marketplace_page.html').read_text()
        rendered = set(re.findall(r"block\.type == '([a-z]+)'", markup))
        self.assertEqual(sorted(set(BLOCK_FIELDS) - rendered), [])

    def test_a_template_can_be_applied_to_the_look_alone(self):
        """`theme` mode repaints without touching a word the creator wrote."""
        self.make_published_page(self.teacher, slug='t-keep')
        page = CreatorPage.objects.get(user=self.teacher)
        page.blocks = [{'id': 'about', 'type': 'about', 'title': 'My own heading',
                        'body': 'My own words', 'enabled': True}]
        page.save(update_fields=['blocks'])

        response = self.post_json(self.teacher, '/api/marketplace/me/page/template/',
                                  {'template': 'night-editorial', 'mode': 'theme'})
        self.assertEqual(response.status_code, 200, response.content)
        page.refresh_from_db()
        self.assertEqual(page.style['scheme'], 'dark')
        self.assertEqual(page.blocks[0]['body'], 'My own words')

        # ...and `sections` mode is the other half: new sections, same look.
        before = dict(page.style)
        response = self.post_json(self.teacher, '/api/marketplace/me/page/template/',
                                  {'template': 'link-hub', 'mode': 'sections'})
        self.assertEqual(response.status_code, 200, response.content)
        page.refresh_from_db()
        self.assertEqual(page.style, before)
        self.assertNotEqual(page.blocks[0].get('body'), 'My own words')

    def test_an_unknown_template_is_refused(self):
        response = self.post_json(self.teacher, '/api/marketplace/me/page/template/',
                                  {'template': 'no-such-template'})
        self.assertEqual(response.status_code, 400)

    def test_the_resolved_palette_travels_with_the_page(self):
        """The app reads hex, not palette names.

        If Android carried its own copy of the palette table, the day somebody
        nudged one hex in Python would be the day the same page looked
        different on a phone.
        """
        # A blank accent means "follow the palette" -- the studio's reset.
        self.make_published_page(self.teacher, slug='t-theme', accent_hex='',
                                 style={'palette': 'ink', 'scheme': 'dark'})
        response = self.get(self.teacher, '/api/marketplace/me/page/')
        theme = response.json()['page']['theme']
        self.assertEqual(theme['palette'], 'ink')
        self.assertEqual(theme['colors']['bg'], '#000000')
        # Ink's accent inverts in the dark ramp, or it would be invisible.
        self.assertEqual(theme['colors']['accent'], '#FFFFFF')
        for key in ('bg', 'surface', 'ink', 'muted', 'line', 'soft', 'accent', 'on_accent'):
            self.assertRegex(theme['colors'][key], r'^#[0-9A-Fa-f]{6}$', key)

    def test_a_custom_accent_overrides_the_palettes_own(self):
        self.make_published_page(self.teacher, slug='t-accent',
                                 accent_hex='#AA3311', style={'palette': 'teal'})
        theme = self.get(self.teacher, '/api/marketplace/me/page/').json()['page']['theme']
        self.assertEqual(theme['colors']['accent'], '#AA3311')
        self.assertEqual(theme['colors']['soft'], palette('teal')['soft'])

    def test_a_nonsense_look_falls_back_instead_of_failing(self):
        """A page saved by an app that has never heard of `pattern` still opens."""
        self.make_published_page(self.teacher, slug='t-junk', style={
            'palette': 'chartreuse', 'scheme': 'sepia', 'card': 'hologram',
            'gallery_columns': 99, 'pattern': None,
        })
        page = CreatorPage.objects.get(user=self.teacher)
        self.assertEqual(page.style['palette'], 'indigo')
        self.assertEqual(page.style['scheme'], 'light')
        self.assertEqual(page.style['card'], 'elevated')
        self.assertEqual(page.style['gallery_columns'], 4)
        self.assertEqual(page.style['pattern'], 'none')

    def test_two_sections_of_one_type_get_distinct_anchors(self):
        """Ids are anchors, and a duplicate anchor makes the first unreachable."""
        self.make_published_page(self.teacher, slug='t-ids', blocks=[
            {'type': 'courses', 'title': 'Morning batch'},
            {'type': 'courses', 'title': 'Evening batch'},
            {'type': 'about', 'id': 'has spaces and is too long to be an anchor at all'},
        ])
        page = CreatorPage.objects.get(user=self.teacher)
        ids = [block['id'] for block in page.blocks]
        self.assertEqual(len(set(ids)), 3, ids)
        for block_id in ids:
            self.assertRegex(block_id, r'^[A-Za-z0-9_-]+$')

    def test_a_hero_button_may_point_at_another_section(self):
        """`#pricing` has to survive the URL allowlist; `javascript:` must not."""
        self.make_published_page(self.teacher, slug='t-anchor', blocks=[
            {'type': 'hero', 'cta_label': 'See fees', 'cta_url': '#pricing'},
            {'type': 'cta', 'cta_label': 'Bad', 'cta_url': 'javascript:alert(1)'},
            {'type': 'banner', 'cta_label': 'Worse', 'cta_url': '#not a fragment'},
        ])
        blocks = CreatorPage.objects.get(user=self.teacher).blocks
        self.assertEqual(blocks[0]['cta_url'], '#pricing')
        self.assertEqual(blocks[1]['cta_url'], '')
        self.assertEqual(blocks[2]['cta_url'], '')

    def test_a_sections_own_settings_reach_the_markup(self):
        self.make_published_page(self.teacher, slug='t-settings', blocks=[
            {'type': 'hero', 'title': 'Hi'},
            {'type': 'quote', 'title': 'Teach the child, not the syllabus.',
             'settings': {'align': 'center', 'tone': 'accent', 'width': 'full', 'columns': 2}},
        ])
        html = self.client.get(
            reverse('web:marketplace_creator', kwargs={'slug': 't-settings'})).content.decode()
        for css_class in ('mkt-align-center', 'mkt-tone-accent', 'mkt-bwidth-full', 'mkt-cols-2'):
            self.assertIn(css_class, html)

    def test_untouched_settings_are_not_stored(self):
        """Defaults do not travel. A page that never used these stays small."""
        self.make_published_page(self.teacher, slug='t-default-settings', blocks=[
            {'type': 'about', 'settings': {'align': 'start', 'tone': 'plain',
                                           'width': 'standard', 'columns': 0}},
        ])
        self.assertNotIn('settings', CreatorPage.objects.get(user=self.teacher).blocks[0])

    def test_only_trusted_hosts_become_an_iframe(self):
        """A pasted video link is framed; anything else is only ever a link."""
        self.assertEqual(video_embed('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                         'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ')
        self.assertEqual(video_embed('https://youtu.be/dQw4w9WgXcQ'),
                         'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ')
        self.assertEqual(video_embed('https://vimeo.com/123456789'),
                         'https://player.vimeo.com/video/123456789')
        self.assertEqual(video_embed('https://evil.example.com/player'), '')

        self.make_published_page(self.teacher, slug='t-video', blocks=[
            {'type': 'video', 'title': 'Intro', 'media_url': 'https://evil.example.com/p'},
        ])
        html = self.client.get(
            reverse('web:marketplace_creator', kwargs={'slug': 't-video'})).content.decode()
        self.assertNotIn('<iframe', html)
        self.assertIn('evil.example.com', html)

    def test_the_editor_schema_describes_every_section(self):
        """Both studios draw their controls from this, so it has to be complete."""
        response = self.client.get('/api/marketplace/editor-schema/')
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertEqual(sorted(b['type'] for b in schema['blocks']), sorted(BLOCK_FIELDS))
        grouped = {t for group in schema['groups'] for t in group['types']}
        self.assertEqual(sorted(grouped), sorted(BLOCK_FIELDS))
        for block in schema['blocks']:
            self.assertTrue(block['hint'], block['type'])
        self.assertEqual(len(schema['theme']['palettes']), len(PALETTES))

    def test_the_gallery_is_filtered_by_who_is_asking(self):
        response = self.client.get('/api/marketplace/templates/?kind=institute')
        self.assertEqual(response.status_code, 200)
        templates = response.json()['templates']
        self.assertTrue(templates)
        for template in templates:
            self.assertIn('institute', template['kinds'])
            self.assertTrue(template['summary'])
            self.assertTrue(template['best_for'])


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
