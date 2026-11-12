# Paper source template (reuse every session; copied from shipped papers)

## 1. Front matter (from 12-econ-2082-3041b)
```
---
file: NEBians-Past-Paper-Grade-12-Economics-2082-3041B.pdf
subject: Economics
grade: 12
year_bs: 2082
year_ad: 2025
stream: Regular + Partial (registration no. 78, 79, 80 and 81)
code: 3041 'B'
time: 3 hrs
marks: 75
students: For regular and partial students ... (new course)
category: Board Exam
---
```
Then `## Group 'A'`, `<small>Very short answer questions · [11×1=11]</small>`, `@q N` blocks with `[[marks]]` chips, `@or` between alternatives, `<!-- SOLUTIONS -->`, `### Group A`, `@s N` blocks.

## 2. MCQ block (science papers, e.g. 12-phy-2081-general)
```
@mcq 3
Stem line.
@opts first | second | third | fourth
```
Use `@opts-col` for long options. Solutions: a key table plus a 2-3 sentence reason per MCQ. Exactly 4 options.

## 3. Group B (5 marks): 150-250 words, table or `$$..$$` working, one figure when it helps.
## 4. Group C (8 marks): split to the printed marks (e.g. 4+3+1), 350-550 words for essays, answer every `@or`.

## 5. Figure block (matplotlib; INK, ACCENT, GRID are in scope; always a caption)
```
```figure caption="AR and MR curves from the table."
fig, ax = plt.subplots(figsize=(4.6,2.9))
ax.plot(x, ar, '-o', color=ACCENT, lw=1.6, ms=3.5)
ax.set_xlabel('Units', fontsize=8); ax.grid(color=GRID, lw=0.5); ax.tick_params(labelsize=7)
```
```
Keep text labels away from axis titles (S = I label overlapped the x-axis title in Econ 2082 until moved inside the axes). Inline SVG variant: flex row `display:flex; gap:10px; align-items:stretch; break-inside:avoid;` with alt text and caption.

## 6. Table block: header row, `|---|---:|` alignment row, same cell count in every row, escape literal pipes as `\|`.

## 7. Math: inline `$...$` short; display `$$...$$` one equation per block (each line of working as its own `$$`). Avoid 2+ `\frac` in one inline span.

## 8. Check script skeleton (notes/papers/checks/check_<slug>.py)
```
import math
assert 727 - 624 == 103                      # exact ints
assert abs(sd - 12.50) < 0.01                # reals
print("<id>: all checks pass")
```
One assert per number and per figure data series. Computed value wins over hand-typed.

Workflow: write source (3 heredocs) -> push -> `python3 notes/papers/tools/lint.py <md>` -> check script -> `build_paper.py <id>` -> `tools/addmanifest.py <id>` -> pdftoppm + 2x2 montage (shots named `<id>-<sha8>-...`) -> `bca/tools/qa_pdf.py` (1 expected Contents FAIL) -> tracker + push.

## 9. Marks chips: `[[..]]` accepts digits, `+` and `.` only. Write printed "3X2+2=8" as `[[6+2]]` and explain the split in the solution.
