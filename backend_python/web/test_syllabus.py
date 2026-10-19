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
        self.assertContains(page, 'data-syl-check="1.0"')
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
