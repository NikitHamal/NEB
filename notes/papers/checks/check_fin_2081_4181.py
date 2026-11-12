"""Numeric checks for 12-fin-2081-4181. Run: python3 check_fin_2081_4181.py"""
# Q10 short term debt
assert abs(700000 * 0.70 - 490000) < 0.01
# Q11 dollars
assert abs(300000 / 135 - 2222.22) < 0.01
# Q14 3/12 net 25, 360-day year
cost = 3 / 97 * 360 / (25 - 12)
ear = (1 + 3 / 97) ** (360 / 13) - 1
print("Q14", cost, ear)
assert abs(cost - 0.8565) < 0.0005 and abs(ear - 1.3245) < 0.001
# Q15
assert 10000 * 40 == 400000 and 10000 * (40 - 25) == 150000
# Q17
icp = 350 / 10; oc = icp + 28; ccc = oc - 21
assert abs(icp - 35) < 0.01 and abs(oc - 63) < 0.01 and abs(ccc - 42) < 0.01
# Q19 Or cross rate
assert abs(1.4661 / 0.0117 - 125.308) < 0.01
# Q20 ratios
ca, cl, inv, ta = 450000, 100000, 80000, 1050000
assert abs((ca - inv) / cl - 3.7) < 0.01
assert abs(300000 / 750000 - 0.4) < 0.01 and abs(200000 / 750000 - 0.2667) < 0.001
assert abs(1800000 / 80000 - 22.5) < 0.01 and abs(1800000 * 0.6 / 80000 - 13.5) < 0.01
assert abs(1800000 / 600000 - 3) < 0.01
assert abs(120000 / ta - 0.1143) < 0.0001 and abs(120000 / 750000 - 0.16) < 0.0001
assert abs(120000 / 1800000 - 0.0667) < 0.0001 and abs(1800000 * 0.4 - 720000) < 0.01
assert 500000 + 200000 + 100000 + 250000 == 1050000 == 600000 + 450000
# Q21 Or
assert abs(1000 / 1.12 ** 10 - 321.97) < 0.01
assert abs(25 * 1.05 / (0.15 - 0.05) - 262.5) < 0.01
# Q22 NPV at 12% (4 dp table factors)
f = [0.8929, 0.7972, 0.7118, 0.6355, 0.5674]
m = [80000, 120000, 140000, 160000, 200000]
pv = [round(c * k, 2) for c, k in zip(m, f)]
print("M pv", pv, sum(pv))
npv_m = sum(pv) - 500000
af = sum(f)
npv_n = 140000 * af - 500000
print("npv_m", npv_m, "af", af, "npv_n", npv_n)
assert abs(af - 3.6048) < 0.0001
print("12-fin-2081-4181: all checks pass")
