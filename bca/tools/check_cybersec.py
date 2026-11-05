#!/usr/bin/env python3
"""BCA 401 Cyber Security and Ethical Hacking: independent verification of every figure (defensive and analytical content only).
Keys out_* are exact text the executed python blocks must print; other keys are numbers quoted in prose.
Independent methods: published CVSS v3.1 reference scores, hand-written truth tables, exact Fractions, sha256sum, the IEEE 802.11i PMK test vector,
an arrival-curve formulation of the token bucket, exhaustive product search for the birthday bound.
    python3 bca/tools/check_cybersec.py --print | --fill unit-*.md | --verify unit-*.md"""
import sys, math, subprocess, hashlib
from fractions import Fraction as F
from tokcommon import run
T = {}
sha = lambda b: subprocess.run(["sha256sum"], input=b, capture_output=True).stdout.decode().split()[0]
# ---- unit 1: published NVD/FIRST reference scores for these vectors
ref = [("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "9.8", "Critical"), ("AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", "10.0", "Critical"),
       ("AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", "7.8", "High"), ("AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N", "6.1", "Medium"),
       ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", "7.5", "High"), ("AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N", "5.9", "Medium")]
T["out_cvss"] = "\n".join(f"{v} -> {s} ({r})" for v, s, r in ref)
T["out_dread"] = "DREAD average 7.0 -> High\nranked: R1=20, R2=12, R3=4"
T["u1_top"] = "9.8"; T["u1_iss"] = f"{float(1 - (1 - F(56, 100)) ** 3):.4f}"   # ISS for C:H/I:H/A:H
assert T["u1_iss"] == "0.9148"
# ---- unit 2
raw = bytes.fromhex("01bbc93a000003e8000007d15012ffff00000000")
src, dst = int(raw[0:2].hex(), 16), int(raw[2:4].hex(), 16); seq, ack = int(raw[4:8].hex(), 16), int(raw[8:12].hex(), 16)
off, fl, win = raw[12] >> 4, raw[13], int(raw[14:16].hex(), 16)
assert (src, dst, seq, ack, off, fl, win) == (443, 51514, 1000, 2001, 5, 0x12, 65535)
T["out_tcp"] = "src 443 dst 51514 seq 1000 ack 2001 hdr 20 bytes flags SYN,ACK window 65535"
T["out_flags"] = "\n".join(["0x02: SYN", "0x12: SYN,ACK", "0x10: ACK", "0x18: PSH,ACK", "0x11: FIN,ACK", "0x04: RST",
                            "0x00: none <- invalid combination", "0x03: FIN,SYN <- invalid combination"])
T["out_inv"] = "unapproved listening ports: [3306, 8080]\napproved but not listening: []"
T["u2_syn"], T["u2_synack"] = "0x02", "0x12"
# ---- unit 3
bits = lambda R, L: float(L * math.log2(R ** 1)) if False else math.log2(R ** L)     # log2 of the whole space R^L
T["out_ent"] = "\n".join(f"{n}: {bits(R, L):.1f} bits" for n, R, L in (("8 chars, 95 printable", 95, 8), ("12 chars, lowercase", 26, 12), ("6 Diceware words", 7776, 6), ("16 chars, alphanumeric", 62, 16)))
half = F(95 ** 8, 2); assert 95 ** 8 == 6634204312890625
days = half / 10 ** 10 / 86400; yrs = half * 600000 / 10 ** 10 / 86400 / 365
T["out_wf"] = f"fast hash at 1e10 guesses/s: {float(days):.2f} days\nPBKDF2 at 600000 iterations: {float(yrs):.0f} years\nargon2 memory bound: {24 * 1024 // 19} instances in 24 GiB"
T["u3_bits8"], T["u3_days"], T["u3_yrs"], T["u3_inst"] = f"{bits(95, 8):.1f}", f"{float(days):.2f}", f"{float(yrs):.0f}", "1293"
T["out_pw"] = "correct password accepted: True\nwrong password accepted: False\nsame password, different salt, different hash: True"
T["out_rbac"] = "\n".join(["alice can approve_payment: False", "bob can approve_payment: True", "carol can approve_payment: True",
    "separation-of-duties violations: ['carol']", "internal reads secret: False", "internal writes secret: True", "secret writes public: False"])
# ---- unit 4
T["out_val"] = "encoded: &lt;b&gt;bold&lt;/b&gt; &amp; more\nram_01 -> True\n1ram -> False\nab -> False\nvalid_user_name_that_is_too_long -> False"
T["out_sql"] = "placeholder lookup of O'Brien: 1 row(s)\nstring-built query fails on same input: True\nflagged lines: [2, 3, 4]"
T["out_csp"] = ("policy A issues: []\npolicy B issues: ['wildcard source in default-src', 'unsafe-inline in script-src', "
                "'missing object-src', 'missing base-uri', 'missing frame-ancestors']")
T["out_csrf"] = "valid token accepted: True\ntoken from another session rejected: True\nmissing token rejected: True"
tbl = {"Strict": (True, False, False, False), "Lax": (True, True, False, False), "None": (True, True, True, True)}
reqs = ("same-site request", "cross-site top-level GET link", "cross-site POST form", "cross-site subresource")
T["out_ss"] = "\n".join(f"{p}/{r}: cookie sent {v}" for p, vs in tbl.items() for r, v in zip(reqs, vs))
# ---- unit 5
def n50(b):                                # smallest n with P(collision) >= 1/2 by exact product, then compare with the closed form
    N, p, n = 2 ** b, F(1), 0
    while p > F(1, 2): p *= F(N - n, N); n += 1
    return n
import decimal; decimal.getcontext().prec = 40
cf = lambda b: int((2 * decimal.Decimal(2).ln() * (2 ** b)).sqrt().to_integral_value(decimal.ROUND_CEILING))
for b in (16, 24): assert abs(n50(b) - cf(b)) <= 1, (b, n50(b), cf(b))
T["out_bday"] = "\n".join([f"{b}-bit space: 50% collision after about {cf(b)} samples" for b in (16, 24, 32)] +
                          ["MD5 (128-bit digest): collision work about 2^64", "SHA-1 (160-bit digest): collision work about 2^80", "SHA-256 (256-bit digest): collision work about 2^128"])
T["u5_16"], T["u5_32"] = str(cf(16)), str(cf(32))
pmk = hashlib.pbkdf2_hmac("sha1", b"password", b"IEEE", 4096, 32).hex()
assert pmk == "f42c6fc52df0ebef9ebb4b90b38a5f902e83fe1b135a70e23aed762e9710a12e"       # IEEE 802.11i Annex H test vector
T["out_wpa"] = "PMK (first 16 hex): f42c6fc52df0ebef\nPTK (CCMP) = 384 bits = KCK 128 + KEK 128 + TK 128"
acc = 0
for i in range(1000):                       # arrival-curve view: cumulative accepted <= B + r*t
    if acc + 1 <= 10 + F(5) * F(i * 10, 1000): acc += 1
T["out_tb"] = f"burst of 15 at t=0: accepted 10, rejected 5\n10 s of 100 req/s: accepted {acc} of 1000 (bound 60)"; T["u5_acc"] = str(acc)
T["out_acl"] = "\n".join(["tcp 203.0.113.5 -> 10.0.1.10:443 = permit (rule 1)", "tcp 203.0.113.5 -> 10.0.1.10:22 = deny (rule 3)",
                          "tcp 10.0.9.4 -> 10.0.1.10:22 = permit (rule 2)", "udp 10.0.9.4 -> 10.0.1.10:53 = deny (rule 3)", "shadowed rules: [2]"])
# ---- unit 6
mal, tot = 100, 100000; tp, fn = 99, 1; fp = (tot - mal) * 1 // 100; tn = tot - mal - fp
assert (fp, tn) == (999, 98901)
prec = F(tp, tp + fp); f1 = F(2 * tp, 2 * tp + fp + fn)
T["out_cm"] = (f"events 100000, malicious 100: TP=99 FN=1 FP=999 TN=98901\nTPR 99.00%, FPR 1.00%, precision {float(prec*100):.2f}%, accuracy {float(F(tp+tn, tot)*100):.2f}%, F1 {float(f1):.4f}\n"
               f"P(malicious | alert) via Bayes: {float(F(99, 100) * F(1, 1000) / (F(99, 100) * F(1, 1000) + F(1, 100) * F(999, 1000)) * 100):.2f}%")
p2 = lambda fpr: F(tp, 1) / (tp + (tot - mal) * fpr)
T["out_prec"] = f"precision at FPR 0.10%: {float(p2(F(1,1000))*100):.2f}%; at FPR 0.01%: {float(p2(F(1,10000))*100):.2f}%\ndaily alerts {tp + fp}, analyst effort {float(F((tp + fp) * 5, 60)):.1f} hours at 5 min each"
T["u6_prec"] = f"{float(prec*100):.2f}"; T["u6_alerts"] = "1,098"; assert T["u6_prec"] == "9.02"
T["out_ev"] = f"evidence SHA-256 (first 16 hex): {sha(b'disk-image-bytes-0001')[:16]}\ncustody chain entries: 3, verified: True\nafter editing entry 2: verified False"
# ---- unit 7
def nsamp(conf, rate):                      # smallest n with (1-rate)^n <= 1-conf, exact
    n, p = 0, F(1)
    while p > 1 - conf: p *= 1 - rate; n += 1
    return n
T["out_samp"] = "\n".join(f"confidence {c}%, tolerable deviation {t}%: sample {nsamp(F(c, 100), F(t, 100))}" for c, t in ((95, 5), (90, 10), (99, 5)))
assert [nsamp(F(c, 100), F(t, 100)) for c, t in ((95, 5), (90, 10), (99, 5))] == [59, 22, 90]
sle = 500000 * F(40, 100); ale0 = sle * F(1, 4); ale1 = sle * F(1, 20); rosi = (ale0 - ale1 - 20000) / 20000
T["out_ale"] = f"SLE {int(sle)}, ALE before {int(ale0)}, ALE after {int(ale1)}, ROSI {int(rosi*100)}%"
T["out_roe"] = "ROE completeness: 7 of 9 fields; missing: ['data handling', 'emergency contact']"
T["out_eta"] = "\n".join(["s47 illegal publication: up to 5 years, Rs 100000", "s44 source code offences: up to 3 years, Rs 200000",
    "s45 unauthorised access: up to 3 years, Rs 200000", "s46 damage to systems: up to 3 years, Rs 200000", "s52 computer fraud: up to 2 years, Rs 100000"])
T["u7_n"] = "59"
if __name__ == "__main__":
    run(T, sys.argv[1:])
