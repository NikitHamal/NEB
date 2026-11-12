"""Numeric checks for SEE 2081 Science RE-1041 'BP'."""
G = 6.67e-11
assert abs(500 * 350 / 200 - 875) < 0.01          # 1(j)
assert abs(3e8 / 2.25e8 - 1.3333) < 0.001         # 2(i)
assert 12 * 3 + 8 == 44                           # Q16 propane
assert abs(0.7 * 4200 * 35 - 102900) < 0.01 and abs(700 * 4.2 * 35 - 102900) < 0.01   # Q14
assert abs(300 * 480 / 240 - 600) < 0.01          # Q21
F = G * 6e24 * 400 / (6.4e6) ** 2; assert abs(F - 3908) < 5, F    # Q23(i)
Rh = (G * 6e24 / 6) ** 0.5; h = Rh - 6.4e6
assert abs(Rh - 8.167e6) < 2e3 and abs(h - 1.767e6) < 3e3, (Rh, h)  # Q23(ii)
assert abs(400 * 9.8 - 3920) < 0.01
assert abs((1/16 + 6/16 + 9/16) - 1) < 1e-9       # 2(g) alt F2 1:6:9
print("sci 2081 BP checks ok")
