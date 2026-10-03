# Class 10 completion + Class 8 build — working handoff

Branch: `resources/class10-class8-dsh` (from `hoplite/gortyn-fcf4f1d3` @ `25e55a3e`).
Pushes go through the AgentSky GitHub connector (the platform injects OAuth);
the owner's private repo is not reachable by plain `git push` from the pod.

## Push rules learned the hard way

- `git clone` works with the short-lived `temp_clone_token` the repo API
  returns, but that token is **read-only** — `git push` always 403s.
- `actl connector call github --body '…'` passes the body as an argv, so the
  kernel's 2 MB `ARG_MAX` caps it. Fine for text, useless for a 25 MB PDF.
- The connector's own HTTP endpoint (`POST {ACTL_BASE_URL}/api/agent/connector`,
  bearer `ACTL_AUTH_TOKEN`) takes the same payload with no argv limit, and that
  is what `notes/tools/push_branch.py` uses: create blobs -> tree -> commit ->
  fast-forward the branch ref.
- Hard ceiling found by probing: a single blob body above ~27 MB is rejected
  with `413 Request Entity Too Large`. **Every committed file must stay under
  25 MB**, so an oversized book is first run through
  `python3 notes/tools/shrink_pdf.py <book.pdf>` — that re-encodes only the
  embedded photographs (`rewrite_images(dpi_threshold=200, dpi_target=150,
  quality=72)`) and leaves the vector figures, the maths and the text untouched.
  Science 10 went 52.3 MB -> 11.0 MB with all 275 pages and 72 images intact.

## Environment recipe (rebuilt from scratch each session)

```
apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libgobject-2.0-0 libcairo2 shared-mime-info fonts-dejavu-core fontconfig
pip install weasyprint numpy matplotlib pymupdf markdown pillow
bash notes/pipeline/fonts/install.sh        # 5 book fonts + Noto Devanagari
```

Then `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md` and
`python3 build_pdf.py <slug>` both work in-tree (the pipeline resolves
`theme.css` and `brand/` beside itself).

## Where class 10 stood at the start of this session

All 7 books were present, `check.py`-clean, and already had 2.5k–6.5k words per
chapter. The gap to the Grade 11/12 books was **density of information
graphics**, not prose:

| Book | chapters | figures | photos | worked examples |
|---|---|---|---|---|
| science 10 | 19 | 56 | 72 | 105 |
| social 10 | 10 | 46 | 59 | 18 |
| english 10 | 18 | 36 | 25 | 77 |
| math 10 | 18 | 62 | **0** | 324 |
| optional math 10 | 12 | 53 | **0** | 268 |
| nepali 10 | 17 | **8** | 18 | 47 |
| question bank 10 | 16 | **7** | **0** | 4 |

Also: `qbank10` stops at unit 16 while its spine lists 19 units; the
`hours:` frontmatter is `0` on several class-10 books so the book's own
"Organisation of the book" table prints em-dashes where 11/12 print hours; and
the web app's Interactive hub ships NEB practical labs for grades 11/12 only.

## Status at the end of this session

| Item | State |
|---|---|
| qbank10 units 17–19 | **done** (book 19/19) |
| Nepali 10 information-graphics pass | **done** (8 figures -> 36, 2.1 per chapter) |
| Class 10 `hours:` backfill | not done — the spines carry a subject-level total only, not per-unit hours, so nothing was invented |
| Interactive layer for class 10 | not started (see below) |
| All class-10 books rebuilt + shrunk + pushed | **done** |
| Grade 8 Science and Technology | **complete, 11/11 units, built (110 pp)** |
| Grade 8 Mathematics | **complete, 21/21 chapters, built (149 pp)** |
| Grade 8 Nepali, English, Social Studies, Health/PE | **not started** — the CDC textbook contents for these four still have to be sourced; the science and maths spines were built from the CDC textbooks at `moecdc.gov.np/content/72/` and `/74/` (Nepali editions) and their English translations at `/71/` and `/73/` |

## Work queue (continued)

1. [ ] Interactive layer for class 10 — the web app's Interactive hub ships NEB
   practical labs for grades 11 and 12 (`backend_python/web/interactive/`) and
   nothing for grade 10. The natural addition is a Class 10 Science virtual-lab
   course (the SEE science practicals) plus a Class 10 Mathematics explorer.
2. [ ] Grade 8 spines and content for Nepali, English, Social Studies and
   Health/Physical & Creative Arts.
3. [ ] Grade 8 question bank, once the four remaining subject books exist.
4. [ ] Class 10 `hours:` frontmatter, from the CDC per-unit working hours if a
   source can be found.
5. [ ] Mathematics 8 is thinner on figures than Mathematics 11 (25 figures over
   21 shorter chapters, against 142 over 21 long ones); a figure pass would
   bring it in line.

## Work queue (original note)

1. [x] qbank10 units 17–19 (spine completion) — written, `check.py` OK; also fixed the mathsvg `\le0`/`\sqrt3` repair rules
2. [~] Class 10 information-graphics pass — nep10 taken from 8 to 36 figures (2.1 per chapter); eng10/math10/omath10 already match their 11/12 density (eng10 2.0 fig/ch vs eng11 1.9; math has no photos in 11/12 either)
3. [ ] `hours:` frontmatter backfill for every class-10 chapter
4. [ ] Interactive layer for class 10 (NEB Science/Maths virtual labs)
5. [ ] Rebuild + size-normalise the class-10 books, push
6. [ ] Class 8: curriculum spines, then the full chapter sets + question bank
