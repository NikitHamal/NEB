---
subject: Discrete Structure
grade: BCA Semester 2
unit: 6
title: Number Theory, Modular Arithmetic and Algebraic Structures
area: BCA 151 · Discrete Structure · Unit 6
---

Number theory, once the purest branch of mathematics, now protects every online payment. This unit covers divisibility, the Euclidean algorithm, modular arithmetic and RSA, then introduces algebraic structures (groups) and the lattice and Boolean algebra viewpoint that unifies sets, logic and circuits.

::: key What this unit gives you
- Divisibility, primes, gcd/lcm, the Euclidean and extended Euclidean algorithms.
- Congruences, modular inverses, Fermat's theorem, the Chinese remainder theorem.
- Applications: hashing, check digits, Caesar cipher, and RSA with a worked toy example.
- Groups and other algebraic structures; Boolean algebra as a lattice.
:::

## 6.1 Divisibility, primes and gcd

a **divides** $b ( a$ | *b*) if $b = a k$ for an integer *k*. **Division algorithm**: for integers a and $d > 0$ there are unique *q* and *r* with $a = d q + r ,\  0 \leq r < d$. A **prime** has exactly two positive divisors $(2 ,\  3 ,\  5 ,\  7 ,\  11 ,\  \ldots)$. **Fundamental theorem of arithmetic**: every integer ≥ 2 factors uniquely into primes (up to order); $360 = 2^{3} \cdot 3^{2} \cdot 5$. There are infinitely many primes (Euclid, proved in Unit 1). To test whether *n* is prime, trial-divide by primes up to $\sqrt{n}$.

**gcd and lcm.** $\gcd (a ,\  b)$ is the largest common divisor; **$\gcd (a ,\  b)$ · lcm(a, $b ) = a b$**. Using factorisations: gcd takes the minimum powers, lcm the maximum. a and *b* are **coprime** if $\gcd = 1$.

**Euclidean algorithm**: $\gcd (a ,\  b) = \gcd ( b$, a mod *b*), stopping when the remainder is 0. It takes at most about 5 × (digits of the smaller number) steps, which is fast even for 300-digit numbers.

::: example Worked example: gcd and extended Euclid
$\gcd (252 ,\  105)$: 252 = 2·105 + 42; 105 = 2·42 + 21; 42 = 2·21 + 0. **$\gcd = 21$**; lcm = 252·105/21 = **1260**.

**Extended Euclid (Bézout):** work backwards: $21 = 105$ − 2·42 = $105 - 2 ( 252$ − 2·105) = **5·105 − 2·252**. So 21 = 5·105 + (−2)·252, and the equation $105 x + 252 y = 21$ has the solution $(x ,\  y) = (5 ,\  - 2)$.
:::

A linear Diophantine equation $a x$ + by = *c* has integer solutions iff $\gcd (a ,\  b)$ | *c*. Example: $6 x + 9 y = 8$ has none ($\gcd 3$ does not divide $8 ) ;\  6 x + 9 y = 12$ does $(x = - 2 ,\  y = 2)$.

### The sieve of Eratosthenes

Eratosthenes, who also measured the size of the Earth, gave the first method for listing primes: write the numbers, cross out the multiples of 2, then of 3, then of 5 and so on up to the square root of the limit. What is left is prime. Plate 6.1 runs the sieve on 1 to 100: crossing out multiples of 2, 3, 5 and 7 is enough because the next prime, 11, has 121 above 100. It leaves 25 primes and 8 pairs of twin primes.

```photogrid label="6.1" cols="2" ratio="1.2" caption="Cross out the multiples. (a) Eratosthenes of Cyrene (about 276-194 BC). (b) The sieve on 1 to 100: the 25 primes are highlighted; sieving with 2, 3, 5 and 7 is enough because 11 $x 11 = 121 > 100$; there are 8 twin-prime pairs and 168 primes below 1,000."
@ photo id="bca151/eratosthenes" cap="Eratosthenes (engraved portrait)"
fit 1.2
focus 0.5 0.4
@ svg cap="Primes up to 100"
def sieve(n):
    ok = [True] * (n + 1); ok[0] = ok[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if ok[i]:
            for j in range(i * i, n + 1, i): ok[j] = False
    return ok
s = sieve(100); pr = [i for i in range(101) if s[i]]
assert len(pr) == 25 and pr[-1] == 97 and sum(sieve(1000)) == 168 and 11 * 11 > 100
tw = [(p, p + 2) for p in pr if p + 2 in pr]
assert len(tw) == 8 and tw[-1] == (71, 73)
f = Fig(400, 250)
f.text(200, 14, "1 to 100: primes highlighted", size=11, color=NAVY, bold=True)
for n in range(1, 101):
    r, c = divmod(n - 1, 10)
    p = s[n]
    f.box(30 + c * 34, 22 + r * 19, 32, 17, str(n), fill=MINT if p else SOFT, stroke=TEAL if p else "#cbd5e1", color=TEAL if p else "#94a3b8", size=10.5, bold=p, r=2)
f.text(200, 240, "25 primes; twin pairs (3,5) (5,7) ... (71,73): 8", size=10.5, color=SLATE, bold=True)
```

## 6.2 Modular arithmetic

**$a \equiv b$ (mod *m*)** means *m* | $(a - b)$, i.e. a and *b* leave the same remainder. Congruence is an equivalence relation with *m* classes $(\mathbb{Z}_{m} = \{0 ,\  1 ,\  \ldots ,\  m - 1\})$. It respects addition, subtraction and multiplication:

$(a + b)$ mod $m = ( ( a$ mod $m ) + ( b$ mod *m*)) mod *m*; likewise for ×, so we can reduce at every step.

::: example Worked example
Last digit of $7^{222}$: powers of 7 mod 10 cycle 7, 9, 3, 1 (period 4). 222 mod $4 = 2$, so the last digit is **9**.

$2^{100}$ mod 7: $2^{3} = 8 \equiv 1$, so $2^{100} = (2^{3})^{33} \cdot 2$ ≡ **2**.

$(123 \times 456)$ mod 11: $123 \equiv 2 ,\  456 \equiv 5 (456 - 451)$, so 10.

**Divisibility by 9:** a number ≡ its digit sum (mod 9); 7,842 has digit sum $21 \equiv 3$, so 7,842 mod $9 = 3$.
:::

**Modular inverse.** a has an inverse mod *m* iff $\gcd (a ,\  m) = 1$; it is found with extended Euclid. Then $a x \equiv b$ (mod *m*) has the solution $x \equiv a^{-1} b$.

::: example Worked example
Inverse of 7 mod 26: 26 = 3·7 + 5; 7 = 1·5 + 2; 5 = 2·2 + 1. Back: $1 = 5$ − 2·2 = $5 - 2 (7 - 5)$ = 3·5 − 2·7 = $3 ( 26$ − 3·7) − 2·7 = 3·26 − 11·7. So $7^{-1} \equiv - 11$ ≡ **15** (check: 7·15 = 105 = 4·26 + 1 ✓).

Solve $3 x \equiv 4$ (mod 7): $3^{-1} = 5 (15 \equiv 1)$, so *x* ≡ 5·4 = 20 ≡ **6** (check 18 mod $7 = 4$ ✓).
:::

**Fermat's little theorem**: if *p* is prime and *p* ∤ a, then **$a^{p-1} \equiv 1$ (mod *p*)**. **Euler's theorem**: if $\gcd (a ,\  n) = 1$ then $a^{\varphi (n)} \equiv 1$ (mod *n*), where $\varphi (n)$ counts integers up to *n* coprime to $n ;\  \varphi (p) = p - 1 ,\  \varphi (p q) = (p - 1) (q - 1)$.

**Chinese remainder theorem (CRT)**: if the moduli are pairwise coprime, the system $x \equiv a_{i}$ (mod $m_{i}$) has a unique solution modulo $M = \prod m_{i}$.

::: example Worked example: CRT
$x \equiv 2$ (mod $3 ) ,\  x \equiv 3$ (mod $5 ) ,\  x \equiv 2$ (mod 7). $M = 105$. Search $x = 2 + 3 t (t = 0 ,\  1 ,\  \ldots)$ satisfying mod $5 = 3$: $x = 8$ (8 mod $5 = 3$). Now $x = 8$ + 15s with $x \equiv 2$ (mod 7): $8 \equiv 1 ,\  15 \equiv 1$, so $1 + s \equiv 2 \Rightarrow s = 1 ,\  x$ = **23**. Check: 23 mod $3 = 2$, mod $5 = 3$, mod $7 = 2$ ✓. Solutions: $23 + 105 k$.
:::

### Arithmetic on a clock face

A clock does arithmetic modulo 12: after 12 it starts again at 0. Ten o'clock plus seven hours is five o'clock because $17 = 12 + 5$, which we write 17 mod $12 = 5$. Powers also cycle: successive powers of 3 modulo 7 are 3, 2, 6, 4, 5, 1 and then repeat, a pattern that cryptography relies on. Plate 6.2 shows the clock sums and the six-step cycle computed with Python's `pow`.

```photogrid label="6.2" cols="2" ratio="1.0" caption="Numbers that wrap round. (a) A quartz clock: its hours count modulo 12. (b) The clock sums $10 + 7 = 5$ and $9 + 5 = 2$ (mod 12), and the powers of 3 modulo 7, which run through 3, 2, 6, 4, 5, 1 and then return to 3."
@ photo id="bca151/clock" cap="Clock face: hours are numbers modulo 12"
fit 1.0
focus 0.5 0.5
@ svg cap="Clock sums and the cycle of powers of 3 mod 7"
import math
assert (10 + 7) % 12 == 5 and (9 + 5) % 12 == 2
cyc = [pow(3, k, 7) for k in range(1, 8)]
assert cyc == [3, 2, 6, 4, 5, 1, 3]
f = Fig(400, 250)
cx, cy, R = 100, 82, 56
f.circle(cx, cy, R + 10, fill=SOFT, stroke=NAVY)
for h in range(12):
    a = math.radians(-90 + 30 * h); n = 12 if h == 0 else h
    hot = n in (10, 5)
    f.text(cx + R * math.cos(a), cy + R * math.sin(a), str(n), size=11, color=RED if hot else NAVY, bold=hot, vmid=True)
f.text(cx, cy, "mod 12", size=10.5, color=SLATE, bold=True, vmid=True)
for i, t in enumerate(["10 + 7 = 17 = 5 (mod 12)", "9 + 5 = 14 = 2 (mod 12)", "5 - 8 = -3 = 9 (mod 12)"]):
    f.text(200, 40 + i * 28, t, size=10.5, color=SLATE, bold=True, anchor="start")
assert (5 - 8) % 12 == 9
f.text(200, 160, "3^k mod 7, k = 1..7", size=11, color=NAVY, bold=True, anchor="middle")
for i, v in enumerate(cyc):
    f.box(8 + i * 55, 172, 50, 34, str(v), fill=MINT if i < 6 else SAND, stroke=TEAL if i < 6 else AMBER, color=TEAL if i < 6 else AMBER, size=13, bold=True)
f.text(200, 232, "Back to 3 after 6 steps: the cycle length is 6.", size=10.5, color=SLATE, bold=True)
```

## 6.3 Applications

- **Hashing**: $h (k) = k$ mod *m* with *m* prime spreads keys well. Keys 123, 456, 789 with $m = 11$ give 2, 5, 8 (789 = 71·11 + 8).
- **Check digits**: ISBN-10 requires $\sum (i \times d_{i}) \equiv 0$ (mod 11); a single wrong digit is always detected, since 11 is prime.
- **Pseudo-random numbers**: linear congruential generator $X_{n+1} = (a X_{n} + c)$ mod *m*.
- **Caesar cipher**: $E (x) = (x + 3)$ mod $26 ,\  D (y) = (y - 3)$ mod 26; "NEPAL" becomes "QHSDO". It is weak (26 keys); an **affine cipher** $E (x) = (a x + b)$ mod 26 needs $\gcd (a ,\  26) = 1$.
- **Fast modular exponentiation** (square and multiply) computes $a^{k}$ mod *m* in $O (\log k)$ multiplications: $3^{13}$ mod 7: $3^{2} = 2 ,\  3^{4} = 4 ,\  3^{8} = 16 \equiv 2 ;\  13 = 8 + 4 + 1 \Rightarrow 2 \cdot 4 \cdot 3 = 24$ ≡ **3**.

**RSA public-key cryptography.**

1. Choose primes $p ,\  q ;\  n = p q ;\  \varphi = (p - 1) (q - 1)$.
2. Choose *e* coprime to *φ* (public key $(e ,\  n)$); compute $d = e^{-1}$ mod *φ* (private key).
3. Encrypt: $c = m^{e}$ mod *n*. Decrypt: $m = c^{d}$ mod *n* (correct by Euler's theorem since ed ≡ 1 mod *φ*).

::: example Worked example: a toy RSA
$p = 61 ,\  q = 53 \Rightarrow n = 3233 ,\  \varphi = 60 \cdot 52 = 3120$. Take $e = 17 (\gcd (17 ,\  3120) = 1)$. Then $d = 17^{-1}$ mod 3120 = **2753** ($17 \cdot 2753$ = 46,801 = $15 \cdot 3120 + 1$ ✓).

Encrypt $m = 65$: $c = 65^{17}$ mod 3233 = **2790**. Decrypt: $2790^{2753}$ mod 3233 = **65** ✓.

Security rests on the difficulty of factoring *n*; real keys use *n* of 2048 bits or more. Real systems also add padding (OAEP) and use RSA mainly to exchange a symmetric key. Quantum computers (Shor's algorithm) could break RSA, which motivates post-quantum cryptography.
:::

### Enigma: a lot of modular arithmetic

The German Enigma machine was a chain of rotors, each a permutation of the 26 letters, advancing like an odometer, so every key press was enciphered with a different permutation. The number of possible settings is a counting problem from Chapter 3. Choosing and ordering three rotors from five gives 60 ways; each rotor starts at one of 26 positions (17,576 combinations); and the plugboard joined ten pairs of letters. Plate 6.3 multiplies the three factors.

```photogrid label="6.3" cols="2" ratio="1.1" caption="A machine made of permutations. (a) A naval Enigma M4 in a museum. (b) The number of Enigma settings from three independent choices: rotor order (5 $x 4 x 3 = 60$), rotor start positions ($26^{3}$ = 17,576) and ten plugboard pairs (150,738,274,937,250); the product is about 1.59 $x 10^{20}$."
@ photo id="bca151/enigma" cap="Enigma M4: keyboard, rotors and lamps"
fit 1.1
focus 0.5 0.5
@ svg cap="Counting the settings of an Enigma"
import math
order = 5 * 4 * 3
pos = 26 ** 3
plug = math.factorial(26) // (math.factorial(6) * math.factorial(10) * 2 ** 10)
total = order * pos * plug
assert order == 60 and pos == 17576 and plug == 150738274937250 and abs(total / 1.5896e20 - 1) < 1e-3
f = Fig(400, 250)
f.text(200, 16, "Three choices multiply (product rule)", size=11, color=NAVY, bold=True)
items = [("rotor order", "5 x 4 x 3", f"{order}", BLUE, NAVY), ("start positions", "26 x 26 x 26", f"{pos:,}", SAND, AMBER), ("plugboard, 10 pairs", "26!/(6! 10! 2^10)", f"{plug:,}", MINT, TEAL)]
for i, (nm, fm, val, fl, st) in enumerate(items):
    y = 30 + i * 52
    f.box(8, y, 384, 44, "", fill=fl, stroke=st, r=4)
    f.text(16, y + 14, nm, size=11, color=st, bold=True, anchor="start", vmid=True)
    f.text(16, y + 32, fm, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(384, y + 22, val, size=12.5, color=st, bold=True, anchor="end", vmid=True)
f.box(8, 192, 384, 44, "", fill=ROSE, stroke=RED, r=4)
f.text(16, 207, "total settings", size=11, color=RED, bold=True, anchor="start", vmid=True)
f.text(384, 214, f"{total:.3e}", size=14, color=RED, bold=True, anchor="end", vmid=True)
f.text(200, 246, "About 159 quintillion, yet the machine was broken.", size=10.5, color=SLATE)
```

## 6.4 Algebraic structures

A **binary operation** on a set S takes two elements and returns an element of S (closure).

| Structure | Axioms |
|---|---|
| **Semigroup** | closed, associative |
| **Monoid** | semigroup with an identity |
| **Group** | monoid where every element has an inverse |
| **Abelian group** | commutative group |
| **Ring** | abelian group under +, monoid (or semigroup) under ×, × distributes over + |
| **Field** | commutative ring where every non-zero element has a multiplicative inverse |

Examples: ($\mathbb{Z}$, +) is an abelian group; ($\mathbb{N}$, +) is a monoid; $(\mathbb{Z} ,\  \times)$ is a monoid; ($\mathbb{Q}$ − {0}, *×*) is a group; **$\mathbb{Z}_{p}$ with + and × is a field when *p* is prime** (that is why inverses mod a prime always exist); strings under concatenation form a monoid (identity: empty string); invertible $n \times n$ matrices under multiplication form a (non-abelian) group; the permutations of *n* objects form the symmetric group $S_{n}$ of order $n !$.

::: example Worked example: the group ℤ₆ under +
Elements $\{0 ,\  \ldots ,\  5\}$, identity 0, inverse of a is $6 - a$ (so $2^{-1} = 4$). Order 6. The element 1 **generates** the group (1, 2, 3, 4, 5, 0), so $\mathbb{Z}_{6}$ is **cyclic**; 5 also generates it; 2 generates only {0, 2, 4}, a **subgroup** of order 3; {0, 3} is a subgroup of order 2. **Lagrange's theorem**: the order of a subgroup divides the order of the group (2 | 6, 3 | 6). The multiplicative set {1, 5} mod 6 is a group, but {1, 2, 3, 4, 5} mod 6 is not (2 has no inverse as $\gcd (2 ,\  6) = 2 ) ;\  \mathbb{Z}_{7} \ast = \{1 ,\  \ldots ,\  6\}$ is a group of order 6 under multiplication mod 7.
:::

A **homomorphism** preserves the operation: $f ( a$ ∗ $b ) = f ( a$) ⋆ $f (b)$. Example: *x* ↦ *x* mod 3 from ($\mathbb{Z}$, +) to ($\mathbb{Z}_{3}$, +), and *x* ↦ $e^{x}$ from ($\mathbb{R}$, +) to $(\mathbb{R}^{+} ,\  \times)$. **Applications:** error-correcting codes are built on finite fields (Reed–Solomon in QR codes, CDs); AES uses arithmetic in $G F (2^{8})$; elliptic-curve cryptography uses a group of curve points.

## 6.5 Lattices and Boolean algebra

A **lattice** is a poset in which every two elements have a least upper bound (**join**, *∨*) and a greatest lower bound (**meet**, *∧*). Examples: (subsets of $S ,\  \subseteq$) with ∪ and ∩; (divisors of *n*, |) with lcm and $\gcd ;\  (\mathbb{N} ,\  \leq)$ with max and min.

A **Boolean algebra** is a complemented distributive lattice with 0 and 1. The two-element algebra {0, 1} is the algebra of switching circuits and of propositional logic; the power set of a set is another; **every finite Boolean algebra has $2^{n}$ elements** and looks like subsets of an n-set. This is why the same laws (De Morgan, distributivity, absorption) hold in logic (Unit 1), sets (Unit 2) and digital circuits (the Digital Logic book): they are three views of one structure.

**Divisor lattice of 12**: elements {1, 2, 3, 4, 6, 12}; join of 4 and 6 = lcm = 12; meet = $\gcd = 2$. It is *not* complemented (4 has no complement), so it is a lattice but not a Boolean algebra; the divisors of 30 (= 2·3·5) form one, with $8 = 2^{3}$ elements.

### The divisors of 12 form a lattice

Under divisibility, the divisors of 12 form a partial order in which every pair of elements has a greatest common divisor (the meet) and a least common multiple (the join). A Hasse diagram draws only the covering relations: a line from a to *b* if a divides *b* and nothing lies strictly between. Plate 6.4 finds those lines by program and confirms that $\gcd (4 ,\  6) = 2$ and lcm(4, $6 ) = 12$.

```photogrid label="6.4" cols="2" ratio="1.2" caption="A lattice drawn as a Hasse diagram. (a) The subgroups of the dihedral group D4 form a lattice drawn the same way. (b) The divisors of 12 ordered by divisibility: the seven covering lines are found by computer; meet is gcd and join is lcm, so $\gcd (4 ,\  6) = 2$ and lcm(4, $6 ) = 12$."
@ photo id="bca151/hasse" cap="Hasse diagram of the subgroups of D4"
fit 1.2
focus 0.5 0.5
@ svg cap="Divisibility lattice of 12"
from math import gcd
D = [1, 2, 3, 4, 6, 12]
cov = {(a, b) for a in D for b in D if a != b and b % a == 0 and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in D)}
assert cov == {(1, 2), (1, 3), (2, 4), (2, 6), (3, 6), (4, 12), (6, 12)}
assert gcd(4, 6) == 2 and 4 * 6 // gcd(4, 6) == 12
P = {1: (200, 215), 2: (130, 150), 3: (270, 150), 4: (80, 80), 6: (200, 80), 12: (140, 25)}
f = Fig(400, 250)
for a, b in cov: f.line(*P[a], *P[b], color=SLATE, sw=1.6)
for k, (x, y) in P.items():
    f.circle(x, y, 15, fill=BLUE if k not in (1, 12) else SAND, stroke=NAVY if k not in (1, 12) else AMBER, label=str(k), size=11, color=NAVY)
f.text(300, 40, "meet = gcd", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(300, 58, "join = lcm", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(300, 90, "4 and 6:", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(300, 108, "gcd = 2", size=10.5, color=SLATE, anchor="start")
f.text(300, 126, "lcm = 12", size=10.5, color=SLATE, anchor="start")
f.text(300, 220, "7 covering lines", size=10.5, color=SLATE, bold=True, anchor="start")
```

## 6.6 Clock arithmetic and the RSA message path

Modular arithmetic is clock arithmetic. On a 12-hour clock, $9 + 7 = 16$, which the clock shows as 4, because $16 = 12 + 4$, written $16 \equiv 4$ (mod 12). The left half of Figure 6.1 shows this "wrap-around": adding 7 hours to 9 o'clock walks 7 steps round the dial and lands on 4. The same picture explains why 7 has an inverse mod 12 but 4 does not: stepping 7 at a time visits all 12 positions $(\gcd (7 ,\  12) = 1)$, whereas stepping 4 at a time only ever visits 0, 4 and 8 $(\gcd (4 ,\  12) = 4)$. The right half traces the toy RSA of Section 6.3 from the sender to the receiver: only the receiver's private number $d = 2753$ can undo the public encryption.

```svgfig label="6.1" caption="Left: clock arithmetic mod $12 ,\  9 + 7 = 16$ and 16 mod $12 = 4$; stepping by 7 reaches every hour, stepping by 4 reaches only 0, 4, 8. Right: the toy RSA message path with $p = 61 ,\  q = 53 ,\  n = 3233 ,\  e = 17 ,\  d = 2753$; message 65 becomes 2790 and back."
import math
f = Fig(600, 270)
cx, cy, R = 120, 135, 90
f.circle(cx, cy, R + 14, fill="#ffffff", stroke=NAVY, sw=2)
def pos(h, r=R):
    a = math.radians(h * 30 - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)
for h in range(12):
    x, y = pos(h)
    hot = h in (9, 4)
    f.circle(x, y, 12, fill="#fde68a" if hot else (BLUE if h % 4 == 0 else "#ffffff"), stroke=NAVY if hot else SLATE, sw=1.5, label=str(h), size=11, color=NAVY)
x1, y1 = pos(9, 62); x2, y2 = pos(4, 62)
f.arrow([(x1, y1), (cx, cy - 30), (x2, y2)], color=RED, sw=2.2, label="+ 7 steps", lpos=(cx - 5, cy - 38), lsize=11)
f.text(cx, cy + 12, "9 + 7 = 16", size=12, color=NAVY, bold=True)
f.text(cx, cy + 30, "16 = 12 + 4", size=12, color=NAVY)
f.text(cx, cy + 48, "so 16 ≡ 4 (mod 12)", size=12, color=RED, bold=True)
f.text(cx, 258, "step 7: all 12 hours | step 4: only 0, 4, 8", size=11, color=TEAL, bold=True)
f.box(250, 28, 190, 52, "Sender: m = 65", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(250, 108, 190, 56, "c = 65^17 mod 3233 = 2790", fill="#fde68a", color=NAVY, size=11, bold=True)
f.box(250, 192, 190, 52, "Receiver: m = 65", fill="#bbf7d0", color=NAVY, size=12, bold=True)
f.arrow([(345, 80), (345, 108)], color=SLATE, sw=2)
f.arrow([(345, 164), (345, 192)], color=SLATE, sw=2)
f.box(466, 108, 126, 56, "public key (17, 3233)", fill="#ffffff", stroke=TEAL, color=NAVY, size=10.5)
f.arrow([(466, 136), (440, 136)], color=TEAL, sw=1.8)
f.box(466, 192, 126, 52, "private d = 2753", fill="#ffffff", stroke=RED, color=NAVY, size=10.5)
f.arrow([(466, 218), (440, 218)], color=RED, sw=1.8)
f.text(528, 50, "d = 17^-1 mod 3120", size=10, color=SLATE, bold=True)
f.text(528, 66, "17 x 2753 = 15 x 3120 + 1", size=10, color=SLATE)
f.text(529, 260, "kept secret", size=10, color=RED, bold=True)
```

### Caesar and Alberti: encryption as modular addition

Shifting every letter three places, as Julius Caesar did, is addition modulo 26: encrypt with $c = (p + 3)$ mod 26 and decrypt with $p = (c - 3)$ mod 26. Leon Battista Alberti built a disc with two alphabets that can be turned, so the shift changes during the message. There are only 25 useful Caesar keys, so an attacker simply tries all of them. Plate 6.5 encrypts NEPAL and shows the shifted alphabet.

```photogrid label="6.5" cols="2" ratio="1.2" caption="Encryption as addition mod 26. (a) A cipher disc after Alberti: the inner ring turns against the outer ring. (b) A Caesar shift of 3 on the alphabet, the word NEPAL encrypted as QHSDO and decrypted again by subtracting 3 mod 26; only 25 non-trivial keys exist."
@ photo id="bca151/alberti" cap="Cipher disc after Alberti: turn the inner ring to change the key"
fit 1.2
focus 0.5 0.5
@ svg cap="Caesar shift of 3"
import string
A = string.ascii_uppercase
enc = lambda w, k: "".join(A[(A.index(c) + k) % 26] for c in w)
assert enc("NEPAL", 3) == "QHSDO" and enc("QHSDO", -3) == "NEPAL" and enc(enc("NEPAL", 13), 13) == "NEPAL"
f = Fig(400, 250)
f.text(200, 14, "Plain letter (top) and cipher letter (bottom), shift 3", size=11, color=NAVY, bold=True)
for i, c in enumerate(A):
    r = i // 13; x = 10 + (i % 13) * 29; y = 28 + r * 58
    f.box(x, y, 27, 20, c, fill=BLUE, stroke=NAVY, color=NAVY, size=10.5, bold=True)
    f.box(x, y + 22, 27, 20, A[(i + 3) % 26], fill=SAND, stroke=AMBER, color=AMBER, size=10.5, bold=True)
w = "NEPAL"
for i, c in enumerate(w):
    f.box(60 + i * 56, 150, 48, 24, c, fill=BLUE, stroke=NAVY, color=NAVY, size=12, bold=True)
    f.arrow([(84 + i * 56, 176), (84 + i * 56, 188)], color=SLATE, sw=1.4)
    f.box(60 + i * 56, 190, 48, 24, enc(w, 3)[i], fill=SAND, stroke=AMBER, color=AMBER, size=12, bold=True)
f.text(200, 236, "c = (p + 3) mod 26,  p = (c - 3) mod 26.  Only 25 keys: try them all.", size=10.5, color=SLATE, bold=True)
```

## 6.7 Eight uses of number theory and algebraic structures

1. **Online banking and payments.** RSA and elliptic-curve keys protect the HTTPS link between your phone and an $a p p$ such as ConnectIPS or Fonepay. The modular exponentiation of Section 6.3 runs every time a secure session starts.
2. **Hash tables.** The function $h (k) = k$ mod *m* spreads student roll numbers or customer IDs over *m* slots. Choosing a prime *m* reduces collisions, so lookups stay fast even for a large university database.
3. **Check digits.** ISBN, bank-card and barcode numbers end with a digit computed with modular arithmetic. A single mistyped digit is caught immediately because the modulus is prime or coprime to the weights.
4. **Error-correcting codes.** QR codes and CDs use Reed–Solomon codes built on finite fields. A damaged label on a parcel can still be scanned because the missing data is rebuilt from the extra field-based symbols.
5. **Calendars and schedules.** Day-of-week calculations use mod 7, clock times use mod 12 or mod 24, and rotating duty rosters use mod *n*. Converting a Bikram Sambat date to a weekday is a modular exercise.
6. **Random numbers.** A linear congruential generator $X (n + 1)$ = (aXn + *c*) mod *m* produces the pseudo-random numbers behind simulations and games. Choosing $a ,\  c$ and *m* with the right gcd conditions gives a long, non-repeating cycle.
7. **Symmetric encryption.** AES works on bytes as elements of the field $G F (2^{8})$, so every substitution step is invertible. This is what protects stored passwords and Wi-Fi traffic in homes and offices.
8. **Circuit design and logic.** A Boolean algebra is the common law-book of logic, sets and switching circuits. Simplifying an expression with these laws gives a cheaper chip with fewer gates.

## Formula and fact sheet

- $a = d q + r ;\  \gcd (a ,\  b) = \gcd ( b$, a mod $b ) ;\  \gcd$ · lcm = $a b$; Bézout: $\gcd = a x$ + by.
- $a \equiv b$ (mod $m ) \Leftrightarrow m$ | $a - b$; inverse exists iff $\gcd (a ,\  m) = 1$.
- Fermat: $a^{p-1} \equiv 1$ (mod *p*). Euler: $a^{\varphi} (n) \equiv 1 ;\  \varphi (p q) = (p - 1) (q - 1)$.
- CRT: coprime moduli give a unique solution mod the product.
- RSA: $n = p q$, ed ≡ 1 (mod $\varphi ) ,\  c = m^{e}$ mod $n ,\  m = c^{d}$ mod *n*.
- Group: closure, associativity, identity, inverse. $\mathbb{Z}_{p}$ is a field for prime *p*. Lagrange: subgroup order divides group order.
- Finite Boolean algebra has $2^{n}$ elements.

## Chapter summary

- The Euclidean algorithm computes gcds quickly and the extended version yields inverses.
- Modular arithmetic lets us compute with remainders; Fermat, Euler and the CRT are its workhorses.
- RSA turns the difficulty of factoring into public-key encryption.
- Groups, rings and fields classify structures by their axioms; Boolean algebras unify logic, sets and circuits.

## Practice

1. Find $\gcd ( 1071$, 462) and express it as $1071 x + 462 y$.
2. Find $5^{-1}$ mod 17 and solve $5 x \equiv 3$ (mod 17).
3. Find the last two digits of $3^{100}$ (hint: $3^{20}$ mod 100).
4. Solve $x \equiv 1$ (mod $4 ) ,\  x \equiv 2$ (mod 9) (use CRT).
5. Compute $7^{100}$ mod 13 using Fermat's theorem.
6. In RSA with $p = 5 ,\  q = 11 ,\  e = 7$, find $n ,\  \varphi ,\  d$, the ciphertext of $m = 8$ and verify decryption.
7. Is ($\mathbb{Z}_{8}$ − {0}, × mod 8) a group? Justify.
8. List all subgroups of ($\mathbb{Z}_{12}$, +).
9. Show that the ISBN-10 check digit detects any single wrong digit.
10. Is the divisor lattice of 18 a Boolean algebra?

::: note Answers and worked solutions
**1.** 1071 = 2·462 + 147; 462 = 3·147 + 21; 147 = 7·21. **$\gcd = 21$**. $21 = 462$ − 3·147 = $462 - 3 ( 1071$ − 2·462) = 7·462 − 3·1071. So $x = - 3 ,\  y = 7$.

**2.** $5 \cdot 7 = 35$ = 2·17 + 1, so $5^{-1}$ = **7**. $5 x \equiv 3 \Rightarrow x$ ≡ 7·3 = 21 ≡ **4** (check 20 mod $17 = 3$ ✓).

**3.** $3^{4} = 81 ;\  3^{20} = 81^{5}$: $81^{2} = 6561 \equiv 61 ;\  81^{4} \equiv 61^{2} = 3721 \equiv 21 ;\  81^{5}$ ≡ 21·81 = $1701 \equiv 1$. So $3^{20} \equiv 1$ (mod 100) and $3^{100}$ ≡ **01**.

**4.** $x = 1 + 4 t \equiv 2$ (mod $9 ) \Rightarrow 4 t \equiv 1 \Rightarrow t \equiv 7$ (4·7 = $28 \equiv 1 ) \Rightarrow x = 29$. Solutions **$x \equiv 29$ (mod 36)** (29 mod $4 = 1$, 29 mod $9 = 2$ ✓).

**5.** $7^{12} \equiv 1$ (mod 13); 100 = 8·12 + $4 ;\  7^{4} = 2401$ = 184·13 + 9. So $7^{100}$ ≡ **9**.

**6.** $n = 55 ,\  \varphi = 40 ;\  d = 7^{-1}$ mod $40 = 23$ (7·23 = 161 = 4·40 + 1). $c = 8^{7}$ mod 55: $8^{2} = 64 \equiv 9 ;\  8^{4} \equiv 81 \equiv 26 ;\  8^{6}$ ≡ 26·9 = $234 \equiv 14 ;\  8^{7} \equiv 112$ ≡ **2**. Decrypt $2^{23}$ mod 55: $2^{10} = 1024 \equiv 34 ;\  2^{20} \equiv 34^{2} = 1156 \equiv 1 ;\  2^{23} \equiv 8$ ✓.

**7.** **No**: 2, 4, 6 have no inverse (gcd with 8 is not 1) and 2·4 = $8 \equiv 0$ is not in the set.

**8.** Subgroups of $\mathbb{Z}_{12}$ correspond to divisors of 12: ⟨1⟩ (order 12), ⟨2⟩ = {0,2,4,6,8,10} (6), ⟨3⟩ = {0,3,6,9} (4), ⟨4⟩ = {0,4,8} (3), ⟨6⟩ = {0,6} (2), ⟨0⟩ = {0} (1): **six** subgroups.

**9.** If digit *i* (weight *i*) changes by $\delta \neq 0 (|\delta| \leq 10)$, the weighted sum changes by $i \delta$, which is not ≡ 0 (mod 11) because 11 is prime and divides neither *i* (1 to 10) nor *δ*.

**10.** $18 = 2 \cdot 3^{2}$ is not square-free (it has a repeated prime factor), so the divisor lattice (1, 2, 3, 6, 9, 18) is **not** a Boolean algebra (6 elements is not $2^{n}$).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find $\gcd ( 252$, 105) with the Euclidean algorithm, express it as $105 x + 252 y$, and state when 105 has an inverse modulo 252.**

*Introduction.* The Euclidean algorithm uses the identity $\gcd (a ,\  b) = \gcd ( b$, a mod *b*). It stops when a remainder is 0, and the last non-zero remainder is the gcd.

*Division steps.*

1. $252 = 2 \times 105 + 42$
2. $105 = 2 \times 42 + 21$
3. $42 = 2 \times 21 + 0$

The last non-zero remainder is 21, so **$\gcd (252 ,\  105) = 21$**, and lcm = $252 \times 105 \div 21$ = 1,260.

*Extended Euclid (Bézout).* Work backwards: $21 = 105 - 2 \times 42$, and $42 = 252 - 2 \times 105$, so $21 = 105 - 2 (252 - 2 \times 105) = 5 \times 105 - 2 \times 252$. Hence $x = 5$ and $y = - 2$. Check: $525 - 504 = 21$.

*Inverse.* An inverse of a modulo *m* exists if and only if $\gcd (a ,\  m) = 1$. Here $\gcd (105 ,\  252) = 21$, not 1, so 105 has **no inverse** modulo 252. By contrast, 7 has the inverse 15 modulo 26 because $7 \times 15 = 105 = 4 \times 26 + 1$.

*Conclusion.* The extended Euclidean algorithm gives the gcd and the coefficients together; the coefficients are what produce modular inverses in RSA.

**Q2 (10 marks). Explain the RSA algorithm with a numerical example, and state the group, ring and field axioms with one example each.**

*Introduction.* RSA is a public-key system: anyone can encrypt with the public key, but only the owner of the private key can decrypt. Its security rests on the difficulty of factoring a large number $n = p q$.

*Algorithm.*

1. **Choose primes.** $p = 61 ,\  q = 53$.
2. **Compute *n* and *φ*.** $n = p q$ = 3,233; $\varphi = (p - 1) (q - 1) = 60 \times 52$ = 3,120.
3. **Public exponent.** Choose $e = 17$, coprime to 3,120. The public key is (17, 3233).
4. **Private exponent.** $d = e^{-1}$ mod *φ* = 2,753, since 17 × 2,753 = 46,801 = 15 × 3,120 + 1.
5. **Encrypt.** For $m = 65 ,\  c = 65^{17}$ mod 3233 = 2,790.
6. **Decrypt.** $m = 2790^{2753}$ mod $3233 = 65$. This works because ed ≡ 1 (mod *φ*) and Euler's theorem.

Figure 6.1 shows this path. Real keys use *n* of 2,048 bits or more, with padding such as OAEP.

*Algebraic structures.*

7. **Group.** A set with one operation that is closed, associative, has an identity and has inverses. Example: $\mathbb{Z}_{6}$ under addition mod 6 (identity 0, inverse of 2 is 4); it is cyclic, generated by 1.
8. **Ring and field.** A ring has two operations (addition forms an abelian group, multiplication is associative and distributes over addition); $\mathbb{Z}$ is a ring. A field also gives every non-zero element a multiplicative inverse; $\mathbb{Z}_{p}$ is a field when *p* is prime.

| Structure | Axioms | Example |
|---|---|---|
| Semigroup | closed, associative | ($\mathbb{N}$, +) |
| Monoid | + identity | $(\mathbb{Z} ,\  \times)$ |
| Group | + inverses | ($\mathbb{Z}$, +) |
| Ring | two operations, distributive | $\mathbb{Z}$ |
| Field | non-zero elements invertible | $\mathbb{Z}_{7}$ |

*Conclusion.* RSA uses arithmetic in the ring $\mathbb{Z}_{n}$ and the group of units mod *φ*, so its correctness is an application of group theory. The same structures also underlie AES and elliptic-curve cryptography.
