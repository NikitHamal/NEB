# Engineering papers, Phase 2 status (read this first, then PAPERS_TRACKER.md)

Branch `claude/engineering`. Phase 1 (download) is in `../PAPERS_TRACKER.md`. This file tracks the work: catalog, typesetting, what is next.

## Done so far
| What | Where | State |
|---|---|---|
| Catalog of every paper on disk (4,086 files) by university / semester / subject / year / kind | `catalog.json`, `catalog-tree.json`, `CATALOG.md` | DONE. Regenerate: `python3 tools/catalog.py && python3 tools/catalog_md.py` |
| Paper pipeline (`../build_paper.py`, `../paper.css`, `../../pipeline`) | `notes/papers/` | DONE. Takes `level:`, `cal:`; env `PAPERS_CONTENT`, `PAPERS_OUT` |
| 6 papers typeset with full worked solutions (every question and every OR) | `content/*.md` -> `pdf/NEBians-IOE-Past-Paper-*.pdf` | DONE (see table below) |
| Subject bundles + master All-in-One book | `bundle_engineering.py` -> `pdf/bundles/`, `bundles.json` | DONE for the 2 subjects that have 2+ papers; re-run after each new paper |

### Papers finished
| id (content/<id>.md) | Paper | Source scan | Pages |
|---|---|---|---|
| ioe-sh101-2081-baishakh | Eng. Maths I, regular new course | `1st-semester/1st-Semester-Engineering-Mathematics-I-New-Course__1UcnNWV9.pdf` p1-2 | 12 |
| ioe-sh101-2081-kartik | Eng. Maths I, back paper | same PDF p3-4 | 14 |
| ioe-ensh101-2081-chaitra | Eng. Maths I, regular | same PDF p5-6 | 12 |
| ioe-sh151-2081-ashwin | Eng. Maths II, regular | `2nd-semester/2nd-Semester-Engineering-Mathematics-II-New-Course__.pdf` p5-6 | 11 |
| ioe-ensh151-2082-bhadra | Eng. Maths II, regular | same PDF p3-4 | 11 |
| ioe-ensh151-2083-baishakh | Eng. Maths II, back paper | same PDF p1-2 | 10 |

Reading notes: the 2083 Baishakh year is printed as such on the scan (checked at 300 dpi). In that paper Q2(a) has an illegible outer upper limit (solved as x from 1 to 2, general result given) and Q14's cross-term was read as 4x1x2 (gives eigenvalues 1,1,7). In 2081 Kartik Q11 the plane line is cut off by the scan edge and was read as x-2y+2z=3.

## Next paper candidates
- `1st-semester/1st-Semester-Engineering-Physics-New-Course__1Wr5rbLk.pdf` (4 pp) and `1st-Semester-Engineering-Chemistry-New-Course__1yEQFgi0.pdf` (3 pp): next in line.
- Then new-course small files: Basic Electrical and Electronics (6 pp), Fundamental of Electrical and Electronics (4), Digital Logic, OOP, Advanced Computer Programming, Electronic Circuits, Applied Mechanics (new, 71 pp compilation), Engineering Drawing (needs figures).
- Then old-course compilations (36-60 pp each): split by sitting, one md per sitting.
- Workflow per batch: `git show HEAD:<path> > src/x.pdf`, `pdftoppm -r 100 -png`, read pages, verify answers with sympy, write md (questions + `<!-- SOLUTIONS -->` + `@s N`), `/tmp/b.sh <id>` build, push, then `python3 bundle_engineering.py`.

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
- The repo is cloned straight into the workspace (`/app` here). Private repo: every git network call needs `GIT_ASKPASS` (the env does not persist between bash calls; `source` a small script each time).
- Sparse checkout must include `/notes/papers/*.py`, `/notes/papers/*.css`, `/notes/papers/engineering/content/**`, `/notes/papers/engineering/pdf/**`, `/notes/papers/tools/**` or the build scripts are missing.
- Conic/lines in scans: crop at 200-300 dpi (`pdftoppm -x -y -W -H`) before guessing a digit.

## Honest scope note
The repo holds 4,086 papers but only SIX (IOE Maths I and II) have been re-typeset with worked solutions so far. The rest are the original scans/DOCs, catalogued and ready. Pokhara DOC/DOCX (2,559 files) need LibreOffice conversion first (not installed; try `micromamba install libreoffice` into /tmp/menv).
