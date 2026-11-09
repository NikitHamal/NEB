# Engineering papers, Phase 2 status (read this first, then PAPERS_TRACKER.md)

Branch `claude/engineering`. Phase 1 (download) is in `../PAPERS_TRACKER.md`. This file tracks the work: catalog, typesetting, what is next.

## Done so far
| What | Where | State |
|---|---|---|
| Catalog of every paper on disk (4,086 files) by university / semester / subject / year / kind | `catalog.json`, `catalog-tree.json`, `CATALOG.md` | DONE. Regenerate: `python3 tools/catalog.py && python3 tools/catalog_md.py` |
| Paper pipeline (`../build_paper.py`, `../paper.css`, `../../pipeline`) | `notes/papers/` | DONE. Takes `level:`, `cal:`; env `PAPERS_CONTENT`, `PAPERS_OUT` |
| 18 papers typeset with full worked solutions (every question and every OR) | `content/*.md` -> `pdf/NEBians-IOE-Past-Paper-*.pdf` | DONE (see table below; session 4 added 4 Physics ENSH/SH 152 papers) |
| Subject bundles + master All-in-One book | `bundle_engineering.py` -> `pdf/bundles/`, `bundles.json` | DONE for the 5 subjects that have 2+ papers (Maths I, II, III, Physics 2081-2083 with 6 papers (Part I + II merged), Chemistry), master book has 18 papers / 242 pp; re-run after each new paper |

### Papers finished
| id (content/<id>.md) | Paper | Source scan | Pages |
|---|---|---|---|
| ioe-sh101-2081-baishakh | Eng. Maths I, regular new course | `1st-semester/1st-Semester-Engineering-Mathematics-I-New-Course__1UcnNWV9.pdf` p1-2 | 12 |
| ioe-sh101-2081-kartik | Eng. Maths I, back paper | same PDF p3-4 | 14 |
| ioe-ensh101-2081-chaitra | Eng. Maths I, regular | same PDF p5-6 | 12 |
| ioe-sh151-2081-ashwin | Eng. Maths II, regular | `2nd-semester/2nd-Semester-Engineering-Mathematics-II-New-Course__.pdf` p5-6 | 11 |
| ioe-ensh151-2082-bhadra | Eng. Maths II, regular | same PDF p3-4 | 11 |
| ioe-ensh151-2083-baishakh | Eng. Maths II, back paper | same PDF p1-2 | 10 |
| ioe-sh102-2081-baishakh | Eng. Physics, regular new course (SH 102) | `1st-semester/1st-Semester-Engineering-Physics-New-Course__1Wr5rbLk.pdf` p1-2 | 16 |
| ioe-ensh102-2081-chaitra | Eng. Physics, regular (ENSH 102) | same PDF p3-4 | 15 |
| ioe-sh103-2081-baishakh | Eng. Chemistry, regular new course (SH 103) | `1st-semester/1st-Semester-Engineering-Chemistry-New-Course__1yEQFgi0.pdf` p1 | 10 |
| ioe-sh103-2081-kartik | Eng. Chemistry, back paper (SH 103) | same PDF p2 | 11 |
| ioe-ensh103-2081-chaitra | Eng. Chemistry, regular (ENSH 103) | same PDF p3 | 11 |
| ioe-ensh201-2081-chaitra | Eng. Maths III, regular (ENSH 201) | `3rd-semester/3rd-Semester-Engineering-Mathematics-III-New-Course__.pdf` p5-6 | 14 |
| ioe-ensh201-2082-kartik | Eng. Maths III, back paper | same PDF p3-4 | 14 |
| ioe-ensh201-2082-chaitra | Eng. Maths III, regular | same PDF p1-2 | 13 |
| ioe-ensh152-2083-baishakh | Eng. Physics (Part II), back paper (ENSH 152) | `2nd-semester/2nd-Semester-Engineering-Physics-New-Course__.pdf` p1-2 | 17 |
| ioe-ensh152-2082-bhadra | Eng. Physics (Part II), regular (ENSH 152) | same PDF p3-4 | 16 |
| ioe-sh152-2082-baishakh | Eng. Physics (Part II), back paper (SH 152) | same PDF p5-6 | 17 |
| ioe-sh152-2081-ashwin | Eng. Physics (Part II), regular, 2080 batch (SH 152) | same PDF p7-8 | 16 |

Reading notes (session 3): Physics 2081 Baishakh Q7(b) solved for a charged, isolated capacitor (battery-connected result also given). Chemistry 2081 Baishakh Q10 is cut off at the bottom of the scan. Chemistry 2081 Kartik Q10(b) carries no marks on the scan. Maths III 2082 Kartik Q5(b) prints sum e^{ak} for a>0 (divergent); both the divergent case and the convergent e^{-ak} are answered. Maths III 2082 Chaitra Q11 prints '2zx - px^2 - 2xy + pq' (q lost); read as 2qxy like the Kartik paper.

Reading notes (earlier): the 2083 Baishakh year is printed as such on the scan (checked at 300 dpi). In that paper Q2(a) has an illegible outer upper limit (solved as x from 1 to 2, general result given) and Q14's cross-term was read as 4x1x2 (gives eigenvalues 1,1,7). In 2081 Kartik Q11 the plane line is cut off by the scan edge and was read as x-2y+2z=3.

Reading notes (session 4, Physics 2nd sem): ENSH 152 2082 Bhadra Q5 prints 'specific heat of solid and its saturated vapor', answered for the condensed phase and saturated vapour (Clausius equation by an entropy cycle). SH 152 2082 Baishakh Q6(b): lens radius taken R = 2(mu-1)f = 100 cm. SH 152 2081 Ashwin Q2(b): both total (5/2 RT) and translational (3/2 RT) energies given. 2083 Baishakh Q2(b): Einstein temperature 100 C taken as 373 K.

## Next paper candidates
DONE in session 4: `2nd-semester/...Engineering-Physics-New-Course` (all 4 sittings). NEXT: `2nd-semester/...Engineering-Chemistry-New-Course__.pdf` (8 pp), fetch with `git checkout HEAD -- notes/papers/engineering/sources/tu-ioe/past-questions-bani/2nd-semester/<file>`; then Basic Electrical, Numerical Methods (3rd), Probability and Statistics (4th), Engineering Mechanics.
Scan page order caveat: in the IOE 'bani' compilations the continuation page of a paper can come BEFORE its first page (Maths III: p1 is the tail of p2). Read all pages before pairing.
- `1st-semester/`: Basic Electrical and Electronics (6 pp), Fundamental of Electrical and Electronics (4), Engineering Drawing (needs figures), Engineering Mechanics (9), Engineering Geology I (3).
- `2nd-semester/`: Engineering Physics new (8 pp, other sittings), Electrical Circuits and Machines (12), Electronic Device and Circuits (5), Object Oriented Programming (4), Strength of Materials (4), Survey I (8).
- `3rd-semester/`: Numerical Methods (6), Fluid Mechanics (8), Communication English (4), Microprocessors (3), Theory of Structures I (4).
- `4th-semester/`: Probability and Statistics (4), Hydraulics (5), Soil Mechanics (4), Operating System (4), Communication English (4).
- Then old-course compilations (36-60 pp each): split by sitting, one md per sitting. Pokhara DOC/DOCX need LibreOffice conversion first.
- Workflow per batch: `git show HEAD:<path> > src/x.pdf`, `pdftoppm -r 110 -png`, read pages, verify answers (sympy or by hand), write md (questions + `<!-- SOLUTIONS -->` + `@s N`), `/tmp/b.sh <id>` (wraps build_paper.py with the env below), then `python3 notes/papers/engineering/bundle_engineering.py`, then commit and push. Run `python3 fixq.py`-style fix (see Gotchas) on each md before building.

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
- Session 4 sandbox could not create `/app` (permission denied), so the repo was cloned to `/home/user/app`. The file tools only take paths relative to the sandbox root, so symlink it (`ln -s /home/user/app /home/user/sandbox/app`) and write to `app/notes/...`.
- `tools/fixq.py <md...>` rewrites every single-line `$$ a, \qquad b $$` display into a `gathered` block. Run it on each new md before building; it prevents the aligned-splitter mangling.
- `bundle_engineering.py` now groups by `BE · Year I` (not Part I/II), so Physics/Chemistry sittings from both parts share one bundle (`engineering-physics-2081-2083.pdf`).
- Sparse clone: `git checkout` without sparse rules downloads ALL blobs (~2 GB). Set `git sparse-checkout set --no-cone '/*' '!/notes/papers/engineering/sources/' ...` BEFORE the first checkout. Read single files with `git show origin/claude/engineering:<path>`.
- A math expression containing `\begin{...}` is exempt from the pipeline's auto "a = b = c" aligned splitter (wrap an inline chain in `\begin{gathered}...\end{gathered}`).
- Do not write `### Question N` headings in solutions: `@s N` already prints one.
- `git add` with one nonexistent path stages nothing at all.
- The repo is cloned straight into the workspace (`/app` here). Private repo: every git network call needs `GIT_ASKPASS` (the env does not persist between bash calls; `source` a small script each time).
- Sparse checkout must include `/notes/papers/*.py`, `/notes/papers/*.css`, `/notes/papers/engineering/content/**`, `/notes/papers/engineering/pdf/**`, `/notes/papers/tools/**` or the build scripts are missing.
- Conic/lines in scans: crop at 200-300 dpi (`pdftoppm -x -y -W -H`) before guessing a digit.

- Display equations with 2+ relation signs are auto-split into an aligned derivation. A line like `$$x = ..., \qquad y = ...$$` (two statements) gets mangled: put it in `\begin{gathered} a \\ b \end{gathered}`. Matplotlib figure text must use mathtext (`H$^+$`, `h$\nu$`), not Unicode super/subscripts or nu, or the glyph is missing.
- Git push to the private repo failed once with `remote rejected` and passed on an immediate retry.
- Bundle naming: `engineering-<subject>-<yearA>-<yearB>.pdf`, e.g. `engineering-mathematics-iii-2081-2082.pdf`.

## Honest scope note
The repo holds 4,086 papers; 14 (IOE Maths I, II, III, Physics, Chemistry; 2081-2083) have been re-typeset with worked solutions. The rest are the original scans/DOCs, catalogued and ready. Pokhara DOC/DOCX (2,559 files) need LibreOffice conversion first (not installed; try `micromamba install libreoffice` into /tmp/menv).
