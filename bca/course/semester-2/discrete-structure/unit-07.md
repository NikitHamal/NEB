---
subject: Discrete Structure
grade: BCA Semester 2
unit: 7
title: Proof Pitfalls, Boolean Functions, Databases, Probability and Algorithms
area: BCA 151 · Discrete Structure · Unit 7
---

The TU outline for Discrete Structure lists several topics that Units 1 to 6 treat only in passing or not at all: **vacuous and trivial proofs, existence and uniqueness proofs and mistakes in proofs**; **Boolean functions, floor and ceiling functions and n-ary relations with their database operations**; **the well-ordering property and the correctness of recursive algorithms**; **integer representations and the algorithms for arithmetic on them**; **permutations of objects that are not all different and the generation of permutations and combinations**; and **discrete probability** (conditional probability, random variables, expected value and variance, randomized algorithms and hashing). The outline also asks for **graph models, isomorphism, matching and the travelling salesman problem**. This unit closes each gap with definitions, worked examples, and small programs whose output is produced by running the code. Read it after the unit that each section extends.

::: key What this unit gives you
- The proof styles that were missing (vacuous, trivial, uniqueness, exhaustive) and the common mistakes in proofs.
- Boolean functions, floor and ceiling, and n-ary relations with select, project and join.
- Well-ordering and proofs that recursive algorithms are correct.
- Integer representations (binary, octal, hexadecimal) and the arithmetic algorithms behind computers.
- Counting with indistinguishable objects and the next-permutation algorithm.
- Discrete probability: conditional probability, Bayes' theorem, expectation, variance, randomized algorithms, hashing.
- Graph models, isomorphism, matching and the travelling salesman problem.
:::

## 7.1 Proof methods that were missing, and mistakes in proofs

Section 1.5 covered direct proof, contrapositive and contradiction. Four more styles appear in the outline.

### Vacuous and trivial proofs

Take an implication $p \to q$.

- A **vacuous proof** shows that the hypothesis $p$ is **false**. Then the implication is true whatever $q$ is. Example: let $P(n)$ be "if $n > 1$ then $n^2 > n$"; we need the statement $P(0)$: "if $0 > 1$ then $0^2 > 0$". The hypothesis $0 > 1$ is false, so $P(0)$ is true. Another: "every element of the empty set is a prime" is vacuously true.
- A **trivial proof** shows that the conclusion $q$ is **true**. Then the implication is true whatever $p$ is. Example: "if $a \ge b$ then $a^0 \ge b^0$" is true because $a^0 = b^0 = 1$ and $1 \ge 1$, so we never use the hypothesis.

Vacuous truth is not a trick: it is what makes statements about empty collections consistent, such as "every vertex of the null graph has even degree".

### Proof by cases and exhaustive proof

A **proof by cases** splits the argument into cases that cover every possibility, proves each, and concludes. An **exhaustive proof** is a proof by cases with a finite and small number of cases, each checked directly. The statement "for every integer $n$, $n^2 + n$ is even" is shown by cases: if $n$ is even then $n^2$ and $n$ are even, so their sum is even; if $n$ is odd then $n^2$ and $n$ are odd, and the sum of two odds is even.

```python
# exhaustive check of the claim n^2 < 2^n for every n from 5 to 30
bad = [n for n in range(5, 31) if not n * n < 2 ** n]
print("counterexamples for 5 <= n <= 30:", bad)
print("n=4 case:", 4 * 4, "vs", 2 ** 4, "-> n^2 < 2^n is", 4 * 4 < 2 ** 4)
```
```output
counterexamples for 5 <= n <= 30: []
n=4 case: 16 vs 16 -> n^2 < 2^n is False
```
The program is itself an exhaustive proof for the stated range, but it is not a proof for **all** $n$; that needs induction (Unit 4). A finite check can disprove a claim but can only prove a claim about a finite set.

### Existence and uniqueness proofs

An **existence proof** shows that at least one object with a property exists. A **constructive** proof exhibits it (the number $2$ is an even prime). A **non-constructive** proof shows existence without naming it: among 13 people, two share a birth month (pigeonhole), though the proof does not say which two. A **uniqueness proof** shows there is at most one such object; the standard method is to assume two objects $a$ and $b$ both have the property and prove $a = b$.

::: example Worked example: existence and uniqueness
*Claim:* for real numbers $a \ne 0$ and $b$, the equation $ax + b = 0$ has exactly one real solution.
*Existence:* $x = -b/a$ is a solution, because $a(-b/a) + b = 0$.
*Uniqueness:* suppose $x$ and $y$ both satisfy it. Then $ax + b = ay + b$, so $ax = ay$, and since $a \ne 0$ we divide to get $x = y$. Hence the solution exists and is unique.
:::

### Proof by counterexample

To disprove a universally quantified statement $\forall x\, P(x)$ it is enough to find one $x$ with $P(x)$ false. "Every prime is odd" is false because $2$ is prime and even. "Every number of the form $n^2 + n + 41$ is prime" holds for $n = 0, 1, \dots, 39$ and fails at $n = 40$:

```python
def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))
first = next(n for n in range(100) if not is_prime(n * n + n + 41))
print("first n where n^2+n+41 is not prime:", first, "value", first * first + first + 41, "=", 41, "x", (first * first + first + 41) // 41)
```
```output
first n where n^2+n+41 is not prime: 40 value 1681 = 41 x 41
```
### Mistakes in proofs

| Mistake | Why it is wrong | Example |
|---|---|---|
| **Affirming the conclusion** (converse error) | from $p \to q$ and $q$ you cannot conclude $p$ | "If it rains the road is wet; the road is wet, so it rained" (a hose may be the cause) |
| **Denying the hypothesis** (inverse error) | from $p \to q$ and $\neg p$ you cannot conclude $\neg q$ | "If you study you pass; you did not study, so you will fail" |
| **Circular reasoning (begging the question)** | the claim is assumed inside the argument | proving $x$ is even by "since $x$ is even, ..." |
| **Dividing by zero** | an unnoticed step uses $0$ in a denominator | "$a = b \Rightarrow a^2 = ab \Rightarrow a^2 - b^2 = ab - b^2 \Rightarrow (a+b)(a-b) = b(a-b) \Rightarrow a + b = b \Rightarrow 2 = 1$" divides by $a - b = 0$ |
| **Generalising from examples** | testing cases is not a proof of a universal claim | the $n^2 + n + 41$ example above |
| **Proving only one direction of an "if and only if"** | an equivalence needs $p \to q$ **and** $q \to p$ | showing $n$ even $\Rightarrow$ $n^2$ even but not the reverse |

For a **proof of equivalence** ("$p$ if and only if $q$") prove both $p \to q$ and $q \to p$, or build a chain of equivalences $p \leftrightarrow r_1 \leftrightarrow \dots \leftrightarrow q$. For a statement such as "the following are equivalent: (a), (b), (c)" prove a cycle $a \to b \to c \to a$.

## 7.2 Boolean functions, floor and ceiling, and relational databases

### Floor and ceiling in detail

The **floor** $\lfloor x \rfloor$ is the largest integer not greater than $x$; the **ceiling** $\lceil x \rceil$ is the smallest integer not less than $x$.

| $x$ | $\lfloor x \rfloor$ | $\lceil x \rceil$ |
|---|---|---|
| 3.7 | 3 | 4 |
| 5 | 5 | 5 |
| -3.7 | -4 | -3 |
| -0.5 | -1 | 0 |

Useful facts: $\lceil x \rceil = -\lfloor -x \rfloor$; $x - 1 < \lfloor x \rfloor \le x \le \lceil x \rceil < x + 1$; and $\lfloor n/2 \rfloor + \lceil n/2 \rceil = n$ for every integer $n$. In computing, the number of bytes needed for $b$ bits is $\lceil b/8 \rceil$, the number of pages for $n$ records with $k$ per page is $\lceil n/k \rceil$, and the depth of a balanced binary tree with $n$ nodes is $\lfloor \log_2 n \rfloor$.

```python
import math
for x in (3.7, 5, -3.7, -0.5):
    print(x, math.floor(x), math.ceil(x))
print("bytes for 29 bits:", math.ceil(29 / 8), " pages for 250 records at 40 per page:", math.ceil(250 / 40))
print("floor(n/2)+ceil(n/2)==n for n in -20..20:", all(math.floor(n / 2) + math.ceil(n / 2) == n for n in range(-20, 21)))
```
```output
3.7 3 4
5 5 5
-3.7 -4 -3
-0.5 -1 0
bytes for 29 bits: 4  pages for 250 records at 40 per page: 7
floor(n/2)+ceil(n/2)==n for n in -20..20: True
```
### Boolean functions

A **Boolean function** of degree $n$ is a function $f : \{0,1\}^n \to \{0,1\}$. It assigns $0$ or $1$ to every combination of $n$ bits, so there are $2^n$ inputs and $2^{2^n}$ different functions: 4 functions of one variable, 16 of two, 256 of three. Every Boolean function is described by a truth table and can be written as a **sum of products** (an OR of AND terms, one for each input that gives $1$), which is the link between this section and Digital Logic (BCA 103). For $f(x, y, z) = xy + \bar{z}$:

```python
from itertools import product
print(" x y z | f")
for x, y, z in product((0, 1), repeat=3):
    f = (x & y) | (1 - z)
    print(f" {x} {y} {z} | {f}")
print("functions of degree 1,2,3,4:", [2 ** (2 ** n) for n in (1, 2, 3, 4)])
```
```output
 x y z | f
 0 0 0 | 1
 0 0 1 | 0
 0 1 0 | 1
 0 1 1 | 0
 1 0 0 | 1
 1 0 1 | 0
 1 1 0 | 1
 1 1 1 | 1
functions of degree 1,2,3,4: [4, 16, 256, 65536]
```
The minterms (inputs giving $1$) are $000, 010, 100, 110, 111$, so the sum of products is $\bar{x}\bar{y}\bar{z} + \bar{x}y\bar{z} + x\bar{y}\bar{z} + xy\bar{z} + xyz$, which simplifies to $xy + \bar{z}$.

An **exponential function** here means $f(n) = b^n$ with $b > 1$; it grows faster than any polynomial, which is why exponential-time algorithms are called infeasible for large inputs (compare $2^{50} \approx 1.1 \times 10^{15}$ with $50^3 = 125{,}000$).

### n-ary relations and relational databases

A relation between two sets is a set of ordered pairs. An **n-ary relation** on sets $A_1, \dots, A_n$ is a subset of $A_1 \times \dots \times A_n$: a set of **n-tuples**. A **relational database** stores each table as an n-ary relation: each row is a tuple, each column is an attribute (a field), and the **primary key** is an attribute (or set of attributes) whose value identifies a tuple uniquely. A **composite key** uses several attributes together.

*Example:* the 3-ary relation STUDENT(Roll, Name, Programme) with rows $(1, \text{Asha}, \text{BCA})$, $(2, \text{Bikash}, \text{BCA})$, $(3, \text{Chitra}, \text{BIT})$ has Roll as a primary key, because no two rows share a roll number. Programme is not a key, because BCA appears twice.

The basic operations on n-ary relations are these.

- **Selection** $\sigma_C(R)$: keeps the rows that satisfy a condition $C$. $\sigma_{\text{Programme}=\text{BCA}}$(STUDENT) gives the first two rows.
- **Projection** $\pi_{i_1, \dots, i_m}(R)$: keeps only the chosen columns and removes duplicate rows. $\pi_{\text{Programme}}$(STUDENT) gives $\{\text{BCA}, \text{BIT}\}$, two rows, not three.
- **Join** $J_p(R, S)$: combines tuples of $R$ and $S$ that agree on the last $p$ components of the tuples of $R$ and the first $p$ components of $S$.
- **Union, intersection and difference** of two relations of the same degree behave as for sets.

```python
STUDENT = [(1, "Asha", "BCA"), (2, "Bikash", "BCA"), (3, "Chitra", "BIT")]
MARKS = [(1, "Math", 78), (1, "Java", 85), (3, "Math", 64)]
select = [t for t in STUDENT if t[2] == "BCA"]
project = sorted({t[2] for t in STUDENT})
join = [(s[0], s[1], m[1], m[2]) for s in STUDENT for m in MARKS if s[0] == m[0]]
print("select BCA:", select)
print("project Programme:", project)
print("join on Roll:")
for row in join:
    print("  ", row)
```
```output
select BCA: [(1, 'Asha', 'BCA'), (2, 'Bikash', 'BCA')]
project Programme: ['BCA', 'BIT']
join on Roll:
   (1, 'Asha', 'Math', 78)
   (1, 'Asha', 'Java', 85)
   (3, 'Chitra', 'Math', 64)
```
Notice that Bikash has no marks, so he does not appear in the join: an ordinary (inner) join keeps only tuples that match on both sides. The same three operations are the core of SQL: `WHERE` is selection, the column list of `SELECT` is projection, and `JOIN` is join.

## 7.3 Well-ordering, strong induction and the correctness of recursive algorithms

### The well-ordering property

**Well-ordering property:** every non-empty set of non-negative integers has a **least element**. It looks obvious, but it is equivalent to induction (each can be proved from the other) and it gives a proof style of its own: to prove that a property holds for all $n \ge 0$, assume the set $S$ of integers for which it fails is non-empty, take its least element $m$, and derive a contradiction.

::: example Worked example: every integer $n \ge 2$ is a product of primes (by well-ordering)
Suppose some integer $\ge 2$ is not a product of primes. By well-ordering there is a **smallest** such integer $m$. It is not prime (a prime is a product of one prime), so $m = ab$ with $2 \le a, b < m$. Because $m$ is the smallest failure, both $a$ and $b$ are products of primes, so $m = ab$ is also a product of primes. This contradicts the choice of $m$, so no failure exists. (The same statement is proved by strong induction in Unit 4: assume it for all $k$ with $2 \le k < n$, then split $n$.)
:::

**Strong induction** differs from simple induction only in the hypothesis: to prove $P(n+1)$ we may assume $P(k)$ for **all** $k \le n$, not only $P(n)$. Use it when a case depends on a much smaller case, as with the factorisation above, with postage stamps ("every amount of at least 12 rupees can be made from 4-rupee and 5-rupee stamps": the base cases are 12, 13, 14, 15 and the step uses $P(n-3)$), and with recursive algorithms that split a problem into unequal parts.

```python
# stamps: which amounts 12..60 can be made with 4s and 5s? (exhaustive check; the proof by strong induction covers all n)
ok = lambda n: any((n - 4 * a) >= 0 and (n - 4 * a) % 5 == 0 for a in range(n // 4 + 1))
print("all of 12..60 possible:", all(ok(n) for n in range(12, 61)), "  impossible below 12:", [n for n in range(1, 12) if not ok(n)])
```
```output
all of 12..60 possible: True   impossible below 12: [1, 2, 3, 6, 7, 11]
```
### Proving a recursive algorithm correct

To prove that a recursive algorithm is correct we use **induction on the size of the input**: (1) show that the **base case** returns the right answer; (2) assume the recursive call returns the correct answer for smaller inputs (the induction hypothesis) and show that the step combines it into the correct answer for the current input. Termination is part of the proof: the argument to the recursive call must move toward the base case.

::: example Worked example: fast exponentiation
```
power(a, n):                # a real, n >= 0 integer
    if n == 0: return 1
    if n is even: return power(a, n/2) ** 2
    return a * power(a, n-1)
```
*Claim:* `power(a, n)` returns $a^n$ for all $n \ge 0$. *Proof by strong induction on $n$.* **Base** $n = 0$: returns $1 = a^0$. **Step**: assume the claim for all smaller exponents. If $n$ is even and positive, $n/2 < n$ so `power(a, n/2)` $= a^{n/2}$ and its square is $a^n$. If $n$ is odd, $n - 1 < n$ so the call returns $a^{n-1}$ and $a \cdot a^{n-1} = a^n$. The exponent decreases at every call, so the algorithm terminates. $\blacksquare$ The number of multiplications is about $\log_2 n$, not $n$.
:::

```python
calls = 0
def power(a, n):
    global calls
    calls += 1
    if n == 0:
        return 1
    if n % 2 == 0:
        return power(a, n // 2) ** 2
    return a * power(a, n - 1)
print(power(3, 13), 3 ** 13, "calls:", calls)
print("agrees for n = 0..40:", all(power(2, n) == 2 ** n for n in range(41)))
```
```output
1594323 1594323 calls: 7
agrees for n = 0..40: True
```
The same pattern proves the recursive $\gcd$: **Base** $\gcd(a, 0) = a$; **Step** $\gcd(a, b) = \gcd(b, a \bmod b)$ because $a$ and $b$ have the same common divisors as $b$ and $a \bmod b$, and the second argument strictly decreases, so the algorithm ends.

## 7.4 Integer representations and the algorithms of arithmetic

### Base-$b$ expansions

For an integer base $b \ge 2$, every positive integer has a unique expansion $n = a_k b^k + \dots + a_1 b + a_0$ with digits $0 \le a_i < b$. Computers use base 2, and base 8 and 16 as shorthand because $8 = 2^3$ and $16 = 2^4$: one octal digit is three bits, one hexadecimal digit is four bits.

**Conversion from decimal** by repeated division: divide by $b$, record the remainder, repeat with the quotient until it is $0$; the remainders read from last to first are the digits.

*Example:* convert $(1234)_{10}$ to base 2, 8 and 16.

```python
def to_base(n, b):
    digits = "0123456789ABCDEF"
    out = []
    while n:
        n, r = divmod(n, b)
        out.append(digits[r])
        print(f"  quotient {n}, remainder {r}")
    return "".join(reversed(out)) or "0"
print("base 16 steps:")
h = to_base(1234, 16)
print("(1234) in base 2 =", bin(1234)[2:], " base 8 =", oct(1234)[2:], " base 16 =", h)
print("bits grouped in fours:", " ".join(bin(1234)[2:].zfill(12)[i:i + 4] for i in range(0, 12, 4)))
```
```output
base 16 steps:
  quotient 77, remainder 2
  quotient 4, remainder 13
  quotient 0, remainder 4
(1234) in base 2 = 10011010010  base 8 = 2322  base 16 = 4D2
bits grouped in fours: 0100 1101 0010
```
*Binary to hexadecimal:* group bits in fours from the right. $10011010010 \to 0100\ 1101\ 0010 = 4\text{D}2$. *Binary to octal:* group in threes, $010\ 011\ 010\ 010 = 2322$.

### Algorithms for the four operations

- **Addition** of two $n$-bit numbers: add column by column with a carry; each column gives a sum bit $(a_j + b_j + c) \bmod 2$ and a new carry $\lfloor (a_j + b_j + c)/2 \rfloor$. The cost is $O(n)$ bit operations, and it is exactly what a ripple-carry adder circuit does.
- **Multiplication** by shift and add: for each bit $b_j = 1$ of the multiplier add the multiplicand shifted left by $j$. The cost is $O(n^2)$ bit operations for $n$-bit numbers.
- **Division with remainder** (the division algorithm): find $q$ and $r$ with $a = dq + r$, $0 \le r < d$, by repeated subtraction or by long division; $q = \lfloor a/d \rfloor$ and $r = a \bmod d$.
- **Modular exponentiation** $b^n \bmod m$ by repeated squaring uses the binary digits of $n$ and keeps every intermediate number below $m$. It makes RSA practical (Unit 6).

```python
def modexp(b, n, m):
    result, base, steps = 1, b % m, 0
    for bit in bin(n)[2:][::-1]:
        if bit == "1":
            result = (result * base) % m
        base = (base * base) % m
        steps += 1
    return result, steps
print("3^200 mod 13 =", modexp(3, 200, 13)[0], " (pow check:", pow(3, 200, 13), ") using", modexp(3, 200, 13)[1], "squarings")
print("7^644 mod 645 =", modexp(7, 644, 645)[0], " (a Fermat test: 645 = 3*5*43 is composite, and the result is not 1)")
```
```output
3^200 mod 13 = 9  (pow check: 9 ) using 8 squarings
7^644 mod 645 = 436  (a Fermat test: 645 = 3*5*43 is composite, and the result is not 1)
```
**Large integers.** A computer word holds 32 or 64 bits, so a larger number (the 600-digit moduli of RSA) is stored as an **array of words** and added and multiplied word by word with carries. For a very large modulus, arithmetic is done modulo several pairwise relatively prime small moduli and reassembled with the **Chinese remainder theorem** (Unit 6), which is faster than direct arithmetic on huge numbers and is also the usual speed-up in RSA decryption.

## 7.5 Counting objects that are not all different, and generating permutations

### Permutations with indistinguishable objects

If $n$ objects contain $n_1$ of type 1, $n_2$ of type 2, ..., $n_k$ of type $k$ (so $n_1 + \dots + n_k = n$), the number of different arrangements is
$$\frac{n!}{n_1!\,n_2!\cdots n_k!}.$$
The reason: arranging the objects as if they were different gives $n!$, and each real arrangement is counted $n_1! \cdots n_k!$ times, once for every reordering of identical objects among themselves.

*Examples.* The word **SUCCESS** has 7 letters: S three times, C twice, U and E once: $7!/(3!\,2!\,1!\,1!) = 5040/12 = 420$. The word **MISSISSIPPI** has 11 letters (I four, S four, P two, M one): $11!/(4!\,4!\,2!\,1!) = 39{,}916{,}800/1{,}152 = 34{,}650$.

```python
from math import factorial as f
print("SUCCESS:", f(7) // (f(3) * f(2)), "  MISSISSIPPI:", f(11) // (f(4) * f(4) * f(2)))
from itertools import permutations
print("brute force SUCCESS:", len(set(permutations("SUCCESS"))))
```
```output
SUCCESS: 420   MISSISSIPPI: 34650
brute force SUCCESS: 420
```
The combination count is a special case: arranging $r$ ones and $n - r$ zeros gives $n!/(r!(n-r)!) = \binom{n}{r}$, which is also the number of shortest grid paths from $(0,0)$ to $(r, n - r)$.

### Distributing identical objects: combinations with repetition

Choosing $r$ objects from $n$ types with repetition allowed, or putting $r$ identical balls into $n$ distinct boxes, can be done in $\binom{n + r - 1}{r}$ ways ("stars and bars": $r$ stars and $n - 1$ bars). For example, 10 identical Rs 100 notes shared among 4 people: $\binom{13}{10} = 286$ ways.

### Generating the next permutation in lexicographic order

Lexicographic (dictionary) order lists permutations of $1..n$ as numbers: 123, 132, 213, ... The rule to find the **next permutation** $a_1 a_2 \dots a_n$ is:

1. Find the largest $j$ with $a_j < a_{j+1}$. (If none exists the permutation is the last one.)
2. Find the smallest $a_k$ to the right of $a_j$ with $a_k > a_j$ (the last such position, since the tail is decreasing), and swap $a_j$ and $a_k$.
3. Reverse the tail $a_{j+1} \dots a_n$.

::: example Worked example: the permutation after 362541 (a past board question)
Step 1: scanning from the right, $4 > 1$, $5 > 4$, then $2 < 5$, so $j$ is the position of 2 (the 3rd digit). Step 2: to the right of 2 the digits are 5, 4, 1; the smallest digit greater than 2 is **4**. Swap 2 and 4: $364\,521$. Step 3: reverse the tail after position $j$: $521 \to 125$. The next permutation is **364125**.
:::

```python
def next_perm(a):
    a = list(a)
    j = len(a) - 2
    while j >= 0 and a[j] > a[j + 1]:
        j -= 1
    if j < 0:
        return None
    k = len(a) - 1
    while a[k] < a[j]:
        k -= 1
    a[j], a[k] = a[k], a[j]
    a[j + 1:] = reversed(a[j + 1:])
    return "".join(a)
print(next_perm("362541"))
x, seq = "1234", []
while x:
    seq.append(x)
    x = next_perm(x)
print(len(seq), "permutations; first five:", seq[:5], " last:", seq[-1])
```
```output
364125
24 permutations; first five: ['1234', '1243', '1324', '1342', '1423']  last: 4321
```
**Generating combinations.** To list the $r$-element subsets of $\{1, \dots, n\}$ in lexicographic order, find the last element $a_i$ of the current subset with $a_i \ne n - r + i$, replace it by $a_i + 1$, and set each later element $a_j = a_i + j - i$. Starting from $\{1, 2, 3\}$ with $n = 5$, the sequence is 123, 124, 125, 134, 135, 145, 234, 235, 245, 345: ten subsets, equal to $\binom{5}{3} = 10$.

```python
from itertools import combinations
print(["".join(map(str, c)) for c in combinations(range(1, 6), 3)])
```
```output
['123', '124', '125', '134', '135', '145', '234', '235', '245', '345']
```
## 7.6 Discrete probability

Unit 3 introduced counting and basic probability. The outline asks for the full set of tools.

### Finite probability, complements and unions

An **experiment** has a **sample space** $S$ of possible outcomes; an **event** $E$ is a subset of $S$. If all outcomes are equally likely, $P(E) = |E|/|S|$. In general, $0 \le P(E) \le 1$ and the probabilities of all outcomes add up to 1. Two rules follow.

- **Complement:** $P(\bar{E}) = 1 - P(E)$. It is often easier to count the opposite event ("at least one" is $1 -$ "none").
- **Union:** $P(E_1 \cup E_2) = P(E_1) + P(E_2) - P(E_1 \cap E_2)$, the inclusion-exclusion principle for probabilities. For mutually exclusive events the last term is $0$.

*Example:* two dice are rolled. $P(\text{sum} = 7) = 6/36 = 1/6$. $P(\text{at least one six}) = 1 - (5/6)^2 = 11/36$. $P(\text{sum is even or at least one die shows 6})$: even sum has 18 outcomes, at least one six has 11, both: $(2,6),(6,2),(4,6),(6,4),(6,6)$ = 5, so $(18 + 11 - 5)/36 = 24/36 = 2/3$.

### Conditional probability, independence and Bayes' theorem

The probability of $E$ given that $F$ has happened is $P(E \mid F) = P(E \cap F)/P(F)$ for $P(F) > 0$. Events are **independent** if $P(E \cap F) = P(E)\,P(F)$, which is the same as $P(E \mid F) = P(E)$. **Bayes' theorem** reverses a conditional probability:
$$P(F \mid E) = \frac{P(E \mid F)\,P(F)}{P(E \mid F)\,P(F) + P(E \mid \bar{F})\,P(\bar{F})}.$$

::: example Worked example: a spam filter
Suppose 20 percent of incoming mail is spam. The word "prize" appears in 60 percent of spam and in 2 percent of genuine mail. A message contains "prize". What is the probability that it is spam?
$P(\text{spam}) = 0.20$, $P(\text{prize} \mid \text{spam}) = 0.60$, $P(\text{prize} \mid \text{not spam}) = 0.02$.
$P(\text{spam} \mid \text{prize}) = \dfrac{0.60 \times 0.20}{0.60 \times 0.20 + 0.02 \times 0.80} = \dfrac{0.120}{0.136} = 0.882$.
The word raises the probability from 20 percent to about 88 percent; this is the core of the naive Bayes classifier.
:::

### Random variables, expected value and variance

A **random variable** $X$ is a function from the sample space to the real numbers (for example, the sum of two dice). Its **distribution** lists $P(X = x)$ for each value. The **expected value** (mean) is $E(X) = \sum x\,P(X = x)$. It is **linear**: $E(X + Y) = E(X) + E(Y)$ always, even when $X$ and $Y$ are dependent. The **variance** measures spread: $V(X) = E(X^2) - E(X)^2$, and the standard deviation is $\sqrt{V(X)}$. For independent variables $V(X + Y) = V(X) + V(Y)$.

```python
from itertools import product
from fractions import Fraction as F
rolls = [a + b for a, b in product(range(1, 7), repeat=2)]
EX = F(sum(rolls), 36)
EX2 = F(sum(r * r for r in rolls), 36)
print("E(sum of two dice) =", EX, " V =", EX2 - EX ** 2, " = about", round(float(EX2 - EX ** 2), 4))
# one die: E=7/2, V=35/12 ; two independent dice: V doubles
print("one die V =", F(35, 12), " two dice V =", 2 * F(35, 12))
# Bayes: spam filter
p = 0.6 * 0.2 / (0.6 * 0.2 + 0.02 * 0.8)
print("P(spam | prize) =", round(p, 3))
```
```output
E(sum of two dice) = 7  V = 35/6  = about 5.8333
one die V = 35/12  two dice V = 35/6
P(spam | prize) = 0.882
```
A **Bernoulli trial** has two outcomes (success with probability $p$). The number of successes in $n$ independent trials is **binomial**: $P(X = k) = \binom{n}{k}p^k(1-p)^{n-k}$, with $E(X) = np$ and $V(X) = np(1-p)$.

### Randomized algorithms and hashing

A **randomized algorithm** makes random choices during execution. A **Monte Carlo** algorithm may give a wrong answer with a small, controllable probability (the Miller-Rabin primality test, whose error falls by a factor of at least 4 for each independent round); a **Las Vegas** algorithm is always correct but its running time is random (randomised quicksort, with expected $O(n \log n)$ time for every input because the pivot is chosen at random).

**Probability in hashing.** A hash function maps $n$ keys into $m$ slots. If every slot is equally likely, the probability that **no collision** occurs among $n$ keys is $\dfrac{m(m-1)\cdots(m-n+1)}{m^n}$. The **birthday problem** is the case $m = 365$: with only 23 people the probability that two share a birthday exceeds one half. The same computation says that a table with 1,000 slots will probably have a collision after about 38 keys, long before it is full, so collisions must always be handled (chaining or open addressing). In **chaining** with load factor $\alpha = n/m$, the expected length of a chain is $\alpha$, so an unsuccessful search costs about $1 + \alpha$ steps on average.

```python
def no_collision(n, m):
    p = 1.0
    for i in range(n):
        p *= (m - i) / m
    return p
print("365 slots: P(no collision) with 23 people =", round(no_collision(23, 365), 4), " -> P(collision) =", round(1 - no_collision(23, 365), 4))
n = next(n for n in range(1, 1000) if no_collision(n, 1000) < 0.5)
print("1000 slots: collision more likely than not after", n, "keys")
```
```output
365 slots: P(no collision) with 23 people = 0.4927  -> P(collision) = 0.5073
1000 slots: collision more likely than not after 38 keys
```
## 7.7 Graph models, isomorphism, matching and the travelling salesman problem

### Graph models

Most real structures are graphs once the **vertices** and **edges** are chosen. A **social network** has people as vertices and friendships as undirected edges (the degree of a vertex is the number of friends). A **communication network** has computers or routers as vertices and links as edges, directed if traffic is one way. An **information network** is the web: pages as vertices and hyperlinks as directed edges (a page's in-degree is how many pages link to it, the basis of ranking). In **software design** the vertices are modules and a directed edge $A \to B$ means that $A$ calls $B$; a cycle shows a circular dependency. A **transportation network** has places as vertices and roads, flights or routes as weighted edges. In a **biological network** the vertices are species, genes or proteins and the edges are interactions such as "eats" or "activates".

Graph types: a **simple graph** has no loops and no parallel edges; a **multigraph** allows parallel edges; a **pseudograph** also allows loops; a **directed graph** gives each edge a direction; a **mixed graph** has both directed and undirected edges. A **tournament** is a directed graph in which every pair of vertices is joined by exactly one directed edge (a round-robin contest in which each pair plays once and the edge points from winner to loser); a tournament on $n$ vertices has $n(n-1)/2$ edges, and the scores (out-degrees) always add up to that number.

### Special simple graphs

The **complete graph** $K_n$ has $n(n-1)/2$ edges. The **cycle** $C_n$ ($n \ge 3$) has $n$ vertices and $n$ edges. The **wheel** $W_n$ adds a hub joined to every vertex of $C_n$ and has $2n$ edges. The **n-cube** $Q_n$ has $2^n$ vertices (the $n$-bit strings), with an edge between strings that differ in exactly one bit, so each vertex has degree $n$ and there are $n\,2^{n-1}$ edges; $Q_3$ is the ordinary cube. A **bipartite graph** has vertices that split into two sets with every edge joining the two sets (equivalent to having no odd cycle, and to being 2-colourable); $K_{m,n}$ has $mn$ edges.

```svgfig label="7.1" caption="The 3-cube Q3. Its 8 vertices are the 3-bit strings, and two vertices are joined exactly when their labels differ in one bit, so every vertex has degree 3 and there are 8 x 3 / 2 = 12 edges. Q3 is bipartite: the strings with an even number of ones (000, 011, 101, 110) form one side and those with an odd number the other."
f = Fig(580, 230)
V = {"000": (190, 190), "100": (320, 190), "110": (320, 100), "010": (190, 100),
     "001": (240, 150), "101": (370, 150), "111": (370, 60), "011": (240, 60)}
for a in V:
    for b in V:
        if a < b and sum(x != y for x, y in zip(a, b)) == 1:
            f.line(V[a][0], V[a][1], V[b][0], V[b][1], color=SLATE, sw=1.6)
for k, (x, y) in V.items():
    even = k.count("1") % 2 == 0
    f.circle(x, y, 7, fill=NAVY if even else AMBER, stroke=NAVY)
off = {"000": (-22, 6), "100": (22, 6), "110": (24, 0), "010": (-24, 0), "001": (-4, 18), "101": (24, 6), "111": (24, -4), "011": (-24, -4)}
for k, (x, y) in V.items():
    f.text(x + off[k][0], y + off[k][1], k, size=10, color=NAVY, bold=True)
f.text(480, 110, "dark: even number of ones", size=10, color=NAVY)
f.text(480, 128, "amber: odd number of ones", size=10, color=AMBER)
```

### Graph isomorphism

Two simple graphs $G_1$ and $G_2$ are **isomorphic** if there is a one-to-one and onto function $f$ between their vertices such that $a$ and $b$ are adjacent in $G_1$ exactly when $f(a)$ and $f(b)$ are adjacent in $G_2$. The graphs are the same structure drawn differently. Isomorphic graphs must agree on every **invariant**: the number of vertices, number of edges, degree sequence, number of cycles of each length, and connectedness. If one invariant differs the graphs are **not** isomorphic; if all agree you must still find the mapping, since no known invariant list is both easy and complete.

::: example Worked example: are these two graphs isomorphic?
$G_1$: vertices $a, b, c, d$ with edges $ab, bc, cd, da, ac$. $G_2$: vertices $1, 2, 3, 4$ with edges $12, 23, 34, 41, 13$. Both have 4 vertices, 5 edges and degree sequence $(3, 3, 2, 2)$. Map $a \to 1$, $b \to 2$, $c \to 3$, $d \to 4$: the edges map to $12, 23, 34, 41, 13$, which are exactly the edges of $G_2$. So they are isomorphic. By contrast, two graphs with degree sequences $(4, 2, 2, 1, 1)$ and $(3, 3, 2, 1, 1)$ cannot be isomorphic, because the sequences differ.
:::

```python
from itertools import permutations
E1 = {frozenset(e) for e in ["ab", "bc", "cd", "da", "ac"]}
E2 = {frozenset(e) for e in ["12", "23", "34", "41", "13"]}
found = [p for p in permutations("1234") if {frozenset(p["abcd".index(x)] for x in e) for e in E1} == E2]
print("isomorphisms found:", len(found), " e.g. a,b,c,d ->", found[0])
```
```output
isomorphisms found: 4  e.g. a,b,c,d -> ('1', '2', '3', '4')
```
### Matching theory

A **matching** in a graph is a set of edges no two of which share a vertex. A **maximum matching** has the greatest possible number of edges, and a **perfect matching** covers every vertex. In a bipartite graph with job-seekers on one side and jobs on the other, a matching is an assignment of people to jobs they can do. **Hall's marriage theorem:** a bipartite graph with parts $X$ and $Y$ has a matching that covers every vertex of $X$ if and only if every subset $S \subseteq X$ is adjacent to at least $|S|$ vertices of $Y$. A maximum matching is found by an **augmenting path** search: start from any matching, look for a path that alternates between unmatched and matched edges and starts and ends at unmatched vertices; flipping it enlarges the matching by one; stop when no augmenting path exists.

*Example:* applicants A, B, C can do jobs {1, 2}, {1}, {2, 3}. B must take job 1; then A must take 2; then C takes 3. The perfect matching is $A\!-\!2$, $B\!-\!1$, $C\!-\!3$. Hall's condition holds: $\{A,B\}$ has neighbours $\{1,2\}$ (2 vertices) and $\{A,B,C\}$ has $\{1,2,3\}$ (3).

```svgfig label="7.2" caption="Matching applicants to jobs. Thin lines show who can do which job; thick lines are the perfect matching found by following the forced choices: B can only take job 1, which forces A to take job 2, which leaves job 3 for C."
f = Fig(580, 190)
ys = {"A": 40, "B": 95, "C": 150}
js = {"1": 40, "2": 95, "3": 150}
for a, jobs in (("A", "12"), ("B", "1"), ("C", "23")):
    for j in jobs:
        f.line(200, ys[a], 380, js[j], color=SLATE, sw=1.2)
for a, j in (("A", "2"), ("B", "1"), ("C", "3")):
    f.line(200, ys[a], 380, js[j], color=TEAL, sw=4)
for a, y in ys.items():
    f.circle(200, y, 14, fill=BLUE, stroke=NAVY, label=a, size=11)
for j, y in js.items():
    f.circle(380, y, 14, fill=SAND, stroke=AMBER, label=j, size=11)
f.text(200, 14, "applicants", size=10.5, color=NAVY, bold=True)
f.text(380, 14, "jobs", size=10.5, color=AMBER, bold=True)
```

### The travelling salesman problem

A salesman must visit every city once and return home, with the least total distance: this is the minimum-weight **Hamilton circuit** in a complete weighted graph. For $n$ cities there are $(n-1)!/2$ distinct circuits, so brute force is practical only for small $n$ ($n = 10$ gives 181,440 circuits; $n = 20$ gives about $6 \times 10^{16}$). No fast exact algorithm is known, and the decision form is NP-complete. Practical methods are heuristics: the **nearest-neighbour** rule (always go to the closest unvisited city) and improvement by swapping edges.

```python
from itertools import permutations
from math import factorial
D = {("A","B"):10, ("A","C"):15, ("A","D"):20, ("B","C"):35, ("B","D"):25, ("C","D"):30}
d = lambda x, y: D.get((x, y)) or D[(y, x)]
best = min(permutations("BCD"), key=lambda p: d("A", p[0]) + d(p[0], p[1]) + d(p[1], p[2]) + d(p[2], "A"))
cost = lambda p: d("A", p[0]) + d(p[0], p[1]) + d(p[1], p[2]) + d(p[2], "A")
print("best tour: A", " ".join(best), "A  cost", cost(best), "  circuits:", factorial(3) // 2)
print("n = 10 circuits:", factorial(9) // 2, "  n = 20:", f"{factorial(19) // 2:.2e}")
```
```output
best tour: A B D C A  cost 80   circuits: 3
n = 10 circuits: 181440   n = 20: 6.08e+16
```
## Key facts at a glance

| Topic | Remember |
|---|---|
| Vacuous / trivial proof | hypothesis false / conclusion true; the implication is then true |
| Uniqueness proof | assume two objects with the property and show they are equal |
| Floor, ceiling | $\lceil x \rceil = -\lfloor -x \rfloor$; bytes for $b$ bits is $\lceil b/8 \rceil$ |
| Boolean functions | $2^{2^n}$ functions of degree $n$; sum of products from the 1-rows |
| n-ary relation operations | selection (rows), projection (columns), join (match on shared fields) |
| Well-ordering | every non-empty set of non-negative integers has a least element |
| Recursive correctness | base case plus induction on input size, plus termination |
| Base conversion | divide by $b$, read remainders upward; group bits in 3s (octal) or 4s (hex) |
| Indistinguishable objects | $n!/(n_1!\cdots n_k!)$; with repetition $\binom{n+r-1}{r}$ |
| Next permutation | rightmost ascent $j$, swap with next larger on the right, reverse the tail |
| Probability | $P(\bar{E}) = 1 - P(E)$; Bayes; $E(X)$ linear; $V = E(X^2) - E(X)^2$ |
| Hashing | no-collision probability $m(m-1)\cdots(m-n+1)/m^n$; birthday 23 of 365 |
| Graph models | vertices and edges chosen to fit the problem; isomorphism needs equal invariants plus a mapping |
| Matching | Hall's condition; augmenting paths; TSP has $(n-1)!/2$ tours |

## Chapter summary

- Vacuous and trivial proofs, proofs by cases, existence and uniqueness proofs and counterexamples complete the proof toolbox; the common mistakes are the converse and inverse errors, circular reasoning and division by zero.
- Floor and ceiling convert real numbers to integers; Boolean functions are maps from bit strings to bits; n-ary relations are the mathematics of database tables with selection, projection and join.
- Well-ordering is equivalent to induction, and recursive algorithms are proved correct by induction on the input size.
- Integers are stored in base 2 and written in base 8 or 16; arithmetic uses carry, shift-and-add, division with remainder and repeated squaring.
- Arrangements with identical objects divide by the factorials of the repeats; next-permutation and combination generation list objects in lexicographic order.
- Probability adds conditional probability, Bayes' theorem, expectation, variance, randomized algorithms and the hashing collision analysis.
- Graphs model many real systems; isomorphism, matching and the travelling salesman problem show where graph questions become easy or hard.

## Practice

1. Prove that "if $n$ is an integer with $n > 5$ and $n < 3$, then $n^2 = 100$" is true. Which kind of proof is this?
2. Prove that for every integer $n$, $n^2 + n$ is even, by cases.
3. Show that the equation $3x - 7 = 11$ has exactly one real solution (existence and uniqueness).
4. Find the flaw: "Let $a = b$. Then $a^2 = ab$, $a^2 - b^2 = ab - b^2$, $(a + b)(a - b) = b(a - b)$, so $a + b = b$, so $2b = b$ and $2 = 1$."
5. Evaluate $\lfloor -2.3 \rfloor$, $\lceil -2.3 \rceil$, $\lfloor 7.9 \rfloor$, $\lceil 7.1 \rceil$. How many 4 KB pages are needed for a file of 10,500 bytes?
6. Define a Boolean function. Write the truth table and the sum-of-products form of $f(x, y) = x \oplus y$. How many Boolean functions of degree 4 exist?
7. For STUDENT = $\{(1,\text{Asha},\text{BCA}), (2,\text{Bikash},\text{BCA}), (3,\text{Chitra},\text{BIT})\}$ give $\sigma_{\text{Programme}=\text{BIT}}$ and $\pi_{\text{Programme}}$. Explain what a primary key is.
8. Prove by well-ordering that there is no integer strictly between 0 and 1.
9. Prove that `power(a, n)` in 7.3 is correct and count the multiplications for $n = 13$.
10. Convert $(2025)_{10}$ to binary and hexadecimal, and $(\text{1AF})_{16}$ to decimal and binary. Compute $5^{13} \bmod 17$ by repeated squaring.
11. How many different arrangements of the letters of BANANA are there? Of the word BOOKKEEPER?
12. In how many ways can 8 identical laptops be distributed among 3 labs?
13. Find the permutation that follows 2 3 6 5 4 1 in lexicographic order, and list all 3-element subsets of $\{1,2,3,4\}$.
14. A bag has 3 red and 2 blue balls. Two are drawn without replacement. Find $P(\text{both red})$, $P(\text{second red} \mid \text{first red})$ and $E(\text{number of red})$.
15. A disease affects 1 percent of people; a test detects it in 95 percent of patients and gives a false alarm for 5 percent of healthy people. A person tests positive; find the probability of disease.
16. Explain the birthday problem and why it matters for hash tables. A table has 100 slots; give the no-collision probability formula for 3 keys.
17. Are the graphs with edge sets $\{12, 23, 34, 41\}$ and $\{ab, bc, cd, da\}$ isomorphic? Show an invariant and a mapping. Draw $Q_3$ and give its number of vertices and edges.
18. Four applicants P, Q, R, S can do jobs {1,2}, {1,3}, {2}, {3,4}. Find a perfect matching or use Hall's theorem to show none exists.
19. Why is the travelling salesman problem hard? Find the best tour for 4 cities with distances AB = 10, AC = 15, AD = 20, BC = 35, BD = 25, CD = 30.

::: note Answers and worked solutions
**1.** The hypothesis "$n > 5$ and $n < 3$" is false for every $n$, so the implication is true. It is a **vacuous proof**.
**2.** Even $n$: $n^2$ and $n$ are both even, sum even. Odd $n$: $n^2$ and $n$ are both odd, and odd + odd is even. Every integer is even or odd, so the claim holds.
**3.** Existence: $x = 6$ gives $18 - 7 = 11$. Uniqueness: if $3x - 7 = 11$ and $3y - 7 = 11$ then $3x = 3y$ and $x = y$.
**4.** The step "divide both sides by $a - b$" divides by $0$ because $a = b$.
**5.** $-3$, $-2$, $7$, $8$. Pages: $\lceil 10500/4096 \rceil = \lceil 2.56 \rceil = 3$.
**6.** A function $\{0,1\}^n \to \{0,1\}$. XOR is 1 for $01$ and $10$: $f = \bar{x}y + x\bar{y}$. Degree 4: $2^{16} = 65{,}536$.
**7.** $\sigma$ gives $\{(3, \text{Chitra}, \text{BIT})\}$; $\pi_{\text{Programme}} = \{\text{BCA}, \text{BIT}\}$. A primary key is an attribute whose value identifies each tuple uniquely, here Roll.
**8.** Suppose the set $S$ of integers $m$ with $0 < m < 1$ is non-empty. By well-ordering $S$ has a least element $m$. Multiplying $0 < m < 1$ by $m > 0$ gives $0 < m^2 < m < 1$, and $m^2$ is an integer, so $m^2 \in S$ and is smaller than $m$: a contradiction. Hence $S$ is empty.
**9.** See 7.3. For $n = 13$: 13 is odd, then 12, 6, 3 (odd), 2, 1 (odd), 0; the program in 7.3 reports 7 calls, so there are 6 multiplications or squarings after the base case.
**10.** $2025 = 11111101001_2 = 7\text{E}9_{16}$. $(\text{1AF})_{16} = 256 + 160 + 15 = 431$, and in binary $0001\ 1010\ 1111$. $5^{13} \bmod 17$: $5^2 = 8$, $5^4 = 64 \bmod 17 = 13$, $5^8 = 169 \bmod 17 = 16$; $13 = 8 + 4 + 1$, so $16 \times 13 \times 5 = 1040 \bmod 17 = 3$ (since $17 \times 61 = 1037$).
**11.** BANANA: $6!/(3!\,2!\,1!) = 60$. BOOKKEEPER: letters B1, O2, K2, E3, P1, R1 total 10: $10!/(2!\,2!\,3!) = 3{,}628{,}800/24 = 151{,}200$.
**12.** $\binom{8 + 3 - 1}{8} = \binom{10}{8} = 45$.
**13.** After 236541 comes **241356**: the rightmost ascent is $3 < 6$ at position 2; the smallest larger digit on the right is 4; swap to get 246531, then reverse the tail 6531 to 1356, giving 241356. The 3-subsets of $\{1,2,3,4\}$: 123, 124, 134, 234.
**14.** $P(\text{both red}) = \frac{3}{5} \cdot \frac{2}{4} = \frac{3}{10}$. $P(\text{second red} \mid \text{first red}) = \frac{2}{4} = \frac12$. $E = 2 \cdot \frac{3}{5} = 1.2$ by linearity.
**15.** $P(D \mid +) = \dfrac{0.95 \times 0.01}{0.95 \times 0.01 + 0.05 \times 0.99} = \dfrac{0.0095}{0.0590} = 0.161$, only about 16 percent, because the disease is rare.
**16.** In a group of 23 people two share a birthday with probability above one half, because the number of pairs grows fast; likewise collisions in a hash table appear long before it is full. For 3 keys in 100 slots: $\frac{100 \cdot 99 \cdot 98}{100^3} = 0.9702$.
**17.** Both are 4-cycles with 4 vertices, 4 edges and degree sequence $(2,2,2,2)$; map $1 \to a$, $2 \to b$, $3 \to c$, $4 \to d$. $Q_3$ has $2^3 = 8$ vertices and $3 \cdot 2^2 = 12$ edges.
**18.** R must take 2; P must then take 1; Q must take 3; S takes 4. Matching $P\!-\!1$, $Q\!-\!3$, $R\!-\!2$, $S\!-\!4$ is perfect.
**19.** The number of tours grows as $(n-1)!/2$ and no polynomial exact algorithm is known. The 3 distinct tours from A are $A\,B\,C\,D\,A = 10 + 35 + 30 + 20 = 95$, $A\,B\,D\,C\,A = 10 + 25 + 30 + 15 = 80$, $A\,C\,B\,D\,A = 15 + 35 + 25 + 20 = 95$. The best is **A B D C A with cost 80**.
:::
