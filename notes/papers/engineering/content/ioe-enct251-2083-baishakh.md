---
file: NEBians-IOE-Past-Paper-Discrete-Structure-ENCT251-2083-Baishakh.pdf
subject: Discrete Structure
level: BE · Year II / Part II
code: ENCT 251
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Consider the premises: "If I get my Dashain bonus and my friends are free then I will take a road trip with my friends." "If my friends don't find a job after Dashain, then they will be free." "I got my Dashain bonus and my friends did not find a job after Dashain." Leads to the conclusion: "I will take a road trip with my friends." using propositional logic. [[3]]

@q 2
Define the term converse, inverse and contrapositive with example. Explain universal quantification and existential quantification. Let x and y be the real number and p(x, y) denotes "x + y >= 0". What are the truth values of nested quantification? [[2+2+3]]

@q 3
Prove that $\sqrt{2}+\sqrt{3}$ is irrational using proof by contradiction. [[3]]

@q 4
Using mathematical induction show that $1^2+2^2+3^2+\cdots+n^2=\dfrac{n(n+1)(2n+1)}{6}$. [[4]]

@q 5
Convert the following NDFA into equivalent DFA. [[4]]

```figure caption="Question 5: the given NDFA: start state P, accepting state R; P-b->R, R-a->P, P-a->Q, Q-b->Q, Q-a,b->R."
import numpy as _np, matplotlib.patches as mp
R_=0.36
def N(ax,p,t,fin=False,st=False,fs=7.5):
    ax.add_patch(mp.Circle(p,R_,fc="white",ec=INK,lw=1.2,zorder=3))
    if fin: ax.add_patch(mp.Circle(p,R_-0.08,fc="none",ec=INK,lw=1.0,zorder=4))
    ax.text(p[0],p[1],t,ha="center",va="center",fontsize=fs,zorder=5)
    if st: ax.annotate("",xy=(p[0]-R_,p[1]),xytext=(p[0]-R_-0.8,p[1]),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.1))
def E(ax,a,b,t,rad=0.0,dl=(0,0)):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.1,shrinkA=15,shrinkB=15,connectionstyle="arc3,rad=%s"%rad),zorder=2)
    dx,dy=b[0]-a[0],b[1]-a[1]; m=((a[0]+b[0])/2+0.5*rad*dy+dl[0],(a[1]+b[1])/2-0.5*rad*dx+dl[1])
    ax.text(m[0],m[1],t,ha="center",va="center",fontsize=7.5,color="#b00020",bbox=dict(fc="white",ec="none",pad=0.4),zorder=6)
def L(ax,p,t):
    ax.add_patch(mp.Arc((p[0],p[1]+R_+0.2),0.6,0.6,theta1=-20,theta2=200,ec=ACCENT,lw=1.1,zorder=2)); ax.text(p[0],p[1]+R_+0.66,t,ha="center",va="center",fontsize=7.5,color="#b00020")
fig,ax=plt.subplots(figsize=(4.6,2.5)); ax.axis("off"); ax.set_xlim(-1.4,6.2); ax.set_ylim(-1.3,3.7); ax.set_aspect("equal")
P=(0,2);R=(5,2);Q=(2.5,0)
N(ax,P,"P",st=True); N(ax,R,"R",fin=True); N(ax,Q,"Q")
E(ax,P,R,"b",rad=-0.3); E(ax,R,P,"a",rad=-0.3); E(ax,P,Q,"a"); E(ax,Q,R,"a, b"); L(ax,Q,"b")
```

@q 6
Write a regular expression for the language that accepts all the string that does not contains three consecutive b over Σ = {a, b}. Write a CFG that generates the palindrome string of even length over the alphabet Σ = {0, 1}. Also generate the string w = 10100101 using right most derivation and draw the parse tree for the same. [[2+3+2]]

@q 7
Show that regular language is closed under Kleene star and complement operation. [[3]]

@q 8
Write an algorithm to perform sort operation using insertion sort. Search for key = 45 from the given data 92, 87, 32, 56, 57, 45, 11, 77, 28. [[2+2]]

@q 9
Solve the recurrence relation $a_n = 5a_{n-1} - 6a_{n-2} + 2^n$ with initial condition $a_0 = 1$ and $a_1 = 4$. [[4]]

@q 10
Define regular graph. Explain different graph representation techniques with example. [[1+4]]

@q 11
State Dirac's and Ore's theorem. Is $K_5$ and $K_{3,3}$ planar graph? Justify your answer. [[2+2+2]]

@q 12
Draw $W_6$ and write its incidence matrix. Find the minimum spanning tree using Prim's algorithm from the graph given below. [[2+4]]

```figure caption="Question 12: weighted graph (edge weights: ab 5, ad 3, bd 4, bc 2, be 6, de 5, ec 6, eg 6, cg 3, cf 5, gf 4, dg 6)."
import numpy as _np
E=[('a', 'b', 5), ('a', 'd', 3), ('b', 'd', 4), ('b', 'c', 2), ('b', 'e', 6), ('d', 'e', 5), ('e', 'c', 6), ('e', 'g', 6), ('c', 'g', 3), ('c', 'f', 5), ('g', 'f', 4), ('d', 'g', 6)]
P={"a":(0,1.5),"b":(2,3),"c":(5,3.2),"d":(2,0),"e":(3.5,1.6),"f":(7,1.6),"g":(5,0)}
fig,ax=plt.subplots(figsize=(5.2,2.9)); ax.axis("off"); ax.set_aspect("equal")
for u,v,w in E:
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color=INK,lw=1.2,zorder=1)
    ax.text((P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2,str(w),fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=9,zorder=5)
ax.set_xlim(-0.6,7.6); ax.set_ylim(-0.7,3.9)
```

@q 13
Find the Maximum flow for the network given below. Each edge is labelled (capacity, flow). [[4]]

```figure caption="Question 13: the given network, edges labelled (capacity, current flow); the current flow is 21."
import numpy as _np, matplotlib.patches as mp
CAP={(1, 2): 15, (1, 5): 15, (2, 3): 9, (2, 4): 7, (5, 4): 7, (4, 3): 5, (4, 6): 15, (4, 7): 5, (5, 7): 7, (6, 3): 4, (6, 8): 10, (6, 7): 4, (3, 8): 10, (7, 8): 10}
FL={(1, 2): 11, (1, 5): 10, (2, 3): 4, (2, 4): 7, (5, 4): 7, (4, 3): 4, (4, 6): 6, (4, 7): 4, (5, 7): 3, (6, 3): 2, (6, 8): 4, (6, 7): 0, (3, 8): 10, (7, 8): 7}
P={1:(0,2.5),2:(2.4,4.7),3:(6.0,4.7),4:(2.8,2.5),5:(2.4,0.3),6:(6.0,2.5),7:(5.4,0.3),8:(8.6,2.5)}
fig,ax=plt.subplots(figsize=(6.0,3.3)); ax.axis("off"); ax.set_aspect("equal")
for (u,v),c in CAP.items():
    f=FL[(u,v)]; sat=(f==c)
    ax.annotate("",xy=P[v],xytext=P[u],arrowprops=dict(arrowstyle="-|>",color="#b00020" if sat else ACCENT,lw=1.2,shrinkA=13,shrinkB=13),zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,"(%d, %d)"%(c,f),fontsize=7,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.3),zorder=4,color="#b00020" if sat else INK)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=300,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],"V%d"%k,ha="center",va="center",fontsize=7.5,zorder=5)
ax.set_xlim(-0.8,9.4); ax.set_ylim(-0.4,5.3)
```
<!-- SOLUTIONS -->

@s 1
Let $p$: I get my Dashain bonus; $f$: my friends are free; $t$: I take a road trip with my friends; $j$: my friends find a job after Dashain.

Premises: $H_1: (p \wedge f) \rightarrow t$, $H_2: \neg j \rightarrow f$, $H_3: p \wedge \neg j$. Conclusion: $t$.

| Step | Statement | Reason |
|---|---|---|
| 1 | $p \wedge \neg j$ | premise $H_3$ |
| 2 | $p$ | simplification of 1 |
| 3 | $\neg j$ | simplification of 1 |
| 4 | $\neg j \rightarrow f$ | premise $H_2$ |
| 5 | $f$ | modus ponens on 3, 4 |
| 6 | $p \wedge f$ | conjunction of 2, 5 |
| 7 | $(p \wedge f) \rightarrow t$ | premise $H_1$ |
| 8 | $t$ | modus ponens on 6, 7 |

$$\boxed{\,((p \wedge f) \rightarrow t) \wedge (\neg j \rightarrow f) \wedge (p \wedge \neg j)\ \Rightarrow\ t\,}$$

The argument is **valid**: the conclusion "I will take a road trip with my friends" follows from the premises. (Truth-table check: the only rows where all three premises are true have $p = T$, $j = F$, $f = T$, which forces $t = T$.)

@s 2
**Converse, inverse, contrapositive.** For a conditional statement $p \rightarrow q$:

| Statement | Form | Example ($p$: it rains, $q$: the ground is wet) |
|---|---|---|
| Conditional | $p \rightarrow q$ | If it rains, then the ground is wet |
| **Converse** | $q \rightarrow p$ | If the ground is wet, then it rains |
| **Inverse** | $\neg p \rightarrow \neg q$ | If it does not rain, then the ground is not wet |
| **Contrapositive** | $\neg q \rightarrow \neg p$ | If the ground is not wet, then it does not rain |

The contrapositive is always logically equivalent to the conditional ($p \rightarrow q \equiv \neg q \rightarrow \neg p$), and the converse and inverse are equivalent to each other, but neither is equivalent to the original.

**Universal quantification.** $\forall x\,P(x)$ ("for all $x$, $P(x)$") is true when $P(x)$ is true for **every** $x$ in the domain; one counter-example makes it false. Negation: $\neg\forall x P(x) \equiv \exists x\,\neg P(x)$.

**Existential quantification.** $\exists x\,P(x)$ ("there exists an $x$ such that $P(x)$") is true when **at least one** $x$ in the domain makes $P(x)$ true; it is false only if $P(x)$ is false for every $x$. Negation: $\neg\exists x P(x) \equiv \forall x\,\neg P(x)$.

**Nested quantifiers for $P(x, y)$: $x + y \ge 0$ over the real numbers.**

| Statement | Truth value | Reason |
|---|---|---|
| $\forall x\,\forall y\,P(x,y)$ | **False** | $x = -1,\ y = -2$ gives $-3 < 0$ |
| $\exists x\,\exists y\,P(x,y)$ | **True** | $x = y = 1$ |
| $\forall x\,\exists y\,P(x,y)$ | **True** | for any $x$ take $y = -x$ (or $y = |x|$): $x + y \ge 0$ |
| $\forall y\,\exists x\,P(x,y)$ | **True** | for any $y$ take $x = -y$ |
| $\exists x\,\forall y\,P(x,y)$ | **False** | whatever $x$ is, $y = -x - 1$ gives $-1 < 0$ |
| $\exists y\,\forall x\,P(x,y)$ | **False** | whatever $y$ is, $x = -y - 1$ gives $-1 < 0$ |

The order of the quantifiers matters: $\forall x\exists y\,P$ is true but $\exists y\forall x\,P$ is false.

@s 3
**Claim:** $\sqrt{2} + \sqrt{3}$ is irrational.

*Proof by contradiction.* Assume $\sqrt{2} + \sqrt{3} = r$ with $r$ rational ($r > 0$). Then $\sqrt{3} = r - \sqrt{2}$. Squaring both sides:

$$3 = r^{2} - 2r\sqrt{2} + 2 \;\Rightarrow\; 2r\sqrt{2} = r^{2} - 1 \;\Rightarrow\; \sqrt{2} = \frac{r^{2} - 1}{2r}$$

Since $r$ is rational and non-zero, the right-hand side is rational, so $\sqrt{2}$ would be rational. But $\sqrt{2}$ is irrational: if $\sqrt{2} = a/b$ in lowest terms, then $a^{2} = 2b^{2}$, so $a$ is even, $a = 2c$; then $b^{2} = 2c^{2}$ and $b$ is even too, contradicting lowest terms.

This contradiction shows that the assumption is false. Hence

$$\boxed{\,\sqrt{2} + \sqrt{3}\ \text{is irrational.}\,}$$

@s 4
**Claim** $P(n)$: $1^{2} + 2^{2} + \cdots + n^{2} = \dfrac{n(n+1)(2n+1)}{6}$ for all integers $n \ge 1$.

**Basis step ($n = 1$).** LHS $= 1^{2} = 1$; RHS $= \dfrac{1\cdot2\cdot3}{6} = 1$. So $P(1)$ is true.

**Inductive step.** Assume $P(k)$ is true for some $k \ge 1$:

$$1^{2} + 2^{2} + \cdots + k^{2} = \frac{k(k+1)(2k+1)}{6}$$

Add $(k+1)^{2}$ to both sides:

$$\begin{aligned}1^{2} + \cdots + k^{2} + (k+1)^{2} &= \frac{k(k+1)(2k+1)}{6} + (k+1)^{2} \\ &= \frac{(k+1)\left[k(2k+1) + 6(k+1)\right]}{6} \\ &= \frac{(k+1)\left(2k^{2} + 7k + 6\right)}{6} \\ &= \frac{(k+1)(k+2)(2k+3)}{6}\end{aligned}$$

This is $P(k+1)$, since $\dfrac{(k+1)((k+1)+1)(2(k+1)+1)}{6} = \dfrac{(k+1)(k+2)(2k+3)}{6}$. Thus $P(k) \Rightarrow P(k+1)$.

By the principle of mathematical induction

$$\boxed{\,1^{2} + 2^{2} + \cdots + n^{2} = \frac{n(n+1)(2n+1)}{6}\ \text{for all}\ n \ge 1.\,}$$

@s 5
**Transition table of the NDFA** (start state P, accepting state R; R has no transition on $b$):

| State | on $a$ | on $b$ |
|---|---|---|
| → P | $\{Q\}$ | $\{R\}$ |
| Q | $\{R\}$ | $\{Q, R\}$ |
| * R | $\{P\}$ | $\varnothing$ |

**Subset construction.** Start with $\{P\}$ and compute the moves of every new subset (a subset is accepting if it contains R):

| DFA state | on $a$ | on $b$ |
|---|---|---|
| → $\{P\}$ | $\{Q\}$ | $\{R\}$ |
| $\{Q\}$ | $\{R\}$ | $\{Q,R\}$ |
| * $\{R\}$ | $\{P\}$ | $\varnothing$ |
| * $\{Q,R\}$ | $\{P,R\}$ | $\{Q,R\}$ |
| $\varnothing$ | $\varnothing$ | $\varnothing$ |
| * $\{P,R\}$ | $\{P,Q\}$ | $\{R\}$ |
| $\{P,Q\}$ | $\{Q,R\}$ | $\{Q,R\}$ |

Here → marks the start state and * the accepting states. The reachable DFA has **seven states**: $\{P\}$, $\{Q\}$, $\{R\}$, $\{Q,R\}$, $\{P,R\}$, $\{P,Q\}$ and the dead (trap) state $\varnothing$. For example $\delta(\{Q,R\}, a) = \delta(Q,a) \cup \delta(R,a) = \{R\} \cup \{P\} = \{P,R\}$ and $\delta(\{P,R\}, a) = \{Q\} \cup \{P\} = \{P,Q\}$.

```figure caption="Equivalent DFA by subset construction (7 states; accepting states are those containing R; the empty set is the dead state)."
import numpy as _np, matplotlib.patches as mp
R_=0.36
def N(ax,p,t,fin=False,st=False,fs=7.5):
    ax.add_patch(mp.Circle(p,R_,fc="white",ec=INK,lw=1.2,zorder=3))
    if fin: ax.add_patch(mp.Circle(p,R_-0.08,fc="none",ec=INK,lw=1.0,zorder=4))
    ax.text(p[0],p[1],t,ha="center",va="center",fontsize=fs,zorder=5)
    if st: ax.annotate("",xy=(p[0]-R_,p[1]),xytext=(p[0]-R_-0.8,p[1]),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.1))
def E(ax,a,b,t,rad=0.0,dl=(0,0)):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.1,shrinkA=15,shrinkB=15,connectionstyle="arc3,rad=%s"%rad),zorder=2)
    dx,dy=b[0]-a[0],b[1]-a[1]; m=((a[0]+b[0])/2+0.5*rad*dy+dl[0],(a[1]+b[1])/2-0.5*rad*dx+dl[1])
    ax.text(m[0],m[1],t,ha="center",va="center",fontsize=7.5,color="#b00020",bbox=dict(fc="white",ec="none",pad=0.4),zorder=6)
def L(ax,p,t):
    ax.add_patch(mp.Arc((p[0],p[1]+R_+0.2),0.6,0.6,theta1=-20,theta2=200,ec=ACCENT,lw=1.1,zorder=2)); ax.text(p[0],p[1]+R_+0.66,t,ha="center",va="center",fontsize=7.5,color="#b00020")
fig,ax=plt.subplots(figsize=(6.4,3.5)); ax.axis("off"); ax.set_xlim(-1.4,9.6); ax.set_ylim(-2.1,5.6); ax.set_aspect("equal")
pos={"P":(0,2.5),"Q":(2.8,4.3),"R":(2.8,0.8),"QR":(5.8,4.3),"PR":(5.8,0.8),"PQ":(8.6,2.5),"D":(0.3,-1.0)}
nm={"P":"{P}","Q":"{Q}","R":"{R}","QR":"{Q,R}","PR":"{P,R}","PQ":"{P,Q}","D":"∅"}
for k,p in pos.items(): N(ax,p,nm[k],fin=k in("R","QR","PR"),st=(k=="P"),fs=6.8)
E(ax,pos["P"],pos["Q"],"a"); E(ax,pos["P"],pos["R"],"b",rad=-0.3); E(ax,pos["R"],pos["P"],"a",rad=-0.3)
E(ax,pos["Q"],pos["R"],"a"); E(ax,pos["Q"],pos["QR"],"b"); L(ax,pos["QR"],"b")
E(ax,pos["QR"],pos["PR"],"a"); E(ax,pos["PR"],pos["R"],"b"); E(ax,pos["PR"],pos["PQ"],"a")
E(ax,pos["PQ"],pos["QR"],"a, b"); E(ax,pos["R"],pos["D"],"b"); L(ax,pos["D"],"a, b")
```

Renaming the states $A = \{P\}$, $B = \{Q\}$, $C = \{R\}$, $D = \{Q,R\}$, $E = \{P,R\}$, $F = \{P,Q\}$, $G = \varnothing$ gives the DFA $(\{A..G\}, \{a,b\}, \delta, A, \{C, D, E\})$ with the table above.

@s 6
**(i) Regular expression** for the strings over $\{a, b\}$ with no three consecutive $b$'s. Every $b$ must be followed by an $a$ unless the string ends, and a run of $b$'s has length at most 2. So the string is a sequence of blocks $a$, $ba$, $bba$ (each ends with $a$) followed by an optional tail of $b$ or $bb$:

$$\boxed{\,r = (a + ba + bba)^{*}\,(\varepsilon + b + bb)\,}$$

(The expression was checked by computer against every string over $\{a,b\}$ of length up to 12: it accepts exactly the strings that do not contain $bbb$.) Examples accepted: $\varepsilon$, $abbabb$, $bbabab$; rejected: $abbba$.

**(ii) CFG for even-length palindromes over $\{0, 1\}$.**

$$\boxed{\,S \rightarrow 0S0 \mid 1S1 \mid \varepsilon\,}$$

The base case $\varepsilon$ gives the empty palindrome; each step wraps the same symbol at both ends, so only even-length palindromes are generated (no single middle symbol).

**(iii) Derivation of $w = 10100101$.** $w$ is a palindrome of length 8 (pairs: $1,1$; $0,0$; $1,1$; $0,0$). Since every sentential form has only one variable, the right-most derivation is also the left-most derivation:

$$S \Rightarrow 1S1 \Rightarrow 10S01 \Rightarrow 101S101 \Rightarrow 1010S0101 \Rightarrow 10100101$$

(rules used: $S \to 1S1$, $S \to 0S0$, $S \to 1S1$, $S \to 0S0$, $S \to \varepsilon$.)

```figure caption="Parse tree of w = 10100101 for S -> 0S0 | 1S1 | e (each internal S has the children digit, S, digit; the last S derives e)."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.2,3.8)); ax.axis("off"); ax.set_xlim(-2.2,2.2); ax.set_ylim(-5.8,0.7)
digs=["1","0","1","0"]
for k,d in enumerate(digs):
    y=-1.15*k; yc=y-1.0
    ax.plot([0,-0.9],[y-0.18,yc+0.18],color=INK,lw=1); ax.plot([0,0.9],[y-0.18,yc+0.18],color=INK,lw=1); ax.plot([0,0],[y-0.18,yc+0.18],color=INK,lw=1)
    ax.text(0,y,"S",ha="center",va="center",fontsize=10,fontweight="bold",color=ACCENT)
    ax.text(-0.9,yc,d,ha="center",va="center",fontsize=10); ax.text(0.9,yc,d,ha="center",va="center",fontsize=10)
y=-1.15*4; ax.text(0,y,"S",ha="center",va="center",fontsize=10,fontweight="bold",color=ACCENT)
ax.plot([0,0],[y-0.18,y-0.8],color=INK,lw=1); ax.text(0,y-1.0,"ε",ha="center",va="center",fontsize=10)
ax.text(1.55,-0.0,"S ⇒ 1S1",fontsize=7.5,va="center"); ax.text(1.55,-1.15,"⇒ 10S01",fontsize=7.5,va="center"); ax.text(1.55,-2.3,"⇒ 101S101",fontsize=7.5,va="center"); ax.text(1.55,-3.45,"⇒ 1010S0101",fontsize=7.5,va="center"); ax.text(1.55,-4.6,"⇒ 10100101",fontsize=7.5,va="center")
ax.set_xlim(-2.0,3.4)
```

@s 7
**Closure under Kleene star.** Let $L$ be regular, recognised by an NFA $M = (Q, \Sigma, \delta, q_0, F)$. Build $M'$ with a new start state $s$ that is also accepting (so $\varepsilon \in L^{*}$):

1. add $\varepsilon$-transitions $s \to q_0$;
2. add $\varepsilon$-transitions from every accepting state $f \in F$ back to $q_0$ (to repeat the string);
3. accepting states of $M'$: $F \cup \{s\}$.

$M'$ accepts $\varepsilon$ and any concatenation $w_1w_2\cdots w_k$ with each $w_i \in L$, i.e. $L(M') = L^{*}$. Since $M'$ is an NFA (with $\varepsilon$-moves), $L^{*}$ is regular. Equivalently, if $r$ is a regular expression for $L$ then $r^{*}$ is a regular expression for $L^{*}$.

**Closure under complement.** Let $L$ be regular and $D = (Q, \Sigma, \delta, q_0, F)$ a *complete* DFA for $L$ (every state has a move on every symbol; add a dead state if needed). Define

$$\overline{D} = (Q, \Sigma, \delta, q_0, Q \setminus F)$$

i.e. the same automaton with accepting and non-accepting states interchanged. For every string $w$, $\delta^{*}(q_0, w)$ is a single state, so $w \in L(\overline{D}) \iff \delta^{*}(q_0,w) \notin F \iff w \notin L$. Hence $L(\overline{D}) = \overline{L} = \Sigma^{*} \setminus L$, which is regular.

**Conclusion:** the class of regular languages is closed under Kleene star and under complement (and by De Morgan also under intersection).

@s 8
**Insertion sort algorithm** (ascending order). The array is divided into a sorted part (left) and an unsorted part; each element in turn is inserted into its place in the sorted part by shifting the larger elements one place to the right.

```
INSERTION-SORT(A, n)
for i = 2 to n
    key = A[i]
    j = i - 1
    while j >= 1 and A[j] > key
        A[j+1] = A[j]          // shift larger element right
        j = j - 1
    A[j+1] = key               // insert key
```

Worst case $O(n^{2})$ comparisons (reverse-sorted input), best case $O(n)$ (already sorted); it is stable and in-place.

**Sorting the data 92, 87, 32, 56, 57, 45, 11, 77, 28:**

| Step | Array after the step |
|---|---|
| initial | 92, 87, 32, 56, 57, 45, 11, 77, 28 |
| pass 1 (insert 87) | 87, 92, 32, 56, 57, 45, 11, 77, 28 |
| pass 2 (insert 32) | 32, 87, 92, 56, 57, 45, 11, 77, 28 |
| pass 3 (insert 56) | 32, 56, 87, 92, 57, 45, 11, 77, 28 |
| pass 4 (insert 57) | 32, 56, 57, 87, 92, 45, 11, 77, 28 |
| pass 5 (insert 45) | 32, 45, 56, 57, 87, 92, 11, 77, 28 |
| pass 6 (insert 11) | 11, 32, 45, 56, 57, 87, 92, 77, 28 |
| pass 7 (insert 77) | 11, 32, 45, 56, 57, 77, 87, 92, 28 |
| pass 8 (insert 28) | 11, 28, 32, 45, 56, 57, 77, 87, 92 |

Sorted data (positions 1 to 9): 11, 28, 32, 45, 56, 57, 77, 87, 92.

**Search for key = 45.** The data is now sorted, so binary search is used ($mid = \lfloor (low + high)/2 \rfloor$):

| Step | low | high | mid | a[mid] | Decision |
|---|---|---|---|---|---|
| 1 | 1 | 9 | 5 | 56 | 45 < 56: high = mid - 1 |
| 2 | 1 | 4 | 2 | 28 | 45 > 28: low = mid + 1 |
| 3 | 3 | 4 | 3 | 32 | 45 > 32: low = mid + 1 |
| 4 | 4 | 4 | 4 | 45 | **found** |

$$\boxed{\,\text{key 45 found at position 4 (index 3 counting from 0) after 4 comparisons}\,}$$

(A linear search on the original unsorted list would find 45 at position 6 after 6 comparisons.)

@s 9
$a_n = 5a_{n-1} - 6a_{n-2} + 2^{n}$, $a_0 = 1$, $a_1 = 4$.

**Homogeneous part.** $a_n - 5a_{n-1} + 6a_{n-2} = 0$ has characteristic equation $r^{2} - 5r + 6 = 0$, i.e. $(r - 2)(r - 3) = 0$, so $r = 2,\ 3$:

$$a_n^{(h)} = \alpha\,2^{n} + \beta\,3^{n}$$

**Particular solution.** The non-homogeneous term is $2^{n}$ and $2$ is a **root** of the characteristic equation, so the trial solution is multiplied by $n$: $a_n^{(p)} = An\,2^{n}$. Substituting:

$$An2^{n} = 5A(n-1)2^{n-1} - 6A(n-2)2^{n-2} + 2^{n}$$

Divide by $2^{n}$: $An = \tfrac{5}{2}A(n-1) - \tfrac{6}{4}A(n-2) + 1 = An + \tfrac{1}{2}A + 1$, so $\tfrac{A}{2} + 1 = 0$ and $A = -2$:

$$a_n^{(p)} = -2n\,2^{n} = -n\,2^{n+1}$$

**General solution:** $a_n = \alpha 2^{n} + \beta 3^{n} - 2n\,2^{n}$.

**Constants.**

$$\begin{gathered}a_0 = 1:\ \alpha + \beta = 1 \\ a_1 = 4:\ 2\alpha + 3\beta - 4 = 4 \;\Rightarrow\; 2\alpha + 3\beta = 8\end{gathered}$$

Subtracting twice the first equation: $\beta = 6$, hence $\alpha = -5$.

$$\boxed{\,a_n = 6\cdot3^{n} - 5\cdot2^{n} - n\,2^{n+1} = 6\cdot3^{n} - (5 + 2n)\,2^{n}\,}$$

*Check:* $a_2 = 5(4) - 6(1) + 4 = 18$ from the recurrence, and the formula gives $54 - 9\cdot4 = 18$ ✓; $a_3 = 5(18) - 6(4) + 8 = 74$ and $162 - 11\cdot8 = 74$ ✓.

@s 10
**Regular graph.** A graph in which **every vertex has the same degree** $k$ is called a $k$-regular graph (for example a cycle $C_n$ is 2-regular, $K_n$ is $(n-1)$-regular, the cube $Q_3$ is 3-regular). A $k$-regular graph on $n$ vertices has $nk/2$ edges.

**Graph representation techniques.** Illustrated for $K_4$ (3-regular, 4 vertices, 6 edges):

```figure caption="K4, a 3-regular graph used as the example (vertices 1-4, edges e1 = 12, e2 = 13, e3 = 14, e4 = 23, e5 = 24, e6 = 34)."
import numpy as _np
fig,ax=plt.subplots(figsize=(2.8,2.6)); ax.axis("off"); ax.set_aspect("equal")
P={1:(0,1),2:(1.6,1),3:(1.6,-0.6),4:(0,-0.6)}
for (a,b),n in zip([(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)],range(1,7)):
    ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=1.2); ax.text((P[a][0]+P[b][0])/2+0.05,(P[a][1]+P[b][1])/2+0.07,"e%d"%n,fontsize=7,color="#b00020")
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],str(k),ha="center",va="center",fontsize=9,zorder=4)
ax.set_xlim(-0.6,2.2); ax.set_ylim(-1.2,1.6)
```

**1. Adjacency matrix** $A = [a_{ij}]$, $a_{ij} = 1$ if vertices $i$ and $j$ are adjacent, else 0 ($n \times n$, symmetric for an undirected graph, diagonal zero; each row sum is the degree):

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 0 | 1 | 1 |
| 3 | 1 | 1 | 0 | 1 |
| 4 | 1 | 1 | 1 | 0 |

**2. Incidence matrix** $B = [b_{ij}]$ ($n \times m$): $b_{ij} = 1$ if vertex $i$ is an end of edge $e_j$, else 0 (each column has exactly two 1's, each row sum is the degree):

| | e1 | e2 | e3 | e4 | e5 | e6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 1 | 1 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 1 |
| 4 | 0 | 0 | 1 | 0 | 1 | 1 |

**3. Adjacency list:** each vertex with the list of its neighbours: 1: 2, 3, 4; 2: 1, 3, 4; 3: 1, 2, 4; 4: 1, 2, 3 (space $O(n + m)$, best for sparse graphs).

**4. Edge list:** the set of edges $\{(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)\}$ (compact; used in Kruskal's algorithm).

| Representation | Space | Test "is $(i,j)$ an edge?" | Best for |
|---|---|---|---|
| Adjacency matrix | $O(n^{2})$ | $O(1)$ | dense graphs |
| Incidence matrix | $O(nm)$ | $O(m)$ | edge-vertex relations |
| Adjacency list | $O(n + m)$ | $O(\deg)$ | sparse graphs, traversal |
| Edge list | $O(m)$ | $O(m)$ | sorting edges |

@s 11
**Dirac's theorem.** If $G$ is a simple graph with $n \ge 3$ vertices and the degree of **every** vertex satisfies $\deg(v) \ge n/2$, then $G$ has a Hamiltonian circuit.

**Ore's theorem.** If $G$ is a simple graph with $n \ge 3$ vertices and $\deg(u) + \deg(v) \ge n$ for **every pair of non-adjacent** vertices $u, v$, then $G$ has a Hamiltonian circuit. (Dirac's theorem is a special case of Ore's: if every degree is at least $n/2$, every pair has degree sum at least $n$.) Both are sufficient, not necessary, conditions.

**Is $K_5$ planar?** No. $K_5$ has $v = 5$ and $e = 10$. For a simple connected planar graph with $v \ge 3$, $e \le 3v - 6 = 9$. Since $10 > 9$, $K_5$ is **not planar** (it is one of the two Kuratowski graphs).

**Is $K_{3,3}$ planar?** No. $K_{3,3}$ has $v = 6$, $e = 9$ and is bipartite, so it has no triangles and every face has at least 4 edges; Euler's formula then gives $e \le 2v - 4 = 8$. Since $9 > 8$, $K_{3,3}$ is **not planar** (Kuratowski's second graph). Any graph containing a subdivision of $K_5$ or $K_{3,3}$ is non-planar.

@s 12
**Wheel $W_6$.** The wheel $W_n$ is a cycle $C_n$ (the rim) plus a hub joined to every rim vertex. Taking $W_6$ as a hub $h$ with a rim of six vertices $v_1 \ldots v_6$ gives 7 vertices and 12 edges: spokes $e_1 = hv_1, \ldots, e_6 = hv_6$ and rim edges $e_7 = v_1v_2, e_8 = v_2v_3, \ldots, e_{12} = v_6v_1$ (the hub has degree 6, each rim vertex degree 3).

```figure caption="Wheel W6: hub h joined to the six rim vertices v1 ... v6 (spokes e1-e6) and the rim cycle v1v2, v2v3, ..., v6v1 (e7-e12)."
import numpy as _np
fig,ax=plt.subplots(figsize=(3.6,3.4)); ax.axis("off"); ax.set_aspect("equal")
V={"h":(0,0)}
for i in range(6):
    a=_np.pi/2-i*_np.pi/3; V["v%d"%(i+1)]=(1.5*_np.cos(a),1.5*_np.sin(a))
ed=[("h","v%d"%i) for i in range(1,7)]+[("v%d"%i,"v%d"%(i%6+1)) for i in range(1,7)]
for n,(a,b) in enumerate(ed,1):
    ax.plot([V[a][0],V[b][0]],[V[a][1],V[b][1]],color=INK,lw=1.1)
    ax.text(0.5*(V[a][0]+V[b][0])*(1.0 if a!="h" else 1.0)+(0.12 if n>6 else 0.0)*_np.sign(V[b][0]+1e-9),0.5*(V[a][1]+V[b][1])+(0.12 if n>6 else 0.1),"e%d"%n,fontsize=6.5,color="#b00020")
for k,p in V.items(): ax.scatter([p[0]],[p[1]],s=300,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=8,zorder=4)
ax.set_xlim(-2.1,2.1); ax.set_ylim(-1.9,1.9)
```

**Incidence matrix** (rows: vertices, columns: edges; entry 1 if the vertex is an end of the edge):

| | e1 | e2 | e3 | e4 | e5 | e6 | e7 | e8 | e9 | e10 | e11 | e12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| h | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| v1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| v2 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| v3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| v4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| v5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| v6 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |

(If $W_6$ is read as a wheel with 6 vertices in total, i.e. a hub and a 5-cycle rim, the matrix is the same construction with $v_6$, $e_6$ and $e_{12}$ removed and the rim closed by $v_5v_1$.)

**Prim's algorithm** starting from vertex $a$: repeatedly add the cheapest edge joining a tree vertex to a non-tree vertex, never forming a cycle.

| Step | Tree vertices so far | Edge chosen (smallest edge leaving the tree) | Weight |
|---|---|---|---|
| 1 | {a} | a - d | 3 |
| 2 | {a, d} | b - d | 4 |
| 3 | {a, b, d} | b - c | 2 |
| 4 | {a, b, c, d} | c - g | 3 |
| 5 | {a, b, c, d, g} | g - f | 4 |
| 6 | {a, b, c, d, f, g} | d - e | 5 |

Minimum spanning tree edges: $ad\,(3),\ bd\,(4),\ bc\,(2),\ cg\,(3),\ gf\,(4),\ de\,(5)$: six edges for seven vertices, as a spanning tree needs.

$$\boxed{\,\text{Total weight} = 3 + 4 + 2 + 3 + 4 + 5 = 21\,}$$

```figure caption="Graph of Question 12 with the minimum spanning tree found by Prim's algorithm from vertex a (thick edges, total weight 21)."
import numpy as _np
E=[('a', 'b', 5), ('a', 'd', 3), ('b', 'd', 4), ('b', 'c', 2), ('b', 'e', 6), ('d', 'e', 5), ('e', 'c', 6), ('e', 'g', 6), ('c', 'g', 3), ('c', 'f', 5), ('g', 'f', 4), ('d', 'g', 6)]
M=[('a', 'd'), ('b', 'd'), ('b', 'c'), ('c', 'g'), ('g', 'f'), ('d', 'e')]
P={"a":(0,1.5),"b":(2,3),"c":(5,3.2),"d":(2,0),"e":(3.5,1.6),"f":(7,1.6),"g":(5,0)}
fig,ax=plt.subplots(figsize=(5.2,2.9)); ax.axis("off"); ax.set_aspect("equal")
for u,v,w in E:
    t=(u,v) in M or (v,u) in M
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color=ACCENT if t else "#9aa",lw=3.0 if t else 1.1,zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,str(w),fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4,color="#b00020" if t else INK)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=9,zorder=5)
ax.set_xlim(-0.6,7.6); ax.set_ylim(-0.7,3.9)
```

(The tree is unique here; starting from any other vertex gives the same total weight. Kruskal's algorithm gives the same weight: $bc\,2,\ ad\,3,\ cg\,3,\ bd\,4,\ gf\,4,\ de\,5$.)

@s 13
**Method (Ford-Fulkerson / Edmonds-Karp).** The given labels are (capacity, flow). First check that the current flow is feasible: every inner vertex satisfies conservation (for example $V_4$: in $7 + 7 = 14$, out $4 + 6 + 4 = 14$) and the current value is $11 + 10 = 21$ (also $10 + 4 + 7 = 21$ into $V_8$).

Residual capacity of an edge = capacity - flow (forward) and flow (backward, to cancel flow). Repeatedly find a path from $V_1$ to $V_8$ with positive residual capacity and push the bottleneck amount:

| Augmenting path | Bottleneck | Total flow |
|---|---|---|
| V1 → V5 → V7 → V8 | 3 | 24 |
| V1 → V2 → V3 → V6 → V8 | 2 | 26 |
| V1 → V2 → V3 → V4 → V6 → V8 | 2 | 28 |
| V1 → V5 → V7 → V4 → V6 → V8 | 1 | 29 |

Details: (1) $V_1V_5$ has residual 5, $V_5V_7$ has 4 and $V_7V_8$ has 3, so the bottleneck is 3. (2) $V_1V_2$ has residual 4 and $V_2V_3$ has 5; at $V_3$ the backward edge $V_3 \to V_6$ cancels 2 units of the flow on $V_6V_3$; then $V_6V_8$ has residual 6: push 2. (3) $V_1V_2$ residual 2, $V_2V_3$ residual 3, the backward edge $V_3 \to V_4$ cancels 2 units on $V_4V_3$, then $V_4V_6$ (residual 9) and $V_6V_8$ (residual 4): push 2. (4) $V_1V_5$ residual 2, then $V_5V_7$ has 1 left, the backward edge $V_7 \to V_4$ cancels 1 unit on $V_4V_7$, then $V_4V_6$ and $V_6V_8$: push 1. After these four augmentations no path is left (all $V_1$ edges are saturated or cut off).

**Flow on every edge after the last augmentation:**

| Edge | Capacity | Initial flow | Maximum flow |
|---|---|---|---|
| V1 → V2 | 15 | 11 | 15 |
| V1 → V5 | 15 | 10 | 14 |
| V2 → V3 | 9 | 4 | 8 |
| V2 → V4 | 7 | 7 | 7 |
| V5 → V4 | 7 | 7 | 7 |
| V4 → V3 | 5 | 4 | 2 |
| V4 → V6 | 15 | 6 | 9 |
| V4 → V7 | 5 | 4 | 3 |
| V5 → V7 | 7 | 3 | 7 |
| V6 → V3 | 4 | 2 | 0 |
| V6 → V8 | 10 | 4 | 9 |
| V6 → V7 | 4 | 0 | 0 |
| V3 → V8 | 10 | 10 | 10 |
| V7 → V8 | 10 | 7 | 10 |

**Min-cut check.** The vertices still reachable from $V_1$ in the residual graph are $S = \{V_1, V_5\}$. The edges leaving $S$ are $V_1V_2\ (15)$, $V_5V_4\ (7)$ and $V_5V_7\ (7)$, and they are all saturated:

$$\text{capacity of the cut} = 15 + 7 + 7 = 29$$

$$\boxed{\,\text{Maximum flow} = 29\,}$$

by the max-flow min-cut theorem (flow into $V_8$: $10 + 9 + 10 = 29$ ✓; out of $V_1$: $15 + 14 = 29$ ✓).

```figure caption="Maximum flow of 29 (edges drawn red are saturated; the minimum cut separates {V1, V5} from the rest)."
import numpy as _np, matplotlib.patches as mp
CAP={(1, 2): 15, (1, 5): 15, (2, 3): 9, (2, 4): 7, (5, 4): 7, (4, 3): 5, (4, 6): 15, (4, 7): 5, (5, 7): 7, (6, 3): 4, (6, 8): 10, (6, 7): 4, (3, 8): 10, (7, 8): 10}
FL={(1, 2): 15, (1, 5): 14, (2, 3): 8, (2, 4): 7, (5, 4): 7, (4, 3): 2, (4, 6): 9, (4, 7): 3, (5, 7): 7, (6, 3): 0, (6, 8): 9, (6, 7): 0, (3, 8): 10, (7, 8): 10}
P={1:(0,2.5),2:(2.4,4.7),3:(6.0,4.7),4:(2.8,2.5),5:(2.4,0.3),6:(6.0,2.5),7:(5.4,0.3),8:(8.6,2.5)}
fig,ax=plt.subplots(figsize=(6.0,3.3)); ax.axis("off"); ax.set_aspect("equal")
for (u,v),c in CAP.items():
    f=FL[(u,v)]; sat=(f==c)
    ax.annotate("",xy=P[v],xytext=P[u],arrowprops=dict(arrowstyle="-|>",color="#b00020" if sat else ACCENT,lw=1.2,shrinkA=13,shrinkB=13),zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,"(%d, %d)"%(c,f),fontsize=7,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.3),zorder=4,color="#b00020" if sat else INK)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=300,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],"V%d"%k,ha="center",va="center",fontsize=7.5,zorder=5)
ax.set_xlim(-0.8,9.4); ax.set_ylim(-0.4,5.3)
```
