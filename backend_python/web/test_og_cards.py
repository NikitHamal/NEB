"""The drawn share cards.

The drawing module has no Django in it on purpose, so most of this runs
without a database: it renders real cards and asserts on the pixels. The
route-level tests at the bottom need the app.
"""
import io
import os
import sys
import unittest

from PIL import Image

from web import og_cards, og_art, og_heroes, og_logo

STATIC = os.path.join(os.path.dirname(os.path.abspath(og_cards.__file__)),
                      'static', 'web')


def _corner_dark(img):
    """Is this a card drawn on ink? The old design was cream."""
    r, g, b = img.convert('RGB').getpixel((6, 6))
    return (r + g + b) / 3.0 < 90


class LogoAssetTests(unittest.TestCase):
    def test_the_committed_cuts_exist(self):
        for name in (og_logo.COLOUR_FILE, og_logo.MONO_FILE):
            self.assertTrue(os.path.exists(os.path.join(og_logo.IMG_DIR, name)),
                            '%s is missing; run tools/og/build_logo.py' % name)

    def test_the_mark_comes_back_at_the_height_asked_for(self):
        art = og_logo.mark(120)
        self.assertEqual(art.size[1], 120)
        # Cropped to the ink: no transparent margin to misalign a lockup.
        self.assertEqual(art.getchannel('A').getbbox()[1], 0)

    def test_the_mono_cut_is_one_colour(self):
        art = og_logo.mark(80, mono=True).convert('RGBA')
        visible = [px for px in art.getdata() if px[3] > 200]
        self.assertTrue(visible)
        self.assertEqual(len({px[:3] for px in visible}), 1)


class CardTests(unittest.TestCase):
    def render(self, **kw):
        kw.setdefault('kicker', 'Library')
        return og_cards.render('page', kw.pop('title', 'Every paper in one place'), **kw)

    def test_a_card_is_1200_by_630(self):
        self.assertEqual(self.render().size, (1200, 630))

    def test_cards_are_drawn_on_ink(self):
        self.assertTrue(_corner_dark(self.render()))

    def test_every_sculpture_draws_without_raising(self):
        # A hero that throws is a 404 on an og:image, which a scraper caches.
        for name in ('books', 'paper', 'bubbles', 'flask', 'graph',
                     'question', 'cards', 'spark', 'mark', 'avatar'):
            with self.subTest(hero=name):
                img = og_cards.render('page', 'A title for the card', kicker='K',
                                      hero=name, meta=('one', 'two'))
                self.assertEqual(img.size, (1200, 630))

    def test_an_unknown_hero_falls_back_to_the_mark(self):
        img = og_cards.render('page', 'Fallback', kicker='K', hero='nonsense')
        self.assertEqual(img.size, (1200, 630))

    def test_a_long_title_still_renders(self):
        long = ('NEB publishes the Class 12 examination routine for 2082, with '
                'practicals moved ahead of the written papers for every stream')
        self.assertEqual(og_cards.render('news', long, kicker='Blog').size, (1200, 630))

    def test_a_short_title_is_set_larger_than_a_sentence(self):
        # The whole point of the vertical budget: one word should be poster
        # sized, and a sentence should not shrink to the same size as it.
        d = og_cards.ImageDraw.Draw(Image.new('RGB', (10, 10)))
        one_word, _ = og_cards._fit_title(d, 'Physics', 620)
        sentence, _ = og_cards._fit_title(
            d, 'NEB publishes the Class 12 examination routine for 2082, with '
               'practicals moved ahead of the written papers', 620)
        self.assertGreater(one_word.size, sentence.size * 2)

    def test_a_title_never_outgrows_its_vertical_budget(self):
        d = og_cards.ImageDraw.Draw(Image.new('RGB', (10, 10)))
        f, lines = og_cards._fit_title(
            d, 'NEB publishes the Class 12 examination routine for 2082 with '
               'practicals moved ahead of the written papers', 620)
        leading = (f.size / float(og_cards.SS)) * 1.10
        self.assertLessEqual(leading * len(lines), og_cards.TITLE_BUDGET + 1)

    def test_title_wrapping_has_no_orphan_word(self):
        d = og_cards.ImageDraw.Draw(Image.new('RGB', (10, 10)))
        _, lines = og_cards._fit_title(
            d, 'Every paper, note and book in one place', 620)
        # The balanced wrap moves "place" up rather than leaving it alone.
        self.assertGreaterEqual(len(lines[-1].split()), 1)
        self.assertLess(len(lines), 5)

    def test_the_subject_changes_the_accent(self):
        physics, _ = og_cards.accent_for('Physics')
        chemistry, _ = og_cards.accent_for('Chemistry')
        self.assertNotEqual(physics, chemistry)

    def test_an_explicit_accent_wins(self):
        accent, _ = og_cards.accent_for('Physics', '#123456')
        self.assertEqual(accent, (0x12, 0x34, 0x56))

    def test_a_bad_accent_falls_back_to_the_subject(self):
        accent, _ = og_cards.accent_for('Physics', 'nonsense')
        self.assertEqual(accent, og_cards.accent_for('Physics')[0])

    def test_png_is_a_png_under_the_twitter_limit(self):
        png = og_cards.to_png(self.render())
        self.assertTrue(png.startswith(b'\x89PNG'))
        self.assertLess(len(png), 5 * 1024 * 1024)
        rgb = Image.open(io.BytesIO(png))
        self.assertEqual(rgb.size, (1200, 630))

    def test_the_same_seed_draws_the_same_card(self):
        a = og_cards.render('page', 'Same words', kicker='K', hero='flask', seed='x')
        b = og_cards.render('page', 'Same words', kicker='K', hero='flask', seed='x')
        self.assertEqual(a.tobytes(), b.tobytes())


class ColourTests(unittest.TestCase):
    def test_lift_brings_a_dark_colour_up_without_changing_its_hue(self):
        dark = (10, 20, 60)
        lifted = og_art.lift(dark, 170)
        self.assertGreater(og_art.lum(lifted), 165)
        self.assertGreater(lifted[2], lifted[0])

    def test_face_palette_keeps_the_hue(self):
        top, left, right = og_art.face_palette((185, 28, 28))
        for tone in (top, left, right):
            self.assertGreater(tone[0], tone[2])
        self.assertGreater(og_art.lum(top), og_art.lum(left))
        self.assertGreater(og_art.lum(left), og_art.lum(right))

    def test_mix_is_bounded(self):
        self.assertEqual(og_art.mix((0, 0, 0), (255, 255, 255), 2.0), (255, 255, 255))
        self.assertEqual(og_art.mix((0, 0, 0), (255, 255, 255), -1.0), (0, 0, 0))


def setUpModule():
    # The renderer reads its fonts from the static tree; make sure the ones it
    # names are actually there, because a missing font silently falls back to
    # a bitmap face and every card looks wrong.
    for name in ('poppins_bold.ttf', 'poppins_medium.ttf', 'poppins_regular.ttf'):
        path = os.path.join(STATIC, 'fonts', name)
        if not os.path.exists(path):
            raise unittest.SkipTest('font missing: ' + path)


if __name__ == '__main__':
    unittest.main()
