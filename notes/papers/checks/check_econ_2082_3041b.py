"""Numeric checks for 12-econ-2082-3041b. Run: python3 check_econ_2082_3041b.py"""
import math
# Q2 MC of 8th unit
assert 727 - 624 == 103
# Q11 coefficient of range
assert abs(25 / 85 - 0.2941) < 0.001
# Q14 table
tfc = 20
tc_given = {2: 50, 4: 100}; tvc_given = {1: 20, 3: 45, 5: 145}
tvc = {0: 0, 1: 20, 2: tc_given[2] - tfc, 3: 45, 4: tc_given[4] - tfc, 5: 145}
tc = {k: tfc + v for k, v in tvc.items()}
assert [tvc[i] for i in range(6)] == [0, 20, 30, 45, 80, 145]
assert [tc[i] for i in range(6)] == [20, 40, 50, 65, 100, 165]
# Q15
Q = 120 / 24
assert Q == 5
TR = 120 * Q - 5 * Q ** 2; TC = 60 + 7 * Q ** 2
assert abs(TR - 475) < 0.01 and abs(TC - 235) < 0.01 and abs(TR - TC - 240) < 0.01
assert 14 > -10 and abs(TR / Q - 95) < 0.01
# Q19 SD
f = [8, 12, 17, 14, 9]; m = [15, 25, 35, 45, 55]; N = sum(f)
assert N == 60
dd = [(x - 35) // 10 for x in m]
sfd = sum(a * b for a, b in zip(f, dd)); sfd2 = sum(a * b * b for a, b in zip(f, dd))
assert sfd == 4 and sfd2 == 94
sd = 10 * math.sqrt(sfd2 / N - (sfd / N) ** 2)
assert abs(sd - 12.50) < 0.01
mean = sum(a * b for a, b in zip(f, m)) / N
assert abs(mean - 35.667) < 0.01 and abs(sd / mean * 100 - 35.0) < 0.1
# Q19 Or Paasche
p0 = [6, 5, 3, 8]; p1 = [10, 8, 5, 7]; q1 = [15, 10, 12, 3]
s1 = sum(a * b for a, b in zip(p1, q1)); s0 = sum(a * b for a, b in zip(p0, q1))
assert s1 == 311 and s0 == 200 and abs(s1 / s0 * 100 - 155.5) < 0.01
# Q20
price = [12, 11, 10, 9, 8, 7, 6, 5]
tr = [p * (i + 1) for i, p in enumerate(price)]
mr = [tr[0]] + [tr[i] - tr[i - 1] for i in range(1, 8)]
assert tr == [12, 22, 30, 36, 40, 42, 42, 40]
assert mr == [12, 10, 8, 6, 4, 2, 0, -2]
print("econ 2082 3041B: all checks pass")
