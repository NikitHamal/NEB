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


class NepalMapTests(TestCase):
    """The map file read by the web page and the Android app (res/raw/nepal_map.json is the same file)."""

    def _map(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        web = (root / 'web/static/web/data/nepal_map.json').read_text(encoding='utf-8')
        app = root.parent / 'app/src/main/res/raw/nepal_map.json'
        if app.exists():
            self.assertEqual(web, app.read_text(encoding='utf-8'))
        return json.loads(web)

    def test_map_has_every_district_and_province(self):
        m = self._map()
        self.assertEqual(len(m['d']), 77)
        self.assertEqual(len(m['pv']), 7)
        self.assertEqual(len({d['n'] for d in m['d']}), 77)
        self.assertEqual(sorted({d['p'] for d in m['d']}), list(range(7)))

    def test_provider_districts_exist_on_the_map(self):
        names = {d['n'] for d in self._map()['d']}
        for p in pathways.payload()['providers']:
            self.assertIn(p['district'], names, p['id'])

    def test_wave7_medical_fees_follow_the_mec_ceiling(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-kist-med']['fees']['mbbs'], [4023250, 4023250])
        self.assertEqual(by['p-gandaki-med']['fees']['mbbs'], [4595720, 4595720])
        self.assertGreaterEqual(len(d['faq']), 51)
        self.assertEqual(pathways.problems(), [])

    def test_wave8_medical_seats_dental_and_work_rules(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-kmc']['seats'], 130)
        self.assertIn('BDS 45', by['p-kmc']['note'])
        self.assertEqual(by['p-kantipur-dental']['fees']['bds'], [2092290, 2092290])
        self.assertEqual(by['p-sdcuhs']['district'], 'Kailali')
        bds = next(r for r in d['routes'] if r['id'] == 'bds')
        self.assertIn('p-kantipur-dental', bds['where'])
        mbbs = next(r for r in d['routes'] if r['id'] == 'mbbs')
        self.assertIn('p-naihs', mbbs['where'])
        my = next(a for a in d['abroad'] if a['id'] == 'my')
        self.assertEqual(my['work_hours'], 20)
        fb = next(s for s in d['scholarships'] if s['id'] == 's-fulbright')
        self.assertEqual(fb['open'], [2, 4])
        self.assertGreaterEqual(len(d['faq']), 55)
        self.assertEqual(pathways.problems(), [])


class Wave9Tests(TestCase):
    """MEC 2083/84 seats for health courses, Purbanchal engineering seats, scholarship windows, work rules."""

    def test_mec_program_seats_follow_the_notice(self):
        d = pathways.payload()
        total = {}
        for p in d['providers']:
            for rid, n in (p.get('route_seats') or {}).items():
                total[rid] = total.get(rid, 0) + n
        # listed colleges can only be a part of the MEC totals (2,640 nursing, 1,160 BNS, 905 BPharm), never more
        self.assertLessEqual(total['bsc-nursing'], 2640)
        self.assertLessEqual(total['bns'], 1160)
        self.assertLessEqual(total['bpharm'], 905)
        self.assertGreater(total['bsc-nursing'], 2000)
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-nams']['route_seats']['bsc-nursing'], 140)
        self.assertEqual(by['p-mmihs']['fees']['bsc-nursing'], [1036000, 1036000])
        self.assertEqual(by['p-pokhara-nursing']['district'], 'Kaski')
        nursing = next(r for r in d['routes'] if r['id'] == 'bsc-nursing')
        self.assertIn('p-biratnagar-nursing', nursing['where'])
        self.assertGreaterEqual(len(nursing['where']), 40)

    def test_purbanchal_engineering_seats(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-pusoe']['seats'], 300)
        self.assertEqual(by['p-acme']['route_seats']['be-civil'], 144)
        self.assertEqual(by['p-khwopa-eng']['route_seats']['barch'], 60)
        self.assertEqual(by['p-nec']['route_seats']['be-computer'], 96)
        civil = next(r for r in d['routes'] if r['id'] == 'be-civil')
        self.assertIn('p-dhulabari', civil['where'])
        pu = [p for p in d['providers'] if 'Purbanchal University. Approved seats' in p.get('note', '')]
        self.assertEqual(sum(p['seats'] for p in pu) + 296, 2938)

    def test_wave9_windows_and_rules(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertEqual(sch['s-taiwan']['open'], [2, 3])
        self.assertEqual(sch['s-sh']['open'], [11, 1])
        self.assertEqual(sch['s-jjwbgsp']['open'], [1, 5])
        self.assertIn('Nepal was not on', sch['s-aga-khan']['who'])
        abroad = {a['id']: a for a in d['abroad']}
        self.assertEqual(abroad['sg']['work_hours'], 16)
        self.assertEqual(abroad['tr']['work_hours'], 24)
        self.assertGreaterEqual(len(d['faq']), 63)
        self.assertEqual(pathways.problems(), [])

    def test_wave9_text_has_no_dashes(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)


class Wave10Tests(TestCase):
    """BSc CSIT quota 2083 by college, TU BCA list, +2 colleges, Commonwealth correction, work rules."""

    def test_csit_quota_matches_the_iost_result(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        listed = [p for p in d['providers'] if (p.get('route_seats') or {}).get('bsc-csit')]
        self.assertEqual(len(listed), 61)
        self.assertEqual(sum(p['route_seats']['bsc-csit'] for p in listed), 3108)
        self.assertEqual(by['p-patan']['route_seats']['bsc-csit'], 144)
        self.assertEqual(by['p-prime']['route_seats']['bsc-csit'], 48)
        self.assertEqual(by['p-kathford']['district'], 'Lalitpur')
        csit = next(r for r in d['routes'] if r['id'] == 'bsc-csit')
        for p in listed:
            self.assertIn(p['id'], csit['where'])

    def test_bca_plus2_and_health_lists_grew(self):
        d = pathways.payload()
        routes = {r['id']: r for r in d['routes']}
        self.assertGreaterEqual(len(routes['bca']['where']), 120)
        self.assertIn('p-hetauda-city', routes['bca']['where'])
        self.assertIn('p-united-academy', routes['plus2-science']['where'])
        self.assertIn('p-united-academy', routes['plus2-law']['where'])
        self.assertIn('p-hamro-nursing', routes['bsc-nursing']['where'])
        self.assertIn('BITM', routes['bim']['name'])
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-hamro-nursing']['district'], 'Morang')
        self.assertEqual(by['p-shankerdev']['route_seats']['bim'], 66)

    def test_commonwealth_is_closed_to_nepal_and_rules_are_filled(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertNotIn('open', sch['s-commonwealth'])
        self.assertIn('Nepal is not a Commonwealth member', sch['s-commonwealth']['who'])
        self.assertEqual(sch['s-holland']['open'], [11, 5])
        abroad = {a['id']: a for a in d['abroad']}
        self.assertEqual(abroad['hu']['work_hours'], 24)
        self.assertEqual(abroad['cn']['work_hours'], 8)
        faq = {f['id']: f for f in d['faq']}
        self.assertNotIn('Chevening, Commonwealth', faq['fa-3']['a'])
        self.assertGreaterEqual(len(d['faq']), 70)
        self.assertEqual(pathways.problems(), [])

    def test_wave10_text_has_no_dashes(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)


class Wave11Tests(TestCase):
    """Civil service pay from Shrawan 2083, BIT seats, scholarship eligibility text, new FAQs."""

    def test_civil_service_pay_follows_the_2083_84_budget(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        self.assertEqual(govt['g-kharidar']['pay'], 44811)
        self.assertEqual(govt['g-nayab']['ladder'][1][1], 47023)
        self.assertEqual(govt['g-so']['pay'], 57864)
        # basic 10 percent higher, plus 10 percent incentive and NPR 5,000 dearness allowance
        for basic, gross in ((36192, 44811), (38203, 47023), (48058, 57864)):
            self.assertEqual(round(basic * 1.1 + 5000), gross)
        self.assertIn('Shrawan 2083', govt['g-kharidar']['note'])
        self.assertNotIn('FY 2082/83, rounded', govt['g-kharidar']['note'])
        self.assertIn('449 posts', govt['g-tsc']['note'])

    def test_bit_seats_and_eligibility_text(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-patan']['route_seats']['bit'], 72)
        self.assertEqual(by['p-bhaktapur-mc']['route_seats']['bit'], 72)
        bit = next(r for r in d['routes'] if r['id'] == 'bit')
        self.assertIn('p-padmakanya', bit['where'])
        sch = {s['id']: s for s in d['scholarships']}
        self.assertIn('three years', sch['s-fulbright']['who'])
        self.assertIn('OASIS', sch['s-australia']['how'])
        self.assertGreaterEqual(len(d['faq']), 75)
        self.assertEqual(pathways.problems(), [])

    def test_wave11_text_has_no_dashes(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)

    def test_law_and_agriculture_seats(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        llb = [p for p in d['providers'] if (p.get('route_seats') or {}).get('llb')]
        self.assertEqual(sum(p['route_seats']['llb'] for p in llb), 3800)
        self.assertEqual(len(llb), 12)
        ballb = [p for p in d['providers'] if (p.get('route_seats') or {}).get('ba-llb')]
        self.assertEqual(sum(p['route_seats']['ba-llb'] for p in ballb), 570)
        self.assertEqual(by['p-tu-law']['route_seats']['llb'], 600)
        self.assertEqual(by['p-aafu']['route_seats']['bsc-agri'], 167)
        self.assertEqual(by['p-cnrm-khajura']['district'], 'Banke')
        self.assertGreaterEqual(len(d['faq']), 78)
        self.assertEqual(pathways.problems(), [])

    def test_india_and_uae_work_rules(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('Off campus work is not allowed', abroad['in']['work'])
        self.assertIn('no objection certificate', abroad['ae']['work'])
        self.assertGreaterEqual(len(d['faq']), 79)

    def test_police_and_apf_numbers(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        self.assertEqual(govt['g-police-asi']['seats'], 211)
        self.assertEqual(govt['g-police-asi']['fee'], 500)
        self.assertEqual(govt['g-police-inspector']['seats'], 29)
        self.assertEqual(16 + 5 + 4 + 2 + 2, 29)
        self.assertEqual(114 + 29 + 26 + 19 + 14 + 5 + 4, 211)
        self.assertIn('604 constable posts', govt['g-apf-asi']['note'])
        self.assertGreaterEqual(len(d['faq']), 80)
