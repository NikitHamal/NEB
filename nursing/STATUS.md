# BSc Nursing - STATUS

Updated: end of Session 1. Branch `claude/bsc-nursing` (from `main`).

## Done
- Scaffold: `nursing/CURRICULUM.md`, `nursing/books.json` (registry: 18 course books + 5 entrance books), tools in `nursing/tools/`.
- **Fundamentals of Nursing (BSN 4-5), Year 1: DONE.** 5 units, 39-page PDF (`nursing/pdfs/`), `qa_pdf.py` fails=0.
  - U1 Profession, history, ethics, NNC Act 2052 | U2 Nursing process, NANDA-I, documentation, Braden/pressure injury | U3 Vital signs and assessment | U4 Infection prevention and control | U5 Medication, injections, IV therapy, dose and drip maths.
  - 14 real open-licensed photographs (Wikimedia Commons, licence-gated, credits auto-generated), 4-up / 3-up / 2-up photogrids with numbered marks and leader callouts, 12 SVG figures, 5-column NANDA-I care plans in every unit.
  - `nursing/tools/check_fundamentals.py`: 38 tokens + 2 executed python blocks + extra asserts, all pass (`--verify`).

## Next (in this order)
1. **Integrated Health Sciences I (BSN 1)** `course/year-1/integrated-health-sciences-1` (anatomy, physiology, biochemistry, pathophysiology for the first body systems). Needs real histology photos (search Commons with `/tmp/ast.py search`).
2. Integrated Health Sciences II (BSN 2-3), Community Health Nursing (BSN 6-7, biostatistics tokens: incidence, prevalence, IMR, MMR, RR, OR), Nutrition and Diet Therapy (BSN 8).
3. Year 2 to Year 4 books in the order of `books.json`; then the five MECEE-BL entrance books (Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20 questions).

## How to continue (Session 2+)
1. `git clone --depth 5 --branch claude/bsc-nursing --single-branch https://github.com/NikitHamal/NEB.git /tmp/NEB` (PAT through an out-of-repo `GIT_ASKPASS` helper, never in the repo). Read this file and AGENTS.md section "BSc Nursing".
2. Toolchain: `sudo apt-get update; sudo apt-get install -y fontconfig poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`; `pip install --user --break-system-packages uv`; `uv venv --python 3.12 /tmp/v`; `uv pip install --python /tmp/v/bin/python weasyprint pymupdf pypdf markdown pygments pillow numpy requests matplotlib fonttools sympy scipy`; `bash notes/pipeline/fonts/install.sh`.
3. Write ONE unit per file (`nursing/course/<year>/<slug>/unit-NN.md`), tokens `{{name}}` filled by `nursing/tools/check_<slug>.py` (copy `check_fundamentals.py` as a model). Keep template copies in `/tmp/src/<slug>/` if you will re-fill.
4. Build + QA + commit + push: `bash nursing/tools/build_book.sh course/<year>/<slug> check_<slug>.py "message"` (needs `source /tmp/gitenv.sh`).
5. Photos: use `/tmp/ast.py` (wrapper that sets User-Agent `NEBiansNursingBot/1.0` and calls `notes/pipeline/assets.py`): `search "query"`, `get nur<code>/<id> "File:Name.jpg"`. Pexels/Unsplash are refused by the licence gate; use Commons (PD, CC0, CC BY, CC BY-SA).
