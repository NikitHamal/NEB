#!/usr/bin/env python3
"""Social and Behavioral Science (BSN 16): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
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
# ---- Unit 3: psychology
import math as _m
def _phi(z): return 0.5 * (1 + _m.erf(z / _m.sqrt(2)))
chk("mem", ([f"{_m.exp(-t / 2) * 100:.1f}" for t in (1, 2, 7)], f"{_m.exp(-7 / 4) * 100:.1f}", 20 // 5), (["60.7", "36.8", "3.0"], "17.4", 4))
_iq = 60 / 96 * 100
chk("iq", (f"{_iq:.1f}", f"{(_iq - 100) / 15:.1f}", f"{_phi(-2.5) * 100:.2f}", f"{_phi(-2) * 100:.2f}", f"{_phi(2) * 100:.2f}", f"{(_phi(1) - _phi(-1)) * 100:.2f}", 50 // 10, f"{10 / 12 * 100:.1f}", f"{100 + 15 * -2.5:.1f}"),
    ("62.5", "-2.5", "0.62", "2.28", "97.72", "68.27", 5, "83.3", "62.5"))
T.update(u3_r1="60.7", u3_r2="36.8", u3_r7="3.0", u3_r7s="17.4", u3_fr=4, c3_iq="62.5", c3_z="-2.5", c3_pct="0.62", u3_p70="2.28", u3_p130="97.72", u3_mid="68.27", u3_m2=5, u3_m3="83.3", u3_m4="62.5")
# ---- Unit 4: social psychology and health behaviour
_raw = [4, 5, 2, 4, 5, 1, 4, 2, 5, 4]
_sc = [6 - x if i in (2, 5, 7) else x for i, x in enumerate(_raw)]
chk("lik", (sum(_raw), _sc, sum(_sc), f"{sum(_sc) / 50 * 100:.0f}"), (36, [4, 5, 4, 4, 5, 5, 4, 4, 5, 4], 44, "88"))
chk("soc", (f"{12 * 0.37:.1f}", f"{26 / 40 * 100:.0f}", f"{(85 - 31) / 85 * 100:.1f}", f"{10 / 20 * 30:.0f}"), ("4.4", "65", "63.5", "15"))
chk("c4", (20 / 20 * 25, f"{20 * 15 * 365:,}", f"{20 * 15 * 365 * 10:,}", (6 + 2 + 2) * 7, (6 + 2 + 2)), (25, "109,500", "1,095,000", 70, 10))
T.update(u4_raw=36, u4_score=44, u4_pct=88, u4_cat="good", u4_asch="4.4", u4_mil="65", u4_m3="63.5", u4_m2="15", c4_py=25, c4_cost="109,500", c4_cost10="1,095,000", c4_patches=70, c4_weeks=10)
# ---- Unit 5: social problems, deviance and applied sociology
_z = 72908
_y = [40000, 58000, 72908, 90000, 120000, 65000, 30000, 150000, 72000, 100000]
_poor = [v for v in _y if v < _z]; _gaps = [(_z - v) / _z for v in _poor]
chk("pov", (f"{_z / 365:.1f}", _z * 5, len(_poor), f"{len(_poor) / len(_y) * 100:.0f}", f"{sum(_gaps) / len(_y) * 100:.1f}", f"{sum(_gaps) / len(_poor) * 100:.1f}", f"{sum(g * g for g in _gaps) / len(_y) * 100:.1f}"),
    ("199.7", 364540, 5, "50", "13.7", "27.3", "6.0"))
chk("unemp", (8000 + 1150, f"{1150 / 9150 * 100:.1f}", f"{22.7 - 12.6:.1f}", f"{12.6 - 11.4:.1f}"), (9150, "12.6", "10.1", "1.2"))
chk("mig", (f"{2190592 / 29164578 * 100:.1f}", f"{94455 / 839266 * 100:.1f}", 45000 * 7 // 10, 45000 * 7 // 10 * 12, 45000 * 7 // 10 * 12 - _z * 5), ("7.5", "11.3", 31500, 378000, 13460))
chk("alc", (f"{60 * 0.4 * 0.789:.1f}", f"{60 / (0.4 * 0.789):.0f}", f"{180 * 0.4 * 0.789:.1f}", f"{180 * 0.4 * 0.789 / 10:.1f}"), ("18.9", "190", "56.8", "5.7"))
chk("cl", (f"{0.153 * 7074756:,.0f}", f"{222493 / 7074756 * 100:.1f}", f"{222493 / (0.153 * 7074756) * 100:.1f}", f"{80 / 187 * 100:.1f}", f"{187 / 134:.1f}"), ("1,082,438", "3.1", "20.6", "42.8", "1.4"))
chk("rate", (f"{2500 / 1200000 * 1e5:.1f}", f"{1.96 ** 2 * 0.25 / 0.05 ** 2:.1f}", math.ceil(1.96 ** 2 * 0.25 / 0.05 ** 2), math.ceil(385 / 0.9)), ("208.3", "384.2", 385, 428))
_inc = 700 * 20; _pp = _inc * 12 / 5
chk("c5", (_inc, _inc * 12, _pp, f"{_pp / _z * 100:.1f}", _z - _pp, (_z - _pp) * 5, 300 * 30, f"{300 * 30 / _inc * 100:.1f}", 300 * 365), (14000, 168000, 33600.0, "46.1", 39308.0, 196540.0, 9000, "64.3", 109500))
T.update(u5_line=_z, u5_p0=50, u5_p1="13.7", c5_inc="14,000", c5_pct="46.1", c5_alc="64.3")
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
# ---- END OF UNITS (insert new units above this line)

def exec_blocks(files):
    """Run every ```python block that is directly followed by a ```text block; stdout must equal that block."""
    n = 0
    for f in files:
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"```python\n(.*?)```\n\n```text\n(.*?)```", t, re.S):
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh: fh.write(m.group(1))
            out = subprocess.run([sys.executable, fh.name], capture_output=True, text=True).stdout.strip()
            os.unlink(fh.name)
            if out != m.group(2).strip(): sys.exit(f"{f}: python block output mismatch\n--got--\n{out}\n--book--\n{m.group(2).strip()}")
            n += 1
    print(f"verify: {n} executed python blocks match their printed output")

if __name__ == "__main__":
    if sys.argv[1:2] == ["--verify"]:
        exec_blocks(sys.argv[2:])
    tokcommon.run(T, sys.argv[1:])
