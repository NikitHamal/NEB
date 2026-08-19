import uuid
from django.test import TestCase
from api.models import User, Post, Poll, PollOption
from api.services import create_post


class PollCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=str(uuid.uuid4()),
            username='poll_tester',
            email='poll_tester@example.com',
            email_verified=True,
        )

    def test_create_post_with_dict_poll_options(self):
        poll_data = {
            'question': 'Which subject do you prefer?',
            'poll_type': 'voting',
            'allow_multiple': False,
            'explanation': 'Choose your favorite subject',
            'options': [
                {'text': 'Physics', 'is_correct': False},
                {'text': 'Chemistry', 'is_correct': True},
                {'text': 'Biology', 'is_correct': False},
                {'text': '  ', 'is_correct': False},  # Should be ignored (empty text)
            ]
        }

        post_data = create_post(
            user=self.user,
            title='Subject Poll',
            content='Please vote on your favorite subject.',
            category='Science',
            poll_data=poll_data
        )

        self.assertIsNotNone(post_data)
        post = Post.objects.get(id=post_data['id'])
        poll = Poll.objects.get(post=post)
        self.assertEqual(poll.question, 'Which subject do you prefer?')

        options = list(PollOption.objects.filter(poll=poll).order_by('order'))
        self.assertEqual(len(options), 3)

        self.assertEqual(options[0].text, 'Physics')
        self.assertEqual(options[0].order, 0)
        self.assertFalse(options[0].is_correct)

        self.assertEqual(options[1].text, 'Chemistry')
        self.assertEqual(options[1].order, 1)
        self.assertTrue(options[1].is_correct)

        self.assertEqual(options[2].text, 'Biology')
        self.assertEqual(options[2].order, 2)
        self.assertFalse(options[2].is_correct)

    def test_create_post_with_string_poll_options(self):
        poll_data = {
            'question': 'Simple Poll',
            'options': ['Option A', 'Option B', 'Option C']
        }

        post_data = create_post(
            user=self.user,
            title='Simple Option Poll',
            content='Testing simple string options.',
            category='General',
            poll_data=poll_data
        )

        self.assertIsNotNone(post_data)
        post = Post.objects.get(id=post_data['id'])
        poll = Poll.objects.get(post=post)
        options = list(PollOption.objects.filter(poll=poll).order_by('order'))

        self.assertEqual(len(options), 3)
        self.assertEqual([o.text for o in options], ['Option A', 'Option B', 'Option C'])
        self.assertEqual([o.order for o in options], [0, 1, 2])
        self.assertTrue(all(not o.is_correct for o in options))
