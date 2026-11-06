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

## 4.6 Seeing public-key cryptography: pioneers, keys and curves

Public-key cryptography solves the oldest problem of secret writing: how can two people who have never met agree on a key over an open line? The plate shows the two researchers who first published the answer and a worked key exchange with small numbers. The figures show the two-key idea, the RSA steps with the textbook numbers, an elliptic-curve addition drawn on real axes and the key sizes that give equal strength.

```photogrid label="4.1" cols="2" ratio="1.25" caption="The first public answer to key exchange. (a) Whitfield Diffie (left) and Martin Hellman (right), who published 'New Directions in Cryptography' in 1976, showing that two people can agree on a shared secret using only public messages. (b) Their exchange with the small numbers p = 23 and g = 5: Alice keeps a = 6 and sends A = 5 to the power 6 mod 23 = 8; Bob keeps b = 15 and sends B = 19; each then computes the same secret 2. An eavesdropper sees only 23, 5, 8 and 19."
@ photo id="crypto353/diffie" cap="Diffie and Hellman"
fit 1.25
focus 0.5 0.5
call 0.25 0.1 0.25 0.45 "Whitfield Diffie"
call 0.75 0.1 0.75 0.45 "Martin Hellman"
@ svg cap="Diffie-Hellman with p = 23, g = 5"
f = Fig(340, 272)
f.text(170, 14, "Public: p = 23, g = 5", size=13, color=NAVY, bold=True)
f.box(6, 30, 130, 70, "Alice\nsecret a = 6\nA = 5^6 mod 23 = 8", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(204, 30, 130, 70, "Bob\nsecret b = 15\nB = 5^15 mod 23 = 19", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.arrow([(136, 52), (204, 52)], color=AMBER, label="A = 8", lpos=(170, 44), lsize=12)
f.arrow([(204, 80), (136, 80)], color=AMBER, label="B = 19", lpos=(170, 98), lsize=12)
f.box(6, 130, 130, 56, "Alice computes\n19^6 mod 23 = 2", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(204, 130, 130, 56, "Bob computes\n8^15 mod 23 = 2", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(71, 100), (71, 130)], color=SLATE); f.arrow([(269, 100), (269, 130)], color=SLATE)
f.box(60, 210, 220, 44, "Shared secret K = 2\nEve knows 23, 5, 8, 19 only", fill=SAND, stroke=AMBER, size=12, bold=True)
```

```svgfig label="4.1" caption="Two keys instead of one. Bob publishes his public key for anyone to use and keeps his private key to himself. Anyone, including Alice, encrypts with the public key; only Bob's private key opens the message (confidentiality). In the reverse use, Bob signs with his private key and anyone checks the signature with his public key (authentication and non-repudiation). The two keys are mathematically linked, but the private key cannot be worked out from the public one in practice."
f = Fig(580, 230)
f.box(8, 20, 100, 44, "Alice\nplaintext", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(160, 20, 130, 44, "Encrypt with\nBob's PUBLIC key", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(340, 20, 100, 44, "Ciphertext", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(470, 20, 100, 44, "Decrypt with\nBob's PRIVATE\nkey", fill=ROSE, stroke=RED, size=10.5, bold=True)
for a, b in ((108, 160), (290, 340), (440, 470)): f.arrow([(a, 42), (b, 42)], color=SLATE)
f.text(290, 92, "Confidentiality: anyone can send, only Bob can read", size=11.5, color=TEAL, bold=True)
f.box(8, 130, 100, 44, "Bob\nmessage", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(160, 130, 130, 44, "Sign with Bob's\nPRIVATE key", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(340, 130, 100, 44, "Signature", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(470, 130, 100, 44, "Verify with\nBob's PUBLIC\nkey", fill=MINT, stroke=TEAL, size=10.5, bold=True)
for a, b in ((108, 160), (290, 340), (440, 470)): f.arrow([(a, 152), (b, 152)], color=SLATE)
f.text(290, 202, "Authentication: anyone can check, only Bob can sign", size=11.5, color=RED, bold=True)
```

```svgfig label="4.2" caption="RSA with the textbook numbers. Key generation: choose primes p = 61 and q = 53, so n = 3233 and phi(n) = 3120; choose e = 17 (gcd 1 with 3120) and find d = 2753 by the extended Euclidean algorithm. The public key is (3233, 17); the private key is d = 2753 (with p and q destroyed). Encrypting m = 65 gives c = 65 to the power 17 mod 3233 = 2790; decrypting gives 2790 to the power 2753 mod 3233 = 65."
f = Fig(580, 214)
st = [("1  Choose primes", "p = 61, q = 53", BLUE, NAVY), ("2  Modulus", "n = p x q = 3233\nphi = 60 x 52 = 3120", BLUE, NAVY), ("3  Public exponent", "e = 17\n(gcd(17, 3120) = 1)", SAND, AMBER), ("4  Private exponent", "d = 2753\n(17 x 2753 = 1 mod 3120)", ROSE, RED)]
for i, (t, d, fl, c) in enumerate(st):
    x = 8 + i * 144
    f.box(x, 10, 134, 26, t, fill=fl, stroke=c, size=10.5, bold=True)
    f.box(x, 40, 134, 46, d, fill="#ffffff", stroke=c, size=10.5, bold=True)
    if i < 3: f.arrow([(x + 134, 23), (x + 144, 23)], color=SLATE)
f.box(30, 120, 240, 46, "Encrypt  c = m^e mod n\n65^17 mod 3233 = 2790", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(310, 120, 240, 46, "Decrypt  m = c^d mod n\n2790^2753 mod 3233 = 65", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(270, 143), (310, 143)], color=SLATE, label="send c", lpos=(290, 135), lsize=10)
f.text(290, 194, "Public key (3233, 17).  Private key d = 2753.  Security rests on the difficulty of factoring n.", size=10.5, color=NAVY, bold=True)
```

```svgfig label="4.3" caption="Adding points on the elliptic curve y squared = x cubed - 3x + 3 over the real numbers. To add P = (-1, 2.236) and Q = (1, 1), draw the line through them; it meets the curve a third time, and reflecting that third point in the x-axis gives P + Q = (0.382, -1.382). The same chord-and-reflect rule, carried out with arithmetic modulo a prime, defines the group used in ECC. For doubling a point the tangent line replaces the chord."
import math
f = Fig(580, 260)
ax = Axes(f, 30, 14, 300, 232, (-2.6, 2.6), (-3.2, 3.2))
ax.grid(1, 1)
fy = lambda x: math.sqrt(max(0.0, x**3 - 3 * x + 3))
ax.curve(fy, -2.1037, 2.6, color=NAVY)
ax.curve(lambda x: -fy(x), -2.1037, 2.6, color=NAVY)
m = (1 - math.sqrt(5)) / 2
ax.curve(lambda x: math.sqrt(5) + m * (x + 1), -1.9, 2.2, color=AMBER, dash=True)
xr = m * m - 0
xr = m * m - (-1) - 1
yr = math.sqrt(5) + m * (xr + 1)
f.line(ax.X(xr), ax.Y(yr), ax.X(xr), ax.Y(-yr), color=SLATE, sw=1.2, dash=True)
ax.pt(-1, math.sqrt(5), "P", dx=-14, dy=-8, anchor="end")
ax.pt(1, 1, "Q", dx=8, dy=-8)
ax.pt(xr, yr, "-R", dx=10, dy=-6)
ax.pt(xr, -yr, "R = P + Q", dx=10, dy=14, color=TEAL)
f.text(350, 40, "Chord-and-reflect rule", size=12, color=NAVY, bold=True, anchor="start")
f.text(350, 62, "1. Draw the line through P and Q.", size=10.5, color=SLATE, anchor="start")
f.text(350, 80, "2. Find the third point -R on the curve.", size=10.5, color=SLATE, anchor="start")
f.text(350, 98, "3. Reflect it in the x-axis: R = P + Q.", size=10.5, color=SLATE, anchor="start")
f.text(350, 130, "Over the field of 17 elements", size=12, color=TEAL, bold=True, anchor="start")
f.text(350, 150, "y^2 = x^3 + 2x + 2: 19 points,", size=10.5, color=SLATE, anchor="start")
f.text(350, 168, "G = (5, 1), 2G = (6, 3), 3G = (10, 6)", size=10.5, color=SLATE, anchor="start")
f.text(350, 186, "19G = O (the point at infinity).", size=10.5, color=SLATE, anchor="start")
f.text(350, 220, "Hard problem: given G and kG, find k.", size=10.5, color=RED, bold=True, anchor="start")
```

```svgfig label="4.4" caption="Key sizes with the same strength (NIST SP 800-57). For 128-bit security a symmetric key needs 128 bits, RSA needs 3072 bits and an elliptic curve needs only 256 bits. At 256-bit security RSA would need 15360 bits against 512 bits for ECC, which is why phones and smart cards prefer curves. The reason is that the best attacks on RSA and Diffie-Hellman are sub-exponential, while the best attacks on a well-chosen curve are fully exponential."
f = Fig(580, 214)
rows = [("112-bit security", 112, 2048, 224), ("128-bit security", 128, 3072, 256), ("192-bit security", 192, 7680, 384), ("256-bit security", 256, 15360, 512)]
f.text(4, 12, "bits of key (bar length to scale for RSA 15360)", size=9.5, color=SLATE, anchor="start")
for i, (nm, s, r, c) in enumerate(rows):
    y = 24 + i * 46
    f.text(4, y + 6, nm, size=10.5, color=NAVY, bold=True, anchor="start")
    wr = r / 15360 * 330
    f.box(130, y - 4, max(wr, 4), 11, "", fill=ROSE, stroke=RED, sw=1, r=2)
    f.text(136 + wr, y + 5, f"RSA {r}", size=10, color=RED, bold=True, anchor="start")
    f.box(130, y + 9, max(c / 15360 * 330, 4), 11, "", fill=MINT, stroke=TEAL, sw=1, r=2)
    f.text(136 + c / 15360 * 330, y + 18, f"ECC {c}   (AES {s})", size=10, color=TEAL, bold=True, anchor="start")
```

### 4.6.1 Eight applications of public-key cryptography

1. **HTTPS and online banking.** When a browser opens a bank or ConnectIPS site, the server proves its identity with a certificate and the two sides agree a session key with public-key methods (RSA or elliptic-curve Diffie-Hellman). The bulk data are then encrypted with fast AES. The padlock beside the address is the visible result.
2. **Digital signatures.** A signer uses a private key to sign a document, and anybody can verify it with the public key. This proves who signed and that the content was not changed. Nepal's Electronic Transactions Act gives legal standing to digital signatures issued by licensed certifying authorities.
3. **Key exchange for private chats.** Messaging apps use Diffie-Hellman variants so that two phones agree on a fresh key without sending it. Even if the server is hacked later, old conversations stay safe when the keys were temporary. This is called forward secrecy.
4. **Secure email and files.** PGP and S/MIME let a sender encrypt an email with the receiver's public key and sign it with their own private key. A hospital can send a patient report so that only the doctor named can open it. No shared password has to be agreed first.
5. **Software updates.** Phone and computer vendors sign each update with a private key, and the device checks the signature with a built-in public key before installing it. This stops an attacker from sending a fake update with malware. The same idea protects app stores.
6. **Server login with SSH keys.** System administrators log in to servers by proving that they hold a private key instead of typing a password. The server stores only the public key, so a stolen server file does not allow log-in. Cloud teams in Kathmandu use this daily.
7. **Cryptocurrency and blockchain.** A wallet address is derived from a public key, and a transaction is authorised by a signature made with the matching private key (elliptic-curve signatures). Anyone can verify the payment, and nobody can spend without the private key. Losing the key means losing the funds.
8. **Smart cards and national ID.** Chips in bank cards, passports and national ID cards store a private key that never leaves the chip. The chip signs a challenge from a reader to prove that the card is genuine. ECC is favoured here because its small keys fit small chips.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Public and private keys in one worked example. (a) A letterbox: anyone can post a letter through the slot, but only the owner with the key can open the box, which is the public-key idea. (b) With the textbook primes p = 61 and q = 53 the modulus is n = 3233. The public key (e = 17, n) turns the message 65 into the ciphertext 2790, and only the private exponent d = 2753 turns it back, all computed with modular exponentiation. The security rests on factoring: trial division on products of two primes of 8, 12, 16 and 20 bits was timed in steps, and every extra 4 bits multiplies the work by about 16 (the 20-bit case already needs 524291 steps). For a 2048-bit modulus the same method would need about 10^308 steps, or 10^299 seconds at a billion steps a second, which is why real RSA keys are that long. The toy key is for learning only."
@ photo id="bcacrypt/mailbox" cap="A letterbox: anyone posts, only the owner opens"
fit 1.2
focus 0.5 0.5
@ svg cap="Toy RSA and the cost of factoring n"
import math
p, q, e = 61, 53, 17
n = p * q
phi = (p - 1) * (q - 1)
dd = pow(e, -1, phi)
m = 65
c = pow(m, e, n)
assert (n, dd, c) == (3233, 2753, 2790) and pow(c, dd, n) == m
def spf_steps(nn):
    s = 0
    k = 3
    while nn % k:
        k += 2
        s += 1
    return s + 1
def nextprime(x):
    x += 1 if x % 2 == 0 else 2
    while any(x % k == 0 for k in range(3, math.isqrt(x) + 1, 2)):
        x += 2
    return x
rows = []
for bits in (8, 12, 16, 20):
    pp = nextprime(2 ** bits)
    qq = nextprime(pp + 1000)
    st = spf_steps(pp * qq)
    rows.append((bits, st))
assert rows[0][1] < rows[1][1] < rows[2][1] < rows[3][1]
log2048 = 1022 * math.log10(2)
secs = log2048 - 9
facts = dict(n=n, d=dd, c=c, lg=round(log2048), sec=round(secs), s20=rows[3][1])
f = Fig(300, 236)
f.text(150, 12, "p=61, q=53, e=17: n=%d, d=%d" % (n, dd), size=10.5, color=NAVY, bold=True)
f.box(6, 24, 70, 24, "m = 65", fill=BLUE, stroke=NAVY, size=11, bold=True, r=4, sw=1)
f.box(115, 24, 70, 24, "c = %d" % c, fill="#fde68a", stroke=AMBER, size=11, bold=True, r=4, sw=1)
f.box(224, 24, 70, 24, "m = %d" % pow(c, dd, n), fill="#bbf7d0", stroke=TEAL, size=11, bold=True, r=4, sw=1)
f.arrow([(76, 36), (115, 36)], color=SLATE)
f.text(75, 62, "encrypt: m^17 mod n", size=10.5, color=SLATE)
f.arrow([(185, 36), (224, 36)], color=SLATE)
f.text(225, 62, "decrypt: c^d mod n", size=10.5, color=SLATE)
f.text(150, 76, "trial-division steps to factor n = p x q", size=10.5, color=NAVY, bold=True)
import math as _m
for i, (b, st) in enumerate(rows):
    y = 86 + i * 24
    f.text(8, y + 8, "%d-bit primes" % b, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    w = 14 * _m.log10(st)
    f.box(96, y, w, 18, "", fill="#fecaca", stroke=SLATE, r=3, sw=1)
    f.text(102 + w, y + 9, format(st, ","), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 198, "each +4 bits: about 16 times the work", size=10.5, color=RED, bold=True)
f.text(150, 214, "2048-bit n: about 10^%d steps" % round(log2048), size=10.5, color=RED, bold=True)
f.text(150, 230, "= 10^%d s at 10^9 steps/s" % round(secs), size=10.5, color=TEAL, bold=True)
```

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). With p = 3 and q = 11, generate RSA keys with e = 7 and encrypt and decrypt the message m = 4.**

*Introduction.* RSA is a public-key system whose security depends on the difficulty of factoring the product of two large primes (section 4.2, Figure 4.2).

1. **Modulus.** n = p x q = 3 x 11 = 33.
2. **Totient.** phi(n) = (3 - 1)(11 - 1) = 20.
3. **Public exponent.** e = 7 is valid because gcd(7, 20) = 1.
4. **Private exponent.** d is the inverse of 7 modulo 20. Since 7 x 3 = 21 = 1 (mod 20), d = 3.
5. **Encryption.** c = m to the power e mod n = 4 to the power 7 mod 33 = 16384 mod 33 = **16**, because 33 x 496 = 16368.
6. **Decryption.** m = c to the power d mod n = 16 to the power 3 mod 33 = 4096 mod 33 = **4**, because 33 x 124 = 4092. The message is recovered.

| Item | Value |
|---|---|
| Public key (n, e) | (33, 7) |
| Private key d | 3 |
| Ciphertext of 4 | 16 |

These numbers are far too small to be secure; real keys use primes of 1024 bits or more.

**Q2 (5 marks). Explain Diffie-Hellman key exchange with an example. Why is it vulnerable to a man-in-the-middle attack?**

*Introduction.* Diffie-Hellman (1976) lets two parties agree on a shared secret over a public channel (section 4.3, Plate 4.1).

1. **Public values.** A prime p = 23 and a generator g = 5 are agreed openly.
2. **Private choices.** Alice picks a = 6, Bob picks b = 15, and each keeps their number secret.
3. **Exchange.** Alice sends A = 5 to the power 6 mod 23 = 8. Bob sends B = 5 to the power 15 mod 23 = 19.
4. **Shared key.** Alice computes B to the power a = 19 to the power 6 mod 23 = 2. Bob computes A to the power b = 8 to the power 15 mod 23 = 2. Both obtain K = 2.
5. **Security.** An eavesdropper sees p, g, A and B but must solve the discrete logarithm problem to find a or b, which is infeasible for large p.
6. **Weakness.** The exchange does not check who is at the other end. Mallory can run one exchange with Alice and another with Bob, and read and forward all messages. The defence is to authenticate the exchanged values, using digital signatures and certificates, as TLS does.

**Q3 (5 marks). Explain elliptic-curve cryptography and point addition with an example.**

*Introduction.* ECC uses the group of points on a curve y squared = x cubed + ax + b over a finite field. It gives the same security as RSA with much smaller keys (section 4.4, Figure 4.3).

1. **Curve and group.** Points (x, y) on the curve, plus a point at infinity O, form a group under a chord-and-tangent addition rule.
2. **Addition formulas.** For P not equal to Q the slope is (y2 - y1)/(x2 - x1); for doubling it is (3 x1 squared + a)/(2 y1). Then x3 = slope squared - x1 - x2 and y3 = slope (x1 - x3) - y1, all modulo p.
3. **Example.** On y squared = x cubed + 2x + 2 mod 17 with G = (5, 1): slope = (3 x 25 + 2)/2 = 77/2 = 9 x 9 = 81 = 13 (mod 17). Then x3 = 169 - 10 = 159 = 6, y3 = 13(5 - 6) - 1 = -14 = 3. So 2G = (6, 3). Continuing gives 3G = (10, 6) and 19G = O, so G has order 19.
4. **Hard problem.** Given G and kG, finding k (the elliptic-curve discrete logarithm) has no sub-exponential algorithm, so a 256-bit curve matches 3072-bit RSA.
5. **Use.** ECDH key exchange and ECDSA signatures in TLS, Bitcoin and smart cards.

**Q4 (10 marks). Describe the RSA algorithm: key generation, encryption and decryption, with a worked example, the reason that it works, the attacks on it and a comparison with Diffie-Hellman and ECC.**

*Introduction.* RSA (Rivest, Shamir and Adleman, 1977) is the most widely taught public-key system. It provides encryption and signatures, and its security rests on the factoring problem: multiplying two primes is easy, recovering them from the product is hard (section 4.2, Figure 4.2).

1. **Key generation.** Choose two large random primes p and q (Miller-Rabin tested). Compute n = pq and phi(n) = (p - 1)(q - 1). Choose e with gcd(e, phi) = 1 (commonly 65537). Compute d with ed = 1 (mod phi) by the extended Euclidean algorithm. Publish (n, e); keep d.
2. **Encryption and decryption.** c = m to the power e mod n, then m = c to the power d mod n.
3. **Worked example.** p = 61, q = 53 give n = 3233 and phi = 3120. With e = 17 the private exponent is d = 2753. For m = 65: c = 65 to the power 17 mod 3233 = 2790, and 2790 to the power 2753 mod 3233 = 65.
4. **Why it works.** ed = 1 + k phi(n), so (m to the power e) to the power d = m times (m to the power phi) to the power k, which is m (mod n) by Euler's theorem (the case gcd(m, n) not 1 follows by the Chinese remainder theorem).
5. **Attacks.** Factoring n (use at least 2048 bits); small exponent and no padding (use OAEP padding); timing and side-channel attacks (use blinding and constant-time code); reusing primes across keys (a gcd test of two public keys reveals them).
6. **Practical use.** RSA encrypts only short data, so it protects an AES session key; it also signs hashes.
7. **Speed.** Decryption with the Chinese remainder theorem is about four times faster than a direct power.

| Point | RSA | Diffie-Hellman | ECC |
|---|---|---|---|
| Purpose | Encryption, signature | Key agreement | Key agreement, signature |
| Hard problem | Factoring | Discrete logarithm | Elliptic-curve discrete log |
| Key for 128-bit security | 3072 bits | 3072 bits | 256 bits |
| Speed | Slow private operation | Moderate | Fast |
| Typical use | Certificates, signatures | TLS key exchange | Phones, smart cards, TLS |

*Conclusion.* RSA made secure communication between strangers practical. It is now mostly used for signatures and key transport, with elliptic curves taking over where small keys and speed matter, and every system must add padding and authentication to be safe.
