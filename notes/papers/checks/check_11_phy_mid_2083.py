import math
g = 10
assert 2 * math.pi / 3600 > 1.74e-3 and 2 * math.pi / 3600 < 1.75e-3          # MCQ 8
assert 20 ** 2 / (2 * g) == 20 and (100 * g * 10) / 10 == 1000 and 10 / 2 * 3 == 15  # MCQ 3, 7, 5
assert math.hypot(3, 4) == 5
fx, fy = 20 * math.cos(math.radians(60)), 20 * math.sin(math.radians(60))       # Q12
assert abs(fx - 10) < 1e-9 and abs(fy - 17.32) < 0.01 and abs(math.hypot(fx, fy) - 20) < 1e-9
imp = 0.15 * (-15 - 20)                                                         # Q14
assert abs(imp + 5.25) < 1e-9 and abs(imp / 0.02 + 262.5) < 1e-6
u, th = 20, math.radians(30)                                                    # Q17
T = 2 * u * math.sin(th) / g; H = u ** 2 * math.sin(th) ** 2 / (2 * g); R = u ** 2 * math.sin(2 * th) / g
assert abs(T - 2) < 1e-9 and abs(H - 5) < 1e-9 and abs(R - 34.64) < 0.01 and abs(u * math.cos(th) * T - R) < 1e-9
m, r, vl = 0.5, 0.8, 7                                                          # Q18
TL = m * g + m * vl ** 2 / r; vh2 = vl ** 2 - 4 * g * r; TH = m * vh2 / r - m * g
assert abs(TL - 35.625) < 1e-9 and vh2 == 17 and abs(TH - 5.625) < 1e-9 and vh2 > g * r
assert 10 + 6 * 4 + 2 * 8 == 50
print("11-phy-mid-2083: all checks pass")
