"""The Pathways "On NEBians" card reads level names, never stored keys."""
from django.test import Client, TestCase

from api import institution_profile as prof
from api.models_institutions import Institution


class PathwaysOnNebLabelTests(TestCase):
    def test_levels_come_back_as_readable_labels(self):
        inst = Institution.objects.create(slug='label-college', name='Label College', kind='college',
                                          district='Kaski', verified=True)
        prof.save(inst, {'about': 'x' * 20, 'levels': ['secondary_9_10', 'plus_two', 'a_level']})
        body = Client().get('/api/pathways/on-neb/').json()
        row = next(r for r in body['items'] if r['slug'] == 'label-college')
        self.assertEqual(row['levels'][0], 'Secondary 9 to 10')
        self.assertNotIn('_', ''.join(row['levels']).replace(' ', ''))
        self.assertEqual(row['levelKeys'], ['secondary_9_10', 'plus_two', 'a_level'])
