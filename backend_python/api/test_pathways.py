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

    def test_wave5_is_merged_and_all_77_districts_covered(self):
        from api.models import NEPAL_DISTRICTS
        d = pathways.payload()
        for key, rid in (
            ('routes', 'pcl-cmlt'), ('routes', 'pcl-radiography'), ('routes', 'pcl-ophthalmic'),
            ('routes', 'bmath-actuarial'), ('routes', 'baslp'), ('routes', 'bmid'),
            ('routes', 'bicte'), ('routes', 'mds-data-science'), ('routes', 'public-enterprise-route'),
            ('careers', 'actuary-risk-analyst'), ('careers', 'speech-audiologist'), ('careers', 'economist-policy'),
            ('providers', 'p-sms-tu'), ('providers', 'p-sohs-ctevt'), ('providers', 'p-mbahs'), ('providers', 'p-rahs'),
            ('scholarships', 's-compex'), ('scholarships', 's-sjss'), ('scholarships', 's-ayush'),
            ('abroad', 'dk'), ('abroad', 'at'), ('abroad', 'pl'), ('abroad', 'es'),
        ):
            self.assertIn(rid, {x['id'] for x in d[key]}, rid)
        self.assertEqual({p['district'] for p in d['providers']}, set(NEPAL_DISTRICTS))
        self.assertGreaterEqual(len(d['routes']), 120)
        self.assertGreaterEqual(len(d['faq']), 40)

    def test_dynamic_posts_lab_loads_data_before_lab(self):
        r = self.client.get('/app/lab/dynamic-posts/')
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertLess(html.index('dynamic-posts-data.js'), html.index('dynamic-posts-lab.js'))

    def test_wave6_enrichment_is_merged(self):
        d = pathways.payload()
        careers = {c['id']: c for c in d['careers']}
        self.assertTrue(all(c.get('ladder') and c.get('employers') for c in careers.values()))
        self.assertEqual(careers['teacher']['licence']['exam'], 'g-tsc')
        for s in d['scholarships']:
            self.assertTrue(s.get('type'), s['id'])
        for rid in ('s-jjwbgsp', 's-clarendon', 's-schwarzman'):
            self.assertIn(rid, {s['id'] for s in d['scholarships']})
        abroad = {a['id']: a for a in d['abroad']}
        self.assertEqual(abroad['au']['code'], 'AU')
        self.assertEqual(abroad['ca']['work_hours'], 24)
        self.assertIn('s-clarendon', abroad['uk']['scholarships'])
        govt = {g['id']: g for g in d['govt']}
        for gid in ('g-police-inspector', 'g-police-asi', 'g-apf-asi', 'g-army-cadet', 'g-nrb'):
            self.assertIn(gid, govt)
        self.assertEqual(govt['g-kharidar']['rung'], 0)
        self.assertAlmostEqual(sum(v for _, v in govt['g-so']['quota']), 100, places=1)
        self.assertEqual(len(d['guides']), 6)
        pulchowk = next(p for p in d['providers'] if p['id'] == 'p-pulchowk')
        self.assertEqual(pulchowk['seats'], 624)
        self.assertIn('be-computer', pulchowk['fees'])
        self.assertGreaterEqual(len(d['faq']), 48)
        self.assertGreaterEqual(len([r for r in d['routes'] if r.get('plan')]), 20)
        self.assertEqual(pathways.problems(), [])

    def test_wave6_text_has_no_dashes(self):
        import json
        d = pathways.payload()
        for key in ('faq', 'govt', 'guides'):
            text = json.dumps(d[key], ensure_ascii=False)
            self.assertNotIn('\u2014', text)
            self.assertNotIn('\u2013', text)
