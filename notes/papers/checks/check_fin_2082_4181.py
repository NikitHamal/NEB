"""Numeric checks for 12-fin-2082-4181."""
assert abs(300000 / 0.40 - 750000) < 0.01          # Q10
assert abs(68900 / 130 - 530) < 0.01               # Q11
cost = 4 / 96 * 360 / (35 - 15); ear = (1 + 4 / 96) ** (360 / 20) - 1
print("Q14", cost, ear)
assert abs(cost - 0.75) < 0.0005 and abs(ear - 1.0851) < 0.001
assert 8000 * 60 == 480000 and 8000 * (60 - 40) == 160000   # Q15
icp = 340 / 8; ccc = icp + 24 - 18                  # Q17
assert abs(icp - 42.5) < 0.01 and abs(ccc - 48.5) < 0.01
# Q19 Or cross rate
print("Q19", 1.3748 / 1.8484, 1.8484 / 1.3748)
assert abs(1.3748 / 1.8484 - 0.7438) < 0.0001 and abs(1.8484 / 1.3748 - 1.3445) < 0.0001
# Q20
assets = 100000 + 200000 + 400000 + 50000
liab = 300000 + 100000 + 80000 + 120000 + 150000
assert assets == liab == 750000
ca, cl, inv = 350000, 200000, 50000
assert abs(ca / cl - 1.75) < 0.001 and abs((ca - inv) / cl - 1.5) < 0.001
assert abs(1500000 / inv - 30) < 0.01
assert abs(300000 / 450000 - 0.6667) < 0.0001
assert abs(1500000 / 750000 - 2) < 0.001
assert abs(100000 / 550000 - 0.1818) < 0.0001 and abs(100000 / 450000 - 0.2222) < 0.0001
assert abs(100000 / 1500000 - 0.0667) < 0.0001
# Q21 Or
assert abs(120 / 0.15 - 800) < 0.01
assert abs(20 * 1.08 / (0.14 - 0.08) - 360) < 0.01
# Q22
f = [0.8929, 0.7972, 0.7118, 0.6355, 0.5674]
a = [150000, 180000, 190000, 200000, 100000]
pv = [round(c * k, 2) for c, k in zip(a, f)]
af = sum(f)
print("A pv", pv, sum(pv), sum(pv) - 400000, "B", 164000 * af, 164000 * af - 400000)
print("12-fin-2082-4181: all checks pass")
