"""Recompute the worked results added to the Digital Logic book (BCA 103). Run: python3 check_digital.py"""
import itertools, sys
from sympy import symbols, SOPform, POSform
ok = True
def chk(label, a, b):
    global ok
    if a != b:
        ok = False
        print("MISMATCH", label, a, b)

def qm(minterms, n):
    """return (stages, primes) of Quine-McCluskey; implicants are (value, mask-of-dashes)."""
    cur = {(m, 0): {m} for m in minterms}
    stages = [dict(cur)]
    primes = {}
    while cur:
        nxt = {}; used = set()
        keys = list(cur)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                (v1, d1), (v2, d2) = keys[i], keys[j]
                if d1 == d2:
                    x = v1 ^ v2
                    if x and (x & (x - 1)) == 0:
                        key = (v1 & v2, d1 | x)
                        nxt.setdefault(key, set()).update(cur[keys[i]] | cur[keys[j]])
                        used.add(keys[i]); used.add(keys[j])
        for k in keys:
            if k not in used: primes[k] = cur[k]
        cur = nxt
        if cur: stages.append(dict(cur))
    return stages, primes

def term(v, d, n, names="ABCDE"):
    s = ""
    for i in range(n):
        bit = n - 1 - i
        if d >> bit & 1: continue
        s += names[i] + ("" if v >> bit & 1 else "'")
    return s

def run_qm(ms, n):
    st, pr = qm(ms, n)
    print("minterms", ms)
    for k, s in enumerate(st):
        print(" stage", k)
        for (v, d), cov in sorted(s.items(), key=lambda t: (bin(t[0][0]).count("1"), t[0])):
            print("   ", format(v, "0%db" % n).replace("0", "0"), "mask", format(d, "0%db" % n), sorted(cov))
    for (v, d), cov in sorted(pr.items()):
        print(" PRIME", term(v, d, n), sorted(cov))
    return pr

pr = run_qm([0, 1, 2, 5, 6, 7, 8, 9, 10, 14], 4)
A, B, C, D, E = symbols("A B C D E")
print(SOPform([A, B, C, D], [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]))
print("--- five variable")
m5 = [0, 2, 4, 6, 9, 11, 13, 15, 17, 21, 25, 27, 29, 31]
print(SOPform([A, B, C, D, E], m5))
run_qm(m5, 5)
print("--- 5-var with dont-care")
print(SOPform([A, B, C, D, E], [1, 3, 5, 7, 9, 11, 13, 15, 16, 20, 24, 28], [2, 18, 26]))
# Petrick-style cover count check for 4-var example
def covers(sel, ms):
    return set().union(*[pr[p] for p in sel]) >= set(ms)
# hazard: F = AB + A'C with B=C=1
def F(a, b, c): return (a & b) | ((1 - a) & c)
chk("static1", [F(a, 1, 1) for a in (0, 1)], [1, 1])
# BCD adder
def bcd_add(x, y, cin=0):
    s = x + y + cin
    if s > 9: s += 6
    return s
for x, y in [(7, 5), (9, 8), (4, 3), (6, 7), (9, 9)]:
    raw = x + y
    corr = raw > 9
    print("BCD", x, y, format(raw, "05b"), "correct" if corr else "", format(raw + 6 if corr else raw, "05b"), "=", (raw + 6 if corr else raw))
# carry-lookahead 4 bit
def cla(a, b, c0):
    g = [(a >> i & 1) & (b >> i & 1) for i in range(4)]
    p = [(a >> i & 1) ^ (b >> i & 1) for i in range(4)]
    c = [c0]
    for i in range(4): c.append(g[i] | (p[i] & c[i]))
    s = [p[i] ^ c[i] for i in range(4)]
    return g, p, c, s
for a, b, c0 in [(0b1011, 0b0110, 0), (0b0111, 0b0001, 1), (0b1111, 0b0001, 0)]:
    g, p, c, s = cla(a, b, c0)
    print("CLA", format(a, "04b"), format(b, "04b"), "cin", c0, "G", g[::-1], "P", p[::-1], "C1..C4", c[1:], "S", s[::-1], "check", a + b + c0)
    chk("cla", sum(s[i] << i for i in range(4)) + (c[4] << 4), a + b + c0)
# gate delays: ripple 4/8/16/32 bit, 2 gate delays per stage vs CLA
for n in (4, 8, 16, 32):
    print("ripple", n, "bits:", 2 * n, "gate delays (carry), CLA 4-bit groups:", 2 + 2 * (n // 4 - 1) if n > 4 else 3)
# MUX hazards etc: 5-var map count
print("OK" if ok else "FAIL")
# ---- unit 1 numbers
print("--- unit 1")
for name, t, p in [("74", 10, 10), ("74S", 3, 19), ("74LS", 9.5, 2), ("74ALS", 4, 1.2)]:
    print("PDP", name, t * p, "pJ")
print("dyn 5V", 20e-12 * 25 * 1e6 * 1e3, "mW; 3.3V", 20e-12 * 3.3 ** 2 * 1e6 * 1e3, "mW; 3.3V 100MHz", 20e-12 * 3.3 ** 2 * 100e6 * 1e3)
print("fanout 74", min(16 / 1.6, 0.4e3 / 40), "74LS", min(8 / 0.4, 400 / 20))
print("Rmin", (5 - 0.4) / (16e-3 - 4 * 1.6e-3), "Rmax", (5 - 2.4) / (3 * 250e-6 + 4 * 40e-6))
print("avg tp", (8 + 12) / 2, "chain5", 5 * 10, "fmax", 1e3 / (50 + 20), "MHz")
for n in (8, 12, 16): print("SNR", n, round(6.02 * n + 1.76, 1))
print("CD bps", 44100 * 16 * 2, "MB/min", 44100 * 16 * 2 / 8 * 60 / 1e6, "tel", 8000 * 8)
print("step 12bit 3.3V", 3.3 / 4096 * 1000, "mV; 10bit 5V", 5 / 1024 * 1000)
print("Nyquist for 20kHz", 2 * 20000)
# ---- unit 3 additions
print("--- unit 3")
# BCD adder correction rule: C = K + S3 S2 + S3 S1 over all digit pairs and carry in
bad = 0
for x in range(10):
    for y in range(10):
        for cin in (0, 1):
            s = x + y + cin
            K = s >> 4; S = s & 15
            cond = K | ((S >> 3 & 1) & (S >> 2 & 1)) | ((S >> 3 & 1) & (S >> 1 & 1))
            chk("bcdrule", int(cond), int(s > 9))
            t = s + 6 if cond else s
            chk("bcdsum", (t >> 4 & 1) * 10 + (t & 15), s)
print("BCD rule verified for all 200 cases")
# seven-segment (a..g), common cathode, BCD input ABCD, 10-15 don't care
seg = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}
for s in "abcdefg":
    ms = [d for d in range(10) if s in seg[d]]
    print("seg", s, ms, SOPform([A, B, C, D], ms, [10, 11, 12, 13, 14, 15]))
# MUX-based truth table sanity: 5-var mintern sets used in practice
print("p1", SOPform([A, B, C, D, E], [1, 3, 5, 7, 9, 11, 13, 15, 16, 20, 24, 28]))
print("p2", SOPform([A, B, C, D, E], [0, 1, 4, 5, 10, 11, 14, 15, 16, 17, 20, 21, 26, 27, 30, 31]))
print("p3 QM 4var", SOPform([A, B, C, D], [1, 3, 4, 5, 9, 11, 12, 13, 14, 15]))
print("p4 QM dc", SOPform([A, B, C, D], [4, 8, 10, 11, 12, 15], [9, 14]))
print("p5 hazard F=AB+A'C+BC", ((1 << 0)))
print(POSform([A, B, C, D], [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]))
# ---- unit 4 additions
print("--- unit 4")
import math
# up/down 3-bit synchronous counter: T0=1, T1 = U Q0 + D Q0', T2 = U Q1 Q0 + D Q1' Q0'
q = 0; seq = []
for u in [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]:
    seq.append((u, format(q, "03b")))
    b0, b1, b2 = q & 1, q >> 1 & 1, q >> 2 & 1
    t0 = 1; t1 = (b0 if u else 1 - b0); t2 = (b1 & b0) if u else ((1 - b1) & (1 - b0))
    q ^= t0 | (t1 << 1) | (t2 << 2)
    chk("updown", q, (seq and ((int(seq[-1][1], 2) + (1 if u else -1)) % 8)))
print("updown", seq, "final", format(q, "03b"))
# LFSR x^4 + x^3 + 1 (Fibonacci, taps on Q4 and Q3), seed 0001, shift left, new bit = Q4 xor Q3
s = 1; states = []
for _ in range(16):
    states.append(format(s, "04b"))
    nb = (s >> 3 & 1) ^ (s >> 2 & 1)
    s = ((s << 1) & 15) | nb
print("lfsr", states, "period", states[1:].index(states[0]) + 1, "distinct", len(set(states)))
# dividers
print("2^15", 2 ** 15, "flipflops clock: sec 4+3, min 4+3, hr 4+2 =", 7 + 7 + 6, "plus 15 =", 7 + 7 + 6 + 15)
print("32768 chain", [32768 / 2 ** k for k in (1, 5, 10, 14, 15)])
print("freq counter res", {g: 1 / g for g in (1, 0.1, 0.01)})
# metastability MTBF
def mtbf(tr, tau, T0, fc, fd): return math.exp(tr / tau) / (T0 * fc * fd)
print("MTBF 1ff", mtbf(1e-9, 0.2e-9, 0.5e-9, 100e6, 10e6), "s")
m2 = mtbf(8e-9, 0.2e-9, 0.5e-9, 100e6, 10e6); print("MTBF 2ff", m2, "s", m2 / 3.156e7, "years")
print("hours in clock", 23 * 3600 + 59 * 60 + 59 + 1)
# ---- unit 5 additions
print("--- unit 5")
# traffic light, Gray assignment: Q1+ = T Q0 + T' Q1 ; Q0+ = T Q1' + T' Q0
q1 = q0 = 0; out = []
names = {(0,0):"NS green/EW red",(0,1):"NS yellow/EW red",(1,1):"NS red/EW green",(1,0):"NS red/EW yellow"}
for T in [0,1,0,1,1,1,1,0,1]:
    out.append((T, names[(q1,q0)]))
    n1 = (T & q0) | ((1-T) & q1); n0 = (T & (1-q1)) | ((1-T) & q0); q1, q0 = n1, n0
print(out, "final", names[(q1,q0)])
# Mealy vs Moore '11' detector equivalence
def mealy(x):
    s=0; o=[]
    for b in x:
        if s==0: o.append(0); s=1 if b else 0
        else: o.append(1 if b else 0); s=1 if b else 0
    return o
def moore(x):
    # states A,B0,B1 ; output of state
    s="A"; o=[]
    trans={"A":("A","B0"),"B0":("A","B1"),"B1":("A","B1")}; outv={"A":0,"B0":0,"B1":1}
    for b in x:
        s=trans[s][b]; o.append(outv[s])   # output after the clock edge, same time as Mealy's
    return o
import random
for _ in range(200):
    x=[random.randint(0,1) for _ in range(12)]
    chk("mealy-moore", mealy(x), moore(x))
x=[0,1,1,1,0,1,1]
print("x",x,"mealy",mealy(x))
# analysis example: D_A = A x + B x ; D_B = A' x ; y = (A + B) x'
print("analysis table")
for A in (0,1):
    for B in (0,1):
        row=[]
        for x_ in (0,1):
            nA=(A&x_)|(B&x_); nB=(1-A)&x_; y=(A|B)&(1-x_)
            row.append((nA,nB,y))
        print(A,B,row)
# sequence for the example: start 00, input 1,1,1,0,1,0
A=B=0; seq=[]
for x_ in [1,1,1,0,1,0]:
    nA=(A&x_)|(B&x_); nB=(1-A)&x_; y=(A|B)&(1-x_); seq.append((x_,"%d%d"%(A,B),y)); A,B=nA,nB
print(seq,"final %d%d"%(A,B))
