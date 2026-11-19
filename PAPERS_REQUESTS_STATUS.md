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
