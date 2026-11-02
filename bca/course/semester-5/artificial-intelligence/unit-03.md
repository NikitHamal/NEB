---
subject: Artificial Intelligence
grade: BCA Semester 5
unit: 3
title: Knowledge Representation and Reasoning
hours: 15
area: BCA 302 · Artificial Intelligence · Unit 3
---

Search can find a path through a graph someone has already drawn. But an intelligent system also needs to *know* things: that Socrates is a man, that all men are mortal, that an alarm may be triggered by a burglary or an earthquake. This unit shows how knowledge is written down so that a program can reason with it: rules, semantic networks, frames, and above all **logic**, where reasoning becomes symbol manipulation that is guaranteed correct. It ends with reasoning under uncertainty: Bayes' theorem and Bayesian networks.

::: key What this unit gives you
- Knowledge: kinds, issues, properties of a good representation scheme.
- Techniques: rule-based systems, semantic nets, frames, logic.
- Propositional logic: syntax, semantics, entailment, inference rules, resolution.
- First-order logic: quantifiers, unification, resolution, forward and backward chaining.
- Uncertainty: probability, Bayes' rule, Bayesian networks.
:::

## 3.1 Knowledge and its importance

**Data** is raw facts, **information** is data with meaning, and **knowledge** is information organised so that it can be used for decisions. A program with a good algorithm and no knowledge of its domain is weak; many practical systems succeed because they hold a lot of knowledge about a narrow domain.

### Types of knowledge

| Type | Meaning | Example |
|---|---|---|
| Declarative | facts about the world | Kathmandu is the capital of Nepal |
| Procedural | how to do something | the steps for long division |
| Meta-knowledge | knowledge about knowledge | which rule is most reliable |
| Heuristic | rules of thumb from experience | if the fever lasts more than three days, test for typhoid |
| Structural | relations between concepts | a bird is an animal; a wing is part of a bird |

### Issues in knowledge representation

How do we represent *attributes* of objects and the relations between them (is-a, instance-of, part-of)? At what level of **granularity** do we represent knowledge? How do we represent **sets** of objects and **default** knowledge that has exceptions (birds fly, but penguins do not)? How do we select the right structure when a problem arrives, and how do we keep knowledge **consistent** when it changes?

### Properties of a good representation scheme

A good scheme has **representational adequacy** (it can express all the needed knowledge), **inferential adequacy** (new knowledge can be derived), **inferential efficiency** (the inference is fast) and **acquisitional efficiency** (knowledge can be added easily).

## 3.2 Knowledge representation techniques

### Rule-based (production) systems

Knowledge is written as **IF–THEN rules**: `IF engine does not start AND lights are dim THEN battery is flat`. A **production system** has a rule base, a working memory of current facts and an inference engine that matches rules to facts, selects one (conflict resolution) and fires it. Rules are modular and easy to read, which is why they dominate expert systems (Unit 6); their weakness is slow matching in large rule sets and difficulty in representing structure.

### Semantic networks

A **semantic network** is a graph: nodes are concepts and objects, labelled arcs are relations such as *is-a* and *has-part*. It supports **inheritance**: if Tweety is-a canary, canary is-a bird, and bird has wings, then Tweety has wings. Questions are answered by following arcs. Limits: no standard meaning for arcs, awkward for negation and quantifiers, and exceptions need special handling.

### Frames

A **frame** groups all the knowledge about an object or concept into **slots** (attributes) with **facets**: value, default, range, and attached procedures (**if-needed**, **if-added**, **demons**). Frames are arranged in a class hierarchy with inheritance and defaults that sub-frames override.

```
Frame: Student            (is-a: Person)
  name:      [string]
  semester:  [1..8], default 1
  college:   default "unknown"
Frame: BCA-student        (is-a: Student)
  semester:  5            <- overrides the default
  credits:   if-needed: sum the credits of enrolled subjects
```

Frames are the ancestor of object-oriented programming.

### Logic-based representation

Logic offers a *formal language* with a precise meaning and *sound* inference rules. It is the subject of the rest of this section.

## 3.3 Propositional logic

### Syntax and semantics

A **proposition** is a statement that is either true or false. **Atomic sentences** are propositional symbols (P, Q, Rain). **Complex sentences** use the connectives ¬ (not), ∧ (and), ∨ (or), → (implies) and ↔ (if and only if). A **model** assigns true or false to every symbol; the truth value of a sentence in a model comes from the truth tables.

| P | Q | ¬P | P ∧ Q | P ∨ Q | P → Q | P ↔ Q |
|---|---|---|---|---|---|---|
| F | F | T | F | F | T | T |
| F | T | T | F | T | T | F |
| T | F | F | F | T | F | F |
| T | T | F | T | T | T | T |

P → Q is false only when P is true and Q is false; it is equivalent to ¬P ∨ Q. A sentence is **valid** (a tautology) if true in all models, **satisfiable** if true in at least one, **unsatisfiable** if true in none.

### Equivalences and entailment

De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q and ¬(P ∨ Q) ≡ ¬P ∧ ¬Q. Contrapositive: P → Q ≡ ¬Q → ¬P. Double negation: ¬¬P ≡ P. Distributivity of ∧ over ∨ and vice versa.

A knowledge base KB **entails** a sentence α (KB ⊨ α) if α is true in every model in which KB is true. The simplest decision procedure is **model checking** by truth table: with n symbols there are 2ⁿ models (8 for the three symbols P, Q, R below). Inference is **sound** if it derives only entailed sentences and **complete** if it derives all of them.

::: example Entailment by truth table
KB: P → Q, Q → R, P. Query: R. With three symbols there are 2³ = 8 models. The only model that makes all three KB sentences true has P, Q and R all true, and R is true there, so KB ⊨ R. A frequent fallacy is *affirming the consequent*: from P → Q and Q one cannot conclude P (the model P false, Q true satisfies the KB), and the program below confirms KB ⊭ P.
:::

### Inference rules

- **Modus Ponens**: from α → β and α infer β.
- **Modus Tollens**: from α → β and ¬β infer ¬α.
- **And-elimination**: from α ∧ β infer α.
- **Hypothetical syllogism**: from α → β and β → γ infer α → γ.
- **Resolution**: from (α ∨ β) and (¬β ∨ γ) infer (α ∨ γ).

### Conjunctive normal form and resolution

Resolution works on **clauses** (disjunctions of literals) and is **refutation-complete**: to prove KB ⊨ α, add ¬α to the KB, convert everything to **CNF** (a conjunction of clauses) and resolve pairs of clauses until the **empty clause** (a contradiction) appears; then the KB with ¬α is unsatisfiable, so KB ⊨ α.

**Converting to CNF** in four steps: (1) eliminate ↔ and → (α → β becomes ¬α ∨ β); (2) move ¬ inward with De Morgan; (3) remove double negations; (4) distribute ∨ over ∧.

::: example Resolution refutation
Prove R from P → Q, Q → R and P. Clauses: (1) ¬P ∨ Q, (2) ¬Q ∨ R, (3) P. Negated query: (4) ¬R.

| Step | Resolve | Result |
|---|---|---|
| 5 | (3) P with (1) ¬P ∨ Q | Q |
| 6 | (5) Q with (2) ¬Q ∨ R | R |
| 7 | (6) R with (4) ¬R | empty clause ⊥ |

The empty clause shows the clauses are contradictory, so R follows from the KB. The program below finds a refutation mechanically; because it saturates by trying every pair, its derivation takes more steps than the three-step proof above but ends at the same empty clause.
:::

### Horn clauses and chaining

A **Horn clause** has at most one positive literal: `P₁ ∧ P₂ ∧ … ∧ Pₙ → Q` (a *rule*), or a single fact. Most rule-based systems use Horn clauses because inference is linear in the size of the KB.

- **Forward chaining** (data-driven): start from known facts, fire every rule whose premises are satisfied, add the conclusion, repeat until the query is derived or nothing new appears. Good for monitoring and when many conclusions are wanted.
- **Backward chaining** (goal-driven): start from the query and look for rules that conclude it, then try to prove their premises as subgoals. Good for answering a specific question; it is how **Prolog** works.

For the rules A ∧ B → C, C → D, E → F and facts A, B: forward chaining derives C, then D; F is never derived (E is unknown). Backward chaining for D asks for C, then for A and B (known), and succeeds, without ever looking at the E rule.

## 3.4 First-order logic

Propositional logic cannot say "all men are mortal" without listing every man. **First-order (predicate) logic (FOL)** adds **objects**, **predicates** (relations) and **functions**, and the **quantifiers** ∀ (for all) and ∃ (there exists).

| Element | Examples |
|---|---|
| Constants | Socrates, Nepal, 5 |
| Variables | x, y |
| Predicates | Man(x), Loves(x, y), Greater(x, y) |
| Functions | Mother(x), Plus(x, y) |
| Connectives | ¬ ∧ ∨ → ↔ |
| Quantifiers | ∀x, ∃x |

### Translating English to FOL

- "All men are mortal": ∀x (Man(x) → Mortal(x)). The natural connective with ∀ is → ; using ∧ would say *everything* is a man.
- "Some student passed": ∃x (Student(x) ∧ Passed(x)). The natural connective with ∃ is ∧ ; using → would be true if anything is not a student.
- "Every student likes some subject": ∀x (Student(x) → ∃y (Subject(y) ∧ Likes(x, y))).
- "No bird is a mammal": ∀x (Bird(x) → ¬Mammal(x)).
- Negation of quantifiers: ¬∀x P(x) ≡ ∃x ¬P(x) and ¬∃x P(x) ≡ ∀x ¬P(x). The order of mixed quantifiers matters: ∀x ∃y Loves(x, y) ("everyone loves someone") differs from ∃y ∀x Loves(x, y) ("someone is loved by everyone").

### Inference in FOL

**Universal instantiation** replaces a ∀ variable by any constant: from ∀x Man(x) → Mortal(x) get Man(Socrates) → Mortal(Socrates). **Existential instantiation** replaces ∃ by a fresh constant (a **Skolem constant**) or, when it depends on a universally quantified variable, a **Skolem function**. **Generalised Modus Ponens** uses unification.

### Unification

**Unification** finds a substitution θ that makes two expressions identical. Rules: a variable unifies with any term not containing it (the *occurs check*); a constant unifies only with itself; two predicates unify if they have the same name and their arguments unify, applying the substitution consistently.

| Pair | Unifier |
|---|---|
| Knows(John, x) and Knows(John, Jane) | {x / Jane} |
| Knows(John, x) and Knows(y, Mother(y)) | {y / John, x / Mother(John)} |
| P(A, B) and P(B, A) | fails (A and B are different constants) |
| Knows(John, x) and Knows(x, Jane) | fails unless the variables are standardised apart: rename one x to x′ and get {x′ / John, x / Jane} |

The **most general unifier** (MGU) is the least restrictive substitution.

### Resolution in FOL

1. Convert to CNF: eliminate →, move ¬ inward, **standardise variables** apart, **skolemise** existentials, drop ∀, distribute ∨ over ∧.
2. Negate the goal and add it.
3. Resolve clauses with complementary literals that unify; apply the unifier to the resolvent.
4. Stop when the empty clause appears.

::: example Socrates is mortal
Premises: (1) ∀x Man(x) → Mortal(x), (2) Man(Socrates). Goal: Mortal(Socrates).

CNF: (1) ¬Man(x) ∨ Mortal(x); (2) Man(Socrates); negated goal (3) ¬Mortal(Socrates).

Resolve (1) with (3) using {x / Socrates}: ¬Man(Socrates). Resolve that with (2): the empty clause. The goal is proved.
:::

::: example "Curiosity killed the cat" style puzzle (sketch)
"Anyone who loves all animals is loved by someone. Jack loves all animals. Is somebody loved by someone?" Skolemising ∃ introduces a function: for each x, a person f(x) who loves x. Unification binds variables to Jack and f(Jack), and resolution finds the contradiction with the negated goal. The point of the exercise is the Skolem function: the lover depends on x.
:::

### Prolog

**Prolog** programs are Horn clauses and execution is backward chaining with unification and backtracking.

```
man(socrates).
man(plato).
mortal(X) :- man(X).
?- mortal(socrates).     % true
?- mortal(Who).          % Who = socrates ; Who = plato
```

Facts end with a period; `:-` means "if"; names starting with a capital are variables. Lists, recursion and unification make Prolog natural for rule-based and natural-language problems; the lab in this subject can use Prolog or LISP.

## 3.5 Reasoning under uncertainty

Logic assumes facts are true or false and known. Real agents face **uncertainty** from partial observability, noise and laziness (too many exceptions to list). **Probability theory** gives a degree of belief between 0 and 1.

### Probability basics

- **Axioms**: 0 ≤ P(a) ≤ 1; P(true) = 1, P(false) = 0; P(a ∨ b) = P(a) + P(b) − P(a ∧ b).
- **Conditional probability**: P(a | b) = P(a ∧ b) / P(b).
- **Product rule**: P(a ∧ b) = P(a | b) P(b). **Independence**: P(a ∧ b) = P(a) P(b).
- **Total probability**: P(b) = Σ P(b | aᵢ) P(aᵢ).
- **Bayes' rule**: P(a | b) = P(b | a) P(a) / P(b).

::: example A medical test
A disease affects 1 % of a population. A test is positive for 95 % of sick people (sensitivity) and negative for 90 % of healthy ones (specificity), so 10 % of healthy people test positive. P(positive) = 0.01 × 0.95 + 0.99 × 0.10 = **0.1085**. By Bayes' rule P(disease | positive) = 0.01 × 0.95 / 0.1085 = **0.0876**, only about 8.8 %, even though the test looks accurate. The rarity of the disease (the **prior**) dominates: most positives are false positives.
:::

### Bayesian networks

A **Bayesian network** is a directed acyclic graph with a node for each random variable and, for each node, a **conditional probability table** (CPT) given its parents. It represents the full joint distribution compactly: **P(x₁, …, xₙ) = Π P(xᵢ | parents(xᵢ))**. A joint over n Boolean variables needs 2ⁿ − 1 numbers; a network with at most k parents per node needs at most n·2ᵏ.

::: example The burglar alarm
Burglary (B, prior 0.001) and Earthquake (E, prior 0.002) can set off the Alarm (A); two neighbours, John (J) and Mary (M), may call when they hear it. CPT for A: P(A | B, E) = 0.95; P(A | B, ¬E) = 0.94; P(A | ¬B, E) = 0.29; P(A | ¬B, ¬E) = 0.001. John calls with P(J | A) = 0.90 and P(J | ¬A) = 0.05; Mary with P(M | A) = 0.70 and P(M | ¬A) = 0.01. A full joint would need 2⁵ − 1 = 31 numbers; the network needs only 1 + 1 + 4 + 2 + 2 = 10.

One joint entry: P(j, m, a, ¬b, ¬e) = P(j | a) P(m | a) P(a | ¬b, ¬e) P(¬b) P(¬e) = 0.90 × 0.70 × 0.001 × 0.999 × 0.998 = **0.000628**.

Inference by enumeration of P(B | j, m): sum the joint over the hidden variables E and A. P(b, j, m) = 0.000592; P(j, m) = 0.002084. So P(B | j, m) = 0.000592 / 0.002084 = **0.2842**: if both neighbours call, there is a 28 % chance of a burglary. It is not higher because false alarms (earthquakes, or the neighbours' own mistakes) are common compared with the very rare burglary.
:::

Inference algorithms: exact (enumeration, **variable elimination**) and approximate (sampling, **Markov-chain Monte Carlo**). **Naive Bayes** (Unit 4) is the simplest Bayesian network. **Hidden Markov models** and **Kalman filters** are Bayesian networks over time.

### Decision under uncertainty

A **utility function** scores outcomes; a rational agent maximises **expected utility**: EU(a) = Σ P(outcome | a) U(outcome). If the chance of rain is 0.3, an umbrella gives utility 70 when it rains and 80 when it does not, and no umbrella gives 0 when it rains and 100 when it does not: EU(umbrella) = 0.3 × 70 + 0.7 × 80 = 77, EU(no umbrella) = 0.7 × 100 = 70, so take the umbrella.

**Other formalisms** for uncertainty: **certainty factors** (MYCIN, Unit 6), **fuzzy logic** (degrees of truth such as "fairly hot" = 0.7) and **Dempster–Shafer** theory.

## Practising the commands

The first program checks entailment by truth table, finds the resolution refutation mechanically and unifies the examples of this unit.

```python
import itertools
imp = lambda a, b: (not a) or b
def entails(kb, q, syms):
    return all(q(m) for vals in itertools.product([False, True], repeat=len(syms))
               for m in [dict(zip(syms, vals))] if kb(m))
print("KB |= R:", entails(lambda m: imp(m["P"], m["Q"]) and imp(m["Q"], m["R"]) and m["P"], lambda m: m["R"], ["P", "Q", "R"]))
print("KB |= P (affirming the consequent):", entails(lambda m: imp(m["P"], m["Q"]) and m["Q"], lambda m: m["P"], ["P", "Q"]))
def resolve(c1, c2):
    out = []
    for l in c1:
        nl = l[1:] if l.startswith("~") else "~" + l
        if nl in c2: out.append(frozenset((c1 - {l}) | (c2 - {nl})))
    return out
clauses = [frozenset(c) for c in ({"~P", "Q"}, {"~Q", "R"}, {"P"}, {"~R"})]
derived = list(clauses); done = False
while not done:
    for a, b in itertools.combinations(list(derived), 2):
        for r in resolve(a, b):
            if r not in derived:
                derived.append(r); print("resolve", sorted(a), "+", sorted(b), "->", sorted(r) or "EMPTY CLAUSE")
                if not r: done = True; break
        if done: break
def is_var(x): return isinstance(x, str) and x in ("x", "y", "z")
def walk(x, s):
    while is_var(x) and x in s: x = s[x]
    return x
def unify(a, b, s):
    if s is False: return False
    a, b = walk(a, s), walk(b, s)
    if a == b: return s
    if is_var(a): return {**s, a: b}
    if is_var(b): return {**s, b: a}
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b):
        for x, y in zip(a, b):
            s = unify(x, y, s)
            if s is False: return False
        return s
    return False
print(unify(("Knows", "John", "x"), ("Knows", "John", "Jane"), {}))
print(unify(("Knows", "John", "x"), ("Knows", "y", ("Mother", "y")), {}))
print(unify(("P", "A", "B"), ("P", "B", "A"), {}))
```
```output
KB |= R: True
KB |= P (affirming the consequent): False
resolve ['Q', '~P'] + ['R', '~Q'] -> ['R', '~P']
resolve ['Q', '~P'] + ['P'] -> ['Q']
resolve ['R', '~Q'] + ['~R'] -> ['~Q']
resolve ['Q', '~P'] + ['~Q'] -> ['~P']
resolve ['R', '~Q'] + ['Q'] -> ['R']
resolve ['Q'] + ['~Q'] -> EMPTY CLAUSE
{'x': 'Jane'}
{'y': 'John', 'x': ('Mother', 'y')}
False
```
The second program computes Bayes' rule for the medical test and enumerates the burglar-alarm network.

```python
pd, sens, spec = 0.01, 0.95, 0.90
ppos = pd * sens + (1 - pd) * (1 - spec)
print("P(positive) = %.4f   P(disease | positive) = %.4f" % (ppos, pd * sens / ppos))
def joint(b, e, a, j, m):
    pb = .001 if b else .999; pe = .002 if e else .998
    pa = {(1, 1): .95, (1, 0): .94, (0, 1): .29, (0, 0): .001}[(b, e)]; pa = pa if a else 1 - pa
    pj = (.90 if a else .05) if j else (.10 if a else .95)
    pm = (.70 if a else .01) if m else (.30 if a else .99)
    return pb * pe * pa * pj * pm
print("P(j,m,a,~b,~e) = %.6f" % joint(0, 0, 1, 1, 1))
num = sum(joint(1, e, a, 1, 1) for e in (0, 1) for a in (0, 1))
den = sum(joint(b, e, a, 1, 1) for b in (0, 1) for e in (0, 1) for a in (0, 1))
print("P(b,j,m) = %.6f  P(j,m) = %.6f  P(B | j,m) = %.4f" % (num, den, num / den))
print("expected utility: umbrella", 0.3 * 70 + 0.7 * 80, " no umbrella", 0.7 * 100)
```
```output
P(positive) = 0.1085   P(disease | positive) = 0.0876
P(j,m,a,~b,~e) = 0.000628
P(b,j,m) = 0.000592  P(j,m) = 0.002084  P(B | j,m) = 0.2842
expected utility: umbrella 77.0  no umbrella 70.0
```
## Formula and fact sheet

- P → Q ≡ ¬P ∨ Q ≡ ¬Q → ¬P. De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q. n symbols give 2ⁿ models.
- Modus Ponens: α → β, α ⊢ β. Resolution: (α ∨ β), (¬β ∨ γ) ⊢ (α ∨ γ). Refutation: add ¬goal and derive the empty clause.
- FOL: ∀ goes with →, ∃ goes with ∧. ¬∀x P ≡ ∃x ¬P. Unify with the most general substitution.
- Forward chaining is data-driven; backward chaining is goal-driven (Prolog).
- Bayes: P(a | b) = P(b | a) P(a) / P(b). Network joint = Π P(xᵢ | parents).
- Expected utility EU(a) = Σ P(s | a) U(s).

## Chapter summary

- Knowledge can be held as rules, semantic networks, frames or logic; a good scheme is adequate, inferentially efficient and easy to extend.
- Propositional logic gives sound, complete reasoning by truth table or resolution; Horn clauses allow efficient forward and backward chaining.
- First-order logic adds objects, relations and quantifiers; unification and resolution (with Skolemisation) prove theorems mechanically; Prolog implements the idea.
- Under uncertainty, probability and Bayes' rule update beliefs; Bayesian networks factor the joint distribution into small CPTs and answer queries by enumeration or sampling.

## Practice

1. Compare rules, semantic nets and frames for representing knowledge about vehicles.
2. Build the truth table of P → Q and show it equals ¬P ∨ Q.
3. Show by truth table that {P → Q, Q → R, P} entails R, and that {P → Q, Q} does not entail P.
4. Prove R from {P → Q, Q → R, P} by resolution refutation.
5. Translate: (a) "Every student who studies passes." (b) "Some student failed." (c) "No cat is a dog."
6. Unify Knows(John, x) with Knows(y, Mother(y)); explain why P(A, B) and P(B, A) do not unify.
7. Prove Mortal(Socrates) from ∀x Man(x) → Mortal(x) and Man(Socrates) by resolution.
8. With rules A ∧ B → C, C → D, E → F and facts A, B, show forward and backward chaining for D.
9. A test with 95 % sensitivity and 90 % specificity is applied to a 1 % prevalence disease. Find P(disease | positive).
10. For the burglar-alarm network compute P(j, m, a, ¬b, ¬e) and explain why P(B | j, m) is only 0.28.
11. How many numbers does the alarm network need compared with the full joint?

::: note Answers and worked solutions
**1.** Rules: IF has-wheels AND has-engine THEN motor-vehicle (modular, no structure). Semantic net: Car is-a Vehicle, Vehicle has-part Wheel (inheritance, no precise semantics). Frame: Car with slots wheels = 4, fuel, owner, default values, inherited from Vehicle.
**2.** Rows (P, Q): FF → T, FT → T, TF → F, TT → T. ¬P ∨ Q has the same four values.
**3.** Only the row P = Q = R = true satisfies the KB and R is true there, so R is entailed. For {P → Q, Q}: the model P = false, Q = true satisfies the KB but not P, so P is not entailed.
**4.** Clauses ¬P ∨ Q, ¬Q ∨ R, P, ¬R. Resolve P with ¬P ∨ Q to get Q; Q with ¬Q ∨ R to get R; R with ¬R to get the empty clause.
**5.** (a) ∀x (Student(x) ∧ Studies(x) → Passes(x)). (b) ∃x (Student(x) ∧ Failed(x)). (c) ∀x (Cat(x) → ¬Dog(x)).
**6.** {y / John, x / Mother(John)}. P(A, B) and P(B, A) require A = B, but they are distinct constants, so unification fails.
**7.** Clauses ¬Man(x) ∨ Mortal(x), Man(Socrates), ¬Mortal(Socrates). Resolving the first and third with {x / Socrates} gives ¬Man(Socrates); with Man(Socrates) it gives the empty clause.
**8.** Forward: from A, B fire A ∧ B → C, then C → D; the E rule never fires. Backward: D needs C (rule C → D); C needs A and B (rule A ∧ B → C); both are facts, so D is proved.
**9.** P(positive) = 0.01 × 0.95 + 0.99 × 0.10 = 0.1085; P(disease | positive) = 0.0095 / 0.1085 = 0.0876.
**10.** 0.90 × 0.70 × 0.001 × 0.999 × 0.998 = 0.000628. P(B | j, m) = 0.000592 / 0.002084 = 0.2842: burglaries are very rare (0.001), so even two calls leave false alarms as the more probable explanation in most cases.
**11.** The network: 1 + 1 + 4 + 2 + 2 = 10 numbers; the full joint over five Boolean variables: 2⁵ − 1 = 31.
:::
