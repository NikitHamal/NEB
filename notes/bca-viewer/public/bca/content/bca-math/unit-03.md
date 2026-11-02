---
subject: Mathematics
grade: BCA
unit: 3
title: Sets, Relations and Functions
hours: 2
area: Algebra
---

Sets and functions give about two questions in the paper, and they are among the most predictable: a Venn-diagram word problem, a count of subsets or relations, the domain of a function, and a composite or inverse. The Dean's Office model asks "A − (B ∪ C)" and a 120-student maths/statistics problem. Learn the counting formulas and the vocabulary, and these are quick marks.

::: key What the paper asks from this chapter
- **Venn counting**: $n(A\cup B)=n(A)+n(B)-n(A\cap B)$ and its three-set form.
- **Counting**: subsets $2^n$, proper subsets $2^n-1$, $n(A\times B)=mn$, relations $2^{mn}$.
- **Laws**: De Morgan, $A-B=A\cap B'$, distributive laws.
- **Relations**: reflexive, symmetric, transitive, equivalence.
- **Functions**: one-one, onto, domain of $\sqrt{\ }$ and $\frac{1}{x}$, composite and inverse.
:::

## 3.1 Sets, subsets, operations and Venn-diagram word problems

- A set with $n$ elements has $2^n$ subsets, $2^n-1$ proper subsets, and $\binom{n}{r}$ subsets of exactly $r$ elements. The power set has $2^n$ elements.
- $A-B=A\cap B'$. $A\,\Delta\,B=(A-B)\cup(B-A)$ and $n(A\Delta B)=n(A)+n(B)-2n(A\cap B)$.
- **De Morgan**: $(A\cup B)'=A'\cap B'$, $(A\cap B)'=A'\cup B'$.
- **Distributive**: $A-(B\cup C)=(A-B)\cap(A-C)$ and $A-(B\cap C)=(A-B)\cup(A-C)$.
- $n(A\cup B\cup C)=n(A)+n(B)+n(C)-n(A\cap B)-n(B\cap C)-n(C\cap A)+n(A\cap B\cap C)$.
- $A\cup A'=U$, $A\cap A'=\varnothing$, and $A\subseteq B$ gives $A\cup B=B$ and $A\cap B=A$.

::: example Maths and statistics
**Problem.** Of 120 students, 90 take mathematics and 72 take statistics; 10 take neither. How many take both?

**Solution.** $n(M\cup S)=120-10=110$. Both $=90+72-110=52$.
:::

## 3.2 Relations and their types

- A relation from $A$ to $B$ is any subset of $A\times B$. If $n(A)=m$ and $n(B)=n$ there are $2^{mn}$ relations.
- On a set $A$: **reflexive** if $(a,a)\in R$ for all $a$; **symmetric** if $(a,b)\in R\Rightarrow(b,a)\in R$; **transitive** if $(a,b),(b,c)\in R\Rightarrow(a,c)\in R$; **equivalence** if all three.
- "$a$ divides $b$" on the positive integers is reflexive and transitive but not symmetric. "$=$" is an equivalence relation; "$<$" is only transitive.
- Domain = set of first coordinates; range = set of second coordinates that actually occur.

## 3.3 Functions, domain, range, composite and inverse functions

- A function from $A$ to $B$ gives every element of $A$ **exactly one** image. With $n(A)=m$, $n(B)=n$ there are $n^m$ functions and $\frac{n!}{(n-m)!}$ one-one functions ($m\le n$).
- **One-one**: different inputs, different outputs. **Onto**: range = codomain. **Bijective**: both.
- **Domain rules**: $\frac{1}{g(x)}$ needs $g(x)\ne0$; $\sqrt{g(x)}$ needs $g(x)\ge0$; $\log g(x)$ needs $g(x)>0$.
- **Composite**: $(f\circ g)(x)=f(g(x))$. In general $f\circ g\ne g\circ f$.
- **Inverse** exists only for a bijection: swap $x$ and $y$ and solve. If $f(x)=3x-6$ then $f^{-1}(x)=\frac{x+6}{3}$, and $f(f^{-1}(x))=x$.
- Even: $f(-x)=f(x)$ ($x^2$, $|x|$). Odd: $f(-x)=-f(x)$ ($x^3$, $\sin x$).

::: caution
$f(x)=x^2$ on $\mathrm{R}$ is neither one-one ($f(2)=f(-2)$) nor onto (no negative outputs). Check both before saying "bijective".
:::

## Formula and fact sheet

| Item | Result |
|---|---|
| Subsets / proper subsets | $2^n$ / $2^n-1$ |
| $n(A\times B)$ | $mn$ |
| Relations from $A$ to $B$ | $2^{mn}$ |
| Functions / one-one functions | $n^m$ / $\frac{n!}{(n-m)!}$ |
| $n(A\cup B)$ | $n(A)+n(B)-n(A\cap B)$ |
| De Morgan | $(A\cup B)'=A'\cap B'$ |

## Chapter summary

- Count with $n(A\cup B)=n(A)+n(B)-n(A\cap B)$; "neither" is the total minus the union.
- A set of $n$ elements has $2^n$ subsets, one of them the empty set.
- $A-B$ means $A\cap B'$.
- Equivalence = reflexive + symmetric + transitive.
- A function gives each input exactly one output; check one-one and onto separately.
- Domain: no zero denominators, no negative square roots, positive log arguments.
- To invert, swap $x$ and $y$; to compose, work from the inside out.

## Practice questions

**Set A — Recall (20 questions)**

1. The number of subsets of a set with 3 elements is
   (a) 6 (b) 8 (c) 9 (d) 3
2. If $n(A)=3$ and $n(B)=4$, then $n(A\times B)$ is
   (a) 7 (b) 1 (c) 81 (d) 12
3. $A-B$ equals
   (a) $A\cap B'$ (b) $A'\cap B$ (c) $A\cup B'$ (d) $A'\cup B$
4. By De Morgan's law, $(A\cup B)'$ equals
   (a) $A'\cup B'$ (b) $A\cap B$ (c) $A'\cap B'$ (d) $A\cup B'$
5. The number of proper subsets of $\{a,b,c\}$ is
   (a) 6 (b) 8 (c) 3 (d) 7
6. A relation that is reflexive, symmetric and transitive is called
   (a) a partial order (b) an equivalence relation (c) a function (d) an identity map
7. If $f(x)=2x+3$, then $f(4)$ is
   (a) 11 (b) 9 (c) 14 (d) 8
8. The domain of $f(x)=\frac{1}{x-2}$ is
   (a) all real numbers (b) $x>2$ (c) $\mathrm{R}-\{2\}$ (d) $x\ne-2$
9. If $f(x)=x^2$ and $g(x)=x+1$, then $(f\circ g)(2)$ is
   (a) 5 (b) 9 (c) 25 (d) 6
10. The inverse of $f(x)=3x-6$ is
    (a) $3x+6$ (b) $\frac{x-6}{3}$ (c) $\frac{x}{3}-6$ (d) $\frac{x+6}{3}$
11. If $n(A)=20$, $n(B)=15$ and $n(A\cap B)=5$, then $n(A\cup B)$ is
    (a) 30 (b) 35 (c) 40 (d) 25
12. Which of the following is the empty set?
    (a) $\{0\}$ (b) $\{\varnothing\}$ (c) $\{x\in\mathrm{R}: x^2=-1\}$ (d) $\{x: x=x\}$
13. $A\cap A'$ equals
    (a) $A$ (b) $U$ (c) $A'$ (d) $\varnothing$
14. The range of $f(x)=x^2$, $x\in\mathrm{R}$, is
    (a) $y\ge0$ (b) all real numbers (c) $y>0$ (d) $y\le0$
15. A function that is both one-one and onto is called
    (a) injective only (b) bijective (c) constant (d) identity only
16. If $A\subseteq B$, then $A\cup B$ equals
    (a) $A$ (b) $A\cap B$ (c) $B$ (d) $U$
17. The number of relations from a 2-element set to a 3-element set is
    (a) 64 (b) 36 (c) 8 (d) 9
18. The function $f(x)=x^3$ is
    (a) even (b) neither even nor odd (c) constant (d) odd
19. $A\cup A$ equals
    (a) $\varnothing$ (b) $A$ (c) $U$ (d) $A'$
20. The number of elements in the power set of a 4-element set is
    (a) 8 (b) 4 (c) 16 (d) 32

::: note Answers and explanations — Set A
**1.** (b) — 2³ = 8, including the empty set and the set itself.
**2.** (d) — n(A×B) = 3 × 4 = 12.
**3.** (a) — A − B keeps what is in A and not in B: A ∩ B′.
**4.** (c) — complement of a union is the intersection of complements.
**5.** (d) — 2³ − 1 = 7; only the set itself is excluded.
**6.** (b) — the three properties together define an equivalence relation.
**7.** (a) — 2(4) + 3 = 11.
**8.** (c) — the denominator vanishes only at x = 2.
**9.** (b) — g(2) = 3 and f(3) = 9. (f∘g) means g first.
**10.** (d) — y = 3x − 6 gives x = (y + 6)/3.
**11.** (a) — 20 + 15 − 5 = 30.
**12.** (c) — x² = −1 has no real solution. {0} and {∅} each have one element.
**13.** (d) — nothing is in both A and its complement.
**14.** (a) — squares are never negative, and 0 is attained.
**15.** (b) — one-one and onto together is bijective.
**16.** (c) — if A is inside B, joining adds nothing new.
**17.** (a) — subsets of a 6-element product: 2⁶ = 64.
**18.** (d) — (−x)³ = −x³.
**19.** (b) — idempotent law.
**20.** (c) — 2⁴ = 16.
:::

**Set B — Understanding (12 questions)**

1. Of 120 students, 90 take mathematics, 72 take statistics and 10 take neither. The number taking both is
   (a) 42 (b) 48 (c) 52 (d) 62
2. In a class of 40, 25 play football, 20 play cricket and 5 play neither. The number playing both is
   (a) 10 (b) 15 (c) 5 (d) 20
3. The domain of $f(x)=\sqrt{x-3}$ is
   (a) $x>3$ (b) $x\le3$ (c) all real numbers (d) $x\ge3$
4. If $f(x)=2x+1$ and $g(x)=x^2$, then $(f\circ g)(3)$ is
   (a) 7 (b) 19 (c) 49 (d) 13
5. The number of functions from a 3-element set to a 2-element set is
   (a) 8 (b) 9 (c) 6 (d) 5
6. $R=\{(1,1),(2,2),(3,3),(1,2)\}$ on $\{1,2,3\}$ is
   (a) symmetric only (b) an equivalence relation (c) reflexive and transitive but not symmetric (d) not reflexive
7. If $f(x)=3x+2$, then $f^{-1}(11)$ is
   (a) 1 (b) 2 (c) 5 (d) 3
8. If $A=\{1,2,3\}$ and $B=\{2,3,4\}$, then $(A-B)\cup(B-A)$ is
   (a) $\{2,3\}$ (b) $\{1,4\}$ (c) $\{1,2,3,4\}$ (d) $\{1\}$
9. If $f(x)=|x|$, then $f(-3)+f(3)$ is
   (a) 0 (b) 3 (c) 6 (d) $-6$
10. The function $f(x)=x^2+1$ on $\mathrm{R}$ is
    (a) one-one and onto (b) one-one into (c) many-one onto (d) many-one into
11. If $n(A)=4$, $n(B)=3$ and $n(A\cap B)=2$, then $n(A\,\Delta\,B)$ is
    (a) 3 (b) 5 (c) 1 (d) 7
12. The number of one-one functions from $\{1,2\}$ to $\{a,b,c\}$ is
    (a) 9 (b) 6 (c) 8 (d) 5

::: note Answers and explanations — Set B
**1.** (c) — union = 110; both = 90 + 72 − 110 = 52.
**2.** (a) — union = 35; both = 25 + 20 − 35 = 10.
**3.** (d) — need x − 3 ≥ 0; at x = 3 the root is 0, which is defined.
**4.** (b) — g(3) = 9, f(9) = 19. Computing g(f(3)) = 49 reverses the order.
**5.** (a) — each of 3 inputs has 2 choices: 2³ = 8; (b) is 3².
**6.** (c) — reflexive, transitive, but (1,2) has no (2,1).
**7.** (d) — 3x + 2 = 11 gives x = 3.
**8.** (b) — A − B = {1}, B − A = {4}.
**9.** (c) — 3 + 3 = 6.
**10.** (d) — f(1) = f(−1), and the range is y ≥ 1, not all of ℝ.
**11.** (a) — 4 + 3 − 2·2 = 3.
**12.** (b) — 3 × 2 = 6 ordered choices without repetition.
:::

**Set C — Application (8 questions)**

1. In a group of 100 people, 60 like tea, 50 like coffee and 20 like both. The number liking neither is
   (a) 0 (b) 5 (c) 20 (d) 10
2. If $f(x)=2x-1$ and $g(x)=\frac{x+1}{2}$, then $f(g(x))$ equals
   (a) 0 (b) $x$ (c) $2x$ (d) $x+1$
3. The number of subsets of a 5-element set having exactly 2 elements is
   (a) 10 (b) 20 (c) 5 (d) 25
4. On the positive integers, "$a$ divides $b$" is
   (a) an equivalence relation (b) symmetric (c) reflexive and transitive but not symmetric (d) symmetric and transitive only
5. If $f(x)=ax+b$, $f(1)=5$ and $f(2)=8$, then $f(5)$ is
   (a) 15 (b) 17 (c) 20 (d) 14
6. In a universal set of 50 elements, $n(A)=30$, $n(B)=25$ and $n(A\cup B)=45$. Then $n(A\cap B)$ is
   (a) 5 (b) 15 (c) 20 (d) 10
7. The range of $f(x)=3x-2$ defined on $\{1,2,3\}$ is
   (a) $\{1,4,7\}$ (b) $\{3,6,9\}$ (c) $\{2,4,6\}$ (d) $\{1,2,3\}$
8. The number of functions from $\{1,2\}$ to $\{a,b,c\}$ is
   (a) 8 (b) 6 (c) 9 (d) 64

::: note Answers and explanations — Set C
**1.** (d) — union = 60 + 50 − 20 = 90, so neither = 10.
**2.** (b) — 2·(x+1)/2 − 1 = x; f and g are inverses.
**3.** (a) — C(5,2) = 10.
**4.** (c) — a | a and transitive, but 2 | 4 does not give 4 | 2.
**5.** (b) — a = 3, b = 2, so f(5) = 17.
**6.** (d) — 30 + 25 − 45 = 10.
**7.** (a) — f(1), f(2), f(3) = 1, 4, 7.
**8.** (c) — 3² = 9; (b) 6 counts only the one-one ones.
:::
