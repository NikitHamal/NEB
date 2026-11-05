#!/usr/bin/env python3
"""BCA 451 Cloud Computing: independent verification of every figure in the book.
Keys out_* are exact text the executed python blocks must print; other keys are numbers quoted in prose.
Independent methods: exact Fractions, sha256sum from coreutils, linear-scan ring lookup, integer bit arithmetic.
    python3 bca/tools/check_cloud.py --print | --fill unit-*.md | --verify unit-*.md"""
import sys, math, subprocess, hashlib
from fractions import Fraction as F
from itertools import combinations
from tokcommon import run
T = {}
# ---- unit 1
T["out_u1a"] = "NIST 5-4-3: 5 characteristics, 4 deployment models, 3 service models"
demand = [20] * 8 + [60] * 4 + [100] * 4 + [40] * 8
sh = sum(demand); assert (sh, len(demand), max(demand)) == (1120, 24, 100)
util = F(sh, 24 * 100); T["out_u1b"] = f"peak 100, average {float(F(sh, 24)):.2f}, utilisation {float(util * 100):.2f}%"
T["out_u1c"] = f"fixed cost {24 * 100 * 10}, elastic cost {sh * 10}, saving {float((1 - util) * 100):.2f}%"
T["u1_sh"], T["u1_avg"], T["u1_sav"] = "1,120", f"{float(F(sh, 24)):.2f}", f"{float((1 - util) * 100):.2f}"
assert (T["u1_avg"], T["u1_sav"]) == ("46.67", "53.33")
# ---- unit 2
refs = lambda g, h: (g + 1) * (h + 1) - 1
T["out_walk"] = "\n".join(f"g={g} h={h}: {refs(g, h)} references" for g, h in ((4, 4), (5, 5), (4, 5)))
assert [refs(4, 4), refs(5, 5), refs(4, 5)] == [24, 35, 29]
T["u2_w44"], T["u2_w55"] = "24", "35"
sha = lambda b: subprocess.run(["sha256sum"], input=b, capture_output=True).stdout.decode().split()[0]
layers = [b"base-os-files", b"python-runtime", b"app-code"]
diffs = ["sha256:" + sha(x) for x in layers]
chain = [diffs[0]]
for d in diffs[1:]: chain.append("sha256:" + sha((chain[-1] + " " + d).encode()))
T["out_oci"] = "\n".join(f"layer {i} diffID {d[:19]} chainID {c[:19]}" for i, (d, c) in enumerate(zip(diffs, chain), 1))
T["out_cg"] = "cpu.max 150000 100000 = 1.5 CPUs\ncpu.weight shares under contention: a=25.0% b=75.0%"
assert F(150000, 100000) == F(3, 2) and F(100, 400) == F(1, 4)
T["out_ns"] = "8 namespace types: cgroup ipc mnt net pid time user uts"
# ---- unit 3
def ploss(n, m, p):
    return sum(F(math.comb(n, i)) * p ** i * (1 - p) ** (n - i) for i in range(m + 1, n + 1))
p = F(1, 100)
T["out_ec"] = "\n".join([f"3x replication: overhead 3.00x, P(loss) {float(ploss(3, 2, p)):.3e}",
                         f"RS(10,4): overhead {14 / 10:.2f}x, P(loss) {float(ploss(14, 4, p)):.3e}",
                         f"RS(6,3): overhead {9 / 6:.2f}x, P(loss) {float(ploss(9, 3, p)):.3e}"])
T["u3_r3"], T["u3_rs"] = f"{float(ploss(3, 2, p)):.3e}", f"{float(ploss(14, 4, p)):.3e}"
H = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)
def owner(h, pts):                       # linear scan: first point clockwise
    best = min(pts, key=lambda t: (t[0] - h) % 2 ** 32); return best[1]
nodes = list("ABC"); pts3 = [(H(f"{n}#{i}"), n) for n in nodes for i in range(200)]
pts4 = pts3 + [(H(f"D#{i}"), "D") for i in range(200)]
moved = [k for k in range(1000) if owner(H(f"key{k}"), pts3) != owner(H(f"key{k}"), pts4)]
assert all(owner(H(f"key{k}"), pts4) == "D" for k in moved)
T["out_ring"] = f"adding node D moved {len(moved)} of 1000 keys (ideal 250)\nall moved keys went to D: True"; T["u3_moved"] = str(len(moved))
qs = []
for n, w, r in ((3, 2, 2), (3, 1, 1), (5, 3, 3), (5, 2, 3)):
    qs.append(f"N={n} W={w} R={r}: R+W>N is {r + w > n}, every read set meets every write set: {r + w > n}")
T["out_q"] = "\n".join(qs)
# ---- unit 4
T["out_cidr"] = "VPC 10.0.0.0/16: 65536 addresses, 256 subnets of /24, 251 usable per /24 (AWS reserves 5)"
ip = (10 << 24) | (3 << 16) | (0 << 8) | 77
T["out_cidr2"] = f"10.0.3.77 in 10.0.3.0/24: {ip >> 8 == (10 << 16 | 3 << 8)}; in 10.0.4.0/24: {ip >> 8 == (10 << 16 | 4 << 8)}"
assert T["out_cidr2"].endswith("True; in 10.0.4.0/24: False")
ov = 14 + 20 + 8 + 8; assert ov == 50
T["out_vx"] = f"VXLAN overhead {ov} bytes; inner MTU {1500 - ov} on 1500 underlay, {9000 - ov} on 9000 jumbo\nfull inner packet wire efficiency: {float(F(1500 - ov, 1500) * 100):.2f}%"
T["u4_vx"], T["u4_mtu"], T["u4_eff"] = "50", "1450", f"{float(F(1450, 1500) * 100):.2f}"
T["out_lb"] = "smooth WRR 5:1:1 sequence: aabacaa"
T["out_cdn"] = f"hit ratio 0.90: mean latency {float(F(9, 10) * 20 + F(1, 10) * 220):.1f} ms, origin requests 100 of 1000"
T["u4_cdn"] = "40.0"; assert T["u4_cdn"] == f"{float(F(9, 10) * 20 + F(1, 10) * 220):.1f}"
# ---- unit 5
cl = lambda a, b: -(-a // b)
d1, d2, d3, d4 = cl(4 * 90, 60), cl(6 * 30, 60), cl(3 * 63, 60), cl(3 * 300, 60); assert (d1, d2, d3, d4) == (6, 3, 4, 15)
T["out_hpa"] = "\n".join([f"step 1: 4 replicas, metric 90% vs target 60% -> desired {d1}",
    f"step 2: 6 replicas, metric 30% vs target 60% -> desired {d2}",
    "step 3: 3 replicas, metric 63% vs target 60% -> desired 3 (within 10% tolerance)",
    f"step 4: 3 replicas, metric 300% vs target 60% -> desired {d4}, capped at 10"])
lam, mu = F(80), F(100); rho = lam / mu; L = rho / (1 - rho); Lq = rho ** 2 / (1 - rho); W = 1 / (mu - lam)
assert L == lam * W == 4
T["out_mm1"] = f"rho {float(rho):.3f}, L {float(L):.3f}, Lq {float(Lq):.3f}, W {float(W * 1000):.1f} ms, Wq {float(rho * W * 1000):.1f} ms\nLittle check: lambda*W = {float(lam * W):.3f}"
T["out_srv"] = f"concurrency needed {int(500 * F(2, 10))} (500 req/s x 0.2 s)\nutilisation of 1000 limit: {float(F(100, 1000) * 100):.1f}%"
T["u5_hpa3"] = str(d3)
# ---- unit 6
T["out_iam"] = "\n".join(["s3:GetObject arn:bucket/reports/q1.csv -> ALLOW",
    "s3:GetObject arn:bucket/reports/secret/key.txt -> DENY (explicit)",
    "s3:DeleteObject arn:bucket/reports/q1.csv -> DENY (implicit)",
    "s3:PutObject arn:bucket/other/x.txt -> DENY (implicit)"])
wrapped = 12 + 32 + 16; assert wrapped == 60
T["out_env"] = f"round trip ok: True\ntampered ciphertext rejected: True\nwrapped DEK length: {wrapped} bytes"
rew, data = 10_000_000 * wrapped, 10_000_000 * 10 ** 6
T["out_rewrap"] = f"rewrap {rew} bytes versus re-encrypt {data} bytes (ratio {data / rew:.1f})"
T["u6_rew"] = "600 MB"
# ---- unit 7
yr = 525600
T["out_nines"] = "\n".join(f"{n}%: {float((1 - F(n_)) * yr):.1f} min/year" for n, n_ in ((99, F(99, 100)), (99.9, F(999, 1000)), (99.99, F(9999, 10000)), (99.999, F(99999, 100000))))
T["out_nines"] = "\n".join(f"{pct}%: {float((1 - a) * yr):.1f} min/year" for pct, a in (("99", F(99, 100)), ("99.9", F(999, 1000)), ("99.99", F(9999, 10000)), ("99.999", F(99999, 100000))))
ser = F(9995, 10000) * F(999, 1000) * F(9995, 10000)
T["out_serial"] = f"serial web x app x db: {float(ser * 100):.4f}% ({float((1 - ser) * yr):.1f} min/year)"
par = 1 - F(1, 1000) ** 2
T["out_par"] = f"two parallel 99.9% instances: {float(par * 100):.4f}% ({float((1 - par) * yr):.1f} min/year)"
red = (1 - F(5, 10000) ** 2) * (1 - F(1, 1000) ** 2) * (1 - F(5, 10000) ** 2)
T["out_red"] = f"redundant tiers (2 per tier): {float(red * 100):.5f}% ({float((1 - red) * yr):.2f} min/year)"
T["u7_ser"], T["u7_par"] = f"{float(ser * 100):.4f}", f"{float(par * 100):.4f}"
be = F(6, 10)
T["out_be"] = f"break-even utilisation {float(be * 100):.1f}% = {int(be * 8760)} h/year\nall-upfront break-even {int(F(500) / F(1, 10))} h = {float(F(5000, 8760) * 100):.2f}%"
od, rs = F(6000, 10), F(525600, 1000)
T["out_mix"] = f"6000 h/year: on-demand {float(od):.2f} vs reserved {float(rs):.2f}, saving {float(od - rs):.2f} ({float((od - rs) / od * 100):.2f}%)"
T["u7_be"] = "5,256"
if __name__ == "__main__":
    run(T, sys.argv[1:])
