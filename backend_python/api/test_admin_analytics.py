from django.test import TestCase, RequestFactory
from api.models import User, PageView, Post, Resource
from web.views_admin import admin_analytics

class DummyAdminUser:
    is_authenticated = True
    is_staff = True
    is_active = True
    username = 'admin_test'

class AdminAnalyticsTest(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.db_user = User.objects.create(id='u_admin', username='admin_test', created_at=1780000000000)

    def test_admin_analytics_view(self):
        request = self.rf.get('/admin/analytics/')
        request.user = DummyAdminUser()

        # Add test records
        PageView.objects.create(session_key='s1', created_at=1780000000000, source='web')
        Post.objects.create(id='p1', user=self.db_user, title='Test Post', created_at=1780000000000)
        Resource.objects.create(id='r1', title='Test Res', added_at=1780000000000)

        response = admin_analytics(request)
        self.assertEqual(response.status_code, 200)
