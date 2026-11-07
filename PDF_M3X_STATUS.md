# PDF pipeline, M3 Expressive revamp: status

Read this before touching `notes/pipeline/` (`build_pdf.py`, `furniture.py`, `m3x.py`, `theme.css`, `i18n.py`).
One pipeline builds every book: Grade 8-12, CEE, IOE (slugs in `notes/curriculum`), and the BCA entrance and course books
(`bca/tools/nebpdf.py` is only an adapter). Fix the pipeline, never a single PDF.

## Branch merge
`claude/bca-entrance-complete` is merged into `main` (merge commit `b2cef8fc`; cs8 unit 20 keeps the Python rewrite).
`claude/bsc-nursing` (BSN books) is a separate branch and is not part of this task; it uses the same pipeline, so a
merge picks up the new theme, and a rebuild with this theme fixes its contents-page overlap.

## The system
- Colour: `m3x.tones(accent)` turns the book's one subject accent into role pairs (accent/on-accent, container/on-container,
  cover tones). Flat only: no gradients, no box-shadow, finite radii.
- Fonts: Poppins (every display and label string, weights 400/500/600/700), Source Serif 4 (running prose),
  JetBrains Mono (code), Noto Sans Devanagari (Nepali, via `DEVA_CSS`). Inter is no longer used in page furniture
  (figures still draw their labels in Inter). `fonts/install.sh` installs Poppins Medium as well.
- Cover: flat accent field, `m3x.cover_art` draws M3E shapes (cookie, squircle, flower) in tonal steps, four arrangements
  chosen by slug; white lockup pill, grade / level / code chips, title, edition chip. No tagline, no blurb.
- About page: tonal tiles, rounded table, exam-pattern card, caution card. Contents: `.toc{break-before:page}` (the old
  bug: both front-matter sections share the named page `frontmatter`, so the contents started under the disclaimer).
  Rows are number badge, title with hours chip, page number; no row splits across pages.
- Chapter opener: rounded container, squircle number badge, title, area / hours chips, rounded syllabus card.
- Cards (`.box`): tonal fill per kind, label pill, 5 mm radius, no side stripe. Tables: tonal rounded header.
  Chapter summary: container card. Answers: tonal strip. Marks: chip.
- No em dash and no double hyphen in any furniture string (`i18n.py`, `nebpdf.py`, theme). Authored markdown is untouched.

## How to build
```
pip install uv; uv venv --python 3.12 /tmp/v; uv pip install --python /tmp/v/bin/python weasyprint markdown matplotlib numpy pymupdf pypdf fonttools pillow sympy scipy cryptography
sudo apt-get install -y fontconfig poppler-utils libpango-1.0-0 libpangoft2-1.0-0; bash notes/pipeline/fonts/install.sh
cd notes/pipeline && /tmp/v/bin/python build_pdf.py sci8          # one book -> notes/pdf/
/tmp/v/bin/python bca/tools/nebpdf.py entrance                    # BCA entrance; `course` for course books
```
Python 3.12 is required (3.11 fails on nested f-strings). 4 cores / 3 GB: run at most 3 builds in parallel.

## Rebuild progress
See the table at the bottom (updated as batches are pushed).

| batch | books | state |
| --- | --- | --- |
| done | all 96 books | rebuilt with the MathJax session below; run at most 2 builds in parallel (3 get OOM-killed on 4 GB) |

## Session: typeset maths, figure fonts, contents rows (read this before touching BCA maths sources)
- **Maths was plain text in four BCA course books** (Mathematics I and II, Discrete Structure, Probability and Statistics, Numerical Methods): `lim (x→a)`, `x²`, `d/dx`, `e^{2x}` and `Σ C(n, k)` printed as typed. The school, CEE and IOE books already used `$...$`.
  `bca/tools/plainmath.py` migrated the sources once (idempotent, lines holding `$` are skipped, every expression is test-parsed by mathtext and kept as text if it fails). It builds real fractions, roots, exponents, limits, sums, integrals, matrices (`[[1, 2], [3, 4]]` becomes `bmatrix`), `\bar{x}`, and puts a lone formula line in `$$...$$`. A lone variable becomes `*x*` (Source Serif italic), because a one-glyph SVG sits on the wrong baseline.
  In `:::` boxes every line is its own paragraph, so worked examples read as steps instead of one wall of text.
  For new BCA maths text write LaTeX directly. `$\frac{dy}{dx}$`, `$$...$$`. The viewer app renders the same sources with KaTeX.
- **Figures** use Poppins (`svgkit.FONT`, `figrun.FAMILY`). `Fig.math(x, y, tex, size, color)` in an `svgfig` block embeds typeset maths (see unit-03 figure 3.3). `mathsvg.render(..., color=)` takes a colour.
- **Fonts**: `fonts/install.sh` now also installs Source Serif 4 Italic (without it every `*emphasis*` printed upright).
- **Contents**: rows are `padding 3.6mm`, badge and page number are centred with `top:50%` so both sit inside the divider.
- Rebuilt with this: the five maths books above. Remaining books keep their older figures until a sweep rebuilds them; every rebuild now picks up Poppins figures automatically.
- Known leftovers: a few headings and `::: example` titles keep Unicode maths (titles cannot hold `$`); `Df(x)`-style two-letter operators stay text.
- Math images are now rendered in an exact box (`mathsvg.render` pad 1.2 px) so `md2html` and `Fig.math` can lower them by depth + pad; the old tight bbox left formulas without descenders floating above the text line.
- Rebuilt in this session: all 41 BCA course books, the 4 BCA entrance books, Python Programming (needs `pandas` in the venv). Not rebuilt: Grade 8-12, CEE and IOE books in `notes/pdf` (they pick up Poppins figures and the exact math boxes on their next rebuild; run a sweep with `build_pdf.py <slug>`).


## Session: MathJax typesetter and readable solutions (read this before touching maths in the pipeline)
Mathtext (matplotlib) is gone. `notes/pipeline/mathsvg.py` now talks to one Node process (`mathjax/mj_server.cjs`, MathJax 3 SVG,
Computer Modern outlines, no font dependency in the PDF). One-time setup: `cd notes/pipeline/mathjax && npm ci` (node_modules is ignored).
Cache key is versioned (`VERSION = "mj3"` in `mathsvg.py`); bump it when you change sizes or macros. Real TeX now works: `aligned`, `cases`,
`array`, matrices, `\text`, `\ce{}` (mhchem), `\cancel`, `\boxed`, `\begin{vmatrix}`. API unchanged: `render()` returns `(path, height_px, depth_px)`,
`render_info()` also returns the width, `width_mm()`, `derive()`, `split_sheet()`, `chain_links()` are the layout helpers.

What `md2html.py` does with maths now (every book, no source change needed):
- **Fact sheets.** Authors and the maths migration chained a whole sheet into one `$a=b ;\ c=d ;\ ...$`. A formula with 3 or more top-level `;`
  parts (or 3 `$..$` in a row) becomes `.fxs`: one tonal cell per formula on an equal 3, 2 or 1 column grid chosen from the widest cell
  (`_sheet`). The sentence mark after a sheet is swallowed. Never write a sheet as one long inline formula.
- **Derivations.** `a = b = c = d` (2 or more links, 26+ characters) and implication chains (`\Rightarrow`, `\iff`) are set as an aligned block (`.dv`)
  on their own lines; an inline formula wider than 150 mm is broken at its `=`. Display `$$..$$` chains are aligned the same way. The
  conclusion that follows (`, so x < 2.`) goes on its own line under the working (`.dvt`). A stray `.` after a block is dropped.
- **Answer keys** (`_answer_parts`): `1. (a) .. (b) .. (c) ..` becomes one line per part with the number in the margin (`.ansline.np`); an
  answer with several statements gets one line per statement (`.stp`).
- **Ragged maths paragraphs.** Any `<p>` or `<li>` holding a formula is `.hm` (left aligned, manual hyphens). Justified text stretched
  words around an unbreakable formula and cut the line.
- **Options** (`.opt`) are `inline-flex` with the badge and the formula centred on one line; column count comes from the real formula
  width (`data-w` on each image, `_mm_len`) with 4, 3, 2 or 1 columns.
- Sizes: inline 10.7 pt, display 13.6 pt, derivations 12 pt, sheet cells 11.2 pt, table cells 9.3 pt, `SCALE = 1.06` for Computer Modern beside Source Serif.
- Source fixes done: `\pi r a d` spacing, `(det | a&b ; c&d |)` in the IOE books became `vmatrix`, Mathematics I figure 4.3 labels moved off the lines.
- Scan of every `$..$` in every book (`125,801` formulas): no MathJax failures besides code snippets that merely contain `$`.

Rebuild state: Mathematics I plus every BCA, Grade 8-12, CEE and IOE book was rebuilt with this (see the pushed `pdf rebuild` commits).
Known leftovers: figure labels still use matplotlib text (a few Greek or arrow glyphs in figures warn `Font 'default' does not have a glyph`);
authored prose with `plain text` maths inside captions (`S(r) = 2 pi r^2` in photo captions) needs rewriting at the source.
