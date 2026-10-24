# Entrance-examination and bachelor books — handoff (start here)

Branch: **`resources/entrance-and-bachelor`** (from `main` @ `1dafb80d`). Push with
`notes/tools/lockpush.sh "message" <paths…>` (serialised commit + push of only the
paths named; the clone's `origin` already carries a token). Never `git add -A`:
`notes/figures/` is the render cache and is excluded locally.

Started 2026-10-24 ~20:00 UTC by an AgentSky Claude session. The owner's brief:
research and write the best free preparation material in Nepal for **CEE (MECEE-BL)**
first, then the **other entrance examinations** (IOE engineering, BSc CSIT, BCA, …),
then **bachelor courses** (BCA, CSIT, …) — notes, PDFs, syllabus, interactive
practice, practice sets, explained solutions, predicted and model papers. Push often;
keep this file current so a new session can continue mid-stream.

## Web and app integration

Done 2026-10-24 20:40–23:20 UTC (integration session; three parallel forks: exporters +
backend, web timed mode, Android). Everything below is pushed to this branch.

**What works**

- **Export.** `notes/tools/export_syllabus.py` exports every book whose slug is a track
  (`spine.track_of`). A track joins `web/data/syllabus/index.json` after the school grades
  as an entry like a grade: `grade` = track key (`cee`), `label`/`exam` from
  `spine.TRACKS`, `short` = `CEE`, `kind` = `entrance`; school entries now also carry
  `short` (`Class 8`) and `kind` (`school`). Subject keys, Nepali names, icons and groups
  are in `TRACK_SUBJECTS` there (physics, chemistry, zoology, botany, mental-agility-test,
  mathematics, english, computer-knowledge, general-knowledge-it → group `entrance`;
  model-papers → group `practice`). A track's units carry `questions` (the spine's `[n]`)
  with `hours: null`; the subject carries `questions` from the spine header `QUESTIONS:`.
  A subject is listed only once `notes/content/<slug>/` has a chapter; a track only once it
  has such a subject. Files: `web/data/syllabus/cee-physics.json` etc.
  `notes/tools/export_study.py` writes `web/data/study/<track>-<subject key>/`
  (`cee-physics/`); with no arguments it runs the school list and then every track book
  with a chapter. A unit of a `*-mock` book whose spine tag is a number (a model paper,
  not the `[Guide]`) gets `"exam": {"minutes", "negative"}` (from `TRACKS`) in its JSON and
  on its item in the folder's `index.json`. School output is byte-identical: export_syllabus
  school files unchanged (index.json only gains `short`/`kind`); export_study `cs10` and
  `eco10` diffed clean before/after in this environment.
- **Backend** (`web/syllabus_data.py`, `views_syllabus.py`, `views_og.py`,
  `api/views_syllabus.py`, templates `syllabus/_hub.html`, `hub.html`, `subject.html`,
  `reader.html`, `css/pages/syllabus.css`, `js/syllabus.js`). Grade keys come from
  index.json (`grade_keys()`, `is_school()`, `school_entries()`, `track_entries()`);
  `library_grade` of a track is "Entrance Prep". API `/api/syllabus/v2/` returns `grades`
  (school only; installed apps print every entry as "Class N"), `tracks` (entrance
  entries) and `totals` (`grades` = school count, new `tracks`). Doc endpoints add `exam`
  (null when absent); subject endpoint units add `exam`; search hits add `short`/`kind`
  (a search from a track ranks entrance books first, from a class the classes). Web hub:
  the classes, a hairline, then the tracks (buttons print `short`; on a phone the tracks
  get their own row); group titles "Exam subjects" / "Model papers and mock tests"; cards
  and subject pages say "N questions in the paper" ("5 of 22 chapters written" while a
  book is incomplete); the exam tab's weightage panel is "Where the questions are"
  (question count per area, or per chapter when there is one area); model-paper rows read
  "Timed test · 180 min · 200 questions"; entrance books say "Chapter N"; SEO titles and
  share cards name the track ("CEE Physics — Entrance Preparation Notes, MCQs and
  Weightage"); the legacy API builds `class-N` slugs only for school grades.
- **Timed model-paper mode, web.** `static/web/js/study-exam.js` (loaded by `reader.html`
  only when the chapter has `exam`; the root carries `data-rd-exam-min`/`-neg`), hooks in
  `study-reader.js` (`window.NebReader`), styles in `css/pages/study-reader.css`. "Take as a
  timed test" → intro (questions, time, +1 / −negative / 0, no pause) → test mode: keys,
  folded answers and answer-key-only sections hidden; one option per question, changeable,
  per-question Clear; bar with countdown (red in the last 5 min), answered/unanswered,
  question palette by section (sheet on phones), Submit (confirms blanks). Deadline is
  absolute and kept in `localStorage["neb.exam.v1"][docKey] = {s, e, n, a, f, o}`; a
  deadline passed while away submits on load. Result: score (right − negative × wrong),
  right/wrong/blank, accuracy, time used, per-section table (the h2 each list sits under),
  then keys marked, wrong picks red, blanks flagged, explanations open; Retake / Back to
  practice. The last result is also saved as NebStudy doc `x`. Practice mode unchanged.
- **Android** (`SyllabusModels.kt`, `SyllabusHub.kt`, `SyllabusSubject.kt`,
  `SyllabusViewModel.kt`, `StudyReader.kt`, `StudyReaderPage.kt`, `StudyProgress.kt`).
  Models gain `tracks`, `short`, `kind`, `questions`, `ApiStudyDoc.exam`
  (`ApiStudyExam(minutes, negative)`), `ApiSyllabusHit.short`; helpers `isSchoolGrade`,
  `syllabusShort` (never "Class cee"). Hub: one scrolling row, classes, a hairline, then
  tracks ("CEE" over "Entrance"); a remembered track stays selected; group titles and
  "N chapters · N questions" as on the web; search badge from `short`, "Chapter N" for
  tracks. Subject screen: questions in the paper, question weightage, Chapter wording.
  Reader: the app bundles its own script, so the timed mode is ported into
  `StudyReaderPage.kt` (`EXAM_JS`, `EXAM_CSS`): same behaviour as the web; state goes
  through the bridge (`NebStudy.examSave`) into `StudyProgress` (`x:<doc key>`) and back
  as `NEB_EXAM_STATE`, so it survives reloads, rotation and restarts; `NebStudy.exam(on)`
  hides "Show answers" while a test runs; Back closes the palette/intro sheets first.
- **Data committed:** CEE physics 5, chemistry 6, zoology 4, botany 4, mental agility 3
  chapters at first export (see the latest "syllabus + study export" commit for the
  current numbers); `cee-mock` had no chapter yet, so no model paper is live.

**How it was tested**

- `cd backend_python && DEBUG=True SECRET_KEY=local-check-key DB_ENGINE=sqlite
  ALLOWED_HOSTS_GLOB=testserver,localhost,127.0.0.1 python3 manage.py test
  web.test_syllabus web.test_icon_font` → 20 tests OK, with the real data. The track tests
  build their own fixture (a CEE physics book and a timed model paper) in a temp dir, so
  they keep working whatever has been exported. (The whole web+api suite has 12 failures
  in test_lazy_tools, test_neby_looks, test_security_hardening and test_proxy_http; the
  same 12 fail on the base commit 03f0d9a9.)
- Playwright (headless Chromium) against `runserver` with a 7-question model-paper fixture:
  hub desktop/phone, CEE subject page, chapter reader (tap-to-check), timed test 4 right,
  2 wrong, 1 blank → 3.5 / 7 with the per-section table, the deadline kept across a
  reload, the key hidden during the test and every explanation open after Submit; a
  200-question paper at 390×844 (the forks' harnesses, numbers checked).
- Android: not compiled here. The page script was tested in a harness assembled from the
  raw strings in `StudyReaderPage.kt` with a stub bridge (start, pick/change/clear,
  palette, reload, submit 2.5 / 7, time-out, retake, practice, dark mode). Kotlin files were
  re-read and checked for template-free `const val` strings.

**Left / TODO**

1. **Android CI build** (`Build Student Release APKs & AAB` on this branch). Spots a
   compiler could still object to: `SyllabusHub.kt` `GradeSwitch` (Dp arithmetic inside
   `BoxWithConstraints`), `StudyReader.kt` (bridge methods `exam`/`examSave`,
   `LaunchedEffect(state.key)`), `StudyReaderPage.kt` (`JSONObject.quote`,
   `JSONObject().put("negative", Double)`).
2. **Re-export as chapters land** — from a clean checkout of HEAD, because writers keep
   half-written chapters in the shared tree:
   `git worktree add --no-checkout --detach /tmp/neb-exp HEAD && cd /tmp/neb-exp && git
   sparse-checkout set notes/pipeline notes/tools notes/curriculum notes/content
   notes/assets backend_python/web/data/syllabus && git checkout`, then
   `python3 notes/tools/export_syllabus.py && python3 notes/tools/export_study.py cee-phy
   cee-chem …` (only books with chapters), copy `backend_python/web/data/syllabus/`
   (index.json + `<track>-*.json`), `backend_python/web/data/study/<track>-*/` and the new
   files of `backend_python/web/static/web/study/` back into the clone, lockpush exactly
   those paths, `git worktree remove --force /tmp/neb-exp`. Never commit the untracked
   media that writers' `mcqcheck.py` runs leave in `web/static/web/study/` unless an
   exported JSON references them.
3. **First real model paper** (`cee-mock` unit 2): check it on a phone in both the site
   and the app — 200 questions, the palette and the result table — and that its key
   boxes are found (`export_study._mcq_keys(far=True)`; mcqcheck must show every MCQ keyed).
4. The app's subject list does not yet mark which chapters are timed papers
   (`units[].exam` is in the subject API; `ApiSyllabusUnit` has no `exam` field yet).
5. IOE / CSIT / BCA need no code: a track appears once its spines and a chapter exist
   (button order = `TRACKS` order). Keep `TRACK_SUBJECTS` in `export_syllabus.py` in step
   with `spine.TRACK_SUBJECTS` if a new subject code is added.
6. Pre-existing, outside this work: `web/static/web/vendor/katex/fonts/` holds 7 of the 16
   KaTeX fonts the CSS asks for (the rest 404 on the site; the app bundles its own).

## What exists (update the table as work lands)

| Book slug | Spine | Chapters written | PDF | Web export |
|---|---|---|---|---|
| cee-phy | `notes/curriculum/cee-phy.md` (22 ch, 50 Qs) | see `notes/content/cee-phy/` | — | — |
| cee-chem | `cee-chem.md` (22 ch, 50 Qs) | | — | — |
| cee-zoo | `cee-zoo.md` (14 ch, 40 Qs) | | — | — |
| cee-bot | `cee-bot.md` (15 ch, 40 Qs) | | — | — |
| cee-mat | `cee-mat.md` (5 ch, 20 Qs) | | — | — |
| cee-mock | `cee-mock.md` (guide + 5 model papers of 200) | | — | — |
| ioe-* | not yet | | | |
| csit-* / bca-* | not yet | | | |

Always check reality with `ls notes/content/<slug>/` and `git log --oneline`.

## Sources (authoritative; copies in `notes/sources/entrance/`)

- **MEC syllabus, third revision 2083-01-15 (28 Apr 2026)** —
  `MEC-MECEE-BL-syllabus-3rd-revision-2026-04-28.pdf` (mirrored by edusanjal
  `media.edusanjal.com/c/New%20Syllabus%20MECEE-BL%20Entrance%20Examination.pdf`;
  mec.gov.np returns 502 from this pod). 200 MCQs, 3 h, −0.25 per wrong answer, merit
  from the 50th percentile, recall:understanding:application 50:30:20, stems ≤ 60
  words. Group I (MBBS/BDS/BSc Nursing/BASLP/B Perfusion): Zoology 40 (3/4/4/6/15/4/2/2),
  Botany 40 (2/9/4/5/6/3/6/2/3), Chemistry 50 (17/10/17/3/3), Physics 50
  (10/7/8/9/4/12), MAT 20 (5/5/5/5). Group II (BAMS, BPharm, MLT…) Chemistry 40,
  Physics 40 + 20 PCL-specific. The second revision (2082-05-02) had different domains —
  do not use it.
- **IOE BE/BArch entrance syllabus 2083** — `IOE-BE-BArch-entrance-syllabus-2083.pdf`
  (same as 2081/2082 except the year). Booklet 2083 (Preeti-encoded; decode with
  `notes/tools/preeti2unicode.py`): computer-based, 2 hours, 100 questions = 60 × 1 +
  40 × 2 = 140 marks, 10 % of a question's marks deducted for a wrong answer.
  Mathematics 50, Physics 40, Chemistry 30, English 20. The per-subject split of
  1- and 2-mark questions is not in the official document (third-party sites:
  Maths 20+15, Physics 14+13, Chemistry 14+8, English 12+4 — consistent with 60/40).
- **BSc CSIT (IOST) model question** — `IOST-BSc-CSIT-entrance-model-question.pdf`:
  100 MCQs, 2 hours, Mathematics 25, Physics 25, Chemistry 25, English 15, Computer 10.
- **BCA (FOHSS)**: 100 MCQs, 2 hours; Mathematics 50, English 40, GK & IT 10 (third
  party, consistent across sites; confirm on entrance.tufohss.edu.np when reachable).

## How the books are made

- Contract: `notes/AUTHORING-ENTRANCE.md` (on top of `notes/AUTHORING.md`).
- Slugs `<track>-<subject>`; `notes/pipeline/spine.py` `TRACKS` / `TRACK_SUBJECTS`
  (cover line, exam minutes and negative marking); `i18n.ENTRANCE_EN` (book furniture:
  "Chapter", "questions in the paper"); `spine.pdf_name()` →
  `notes/pdf/NEBians-CEE-Entrance-Physics.pdf` etc.
- Spine `[n]` = questions in the paper for that chapter (area totals official,
  per-chapter split = our estimate, stated in the spine header and the book).
- Checks per chapter: `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md`
  (must print OK) and `python3 notes/tools/mcqcheck.py notes/content/<slug>/unit-NN.md`
  (every MCQ keyed; key-letter spread).
- Build a book: `cd notes/pipeline && python3 build_pdf.py cee-phy` → `notes/pdf/`.
- Web/app export (after a book changes): `python3 notes/tools/export_syllabus.py` and
  `python3 notes/tools/export_study.py cee-phy …` (entrance books key MCQ lists that start
  at any number from a later answer box — `export_study._mcq_keys(far=True)`).

## Process that works

Parallel writer subagents (Agent tool), 4–5 at a time, each given 3–6 chapters of one
book with the brief in this file's "Writer brief" section; each writes → check.py →
mcqcheck → looks at figure PNGs → `lockpush.sh` per chapter. The coordinator reviews
(spot-checks keys by recomputing), builds PDFs one book at a time, exports for the
web, updates this file, pushes.

## Writer brief (paste into an Agent prompt, fill in the slug and units)

> You are writing chapters of a free entrance-preparation book in the NEBians repo at
> /data/workspace/NEB (branch resources/entrance-and-bachelor, environment ready:
> matplotlib, fonts, check.py). Book: <slug>; write units <list>, in this order, one at a
> time. Read fully first: notes/AUTHORING-ENTRANCE.md, then notes/AUTHORING.md §3–6,
> §11–12 (§14 for biology), the spine notes/curriculum/<slug>.md, and the official
> syllabus text (CEE: notes/sources/entrance/MEC-…pdf, or the extracted text in
> /data/workspace/task/sources/mec-2026.txt). Use the NEBians Grade 11/12 book chapters
> (notes/content/phy11, phy12, chem11, chem12, bio11, bio12, math11, math12) for
> curriculum terms, but write denser, MCQ-first material. After each chapter: check.py
> OK, mcqcheck OK, figures PNG-inspected, then lockpush it. Verify every numerical key
> in Python. Do not start a new chapter after <deadline UTC> (`date -u`); finish and
> push the one in progress. Report briefly per chapter: words, figures, MCQs, status.

## Next steps (keep ordered)

1. Finish CEE: all chapters of cee-phy, cee-chem, cee-zoo, cee-bot, cee-mat; cee-mock
   unit 1 (exam guide) and five model papers.
2. Build the six CEE PDFs; export syllabus + study JSON; check the reader keys.
3. IOE spines (`ioe-math`, `ioe-phy`, `ioe-chem`, `ioe-eng`, `ioe-mock`) from the 2083
   syllabus → chapters → PDFs → export.
4. CSIT (`csit-*`, incl. `csit-comp`) and BCA (`bca-math`, `bca-eng`, `bca-gk`, mocks).
5. Bachelor programmes (first semesters of BSc CSIT and BCA first), as new tracks.
6. Web + Android: entrance tracks in the syllabus hub (API `tracks` key for
   backward compatibility), timed model-paper mode in the reader.

## Session log

- 2026-10-24 20:00–20:45 UTC — recon, toolchain (WeasyPrint 70, matplotlib 3.11.2,
  fonts), official syllabi found and saved, pipeline track support, CEE spines,
  authoring contract, mcqcheck, lockpush; first wave of writers dispatched.
