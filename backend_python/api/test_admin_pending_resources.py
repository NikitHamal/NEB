from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User as DjangoUser
from api.models import Resource
from web.views_admin import admin_pending_resources


class AdminPendingResourcesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = DjangoUser.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='password',
            is_staff=True
        )

        # Group 1 (3 resources)
        Resource.objects.create(
            id='res_g1_1',
            title='Group 1 Lead',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=True,
            added_at=1000
        )
        Resource.objects.create(
            id='res_g1_2',
            title='Group 1 Part 2',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=False,
            added_at=1001
        )
        Resource.objects.create(
            id='res_g1_3',
            title='Group 1 Part 3',
            subject='Physics',
            grade_level='12',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_1',
            is_lead=False,
            added_at=1002
        )

        # Group 2 (2 resources)
        Resource.objects.create(
            id='res_g2_1',
            title='Group 2 Lead',
            subject='Chemistry',
            grade_level='11',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_2',
            is_lead=True,
            added_at=2000
        )
        Resource.objects.create(
            id='res_g2_2',
            title='Group 2 Part 2',
            subject='Chemistry',
            grade_level='11',
            type='PDF',
            approval_status='pending',
            upload_group_id='group_2',
            is_lead=False,
            added_at=2001
        )

        # Single Resource
        Resource.objects.create(
            id='res_single_1',
            title='Single Resource',
            subject='Math',
            grade_level='10',
            type='PDF',
            approval_status='pending',
            upload_group_id='',
            is_lead=True,
            added_at=3000
        )

    def test_admin_pending_resources_query_count(self):
        request = self.factory.get('/admin/resources/pending/')
        request.user = self.staff_user

        # Verify that views_admin.admin_pending_resources executes exactly 1 query
        with self.assertNumQueries(1):
            response = admin_pending_resources(request)

        self.assertEqual(response.status_code, 200)

    def test_admin_pending_resources_via_client(self):
        self.client.force_login(self.staff_user)

        response = self.client.get('/admin/resources/pending/')

        self.assertEqual(response.status_code, 200)
        pending_resources = response.context['pending_resources']
        self.assertEqual(len(pending_resources), 3)

        # Check group 1
        g1 = pending_resources[0]
        self.assertEqual(g1['title'], 'Group 1 Lead')
        self.assertEqual(len(g1['group_files']), 3)

        # Check group 2
        g2 = pending_resources[1]
        self.assertEqual(g2['title'], 'Group 2 Lead')
        self.assertEqual(len(g2['group_files']), 2)

        # Check single resource
        single = pending_resources[2]
        self.assertEqual(single['title'], 'Single Resource')
        self.assertEqual(len(single['group_files']), 1)
