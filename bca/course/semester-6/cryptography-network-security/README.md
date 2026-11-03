# Cryptography and Network Security — BCA 353 (Semester VI, 3 credits)

Security goals and classical ciphers (Caesar, Vigenère, Playfair, Hill, rail fence), number theory (extended Euclid, Euler, Fermat, CRT, Miller–Rabin, primitive roots), symmetric ciphers (Feistel, DES, a verified AES-128 built from GF(2⁸), ECB/CBC/CTR/GCM), public-key cryptography (RSA, Diffie–Hellman, ElGamal, elliptic curves), hashes, HMAC, signatures and PKI, authentication protocols (Kerberos, TLS 1.3, IPsec, PGP, SSH), and network security (firewalls, IDS, VPN, wireless, key management). 50 teaching hours in this reconstruction (old TU CACS-style elective *Cryptography*; revised list BCA 353).

| Unit | Title | Hours |
|---|---|---|
| 1 | Security Goals and Classical Ciphers | 6 |
| 2 | Number Theory for Cryptography | 7 |
| 3 | Symmetric Ciphers: Feistel, DES, AES and Modes of Operation | 9 |
| 4 | Public-Key Cryptography: RSA, Diffie–Hellman, ElGamal and ECC | 8 |
| 5 | Hash Functions, MACs, Digital Signatures and PKI | 7 |
| 6 | Authentication and Secure Network Protocols | 8 |
| 7 | Network and System Security: Firewalls, IDS, VPN and Wireless | 5 |

## Verification

`bca/tools/check_crypto.py` plus `fill_script_outputs.py`: every Python block in the book is **executed** and its output inserted; the checker then recomputes each printed line with independent code or published constants and `--verify` demands that every expected line is present. Independent references: the textbook ciphertexts (LXFOPVEFRNHR, WECRLTEERDSOEEFEAOCAIVDEN, BMODZBXDNABEKUDMUIXMMOUVIF, POH) and the Hill inverse via sympy's adjugate; `sympy.gcdex`, the Bézout identity on every row of the extended-Euclid table, `sympy.totient`, `isprime`, `primitive_root`; the FIPS-197 AES-128 vector and the `cryptography` library for AES-ECB/CBC/CTR; the NIST SHA-256("abc") value and RFC 4231 HMAC-SHA256 test case 2; RSA identities and the textbook key (d = 2753, c = 2790); brute-force enumeration of the points on y² = x³ + 2x + 2 (mod 17) and the known multiples of G = (5, 1); and exact arithmetic for the birthday bound, brute-force times, TLS round-trip latency, ESP overhead (loop search for the maximum unfragmented inner packet) and the IDS base-rate calculation. All practice answers computed by hand in the text are asserted too.

## Source and honesty

No TU unit list for BCA 353 was retrieved; the seven units are a reconstruction from the topics named in the course brief (classical ciphers, modular arithmetic, symmetric and asymmetric cryptography, hashes and MACs, signatures and PKI, Kerberos/TLS/IPsec/PGP, firewalls/IDS). Algorithms follow Stallings, *Cryptography and Network Security*, Paar and Pelzl, *Understanding Cryptography*, and the cited standards (FIPS-197, RFC 2104, 4231, 8446); prose is original. The Python implementations are **teaching code, not for production**: use a vetted library. The AES implementation is not constant-time.

## Figures and photographs

Every unit ends with a section of plates and figures: real photographs from Wikimedia Commons (scytale, Alberti disk, Enigma, Lorenz SZ42, Bombe, the EFF DES cracker board, hardware security module, portraits of Euler, Fermat, Gauss, Diffie and Hellman, Rivest, Zimmermann, a fire wall, a Cisco ASA, a VPN router, Wi-Fi access points), all licence-gated and credited in the Picture Credits; about 35 SVG schematics (attack model, Feistel round, AES round, CBC, RSA with the textbook numbers, an elliptic-curve addition on real axes, HMAC, signatures, chain of trust, Kerberos, TLS 1.3, ESP, DMZ, rule matching, base-rate arithmetic, Wi-Fi generations, key life cycle); an eight-point section per unit and 5-mark and 10-mark model answers.
