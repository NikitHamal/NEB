"""Verify every number added to BCA 104 Mathematics I units 2 and 6 (session 45).
Run: python3 bca/tools/check_math1_u2u6.py   (plain python 3 + sympy)"""
import math
from fractions import Fraction as Fr
import sympy as sp

ok = True
def chk(name, got, want, tol=1e-6):
    global ok
    good = abs(got - want) <= tol if isinstance(got, (int, float)) and isinstance(want, (int, float)) else got == want
    if not good:
        ok = False
    print(("ok   " if good else "FAIL ") + name, got, want)

# ---- Unit 2
n = sp.symbols("n", integer=True, positive=True)
# recurrence a1=3, a_{n+1}=2a_n+1  -> 2^(n+1)-1
a = [3]
for _ in range(9): a.append(2 * a[-1] + 1)
chk("rec closed form a10", a[9], 2 ** 11 - 1)
chk("hanoi 20", 2 ** 20 - 1, 1048575)
fib = [0, 1]
for _ in range(60): fib.append(fib[-1] + fib[-2])
phi = (1 + 5 ** .5) / 2
chk("binet F10", round(phi ** 10 / 5 ** .5), fib[10])
chk("F10", fib[10], 55); chk("F20", fib[20], 6765)
chk("ratio F21/F20", fib[21] / fib[20], 1.618034, 1e-5)
H = lambda k: sum(1 / i for i in range(1, k + 1))
chk("H10", H(10), 2.928968, 1e-5); chk("H100", H(100), 5.187378, 1e-5); chk("H1000", H(1000), 7.485471, 1e-5)
chk("H 2^k >= 1+k/2 k=10", H(2 ** 10) >= 1 + 10 / 2, True)
Z = lambda k: sum(1 / i ** 2 for i in range(1, k + 1))
chk("Z10", Z(10), 1.549768, 1e-5); chk("Z100", Z(100), 1.634984, 1e-5)
chk("pi^2/6", math.pi ** 2 / 6, 1.644934, 1e-5)
chk("sum n/2^n", sum(k / 2 ** k for k in range(1, 200)), 2.0, 1e-9)
chk("sum 1/n! ", sum(1 / math.factorial(k) for k in range(0, 20)), math.e, 1e-12)
chk("(1+1/n)^n n=1000", (1 + 1 / 1000) ** 1000, 2.716924, 1e-5)
chk("telescoping 1/(k(k+1)) n=99", sum(Fr(1, k * (k + 1)) for k in range(1, 100)), Fr(99, 100))
chk("1/(k(k+2)) n=10", sum(Fr(1, k * (k + 2)) for k in range(1, 11)), Fr(3, 4) - Fr(1, 2) * (Fr(1, 11) + Fr(1, 12)))
chk("sum k(k+1) n=10", sum(k * (k + 1) for k in range(1, 11)), 10 * 11 * 12 // 3)
chk("sum 1/(sqrt k+sqrt k+1) n=99", sum(1 / (k ** .5 + (k + 1) ** .5) for k in range(1, 100)), 100 ** .5 - 1, 1e-9)
chk("quad seq 2,5,10,17", [k * k + 1 for k in range(1, 5)], [2, 5, 10, 17])
chk("3,7,13,21,31", [k * k + k + 1 for k in range(1, 6)], [3, 7, 13, 21, 31])
chk("sum k^2+1 n=10", sum(k * k + 1 for k in range(1, 11)), 395)
chk("sum binom 2^8", sum(math.comb(8, k) for k in range(9)), 256)
P, r, N = 500000, 0.01, 60
emi = P * r * (1 + r) ** N / ((1 + r) ** N - 1)
chk("EMI", round(emi, 2), 11122.22, 0.011)
chk("total paid", round(emi * N, 0), 667333, 1.5)
chk("FV annuity", round(1000 * ((1.01 ** 12 - 1) / 0.01), 2), 12682.50, 0.011)
chk("depreciation 80000 *0.85^4", round(80000 * 0.85 ** 4, 2), 41760.50, 0.011)
chk("doubling copies", sum(2 ** k for k in range(10)), 1023)
chk("nested loop count n=10", sum(i for i in range(1, 11)), 55)
chk("sum i*i? 1..8 pairs", sum(1 for i in range(1, 9) for j in range(i + 1, 9)), 28)
chk("sum of 2^i i<20", sum(2 ** i for i in range(20)), 2 ** 20 - 1)
chk("S15 squares", sum(k * k for k in range(1, 16)), 1240)
chk("0.4545 = 5/11", Fr(45, 99), Fr(5, 11))
chk("log2 1e6 steps", math.ceil(math.log2(1_000_000)), 20)

# ---- Unit 6
chk("tangent parabola y2=8x at (2,4)", 4 * 4, 2 * 2 * (2 + 2))
x1, y1 = 3, Fr(12, 5)
chk("pt on ellipse", Fr(x1 ** 2, 25) + y1 ** 2 / 9, 1)
chk("ellipse tangent 9x+20y=75", (9 * x1 + 20 * y1), 75)
chk("c^2 ellipse m=1/2", 25 * Fr(1, 4) + 9, Fr(61, 4))
tt = math.pi / 3
Px, Py = 5 * math.cos(tt), 3 * math.sin(tt)
chk("PF1", math.hypot(Px + 4, Py), 7); chk("PF2", math.hypot(Px - 4, Py), 3)
chk("a+ex", 5 + 0.8 * Px, 7); chk("a-ex", 5 - 0.8 * Px, 3)
X, Y = sp.symbols("X Y")
e1 = sp.expand(9 * (X - 1) ** 2 + 4 * (Y + 2) ** 2 - 36)
chk("complete square ellipse", e1, 9 * X ** 2 + 4 * Y ** 2 - 18 * X + 16 * Y - 11)
e2 = sp.expand((Y - 2) ** 2 - 8 * (X - 2))
chk("parabola", e2, Y ** 2 - 4 * Y - 8 * X + 20)
e3 = sp.expand(16 * (X - 2) ** 2 - 9 * (Y + 1) ** 2 - 144)
chk("hyperbola", e3, 16 * X ** 2 - 9 * Y ** 2 - 64 * X - 18 * Y - 89)
chk("ellipse e", round(5 ** .5 / 3, 4), 0.7454, 1e-4)
M = sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]])
chk("x2+xy+y2 eig", sorted(M.eigenvals().keys()), [sp.Rational(1, 2), sp.Rational(3, 2)])
M2 = sp.Matrix([[3, sp.Rational(3, 2)], [sp.Rational(3, 2), 3]])
chk("3x2+3xy+3y2 eig", sorted(M2.eigenvals().keys()), [sp.Rational(3, 2), sp.Rational(9, 2)])
M3 = sp.Matrix([[5, 2], [2, 2]])
chk("5x2+4xy+2y2 eig", sorted(M3.eigenvals().keys()), [1, 6])
chk("5x2+4xy+2y2 disc", 16 - 4 * 5 * 2, -24)
chk("tan2theta 5,4,2", round(math.degrees(0.5 * math.atan2(4, 5 - 2)), 3), round(math.degrees(0.5 * math.atan(4 / 3)), 3))
M4 = sp.Matrix([[1, 2], [2, 1]])
chk("x2+4xy+y2 eig", sorted(M4.eigenvals().keys()), [-1, 3])
# dish
a_d = 0.6 ** 2 / (4 * 0.2)
chk("dish focus", a_d, 0.45)
chk("bridge a", 50 ** 2 / (4 * 20), 31.25)
chk("bridge h at 25", 25 ** 2 / (4 * 31.25), 5.0)
a_h, e_h = 17.8, 0.967
chk("halley peri", round(a_h * (1 - e_h), 3), 0.587, 1e-3)
chk("halley aph", round(a_h * (1 + e_h), 2), 35.01, 0.011)
chk("earth peri", round(1 * (1 - 0.0167), 4), 0.9833, 1e-4); chk("earth aph", round(1.0167, 4), 1.0167)
# circle tangent length from (7,1) to x2+y2-4x+2y-20? S1 = 49+1-28+2-20
chk("S1", 49 + 1 - 28 + 2 - 20, 4)
chk("tangent c^2 circle r=5 m=3/4", 25 * (1 + Fr(9, 16)), Fr(625, 16))
chk("parabola c=a/m", Fr(2) / 2, 1)
# parabola y2=8x, tangent slope 2: c=a/m=2/2=1 -> y=2x+1 ; check discriminant
xx = sp.symbols("xx")
chk("y=2x+1 tangent y2=8x", sp.discriminant(sp.expand((2 * xx + 1) ** 2 - 8 * xx), xx), 0)
chk("hyperbola x2/16-y2/9 tangent c^2 = 16m^2-9, m=1", 16 - 9, 7)
# polar families: r = l/(1+e cos t), l=3
for e in (0, .5, 1, 1.5):
    print("polar e", e, "r(0)=", 3 / (1 + e), "r(pi/2)=", 3)
chk("polar hyperbola r(pi) e=1.5", 3 / (1 - 1.5), -6)
chk("asymptote angle atan(4/3)", round(math.degrees(math.atan(4 / 3)), 2), 53.13, 0.01)
chk("rect hyperbola e", round(2 ** .5, 4), 1.4142, 1e-4)
chk("circle through (1,2),(5,6) centre", ((1 + 5) / 2, (2 + 6) / 2), (3.0, 4.0))
chk("lorentz latus ellipse", 2 * 9 / 5, 3.6)
print("ALL OK" if ok else "SOME FAILED")
