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
