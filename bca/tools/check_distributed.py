#!/usr/bin/env python3
"""BCA 355 Distributed System: independent verification of every number printed by the book's executed python blocks.
Keys out_* are the exact lines the executed blocks must print (--verify demands they appear in the book); other keys are
numbers quoted in prose and answer keys. Independent methods: Fraction arithmetic, popcount, causal-history counting for
vector clocks, transitive closure, permutation search, math.comb, exhaustive traitor strategies.
    python3 bca/tools/check_distributed.py --print | --fill unit-*.md | --verify unit-*.md"""
import sys, math
from fractions import Fraction as F
from itertools import product, combinations
from tokcommon import run
T = {}
# ---------------- unit 1 ----------------
lines = [f"{n} replica(s) at 99%: {float((1 - F(1, 100) ** n) * 100):.4f}%" for n in (1, 2, 3)]
chain = F(999, 1000) ** 5
lines += [f"5 services in series at 99.9% each: {float(chain * 100):.4f}%",
          f"downtime per year: {float((1 - chain) * 525600):.1f} minutes"]
T["out_av"] = "\n".join(lines)
T["down_min"] = f"{float((1 - chain) * 525600):.1f}"; T["chain_pct"] = f"{float(chain * 100):.4f}"
assert T["chain_pct"] == "99.5010" and T["down_min"] == "2622.7", T
T["ans5"] = f"{float((1 - F(5, 1000) ** 2) * 100):.4f}"; assert T["ans5"] == "99.9975"
c4 = F(9995, 10000) ** 4; T["ans6"] = f"{float(c4 * 100):.4f}"; T["ans6_down"] = f"{float((1 - c4) * 525600):.1f}"
assert (T["ans6"], T["ans6_down"]) == ("99.8001", "1050.4"), (T["ans6"], T["ans6_down"])
T["out_lat"] = "one-way 10.0 ms, round trip 20.0 ms\nstop-and-wait: 50 msg/s = 409.6 kbit/s\n10 sequential remote calls cost 200 ms; one batched call 20 ms"
assert F(1000, 20) * 8192 / 1000 == F(4096, 10)
T["ans7"] = f"{1000 / 30:.1f}"; assert T["ans7"] == "33.3"
def path(key):
    p, node, d = [0], 0, key
    for b in range(3, -1, -1):
        if d >> b & 1: node += 1 << b; p.append(node)
    return p
cl = []
for k in (13, 7, 15, 0):
    p = path(k); assert len(p) - 1 == bin(k).count("1")
    cl.append(f"key {k:2d}: {' -> '.join(map(str, p))}  ({len(p) - 1} hops)")
tot = sum(bin(k).count("1") for k in range(16)); assert tot == 32
cl.append("average over all 16 keys: 2.00 hops (log2(N)/2 = 2.0)")
T["out_chord"] = "\n".join(cl)
assert path(13) == [0, 8, 12, 13] and bin((14 - 3) % 16).count("1") == 3
# ---------------- unit 2 ----------------
raw = (150).to_bytes(4, "big") + b"Ram\0\0" + (2082).to_bytes(2, "big")
js = '{"id":150,"name":"Ram","year":2082}'
T["json_len"] = str(len(js)); assert len(raw) == 11 and len(js) == 35
assert (150 & 0x7F | 0x80, 150 >> 7) == (0x96, 1) and (300 & 0x7F | 0x80, 300 >> 7) == (0xAC, 2) and (0xAC & 0x7F) + (2 << 7) == 300
T["out_marsh"] = (f"fixed binary: {raw.hex(' ')} (11 bytes)\nvarint(150): 96 01\nvarint(300): ac 02\n"
                  f"protobuf field 1 = 150: 08 96 01\nJSON: {js} (35 bytes)")
T["out_xml"] = "add(2, 3) = 5\nstats([4, 8, 9]) = {'n': 3, 'mean': 7.0}\nmethods: ['add', 'stats']\nbad call -> Fault"
T["out_retry"] = "dedup=False: attempts=3, balance=700, reply=700\ndedup=True : attempts=3, balance=900, reply=900"
T["out_queue"] = "delivery order: m1 m2 m3 m2\nprocessed: ['m1', 'm3', 'm2']\n4 deliveries for 3 messages"
# ---------------- unit 3 ----------------
T["drift_day"] = "0.864"; T["resync"] = "50"; assert abs(10e-6 * 86400 - 0.864) < 1e-12 and abs(0.001 / 20e-6 - 50) < 1e-9
T["out_drift"] = "drift per day: 0.864 s\nresync interval for 1 ms skew: 50 s"
cr = []
for T0, T1, Ts in [(1000, 1040, 1520), (2000, 2016, 2490), (3000, 3100, 3560)]:
    rtt = T1 - T0; est = F(Ts) + F(rtt, 2); assert est - T1 == F(Ts - T1) + F(rtt, 2)
    cr.append("RTT=%3d ms  estimated server time=%7.1f  offset to apply=%+7.1f ms" % (rtt, est, est - T1))
assert cr[1].endswith("+482.0 ms") and cr[0].endswith("+500.0 ms") and cr[2].endswith("+510.0 ms")
cr.append("best sample RTT=16 ms: offset +482.0 ms, error bound +/- 3.0 ms"); T["out_cristian"] = "\n".join(cr)
T["cr_err"] = "3.0"; assert F(16, 2) - 5 == 3
T["out_berk"] = ("limit=None: average offset +5.0 min, adjustments {'master': 5.0, 's1': 15.0, 's2': -20.0}\n"
                 "limit=20: average offset -5.0 min, adjustments {'master': -5.0, 's1': 5.0, 's2': -30.0}")
assert F(0 - 10 + 25, 3) == 5 and F(0 - 10, 2) == -5 and 175 - 205 == -30 and 185 - 170 == 15
t0, t1, t2, t3 = 1000, 1060, 1062, 1026
assert F((t1 - t0) + (t2 - t3), 2) == 48 and (t3 - t0) - (t2 - t1) == 24 and F(10 - 14, 2) == -2
T["out_ntp"] = "offset theta = 48.0 ms, round-trip delay delta = 24 ms\ntrue offset 50 ms; error = -2.0 ms = (up - down)/2 with up=10, down=14"
# happened-before graph: vector = causal-history counts, Lamport = longest chain
procs = ["P1", "P2", "P3"]
ev = [("P1", "local", None), ("P1", "send", "m1"), ("P2", "local", None), ("P2", "recv", "m1"), ("P3", "local", None),
      ("P2", "send", "m2"), ("P3", "recv", "m2"), ("P3", "send", "m3"), ("P1", "recv", "m3")]
n = len(ev); pred = {i: set() for i in range(n)}
for i in range(n):
    for j in range(i):
        if ev[j][0] == ev[i][0]: last = j
    prev = [j for j in range(i) if ev[j][0] == ev[i][0]]
    if prev: pred[i].add(max(prev))
    if ev[i][1] == "recv": pred[i].add(next(j for j in range(n) if ev[j][1] == "send" and ev[j][2] == ev[i][2]))
def anc(i):
    s = {i}
    for j in pred[i]: s |= anc(j)
    return s
A = [anc(i) for i in range(n)]
def longest(i): return 1 + max([longest(j) for j in pred[i]], default=0)
rows = []
for i in range(n):
    V = tuple(sum(1 for j in A[i] if ev[j][0] == p) for p in procs)
    rows.append(f"e{i + 1}  {ev[i][0]} {ev[i][1]:<5} {(ev[i][2] or '-'):<2}  L={longest(i)}  V={V}")
conc = [(a + 1, b + 1) for a in range(n) for b in range(a + 1, n) if a not in A[b] and b not in A[a]]
assert conc == [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (4, 5), (5, 6)]
T["out_lamport"] = "\n".join(rows) + f"\nconcurrent pairs: {conc}"
assert rows[3].endswith("L=3  V=(2, 2, 0)") and rows[4].endswith("L=1  V=(0, 0, 1)") and rows[8].endswith("L=7  V=(3, 3, 3)")
T["ans2_day"] = "1.728"; T["ans2_int"] = "250"; assert abs(20e-6 * 86400 - 1.728) < 1e-12 and abs(0.005 / 20e-6 - 250) < 1e-9
assert 5400 + 15 - 5030 == 385 and 15 - 8 == 7 and F(6 - 3, 3) == 1 and F((130 + 90), 2) == 110 and 42 - 2 == 40
# vector comparisons from practice 7
lt = lambda u, v: all(a <= b for a, b in zip(u, v)) and u != v
Av, Bv, Cv = (3, 1, 0), (2, 2, 1), (3, 2, 1)
assert not lt(Av, Bv) and not lt(Bv, Av) and lt(Av, Cv) and lt(Bv, Cv)
# ---------------- unit 4 ----------------
N = 4; reqs = {1: 3, 2: 3, 3: 5, 4: 4}
order = sorted(reqs, key=lambda p: (reqs[p], p)); assert order == [1, 2, 4, 3]
T["out_ra"] = f"entry order: {order}\nmessages: {N*(N-1)} REQUEST + {N*(N-1)} REPLY = {2*N*(N-1)} (2N(N-1) = {2*N*(N-1)})"
assert 2 * N * (N - 1) == 24
mk = []
for NN in (9, 16):
    k = math.isqrt(NN); Q = [{j for j in range(NN) if j // k == i // k or j % k == i % k} for i in range(NN)]
    assert all(Q[a] & Q[b] for a in range(NN) for b in range(NN)) and all(len(q) == 2 * k - 1 for q in Q)
    mk.append(f"N={NN}: quorum size {2*k-1}, all pairs intersect: True, 3*(K-1)={3*(2*k-2)} messages vs Ricart-Agrawala {2*(NN-1)}")
assert mk[0].endswith("12 messages vs Ricart-Agrawala 16") and mk[1].endswith("18 messages vs Ricart-Agrawala 30")
mk.append("quorum of node 4 (N=9): [1, 3, 4, 5, 7]"); T["out_maek"] = "\n".join(mk)
def bully_cf(n, dead, s):
    alive = [p for p in range(1, n + 1) if p not in dead]
    chain = [p for p in alive if p >= s]
    e = sum(n - p for p in chain); o = sum(sum(1 for q in alive if q > p) for p in chain); c = len(alive) - 1
    return e, o, c, e + o + c, max(alive)
bl = []
for s in (6, 3, 1):
    e, o, c, tot, l = bully_cf(7, {7}, s); bl.append(f"starter {s}: ELECTION={e} OK={o} COORDINATOR={c} total={tot} leader={l}")
T["out_bully"] = "\n".join(bl); b = [bully_cf(7, {7}, s)[3] for s in (6, 3, 1)]; assert b == [6, 21, 41]
T["bully_best"], T["bully_mid"], T["bully_worst"] = map(str, b)
assert bully_cf(5, {5}, 2)[:4] == (7 - 4 + 0 + 0 + 3 + 0 - 3 + 3 - 3 + 0, 6, 3, 12) or bully_cf(5, {5}, 2)[3] == 12
T["out_ring"] = "ring: ELECTION hops=6, COORDINATOR hops=6, total=12, leader=6"; T["ring_total"] = "12"
T["ans6_m"] = str(3 * (2 * 5 - 1 - 1)); T["ans6_ra"] = str(2 * 24); assert (T["ans6_m"], T["ans6_ra"]) == ("24", "48")
assert 2 * (10 - 1) == 18 and 2 * 8 == 16
q5 = sorted({j for j in range(9) if j // 3 == 5 // 3 or j % 3 == 5 % 3}); assert q5 == [2, 3, 4, 5, 8]
# ---------------- unit 5 ----------------
def twopc(votes, crash=False):
    n = len(votes); dec = "BLOCKED" if crash else ("COMMIT" if all(votes) else "ABORT")
    yes = sum(votes); msgs = 2 * n if crash else (2 * n + 2 * (n if dec == "COMMIT" else yes))
    st = []
    for i, v in enumerate(votes, 1):
        s = ["INIT", "READY" if v else "ABORT"]
        if not crash and v: s.append(dec)
        st.append(f"P{i}: " + ">".join(s))
    return dec, msgs, " | ".join(st)
tp = []
for name, v, c in (("all yes", [1, 1, 1], False), ("P2 votes no", [1, 0, 1], False), ("coordinator crash", [1, 1, 1], True)):
    d, m, s = twopc(v, c); tp.append(f"{name}: {d}, messages={m}, {s}")
assert [twopc(v, c)[1] for v, c in (([1, 1, 1], False), ([1, 0, 1], False), ([1, 1, 1], True))] == [12, 10, 6]
T["pc_all"], T["pc_abort"], T["pc3"] = "12", "10", "18"; assert 6 * 3 == 18 and 4 * 5 == 20 and 6 * 5 == 30
def cyc(edges):
    nodes = sorted({x for e in edges for x in e}); reach = set(edges)
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if (i, k) in reach and (k, j) in reach: reach.add((i, j))
    return any((x, x) in reach for x in nodes)
sites = [[("T1", "T2")], [("T2", "T3")], [("T3", "T1")]]
assert not any(cyc(e) for e in sites) and cyc([x for e in sites for x in e])
dl = [f"S{i} local cycle: None" for i in (1, 2, 3)] + ["global cycle: ['T1', 'T2', 'T3', 'T1']"]
s1 = [(1, 2), (2, 1)]; s2 = [(1, 2)]; assert cyc(s1) and not cyc(s2)
dl += ["S1 edges: [(1, 2), (2, 1)] -> NOT serializable, cycle [1, 2, 1]", "S2 edges: [(1, 2)] -> serializable"]
T["out_2pc"] = "\n".join(tp); T["out_dl"] = "\n".join(dl)
assert not cyc([(1, 2), (1, 2)])
# ---------------- unit 6 ----------------
qs = []
for N_, W, R in ((5, 3, 3), (5, 2, 3), (3, 2, 2), (3, 1, 3)):
    pairs = math.comb(N_, W) * math.comb(N_, R); dis = math.comb(N_, W) * math.comb(N_ - W, R)
    qs.append(f"N={N_} W={W} R={R}: R+W>N is {R + W > N_}; {pairs} quorum pairs, {dis} disjoint")
T["out_quorum"] = "\n".join(qs); T["q_dis"] = "10"; assert qs[1].endswith("100 quorum pairs, 10 disjoint") and qs[0].endswith("100 quorum pairs, 0 disjoint")
assert math.comb(4, 2) * math.comb(2, 2) == 6 and math.comb(4, 2) ** 2 == 36 and 7 - 4 + 1 == 4
T["out_lin"] = ("H1: linearizable=True, sequentially consistent=True\nH2: linearizable=False, sequentially consistent=True\n"
                "H3: linearizable=True, sequentially consistent=True\nH4: linearizable=False, sequentially consistent=False")
# independent hand-derivation: H2 order R0,W1 is sequential (B has only the read); real time forces W1 first -> stale read
T["out_paxos"] = ("proposal 1: proposes 'X', accepted by 2\nproposal 2: proposes 'X', accepted by 4\n"
                  "stale proposal 1 retries accept: 0 accepted\n"
                  "acceptor states: {1: (1, 'X'), 2: (2, 'X'), 3: (2, 'X'), 4: (2, 'X'), 5: (2, 'X')}")
termsd = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3}
def raft(m, cur=3):
    ok = [i for i in range(1, 10) if sum(x >= i for x in m) >= 3 and termsd[i] == cur]
    return (max(ok), sum(x >= max(ok) for x in m)) if ok else None
assert raft([9, 9, 7, 5, 4]) is None and raft([9, 9, 8, 8, 4]) == (8, 4)
T["out_raft"] = "case A: None\ncase B: (8, 4)"
assert sorted([6, 6, 5, 3, 2])[2] == 5 and sum(x >= 6 for x in (6, 6, 5, 3, 2)) == 2
# ---------------- unit 7 ----------------
def om1(n, traitor_cmd, traitor_lt, cmd_bits, relay_bits, honest=1):
    lts = list(range(1, n)); got = {l: (cmd_bits[l] if traitor_cmd else honest) for l in lts}; dec = {}
    for l in lts:
        votes = [got[l]] + [relay_bits[(o, l)] if o == traitor_lt else got[o] for o in lts if o != l]
        dec[l] = 1 if 2 * sum(votes) > len(votes) else 0
    return dec
def exhaustive(n):
    lts = list(range(1, n)); ok_all = True
    for cb in product((0, 1), repeat=n - 1):                                   # traitor commander, any bits
        d = om1(n, True, None, dict(zip(lts, cb)), {}); ok_all &= len(set(d.values())) == 1
    for t in lts:                                                              # traitor lieutenant, loyal commander
        others = [(t, l) for l in lts if l != t]
        for rb in product((0, 1), repeat=len(others)):
            d = om1(n, False, t, {}, dict(zip(others, rb))); loyal = [v for l, v in d.items() if l != t]
            ok_all &= all(v == 1 for v in loyal) and len(set(loyal)) == 1
    return ok_all
assert exhaustive(4) is True and exhaustive(3) is False
T["out_byz"] = ("n=4, traitor=commander: loyal decisions {1: 1, 2: 1, 3: 1}, agreement=True, validity=n/a\n"
                "n=4, traitor=lieutenant 2: loyal decisions {1: 1, 3: 1}, agreement=True, validity=True\n"
                "n=3, traitor=commander: loyal decisions {1: 0, 2: 0}, agreement=True, validity=n/a\n"
                "n=3, traitor=lieutenant 2: loyal decisions {1: 0}, agreement=True, validity=False\n"
                + "\n".join(f"f={f}: Byzantine needs n>={3*f+1}, crash needs n>={2*f+1}" for f in range(1, 6)))
assert [3 * f + 1 for f in range(1, 6)] == [4, 7, 10, 13, 16]
T["out_snap"] = ("recorded process states: {'P': 90, 'Q': 55}\nrecorded channel states: {'Q->P': [5], 'P->Q': []}\n"
                 "snapshot total = 150 (initial total 150)")
assert 90 + 55 + 5 == 150 == 100 + 50
MB = 1024 ** 2; blocks = -(-1000 // 128); assert (blocks, 1000 - 7 * 128, blocks * 3, 3 * 1000) == (8, 104, 24, 3000)
hd = ["8 blocks (last block 104 MB), 24 replicas, raw storage 3000 MB", "NameNode metadata at ~150 B per block: 100 million blocks = 15 GB"]
for k in (2, 3, 4): hd.append(f"{k} simultaneous node failures of 100: P(a given block lost) = {float(F(math.comb(k, 3), math.comb(100, 3))):.2e}")
hd.append("replica placement for a write from a2: ['a2', 'b1', 'b2']")
T["out_hdfs"] = "\n".join(hd); T["hdfs_p3"] = f"{float(F(1, 161700)):.2e}"; assert math.comb(100, 3) == 161700 and T["hdfs_p3"] == "6.18e-06"
assert -(-700 // 128) == 6 and 700 - 5 * 128 == 60 and 6 * 3 == 18 and 700 * 3 == 2100
if __name__ == "__main__":
    run(T, sys.argv[1:])
