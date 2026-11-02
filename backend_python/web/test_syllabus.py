import json
import os
import re
import shutil
import tempfile
from unittest import mock

from django.test import TestCase

from web import study_data, syllabus_data, views_syllabus


class SyllabusTests(TestCase):
    def test_every_grade_has_subjects(self):
        entries = syllabus_data.index()['grades']
        grades = {g['grade']: g for g in entries if g['kind'] == 'school'}
        self.assertEqual(sorted(grades, key=int), ['8', '10', '11', '12'])
        for g in grades.values():
            self.assertTrue(g['subjects'])
            self.assertEqual(g['short'], 'Class %s' % g['grade'])
        # the entrance tracks come after the classes, and only with something written
        kinds = [g['kind'] for g in entries]
        self.assertEqual(kinds, sorted(kinds, key=lambda k: k != 'school'))
        for t in syllabus_data.track_entries():
            self.assertEqual(t['kind'], 'entrance')
            self.assertTrue(t['subjects'], t['grade'])
            for s in t['subjects']:
                self.assertGreaterEqual(s['notes_ready'], 1, (t['grade'], s['subject']))

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
        self.assertEqual(data['results'][0]['short'], 'Class 10')

    def test_app_api(self):
        index = self.client.get('/api/syllabus/v2/').json()
        self.assertEqual([g['grade'] for g in index['grades']], ['8', '10', '11', '12'])
        self.assertIn('tracks', index)
        self.assertEqual(index['totals']['grades'], 4)
        unit = self.client.get('/api/syllabus/v2/8/nepali/').json()['units'][0]
        self.assertTrue(unit['topics'])
        legacy = self.client.get('/api/syllabus/subjects/class-10/science/').json()
        self.assertTrue(legacy['chapters'][0]['guide_sections'])
        self.assertEqual(legacy['grade_slug'], 'class-10')


class StudyReaderTests(TestCase):
    """The chapters and question banks exported from the books (notes/tools/export_study.py)."""

    def test_every_subject_has_its_chapters_and_a_bank(self):
        for g in syllabus_data.school_entries():
            for s in g['subjects']:
                idx = study_data.subject_index(g['grade'], s['subject'])
                self.assertEqual(len(idx['units']), s['unit_count'], (g['grade'], s['subject']))
                self.assertTrue(idx['banks'], (g['grade'], s['subject']))

    def test_every_track_subject_has_a_chapter(self):
        """Entrance books are listed while they are being written, but never empty."""
        for g in syllabus_data.track_entries():
            for s in g['subjects']:
                idx = study_data.subject_index(g['grade'], s['subject'])
                self.assertTrue(idx['units'], (g['grade'], s['subject']))

    def test_reader_pages(self):
        page = self.client.get('/app/syllabus/11/physics/unit-3/')
        self.assertContains(page, '<h1 class="rd-title">Kinematics</h1>', html=False)
        self.assertContains(page, 'class="mcq"')
        self.assertContains(page, '<details class="ans')
        self.assertContains(page, 'href="/app/syllabus/11/physics/unit-4/"')
        self.assertContains(page, 'data-rd-label="Class 11 · Physics"')
        self.assertNotContains(page, 'data-rd-exam-min')
        self.assertEqual(self.client.get('/app/syllabus/10/nepali/bank-1/').status_code, 200)
        self.assertEqual(self.client.get('/app/syllabus/12/physics/exam-guide/').status_code, 200)
        self.assertEqual(self.client.get('/app/syllabus/11/physics/unit-99/').status_code, 404)

    def test_crumbs_switch_class_subject_and_unit(self):
        """The breadcrumb is also the switcher, so every target its popups offer
        has to be live, and the trigger has to show its own value only."""
        html = self.client.get('/app/syllabus/11/physics/unit-3/').content.decode()
        nav = re.search(r'<nav class="st-crumbs".*?</nav>', html, re.S).group(0)
        self.assertEqual(re.findall(r'aria-label="(Choose [^"]+)"', nav),
                         ['Choose class', 'Choose subject', 'Choose unit'])
        self.assertIn('<a class="st-pick-o is-current" role="menuitem" href="/app/syllabus/11/">Class 11</a>', nav)
        self.assertIn(' href="/app/syllabus/11/physics/">Physics</a>', nav)
        self.assertIn('>Unit 3 · Kinematics</a>', nav)
        self.assertIn('<span class="st-pick-t">Physics</span>', nav)
        for url in re.findall(r'href="([^"]+)"', nav):
            self.assertEqual(self.client.get(url).status_code, 200, url)

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
        self.assertIsNone(ch['exam'])
        self.assertEqual(self.client.get('/api/syllabus/v2/12/english/bank/1/').status_code, 200)
        self.assertEqual(self.client.get('/api/syllabus/v2/12/english/guide/').status_code, 200)


# ---------------------------------------------------------------------------------------------
# Entrance tracks, on a small fixture in the shape notes/tools/export_syllabus.py and
# export_study.py write: one class (11) and the CEE track with a subject book and the model
# papers, whose paper carries the timed-test rules.

CEE = {"label": "CEE · MECEE-BL Medical Entrance", "label_ne": "CEE प्रवेश परीक्षा",
       "exam": "Medical Education Common Entrance Examination, Bachelor Level (MEC)",
       "short": "CEE", "kind": "entrance", "grade": "cee"}
PAPER = ("3 hours, 200 single-best-answer MCQs with four options, 200 marks, 0.25 deducted per wrong answer"
         " | Zoology 40x1=40 | Botany 40x1=40 | Chemistry 50x1=50 | Physics 50x1=50 | Mental Agility Test 20x1=20")
EXAM = {"minutes": 180, "negative": 0.25}


def _unit(no, title, area, questions, notes, topics, hours=None):
    return {"no": no, "title": title, "hours": hours, "questions": questions, "area": area, "topics": topics,
            "sections": [{"no": "%d.1" % no, "title": topics[0]}] if notes else [],
            "summary": ["Range is greatest at 45 degrees for a projectile on level ground."] if notes else [],
            "terms": ["Projectile"] if notes else [], "stats": {"words": 900 if notes else 0, "figures": 0, "examples": 2},
            "has_notes": notes}


def _card(subject, name, name_ne, icon, group, color, units, questions):
    return {"subject": subject, "name": name, "name_ne": name_ne, "icon": icon, "group": group, "color": color,
            "lang": "en", "hours": None, "unit_count": len(units),
            "topic_count": sum(len(u["topics"]) for u in units),
            "notes_ready": sum(1 for u in units if u["has_notes"]), "questions": questions}


def _doc(no, title, area, html, toc, exam=None):
    doc = {"no": no, "file_no": no, "title": title, "area": area, "hours": "10", "lang": "en", "words": 900,
           "read_min": 5, "figures": 0, "examples": 0, "has_questions": False, "toc": toc, "html": html}
    if exam:
        doc["exam"] = dict(exam)
    return doc


PHY_UNITS = [_unit(1, "Vectors and Kinematics", "Mechanics", 10, True, ["Scalars and vectors", "Projectile motion"]),
             _unit(2, "Nuclear Physics", "Modern Physics", 12, False, ["Binding energy", "Radioactive decay"])]
MOCK_UNITS = [_unit(1, "The MECEE-BL Examination: Pattern, Weightage and Strategy", "The Examination", None, False,
                    ["The paper and its marking"]),
              _unit(2, "Model Paper 1", "Full Model Papers", 200, True, ["Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20"])]
SCHOOL_UNITS = [_unit(1, "Physical Quantities", "Mechanics", None, True, ["Units", "Dimensions"], hours=8)]

PAPER_HTML = (
    '<p><strong>Instructions.</strong> 3 hours; 0.25 is deducted for each wrong answer.</p>\n'
    '<h2 id="s1">Zoology (questions 1–2)</h2>\n<ol class="mcq">\n'
    '<li data-key="b">Which blood cells produce antibodies?<span class="opts c4"><span class="opt"><i>a</i>Neutrophils</span>'
    '<span class="opt"><i>b</i>Plasma cells</span><span class="opt"><i>c</i>Erythrocytes</span><span class="opt"><i>d</i>Platelets</span></span></li>\n'
    '<li data-key="c">The functional unit of the kidney is the<span class="opts c4"><span class="opt"><i>a</i>neuron</span>'
    '<span class="opt"><i>b</i>alveolus</span><span class="opt"><i>c</i>nephron</span><span class="opt"><i>d</i>villus</span></span></li>\n</ol>\n'
    '<h2 id="s2">Physics (question 3)</h2>\n<ol class="mcq" start="3">\n'
    '<li data-key="c">The SI unit of power is the<span class="opts c4"><span class="opt"><i>a</i>joule</span>'
    '<span class="opt"><i>b</i>newton</span><span class="opt"><i>c</i>watt</span><span class="opt"><i>d</i>pascal</span></span></li>\n</ol>\n'
    '<h2 id="s3">Answer key and explanations</h2>\n'
    '<details class="ans box note"><summary>Answers — Zoology (1–2)</summary><div class="ans-body">'
    '<p class="ansline"><strong>1.</strong> (b) — plasma cells secrete antibodies.</p>'
    '<p class="ansline"><strong>2.</strong> (c) — the nephron.</p></div></details>\n'
    '<details class="ans box note"><summary>Answers — Physics (3)</summary><div class="ans-body">'
    '<p class="ansline"><strong>3.</strong> (c) — one watt is one joule per second.</p></div></details>')
PAPER_TOC = [{"id": "s1", "title": "Zoology (questions 1–2)", "kind": ""}, {"id": "s2", "title": "Physics (question 3)", "kind": ""},
             {"id": "s3", "title": "Answer key and explanations", "kind": ""}]


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)


def _clear_caches():
    syllabus_data.index.cache_clear()
    syllabus_data.subject.cache_clear()
    study_data.subject_index.cache_clear()
    study_data._read.cache_clear()
    views_syllabus._search_rows.cache_clear()


class EntranceTrackTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmp = tempfile.mkdtemp(prefix="neb-syllabus-")
        syl, study = os.path.join(cls.tmp, "syllabus"), os.path.join(cls.tmp, "study")
        school = {"label": "Class 11", "label_ne": "कक्षा ११", "exam": "NEB Grade 11 examination",
                  "short": "Class 11", "kind": "school", "grade": "11"}
        phy11 = dict(_card("physics", "Physics", "भौतिक विज्ञान", "bolt", "science", "#4A42D6", SCHOOL_UNITS, None), hours=8)
        phy11.pop("questions")
        phy = _card("physics", "Physics", "भौतिक विज्ञान", "bolt", "entrance", "#4A42D6", PHY_UNITS, 50)
        mock_ = _card("model-papers", "Model Papers and Mock Tests", "नमुना प्रश्नपत्र तथा अभ्यास परीक्षा", "quiz",
                      "practice", "#B02A5B", MOCK_UNITS, 200)
        _write(os.path.join(syl, "index.json"), {"grades": [dict(school, subjects=[phy11]), dict(CEE, subjects=[phy, mock_])]})
        _write(os.path.join(syl, "11-physics.json"), dict(
            {k: phy11[k] for k in ("subject", "name", "name_ne", "icon", "group", "color", "lang")},
            grade="11", grade_label="Class 11", grade_label_ne="कक्षा ११", code="1021", hours=8, exam="", areas=["Mechanics"],
            units=SCHOOL_UNITS, unit_count=1, topic_count=2, notes_ready=1))
        for card, units in ((phy, PHY_UNITS), (mock_, MOCK_UNITS)):
            _write(os.path.join(syl, "cee-%s.json" % card["subject"]), dict(
                {k: card[k] for k in ("subject", "name", "name_ne", "icon", "group", "color", "lang", "hours", "questions")},
                grade="cee", grade_label=CEE["label"], grade_label_ne=CEE["label_ne"], short="CEE", kind="entrance",
                code="", exam=PAPER, areas=sorted({u["area"] for u in units}, key=[u["area"] for u in units].index),
                units=units, unit_count=len(units), topic_count=card["topic_count"], notes_ready=card["notes_ready"]))
        _write(os.path.join(study, "cee-physics", "index.json"), {"book": "cee-phy", "units": [
            {"no": 1, "title": "Vectors and Kinematics", "area": "Mechanics", "words": 900, "read_min": 5, "figures": 0,
             "has_questions": True}]})
        _write(os.path.join(study, "cee-physics", "unit-01.json"), _doc(
            1, "Vectors and Kinematics", "Mechanics",
            '<h2 id="s1">1.1 Scalars and vectors</h2><p>A projectile on level ground goes furthest at 45 degrees.</p>',
            [{"id": "s1", "title": "1.1 Scalars and vectors", "kind": ""}]))
        _write(os.path.join(study, "cee-model-papers", "index.json"), {"book": "cee-mock", "units": [
            {"no": 2, "title": "Model Paper 1", "area": "Full Model Papers", "words": 900, "read_min": 5, "figures": 0,
             "has_questions": False, "exam": dict(EXAM)}]})
        _write(os.path.join(study, "cee-model-papers", "unit-02.json"), _doc(
            2, "Model Paper 1", "Full Model Papers", PAPER_HTML, PAPER_TOC, EXAM))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        for target, sub in ((syllabus_data, "syllabus"), (study_data, "study")):
            patcher = mock.patch.object(target, "DATA_DIR", os.path.join(self.tmp, sub))
            patcher.start()
            self.addCleanup(patcher.stop)
        _clear_caches()
        self.addCleanup(_clear_caches)

    def test_track_keys_are_grades(self):
        self.assertEqual(syllabus_data.normalize_grade("cee"), "cee")
        self.assertEqual(syllabus_data.normalize_grade("CEE"), "cee")
        self.assertIsNone(syllabus_data.normalize_grade("ioe"))
        data = syllabus_data.subject("cee", "physics")
        self.assertEqual((data["kind"], data["short"], data["library_grade"]), ("entrance", "CEE", "Entrance Prep"))
        school = syllabus_data.subject("11", "physics")
        self.assertEqual((school["kind"], school["short"], school["questions"]), ("school", "Class 11", None))

    def test_hub_lists_the_classes_then_the_tracks(self):
        page = self.client.get('/app/syllabus/').content.decode()
        buttons = re.findall(r'data-syl-grade="([^"]+)" aria-selected="(true|false)"[^>]*>([^<]+)</button>', page)
        self.assertEqual([(g, label) for g, _, label in buttons], [("11", "Class 11"), ("cee", "CEE")])
        self.assertEqual([g for g, sel, _ in buttons if sel == "true"], ["11"])   # a class, not the track, by default
        self.assertLess(page.index('data-syl-grade="11"'), page.index('class="syl-grade-sep"'))
        self.assertLess(page.index('class="syl-grade-sep"'), page.index('data-syl-grade="cee"'))
        self.assertIn('Exam subjects', page)
        self.assertIn('Model papers and mock tests', page)
        self.assertIn('1 of 2 chapters written · 50 questions in the paper', page)
        self.assertIn('href="/app/syllabus/cee/physics/"', page)
        self.assertNotIn('Class cee', page)
        self.assertIn('aria-selected="true"', self.client.get('/app/syllabus/cee/').content.decode().split('data-syl-grade="cee"')[1][:40])

    def test_track_subject_page(self):
        page = self.client.get('/app/syllabus/cee/physics/')
        self.assertContains(page, '2 chapters · 50 questions in the paper · 1 written so far')
        self.assertContains(page, '10 questions in the paper · 5 min read')
        self.assertContains(page, 'href="/app/syllabus/cee/physics/unit-1/"')
        self.assertContains(page, 'Where the questions are')
        self.assertContains(page, '10 Qs')
        self.assertContains(page, 'data-st-word="Chapter"')
        self.assertContains(page, '<title>CEE Physics — Entrance Preparation Notes, MCQs and Weightage | NEBians</title>', html=False)
        self.assertNotContains(page, 'Class cee')
        self.assertNotContains(page, 'teaching hours')
        self.assertEqual(self.client.get('/app/syllabus/CEE/physics/').status_code, 301)
        self.assertEqual(self.client.get('/app/syllabus/ioe/physics/').status_code, 404)

    def test_model_papers_page_and_reader(self):
        page = self.client.get('/app/syllabus/cee/model-papers/')
        self.assertContains(page, 'Timed test · 180 min · 200 questions')
        self.assertNotContains(page, 'Where the questions are')
        reader = self.client.get('/app/syllabus/cee/model-papers/unit-2/')
        self.assertContains(reader, 'data-rd-exam-min="180"')
        self.assertContains(reader, 'data-rd-exam-neg="0.25"')
        self.assertContains(reader, 'data-rd-label="CEE · Model Papers and Mock Tests"')
        self.assertContains(reader, 'data-rd-key="cee/model-papers/unit2"')
        self.assertContains(reader, 'Chapter 2 · Full Model Papers · 200 questions in the paper')
        self.assertContains(reader, '<li data-key="b">')
        self.assertNotContains(reader, 'Class cee')
        chapter = self.client.get('/app/syllabus/cee/physics/unit-1/')
        self.assertContains(chapter, '10 questions in the paper')
        self.assertNotContains(chapter, 'data-rd-exam-min')
        self.assertContains(chapter, 'CEE Physics Entrance Notes and MCQs')

    def test_track_crumbs_offer_classes_and_tracks(self):
        """Entrance books say "chapter", and the class popup lists the school
        classes and the tracks side by side."""
        html = self.client.get('/app/syllabus/cee/physics/unit-1/').content.decode()
        nav = re.search(r'<nav class="st-crumbs".*?</nav>', html, re.S).group(0)
        self.assertIn('aria-label="Choose chapter"', nav)
        self.assertIn('<a class="st-pick-o is-current" role="menuitem" href="/app/syllabus/cee/">CEE</a>', nav)
        self.assertIn('<a class="st-pick-o" role="menuitem" href="/app/syllabus/11/">Class 11</a>', nav)
        self.assertIn('>Chapter 1 · Vectors and Kinematics</a>', nav)

    def test_api_index_splits_classes_and_tracks(self):
        data = self.client.get('/api/syllabus/v2/').json()
        self.assertEqual([g['grade'] for g in data['grades']], ['11'])
        self.assertEqual([t['grade'] for t in data['tracks']], ['cee'])
        self.assertEqual((data['tracks'][0]['short'], data['tracks'][0]['kind']), ('CEE', 'entrance'))
        self.assertEqual(data['tracks'][0]['subjects'][0]['questions'], 50)
        self.assertEqual((data['totals']['grades'], data['totals']['tracks']), (1, 1))

    def test_api_subject_and_paper(self):
        doc = self.client.get('/api/syllabus/v2/cee/physics/').json()
        self.assertEqual((doc['kind'], doc['short'], doc['questions']), ('entrance', 'CEE', 50))
        self.assertEqual((doc['units'][0]['questions'], doc['units'][0]['hours']), (10, None))
        self.assertEqual([u['has_chapter'] for u in doc['units']], [True, False])
        papers = self.client.get('/api/syllabus/v2/cee/model-papers/').json()
        self.assertEqual(papers['units'][1]['exam'], EXAM)
        self.assertIsNone(papers['units'][0]['questions'])
        paper = self.client.get('/api/syllabus/v2/cee/model-papers/unit/2/').json()
        self.assertEqual(paper['exam'], EXAM)
        self.assertIn('data-key="c"', paper['html'])
        self.assertIsNone(self.client.get('/api/syllabus/v2/cee/physics/unit/1/').json()['exam'])

    def test_search_names_the_track(self):
        data = self.client.get('/app/syllabus/search/', {'q': 'projectile', 'grade': 'cee'}).json()
        self.assertTrue(data['results'])
        hit = data['results'][0]
        self.assertEqual((hit['grade'], hit['short'], hit['kind'], hit['subject']), ('cee', 'CEE', 'entrance', 'physics'))
        api = self.client.get('/api/syllabus/v2/search/', {'q': 'projectile', 'tracks': '1'}).json()
        self.assertIn('CEE', [r['short'] for r in api['results']])
        # installed app versions (no tracks=1) print every hit as "Class N": they get the classes only
        old_app = self.client.get('/api/syllabus/v2/search/', {'q': 'projectile', 'grade': '11'}).json()
        self.assertTrue(old_app['results'])
        self.assertEqual({r['kind'] for r in old_app['results']}, {'school'})
        from_track = self.client.get('/api/syllabus/v2/search/', {'q': 'projectile', 'grade': 'cee'}).json()
        self.assertEqual(from_track['results'][0]['grade'], 'cee')

    def test_legacy_api_slugs(self):
        detail = self.client.get('/api/syllabus/subjects/cee/physics/').json()
        self.assertEqual(detail['grade_slug'], 'cee')
        self.assertEqual([g['slug'] for g in detail['grade_list']], ['cee'])
        self.assertEqual([g['slug'] for g in self.client.get('/api/syllabus/subjects/class-11/physics/').json()['grade_list']],
                         ['class-11'])
        # pre-v2 app versions slugify a category's label to open it: they get the classes only
        cats = self.client.get('/api/syllabus/categories/').json()['categories']
        self.assertEqual([c['grade'] for c in cats], ['Class 11'])
        self.assertTrue(detail['chapters'][0]['name'].startswith('Chapter 1:'))
        self.assertEqual(self.client.get('/api/syllabus/subjects/class-11/physics/').json()['grade_slug'], 'class-11')

    def test_share_cards_name_the_track(self):
        from web import views_og
        card = views_og._syllabus_subject_card('cee/physics')
        self.assertEqual(card['kicker'], 'CEE entrance')
        self.assertIn('50 questions in the paper', card['meta'])
        self.assertEqual(views_og._syllabus_chapter_card('cee/physics/1')['kicker'], 'Chapter 1')
        self.assertEqual(views_og._syllabus_grade_card('cee')['kicker'], 'Entrance preparation')
