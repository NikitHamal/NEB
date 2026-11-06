#!/usr/bin/env python3
"""Psychiatric Nursing (BSN 13-14): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: foundations
_life, _cur, _teen = round(9200 * 0.10), round(9200 * 0.043), round(5888 * 0.052)
chk("nmhs", (_life, _cur, _teen, round(1000 * 0.23), round(1000 * 0.77), round(2_000_000 / 100_000 * 1.5)), (920, 396, 306, 230, 770, 30))
_exp = [100 - 7 * i for i in range(1, 6)]
_said = [93, 86, 78, 71, 64]; _p = 100; _sc = 0
for _s in _said:
    _sc += (_s == _p - 7); _p = _s
chk("s7", (_exp, _sc, 24 * 60 // 30, 24 * 60 // 15), ([93, 86, 79, 72, 65], 4, 48, 96))
chk("case1", (f"{48 / 1.68 ** 2:.1f}", f"{30 * 48:,}", 3 * 7), ("17.0", "1,440", 21))
T.update(u1_life=920, u1_cur=396, u1_teen=306, u1_treated=230, u1_untreated=770, u1_gap=77, u1_beds=30, u1_s7=4, u1_exp="93, 86, 79, 72, 65",
         u1_obs30=48, u1_obs15=96, c_bmi="17.0", c_fluid="1,440", c_meals=21)
# ---- Unit 2: schizophrenia and antipsychotics
chk("est", f"{29.16e6 / 300:,.0f}", "97,200")
_ch, _co = 10 / 2 * 100, 10 / 5 * 100
chk("cpz", (_ch, _co, _ch + _co, f"{2.5 / 5.0:.1f}", f"{37.5 / 25.0:.1f}", 3 * 28), (500.0, 200.0, 700.0, "0.5", "1.5", 84))
_g = (67 - 62) / 62 * 100
chk("met", (f"{_g:.1f}", f"{62 / 1.6 ** 2:.1f}", f"{67 / 1.6 ** 2:.1f}", 2 + 2 + 1 + 2 + 1 + 0 + 1, f"{25 / 30 * 100:.1f}"), ("8.1", "24.2", "26.2", 9, "83.3"))
chk("p2", (52 // 2, 6 / 2 * 100), (26, 300.0))
chk("case2", (2 * 2 / 2 * 100, 2 * 28, f"{25 / 25:.1f}", f"{(63 - 58) / 58 * 100:.1f}", f"{58 / 1.55 ** 2:.1f}", f"{63 / 1.55 ** 2:.1f}", 12 // 2), (200.0, 56, "1.0", "8.6", "24.1", "26.2", 6))
T.update(u2_est="97,200", u2_cpzh=500, u2_cpzo=200, u2_cpzt=700, u2_hal="0.5", u2_flu="1.5", u2_thp=84, u2_gain="8.1", u2_bmi0="24.2", u2_bmi1="26.2", u2_aims=9, u2_mpr="83.3",
         c2_cpz=200, c2_tabs=56, c2_trihex=84, c2_ml="1.0", c2_gain="8.6", c2_bmi0="24.1", c2_bmi1="26.2", c2_inj=6)
# ---- Unit 3: mood disorders and suicide
_ph = [2, 2, 3, 2, 1, 2, 2, 1, 1]
chk("phq", (sum(_ph), _ph[8], round((16 - 8) / 16 * 100), 900 // 300, 900 // 300 * 14, 3 * 3, 10 * 55, 10 * 55 // 25), (16, 1, 50, 3, 42, 9, 550, 22))
chk("sui", (f"{7221 / 29.16e6 * 100_000:.1f}", f"{round(7221 * 0.85):,}", f"{round(7221 * 0.56):,}", round(7221 / 365)), ("24.8", "6,138", "4,044", 20))
chk("p3", (2 + 2 + 3 + 2 + 1 + 2, round((16 - 7) / 16 * 100), 30 * 9), (12, 56, 270))
T.update(u3_deaths="7,221", u3_day=20, u3_phq=16, u3_i9=1, u3_fall=50, u3_litab=3, u3_lit14=42, u3_ect=9, u3_toxmg=550, u3_toxtab=22,
         u3_rate="24.8", u3_hang="6,138", u3_men="4,044", c3_phq=16, c3_caps=30, c3_270=270, c3_tox=550, c3_tabs=22, c3_resp=56)
# ---- Unit 4: anxiety, OCD, trauma, dissociative
_gad = sum([2, 2, 3, 2, 1, 1, 2]); _yb = sum([3, 2, 3, 2, 3, 3, 2, 3, 2, 3]); _pcl = sum([3] * 8 + [2] * 8 + [1] * 4)
chk("u4a", (round(9200 * 0.03), round(5888 * 0.028), _gad, 2.0 * 10, 2 * 10, _yb, 25 * 4, f"{25 * 4 * 7 / 60:.1f}", f"{25 * 4 / 960 * 100:.1f}", _pcl), (276, 165, 13, 20.0, 20, 26, 100, "11.7", "10.4", 44))
_bpm = 60 // (4 + 6)
chk("case4", (sum([3, 2, 3, 2, 1, 2, 2]), 4 + 6, _bpm, _bpm * 5, round((28 - _bpm) / 28 * 100), 7 * 1 + 21 * 2, 3 * 8, 3 * 8 // 2), (15, 10, 6, 30, 79, 49, 24, 12))
T.update(u4_adult=276, u4_teen=165, u4_gad=13, u4_dz=20, u4_tabs=20, u4_ybocs=26, u4_wash=100, u4_week="11.7", u4_share="10.4", u4_pcl=44,
         c4_gad=15, c4_cyc=10, c4_bpm=6, c4_in5=30, c4_fall=79, c4_sert=49, c4_att=24, c4_goal=12)
# ---- Unit 5: substance use, emergencies, community psychiatry
_g = 650 * 0.05 * 0.789
chk("alc", (f"{_g:.1f}", f"{_g / 10:.1f}", f"{_g * 3:.1f}", f"{_g * 3 / 10:.1f}", sum([3, 3, 2, 2, 2, 1, 2, 1, 2, 0])), ("25.6", "2.6", "76.9", "7.7", 18))
chk("ciwa", (sum([3, 4, 3, 4, 3, 2, 2, 2, 2, 2]), 4 + 3 + 2 + 1, (4 + 3 + 2 + 1) * 10, f"{200 * 3 * 3:,}"), (27, 10, 100, "1,800"))
chk("opi", (f"{0.4 / 0.4:.1f}", f"{2.0 / 0.4:.0f}", sum([2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1]), 80 // 5, f"{80 * 28:,}"), ("1.0", "5", 18, 16, "2,240"))
chk("rt", (f"{5.0 / 5.0:.1f}", f"{25.0 / 25.0:.1f}", 60 // 15), ("1.0", "1.0", 4))
_cg = 650 * 0.05 * 0.789 * 3 + 100 * 0.40 * 0.789
chk("case5", (f"{_cg:.1f}", f"{_cg / 10:.1f}", f"{30 * 62:,}", 24), ("108.5", "10.8", "1,860", 24))
chk("p5", (f"{60 * 0.40 * 0.789:.1f}",), ("18.9",))
T.update(u5_g="25.6", u5_sd="2.6", u5_day="76.9", u5_day10="7.7", u5_audit=18, u5_ciwa=27, u5_dztab=10, u5_dz=100, u5_thi="1,800",
         u5_nal="1.0", u5_nal5="5", u5_cows=18, u5_meth=16, u5_meth28="2,240", u5_rth="1.0", u5_rtp="1.0", u5_obs=4,
         c5_g="108.5", c5_sd="10.8", c5_ciwa=27, c5_dz=100, c5_thi="1,800", c5_fl="1,860", c5_obs=24)
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
