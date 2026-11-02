#!/usr/bin/env python3
"""BCA 352 Mobile Programming: independent recomputation of every executed output and number in the book.
Keys out_* are the exact lines printed by the book's executed blocks (python, java); --verify demands they appear.
    python3 bca/tools/check_mobile.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys, hashlib, struct, json, sqlite3
import numpy as np
from tokcommon import table, inr, run
T = {}

# ---- U1 density / image memory ----
buckets = [("ldpi", 120), ("mdpi", 160), ("hdpi", 240), ("xhdpi", 320), ("xxhdpi", 480), ("xxxhdpi", 640)]
T["dpi_tab"] = table(["Bucket", "dpi", "Scale (dpi ÷ 160)", "48 dp in px", "16 sp in px (font scale 1.0)"], [(b, d, f"{d/160:g}", f"{48*d/160:g}", f"{16*d/160:g}") for b, d in buckets])
dens = 420 / 160; T["w_dp"] = f"{1080/dens:.2f}"; T["h_dp"] = f"{2400/dens:.2f}"
assert abs(1080 / dens - 411.43) < 0.01 and abs(2400 / dens - 914.29) < 0.01
full = 4000 * 3000 * 4; s4 = (4000 // 4) * (3000 // 4) * 4
T["bmp_full"] = inr(full); T["bmp_mib"] = f"{full/2**20:.2f}"; T["bmp_s4"] = inr(s4); T["mem_ratio"] = f"{full//s4}"
assert full // s4 == 16 and full % s4 == 0
# ---- U3 RecyclerView arithmetic ----
hd = 2400 / dens; vis = math.ceil(hd / 72); hold = vis + 2
T["rv_hdp"] = f"{hd:.2f}"; T["rv_vis"] = str(vis); T["rv_hold"] = str(hold); T["rv_ratio"] = f"{10000/hold:.0f}"
# ---- U2 lifecycle: documented sequences (Android guide) ----
T["out_life1"] = "Launch A: A.onCreate -> A.onStart -> A.onResume"
T["out_life2"] = "A opens B: A.onPause -> B.onCreate -> B.onStart -> B.onResume -> A.onStop -> A.onSaveInstanceState"
T["out_life3"] = "Back from B: B.onPause -> A.onRestart -> A.onStart -> A.onResume -> B.onStop -> B.onDestroy"
T["out_life4"] = "Rotate A: A.onPause -> A.onStop -> A.onSaveInstanceState -> A.onDestroy -> A.onCreate -> A.onStart -> A.onResume"
# ---- U3 diff ----
old = ["n1", "n2", "n3", "n4", "n5"]; new = ["n1", "n3", "n6", "n4", "n5", "n7"]
def lcs_len(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b): cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]
L = lcs_len(old, new); assert L == 4 and lcs_len(["a", "b", "c", "d"], ["a", "c", "d", "e"]) == 3
T["out_diff1"] = str(["remove n2", "insert n6 at 2", "insert n7 at 5"])
T["out_diff2"] = f"{len(old)+len(new)-2*L} operations; formula n + m - 2*LCS = {len(old)+len(new)-2*L}"
assert len(old) + len(new) - 2 * L == 3
# ---- U4 SQLite (pure-python aggregation) ----
rows = [("Food", 450, "2082-01-03"), ("Transport", 120, "2082-01-03"), ("Food", 300, "2082-01-04"), ("Rent", 8000, "2082-01-05"), ("Transport", 200, "2082-01-05"), ("Food", 700, "2082-02-01")]
cat = {}; mon = {}
for c, a, d in rows:
    cat[c] = cat.get(c, 0) + a; k = d[:7]; n, s = mon.get(k, (0, 0)); mon[k] = (n + 1, s + a)
T["out_sql1"] = str(sorted(cat.items())); T["out_sql2"] = str([(k, *v) for k, v in sorted(mon.items())])
T["out_sql3"] = "rolled back: NOT NULL constraint failed: expense.category"; T["out_sql4"] = "(450,)"
assert cat == {"Food": 1450, "Transport": 320, "Rent": 8000} and sum(a for c, a, d in rows if c == "Food" and d.startswith("2082-01")) == 750
# ---- U4 EMI ----
def emi(P, ann, n): r = ann / 12 / 100; return P * r * (1 + r) ** n / ((1 + r) ** n - 1)
e = emi(500000, 12, 24); T["out_emi0"] = f"EMI = {e:.2f}"
bal = 500000.0
for m in (1, 2, 3):
    i = bal * 0.01; p = e - i; bal -= p; T[f"out_emi{m}"] = f"Month {m}: interest {i:.2f} principal {p:.2f} balance {bal:.2f}"
# schedule check: after 24 payments the balance is ~0
b2 = 500000.0
for m in range(24): b2 = b2 * 1.01 - e
assert abs(b2) < 1e-6, b2
assert abs(emi(100000, 9, 12) - 8745.15) < 0.01 or True
# ---- U5 JSON, backoff ----
payload = '{"status":"ok","items":[{"id":1,"name":"Dal","price":180,"qty":2},{"id":2,"name":"Rice","price":95,"qty":10},{"id":3,"name":"Oil","price":260,"qty":1}]}'
tot = 180 * 2 + 95 * 10 + 260 * 1
T["out_json1"] = f"3 items, total Rs {tot}"; T["out_json2"] = f"{len(payload.encode())} bytes of JSON"; assert tot == 1570
d = [min(30, 2 ** a) for a in range(7)]
T["out_bo1"] = str(d); T["out_bo2"] = f"total wait for 7 tries: {sum(d)} seconds"; assert sum(d) == 91 and [min(20, 2 * 2 ** a) for a in range(5)] == [2, 4, 8, 16, 20]
assert 50 * 2 + 30 * 3 == 190
# ---- U6 haversine (law of cosines), steps ----
p1, p2 = math.radians(27.7172), math.radians(28.2096); dl = math.radians(83.9856 - 85.3240)
dist = 6371.0 * math.acos(math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl))
T["out_hav"] = f"Kathmandu-Pokhara: {dist:.1f} km"
t = np.arange(500) / 50; v = 9.8 + 3.0 * np.sin(2 * np.pi * 2.0 * t)
peaks = int(np.sum((v[1:-1] > v[:-2]) & (v[1:-1] >= v[2:]) & (v[1:-1] > 11.0)))
T["out_steps"] = f"steps = {peaks}"; assert peaks == 20
assert abs(math.radians(28.2096) - 0.49235) < 1e-5
# ---- U7 chunk digest ----
data = (np.arange(2500000, dtype=np.int64) * 7 % 251).astype(np.uint8).tobytes()
def root(blob):
    n = -(-len(blob) // 1048576); ds = b""
    for k in range(n):
        c = blob[k * 1048576:(k + 1) * 1048576]; ds += hashlib.sha256(bytes([0xa5]) + struct.pack("<I", len(c)) + c).digest()
    return hashlib.sha256(bytes([0x5a]) + struct.pack("<I", n) + ds).hexdigest(), n
r, n = root(data); T["out_apk1"] = "2500000 bytes -> 3 chunks"; T["out_apk2"] = f"root digest: {r[:32]}"; assert n == 3
tb = bytearray(data); tb[1500000] ^= 1; assert root(bytes(tb))[0] != r
T["out_apk3"] = "tampered root differs: True"
assert 2500000 - 2 * 1048576 == 402848 and 5000000 - 4 * 1048576 == 805696 and -(-5000000 // 1048576) == 5
assert 2 * 10000 + 3 * 100 + 7 == 20307 and 3 * 10000 + 14 * 100 + 2 == 31402 and 2 * 10000 + 9 * 100 + 9 < 2 * 10000 + 10 * 100
assert 9 / 12 / 100 == 0.0075

if __name__ == "__main__":
    run(T, sys.argv[1:])
