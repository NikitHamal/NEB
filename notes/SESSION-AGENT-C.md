# Agent C — Class 10 commerce/management + Class 8 (session log)

Branch: `resources/class10-commerce-class8`, based on
`resources/class10-class8-agent-a` @ `2e1ae79025`.

Pushes go through the AgentSky GitHub connector, not `git push` (the pod has no
usable git credential: the session was created without a mounted repository, so
`AGENT_GIT_PLACEHOLDER` is unset and `git push` fails). Use
`notes/tools/push_branch.py` with `NEB_BRANCH=resources/class10-commerce-class8`:

```
export NEB_BRANCH=resources/class10-commerce-class8
python3 notes/tools/push_branch.py push "message" --all-changed
python3 notes/tools/push_branch.py push "message" path/to/new/file
```

## Brief

1. Class 10 **commerce/management stream** — full sets, interactive, real
   images, question banks. (The SEE electives a commerce/management-bound
   student takes: **Accountancy — कार्यालय सञ्चालन तथा लेखा**, and
   **Economics — अर्थशास्त्र**.)
2. Polish the class-10 books (they were behind the 11/12 series in density of
   information graphics). Already largely done on the base branch — verify.
3. Class 8 full sets from scratch.

## Official sources found (keep this list — it took a while to find)

The CDC site (`https://moecdc.gov.np/content/<id>/`) publishes the specification
grids and textbooks. Nepali PDFs are legacy **Preeti** encoded; read them with
`notes/tools/preeti2unicode.py` (per-span font detection), and the CDC's own
section headings come out as `!=!` (१.१) — the separator is `=`, not `.`.

| id | document |
|---|---|
| 274 | विशिष्टीकरण तालिका २०८०, **कार्यालय सञ्चालन र लेखा, कक्षा १०** → `/media/pdf_upload/विशिष्टीकरण तालिका २०८० (कार्यालय सञ्चालन र लेखा) कक्षा १०_ehxmps3.pdf` |
| 597 | **कार्यालय सञ्चालन तथा लेखा, कक्षा १०** textbook (2082), 318 pp |
| 585 | कार्यालय सञ्चालन तथा लेखा, कक्षा ९ textbook |
| 700 | विशिष्टीकरण तालिका र नमुना प्रश्न **अर्थशास्त्र कक्षा १०** (2083) → `GRID-ECO-10-083_potd9to.pdf` |
| 568 | **अर्थशास्त्र, कक्षा १०** textbook (2082), 217 pp |
| 452 | विशिष्टीकरण तालिका अर्थशास्त्र कक्षा ९ |
| 289 | विशिष्टीकरण तालिका (कक्षा ६–८) **स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला** |
| 290 | `Grid-Grade 6-8-Social_cij9s0m.pdf` — सामाजिक अध्ययन तथा मानव मूल्य शिक्षा, कक्षा ६–८ |
| 283 | विशिष्टीकरण तालिका २०७८ (कक्षा ८) विज्ञान तथा प्रविधि |
| 292 | विशिष्टीकरण तालिका (कक्षा ६-८) गणित — नमुना प्रश्नहरू (२०८०) |
| 659 | कक्षा १० ऐच्छिक गणित: विशिष्टीकरण तालिका, नमूना प्रश्नपत्र र उत्तरकुञ्जिका |
| 658 | कक्षा १० ऐच्छिक कम्प्युटर विज्ञान: विशिष्टीकरण तालिका, नमुना प्रश्नपत्र र उत्तरकुञ्जिका |

There is **no web-search capability granted to this agent** (no capabilities and
no gateway endpoints are granted), but the pod has general egress, so
`curl`/`urllib` reach the CDC site, Wikimedia Commons and webnotee.com fine.
The WordPress REST API (`https://webnotee.com/wp-json/wp/v2/search?search=…`)
is a working substitute for a search engine when DDG/Bing/Google rate-limit.

### SEE elective paper pattern (both subjects)

Full Marks 75, Time 3 hours. **Group A** very short answer 11 × 1 = 11 (all
compulsory), **Group B** short answer 8 × 5 = 40 (all compulsory), **Group C**
long answer 3 × 8 = 24. 22 questions in all. (The blog reproductions of these
model papers print the Group A/B marks wrongly; the CDC grid PDFs above are the
authority.)

## Status

| item | state |
|---|---|
| `notes/curriculum/acc10.md` | done — 15 units, 96 official hours, marks grid in the header |
| `notes/pipeline/spine.py` | `acc`, `eco`, `qbankacc`, `qbankeco` subjects registered |
| `notes/content/acc10/unit-01…15.md` | in progress |
| `notes/content/eco10/…` | pending |
| Accountancy question bank | pending |
| Class 10 polish | verify only (base branch already did the graphics pass) |
| Class 8 remaining (social studies, health/PE, Nepali 13–17) | pending |
