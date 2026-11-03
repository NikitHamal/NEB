# Past Papers Pipeline — tracker (read this first in a new session)

Task: rebuild every NEB board paper (all years, all variants) for every class that has a note book in `notes/content`,
as NEBians-branded PDFs with full solutions, so the Library's "Past Paper" filter has real resources. Start from Class 12.
Papers are re-typeset from the published exam; question wording and marks are kept, the layout, watermark and solutions are ours.
No third-party name, watermark or mark appears in any output PDF.

Branch: `resources/past-papers-class12` (from `main`). Push after every paper (session 2 continued on this same branch).

## Layout
```
notes/papers/
  content/<id>.md        one paper: front matter + question paper + <!-- SOLUTIONS --> + solutions
  build_paper.py         content -> pdf/<file>.pdf, and manifest.json (python3 build_paper.py --all)
  paper.css              exam layout (extends pipeline/theme.css, NEBians watermark + Poppins/Source Serif)
  pdf/                   built PDFs (committed)
  manifest.json          one record per PDF: subject, grade, year_bs/ad, stream, code, pages, bytes, category "Board Exam"
  tools/fetch.py         scratch fetcher: draft OCR text + page images into /tmp/psrc (never committed)
  tools/cropfig.py       crop ONE figure out of a cached page image, strip the faint overlay, save to figures/ (committed)
  figures/               exact figure crops used by `@img` lines (notes/.gitignore ignores figures/; papers/.gitignore re-includes it)
  bundle_papers.py       subject bundles across years -> pdf/bundles/*.pdf + bundles.json (cover + contents + bookmarks)
```
Id convention: `<grade>-<subject>-<yearBS>-<variant>` e.g. `12-phy-2082-general`.
PDF name: `NEBians-Past-Paper-Grade-12-<Subject>-<yearBS>-<Variant>.pdf`.

## Paper source format
Front matter keys: file, subject, grade, year_bs, year_ad, stream, code, time, marks, students, category.
Question part (before `<!-- SOLUTIONS -->`):
- `## Group 'A'` headings, `<small>..</small>` one-line group rule.
- `@mcq N` then stem line(s), then `@opts a | b | c | d` (or `@opts-col` for long options, stacked).
- `@q N` then parts `(a) ... [[2]]`, sub-parts `(i) ...`; `@or` between alternative sets. `[[n]]` = marks chip.
- Math `$...$` (matplotlib mathtext, see notes/AUTHORING.md section 4). Figures: ```figure caption="..." matplotlib blocks (palette INK/ACCENT/GRID in scope).
Solutions part: `@s N` starts "Question N"; markdown, `$$..$$` display math, tables for the MCQ key.

## Method for each paper (do not skip the checks)
1. `python3 notes/papers/tools/fetch.py <page-url> <cache-key>`; the page text is OCR and is truncated ("Contd... See more") and wrong on exponents/symbols.
2. Open every page image (`read_file` on `/tmp/psrc/<key>/pN.jpg`; symlink `/tmp/psrc` into the file-tool root) and transcribe from the image, never from OCR alone.
3. Re-derive every numerical answer; write full solutions. MCQs get an answer key with a one-line reason.
4. Build, render pages to PNG (pymupdf), look at them. Then commit + push, update the table below.

## Environment notes
- File tool root here was `/home/user/sandbox` (not `/app`); bash sees everything. `ln -sfn /tmp/NEB /home/user/sandbox/neb`, `ln -sfn /tmp/psrc /home/user/sandbox/psrc`. File-tool paths must be relative.
- Git auth: `/tmp/gitenv.sh` (GIT_ASKPASS) echoing `$GH_PAT`; the token is never written to the repo.
- Python 3.11: needs `pip install --user --break-system-packages weasyprint markdown matplotlib numpy pymupdf pillow requests`, `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 fontconfig`, and `bash notes/pipeline/fonts/install.sh` then `fc-cache -f ~/.local/share/fonts/nebians`.
- `notes/pipeline/md2html.py` had one 3.12-only f-string; patched for 3.11.

## Scope and status
Years: 2080, 2081, 2082 BS (new course) per variant. Science-stream core first (matches note books phy12, chem12, bio12, math12, cs12, eng12, nep12), then the rest of Grade 12, then Grade 11, then SEE (Grade 10) and Grade 8.

### Variants: what actually exists (researched in session 2)
- **Grade 12 (NEB) is a national paper, NOT province-wise.** The "province-wise" pages for class 12 are SEO aggregation pages; the board prints one paper per subject per year. Real Grade 12 variants are: (a) *sets / paper codes* ('H', 'Q', 'W', 'M', 'D', 'R', ...; Mathematics and some others print several sets), (b) *Regular vs Grade-increment (supplementary) and partial* papers (separate paper per exam sitting, e.g. Physics 1021 'A' 2080), (c) *Technical stream* (Physics 9131, Chemistry 9111, Biology 9101, Mathematics 9121), (d) *Old course* papers (3-digit codes), (e) Optional papers.
- **The 7-province variants exist for SEE (Grade 10) and Grade 8** (Koshi, Madhesh, Bagmati, Gandaki, Lumbini, Karnali, Sudurpashchim; each province sets its own paper; SEE 2081 and 2082 have all 7 per subject, plus an all-province combined sheet). Build all 7 for each SEE subject when we reach Grade 10.
- So for Grade 12 the "bundle" request is met by `bundle_papers.py` (one PDF per subject across years, newest first, with a cover and bookmarks) and by building every set / sitting per year.

### Answer-length standard used in the solutions (researched: 30 to 40 words per mark for theory)
| Marks | What the answer must contain |
|---|---|
| 1 | one line / one fact / one equation |
| 2 | 2 distinct points, about 40 to 60 words (or definition + example / equation) |
| 3 | about 80 to 100 words, 3 points; numericals with formula, substitution, unit |
| 4 | about 120 to 160 words, headed points + equation/diagram; compare questions as a table with 5+ rows |
| 5 | about 150 to 200 words; steps/numbered points, labelled diagram where relevant, example |
| 8 (Group C) | answered part by part to the printed split; each part sized as above; derivations complete; labelled diagram; summary line |
Numericals: formula, substitution, answer with unit, one-line check. Every `@or` alternative gets a full answer too.

### Status
| Grade | Subject | Year | Variant | Status |
|---|---|---|---|---|
| 12 | Physics | 2082 | General | DONE (12 pp) |
| 12 | Chemistry | 2082 | General | DONE (10 pp) |
| 12 | Chemistry | 2081 | General 3021 'Q' | DONE (13 pp; session 2; 3 drawn figures: galvanic cell, blast furnace, energy profile) |
| 12 | Biology | 2082 | General | DONE (12 pp; schematic redraws) |
| 12 | Biology | 2081 | General 2021 'W' | DONE (16 pp; session 2; Q7 pollen grain and Q20 pituitary are EXACT crops of the published figures, the solution figures are redraws; the male-reproductive-system drawing is the weakest and wants an artist pass) |
| 12 | Mathematics | 2082 | Set R | DONE (8 pp). Other 2082 sets not yet built |
| 12 | Computer Science | 2082 | Regular + Partial | DONE (7 pp) |
| 12 | Computer Science | 2081 | Regular + grade increment 4281 | DONE (10 pp; session 2) |
| 12 | Compulsory English | 2082, 2081, 2080 | all | queued (see source index) |
| 12 | Compulsory Nepali | 2082, 2081, 2080 | | queued |
| 12 | Physics | 2081, 2080 | General | queued (2080 URL below; 2081 general URL not found on the aggregator, search `dhanrajgurung.com` or the NEB site) |
| 12 | Chemistry, Biology, Mathematics, CS | 2080 | General / grade increment | queued |
| 12 | Mathematics | 2081 | Regular 0081 'W' | queued (paper + MCQ sheet) |
| 12 | Physics, Chemistry, Biology, Mathematics | 2082, 2081, 2080 | Technical | queued |
| 12 | Management / Humanities / Education / Law | 2082-2080 | all | queued |
| 11 | all science subjects | | | queued |
| 10, 8 | all | | 7 provinces each | queued |

Bundles built so far (`python3 bundle_papers.py`): Chemistry 2081-2082, Biology 2081-2082, Computer Science 2081-2082. Physics and Mathematics get a bundle once a second year exists.

### Source index (internal use only; never cite in a PDF). Base `https://www.dhanraj.com.np/`
2081: `2025/03/Chemistry-General-Stream-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Chemistry-General-Stream-MCQ-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Biology-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Biology-MCQs-2081-2024-of-Class-12-NEB`, `.../Computer-Science-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Computer-Science-MCQs-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Compulsory-English-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Mathematics-Question-Paper-2081-2024-for-Regular-Students-of-Class-12-NEB`, `.../Mathematics-MCQs-2081-2024-for-Regular-Students-of-Class-12-NEB`, `.../Mathematics-Technical-Stream-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Physics-Technical-Stream-Question-Paper-2081-2024-of-Class-12-NEB`, `.../chemistry-technical-stream-question-paper-2081-2024-of-class-12-neb`, `.../Biology-Technical-Stream-Question-Paper-2081-2024-of-Class-12-NEB`, `.../Optional-English-...`, `.../Optional-Nepali-...`; Nepali: `2024/08/nepali-question-paper-2081-2024-of-class12-neb`.
2080: `2025/09/Physics-General-Stream-NEB-Class-12-Question-Paper-2080-2023-New-Course-Code-1021Q-PDF`, `2025/08/Mathematics-NEB-Class-12-Question-Paper-2080-2023-New-Course-Code-0081H`, `2025/08/Compulsory-English-Question-Paper-2080-2023-of-Class-12-NEB-Code-0041G`, `2025/08/Compulsory-Nepali-Question-Paper-2080-2023-of-Class-12-NEB-Code-0021B`, `2025/08/Biology-Question-Paper-2080-2023-of-Class-12-NEB-Technical-Stream-Code-9101-PDF-Download`, `2025/09/Physics-Technical-Stream-NEB-Class-12-Question-Paper-2080`; the 2080 Chemistry/Biology/CS general pages are linked from any 2080 page's collection list (fetch `2025/09/Social-Studies-and-Life-Skill-Education-General-Stream-NEB-Class-12-Question-Paper-2080-2023` and grep hrefs).
2082: `2026/03/<Subject>-<Stream>-Question-Paper-2082-2025-of-Class-12-NEB` (+ `-MCQs-` sheets), `2025/05/Compulsory-English-Question-Paper-2082-2025-of-Class-12-NEB`, `2026/03/Mathematics-Optional-Question-Paper-2082-2025-of-Class-12-NEB-PDF-Download`, `2026/03/Mathematics-Technical-Stream-...`.
Blogger search feed works for discovery: `GET /feeds/posts/default?q=<terms>&max-results=30&alt=json` (list `entry[].link[rel=alternate].href`).

## Method notes learned in session 2
- The fetched page text (OCR) is clean for text-only papers (Chemistry, CS) but still verify against the images; it loses chemical structures and figures.
- `read_file` on a freshly written file sometimes fails the first time: just call it again. The two page images of one read call can come back in swapped order, so check the printed page number / code before cropping.
- Source sheets carry a large translucent circular overlay and a coloured URL line. Never reuse a full page. `tools/cropfig.py` crops only the figure and maps everything lighter than the ink to white (`--lo/--hi`, try `--lo 40 --hi 105` when the overlay touches the figure, `--lo 60 --hi 150` otherwise). Look at the result before using it.
- In a paper use `@img <file> | <caption> | <width%>` on its own line (builder embeds `figures/<file>`).
- md2html math (matplotlib mathtext) has no `\xrightarrow`; write reaction schemes as text with unicode arrows.
- `solution_markup` now keeps author line breaks inside a paragraph, so write one reaction or step per line.
- MCQ option text must not contain a bare `|` (it splits options).

## Library registration
`manifest.json` (single papers) and `bundles.json` (subject bundles) are the import lists. Each is a `Resource` of type `Past Paper`, exam type `Board`, class `12`, subject, year(s). The library filter on `/app/past-papers/` (`default_type="Past Paper"`) lists them once uploaded. Uploading to the live site needs the admin; nothing here does that.

## Integrity notes
- Every paper must be checked against its page images before it is marked DONE; the answer keys are ours and must be re-derived.
- Assumptions are stated in the solution where the printed text is ambiguous: Biology 2081 Q5 (options A and B are both true statements, B chosen as the one showing auxin promoting root development), Biology 2081 Q7 labels (A exine, C vegetative cell, B intine, D generative cell, read from a small figure), Chemistry 2081 MCQ 6 (CO2 does not act as a ligand), CS 2081 MCQ 1 (printed table/column names were garbled in the source text; read as emp / empid).
- MCQ keys and the figure redraws have had no teacher review.

## Session log
- Session 1: pipeline + 5 Grade 12 papers (Physics, Chemistry, Computer Science, Mathematics, Biology; all 2082).
- Session 2 (same branch): re-cloned to /tmp/NEB (symlink /app/neb); added Chemistry 2081, Biology 2081 (with 2 exact figure crops), Computer Science 2081; added `tools/cropfig.py`, the `@img` directive, `bundle_papers.py`, solution line-break fix; researched variants and answer-length standard (above). 8 papers + 3 bundles in total. NOT done: the other ~60 Grade 12 papers (English, Nepali, Physics 2081/2080, 2080 science papers, Mathematics 2081 and other sets, Technical, Management/Humanities), Grade 11, 10 (7 provinces), 8.
- Next session, in this order: (1) Mathematics 2081 Regular (+ 2080 'H'), (2) Compulsory English 2082, 2081, 2080, (3) Physics 2080 General and find Physics 2081 general, (4) Chemistry/Biology/CS 2080, (5) Compulsory Nepali 2082/2081/2080, (6) Technical stream papers, (7) Management/Humanities, (8) Grade 11, (9) SEE with all 7 provinces, Grade 8. After each paper: `build_paper.py --all`, `bundle_papers.py`, leak check, push, verify `git ls-remote`.
