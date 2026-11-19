import itertools, math
import numpy as np
assert 5 + 3 - 2 == 6 and 3 + 9 * 4 == 39 and 1 / (1 - 0.5) == 2 and math.sqrt(4 * 16) == 8
assert 2 * 4 - 3 * 1 == 5 and 2 ** 3 * 4 == 32
for p, q in itertools.product([True, False], repeat=2):          # Q11
    assert ((not p) or q) == ((not p) or q) and (p <= q) == ((not p) or q)
assert 30 + 25 - (50 - 8) == 13 and 30 - 13 == 17 and 25 - 13 == 12 and 17 + 13 + 12 + 8 == 50
d = (23 - 3) / 5; assert d == 4 and [3 + d * i for i in range(6)] == [3, 7, 11, 15, 19, 23] and sum([3, 7, 11, 15, 19, 23]) == 78
A = np.array([[2, 1], [5, 3]]); Ai = np.array([[3, -1], [-5, 2]])  # Q16
assert round(np.linalg.det(A)) == 1 and (A @ Ai == np.eye(2)).all()
r = [(29 + 21) / 20, (29 - 21) / 20]                              # Q18a
assert r == [2.5, 0.4] and abs(0.4 + 1 + 2.5 - 3.9) < 1e-12 and abs(0.4 * 1 * 2.5 - 1) < 1e-12
D, Dx, Dy = -2 - 3, -13 + 3, -2 - 13                              # Q18b
assert (Dx / D, Dy / D) == (2, 3) and 2 * 2 + 3 * 3 == 13 and 2 - 3 == -1
assert all((x ** 2 - 4 * x + 3) == 0 for x in (1, 3)) and (2 ** 2 - 8 + 3) == -1
assert 10 + 6 * 4 + 2 * 8 == 50
print("11-math-mid-2083: all checks pass")
