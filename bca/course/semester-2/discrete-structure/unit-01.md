---
subject: Discrete Structure
grade: BCA Semester 2
unit: 1
title: Logic and Proof Techniques
area: BCA 151 · Discrete Structure · Unit 1
---

Discrete mathematics is the mathematics of countable, separate things: statements, sets, integers, graphs, strings. It is the language in which algorithms are specified and proved correct. This unit begins with logic, the grammar of every proof and every `if` statement you will write.

::: key What this unit gives you
- Propositions, connectives, truth tables, equivalences, tautologies.
- Normal forms and the algebra of logic.
- Predicates and quantifiers, with negation rules.
- Rules of inference and the standard proof techniques.
:::

## 1.1 Propositions and connectives

A **proposition** is a declarative sentence that is either true or false, never both. "Kathmandu is the capital of Nepal" is a proposition (true); "x + 2 = 5" is not (until *x* is given); "Close the door" is not.

| Connective | Symbol | Read | True when |
|---|---|---|---|
| Negation | $\neg p$ | not *p* | *p* is false |
| Conjunction | $p \wedge q$ | *p* and *q* | both true |
| Disjunction | $p \vee q$ | *p* or *q* (inclusive) | at least one true |
| Exclusive or | $p \oplus q$ | *p* xor *q* | exactly one true |
| Implication | $p \to q$ | if *p* then *q* | false only when *p* is true and *q* is false |
| Biconditional | $p \leftrightarrow q$ | *p* iff *q* | *p* and *q* have the same value |

**Implication** surprises beginners: "If it rains, I carry an umbrella" is not broken when it does not rain, so $p \to q$ is true whenever *p* is false. Related forms of $p \to q$:

- **Converse** $q \to p$, **inverse** $\neg p \to \neg q$, **contrapositive** $\neg q \to \neg p$.
- The contrapositive is *equivalent* to the original; the converse and inverse are equivalent to each other but not to it.

Truth table of the main connectives (T/F):

| *p* | *q* | $p \wedge q$ | $p \vee q$ | $p \oplus q$ | $p \to q$ | $p \leftrightarrow q$ |
|---|---|---|---|---|---|---|
| T | T | T | T | F | T | T |
| T | F | F | T | T | F | F |
| F | T | F | T | T | T | F |
| F | F | F | F | F | T | T |

A formula with *n* variables has **$2^{n}$** rows. **Precedence:** *¬*, then ∧, then ∨, then →, then ↔.

### Boole's idea: logic as calculation

In 1854 George Boole showed that reasoning can be written as algebra on two values, true and false. Augustus De Morgan, his contemporary, stated the two laws that bear his name: the negation of "and" is the "or" of the negations, and the negation of "or" is the "and" of the negations. Every program that writes `!(a && b)` as `!a || !b` uses them. Plate 1.1 does not trust the statement: it evaluates both sides on all four rows of the truth table and checks that the columns are identical.

```photogrid label="1.1" cols="2" ratio="1.1" caption="Logic as algebra. (a) George Boole, who wrote logic as calculation on the two values true and false. (b) De Morgan's laws checked on every row of the truth table: not (*p* and *q*) equals (not *p*) or (not *q*), and not (*p* or *q*) equals (not *p*) and (not *q*); the two columns of each pair agree on all four rows."
@ photo id="bca151/boole" cap="George Boole (1815-1864)"
fit 1.1
focus 0.5 0.4
@ svg cap="De Morgan's laws on all four rows"
rows = [(p, q) for p in (True, False) for q in (True, False)]
a1 = [not (p and q) for p, q in rows]; b1 = [(not p) or (not q) for p, q in rows]
a2 = [not (p or q) for p, q in rows]; b2 = [(not p) and (not q) for p, q in rows]
assert a1 == b1 and a2 == b2 and a1 == [False, True, True, True] and a2 == [False, False, False, True]
f = Fig(400, 250)
f.text(200, 16, "T = true, F = false", size=11, color=NAVY, bold=True)
heads = ["p", "q", "not(p and q)", "(not p) or (not q)", "not(p or q)", "(not p) and (not q)"]
xs = [10, 44, 78, 154, 250, 326]; ws = [30, 30, 70, 92, 72, 70]
for x, w, h in zip(xs, ws, ["p", "q", "!(p&q)", "!p | !q", "!(p|q)", "!p & !q"]):
    f.text(x + w / 2, 42, h, size=10.5, color=SLATE, bold=True)
for i, (p, q) in enumerate(rows):
    y = 52 + i * 34
    vals = [p, q, a1[i], b1[i], a2[i], b2[i]]
    for j, (x, w, v) in enumerate(zip(xs, ws, vals)):
        same = j >= 2
        f.box(x, y, w, 28, "T" if v else "F", fill=MINT if (v and same) else (BLUE if not same else SOFT), stroke=TEAL if (v and same) else NAVY, color=TEAL if v else RED, size=12, bold=True)
f.text(200, 206, "Columns 3 and 4 are identical;  columns 5 and 6 are identical.", size=10.5, color=SLATE, bold=True)
f.text(200, 228, "In C: !(a && b) is the same as !a || !b for every a and b.", size=10.5, color=SLATE)
```

## 1.2 Tautologies and equivalences

A **tautology** is always true; a **contradiction** is always false; otherwise a **contingency**. Two formulas are **logically equivalent** $(\equiv)$ if they have identical truth tables.

| Law | Equivalence |
|---|---|
| Implication | $p \to q \equiv \neg p \vee q$ |
| Contrapositive | $p \to q \equiv \neg q \to \neg p$ |
| Biconditional | $p \leftrightarrow q \equiv (p \to q) \wedge (q \to p)$ |
| De Morgan | $\neg (p \wedge q) \equiv \neg p \vee \neg q ;\  \neg (p \vee q) \equiv \neg p \wedge \neg q$ |
| Double negation | $\neg \neg p \equiv p$ |
| Distributive | $p \wedge (q \vee r) \equiv (p \wedge q) \vee (p \wedge r) ;\  p \vee (q \wedge r) \equiv (p \vee q) \wedge (p \vee r)$ |
| Absorption | $p \vee (p \wedge q) \equiv p ;\  p \wedge (p \vee q) \equiv p$ |
| Negation of → | $\neg (p \to q) \equiv p \wedge \neg q$ |
| Commutative, associative, idempotent, identity, domination | as in Boolean algebra |

::: example Worked example: prove an equivalence by laws
Show $\neg (p \vee (\neg p \wedge q)) \equiv \neg p \wedge \neg q$.

$\neg (p \vee (\neg p \wedge q)) \equiv \neg p \wedge \neg (\neg p \wedge q)$ (De Morgan) ≡ $\neg p \wedge (p \vee \neg q)$ (De Morgan, double negation) ≡ $(\neg p \wedge p) \vee (\neg p \wedge \neg q)$ (distributive) ≡ $F \vee (\neg p \wedge \neg q)$ ≡ **$\neg p \wedge \neg q$**. ∎
:::

::: example Worked example: is it a tautology?
$(p \to q) \wedge (q \to r) \to (p \to r)$ (hypothetical syllogism). The formula can be false only if the antecedent is true and $p \to r$ is false, i.e. $p = T ,\  r = F$. Then $p \to q$ true forces $q = T$, and $q \to r$ with $q = T ,\  r = F$ is false, contradicting the antecedent. So it is never false: a **tautology**.
:::

**Normal forms.** A **DNF** (disjunctive normal form) is an OR of ANDs of literals; a **CNF** is an AND of ORs. Every formula has both (read the T rows for DNF, the F rows for CNF), which is the same canonical SOP/POS idea from Digital Logic. For $p \to q$: $\mathrm{DNF} = \neg p \vee q$ (already). For $p \oplus q$: DNF $(p \wedge \neg q) \vee (\neg p \wedge q) ,\  \mathrm{CNF} (p \vee q) \wedge (\neg p \vee \neg q)$.

**Counting formulas.** There are $2^{2^{n}}$ distinct truth functions of *n* variables: 4 for one variable, 16 for two, 256 for three. **Satisfiability (SAT)**: is there an assignment making the formula true? It is the first problem proven NP-complete, which is why logic matters for complexity.

## 1.3 Predicates and quantifiers

A **predicate** $P (x)$ becomes a proposition when *x* is given a value or **quantified** over a **domain**.

- **Universal:** $\forall x P (x)$, "for all x, P(x)".
- **Existential:** $\exists x P (x)$, "there exists *x* such that P(x)".
- **Negation:** $\neg \forall x P (x) \equiv \exists x \neg P (x) ;\  \neg \exists x P (x) \equiv \forall x \neg P (x)$.

**Order matters.** Over the integers, $\forall x \exists y (x + y = 0)$ is true (take $y = - x$) but $\exists y \forall x (x + y = 0)$ is false (no single *y* works for all *x*).

::: example Worked example: translating English
"Every student who studies passes": $\forall x (S (x) \wedge T (x) \to P (x))$ where S = is a student, T = studies, P = passes.

"Some student failed": $\exists x (S (x) \wedge \neg P (x))$.

Negation of "every student passes": $\exists x (S (x) \wedge \neg P (x))$, "some student fails".

Note: with *∀* use →; with *∃* use ∧. Writing $\forall x (S (x) \wedge P (x))$ would say that *everything* is a passing student.
:::

**Nested quantifiers in computing:** "Every array has a maximum" is $\forall A \exists m (m \in A \wedge \forall a \in A ,\  a \leq m)$; the limit definition $\forall \epsilon > 0 \exists \delta > 0 (\ldots)$ is the same pattern. In loops, `for all` is a loop that stops at the first counterexample; `exists` stops at the first witness.

## 1.4 Rules of inference

An **argument** is valid if whenever all the premises are true the conclusion is true.

| Rule | Form |
|---|---|
| Modus ponens | $p ,\  p \to q \vdash q$ |
| Modus tollens | $\neg q ,\  p \to q \vdash \neg p$ |
| Hypothetical syllogism | $p \to q ,\  q \to r \vdash p \to r$ |
| Disjunctive syllogism | $p \vee q ,\  \neg p \vdash q$ |
| Addition | $p \vdash p \vee q$ |
| Simplification | $p \wedge q \vdash p$ |
| Conjunction | $p ,\  q \vdash p \wedge q$ |
| Resolution | $p \vee q ,\  \neg p \vee r \vdash q \vee r$ |
| Universal instantiation | $\forall x P (x) \vdash P (c)$ |
| Existential generalisation | $P (c) \vdash \exists x P (x)$ |

::: example Worked example: a valid argument
Premises: (1) If the server is down then the website is not reachable. (2) The website is reachable. (3) If the router fails then the server is down. Conclude: the router has not failed.

Let *s* = server down, *w* = reachable, *r* = router fails. (1) $s \to \neg w ;\  (2) w ;\  (3) r \to s$. From (1) and (2) by modus tollens: $\neg s$. From (3) and $\neg s$ by modus tollens: **$\neg r$**. ∎
:::

**Fallacies.** *Affirming the conclusion*: $p \to q ,\  q \vdash p$ is **invalid** (the wet road does not prove it rained). *Denying the hypothesis*: $p \to q ,\  \neg p \vdash \neg q$ is **invalid**.

### Aristotle's syllogism, checked by machine

Aristotle was the first to $a s k$ which arguments are valid whatever the subject matter. Today we can answer by brute force: an argument is valid if there is no row of the truth table where all premises are true and the conclusion is false. Plate 1.2 runs that test on three valid rules and on the two fallacies of Section 1.4. For modus ponens only one row makes both premises true, and the conclusion holds there; for "affirming the conclusion" a row exists with true premises and a false conclusion, which is the counterexample.

```photogrid label="1.2" cols="2" ratio="1.0" caption="Validity by exhaustive check. (a) A Roman copy of the bust of Aristotle, who first listed valid forms of argument. (b) Five argument forms tested on every truth-table row: for each, the number of rows in which all premises are true and the number of those rows where the conclusion fails; a form is valid exactly when that last number is 0."
@ photo id="bca151/aristotle" cap="Aristotle (384-322 BC), Roman copy of a Greek bust"
fit 1.0
focus 0.5 0.4
@ svg cap="Counterexample search over all rows"
from itertools import product
imp = lambda a, b: (not a) or b
forms = [("modus ponens", lambda p, q, r: [imp(p, q), p], lambda p, q, r: q),
         ("modus tollens", lambda p, q, r: [imp(p, q), not q], lambda p, q, r: not p),
         ("hypothetical syllogism", lambda p, q, r: [imp(p, q), imp(q, r)], lambda p, q, r: imp(p, r)),
         ("affirming the conclusion", lambda p, q, r: [imp(p, q), q], lambda p, q, r: p),
         ("denying the hypothesis", lambda p, q, r: [imp(p, q), not p], lambda p, q, r: not q)]
res = []
for nm, prem, con in forms:
    t = bad = 0
    for p, q, r in product((True, False), repeat=3):
        if all(prem(p, q, r)): t += 1; bad += (not con(p, q, r))
    res.append((nm, t, bad))
assert [x[2] for x in res] == [0, 0, 0, 2, 2] and res[0][1] == 2 and res[2][1] == 4
f = Fig(400, 240)
f.text(200, 16, "Rows over p, q, r (8 rows in all)", size=11, color=NAVY, bold=True)
f.text(10, 40, "form", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(262, 40, "premises true", size=10.5, color=SLATE, bold=True)
f.text(356, 40, "fails", size=10.5, color=SLATE, bold=True)
for i, (nm, t, b) in enumerate(res):
    y = 50 + i * 34
    ok = b == 0
    f.box(6, y, 388, 29, "", fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, r=4)
    f.text(12, y + 15, nm, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(262, y + 15, str(t), size=12, color=SLATE, bold=True, vmid=True)
    f.text(356, y + 15, str(b), size=12, color=TEAL if ok else RED, bold=True, vmid=True)
f.text(200, 232, "0 failures = valid.  Any failure is a counterexample = invalid.", size=10.5, color=SLATE, bold=True)
```

## 1.5 Proof techniques

| Technique | Idea | Template |
|---|---|---|
| **Direct** | assume *p*, derive *q* | "Let *n* be even; $n = 2 k ;\  n^{2} = 4 k^{2} = 2 (2 k^{2})$, so even." |
| **Contrapositive** | prove $\neg q \to \neg p$ | to prove "n² even ⇒ *n* even", show *n* odd ⇒ $n^{2}$ odd |
| **Contradiction** | assume the negation, reach an impossibility | $\sqrt{2}$ irrational |
| **Cases** | split into exhaustive cases |  | *x* | ≥ 0 by $x \geq 0$ and $x < 0$ |
| **Existence** | constructive (exhibit) or non-constructive |  |
| **Counterexample** | one example disproves a *∀* claim | "n² + n + 41 is prime for all n" fails at $n = 40$ |
| **Induction** | base case + step | Unit 4 |

::: example Worked example: √2 is irrational (contradiction)
Suppose $\sqrt{2} = \frac{a}{b}$ in lowest terms ($a ,\  b$ integers with no common factor). Then $a^{2} = 2 b^{2}$, so $a^{2}$ is even, so a is even (contrapositive: odd² is odd). Write $a = 2 c$: $4 c^{2} = 2 b^{2}$, so $b^{2} = 2 c^{2}$, so *b* is even. Both a and *b* are even, contradicting lowest terms. Hence $\sqrt{2}$ is irrational. ∎
:::

::: example Worked example: contrapositive
Claim: if $3 n + 2$ is odd then *n* is odd. Contrapositive: if *n* is even then $3 n + 2$ is even. $n = 2 k \Rightarrow 3 n + 2 = 6 k + 2 = 2 (3 k + 1)$, even. ∎
:::

::: example Worked example: counterexample
Claim: for every integer $n ,\  n^{2} + n + 41$ is prime. $n = 40$ gives $40^{2} + 40 + 41 = 1681 = 41^{2}$, which is composite. The claim is **false**.
:::

## 1.6 Which proof technique should I try?

Students often stare at a statement without knowing how to start. A short decision chain (Figure 1.1) removes most of the fear. Begin with the **direct proof**: assume the hypothesis and walk to the conclusion. If the conclusion is awkward (for example "n is even") but its negation is easy, $t r y$ the **contrapositive** (prove $\neg q \to \neg p$). If the statement says something does not exist or cannot be written in a form, assume the opposite and look for a **contradiction**. If it is about all natural numbers $n \geq n_{0}$, use **induction** (Unit 4). To disprove "for all", one **counterexample** is enough.

```svgfig label="1.1" caption="Choosing a proof technique. Start with the direct proof; switch to the contrapositive when the conclusion is hard to reach; use contradiction for 'cannot' and 'does not exist'; use induction for statements about every natural number; use a single counterexample to disprove a 'for all' claim."
f = Fig(580, 215)
f.box(10, 80, 100, 52, "Statement\np -> q", fill=BLUE, stroke=NAVY, size=11, color=NAVY, bold=True)
tech = [("Direct proof", "assume p,\nreach q", 150, 10, SOFT, TEAL), ("Contrapositive", "assume not q,\nreach not p", 150, 80, SOFT, TEAL),
        ("Contradiction", "assume p and not q,\nreach a falsehood", 150, 150, SOFT, TEAL)]
for n, d, x, y, fl, s in tech:
    f.box(x, y, 150, 54, "", fill=fl, stroke=s)
    f.text(x + 75, y + 17, n, size=11.5, color=NAVY, bold=True)
    f.text(x + 75, y + 33, d.split("\n")[0], size=9.5, color=NAVY)
    f.text(x + 75, y + 46, d.split("\n")[1], size=9.5, color=NAVY)
    f.arrow([(110, 106), (150, y + 27)], color=SLATE)
f.box(350, 30, 220, 50, "For every n >= n0?\nuse induction", fill="#fde68a", stroke=AMBER, size=11, color=NAVY, bold=True)
f.box(350, 130, 220, 50, "Claim 'for all' looks false?\nfind one counterexample", fill="#fecaca", stroke=RED, size=11, color=NAVY, bold=True)
f.arrow([(300, 37), (350, 55)], color=SLATE, dash=True); f.arrow([(300, 177), (350, 155)], color=SLATE, dash=True)
```

### Logic made of switches

Before transistors, a telephone exchange computed with relays: a small electromagnet that closes or opens a metal contact. Two contacts in series carry current only if both are closed, which is AND; two in parallel carry current if either is closed, which is OR. Plate 1.3 lists what a lamp does in each of the four switch settings. This is the same truth table you wrote for `p ∧ q` and `p ∨ q`, now built from metal.

```photogrid label="1.3" cols="2" ratio="1.2" caption="Truth tables you can hear click. (a) A reed relay of the kind used in telephone exchanges, shown beside a ruler. (b) Two switches *p* and *q* wired in series (lamp lights only when both are closed, AND) or in parallel (lamp lights when at least one is closed, OR), listed for all four settings."
@ photo id="bca151/relay" cap="Relay used in a telephone exchange (ruler for scale)"
fit 1.2
focus 0.5 0.5
@ svg cap="Series is AND, parallel is OR"
rows = [(p, q) for p in (1, 0) for q in (1, 0)]
ser = [p & q for p, q in rows]; par = [p | q for p, q in rows]
assert ser == [1, 0, 0, 0] and par == [1, 1, 1, 0]
f = Fig(400, 264)
f.text(100, 16, "Series (AND)", size=11, color=TEAL, bold=True)
f.text(300, 16, "Parallel (OR)", size=11, color=AMBER, bold=True)
f.line(20, 50, 40, 50, color=SLATE); f.box(40, 38, 40, 24, "p", fill=BLUE, stroke=NAVY, color=NAVY, bold=True); f.line(80, 50, 100, 50, color=SLATE)
f.box(100, 38, 40, 24, "q", fill=BLUE, stroke=NAVY, color=NAVY, bold=True); f.line(140, 50, 160, 50, color=SLATE); f.circle(172, 50, 12, fill=SAND, stroke=AMBER, label="L", color=AMBER)
f.line(220, 50, 240, 50, color=SLATE); f.line(240, 34, 240, 76, color=SLATE)
f.box(260, 22, 40, 24, "p", fill=BLUE, stroke=NAVY, color=NAVY, bold=True); f.box(260, 64, 40, 24, "q", fill=BLUE, stroke=NAVY, color=NAVY, bold=True)
f.line(240, 34, 260, 34, color=SLATE); f.line(240, 76, 260, 76, color=SLATE); f.line(300, 34, 320, 34, color=SLATE); f.line(300, 76, 320, 76, color=SLATE); f.line(320, 34, 320, 76, color=SLATE); f.line(320, 55, 340, 55, color=SLATE)
f.circle(352, 55, 12, fill=SAND, stroke=AMBER, label="L", color=AMBER)
f.text(60, 118, "p  q   lamp", size=10.5, color=SLATE, bold=True); f.text(260, 118, "p  q   lamp", size=10.5, color=SLATE, bold=True)
for i, ((p, q), s, a) in enumerate(zip(rows, ser, par)):
    y = 132 + i * 28
    for x0, v, st, fl in ((14, s, TEAL, MINT), (214, a, AMBER, SAND)):
        f.text(x0 + 10, y + 12, str(p), size=11, color=NAVY, bold=True, vmid=True); f.text(x0 + 46, y + 12, str(q), size=11, color=NAVY, bold=True, vmid=True)
        f.box(x0 + 80, y, 90, 24, "ON" if v else "off", fill=fl if v else SOFT, stroke=st if v else SLATE, color=st if v else SLATE, size=11, bold=True)
f.text(200, 254, "1 = switch closed.  Lamp ON = current flows.", size=10.5, color=SLATE)
```

## 1.7 Eight uses of logic in computing

1. **Program conditions.** Every `if`, `while` and `for` test is a proposition built with AND, OR and NOT. Simplifying a condition with De Morgan's laws makes code shorter and less error-prone. A voter-eligibility check (age ≥ 18 AND citizen AND NOT already registered) is pure logic.
2. **Digital circuits.** Gates implement the connectives, and a processor is millions of them. Minimising a Boolean expression reduces chip area and power. This is the content of Digital Logic and Computer Architecture.
3. **Database queries.** The WHERE clause of SQL is a logical formula, and quantifiers appear as EXISTS and NOT EXISTS. A query such as "students with no unpaid fee" is a *∀* statement in disguise. Understanding logic helps to write correct queries.
4. **Search engines.** Boolean search ("Kathmandu AND hostel NOT expensive") is propositional logic over documents. Advanced filters on job and property sites work the same way.
5. **Program verification.** Preconditions, postconditions and loop invariants are logical statements about a program. Proving them shows the program correct. Aviation and banking software use such proofs.
6. **Artificial intelligence.** Rule-based and expert systems store knowledge as implications and use modus ponens to derive conclusions. A health-post advice tool might hold rules such as "fever AND rash → refer".
7. **Software testing.** Test cases are chosen to cover every combination of truth values of the conditions in a program. A truth table tells how many cases a condition with *n* parts needs, namely $2^{n}$.
8. **Legal and policy rules.** Eligibility rules for scholarships, loans or ConnectIPS limits are implications with several conditions. Writing them as logic exposes gaps and contradictions before they are coded.

## Formula and fact sheet

- $2^{n}$ rows for *n* variables; $2^{2^{n}}$ truth functions.
- $p \to q \equiv \neg p \vee q \equiv \neg q \to \neg p ;\  \neg (p \to q) \equiv p \wedge \neg q$.
- De Morgan for connectives and quantifiers.
- *∀* pairs with →, *∃* pairs with ∧; quantifier order matters.
- Valid: modus ponens, tollens, syllogisms, resolution. Invalid: affirming the consequent, denying the antecedent.
- Proofs: direct, contrapositive, contradiction, cases, counterexample, induction.

## Chapter summary

- Propositions combine through connectives; the truth table decides equivalence, tautology or contradiction.
- Quantifiers extend logic to properties of many objects; negation swaps *∀* and *∃*.
- Valid arguments chain inference rules; invalid ones commit fallacies.
- Proof techniques are templates; choose by the shape of the statement.

## Practice

1. Construct the truth table of $(p \to q) \wedge (\neg q \vee r)$ and decide whether it is a tautology.
2. Show $p \to (q \to r) \equiv (p \wedge q) \to r$ using laws.
3. Write the converse, inverse and contrapositive of "If a number is divisible by 6 then it is divisible by 3".
4. Write the DNF and CNF of $p \leftrightarrow q$.
5. Express with quantifiers: "Every program has a bug" and "Some program has no bug"; negate the first.
6. Is $\forall x \exists y (y > x)$ true over $\mathbb{N}$? Is $\exists y \forall x (y > x)$?
7. Test the validity: $p \to q ,\  q \to r ,\  \neg r \vdash \neg p$.
8. Prove by contradiction that there is no largest prime.
9. Prove or disprove: the sum of two irrational numbers is irrational.
10. How many different truth functions of 3 variables exist?

::: note Answers and worked solutions
**1.** Evaluating $(p \to q) \wedge (\neg q \vee r)$ row by row $(p q r)$: $\mathrm{TTT} = T ,\  \mathrm{TTF} = F ,\  \mathrm{TFT} = F ,\  \mathrm{TFF} = F ,\  \mathrm{FTT} = T ,\  \mathrm{FTF} = F ,\  \mathrm{FFT} = T ,\  \mathrm{FFF} = T$. It is true in 4 of the 8 rows, so it is **not a tautology** (a contingency).

**2.** $p \to (q \to r) \equiv \neg p \vee (\neg q \vee r) \equiv (\neg p \vee \neg q) \vee r \equiv \neg (p \wedge q) \vee r \equiv (p \wedge q) \to r$. ∎

**3.** Converse: if divisible by 3 then divisible by 6 (false: 9). Inverse: if not divisible by 6 then not divisible by 3 (false: 9). Contrapositive: if not divisible by 3 then not divisible by 6 (true).

**4.** DNF: $(p \wedge q) \vee (\neg p \wedge \neg q)$. CNF: $(\neg p \vee q) \wedge (p \vee \neg q)$.

**5.** $\forall x$ (Program(x) → $\exists b$ Bug(b, $x ) ) ;\  \exists x$ (Program(x) ∧ $\neg \exists b$ Bug(b, *x*)); negation of the first is the second.

**6.** $\forall x \exists y (y > x)$ is **true** $(y = x + 1)$. $\exists y \forall x (y > x)$ is **false** (take $x = y$).

**7.** From $q \to r$ and $\neg r$: $\neg q$ (modus tollens). From $p \to q$ and $\neg q$: $\neg p$ (modus tollens). **Valid.**

**8.** Suppose $p_{1} \ldots p_{k}$ are all the primes. $N = p_{1} p_{2} \ldots p_{k} + 1$ is not divisible by any $p_{i}$ (remainder 1), so N has a prime factor not in the list, a contradiction. ∎

**9.** **False**: $\sqrt{2}$ and $- \sqrt{2}$ are irrational but their sum is 0, rational.

**10.** $2^{2^{3}} = 2^{8}$ = **256**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Show by a truth table that $p \to q$ is logically equivalent to its contrapositive $\neg q \to \neg p$, and state the converse and inverse.**

*Introduction.* Two statements are logically equivalent when they have the same truth value for every assignment of their variables. The contrapositive of $p \to q$ is $\neg q \to \neg p$.

*Truth table.*

| *p* | *q* | $p \to q$ | $\neg q$ | $\neg p$ | $\neg q \to \neg p$ |
|---|---|---|---|---|---|
| T | T | T | F | F | T |
| T | F | F | T | F | F |
| F | T | T | F | T | T |
| F | F | T | T | T | T |

The columns for $p \to q$ and $\neg q \to \neg p$ are identical (T, F, T, T), so they are equivalent.

*Related forms.* The **converse** $q \to p$ and the **inverse** $\neg p \to \neg q$ are equivalent to each other but **not** to $p \to q$: with $p = F$ and $q = T$ the original is true while the converse is false.

*Example.* "If it is raining, the road is wet" is equivalent to "if the road is not wet, it is not raining". *Conclusion.* A statement and its contrapositive always agree, which is why a proof of one is a proof of the other.

**Q2 (10 marks). Explain the main proof techniques with one example for each.**

*Introduction.* A proof is a chain of valid inferences from known facts to a conclusion. Different statements suit different techniques (Figure 1.1).

*Techniques.*

1. **Direct proof.** Assume *p* and derive *q*. *Example:* the sum of two even numbers is even. Let a = 2m and $b = 2 n$; then $a + b = 2 (m + n)$, which is even.
2. **Contrapositive.** Prove $\neg q \to \neg p$. *Example:* if $n^{2}$ is even then *n* is even. Suppose *n* is odd, $n = 2 k + 1$; then $n^{2} = 4 k^{2} + 4 k + 1$ is odd. So if *n* is not even, $n^{2}$ is not even.
3. **Contradiction.** Assume the negation and reach an absurdity. *Example:* $\sqrt{2}$ is irrational. Suppose $\sqrt{2} = \frac{a}{b}$ in lowest terms; then $a^{2} = 2 b^{2}$, so a is even, $a = 2 c$, and $b^{2} = 2 c^{2}$, so *b* is even; a and *b* share the factor 2, a contradiction.
4. **Induction.** Prove a base case and the step $P (k) \to P (k + 1)$. *Example:* $1 + 2 + \ldots + n = \frac{n (n + 1)}{2}$ (Unit 4).
5. **Cases.** Split into exhaustive cases. *Example:* $n^{3} - n$ is divisible by 3 for every integer *n*, checking $n = 3 k ,\  3 k + 1 ,\  3 k + 2$.
6. **Counterexample.** To refute "every prime is odd", the single prime 2 suffices.
7. **Existence proofs.** A constructive proof exhibits the object; a non-constructive proof shows one must exist (the pigeonhole principle, Unit 3).
8. **Equivalence proofs.** To prove "p if and only if q", prove both $p \to q$ and $q \to p$.

| Technique | Start from | Typical use |
|---|---|---|
| Direct | *p* | straightforward implications |
| Contrapositive | not *q* | conclusion is a negation or "even" |
| Contradiction | *p* and not *q* | irrationality, non-existence |
| Induction | base and step | statements about all *n* |
| Counterexample | one case | disproving "for all" |

*Conclusion.* Choosing the right technique is half of the proof; the six above cover almost every question in this course.
