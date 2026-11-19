# Past paper requests: status and pickup (session 125 onward)

Read `notes/papers/PAPERS_TRACKER.md` for the paper pipeline itself. This file tracks the three open student requests so the next session does not repeat research.

## Live check (session 125, after the first publish)

`Publish Past Papers to Library` ran for real (run 44628389901, `4 created, 0 refreshed, 0 failed`; dry run before it, run 44628242579). Verified on the live API (`/api/resources/?type=Past%20Paper&search=Computer%20Engineering`): the three papers and the bundle are listed, the PDF (`/media/papers/12-vp-2080-9341.pdf`, 200) and the cover (200) load. The library already holds an upload `NEB Grade 12 Computer Engineering Board Question Papers (All Subjects) 2083 (2026)` (not ours, raw papers): do not duplicate 2083, only add solved papers.

## Request 1: Class 12 technical stream, Computer Engineering, board papers 2078/79

**Session 126 re-check (do not repeat):** the dhanraj.com.np feed search ignores `q` and returns the same list, and it only holds 2080 technical papers (the same three CE subjects plus shared Physics 913, Social Studies technical). Web search found no 2078 or 2079 technical Computer Engineering board paper anywhere (only TU Digital Logic and general Computer Science 2078, which are different). Physics Technical 2080 (`12-phy-2080-9131`) is already built. Ask the requester which exact old-course subjects he needs and whether he can send photos of the paper; until then the 2080 set is the closest official material.

**Research result (do not repeat).**
- The Computer Engineering technical subjects are Visual Programming (9341), Web Development and Database (656 old, new code not yet seen), Software Engineering and Project Management (9371), plus the shared technical Physics 9131, Chemistry 9111, Mathematics 4021 and English/Nepali.
- The new technical course starts with registration 79, so its first board sitting is 2080. A 2078 or 2079 technical Computer Engineering paper exists only for the OLD course (registration 76 to 78). No page that carries them was found: dhanraj.com.np starts its Class 12 board papers at 2080 (feed search for 2078, 2079, "Computer Engineering", "Visual Programming" returned nothing older), dhanrajgurung.com is down (HTTP 522), nepalieducate.com and blog.educatenepal.com have only general Computer Science 2079 (already built as `12-cs-2079-4281`) and model sets. nebexam.com "2078" pages are model questions, not the board paper.
- Closest official source found and built this session: the three 2080 (2023) technical Computer Engineering papers below.

**Done (built, visually checked page by page, bundled, listed):**

| Id | Paper | Pages |
| --- | --- | --- |
| `12-vp-2080-9341` | Visual Programming, new course, 50 marks | 8 |
| `12-wdd-2080-656` | Web Development and Database, old course, 50 marks | 6 |
| `12-sepm-2080-9371` | Software Engineering and Project Management, new course, 50 marks | 8 |
| `12-ce-technical-2080-bundle` | All three with cover, contents and bookmarks (`notes/papers/bundle_stream.py`) | 23 |

Stated openly in the PDFs: SEPM MCQ 7 key C is an assumption (the printed options overlap); MCQ 6 key B (three classic maintenance types). VP MCQ 6 key D (structs have no destructor), MCQ 7 key `ref`. Numbers of the PERT example are asserted in `notes/papers/checks/check_sepm_2080_9371.py`. The C#, JavaScript and PHP programs were written by hand, not compiled (no mono or php in the sandbox): compile them in a later session if a compiler is available.

**Pickup list:**
1. Other Computer Engineering technical 2080 subjects on dhanraj.com.np (same `2025/09/...-NEB-Class-12-Question-Paper-2080.html` pattern; list in the links of any 2080 page): Computer Network, Database, and the rest of the technical codes. Only these three were built.
2. Same technical subjects for 2081, 2082 and 2083 (search the feed `GET /feeds/posts/default?q=<subject>&alt=json`).
3. 2078 and 2079 old course technical papers: ask the requester for the exact subject list, or look for scans on nebexam.com, edusanjal.com (`media.edusanjal.com/u/...pdf`) and college sites.
4. Chemistry Technical 9111 and Mathematics Technical 2080 are still queued (tracker).
5. Publish: run the workflow `Publish Past Papers to Library` (below).

## Request 2: Class 11 science mid-term papers (DONE in session 126, ids `11-<subject>-mid-2083`)

Mid-terms are set by each school, so there is no official source. Built five ORIGINAL NEBians practice papers in the NEB new-course pattern (50 marks, 2 hrs: Group A 10 MCQ x 1, Group B 6 x 4, Group C 2 x 8), full solutions, figures, each with a `notes/papers/checks/check_11_<x>_mid_2083.py` that re-derives every number. All pages were looked at on 2x2 sheets; defects found and fixed: orphaned Group B heading (page-break div), multi-`=` display equations the builder splits badly (one equation per `$$`), `$A$1` swallowed as math, split tables, cover art in a fallback font (copy `app/src/main/res/font/poppins_*.ttf` to `~/.fonts/Poppins-Bold.ttf`, `-SemiBold`, `-Regular`).

| Id | Paper | Units | Pages |
| --- | --- | --- | --- |
| `11-phy-mid-2083` | Physics | 1 to 6 (quantities, vectors, kinematics, dynamics, work-energy, circular motion) | 9 |
| `11-chem-mid-2083` | Chemistry | 1 to 5 (fundamentals, stoichiometry, atomic structure, periodic table, bonding) | 6 |
| `11-math-mid-2083` | Mathematics | 1 to 6 (logic and set to matrices) | 7 |
| `11-cs-mid-2083` | Computer Science | 1 to 4 | 7 |
| `11-bio-mid-2083` | Biology | 1 to 4 | 6 |
| `11-science-cs-mid-2083` (listing slug `...-bundle`) | Physics + Chemistry + Maths + Computer Science | | 30 |
| `11-science-bio-mid-2083` (listing slug `...-bundle`) | Physics + Chemistry + Maths + Biology | | 29 |

Tooling added: `build_paper.py` front matter key `kind` (replaces the hard-coded "Past Paper" running head) and empty `code` is allowed; `notes/papers/tools/assemble.py` joins `content/_parts/<id>.<n>.md` into one paper; `bundle_stream.py` now takes `--grade --label --filetag --category`; `tools/publish/build_midterm_listings.py` writes listings (exam_type `Midterm`, type `Past Paper`, author NEBians, honest "original practice paper" text) and covers, merging into `papers_listing.json`. Next mid-term pickup: second paper per subject (units 7 to 12 or a second set), Class 11 English and Nepali, and the Second Terminal papers.

## Publish log (session 126)

`Publish Past Papers to Library`: dry run 44631909592 (`7 created, 0 refreshed, 0 failed`), real run right after (`7 created, 0 refreshed, 0 failed`, `/` and `/api/posts/` answered 200). Live check: `GET /api/resources/?search=Mid-Term` lists all seven (grade_level Class 11, exam_type Midterm, type Past Paper), every PDF and cover returned 200, and the Computer Engineering (5) and BLE SET (4) listings are unchanged, so nothing was deleted or overwritten. Note for the admin: the library also holds an upload `Class 12 Computer Engineering — Internal & Terminal Exams` (not ours).

## Request 3: Class 8 set solutions

Nothing built by us yet and no earlier work exists in the repo (searched `notes/` handoffs, tracker, git log). **Found on the live library:** the requester almost certainly means the BLE (Basic Level Examination) SET solutions. The library already has uploaded `BLE | SET Solutions` PDFs for Class 8 Computer Science, Science and Technology and Health and Physical Education (Health is listed twice, once without a grade, a cleanup for the admin). Missing and the likely ask: Mathematics, English, Nepali, Social Studies and Human Values, Creative Arts. Check them with `GET /api/resources/?search=SET%20Solutions` before building so nothing is duplicated, then build NEBians-solved SET papers (`8-<subject>-set-<n>` ids, `--grade 8` listing, exam_type "BLE SET"). Class 8 has provincial and local-level exams, and the tracker says each province sets its own paper. dhanraj.com.np and nepalieducate.com have no Class 8 posts. Pickup: ask the requester which province and which subject set, search local-level (Bagmati, Gandaki, Lumbini) Class 8 sets, then solve with the Class 8 books in `notes/content` as the answer base.

## How to publish (backend upload, no local build, no deletions)

1. Push the commit, then in GitHub run `Publish Past Papers to Library` (`.github/workflows/publish-papers.yml`) with `dry_run=true` and `slugs` = `12-vp-2080-9341 12-wdd-2080-656 12-sepm-2080-9371 12-ce-technical-2080-bundle`.
2. Read the log (`create ...` lines), then run it again with `dry_run=false`.
3. It uses the existing `SSH_HOST` and `SSH_KEY` secrets, stages files in `/home/consicac/nebians_api/tmp/papers` and calls `manage.py import_past_papers`, which only creates or refreshes `Resource` rows (files stored under deterministic names, existing ids and counters kept). The command must already be on the server: if the dry run says the command is unknown, run `Deploy Backend to cPanel` first.
4. Check the paper pages on the live site (title, description, tags, cover) after the real run.

Nothing was built locally for the app (no Gradle, no Django server). PDFs were built with WeasyPrint as in the tracker; the sandbox needed Debian pango debs unpacked into `/tmp/neb_root` (`LD_LIBRARY_PATH`), fonts via `notes/pipeline/fonts/install.sh` and a copy of the Poppins files into `~/.fonts` for the cover art.

## Class 8 pickup (session 126 research, nothing built yet)

Sources that exist for BLE (Basic Level Examination, Class 8): every municipality sets its own paper (Kathmandu Metropolitan, Lalitpur, Bhaktapur, Pokhara, Bharatpur, Ghorahi and others), with 2081 and 2082 papers on `bidhyamandir.com` (question PDF plus an answer sheet per municipality), `subeshyadav.com.np/blog/ble-past-year-questions-class-8` (38 papers, 2 PDFs of 230 pages) and `nebeducation.com` (2082 model questions with answers). Maths BLE pattern: 12 questions, 50 marks, 2 hrs (Sets 3, Arithmetic 14, Mensuration 5, Algebra 10, Geometry 15, Statistics 3). Plan: one session per subject. Start with BLE Maths 2082 Kathmandu Metropolitan (page images into `/tmp/psrc`, transcribe, solve with `notes/content/qbank8`/Class 8 books, ids `8-math-ble-2082-kathmandu`), then English, Nepali, Social Studies and Human Values, Creative Arts (the library already has Computer Science, Science and Technology and Health SET Solutions, check `GET /api/resources/?search=SET%20Solutions` first). Add a `--grade 8` path to `tools/publish/build_midterm_listings.py` (copy its pattern, exam_type `Mock`, tags BLE, SET, municipality name).

## Session 127 (this file is the pickup point, do not repeat the research below)

**Request 1 (Class 12 Computer Engineering technical, board 2078/79): closed as "no official source exists".** Re-checked the full dhanraj.com.np Blogger feed (`/feeds/posts/default?q=...&max-results=500`, queries Visual Programming, Web Development, Software Engineering, Computer Engineering, Technical, Database) and web search again. The only technical Computer Engineering board papers anywhere are the three 2080 papers already built and published (VP 9341, WDD 656, SEPM 9371). 2078 and 2079 results are general Computer Science model sets (2079 board already built as `12-cs-2079-4281`). Tell the requester this plainly and ask for photos of his paper if he has the old-course scans. Also still queued for him: Mathematics Technical 2080/2081/2082 (Chemistry and Physics technical are built).

**Request 2 (Class 11 science mid-term): done in session 126**, nothing new. Pickup ideas: second paper per subject, English, Nepali.

**Request 3 (Class 8 SET solutions): started.** The library already has uploaded `BLE | SET Solutions` for Computer Science, Science and Technology, Health and Physical Education. Built and visually checked (all 11 pages on 2x2 sheets, defects fixed: stem/figure split across pages with page breaks before Q5 and Q9, `=` after inline math and arrow lines turned into broken displays, rewritten as plain words or one `$$` per equation):

| Id | Paper | Pages |
| --- | --- | --- |
| `8-math-ble-2082-kathmandu` | Compulsory Mathematics, BLE 2082, Kathmandu Metropolitan City, 50 marks, 12 questions, English wording only (the original is bilingual), 6 figures, every sub-part solved, marks add to 50 | 11 |

Source: `bidhyamandir.com/ble-class-8-maths-2082-papers-kathmandu-metropolitan-city/` (the site returns 406 unless curl sends a browser User-Agent; images `wp-content/uploads/2026/03/BLE-Maths-2082-Kathmandu_1..6.jpg`). Numbers re-derived in `notes/papers/checks/check_8_math_ble_2082_kathmandu.py`. Listing builder for all Class 8 papers: `tools/publish/build_class8_listings.py` (add a dict to `PAPERS`; exam_type Final, title `NEB Class 8 <Subject> BLE Past Paper <year> (<ad>) <municipality> with Solutions`). The importer ignores `pradesh`/`district` (not in `LISTING_FIELDS`), the municipality is in the tags instead.

Class 8 pickup, in order: BLE English 2082 Kathmandu, Nepali 2082 Kathmandu, Social Studies, Science (Musikot Gulmi 2082 exists on bidhyamandir), Health/Physical/Creative Arts, then BLE Maths 2082 DMUN and 2081 sets, then a Class 8 Maths bundle (`bundle_stream.py --grade 8`). The bidhyamandir pages list every municipality paper with an answer sheet.

Sandbox recipe that worked this session (no sudo prompt, apt worked): `pip install --user --break-system-packages weasyprint pillow matplotlib pymupdf markdown pygments requests`, `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 poppler-utils fontconfig`, `bash notes/pipeline/fonts/install.sh`, `npm install` in `notes/pipeline/mathjax`, Poppins from `app/src/main/res/font` copied to `~/.fonts` as `Poppins-Bold/SemiBold/Regular.ttf`. The repo was sparse-cloned with `notes/` excluded, then `git sparse-checkout add /notes/papers/ /notes/pipeline/ /notes/tools/` (papers is 341 MB). Git needs `GIT_ASKPASS` exported in every shell because the clone is blob-filtered.

**Publish log (session 127):** `Publish Past Papers to Library` dry run 44634132615 (`1 created, 0 refreshed, 0 failed`), real run 44634251527. Live check: `GET /api/resources/?search=Class%208%20Mathematics%20BLE` lists the paper (grade_level Class 8, exam_type Final, tags with BLE and the municipality), PDF `/media/papers/8-math-ble-2082-kathmandu.pdf` and cover `/media/resource_thumbnails/paper_8-math-ble-2082-kathmandu.jpg` both 200. The four uploaded `BLE | SET Solutions` rows, the Computer Engineering and the Mid-Term listings were not touched (counts unchanged).

**Next paper in progress: BLE English 2082 Kathmandu (`8-eng-ble-2082-kathmandu`), source read, nothing written yet.** Page: `bidhyamandir.com/blegrade-8-english-papers-2082-kathmandu-metropolitan-city/`; images `.../2026/03/BLE-English-2082-Kathmandu_1..4.jpg` and `_5-scaled.jpg`, `_6-scaled.jpg` (curl with a browser User-Agent, shrink 5 and 6 to 1300 px wide). Pages 1 to 4 were read: Q1 letter to the head teacher (Kushma-9, Parbat, 27 August 2024, request to increase computer lab facilities) with 5 True/False; Q2 passage "Every living creature has a place where it feels at home" (polar bears, lions, natural habitat) with 5 fill-ins (a: feels at home, b: scorching/hot sun, c: natural habitat, d: ancestors, e: for long/survive for long, in a different one); Q3 advertisement "Required Urgently" (Adarsha Shiksha H. S. School, Baneshwor, Kathmandu; English Teacher 1 basic level, age not exceeding 30, deadline 15 Chaitra 2082 before 4 pm; Mathematics Teacher 1, masters) with 5 questions; Q4 passage on friendship starts on page 4. Pages 5 and 6 (rest of Q4, grammar, writing) still have to be read. The scans carry someone's handwritten ticks and T/F answers, do not copy them: solve from the text.

## Session 128 (pickup point)

**Request 1 (Class 12 Computer Engineering board 2078/79): final answer, do not search again.** New angle checked this session: the "Class 11 Computer Engineering 2079 (2022)" papers on `qsnpapers.nepalenotes.com` (Java Programming, Computer Organization and Architecture, Operating System, Web and Mobile Application) are **municipality examinations of Class 11**, not NEB board papers, and are unrelated to Class 12. They are not copied. No Class 12 Computer Engineering technical board paper exists for 2078 or 2079 (the first technical board sitting is 2080, already built: VP, WDD, SEPM, plus Physics Technical 2080/81/82 and Chemistry Technical 2081/82). Tell the requester so, and offer the 2080 set and the 2081/82 shared technical papers. Still queued for his stream: Chemistry Technical 2080 and Mathematics Technical 2080.

**Request 2 (Class 11 science mid-term):** done in session 126, nothing new.

**Request 3 (Class 8 BLE set solutions):**

| Id | Paper | Pages | State |
| --- | --- | --- | --- |
| `8-math-ble-2082-kathmandu` | Mathematics | 11 | published and verified (S127) |
| `8-eng-ble-2082-kathmandu` | Compulsory English | 9 | published (S128, dry run 44636715171, real run 44636822974) |
| `8-soc-ble-2082-kathmandu` | Social Studies and Human Values (Nepali medium paper, Nepali solutions) | 7 | published (dry run 44637802799, real run 44638079583) |
| `8-nep-ble-2082-pokhara` | Nepali, Pokhara Metropolitan City (Kathmandu Nepali paper not found; 17 questions, 50 marks, 8 scanned pages, Nepali solutions) | 9 | built and checked page by page, listing and cover made, publish pending |

Source of Social: `bidhyamandir.com/ble-class-8-social-studies-papers-2082-kathmandu-metropolitan/` (2 page images `.../2026/04/BLE-Social-2082-Kathmandu-_1.jpg`, `_2.jpg`). 50 marks: A 9x1, B 7x3, C 4x5 (B marks are not printed, derived). Solutions are model answers because the paper asks for creative answers in the student's own style. Q4 (25 ministers, Art. 76) and the census figures (142 castes, 124 languages) are stated from the 2078 census and the Constitution. The Q20 outline map of Nepal is a simplified border polygon with the real coordinates of Sagarmatha and Boudhanath: `notes/papers/figures/make_8_soc_map.py` writes an SVG without text and an HTML overlay (WeasyPrint shapes Devanagari in HTML but not inside SVG text). `build_paper.py` now accepts `.svg` and `.html` in `@img`. `build_class8_listings.py` has a `lang: ne` switch for the description.

Class 8 pickup, in order: Nepali 2082 Kathmandu (not found for Kathmandu, use Pokhara `ble-class-8-nepali-past-papers-2082-pokhara-metropolitan`), Science 2082 (Lalitpur, Pokhara, Kawasoti, Madi), Health/Physical/Creative Arts (Pokhara 2081), then a Class 8 bundle (`bundle_stream.py --grade 8`). Sandbox recipe: `sudo apt-get update` first, then the packages in the S127 note; `npm install` in `notes/pipeline/mathjax` is needed when a paper contains `$...$` math.

**Nepali BLE 2082 Pokhara (`8-nep-ble-2082-pokhara`)**: source `bidhyamandir.com/ble-class-8-nepali-past-papers-2082-pokhara-metropolitan/` (8 images `.../2026/03/BLE-Nepali-2082-Pokhara-Metropolitan_1..8.jpg`). Marks 2,2,2,1,2,2,2,3,3,4,4,3,3,3,4,5,5 = 50 (`checks/check_8_nep_ble_2082_pokhara.py`). Honest notes: Q2(ग) 'कर' odd word taken as 'ढिपी', Q2(घ) 'थोपो', Q15(घ) taken as the buyer (भक्त), Q16(ख) answer is from the printed extract only (the full story was not read). The 125-word essay is 138 words. Both options of every "or" question are answered. Layout lesson: put `<div style="break-before:page"></div>` before a question whose passage box would be pushed to the next page (heading orphan), and check the last page for 1 or 2 spilled lines.

Class 8 pickup now: Science 2082 (Lalitpur `ble-grade-8-science-papers-2082-lalitpur-metropolitan-city`, Pokhara, Kawasoti, Madi), Health/Physical/Creative Arts (Pokhara 2081), a second Maths set (Lalitpur 2082 or DMUN 2082), then the Class 8 bundle (`bundle_stream.py --grade 8 --label ... --filetag ... --category`).
