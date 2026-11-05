#!/usr/bin/env python3
"""Numbers quoted in BCA 251 Units 7-9: inode capacity, password search space, HOTP/TOTP (RFC 4226/6238 test vectors),
salted hashing, Cristian/Berkeley clock synchronisation, Lamport clocks."""
import hmac, hashlib, struct, time
# --- Unit 7: Unix-style inode, 4 KB blocks, 4-byte pointers, 12 direct
B, ptr, direct = 4096, 4, 12
per = B // ptr
sizes = {"direct": direct * B, "single": per * B, "double": per ** 2 * B, "triple": per ** 3 * B}
print("pointers per block", per, sizes, "max file bytes", sum(sizes.values()), "= %.3f TiB" % (sum(sizes.values()) / 2 ** 40))
assert sizes["direct"] == 49152 and sizes["single"] == 4 * 2 ** 20 and sizes["double"] == 4 * 2 ** 30
# 10 KB file in 4 KB blocks, and a 100 MB file
print("blocks for 10,000 B:", -(-10000 // B), "internal waste", -(-10000 // B) * B - 10000)
print("100 MB file blocks", 100 * 2 ** 20 // B, "needs single-indirect?", 100 * 2 ** 20 // B > direct, "double?", 100 * 2 ** 20 // B > direct + per)
# FAT: 4 KB clusters, FAT32 4-byte entries; table for 32 GB volume
print("FAT32 32 GB volume entries", 32 * 2 ** 30 // B, "FAT bytes MB", 32 * 2 ** 30 // B * 4 / 2 ** 20)
# --- Unit 8
for name, n, rate in [("8 lowercase", 26 ** 8, 1e9), ("8 lower+digits", 36 ** 8, 1e9), ("8 printable ASCII (95)", 95 ** 8, 1e9), ("12 printable", 95 ** 12, 1e9)]:
    t = n / rate
    print(f"{name}: {n:,} combos, {t:,.1f} s = {t/86400:,.2f} days = {t/86400/365.25:,.2f} years at 1e9/s")
def hotp(key, counter, digits=6):
    h = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    o = h[-1] & 0xF
    return str((struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % 10 ** digits).zfill(digits)
K = b"12345678901234567890"
rfc = ["755224", "287082", "359152", "969429", "338314", "254676", "287922", "162583", "399871", "520489"]
mine = [hotp(K, c) for c in range(10)]
print("HOTP counters 0-9:", mine); assert mine == rfc
print("TOTP T=59 (30 s step) 8 digits:", hotp(K, 59 // 30, 8)); assert hotp(K, 59 // 30, 8) == "94287082"
import os
salt = bytes.fromhex("a1b2c3d4e5f60718")
print("sha256('nepal123')        =", hashlib.sha256(b"nepal123").hexdigest()[:32] + "...")
print("sha256(salt+'nepal123')   =", hashlib.sha256(salt + b"nepal123").hexdigest()[:32] + "...")
dk = hashlib.pbkdf2_hmac("sha256", b"nepal123", salt, 100_000)
print("pbkdf2-sha256 x100000     =", dk.hex()[:32] + "...")
# --- Unit 9
t0, t1, ts = 0.000, 0.100, 0.550
print("Cristian: RTT", t1 - t0, "estimate", ts + (t1 - t0) / 2); assert abs(ts + 0.05 - 0.600) < 1e-9
times = {"master": 180, "A": 205, "B": 170}; avg = sum(times.values()) / 3
print("Berkeley avg", avg, "min =", f"{int(avg//60)}:{int(avg%60):02d}", {k: avg - v for k, v in times.items()}); assert avg == 185
# Lamport: P1: a, b, send(m1) ; P2: c, recv(m1), d ; P1 recv(m2 from P2 at its time)
L1 = 0; L2 = 0
L1 += 1; a = L1; L1 += 1; b = L1; L1 += 1; send1 = L1
L2 += 1; c = L2; L2 = max(L2, send1) + 1; recv = L2; L2 += 1; d = L2; L2 += 1; send2 = L2
L1 = max(L1, send2) + 1; recv2 = L1
print("Lamport P1 a,b,send:", a, b, send1, "| P2 c, recv, d, send:", c, recv, d, send2, "| P1 recv:", recv2)
assert (a, b, send1, c, recv, d, send2, recv2) == (1, 2, 3, 1, 4, 5, 6, 7)
# RPC: marshalled latency example
print("RPC: local call 1 us vs RPC 2 x 0.5 ms network + 20 us stubs =", 2 * 500 + 20, "us ->", (2 * 500 + 20) / 1, "x slower")
print("OK")
