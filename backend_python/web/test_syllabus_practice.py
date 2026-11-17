"""The hub and the apps say where question banks and model papers are."""
from django.test import SimpleTestCase

from web import study_data, syllabus_data


class PracticeCountsTests(SimpleTestCase):
    def test_counts_match_the_exported_banks(self):
        entries = syllabus_data.with_practice(syllabus_data.school_entries() + syllabus_data.track_entries())
        self.assertTrue(entries)
        for entry in entries:
            for card in entry["subjects"]:
                info = study_data.subject_index(str(entry["grade"]), card["subject"])
                banks = info.get("banks") or []
                self.assertEqual(card["model_count"], sum(1 for b in banks if b.get("kind") == "model"))
                self.assertEqual(card["bank_count"], sum(1 for b in banks if b.get("kind") != "model"))

    def test_source_entries_are_not_mutated(self):
        syllabus_data.with_practice(syllabus_data.school_entries())
        for entry in syllabus_data.school_entries():
            for card in entry["subjects"]:
                self.assertNotIn("bank_count", card)
