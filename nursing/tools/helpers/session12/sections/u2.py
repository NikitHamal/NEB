# ---- Unit 2: family, marriage, stratification
from datetime import date, timedelta
_avg = 29164578 / 6666937
chk("hh", (f"{_avg:.2f}", f"{250 * _avg:.0f}", f"{250 * 34.9 / 100:.0f}", f"{1200 * 71 / 1000:.0f}"), ("4.37", "1094", "87", "85"))
_sh = [6, 10, 15, 22, 47]; _cum = [0]
for _s in _sh: _cum.append(_cum[-1] + _s / 100)
_au = sum(0.2 * (_cum[i] + _cum[i + 1]) / 2 for i in range(5))
chk("gini", (f"{1 - 2 * _au:.3f}", f"{47 / 6:.2f}", f"{47 / 6:.1f}", [round(c, 2) for c in _cum]), ("0.376", "7.83", "7.8", [0, 0.06, 0.16, 0.31, 0.53, 1.0]))
_lmp, _v = date(2025, 3, 10), date(2025, 9, 22)
_e280 = _lmp + timedelta(days=280); _n = _lmp + timedelta(days=7)
_m, _y = _n.month - 3, _n.year + 1
if _m <= 0: _m, _y = _m + 12, _y - 1
_nae = date(_y, _m, _n.day); _d = (_v - _lmp).days; _w, _r = divmod(_d, 7)
chk("c2", (f"{_e280:%d %b %Y}", f"{_nae:%d %b %Y}", _d, f"{_w} weeks {_r} days", f"{41 / 1.48 ** 2:.1f}", (_e280 - _v).days), ("15 Dec 2025", "17 Dec 2025", 196, "28 weeks 0 days", "18.7", 84))
T.update(u2_hh="4.37", u2_ward="1094", u2_brides="87", u2_abr="85", u2_gini="0.376", u2_q="7.83", u2_m3="7.8", u2_m4="4.37", c2_edd="15 Dec 2025", c2_naegele="17 Dec 2025", c2_days=196, c2_ga="28 weeks 0 days", c2_bmi="18.7", c2_ifa=84)
