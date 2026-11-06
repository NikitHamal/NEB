# ---- Unit 6: stress, mental hygiene, human relations and leadership
_pr = [3, 3, 4, 1, 2, 3, 1, 2, 3, 3]
_ps = [4 - x if i in (3, 4, 6, 7) else x for i, x in enumerate(_pr)]
_band = lambda s: "low" if s <= 13 else ("moderate" if s <= 26 else "high")
chk("pss", (sum(_pr), _ps, sum(_ps), _band(sum(_ps)), _band(sum(_pr))), (25, [3, 3, 4, 3, 2, 3, 3, 2, 3, 3], 29, "high", "moderate"))
_p = 0.785; _n = 246; _se = (_p * (1 - _p) / _n) ** 0.5
chk("ci", (round(_p * _n), f"{_se * 100:.2f}", f"{(_p - 1.96 * _se) * 100:.1f}", f"{(_p + 1.96 * _se) * 100:.1f}"), (193, "2.62", "73.4", "83.6"))
chk("staff", (30 * 0.8, 24 * 3.5, 24 * 3.5 / 6, math.ceil(24 * 3.5 / 6 * 1.2), f"{24 * 3.5 / 6 * 1.2:.1f}"), (24.0, 84.0, 14.0, 17, "16.8"))
chk("c6", ((7.5 - 5.0) * 5, 5 * 12, 5 * 12 - 48, f"{5 * 12 / 48 * 100:.1f}"), (12.5, 60, 12, "125.0"))
T.update(u6_pss=29, u6_ci_low="73.4", u6_ci_high="83.6", u6_shifts=17, c6_debt="12.5", c6_ot=12)
