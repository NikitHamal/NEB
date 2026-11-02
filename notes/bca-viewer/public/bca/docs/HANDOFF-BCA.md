# BCA entrance books — handoff (start here)

Branch: `claude/bca-entrance-complete` (from `main` @ `bb19a74`). Written in one session by Claude
(Anthropic) for the NEBians open-learning platform. Read `AUTHORING-ENTRANCE.md` first (the contract),
then this file. The reader app that serves these books lives in the NEBians workspace under
`public/bca/` (see "Where the files are").

## State

| Book slug | Spine | Chapters | MCQs | bcacheck | PDF |
|---|---|---|---|---|---|
| bca-math | `curriculum/bca-math.md` (15 units, 50 Q) | 15 of 15 | 600 | OK | `NEBians-BCA-Entrance-Mathematics.pdf` |
| bca-eng | `curriculum/bca-eng.md` (7 units, 40 Q) | 7 of 7 | 272 | OK | `NEBians-BCA-Entrance-English.pdf` |
| bca-gk | `curriculum/bca-gk.md` (4 units, 10 Q) | 4 of 4 | 160 | OK | `NEBians-BCA-Entrance-General-Knowledge-and-IT.pdf` |
| bca-mock | `curriculum/bca-mock.md` (guide + 3 model papers of 100) | 4 of 4 | 300 | OK | `NEBians-BCA-Entrance-Model-Papers-and-Mock-Tests.pdf` |

In total 30 chapters and 1,332 keyed multiple-choice questions. Every chapter has the contract shape: opening,
"What the paper asks" box, one `## N.k` section per spine bullet, formula and fact sheet, chapter summary,
and Sets A (recall) / B (understanding) / C (application) each with an `::: note Answers …` box.

## What the exam is (and where sources disagree)

- **TU FOHSS BCA entrance**: 100 MCQs, 100 marks, 2 hours. English grammar 40 %, Mathematics 50 %,
  General Knowledge 10 %. Confirmed by the faculty-published description (edusanjal / educatenepal quoting
  the TU notice) and by the Dean's Office *Model Questions for BCA* (2018): Group A English Q1–40, Group B
  Mathematics Q41–90, Group C General Knowledge Q91–100.
- Mathematics area ranges (collegeinfonepal, consistent with the model paper): calculus 6–8, coordinate 5–8,
  trigonometry 2–5, vectors 1–2, algebra 8–10, arithmetic 8–10, reasoning 7–10. English: paragraph 4–5,
  grammar 35–45. GK and IT: about 5 + 5.
- **Disagreement, resolved on purpose**: a few sites (nepaliupdates, insightsnp) describe 4 × 25
  (English / Maths / Logical Ability / GK), and one blog (padmashreecollege) a 40-mark computer section.
  Neither matches the Dean's Office layout, so the books follow 40 / 50 / 10. `bca-mock/unit-01` says so
  to the student. If TU publishes a different pattern, change the spines and the three papers.
- **Not confirmed from a primary source**: no negative marking (every third-party page agrees; TU's page
  does not say), pass mark (35 vs 40 on different sites), the exact fee. The books state "no negative
  marking is reported" and tell students to read the notice of their year.
- The per-chapter question counts `[n]` in the spines are NEBians estimates inside the published ranges and
  add to exactly 50 / 40 / 10 / 100.
- The BCA programme table in `bca-mock/unit-01` (semesters I–VIII of the revised 2082-batch curriculum)
  is compiled from college and education-portal summaries, not from the TU PDF. It says so.

## Facts that must be refreshed (current affairs)

`bca-gk/unit-01` and `unit-02`, and model-paper questions 91–100, hold dated facts: Balendra Shah sworn in
as Prime Minister on 27 March 2026 after the 5 March 2026 election (RSP 182 of 275 seats); Sushila Karki
interim PM from September 2025; Kami Rita Sherpa's 32 Everest summits (17 May 2026); FIFA World Cup 2026
won by Spain (1–0 after extra time, 19 July 2026); Women's ODI World Cup 2025 won by India; Euro 2024 Spain;
Everest 8,848.86 m. Re-check these before every exam year. Miss Nepal winners are deliberately not listed.

## Verification done

- `python3 notes/tools/bcacheck.py notes/content/bca-*/unit-*.md` → 30/30 OK: frontmatter, every MCQ has a
  stem plus one `(a)…(d)` option line, option length ≤ 78 characters, stem ≤ 60 words, every question keyed,
  no run of five identical keys, no key letter above 40 % of a set, inline `$…$` paired, no unbraced
  `\frac12` / `\sqrt3` / `\mathbb`. Key spread over the whole set is 25 % ± 2 % per letter.
- Every numerical key was computed by hand while writing; calendar answers were checked in Python
  (1 Jan 2026 Thursday, 5 Mar 2026 Thursday, 27 Mar 2026 Friday, 15 Aug 2026 Saturday, 1 Jan 2025 Wednesday).
- The repo's own `check.py` / `mcqcheck.py` need Python 3.12 (nested f-string quotes) and WeasyPrint; the
  session had Python 3.11 and no Pango, so those two were **not** run. `bcacheck.py` (dependency-free) and
  `texfix.py` were added instead, and `bca_build.py` renders the PDFs with ReportLab.

## What is still missing (be honest with students)

- **Figures: 0.** The chapters are tables, equations and worked examples. Priority: unit circle and graph of
  sin/cos, line and circle sketches, conic shapes, Venn diagrams, a painted-cube drawing, clock faces.
- **MCQ depth is 40 per chapter** (A 20 / B 12 / C 8); `AUTHORING-ENTRANCE.md` asks for 50 where a chapter
  carries 3+ questions. Math units 1, 2, 4, 8, 9, 10, 12, 13, 14, 15, English 1–6, GK 1 and 3 are the
  ones to extend with a **Set D**. `bca-eng/unit-07` has 32 passage questions (4 passages).
- **Three model papers.** The spine allows more: add units 5–6 (Model Papers 4–5) in the same format.
- **No real past papers.** None were reachable as text from this environment except the 2018 Dean's Office
  model; every question here is original practice. Add 2078–2082 papers if the platform can license them.
- **Not reviewed by a BCA entrance teacher.** If a key is wrong, fix the Markdown, rerun `bcacheck.py`.
- **PDFs are ReportLab builds**, plain and readable, with maths converted to Unicode text (fractions as
  `(a)/(b)`). The house WeasyPrint pipeline gives nicer typography once Python 3.12 + Pango are available:
  `python notes/pipeline/build_pdf.py bca-math bca-eng bca-gk bca-mock`.
- **Web/app export** (`export_syllabus.py`, `export_study.py`) was not run. `spine.py` already has the
  `bca` track, and `gk`, `math`, `eng`, `mock` subjects; the exporters should pick the books up unchanged,
  but run `export_syllabus.py` and `export_study.py bca-math bca-eng bca-gk bca-mock` and look at the
  hub before announcing. The 0-negative marking is already in `TRACKS["bca"]`.
- Bachelor-course books (semester notes for BCA subjects) are the next track step (see HANDOFF-ENTRANCE).

## Where the files are

- Sources: `notes/content/bca-{math,eng,gk,mock}/unit-NN.md`; spines `notes/curriculum/bca-*.md`.
- Tools: `notes/tools/bcacheck.py`, `texfix.py`, `bca_build.py` (PDF + manifest).
- Built books: `notes/pdf/NEBians-BCA-Entrance-*.pdf`.
- Viewer: `notes/bca-viewer/` (Next.js reader + the same files under `public/bca/`).

## Sources

| Source | Used for |
|---|---|
| TU FOHSS notice as quoted by edusanjal.com/exam/bca-tu-entrance-exam | 100 MCQs, 100 marks, 40/50/10, eligibility |
| Dean's Office *Model Questions for BCA* (2018), hosted by nationalinfotechcollege.edu.np | the real layout and question style |
| collegeinfonepal.com BCA syllabus page | mathematics area ranges, English and GK topic lists |
| TU BCA syllabus summaries (texasintl.edu.np, nplupdates.com, collegenp.com) | programme structure, 2074 vs 2082 curricula |
| Reuters, Al Jazeera, The Hindu, Britannica (Mar–Apr 2026) | Prime Minister, election result |
| Britannica, People (Jul 2026) | FIFA World Cup 2026 |
| Department of Tourism release, 17 May 2026 | Kami Rita Sherpa's 32nd summit; Everest 8,848.86 m |
