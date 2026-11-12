# Mathematics II: BCA 154 (Semester II, 3 credits)

**Rebuilt in session 21 to the TU syllabus** (hamronotes.com and tabflux.com both list the same six units for BCA 154). The calculus units previously filed
under BCA 104 now live here, and Unit 6 is new.

| Unit | Title | Syllabus topics covered |
|---|---|---|
| 1 | Limits and Continuity | epsilon-delta idea, one-sided limits, limit laws, continuity, discontinuities, IVT |
| 2 | Differentiation | first principles, rules, implicit, logarithmic, parametric, higher-order |
| 3 | Applications of Derivatives | tangent and normal, rates, extrema, optimisation, mean value theorems, L'Hopital, Taylor and Maclaurin |
| 4 | Integration | substitution, parts, partial fractions, FTC, area, volume, improper integrals |
| 5 | Differential Equations | separable, homogeneous, exact, linear, second-order, modelling |
| 6 | Computational Methods (NEW) | LPP, graphical method, simplex (up to 3 variables), duality, matrix inversion, Gauss elimination, Gauss-Seidel, bisection, Newton-Raphson |

## Known gaps against the syllabus (queue for the next session)
Partial derivatives, derivatives of inverse circular and hyperbolic functions, Cauchy and generalised mean value theorems, applications in economics,
Riemann-sum definition, surface and volume integrals, trapezoidal and Simpson's rules, reducible-to-linear equations and basic partial differential
equations are touched lightly or not at all in Units 1 to 5 and should be added as new sections.

## Verification
Units 1 to 5 were SymPy-checked in earlier sessions (`bca/tools/check_math1.py`, old file names). Unit 6 numbers were recomputed in Python this session
(simplex pivots with exact fractions, Gauss-Seidel iterations, bisection and Newton-Raphson tables, Gauss elimination).
