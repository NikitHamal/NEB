# NEBians Study Notes — Session Handoff (for Claude Code on AgentSky)

Branch: `resources/neb-notes-11-12` (from `main` @ `a0f5c55`). Head at handoff:
`cc3e796c` (pushed). Goal: complete chapter-by-chapter study books (PDF) for
NEB/CDC Grade 11 & 12 Science + Compulsory English + Nepali, built from
Markdown sources in this repo, uploaded to the NEBians library.

## Session history (compacted) — AgentSky `claude-opus-5`, 2026-09-25 → 26

12,640 events, 7 user turns, ~76 subagent dispatches. The agent never had git
credentials, so it committed locally (`1d78b2c`, `c0846b7`) but never pushed;
the owner exported the tree as `6a54d59f`. Two sessions ran in parallel in the
same playground: this Claude session (content authoring) and a Deepseek
session (a separate ReportLab prototype in `/workspace/nebians` — unrelated,
ignore anything about `nbrender.py`/`figlib.py`/`bookkit.py`/`.py` content
modules; the shipped system is Markdown → `notes/pipeline` → WeasyPrint).

- **T1 – the brief (Sep 25 18:45 UTC).** Clone NEB; an account-deletion
  complaint ("not really effective") + resource requests for classes 8/11/12
  exposed an empty library. Task: research NEB/CDC end-to-end, then write
  complete no-shortcut notes (all subjects/chapters, Class 11+12 Science,
  figures/diagrams/tables/formulas/solutions/model questions). Method
  approved: parallel subagents, hours-long run. Agent started with recon
  (repo, `api.models.Resource`, toolchain) + syllabus research.
- **Research base.** Indexed the CDC PDF store (~11.5k files); pulled official
  CDC Grade 11/12 textbooks (Physics/Chemistry/Biology) + curriculum 2076/2078
  via Wayback where `neb.gov.np`/`moecdc.gov.np` routes 404/500. Chapter lists
  in `notes/curriculum/*.md` come from the official CDC tables of contents;
  each book's cover states its source (CDC vs NEB) explicitly.
- **T2 – "push to a new branch first, then keep writing" (Sep 26 04:35).**
  Created `resources/neb-notes-11-12`, commit `1d78b2c` (151 files, source +
  pipeline + spines). Continued authoring (chem12 units 13–14 etc.).
- **T3 – "push the made PDFs too, not just pipeline" (07:57).** `notes/pdf/`
  now ships built books alongside sources (`sync_notes.sh` pattern: mirror
  working tree → `notes/{content,curriculum,pipeline,pdf}`).
- **T4 – issue #48 (09:45).** Teacher/student review of the Physics 11 PDF.
  Fixes committed as `c0846b7`: inline-math hard-wrap repair, UNPAIRED-`$`
  check, `\\command` repair, MCQ option grid, per-answer answer keys,
  chapter-summary panel, site URL + N-watermark branding.
- **T5/T6/T7 – "push occasionally" + `continue` ×2 (11:20 → 13:16).**
  Steady-state authoring: cs12 OOP/C++ (9 programs actually compiled and run,
  real outputs pasted), chem11 organics, math11 17/18/21, chem12 07–09,
  eng11 grammar units 21–30, nep11 units 13–25. Session ended 18:45 UTC with
  work uncommitted (recovered since — see Recovery notes).

## How the work gets done (keep this architecture)

- **Swarm**: parent dispatches 2–4 chapter subagents with a tight brief
  (units, spine file, pipeline notes); each writes + validates + PNG-inspects
  its figures, reports words/figures/examples + check.py status.
- **Spine-first**: `notes/curriculum/<subj>.md` is law — frontmatter
  (title/hours/area) verbatim, every syllabus bullet a numbered `## N.N`
  section in spine order. Extra sections allowed only if labelled.
- **QA gate per chapter**: `check.py` must print `OK` (renders ALL math via
  mathsvg + ALL figures via figrun); every figure inspected as PNG via
  `preview.py` (private `/tmp` dirs), never judged from code. Practice sets:
  Group A MCQ + B short + C long, with answer keys/worked solutions.
- **Dialect** (`notes/AUTHORING.md` §1–13, read fully before writing):
  `::: key/definition/example/caution/tip/memory/note` boxes,
  `## N.N` sections, `**Group A/B/C**` practice, ` ```figure caption="..."`
  fences with real matplotlib code (`INK, MUTED, GRID, ACCENT, SERIES`).

## Repo map

- `notes/content/<subj><grade>/unit-NN.md` — chapter sources.
- `notes/pipeline/` — `build_pdf.py` (books), `check.py`, `preview.py`,
  `md2html.py`, `mathsvg.py`, `figrun.py`, `patchfig.py`, `spine.py`
  (`ALL` roster), `theme.css`, `brand/`, `fonts/` (README + install.sh only —
  fonts NOT vendored, fetch via install.sh).
- `notes/curriculum/*.md` — syllabus spines. `notes/pdf/` — built books
  (regenerate on any chapter change; never hand-edit). `notes/AUTHORING.md`
  — the contract.

## Coverage + built books (all in `notes/pdf/`, 2,820 pages total)

| Book | Units | Pages | MB |
|---|---|---|---|
| Physics 11 / 12 | 26/26, 25/25 | 381 / 271 | 11.2 / 9.3 |
| Chemistry 11 / 12 | 17/17, 21/21 | 258 / 319 | 4.7 / 5.7 |
| Biology 11 / 12 | 8, 7 units | 167 / 153 | 4.0 / 3.2 |
| Mathematics 11 / 12 | 21/21, 16/17 | 368 / 329 | 13.9 / 13.6 |
| CS 11 / 12 | 4/8, 7/7 | 76 / 148 | 1.4 / 2.2 |
| English 11 | 23/35 (units 01–13, 21–30) | 235 | 2.6 |
| Nepali 11 | 13/27 (units 13–25) | 115 | 1.2 |

Missing: English 12 + Nepali 12 (not started, no sources), math12 unit-09
(Product of Vectors), eng11 units 14–20, nep11 units 01–12, cs11 units 05–08.

## Gotchas (learned the hard way — do not regress)

1. Inline `$...$` must never hard-wrap across source lines — delimiters pair
   with neighbours and raw LaTeX reaches the PDF. `check.py` fails the file
   on UNPAIRED `$`.
2. `\\command` prints the bare word; single backslash for commands.
3. Braced args always: `\sqrt{3}` not `\sqrt3`, `\frac{1}{2}`. (mathtext
   strictness varies by matplotlib version — the braced form passes
   everywhere.)
4. No `\underline` in mathtext — restate without it.
5. Figure fences on their own lines, one block per figure; PNG-inspect all.
6. MCQ runs → option grid; multi-part → stacked parts; answer keys one line
   per answer; `## Chapter summary` in a highlighted panel (all pipeline).
7. Devanagari needs Noto Sans Devanagari installed or figures fall back
   (findfont warnings) — and Windows builds need `PYTHONUTF8=1` + a UTF-8
   console or Nepali titles crash the build.
8. Branding: `nebians.consica.com.np`; N mark watermark from `pipeline/brand/`.

## Recovery notes (what happened between the session and this file)

After the session died with work uncommitted, its 44 post-export units were
replayed op-by-op from the session event log into `notes/content` and
verified with `check.py` (42 clean immediately). Three minimal fixes were
required, all matching session intent: 7× unbraced `\sqrt` (the session's own
`sed` for this was a GNU-`\s` no-op), 1× `\underline` unwrap in math12
unit-01. All 12 books were then rebuilt with the repo pipeline (WeasyPrint 70
+ Pango/Cairo + the 5 book fonts) and committed with the sources.

Build recipe that works: `build_pdf.py` resolves its theme as
`<parent-of-pipeline>/build/theme.css`, i.e. it expects a working tree shaped
`nebians/{content,curriculum,build,pdf}`. To build from this repo, copy
`notes/content`, `notes/curriculum`, `notes/pipeline/*` into scratch as
`nebians/{content,curriculum,build}` and run `build_pdf.py <targets>` there
(`targets` default to `spine.ALL`); copy PDFs back to `notes/pdf/`.
Proven env: Python 3.12, matplotlib 3.11.2, WeasyPrint 70. Physics-scale
books take ~5–9 min each; build big subjects one at a time.

## Continue-job checklist

1. Write the missing units (table above), each `check.py`-OK + PNG-inspected.
2. Rebuild affected books, confirm page counts grow, commit sources + PDFs.
3. Keep issue #48's bar: teacher/student-facing accuracy first, NEB exam
   pattern (Group A 11×1, B 8×5, C 3×8 for model questions).
