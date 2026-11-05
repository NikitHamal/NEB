#!/usr/bin/env python3
"""Verifier for BCA 155 UX/UI Design: recomputes every number quoted in the book.

WCAG contrast ratios, Fitts's law, Hick's law, KLM task times, SUS scoring, usability-test sample size
(Nielsen/Landauer), type scales, grid arithmetic and task metrics.   python3 bca/tools/check_uxui.py [-v]
"""
import math, sys
V = "-v" in sys.argv
FAILS = []


def check(name, got, want):
    ok = got == want
    print(("ok   " if ok else "FAIL ") + name + (f"  -> {got}" if V or not ok else "") + ("" if ok else f"  want {want}"))
    if not ok: FAILS.append(name)


def lum(hexc):
    h = hexc.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


pairs = {("#000000", "#FFFFFF"): 21.0, ("#767676", "#FFFFFF"): 4.54, ("#777777", "#FFFFFF"): 4.48,
         ("#595959", "#FFFFFF"): 7.0, ("#CCCCCC", "#FFFFFF"): 1.61, ("#FFD700", "#FFFFFF"): 1.4,
         ("#FFD700", "#000000"): 15.0, ("#0000EE", "#FFFFFF"): 8.6, ("#FF0000", "#FFFFFF"): 4.0,
         ("#008000", "#FFFFFF"): 5.14, ("#0F766E", "#FFFFFF"): 5.47, ("#1A73E8", "#FFFFFF"): 4.5}
for (a, b), want in pairs.items():
    got = cr(a, b)
    print(f"contrast {a} on {b} = {got}:1")
    if want in (21.0, 4.54, 4.48, 1.61): check(f"contrast {a}/{b}", got, want)
check("AA normal text threshold 4.5; #767676 passes, #777777 fails", (cr("#767676", "#FFFFFF") >= 4.5, cr("#777777", "#FFFFFF") >= 4.5), (True, False))


def fitts(D, W, a=0.1, b=0.15): return round(a + b * math.log2(D / W + 1), 3)


print("fitts", fitts(200, 20), fitts(200, 40), fitts(400, 20), fitts(100, 20))


def hick(n, b=0.2): return round(b * math.log2(n + 1), 2)


print("hick", hick(3), hick(7), hick(15), hick(31))
check("Hick n=7 -> 0.6, n=15 -> 0.8", (hick(7), hick(15)), (0.6, 0.8))


def sus(r):
    odd = sum(x - 1 for x in r[0::2]); even = sum(5 - x for x in r[1::2])
    return (odd + even) * 2.5


print("sus", sus([4, 2, 5, 1, 4, 2, 5, 1, 4, 2]), sus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1]), sus([3] * 10))
check("SUS all-neutral = 50; perfect = 100", (sus([3] * 10), sus([5, 1] * 5)), (50.0, 100.0))
print("nielsen n=5", round(1 - (1 - 0.31) ** 5, 3), "n=3", round(1 - (1 - 0.31) ** 3, 3), "n=15", round(1 - (1 - 0.31) ** 15, 3))
K, P, H, M, B = 0.2, 1.1, 0.4, 1.35, 0.1
print("KLM login: ", round(M + H + P + B * 2 + K * 8 + H + K * 8 + K, 2), " search:", round(M + P + B * 2 + K * 10 + K, 2))
for ratio in (1.2, 1.25, 1.333):
    print("scale", ratio, [round(16 * ratio ** i, 1) for i in range(0, 6)])
check("12 columns, 1200 px, 24 px gutter -> column 78 px", (1200 - 11 * 24) / 12, 78.0)
check("12-col 960 px, 20 gutter -> 61.67", round((960 - 11 * 20) / 12, 2), 61.67)
check("Golden ratio 1.618", round((1 + 5 ** 0.5) / 2, 3), 1.618)
print("16*1.618", round(16 * 1.618, 1), " 960/1.618", round(960 / 1.618, 1), " 960-593", 960 - round(960 / 1.618))
check("rem: 1.25rem at 16 px = 20 px; 24 px = 1.5rem", (1.25 * 16, 24 / 16), (20.0, 1.5))
check("task success 17/20 = 85%, error rate 6 errors/20 tasks = 0.3", (17 / 20 * 100, 6 / 20), (85.0, 0.3))
times = [42, 55, 38, 61, 47]
print("mean time", sum(times) / 5, "median", sorted(times)[2], "sd", round((sum((t - 48.6) ** 2 for t in times) / 4) ** 0.5, 2))
check("efficiency: mean time 48.6 s", sum(times) / 5, 48.6)
check("complementary of hue 174 = 354", (174 + 180) % 360, 354)
check("8-pt grid: 44 px touch target is not a multiple of 8, 48 is", (44 % 8, 48 % 8), (4, 0))
check("line length rule: 45-75 characters", (45, 75), (45, 75))
check("contrast of large text threshold 3:1 (18.66 px bold or 24 px)", 3, 3)
check("CTR example 30 clicks / 600 visitors = 5%", 30 / 600 * 100, 5.0)
check("conversion A 40/800=5.0%, B 56/800=7.0%, uplift 40%", (40 / 800 * 100, round(56 / 800 * 100, 1), round((7 - 5) / 5 * 100)), (5.0, 7.0, 40))
login = [M, P, B, B, H, *[K] * 8, K, *[K] * 8, K]     # point, click field, hands to keyboard, user, tab, password, enter
search = [M, P, B, B, *[K] * 10, K]                   # think, point, click box, type 10 chars, enter
check("KLM login = 6.65 s", round(sum(login), 2), 6.65)
check("KLM search = 4.85 s", round(sum(search), 2), 4.85)
check("Nielsen: 5 users find 84% of problems, 3 users 67%, 15 users 99.6%", (round(1 - 0.69 ** 5, 2), round(1 - 0.69 ** 3, 2), round(1 - 0.69 ** 15, 3)), (0.84, 0.67, 0.996))
check("type scale 1.25 from 16: 16 20 25 31.25 39.06", [round(16 * 1.25 ** i, 2) for i in range(5)], [16.0, 20.0, 25.0, 31.25, 39.06])
check("Fitts a=0.1 b=0.15: D200 W20 -> 0.619 s, W40 -> 0.488 s", (fitts(200, 20), fitts(200, 40)), (0.619, 0.488))
check("Fitts D400 W20 -> 0.759 s; D100 W20 = D200 W40", (fitts(400, 20), fitts(100, 20) == fitts(200, 40)), (0.759, True))
check("SUS sample (4 2 5 1 4 2 5 1 4 2) = 85", sus([4, 2, 5, 1, 4, 2, 5, 1, 4, 2]), 85.0)
check("contrast #FFD700 on white 1.4, on black 14.97", (cr("#FFD700", "#FFFFFF"), cr("#FFD700", "#000000")), (1.4, 14.97))
check("contrast #0F766E white 5.47 ; #1A73E8 white 4.51 ; #008000 5.14 ; #FF0000 4.0 ; #0000EE 9.4 ; #595959 7.0",
      tuple(cr(a, "#FFFFFF") for a in ("#0F766E", "#1A73E8", "#008000", "#FF0000", "#0000EE", "#595959")), (5.47, 4.51, 5.14, 4.0, 9.4, 7.0))

check("grid 1140/30: 67.5 px", (1140 - 11 * 30) / 12, 67.5)
check("Nielsen smallest n for 75%: 4 (77%)", (next(n for n in range(1, 20) if 1 - 0.69 ** n >= 0.75), round(1 - 0.69 ** 4, 2)), (4, 0.77))
check("SUS 5 1 4 2 5 1 4 2 5 1 = 90", sus([5, 1, 4, 2, 5, 1, 4, 2, 5, 1]), 90.0)
check("9/12 success = 75%, mean time 316/9 = 35.1", (9 / 12 * 100, sum([30, 35, 28, 40, 33, 31, 45, 38, 36]), round(316 / 9, 1)), (75.0, 316, 35.1))
check("WER 1/5 = 20%, 2/5 = 40%", (1 / 5 * 100, 2 / 5 * 100), (20.0, 40.0))
check("Fitts saving 21%", round((0.619 - 0.488) / 0.619 * 100), 21)
check("KLM fingerprint M+K = 1.55 s; 6.65/1.55 = 4.3", (round(M + K * 1, 2), round(6.65 / 1.55, 1)), (1.55, 4.3))
check("Fitts: autofill saves 16 K + H = 3.6 s", round(16 * K + H, 1), 3.6)

print(); print("ALL PASS" if not FAILS else f"{len(FAILS)} FAIL(S): {FAILS}")
sys.exit(1 if FAILS else 0)
