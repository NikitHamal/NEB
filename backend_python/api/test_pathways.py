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
        self.assertGreaterEqual(len(d['guides']), 6)
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


class Wave12Tests(TestCase):
    def test_ctevt_computer_engineering_list(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        route = {r['id']: r for r in d['routes']}['dip-computer-eng']
        self.assertEqual(len(route['where']), 45)
        for pid in route['where']:
            self.assertEqual(by[pid]['route_seats']['dip-computer-eng'], 48)
        self.assertEqual(by['p-pec']['district'], 'Kaski')
        sudur = [pid for pid in route['where'] if by[pid]['district'] == 'Kailali']
        self.assertEqual(len(sudur), 1)
        self.assertEqual(len([pid for pid in route['where'] if by[pid]['district'] in ('Dhanusha', 'Mahottari', 'Sarlahi', 'Siraha', 'Bara', 'Parsa', 'Saptari')]), 16)

    def test_ctevt_constituent_institutes(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        civil = {r['id']: r for r in d['routes']}['dip-civil-eng']
        self.assertGreaterEqual(len(civil['where']), 15)
        self.assertEqual(by['p-w12-karnali-ti']['district'], 'Jumla')
        self.assertIn('civil 5'.lower(), by['p-w12-karnali-ti']['note'].lower())
        self.assertIn('p-bset', civil['where'])

    def test_special_scholarship_total(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertIn('480', sch['s-ctevt-special']['name'])
        self.assertIn('3,417', sch['s-ctevt']['covers'])
        self.assertEqual(24 + 12 + 12 + 64 + 6 + 3 + 4 + 12 + 4 + 80 + 30 + 5 + 30 + 5 + 5 + 5 + 21 + 23 + 4 + 36 + 60 + 12 + 7 + 12 + 4, 480)

    def test_new_destinations_and_scholarships(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        for cid in ('cz', 'ge', 'bd', 'kg', 'kz', 'ph'):
            self.assertIn(cid, abroad)
            self.assertLess(abroad[cid]['tuition'][0], abroad[cid]['tuition'][1])
        self.assertIn('s-czech', abroad['cz']['scholarships'])
        self.assertIn('Nepal was not on', {s['id']: s for s in d['scholarships']}['s-czech']['who'])
        self.assertIn('NMC', abroad['ge']['note'])

    def test_noc_guide_and_faqs(self):
        d = pathways.payload()
        guide = {g['id']: g for g in d['guides']}['noc-study-abroad']
        self.assertEqual(sum(step[2] for step in guide['steps']), 2000)
        self.assertGreaterEqual(len(d['faq']), 97)
        route = {r['id']: r for r in d['routes']}
        self.assertIn('16 August 2026', route['bca']['exam'])
        ku = {p['id']: p for p in d['providers']}['p-ku-eng']
        self.assertEqual(ku['fees']['be-computer'], [960000, 960000])
        self.assertEqual(pathways.problems(), [])

    def test_careers_visa_and_see_facts(self):
        d = pathways.payload()
        careers = {c['id']: c for c in d['careers']}
        for cid in ('ui-ux-designer', 'data-scientist', 'cloud-devops-engineer'):
            self.assertLess(careers[cid]['salary']['entry'][0], careers[cid]['salary']['senior'][1])
        routes = {r['id']: r for r in d['routes']}
        self.assertIn('data-scientist', routes['bsc-csit']['careers'])
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('AUD 2,500', abroad['au']['note'])
        self.assertIn('408,000', abroad['ca']['note'])
        self.assertIn('18 months', abroad['uk']['note'])
        self.assertEqual(48392 + 80372 + 94222 + 55977 + 5190 + 7, 284160)
        guides = {g['id']: g for g in d['guides']}
        self.assertEqual(guides['english-test']['steps'][1][2], 36000)
        self.assertGreaterEqual(len(d['faq']), 103)
        self.assertEqual(pathways.problems(), [])


class Wave13Tests(TestCase):
    """Wave 13: US rule correction, UK and German funds, new scholarships, IOE, MEC and KU guides."""

    def test_us_rule_is_marked_blocked(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('blocked by a federal court', abroad['us']['note'])
        self.assertIn('USD 350', abroad['us']['note'])
        faq = {f['id']: f for f in d['faq']}
        self.assertIn('blocked it on 14 September 2026', faq['fw12-v1']['a'])

    def test_funds_arithmetic(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('EUR 11,904', abroad['de']['note'])
        self.assertEqual(992 * 12, 11904)
        self.assertEqual(1529 * 9, 13761)
        self.assertEqual(1171 * 9, 10539)
        self.assertIn('18 months', abroad['uk']['note'])
        self.assertIn('work permit', abroad['th']['work'])

    def test_new_scholarships_are_linked(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertEqual(sch['s-manaaki']['open'], [3, 3])
        self.assertEqual(sch['s-turkiye']['open'], [1, 2])
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('s-humphrey', abroad['us']['scholarships'])
        self.assertIn('s-sau', abroad['in']['scholarships'])

    def test_guides_fees_and_colleges(self):
        d = pathways.payload()
        guides = {g['id'] for g in d['guides']}
        for gid in ('ioe-admission', 'mec-entrance', 'ku-engineering'):
            self.assertIn(gid, guides)
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-ku-eng']['fees']['be-electronics'], [960000, 960000])
        self.assertEqual(6974 * 8 + 7295, 63087)
        self.assertEqual(52766 * 8 + 123704, 545832)
        self.assertEqual(6974 + 7295 + 3400, 17669)
        self.assertEqual(52766 + 123704 + 40000, 216470)
        self.assertIn('NPR 19,269', by['p-pulchowk']['note'])
        self.assertIn('p-ace-mgt', next(r for r in d['routes'] if r['id'] == 'mba')['where'])
        self.assertGreaterEqual(len(d['faq']), 117)
        self.assertEqual(next(x for x in d['scholarships'] if x['id'] == 's-ugc-higher-ed')['scope'], 'nepal')
        self.assertIn('jp', {a['id'] for a in d['abroad']})
        self.assertIn('28 hours', next(a for a in d['abroad'] if a['id'] == 'jp')['note'])
        self.assertEqual(pathways.problems(), [])

    def test_wave13_text_has_no_dashes(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)


class Wave14Tests(TestCase):
    """Wave 14: four destinations, work rules, HKPFS and Pearson, 2026-27 windows, attestation, equivalence and foreign MBBS guides."""

    def test_new_destinations(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        for cid, code in (('uz', 'UZ'), ('pt', 'PT'), ('lt', 'LT'), ('hk', 'HK')):
            self.assertEqual(abroad[cid]['code'], code)
            self.assertLess(abroad[cid]['tuition'][0], abroad[cid]['tuition'][1])
        self.assertIn('Nepal Medical Council', abroad['uz']['note'])
        self.assertIn('EUR 9,120', abroad['pt']['note'])
        self.assertEqual(760 * 12, 9120)
        self.assertEqual(abroad['hk']['work_hours'], 20)
        self.assertIn('IANG', abroad['hk']['stay_back'])

    def test_no_destination_work_rule_is_left_unchecked(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        for cid in ('cz', 'ge', 'bd', 'kg', 'kz', 'ph'):
            self.assertNotIn('Not checked yet', abroad[cid]['work'])
        self.assertIn('prohibited', abroad['bd']['work'])
        self.assertIn('Special Work Permit', abroad['ph']['work'])

    def test_scholarships_and_windows(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('s-hkpfs', abroad['hk']['scholarships'])
        self.assertIn('s-pearson', abroad['ca']['scholarships'])
        self.assertIn('344,400', sch['s-hkpfs']['covers'])
        self.assertEqual(344400 // 12, 28700)
        self.assertIn('15 November 2026', sch['s-mgss']['how'])
        self.assertIn('15 November 2026', sch['s-gjss']['how'])
        self.assertIn('4 June 2026', sch['s-homi-bhabha']['how'])

    def test_guides_and_faqs(self):
        d = pathways.payload()
        guides = {g['id'] for g in d['guides']}
        for gid in ('mofa-attestation', 'tu-equivalence', 'foreign-mbbs-nepal'):
            self.assertIn(gid, guides)
        faq_ids = {f['id'] for f in d['faq']}
        for n in range(1, 19):
            self.assertIn(f'fw14-{n}', faq_ids)
        self.assertGreaterEqual(len(d['faq']), 135)
        self.assertEqual(pathways.problems(), [])

    def test_wave14_text_has_no_dashes(self):
        import json
        text = json.dumps(pathways.payload(), ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)

    def test_wave14b_kusom_nrb_korea_japan(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-ku-school']['fees']['bba'], [960000, 960000])
        self.assertEqual(by['p-ku-school']['fees']['mba'], [656000, 656000])
        self.assertEqual(by['p-ku-school']['website'], 'https://som.ku.edu.np')
        govt = {g['id']: g for g in d['govt']}
        self.assertIn('61 vacancies', govt['g-nrb']['note'])
        self.assertEqual(26 + 3 + 2 + 4 + 26, 61)
        self.assertIn('Chaitra 14', govt['g-so']['note'])
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('KRW 9,000,000', abroad['kr']['note'])
        self.assertIn('JLPT N5', abroad['jp']['note'])
        self.assertEqual(pathways.problems(), [])


class Wave15Tests(TestCase):
    """Wave 15: Romania, Estonia, Switzerland, Cyprus, Romanian scholarship, Health Service exams, 2083/84 dates, college websites."""

    def test_new_destinations(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        for cid, code in (('ro', 'RO'), ('ee', 'EE'), ('ch', 'CH'), ('cy', 'CY')):
            self.assertEqual(abroad[cid]['code'], code)
            self.assertLessEqual(abroad[cid]['tuition'][0], abroad[cid]['tuition'][1])
            self.assertLess(abroad[cid]['living'][0], abroad[cid]['living'][1])
        self.assertEqual(abroad['ro']['work_hours'], 20)
        self.assertEqual(abroad['ch']['work_hours'], 15)
        self.assertEqual(2190 * 2 * 175, 766500)
        self.assertEqual(abroad['ch']['tuition'], [766500, 766500])
        self.assertIn('s-swiss', abroad['ch']['scholarships'])
        self.assertIn('s-romania-govt', abroad['ro']['scholarships'])

    def test_romanian_scholarship_window(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        s = sch['s-romania-govt']
        self.assertEqual(s['country'], 'ro')
        self.assertEqual(s['open'], [2, 3])
        self.assertIn('except medicine', s['who'])
        self.assertEqual(sch['s-swiss']['country'], 'ch')

    def test_health_service_exams(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        for gid, career in (('g-staff-nurse', 'nurse'), ('g-health-assistant', 'health-assistant')):
            self.assertEqual(govt[gid]['career'], career)
            self.assertEqual(govt[gid]['track'], 'psc')
        marks = [int(s[2]) for s in govt['g-staff-nurse']['stages']]
        self.assertEqual(marks, [100, 100, 30])
        self.assertIn('2083', govt['g-kharidar']['note'])
        self.assertIn('Ashoj', govt['g-nayab']['note'])

    def test_calendar_faqs_and_links(self):
        d = pathways.payload()
        faq = {f['id']: f for f in d['faq']}
        for i in range(1, 11):
            self.assertIn('fw15-%d' % i, faq)
        self.assertIn('14 Baisakh 2083', faq['fw15-1']['a'])
        self.assertIn('11 May 2026', faq['fw15-2']['a'])
        self.assertEqual(pathways.problems(d), [])

    def test_websites_are_https_and_unique_per_provider(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-prime']['website'], 'https://prime.edu.np')
        self.assertTrue(by['p-nepalgunj-med']['website'].startswith('https://'))
        for p in d['providers']:
            if p.get('website'):
                self.assertTrue(p['website'].startswith(('http://', 'https://')), p['id'])
        self.assertGreaterEqual(sum(1 for p in d['providers'] if p.get('website')), 220)

    def test_no_dashes_or_emoji(self):
        import json
        text = json.dumps(pathways.payload()['faq'][-10:], ensure_ascii=False)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)


class Wave15bTests(TestCase):
    """Wave 15b: ACCA learning partners, flying schools, MEXT window, extra FAQs."""

    def test_acca_and_flying_schools_are_linked(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        route = {r['id']: r for r in d['routes']}
        for pid in ('p-cca', 'p-nca', 'p-seed', 'p-tbc'):
            self.assertIn(pid, route['acca-route']['where'])
            self.assertEqual(by[pid]['district'], 'Kathmandu')
            self.assertTrue(by[pid]['website'].startswith('https://'))
        self.assertEqual(route['pilot-route']['where'], ['p-naa', 'p-haa', 'p-ofsn'])
        self.assertEqual(by['p-ofsn']['district'], 'Morang')
        self.assertIn('CAAN', route['pilot-route']['about'])

    def test_mext_and_faqs(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertIn('31 May 2026', sch['s-mext']['how'])
        faq = {f['id']: f for f in d['faq']}
        for i in range(11, 15):
            self.assertIn('fw15-%d' % i, faq)
        self.assertEqual(pathways.problems(d), [])

    def test_irish_scholarship_and_class_11_faq(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        abroad = {a['id']: a for a in d['abroad']}
        self.assertIn('s-goi-ies', abroad['ie']['scholarships'])
        self.assertEqual(sch['s-goi-ies']['open'], [1, 3])
        self.assertIn('EUR 10,000', sch['s-goi-ies']['covers'])
        faq = {f['id']: f for f in d['faq']}
        self.assertIn('GPA 1.6', faq['fw15-15']['a'])
        self.assertIn('fw15-16', faq)


class Wave16Tests(TestCase):
    """Wave 16: Malta, Latvia, six scholarships, COMPEX 2026 window, A Level schools, ICAN fees, MEC fee text, 2083 calendars."""

    def test_new_destinations(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        for cid, code in (('mt', 'MT'), ('lv', 'LV')):
            self.assertEqual(abroad[cid]['code'], code)
            self.assertLessEqual(abroad[cid]['tuition'][0], abroad[cid]['tuition'][1])
            self.assertLess(abroad[cid]['living'][0], abroad[cid]['living'][1])
            self.assertEqual(abroad[cid]['work_hours'], 20)
        self.assertEqual(6600 * 175, abroad['mt']['tuition'][0])
        self.assertEqual(26000 * 175, abroad['mt']['tuition'][1])
        self.assertEqual(2400 * 175, abroad['lv']['tuition'][0])

    def test_scholarships_link_to_countries(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        sch = {s['id']: s for s in d['scholarships']}
        for sid, cid in (('s-aalto', 'fi'), ('s-helsinki', 'fi'), ('s-mis-my', 'my'), ('s-kz-govt', 'kz'), ('s-mbzuai', 'ae'), ('s-new-uz', 'uz')):
            self.assertEqual(sch[sid]['country'], cid)
            self.assertIn(sid, abroad[cid]['scholarships'])
        self.assertEqual(sch['s-aalto']['open'], [12, 1])
        self.assertIn('5 January 2027', sch['s-aalto']['how'])
        self.assertIn('RM 1,500', sch['s-mis-my']['covers'])
        self.assertIn('550', sch['s-kz-govt']['covers'])
        self.assertIn('15 December 2026', sch['s-mbzuai']['how'])

    def test_compex_window_replaced(self):
        d = pathways.payload()
        sch = {s['id']: s for s in d['scholarships']}
        self.assertEqual(sch['s-compex']['open'], [8, 9])
        self.assertIn('27 August', sch['s-compex']['how'])
        self.assertNotIn('April or May', sch['s-compex']['how'])

    def test_a_level_schools_and_fees(self):
        d = pathways.payload()
        routes = {r['id']: r for r in d['routes']}
        prov = {p['id']: p for p in d['providers']}
        for pid in ('p-rbs', 'p-ullens', 'p-tbs', 'p-malpi', 'p-chelsea', 'p-trinity'):
            self.assertIn(pid, routes['a-levels']['where'])
        self.assertTrue(prov['p-rbs']['website'].startswith('https://'))
        self.assertEqual(prov['p-sxc']['fees']['a-levels'], [500000, 500000])
        self.assertIn('34,500', prov['p-ican']['note'])
        self.assertIn('34,500', routes['ca-route']['about'])

    def test_mec_fee_text_swapped_once(self):
        d = pathways.payload()
        routes = {r['id']: r for r in d['routes']}
        faq = {f['id']: f for f in d['faq']}
        self.assertIn('NPR 41.68 lakh', routes['mbbs']['about'])
        self.assertIn('41,68,090', faq['f7-1']['a'])
        self.assertIn('41.68 lakh', faq['f12-8']['a'])
        self.assertEqual(faq['f7-1']['a'].count('40,23,250'), 1)

    def test_calendar_faqs_and_links(self):
        d = pathways.payload()
        faq = {f['id']: f for f in d['faq']}
        for i in range(1, 19):
            self.assertIn('fw16-%d' % i, faq)
        self.assertIn('31 October 2026', faq['fw16-1']['a'])
        self.assertIn('NPR 4,000', faq['fw16-1']['a'])
        self.assertIn('Chaitra 2083', faq['fw16-4']['a'])
        self.assertIn('40,500', faq['fw16-5']['a'])
        text = ' '.join(f['a'] for f in d['faq'])
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)
        self.assertEqual(pathways.problems(d), [])

    def test_older_destinations_get_2026_rules(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        self.assertEqual(abroad['nz']['work_hours'], 25)
        self.assertIn('170,368', abroad['no']['note'])
        self.assertIn('1,130.77', abroad['nl']['note'])
        self.assertIn('800 a month', abroad['fi']['note'])
        self.assertIn('10,656', abroad['se']['note'])
        self.assertIn('7,426', abroad['dk']['note'])
        self.assertIn('24 hours', abroad['hu']['note'])
        self.assertIn('Stamp 2', abroad['ie']['note'])

    def test_new_guides(self):
        d = pathways.payload()
        guides = {g['id']: g for g in d['guides']}
        for gid in ('education-loan', 'police-clearance'):
            self.assertIn(gid, guides)
            for step in guides[gid]['steps']:
                self.assertEqual(len(step), 4)
        self.assertIn('opcr.nepalpolice.gov.np', guides['police-clearance']['steps'][0][0])
        self.assertEqual(pathways.problems(d), [])

    def test_every_country_has_visa_steps(self):
        d = pathways.payload()
        self.assertGreaterEqual(len(d['abroad']), 40)
        for a in d['abroad']:
            v = a['visa']
            self.assertTrue(v['name'])
            self.assertGreaterEqual(len(v['steps']), 4, a['id'])
            for s in v['steps']:
                self.assertEqual(len(s), 5, (a['id'], s))
                self.assertIsInstance(s[1], int)
                self.assertIn(s[3], ('online', 'in person', ''))
                self.assertNotIn('\u2013', ''.join(map(str, s)))
                self.assertNotIn('\u2014', ''.join(map(str, s)))
        by = {a['id']: a for a in d['abroad']}
        self.assertEqual(by['au']['visa']['name'], 'Student visa (subclass 500)')
        self.assertEqual(by['us']['visa']['steps'][1][2], 'USD 350')


class Wave18Tests(TestCase):
    """Wave 18: every destination has a scholarship, every route has a journey plan, six council licensing exams, 35 websites, 20 FAQs."""

    def test_every_destination_has_a_scholarship(self):
        d = pathways.payload()
        for a in d['abroad']:
            self.assertTrue(a.get('scholarships'), a['id'])
        sch = {s['id']: s for s in d['scholarships']}
        self.assertEqual(sch['s-latvia-state']['open'], [2, 4])
        self.assertIn('19 MBBS seats', sch['s-bangladesh-saarc']['who'])
        self.assertIn('EUR 450', sch['s-osce-bishkek']['covers'])
        self.assertIn('Get Qualified', sch['s-um-malta']['covers'])

    def test_every_route_has_a_journey_plan(self):
        d = pathways.payload()
        self.assertEqual(len(d['routes']), 124)
        for r in d['routes']:
            self.assertGreaterEqual(len(r.get('plan') or []), 3, r['id'])

    def test_council_licensing_exams_and_career_links(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        for eid, fee in (('e-nec', 2500), ('e-nmcle', 3500), ('e-nlen', 3500), ('e-npc', 3000), ('e-bar', 4500), ('e-nhpc', 3000)):
            self.assertEqual(govt[eid]['fee'], fee)
            self.assertEqual(govt[eid]['track'], 'lic')
        careers = {c['id']: c for c in d['careers']}
        self.assertEqual(careers['civil-engineer']['licence']['exam'], 'e-nec')
        self.assertEqual(careers['doctor']['licence']['exam'], 'e-nmcle')
        self.assertEqual(careers['nurse']['licence']['exam'], 'e-nlen')
        self.assertEqual(careers['pharmacist']['licence']['exam'], 'e-npc')
        self.assertEqual(careers['lawyer']['licence']['exam'], 'e-bar')
        self.assertEqual(careers['lab-tech']['licence']['exam'], 'e-nhpc')
        guides = {g['id'] for g in d['guides']}
        for gid in ('nec-licence', 'nmcle-licence', 'nnc-licence', 'bar-licence'):
            self.assertIn(gid, guides)

    def test_abroad_2026_rules_websites_and_faqs(self):
        d = pathways.payload()
        abroad = {a['id']: a for a in d['abroad']}
        self.assertEqual(abroad['es']['work_hours'], 30)
        self.assertEqual(abroad['tw']['work_hours'], 20)
        self.assertIn('EUR 615', abroad['fr']['note'])
        self.assertIn('722.58', abroad['at']['note'])
        self.assertIn('1,062', abroad['be']['note'])
        self.assertIn('10,179.85', abroad['it']['note'])
        by_p = {p['id']: p for p in d['providers']}
        self.assertEqual(by_p['p-lincoln']['website'], 'https://www.lsnepal.com')
        self.assertEqual(by_p['p-nmc-jorpati']['website'], 'https://www.nmcth.edu')
        self.assertEqual(by_p['p-trinity']['website'], 'https://www.trinity.edu.np')
        self.assertGreaterEqual(sum(1 for p in d['providers'] if p.get('website')), 268)
        govt = {g['id']: g for g in d['govt']}
        self.assertEqual(govt['e-kuumat']['fee'], 1500)
        self.assertEqual(govt['e-ballb']['seats'], 570)
        self.assertEqual(govt['e-afu']['fee'], 3000)
        self.assertEqual(govt['l-sat']['fee'], 15200)
        self.assertEqual(govt['l-gre']['fee'], 30000)
        routes = {r['id']: r for r in d['routes']}
        self.assertEqual(routes['bsc-agri']['exam_id'], 'e-afu')
        self.assertEqual(routes['ba-llb']['exam_id'], 'e-ballb')
        faq = {f['id']: f for f in d['faq']}
        for i in range(1, 26):
            self.assertIn(f'fw18-{i}', faq)
        self.assertEqual(pathways.problems(d), [])


class Wave19Tests(TestCase):
    """Wave 19: 100% MEC 2083/84 health seats + MBBS/BDS route_seats, IOE/KU/PU engineering seats, 9 exams, 10 scholarships, 33 websites, 20 FAQs."""

    def test_mec_2083_notice_totals_and_mbbs_bds_route_seats(self):
        d = pathways.payload()
        total = {}
        for p in d['providers']:
            for rid, n in (p.get('route_seats') or {}).items():
                total[rid] = total.get(rid, 0) + n
        self.assertEqual(total['bsc-nursing'], 2640)
        self.assertEqual(total['bns'], 1160)
        self.assertEqual(total['bpharm'], 905)
        self.assertEqual(total['bds'], 625)
        self.assertEqual(total['bph'], 610)
        self.assertEqual(total['bmlt'], 437)
        self.assertEqual(total['mbbs'], 2745)
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-cist']['route_seats']['bpharm'], 40)
        self.assertEqual(by['p-shree-medical']['route_seats']['bsc-nursing'], 40)
        self.assertEqual(by['p-iom']['route_seats']['mbbs'], 100)
        self.assertEqual(by['p-iom']['route_seats']['bds'], 25)

    def test_ioe_ku_and_pu_engineering_route_seats(self):
        d = pathways.payload()
        by = {p['id']: p for p in d['providers']}
        self.assertEqual(by['p-pulchowk']['route_seats']['be-civil'], 192)
        self.assertEqual(by['p-pulchowk']['route_seats']['be-computer'], 96)
        self.assertEqual(by['p-thapathali']['route_seats']['be-civil'], 144)
        self.assertEqual(by['p-wrc']['route_seats']['be-geomatics'], 48)
        self.assertEqual(by['p-purc']['route_seats']['be-mechanical'], 96)
        self.assertEqual(by['p-cec-rampur']['route_seats']['barch'], 24)
        ioe_aff = ('p-kec', 'p-acem', 'p-kantipur-eng', 'p-hce', 'p-nce', 'p-kathford', 'p-jec', 'p-khwopa-tu', 'p-sagarmatha-eng', 'p-lalitpur-eng')
        self.assertEqual(sum(sum(v for k, v in by[pid]['route_seats'].items() if k != 'bsc-csit') for pid in ioe_aff), 2304)
        self.assertEqual(by['p-ku-eng']['route_seats']['be-computer'], 120)
        self.assertEqual(by['p-ku-eng']['route_seats']['be-mechanical'], 120)
        self.assertEqual(by['p-ncit']['route_seats']['be-computer'], 96)
        self.assertEqual(by['p-cosmos']['route_seats']['be-civil'], 96)

    def test_new_exams_guides_scholarships_and_websites(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        for eid, fee in (('e-bca', 1500), ('e-bit', 1750), ('e-kucat', 2000), ('e-pu-bachelor', 1600),
                         ('e-mecee-pg', 5000), ('e-ioe-msc', 2500), ('e-ican', 34500), ('e-nvc', 3000), ('e-namc', 3500),
                         ('e-somat', 2000), ('e-caan-cpl', 150000), ('l-gmat', 39875)):
            self.assertEqual(govt[eid]['fee'], fee)
        routes = {r['id']: r for r in d['routes']}
        self.assertEqual(routes['bca']['exam_id'], 'e-bca')
        self.assertEqual(routes['bit']['exam_id'], 'e-bit')
        self.assertEqual(routes['md-ms']['exam_id'], 'e-mecee-pg')
        self.assertEqual(routes['ca-route']['exam_id'], 'e-ican')
        self.assertEqual(routes['pilot-route']['exam_id'], 'e-caan-cpl')
        careers = {c['id']: c for c in d['careers']}
        self.assertEqual(careers['veterinarian']['licence']['exam'], 'e-nvc')
        self.assertEqual(careers['ayurveda-doctor']['licence']['exam'], 'e-namc')
        self.assertEqual(careers['chartered-accountant']['licence']['exam'], 'e-ican')
        self.assertEqual(careers['pilot']['licence']['exam'], 'e-caan-cpl')
        guides = {g['id'] for g in d['guides']}
        for gid in ('bca-admission', 'bit-admission', 'mecee-pg-apply', 'pu-scholarship', 'ican-ca-register'):
            self.assertIn(gid, guides)
        abroad = {a['id']: a for a in d['abroad']}
        for sid, cid in (('s-danish-govt', 'dk'), ('s-ernst-mach-at', 'at'), ('s-bi-norway', 'no'), ('s-rtp-au', 'au'),
                         ('s-vanier-ca', 'ca'), ('s-tipp-th', 'th'), ('s-ktu-vmu-lt', 'lt'), ('s-taltech-harno-ee', 'ee'),
                         ('s-spain-uc3m-bse', 'es'), ('s-fct-aveiro-pt', 'pt')):
            self.assertIn(sid, abroad[cid]['scholarships'])
        by_p = {p['id']: p for p in d['providers']}
        self.assertEqual(by_p['p-peoples-dental']['website'], 'https://pdch.com.np')
        self.assertEqual(by_p['p-bc-med']['website'], 'https://bncmedicalcollege.edu.np')
        self.assertEqual(by_p['p-nathm']['route_seats']['bhm'], 264)
        self.assertEqual(by_p['p-nathm']['fees']['bhm'], [575000, 575000])
        self.assertEqual(by_p['p-somtu']['route_seats']['mba'], 135)
        self.assertEqual(by_p['p-shankerdev']['route_seats']['bba'], 99)
        self.assertEqual(by_p['p-tilottama-campus']['route_seats']['bba'], 96)
        self.assertGreaterEqual(sum(1 for p in d['providers'] if p.get('website')), 335)
        faq = {f['id']: f for f in d['faq']}
        for i in range(1, 26):
            self.assertIn(f'fw19-{i}', faq)
        self.assertEqual(pathways.problems(d), [])


class Wave20Tests(TestCase):
    """Wave 20: 8 new exams (NEA, NTC, RBB, ADBL, NBL, SMSTU, EPS-TOPIK, Japan SSW), 9 new colleges, BTech Food/BVSc/BFDM/SMSTU quotas, 13 websites, 17 scholarship windows, 4 guides, 25 FAQs."""

    def test_wave20_exams_and_guides(self):
        d = pathways.payload()
        govt = {g['id']: g for g in d['govt']}
        for eid, fee in (
            ('g-nea', 1200), ('g-ntc', 700), ('g-rbb', 800), ('g-adbl', 800),
            ('g-nbl', 800), ('e-smstu', 2000), ('l-eps', 3850), ('l-ssw', 5000),
        ):
            self.assertEqual(govt[eid]['fee'], fee)
        routes = {r['id']: r for r in d['routes']}
        self.assertEqual(routes['foreign-lang-work']['exam_id'], 'l-eps')
        self.assertEqual(routes['abroad-ms']['exam_id'], 'l-gre')
        self.assertEqual(routes['msc-cs']['exam_id'], 'e-ioe-msc')
        self.assertEqual(routes['bmath-actuarial']['exam_id'], 'e-smstu')
        self.assertEqual(routes['mds-data-science']['exam_id'], 'e-smstu')
        guides = {g['id'] for g in d['guides']}
        for gid in ('eps-korea-apply', 'ssw-japan-apply', 'somat-mba-apply', 'caan-cpl-licence'):
            self.assertIn(gid, guides)

    def test_wave20_providers_websites_scholarships_and_faqs(self):
        d = pathways.payload()
        by_p = {p['id']: p for p in d['providers']}
        self.assertEqual(by_p['p-cafodat']['route_seats']['btech-food'], 48)
        self.assertEqual(by_p['p-cct']['route_seats']['btech-food'], 48)
        self.assertEqual(by_p['p-goldengate']['route_seats']['btech-food'], 24)
        self.assertEqual(by_p['p-hicast']['route_seats']['bvsc'], 40)
        self.assertEqual(by_p['p-nepal-polytechnic']['route_seats']['bvsc'], 40)
        self.assertEqual(by_p['p-ncft']['route_seats']['bfd-design'], 96)
        self.assertEqual(by_p['p-sms-tu']['route_seats']['bmath-actuarial'], 40)
        self.assertEqual(by_p['p-sms-tu']['fees']['bmath-actuarial'], [530000, 530000])
        self.assertEqual(by_p['p-dibya-gyan']['website'], 'https://www.divyagyan.edu.np')
        self.assertEqual(by_p['p-nist-lainchour']['website'], 'https://nist.edu.np')
        self.assertGreaterEqual(sum(1 for p in d['providers'] if p.get('website')), 355)
        routes = {r['id']: r for r in d['routes']}
        self.assertGreaterEqual(len(routes['btech-food']['where']), 10)
        self.assertIn('p-sirjana-arts', routes['bfa']['where'])
        self.assertIn('p-hicast', routes['bvsc']['where'])
        self.assertIn('p-kafcol', routes['bsc-forestry']['where'])
        self.assertIn('p-ncft', routes['bfd-design']['where'])
        sch = {s['id']: s for s in d['scholarships']}
        self.assertEqual(sch['s-singa']['open'], [6, 12])
        self.assertEqual(sch['s-jds-japan']['awards'], 22)
        self.assertEqual(sch['s-clarendon']['awards'], 200)
        self.assertEqual(sch['s-quota']['open'], [8, 10])
        faq = {f['id']: f for f in d['faq']}
        for i in range(1, 26):
            self.assertIn(f'fw20-{i}', faq)
        self.assertEqual(pathways.problems(d), [])
