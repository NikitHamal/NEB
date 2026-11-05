"""The quick pickers: stages, popular courses and the status each stage implies."""
from django.test import SimpleTestCase

from api import education_catalog as cat


class StageCatalogTests(SimpleTestCase):
    def test_every_stage_level_exists_and_is_listed_once(self):
        seen = []
        for stage in cat.STAGES:
            for value in stage['levels']:
                self.assertIn(value, cat.LEVEL_BY_VALUE, value)
                seen.append(value)
        self.assertEqual(len(seen), len(set(seen)), 'a level sits in two stages')

    def test_every_level_is_reachable_from_a_stage(self):
        listed = {v for s in cat.STAGES for v in s['levels']}
        self.assertEqual(set(cat.LEVEL_VALUES), listed)

    def test_popular_courses_are_real_courses(self):
        for lv in cat.LEVELS:
            for name in lv['popular']:
                self.assertIn(name, lv['programs'], f"{lv['value']}: {name}")

    def test_the_courses_people_ask_for_are_one_tap(self):
        top = cat.LEVEL_BY_VALUE['Bachelors']['popular']
        for name in ['BCA', 'BBS', 'BBA', 'BSc CSIT', 'BSc Computer Science', 'BE Computer',
                     'BSc Nursing']:
            self.assertIn(name, top)
        self.assertLessEqual(len(top), 16)

    def test_stage_statuses_are_valid(self):
        for stage in cat.STAGES:
            self.assertTrue(stage['status'] == '' or stage['status'] in cat.STATUS_VALUES)
        for status in cat.LEVEL_STATUS.values():
            self.assertIn(status, cat.STATUS_VALUES)

    def test_catalog_json_carries_the_new_keys(self):
        data = cat.catalog()
        self.assertIn('stages', data)
        self.assertIn('levelStatus', data)
