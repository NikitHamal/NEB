---
file: NEBians-IOE-Past-Paper-Theory-of-Computation-ENCT203-2081-Chaitra.pdf
subject: Theory of Computation
level: BE · Year II / Part I
code: ENCT203
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) State Diagonalization principle. Using the principle of mathematical induction show that $1^3+2^3+3^3+\cdots+n^3=\left[\dfrac{n(n+1)}{2}\right]^2$. [[1+3]]

(b) Using rules of inference, show that the premises "If you send me an e-mail message, then I will finish writing the program," "If you do not send me an e-mail message, then I will go to sleep early," and "If I go to sleep early, then I will wake up feeling refreshed" lead to the conclusion "If I do not finish writing the program, then I will wake up feeling refreshed." [[3]]

(c) What are power of an alphabet and positive closure of an alphabet? [[2]]

@q 2
(a) Explain the processing of a string by finite automata along with its block diagram. Construct DFA that accepts all the string that doesn't contain two consecutive b over $\Sigma(a, b)$ and process the string $w$ = baaaababb. [[2+3]]

(b) Write down the procedure to check the equivalence of two automata. Convert the given NFA into equivalent DFA. [[1+4]]

```figure caption="Question 2(b): the given NFA: A (start) loops on 0 and goes to B on 1; B loops on 0, 1 and goes to C on 0; C (accepting) loops on 0, 1 and goes back to B on 1."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
fig = T.graph({"A": (0, 0, "s"), "B": (3.4, 0, ""), "C": (6.8, 0, "f")},
              [("A", "B", "1", 0), ("B", "C", "0", 0.0), ("C", "B", "1", 0.55)],
              loops=[("A", "0", "up"), ("B", "0, 1", "up"), ("C", "0, 1", "up")])
```

(c) Explain the decision properties of regular languages. [[3]]

@q 3
(a) Construct CFG for the language $L: a^nb^mc^md^n$. Test your grammar to generate $w$ = aabbbcccdd and draw parse tree for the same. [[4]]

(b) Convert the following CFG, into CNF: $G = (V, \Sigma, R, S)$ where $V = \{S, A, B\}$, $\Sigma = \{a, b\}$, $R = \{S\to A,\ S\to B,\ A\to aBa,\ A\to\varepsilon,\ B\to bAb,\ B\to\varepsilon\}$ and $S$ is starting symbol. [[5]]

(c) State pumping lemma for context free language and show that $L=\{ww \mid w=\{0,1\}^*\}$ is not CFL. [[4]]

@q 4
(a) Design a TM that recognize the $L=\{a^ncb^n\}$. Also show how the string $w$ = aaaacbbbb is accepted by your Turing machine. [[6]]

(b) Design a Turing machine that can compute a function $f(x)=2x$ [[4]]

(c) Explain the properties of recursive language. [[4]]

@q 5
(a) How encoding is done in Turing Machine? Explain. [[3]]

(b) Explain NP-Complete problems. [[2]]

@q 6
(a) How lexical analyzer and DFA related with each other? Explain with an appropriate example. [[3]]

(b) Construct the parse tree for the following. $r = a + b * c / (d * e)$ [[3]]
<!-- SOLUTIONS -->

@s 1
**(a) Diagonalization principle.** Let $R$ be a binary relation on a set $A$ and for each $a\in A$ let $R_a=\{b : (a,b)\in R\}$ (row $a$ of the table of $R$). Define the *diagonal set* $D=\{a\in A : (a,a)\notin R\}$ (the elements that are not in their own row). Then $D$ is different from every row $R_a$, because $a\in D\iff a\notin R_a$. Consequence: the power set of $\mathbb N$ is uncountable, and the language $\{\langle M\rangle : M\text{ does not accept }\langle M\rangle\}$ is not recursively enumerable.

**Induction.** Let $P(n)$: $1^3+2^3+\cdots+n^3=\left[\dfrac{n(n+1)}2\right]^2$.

*Basis* $n=1$: LHS $=1$, RHS $=\left[\dfrac{1\cdot2}{2}\right]^2=1$. True.

*Step.* Assume $P(k)$: $\sum_{i=1}^{k}i^3=\dfrac{k^2(k+1)^2}{4}$. Add $(k+1)^3$:

$$\begin{aligned}
\sum_{i=1}^{k+1}i^3 &= \frac{k^2(k+1)^2}{4}+(k+1)^3\\
&= \frac{(k+1)^2\left[k^2+4(k+1)\right]}{4}\\
&= \frac{(k+1)^2(k+2)^2}{4}=\left[\frac{(k+1)(k+2)}{2}\right]^2 .
\end{aligned}$$

This is $P(k+1)$. By the principle of mathematical induction $P(n)$ holds for all $n\ge1$. $\blacksquare$ (Check: $n=4$: $1+8+27+64=100=\left[\tfrac{4\cdot5}{2}\right]^2$.)

**(b) Rules of inference.** Let $p$: you send me an e-mail, $q$: I finish writing the program, $r$: I go to sleep early, $s$: I wake up feeling refreshed.

Premises: (1) $p\to q$, (2) $\lnot p\to r$, (3) $r\to s$. Conclusion: $\lnot q\to s$.

| Step | Statement | Reason |
|---|---|---|
| 1 | $p\to q$ | premise 1 |
| 2 | $\lnot q\to\lnot p$ | contrapositive of step 1 |
| 3 | $\lnot p\to r$ | premise 2 |
| 4 | $\lnot q\to r$ | hypothetical syllogism (2, 3) |
| 5 | $r\to s$ | premise 3 |
| 6 | $\lnot q\to s$ | hypothetical syllogism (4, 5) |

Step 6 is the required conclusion: **if I do not finish writing the program, then I will wake up feeling refreshed.** $\blacksquare$

**(c) Power of an alphabet.** For an alphabet $\Sigma$ and $k\ge0$, $\Sigma^k$ is the set of all strings of length exactly $k$ over $\Sigma$; $\Sigma^0=\{\varepsilon\}$. For $\Sigma=\{0,1\}$: $\Sigma^1=\{0,1\}$, $\Sigma^2=\{00,01,10,11\}$, and $|\Sigma^k|=|\Sigma|^k$.

**Closures.** The Kleene closure $\Sigma^*=\Sigma^0\cup\Sigma^1\cup\Sigma^2\cup\cdots$ (all strings, including $\varepsilon$). The **positive closure** is

$$\Sigma^+=\Sigma^1\cup\Sigma^2\cup\Sigma^3\cup\cdots=\Sigma^*-\{\varepsilon\},$$

the set of all *non-empty* strings over $\Sigma$. For $\Sigma=\{a,b\}$: $\Sigma^+=\{a,b,aa,ab,ba,bb,aaa,\dots\}$. Also $\Sigma^*=\Sigma^+\cup\{\varepsilon\}$.

@s 2
**(a) Processing a string by a finite automaton.** A finite automaton has three parts: a read-only **input tape** divided into cells that hold the symbols of $w$, a **read head** that moves only to the right (one cell per move), and a **finite control** that stores the current state and the transition function $\delta$. The machine starts in the start state $q_0$ with the head on the first symbol. At every step it reads the symbol $a$ under the head, moves to the state $\delta(q,a)$ and advances the head. When the whole string has been read, $w$ is accepted if the machine is in an accepting state and rejected otherwise.

```figure caption="Block diagram of a finite automaton processing the string baaaababb (head on the first cell)."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(5.6, 2.5)); ax.axis("off"); ax.set_xlim(-0.5, 10.5); ax.set_ylim(-2.4, 3.2)
w = "baaaababb"
for i, ch in enumerate(w):
    ax.add_patch(mp.Rectangle((0.5 + i, 2.0), 1, 0.9, fc="white", ec=INK, lw=1.1)); ax.text(1.0 + i, 2.45, ch, ha="center", va="center", fontsize=9)
ax.text(-0.3, 2.45, "tape", ha="right", va="center", fontsize=8, color=MUTED)
ax.annotate("", xy=(1.0, 2.0), xytext=(1.0, 0.9), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6))
ax.text(1.5, 1.4, "read head (moves right)", fontsize=7.5, color=ACCENT, va="center")
ax.add_patch(mp.FancyBboxPatch((0.4, -1.9), 5.2, 2.7, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#eef3fa", ec=INK, lw=1.2))
ax.text(3.0, 0.2, "finite control", ha="center", fontsize=8.5, fontweight="bold")
ax.text(3.0, -0.55, "current state q   and   transition function δ(q, a)", ha="center", fontsize=7.4)
ax.add_patch(mp.Circle((8.0, -0.55), 0.8, fc="white", ec=INK, lw=1.2)); ax.add_patch(mp.Circle((8.0, -0.55), 0.68, fc="none", ec=INK, lw=1.0))
ax.text(8.0, -0.55, "accept /\nreject", ha="center", va="center", fontsize=6.8)
ax.annotate("", xy=(7.2, -0.55), xytext=(5.6, -0.55), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
ax.text(8.0, -1.8, "output after the last symbol", ha="center", fontsize=7, color=MUTED)
```

**DFA for strings with no two consecutive $b$'s over $\{a,b\}$.** Three states: $q_0$ (last symbol was not $b$, or nothing read yet), $q_1$ (last symbol was a single $b$) and the trap $q_d$ (a $bb$ has occurred). $q_0$ and $q_1$ accept.

| State | on a | on b |
|---|---|---|
| → * $q_0$ | $q_0$ | $q_1$ |
| * $q_1$ | $q_0$ | $q_d$ |
| $q_d$ | $q_d$ | $q_d$ |

```figure caption="Question 2(a): DFA for strings over {a, b} with no two consecutive b's."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
fig = T.graph({"q0": (0, 0, "s,f"), "q1": (3.6, 0, "f"), "qd": (7.2, 0, "")},
              [("q0", "q1", "b", 0.25), ("q1", "q0", "a", 0.25), ("q1", "qd", "b", 0)],
              loops=[("q0", "a", "up"), ("qd", "a, b", "up")])
```

**Processing $w=baaaababb$** (9 symbols):

$q_0\xrightarrow{b}q_1\xrightarrow{a}q_0\xrightarrow{a}q_0\xrightarrow{a}q_0\xrightarrow{a}q_0\xrightarrow{b}q_1\xrightarrow{a}q_0\xrightarrow{b}q_1\xrightarrow{b}q_d$

The string ends in the trap state $q_d$ (the last two symbols are $bb$), so **$w$ is rejected**. (By contrast $baaaabab$ without the final $b$ ends in $q_1$ and is accepted.) A regular expression for the language is $(a+ba)^*(\varepsilon+b)$.

**(b) Equivalence of two automata (procedure).**

1. Convert any NFA to a DFA and complete both DFAs (add a trap state if needed) over the same alphabet.
2. **Method 1, minimisation:** minimise both DFAs; they accept the same language iff the minimal DFAs are identical up to renaming of states.
3. **Method 2, table filling on the union:** take the disjoint union of the two DFAs with start states $s_1,s_2$ and run the table-filling algorithm; mark a pair $(p,q)$ if exactly one of them is accepting, and mark $(p,q)$ if $(\delta(p,a),\delta(q,a))$ is already marked for some $a$. Repeat until no change. The automata are equivalent iff the pair $(s_1,s_2)$ is **not** marked.
4. **Method 3, product automaton:** build a DFA accepting $L_1\triangle L_2$; the automata are equivalent iff its language is empty (no accepting state reachable).

**Conversion of the given NFA to a DFA** (subset construction). $\delta(A,0)=\{A\}$, $\delta(A,1)=\{B\}$, $\delta(B,0)=\{B,C\}$, $\delta(B,1)=\{B\}$, $\delta(C,0)=\{C\}$, $\delta(C,1)=\{B,C\}$; start $\{A\}$, accepting: any set containing $C$.

- $\{A\}$: on 0 $\to\{A\}$; on 1 $\to\{B\}$.
- $\{B\}$: on 0 $\to\{B,C\}$; on 1 $\to\{B\}$.
- $\{B,C\}$: on 0 $\to\delta(B,0)\cup\delta(C,0)=\{B,C\}\cup\{C\}=\{B,C\}$; on 1 $\to\delta(B,1)\cup\delta(C,1)=\{B\}\cup\{B,C\}=\{B,C\}$.

| DFA state | on 0 | on 1 |
|---|---|---|
| → $\{A\}$ | $\{A\}$ | $\{B\}$ |
| $\{B\}$ | $\{B,C\}$ | $\{B\}$ |
| * $\{B,C\}$ | $\{B,C\}$ | $\{B,C\}$ |

```figure caption="Question 2(b): equivalent DFA (3 reachable states; {B,C} is accepting and absorbing)."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
fig = T.graph({"A": (0, 0, "s,label:{A}"), "B": (3.8, 0, "label:{B}"), "BC": (7.6, 0, "f,label:{B,C}")},
              [("A", "B", "1", 0), ("B", "BC", "0", 0)],
              loops=[("A", "0", "up"), ("B", "1", "up"), ("BC", "0, 1", "up")], R=0.5)
```

The three DFA states are pairwise distinguishable ($\{B,C\}$ is the only accepting one; $\{A\}$ and $\{B\}$ differ on input 0), so this DFA is already minimal. It accepts every string that contains the substring **10** (a 1 followed later immediately by a 0), i.e. $(0+1)^*10(0+1)^*$.

**(c) Decision properties of regular languages.** Questions about a regular language $L$ (given as a DFA, NFA or regular expression) that can be answered by an algorithm:

| Property | Algorithm |
|---|---|
| **Membership**, is $w\in L$? | run the DFA on $w$ ($|w|$ steps) |
| **Emptiness**, is $L=\varnothing$? | search the transition graph: $L\ne\varnothing$ iff an accepting state is reachable from the start state |
| **Finiteness**, is $L$ finite? | $L$ is infinite iff a cycle lies on some path from the start state to an accepting state (equivalently, $L$ contains a string with $n\le|w|<2n$ where $n$ is the number of states) |
| **Universality**, is $L=\Sigma^*$? | complement the DFA and test emptiness |
| **Equivalence**, $L_1=L_2$? | minimise both and compare, or test $L_1\triangle L_2=\varnothing$ |
| **Containment**, $L_1\subseteq L_2$? | test $L_1\cap\overline{L_2}=\varnothing$ |
| **Disjointness** | test $L_1\cap L_2=\varnothing$ via the product DFA |

All of them are decidable for regular languages, which is not true for context-free languages (equivalence and universality are undecidable there).

@s 3
**(a) CFG for $L=\{a^nb^mc^md^n : n,m\ge0\}$.** The outer $a$'s match the outer $d$'s, and inside them the $b$'s match the $c$'s:

$$\boxed{\begin{aligned}S&\to aSd\mid T\\ T&\to bTc\mid\varepsilon\end{aligned}}$$

**Test with $w=aabbbcccdd$** ($n=2$, $m=3$):

$$S\Rightarrow aSd\Rightarrow aaSdd\Rightarrow aaTdd\Rightarrow aabTcdd\Rightarrow aabbTccdd\Rightarrow aabbbTcccdd\Rightarrow aabbbcccdd$$

The rules used are $S\to aSd$ twice, $S\to T$, $T\to bTc$ three times and finally $T\to\varepsilon$, so $w\in L(G)$.

```figure caption="Question 3(a): parse tree of aabbbcccdd (the last T derives the empty string e)."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
t = ("S", ["a", ("S", ["a", ("S", [("T", ["b", ("T", ["b", ("T", ["b", ("T", ["ε"]), "c"]), "c"]), "c"])]), "d"]), "d"])
fig = T.tree(t, dx=0.5)
```

**(b) Conversion to CNF.** $G$: $S\to A\mid B$, $A\to aBa\mid\varepsilon$, $B\to bAb\mid\varepsilon$. The language contains $\varepsilon$ (via $S\Rightarrow A\Rightarrow\varepsilon$), so the CNF grammar will need $S_0\to\varepsilon$ for the empty string.

*Step 0: new start symbol.* $S_0\to S$ (the start symbol must not occur on a right-hand side).

*Step 1: remove $\varepsilon$-productions.* Nullable variables: $A$, $B$ (they derive $\varepsilon$ directly) and $S$, $S_0$ (through $A$). Substituting the nullable variables in all ways (and dropping the $\varepsilon$-rules except $S_0\to\varepsilon$):

$S_0\to S\mid\varepsilon$; $S\to A\mid B$; $A\to aBa\mid aa$; $B\to bAb\mid bb$.

*Step 2: remove unit productions.* $S\to A$, $S\to B$ and $S_0\to S$ are units. Replace each by the rules of the target:

$S_0\to aBa\mid aa\mid bAb\mid bb\mid\varepsilon$; $S\to aBa\mid aa\mid bAb\mid bb$ (now $S$ is unreachable and can be dropped); $A\to aBa\mid aa$; $B\to bAb\mid bb$.

*Step 3: terminals.* Introduce $T_a\to a$, $T_b\to b$ and use them in every right-hand side of length $\ge2$:

$S_0\to T_aBT_a\mid T_aT_a\mid T_bAT_b\mid T_bT_b\mid\varepsilon$; $A\to T_aBT_a\mid T_aT_a$; $B\to T_bAT_b\mid T_bT_b$.

*Step 4: shorten right sides of length 3.* $E_1\to BT_a$ (for $T_aBT_a$) and $F_1\to AT_b$ (for $T_bAT_b$):

$$\boxed{\begin{aligned}
S_0&\to T_aE_1\mid T_aT_a\mid T_bF_1\mid T_bT_b\mid\varepsilon\\
A&\to T_aE_1\mid T_aT_a\\
B&\to T_bF_1\mid T_bT_b\\
E_1&\to BT_a,\qquad F_1\to AT_b\\
T_a&\to a,\qquad T_b\to b
\end{aligned}}$$

All rules have the form $X\to YZ$ or $X\to a$ (plus the allowed $S_0\to\varepsilon$ for the start symbol). (Computer check: the original and the CNF grammar generate the same strings of length $\le 12$: $\varepsilon$, $aa$, $bb$, $abba$, $baab$, $abaaba$, $babbab$, ...)

**(c) Pumping lemma for CFLs.** If $L$ is context-free there is a constant $p\ge1$ (pumping length) such that every string $z\in L$ with $|z|\ge p$ can be written $z=uvwxy$ with (i) $|vwx|\le p$, (ii) $|vx|\ge1$ and (iii) $uv^iwx^iy\in L$ for all $i\ge0$.

**$L=\{ww : w\in\{0,1\}^*\}$ is not context-free.** Suppose it is, with pumping length $p$. Take $z=0^p1^p0^p1^p=ww$ with $w=0^p1^p$, so $|z|=4p\ge p$. Write $z=uvwxy$ with $|vwx|\le p$ and $|vx|=k\ge1$, and pump **down** ($i=0$) to get $z'=uwy$ of length $4p-k$. If $k$ is odd, $|z'|$ is odd and $z'$ cannot be of the form $tt$, so let $k$ be even; if $z'=tt$ then $|t|=2p-k/2$. Because $|vwx|\le p$ the window $vwx$ cannot meet blocks 1 and 3, or blocks 2 and 4, so there are three cases ($z=\underbrace{0^p}_{1}\underbrace{1^p}_{2}\underbrace{0^p}_{3}\underbrace{1^p}_{4}$).

- **Case 1: $vwx$ lies in the first half** (blocks 1-2). The last $2p$ symbols of $z'$ are still $0^p1^p$, so the second half of $z'$ is $0^{p-k/2}1^p$ and ends with $1$. The first half of $z'$ ends at position $2p-k/2>2p-k$, i.e. inside the untouched block $0^p$ that follows the modified prefix (here $k\ge2$ is used), so it ends with $0$. The two halves differ.
- **Case 2: $vwx$ lies in the second half** (blocks 3-4). The first $2p$ symbols of $z'$ are still $0^p1^p$, so the first half is $0^p1^{p-k/2}$ and starts with $0$. The second half starts with the last $k/2\ge1$ symbols of block 2, i.e. with $1$. The two halves differ.
- **Case 3: $vwx$ straddles the middle** (so it lies inside $1^p0^p$ of blocks 2-3). Deleting $v$ and $x$ removes $a$ ones and $b$ zeros, $a+b=k\ge1$, so $z'=0^p1^{p-a}0^{p-b}1^p$. If $z'=tt$ then $t$ starts with $0^p$ and ends with $1^p$, so the junction of the two copies contains the substring $1^p0^p$ (a run of at least $p$ ones followed directly by a run of at least $p$ zeros). The runs of $z'$ have lengths $p,\ p-a,\ p-b,\ p$ in this order, so such a junction would need $p-a\ge p$ and $p-b\ge p$, i.e. $a=b=0$, which contradicts $k\ge1$.

In every case $uv^0wx^0y\notin L$, contradicting the pumping lemma. Hence $L=\{ww\}$ is **not context-free**. $\blacksquare$ (Its complement, in contrast, is context-free.)

@s 4
**(a) TM for $L=\{a^ncb^n : n\ge0\}$.** Mark the leftmost unmarked $a$ as $X$, run to the right across the $c$, mark the first unmarked $b$ as $Y$ and return to the $X$. Repeat. When no $a$ is left the head meets $c$, and the machine checks that only $Y$'s remain after $c$.

$M=(\{q_0,q_1,q_2,q_4,q_f\},\{a,b,c\},\{a,b,c,X,Y,B\},\delta,q_0,B,\{q_f\})$ (the state $q_3$ is not used):

{{TMTAB:ACB}}

```figure caption="Question 4(a): transition diagram of the a^n c b^n Turing machine (label: read / write, move)."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
nodes = {"q0": (0, 0, "s"), "q1": (4.2, 0, ""), "q2": (4.2, -3, ""), "q4": (0, -3, ""), "qf": (-3.5, -3, "f")}
edges = [("q0", "q1", "a/X,R", 0), ("q1", "q2", "b/Y,L", 0), ("q2", "q0", "X/X,R", 0.15), ("q0", "q4", "c/c,R", 0), ("q4", "qf", "B/B,S", 0)]
loops = [("q1", "a, c, Y: R", "up"), ("q2", "a, c, Y: L", "down"), ("q4", "Y: R", "down")]
fig = T.graph(nodes, edges, loops, fs=6.8)
```

**Acceptance of $w=aaaacbbbb$.** Sequence of configurations (computed by running the machine; the bracket marks the state and head position):

{{TM:ACB:aaaacbbbb}}

The machine ends in $q_f$, so **$w$ is accepted**. It rejects, for example, $aacb$ (the $a$ is left over: the head reaches $B$ in $q_1$ without a $b$) and $acbb$ (a $b$ remains after the last $Y$ check, so $q_4$ finds a $b$ and stops); $c$ alone is accepted ($n=0$). (Verified on every string over $\{a,b,c\}$ up to length 9.)

**(b) TM computing $f(x)=2x$.** Represent the non-negative integer $x=n$ in **unary** as $1^n$ on the tape; the machine must leave $1^{2n}$. (In binary the same function is trivial: move to the right end and append a 0, i.e. shift left by one bit.)

Idea: for each original $1$, mark it $X$ and add *two* new marked 1s ($Y$) at the right end. At the end, erase the $X$'s and turn the $Y$'s into 1s, leaving $2n$ ones.

{{TMTAB:DBL}}

States: $q_0$ finds the next unmarked 1 (skipping $X$'s); $q_1$-$q_3$ go right, append $YY$ and come back; $q_6$ turns $Y\to1$ at the end; $q_7$-$q_9$ erase the $X$'s and stop ($q_h$, the head is on the first 1 of the answer).

**Trace for $x=2$** ($11\mapsto1111$):

{{TM:DBL:11}}

The final tape is $1111=1^4$, i.e. $f(2)=4$. (Checked for $n=0,1,\dots,8$: the output is always $1^{2n}$.)

**(c) Properties of recursive (decidable) languages.** A language is **recursive** if some TM *halts on every input* and accepts exactly the strings of the language.

1. Every recursive language is recursively enumerable, but not conversely (the halting language is RE but not recursive).
2. **Complement:** the complement of a recursive language is recursive (swap the accepting and rejecting halt states of the always-halting TM).
3. **Union and intersection:** closed (run both deciders, combine the answers).
4. **Concatenation and Kleene star:** closed (try all splits of $w$, finitely many).
5. **Reversal, difference, intersection with a regular language:** closed.
6. **Not closed under homomorphism** (the homomorphic image of a recursive language can be any recursively enumerable language), but closed under inverse homomorphism.
7. **Characterisation:** $L$ is recursive iff both $L$ and $\overline L$ are recursively enumerable (Post's theorem). Run the two recognisers in parallel; exactly one of them accepts.
8. **Membership** is decidable (that is the definition), but for general recursive languages emptiness, equivalence and finiteness are undecidable (Rice's theorem).
9. Every context-free and every context-sensitive language is recursive.

@s 5
**(a) Encoding of a Turing machine.** To give a TM as *input* to another TM (a universal machine), the machine $M=(Q,\Sigma,\Gamma,\delta,q_1,B,F)$ is written as a string over $\{0,1\}$:

1. Number the states $q_1,\dots,q_n$ ($q_1$ start, $q_2$ accepting), the tape symbols $X_1=0,X_2=1,X_3=B,\dots$ and the directions $D_1=L$, $D_2=R$.
2. Each move $\delta(q_i,X_j)=(q_k,X_l,D_m)$ is encoded as the block $0^i10^j10^k10^l10^m$ (the 1 is a separator, so a block never contains $11$).
3. The machine is the concatenation of all move blocks separated by $11$: $\langle M\rangle=C_1\,11\,C_2\,11\cdots11\,C_r$. An input $w$ is encoded by writing each symbol as $0^j$ separated by single 1s, and $\langle M,w\rangle=\langle M\rangle\,111\,\langle w\rangle$.

**Example.** The bit-complement machine {{ENC:COMP}}

This encoding makes TMs ordinary strings, so a *universal* TM can read $\langle M,w\rangle$, simulate $M$ on $w$, and one can talk about "a TM given the code of a TM" (halting problem, diagonal language).

**(b) NP-complete problems.** **P** is the class of decision problems solvable by a deterministic TM in polynomial time; **NP** is the class solvable by a non-deterministic TM in polynomial time (equivalently, a given solution can be *verified* in polynomial time). A problem $L$ is **NP-complete** if

1. $L\in NP$, and
2. every problem in NP reduces to $L$ in polynomial time ($L$ is NP-hard).

If one NP-complete problem is solvable in polynomial time then $P=NP$; so these are the hardest problems in NP. The first NP-complete problem is **SAT** (Cook-Levin theorem); others follow by polynomial reductions: 3-SAT, Clique, Vertex Cover, Hamiltonian Cycle, Travelling Salesman (decision version), Subset Sum, 3-Colouring. To prove a new problem NP-complete: show it is in NP (give a polynomial verifier) and reduce a known NP-complete problem to it in polynomial time.

@s 6
**(a) Lexical analyzer and DFA.** The lexical analyzer (scanner) turns the character stream of the source code into tokens. Each token class (identifier, number, keyword, operator, ...) is described by a **regular expression**, and every regular expression is equivalent to a finite automaton. The scanner generator (Lex/Flex) converts all expressions into one NFA, then into a **DFA**, which is the scanning engine: the DFA reads characters from the start state, remembers the last accepting state it passed through (longest-match rule) and, when no move is possible, returns the token of that accepting state, backing up the input to the end of that lexeme. A DFA is used because it needs one table look-up per character, so the scanner is linear in the length of the program.

**Example: identifiers and integers.** Patterns: $\text{id}=\text{letter}(\text{letter}+\text{digit})^*$, $\text{num}=\text{digit}^+$.

```figure caption="Question 6(a): one DFA recognising identifiers (state id) and unsigned integers (state num); both are accepting."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
fig = T.graph({"s": (0, 0, "s,label:start"), "id": (4, 1.4, "f"), "num": (4, -1.4, "f")},
              [("s", "id", "letter", 0), ("s", "num", "digit", 0)],
              loops=[("id", "letter, digit", "up"), ("num", "digit", "down")], R=0.55)
```

Scanning `x1 = 25;`: from the start state `x` (letter) goes to *id*, `1` (digit) stays in *id*, the blank has no move, so the token `<id, x1>` is returned; `=` gives `<op, =>`; `2` goes to *num* and `5` stays in *num*, so `<num, 25>` is returned; `;` gives `<punct, ;>`. Keywords such as `if` also match the identifier DFA and are separated out afterwards by a look-up in the keyword table.

**(b) Parse tree of $r=a+b*c/(d*e)$.** Use the standard unambiguous expression grammar, in which $*$ and $/$ have the same precedence (higher than $+$) and associate to the left:

$$\begin{aligned}S&\to \textbf{id}=E\\ E&\to E+T\mid T\\ T&\to T*F\mid T/F\mid F\\ F&\to(E)\mid\textbf{id}\end{aligned}$$

So $a+b*c/(d*e)=a+\big((b*c)/(d*e)\big)$. Derivation (leftmost): `S` ⇒ `r = E` ⇒ `r = E + T` ⇒ `r = T + T` ⇒ `r = F + T` ⇒ `r = a + T` ⇒ `r = a + T / F` ⇒ `r = a + T * F / F` ⇒ `r = a + F * F / F` ⇒ `r = a + b * F / F` ⇒ `r = a + b * c / F` ⇒ `r = a + b * c / ( E )` ⇒ `r = a + b * c / ( T )` ⇒ `r = a + b * c / ( T * F )` ⇒ `r = a + b * c / ( F * F )` ⇒ `r = a + b * c / ( d * e )`.

```figure caption="Question 6(b): parse tree of r = a + b * c / (d * e) (E: expression, T: term, F: factor)."
import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib as T
F = lambda *k: ("F", list(k))
a_ = ("E", [("T", [F("a")])])
bc = ("T", [("T", [F("b")]), "*", F("c")])
de = ("E", [("T", [("T", [F("d")]), "*", F("e")])])
div = ("T", [bc, "/", F("(", de, ")")])
fig = T.tree(("S", ["r", "=", ("E", [a_, "+", div])]), dx=0.5, fs=7.6)
```

The root $E\to E+T$ shows that the addition is performed last; the right operand $T\to T/F$ divides the product $b*c$ by the bracketed factor $(d*e)$. A post-order walk of the tree gives the evaluation order $b\,c\,*\,d\,e\,*\,/\,a\,+$ (postfix).
