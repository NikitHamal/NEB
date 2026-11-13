# Mathematics II: BCA 154 (Semester II, 3 credits)

**Rebuilt in session 21 to the TU syllabus** (hamronotes.com and tabflux.com both list the same six units for BCA 154). The calculus units previously filed
under BCA 104 now live here, and Unit 6 is new.

| Unit | Title | Syllabus topics covered |
|---|---|---|
| 1 | Limits and Continuity | epsilon-delta idea, one-sided limits, limit laws, continuity, discontinuities, IVT |
| 2 | Differentiation | first principles, rules, implicit, logarithmic, parametric, higher-order, inverse trigonometric and hyperbolic derivatives, partial derivatives, gradient |
| 3 | Applications of Derivatives | tangent and normal, rates, extrema, optimisation, mean value theorems, L'Hopital, Taylor and Maclaurin |
| 4 | Integration | substitution, parts, partial fractions, FTC, area, volume, surface of revolution, improper integrals, trapezoidal and Simpson rules |
| 5 | Differential Equations | separable, homogeneous, exact, linear, Bernoulli (reducible to linear), second-order, modelling, logistic, partial differential equations (forming, direct integration, heat/wave/Laplace) |
| 6 | Computational Methods (NEW) | LPP, graphical method, simplex (up to 3 variables), duality, matrix inversion, Gauss elimination, Gauss-Seidel, bisection, Newton-Raphson |

## Known gaps against the syllabus (queue for the next session)
Partial derivatives, derivatives of inverse circular and hyperbolic functions, Cauchy and generalised mean value theorems, applications in economics,
Riemann-sum definition, surface and volume integrals, trapezoidal and Simpson's rules, reducible-to-linear equations and basic partial differential
equations are touched lightly or not at all in Units 1 to 5 and should be added as new sections.

## Verification
Units 1 to 5 were SymPy-checked in earlier sessions (`bca/tools/check_math1.py`, old file names). Unit 6 numbers were recomputed in Python this session
(simplex pivots with exact fractions, Gauss-Seidel iterations, bisection and Newton-Raphson tables, Gauss elimination).


## Session 23: syllabus gap closed

Checked against the BCA 154 outline (tabflux/hamronotes lists of the revised TU syllabus). Added: derivatives of inverse circular and hyperbolic functions and partial derivatives (2.7, 2.8); surface of revolution and numerical integration, trapezoidal and Simpson (4.8, 4.9); Bernoulli equation, logistic model and basic partial differential equations (5.8, 5.9). All numbers recomputed with sympy/scipy; every code block is executed by `fill_script_outputs.py`.


## Session 43: unit 6 (Computational Methods) deepened, 4.1k to 12.5k words, book 97 to 121 pages

New in unit 6 (all numbers recomputed in `bca/tools/check_math2_u6.py`, plus exact-fraction simplex tableaux; Python blocks are executed, outputs are real):
- 6.1 more formulations (minimum-cost diet, three-product mix, translation tips), the three special cases with Fig 6.2, why only corners matter.
- 6.2 geometric view of the simplex path (Fig 6.3), full three-variable tableaux, special cases in the tableau, a degenerate corner, sensitivity ranging, big-M note.
- 6.3 minimisation by simplex on the dual (diet), reading the primal from the dual, complementary slackness, shadow-price meaning, the four primal/dual outcomes.
- 6.4 Gauss-Jordan inverse of a 3 by 3, partial pivoting with a 3-significant-figure demonstration, ill-conditioning (kappa about 40,000), LU factorisation with a reused right-hand side, Jacobi against Gauss-Seidel with a bad ordering that diverges (Fig 6.4).
- 6.5 bracketing, regula falsi, secant, orders of convergence (Fig 6.5), Newton failures (cycle, Fig 6.6), Babylonian square root, stopping criteria, the interest rate hidden in an EMI by bisection.
- 6.6 (new) computer lab: Excel layouts (bisection, Newton, Gauss-Seidel, MINVERSE/MMULT, Solver), four executed Python programs (bisection/Newton/EMI, Gauss-Seidel, NumPy, SciPy linprog), MATLAB equivalents (not executed here; values are those of the Python runs).
- Practice 9 to 23 with worked answers; fact sheet and summary extended.
