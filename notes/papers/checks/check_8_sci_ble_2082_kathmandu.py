"""Re-derive every numerical and factual answer of Class 8 BLE Science and Technology 2082 (Kathmandu Metropolitan City)."""

# Marks breakdown: Section A (10x1=10), Section B (8x1=8), Section C (8x2=16), Section D (4x4=16)
sec_a = [1] * 10
sec_b = [1] * 8   # Q2..Q9
sec_c = [2] * 8   # Q10..Q17
sec_d = [4] * 4   # Q18..Q21
assert sum(sec_a) + sum(sec_b) + sum(sec_c) + sum(sec_d) == 50

# Q1(e): Relative velocity of car (60 km/h) and man (15 km/h) moving towards each other
v_car = 60
v_man = 15
v_rel = v_car + v_man
assert v_rel == 75

# Q1(i): Elements in the same period: A(Z=2), B(Z=10), C(Z=5), D(Z=11)
def period(z):
    shells = []
    rem = z
    for cap in (2, 8, 8, 18):
        if rem <= 0:
            break
        take = min(rem, cap)
        shells.append(take)
        rem -= take
    return len(shells)

assert period(2) == 1
assert period(10) == 2
assert period(5) == 2
assert period(11) == 3
assert period(10) == period(5)

# Q6: Wave frequency: 3 full cycles in 1 second
cycles = 3
time_s = 1
freq_hz = cycles / time_s
assert freq_hz == 3.0

# Q9: pH values: A = 6 (acidic), B = 8 (basic, slippery to touch)
pH_A, pH_B = 6, 8
assert pH_A < 7 and pH_B > 7

# Q20: Electrical energy and monthly bill
# 3 bulbs of 100 W for 3 h/day; 10 tube lights of 40 W for 3 h/day; 30 days; Rs. 8 per kWh
p_bulbs_kw = (3 * 100) / 1000
p_tubes_kw = (10 * 40) / 1000
assert p_bulbs_kw == 0.3
assert p_tubes_kw == 0.4
e_day_kwh = p_bulbs_kw * 3 + p_tubes_kw * 3
assert abs(e_day_kwh - 2.1) < 1e-9
e_month_kwh = e_day_kwh * 30
assert abs(e_month_kwh - 63.0) < 1e-9
cost_rs = e_month_kwh * 8
assert abs(cost_rs - 504.0) < 1e-9

# Q21: Atomic number 8 (Oxygen): K=2, L=6 -> valence electrons = 6, valency = 8 - 6 = 2
Z = 8
k_shell = 2
l_shell = Z - k_shell
valence_electrons = l_shell
valency = 8 - valence_electrons
assert valence_electrons == 6
assert valency == 2

print("All Class 8 BLE Science 2082 Kathmandu checks passed.")
