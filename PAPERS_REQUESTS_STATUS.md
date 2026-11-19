# Past paper requests: status and pickup (session 125 onward)

Read `notes/papers/PAPERS_TRACKER.md` for the paper pipeline itself. This file tracks the three open student requests so the next session does not repeat research.

## Request 1: Class 12 technical stream, Computer Engineering, board papers 2078/79

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

## Request 2: Class 11 science mid-term papers (physics, chemistry, maths, computer science and biology streams)

Nothing built yet. Mid-terms are set by each school, so there is no official source. Plan: author NEBians mid-term practice papers (not copies of any school's paper) for Class 11 Physics, Chemistry, Mathematics, Computer Science and Biology with the NEB new-course marking pattern (full solutions), each as `11-<subject>-mid-<variant>.md` in `notes/papers/content`, and a bundle per stream (Science with Computer Science, Science with Biology). `build_papers.py` needs `--grade 11` listings, exam_type "Mid Term". Pickup: start with Physics and Mathematics (units 1 to 6 of the CDC Class 11 syllabus) using the Class 11 books in `notes/content`.

## Request 3: Class 8 set solutions

Nothing built yet and no earlier work exists in the repo (searched `notes/` handoffs, tracker, git log). Class 8 has provincial and local-level exams, and the tracker says each province sets its own paper. dhanraj.com.np and nepalieducate.com have no Class 8 posts. Pickup: ask the requester which province and which subject set, search local-level (Bagmati, Gandaki, Lumbini) Class 8 sets, then solve with the Class 8 books in `notes/content` as the answer base.

## How to publish (backend upload, no local build, no deletions)

1. Push the commit, then in GitHub run `Publish Past Papers to Library` (`.github/workflows/publish-papers.yml`) with `dry_run=true` and `slugs` = `12-vp-2080-9341 12-wdd-2080-656 12-sepm-2080-9371 12-ce-technical-2080-bundle`.
2. Read the log (`create ...` lines), then run it again with `dry_run=false`.
3. It uses the existing `SSH_HOST` and `SSH_KEY` secrets, stages files in `/home/consicac/nebians_api/tmp/papers` and calls `manage.py import_past_papers`, which only creates or refreshes `Resource` rows (files stored under deterministic names, existing ids and counters kept). The command must already be on the server: if the dry run says the command is unknown, run `Deploy Backend to cPanel` first.
4. Check the paper pages on the live site (title, description, tags, cover) after the real run.

Nothing was built locally for the app (no Gradle, no Django server). PDFs were built with WeasyPrint as in the tracker; the sandbox needed Debian pango debs unpacked into `/tmp/neb_root` (`LD_LIBRARY_PATH`), fonts via `notes/pipeline/fonts/install.sh` and a copy of the Poppins files into `~/.fonts` for the cover art.
