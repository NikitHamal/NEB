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

## Verification
Worked numbers in units 3, 4, 5, 7 and 8 were checked with SymPy in earlier sessions (`bca/tools/check_math2.py`, written for the old BCA 154 file names).
Numbers in the new Unit 2, Unit 6 and Unit 1 sections 1.6 to 1.9 were checked by hand (identities and arithmetic re-derived).

## Source and honesty
Unit division follows the syllabus topic list; hours per unit are not stated. `check_math2.py --verify` still points at the old unit numbering and should be
re-targeted if the units are edited. Units 3 to 8 were renumbered mechanically (headings, figure labels, cross-references).
