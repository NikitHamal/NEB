# Numerical Methods — BCA 253 (Semester IV, 3 credits)

Old code CACS252 (2074 curriculum, Semester IV, 3 credits; the revised list numbers it BCA 253 and swaps places with Software Engineering). 45 teaching hours.

| Unit | Title | Hours |
|---|---|---|
| 1 | Solution of Nonlinear Equations (errors, bisection, false position, Newton–Raphson, secant, fixed point, systems) | 10 |
| 2 | Interpolation and Approximation (Lagrange, divided differences, Newton forward/backward, cubic spline, least squares) | 8 |
| 3 | Numerical Differentiation and Integration (Newton's formulas, trapezoidal, Simpson 1/3 and 3/8, Romberg, double integrals) | 5 |
| 4 | Solution of Linear Algebraic Equations (Gauss, Gauss–Jordan, LU, Jacobi, Gauss–Seidel, conditioning, power method) | 10 (by subtraction, see below) |
| 5 | Solution of Ordinary Differential Equations (Taylor, Picard, Euler, Heun, Runge–Kutta, systems, shooting) | 7 |
| 6 | Solution of Partial Differential Equations (Laplace, Poisson) | 5 |

## Verification

Every iteration table and every computed number in the unit files comes from **real execution**: `bca/tools/check_numerical.py` implements each method (bisection, false position, Newton, secant, fixed point, 2-D Newton, Lagrange, divided differences, forward/backward differences, natural cubic spline, least squares, finite differences, trapezoidal / Simpson / Romberg / double integration, Gaussian elimination with partial pivoting, LU, Jacobi, Gauss–Seidel, power method, Euler, Heun, RK4, RK4 for systems, shooting, Liebmann, Poisson), writes the tables, and substitutes them into the markdown (`--fill`). `--verify` confirms that all 191 computed tables and values appear verbatim in the units. The methods are cross-checked inside the script against NumPy (`solve`, `polyfit`, `inv`, `cond`), SciPy (`CubicSpline`, `quad`, `dblquad`, `solve_ivp`) and SymPy (Picard iterates), and against exact answers (π/4, ln 2.5, (√6 ± √2)/2, 2eˣ − x − 1, 2 sinh x/sinh 1).

**What the script caught while writing:** (1) the secant method from (1, 2) has not reached 10⁻⁹ after six steps (it reaches about 10⁻⁷), so the table shows the six steps and the text says "six decimals"; (2) the draft cancellation example (√1000001 − √1000000 in seven digits) lost nothing, so it was replaced by a five-digit case that loses everything; (3) Romberg R(3, 3) is *less* accurate than R(3, 2) for this integrand, so the table was extended to R(4, 4) and the text says so; (4) a draft sentence said false position was slower than ten bisection steps — in fact its error after seven steps (1.2 × 10⁻⁴) is smaller than bisection's after ten (8.7 × 10⁻⁴), so the text now blames only the one-sided approach; (5) the quoted bisection bracket after six steps was the pre-step interval, corrected to [3.156250, 3.171875]; (6) the optimal step for numerical differentiation was misquoted as 10⁻⁵ for the forward formula (it is about 10⁻⁸; 10⁻⁵ is the central formula's); (7) the power method started from (1, 1, 1) flips sign at the third step, so the start vector was changed to (0, 1, 0), which converges monotonically.

## Source and honesty

Unit titles, topics and hours are the TU **CACS252** syllabus as reproduced on notebahadur.com (see `bca/SOURCES.md`); the revised BCA 253 PDF was not retrievable. The mirror's unit list omits the unit on *linear algebraic equations* (its course description and lab list include it, and other TU outlines place it as Unit 4); it is written here as Unit 4 and its 10 hours are 45 minus the other five units' 35, an inference. The old lab work is C or C++; this book's programs are Python for reproducibility, and every algorithm is given as steps or formulas so it can be coded in C.

## Layout notes from the PDF QA

See the build record in `bca/course/CHANGELOG_BCA_COURSE.md`.
