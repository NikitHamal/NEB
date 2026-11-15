from django.test import TestCase

from api import pathways


class PathwaysDataTests(TestCase):
    def test_references_resolve(self):
        self.assertEqual(pathways.problems(), [])

    def test_every_stage_has_routes(self):
        d = pathways.payload()
        for s in d['stages']:
            self.assertTrue([r for r in d['routes'] if r['stage'] == s['id']], s['id'])

    def test_career_scores_in_range(self):
        for c in pathways.payload()['careers']:
            for k in ('demand', 'competition', 'abroad'):
                self.assertIn(c[k], range(1, 6), c['id'])
            self.assertLessEqual(c['salary']['entry'][0], c['salary']['senior'][1])

    def test_api_is_public_and_cached(self):
        r = self.client.get('/api/pathways/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.get('/api/pathways/', HTTP_IF_NONE_MATCH=r['ETag']).status_code, 304)

    def test_web_page_is_public(self):
        r = self.client.get('/app/pathways/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'pw-districts')

    def test_no_emoji_in_data(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertFalse([ch for ch in text if ord(ch) > 0x2fff])

    def test_faq_is_complete_and_clean(self):
        d = pathways.payload()
        self.assertGreaterEqual(len(d['faq']), 15)
        topics = {t['id'] for t in d['topics']}
        for f in d['faq']:
            self.assertIn(f['topic'], topics, f['id'])
            self.assertTrue(f['q'].endswith('?'), f['id'])
            self.assertNotIn('\u2014', f['a'])
            self.assertNotIn('\u2013', f['a'])
            self.assertNotIn('--', f['a'])
        self.assertEqual(pathways.problems(), [])

    def test_wave3_is_merged(self):
        d = pathways.payload()
        for key, rid in (('routes', 'bit'), ('careers', 'ai-engineer'), ('providers', 'p-cct'), ('scholarships', 's-taiwan'), ('abroad', 'ie')):
            self.assertIn(rid, {x['id'] for x in d[key]}, rid)
        self.assertIn('ai-engineer', next(r for r in d['routes'] if r['id'] == 'bsc-csit')['careers'])

    def test_wave4_is_merged(self):
        d = pathways.payload()
        for key, rid in (
            ('routes', 'bim'), ('routes', 'pcl-nursing'), ('routes', 'bns'), ('routes', 'bams'),
            ('routes', 'ba-llb'), ('routes', 'be-geomatics'), ('routes', 'council-license'),
            ('careers', 'geomatics-engineer'), ('careers', 'optometrist'), ('careers', 'product-manager'),
            ('providers', 'p-trichandra'), ('providers', 'p-kahs'), ('providers', 'p-butwal'),
            ('scholarships', 's-mgss'), ('scholarships', 's-gjss'), ('scholarships', 's-eiffel'),
            ('abroad', 'fr'), ('abroad', 'se'), ('abroad', 'be'), ('abroad', 'th'),
        ):
            self.assertIn(rid, {x['id'] for x in d[key]}, rid)
        self.assertGreaterEqual(len({p['district'] for p in d['providers']}), 24)
        self.assertGreaterEqual(len(d['faq']), 30)

    def test_dynamic_posts_lab_loads_data_before_lab(self):
        r = self.client.get('/app/lab/dynamic-posts/')
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertLess(html.index('dynamic-posts-data.js'), html.index('dynamic-posts-lab.js'))
