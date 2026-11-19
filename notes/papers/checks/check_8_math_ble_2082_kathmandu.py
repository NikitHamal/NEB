import math
from fractions import Fraction as F
# Q1 / Q2: number systems
def to_base(n, b):
    out = ""
    while n:
        out = str(n % b) + out
        n //= b
    return out
assert to_base(198, 5) == "1243" and int("1243", 5) == 198 and to_base(198, 2) == "11000110" and int("11000110", 2) == 198
# Q3
assert F(3, 5) * 400000 == 240000 and F(2, 5) * 400000 * 2 == 320000 and F(320000, 240000) == F(4, 3)
assert 400000 * 2 * 10 // 100 == 80000
# Q4
assert 432 / (18 * 12) == 2 and 9 * 2 == 18 and 18 * 6 == 108 and 432 / 18 == 24 and 24 - 12 == 12
# Q5
h = 2 * 56 / 14
assert h == 8 and (14 + 10) * h / 2 == 96 and 96 - 56 == 40 == 10 * h / 2
# Q7(b)
for a, x, y in [(2, 5, 3), (7, 1, 4), (3, 2, 9)]:
    assert F(a * x, a * x - a * y) + F(a * y, a * y - a * x) == 1
# Q8
for x in (2, 5, 7):
    assert (x + 3) * (x + 2) == x * x + 5 * x + 6
# Q9
assert abs(math.dist((-3, 2), (3, 6)) - 2 * math.sqrt(13)) < 1e-12
P = [(-3, 2), (3, 6), (5, 3)]
def sides(t): return sorted(round(math.dist(t[i], t[(i + 1) % 3]), 9) for i in range(3))
assert sides(P) == sides([(x, -y) for x, y in P]) == sides([(-x, y) for x, y in P])
# Q10: pyramid with equilateral side faces of side 5
assert abs(5 * math.sqrt(3) / 2 - 4.33) < 0.005
# Q11
assert math.hypot(8, 6) == 10
# Q12
runs = [62, 2, 62, 16, 16, 96, 1, 2]
assert sum(runs) == 257 and sum(runs) / 8 == 32.125 and 9 * 40 - sum(runs) == 103
assert 3 + 4 + 5 + 5 + 5 + 3 + 3 + 4 + 7 + 3 + 5 + 3 == 50
print("8-math-ble-2082-kathmandu: all checks pass")
