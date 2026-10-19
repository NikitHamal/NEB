import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch
from django.test import SimpleTestCase
from django.template.loader import get_template, render_to_string
from web.note_syllabus import books, entries_for, navigation, categories
from web.view_helpers import parse_sections


class NoteSyllabusTests(SimpleTestCase):
    def test_every_published_chapter_matches_its_authored_source(self):
        root = Path(__file__).resolve().parents[2]
        seen = set()
        for book in books():
            self.assertIn(book['grade'], ('Class 8', 'Class 10 / SEE', 'Class 11', 'Class 12'))
            for chapter in book['chapters']:
                self.assertNotIn(chapter['id'], seen)
                seen.add(chapter['id'])
                source = (root / chapter['source_path']).read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), chapter['source_sha256'])
                self.assertTrue(chapter['topics'])
                self.assertTrue(chapter['summary'])
                self.assertNotRegex(chapter['text_content'], r'```(?:figure|photo)|:::')
                self.assertTrue(chapter['self_checks'], chapter['id'])
                for check in chapter['self_checks']:
                    self.assertTrue(check['answer'])
        self.assertEqual(len(books()), 28)
        self.assertEqual(len(seen), 492)

    def test_managed_grade_ignores_stale_database_syllabus(self):
        with patch('api.models.SyllabusContent.objects.filter', side_effect=AssertionError('stale content read')):
            chapters = entries_for('Class 12', 'English')
            self.assertEqual(len(chapters), 35)
            self.assertEqual(chapters[0].chapter_id, 'eng12-unit-01')
            self.assertEqual(entries_for('Class 8', 'Physics'), [])

    def test_shared_navigation_resolves_grade10_and_all_subjects(self):
        with patch('api.models.SyllabusContent.objects.exclude') as query:
            query.return_value.values_list.return_value.distinct.return_value = []
            cats = categories()
            self.assertEqual([len(c['subjects']) for c in cats], [6, 8, 7, 7])
            grades, subjects = navigation('Class 10 / SEE')
            self.assertEqual(grades[1]['slug'], 'class-10-see')
            self.assertTrue(any(s['slug'] == 'optional-mathematics' for s in subjects))
            self.assertEqual(len({s['url'] for c in cats for s in c['subjects']}), 28)

    def test_nepali_sections_have_unique_nonempty_anchors(self):
        parts = parse_sections('## विषयवस्तु\n\nपहिलो।\n\n## पाठको सार\n\nदोस्रो।')
        self.assertEqual(len({part['id'] for part in parts}), 2)
        self.assertTrue(all(part['id'] for part in parts))

    def test_nepali_topics_and_furniture_have_no_english_words(self):
        for book in books():
            if book['language'] != 'ne':
                continue
            for chapter in book['chapters']:
                self.assertNotRegex(' '.join(chapter['topics']), '[A-Za-z]')
                headings = re.findall(r'^## (.+)$', chapter['text_content'], re.M)
                self.assertTrue(headings)
                for heading in headings:
                    self.assertNotRegex(heading, '[A-Za-z]')

    def test_templates_compile_and_escape_subjects(self):
        for name in ('web/library.html', 'web/subject_page.html', 'web/partials/syllabus_study_tools.html'):
            self.assertIsNotNone(get_template(name))
        markup = render_to_string('web/partials/syllabus_catalogue.html', {
            'categories_list': [{'grade': '<script>alert(1)</script>', 'subjects': []}],
        })
        self.assertNotIn('<script>alert', markup)
        self.assertIn('&lt;script&gt;', markup)
