# BSc Nursing - STATUS

Updated: end of Session 3. Branch `claude/bsc-nursing` (from `main`).

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

- **Integrated Health Sciences II (BSN 2-3), Year 1: DONE (session 3).** 5 units, 44-page PDF, `qa_pdf.py` fails=0 (warns are small SVG text in 3-up strips). U1 Nervous system and special senses | U2 Endocrine and diabetes | U3 Renal, fluids, electrolytes, acid-base | U4 Reproductive, menstrual cycle, early pregnancy | U5 Musculoskeletal and integumentary, burns.
  - 16 images (slug `nur2`: brain MRI, eye, Snellen, thyroid, pancreas, kidney, JGA figure, urine dipstick, ovary, testis, bone, knee X-ray, skin, burn; glucometer is an illustration and labelled so), 3-up and 2-up photogrids with numbered marks (y is measured from the BOTTOM), 20 SVG figures, five executed python blocks, 5-column NANDA-I plans in every unit.
  - `nursing/tools/check_ihs2.py`: 75 tokens + 5 executed python blocks + extra asserts (`--verify`). Case tokens are prefixed `c`, `c3`, `c4`, `c5` to avoid collisions.
  - Lessons: write each unit in two parts (part A to the practice section, part B appended) so no call is cut off; fix photo marks after viewing the rendered page; Nepal facts used: PEN, iodised salt 30 ppm, trachoma elimination 2018, NDHS 2022 TFR 2.1, 4 ANC visits (months 4, 6, 8, 9), 180 IFA tablets, Jadelle 5 y, copper T 10 y.

## Next (in this order)
1. **Community Health Nursing (BSN 6-7)** `course/year-1/community-health-nursing` (biostatistics tokens: incidence, prevalence, IMR, MMR, NMR, RR, OR, attributable risk, vaccine efficacy, sensitivity/specificity, sample size; NIP schedule, IMNCI, DOTS, HMIS; copy `check_ihs2.py` as `check_chn.py`, photo slug `nur3`).
2. Nutrition and Diet Therapy (BSN 8).
3. Year 2 to Year 4 books in the order of `books.json`; then the five MECEE-BL entrance books (Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20 questions).
4. Optional polish: enlarge SVG font sizes inside 3-up strips (qa warns about 5-6 pt text).

## How to continue (Session 2+)
1. `git clone --depth 5 --branch claude/bsc-nursing --single-branch https://github.com/NikitHamal/NEB.git /tmp/NEB` (PAT through an out-of-repo `GIT_ASKPASS` helper, never in the repo). Read this file and AGENTS.md section "BSc Nursing".
2. Toolchain: `sudo apt-get update; sudo apt-get install -y fontconfig poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`; `pip install --user --break-system-packages uv`; `uv venv --python 3.12 /tmp/v`; `uv pip install --python /tmp/v/bin/python weasyprint pymupdf pypdf markdown pygments pillow numpy requests matplotlib fonttools sympy scipy`; `bash notes/pipeline/fonts/install.sh`.
3. Write ONE unit per file (`nursing/course/<year>/<slug>/unit-NN.md`), tokens `{{name}}` filled by `nursing/tools/check_<slug>.py` (copy `check_fundamentals.py` as a model). Keep template copies in `/tmp/src/<slug>/` if you will re-fill.
4. Build + QA + commit + push: `bash nursing/tools/build_book.sh course/<year>/<slug> check_<slug>.py "message"` (needs `source /tmp/gitenv.sh`).
5. Photos: use `nursing/tools/ast.py` (copy to /tmp/ast.py; wrapper that sets User-Agent `NEBiansNursingBot/1.0` and calls `notes/pipeline/assets.py`): `search "query"`, `get nur<code>/<id> "File:Name.jpg"`. Pexels/Unsplash are refused by the licence gate; use Commons (PD, CC0, CC BY, CC BY-SA).
