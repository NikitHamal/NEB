# ---- Unit 1: sociology, society, culture
_pop = 29164578
_rel = [23677744, 2393549, 1483066, 924204, 512313]
_oth = _pop - sum(_rel)
_sh = [v / _pop for v in _rel] + [_oth / _pop]
_top = [16.45, 11.29, 6.90, 6.20, 5.62]
_rest = 100 - sum(_top)
chk("cen", ([f"{v / _pop * 100:.2f}" for v in _rel], f"{_oth / _pop * 100:.2f}", f"{1 - sum(s * s for s in _sh):.2f}", f"{sum(_top):.2f}", f"{_rest:.2f}", f"{1 - sum((x / 100) ** 2 for x in _top + [_rest]):.2f}"),
    (["81.19", "8.21", "5.09", "3.17", "1.76"], "0.60", "0.33", "46.46", "53.54", "0.66"))
chk("c1", (f"{(3000 - 2850) / 3000 * 100:.1f}", 24 / 8, 8 * 3, f"{1 - (0.5 ** 2 + 0.5 ** 2):.2f}", f"{23677744 / 29164578 * 100:.2f}"), ("5.0", 3.0, 24, "0.50", "81.19"))
T.update(u1_simpson_rel="0.33", u1_other_pct="0.60", u1_top5="46.46", u1_rest="53.54", u1_simpson_caste="0.66", u1_m2="0.50", u1_m5="81.19", c1_loss="5.0", c1_interval=3, c1_missed=24)
