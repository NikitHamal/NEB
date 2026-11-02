# IOE books — audit and review (Nov 2026)

Scope set by the brief: audit, fix what is found, build PDFs through the house pipeline — **not** rewrite. Everything below was run in this session; commands and numbers are real.

## What was audited, and how

| Check | Method | Result |
|---|---|---|
| Maths and figures render | `notes/pipeline/check.py` on all 23 chapter files; then full `build_pdf.py` build of all 5 books | 23/23 OK; 0 maths fall-backs, 0 figure failures |
| MCQs are tied to keys | `notes/tools/mcqcheck.py` on all 23 files | 737 MCQs, every one keyed, no unkeyed list, no over-long option, no non-contiguous answer box, no run of 5 equal keys |
| Key-letter spread | same | per book a/b/c/d within ≈ 22–29 %; the two 100-question papers: 24/23/28/25 and 23/24/27/26 |
| Syllabus alignment | Official PDF text extracted with `pdftotext`; **86 numbered syllabus items** compared with the **86 spine bullets** (22 maths, 35 physics, 17 chemistry, 12 English); fuzzy match of wording; then term-by-term grep of the chapters for 29 specific official sub-topics (Poiseuille, Reynolds, triple point, Otto/Diesel, Seebeck/Peltier/Thomson, banking, conical pendulum, polarization, Higgs, dark matter, gravitational wave, black hole, seismology, …) | Item count matches exactly. Maths spine ≈ verbatim; physics/chemistry/English bullets are condensed paraphrases of the official lines (22 of 86 below 0.90 similarity), but every probed sub-topic is taught in the chapters. No missing official topic found. |
| Exam pattern and subject marks | Official sources found by web search (IOE admission page as quoted by collegenp.com, edusanjal.com notice summary, icenepal.com booklet reading, allresultnp.com) | Confirmed: computer-based, 100 MCQs, 140 marks, 2 h, Section A 60×1 and Section B 40×2 (booklet headers), 10 % **of the question's own marks** deducted (−0.1 / −0.2); subjects 50/40/30/20. Matches `ioe-mock/unit-01`. |
| PDF layout | `bca/tools/qa_pdf.py` on the 5 PDFs + eyeballed contact sheets | 0 failures; cover, linked contents, running heads, page numbers, fonts, no margin overflow, no clipped code, no leaked TeX |

## Findings and fixes

| # | Finding | Action |
|---|---|---|
| 1 | **Guide overclaimed.** `ioe-mock/unit-01` said third-party sources "agree" on the Maths 20 + 15 split. One (allresultnp.com) lists Maths 14 + 18; its table totals 54 one-mark + 43 two-mark questions, which contradicts the booklet's 60 + 40, so it is wrong. | **Fixed** — the sentence now says "most sources", names the contradiction and why it fails. The split itself is unchanged and still labelled a NEBians estimate. |
| 2 | **Eligibility vague.** Guide said "45 % marks in the qualifying examination". The 2083/84 notice (edusanjal summary) specifies 45 % in Physics, Chemistry and Mathematics in Class 11 and 12 and ≥ C grade in each for NEB candidates. | **Fixed** in `ioe-mock/unit-01`; web JSON `ioe-model-papers` re-exported (only that chapter's files changed). |
| 3 | **No PDFs.** | **Fixed** — five PDFs built with the house pipeline: 179 pages total (50 + 42 + 26 + 31 + 30). |
| 4 | **`\bmod`-style mathtext failures** from the earlier import were already normalised: the build reports 0 maths fall-backs. | none needed |
| 5 | **Front-matter orphan (house layout, all short books).** The "Contents" area label (e.g. MATHEMATICS) can sit alone at the foot of page ii with its list on the next page; the second front-matter page is mostly empty. Seen in every IOE and BCA book. | **Open.** Cause is `theme.css` / front-matter flow in `notes/pipeline`, shared with every shipped book. A one-line `break-after: avoid` on `.toc .area` plus keeping the contents on one page is the fix; not applied because it changes the look of books I did not rebuild. |
| 6 | **Zero figures in every chapter** (contract asks 1–4 per chapter): projectile and v–t graphs, ray diagrams, circuits, conics, p–n junction. | **Open — not fixed.** Authoring work, not an audit fix. |
| 7 | **MCQ counts below the contract** (≥ 40 per chapter, 50 for chapters with ≥ 3 paper questions). Actual per chapter — Maths: 30, 34, 24, 26, 32, 23, 23; Physics: 32, 22, 22, 20, 26, 20; Chemistry: 34, 28, 28; English: 28, 32, 18, 25. Every chapter is short of the contract. | **Open — not fixed.** Needs a Set D per chapter (new, verified questions). |
| 8 | **Two of five model papers** (`ioe-mock` units 2–3). | **Open.** |
| 9 | **Readers apply flat −0.1** to every question; IOE deducts 10 % of the question's marks (Section B: −0.2). Per `notes/HANDOFF-IOE.md`; the book text states the true rule. | **Open** (app/web code, outside this task). |
| 10 | **Cycle dates.** Guide states the 2083/84 cycle (exam from 11 Shrawan 2083; original notice said 28 Asar and was revised). That cycle has now run. | Left as published history; **must be re-verified for the 2084 cycle.** |

## What this audit did NOT do

I did not independently recompute the numerical answers of the 737 MCQs or read all ≈ 47,000 words for factual errors. The checks above are mechanical (render, key-tied, syllabus coverage, pattern) plus the source cross-checks listed. A subject-teacher read and a Python recomputation of every numerical key remain to be done, and the books say they are not faculty-reviewed.
