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
