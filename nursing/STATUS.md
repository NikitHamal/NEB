# BSc Nursing - STATUS

Updated: end of Session 2. Branch `claude/bsc-nursing` (from `main`).

## Done
- Scaffold: `nursing/CURRICULUM.md`, `nursing/books.json` (registry: 18 course books + 5 entrance books), tools in `nursing/tools/`.
- **Fundamentals of Nursing (BSN 4-5), Year 1: DONE.** 5 units, 39-page PDF (`nursing/pdfs/`), `qa_pdf.py` fails=0.
  - U1 Profession, history, ethics, NNC Act 2052 | U2 Nursing process, NANDA-I, documentation, Braden/pressure injury | U3 Vital signs and assessment | U4 Infection prevention and control | U5 Medication, injections, IV therapy, dose and drip maths.
  - 14 real open-licensed photographs (Wikimedia Commons, licence-gated, credits auto-generated), 4-up / 3-up / 2-up photogrids with numbered marks and leader callouts, 12 SVG figures, 5-column NANDA-I care plans in every unit.
  - `nursing/tools/check_fundamentals.py`: 38 tokens + 2 executed python blocks + extra asserts, all pass (`--verify`).

- **Integrated Health Sciences I (BSN 1), Year 1: DONE (session 2).** 5 units, 48-page PDF, `qa_pdf.py` fails=0. U1 Cell, tissues, homeostasis, pH buffer | U2 Blood, haemostasis, immunity, transfusion | U3 Cardiovascular system and ECG | U4 Respiratory system, gas transport, ABG | U5 Digestion, metabolism, energy, ORS.
  - 17 real Commons photographs (slug `nur1`: histology, blood smears, ECG, CXR, spirometer, peak flow, stethoscope, gastric mucosa, liver, villus, dal-bhat), photogrid strips (2-up and 3-up, photo + SVG pairs), 16 SVG figures, five executed python blocks, 5-column NANDA-I plans in every unit.
  - `nursing/tools/check_ihs1.py`: 84 tokens + 5 executed python blocks + extra asserts, all pass (`--verify`).
  - Lessons: in a quoted heredoc write `\n` as a single backslash-n inside svgfig strings (a double backslash prints literally); read the rendered page before trusting photo marks; two Commons "histology" files turned out to be hand drawings, so always view a contact sheet before use.

## Next (in this order)
1. **Integrated Health Sciences II (BSN 2-3)** `course/year-1/integrated-health-sciences-2` (nervous system and special senses, endocrine, renal and fluid-electrolyte, reproductive, musculoskeletal and integumentary; copy `check_ihs1.py` as `check_ihs2.py`, photo slug `nur2`).
2. Community Health Nursing (BSN 6-7, biostatistics tokens: incidence, prevalence, IMR, MMR, RR, OR), Nutrition and Diet Therapy (BSN 8).
3. Year 2 to Year 4 books in the order of `books.json`; then the five MECEE-BL entrance books (Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20 questions).

## How to continue (Session 2+)
1. `git clone --depth 5 --branch claude/bsc-nursing --single-branch https://github.com/NikitHamal/NEB.git /tmp/NEB` (PAT through an out-of-repo `GIT_ASKPASS` helper, never in the repo). Read this file and AGENTS.md section "BSc Nursing".
2. Toolchain: `sudo apt-get update; sudo apt-get install -y fontconfig poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`; `pip install --user --break-system-packages uv`; `uv venv --python 3.12 /tmp/v`; `uv pip install --python /tmp/v/bin/python weasyprint pymupdf pypdf markdown pygments pillow numpy requests matplotlib fonttools sympy scipy`; `bash notes/pipeline/fonts/install.sh`.
3. Write ONE unit per file (`nursing/course/<year>/<slug>/unit-NN.md`), tokens `{{name}}` filled by `nursing/tools/check_<slug>.py` (copy `check_fundamentals.py` as a model). Keep template copies in `/tmp/src/<slug>/` if you will re-fill.
4. Build + QA + commit + push: `bash nursing/tools/build_book.sh course/<year>/<slug> check_<slug>.py "message"` (needs `source /tmp/gitenv.sh`).
5. Photos: use `/tmp/ast.py` (wrapper that sets User-Agent `NEBiansNursingBot/1.0` and calls `notes/pipeline/assets.py`): `search "query"`, `get nur<code>/<id> "File:Name.jpg"`. Pexels/Unsplash are refused by the licence gate; use Commons (PD, CC0, CC BY, CC BY-SA).
