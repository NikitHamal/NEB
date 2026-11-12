# Python Programming — BCA 254 (Semester IV, 3 credits)

New in the revised curriculum (2082 batch); it replaces the old CACS254 *Scripting Language* (JavaScript + PHP), whose server-side half is covered by Web Technology II (BCA 255) in this repository.

| Unit | Title | Hours (planned, 45 total) |
|---|---|---|
| 1 | Introduction to Python and Basic Elements | 6 |
| 2 | Control Flow | 5 |
| 3 | Strings and Built-in Data Structures | 7 |
| 4 | Functions, Modules and Packages | 7 |
| 5 | File Handling and Exception Handling | 6 |
| 6 | Object-Oriented Programming in Python | 7 |
| 7 | Data Analysis and Visualisation: NumPy, Pandas, Matplotlib | 7 |
| 8 | Regular Expressions, Databases and Testing | 5 |
| 9 | Putting It Together: Three Complete Programs | 4 |

## IMPORTANT: this unit list is a reconstruction

**No TU syllabus for BCA 254 was retrievable.** Only the course code, title and 3 credits were confirmed (see `bca/SOURCES.md`). The nine units and their hours (which sum to 54, scaled in the table above only as a planning guide, not a TU figure) are a reconstruction from the usual shape of a first university Python course, and from the Python outlines of other universities' BCA programmes. **Check your college's notice for the exact units before relying on this book for exam coverage.** In particular, if TU's outline includes GUI programming (Tkinter), network programming, or Django, those are *not* covered here.

## Verification

Every ` ```python ` block in the unit files was **executed** with Python 3.12 (NumPy 2.5, Pandas 3.1, Matplotlib 3.11) by `bca/tools/fill_script_outputs.py`, and the ` ```output ` block under it is the real stdout (and, for the deliberate error demonstrations marked `# raises`, the real traceback, with the temporary file name shortened to `p.py`). The tool exits non-zero if any block fails unexpectedly, and it exited 0 for the whole book. Blocks that wait for keyboard input are marked `# noexec`, and the same logic is run with a simulated `stdin` right after them. Each block is self-contained because the tool runs each in a fresh directory. Matplotlib figures are saved to files and the printed output reports their properties, since the images themselves are not reproduced.

**What running the code caught:** (1) a first draft of the loop-`else` example used an unreadable one-line conditional `print(...) if n == 91 else None`; replaced by a plain `print` after `break`; (2) the Project 2 text-analyser blocks depended on a file written by an earlier block, which breaks because every block runs in its own directory, so each block now carries its own data; (3) the unit-test example's last output line was a diff marker (`+ A`) rather than the assertion text, so the print statement was changed to select the `AssertionError` line.

## Source and honesty

All explanations and examples are original. The text follows standard Python 3 documentation and PEP 8. Python behaviours that differ between versions (the `match` statement needs 3.10+; Pandas 3.1 prints string columns as `str` rather than `object`; printed table layouts may vary) are noted where they appear.

## Layout notes from the PDF QA

See the build record in `bca/course/CHANGELOG_BCA_COURSE.md`.
