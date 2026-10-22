from django.test import TestCase

from web import syllabus_data


class SyllabusTests(TestCase):
    def test_every_grade_has_subjects(self):
        grades = {g['grade']: g for g in syllabus_data.index()['grades']}
        self.assertEqual(sorted(grades, key=int), ['8', '10', '11', '12'])
        for g in grades.values():
            self.assertTrue(g['subjects'])

    def test_hub_and_subject_pages(self):
        self.assertEqual(self.client.get('/app/syllabus/').status_code, 200)
        self.assertEqual(self.client.get('/app/library/?tab=categories').status_code, 200)
        page = self.client.get('/app/syllabus/11/physics/')
        self.assertContains(page, 'href="/app/syllabus/11/physics/unit-3/"')
        self.assertContains(page, 'data-st-panel="bank"')
        self.assertEqual(self.client.get('/app/syllabus/12/nothing/').status_code, 404)

    def test_old_subject_page_redirects(self):
        response = self.client.get('/app/subject/class-12/english/')
        self.assertRedirects(response, '/app/syllabus/12/english/', fetch_redirect_response=False)

    def test_search_ranks_the_selected_class_first(self):
        data = self.client.get('/app/syllabus/search/', {'q': 'photosynthesis', 'grade': '10'}).json()
        self.assertGreater(data['total'], 1)
        self.assertEqual(data['results'][0]['grade'], '10')

    def test_app_api(self):
        self.assertEqual(self.client.get('/api/syllabus/v2/').status_code, 200)
        unit = self.client.get('/api/syllabus/v2/8/nepali/').json()['units'][0]
        self.assertTrue(unit['topics'])
        legacy = self.client.get('/api/syllabus/subjects/class-10/science/').json()
        self.assertTrue(legacy['chapters'][0]['guide_sections'])


class StudyReaderTests(TestCase):
    """The chapters and question banks exported from the books (notes/tools/export_study.py)."""

    def test_every_subject_has_its_chapters_and_a_bank(self):
        from web import study_data
        for g in syllabus_data.index()['grades']:
            for s in g['subjects']:
                idx = study_data.subject_index(g['grade'], s['subject'])
                self.assertEqual(len(idx['units']), s['unit_count'], (g['grade'], s['subject']))
                self.assertTrue(idx['banks'], (g['grade'], s['subject']))

    def test_reader_pages(self):
        page = self.client.get('/app/syllabus/11/physics/unit-3/')
        self.assertContains(page, '<h1 class="rd-title">Kinematics</h1>', html=False)
        self.assertContains(page, 'class="mcq"')
        self.assertContains(page, '<details class="ans')
        self.assertContains(page, 'href="/app/syllabus/11/physics/unit-4/"')
        self.assertEqual(self.client.get('/app/syllabus/10/nepali/bank-1/').status_code, 200)
        self.assertEqual(self.client.get('/app/syllabus/12/physics/exam-guide/').status_code, 200)
        self.assertEqual(self.client.get('/app/syllabus/11/physics/unit-99/').status_code, 404)

    def test_nepali_questions_are_tappable(self):
        page = self.client.get('/app/syllabus/10/nepali/bank-1/')
        self.assertContains(page, 'class="mcq-p" data-key=')

    def test_app_chapter_api(self):
        doc = self.client.get('/api/syllabus/v2/11/physics/').json()
        self.assertTrue(doc['units'][0]['has_chapter'])
        self.assertGreater(doc['units'][0]['read_min'], 0)
        self.assertTrue(doc['banks'])
        ch = self.client.get('/api/syllabus/v2/11/physics/unit/3/').json()
        self.assertEqual(ch['title'], 'Kinematics')
        self.assertEqual((ch['prev'], ch['next']), (2, 4))
        self.assertIn('<span class="m">', ch['html'])
        self.assertEqual(self.client.get('/api/syllabus/v2/12/english/bank/1/').status_code, 200)
        self.assertEqual(self.client.get('/api/syllabus/v2/12/english/guide/').status_code, 200)
