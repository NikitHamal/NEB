---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 4
title: Public-Key Cryptography - RSA, Diffie-Hellman, ElGamal and ECC
hours: 8
area: BCA 353 · Cryptography and Network Security · Unit 4
---

Symmetric ciphers have a problem that no amount of cleverness inside the cipher can solve: both parties must already share a secret key. How do two strangers, a customer and an online shop, agree on one over a network that anyone can listen to? **Public-key** (asymmetric) cryptography solved this in the 1970s. Each party has a **public key**, which may be published, and a **private key**, which is never shared, linked by a mathematical one-way relationship from Unit 2: easy to compute in one direction and infeasible to reverse. This unit works through **RSA**, **Diffie–Hellman**, **ElGamal** and **elliptic-curve cryptography** with small numbers you can verify by hand, every one of which was executed and cross-checked.

::: key What this unit gives you
- The public-key idea and the hard problems behind it (factoring, discrete log, elliptic-curve discrete log).
- RSA key generation, encryption, decryption, CRT decryption and signing, with a worked example.
- Diffie–Hellman key exchange and the man-in-the-middle attack; ElGamal encryption.
- Elliptic curves over a prime field: point addition, scalar multiplication, ECDH; key sizes.
:::

## 4.1 The public-key idea

With **n users**, symmetric keys need n(n − 1)/2 pairs: 1,000 users need **499,500** shared keys. Public-key schemes need only n key pairs. The roles: a **public key** encrypts (or verifies signatures) and a **private key** decrypts (or signs). Two uses follow: **encryption** (anyone encrypts with Alice's public key; only Alice decrypts) and **digital signatures** (Alice signs with her private key; anyone verifies with her public key, Unit 5). Public-key operations are slow (thousands of times slower than AES), so in practice they are used to **establish or transport a symmetric session key**, and AES encrypts the data: a **hybrid** scheme. The security rests on hard problems: **integer factorisation** (RSA), the **discrete logarithm** (Diffie–Hellman, ElGamal, DSA) and the **elliptic-curve discrete logarithm** (ECDH, ECDSA).

## 4.2 RSA

**Key generation** (Rivest, Shamir, Adleman, 1977):

1. Choose two large distinct primes **p** and **q** (1024 bits each for a 2048-bit key).
2. Compute **n = pq** and **φ(n) = (p − 1)(q − 1)**.
3. Choose a public exponent **e** with 1 < e < φ(n) and gcd(e, φ(n)) = 1 (commonly 65537).
4. Compute the private exponent **d = e⁻¹ mod φ(n)** (extended Euclid).

The **public key** is (e, n); the **private key** is d (with p and q kept secret). **Encryption:** c = mᵉ mod n, for 0 ≤ m < n. **Decryption:** m = cᵈ mod n. **Why it works:** ed ≡ 1 (mod φ(n)), so ed = 1 + kφ(n) and, by Euler's theorem (Unit 2), mᵉᵈ = m · (m^φ(n))ᵏ ≡ m (mod n) (the case where m shares a factor with n also works, by the Chinese Remainder Theorem). **Security** depends on the difficulty of factoring n: anyone who can factor n computes φ(n) and then d.

**CRT speed-up.** The owner knows p and q, so decryption is done modulo each prime separately: m₁ = c^(d mod (p−1)) mod p, m₂ = c^(d mod (q−1)) mod q, and h = q⁻¹(m₁ − m₂) mod p gives m = m₂ + h·q. This is about four times faster and is how real RSA libraries decrypt. **Signing** with RSA is the same operation as decryption applied to a digest: s = hᵈ mod n; verification computes sᵉ mod n and compares it with h.

The classic textbook example, p = 61, q = 53, e = 17, message m = 65:

```python
p, q, e = 61, 53, 17
n, phi = p * q, (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = 65
c = pow(m, e, n)
print("n =", n, " phi =", phi, " d =", d)
print("c =", c, " decrypted =", pow(c, d, n))
dp, dq, qinv = d % (p - 1), d % (q - 1), pow(q, -1, p)
m1, m2 = pow(c, dp, p), pow(c, dq, q)
h = qinv * (m1 - m2) % p
print("CRT decrypt =", m2 + h * q, " (dp, dq, qinv) =", (dp, dq, qinv))
s = pow(m, d, n)
print("signature =", s, " verifies:", pow(s, e, n) == m)

p2, q2, e2 = 17, 11, 7
n2, d2 = p2 * q2, pow(e2, -1, (p2 - 1) * (q2 - 1))
print("second key: n =", n2, " d =", d2, " 88 ->", pow(88, e2, n2), "->", pow(pow(88, e2, n2), d2, n2))
```
```output
n = 3233  phi = 3120  d = 2753
c = 2790  decrypted = 65
CRT decrypt = 65  (dp, dq, qinv) = (53, 49, 38)
signature = 588  verifies: True
second key: n = 187  d = 23  88 -> 11 -> 88
```
By hand: n = 3233, φ = 60 × 52 = 3120, e = 17, d = 2753 (since 17 × 2753 = 46801 = 15 × 3120 + 1). Then 65¹⁷ mod 3233 = 2790, and 2790²⁷⁵³ mod 3233 = 65. The second key (n = 187, e = 7, d = 23) is the small example used in many textbooks: 88 encrypts to 11 and decrypts back.

::: caution Textbook RSA is not safe as written
Real use needs **padding**: RSA-OAEP for encryption and RSA-PSS for signatures. Without it, RSA is deterministic (an attacker can test guesses), malleable (c·2ᵉ mod n decrypts to 2m) and breakable when the same short message is sent to several recipients with a small e (Håstad). Use at least **2048-bit** keys (3072 for long-term), a random padding scheme and a vetted library. Never reuse p or q across keys: gcd of two moduli reveals the shared prime.
:::

## 4.3 Diffie–Hellman key exchange

**Diffie–Hellman (1976)** lets two parties create a shared secret over a public channel. They agree publicly on a prime p and a primitive root g (Unit 2). Alice picks a secret a and sends **A = gᵃ mod p**; Bob picks b and sends **B = gᵇ mod p**. Alice computes Bᵃ mod p, Bob computes Aᵇ mod p, and both equal **gᵃᵇ mod p**. An eavesdropper sees p, g, A, B but would need the discrete log to find a or b. **ElGamal encryption** turns this into a cipher: with private x and public y = gˣ mod p, to encrypt m choose a random k and send **(c₁, c₂) = (gᵏ mod p, m·yᵏ mod p)**; to decrypt compute s = c₁ˣ mod p and **m = c₂·s⁻¹ mod p**. The ciphertext is twice as long as the message and must use a fresh k each time.

```python
p, g = 23, 5
a, b = 6, 15
A, B = pow(g, a, p), pow(g, b, p)
print("A =", A, " B =", B, " shared:", pow(B, a, p), pow(A, b, p))
x = 6
y = pow(g, x, p)
m, k = 10, 3
c1, c2 = pow(g, k, p), m * pow(y, k, p) % p
s = pow(c1, x, p)
print("ElGamal: y =", y, " c1 =", c1, " c2 =", c2, " decrypted =", c2 * pow(s, -1, p) % p)
```
```output
A = 8  B = 19  shared: 2 2
ElGamal: y = 8  c1 = 10  c2 = 14  decrypted = 10
```
Plain Diffie–Hellman provides **no authentication**: in a **man-in-the-middle attack** Mallory intercepts A and B, replaces them with her own values, and holds one shared key with Alice and another with Bob, relaying and reading everything. The defence is to **authenticate the exchanged values**, with digital signatures and certificates (Unit 5), as TLS does. Modern protocols use **ephemeral** DH (a fresh key per session), giving **forward secrecy**: stealing a server's long-term key later cannot decrypt recorded old sessions. Real groups use 2048-bit or larger primes, or elliptic curves.

## 4.4 Elliptic-curve cryptography

An **elliptic curve** over a prime field is the set of points (x, y) satisfying **y² = x³ + ax + b (mod p)** together with a special **point at infinity O** (the identity). Points can be **added** with a geometric rule that is computed algebraically: for P = (x₁, y₁) and Q = (x₂, y₂), the slope is **m = (y₂ − y₁)/(x₂ − x₁)** for P ≠ Q and **m = (3x₁² + a)/(2y₁)** for doubling P = Q (division means multiplying by the modular inverse); then **x₃ = m² − x₁ − x₂** and **y₃ = m(x₁ − x₃) − y₁**, all mod p; P + (−P) = O, where −P = (x, −y). **Scalar multiplication** kP = P + P + … + P (k times) is computed fast by double-and-add; but recovering k from P and kP is the **elliptic-curve discrete logarithm problem**, which has no sub-exponential algorithm, so a 256-bit curve key gives security comparable to a 3072-bit RSA key, with smaller keys and faster operations.

The textbook curve y² = x³ + 2x + 2 over p = 17 with base point G = (5, 1):

```python
p, a, b = 17, 2, 2
G = (5, 1)

def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        m = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (m * m - x1 - x2) % p
    return (x3, (m * (x1 - x3) - y1) % p)

def mul(k, P):
    R = None
    while k:
        if k & 1:
            R = add(R, P)
        P = add(P, P)
        k >>= 1
    return R

pts, P = [], G
while P is not None:
    pts.append(P)
    P = add(P, G)
print("multiples:", pts)
print("order of G =", len(pts) + 1)
alice, bob = 3, 7
A, B = mul(alice, G), mul(bob, G)
print("ECDH: A =", A, " B =", B, " shared:", mul(alice, B), mul(bob, A))
```
```output
multiples: [(5, 1), (6, 3), (10, 6), (3, 1), (9, 16), (16, 13), (0, 6), (13, 7), (7, 6), (7, 11), (13, 10), (0, 11), (16, 4), (9, 1), (3, 16), (10, 11), (6, 14), (5, 16)]
order of G = 19
ECDH: A = (10, 6)  B = (0, 6)  shared: (6, 3) (6, 3)
```
G has **order 19** (19G = O), so there are 19 distinct multiples; 2G = (6, 3). In the elliptic-curve Diffie–Hellman, Alice (secret 3) sends 3G = (10, 6), Bob (secret 7) sends 7G = (0, 6), and both compute 21G = 2G = (6, 3). Real curves (P-256, Curve25519) use primes of 256 bits; **ECDSA** and **EdDSA** (Ed25519) are the matching signature schemes.

## 4.5 Comparing key sizes and uses

| Security level (bits) | Symmetric | RSA / DH modulus | Elliptic curve |
|---|---|---|---|
| 80 (legacy) | 80 | 1024 | 160 |
| 112 | 112 (3DES) | 2048 | 224 |
| 128 | AES-128 | 3072 | 256 |
| 192 | AES-192 | 7680 | 384 |
| 256 | AES-256 | 15360 | 512 |

RSA is simple and universal but its keys are large and key generation slow; elliptic curves give small keys and signatures and dominate on mobile and in TLS 1.3. **Quantum computers** running Shor's algorithm would break RSA, DH and ECC; NIST has standardised **post-quantum** algorithms (ML-KEM/Kyber for key exchange, ML-DSA/Dilithium for signatures), and "harvest now, decrypt later" is the reason migration is already under way, while symmetric ciphers need only larger keys (AES-256).

## Chapter summary

- Public-key cryptography removes the shared-secret problem: n users need n key pairs instead of n(n − 1)/2, and it is used to exchange symmetric keys (hybrid encryption).
- RSA: n = pq, d = e⁻¹ mod φ(n), c = mᵉ mod n, m = cᵈ mod n; the example n = 3233, d = 2753 encrypts 65 to 2790; real RSA needs OAEP/PSS padding and ≥ 2048-bit keys.
- Diffie–Hellman agrees gᵃᵇ mod p and needs authentication against man-in-the-middle; ElGamal encrypts with a fresh k.
- Elliptic curves give the same security with far smaller keys; the example curve has a point of order 19.

## Practice

1. How many symmetric keys do 50 users need for pairwise secure communication, and how many key pairs for public-key?
2. Generate an RSA key with p = 11, q = 13, e = 7: give n, φ, d.
3. Encrypt m = 9 with the key from question 2.
4. Why does RSA decryption recover m? State the theorem used.
5. Alice and Bob use p = 13, g = 2, a = 5, b = 4. Compute A, B and the shared key.
6. How does a man-in-the-middle break unauthenticated Diffie–Hellman?
7. ElGamal with p = 11, g = 2, x = 3: compute y; then encrypt m = 7 with k = 4.
8. On y² = x³ + 2x + 2 (mod 17) double P = (5, 1).
9. Why is textbook RSA unsafe and what fixes it?
10. Why do elliptic curves allow shorter keys?

::: note Answers and worked solutions
**1.** 50 × 49 / 2 = **1,225** symmetric keys; **50** key pairs.
**2.** n = 143, φ = 10 × 12 = 120, d = 7⁻¹ mod 120: 7 × 103 = 721 = 6 × 120 + 1, so **d = 103**.
**3.** 9⁷ mod 143: 9² = 81; 9⁴ = 6561 mod 143 = 6561 − 45 × 143 (6435) = 126; 9⁷ = 9⁴ · 9² · 9 = 126 · 81 · 9 mod 143. 126 · 81 = 10206 mod 143 = 10206 − 71 × 143 (10153) = 53; 53 · 9 = 477 mod 143 = 477 − 429 = **48**. (Decrypting: 48¹⁰³ mod 143 = 9.)
**4.** ed ≡ 1 (mod φ(n)); by Euler's theorem m^φ(n) ≡ 1 (mod n), so mᵉᵈ ≡ m.
**5.** A = 2⁵ mod 13 = 32 mod 13 = 6; B = 2⁴ mod 13 = 3; shared = B⁵ mod 13 = 3⁵ = 243 mod 13 = **9** (check: A⁴ = 6⁴ = 1296 mod 13 = 9).
**6.** Mallory replaces A and B with her own public values and negotiates separate keys with each side, then decrypts and re-encrypts all traffic; neither side can tell without authentication.
**7.** y = 2³ mod 11 = 8. c₁ = 2⁴ mod 11 = 5; c₂ = 7 · 8⁴ mod 11; 8² = 64 ≡ 9, 8⁴ ≡ 81 ≡ 4; c₂ = 28 mod 11 = **6**. Ciphertext **(5, 6)**.
**8.** m = (3·25 + 2)/(2·1) = 77/2 mod 17 = 9 · 2⁻¹ = 9 · 9 = 81 mod 17 = 13 (since 77 mod 17 = 9 and 2⁻¹ = 9). x₃ = 13² − 10 = 159 mod 17 = 6; y₃ = 13(5 − 6) − 1 = −14 mod 17 = 3. **2G = (6, 3)**.
**9.** It is deterministic and malleable, and has attacks for small messages and small e; OAEP/PSS randomised padding fixes it.
**10.** The best known attacks on the elliptic-curve discrete logarithm are fully exponential, whereas factoring and the ordinary discrete log have sub-exponential algorithms, so smaller keys reach the same security.
:::
