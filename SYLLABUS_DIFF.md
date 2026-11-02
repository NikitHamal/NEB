# SYLLABUS_DIFF.md

Contract for the polish pass. **Read §0 first: this is not the exhaustive topic-by-topic diff the brief asked for.** It records what was actually compared, how, and what was found. Status column: FIXED (with commit), MATCH, OPEN, or NOT-CHECKED.

## 0. What was and was not done
- **Done, all 36 school books (classes 8/10/11/12, incl. question banks):** mechanical audit with `notes/tools/school_audit.py` — every spine unit has a chapter file; frontmatter title/hours/area equal the spine; numbered sections ≥ syllabus bullets (English/maths/science/CS/accountancy); stale-term scan (QBASIC, Windows XP/7/8, Office 2003–2013, Flash/IE, SLC, HSEB, 75 districts, zones/development regions, Python 2, census-2068-as-current).
- **Done, against an outside source (see SCHOOL_SOURCES.md):** unit lists of cs10, sci10, math10 (A/A-/B+), and unit lists + hours of cs11, chem11, phy11 (B).
- **NOT done:** an independent topic-by-topic re-derivation of the official syllabus for every subject, and a line-by-line factual re-read of ~3.3 M words of chapter text. The remaining subjects are graded **C** in SCHOOL_INVENTORY.md (self-consistent, not independently re-researched). The brief's premise that "there are almost certainly more misses" is therefore **neither confirmed nor refuted** for them.

## 1. Class 8 — Computer Science (`cs8`)  → **OPEN DECISION, not changed**
| Item | Class | Evidence |
|---|---|---|
| Unit 20 "Computer Programming using QBASIC" (and QBASIC in units 5, 6, 18, 19; qbank8 units 23–25) | **UNVERIFIED — kept** | The brief says the current Class 8 curriculum has Python and QBASIC "should not be there at all". I found **no source saying that**. Every Class 8 source found (2023–Nov 2024 CDC-aligned books) teaches QBASIC; the Dec 2024 CDC-curriculum study says the CDC wants to retain QBASIC at this level. Python replaced QBASIC in **Class 9 (from 2082 BS) and Class 10 (from 2083 BS)** — and the repo's `cs10` already reflects that. The CDC's published Class 8 set also has no Computer book (computer content sits in Science), so the 20-lesson course is a school-level/local subject. The primary document (CDC basic curriculum 2076, class 6–8) could not be opened from the sandbox. |
| Existing spine note | — | Spine already says QBASIC is kept deliberately and each programming lesson also shows Python. |
| **To resolve** | | Provide the CDC Class 8 Computer/Science curriculum PDF or textbook page that lists Python (or confirm the school/palika course you target). If confirmed, the change is: delete unit 20 + QBASIC passages in units 5/6/18/19 and qbank8 units 23–25, add a Python unit, rebuild `cs8` and `qbank8`. I did not do this on an unverified premise: removing a taught, examined lesson cannot be undone silently. |

## 2. Class 10
| Subject | Result |
|---|---|
| `cs10` Computer Science | MATCH. Already the Python curriculum (QBASIC/C gone, 0 mentions). 5 units match CDC list; unit 4 sections 4.1–4.7 cover revision, functions, libraries, Turtle, errors, pandas CSV, matplotlib. |
| `sci10` | MATCH — 19 units identical to the CDC textbook. |
| `math10` | MATCH — 18 chapters identical to the CDC textbook contents. |
| `eng10` | **FIXED** (9892c97) — FACTUAL/OUTDATED: model letter "After passing my SLC" → "SEE"; PDF rebuilt. `eng10` u15 reading passage mentions an older man who "passed the SLC examination" — correct for his generation, kept. |
| `acc10` | **FIXED** (0e4b9ff) — STRUCTURAL: u14 frontmatter `area` said "Government Accounting of Nepal", spine says "Control and Audit". No PDF change (PDF takes areas from the spine). Audit also flagged u12 (6 sections / 9 bullets) and u15 (7/8): reviewed, bullets are merged into combined sections (e.g. 12.3 = consolidated fund + its operation) — MATCH. |
| `eco10, omath10, nep10, soc10, qbank10, qbankc10` | Structure MATCH; **NOT-CHECKED** against an outside source. Note: listings show 2083 BS editions of CDC Class 10 Nepali, English, Maths, Science, Social and Optional Maths; `eng10/nep10/soc10` spines cite the 2080 edition. I verified Maths and Science unit lists are unchanged; English, Nepali, Social, Optional Maths are **not verified against the 2083 editions** → OPEN. |

## 3. Class 8 (other subjects), 11, 12
All: structure MATCH (spine↔chapters↔PDF). Outside-source checks: `chem11` (17 units, all hours), `phy11` (26 units, all hours), `cs11` (8 units; unit-8 hours 10 vs secondary source 8 — spine total 80 h = official, secondary source total 78 → spine kept). Everything else NOT-CHECKED against an outside source.
`math8` u15: 3 sections for 4 bullets — "ratio of areas of similar triangles" is covered by a worked example in 15.3 — MATCH.
`health8`, `nep8`, `soc8`, `soc10`: audit initially flagged hundreds of "missing sections"; false positive — Nepali-medium books do not use `## N.k` numbering, so the check is skipped for them (they are **not** verified section-by-section).

## 4. Stale-term hits reviewed and deliberately left
| Hit | Why kept |
|---|---|
| `cs8` u13 "Windows 7" | Still true (unsupported). `cs8` u5/u6 already state Windows 10 support ended 14 Oct 2025. |
| `eng8` u10 "SLC/SEE" | Quotes a real 2021 job advertisement. |
| `eng11`/`eng12` u23 "an SLC certificate" | Article-before-vowel-sound example; people still hold SLC certificates, rule is unchanged. Changing it would force two 35-chapter PDF rebuilds for no accuracy gain. |
| `cs11` u6 `<bgsound>` / Internet Explorer | Explicitly taught as obsolete. |
| census 2068 (26.49 M) in `cs10`, `bio12`, `qbank10` | Appears alongside 2021 data (29.16 M); correct as historical series. |
| `qbank10` u22 "Python 2, 3, 1" | Regex false positive (question counts). |

## 5. Added after the second pass (FACTUAL/STRUCTURAL → fixed; one OPEN)
| Item | Class | Status |
|---|---|---|
| acc10 u12 figure printed literal `\n` | STRUCTURAL | FIXED (this branch's tip commit) |
| acc10 u11 figure labels overflow boxes / below 6.8 pt | STRUCTURAL | FIXED (tip commit) |
| eng10 u7 figure labels overlap | STRUCTURAL | FIXED (tip commit) |
| `\%` … `\times` prints `imes` (25 spots / 7 chapters, confirmed on acc10 p148 in old and new PDF) | FACTUAL (rendering) | **OPEN**, see SCHOOL_REVIEW.md |
