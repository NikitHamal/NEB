import time
from django.test import TestCase, override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

from api.models import User, Notification
from api.notifications import (
    delete_notifications_for_target,
    delete_notifications_for_actor_and_target,
)


class NotificationPerformanceTests(TestCase):
    def setUp(self):
        self.actor = User.objects.create(
            id="actor_user_1",
            username="actor_1",
            email="actor1@test.com",
            is_bot=False,
        )

    def test_delete_notifications_for_target_query_count(self):
        num_recipients = 20
        recipients = []
        for i in range(num_recipients):
            u = User.objects.create(
                id=f"recipient_user_{i}",
                username=f"recipient_{i}",
                email=f"recipient_{i}@test.com",
                is_bot=False,
                unread_notification_count=1,
            )
            recipients.append(u)
            Notification.objects.create(
                id=f"notif_target_{i}",
                recipient_id=u.id,
                actor_id=self.actor.id,
                verb="reply",
                target_type="post",
                target_id="post_target_123",
                is_read=False,
                created_at=1000,
            )

        start_time = time.perf_counter()
        with CaptureQueriesContext(connection) as queries:
            delete_notifications_for_target("post", "post_target_123")
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        print(f"\n[BENCHMARK] delete_notifications_for_target with {num_recipients} recipients:")
        print(f"  Query Count: {len(queries)}")
        print(f"  Elapsed Time: {elapsed_ms:.2f} ms")

        # Verify correctness
        self.assertEqual(Notification.objects.filter(target_type="post", target_id="post_target_123").count(), 0)
        for u in recipients:
            u.refresh_from_db()
            self.assertEqual(u.unread_notification_count, 0)

    def test_delete_notifications_for_actor_and_target_query_count(self):
        num_recipients = 20
        recipients = []
        for i in range(num_recipients):
            u = User.objects.create(
                id=f"actor_target_recipient_{i}",
                username=f"actor_rec_{i}",
                email=f"actor_rec_{i}@test.com",
                is_bot=False,
                unread_notification_count=1,
            )
            recipients.append(u)
            Notification.objects.create(
                id=f"notif_actor_target_{i}",
                recipient_id=u.id,
                actor_id=self.actor.id,
                verb="like_post",
                target_type="post",
                target_id="post_actor_target_456",
                is_read=False,
                created_at=1000,
            )

        start_time = time.perf_counter()
        with CaptureQueriesContext(connection) as queries:
            delete_notifications_for_actor_and_target(self.actor.id, "like_post", "post", "post_actor_target_456")
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        print(f"\n[BENCHMARK] delete_notifications_for_actor_and_target with {num_recipients} recipients:")
        print(f"  Query Count: {len(queries)}")
        print(f"  Elapsed Time: {elapsed_ms:.2f} ms")

        # Verify correctness
        self.assertEqual(Notification.objects.filter(actor_id=self.actor.id, verb="like_post", target_type="post", target_id="post_actor_target_456").count(), 0)
        for u in recipients:
            u.refresh_from_db()
            self.assertEqual(u.unread_notification_count, 0)
