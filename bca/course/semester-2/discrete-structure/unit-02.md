---
subject: Discrete Structure
grade: BCA Semester 2
unit: 2
title: Sets, Relations and Functions
area: BCA 151 · Discrete Structure · Unit 2
---

Sets, relations and functions are the vocabulary of data: a table is a relation, a database query is a set operation, a hash is a function. This unit defines them precisely and shows how to count and classify them.

::: key What this unit gives you
- Set notation, operations, identities, Venn diagrams and inclusion–exclusion.
- Relations: properties, representations, closures, equivalence relations and partial orders.
- Functions: one-to-one, onto, composition, inverse, and counting functions.
- Cardinality: finite, countable and uncountable sets.
:::

## 2.1 Sets and their operations

A **set** is an unordered collection of distinct objects. Notation: roster {1, 2, 3}; builder $\{x \mid x i s \mathrm{even} \mathrm{and} x < 10\}$. *∅* is the empty set; **U** the universal set; $|A|$ the cardinality; $x \in A$ membership; $A \subseteq B$ subset; $A \subset B$ proper subset.

| Operation | Definition |
|---|---|
| Union $A \cup B$ | in A or B |
| Intersection $A \cap B$ | in both |
| Difference $A - B$ | in A but not B |
| Complement $A'$ | in U but not A |
| Symmetric difference $A \oplus B$ | in exactly one: $(A - B) \cup (B - A)$ |
| Cartesian product $A \times B$ | all ordered pairs $(a ,\  b)$; \|A × B\| = $|A| \cdot |B|$ |
| Power set $P (A)$ | the set of all subsets; $|P (A)| = 2^{|A|}$ |

**Set identities** mirror logic: $A \cup (B \cap C) = (A \cup B) \cap (A \cup C) ;\  (A \cup B)' = A' \cap B'$ (De Morgan); $A \cup A' = U ;\  A \cap A' = \emptyset ;\  A - B = A \cap B'$. Prove equality by showing each side is a subset of the other, or by a membership table.

**Inclusion–exclusion.** |A ∪ B| = $|A| + |B|$ − |A ∩ B|; |A ∪ B ∪ C| = $|A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$.

::: example Worked example
In a class of 60, 35 study Java, 28 study Python and 10 study both. Either = $35 + 28 - 10 = 53$, so **7** study neither; Java only = 25; Python only = 18.

**Power set:** $P (\{a ,\  b ,\  c\})$ has $2^{3} = 8$ elements: *∅*, {a}, {b}, {c}, {a,b}, {a,c}, {b,c}, {a,b,c}.

**Bit-string view:** a subset of an n-element set is an n-bit string, so union is bitwise OR, intersection bitwise AND, and complement bitwise NOT. This is how sets are stored in machine words.
:::

### Russell, and the set of all subsets

The size of a set grows very fast when we $a s k$ for all its subsets. A set with *n* elements has $2^{n}$ subsets, because every element is either in or out. Bertrand Russell showed in 1901 that talking about "the set of all sets" leads to a contradiction, which is why mathematics treats sets with care. Plate 2.1 lists the eight subsets of {a, b, c} by counting in binary and shows the doubling for larger *n*.

```photogrid label="2.1" cols="2" ratio="1.2" caption="Every element is in or out. (a) Bertrand Russell, whose paradox about the set of all sets forced mathematicians to define sets carefully. (b) The $2^{3} = 8$ subsets of {a, b, c} listed by the binary numbers 000 to 111, and the number of subsets of an n-element set for $n = 0$ to 8."
@ photo id="bca151/russell" cap="Bertrand Russell (1872-1970)"
fit 1.2
focus 0.5 0.4
@ svg cap="Subsets of {a, b, c} by binary counting"
subs = []
for m in range(8):
    subs.append("".join(c for i, c in enumerate("abc") if m >> (2 - i) & 1) or "{}")
assert len(subs) == 8 and subs[0] == "{}" and subs[7] == "abc" and subs[5] == "ac"
assert [2**n for n in range(9)] == [1, 2, 4, 8, 16, 32, 64, 128, 256]
f = Fig(400, 250)
f.text(200, 16, "Subsets of {a, b, c}", size=11, color=NAVY, bold=True)
for m in range(8):
    x, y = 12 + (m % 4) * 96, 28 + (m // 4) * 54
    f.box(x, y, 88, 46, "", fill=BLUE, stroke=NAVY, r=4)
    f.text(x + 44, y + 15, format(m, "03b"), size=10.5, color=SLATE, bold=True)
    f.text(x + 44, y + 34, "{" + ",".join(subs[m]) + "}" if subs[m] != "{}" else "{ }", size=12, color=NAVY, bold=True)
f.text(200, 150, "Number of subsets of an n-element set", size=10.5, color=NAVY, bold=True)
for n in range(9):
    f.box(8 + n * 43, 160, 41, 36, "", fill=SAND, stroke=AMBER, r=3)
    f.text(8 + n * 43 + 20, 172, f"n={n}", size=10.5, color=SLATE)
    f.text(8 + n * 43 + 20, 188, str(2**n), size=10.5, color=AMBER, bold=True)
f.text(200, 224, "2^n: each new element doubles the number of subsets.", size=10.5, color=SLATE, bold=True)
f.text(200, 242, "2^10 = 1,024 and 2^20 = 1,048,576.", size=10.5, color=SLATE)
assert (2**10, 2**20) == (1024, 1048576)
```

## 2.2 Relations

A **relation** R from A to B is a subset of $A \times B$; "a R b" means $(a ,\  b) \in R$. A relation on A is a subset of $A \times A$. A relation can be shown as a set of pairs, a **matrix** (1 if related), or a **digraph**.

**Properties of a relation R on A**

| Property | Meaning |
|---|---|
| Reflexive | $(a ,\  a) \in R$ for all a |
| Irreflexive | $(a ,\  a) \notin R$ for all a |
| Symmetric | $(a ,\  b) \in R \Rightarrow (b ,\  a) \in R$ |
| Antisymmetric | $(a ,\  b)$ and $(b ,\  a) \in R \Rightarrow a = b$ |
| Transitive | $(a ,\  b) ,\  (b ,\  c) \in R \Rightarrow (a ,\  c) \in R$ |

An **equivalence relation** is reflexive, symmetric and transitive; it partitions A into **equivalence classes**. A **partial order** is reflexive, antisymmetric and transitive; $(A ,\  \leq)$ is a **poset**, drawn as a **Hasse diagram** (omit loops and implied edges).

::: example Worked example
On {1, 2, 3}: R = {(1,1), (2,2), (3,3), (1,2), (2,1)} is reflexive, symmetric and transitive: an equivalence relation with classes {1, 2} and {3}.

"Divides" on {1, 2, 3, 4, 6, 12} is a partial order; its Hasse diagram has 1 at the bottom, then 2 and 3, then 4 and 6, and 12 at the top. 1 is the minimum, 12 the maximum; 4 and 6 are incomparable.

**Congruence mod 3** on $\mathbb{Z} ( a$ ~ *b* iff 3 | $a - b$) is an equivalence with three classes: $[0] = \{\ldots ,\  - 3 ,\  0 ,\  3 ,\  \ldots\} ,\  [1] ,\  [2]$.
:::

**Counting relations.** On an n-element set there are $2^{n^{2}}$ relations; $2^{n^{2} - n}$ reflexive ones; $2^{\frac{n (n + 1)}{2}}$ symmetric ones. For $n = 3$: 512, 64 and 64.

**Composition and closures.** $R \circ S = \{(a ,\  c) \mid \exists b : (a ,\  b) \in S ,\  (b ,\  c) \in R\}$ (order convention varies; here S is applied first). In matrix form it is the Boolean matrix product. The **reflexive**, **symmetric** and **transitive closures** are the smallest relations containing R with that property.

::: example Worked example: transitive closure
R = {(1,2), (2,3), (3,4)} on {1, 2, 3, 4}. Add (1,3) from (1,2),(2,3); (2,4) from (2,3),(3,4); then (1,4) from (1,3),(3,4). Closure = {(1,2), (2,3), (3,4), (1,3), (2,4), (1,4)}. **Warshall's algorithm** does this in $O (n^{3})$: for each $k ,\  i ,\  j$, set M[i][j] |= M[i][k] & M[k][j].
:::

**Databases:** a relational table is a relation; a join is a composition-like operation; a primary key makes the relation a function from key to row.

## 2.3 Functions

A **function** *f*: $A \to B$ assigns each $a \in A$ exactly one $f (a) \in B$. Domain A, codomain B, range = set of actual outputs.

| Type | Meaning | Test |
|---|---|---|
| **Injective** (one-to-one) | $f (a) = f (a') \Rightarrow a = a'$ | no output hit twice |
| **Surjective** (onto) | every *b* has some a | range = codomain |
| **Bijective** | both | invertible |

**Composition** $(g \circ f) (x) = g (f (x))$; composition of bijections is a bijection; a bijection has an inverse $f^{-1}$ with $f^{-1} \circ f$ = id.

::: example Worked example
$f (x) = 2 x + 1$ on $\mathbb{Z} \to \mathbb{Z}$ is injective but not onto (even numbers are never reached). $g (x) = x^{2}$ on $\mathbb{R}$ is neither ($g (2) = g (- 2) ;\  - 1$ is never reached); on [$0 ,\  \infty ) \to [ 0 ,\  \infty$) it is a bijection.

**Counting functions** from an m-set A to an n-set B: total $n^{m}$; injective $\frac{n !}{(n - m) !}$ (needs $m \leq n$); bijections $n ! (m = n)$; **onto** by inclusion–exclusion: for $m = 4 ,\  n = 3$: $3^{4} - 3 \cdot 2^{4} + 3 \cdot 1^{4} = 81 - 48 + 3$ = **36**.

**Pigeonhole principle:** a function from a set of more than *k* elements to a set of *k* elements cannot be injective, so some two elements share an image. Among 13 people, two share a birth month.

**Hash functions** are not injective (collisions are certain when keys outnumber slots), which is the pigeonhole principle at work.
:::

Special functions: **floor** $\lfloor x \rfloor$, **ceiling** $\lceil x \rceil$, **mod**, **characteristic function** of a set, **recursive functions** (Unit 4). Growth of functions (big-O) uses these: $n \log n \ll n^{2} \ll 2^{n} \ll n !$.

## 2.4 Cardinality and countability

Two sets have the same cardinality if a bijection exists between them. A set is **countable** if it is finite or has the same size as $\mathbb{N}$. $\mathbb{Z}$ is countable (list $0 ,\  1 ,\  - 1 ,\  2 ,\  - 2 ,\  \ldots ) ;\  \mathbb{Q}$ is countable; the set of all finite strings over a finite alphabet is countable (so the set of all programs is countable). **$\mathbb{R}$ is uncountable** (Cantor's diagonal argument): any list of reals in (0,1) misses the number whose nth digit differs from the nth digit of the nth number. Consequence: there are more functions $\mathbb{N}$ → {0,1} than programs, so some functions are **not computable**.

### Cantor: some infinities are bigger

Georg Cantor compared infinite sets by pairing their members. The natural numbers and the even numbers can be paired one to one (*n* with $2 n$), so they have the same size even though the evens look like half. The real numbers cannot be listed at all: whatever list is given, change the diagonal digit of every entry and the new sequence differs from each row. Plate 2.2 pairs the numbers and runs the diagonal argument on a small list.

```photogrid label="2.2" cols="2" ratio="1.1" caption="Counting infinity. (a) Georg Cantor, who proved that the real numbers are more numerous than the natural numbers. (b) The pairing *n* to $2 n$ for the first eight naturals, and Cantor's diagonal trick on a list of five binary sequences: flipping the diagonal gives a sequence that differs from every row of the list."
@ photo id="bca151/cantor" cap="Georg Cantor (1845-1918)"
fit 1.1
focus 0.5 0.35
@ svg cap="A one-to-one pairing and the diagonal argument"
lst = ["10110", "01101", "11000", "00111", "10010"]
diag = "".join("1" if lst[i][i] == "0" else "0" for i in range(5))
assert all(diag[i] != lst[i][i] for i in range(5))
assert all(diag != row for row in lst)
assert [2 * n for n in range(1, 9)] == [2, 4, 6, 8, 10, 12, 14, 16]
f = Fig(400, 272)
f.text(200, 16, "n pairs with 2n: both lists are endless", size=11, color=NAVY, bold=True)
for n in range(1, 9):
    x = 8 + (n - 1) * 48
    f.box(x, 26, 42, 24, str(n), fill=BLUE, stroke=NAVY, color=NAVY, bold=True)
    f.line(x + 21, 50, x + 21, 66, color=SLATE)
    f.box(x, 66, 42, 24, str(2 * n), fill=SAND, stroke=AMBER, color=AMBER, bold=True)
f.text(200, 116, "Diagonal argument: flip the circled digit of each row", size=11, color=NAVY, bold=True)
for i, row in enumerate(lst):
    for j, ch in enumerate(row):
        hot = i == j
        f.box(110 + j * 30, 126 + i * 22, 28, 20, ch, fill=ROSE if hot else BLUE, stroke=RED if hot else NAVY, color=RED if hot else NAVY, size=10.5, bold=True)
f.text(60, 252, "new:", size=11, color=TEAL, bold=True)
for j, ch in enumerate(diag):
    f.box(110 + j * 30, 242, 28, 20, ch, fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True)
f.text(270, 252, "differs from all", size=10.5, color=TEAL, bold=True, anchor="start")
```

## 2.5 Three kinds of function in one picture

A function assigns to every element of the domain exactly one element of the codomain. Three questions classify it (Figure 2.1). Is every codomain element hit? If yes it is **surjective** (onto). Does any codomain element get hit twice? If no, it is **injective** (one-to-one). If both hold the function is **bijective**, and only a bijection has an inverse. Counting also becomes easy: between two finite sets of the same size *n*, there are $n !$ bijections.

```svgfig label="2.1" caption="Mapping diagrams. (a) Injective but not surjective: every input has its own output, but *d* is never reached. (b) Surjective but not injective: every output is reached, but 1 and 2 share the output a. (c) Bijective: a perfect pairing, so the inverse function exists."
f = Fig(580, 215)
def panel(x0, dom, cod, arrows, title, note):
    f.text(x0 + 70, 14, title, size=11.5, color=NAVY, bold=True)
    f.box(x0, 26, 50, 150, "", fill=BLUE, stroke=NAVY)
    f.box(x0 + 90, 26, 50, 150, "", fill=SOFT, stroke=TEAL)
    pos = lambda n, i: 26 + (i + 0.5) * 150 / n
    for i, d in enumerate(dom):
        f.text(x0 + 25, pos(len(dom), i), d, size=12, color=NAVY, bold=True, vmid=True)
    for i, c in enumerate(cod):
        f.text(x0 + 115, pos(len(cod), i), c, size=12, color=NAVY, bold=True, vmid=True)
    for a, b in arrows:
        f.arrow([(x0 + 40, pos(len(dom), a)), (x0 + 100, pos(len(cod), b))], color=RED)
    f.text(x0 + 70, 196, note, size=10, color=SLATE, italic=True)
panel(18, "123", "abcd", [(0, 0), (1, 1), (2, 2)], "(a) injective", "d is missed")
panel(210, "1234", "abc", [(0, 0), (1, 0), (2, 1), (3, 2)], "(b) surjective", "1 and 2 share a")
panel(402, "123", "abc", [(0, 1), (1, 2), (2, 0)], "(c) bijective", "inverse exists")
```

## 2.6 Eight uses of sets, relations and functions

1. **Databases.** A table is a relation, a row is a tuple, and the join of two tables is the composition of relations. SQL's UNION, INTERSECT and EXCEPT are set operations. The structure of a school database is relational algebra at work.
2. **Hashing and look-up.** A hash function maps keys (names, citizenship numbers) into table slots. It is a function that is intentionally not injective, and collisions are the price. Knowing injectivity explains why collisions must be handled.
3. **Data types and programming.** A type is a set of values, a function signature is a domain and codomain, and a pure function maps every input to one output. Thinking in sets prevents many type bugs.
4. **Equivalence and grouping.** An equivalence relation partitions a set into classes. Clustering users, merging duplicate student records and congruence classes mod *n* use this idea.
5. **Orderings and scheduling.** A partial order such as "course A must come before B" is a relation. Sorting the courses so that all prerequisites come first is a topological sort. Every timetable system relies on it.
6. **Encryption and codes.** Encryption must be a bijection, otherwise two messages would share one ciphertext and decryption would be impossible. Checksum and error-detecting codes are functions with chosen properties.
7. **Counting data.** The size of the power set, $2^{n}$, counts the possible subsets of *n* features or permissions. A system with 10 permissions has 1,024 possible permission sets.
8. **Infinite data and limits of computing.** Cardinality shows that there are more real numbers than programs, so some functions cannot be computed at all. This is the first step towards the theory of computation.

## Formula and fact sheet

- $|P (A)| = 2^{n}$; |A × B| = $|A| |B|$; |A ∪ B| = $|A| + |B|$ − |A ∩ B|.
- Equivalence = reflexive + symmetric + transitive (partitions); partial order = reflexive + antisymmetric + transitive.
- Relations on n-set: $2^{n^{2}}$; reflexive $2^{n^{2} - n}$; symmetric $2^{\frac{n (n + 1)}{2}}$.
- Functions $A \to B$: $|B|^{|A|}$; injective $\frac{n !}{(n - m) !}$; onto by inclusion–exclusion.
- Pigeonhole: $n + 1$ objects in *n* boxes ⇒ a box with two.
- $\mathbb{N} ,\  \mathbb{Z} ,\  \mathbb{Q}$ countable; $\mathbb{R}$ uncountable.

## Chapter summary

- Sets and bit strings: union, intersection and complement are the logical operators applied to membership.
- Relations capture structure (equivalence → partitions, order → posets); closures add forced pairs.
- Functions classified as injective, surjective, bijective; counting uses powers, falling factorials and inclusion–exclusion.
- Cardinality separates countable from uncountable infinities, with consequences for computability.

## Practice

1. If A = {1, 2, 3, 4}, B = {3, 4, 5}, $U = \{1 ,\  \ldots ,\  6\}$, find $A \cup B ,\  A \cap B ,\  A - B ,\  B' ,\  A \oplus B ,\  |P (A)|$, |A × B|.
2. Of 100 students 70 like cricket, 55 like football and 25 like neither. How many like both?
3. Prove $(A \cup B)' = A' \cap B'$.
4. Test the relation R on $\mathbb{Z}$: a $R b$ iff $a - b$ is even; classify and give the classes.
5. Is "divides" on positive integers an equivalence relation? A partial order?
6. Find the transitive closure of {(a, b), (b, c), (c, a)} on {a, b, c}.
7. How many reflexive and symmetric relations on a 4-element set?
8. Classify $f (x) = x^{3}$ on $\mathbb{R} \to \mathbb{R}$ and $f (n) = n$ mod 5 on $\mathbb{Z} \to \{0 ,\  \ldots ,\  4\}$.
9. Count the functions from a 3-set to a 5-set, and the injective ones.
10. Show that the set of positive rationals is countable (describe the listing).

::: note Answers and worked solutions
**1.** $A \cup B$ = {1,2,3,4,5}; $A \cap B$ = {3,4}; $A - B$ = {1,2}; $B'$ = {1,2,6}; $A \oplus B$ = {1,2,5}; $|P (A)| = 16$; |A × B| = 12.

**2.** Likes at least one = $100 - 25 = 75 = 70 + 55$ − both ⇒ both = **50**.

**3.** $x \in (A \cup B)' \Leftrightarrow \neg (x \in A \vee x \in B) \Leftrightarrow x \notin A \wedge x \notin B \Leftrightarrow x \in A' \cap B'$. ∎

**4.** Reflexive (0 is even), symmetric, transitive (even + even = even): an **equivalence** with two classes: the evens and the odds.

**5.** Not symmetric (2 | 4, 4 ∤ 2), so not an equivalence. It is reflexive, antisymmetric and transitive: a **partial order**.

**6.** The closure is all nine pairs of {a, b, c}²: $a \to b \to c \to a$ lets every element reach every element, including itself.

**7.** Reflexive: diagonal pairs forced (4). Symmetric on the 6 off-diagonal pairs: $2^{6}$ = **64** relations that are both.

**8.** $x^{3}$ is a **bijection** on $\mathbb{R}$. *n* mod 5 is **onto** but not injective.

**9.** $5^{3}$ = **125**; injective: 5·4·3 = **60**.

**10.** Arrange $\frac{p}{q}$ in a grid by numerator *p* and denominator *q*; walk the diagonals $p + q = 2 ,\  3 ,\  4 ,\  \ldots$ skipping fractions not in lowest terms; every positive rational appears exactly once, giving a bijection with $\mathbb{N}$.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Show that the relation "a ≡ *b* (mod 3)" on A = {1, 2, 3, 4, 5, 6} is an equivalence relation and list its classes.**

*Introduction.* A relation is an equivalence relation if it is reflexive, symmetric and transitive. Here a $R b$ means that 3 divides $a - b$.

*Reflexive.* $a - a = 0$ is divisible by 3, so a R a for every a.

*Symmetric.* If 3 divides $a - b$, it divides $b - a = - (a - b)$, so a $R b$ implies $b R a$.

*Transitive.* If 3 | $(a - b)$ and 3 | $(b - c)$, then 3 divides the sum $(a - b) + (b - c) = a - c$, so a $R c$.

*Classes.* The remainders on division by 3 give {1, 4}, {2, 5} and {3, 6}. They are disjoint and cover A, so they form a **partition**; the relation has 3 classes. *Conclusion.* R is an equivalence relation with the three classes above.

**Q2 (10 marks). Define injective, surjective and bijective functions, composition and inverse, with examples; state the number of subsets of a set.**

*Introduction.* A function *f*: $A \to B$ sends each element of A to exactly one element of B. Its type is decided by how it covers B (Figure 2.1).

*Types.*

1. **Injective.** $f (x) = f (y)$ implies $x = y$. Example: $f (x) = 2 x$ on the integers; different inputs give different outputs.
2. **Surjective.** Every *b* in B equals $f (a)$ for some a. Example: $f (x) = 2 x$ is **not** surjective onto the integers, since 3 is never reached.
3. **Bijective.** Both. Example: $g (x) = x + 3$ on the integers.
4. **Test for finite sets.** An injective map between sets of the same finite size is automatically bijective.

*Composition and inverse.*

5. **Composition.** $(g \circ f) (x) = g (f (x))$. With $f (x) = 2 x$ and $g (x) = x + 3 ,\  (g \circ f) (x) = 2 x + 3$, whereas $(f \circ g) (x) = 2 x + 6$, so composition is not commutative.
6. **Inverse.** Only a bijection has an inverse. For $g (x) = x + 3 ,\  g^{-1} (x) = x - 3$, and $g^{-1} (g (x)) = x$.
7. **Composition of bijections** is a bijection, and $(g \circ f)^{-1} = f^{-1} \circ g^{-1}$.

*Counting.*

8. **Subsets.** A set of *n* elements has $2^{n}$ subsets, so A = {1, 2, 3} has 8, and there are $n !$ bijections from A to a set of the same size (here 6).

| Type | Condition | Example |
|---|---|---|
| Injective | no two inputs share an output | $2 x$ on integers |
| Surjective | every output is reached | $x^{3}$ on the reals |
| Bijective | both | $x + 3$ |
| Inverse exists | iff bijective | $x - 3$ |

*Conclusion.* Injectivity, surjectivity and bijectivity describe how a function covers its codomain, and only bijections can be undone.
