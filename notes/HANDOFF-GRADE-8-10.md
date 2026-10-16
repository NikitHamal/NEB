# Grade 8 and Grade 10 — session handoff

Branch: `resources/grade8-rebuild-grade10-books`, cut from
`resources/class8-rebuild-class10-complete-20261012`.

## The thing that was actually wrong

Social Studies and Health/PE/Creative Arts are **Nepali-medium** subjects. The
CDC publishes both in Nepali and both boards examine them in Nepali. Edition 1
had written `soc10` entirely in English (≈ 44,000 Latin words across 10 units)
and `health8` in English too. A Grade 10 student sitting the SEE social studies
paper cannot use an English book.

That is now fixed in the pipeline and fixed in two of the three affected books.

## Done this session

**Pipeline — Devanagari is now first-class**

| Fault | Fix |
|---|---|
| `letter-spacing` broke conjuncts — "नेबियन्स" printed "ने बि य न्स" | `DEVA_CSS` resets tracking and `text-transform` for every furniture class in a Nepali book |
| Cover and headings used Poppins' secondary Devanagari | Nepali books set `Noto Sans Devanagari` for all display type |
| Page footer brand and page number fell back to a Latin font | the `@page` margin boxes carry the Devanagari family explicitly |
| `[5]` marks chips stayed in Latin digits | `localise_marks()` runs over every chapter body |
| A Latin subject code printed on a Nepali cover | the code is dropped when it is not Devanagari |
| `i18n` treated only `nep*` as Nepali | `NEPALI_MEDIUM = ("nep", "soc", "health")` |

**Content**

- `health8` — **13/13 units written from scratch in Nepali.** The book existed
  as 2 English units. 68 pages, built.
- `soc10` — **units 1–2 rewritten in Nepali.** Spine rewritten in Nepali and
  units 6–10 given the syllabus bullets they never had.
- `soc8` — all remaining English removed: organisation names are Nepali only
  (the Latin initialisms in brackets are gone), and every demography, interest
  and trade-balance formula is restated in Nepali terms.
- `math8` — unbraced `\sqrt3` repaired; it was failing the build.
- `curriculum/soc10.md`, `curriculum/health8.md` — rewritten in Nepali.

**Books built and committed to `notes/pdf/`**

| Book | Pages |
|---|---|
| अनिवार्य नेपाली — कक्षा ८ | 130 |
| गणित — कक्षा ८ | 149 |
| विज्ञान तथा प्रविधि — कक्षा ८ | 110 |
| अनिवार्य अङ्ग्रेजी — कक्षा ८ | 145 |
| सामाजिक अध्ययन — कक्षा ८ | 69 |
| स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला — कक्षा ८ | 68 |
| अनिवार्य नेपाली — कक्षा १० | 256 |

## Next, in priority order

1. **`soc10` units 3–10 are still English.** Rewrite them in Nepali the way
   units 1–2 were done: keep the section order (it follows the CDC book), keep
   the `photo` ids (the assets are already registered under `soc10/`), redraw
   the figures with Nepali labels. Do **not** machine-translate — the register
   has to be textbook Nepali. Only build the book once all ten are converted;
   a half-English book is worse than the English one.
2. **Depth pass on Grade 8.** The chapters average 1,800–2,400 words where the
   Grade 10 books run 4,000–6,000. `soc8` carries almost no worked examples.
   The thin ones, worst first: `math8` (1,831 avg), `soc8` (2,265, 1 example
   across 9 units), `nep8` (2,202), `eng8` (2,414).
3. **Remaining Grade 10 books**: `sci10`, `qbank10` still to build.

## How to check Nepali purity

```
python3 - <<'PY'
import re, glob, collections
c = collections.Counter()
for f in glob.glob('content/soc10/*.md'):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'```.*?```', '', s, flags=re.S)      # figure/photo code
    s = re.sub(r'<[^>]+>|^---$.*?^---$', '', s, flags=re.S | re.M)
    c.update(re.findall(r'[A-Za-z][A-Za-z\'-]{2,}', s))
print(sum(c.values()), c.most_common(15))
PY
```
Box markers (`::: note`), figure code and the site URL are the only Latin that
may remain. Everything a student reads must be Devanagari.

## Build

Fonts and deps once:

```
pip install weasyprint markdown matplotlib numpy pymupdf
cd notes/pipeline/fonts && ./install.sh
```

`build_pdf.py` resolves `theme.css` beside itself now, so a scratch tree shaped
`nebians/{content,curriculum,assets,build,pdf}` works — copy `notes/pipeline/*`
into `build/`. Grade 8 books take 1–3 minutes each; `nep10` about 5.
