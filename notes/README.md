# NEBians Notes — Grade 11 & 12 Science

Source for the NEBians study books: complete, chapter-by-chapter notes for the
NEB / CDC Grade 11 and 12 science stream, written against the CDC curriculum
(2076/2078 BS editions, in force for 2082 BS / 2025-26 AD).

Each subject-grade builds into a single print-ready PDF with running headers, a
linked table of contents, figures, worked examples, callout boxes and NEB-pattern
practice questions with answer keys.

## Layout

```
notes/
  curriculum/   one syllabus spine per subject-grade, transcribed from the CDC
                document — unit titles, teaching hours, area, exam pattern.
                This is the authority; chapters are written against it.
  content/      the chapters. content/<subject><grade>/unit-NN.md
  pipeline/     the build. Markdown -> HTML -> PDF (WeasyPrint), with
                matplotlib rendering both the maths and the figures.
  AUTHORING.md  the binding format + quality contract for chapter authors.
```

## Building

```
pip install weasyprint markdown matplotlib numpy pymupdf
cd notes/pipeline
python3 check.py ../content/phy11/unit-03.md      # validate one chapter
python3 build_pdf.py phy11                        # build one book -> ../out/
```

`check.py` renders every maths expression and executes every figure block in a
chapter and reports what failed. It does **not** check that the content is
correct — figures must also be rendered to PNG and looked at, and every
numerical answer independently recomputed.

## How a chapter is written

`AUTHORING.md` is the contract. In short: one numbered section per syllabus
bullet in spine order; maths in `$...$` / `$$...$$` (matplotlib mathtext, not
LaTeX — see §4 for what is and isn't supported); figures as fenced ```figure
blocks of matplotlib code that leave a `Figure` in `fig`; callout boxes as
`::: key`, `::: example`, `::: caution` and so on; then a chapter summary and
practice questions in the subject's real NEB group/marks pattern, each with a
worked solution.

## Status

Edition 1.0 drafts. Physics 11 and 12 are complete and built. The remaining
subjects are in progress. **Every book needs a subject-teacher review pass
before it is published to students** — the content is written to the syllabus
and independently checked, but it has not yet been read by a Nepali subject
teacher against the current NEB question papers.

## Built books

`pdf/` holds the built PDFs, so they can be downloaded and uploaded to the
platform without running the pipeline. They are regenerated from `content/` by
`pipeline/build_pdf.py` and should be rebuilt whenever a chapter changes.
