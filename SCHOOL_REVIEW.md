# SCHOOL_REVIEW.md

Branch `polish/school-books-claude` (from `main` f372ce8). Read with SYLLABUS_DIFF.md, SCHOOL_SOURCES.md, SCHOOL_INVENTORY.md, POLISH_ENV.md.

## Bottom line (honest)
- The brief asks for an end-to-end re-audit and rewrite of 36 school books (~3.3 M words). **That did not happen.** I audited all 36 mechanically and verified six against outside sources; I found and fixed **two** small defects and rebuilt **one** PDF.
- **The brief's headline example could not be confirmed.** I found no evidence that the current Class 8 curriculum has Python instead of QBASIC. Evidence says QBASIC is still the Class 8 language and that Python replaced it in Class 9 (2082) and Class 10 (2083), where the repo is **already correct**. I therefore did **not** remove QBASIC from `cs8`. This is an open decision for you (SYLLABUS_DIFF.md §1).

## Audited
- All 36 school slugs (cs8…qbank12): spine ↔ chapter ↔ frontmatter ↔ PDF presence, section coverage, stale-term scan (`notes/tools/school_audit.py`, new, reusable).
- Outside-source unit/hour checks: cs10, sci10, math10, cs11, chem11, phy11.

## Found
1. eng10 u4 — model letter by a 20-year-old "after passing my SLC" (SLC no longer exists). Fixed.
2. acc10 u14 — frontmatter area ≠ spine. Fixed (no PDF effect).
3. Pipeline portability: `md2html.py` needs Python ≥ 3.12 (SyntaxError on 3.11) and the fonts are not vendored; building without them silently degrades figures. Not changed; documented in SCHOOL_INVENTORY.md.
4. Everything else flagged by the audit was a false positive or a deliberate keep (listed in SYLLABUS_DIFF.md §4).

## Fixed (SYLLABUS_DIFF items → commits)
| Item | Commit |
|---|---|
| tooling + POLISH_ENV.md + acc10 u14 area | 0e4b9ff |
| eng10 u4 SLC→SEE + rebuilt PDF | 9892c97 |
| four audit docs + inventory | see `git log` tip of this branch |

## PDF rebuild evidence (eng10)
- Rebuilt with the repo pipeline (`build_pdf.py eng10`, Python 3.12.16, WeasyPrint 70, fonts from `fonts/install.sh`): **281 pages**, 5.8 MB; the committed original was 281 pages, 5.96 MB.
- `pdftotext` diff old↔new: the intended SLC→SEE line plus line-wrap/hyphenation shifts (63 differing lines, same page for every unit start) caused by newer WeasyPrint/Pyphen. Page 60 (the edited page) rendered side-by-side with the original: identical cover/header/watermark/boxes/page number.
- Not eyeballed: the other 280 pages (identical source, same pipeline; I checked the edited page, unit start pages and the cover only). No `qa_pdf.py` exists in the repo.
- `audit.py` on eng10 + acc10 chapters:
```
ok  ../content/eng10/unit-17.md  | 4307 words, 5 figures, 2 photos, 3 worked examples, OK
ok  ../content/eng10/unit-18.md  | 4792 words, 5 figures, 2 photos, 3 worked examples, OK

==== 33 files, 3 FAILED
```
- `school_audit.py` after fixes:
```
13 issue(s)
[OUTDATED?] cs8 u-: old Windows version: u13:1x@L292
[OUTDATED?] eng8 u-: SLC (replaced by SEE from 2073 BS): u10:1x@L39
[MISSING] math8 u15: 3 numbered sections for 4 syllabus bullets
[MISSING] acc10 u12: 6 numbered sections for 9 syllabus bullets
[MISSING] acc10 u15: 7 numbered sections for 8 syllabus bullets
[OUTDATED?] cs10 u-: census 2068 population as current: u4:3x@L1672
[OUTDATED?] eng10 u-: SLC (replaced by SEE from 2073 BS): u15:1x@L455
[OUTDATED?] qbank10 u-: census 2068 population as current: u14:1x@L68
[OUTDATED?] qbank10 u-: Python 2 idiom: u22:1x@L552
[OUTDATED?] cs11 u-: dead browser/plugin: u6:1x@L315
[OUTDATED?] eng11 u-: SLC (replaced by SEE from 2073 BS): u23:1x@L56
[OUTDATED?] bio12 u-: census 2068 population as current: u9:3x@L123
[OUTDATED?] eng12 u-: SLC (replaced by SEE from 2073 BS): u23:1x@L54
```
(remaining lines are the reviewed false positives / deliberate keeps.)

## Open (nothing below is marked done)
1. **cs8 / qbank8 QBASIC vs Python** — needs the CDC Class 8 primary document or your confirmation of the target course.
2. **Class 10 English, Nepali, Social, Optional Maths** — verify against the 2083 BS CDC editions (spines cite 2080).
3. **All C-graded subjects** (see SCHOOL_INVENTORY.md) — no outside-source syllabus re-research, no line-by-line factual reread. Includes classes 11/12 English, Nepali, Maths, Biology, Chemistry 12, Physics 12, CS12, and every Class 8 subject except none verified.
4. Depth/clarity/typo polish pass over every chapter — not performed.
5. The CDC library and `moecdc.gov.np/storage` PDFs were unreachable from the sandbox, so no *primary* curriculum PDF was read for classes 8, 11, 12.

## Judgement calls
- Kept QBASIC in Class 8 (above).
- Left "an SLC certificate" in eng11/eng12 u23 (valid article example; avoids two large PDF rebuilds).
- Used the spine as authority when a secondary source disagreed (cs11 unit-8 hours).

## Security
The PAT you pasted has been shared across sessions and was used here. It was passed per command (`http.extraheader`) and never written to the repo, remote URL or git config. **Rotate it now.**
