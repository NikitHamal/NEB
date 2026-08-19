import uuid

from django.test import SimpleTestCase, TestCase

from api.models import User
from api.services import avatar_or_photo_url, avatar_url_for, save_avatar_customization


class AvatarUrlHelperTests(SimpleTestCase):
    def test_avatar_url_for_includes_prefs_sorted(self):
        user = User(
            username='tester',
            avatar_hue=200,
            avatar_anim='bob',
            avatar_expression='wink',
            avatar_eye_color='#aabbcc',
            avatar_color='#123456',
            avatar_shape='capsule',
        )
        url = avatar_url_for(user)
        self.assertTrue(url.startswith('/avatar/tester/?'))
        self.assertIn('anim=bob', url)
        self.assertIn('color=%23123456', url)
        self.assertIn('expression=wink', url)
        self.assertIn('eyecolor=%23aabbcc', url)
        self.assertIn('hue=200', url)
        self.assertIn('shape=capsule', url)
        self.assertEqual(url, '/avatar/tester/?' + '&'.join(sorted(url.split('?')[1].split('&'))))

    def test_avatar_or_photo_url_photo_first_when_flag_off(self):
        user = User(username='photo_user', photo_url='https://example.com/me.jpg', avatar_use_pp=False)
        self.assertEqual(avatar_or_photo_url(user), 'https://example.com/me.jpg')

    def test_avatar_or_photo_url_avatar_wins_when_flag_on(self):
        user = User(username='avatar_user', photo_url='https://example.com/me.jpg', avatar_use_pp=True)
        self.assertEqual(avatar_or_photo_url(user), '/avatar/avatar_user/')

    def test_avatar_or_photo_url_falls_back_to_avatar(self):
        user = User(username='no_photo', photo_url='', avatar_use_pp=False)
        self.assertEqual(avatar_or_photo_url(user), '/avatar/no_photo/')


class AvatarUsePpCustomizeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=str(uuid.uuid4()),
            username='use_pp_tester',
            email='use_pp_tester@example.com',
            email_verified=True,
        )

    def test_customize_toggles_use_pp(self):
        result, code = save_avatar_customization(self.user, {'use_pp': True})
        self.assertEqual(code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar_use_pp)
        self.assertEqual(avatar_or_photo_url(self.user), '/avatar/use_pp_tester/')

        result, code = save_avatar_customization(self.user, {'use_pp': 'false'})
        self.assertEqual(code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.avatar_use_pp)

    def test_customize_without_use_pp_keeps_flag(self):
        self.user.avatar_use_pp = True
        self.user.save(update_fields=['avatar_use_pp'])
        result, code = save_avatar_customization(self.user, {'shape': 'round'})
        self.assertEqual(code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar_use_pp)
        self.assertEqual(self.user.avatar_shape, 'round')

    def test_customize_use_pp_sets_anim(self):
        result, code = save_avatar_customization(self.user, {'use_pp': True, 'anim': 'bob'})
        self.assertEqual(code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar_use_pp)
        self.assertEqual(self.user.avatar_anim, 'bob')
        self.assertIn('anim=bob', avatar_or_photo_url(self.user))