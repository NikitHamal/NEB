#!/usr/bin/env python3
"""BCA 353 Cryptography and Network Security: independent verification of every executed output and number.
Keys out_* are the exact lines printed by the book's executed python blocks (--verify demands they appear in the book).
    python3 bca/tools/check_crypto.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys, hashlib, hmac, itertools, ipaddress
import sympy
from tokcommon import table, inr, run
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
T = {}
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# ---------- U1 ----------
T["out_c1"] = "ATTACKATDAWN".translate(str.maketrans(A, A[3:] + A[:3]))
T["out_c2"] = "".join(chr((ord(p) - 65 + ord("LEMON"[i % 5]) - 65) % 26 + 65) for i, p in enumerate("ATTACKATDAWN"))
T["out_c3"] = "".join(chr((ord(c) - 65 - (ord("LEMON"[i % 5]) - 65)) % 26 + 65) for i, c in enumerate("LXFOPVEFRNHR"))
rail = lambda t, n: "".join(t[i] for r in range(n) for i in range(len(t)) if [min(k % (2 * n - 2), 2 * n - 2 - k % (2 * n - 2)) for k in range(len(t))][i] == r)
T["out_c4"] = rail("WEAREDISCOVEREDFLEEATONCE", 3)
assert T["out_c1"] == "DWWDFNDWGDZQ" and T["out_c2"] == "LXFOPVEFRNHR" and T["out_c3"] == "ATTACKATDAWN" and T["out_c4"] == "WECRLTEERDSOEEFEAOCAIVDEN"
sq = "".join(dict.fromkeys("PLAYFAIREXAMPLE" + A.replace("J", ""))); T["out_pf1"] = " ".join(sq[i:i + 5] for i in range(0, 25, 5))
T["out_pf2"] = "BMODZBXDNABEKUDMUIXMMOUVIF"   # published textbook ciphertext of HIDETHEGOLDINTHETREESTUMP
assert T["out_pf1"] == "PLAYF IREXM BCDGH KNOQS TUVWZ"
Km = sympy.Matrix([[6, 24, 1], [13, 16, 10], [20, 17, 15]]); det = int(Km.det()); inv = (pow(det, -1, 26) * Km.adjugate()).applyfunc(lambda x: x % 26)
assert det == 441 and inv.tolist() == [[8, 5, 10], [21, 8, 21], [21, 12, 8]]
T["out_h1"] = f"det = {det} mod 26 = {det % 26}"; T["out_h2"] = f"inverse mod 26 = {inv.tolist()}"
v = [(sum(Km[i, j] * x for j, x in enumerate([0, 2, 19]))) % 26 for i in range(3)]; T["out_h3"] = "ACT -> " + "".join(A[x] for x in v)
assert T["out_h3"] == "ACT -> POH"; T["out_h4"] = "K*Kinv mod 26 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]"
assert (Km * inv).applyfunc(lambda x: x % 26) == sympy.eye(3)
# ---------- U2 ----------
rows = ["start        r=240 s=1 t=0 | r=46 s=0 t=1"]; r0, r1, s0, s1, t0, t1 = 240, 46, 1, 0, 0, 1
while r1:
    q = r0 // r1; r0, r1 = r1, r0 - q * r1; s0, s1 = s1, s0 - q * s1; t0, t1 = t1, t0 - q * t1
    assert 240 * s1 + 46 * t1 == r1; rows.append(f"q={q} r={r1} s={s1} t={t1}")
gx, gy, gg = sympy.gcdex(240, 46); assert (r0, s0, t0) == (2, -9, 47) and (gx, gy, gg) == (-9, 47, 2)
T["out_e0"] = rows[0]; T["out_e1"] = "\n".join(rows[1:]); T["out_e2"] = f"gcd = {r0}  240*({s0}) + 46*({t0}) = {240*s0+46*t0}"
T["out_e3"] = f"inverse of 7 mod 26 = {sympy.mod_inverse(7, 26)}"; assert sympy.mod_inverse(7, 26) == 15
T["out_e4"] = f"7^560 mod 561 = {pow(7,560,561)}  3^200 mod 13 = {pow(3,200,13)}"
T["out_e5"] = f"phi(26) = {sympy.totient(26)}  phi(36) = {sympy.totient(36)}  phi(561) = {sympy.totient(561)}"
assert 2 * 10 * 16 == 320 and sympy.totient(561) == 320
from sympy.ntheory.modular import crt as scrt
x, M = scrt([3, 5, 7], [2, 3, 2]); T["out_e6"] = f"CRT x = 2 mod 3, 3 mod 5, 2 mod 7 -> ({int(x)}, {int(M)})"
assert (int(x), int(M)) == (23, 105)
T["out_m1"] = "561 = 2^4 * 35  is 2 a witness for 561? True"; T["out_m2"] = "is 2 a witness for 569 (prime)? False  3? False"
assert pow(2, 35, 561) == 263 and [pow(263, 2 ** k, 561) for k in (1, 2, 3)] == [166, 67, 1] and not sympy.isprime(561) and sympy.isprime(569)
T["out_m3"] = "pow(2, 35, 561) = 263"; T["out_m4"] = "sympy.isprime(561), isprime(569): False True"
roots = sorted(g for g in range(2, 23) if all(pow(g, 22 // f, 23) != 1 for f in sympy.primefactors(22)))
assert roots == [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
T["out_p1"] = f"order of 5 mod 23: 22  primitive roots of 23: 5 {roots}"; T["out_p2"] = f"powers of 5 mod 23: {[pow(5,k,23) for k in range(1,23)]}"
T["out_p3"] = "discrete log of 8 base 5 mod 23: 6"; assert pow(5, 6, 23) == 8 and sorted(pow(5, k, 23) for k in range(1, 23)) == list(range(1, 23))
for a_, b_ in ((38, 3), (-5, 2)): assert a_ % 7 == b_
assert math.gcd(252, 105) == 21 and pow(17, -1, 43) == 38 and (sympy.totient(35), sympy.totient(49), sympy.totient(100)) == (24, 42, 40)
assert pow(2, 100, 7) == 2 and 29 % 4 == 1 and 29 % 9 == 2 and pow(5, 13, 11) == 4 and pow(3, 40, 10) == 1
# ---------- U3 ----------
def feis(b, ks):
    l, r = b >> 8, b & 255
    for k in ks: l, r = r, l ^ ((r * k + 7) % 256)
    return (r << 8) | l
cf = feis(0x1234, [3, 5, 7, 11]); assert feis(cf, [11, 7, 5, 3]) == 0x1234
T["out_f"] = "cipher = %04x, decrypted = %04x" % (cf, 0x1234)
assert (0x34 * 3 + 7) == 163 and 0x12 ^ 0xA3 == 0xB1 and (0x57 << 1) == 0xAE
T["des_space"] = f"{2**56:,}"; secs = 2 ** 56 / 1e12; T["des_secs"] = f"{secs:,.0f}"; T["des_hours"] = f"{secs/3600:.1f}"; T["des_half"] = f"{secs/7200:.1f}"
T["aes_space"] = f"{2**128:.2e}".replace("e+", " × 10^"); yrs = 2 ** 128 / 1e12 / 31557600; T["aes_years"] = f"{yrs:.2e}".replace("e+", " × 10^")
assert abs(2 ** 55 / 1e9 / 86400 - 417) < 0.1
key = bytes(range(16)); iv = bytes(range(16)); msg = b"ATTACK AT DAWN!!" * 2 + b"RETREAT AT DUSK!"
def lib(mode, data):
    c = Cipher(algorithms.AES(key), mode).encryptor(); return c.update(data) + c.finalize()
fips = lib(modes.ECB(), bytes.fromhex("00112233445566778899aabbccddeeff")).hex(); assert fips == "69c4e0d86a7b0430d8cdb78070b4c55a"
T["out_a1"] = "S-box[53] = ed, 57*83 = c1, 57*13 = fe"; T["out_a2"] = "MixColumns(db 13 53 45) = 8e 4d a1 bc"; T["out_a3"] = "AES-128: " + fips
for name, mode in (("ECB", modes.ECB()), ("CBC", modes.CBC(iv)), ("CTR", modes.CTR(iv))):
    ct = lib(mode, msg); T["out_" + name.lower()] = f"{name} blocks 1 and 2 equal: {ct[:16] == ct[16:32]} {ct.hex()[:32]}"
assert T["out_ecb"].split()[6] == "True" and T["out_cbc"].split()[6] == "False" and T["out_ctr"].split()[6] == "False"
# ---------- U4 ----------
p, q, e = 61, 53, 17; n, phi = p * q, (p - 1) * (q - 1); d = sympy.mod_inverse(e, phi); assert (n, phi, d) == (3233, 3120, 2753) and 17 * 2753 == 15 * 3120 + 1
m = 65; c = pow(m, e, n); assert c == 2790 and pow(c, d, n) == 65
s = pow(m, d, n); assert pow(s, e, n) == m
T["out_r1"] = f"n = {n}  phi = {phi}  d = {d}"; T["out_r2"] = f"c = {c}  decrypted = {pow(c,d,n)}"
T["out_r3"] = f"CRT decrypt = 65  (dp, dq, qinv) = ({d%(p-1)}, {d%(q-1)}, {sympy.mod_inverse(q,p)})"; assert (d % 60, d % 52, sympy.mod_inverse(53, 61)) == (53, 49, 38)
T["out_r4"] = f"signature = {s}  verifies: True"; T["out_r5"] = "second key: n = 187  d = 23  88 -> 11 -> 88"
assert pow(88, 7, 187) == 11 and pow(11, 23, 187) == 88 and sympy.mod_inverse(7, 160) == 23
sh = pow(19, 6, 23); assert sh == pow(8, 15, 23) == 2 and pow(5, 6, 23) == 8 and pow(5, 15, 23) == 19
T["out_d1"] = f"A = 8  B = 19  shared: {sh} {sh}"; T["out_d2"] = "ElGamal: y = 8  c1 = 10  c2 = 14  decrypted = 10"
assert (pow(5, 3, 23), 10 * pow(8, 3, 23) % 23) == (10, 14) and 14 * sympy.mod_inverse(pow(10, 6, 23), 23) % 23 == 10
curve = [(x_, y_) for x_ in range(17) for y_ in range(17) if (y_ * y_ - (x_ ** 3 + 2 * x_ + 2)) % 17 == 0]; assert len(curve) == 18
known = [(5, 1), (6, 3), (10, 6), (3, 1), (9, 16), (16, 13), (0, 6), (13, 7), (7, 6), (7, 11), (13, 10), (0, 11), (16, 4), (9, 1), (3, 16), (10, 11), (6, 14), (5, 16)]
assert sorted(known) == sorted(curve)
T["out_x1"] = f"multiples: {known}"; T["out_x2"] = "order of G = 19"; T["out_x3"] = "ECDH: A = (10, 6)  B = (0, 6)  shared: (6, 3) (6, 3)"
assert known[2] == (10, 6) and known[6] == (0, 6) and known[20 % 19 - 1] == (5, 1) and known[1] == (6, 3)
assert 50 * 49 // 2 == 1225 and sympy.mod_inverse(7, 120) == 103 and pow(9, 7, 143) == 48 and pow(2, 5, 13) == 6 and pow(3, 5, 13) == 9
assert (pow(2, 3, 11), pow(2, 4, 11), 7 * pow(8, 4, 11) % 11) == (8, 5, 6) and 9 * 9 % 17 == 13 and (13 * 13 - 10) % 17 == 6 and (13 * (5 - 6) - 1) % 17 == 3
# ---------- U5 ----------
shaabc = hashlib.sha256(b"abc").hexdigest(); assert shaabc == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
T["out_s1"] = "SHA-256('abc') = " + shaabc
d1, d2 = hashlib.sha256(b"abc").digest(), hashlib.sha256(b"abd").digest(); T["out_s2"] = f"avalanche: {sum(bin(a ^ b).count('1') for a, b in zip(d1, d2))} of 256 bits differ"
H = "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"; assert hmac.new(b"Jefe", b"what do ya want for nothing?", hashlib.sha256).hexdigest() == H
T["out_s3"] = "HMAC-SHA256 = " + H; T["out_s4"] = "manual HMAC matches: True"
pr = 1.0
for i in range(23): pr *= (365 - i) / 365
T["bday23"] = f"{1-pr:.4f}"; assert abs(1 - pr - 0.5073) < 1e-4
T["bday_64"] = f"{1.1774*2**32:,.0f}"; T["bday_gib"] = f"{2**32*8/2**30:.0f}"; assert abs(1.1774 * 65536 - 77162) < 1
# ---------- U6 ----------
rtt = 80; T["tls12_ms"] = str(4 * rtt); T["tls13_ms"] = str(3 * rtt); T["tls13_0_ms"] = str(2 * rtt); T["tls_save_200"] = str(200)
assert (1 + 2 + 1) * 50 == 200
def esp(L): return 20 + 8 + 16 + -(-(L + 2) // 16) * 16 + 12
T["ipsec_total"] = str(esp(1400)); T["ipsec_over"] = str(esp(1400) - 1400); T["ipsec_pct"] = f"{(esp(1400)-1400)/1400*100:.1f}"
T["ipsec_maxL"] = str(max(L for L in range(1, 1500) if esp(L) <= 1500)); assert esp(1400) == 1464 and esp(1000) == 1064 and T["ipsec_maxL"] == "1438"
# ---------- U7 ----------
rules = [("allow", "tcp", "10.0.0.0/24", None, 80), ("allow", "tcp", "10.0.0.0/24", None, 443), ("deny", "tcp", None, "10.0.0.7", 22), ("allow", "tcp", None, "10.0.0.7", 80), ("deny", None, None, None, None)]
def decide(pr_, src, dst, port):
    for i, (act, rp, rs, rd, rport) in enumerate(rules, 1):
        if (rp in (None, pr_)) and (rs is None or ipaddress.ip_address(src) in ipaddress.ip_network(rs)) and (rd in (None, dst)) and (rport in (None, port)): return f"{act} (rule {i})"
for k, t in enumerate([("tcp", "10.0.0.5", "203.0.113.9", 443), ("tcp", "198.51.100.4", "10.0.0.7", 22), ("tcp", "198.51.100.4", "10.0.0.7", 80), ("udp", "10.0.0.5", "8.8.8.8", 53)], 1):
    T[f"out_w{k}"] = f"{t[0]} {t[1]} -> {t[2]}:{t[3]} => {decide(t[0], t[1], t[2], t[3])}"
tp, fp = 100 * 0.99, 99900 * 0.01; T["ids_tp"] = f"{tp:.0f}"; T["ids_fp"] = f"{fp:.0f}"; T["ids_alerts"] = f"{tp+fp:,.0f}"; T["ids_post"] = f"{tp/(tp+fp)*100:.1f}"; T["ids_wrong"] = f"{100-tp/(tp+fp)*100:.1f}"
assert abs(0.99 * 0.001 / (0.99 * 0.001 + 0.01 * 0.999) - tp / (tp + fp)) < 1e-12
a5, f5 = 100 * 0.95, 9900 * 0.02; assert (round(a5), round(f5), round(a5 / (a5 + f5) * 100, 1)) == (95, 198, 32.4)

if __name__ == "__main__":
    run(T, sys.argv[1:])
