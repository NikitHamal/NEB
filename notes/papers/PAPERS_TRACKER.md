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
| 12 | Physics | 2080 | General 1021 'Q' (reg. 78, 79) | DONE (17 pp; session 4; 7 EXACT figure crops (PV cycle, beaker, NOR-gate combination, loop, potentiometer, photoelectric graph, parallel wires), 8 drawn solution/question figures; long answers sized to the marks standard) |
| 12 | Chemistry | 2082 | General | DONE (10 pp) |
| 12 | Chemistry | 2081 | General 3021 'Q' | DONE (13 pp; session 2; 3 drawn figures: galvanic cell, blast furnace, energy profile) |
| 12 | Biology | 2082 | General | DONE (12 pp; schematic redraws) |
| 12 | Biology | 2081 | General 2021 'W' | DONE (16 pp; session 2; Q7 pollen grain and Q20 pituitary are EXACT crops of the published figures, the solution figures are redraws; the male-reproductive-system drawing is the weakest and wants an artist pass) |
| 12 | Mathematics | 2082 | Set R | DONE (8 pp). Other 2082 sets not yet built |
| 12 | Mathematics | 2082 | Optional 4021 'A' (regular, reg. 80, 81) | DONE (11 pp; session 14; source `mathopt82`, 4 exam page images; text paper; 2 drawn figures (hyperbola for Q14(b), feasible region for Q19(b)); every `Or` answered; stated openly in the solutions: Q19(b) simplex optimum Z = 18 is not unique (reduced cost of y is 0; the edge 2x - 3y = 6 is optimal), Q22(c) x^2 - y^2 = Cx is a polynomial equation but y is not a polynomial in x unless C = 0, Q21(a) gives both orientations of the ellipse, Q10 key B (differential) vs A (exact increase); Mathematics bundle now 7 papers) |
| 12 | Computer Science | 2082 | Regular + Partial | DONE (7 pp) |
| 12 | Computer Science | 2081 | Regular + grade increment 4281 | DONE (10 pp; session 2) |
| 12 | Compulsory English | 2081 | 0041 'B' | DONE (8 pp; session 3). Q3a OR (Human Rights and the Age of Inequality, Samuel Moyn) answered in session 4 |
| 12 | Compulsory English | 2082 Regular 0041 'C' | regular (reg. no. 81) | DONE (8 pp; session 3). OR alternative *On Libraries* (Oliver Sacks) answered in session 4 |
| 12 | Compulsory English | 2083 Regular 0041 'C' (reg. 82) | regular | DONE (10 pp; session 4; reading passage 'magical library', table interpretation, letter, essay, grammar all with model answers) |
| 12 | Compulsory English | 2080 Grade-increment 0041 'G' (reg. 78 only) | grade increment | DONE (9 pp; session 4; obesity reading passage, press release, email, story; Treasure in the Forest verified by search) |
| 12 | Compulsory English | 2082 Partial 0041 'P' (reg. 78, 79, 80; Maginot Line reading passage) | partial | DONE (8 pp; session 9; text-only; Maginot passage, Ilam herbal-oils news story, shopping letter, journey essay, grammar all with model answers; assumptions: 1A(a) 'invasion', 1B(e) TRUE, Q7(b) 'to', Q7(c) 'listening', Q7(a) 'comes'). Still queued: 2080 old-course 004 (2080 'D' DONE in session 12). Old note on the Partial page: Partial page: `/2025/05/Compulsory-English-Question-Paper-2082-2025-of-Class-12-Partial-Students-NEB-PDF-Download.html` (different passage from the regular paper) |
| 12 | Compulsory Nepali | 2082 | Regular + partial 0021 'B' (reg. 78-81) | DONE (11 pp; session 5; Devanagari; every question answered in Nepali, essays 240-260 words; no figures) |
| 12 | Compulsory Nepali | 2081 | Regular + grade increment 0021 'B' (reg. 78-80) | DONE (12 pp; session 6; Devanagari; Q15(a) Damayanti and Q14 are tied to the note books `notes/content/nep12`) |
| 12 | Compulsory Nepali | 2080 | Regular 0021 'B' (reg. 78, 79) | DONE (12 pp; session 6; Q11 passage is the same as 2082 so its tipot/summary is reused; Q12(b) tamsuk, Q13(a) educational-tour report, Q17 Ek Chihan social evils and Himchuli national feeling written out in full; Nepali bundle 2080-2082 built) |
| 12 | Physics | 2081 | General 1021 'C' (reg. 78, 79, 80; regular + grade increment) | DONE (18 pp; session 8; source = 6 page photos from educatenepal (`phy81`); 7 EXACT figure crops (SHM graph, heat engine, P-V cycle, potentiometer, decay graph, NAND-gate circuit, open pipe); 6 drawn solution figures; MCQ 7 key stated as an assumption) |
| 12 | Chemistry | 2080 | General 3021 'J' (reg. 78, 79) | DONE (14 pp; session 7; source = photographed 2-page sheet; 3 redrawn figures (Fe/Cu cell, open-hearth furnace, paper flow sheet); Q21 OR text prints C3H6O for A, solution notes the ethanal reading; amine formula misprint C3H6N read as C3H9N) |
| 12 | Biology | 2080 | General 2021 'R' (reg. 78, 79) | DONE (18 pp; session 7; Q7 anther and Q19 synapse are EXACT crops; Krebs, allopolyploidy, replication fork, J-curve, heart, lungs drawn; Q7 labels A tapetum, B middle layer, C endothecium, D epidermis read inside-out, Q19 A knob, C vesicle, D cleft, B postsynaptic membrane) |
| 12 | Computer Science | 2080 | 4281 (reg. 78, 79) | DONE (11 pp; session 7; 50 marks; PHP/JS/C programs, topology figure, SQL DDL; Q10 OR prints only the schema so the DDL tasks are create/alter/drop; Q16 football area read as pi r^2 with the 4 pi r^2 variant noted) |
| 12 | Mathematics | 2080 | General / grade increment (other sets) | queued |
| 12 | Mathematics | 2081 | General 4021 (regular, reg. 80) | DONE (10 pp; session 9; second 2081 Mathematics paper, different from 'W'; no figures; 3 printing problems stated openly in the solutions: Q18(a) point (2,5) is not on the curve (y(2)=4), Q20(c) n! < 2^n is false for n>=4 (proved n! > 2^n for n>=4 instead), Q21(a) sides 3+sqrt3, 2, sqrt3 violate the triangle inequality (solved the standard a=sqrt3+1, b=2, c=sqrt6 version); assumptions: MCQ 4 focus (5,0), Q19 Or (b) force = (dm/dt)(v1-v2)=16 N) |
| 12 | Mathematics | 2080 | General 0081 'H' (reg. 78, 79) | DONE (12 pp; session 5; Q16 Rolle figure is an EXACT crop; Q18 simplex table + feasible-region figure; Q19 both alternatives; Group C full steps) |
| 12 | Mathematics | 2081 | Regular 0081 'W' | DONE (11 pp; session 3; MCQ sheet + paper transcribed from images; 2 solution figures) |
| 12 | Mathematics | 2081 | Technical 9121 (plant and animal science; reg. 79, 80; regular + grade increment) | DONE (8 pp; session 9; text-only; Q14(a) prints the denominator as '6c', proved for the standard 'bc' and said so; Q14(b) gives both C = 60 and 120 degrees; Q15(b) discriminant -43.75 so not a pair of lines; Q19(b) area 16/3 for the upper branch) |
| 12 | Physics | 2081 | Technical 9131 (civil / computer / electrical engineering; reg. 79, 80) | DONE (15 pp; session 10; source `phyT81`; Q20 OR closed-pipe figure is an EXACT crop (3 nodes, 3 antinodes, L = 5 lambda/4); Q18(b) circuit and Q10 graphs are redraws; Q18(b) middle cell has no printed emf: R1 = 16 - E2 and E3 = 13 - E2 derived, numbers given for E2 = 0, stated openly in the solution) |
| 12 | Chemistry | 2081 | Technical 9111 (reg. 79, 80) | DONE (12 pp; session 10; source `chemT81`; text paper; Q20 rate law rate = k[M][N]^2, k = 6 L^2 mol^-2 s^-1; Q15 OR heat of combustion -331.4 kcal/mol; copper flow chart drawn, blast furnace figure reused from Chemistry 2081 General) |
| 12 | Biology | 2081 | Technical 9101 (reg. 79, 80) | DONE (11 pp; session 10; source `bioT81`; text paper; male reproductive figure reused from Biology 2081 General (still the weakest drawing), thyroid and RNA figures drawn) |
| 12 | Biology | 2080 | Technical 9101 (regular) | DONE (13 pp; session 11; source `bioT80`; text paper, no printed figures; drawn: dicot + monocot T.S., excretory system, semi-conservative replication (replication fork reused from Biology 2080 General); Q16 and Q22 both alternatives answered; Q11 key B stated as an assumption because the printed wording is loose; Q7 key isograft) |
| 12 | Compulsory English | 2080 Regular 0041 'D' (reg. 78, 79) | regular | DONE (9 pp; session 12; source `eng80d`, 5 page images; text paper; daylight-saving-time reading passage, Anuradha Koirala summary, sports-goods catalogue letter, Udayapur Cement press release (model answers, invented names and figures, said so in the solution), grammar and MCQ keys; literature answers use `notes/content/eng12` units 05, 06, 09, 10, 13, 15, 16, 18, 19; the passage prints misprinted dates (Franklin 1984, Willett 1957-1915, Johnson 1996), kept as printed and flagged in the solution; MCQ Q8(b) key 'satisfy' and Q7(d) 'might' (could also fits) are our keys; English bundle now 6 papers) |
| 12 | Physics | 2080 | Technical 9131 (regular; first-two-digits reg. not printed) | DONE (16 pp; session 12; source `phyT80`, 3 exam page images; text paper; 12 drawn solution figures (pendulum, v-t, closed pipe, meter bridge, coil, voltmeter conversion, rod, Xc graph, Millikan graph, Coolidge tube; parabola and full-wave rectifier reused from Physics 2081 Technical); Q16(c) printed 30 degrees gives mu = tan 30 = 0.577 < 1, stated openly in the solution (60 degrees would give 1.73); MCQ 1 'angular momentum ratio' key B stated as an assumption (sqrt2 : 1 with the 2I body first); Physics bundle now 5 papers) |
| 12 | Chemistry | 2082 | Technical 9111 (reg. 79, 80, 81; regular + partial) | DONE (14 pp; session 13; source `chemT82`, 4 exam page images; text paper; 2 drawn figures (standard hydrogen electrode, zinc extraction flow chart), blast furnace reused from Chemistry 2081 Technical; assumptions: MCQ 3 key C because option B is printed as neutral H2PO4, MCQ 10 key B propene (ozonolysis gives ethanal + methanal), Q22(b) item 'i' printed twice, second is item (ii); Chemistry bundle now 5 papers) |
| 12 | Physics | 2082 | Technical 9131 (civil / computer / electrical; reg. 79, 80, 81; regular + partial) | DONE (14 pp; session 13; source `phyT82`, 4 exam page images + the circuit image; Q21(d) LCR circuit is the EXACT published figure (clean, overlay-free image, `figures/phyT82-q21-lcr.png`); MCQ 9 graphs are a redraw (`figures/phyT82-q9-graphs.png`); drawn: open-pipe modes, inductor phasor diagram; full-wave rectifier reused from Physics 2081 Technical; stated openly in the solutions: Q22 Or(b) prints R = 1.097e-7 (read as e+7), Q22 Or(d) says 'X-rays' but gives the electron mass (solved for an electron of 200 eV), Q22(d) takes rho = 1000 and g = 9.8, MCQ 4 key +30 J; Physics bundle now 6 papers) |
| 12 | Mathematics | 2081 | Old Course 216 (grade improvement / partial; general reg. 76, 77, technical 76-78; 100 marks) | DONE (20 pp; session 15; source `mathold81`, 4 exam page images; text paper plus 4 drawn figures (parallelogram of the vector product, three-force resultant, wall projectile, feasible region); every `Or` answered; stated openly in the solutions: Q1(b) prints x^6 in (3x-1/(3x))^9 so the coefficient is 0 (x^5 = 8748, x^7 = -19683 given), Q2(a) focus/vertex read as (+-5,0), (+-3,0), Q8(b)(i) read as all three boys (253/620; 3/4 if literal), Q16(c) 'ill-defined' answered as ad - bc = 0 plus the ill-conditioned case; Mathematics bundle now 8 papers) |
| 12 | Chemistry | 2080 | Technical 9111 | queued (linked from the 2082 Chemistry Technical page) |
| 12 | Mathematics | 2082 | Technical 9121 (plant and animal science; reg. 79, 80, 81; regular + partial) | DONE (10 pp; session 13; source `mathT82`, 3 exam page images; no printed figures; 1 drawn figure (area between y^2 = 8x and y = x), matrix inverse drawn with `mateq`; stated openly in the solutions: Q17(a) needs the events to be exhaustive (sum of probabilities 1), Q21(c) gives r = 1.94 > 1 so the coefficient cannot be calculated, MCQ 4 takes theta acute; Mathematics bundle now 6 papers) |
| 12 | Mathematics | 2080 | Technical 9121 | queued |
| 12 | Management / Humanities / Education / Law | 2082-2080 | all | queued |
| 11 | all science subjects | | | queued |
| 10, 8 | all | | 7 provinces each | queued |

Bundles built so far (`python3 bundle_papers.py`): Chemistry (2080-2082), Biology (2080-2082), Computer Science (2080-2082), Mathematics (2080-2082, now 5 papers), English (2080-2083, now 5 papers incl. the 2082 Partial), Physics (2080-2082, now with all three years), Compulsory Nepali (2080-2082).

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

## Session 3 notes (same branch)
- **Fetch URLs need the `.html` suffix** (the source slugs listed above without it silently return the blog home page: 2373 chars, 0 images). Find slugs with the full feed index: `/tmp/index.py` pages `GET /feeds/posts/default?start-index=N&max-results=150&alt=json` into `/tmp/index.txt` (1152 posts; ~160 Class 12 paper posts); then `grep -i`. The feed `q=` search parameter is ignored. Recreate the script if /tmp is wiped (10 lines).
- **mathtext needs braces**: `\sqrt{3}` not `\sqrt3`, `\dfrac{\infty}{\infty}`. No `array`, `vmatrix`. A bare `|` in an `@opts` line splits options (write 'for $-1<x<1$' instead of $|x|<1$). Check the build log for `[math] fell back:`; it must be empty.
- A paper newer than the ones listed exists: **2083 (2026) Compulsory English** (`/2026/04/NEB-Grade-12-Compulsory-English-Exam-Question-Paper-2083-2026.html`). Search the index for `2083` too.
- The source pages for 2081 papers: image 0 is the cover banner, images 1..n are the exam pages (check `p1.jpg` onward).
- Session 3 result: Mathematics 2081 'W', Compulsory English 2081 'B', Compulsory English 2082 'C' built and pushed (total 11 single papers; bundles: Biology, Chemistry, CS, Mathematics, English where two years exist). English literature answers were written from the textbook facts found by web search (Neighbours, A Respectable Woman, A Devoted Son, A Day, Marriage as a Social Institution, A Very Old Man with Enormous Wings, A Matter of Husbands, Facing Death, Soft Storm, Half-Closed Eyes of the Buddha, The Bull, Every Morning I Wake, Humility, Knowledge and Wisdom). Still to answer in English papers: *Human Rights and the Age of Inequality* (2081 Q3a OR) and *On Libraries* (2082 Q2b OR). Fix these first next session.
- Literature answers are model answers (not an official marking scheme); MCQ/grammar keys are ours and un-reviewed. English 2081 Q8d has two defensible answers (heart, hectic); the solution says so.
- **Next session order**: (1) Physics 2080 General 1021 'Q' (fetched as key `phy80`, 7 pages, if /tmp/psrc still exists; else refetch with the `.html` URL in the index), find Physics 2081 general, (2) Compulsory English 2080 'G' + 2082 Partial + 2083, (3) Chemistry/Biology/CS 2080, (4) Compulsory Nepali 2082/2081/2080, (5) Technical stream, (6) Management/Humanities, (7) Grade 11, (8) SEE with 7 provinces, Grade 8. Realistic pace: 2 to 3 papers per session when each is transcribed from images and fully solved.

## Session 4 notes (same branch)
- Fresh sandbox again: re-cloned to /tmp/NEB (symlink /app/neb), `/tmp/psrc` symlinked as /app/psrc, `sudo apt-get update` is needed before installing libpango-1.0-0 libpangoft2-1.0-0 fontconfig, then `fc-cache -f ~/.local/share/fonts/nebians`.
- Built Physics 2080 General 'Q' (`content/12-phy-2080-general.md`) and the Physics 2080-2082 bundle. Fetch URL (with `.html`): `/2025/09/Physics-General-Stream-NEB-Class-12-Question-Paper-2080-2023-New-Course-Code-1021Q-PDF.html`.
- **Builder gotcha:** a ```figure fence inside the QUESTION part needs a blank line before and after it, otherwise it is swallowed into the preceding paragraph and printed as code. `@img` lines are fine.
- **Crop tool gotcha:** thin lines (field arrows, faint wave sketches, small text) vanish with the default levels; redraw those with matplotlib instead (done for Q20 sound sketch, Q22 frame, LCR circuit). Coordinates: displayed page images are ~1.02x smaller than the file (page jpgs are ~1132x1600).
- `build_paper.py --all` rewrites every PDF byte-differently; only commit the PDFs whose source changed (`git checkout` the rest).
- Answer notes: Q19(b)(ii) (S in the galvanometer branch) -> no shift, stated with the reason; Q12 OR (b) assumes the 60 N restoring force acts at the amplitude. The figure in Q20(c)(ii) is labelled v + v_s, so the solution treats a receding source.
- Next: Physics 2081 general (find source), English 2080 'G'/'D', 2082 partial, 2083, Chemistry/Biology/CS 2080, Nepali, Technical, Management/Humanities, then Grade 11, 10 (7 provinces), 8.
- Also in session 4: English 2083 'C' built (fetched as key `eng80g`/`eng80d` are cached for 2080 'G' and 'D': pages p1.. in /tmp/psrc if still present; URLs: `/2025/08/Compulsory-English-Question-Paper-2080-2023-of-Class-12-NEB-Code-0041G.html`, `/2023/07/Class-12-Compulsory-English-Question-Paper-2080.html`). English bundle is now 2080-2083 (older English bundle files were removed; the bundler does NOT delete stale bundles, `git rm` them by hand).
- Literature facts verified by search: On Libraries = Oliver Sacks; Human Rights and the Age of Inequality = Samuel Moyn (Croesus, Herodotus, UDHR 10 Dec 1948); Marriage as a Social Institution = Stephen L. Nock (social capital, normative marriage); 'A Day' = Emily Dickinson.

## Session 5 notes (same branch)
- Fresh sandbox: PAT is read from env var via `/tmp/gitenv.sh` (GIT_ASKPASS), sourced from `/tmp/gitenv.env` (outside the repo). Clone to /tmp/NEB, symlink /app/neb. Fonts/pip/apt steps as in session 4. File-tool paths: `neb/notes/...` and `psrc/...` (symlinks under /app); `read_file` often fails the first time for freshly written files, retry.
- `build_paper.py`: marks chips `[[n]]` are now converted on plain lines too (e.g. the paragraph after a table inside an `@or` alternative); before that it printed `[[5]]` literally.
- Built Mathematics 2080 'H' (`content/12-math-2080-set-h.md`, fetched as key `math80`), Mathematics bundle is now 2080-2082 (old 2081-2082 bundle removed by hand).
- Assumptions stated in the solution: Math 2080 MCQ 9 (sign in front of 1/2 in option D is faint in the print; D read as -1/2 log((x+1)/(x-1))), Q13(a) no repetition (120; 216 if repetition), Q21(b) 'plane' read as the line through the two points, Q22(c) fails at k = 0.
- Cached for next papers (if /tmp/psrc survives): `nep82`, `nep81`, `nep80` (Compulsory Nepali 2082, 2081, 2080 'B' 0021; Devanagari font Noto Sans Devanagari is installed by pipeline/fonts/install.sh; use `:lang(ne)` / `.deva`).
- Next: Nepali 2082/2081/2080, Physics 2081 general, Chemistry/Biology/CS 2080, English 2082 partial/2080 'D', Technical, Management/Humanities, then Grade 11, SEE (7 provinces), Grade 8.
- Built Compulsory Nepali 2082 (`content/12-nep-2082-0021b.md`, front matter `lang: ne` switches the builder to Devanagari: Noto Sans Devanagari body, Devanagari marks digits, Devanagari part labels (क)(ख)(ग) and sub-parts (अ)(आ); question numbers/`@s` numbers are typed in Devanagari). No bundle yet (needs a second Nepali year).
- Underlines in Q1-Q7 were read from zoomed crops of the page images; Q4 underlines: जान्ने, लिई, घडी, तथा, र, उनी, गर्थे (तथा is faint in the source and was kept).
- Textbook facts used (verified by search): Gorkhe = Bakhat Bahadur Thapa (Pesal builds the 'Gorkhe' antivirus, Satpal's computer is infected); Ek Chihan = Hridaya Chandra Singh Pradhan (Dr Godatprasad, Nanithakun, Shivnaran, Ranjana Devi, Surman Subba); Ghanghasyako Ukalo Katta = Taranath Sharma; Hamilai Bolaunchhan Himchuli = Madhav Prasad Ghimire; Aamako Sapana = Gopal Prasad Rimal; Stephen William Hawking = biography (ALS; 'ashaa raakh ra byasta bana'; parents Isabel and Frank). The Q15(a) poem interpretation (mother's dream / 'Banshuri') is a reading of the stanza, not an official key.
- Nepali answers are model answers; sample letters/reports use invented names and places. Not reviewed by a Nepali teacher: ask one to check grammar items (Q1 syllable split, Q6 morphology, Q7 karak) before publishing.
- Leak check done: a git grep for the token prefix finds nothing in the paper files.
- Next (in order): Nepali 2081 and 2080 (+ bundle), Physics 2081 general, Chemistry/Biology/CS 2080, English 2082 partial and 2080 'D', Technical stream, Management/Humanities, then Grade 11, SEE (7 provinces), Grade 8.

## Session 6 notes (same branch)
- Fresh sandbox again. Clone to /tmp/NEB (symlink /app/neb), `/tmp/psrc` symlinked as /app/psrc. PAT: `/tmp/gitenv.sh` (GIT_ASKPASS) echoes `$NEB_GH_TOKEN`; push with `NEB_GH_TOKEN=... /tmp/gitrun.sh push origin resources/past-papers-class12` (token lives only in the shell env, never in the repo). Set `git config user.name/user.email` locally.
- **Do NOT run `build_paper.py --all`** (takes over 3 minutes, times out in the tool, and rewrites every PDF byte-differently). Build one paper with `python3 build_paper.py <id>` (id without `.md`, e.g. `12-nep-2081-0021b`), then refresh the manifest for that one paper with the new `python3 tools/addmanifest.py <id>` (renders it and updates manifest.json). `bundle_papers.py` also rewrites every bundle: run it, then `git checkout -- $(git ls-files -m pdf/bundles)` so only the changed bundle is committed. `git checkout` any other PDF that shows as modified.
- Built Nepali 2081 and 2080 (`content/12-nep-2081-0021b.md`, `content/12-nep-2080-0021b.md`). The question text was transcribed from the page images (`nep81`, `nep80` caches). The textbook-based answers (Q14-Q17) use the note books in `notes/content/nep12` (unit-01 Aamako Sapana, unit-02 Birahini Damayanti, unit-03 Ghanghasyako Ukalo Katta, unit-05 Ek Chihan, unit-06 Stephen Hawking, unit-07 Himchuli, unit-08 Matritwa, unit-10 Nepali Pahichan) which saves searching.
- Facts confirmed from the note books: Q15(a) 2080 'jogbani-dharan alkatre baato' = Ghanghasya (Taranath Sharma); Q15(b) 2080 and 2081 dialogue = Nepali Pahichan; Q14 2080 (a) is a line of Matritwa, (b) is Aamako Sapana.
- Open points for a Nepali teacher: Q4 2081 'tyo' tagged as determiner/pronoun; Q6 2080 prefix/suffix examples (bi, ku, abhi, yauli, y, tavya) use bidesh, kusanskar, abhibhavak, thatyauli, gramya, kartavya; Q7 2081 vibhakti sentences; the essays are model answers.
- Next (in order): Physics 2081 general (source not yet found), Chemistry / Biology / Computer Science 2080, English 2082 Partial and 2080 'D', Technical stream, Management / Humanities, Grade 11, SEE (7 provinces each), Grade 8.

## Session 7 notes (same branch)
- Fresh sandbox. `/tmp/gitenv.sh` echoes `$NEB_GH_TOKEN` (GIT_ASKPASS); clone to /tmp/NEB, symlink /app/neb, `/tmp/psrc` symlinked as /app/psrc. Same pip/apt/fonts steps as session 4. File-tool `read_file` fails on the first call for new files, call it again.
- **New source for 2080 and 2081 papers the first aggregator lacks.** The Blogger index at the first source (627 posts now) has NO 2080 Chemistry / Biology / CS general or Physics 2081 general. Found instead:
  - `https://www.nepalieducate.com/2023/05/2080class-12-board-exam-question-paper.html` links Google-Drive scan PDFs for the real 2080 papers (English, Nepali, Mathematics, Social, Physics, Chemistry, Biology, Computer). Direct download: `curl -sL "https://drive.google.com/uc?export=download&id=<id>"`. Ids: English `1DLvK5OohnC7xpwymvDf00wMWfnsOLpGt`, Nepali `1eCRQ1ll8Q5SkA82RMlFZ5-h0Jn5ozDfI`, Mathematics `1vz2m880H1BA9UCNAzZogoekLmsT7C8rO`, Social `1br_blYK3pvVTcX3LtoAgUXj_ZXZY8oFd`, Physics `1jLo4Fkz4rFbQUfBKuk0WYgKz2P4Yb2_b`, Chemistry `1S-5Lm8cJwle9Av6vle5OzDh-3ceS-hy2`, Biology `17NiZY6S37XwUIzXvGDw6jKZdrKfjHTd4`, Computer `1kPkJiKo1GwFgc3G86pbOOwG3vGeFrve6`. Render with pymupdf at 130 dpi to /tmp/psrc/<key>/pN.jpg. Chemistry 2080 is code 3021 'J', Biology 2021 'R', Physics (the same page) is not the 'Q' paper already built, check its code before reuse.
  - `https://blog.educatenepal.com/2024/05/neb-grade-12-physics-exam-questions.html` = Physics 2081 1021 'C' (6 page images `...-physics-questions-2081-p1-m.jpg` .. p6, 693x996, small; cached as `phy81`). NOT yet built.
  - nebnotebank.com lists Physics 2080 1021 'A' Grade Increment and 2081 'C'.
- Each scan page is a camera photo: crop figures with `tools/cropfig.py bio80 <page> x0 y0 x1 y1 <name> --lo 90 --hi 170` (page jpgs are 1075x1521 for bio80).
- Next (in order): Physics 2081 'C' (`phy81`), Physics 2080 'A' grade increment, Mathematics sets 2082 other than 'R', Chemistry 2082 other sets, English 2082 Partial / 2080 'D', Technical stream, Management / Humanities, Grade 11, SEE (7 provinces each), Grade 8.

## Session 8 notes (same branch)
- Fresh sandbox. `/tmp/gitenv.sh` echoes `$NEB_GH_PAT` (GIT_ASKPASS, outside the repo); `GIT_TERMINAL_PROMPT=0`. Clone with `--branch resources/past-papers-class12` to /tmp/NEB, symlink /app/neb and /app/psrc. pip, apt (`sudo apt-get update` first) and fonts steps as in session 4; `import fitz` works but warns, use `import pymupdf`.
- Built Physics 2081 'C' (`content/12-phy-2081-general.md`). Page images: the `s16000` URLs on `blog.educatenepal.com/2024/05/neb-grade-12-physics-exam-questions.html` (693-700 px wide, so figures are `--scale 4 --lo 70 --hi 165` crops; keep the crop box clear of neighbouring text lines or fragments show).
- Math: mathtext needs braces for EVERY `\frac`, `\dfrac`, `\sqrt`, `\overline`; `\boxed` is unsupported (the builder falls back to raw text). Check the build output for `[math] fell back:`.
- Assumptions in the solution: MCQ 7 (polarizer; only 'reduce intensity' is acceptable), MCQ 11 (P-wave slows in a liquid), Q14 III read as adiabatic (steeper than the isotherm through (3V1, 4P1)), Q16 l1 = open key, l2 = closed key, Q22 c uses e = 1.6e-19 C (not printed).
- Next (in order): Physics 2080 'A' grade increment, Mathematics 2082 other sets and 2080 other sets, Chemistry 2082 other sets, English 2082 Partial / 2080 'D', Technical stream (Physics 9131, Chemistry 9111, Biology 9101, Mathematics 9121), Management / Humanities / Education / Law, Grade 11, SEE (7 provinces each), Grade 8.

## Session 9 notes (same branch)
- Fresh sandbox, PAT via `/tmp/gitenv.sh` echoing `$NEB_GH_TOKEN` (GIT_ASKPASS), clone to /tmp/NEB, symlink /app/neb, /tmp/psrc symlinked as /app/psrc. apt (`sudo apt-get update` first), pip, fonts as in session 4. The index script is `/tmp/index.py` (10 lines, see session 3).
- Built Mathematics 2081 General 4021 (`content/12-math-2081-4021.md`), source `2024/08/class-12-mathematics-question-paper-2081-2024-general-stream-neb.html` (4 exam pages, p1..p4). Zoom into a page region with PIL crop + resize before deciding a printed value is a misprint.
- Mathtext: `\sqrt3`, `\dfrac x2`, `\dfrac\theta2` all fall back to raw text; always brace. `vmatrix` is unsupported: describe the determinant expansion in words.
- Sources found but NOT yet built: Math Technical 2081 (9121) `2025/03/Mathematics-Technical-Stream-Question-Paper-2081-2024-of-Class-12-NEB.html` (fetched as `math81tech`), English 2082 Partial (`eng82p`), English 2080 'D' `2023/07/Class-12-Compulsory-English-Question-Paper-2080.html` (`eng80d`), Physics/Chemistry/Biology Technical 2081 (`2025/03/...Technical-Stream...`), SEE 2082 all 7 provinces are in the index (`2026/04/SEE-2082-2026-Compulsory-<Subject>-Question-Paper-of-<Province>-Province.html`; Math Karnali/Koshi/Lumbini/Madhesh/Sudurpashchim in `2026/06`).
- Next (in order): English 2082 Partial, Mathematics Technical 2081, Physics/Chemistry/Biology Technical 2081, other 2080/2082 sets, Management / Humanities, Grade 11, SEE (7 provinces each), Grade 8.
- Session 9 later: built English 2082 Partial 0041 'P' (`content/12-eng-2082-0041p.md`). Facts for literature answers were checked by search (Earnest Woman blames the Famous Actress; the bull's death signs are no breathing, no eating, ears drooped, tail loose, eyes still). The partial page's collection list also names the 2082 sets: Chemistry 3021 'D', Physics 1021 'H', Biology 2021 'M', Computer Science 4281 'D', Mathematics General 4021 and Optional 4021A, Technical 9101/9111/9121/9131; compare with the 2082 'General' papers already built before treating them as new.
- Session 9 end: Mathematics Technical 2081 (9121) built. Next: Physics/Chemistry/Biology Technical 2081 (fetch the `2025/03/...Technical-Stream...` posts), Mathematics Technical 2082/2080, English 2080 'D' (`eng80d` cached), then Grade 11, SEE 7 provinces.

## Session 10 notes (same branch)
- Fresh sandbox again. `/tmp/gitenv.sh` echoes `$NEB_GH_TOKEN` (GIT_ASKPASS); `/tmp/gitrc` (outside the repo, chmod 600) exports GIT_ASKPASS, GIT_TERMINAL_PROMPT=0 and the token for `git push`. The repo is private, so even `git ls-remote` needs the token. Clone with `-b resources/past-papers-class12` to /tmp/NEB, `ln -sfn /tmp/NEB /app/neb`, `ln -sfn /tmp/psrc /app/psrc`. pip, `sudo apt-get update` + apt, fonts install as in session 4; `git config user.name/user.email` locally.
- Built Physics 2081 Technical 9131, Chemistry 2081 Technical 9111, Biology 2081 Technical 9101 (all from the `2025/03/...Technical-Stream...` posts; each has 4 to 5 images with p0 = banner, p1.. = exam pages). Physics, Chemistry bundles refreshed (Technical papers sit in the subject bundle of the same name), Biology bundle refreshed.
- **Builder gotcha (new):** a markdown table must be preceded by a BLANK line, otherwise it prints as flat `| a | b |` text. After writing a paper run a check: every line starting with `|` must follow a blank line or another `|` line (a 6-line python loop fixes it).
- `@q` Or-questions numbered separately in the printed paper (16 Or 17): put the second question inside the first `@q` after `@or` as `**17.** ...`, and answer under `@s 16` with an `Or (Q17)` line.
- Figures reused by regex from an earlier content file (copy the whole ```figure block) saves time: blast furnace, full wave rectifier, male reproductive system.
- Open points: Physics 9131 Q18(b) middle-cell emf (see above); Chemistry 9111 MCQ 11 (paracetamol chosen; Novalgin is also an antipyretic); MCQ keys and figures have had no teacher review.
- Next (in order): Biology 2080 Technical (`bioT80` cached), Physics/Chemistry Technical 2080 and 2082, Mathematics Technical 2082/2080, Mathematics 2082 other sets and 2080 other sets, English 2080 'D', Management / Humanities / Education / Law, Grade 11, SEE (7 provinces each), Grade 8.

## Session 11 notes (same branch)
- Fresh sandbox, third clone of the 3 GB repo (takes about 3 minutes; run `git clone --progress` in the background with nohup, a foreground clone hits the 60 s tool limit). Token only via `/tmp/gitenv.sh` (GIT_ASKPASS, reads `$NEB_GH_TOKEN`); never written to the repo. `ln -sfn /tmp/NEB /app/neb`, `ln -sfn /tmp/psrc /app/psrc`.
- Toolchain install as in session 10 worked unchanged (apt libpango + fontconfig, pip --user packages, `notes/pipeline/fonts/install.sh`, `fc-cache`).
- Built Biology 2080 Technical 9101 (`content/12-bio-2080-9101.md`); Biology bundle refreshed. Running `bundle_papers.py` rewrites every bundle PDF (non-deterministic bytes): `git checkout` the other subjects' bundles unless their contents changed.
- Visual checks that caught defects this session: matplotlib annotation text overlapping the drawing (give left-hand labels `ha='right'`), legend colliding with a title line, and a numbered list restarting after a table (use a bold paragraph instead of `4.`).
- Next (in order): Physics / Chemistry Technical 2080 and 2082, Mathematics Technical 2082/2080, Mathematics 2082 other sets and 2080 other sets, English 2080 'D', Management / Humanities / Education / Law, Grade 11, SEE (7 provinces each), Grade 8.

## Session 12 notes (same branch)
- Fresh sandbox; file-tool root `/app`, symlinks `/app/neb` -> /tmp/NEB, `/app/psrc` -> /tmp/psrc, `/app/view` -> /tmp/view (for page renders). Repo is ~2.3 GB: clone with `--depth 1 --single-branch --branch resources/past-papers-class12 --progress` under `nohup ... &` (a foreground clone is killed by the tool timeout, takes about 3 minutes). Token only through `/tmp/gitenv.sh` (GIT_ASKPASS reading `$NEB_GH_TOKEN`) and `/tmp/gitrc` (outside the repo).
- `sudo` works in this sandbox; apt / pip / fonts steps from session 4 worked unchanged.
- `$\text{\AA}$` prints "AA" in mathtext: type the unicode letter Å in plain text instead. Mathtext also needs `\sqrt{3}` inside `\frac{1}{\sqrt{3}}`.
- Built Physics 2080 Technical 9131 (`content/12-phy-2080-9131.md`). `bundle_papers.py` rewrites every bundle and bundles.json byte counts: after running it, `git checkout` the unrelated bundle PDFs and keep only the changed subject's entry in bundles.json.
- Also in session 12: English 2080 'D' built (`content/12-eng-2080-0041d.md`). The dhanraj index (627 posts, re-run `/tmp/index.py` style fetch of `/feeds/posts/default?start-index=N&max-results=150&alt=json`) has NO Chemistry Technical 2080/2082, Mathematics Technical 2080/2082 or Physics Technical 2082 posts: those need another source (nepalieducate / nebnotebank / Google-Drive scans, see session 7) before they can be built.
- Next (in order): Chemistry Technical 2080 and 2082 (find a source), Physics Technical 2082, Mathematics Technical 2082 / 2080, Mathematics 2082 other sets and 2080 other sets, English 2080 'D', Management / Humanities / Education / Law, Grade 11, SEE (7 provinces each), Grade 8.

## Session 13 notes (same branch)
- Fresh sandbox; file-tool root `/app`. Shallow clone of this one branch (`--depth 1 --single-branch`) took under 3 minutes in the foreground. `sudo apt-get update` is needed before `apt-get install libpango-1.0-0 libpangoft2-1.0-0 fontconfig` on a fresh image; then pip, `notes/pipeline/fonts/install.sh`, `fc-cache`.
- The session 12 claim that dhanraj has no Chemistry / Mathematics Technical 2082 post was wrong: the blogger feed search (`/feeds/posts/default?q=Chemistry%20Technical&alt=json`) finds `2026/03/Chemistry-Technical-Stream-Question-Paper-2082-2025-of-Class-12-NEB`, `2026/03/Mathematics-Technical-Stream-Question-Paper-2082-2025-of-Class-12-` and `2026/03/Physics-Technical-...`. Use the feed query, not only the cached index.
- New helper `tools/add_paper.py <id>`: builds one paper, adds it to manifest.json, refreshes only that subject's bundle and restores the other bundle PDFs. Use it instead of `build_paper.py --all` + `bundle_papers.py`.
- mathtext has no `\xrightarrow` and no `\tfrac`: use `\longrightarrow` and `\frac`, put the conditions in the sentence.
- Built Chemistry 2082 Technical 9111, Mathematics 2082 Technical 9121 and Physics 2082 Technical 9131. Next: Chemistry Technical 2080, then Mathematics 2082 / 2080 other sets, then Grade 11.
- Grade 12 Management / Humanities / Education / Law: the repo has no note book for them (`notes/content` has only phy, chem, bio, math, cs, eng, nep for grade 12 plus qbank12), so they are outside the 'every class in the note pipeline' scope unless the owner wants them added.
- Chemistry Technical 2080 and Mathematics Technical 2080: the blogger feed query for them returned nothing on dhanraj; they need another source (the 2082 Chemistry Technical page lists 2080 / 2081 / 2082 links only as text). Mathematics 2082 other sets (`4021`, `4021A`) and 2080 other sets also still need sources: `2026/03/Mathematics-Optional-Question-Paper-2082-2025-of-Class-12-NEB-PDF-Download` is the 4021A Optional paper.
- After session 13 the Grade 12 science / English / Nepali core is built for 2080-2082 except: Chemistry Technical 2080, Mathematics Technical 2080, Mathematics other sets of 2080 and 2082, and the old-course / optional papers.

## Session 14 notes (same branch)
- Fresh sandbox; file-tool root `/app`, `ln -sfn /tmp/NEB /app/neb`, `ln -sfn /tmp/psrc /app/psrc`, `ln -sfn /tmp/view /app/view`. Token only through `/tmp/gitenv.sh` (GIT_ASKPASS reading `$NEB_GH_TOKEN`); export `NEB_GH_TOKEN`, `GIT_ASKPASS=/tmp/gitenv.sh` and `GIT_TERMINAL_PROMPT=0` in EVERY bash call that touches git (each call is a fresh shell). The PAT was pasted into the task text: the owner should rotate it.
- **Clone recipe that worked (repo is ~2.3 GB):** the plain `--depth 1 --single-branch` clone dropped the connection ("unexpected disconnect while reading sideband packet"). Use `git clone --depth 1 --single-branch --filter=blob:none --branch resources/past-papers-class12 <url> /tmp/NEB` (fast, about 260 MB), then `git sparse-checkout init --no-cone` and `git sparse-checkout set '/notes/papers/*' '/notes/pipeline/*' '/notes/AUTHORING.md' '/notes/.gitignore'` and `git checkout`. Needs the token env for the lazy blob fetches. Working tree is about 23 MB. `AGENTS.md` / `ENV.md` show as deleted in `git status` because they are outside the sparse set: never `git add -A`; add explicit paths only and check `git status --short | grep '^D '` is empty before committing.
- Toolchain: `sudo apt-get update`, `apt-get install libpango-1.0-0 libpangoft2-1.0-0 fontconfig`, `pip install --user --break-system-packages weasyprint markdown matplotlib numpy pymupdf pillow requests`, `bash notes/pipeline/fonts/install.sh`, `fc-cache -f ~/.local/share/fonts/nebians`. All worked unchanged.
- `tools/add_paper.py` restores the other subjects' bundle PDFs with `git checkout`; with a partial clone that needs the token env, otherwise the unrelated bundles stay rewritten (run the checkout by hand afterwards).
- Mathtext: `pmatrix`, `array`, `\boxed`, `\xrightarrow` fall back; unbraced `\frac k{..}`, `\frac1{..}`, `\frac12`, `\sqrt3`, `\mathbb N`, `\frac{dx}x` fall back too. Brace everything and check the build output for `[math] fell back:`. Long chains of `\Rightarrow` in one display also failed: split into one display per step. A `|` inside inline math in a paragraph prints oddly: write rows in words.
- Source for Mathematics Optional 2082: `2026/03/Mathematics-Optional-Question-Paper-2082-2025-of-Class-12-NEB-PDF-Download.html` (cache key `mathopt82`, p1..p4 = exam pages). The page `2026/03/Mathematics-Question-Paper-2082-2025-of-Class-12-NEB.html` is the 0081 'R' paper already built.
- **Still open for Grade 12:** Chemistry Technical 2080, Mathematics Technical 2080, Mathematics 2080 other sets (grade increment), Mathematics 2082 `4021` general (named on the Partial page, source not found yet), old-course / optional papers of other subjects. Then Grade 11, then SEE and Grade 8 with all 7 provinces. The 2082 Optional English, Optional Nepali and many non-science subjects have posts on the source site (`2026/03/...`) but have no note book in this repo, so they are out of scope unless the owner wants them.

## Session 15 notes (same branch)
- Fresh sandbox, file-tool root `/app`, `ln -sfn /tmp/NEB /app/neb`, `ln -sfn /tmp/psrc /app/psrc`, `ln -sfn /tmp/view /app/view`. A plain `git clone --depth 1 --single-branch --branch resources/past-papers-class12` (full tree, 8943 files) worked in the foreground in under 3 minutes this time. Toolchain install as in session 14 worked unchanged (`pip` needs to finish before `/tmp/index.py` runs).
- **Math check script (new habit):** `matplotlib` failures are only recorded when the SVG is not already cached, and `add_paper.py` prints nothing about them. Extract every `$..$` / `$$..$$` from the content file and call `mathsvg.render()` on each, then print `mathsvg.FAILS` (10 lines, see `tools/mathcheck.py`). Typical fails: unbraced `\sqrt3`, `\dfrac\pi2`, `\dfrac a2`, `\mathbb Q` (use `\mathbf{Q}`).
- **Figure captions are not unicode-unescaped**: type the real character in a ```figure caption (`≤` printed literally); `\u..` inside the code lines is fine.
- `read_file` on a PNG can return a stale copy when the same path was read before: write renders to a new filename each time.
- Found on the source site and still not built (all in scope): none of Chemistry Technical 2080 / Mathematics Technical 2080 exist on dhanraj (feed query returned nothing again). Old-course papers that DO exist for note-book subjects: Mathematics Old Course 2081 (built this session), Compulsory English Old Course 2080 code 004 (`engold80`, 4 page images fetched).
