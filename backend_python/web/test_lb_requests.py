from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api.models import User


class LeaderboardRequestsScreens(TestCase):
    def setUp(self):
        cache.clear()
        for i, n in enumerate(['ann', 'bo', 'cy', 'di']):
            User.objects.create(id=f'u{n}', username=n, display_name=n.title(), email=f'{n}@x.com',
                                email_verified=True, contribution_score=400 - i * 50)

    def test_leaderboard_has_podium_and_ranked_rows_without_emoji_or_live_badge(self):
        html = self.client.get(reverse('web:leaderboard')).content.decode()
        self.assertEqual(html.count('lb-pod-link'), 3)
        self.assertIn('lb-row', html)
        self.assertIn('lb-meter', html)
        self.assertNotIn('LIVE', html)

    def test_requests_page_renders_filters(self):
        html = self.client.get(reverse('web:resource_requests')).content.decode()
        self.assertIn('rq-seg', html)
        self.assertIn('rq-empty', html)
