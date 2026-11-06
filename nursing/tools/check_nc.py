#!/usr/bin/env python3
"""Nursing Concepts (BSN 15): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: health, illness, stress, crisis
_ev = [65, 38, 63, 29, 16]
chk("hr", (sum(_ev), round(65 / sum(_ev) * 100)), (211, 31))
chk("hr2", (100 + 38 + 29, 100 + 38 + 29 + 20 + 16, 6 * 7, round(13 / 42 * 100)), (167, 203, 42, 31))
T.update(u1_lcu=211, c1_lcu=203, c1_days=42, c1_visits=7)
# ---- Unit 2: pain
chk("fl", (1 + 2 + 1 + 2 + 1, 18 * 15, round(18 * 15 / 120 * 5, 2), 18 * 60, 1080 // 270), (7, 270, 11.25, 1080, 4))
chk("op", (10 * 6, 60 / 6, 60 / 2, 30 / 6, 5 / 10, 60 / 2, 25 * 72, 60 // 6, 30 / 4), (60, 10.0, 30.0, 5.0, 0.5, 30.0, 1800, 10, 7.5))
chk("c2", (30 + 20, round(50 / 6, 1), 10 * 6, 60 / 6, 60 / 2, 20 * 15, 5 * 6, round(30 / 6)), (50, 8.3, 60, 10.0, 30.0, 300, 30, 5))
T.update(u2_flacc=7, u2_pcm=270, u2_ml="11.25", u2_max=1080, u2_oral=60, u2_bt=10, u2_sc=30, u2_scdose="5.0", u2_scml="0.50",
         u2_sr=30, u2_patch=1800, c2_24h=50, c2_new="8.3", c2_tab=10, c2_oral=60, c2_bt=10, c2_sr=30)
# ---- Unit 3: communication and examination
chk("vit", (f"{(148 + 2 * 92) / 3:.1f}", 148 - 92, 96 - 88, 11 * 2, f"{70 / 1.62 ** 2:.1f}", f"{98 / 100:.2f}"), ("110.7", 56, 8, 22, "26.7", "0.98"))
chk("c3", ((90 + 2 * 60) / 3, 90 - 60, 13 * 2, 112 - 96, f"{52 / 1.5 ** 2:.1f}", f"{(120 + 160) / 3:.1f}", f"{60 / 1.5 ** 2:.1f}"), (70.0, 30, 26, 16, "23.1", "93.3", "26.7"))
T.update(u3_map="110.7", u3_pp=56, u3_def=8, u3_rr=22, u3_bmi="26.7", u3_whr="0.98", c3_map=70, c3_pp=30, c3_rr=26, c3_def=16, c3_bmi="23.1")
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
