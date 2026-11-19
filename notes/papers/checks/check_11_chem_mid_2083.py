import math
assert 11 / 44 == 0.25 and 0.5 * 40 == 20 and 2 * 3 ** 2 == 18 and 19 - 1 == 18
m = 25 / 100                                                      # Q11
assert m == 0.25 and m * 44 == 11 and abs(m * 22.4 - 5.6) < 1e-9
c, h, o = 40 / 12, 6.67 / 1.008, 53.33 / 16                       # Q12
assert abs(c - 3.333) < 0.001 and abs(o - 3.333) < 0.001 and round(h / c) == 2 and abs(h / c - 2) < 0.02
assert 12 + 2 + 16 == 30 and 180 / 30 == 6
lam = 6.626e-34 / (9.109e-31 * 1e6)                               # Q13
assert abs(lam - 7.27e-10) < 0.01e-10
assert -13.6 / 4 == -3.4                                          # Q17
inv = 1.097e7 * (1 / 4 - 1 / 9)
assert abs(inv - 1.524e6) < 0.001e6 and abs(1 / inv - 6.56e-7) < 0.01e-7
assert 10 + 6 * 4 + 2 * 8 == 50
print("11-chem-mid-2083: all checks pass")
