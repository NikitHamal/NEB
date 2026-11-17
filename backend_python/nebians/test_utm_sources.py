from django.test import SimpleTestCase

from nebians.analytics import rules
from nebians.analytics.report import _plural


class UtmSourceTests(SimpleTestCase):
    own = ['nebians.com']

    def test_ai_utm_source_is_an_ai_assistant_not_a_campaign(self):
        for src in ('chatgpt.com', 'chatgpt', 'ChatGPT.com'):
            ref = rules.classify_referrer('', self.own, src, '')
            self.assertEqual((ref.channel, ref.name), ('ai', 'ChatGPT'))

    def test_known_aliases_and_custom_campaigns(self):
        self.assertEqual(rules.classify_referrer('', self.own, 'ig').name, 'Instagram')
        custom = rules.classify_referrer('', self.own, 'bzzly')
        self.assertEqual((custom.channel, custom.name), ('campaign', 'bzzly'))

    def test_real_referrer_wins_over_utm(self):
        ref = rules.classify_referrer('https://www.google.com/', self.own, 'chatgpt.com')
        self.assertEqual(ref.channel, 'search')

    def test_plural(self):
        self.assertEqual(_plural(1, 'visit'), 'visit')
        self.assertEqual(_plural(0, 'visit'), 'visits')
