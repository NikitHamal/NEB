#!/usr/bin/env python3
"""Recompute every worked table in BCA 251 Operating Systems (CPU scheduling, Banker's algorithm, deadlock detection,
disk scheduling, page replacement, memory allocation, address translation, effective access time).
Prints the tables and asserts the headline numbers quoted in the unit files.   python3 bca/tools/check_os.py"""
from collections import deque


def fmt(rows, head):
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


# ---------------- CPU scheduling ----------------
def metrics(name, procs, done, gantt):
    rows, tw, tt = [], 0, 0
    for p, (at, bt) in procs.items():
        ct = done[p]; tat = ct - at; wt = tat - bt
        rows.append((p, at, bt, ct, tat, wt)); tw += wt; tt += tat
    n = len(procs)
    print(f"\n### {name}\nGantt: {gantt}")
    fmt(rows, ["P", "AT", "BT", "CT", "TAT", "WT"])
    print(f"avg TAT = {tt/n:.2f}, avg WT = {tw/n:.2f}")
    return tw / n, tt / n


def fcfs(procs):
    t, done, g = 0, {}, []
    for p, (at, bt) in sorted(procs.items(), key=lambda x: x[1][0]):
        t = max(t, at); g.append(f"{p}[{t}-{t+bt}]"); t += bt; done[p] = t
    return done, " ".join(g)


def sjf(procs):  # non-preemptive
    t, done, g, left = 0, {}, [], dict(procs)
    while left:
        ready = {p: v for p, v in left.items() if v[0] <= t}
        if not ready: t = min(v[0] for v in left.values()); continue
        p = min(ready, key=lambda k: (ready[k][1], ready[k][0]))
        g.append(f"{p}[{t}-{t+left[p][1]}]"); t += left[p][1]; done[p] = t; del left[p]
    return done, " ".join(g)


def srtf(procs):
    t, rem, done, g, last = 0, {p: v[1] for p, v in procs.items()}, {}, [], None
    while rem:
        ready = [p for p in rem if procs[p][0] <= t]
        if not ready: t += 1; continue
        p = min(ready, key=lambda k: (rem[k], procs[k][0]))
        if last != p: g.append([p, t, t + 1]); last = p
        else: g[-1][2] = t + 1
        rem[p] -= 1; t += 1
        if rem[p] == 0: done[p] = t; del rem[p]
    return done, " ".join(f"{a}[{b}-{c}]" for a, b, c in g)


def rr(procs, q):
    t, rem, done, g = 0, {p: v[1] for p, v in procs.items()}, {}, []
    order = sorted(procs, key=lambda k: procs[k][0]); queue = deque(); arrived = set()
    def admit(upto):
        for p in order:
            if p not in arrived and procs[p][0] <= upto: arrived.add(p); queue.append(p)
    admit(0)
    while len(done) < len(procs):
        if not queue:
            t = min(procs[p][0] for p in order if p not in arrived); admit(t); continue
        p = queue.popleft(); run = min(q, rem[p]); g.append(f"{p}[{t}-{t+run}]")
        t += run; rem[p] -= run; admit(t)
        if rem[p] == 0: done[p] = t
        else: queue.append(p)
    return done, " ".join(g)


def prio_np(procs, prio):  # all arrive at 0, smaller number = higher priority
    t, done, g = 0, {}, []
    for p in sorted(procs, key=lambda k: prio[k]):
        g.append(f"{p}[{t}-{t+procs[p][1]}]"); t += procs[p][1]; done[p] = t
    return done, " ".join(g)


A = {"P1": (0, 8), "P2": (1, 4), "P3": (2, 9), "P4": (3, 5)}
res = {}
res["fcfs"] = metrics("FCFS", A, *fcfs(A))
res["sjf"] = metrics("SJF (non-preemptive)", A, *sjf(A))
res["srtf"] = metrics("SRTF", A, *srtf(A))
res["rr3"] = metrics("Round robin q=3", A, *rr(A, 3))
assert [round(x, 2) for x in res["fcfs"]] == [8.75, 15.25]
assert [round(x, 2) for x in res["sjf"]] == [7.75, 14.25]
assert [round(x, 2) for x in res["srtf"]] == [6.5, 13.0]

B = {"P1": (0, 24), "P2": (0, 3), "P3": (0, 3)}
res["rr4"] = metrics("Round robin q=4, burst 24,3,3", B, *rr(B, 4))
res["fcfsB"] = metrics("FCFS same set", B, *fcfs(B))
assert round(res["rr4"][0], 2) == 5.67 and res["fcfsB"][0] == 17.0

C = {"P1": (0, 10), "P2": (0, 1), "P3": (0, 2), "P4": (0, 1), "P5": (0, 5)}
pr = {"P1": 3, "P2": 1, "P3": 4, "P4": 5, "P5": 2}
res["prio"] = metrics("Priority (non-preemptive, lower number = higher)", C, *prio_np(C, pr))
assert round(res["prio"][0], 2) == 8.2

# HRRN
def hrrn(procs):
    t, done, g, left = 0, {}, [], dict(procs)
    while left:
        ready = {p: v for p, v in left.items() if v[0] <= t}
        if not ready: t = min(v[0] for v in left.values()); continue
        rr_ = {p: (t - v[0] + v[1]) / v[1] for p, v in ready.items()}
        p = max(rr_, key=lambda k: rr_[k]); g.append(f"{p}[{t}-{t+left[p][1]}] RR={rr_[p]:.2f}")
        t += left[p][1]; done[p] = t; del left[p]
    return done, " ".join(g)
res["hrrn"] = metrics("HRRN", A, *hrrn(A))

# ---------------- Banker's algorithm ----------------
def safe(avail, alloc, need):
    work, fin, seq = list(avail), [False] * len(alloc), []
    while True:
        for i in range(len(alloc)):
            if not fin[i] and all(n <= w for n, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]; fin[i] = True; seq.append(f"P{i}"); break
        else: break
    return all(fin), seq

alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
mx = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
avail = [3, 3, 2]
need = [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(mx, alloc)]
print("\n### Banker's: Need matrix", need)
ok, seq = safe(avail, alloc, need); print("safe:", ok, seq)
def valid_seq(order):
    work = list(avail)
    for pid in order:
        i = int(pid[1])
        if any(n > w for n, w in zip(need[i], work)): return False
        work = [w + a for w, a in zip(work, alloc[i])]
    return True
# safe sequences are not unique: the scan-from-P0 order and the textbook's order are both valid
assert ok and seq == ["P1", "P3", "P0", "P2", "P4"] and valid_seq(seq) and valid_seq(["P1", "P3", "P4", "P0", "P2"])
assert not valid_seq(["P0", "P1", "P2", "P3", "P4"])

def request(i, req):
    if any(r > n for r, n in zip(req, need[i])): return "error: exceeds claim"
    if any(r > a for r, a in zip(req, avail)): return "wait: not enough available"
    av2 = [a - r for a, r in zip(avail, req)]
    al2 = [row[:] for row in alloc]; ne2 = [row[:] for row in need]
    al2[i] = [a + r for a, r in zip(al2[i], req)]; ne2[i] = [n - r for n, r in zip(ne2[i], req)]
    ok, s = safe(av2, al2, ne2)
    return f"granted, new available {av2}, safe sequence {s}" if ok else f"denied: unsafe (available would be {av2})"
for i, rq in [(1, [1, 0, 2]), (4, [3, 3, 0]), (0, [0, 2, 0])]:
    print(f"request P{i} {rq}: {request(i, rq)}")
assert request(1, [1, 0, 2]).startswith("granted") and request(4, [3, 3, 0]).startswith("denied") and request(0, [0, 2, 0]).startswith("granted")
# chained: commit P1's grant, then ask again from the new state
alloc[1] = [a + r for a, r in zip(alloc[1], [1, 0, 2])]; need[1] = [n - r for n, r in zip(need[1], [1, 0, 2])]; avail = [2, 3, 0]
print("after committing P1's grant: alloc", alloc, "need", need, "avail", avail)
for i, rq in [(4, [3, 3, 0]), (0, [0, 2, 0])]:
    print(f"chained request P{i} {rq}: {request(i, rq)}")
assert request(4, [3, 3, 0]).startswith("wait") and request(0, [0, 2, 0]).startswith("denied")
alloc[1] = [2, 0, 0]; need[1] = [1, 2, 2]; avail = [3, 3, 2]  # restore base state

# deadlock detection (one resource type each, 3 types) -- Tanenbaum style 4 processes
alloc_d = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
req_d = [[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
avail_d = [0, 0, 0]
def detect(avail, alloc, req):
    work, fin = list(avail), [all(a == 0 for a in alloc[i]) for i in range(len(alloc))]
    ch = True
    while ch:
        ch = False
        for i in range(len(alloc)):
            if not fin[i] and all(r <= w for r, w in zip(req[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]; fin[i] = True; ch = True
    return [f"P{i}" for i, f in enumerate(fin) if not f]
print("\n### Detection: deadlocked =", detect(avail_d, alloc_d, req_d))
req_d2 = [row[:] for row in req_d]; req_d2[2] = [0, 0, 1]
print("after P2 requests one more C: deadlocked =", detect(avail_d, alloc_d, req_d2))
assert detect(avail_d, alloc_d, req_d) == [] and detect(avail_d, alloc_d, req_d2) == ["P1", "P2", "P3", "P4"]

# ---------------- disk scheduling ----------------
q = [98, 183, 37, 122, 14, 124, 65, 67]; head = 53; MAXC = 199
def total(path): return sum(abs(a - b) for a, b in zip(path, path[1:]))
fc = [head] + q
rest = q[:]; cur = head; ss = [head]
while rest:
    nx = min(rest, key=lambda c: abs(c - cur)); rest.remove(nx); ss.append(nx); cur = nx
lo = sorted(c for c in q if c < head)[::-1]; hi = sorted(c for c in q if c >= head)
scan = [head] + hi + [MAXC] + lo           # up first, to the end, then reverse
scan_dn = [head] + lo + [0] + hi           # down first, to 0
look = [head] + hi + lo
cscan = [head] + hi + [MAXC, 0] + sorted(c for c in q if c < head)
clook = [head] + hi + sorted(c for c in q if c < head)
cscan_nj = total([head] + hi + [MAXC]) + total([0] + sorted(c for c in q if c < head))
print("\n### Disk, head 53, queue", q)
for n, p in [("FCFS", fc), ("SSTF", ss), ("SCAN up", scan), ("SCAN down", scan_dn), ("LOOK up", look), ("C-SCAN up (count return jump)", cscan), ("C-LOOK (count return jump)", clook)]:
    print(f"{n}: path {p} total {total(p)}")
print("C-SCAN not counting the return jump:", cscan_nj)
assert total(fc) == 640 and total(ss) == 236 and total(scan) == 331 and total(scan_dn) == 236 and cscan_nj == 183 and total(look) == 299
assert total(cscan) == 382 and total(clook) == 322

# ---------------- page replacement ----------------
def fifo(refs, n):
    fr, faults, rows = deque(), 0, []
    for r in refs:
        hit = r in fr
        if not hit:
            faults += 1
            if len(fr) == n: fr.popleft()
            fr.append(r)
        rows.append((r, list(fr), "hit" if hit else "FAULT"))
    return faults, rows

def lru(refs, n):
    fr, faults, rows = [], 0, []
    for r in refs:
        hit = r in fr
        if hit: fr.remove(r)
        else:
            faults += 1
            if len(fr) == n: fr.pop(0)
        fr.append(r); rows.append((r, list(fr), "hit" if hit else "FAULT"))
    return faults, rows

def opt(refs, n):
    fr, faults, rows = [], 0, []
    for i, r in enumerate(refs):
        hit = r in fr
        if not hit:
            faults += 1
            if len(fr) == n:
                def nxt(p):
                    return refs.index(p, i + 1) if p in refs[i + 1:] else 10 ** 9
                fr.remove(max(fr, key=nxt))
            fr.append(r)
        rows.append((r, sorted(fr), "hit" if hit else "FAULT"))
    return faults, rows

def second_chance(refs, n):
    fr, ref, faults, ptr, rows = [], {}, 0, 0, []
    for r in refs:
        if r in fr: ref[r] = 1; rows.append((r, list(fr), "hit")); continue
        faults += 1
        if len(fr) < n: fr.append(r); ref[r] = 0
        else:
            while ref[fr[ptr]]:
                ref[fr[ptr]] = 0; ptr = (ptr + 1) % n
            del ref[fr[ptr]]; fr[ptr] = r; ref[r] = 0; ptr = (ptr + 1) % n
        rows.append((r, list(fr), "FAULT"))
    return faults, rows

refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
print("\n### Page replacement, 3 frames, string", refs)
for n, f in [("FIFO", fifo), ("OPT", opt), ("LRU", lru), ("Second chance", second_chance)]:
    fl, rows = f(refs, 3); print(f"{n}: {fl} faults")
    if n in ("FIFO", "LRU", "OPT"):
        print("  " + "; ".join(f"{r}:{fr}{'*' if h=='FAULT' else ''}" for r, fr, h in rows))
assert [fifo(refs, 3)[0], opt(refs, 3)[0], lru(refs, 3)[0]] == [15, 9, 12]
bel = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
print("Belady FIFO:", {n: fifo(bel, n)[0] for n in (3, 4)}, "LRU:", {n: lru(bel, n)[0] for n in (3, 4)}, "OPT:", {n: opt(bel, n)[0] for n in (3, 4)})
assert fifo(bel, 3)[0] == 9 and fifo(bel, 4)[0] == 10
sm = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
print("Exam string", sm, {n: (fifo(sm, 3)[0], lru(sm, 3)[0], opt(sm, 3)[0]) for n in ("3 frames F/L/O",)})

# ---------------- memory allocation ----------------
def place(parts, procs, mode):
    parts = parts[:]; out = []
    for p in procs:
        c = [i for i, s in enumerate(parts) if s >= p]
        if not c: out.append((p, None)); continue
        i = {"first": c[0], "best": min(c, key=lambda k: parts[k]), "worst": max(c, key=lambda k: parts[k])}[mode]
        out.append((p, i + 1)); parts[i] -= p      # partition number, 1-based
    return out, parts
parts = [100, 500, 200, 300, 600]; procs = [212, 417, 112, 426]
print("\n### Contiguous allocation", parts, procs)
for m in ("first", "best", "worst"):
    o, left = place(parts, procs, m); print(m, o, "holes left", left)
assert place(parts, procs, "first")[0] == [(212, 2), (417, 5), (112, 2), (426, None)]
assert place(parts, procs, "best")[0] == [(212, 4), (417, 2), (112, 3), (426, 5)]
assert place(parts, procs, "worst")[0] == [(212, 5), (417, 2), (112, 5), (426, None)]

# ---------------- address translation, EAT ----------------
print("\n### Paging: logical 13,000 with 4096-byte pages -> page", 13000 // 4096, "offset", 13000 % 4096)
pt = {0: 5, 1: 9, 2: 3, 3: 7}
la = 13000; pg, off = divmod(la, 4096); print("frame", pt[pg], "physical", pt[pg] * 4096 + off)
assert (pg, off, pt[pg] * 4096 + off) == (3, 712, 7 * 4096 + 712)
for h in (0.80, 0.98):
    print(f"EAT hit {h}: {h*(20+100)+(1-h)*(20+100+100):.1f} ns")
pf = 1e-3  # demand paging
print("demand paging EAT p=1/1000, ma=200ns, fault 8ms:", round((1 - pf) * 200 + pf * 8_000_000), "ns")
print("p for <10% slowdown:", (220 - 200) / (8_000_000 - 200))
seg = {0: (1400, 1000), 1: (6300, 400), 2: (4300, 400), 3: (3200, 1100), 4: (4700, 1000)}
for s, o in [(2, 53), (3, 852), (0, 1222)]:
    b, l = seg[s]; print(f"segment {s} offset {o}:", b + o if o < l else "trap (offset >= limit)")
print("2-level 32-bit, 4KB pages, 4-byte entries: p1/p2/offset = 10/10/12; single table =", 2**20 * 4 // 1024, "KB")
print("inverted: 4 GB RAM / 4 KB =", 2**32 // 2**12, "frames")

# ---------------- disk time ----------------
rpm = 7200; lat = 60 / rpm / 2 * 1000
print(f"\n### 7200 rpm avg rotational latency {lat:.2f} ms; transfer of 4 KB at 100 MB/s {4/1024/100*1000:.3f} ms; total with 9 ms seek {9+lat+4/1024/100*1000:.2f} ms")
print("sectors/track 400 x 512 B at 7200 rpm -> rate", 400 * 512 * 120 / 1e6, "MB/s")

# ---------------- practice-question answers quoted in the units ----------------
print("\n### Practice answers")
tau, a, meas = 10, 0.5, [6, 4, 6, 4, 13, 13, 13]; pred = []
for t in meas: tau = a * t + (1 - a) * tau; pred.append(tau)
print("exp average predictions", pred); assert pred == [8, 6, 6, 5, 9, 11, 12]
P = {"P1": (0, 6), "P2": (0, 8), "P3": (0, 7), "P4": (0, 3)}
print("U3 Q11 FCFS", metrics("FCFS", P, *fcfs(P))[0], "SJF", metrics("SJF", P, *sjf(P))[0])
Q = {"P1": (0, 5), "P2": (0, 3), "P3": (0, 1)}
print("U3 Q12 RR q2 avg TAT", round(metrics("RR2", Q, *rr(Q, 2))[1], 2))
print("RMS bound n=3", round(3 * (2 ** (1 / 3) - 1), 4), "U=", round(2 / 5 + 2 / 7 + 3 / 10, 4), "U'=", round(1 / 4 + 2 / 6 + 1 / 8, 4))
# U4 Q5 banker
alloc = [[1, 0, 1], [2, 1, 0], [1, 1, 1]]; mx = [[3, 2, 2], [3, 2, 1], [2, 2, 3]]; tot = [6, 4, 4]
avail = [t - sum(c) for t, c in zip(tot, zip(*alloc))]; need = [[m - x for m, x in zip(mr, ar)] for mr, ar in zip(mx, alloc)]
print("U4 Q5 avail", avail, "need", need, "safe", safe(avail, alloc, need))
# U4 Q6: P3 asks (0,1,1) in the original state
alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]; mx = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
avail = [3, 3, 2]; need = [[m - x for m, x in zip(mr, ar)] for mr, ar in zip(mx, alloc)]
print("U4 Q6", request(3, [0, 1, 1])); assert request(3, [0, 1, 1]).startswith("granted")
# U5 Q3 placement
parts3 = [150, 350, 100, 600, 250]; procs3 = [210, 130, 480, 90]
for m in ("first", "best", "worst"):
    o, left = place(parts3, procs3, m); print("U5 Q3", m, o, left)
print("U5 Q4 bitmap bits", 2 ** 31 // 2 ** 13, "-> KB", 2 ** 31 // 2 ** 13 // 8 // 1024)
la = 5300; print("U5 Q5 page", la // 2048, "off", la % 2048, "phys", {0: 6, 1: 2, 2: 8, 3: 1}[la // 2048] * 2048 + la % 2048)
print("U5 Q6 table bytes", 2 ** (32 - 13) * 4)
print("U5 Q7 EAT", 0.9 * 90 + 0.1 * 170); print("U5 Q8 EAT", (1 - 1e-4) * 100 + 1e-4 * 10_000_000)
r9 = [1, 2, 3, 2, 4, 1, 5, 2, 1, 2, 3, 4]
print("U5 Q9 FIFO/LRU/OPT", fifo(r9, 3)[0], lru(r9, 3)[0], opt(r9, 3)[0])
# U6 Q6, Q7
print("U6 Q6", 60 / 5400 / 2 * 1000, 12 + 60 / 5400 / 2 * 1000 + 8 / 1024 / 80 * 1000)
q7 = [82, 170, 43, 140, 24, 16, 190]; h = 50
ssq = [h]; rest = q7[:]
while rest:
    nx = min(rest, key=lambda c: abs(c - ssq[-1])); rest.remove(nx); ssq.append(nx)
up = sorted(c for c in q7 if c >= h); dn = sorted((c for c in q7 if c < h), reverse=True)
print("U6 Q7 FCFS", total([h] + q7), "SSTF", total(ssq), "SCAN up", total([h] + up + [199] + dn))
assert (total([h] + q7), total(ssq), total([h] + up + [199] + dn)) == (642, 208, 332)
print("\nALL ASSERTIONS PASSED")
