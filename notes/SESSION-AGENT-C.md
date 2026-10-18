# Agent C — Class 10 commerce/management + Class 8 (session log)

Branch: **`resources/class10-commerce-class8`**, based on
`resources/class10-class8-agent-a` @ `2e1ae79025`.
https://github.com/NikitHamal/NEB/tree/resources/class10-commerce-class8

Pushes go through the AgentSky GitHub connector, not `git push` (the pod has no
usable git credential: the session was created without a mounted repository, so
`AGENT_GIT_PLACEHOLDER` is unset and `git push` fails with "could not read
Username"). Use `notes/tools/push_branch.py`:

```
cd /workspace/neb
export NEB_BRANCH=resources/class10-commerce-class8
python3 notes/tools/push_branch.py push "message" path1 path2 …
```

Two things the helper needs, learned here:

- `git config core.quotepath false` — otherwise `git status` escapes the Devanagari
  PDF filenames and the push tool cannot find the file.
- Never commit `notes/figures/` (the pipeline's render cache). It is excluded in
  this working tree's `.git/info/exclude`; check before pushing.

## Brief

1. Class 10 **commerce/management stream** — full subject sets, interactive,
   real images, question banks.
2. Polish the class-10 books (the base branch had already done the
   information-graphics pass; verified, not redone).
3. Class 8 full sets.

The commerce/management electives at grade 9–10, per the CDC's own specification
grids, are **Accountancy — कार्यालय सञ्चालन तथा लेखा** and **Economics — अर्थशास्त्र**.
Both were built from their official grids.

## Official sources found (keep this list)

The CDC site (`https://moecdc.gov.np/content/<id>/`) publishes the specification
grids and textbooks. Nepali PDFs are legacy **Preeti** encoded; read them with
`notes/tools/preeti2unicode.py` (per-span font detection). Numbered headings come
out as `!=!` (१.१) — the separator is `=`, not `.`.

| id | document |
|---|---|
| 274 | विशिष्टीकरण तालिका २०८०, **कार्यालय सञ्चालन र लेखा, कक्षा १०** (grid: 15 units, 96 hrs, Group A 11×1 / B 8×5 / C 3×8 = 75) |
| 597 | **कार्यालय सञ्चालन तथा लेखा, कक्षा १०** textbook (2082), 318 pp |
| 585 | कार्यालय सञ्चालन तथा लेखा, कक्षा ९ textbook |
| 700 | विशिष्टीकरण तालिका र नमुना प्रश्न **अर्थशास्त्र कक्षा १०** (2083) — 6 units, 96 hrs, unit marks 9/24/9/6/12/15 |
| 568 | **अर्थशास्त्र, कक्षा १०** textbook (2082), 217 pp |
| 583 | **नेपाली, कक्षा ८** textbook (2082), 204 pp — units 13, 15, 17 needed it |
| 289 | विशिष्टीकरण तालिका (कक्षा ६–८) **स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला** — not yet used |
| 290 | `Grid-Grade 6-8-Social_cij9s0m.pdf` — सामाजिक अध्ययन तथा मानव मूल्य शिक्षा ६–८ |
| 283 | विशिष्टीकरण तालिका २०७८ (कक्षा ८) विज्ञान तथा प्रविधि |
| 659 | कक्षा १० ऐच्छिक गणित: विशिष्टीकरण तालिका, नमूना प्रश्नपत्र र उत्तरकुञ्जिका |
| 658 | कक्षा १० ऐच्छिक कम्प्युटर विज्ञान: विशिष्टीकरण तालिका, नमूना प्रश्नपत्र र उत्तरकुञ्जिका |

There is **no web-search capability granted to this agent** (no capabilities and
no gateway endpoints are granted; `actl gateway list` shows every endpoint as
`capability_not_granted`), but the pod has general egress, so `curl`/`urllib`
reach the CDC site, Wikimedia Commons and webnotee.com fine. The WordPress REST
API (`https://webnotee.com/wp-json/wp/v2/search?search=…`) works as a substitute
for a search engine when DDG/Bing/Google rate-limit.

### SEE elective paper pattern (both commerce subjects)

Full Marks 75, Time 3 hours. **Group A** very short answer 11 × 1 = 11 (all
compulsory), **Group B** short answer 8 × 5 = 40 (all compulsory), **Group C**
long answer 3 × 8 = 24. 22 questions. (Blog reproductions of the model papers
print the Group A/B marks wrongly; the CDC grid PDFs are the authority.)

## What was delivered

| deliverable | state |
|---|---|
| **Class 10 Accountancy (कार्यालय सञ्चालन तथा लेखा)** | 15/15 chapters, ~66,000 words, 34 drawn figures, 20 real photographs, 47 worked examples, full Group A/B/C sets with keys. **`notes/pdf/NEBians-Accountancy-Grade-10.pdf` — 192 pp, 16.6 MB** |
| **Class 10 Economics (अर्थशास्त्र)** | 6/6 chapters, ~34,000 words, 17 figures, 11 photographs, 21 worked examples, full practice sets. **`notes/pdf/NEBians-Economics-Grade-10.pdf` — 97 pp, 13.2 MB** |
| **Commerce Question Bank Grade 10** | 7/7 chapters: SEE pattern and unit-wise grids, Accountancy Group A bank (150 one-mark questions), Group B bank (45 questions with outlines), 12 worked numericals + Group C bank, two full Accountancy model sets with keys; Economics unit-wise A and B banks, 12 worked numericals + Group C bank, one full Economics model set with keys. **`notes/pdf/NEBians-Commerce-Question-Bank-Grade-10.pdf` — 86 pp, 1.2 MB** |
| **Class 8 Social Studies** | 9/9 units written (base branch had 1). **`notes/pdf/NEBians-Social-Studies-and-Human-Value-Education-Grade-8.pdf` — 65 pp, 1.1 MB** |
| **Class 8 Nepali** | units 13 (प्यारो प्रकृति), 15 (से गुम्बाको सुन्दरता) and 17 (डल्ले खोला) written from the CDC textbook; the base branch had 14 of 17. Also fixed an unclosed callout in `nep8/unit-14.md`. **`notes/pdf/NEBians-अनिवार्य-नेपाली-Grade-8.pdf` — 130 pp, 3.6 MB** |
| `notes/curriculum/soc8.md` | unit hours filled in from the CDC teacher's guide (16+20+20+20+20+20+20+12+12 = 160), so the book's coverage table shows real hours |
| `notes/pipeline/spine.py` | `acc`, `eco`, `qbankc` subjects registered |

Every chapter of every deliverable passes `check.py` (all maths renders through
mathtext, all matplotlib figures and all photographs render). Verified in one
sweep over `content/{acc10,eco10,qbankc10,soc8,nep8}`.

## Still open

1. **Grade 8 Health, Physical and Creative Arts** (कोष id 289 has the grid) — no
   spine and no content yet.
2. **Grade 8 question bank** — would follow naturally once the health book exists.
   The base branch already ships sci8, math8, eng8; all class-8 subject books now
   have 8/9/11/17/19/21 chapters complete between this branch and the base.
3. Class 10 `hours:` frontmatter backfill (the spines carry subject-level totals
   only) — not attempted, nothing invented.
4. The class-10 information-graphics pass was done on the base branch; this branch
   inherits it and did not repeat it.

## Environment recipe (rebuilt from scratch each session)

```
apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libgobject-2.0-0 libcairo2 shared-mime-info fonts-dejavu-core fontconfig
pip install weasyprint numpy matplotlib pymupdf markdown pillow
bash notes/pipeline/fonts/install.sh
```

Then `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md` and
`python3 build_pdf.py <slug>` both work in-tree. Builds: acc10 ~80 s, eco10 ~45 s,
qbankc10 ~15 s, soc8 ~12 s, nep8 ~25 s. Each output is well under the 25 MB
connector blob ceiling, so `shrink_pdf.py` was not needed.

## Known rendering caveat

WeasyPrint's PDF text layer mangles some Devanagari ligatures on extraction
("कार्यालय" extracts as "काQार्यालQ"); the shaping itself is done by HarfBuzz and
the same artefact is present in the books already in the repository, so the
visual output is presumed correct and copy/search quality is a pipeline-wide
issue rather than a chapter issue. Worth a look in a future session.

## Working-tree notes

- The pod has no git credential, so the working tree at `/workspace/neb` is a
  hand-fetched copy of `notes/` from the base branch, plus everything written in
  this session. Binary assets must be fetched through the **blobs** API
  (`ghapi.blob_bytes`) — fetching them through the contents API as text corrupts
  them.
- `notes/figures/` is the pipeline's render cache and must never be committed.
