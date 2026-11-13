# Mathematics I: BCA 104 (Semester I, 3 credits)

**Rebuilt in session 21 to the TU syllabus.** Earlier sessions had written single-variable calculus here and linear algebra in BCA 154, but the TU
syllabus (hamronotes.com chapter list for "Mathematics - 1", cross-checked against the note-bahadur list) puts logic, sequences, matrices, conics and
vectors in BCA 104, and calculus in BCA 154. The calculus units moved to `semester-2/mathematics-2`; the linear-algebra units moved here.

| Syllabus unit | Where it is covered in this book |
|---|---|
| 1 Logic, relations, functions and graphs | Unit 1 (logic, real and complex numbers, relations, functions, composition, inverse, graph transformations) |
| 2 Sequence and series | Unit 2 (AP, GP, HP, means, special sums, arithmetico-geometric series) |
| 3 Matrices and determinants (incl. rank, transformations, characteristic equation, eigenvalues) | Unit 3 Matrices and Determinants, Unit 4 Systems of Linear Equations (rank, Cramer), Unit 5 Eigenvalues, Eigenvectors and Diagonalisation |
| 4 Analytical geometry (conics, polar equations) | Unit 6 Conic sections |
| 5 Vector and vector space | Unit 7 Vector Spaces and Linear Transformations, Unit 8 Vectors in Space, Lines and Planes |

## Session 45 additions
Unit 2 gained 2.6 recurrences (Hanoi, Fibonacci/Binet), 2.7 limits and convergence tests, 2.8 telescoping and the method of differences, 2.9 series in computing and finance (loop counts, amortised doubling, annuity, EMI), Figure 2.1 and practice 9 to 20. Unit 6 gained 6.7 tangents and normals, 6.8 parametric forms and focal distances, 6.9 translation of axes, 6.10 the general second-degree equation and rotation, 6.11 applications, Figures 6.2 to 6.4 and practice 9 to 24. Every number is recomputed in `bca/tools/check_math1_u2u6.py` (ALL OK). Sections 2.6 to 2.9 and 6.7 to 6.11 go beyond the printed topic list as reinforcement.

## Verification
Worked numbers in units 3, 4, 5, 7 and 8 were checked with SymPy in earlier sessions (`bca/tools/check_math2.py`, written for the old BCA 154 file names).
Numbers in the new Unit 2, Unit 6 and Unit 1 sections 1.6 to 1.9 were checked by hand (identities and arithmetic re-derived).

## Source and honesty
Unit division follows the syllabus topic list; hours per unit are not stated. `check_math2.py --verify` still points at the old unit numbering and should be
re-targeted if the units are edited. Units 3 to 8 were renumbered mechanically (headings, figure labels, cross-references).
