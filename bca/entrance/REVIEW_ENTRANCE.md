# REVIEW_ENTRANCE — audit of the BCA entrance books

Reviewer: second Claude session, on top of the first session's work (commit `9fbf94e`).
Scope: 30 chapters (15 Mathematics, 7 English, 4 GK and IT, 4 model-paper chapters), 1,332 keyed MCQs, 4 PDFs.

## 1. What was checked, and how

| Check | Method | Result |
|---|---|---|
| Structure: frontmatter, one option line per MCQ, option and stem length, every question keyed, no orphan keys, key spread, paired `$`, no unsupported TeX | `notes/tools/bcacheck.py` over all 30 chapters | 30/30 OK. Key spread 25 % ± 2 % per letter overall |
| Slop markers: TODO, TBD, lorem, placeholder, "refer to textbook" | `grep -i` over `notes/content/bca-*` | none found |
| Answer correctness | I recomputed every key by hand in **Mathematics unit 5** (sequences and series, 40 questions) and **unit 6** (matrices and determinants, Sets A and B, 32 questions; the Set C key lines were cut off in my read and were not rechecked) | 0 wrong keys in 72 questions. The explanations also state why the tempting distractor is wrong (for example unit 5 Set B Q9 notes that 5,050 is the sum of 1 to 100, not of the even numbers) |
| Exam pattern | Re-read edusanjal's reproduction of the TU FOHSS notice, hamrocsit.com, educatenepal.com, the Dean's Office model-question notice mirrored by divyagyan.edu.np | 100 MCQs / 100 marks / 2 hours; 40 / 50 / 10 split confirmed. Dissenting "4 × 25" sites remain unconfirmed and are already flagged in `model-papers/unit-01` |
| Dates and current affairs | Searched again: Reuters via NBC News, 27 Mar 2026 | Balendra Shah sworn in as Prime Minister on 27 March 2026; RSP won 182 of 275 seats in the 5 March 2026 election. Matches `gk-and-it/unit-01` |
| 2083 exam date | edusanjal notice listing | 16 August 2026; applications 29 Jun – 14 Aug 2026. Matches the "mid-August 2026" wording in `model-papers/unit-01` |
| Programme table (semesters I–VIII, 2082 batch) | Compared with the full revised-curriculum listing on texasintl.edu.np, September 2026 | Identical, subject for subject |
| PDF quality | Built with WeasyPrint, rendered pages to PNG and looked at them | see §4 |

## 2. What is good

- The books follow the real paper layout (Group A English Q1–40, B Mathematics Q41–90, C GK and IT Q91–100) instead of the loosely described 4 × 25 variants.
- Every chapter has the same shape, and every question has a keyed explanation. Wrong-answer reasoning is in the explanation, not only the right answer.
- The honest-sourcing notes ("source honesty", "where the sources disagree") are accurate and should stay.
- Numerical keys that I recomputed were all correct, including the trap-type items (|2A| for a 3 × 3 matrix is 16, not 4).

## 3. What was wrong or weak, and what was done

| # | Finding | Action |
|---|---|---|
| 1 | Eligibility was given only as D / CGPA 1.8. Current sources split it by Grade 12 pass year (2079 BS or later: D and 1.8; earlier: D+ and 2.0) and note the grade-12 certificate must be shown at entrance | **Fixed** in `notes/content/bca-mock/unit-01.md` §1.1 |
| 2 | Pass mark: sources say 35 (hamrocsit) and 40 (educatenepal); TU lists none. The book said nothing | **Fixed**: stated as unconfirmed, with the advice that rank decides admission |
| 3 | The book told students about the programme but not where the full course is | **Fixed**: points to `bca/course/CURRICULUM.md` |
| 4 | PDFs were plain ReportLab output; every formula flattened to text such as `(a)/(b)`, MCQ options running together | **Fixed**: all four books rebuilt with WeasyPrint. Stacked fractions, roots, coloured example, caution, tip and memory boxes, option grids, cover, contents page, bookmarks, running headers |
| 5 | Sources lived only under `notes/content/`, with no browsable entrance tree and no PDFs beside the Markdown | **Fixed**: `bca/entrance/` mirrors the sources with `sync_entrance.sh`, PDFs in `bca/entrance/pdfs/`. The older PDFs in `notes/pdf/` were overwritten with the new builds |
| 6 | The repo's own `check.py` / `mcqcheck.py` were never run (Python 3.11 here, they need 3.12) | **Not fixed.** `bcacheck.py` is the only structural check that was run |

## 4. Still open (honest limitations)

- **Only about 7 % of the keys (72 of 1,332) were independently recomputed in this pass.** The rest pass the structural checker but have not been re-solved by a second person. A BCA entrance teacher should review the sets.
- **No figures** in the entrance books (unit circle, conic sketches, Venn diagrams, clock faces). Priority for the next session.
- **MCQ depth** is 40 per chapter where `AUTHORING-ENTRANCE.md` asks for 50 on heavy chapters; maths units 1, 2, 4, 8–10, 12–15 and English 1–6 are the ones to extend.
- **Three model papers only.** The spine allows five.
- **No real past papers.** None were reachable as text except the 2018 Dean's Office model. Every question is original practice.
- **GK and IT current affairs** are dated to mid-2026 and expire; the FIFA World Cup 2026, Women's ODI World Cup 2025, Kami Rita Sherpa and Everest-height claims were taken over from the first session's sourcing and not re-searched here (only the Prime Minister / election item was).
- Entrance PDFs are text-math (Unicode and CSS fractions), not LaTeX-typeset; complicated expressions are legible but not publication typography.
