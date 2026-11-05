# Web Technology I — BCA 203 (Semester III, 3 credits)

Revised-curriculum code BCA 203. The 2074 curriculum has this as CACS205 "Web Technology" (3 credits, 3 h theory + 3 h practical).

| Unit | Title |
|---|---|
| 1 | Internet and the World Wide Web |
| 2 | HTML and Graphics |
| 3 | Scripting Language (JavaScript) |
| 4 | CSS (Cascading Style Sheets) |
| 5 | XML |
| 6 | Introduction to jQuery |
| 7 | Website Page Layout and Design Issues |

## Verification

- Every `js` block (Units 3 and 7) was run with Node.js 22 and every `jquery` block (Unit 6) was run in jsdom with jQuery 3; the `output` blocks are the real console output (`bca/tools/fill_web_outputs.py`, `bca/tools/jq_runner.js`).
- Every complete XML document in Unit 5 was checked with `xmllint` (well-formedness; the DTD example was validated with `--valid`).
- HTML, CSS, XSLT and AJAX snippets are standard examples that were **not** rendered in a browser or sent to a server.

## Source and honesty

The seven-unit list (Internet and WWW; HTML and Graphics; Scripting Language; CSS; XML; Introduction to jQuery; Website Page Layout and Design Issues) is the TU course outline as listed on ckundan.com.np (see `bca/SOURCES.md`). **Unit hours were not found**, so none are printed. The official revised BCA 203 PDF was not retrievable. The syllabus lists "graphics" under HTML, which this book covers with image formats, image maps, SVG and canvas.

## Layout notes from the PDF QA

45 pages, 0 hard failures. Two near-empty-page warnings: p3 is the table-of-contents overflow and p34 is the last answer(s) of a chapter spilling onto a new page before the next chapter begins.
