import time
import uuid

from django.test import TestCase

from api.models import Resource, ResourceComment


def _now_ms():
    return int(time.time() * 1000)


class ReaderDeletedAuthorTests(TestCase):
    """The reader must render even when the rows it points at outlived their users."""

    def _resource(self, **overrides):
        values = {
            'id': str(uuid.uuid4()),
            'title': 'Orphaned resource',
            'subject': 'Physics',
            'grade_level': '12',
            'type': 'PDF',
            'approval_status': 'approved',
            'is_lead': True,
            'uploaded_by': None,
            'added_at': _now_ms(),
        }
        values.update(overrides)
        return Resource.objects.create(**values)

    def test_reader_renders_with_deleted_uploader_and_comment_author(self):
        resource = self._resource()
        ResourceComment.objects.create(
            id=str(uuid.uuid4()),
            resource=resource,
            user=None,
            content='Comment left by an account that no longer exists',
            created_at=_now_ms(),
        )

        response = self.client.get(f'/app/reader/{resource.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Deleted user')

    def test_reader_renders_with_deleted_author_on_nested_reply(self):
        resource = self._resource()
        parent = ResourceComment.objects.create(
            id=str(uuid.uuid4()),
            resource=resource,
            user=None,
            content='Parent comment',
            reply_count=1,
            created_at=_now_ms(),
        )
        ResourceComment.objects.create(
            id=str(uuid.uuid4()),
            resource=resource,
            user=None,
            parent_comment=parent,
            content='Nested reply',
            created_at=_now_ms(),
        )

        response = self.client.get(f'/app/reader/{resource.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Deleted user')
