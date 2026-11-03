---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 2
title: Number Theory for Cryptography
hours: 7
area: BCA 353 · Cryptography and Network Security · Unit 2
---

Modern public-key cryptography is built on questions about whole numbers that look innocent: what is the remainder when you divide, which numbers have inverses, how do you compute 7⁵⁶⁰ mod 561 without a trillion-digit intermediate result? This unit collects the toolkit used by RSA, Diffie–Hellman and elliptic-curve cryptography in Units 4 and 5: modular arithmetic, the Euclidean and extended Euclidean algorithms, Euler's totient, Fermat's and Euler's theorems, the Chinese Remainder Theorem, fast exponentiation and primality testing. Every number below comes from an executed program and was cross-checked with sympy or Python's built-in modular functions.

::: key What this unit gives you
- Modular arithmetic, congruences, inverses; gcd by Euclid and the extended Euclidean algorithm (with a table).
- Euler's φ, Fermat's little theorem and Euler's theorem; the Chinese Remainder Theorem.
- Square-and-multiply; Miller–Rabin primality testing (and why the Fermat test is fooled by 561).
- Primitive roots and the discrete logarithm.
:::

## 2.1 Modular arithmetic

**a ≡ b (mod n)** means n divides (a − b); **a mod n** is the remainder r with 0 ≤ r < n. Congruence behaves like equality for addition, subtraction and multiplication: (a ± b) mod n = ((a mod n) ± (b mod n)) mod n and (a·b) mod n = ((a mod n)(b mod n)) mod n. The integers mod n, written **Zₙ**, form a clock arithmetic; division is more delicate. The **multiplicative inverse** of a is a number x with a·x ≡ 1 (mod n), and it exists **if and only if gcd(a, n) = 1**. For example, 7 has the inverse 15 modulo 26 because 7 × 15 = 105 = 4 × 26 + 1; this is why the affine cipher needs a coprime with 26. When n is a prime p every non-zero element has an inverse, and **Z_p** is a *field*.

## 2.2 The Euclidean and extended Euclidean algorithms

**Euclid's algorithm** finds gcd(a, b) by repeating gcd(a, b) = gcd(b, a mod b) until the remainder is 0: gcd(240, 46): 240 = 5·46 + 10; 46 = 4·10 + 6; 10 = 1·6 + 4; 6 = 1·4 + 2; 4 = 2·2 + 0, so the gcd is **2**. The **extended** algorithm also finds integers s, t with **a·s + b·t = gcd(a, b)** (Bézout's identity), by tracking the coefficients alongside the remainders; when gcd = 1 and b = n, then t is irrelevant and **s is the inverse of a mod n**. The table below (columns: quotient q, remainder r, and the coefficients s, t such that 240·s + 46·t = r) is printed by the program after the next paragraph.

The same program computes the totient, the inverse of 7 mod 26, the Chinese Remainder solution, and fast exponentiation. It first defines the extended Euclid as a loop that prints each row, then the **square-and-multiply** method (process the exponent's bits, squaring each time and multiplying when the bit is 1, so 560 needs about 10 squarings instead of 560 multiplications), then CRT.

```python
import sympy

def egcd(a, b):
    r0, r1, s0, s1, t0, t1 = a, b, 1, 0, 0, 1
    print("start        r=%d s=1 t=0 | r=%d s=0 t=1" % (a, b))
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
        print("q=%d r=%d s=%d t=%d" % (q, r1, s1, t1))
    return r0, s0, t0

g, s, t = egcd(240, 46)
print("gcd =", g, " 240*(%d) + 46*(%d) = %d" % (s, t, 240 * s + 46 * t))
print("inverse of 7 mod 26 =", egcd(7, 26)[1] % 26)

def power(base, exp, mod):
    result, base = 1, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result

print("7^560 mod 561 =", power(7, 560, 561), " 3^200 mod 13 =", power(3, 200, 13))
print("phi(26) =", sympy.totient(26), " phi(36) =", sympy.totient(36), " phi(561) =", sympy.totient(561))

def crt(rems, mods):
    M = 1
    for m in mods:
        M *= m
    x = 0
    for r, m in zip(rems, mods):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M, M

print("CRT x = 2 mod 3, 3 mod 5, 2 mod 7 ->", crt([2, 3, 2], [3, 5, 7]))
```
```output
start        r=240 s=1 t=0 | r=46 s=0 t=1
q=5 r=10 s=1 t=-5
q=4 r=6 s=-4 t=21
q=1 r=4 s=5 t=-26
q=1 r=2 s=-9 t=47
q=2 r=0 s=23 t=-120
gcd = 2  240*(-9) + 46*(47) = 2
start        r=7 s=1 t=0 | r=26 s=0 t=1
q=0 r=7 s=1 t=0
q=3 r=5 s=-3 t=1
q=1 r=2 s=4 t=-1
q=2 r=1 s=-11 t=3
q=2 r=0 s=26 t=-7
inverse of 7 mod 26 = 15
7^560 mod 561 = 1  3^200 mod 13 = 9
phi(26) = 12  phi(36) = 12  phi(561) = 320
CRT x = 2 mod 3, 3 mod 5, 2 mod 7 -> (23, 105)
```
Reading the output: the table's last row with remainder 0 is not used; the previous remainder, **2**, is the gcd, and its coefficients satisfy 240·(−9) + 46·47 = −2160 + 2162 = 2. The inverse of 7 modulo 26 is 15. The totients φ(26) = 12, φ(36) = 12 and φ(561) = 320 follow from the formula below. The Chinese Remainder solution is **23** modulo 105 (Sun Tzu's classical puzzle: a number leaving 2, 3, 2 when divided by 3, 5, 7).

## 2.3 Euler's totient, Fermat and Euler

**Euler's totient φ(n)** counts the integers from 1 to n that are coprime with n. Rules: for a prime p, **φ(p) = p − 1**; for a prime power φ(pᵏ) = pᵏ − pᵏ⁻¹; and it is **multiplicative** for coprime arguments: φ(mn) = φ(m)φ(n). So φ(26) = φ(2)φ(13) = 1 × 12 = 12; φ(36) = φ(4)φ(9) = 2 × 6 = 12; and for **RSA** with n = pq, **φ(n) = (p − 1)(q − 1)**; φ(561) = φ(3)φ(11)φ(17) = 2 × 10 × 16 = 320.

**Fermat's little theorem:** if p is prime and p ∤ a, then **a^(p−1) ≡ 1 (mod p)**. Hence 3²⁰⁰ mod 13: 3¹² ≡ 1 so 3²⁰⁰ = 3^(12·16 + 8) ≡ 3⁸ = 6561 = 504 × 13 + 9, which is **9**. **Euler's theorem** generalises it: if gcd(a, n) = 1 then **a^φ(n) ≡ 1 (mod n)**. RSA decryption works because of this theorem (Unit 4): the exponent is reduced modulo φ(n).

## 2.4 Primality testing

Cryptography needs large primes (hundreds of digits), found by choosing random odd numbers and **testing**. A tempting test is Fermat's: if aⁿ⁻¹ mod n ≠ 1 then n is composite. But some composites, the **Carmichael numbers**, satisfy the congruence for *every* a coprime to them: 561 = 3 × 11 × 17 is the smallest, and the program above shows 7⁵⁶⁰ ≡ 1 (mod 561) even though 561 is composite. The **Miller–Rabin** test is stronger. Write n − 1 = 2ˢ·d with d odd; for a base a compute x = aᵈ mod n; if x is 1 or n − 1 the base gives no information (n is a "probable prime" for that base); otherwise square x up to s − 1 times and look for n − 1. If never, a is a **witness** that n is composite. For a composite n at least 3/4 of bases are witnesses, so k random bases leave an error probability at most 4⁻ᵏ; 40 rounds give less than 2⁻⁸⁰.

```python
import sympy

def witness(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return False
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False
    return True

print("561 = 2^%d * %d" % (4, 35), " is 2 a witness for 561?", witness(561, 2))
print("is 2 a witness for 569 (prime)?", witness(569, 2), " 3?", witness(569, 3))
print("pow(2, 35, 561) =", pow(2, 35, 561))
print("sympy.isprime(561), isprime(569):", sympy.isprime(561), sympy.isprime(569))
```
```output
561 = 2^4 * 35  is 2 a witness for 561? True
is 2 a witness for 569 (prime)? False  3? False
pow(2, 35, 561) = 263
sympy.isprime(561), isprime(569): False True
```
For 561 the base 2 is a witness (x = 2³⁵ mod 561 = 263, then 166, 67, 1, never 560), so Miller–Rabin correctly reports composite where the Fermat test was fooled. The prime 569 has no witnesses, as it must.

## 2.5 Primitive roots and the discrete logarithm

For a prime p, the powers of a **primitive root** (generator) g produce *every* non-zero residue 1, …, p − 1. Modulo 23, g = 5 is a primitive root: its powers 5¹ … 5²² cycle through all 22 non-zero values. The **discrete logarithm problem**: given g, p and y = gˣ mod p, find x. Computing y from x is fast (square-and-multiply); finding x from y has no known efficient algorithm for large p (the best known methods are sub-exponential). This *one-way* asymmetry is the foundation of Diffie–Hellman and ElGamal in Unit 4.

```python
import sympy

print("order of 5 mod 23:", sympy.n_order(5, 23), " primitive roots of 23:", sympy.primitive_root(23), sorted(
    g for g in range(2, 23) if sympy.n_order(g, 23) == 22))
print("powers of 5 mod 23:", [pow(5, k, 23) for k in range(1, 23)])
print("discrete log of 8 base 5 mod 23:", next(x for x in range(22) if pow(5, x, 23) == 8))
```
```output
order of 5 mod 23: 22  primitive roots of 23: 5 [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
powers of 5 mod 23: [5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, 18, 21, 13, 19, 3, 15, 6, 7, 12, 14, 1]
discrete log of 8 base 5 mod 23: 6
```
The smallest primitive root of 23 is 5, and the printed list shows all 22 distinct values. The discrete log of 8 base 5 is 6 (5⁶ = 15625 = 679 × 23 + 8), found here by **brute force**, which takes up to p − 1 steps: for a 2048-bit prime that is impossible.

## 2.6 Why the arithmetic is feasible and the inverse is hard

| Operation | Cost | Used in |
|---|---|---|
| Modular multiplication of k-bit numbers | about k² bit operations | Everything |
| Modular exponentiation (square-and-multiply) | about k multiplications for a k-bit exponent | RSA, DH, ElGamal |
| Extended Euclid / modular inverse | about k² | RSA key generation |
| Primality test (Miller–Rabin) | k rounds of exponentiation | Key generation |
| Factoring n = pq | sub-exponential, infeasible at 2048 bits | Security of RSA |
| Discrete logarithm | sub-exponential, infeasible at 2048 bits | Security of DH, ElGamal |

## 2.7 Seeing the arithmetic: portraits, clocks, cycles and chains

Number theory in cryptography is about a few small ideas: clock arithmetic, the Euclidean chain, cycles of powers, the sieve-like tests for primes and the Chinese remainder theorem. The plate introduces three mathematicians whose theorems are used in every RSA key, and the figures draw each idea on small numbers that can be checked by hand.

```photogrid label="2.1" cols="3" ratio="0.85" caption="Three names behind the theorems of this unit. (a) Leonhard Euler (1707-1783), whose totient function and generalisation of Fermat's theorem (a to the power phi(n) is 1 mod n) make RSA decryption work. (b) Pierre de Fermat (1607-1665), who stated that a to the power p-1 is 1 mod p for a prime p, the basis of the Fermat primality test. (c) Carl Friedrich Gauss (1777-1855), who introduced the congruence notation a = b (mod n) in his Disquisitiones Arithmeticae of 1801 and proved results on primitive roots."
@ photo id="crypto353/euler" cap="Leonhard Euler"
fit 0.85
focus 0.5 0.62
@ photo id="crypto353/fermat" cap="Pierre de Fermat"
fit 0.85
focus 0.5 0.62
@ photo id="crypto353/gauss" cap="Carl Friedrich Gauss"
fit 0.85
focus 0.5 0.62
```

```svgfig label="2.1" caption="Clock arithmetic modulo 7. The numbers 0 to 6 sit on a clock face and adding wraps around: 5 + 4 = 9, which is 2 on this clock, so 5 + 4 = 2 (mod 7). Multiplication wraps too: 3 times 5 = 15 = 1 (mod 7), so 5 is the multiplicative inverse of 3 and 'dividing by 3' means 'multiplying by 5'. Every non-zero number has an inverse here because 7 is prime; modulo 6 the number 3 has none."
import math
f = Fig(580, 230)
cx, cy, R = 120, 115, 80
for k in range(7):
    a = -math.pi / 2 + k * 2 * math.pi / 7
    x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    f.circle(x, y, 17, fill=(SAND if k in (2, 5, 3) else BLUE), stroke=(AMBER if k in (2, 5, 3) else NAVY), label=str(k), size=13)
f.text(cx, cy - 4, "mod 7", size=13, color=NAVY, bold=True)
f.text(cx, cy + 14, "clock", size=11, color=SLATE)
f.box(260, 20, 300, 58, "Addition wraps\n5 + 4 = 9 = 2 (mod 7)", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(260, 90, 300, 58, "Multiplication wraps\n3 x 5 = 15 = 1 (mod 7)", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(260, 160, 300, 58, "Inverse exists when gcd(a, n) = 1\n3 has no inverse mod 6 (gcd = 3)", fill=ROSE, stroke=RED, size=12, bold=True)
```

```svgfig label="2.2" caption="The Euclidean chain for gcd(1071, 462). Each step replaces the pair (a, b) by (b, a mod b) until the remainder is 0; the last non-zero remainder, 21, is the gcd. Working back up the chain gives the Bezout identity 21 = 7 x 462 - 3 x 1071, which is how the extended algorithm finds modular inverses (check: 3234 - 3213 = 21)."
f = Fig(580, 210)
rows = [("1071 = 2 x 462 + 147", BLUE, NAVY), ("462 = 3 x 147 + 21", BLUE, NAVY), ("147 = 7 x 21 + 0", MINT, TEAL)]
for i, (t, fl, st) in enumerate(rows):
    f.box(10, 14 + i * 46, 250, 36, t, fill=fl, stroke=st, size=12, bold=True)
    if i < 2: f.arrow([(135, 50 + i * 46), (135, 60 + i * 46)], color=SLATE)
f.text(135, 160, "last non-zero remainder: gcd = 21", size=12, color=TEAL, bold=True)
f.text(300, 30, "Back-substitute:", size=12, color=NAVY, bold=True, anchor="start")
f.box(300, 42, 270, 30, "21 = 462 - 3 x 147", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(300, 82, 270, 30, "21 = 462 - 3 x (1071 - 2 x 462)", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(300, 122, 270, 30, "21 = 7 x 462 - 3 x 1071", fill=MINT, stroke=TEAL, size=12, bold=True)
f.text(435, 178, "x = 7, y = -3 solve 1071y + 462x = 21", size=10.5, color=SLATE)
```

```svgfig label="2.3" caption="Cycles of powers modulo 7. The powers of 3 visit all six non-zero residues (3, 2, 6, 4, 5, 1) before returning, so 3 is a primitive root of 7 and the order of 3 is 6 = phi(7). The powers of 2 visit only 2, 4, 1, a cycle of length 3, so 2 has order 3, which divides 6 as Euler's theorem requires. Discrete logarithms ask 'which exponent leads from 1 to this value?', easy here and very hard for numbers of 2048 bits."
import math
f = Fig(580, 220)
def ring(cx, cy, R, vals, color, fill, title):
    n = len(vals)
    pts = []
    for k, v in enumerate(vals):
        a = -math.pi / 2 + k * 2 * math.pi / n
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for k in range(n):
        p, q = pts[k], pts[(k + 1) % n]
        f.line(p[0], p[1], q[0], q[1], color=color, sw=1.4)
    for k, v in enumerate(vals):
        f.circle(pts[k][0], pts[k][1], 15, fill=fill, stroke=color, label=str(v), size=12)
    f.text(cx, cy - 4, title, size=12, color=color, bold=True)
ring(150, 112, 75, [1, 3, 2, 6, 4, 5], NAVY, BLUE, "powers\nof 3")
ring(440, 112, 70, [1, 2, 4], TEAL, MINT, "powers\nof 2")
f.text(150, 210, "3^0..3^5 = 1, 3, 2, 6, 4, 5: order 6", size=11, color=NAVY, bold=True)
f.text(440, 210, "2^0..2^2 = 1, 2, 4: order 3", size=11, color=TEAL, bold=True)
```

```svgfig label="2.4" caption="The Miller-Rabin test and a trace for n = 561 = 3 x 11 x 17. Write n - 1 = 2 to the power s times d (560 = 16 x 35), pick a base a and compute x = a^d mod n, then square s - 1 times. If x is 1 at the start or n - 1 at any point the test says 'probably prime'; otherwise n is certainly composite. For a = 2 the values are 263, 166, 67, 1: the sequence reaches 1 from 67, not from 560, and 67 is a non-trivial square root of 1, so 561 is composite. The plain Fermat test cannot tell, because every base coprime to 561 passes it."
f = Fig(580, 230)
f.box(10, 10, 170, 40, "n - 1 = 2^s x d\npick base a", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 70, 170, 40, "x = a^d mod n", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 130, 170, 40, "x = 1 or x = n - 1 ?", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(10, 188, 170, 36, "square x up to s - 1 times", fill=BLUE, stroke=NAVY, size=11, bold=True)
for y in (50, 110, 170): f.arrow([(95, y), (95, y + 20 if y < 170 else y + 18)], color=SLATE)
f.box(215, 120, 120, 40, "yes: probably\nprime", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(180, 150), (215, 140)], color=TEAL)
f.box(215, 188, 120, 36, "hits n - 1: probably\nprime", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(180, 206), (215, 206)], color=TEAL)
f.box(215, 66, 120, 40, "never hits n - 1:\ncomposite", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(375, 24, "Trace: n = 561, a = 2, d = 35, s = 4", size=11.5, color=NAVY, bold=True, anchor="start")
vals = [("2^35", "263"), ("squared", "166"), ("squared", "67"), ("squared", "1")]
for i, (a, b) in enumerate(vals):
    x = 375 + i * 50
    f.box(x, 40, 44, 34, b, fill=(ROSE if b == "1" else BLUE), stroke=(RED if b == "1" else NAVY), size=12, bold=True)
    f.text(x + 22, 88, a, size=9.5, color=SLATE)
f.text(375, 118, "67 x 67 = 4489 = 8 x 561 + 1", size=11, color=RED, bold=True, anchor="start")
f.text(375, 138, "67 is a square root of 1 that is not", size=10.5, color=SLATE, anchor="start")
f.text(375, 154, "1 or 560, so 561 cannot be prime.", size=10.5, color=SLATE, anchor="start")
f.text(375, 184, "Fermat test with base 2 says:", size=10.5, color=SLATE, anchor="start")
f.text(375, 200, "2^560 = 1 mod 561 (fooled)", size=11, color=AMBER, bold=True, anchor="start")
```

```svgfig label="2.5" caption="The Chinese remainder theorem on the classic puzzle x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7). Each row marks the numbers 0 to 40 that fit one congruence; the marks line up in a single column at 23, and the next solution is 23 + 105 = 128 because 3 x 5 x 7 = 105. RSA decryption uses the same idea to work modulo p and modulo q separately and then combine the two answers, which is about four times faster than working modulo n."
f = Fig(580, 200)
rows = [("x = 2 (mod 3)", 3, 2, BLUE, NAVY), ("x = 3 (mod 5)", 5, 3, SAND, AMBER), ("x = 2 (mod 7)", 7, 2, MINT, TEAL)]
for r, (lab, m, a, fl, st) in enumerate(rows):
    y = 30 + r * 46
    f.text(4, y + 4, lab, size=10.5, color=st, bold=True, anchor="start")
    for x in range(0, 41):
        px = 120 + x * 11
        if x % m == a:
            f.circle(px, y, 5, fill=(RED if x == 23 else st), stroke=(RED if x == 23 else st), sw=1)
f.line(116, 160, 564, 160, color=SLATE, sw=1)
for x in range(0, 41, 5):
    f.text(120 + x * 11, 176, str(x), size=9.5, color=SLATE)
f.line(120 + 23 * 11, 20, 120 + 23 * 11, 156, color=RED, sw=1.2, dash=True)
f.text(120 + 23 * 11 + 6, 14, "23: the common solution", size=10.5, color=RED, bold=True, anchor="start")
```

### 2.7.1 Eight uses of number theory in cryptography

1. **Modular arithmetic keeps numbers small.** Every operation is followed by a remainder, so a 2048-bit calculation never grows beyond 2048 bits. Without this wrap-around, the intermediate results of a modular power would need more memory than any computer has. Clock arithmetic is therefore the working floor of all public-key systems.
2. **The gcd test checks that an inverse exists.** Before a Hill key, an affine key or an RSA exponent is accepted, we test that gcd is 1. The Euclidean algorithm does this in a few hundred steps even for huge numbers. Saying 'the key is valid' is, in many ciphers, the same as saying 'the gcd is 1'.
3. **The extended Euclidean algorithm finds private keys.** RSA computes the private exponent d as the inverse of e modulo phi(n). The extended algorithm gives it directly, as in 17 times 2753 = 1 (mod 3120). It needs no guessing or searching.
4. **Euler's theorem makes decryption work.** Because a to the power phi(n) is 1 modulo n, raising to the power e and then d returns the original message when e times d is 1 modulo phi(n). This is the whole mathematical proof that RSA is correct. It was proved two centuries before computers.
5. **Fermat's little theorem gives a quick primality filter.** If a to the power n - 1 is not 1 modulo n, then n is certainly not prime. This lets a program discard most composite candidates cheaply when it generates RSA primes. The stronger Miller-Rabin test then removes the rare liars such as 561.
6. **Primality testing makes key generation practical.** Primes near 2 to the power 1024 are plentiful: about one number in 710 is prime, so a program needs on average a few hundred random tries. Miller-Rabin with 40 random bases makes the chance of error negligible. This is why every phone can create its own keys in a moment.
7. **Primitive roots and discrete logarithms support Diffie-Hellman and ElGamal.** Powers of a primitive root run through all residues, so g to the power x mod p looks random. Going from x to g to the power x is fast, while recovering x is believed to be hard. This one-way property is used when two apps agree on a secret over an open network.
8. **The Chinese remainder theorem speeds up and protects computation.** RSA decryption can be done modulo p and modulo q separately and recombined, which is about four times faster, a real saving on a bank's server handling thousands of requests. The same theorem also appears in secret sharing and in the design of fast arithmetic hardware.

## Chapter summary

- a mod n arithmetic is closed under + − ×; an inverse exists iff gcd(a, n) = 1; the extended Euclidean algorithm finds it (240·(−9) + 46·47 = 2; 7⁻¹ ≡ 15 mod 26).
- φ(p) = p − 1, φ(pq) = (p − 1)(q − 1); Fermat a^(p−1) ≡ 1; Euler a^φ(n) ≡ 1; CRT combines congruences (x ≡ 2, 3, 2 mod 3, 5, 7 gives 23).
- Square-and-multiply makes huge powers cheap; Miller–Rabin finds primes where the Fermat test is fooled by Carmichael numbers such as 561.
- Primitive roots and the hard discrete log underlie Diffie–Hellman and ElGamal.

## Practice

1. Compute 38 mod 7 and −5 mod 7.
2. Find gcd(252, 105) by Euclid's algorithm.
3. Use the extended algorithm to find the inverse of 17 mod 43.
4. Compute φ(35), φ(49) and φ(100).
5. Compute 2¹⁰⁰ mod 7 using Fermat's theorem.
6. Solve x ≡ 1 (mod 4), x ≡ 2 (mod 9) with the Chinese Remainder Theorem.
7. Compute 5¹³ mod 11 by square-and-multiply.
8. Explain why 561 fools the Fermat test.
9. State Euler's theorem and use it to compute 3⁴⁰ mod 10.
10. Why is the discrete logarithm problem the basis for key exchange?

::: note Answers and worked solutions
**1.** 38 = 5·7 + 3, so **3**; −5 + 7 = **2**.
**2.** 252 = 2·105 + 42; 105 = 2·42 + 21; 42 = 2·21 + 0, so gcd = **21**.
**3.** 43 = 2·17 + 9; 17 = 1·9 + 8; 9 = 1·8 + 1. Back-substitute: 1 = 9 − 8 = 9 − (17 − 9) = 2·9 − 17 = 2(43 − 2·17) − 17 = 2·43 − 5·17. So 17·(−5) ≡ 1, and the inverse is −5 mod 43 = **38** (check: 17 × 38 = 646 = 15·43 + 1).
**4.** φ(35) = 4 × 6 = **24**; φ(49) = 49 − 7 = **42**; φ(100) = φ(4)φ(25) = 2 × 20 = **40**.
**5.** 2⁶ ≡ 1 (mod 7); 100 = 6·16 + 4, so 2¹⁰⁰ ≡ 2⁴ = 16 ≡ **2**.
**6.** x = 1 + 4k; 1 + 4k ≡ 2 (mod 9) → 4k ≡ 1 → k ≡ 7 (since 4 × 7 = 28 ≡ 1); x = 1 + 28 = **29** (mod 36). Check: 29 mod 4 = 1, 29 mod 9 = 2.
**7.** 13 = 1101₂. 5¹ = 5; 5² = 25 ≡ 3; 5⁴ ≡ 9; 5⁸ ≡ 81 ≡ 4. 5¹³ = 5⁸·5⁴·5¹ ≡ 4 · 9 · 5 = 180 ≡ 180 − 176 = **4**.
**8.** 561 is a Carmichael number: aⁿ⁻¹ ≡ 1 (mod 561) for every a coprime with 561, although 561 = 3 × 11 × 17.
**9.** If gcd(a, n) = 1 then a^φ(n) ≡ 1 (mod n). φ(10) = 4, so 3⁴ ≡ 1 and 3⁴⁰ = (3⁴)¹⁰ ≡ **1** (mod 10).
**10.** Computing gˣ mod p is fast but recovering x from the result is infeasible for large p, so two parties can publish gˣ values and combine them privately.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Use the extended Euclidean algorithm to find the inverse of 17 modulo 3120 and state where this is used.**

*Introduction.* A number a has an inverse modulo n only if gcd(a, n) = 1, and the extended Euclidean algorithm finds both the gcd and the inverse (section 2.2, Figure 2.2).

1. **Divide.** 3120 = 183 x 17 + 9, then 17 = 1 x 9 + 8, then 9 = 1 x 8 + 1, then 8 = 8 x 1 + 0. The last non-zero remainder is 1, so gcd(17, 3120) = 1 and an inverse exists.
2. **Back-substitute.** 1 = 9 - 8 = 9 - (17 - 9) = 2 x 9 - 17 = 2 x (3120 - 183 x 17) - 17 = 2 x 3120 - 367 x 17.
3. **Read off the inverse.** The coefficient of 17 is -367. Add 3120 to make it positive: -367 + 3120 = 2753.
4. **Check.** 17 x 2753 = 46,801 = 15 x 3120 + 1, so 17 x 2753 = 1 (mod 3120).
5. **Use.** In RSA with p = 61 and q = 53 we have n = 3233 and phi(n) = 3120. With public exponent e = 17, the private exponent is d = 2753, exactly the value found above.

| Step | Quotient | Remainder |
|---|---|---|
| 3120 / 17 | 183 | 9 |
| 17 / 9 | 1 | 8 |
| 9 / 8 | 1 | 1 |
| 8 / 1 | 8 | 0 |

**Q2 (5 marks). State Fermat's little theorem and Euler's theorem with examples and show how they simplify large powers.**

*Introduction.* Both theorems say that powers of a number repeat in a cycle, so a huge exponent can be reduced before computing (section 2.3, Figure 2.3).

1. **Fermat.** If p is prime and p does not divide a, then a to the power p - 1 = 1 (mod p). Example: 3 to the power 6 = 729 = 104 x 7 + 1, so it is 1 modulo 7.
2. **Euler.** If gcd(a, n) = 1, then a to the power phi(n) = 1 (mod n), where phi(n) counts the numbers up to n that are coprime to n. For n = 10, phi = 4 (the numbers 1, 3, 7, 9) and 3 to the power 4 = 81 = 1 (mod 10).
3. **Reducing a power.** To find 3 to the power 100 mod 7, note that 100 mod 6 = 4, so the answer is 3 to the power 4 = 81 = **4** (mod 7).
4. **Relation.** Fermat's theorem is the case n = p of Euler's, because phi(p) = p - 1.
5. **Use.** The same reduction (exponent modulo phi(n)) is the reason that RSA decryption returns the message.

**Q3 (10 marks). Explain primality testing for cryptography. Describe the Fermat and Miller-Rabin tests with a worked example, and explain why a good test is essential for RSA.**

*Introduction.* RSA and Diffie-Hellman need very large random primes, typically 1024 bits or more. Trial division is hopeless at that size, so programs use fast probabilistic tests that either prove a number composite or say that it is prime with a tiny chance of error (section 2.4, Figure 2.4).

1. **Why primes are plentiful.** The density of primes near N is about 1 over ln N. For N near 2 to the power 1024, ln N is about 710, so about one number in 710 is prime, or one in 355 among odd numbers. A program therefore needs only a few hundred random candidates.
2. **Fermat test.** Pick a, compute a to the power n - 1 mod n. If the result is not 1, n is certainly composite. If it is 1, n is probably prime. The flaw is that **Carmichael numbers** such as 561 = 3 x 11 x 17 pass for every base coprime to n; for 561 all 320 coprime bases pass.
3. **Miller-Rabin test.** Write n - 1 = 2 to the power s times d with d odd. Compute x = a to the power d mod n and square it up to s - 1 times. If x = 1 at the start or x = n - 1 at any step, n passes for this base; otherwise n is composite.
4. **Worked example, n = 561.** Here n - 1 = 560 = 16 x 35, so s = 4 and d = 35. For a = 2 the sequence is 263, 166, 67, 1. It never reaches 560, and it reaches 1 from 67, a non-trivial square root of 1 (67 x 67 = 4489 = 8 x 561 + 1). So 561 is composite, although the Fermat test could not tell.
5. **Error bound.** For any odd composite n, at most one quarter of the bases are liars, so k random bases leave an error chance of at most 4 to the power -k. With k = 40 this is below 10 to the power -24.
6. **Key generation loop.** Draw a random odd number of the required size, quick-check small prime divisors, then run Miller-Rabin. Repeat until a number passes.

| Point | Fermat test | Miller-Rabin test |
|---|---|---|
| Idea | a to the power n - 1 is 1 | Also checks square roots of 1 |
| Fooled by Carmichael numbers | Yes (561) | No |
| Liars among bases | Possibly all | At most 1/4 |
| Used in practice | As a first filter | As the main test |

*Why it matters for RSA.* If one of the two secret numbers were composite, phi(n) would be computed wrongly and either decryption would fail or n would be easy to factor. A weak primality test could therefore silently produce an insecure key.

*Conclusion.* Miller-Rabin is fast, simple and reliable enough that a phone can generate a key pair in a moment, which is why it is used in every major cryptographic library.
