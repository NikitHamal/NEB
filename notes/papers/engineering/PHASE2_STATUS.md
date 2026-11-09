# Engineering papers, Phase 2 status (read this first, then PAPERS_TRACKER.md)

Branch `claude/engineering`. Phase 1 (download) is in `../PAPERS_TRACKER.md`. This file tracks the work: catalog, typesetting, what is next.

## Done so far
| What | Where | State |
|---|---|---|
| Catalog of every paper on disk (4,086 files: Pokhara 3,093, TU IOE 949, KU 13, CTEVT 11, Purbanchal 8, NEC 7, IOE entrance 5) by university / semester / subject / year / kind | `catalog.json`, `catalog-tree.json` (nested, app-ready), `CATALOG.md` | DONE. Regenerate: `python3 tools/catalog.py && python3 tools/catalog_md.py` (needs only git tree + manifests) |
| Paper pipeline imported from `resources/past-papers-class12` | `../build_paper.py`, `../bundle_papers.py`, `../paper.css`, `../tools/` | DONE. `build_paper.py` now accepts `level:` (instead of `grade:`), `cal:` and env `PAPERS_CONTENT`, `PAPERS_OUT` |
| Typeset paper 1: IOE Engineering Mathematics I (ENSH 101), 2081 Chaitra, regular new course, 60 marks | `content/ioe-ensh101-2081-chaitra.md` -> `pdf/NEBians-IOE-Past-Paper-Engineering-Mathematics-I-ENSH101-2081-Chaitra.pdf` (12 pp) | DONE. Transcribed from the scan image (not OCR), all 14 questions solved in full and re-checked (Q6 by factoring the curve, Q11 by substitution, Q13 by substitution, Q14 by initial conditions) |

## Next paper candidates (same PDF, `tu-ioe/past-questions-bani/1st-semester/1st-Semester-Engineering-Mathematics-I-New-Course__1UcnNWV9.pdf`)
- 2081 Baishakh (pages 1-2) and 2081 Kartik (pages 3-4) Engineering Mathematics I: same PDF, scans, OCR text is garbage, read the page PNGs.
- Then every file in `sources/tu-ioe/past-questions-bani/1st-semester/` (21 files; Engineering Physics, Chemistry, Drawing, Applied Mechanics, Basic Electrical). Many are multi-year compilations: split by exam sitting, one md per sitting.
- Then semesters 2 to 8 in the same folder layout, ranked by student demand: Maths II/III, Programming, Digital Logic, Electrical Machines, Structural Analysis.

## Environment recipe (no root, no apt; worked in this sandbox)
```
curl -sL https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj -C /tmp/mmx bin/micromamba
MAMBA_ROOT_PREFIX=/tmp/mroot /tmp/mmx/bin/micromamba create -y -p /tmp/menv -c conda-forge python=3.12 pango fontconfig poppler tesseract
/tmp/menv/bin/pip install weasyprint markdown matplotlib numpy pymupdf pypdf fonttools pillow sympy scipy cryptography requests
(cd notes/pipeline/mathjax && npm install)          # the pipeline typesets maths with MathJax now, not mathtext
PATH=/tmp/menv/bin:$PATH bash notes/pipeline/fonts/install.sh
PATH=/tmp/menv/bin:$PATH FONTCONFIG_PATH=/tmp/menv/etc/fonts PAPERS_CONTENT=$PWD/notes/papers/engineering/content PAPERS_OUT=$PWD/notes/papers/engineering/pdf python3 notes/papers/build_paper.py <id>
```
Tesseract 5 with 125 languages is in that env (use `-l eng`) for scans whose page images are too small to read.

## Gotchas learned
- Sparse clone: `git checkout` without sparse rules downloads ALL blobs (~2 GB). Set `git sparse-checkout set --no-cone '/*' '!/notes/papers/engineering/sources/' ...` BEFORE the first checkout. Read single files with `git show origin/claude/engineering:<path>`.
- A math expression containing `\begin{...}` is exempt from the pipeline's auto "a = b = c" aligned splitter (wrap an inline chain in `\begin{gathered}...\end{gathered}`).
- Do not write `### Question N` headings in solutions: `@s N` already prints one.
- `git add` with one nonexistent path stages nothing at all.
- The file-edit tool root was `/home/user/sandbox`; the repo clone is `/home/user/sandbox/neb` (`/app` was root-owned and not writable here).

## Honest scope note
The repo holds 4,086 papers but only ONE has been re-typeset with worked solutions so far. The rest are the original scans/DOCs, catalogued and ready. Pokhara DOC/DOCX (2,559 files) need LibreOffice conversion first (not installed; try `micromamba install libreoffice` into /tmp/menv).
