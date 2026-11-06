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
