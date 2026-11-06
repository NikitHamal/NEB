"""The right rail shows a post's own picture where there is one: the thumbnail
slot is the icon slot, and a post with no picture keeps the icon."""
from django.template.loader import render_to_string
from django.test import TestCase

NOW = 1_700_000_000_000


def _post(**kwargs):
    row = {'id': 'p1', 'title': 'Why does a heavier object fall at the same rate?',
           'category': 'Science', 'createdAt': NOW, 'images': [], 'attachments': []}
    row.update(kwargs)
    return row


def _rail(rows):
    return render_to_string('web/_home_aside.html', {
        'home_unanswered': rows, 'home_contributors': [], 'feed_entries': [],
    })


class HomeRailThumbTests(TestCase):
    def test_a_post_with_a_picture_shows_the_picture(self):
        html = _rail([_post(images=[{'id': 1, 'imageUrl': '/media/forum_images/a.png', 'order': 0}])])
        self.assertIn('class="hf-side-thumb"', html)
        self.assertIn('src="/media/forum_images/a.png"', html)
        self.assertNotIn('hf-side-icon', html)

    def test_a_video_post_falls_back_to_its_poster(self):
        html = _rail([_post(attachments=[{'kind': 'video', 'thumbnail_url': '/media/forum_media/poster.jpg'}])])
        self.assertIn('class="hf-side-thumb"', html)
        self.assertIn('src="/media/forum_media/poster.jpg"', html)

    def test_a_post_with_no_picture_keeps_the_icon(self):
        html = _rail([_post()])
        self.assertIn('class="hf-side-icon"', html)
        self.assertIn('>help<', html)
        self.assertNotIn('hf-side-thumb', html)

    def test_the_first_picture_is_the_one_that_shows(self):
        html = _rail([_post(images=[{'id': 2, 'imageUrl': '/media/forum_images/first.png', 'order': 0},
                                    {'id': 3, 'imageUrl': '/media/forum_images/second.png', 'order': 1}])])
        self.assertIn('/media/forum_images/first.png', html)
        self.assertNotIn('/media/forum_images/second.png', html)
