"""The push-notification audience filter is `User.objects.filter(class_level__iexact=...)`,
so the option's `value` has to be the exact string stored in `users.class`.

It was not: the dropdown read "Class 10 / SEE" but submitted `Class 10`, and
`Bachelor` / `Master` instead of `Bachelors` / `Masters`. Nobody in the database
holds those values, so picking a class matched zero users and the broadcast
went out to nobody while the page still reported a healthy-looking count.

The values here mirror `admin_panel/user_detail.html`, which edits the same
field, so both screens agree on the one vocabulary.
"""
import re
from pathlib import Path

from django.core.cache import cache
from django.test import Client, TestCase

from api.models import User
from api.security import issue_auth_token

TEMPLATES = Path(__file__).resolve().parent.parent / 'web' / 'templates'
PUSH_PAGE = TEMPLATES / 'admin_panel' / 'push_notifications.html'
USER_DETAIL = TEMPLATES / 'admin_panel' / 'user_detail.html'

OPTION_RE = re.compile(r'<option value="([^"]*)"')
SELECT_RE = re.compile(r'<select[^>]*id="class_level".*?</select>', re.DOTALL)


def _class_option_values(path):
    """Only the class-level select, not the pradesh/gender selects on the same page."""
    block = SELECT_RE.search(path.read_text(encoding='utf-8'))
    assert block, f'no class_level select in {path.name}'
    return set(OPTION_RE.findall(block.group(0)))


def _class_option_labels(path):
    block = SELECT_RE.search(path.read_text(encoding='utf-8'))
    assert block, f'no class_level select in {path.name}'
    return dict(re.findall(r'<option value="([^"]*)"[^>]*>([^<]*)</option>', block.group(0)))


def _user(username, **kwargs):
    return User.objects.create(
        id=username, username=username, email=f'{username}@example.com',
        created_at=1, email_verified=True, role='student', **kwargs,
    )


class PushFilterOptionTests(TestCase):
    def test_class_options_are_values_the_profile_actually_stores(self):
        canonical = _class_option_values(USER_DETAIL) - {''}
        offered = _class_option_values(PUSH_PAGE) - {''}

        self.assertTrue(offered, 'no class options found — did the markup change?')
        self.assertEqual(
            offered - canonical, set(),
            'push filter offers values no profile can hold, so they match nobody',
        )

    def test_the_see_option_is_labelled_and_submitted_alike(self):
        labels = _class_option_labels(PUSH_PAGE)
        self.assertIn('Class 10 / SEE', labels)
        self.assertEqual(labels['Class 10 / SEE'], 'Class 10 / SEE')

    def test_no_singular_bachelor_or_master(self):
        offered = _class_option_values(PUSH_PAGE)
        self.assertNotIn('Bachelor', offered)
        self.assertNotIn('Master', offered)
        self.assertIn('Bachelors', offered)
        self.assertIn('Masters', offered)


class PushFilterAudienceTests(TestCase):
    def setUp(self):
        cache.clear()
        self.see_1 = _user('see_one', class_level='Class 10 / SEE')
        self.see_2 = _user('see_two', class_level='Class 10 / SEE')
        self.eleven = _user('eleven', class_level='11')
        _user('no_class')
        self.admin = _user('boss', is_admin=True)

        self.client = Client()
        session = self.client.session
        session['auth_token'] = issue_auth_token(self.admin)
        session.save()

    def _count(self, **params):
        response = self.client.get('/admin/push-notifications/', {'count_only': '1', **params})
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()['matching_users']

    def test_requires_admin(self):
        self.assertEqual(Client().get('/admin/push-notifications/?count_only=1').status_code, 302)

    def test_class_10_see_reaches_exactly_those_users(self):
        self.assertEqual(self._count(class_level='Class 10 / SEE'), 2)

    def test_bare_11_and_12_are_targetable(self):
        self.assertEqual(self._count(class_level='11'), 1)

    def test_all_classes_counts_everyone(self):
        self.assertEqual(self._count(), 5)

    def test_the_old_value_matches_nobody(self):
        self.assertEqual(self._count(class_level='Class 10'), 0)
