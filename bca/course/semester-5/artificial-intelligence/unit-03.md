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

- **Axioms**: 0 ≤ P(α) ≤ 1; P(true) = 1, P(false) = 0; P(α ∨ β) = P(α) + P(β) − P(α ∧ β).
- **Conditional probability**: P(α | β) = P(α ∧ β) / P(β).
- **Product rule**: P(α ∧ β) = P(α | β) P(β). **Independence**: P(α ∧ β) = P(α) P(β).
- **Total probability**: P(β) = Σ P(β | αᵢ) P(αᵢ).
- **Bayes' rule**: P(α | β) = P(β | α) P(α) / P(β).

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
## 3.6 Seeing the ideas: logicians, rules, networks and probabilities

Knowledge representation is abstract until you run it. Plate 3.1 shows four figures behind logic: Aristotle (the syllogism), George Boole (algebra of true and false), Gottlob Frege (quantifiers and predicate logic) and Socrates, the man of the most famous syllogism. Plate 3.2 shows four people behind the tools of this unit: Alain Colmerauer (Prolog), Edward Feigenbaum (expert systems and rules), Marvin Minsky (frames) and Judea Pearl (Bayesian networks). Plate 3.3 uses a canary and a penguin to show inheritance with exceptions, and Plate 3.4 shows the objects of the two uncertainty examples: a burglar alarm and a medical test, with the tomb of Thomas Bayes. Figures 3.1 to 3.12 then run the ideas: every trace, truth value and probability is computed by the figure code.

```photogrid label="3.1" cols="4" ratio="1.0" caption="Four figures behind logic. (a) Aristotle (Roman copy of a Greek bust, public domain), who set out the syllogism: all men are mortal, Socrates is a man, so Socrates is mortal. (b) George Boole (portrait, public domain), whose 1854 book treated true and false as algebra: the AND, OR and NOT of propositional logic. (c) Gottlob Frege (public domain), who invented predicates and quantifiers in 1879, the basis of first-order logic. (d) Socrates (Louvre bust, public domain), the man in the textbook example that every resolution proof in this unit repeats."
@ photo id="bca302/aristotle" cap="Aristotle: the syllogism"
fit 1.0
focus 0.5 0.3
@ photo id="bca302/boole" cap="George Boole: logic as algebra"
fit 1.0
focus 0.5 0.3
@ photo id="bca302/frege" cap="Gottlob Frege: quantifiers"
fit 1.0
focus 0.6 0.35
@ photo id="bca302/socrates" cap="Socrates: the mortal man"
fit 1.0
focus 0.5 0.35
```

```photogrid label="3.2" cols="4" ratio="1.0" caption="Four builders of the tools. (a) Alain Colmerauer (CC BY-SA 4.0), who created Prolog at Marseille in 1972, the language whose programs are Horn clauses run by backward chaining. (b) Edward Feigenbaum (CC BY 2.0), leader of the Stanford projects DENDRAL and MYCIN, the first successful rule-based expert systems. (c) Marvin Minsky (CC BY-SA 2.0), who proposed frames in 1974 as a way to store typical knowledge with defaults. (d) Judea Pearl at a poster on graphical models (CC BY 2.0), who made Bayesian networks the standard tool for reasoning under uncertainty and won the Turing Award in 2011."
@ photo id="bca302/colmerauer" cap="Alain Colmerauer: Prolog"
fit 1.0
focus 0.3 0.4
@ photo id="bca302/feigenbaum" cap="Edward Feigenbaum: expert systems"
fit 1.0
focus 0.5 0.35
@ photo id="bca302/minsky" cap="Marvin Minsky: frames"
fit 1.0
focus 0.5 0.35
@ photo id="bca302/pearl" cap="Judea Pearl: Bayesian networks"
fit 1.0
focus 0.5 0.45
```

```photogrid label="3.3" cols="3" ratio="1.0" caption="Inheritance with an exception. (a) A canary (CC0): the knowledge base says a canary is a bird and birds fly, so a canary flies by default. (b) An emperor penguin sliding on its belly (CC BY 4.0): a penguin is also a bird, but it overrides the default and cannot fly. (c) The lookup computed by the figure code: a value is searched up the is-a chain and the nearest one wins, so Tweety (a canary) inherits can-fly = yes from Bird, two steps up, while Pingu (a penguin) finds can-fly = no one step up and never reaches the default."
@ photo id="bca302/canary" cap="Canary: a bird, so it flies"
fit 1.0
focus 0.5 0.4
@ photo id="bca302/penguin" cap="Penguin: a bird that cannot fly"
fit 1.0
focus 0.55 0.6
@ svg cap="Nearest value wins"
f = Fig(300, 300)
net = {"Animal": {"alive": "yes"}, "Bird": {"isa": "Animal", "can-fly": "yes", "has": "wings"}, "Canary": {"isa": "Bird"}, "Penguin": {"isa": "Bird", "can-fly": "no"}, "Tweety": {"isa": "Canary"}, "Pingu": {"isa": "Penguin"}}
def get(o, slot):
    hops = 0
    while o:
        if slot in net[o]: return net[o][slot], o, hops
        o = net[o].get("isa"); hops += 1
assert get("Tweety", "can-fly") == ("yes", "Bird", 2) and get("Pingu", "can-fly") == ("no", "Penguin", 1) and get("Pingu", "has") == ("wings", "Bird", 2)
f.text(150, 18, "search up the is-a chain", size=13, color=NAVY, bold=True)
for i, (o, s) in enumerate([("Tweety", "can-fly"), ("Pingu", "can-fly"), ("Pingu", "has")]):
    v, src, h = get(o, s)
    y = 34 + i * 88
    f.box(8, y, 284, 78, "%s . %s ?\n%s\nfound in %s,\n%d step%s up" % (o, s, v.upper(), src, h, "" if h == 1 else "s"), fill=MINT if v == "yes" or v == "wings" else SAND, stroke=TEAL if v != "no" else AMBER, size=13, r=8, bold=True, color=NAVY, sw=1.8)
```

```photogrid label="3.4" cols="3" ratio="1.0" caption="The objects of the two uncertainty examples. (a) An old burglar-alarm siren with its cover off (CC BY-SA 3.0): a sensor that sounds when it thinks a burglar is present but can also be set off by something harmless, the alarm of the Bayesian network in Fig. 3.11. (b) A rapid test cassette (CC BY-SA 4.0): like every test it has a sensitivity and a false-positive rate, so a positive result must be combined with how common the disease is (Fig. 3.10). (c) The tomb of Thomas Bayes in Bunhill Fields, London (CC BY-SA 2.0): the English minister whose rule for updating a belief from evidence was published after his death in 1763."
@ photo id="bca302/siren" cap="Alarm siren: noisy evidence"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/testkit" cap="Rapid test: sensitivity and false positives"
fit 1.0
focus 0.4 0.4
@ photo id="bca302/bayestomb" cap="Tomb of Thomas Bayes, London"
fit 1.0
focus 0.5 0.45
```

```svgfig label="3.1" caption="A production system running its recognise-act cycle, computed in the figure code. The five rules (left) are matched against the working memory {no_start, dim_lights, horn_weak}. In each cycle the conflict set is every rule whose conditions all hold and which has not yet fired; the strategy picks the most specific rule (most conditions), and the first listed on a tie. R1 fires first although the shorter R5 also matches, R2 and R3 follow as new facts appear, and R5 finally fires when nothing else matches. R4 never fires because fuel_empty is never known. The run stops after four cycles with no rule left to fire."
f = Fig(580, 262)
rules = [("R1", ["no_start", "dim_lights"], "battery_weak"), ("R2", ["horn_weak", "battery_weak"], "battery_flat"), ("R3", ["battery_flat"], "ACTION: jump-start or replace battery"), ("R4", ["no_start", "fuel_empty"], "ACTION: refuel"), ("R5", ["no_start"], "ACTION: check the fuel gauge")]
wm = {"no_start", "dim_lights", "horn_weak"}; fired = []; trace = []
while True:
    cs = [r for r in rules if r[0] not in fired and all(c in wm for c in r[1])]
    if not cs: break
    pick = max(cs, key=lambda r: (len(r[1]), -rules.index(r)))
    fired.append(pick[0]); wm.add(pick[2])
    trace.append(([r[0] for r in cs], pick[0], pick[2]))
assert fired == ["R1", "R2", "R3", "R5"] and "R4" not in fired and len(trace) == 4
f.text(140, 14, "rule base (IF ... THEN ...)", size=10.5, color=NAVY, bold=True)
for i, (n, c, t) in enumerate(rules):
    y = 24 + i * 40
    used = n in fired
    f.box(6, y, 268, 34, "%s IF %s\nTHEN %s" % (n, " AND ".join(c), t), fill=MINT if used else "#f1f5f9", stroke=TEAL if used else "#94a3b8", size=9.5, r=5, color=NAVY, anchor="start", dash=not used)
f.text(430, 14, "recognise-act trace (computed)", size=10.5, color=NAVY, bold=True)
for k, hd in enumerate([("cycle", 304, "middle"), ("conflict set", 326, "start"), ("fires", 432, "middle"), ("adds to memory", 462, "start")]):
    f.text(hd[1], 38, hd[0], size=9.5, color=SLATE, bold=True, anchor=hd[2])
for i, (cs, fr, add) in enumerate(trace):
    y = 46 + i * 38
    f.box(290, y, 284, 32, "", fill=BLUE, stroke=NAVY, r=5, sw=1.2)
    f.text(304, y + 16, str(i + 1), size=11, color=NAVY, bold=True, vmid=True)
    f.text(326, y + 16, ", ".join(cs), size=10, color=SLATE, anchor="start", vmid=True)
    f.text(432, y + 16, fr, size=11, color=TEAL, bold=True, vmid=True)
    f.text(462, y + 9, add if not add.startswith("ACTION") else "ACTION", size=9.5, color=RED, bold=True, anchor="start", vmid=True)
    if add.startswith("ACTION"): f.text(462, y + 22, add[8:].replace("jump-start or replace battery", "jump-start or replace").replace("check the fuel gauge", "check fuel gauge"), size=9.5, color=SLATE, anchor="start", vmid=True)
facts_left = [x for x in sorted(wm) if not x.startswith("ACTION")]
assert facts_left == ["battery_flat", "battery_weak", "dim_lights", "horn_weak", "no_start"]
f.box(290, 202, 284, 50, "memory at the end: no_start, dim_lights, horn_weak,\nbattery_weak, battery_flat (+ 2 actions)\nR4 never fires (fuel_empty unknown)", fill=SAND, stroke=AMBER, size=9.5, r=5, color=NAVY)
```

```svgfig label="3.2" caption="A semantic network with inheritance and an exception. Boxes are concepts with their own slots; arrows are is-a links. The lookup code walks up the links and returns the first value it finds, so Tweety (a canary, which is a bird, which is an animal) inherits can-fly = yes from Bird two steps up, Pingu inherits can-fly = no from Penguin one step up because Penguin overrides the default of Bird, and Pingu still inherits has = wings from Bird. Default reasoning with exceptions is what makes semantic networks and frames more convenient than plain logic, where 'birds fly' followed by 'penguins do not' would be a contradiction."
f = Fig(580, 262)
net = {"Animal": {"alive": "yes"}, "Bird": {"isa": "Animal", "can-fly": "yes", "has": "wings"}, "Canary": {"isa": "Bird", "colour": "yellow"}, "Penguin": {"isa": "Bird", "can-fly": "no"}, "Tweety": {"isa": "Canary"}, "Pingu": {"isa": "Penguin"}}
def get(o, slot):
    hops = 0
    while o:
        if slot in net[o]: return net[o][slot], o, hops
        o = net[o].get("isa"); hops += 1
assert get("Tweety", "can-fly") == ("yes", "Bird", 2) and get("Pingu", "can-fly") == ("no", "Penguin", 1) and get("Pingu", "has") == ("wings", "Bird", 2)
def nb(cx, cy, w, h, lab, fl, st):
    f.box(cx - w / 2, cy - h / 2, w, h, lab, fill=fl, stroke=st, size=9.5, r=6, color=NAVY, bold=False, sw=1.6)
nb(170, 30, 140, 34, "Animal\nalive: yes", SAND, AMBER)
nb(170, 96, 180, 42, "Bird\ncan-fly: yes   has: wings", BLUE, NAVY)
nb(70, 172, 124, 40, "Canary\ncolour: yellow", BLUE, NAVY)
nb(270, 172, 136, 40, "Penguin\ncan-fly: no (override)", "#fee2e2", RED)
nb(70, 232, 100, 28, "Tweety", MINT, TEAL)
nb(270, 232, 100, 28, "Pingu", MINT, TEAL)
for a, b in [((170, 75), (170, 47)), ((100, 152), (140, 117)), ((240, 152), (200, 117)), ((70, 218), (70, 192)), ((270, 218), (270, 192))]:
    f.arrow([a, b], color=NAVY, sw=1.6)
    f.text((a[0] + b[0]) / 2 + 17, (a[1] + b[1]) / 2 + 3, "is-a", size=9.5, color=SLATE, bold=True)
f.text(470, 18, "inheritance lookups (computed)", size=10.5, color=NAVY, bold=True)
for i, (o, s) in enumerate([("Tweety", "can-fly"), ("Pingu", "can-fly"), ("Pingu", "has")]):
    v, src, h = get(o, s)
    f.box(380, 30 + i * 74, 192, 64, "%s . %s ?\n%s (from %s,\n%d step%s up)" % (o, s, v, src, h, "" if h == 1 else "s"), fill=SAND if v == "no" else MINT, stroke=AMBER if v == "no" else TEAL, size=10.5, r=7, bold=True, color=NAVY, sw=1.6)
```

```svgfig label="3.3" caption="A frame hierarchy and the slot values that result, computed in the figure code. Student is the general frame with a default semester of 1, a default college of 'unknown' and a credits slot with an if-needed procedure (sum the credits of enrolled courses). BCA-student is-a Student and overrides semester with 5. The instance asha is-a BCA-student with her own name and four 3-credit courses. Resolving each slot of asha gives semester 5 (override in BCA-student), college unknown (default of Student), name Asha (own value) and credits 12 (computed by the if-needed procedure when asked). Frames are the ancestor of classes with inheritance in object-oriented programming."
f = Fig(580, 252)
frames = {"Student": {"isa": None, "semester": ("default", 1), "college": ("default", "unknown"), "credits": ("if-needed", lambda o: sum(c for _, c in o.get("courses", [])))},
          "BCA-student": {"isa": "Student", "semester": ("value", 5)},
          "asha": {"isa": "BCA-student", "name": ("value", "Asha"), "courses": ("value", [("course A", 3), ("course B", 3), ("course C", 3), ("course D", 3)])}}
def slot(o, s):
    cur = o
    while cur:
        fr = frames[cur]
        if s in fr: return fr[s], cur
        cur = fr["isa"]
own = {"courses": frames["asha"]["courses"][1]}
res = {}
for s in ["semester", "college", "name", "credits"]:
    (kind, v), src = slot("asha", s)
    res[s] = (v(own) if kind == "if-needed" else v, kind, src)
assert res == {"semester": (5, "value", "BCA-student"), "college": ("unknown", "default", "Student"), "name": ("Asha", "value", "asha"), "credits": (12, "if-needed", "Student")}
bx = [(8, "Student", ["semester: default 1", "college: default 'unknown'", "credits: if-needed", "  sum of course credits"], SAND, AMBER), (200, "BCA-student  (is-a Student)", ["semester: 5", "  overrides the default"], BLUE, NAVY), (392, "asha  (instance)", ["name: Asha", "courses: 4 x 3 credits"], MINT, TEAL)]
for x, t, ls, fl, st in bx:
    f.box(x, 8, 180, 100, "", fill=fl, stroke=st, r=7, sw=1.8)
    f.text(x + 90, 24, t, size=10, color=NAVY, bold=True)
    f.line(x + 8, 33, x + 172, 33, color=st, sw=1)
    for i, l in enumerate(ls): f.text(x + 10, 48 + i * 15, l, size=9.5, color=SLATE, anchor="start")
f.arrow([(392, 58), (380, 58)], color=NAVY, sw=1.8); f.arrow([(200, 58), (188, 58)], color=NAVY, sw=1.8)
f.text(290, 126, "resolved view of asha (computed by the lookup)", size=10.5, color=NAVY, bold=True)
for k, hd in enumerate([("slot", 16, "start"), ("value", 130, "start"), ("kind", 250, "start"), ("taken from", 360, "start")]):
    f.text(hd[1], 144, hd[0], size=9.5, color=SLATE, bold=True, anchor=hd[2])
for i, s in enumerate(["semester", "college", "name", "credits"]):
    v, kind, src = res[s]
    y = 152 + i * 24
    f.box(8, y, 564, 21, "", fill=MINT if kind == "value" else SAND, stroke=TEAL if kind == "value" else AMBER, r=4, sw=1.1)
    f.text(16, y + 10.5, s, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(130, y + 10.5, str(v), size=10, color=RED, bold=True, anchor="start", vmid=True)
    f.text(250, y + 10.5, kind, size=10, color=SLATE, anchor="start", vmid=True)
    f.text(360, y + 10.5, src, size=10, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="3.4" caption="Truth tables and equivalences checked by machine. Left: the truth table of the five connectives computed over the four models of P and Q (green is true, red is false); the implication is false only when P is true and Q is false. Right: each equivalence of the unit is tested over every model: P implies Q equals not-P or Q; the contrapositive equals the original; both De Morgan laws hold; but the converse Q implies P is NOT equivalent. Bottom: the number of models grows as 2 to the power n (log scale), 8 for three symbols but over a billion for thirty, which is why truth-table checking is replaced by resolution for large knowledge bases."
f = Fig(580, 284)
it = __import__("itertools"); cm = __import__("math")
rows = list(it.product([False, True], repeat=2))
cols = [("P", lambda p, q: p), ("Q", lambda p, q: q), ("¬P", lambda p, q: not p), ("P∧Q", lambda p, q: p and q), ("P∨Q", lambda p, q: p or q), ("P→Q", lambda p, q: (not p) or q), ("P↔Q", lambda p, q: p == q)]
tt = [[fn(p, q) for _, fn in cols] for p, q in rows]
assert tt == [[False, False, True, False, False, True, True], [False, True, True, False, True, True, False], [True, False, False, False, True, False, False], [True, True, False, True, True, True, True]]
f.text(190, 14, "truth table (computed)", size=10.5, color=NAVY, bold=True)
for j, (nm, _) in enumerate(cols): f.text(30 + j * 50, 34, nm, size=10.5, color=NAVY, bold=True)
for i, r in enumerate(tt):
    for j, v in enumerate(r): f.box(8 + j * 50, 42 + i * 26, 44, 22, "T" if v else "F", fill="#bbf7d0" if v else "#fecaca", stroke=TEAL if v else RED, r=4, size=11, bold=True, color=NAVY, sw=1.2)
imp = lambda a, b: (not a) or b
eqs = [("P→Q  ≡  ¬P∨Q", lambda p, q: imp(p, q) == ((not p) or q)), ("P→Q  ≡  ¬Q→¬P", lambda p, q: imp(p, q) == imp(not q, not p)), ("¬(P∧Q)  ≡  ¬P∨¬Q", lambda p, q: (not (p and q)) == ((not p) or (not q))), ("¬(P∨Q)  ≡  ¬P∧¬Q", lambda p, q: (not (p or q)) == ((not p) and (not q))), ("P→Q  ≡  Q→P", lambda p, q: imp(p, q) == imp(q, p))]
verd = [all(fn(p, q) for p, q in rows) for _, fn in eqs]
assert verd == [True, True, True, True, False]
f.text(470, 14, "equivalence tests", size=10.5, color=NAVY, bold=True)
for i, ((t, _), v) in enumerate(zip(eqs, verd)):
    y = 26 + i * 33
    f.box(376, y, 196, 28, "", fill="#bbf7d0" if v else "#fecaca", stroke=TEAL if v else RED, r=5, sw=1.2)
    f.text(384, y + 14, t, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(562, y + 14, "holds" if v else "NOT", size=10, color=TEAL if v else RED, bold=True, anchor="end", vmid=True)
f.text(290, 202, "models of n symbols = 2^n (log scale)", size=10.5, color=NAVY, bold=True)
for i, n in enumerate([3, 10, 20, 30]):
    v = 2 ** n
    y = 212 + i * 18
    w = cm.log10(v) * 40
    f.text(8, y + 7, "n = %d" % n, size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(56, y, w, 14, "", fill=SAND if n < 20 else "#fee2e2", stroke=AMBER if n < 20 else RED, r=2, sw=1)
    f.text(56 + w + 6, y + 7, "{:,}".format(v), size=10, color=AMBER if n < 20 else RED, bold=True, anchor="start", vmid=True)
assert 2 ** 30 == 1073741824
```

```svgfig label="3.5" caption="Entailment by model checking, computed. Left: all 8 models of P, Q and R with the truth value of each sentence of the knowledge base {P implies Q, Q implies R, P}. Only one model, with P, Q and R all true, satisfies the whole knowledge base, and R is true there, so the knowledge base entails R. Right: for the knowledge base {P implies Q, Q} there are two models (P false, Q true and P true, Q true), and P is false in the first, so the knowledge base does not entail P: concluding P from P implies Q and Q is the fallacy of affirming the consequent."
f = Fig(580, 262)
it = __import__("itertools")
imp = lambda a, b: (not a) or b
M = list(it.product([False, True], repeat=3))
kbrows = [(p, q, r, imp(p, q), imp(q, r), p, imp(p, q) and imp(q, r) and p) for p, q, r in M]
good = [m for m, k in zip(M, kbrows) if k[6]]
assert good == [(True, True, True)] and all(m[2] for m in good)
f.text(170, 14, "KB = {P→Q, Q→R, P}: 8 models", size=10.5, color=NAVY, bold=True)
for j, h in enumerate(["P", "Q", "R", "P→Q", "Q→R", "P", "KB"]): f.text(26 + j * 44, 34, h, size=10, color=NAVY, bold=True)
for i, k in enumerate(kbrows):
    for j, v in enumerate(k):
        isb = (j == 6)
        f.box(6 + j * 44, 42 + i * 24, 40, 20, "T" if v else "F", fill="#bbf7d0" if v else "#fecaca", stroke=TEAL if v else RED, r=3, size=10, bold=True, color=NAVY, sw=2.2 if (isb and v) else 1)
f.box(6, 238, 312, 18, "only (T,T,T) works: KB entails R", fill=MINT, stroke=TEAL, size=9.5, r=4, color=NAVY, bold=True)
N = list(it.product([False, True], repeat=2))
rows2 = [(p, q, imp(p, q), q, imp(p, q) and q) for p, q in N]
goodN = [(p, q) for p, q in N if imp(p, q) and q]
assert goodN == [(False, True), (True, True)] and not all(p for p, q in goodN)
f.text(460, 14, "KB = {P→Q, Q}: 4 models", size=10.5, color=NAVY, bold=True)
for j, h in enumerate(["P", "Q", "P→Q", "Q", "KB"]): f.text(344 + j * 44, 34, h, size=10, color=NAVY, bold=True)
for i, k in enumerate(rows2):
    for j, v in enumerate(k):
        f.box(324 + j * 44, 42 + i * 24, 40, 20, "T" if v else "F", fill="#bbf7d0" if v else "#fecaca", stroke=TEAL if v else RED, r=3, size=10, bold=True, color=NAVY, sw=2.2 if (j == 4 and v) else 1)
f.box(324, 148, 248, 58, "KB models: (P=F, Q=T) and (P=T, Q=T)\nP is false in the first one,\nso KB does NOT entail P\n(affirming the consequent)", fill=SAND, stroke=AMBER, size=9.5, r=5, color=NAVY, bold=True)
```

```svgfig label="3.6" caption="Resolution refutation of R from the knowledge base P implies Q, Q implies R, P. The clauses are (1) not-P or Q, (2) not-Q or R, (3) P and the negated query (4) not-R. Each resolvent is computed by the figure code from its two parents: clause (3) with (1) removes P and gives Q (5); (5) with (2) removes Q and gives R (6); (6) with (4) removes R and leaves the empty clause (7), a contradiction, so the knowledge base entails R. The program also saturates the clause set (resolving every pair until nothing new appears) and finds the empty clause there too, as the right-hand box reports; saturation always finds a refutation when one exists, but it may derive many useless clauses on the way."
f = Fig(580, 270)
def lit_neg(l): return l[1:] if l.startswith("~") else "~" + l
def resolvents(a, b):
    out = []
    for l in a:
        if lit_neg(l) in b:
            out.append(frozenset((a - {l}) | (b - {lit_neg(l)})))
    return out
C = {1: frozenset({"~P", "Q"}), 2: frozenset({"~Q", "R"}), 3: frozenset({"P"}), 4: frozenset({"~R"})}
c5 = resolvents(C[3], C[1]); assert c5 == [frozenset({"Q"})]
c6 = resolvents(c5[0], C[2]); assert c6 == [frozenset({"R"})]
c7 = resolvents(c6[0], C[4]); assert c7 == [frozenset()]
S = set(C.values()); derived = 0; empty = False
while not empty:
    new = set()
    for a in list(S):
        for b in list(S):
            for r in resolvents(a, b):
                if r not in S: new.add(r)
    if not new: break
    derived += len(new); S |= new
    empty = frozenset() in S
assert empty
def txt(c):
    return " ∨ ".join(("¬" + l[1:]) if l.startswith("~") else l for l in sorted(c)) if c else "empty"
nodes = {1: (170, 34), 2: (276, 34), 3: (60, 34), 4: (382, 34), 5: (115, 112), 6: (196, 170), 7: (289, 228)}
labels = {1: "(1) " + txt(C[1]), 2: "(2) " + txt(C[2]), 3: "(3) " + txt(C[3]), 4: "(4) " + txt(C[4]), 5: "(5) " + txt(c5[0]), 6: "(6) " + txt(c6[0]), 7: "(7) " + txt(c7[0])}
for a, b, c in [(3, 1, 5), (5, 2, 6), (6, 4, 7)]:
    for p in (a, b):
        f.arrow([(nodes[p][0], nodes[p][1] + 16), (nodes[c][0] + (-14 if p in (a,) else 14) * 0, nodes[c][1] - 16)], color=NAVY, sw=1.6)
for k, (x, y) in nodes.items():
    base = k <= 4
    f.box(x - 52, y - 16, 104, 32, labels[k], fill=BLUE if base else (MINT if k < 7 else "#bbf7d0"), stroke=NAVY if base else TEAL, size=10.5, r=6, bold=True, color=NAVY, sw=1.6 if k < 7 else 2.6)
f.box(440, 20, 130, 150, "knowledge base:\nP → Q\nQ → R\nP\n\nnegated query:\n¬R", fill=SAND, stroke=AMBER, size=10.5, r=6, color=NAVY, bold=True)
f.box(380, 196, 192, 62, "saturation also finds the\nempty clause after %d\nderived clauses" % derived, fill="#f1f5f9", stroke="#94a3b8", size=10, r=6, color=NAVY, bold=True)
f.text(100, 262, "arrows: parents to resolvent", size=9.5, color=SLATE, italic=True)
```

```svgfig label="3.7" caption="Forward and backward chaining on the same rules A and B imply C, C implies D, E implies F, with the facts A and B, computed in the figure code. Left: forward chaining (data-driven) fires every rule whose premises are known: first A and B imply C, then C implies D, and the rule E implies F never fires because E is unknown, so F is never derived (grey dashed); 2 of the 3 rules fire. Right: backward chaining (goal-driven) starts from the query D and asks which rule concludes it: C implies D needs C, A and B imply C needs A and B, and both are facts, so D is proved after looking at only 2 rules and never touching the E rule. Prolog works this way."
f = Fig(580, 262)
rules = [(("A", "B"), "C"), (("C",), "D"), (("E",), "F")]
facts = {"A", "B"}; known = set(facts); fwd = []; changed = True
while changed:
    changed = False
    for p, c in rules:
        if all(x in known for x in p) and c not in known:
            known.add(c); fwd.append((p, c)); changed = True
assert [c for _, c in fwd] == ["C", "D"] and "F" not in known and len(fwd) == 2
calls = []
def prove(g):
    calls.append(g)
    if g in facts: return True
    for p, c in rules:
        if c == g and all(prove(x) for x in p): return True
    return False
assert prove("D") and calls == ["D", "C", "A", "B"]
f.text(140, 14, "forward chaining (data-driven)", size=10.5, color=NAVY, bold=True)
for x, n, ok in [(50, "A", True), (110, "B", True), (230, "E", False)]:
    f.circle(x, 48, 15, fill=MINT if ok else "#f1f5f9", stroke=TEAL if ok else "#94a3b8", label=n, size=12, sw=2 if ok else 1.4)
f.box(30, 82, 100, 28, "A ∧ B → C", fill=SAND, stroke=AMBER, size=10.5, r=5, bold=True, color=NAVY)
f.arrow([(50, 64), (70, 82)], color=NAVY, sw=1.5); f.arrow([(110, 64), (90, 82)], color=NAVY, sw=1.5)
f.circle(80, 142, 15, fill=MINT, stroke=TEAL, label="C", size=12, sw=2); f.arrow([(80, 110), (80, 126)], color=NAVY, sw=1.5)
f.box(40, 168, 80, 26, "C → D", fill=SAND, stroke=AMBER, size=10.5, r=5, bold=True, color=NAVY); f.arrow([(80, 157), (80, 168)], color=NAVY, sw=1.5)
f.circle(80, 226, 15, fill=MINT, stroke=TEAL, label="D", size=12, sw=2); f.arrow([(80, 194), (80, 211)], color=NAVY, sw=1.5)
f.box(190, 82, 80, 28, "E → F", fill="#f1f5f9", stroke="#94a3b8", size=10.5, r=5, dash=True, color="#94a3b8")
f.circle(230, 142, 15, fill="#ffffff", stroke="#94a3b8", label="F", size=12, color="#94a3b8"); f.arrow([(230, 110), (230, 126)], color="#94a3b8", sw=1.2, dash=True)
f.text(210, 190, "E is unknown: never fires", size=9.5, color=SLATE, italic=True)
f.text(210, 230, "%d of 3 rules fired" % len(fwd), size=10.5, color=TEAL, bold=True)
f.text(430, 14, "backward chaining (goal-driven)", size=10.5, color=NAVY, bold=True)
steps = ["goal D: rule C → D, new subgoal C", "goal C: rule A ∧ B → C, subgoals A, B", "goal A: it is a fact: proved", "goal B: it is a fact: proved", "D is proved; rule E → F never looked at"]
for i, s in enumerate(steps):
    f.box(300, 30 + i * 44, 272, 36, "%d.  %s" % (i + 1, s), fill=MINT if i == 4 else BLUE, stroke=TEAL if i == 4 else NAVY, size=10, r=6, bold=i == 4, color=NAVY, anchor="start", sw=1.6)
    if i < 4: f.arrow([(436, 66 + i * 44), (436, 74 + i * 44)], color=NAVY, sw=1.4)
f.text(436, 252, "subgoal order: " + ", ".join(calls), size=10, color=RED, bold=True)
```

```svgfig label="3.8" caption="Why the connective must match the quantifier, tested on three small models. Each model has three individuals; Asha and Chandra are students and Dolma is a teacher. In model A both students passed, in model B one student failed, in model C no student passed. The correct translation of 'all students passed' is the universal quantifier with an implication, and it is true only in A. The wrong version with a conjunction says that everyone is a student who passed, and it is false even in A because Dolma is not a student. The correct translation of 'some student passed' uses the existential quantifier with a conjunction and is true in A and B. The wrong version with an implication is true in every model, even C where no student passed, because the teacher Dolma makes the implication true."
f = Fig(580, 296)
models = {"A": {"Asha": (True, True), "Chandra": (True, True), "Dolma": (False, False)}, "B": {"Asha": (True, True), "Chandra": (True, False), "Dolma": (False, False)}, "C": {"Asha": (True, False), "Chandra": (True, False), "Dolma": (False, False)}}
imp = lambda a, b: (not a) or b
sent = [("∀x (Student(x) → Passed(x))", "all students passed (correct)", lambda m: all(imp(s, p) for s, p in m.values()), True),
        ("∀x (Student(x) ∧ Passed(x))", "wrong: everyone is a passing student", lambda m: all(s and p for s, p in m.values()), False),
        ("∃x (Student(x) ∧ Passed(x))", "some student passed (correct)", lambda m: any(s and p for s, p in m.values()), True),
        ("∃x (Student(x) → Passed(x))", "wrong: true if anyone is not a student", lambda m: any(imp(s, p) for s, p in m.values()), False)]
val = [[fn(m) for m in models.values()] for _, _, fn, _ in sent]
assert val == [[True, False, False], [False, False, False], [True, True, False], [True, True, True]]
for k, (nm, m) in enumerate(models.items()):
    x = 8 + k * 192
    f.box(x, 8, 180, 76, "", fill=BLUE, stroke=NAVY, r=7, sw=1.4)
    f.text(x + 90, 22, "model " + nm, size=10.5, color=NAVY, bold=True)
    for i, (who, (s, p)) in enumerate(m.items()):
        f.text(x + 10, 40 + i * 16, "%s: %s%s" % (who, "student" if s else "teacher", (", passed" if p else ", failed") if s else ""), size=10, color=SLATE, anchor="start")
for k, nm in enumerate(models): f.text(424 + k * 52, 104, "model " + nm, size=10, color=NAVY, bold=True)
f.text(8, 104, "sentence", size=10, color=SLATE, bold=True, anchor="start")
for i, (s, meaning, _, good) in enumerate(sent):
    y = 112 + i * 40
    f.box(8, y, 564, 36, "", fill=MINT if good else "#fff1f2", stroke=TEAL if good else RED, r=5, sw=1.2)
    f.text(16, y + 11, s, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(16, y + 26, meaning, size=9.5, color=TEAL if good else RED, anchor="start", vmid=True)
    for k, v in enumerate(val[i]):
        f.box(402 + k * 52 , y + 6, 44, 24, "true" if v else "false", fill="#bbf7d0" if v else "#fecaca", stroke=TEAL if v else RED, r=4, size=10, bold=True, color=NAVY, sw=1.2)
f.text(290, 284, "English: 'all students passed' = A only;  'some student passed' = A and B", size=10, color=RED, bold=True)
```

```svgfig label="3.9" caption="Unification computed by a real algorithm with the occurs check. Capitalised names are constants, lower-case letters are variables and Mother(y) is a function term. Knows(John, x) unifies with Knows(John, Jane) by x = Jane. It unifies with Knows(y, Mother(y)) by y = John and then x = Mother(John), which is the most general unifier. P(A, B) and P(B, A) fail because the constants A and B differ. Knows(John, x) and Knows(x, Jane) fail because the same variable x would have to be both John and Jane, but after standardising apart (rename one x to x1) they unify with x1 = John and x = Jane. P(x) and P(f(x)) fail the occurs check because x would have to contain itself."
f = Fig(580, 262)
def isvar(t): return isinstance(t, str) and t[0].islower()
def walk(t, s):
    while isvar(t) and t in s: t = s[t]
    return t
def occurs(v, t, s):
    t = walk(t, s)
    if t == v: return True
    return isinstance(t, tuple) and any(occurs(v, a, s) for a in t[1:])
def unify(a, b, s):
    if s is None: return None
    a, b = walk(a, s), walk(b, s)
    if a == b: return s
    if isvar(a):
        return None if occurs(a, b, s) else {**s, a: b}
    if isvar(b):
        return None if occurs(b, a, s) else {**s, b: a}
    if isinstance(a, tuple) and isinstance(b, tuple) and a[0] == b[0] and len(a) == len(b):
        for x, y in zip(a[1:], b[1:]):
            s = unify(x, y, s)
        return s
    return None
def full(t, s):
    t = walk(t, s)
    return (t[0],) + tuple(full(x, s) for x in t[1:]) if isinstance(t, tuple) else t
def ts(t): return t if isinstance(t, str) else "%s(%s)" % (t[0], ", ".join(ts(x) for x in t[1:]))
def fmt(s, keys): return "{" + ", ".join("%s/%s" % (k, ts(full(k, s))) for k in keys) + "}"
cases = [(("Knows", "John", "x"), ("Knows", "John", "Jane"), ["x"]), (("Knows", "John", "x"), ("Knows", "y", ("Mother", "y")), ["y", "x"]), (("P", "A", "B"), ("P", "B", "A"), []), (("Knows", "John", "x"), ("Knows", "x", "Jane"), []), (("P", "x"), ("P", ("f", "x")), [])]
out = []
for a, b, keys in cases:
    s = unify(a, b, {}); out.append(None if s is None else fmt(s, keys))
assert out == ["{x/Jane}", "{y/John, x/Mother(John)}", None, None, None]
s2 = unify(("Knows", "John", "x"), ("Knows", "x1", "Jane"), {}); assert fmt(s2, ["x1", "x"]) == "{x1/John, x/Jane}"
why = ["", "", "constants A and B differ", "same x: John and Jane clash\nstandardise apart: " + fmt(s2, ["x1", "x"]), "occurs check: x inside f(x)"]
f.text(60, 14, "term 1", size=10, color=SLATE, bold=True); f.text(222, 14, "term 2", size=10, color=SLATE, bold=True); f.text(468, 14, "most general unifier", size=10, color=SLATE, bold=True)
for i, ((a, b, _), o) in enumerate(zip(cases, out)):
    y = 22 + i * 46
    ok = o is not None
    f.box(6, y, 568, 40, "", fill=MINT if ok else "#fff1f2", stroke=TEAL if ok else RED, r=6, sw=1.3)
    f.text(14, y + 20, ts(a), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(176, y + 20, ts(b), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(374, y + (20 if ok else (13 if "\n" in why[i] else 20)), o if ok else "fails: " + why[i].split("\n")[0], size=10, color=TEAL if ok else RED, bold=True, anchor="start", vmid=True)
    if "\n" in why[i]: f.text(374, y + 28, why[i].split("\n")[1], size=9.5, color=SLATE, anchor="start", vmid=True)
```

```svgfig label="3.10" caption="Bayes' rule on a medical test, computed for 10,000 people. The disease affects 1 percent (100 people), the test is positive for 95 percent of the sick and for 10 percent of the healthy. Top left: the red sliver is the 100 sick people. Bottom left: of the 1,085 people who test positive, 95 are sick (red) and 990 are healthy (amber), so P(disease | positive) = 95 / 1,085 = 8.76 percent: most positives are false alarms because healthy people are 99 times more numerous. Right: the same test applied where the disease is more common; the probability of disease given a positive result rises to 51.4 percent at 10 percent prevalence and 90.5 percent at 50 percent. A test result cannot be read without the base rate."
f = Fig(580, 246)
N = 10000; prev = 0.01; sens = 0.95; fpr = 0.10
sick = round(N * prev); healthy = N - sick
tp = round(sick * sens); fp = round(healthy * fpr)
post = tp / (tp + fp)
assert (sick, tp, fp, tp + fp) == (100, 95, 990, 1085) and round(post, 4) == 0.0876 and healthy // sick == 99
def pp(pr): return pr * sens / (pr * sens + (1 - pr) * fpr)
assert round(pp(0.10), 3) == 0.514 and round(pp(0.5), 3) == 0.905
f.text(150, 14, "10,000 people", size=10.5, color=NAVY, bold=True)
sc = 0.029
f.box(8, 22, sick * sc, 24, "", fill="#ef4444", stroke="#ef4444", r=0, sw=1)
f.box(8 + sick * sc, 22, healthy * sc, 24, "", fill=MINT, stroke=TEAL, r=0, sw=1)
f.text(8, 62, "100 sick (red sliver)", size=10, color=RED, bold=True, anchor="start")
f.text(292, 62, "9,900 healthy", size=10, color=TEAL, bold=True, anchor="end")
f.text(150, 92, "%s people test positive" % "{:,}".format(tp + fp), size=10.5, color=NAVY, bold=True)
s2 = 0.25
f.box(8, 100, tp * s2, 28, "", fill="#ef4444", stroke="#ef4444", r=0)
f.box(8 + tp * s2, 100, fp * s2, 28, "990 healthy: false alarms", fill=SAND, stroke=AMBER, r=0, size=10, bold=True, color=NAVY)
f.text(8, 146, "%d sick" % tp, size=10, color=RED, bold=True, anchor="start")
f.line(20, 130, 20, 138, color=RED, sw=1.4)
f.box(8, 160, 284, 36, "P(disease | positive) = %d / %s = %.2f%%" % (tp, "{:,}".format(tp + fp), post * 100), fill="#fee2e2", stroke=RED, size=11, r=6, bold=True, color=NAVY, sw=1.8)
f.text(150, 216, "healthy people outnumber sick people %d to 1" % (healthy // sick), size=10, color=SLATE, bold=True)
f.text(150, 234, "sensitivity 95%, false-positive rate 10%", size=10, color=SLATE)
ax = Axes(f, 350, 30, 210, 150, (0, 0.5), (0, 1))
ax.grid(0.1, 0.25, xfmt=lambda v: "%d%%" % round(v * 100), yfmt=lambda v: "%d%%" % round(v * 100))
ax.curve(pp, color=NAVY, sw=2.4)
for pr, col in [(0.01, RED), (0.10, AMBER), (0.50, TEAL)]:
    f.circle(ax.X(pr), ax.Y(pp(pr)), 4.5, fill=col, stroke="#ffffff", sw=1.2)
f.text(ax.X(0.01) + 8, ax.Y(pp(0.01)) - 6, "1%: 8.8%", size=10, color=RED, bold=True, anchor="start")
f.text(ax.X(0.10) + 8, ax.Y(pp(0.10)) + 14, "10%: 51.4%", size=10, color=AMBER, bold=True, anchor="start")
f.text(ax.X(0.5) - 8, ax.Y(pp(0.5)) - 10, "50%: 90.5%", size=10, color=TEAL, bold=True, anchor="end")
f.text(455, 14, "P(disease | positive) by prevalence", size=10.5, color=NAVY, bold=True)
f.text(455, 204, "prevalence in the tested group", size=10, color=SLATE)
```

```svgfig label="3.11" caption="The burglar-alarm Bayesian network with every number computed by enumeration. Burglary (prior 0.001) and Earthquake (prior 0.002) can trigger the Alarm, with the conditional probability table shown; John and Mary call with the probabilities under their nodes. The full joint over five Boolean variables needs 2^5 - 1 = 31 numbers, but the network needs only 1 + 1 + 4 + 2 + 2 = 10. One joint entry, the probability that John and Mary call, the alarm sounds and there is neither a burglary nor an earthquake, is 0.90 x 0.70 x 0.001 x 0.999 x 0.998 = 0.000628. Summing the joint over the hidden variables gives P(b, j, m) = 0.000592 and P(j, m) = 0.002084, so P(burglary | John and Mary call) = 0.2842: a burglary is still less likely than not because it is so rare and false alarms are common."
f = Fig(580, 290)
it = __import__("itertools")
pB, pE = 0.001, 0.002
pA = {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}
pJ = {1: 0.90, 0: 0.05}; pM = {1: 0.70, 0: 0.01}
def joint(b, e, a, j, m):
    p = (pB if b else 1 - pB) * (pE if e else 1 - pE)
    p *= pA[(b, e)] if a else 1 - pA[(b, e)]
    p *= pJ[a] if j else 1 - pJ[a]
    p *= pM[a] if m else 1 - pM[a]
    return p
one = joint(0, 0, 1, 1, 1)
pbjm = sum(joint(1, e, a, 1, 1) for e in (0, 1) for a in (0, 1))
pjm = sum(joint(b, e, a, 1, 1) for b in (0, 1) for e in (0, 1) for a in (0, 1))
post = pbjm / pjm
assert round(one, 6) == 0.000628 and round(pbjm, 6) == 0.000592 and round(pjm, 6) == 0.002084 and round(post, 4) == 0.2842
assert abs(sum(joint(*v) for v in it.product((0, 1), repeat=5)) - 1) < 1e-12 and 2 ** 5 - 1 == 31 and 1 + 1 + 4 + 2 + 2 == 10
for (x, y, n) in [(60, 56, "B"), (230, 56, "E"), (145, 130, "A"), (60, 210, "J"), (230, 210, "M")]:
    f.circle(x, y, 22, fill=SAND if n in "BE" else (BLUE if n == "A" else MINT), stroke=AMBER if n in "BE" else (NAVY if n == "A" else TEAL), label=n, size=14, sw=2)
for a, b in [((60, 78), (132, 112)), ((230, 78), (160, 112)), ((145, 152), (68, 192)), ((145, 152), (222, 192))]:
    f.arrow([a, b], color=NAVY, sw=1.8)
f.text(60, 18, "Burglary: P(β) = 0.001", size=9.5, color=SLATE, bold=True)
f.text(235, 18, "Earthquake: P(e) = 0.002", size=9.5, color=SLATE, bold=True)
f.box(196, 96, 134, 70, "P(a | B, E)\nB, E: 0.95\nB, ¬E: 0.94\n¬B, E: 0.29\n¬B, ¬E: 0.001", fill="#ffffff", stroke="#94a3b8", size=9.5, r=5, color=NAVY, sw=1)
f.text(8, 246, "P(j | a) = 0.90, P(j | ¬a) = 0.05", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(8, 262, "John calls", size=9.5, color=SLATE, anchor="start")
f.text(170, 246, "P(m | a) = 0.70, P(m | ¬a) = 0.01", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(170, 262, "Mary calls", size=9.5, color=SLATE, anchor="start")
items = [("one joint entry P(j, m, a, ¬b, ¬e)\n= %.6f" % one, BLUE, NAVY), ("P(b, j, m) = %.6f" % pbjm, BLUE, NAVY), ("P(j, m) = %.6f" % pjm, BLUE, NAVY), ("P(burglary | j, m)\n= %.4f" % post, "#fee2e2", RED), ("numbers needed:\n10 (network) vs 31 (full joint)", MINT, TEAL)]
for i, (t, fl, st) in enumerate(items):
    f.box(346, 10 + i * 56, 226, 48, t, fill=fl, stroke=st, size=10.5, r=7, bold=True, color=NAVY, sw=1.8)
```

```svgfig label="3.12" caption="Choosing under uncertainty by expected utility, computed. The chance of rain is 0.3; an umbrella is worth 70 if it rains and 80 if it does not, and no umbrella is worth 0 if it rains and 100 if it does not. The expected utilities are 0.3 x 70 + 0.7 x 80 = 77 for the umbrella and 0.7 x 100 = 70 for no umbrella, so a rational agent takes the umbrella. Right: both expected utilities as the chance of rain p varies, with EU(umbrella) = 80 - 10p and EU(no umbrella) = 100 - 100p; the lines cross at p = 2/9 = 0.2222, so the umbrella is the better choice whenever rain is more than 22 percent likely. The decision depends on the probability, not only on the utilities."
f = Fig(580, 230)
p = 0.3
U = {"umbrella": (70, 80), "no umbrella": (0, 100)}
eu = {k: p * a + (1 - p) * b for k, (a, b) in U.items()}
assert round(eu["umbrella"], 6) == 77 and round(eu["no umbrella"], 6) == 70 and abs(20 / 90 - 2 / 9) < 1e-12
cross = 20 / 90
f.text(150, 14, "utilities and expected utility (p = 0.3)", size=10.5, color=NAVY, bold=True)
f.text(130, 36, "rain 0.3", size=10, color=NAVY, bold=True); f.text(200, 36, "dry 0.7", size=10, color=NAVY, bold=True); f.text(268, 36, "EU", size=10, color=RED, bold=True)
for i, (k, (a, b)) in enumerate(U.items()):
    y = 44 + i * 36
    best = eu[k] == max(eu.values())
    f.box(6, y, 296, 30, "", fill=MINT if best else SAND, stroke=TEAL if best else AMBER, r=6, sw=1.5)
    f.text(14, y + 15, k, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(130, y + 15, str(a), size=11, color=SLATE, bold=True, vmid=True); f.text(200, y + 15, str(b), size=11, color=SLATE, bold=True, vmid=True)
    f.text(268, y + 15, "%g" % round(eu[k], 6), size=12, color=RED, bold=True, vmid=True)
f.box(6, 124, 296, 36, "take the umbrella: EU 77 > 70", fill="#bbf7d0", stroke=TEAL, size=11.5, r=6, bold=True, color=NAVY, sw=1.8)
f.text(150, 188, "crossover at p = 2/9 = %.4f" % cross, size=10.5, color=AMBER, bold=True)
f.text(150, 208, "umbrella is better when rain chance > 22.2%", size=10, color=SLATE)
ax = Axes(f, 350, 26, 210, 150, (0, 1), (0, 100))
ax.grid(0.25, 25, xfmt=lambda v: "%g" % v)
ax.curve(lambda x: 80 - 10 * x, color=TEAL, sw=2.4)
ax.curve(lambda x: 100 - 100 * x, color=AMBER, sw=2.4)
f.circle(ax.X(cross), ax.Y(80 - 10 * cross), 5, fill=RED, stroke="#ffffff", sw=1.3)
f.text(ax.X(0.62), ax.Y(80 - 10 * 0.62) - 8, "umbrella", size=10, color=TEAL, bold=True, anchor="start")
f.text(ax.X(0.52), ax.Y(100 - 100 * 0.52) - 8, "no umbrella", size=10, color=AMBER, bold=True, anchor="start")
f.text(ax.X(cross) + 8, ax.Y(80 - 10 * cross) - 10, "p = 0.222", size=10, color=RED, bold=True, anchor="start")
f.text(455, 14, "expected utility vs chance of rain p", size=10.5, color=NAVY, bold=True)
f.text(455, 212, "p = probability of rain", size=10, color=SLATE)
```

### 3.6.1 Eight uses of knowledge and reasoning in Nepal

1. **Farm advice by rules.** A crop-advice service can store the knowledge of agriculture officers as IF-THEN rules, such as IF the leaves have yellow stripes AND the weather is cool and wet THEN suspect rust disease. A farmer answers a few questions by phone or app and the inference engine fires the matching rules, as in Fig. 3.1. The rules are easy for an expert to read and correct, which is why this style is used when the advice must be explained.
2. **Medical decision support.** District hospitals and health posts use rapid tests for infections. As Fig. 3.10 shows, a positive result means different things in a village with many cases and in a town with few, so a good support tool combines the test with the local base rate using Bayes' rule. The tool suggests a confirmation test and leaves the decision to the health worker.
3. **Eligibility and rule checkers.** Scholarship, tax and licence rules are written as conditions on age, income and documents. A program that holds them as rules can say yes or no and also explain which rule decided, which matters for fairness. This is forward chaining over a small fact base, and it avoids the errors of a clerk who forgets one clause.
4. **Spam and fraud filters.** Banks and wallets such as eSewa, Khalti and Fonepay, and mail providers, estimate the probability that a message or payment is bad from signs such as the sender, amount and time. Each sign changes the belief by Bayes' rule, and naive Bayes (Unit 4) multiplies the evidence. The filter must keep false alarms low, because most payments are honest (the base-rate lesson of Fig. 3.10).
5. **Knowledge graphs and search.** Facts such as Kathmandu is-a city, capital-of Nepal, part-of Bagmati Province are stored as a graph, a modern semantic network. A search engine uses the graph to answer a question directly and to find related pages, and inheritance lets it infer that a museum in Kathmandu is in Nepal. Wikipedia and Wikidata hold such facts for Nepali places and people.
6. **Chatbots with frames.** A bank or telecom chatbot fills the slots of a frame, for example transfer: account, amount, receiver. It asks for each empty slot, uses defaults where it can and calls a procedure when the frame is full, as in Fig. 3.3. This keeps a conversation on track far better than free-form guessing.
7. **Flood and earthquake warning.** Rainfall, river level, soil wetness and earlier floods are uncertain signs of a coming flood. A Bayesian network, like the alarm network of Fig. 3.11, combines them into one probability, and an agency such as the Department of Hydrology and Meteorology can decide when to warn villages along a river. The same method updates the chance of aftershocks.
8. **Decisions about risk.** A bank decides on a loan, an insurer on a premium and a farmer on which crop to plant by comparing expected utility, as in Fig. 3.12. The best choice changes when the probability changes, so the numbers must be kept up to date. Such a model is a decision aid; it does not replace judgement about people.

## Formula and fact sheet

- P → Q ≡ ¬P ∨ Q ≡ ¬Q → ¬P. De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q. n symbols give 2ⁿ models.
- Modus Ponens: α → β, α ⊢ β. Resolution: (α ∨ β), (¬β ∨ γ) ⊢ (α ∨ γ). Refutation: add ¬goal and derive the empty clause.
- FOL: ∀ goes with →, ∃ goes with ∧. ¬∀x P ≡ ∃x ¬P. Unify with the most general substitution.
- Forward chaining is data-driven; backward chaining is goal-driven (Prolog).
- Bayes: P(α | β) = P(β | α) P(α) / P(β). Network joint = Π P(xᵢ | parents).
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

## Model answers for Unit 3

**Q1. Explain the main techniques of knowledge representation. What makes a good representation scheme? (10 marks)**

**Introduction.** Knowledge is information organised so that a program can use it for decisions. A knowledge representation scheme is a language for writing that knowledge down together with procedures that derive new knowledge from it. The kinds to be represented include declarative facts, procedural know-how, heuristic rules of thumb and structural relations between concepts.

**Main techniques.**

1. **Rule-based (production) systems** store knowledge as IF-THEN rules in a rule base, with the known facts in a working memory. An inference engine matches rules to facts, chooses one by conflict resolution and fires it (Fig. 3.1). Rules are modular and easy to read, which is why expert systems use them, but matching is slow in very large rule bases.
2. **Semantic networks** are graphs in which nodes are concepts and labelled arcs such as is-a and has-part are relations. They support inheritance: Tweety is-a canary, canary is-a bird, so Tweety has the wings and the default flight of a bird (Fig. 3.2). Their weakness is that arcs have no standard meaning and negation and quantifiers are awkward.
3. **Frames** group the slots of an object, each with a value, a default, a range or an attached procedure, in a class hierarchy (Fig. 3.3). Sub-frames override defaults, and an if-needed procedure computes a slot when it is asked for. Frames are the ancestor of classes in object-oriented programming.
4. **Logic** gives a formal language with exact meaning and sound inference. Propositional logic handles true and false statements, and first-order logic adds objects, predicates and quantifiers.

| Technique | Strength | Weakness |
|---|---|---|
| Rules | modular, explainable | slow for huge rule sets |
| Semantic nets | visual, inheritance | no precise semantics |
| Frames | defaults, procedures | rigid structure |
| Logic | precise, sound inference | hard to state uncertain knowledge |

**Properties of a good scheme.** It needs representational adequacy (it can express all the needed knowledge), inferential adequacy (it can derive new knowledge), inferential efficiency (inference is fast) and acquisitional efficiency (knowledge is easy to add).

**Conclusion.** No single scheme is best; practical systems combine rules, hierarchies and logic, and add probability when knowledge is uncertain.

**Q2. Explain propositional logic: syntax, semantics, equivalences and entailment, with an example. (10 marks)**

**Introduction.** Propositional logic is the simplest logic. A proposition is a statement that is either true or false, and sentences are built from propositional symbols with five connectives. It is the base on which first-order logic and resolution are built.

**Syntax.** Atomic sentences are symbols such as P, Q and Rain. Complex sentences use ¬ (not), ∧ (and), ∨ (or), → (implies) and ↔ (if and only if), with brackets.

**Semantics.** A model assigns true or false to every symbol, and the value of a sentence in that model follows the truth tables (Fig. 3.4). The implication P → Q is false only when P is true and Q is false, and it is equivalent to ¬P ∨ Q. A sentence is valid if it is true in every model, satisfiable if it is true in at least one and unsatisfiable if it is true in none.

**Equivalences.** Machine checking over every model confirms that P → Q ≡ ¬P ∨ Q, that P → Q ≡ ¬Q → ¬P (contrapositive), and the two De Morgan laws ¬(P ∧ Q) ≡ ¬P ∨ ¬Q and ¬(P ∨ Q) ≡ ¬P ∧ ¬Q. The converse Q → P is not equivalent to P → Q.

**Entailment.** A knowledge base KB entails a sentence α, written KB ⊨ α, if α is true in every model in which KB is true. For n symbols there are 2ⁿ models, which is 8 for three symbols but more than a billion for thirty.

**Example (Fig. 3.5).** Let KB = {P → Q, Q → R, P} and the query R. Among the 8 models only the one with P, Q and R all true makes the whole KB true, and R is true in it, so KB ⊨ R. For KB = {P → Q, Q} the models P false, Q true and P true, Q true both satisfy it, so P is not entailed: this is the fallacy of affirming the consequent.

**Inference rules.** Modus ponens infers β from α → β and α; modus tollens infers ¬α from α → β and ¬β; hypothetical syllogism chains α → β and β → γ; and-elimination infers α from α ∧ β. They are sound: they derive only entailed sentences.

**Conclusion.** Propositional logic is exact and decidable, but truth tables grow exponentially, so resolution and chaining are used for large knowledge bases.

**Q3. Explain resolution in propositional logic. Convert sentences to CNF and prove R from P → Q, Q → R and P. (10 marks)**

**Introduction.** Resolution is a single inference rule that is sound and refutation-complete: if a set of clauses is unsatisfiable, resolution will derive the empty clause. It works on clauses, which are disjunctions of literals, and it proves a query by contradiction.

**The rule.** From (α ∨ β) and (¬β ∨ γ) infer (α ∨ γ). Two clauses that contain complementary literals are resolved by cancelling the pair and joining what remains. Resolving P with ¬P gives the empty clause, a contradiction.

**Conversion to conjunctive normal form (CNF).**
1. Eliminate ↔ and → : replace α → β by ¬α ∨ β.
2. Move ¬ inward with De Morgan's laws.
3. Remove double negations.
4. Distribute ∨ over ∧ so that the result is a conjunction of clauses.

**Refutation procedure.** To prove KB ⊨ α, add ¬α to the clauses of KB, resolve pairs of clauses and add the resolvents, and stop when the empty clause appears. If it appears, KB together with ¬α is unsatisfiable, so KB entails α.

**Worked proof (Fig. 3.6).** The clauses are (1) ¬P ∨ Q, (2) ¬Q ∨ R, (3) P, and the negated query (4) ¬R.

| Step | Resolve | Result |
|---|---|---|
| 5 | (3) P with (1) ¬P ∨ Q | Q |
| 6 | (5) Q with (2) ¬Q ∨ R | R |
| 7 | (6) R with (4) ¬R | empty clause |

The empty clause is a contradiction, so R follows from the knowledge base. A program that resolves every pair until nothing new appears also reaches the empty clause, but it derives many useless clauses on the way.

**Why it works.** Suppose the knowledge base is true and the query R is false. Then clauses (1) to (4) would all be true in one model, but resolution is sound, so every clause it derives is true in that model, and the empty clause is never true. Because the empty clause is derived, no such model exists: whenever the knowledge base is true, R must be true. This is proof by contradiction, and it is why resolution needs only one rule instead of the many inference rules of natural deduction. In practice programs add control strategies, such as always resolving with the shortest clause, to avoid deriving clauses that cannot help.

**Conclusion.** Resolution reduces reasoning to one mechanical rule on clauses, and Horn clauses allow a faster special case, chaining.

**Q4. Explain first-order logic: syntax, quantifiers, English translation, unification and resolution. (10 marks)**

**Introduction.** Propositional logic cannot say that all men are mortal without listing every man. First-order logic (FOL) adds objects, predicates and functions, and the quantifiers ∀ (for all) and ∃ (there exists), so one sentence can speak about many objects.

**Syntax.** The elements are constants (Socrates), variables (x, y), predicates (Man(x), Loves(x, y)), functions (Mother(x)), the five connectives and the two quantifiers.

**Translation rules.** The natural connective with ∀ is → and with ∃ is ∧ (Fig. 3.8). "All students passed" is ∀x (Student(x) → Passed(x)); writing ∧ would say that everyone is a student who passed, which is false whenever there is a teacher. "Some student passed" is ∃x (Student(x) ∧ Passed(x)); writing → would be true whenever anything is not a student, even if no student passed. Also ¬∀x P(x) ≡ ∃x ¬P(x).

**Unification.** To resolve in FOL we need a substitution that makes two literals identical. Knows(John, x) and Knows(y, Mother(y)) unify with {y/John, x/Mother(John)}, the most general unifier (Fig. 3.9). P(A, B) and P(B, A) fail because the constants differ, and a variable cannot be bound to a term that contains itself (occurs check).

**Resolution in FOL.** Convert to CNF, standardise the variables apart, replace each ∃ by a Skolem constant or function, drop the ∀, add the negated goal, and resolve literals that unify until the empty clause appears.

**Example.** Premises: ¬Man(x) ∨ Mortal(x) and Man(Socrates); negated goal ¬Mortal(Socrates). Resolving the first and the goal with {x/Socrates} gives ¬Man(Socrates), and resolving that with Man(Socrates) gives the empty clause, so Mortal(Socrates) is proved.

**Comparison.**

| | Propositional logic | First-order logic |
|---|---|---|
| Objects | none, only true or false symbols | constants, variables, functions |
| Relations | no | predicates such as Man(x) |
| General statements | must list every case | ∀ and ∃ in one sentence |
| Inference | truth tables, resolution | unification with resolution |

The price of this power is that FOL entailment is only semi-decidable: a proof is found if the sentence is entailed, but the search may never finish if it is not.

**Conclusion.** FOL is far more expressive than propositional logic, and unification with resolution lets a program prove theorems; Prolog applies the idea to Horn clauses.

**Q5. What is a Bayesian network? Explain with the burglar-alarm example. (10 marks)**

**Introduction.** Real knowledge is uncertain. A Bayesian network is a directed acyclic graph in which each node is a random variable and each node has a conditional probability table (CPT) given its parents. It represents the full joint distribution compactly: P(x₁, …, xₙ) = Π P(xᵢ | parents(xᵢ)).

**The example (Fig. 3.11).** Burglary B (prior 0.001) and Earthquake E (prior 0.002) can set off the Alarm A; John (J) and Mary (M) may call when they hear it. The CPT of A is P(a | b, e) = 0.95, P(a | b, ¬e) = 0.94, P(a | ¬b, e) = 0.29 and P(a | ¬b, ¬e) = 0.001; John calls with probability 0.90 if the alarm sounds and 0.05 if not, and Mary with 0.70 and 0.01.

**Compact representation.** The full joint over five Boolean variables needs 2⁵ − 1 = 31 numbers, but the network needs 1 + 1 + 4 + 2 + 2 = 10. The saving grows quickly with more variables if each node has few parents.

**Computing a joint entry.** P(j, m, a, ¬b, ¬e) = P(j | a) P(m | a) P(a | ¬b, ¬e) P(¬b) P(¬e) = 0.90 × 0.70 × 0.001 × 0.999 × 0.998 = 0.000628.

**Inference by enumeration.** To find P(B | j, m) sum the joint over the hidden variables E and A: P(b, j, m) = 0.000592 and P(j, m) = 0.002084, so P(B | j, m) = 0.000592 / 0.002084 = 0.2842. Even when both neighbours call, the chance of a burglary is only 28 percent, because burglaries are rare and false alarms from earthquakes or mistaken neighbours are common.

**Reading the network.** The arrows show the causes: the alarm depends on burglary and earthquake only, and John and Mary depend on the alarm only, so given the alarm they are independent of the burglary itself. This is the independence assumption that makes the small tables enough. The result also shows explaining away: if the neighbours call and we then learn that an earthquake happened, the probability of a burglary falls, because the earthquake already explains the alarm.

| Method | Idea |
|---|---|
| Enumeration | sum the joint over hidden variables |
| Variable elimination | reuse partial sums |
| Sampling (MCMC) | approximate by random samples |

**Conclusion.** Bayesian networks factor a large joint distribution into small tables and answer queries by exact or approximate inference.

**Q6. Distinguish forward chaining from backward chaining with an example. (5 marks)**

Both methods use Horn clauses, rules with one conclusion and several premises. **Forward chaining** is data-driven: it starts from the known facts, fires every rule whose premises are all known, adds the conclusion to the facts and repeats until the query is derived or nothing new appears. It suits monitoring systems and cases where many conclusions are wanted. **Backward chaining** is goal-driven: it starts from the query, finds a rule that concludes it and tries to prove the premises as subgoals. It suits answering one question and is how Prolog works.

**Example (Fig. 3.7).** Rules: A ∧ B → C, C → D, E → F. Facts: A and B. Forward chaining fires A ∧ B → C, then C → D, and derives C and D; E → F never fires because E is unknown, so F is not derived. Backward chaining for D uses the rule C → D and asks for C; the rule A ∧ B → C asks for A and B, which are facts, so D is proved after looking at only two rules and without touching the E rule.

| | Forward | Backward |
|---|---|---|
| Starts from | facts | the query |
| Direction | data-driven | goal-driven |
| May waste work on | irrelevant facts | repeated subgoals |

**Q7. Explain Bayes' rule with the example of a medical test. (5 marks)**

Bayes' rule updates a belief from evidence: P(α | β) = P(β | α) P(α) / P(β), where P(α) is the prior probability and P(β) comes from the total probability P(β) = Σ P(β | αᵢ) P(αᵢ).

**Example (Fig. 3.10).** A disease affects 1 percent of a population. The test is positive for 95 percent of the sick (sensitivity) and for 10 percent of the healthy (false-positive rate). In 10,000 people, 100 are sick and 95 of them test positive; 9,900 are healthy and 990 of them test positive. The probability of a positive result is P(positive) = 0.01 × 0.95 + 0.99 × 0.10 = 0.1085, which is 1,085 people in 10,000. By Bayes' rule P(disease | positive) = 0.01 × 0.95 / 0.1085 = 0.0876.

So a positive result means only an 8.8 percent chance of disease, although the test looks accurate. The reason is the base rate: healthy people outnumber the sick 99 to 1, so false alarms outnumber true positives. If the same test were used where 10 percent are sick, the probability would rise to 51.4 percent. A test result must always be read together with how common the disease is.

**Q8. Compare semantic networks with frames. (5 marks)**

A **semantic network** is a graph in which nodes are concepts or objects and labelled arcs are relations such as is-a, instance-of and has-part. Knowledge is found by following arcs, and inheritance passes properties down the is-a links: Tweety is-a canary and canary is-a bird, so Tweety inherits has = wings (Fig. 3.2). An exception is handled by putting the value lower in the hierarchy: the nearest value wins, so Penguin overrides the can-fly = yes of Bird with can-fly = no.

A **frame** collects all the knowledge about one concept in named slots. A slot can hold a value, a default, a range or an attached procedure: an if-needed procedure computes the value when it is asked for, an if-added procedure runs when a value is stored, and a demon reacts to a change. Frames are arranged in a class hierarchy, and an instance frame inherits the slots of its class (Fig. 3.3), such as the credits that are computed for a student.

| | Semantic network | Frame |
|---|---|---|
| Unit of knowledge | node and arcs | slots in one structure |
| Procedures | no | yes (if-needed, demons) |
| Defaults | by position in the graph | explicit default facet |
| Descendant | knowledge graphs | object-oriented classes |

Both support inheritance and defaults, but frames add structure and procedures.

**Q9. What is unification? Unify Knows(John, x) with Knows(y, Mother(y)). (5 marks)**

Unification finds a substitution of terms for variables that makes two logical expressions identical. It is the step that lets resolution and Prolog match a general rule with a specific fact. The substitution θ is the **most general unifier** (MGU) if every other unifier is a special case of it, so it commits to as little as possible.

**Algorithm.** Compare the two expressions argument by argument. If they are equal, nothing is needed. If one is a variable, bind it to the other term, provided the variable does not occur inside that term (occurs check). If both are compound terms, the function symbols and the number of arguments must match, and the arguments are unified in turn with the bindings so far. Otherwise unification fails.

**Worked example (Fig. 3.9).** In Knows(John, x) and Knows(y, Mother(y)) the first arguments John and y give y = John. The second arguments x and Mother(y) give x = Mother(y), which becomes x = Mother(John) after applying y = John. The MGU is {y/John, x/Mother(John)}.

**Failures.** P(A, B) and P(B, A) fail because the constants A and B differ. Knows(John, x) and Knows(x, Jane) fail because x cannot be both John and Jane; after standardising apart (renaming one x to x₁) they unify with {x₁/John, x/Jane}. P(x) and P(f(x)) fail the occurs check.

**Q10. What is expected utility? How does a rational agent choose under uncertainty? (5 marks)**

A **utility function** gives each outcome a number that says how desirable it is, and the **expected utility** of an action is the sum over its possible outcomes of the probability of the outcome times its utility: EU(a) = Σ P(outcome | a) U(outcome). A rational agent chooses the action with the highest expected utility. This combines probability theory, which says what is likely, with utility theory, which says what is wanted.

**Example (Fig. 3.12).** The chance of rain is 0.3. An umbrella gives utility 70 if it rains and 80 if it does not; no umbrella gives 0 if it rains and 100 if it does not. Then EU(umbrella) = 0.3 × 70 + 0.7 × 80 = 77 and EU(no umbrella) = 0.7 × 100 = 70, so the agent takes the umbrella.

**Sensitivity.** With rain probability p, EU(umbrella) = 80 − 10p and EU(no umbrella) = 100 − 100p. The two are equal at p = 2/9 = 0.2222, so the umbrella is better whenever rain is more than 22 percent likely. The decision therefore depends on the probability as well as on the utilities, which is why a loan decision or a flood warning must be re-evaluated when the probabilities change.
