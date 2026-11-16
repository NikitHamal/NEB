import json

from django.test import SimpleTestCase

from . import post_look


class PostLookTests(SimpleTestCase):
    def test_empty_values_clear_the_look(self):
        for raw in (None, '', {}, 'null', {'tone': 0, 'cover': 0}):
            self.assertEqual(post_look.clean(raw), ('', None))

    def test_values_are_bounded_and_unknown_keys_dropped(self):
        out, err = post_look.clean({'tone': 3, 'cover': 999, 'icon': 'school', 'paper': 2, 'evil': '<script>'})
        self.assertIsNone(err)
        self.assertEqual(json.loads(out), {'tone': 3, 'icon': 'school', 'paper': 2})

    def test_icon_must_be_a_slug(self):
        out, _ = post_look.clean({'tone': 1, 'icon': '"><img src=x>'})
        self.assertEqual(json.loads(out), {'tone': 1})

    def test_cover_photo_kept_as_number(self):
        out, _ = post_look.clean({'photo': '42', 'font': 1})
        self.assertEqual(json.loads(out), {'photo': 42, 'font': 1})

    def test_bad_input_is_an_error(self):
        self.assertIsNotNone(post_look.clean('[1,2]')[1])
        self.assertIsNotNone(post_look.clean('{nope')[1])
        self.assertIsNotNone(post_look.clean('x' * 500)[1])

    def test_parse_round_trip(self):
        out, _ = post_look.clean({'tone': 5, 'cover': 7})
        self.assertEqual(post_look.parse(out), {'tone': 5, 'cover': 7})
        self.assertIsNone(post_look.parse(''))

    def test_page_picture_is_a_number_and_counts_as_a_look(self):
        out, err = post_look.clean({'bg': '7', 'bogus': 1})
        self.assertIsNone(err)
        self.assertEqual(json.loads(out), {'bg': 7})
        self.assertEqual(post_look.clean({'bg': 'x'}), ('', None))
