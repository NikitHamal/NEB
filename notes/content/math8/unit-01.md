---
subject: Mathematics
grade: 8
unit: 1
title: Sets
hours: 0
area: Compulsory Mathematics
---

A set is a collection of things that are certainly known to belong together —
the districts of Province 1, the prime numbers below 20, the students in your
class who play football. Writing the members of a collection inside curly
brackets and giving the collection a name turns it into something a
mathematician can count, compare and reason with. This chapter reviews set
notation and then works through the ideas that the Grade 8 syllabus tests:
universal set and complement, disjoint and overlapping sets, subsets, and the
operations of union and intersection with their Venn diagrams.

::: key What this chapter asks of you
You should be able to write a set in listing and in set-builder form, find the
number of subsets of a given set, count the members of a universal set and its
complement, use the formula
$n(A\cup B)=n(A)+n(B)-n(A\cap B)$ and its rearrangement, draw and read a Venn
diagram, and solve word problems about two groups.
:::

## 1.1 Review of sets and set notation

A **set** is a well-defined collection of objects. "Well-defined" means that for
any object it is clear whether it belongs to the collection or not. The set of
districts of Nepal is well-defined; "the set of good students of a class" is not,
because "good" has not been defined.

| Way of writing | Example | When to use it |
|---|---|---|
| Listing (roster) method | $A=\{2,4,6,8\}$ | when the members are few |
| Set-builder method | $A=\{x:x$ is an even number, $x<10\}$ | when the rule is easier to state than the list |
| Description method | $A$ is the set of even numbers less than 10 | in words, at the start of a sum |

The members of a set are written inside curly brackets and separated by commas.
The symbol $\in$ means "is a member of" and $\notin$ means "is not a member of".
So if $A=\{2,4,6,8\}$, then $4\in A$ and $7\notin A$.

| Symbol | Reads as |
|---|---|
| $n(A)$ | the number of members of $A$ |
| $\cup$ | union — everything in either set |
| $\cap$ | intersection — only what is in both |
| $'$ | complement — everything outside, within the universal set |
| $\subset$ | is a subset of |
| $\emptyset$ or $\{\ \}$ | the empty set, with no members |

::: definition Equal sets and equivalent sets
Two sets are **equal** if they contain exactly the same members in any order:
$\{1,2,3\}=\{3,1,2\}$. Two sets are **equivalent** if they have the same number
of members but different members: $\{a,b,c\}$ and $\{1,2,3\}$ are equivalent
but not equal.
:::

## 1.2 Universal set and complement

When we discuss a problem we fix the largest set under consideration. This is
the **universal set**, written $U$. It contains every member that the problem
allows.

- If the problem is about the districts of Nepal, then $U$ is the set of all 77
  districts and a set of hill districts is a subset of it.
- If the problem is about whole numbers up to 20, then $U$ is the set of whole
  numbers from 0 to 20.

The **complement** of $A$, written $A'$, is the set of all members of $U$ that
are not in $A$.

$$n(U)=n(A)+n(A')$$

::: example Complement of a set
**Problem.** Let $U=\{1,2,3,4,5,6,7,8,9,10\}$ and $A=\{2,4,6,8,10\}$. Find
$A'$ and verify that $n(U)=n(A)+n(A')$.

**Solution.** $A'$ contains everything in $U$ that is not in $A$:

$$A'=\{1,3,5,7,9\}$$

Check: $n(A)=5$ and $n(A')=5$, so $n(A)+n(A')=5+5=10=n(U)$. ✓

**Note.** $A$ was the even numbers up to 10 and $A'$ the odd ones. Together they
make the whole universal set, and neither shares a member with the other.
:::

## 1.3 Disjoint and overlapping sets

Two sets are **disjoint** if they have no common member, that is
$A\cap B=\emptyset$. Two sets are **overlapping** if they share at least one
member.

- $A=\{$football players$\}$ and $B=\{$chess players$\}$ in a school are
  usually overlapping, because some students play both.
- $A=\{$even numbers$\}$ and $B=\{$odd numbers$\}$ are disjoint: no number is
  both even and odd.

```figure caption="Two sets drawn as circles. On the left they share a region, so they overlap; on the right they do not touch at all, so they are disjoint."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.5))
for ax in (ax1, ax2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
ax1.add_patch(plt.Rectangle((0.4, 0.4), 9.2, 9.2, fill=False, ec=GRID, lw=1.0))
ax1.add_patch(plt.Circle((4.1, 5.5), 2.5, fc=ACCENT, alpha=0.20, ec=ACCENT, lw=1.1))
ax1.add_patch(plt.Circle((5.9, 5.5), 2.5, fc=SERIES[1], alpha=0.20, ec=SERIES[1], lw=1.1))
ax1.text(2.9, 5.5, "A", fontsize=8, color=ACCENT)
ax1.text(7.1, 5.5, "B", fontsize=8, color=SERIES[1])
ax1.text(5.0, 2.2, "overlapping: share some members", ha="center", fontsize=6.4, color=MUTED)
ax1.text(8.9, 9.0, "U", fontsize=7.5, color=MUTED)
ax2.add_patch(plt.Rectangle((0.4, 0.4), 9.2, 9.2, fill=False, ec=GRID, lw=1.0))
ax2.add_patch(plt.Circle((3.0, 5.5), 2.2, fc=ACCENT, alpha=0.20, ec=ACCENT, lw=1.1))
ax2.add_patch(plt.Circle((7.0, 5.5), 2.2, fc=SERIES[1], alpha=0.20, ec=SERIES[1], lw=1.1))
ax2.text(3.0, 5.5, "A", fontsize=8, color=ACCENT)
ax2.text(7.0, 5.5, "B", fontsize=8, color=SERIES[1])
ax2.text(5.0, 2.2, "disjoint: no member in common", ha="center", fontsize=6.4, color=MUTED)
ax2.text(8.9, 9.0, "U", fontsize=7.5, color=MUTED)
fig.tight_layout()
```

### 1.3.1 Union and intersection

- The **union** $A\cup B$ is the set of all members that are in $A$, or in $B$,
  or in both. Counting it member by member, the shared members would be counted
  twice, so we must subtract them once:

$$n(A\cup B)=n(A)+n(B)-n(A\cap B)$$

- The **intersection** $A\cap B$ is the set of members that are in both.
- If the sets are disjoint, $n(A\cap B)=0$ and the formula becomes
  $n(A\cup B)=n(A)+n(B)$.

::: tip The three questions that solve every two-set problem
**(1)** What is $n(A)$? **(2)** What is $n(B)$? **(3)** Is the number given for
"both" or for "at least one"? If the problem gives the number who like
*both*, put it in the middle of the Venn diagram first and work outwards. If it
gives the number who like *at least one*, that is $n(A\cup B)$ and the middle
must be found from the formula.
:::

::: example Both, from the totals
**Problem.** In a class of 40 students, 25 like football and 20 like cricket.
Every student likes at least one of the two games. How many like both?

**Solution.** Here $n(A\cup B)=40$, because everyone likes at least one,
$n(A)=25$ and $n(B)=20$. From the formula:

$$n(A\cup B)=n(A)+n(B)-n(A\cap B)$$

$$40=25+20-n(A\cap B)\;\Longrightarrow\;40=45-n(A\cap B)$$

$$\text{so }n(A\cap B)=45-40=5$$

**Answer.** 5 students like both games.

**Check.** Only football $=25-5=20$; only cricket $=20-5=15$; both $=5$. Total
$=20+15+5=40$ ✓.
:::

::: example Neither, from the union
**Problem.** In a survey of 50 households, 32 grow rice and 21 grow maize; 12
grow both. How many households grow neither?

**Solution.** First find the number growing at least one crop:

$$n(A\cup B)=32+21-12=41$$

The rest grow neither:

$$n(U)-n(A\cup B)=50-41=9$$

**Answer.** 9 households grow neither.

**Check.** Only rice $=32-12=20$; only maize $=21-12=9$; both $=12$; neither
$=9$. Total $=20+9+12+9=50$ ✓.
:::

## 1.4 Subset

If every member of $A$ is also a member of $B$, then $A$ is a **subset** of $B$,
written $A\subset B$. Every set is a subset of itself, and the empty set is a
subset of every set.

The number of subsets of a set with $n$ members is $2^n$.

| $n$ | Subsets | Number $=2^n$ |
|---|---|---|
| 0 | $\emptyset$ | 1 |
| 1 | $\emptyset$, $\{a\}$ | 2 |
| 2 | $\emptyset$, $\{a\}$, $\{b\}$, $\{a,b\}$ | 4 |
| 3 | 8 subsets, including the set itself | 8 |

Of these, the set itself is not a **proper** subset, so a set with $n$ members
has $2^n-1$ proper subsets when $n\ge1$.

::: caution "B contains A" and "B belongs to A" are different
$A\subset B$ means every member of $A$ is also a member of $B$. The symbol
$\in$ asks about a single object: $3\in\{1,2,3\}$. Mixing the two up is the
commonest error in set questions — a set cannot "belong to" another set unless
it is listed as one of the members.
:::

::: example Number of subsets
**Problem.** A set $A$ has 4 members. Find the number of subsets, the number of
proper subsets, and the number of subsets that contain at least three members.

**Solution.** Number of subsets $=2^4=16$. Proper subsets $=16-1=15$.

To contain at least three members, a subset has 3 or 4 members:
$\binom{4}{3}+\binom{4}{4}=4+1=5$.

**Answer.** 16 subsets, 15 proper subsets, 5 with at least three members.

**Check.** The subsets with fewer than three members number
$\binom{4}{0}+\binom{4}{1}+\binom{4}{2}=1+4+6=11$, and $11+5=16$ ✓.
:::

## 1.5 Word problems with a Venn diagram

The method is always the same.

1. Draw a rectangle for $U$ and two circles for the two sets.
2. Put the number who belong to **both** in the middle region first.
3. Subtract to find the rest of each circle.
4. Find the number outside both by subtraction from $n(U)$.
5. Add up all the regions and check against $n(U)$.

::: example A full survey problem
**Problem.** In a ward of 120 families, 70 use LPG, 55 use firewood and 30 use
both. Find (a) the number using at least one fuel, (b) the number using only
LPG, (c) the number using neither, and (d) the number using firewood but not
LPG.

**Solution.** Let $L$ be the families using LPG and $W$ those using firewood.
$n(L)=70$, $n(W)=55$, $n(L\cap W)=30$, $n(U)=120$.

(a) $n(L\cup W)=70+55-30=95$.

(b) Only LPG $=70-30=40$.

(c) Neither $=120-95=25$.

(d) Firewood but not LPG $=55-30=25$.

**Check.** $40+30+25+25=120$ ✓, which is the whole universal set.

**Note.** Part (d) is a good trap: it asks for firewood only, not for
firewood. Reading which region the question wants is worth more marks than the
arithmetic.
:::

## 1.6 Venn diagrams as a method, not a decoration

A Venn diagram is not an illustration drawn after the answer; it is the
fastest way **to** the answer. Fill the overlap first, then work outwards.

```figure caption="The order of filling a two-set Venn diagram: the intersection first, then each 'only' region, then whatever is left outside."
fig, ax = flow([("Both", "fill n(A∩B)"), ("Only A", "n(A) − n(A∩B)"),
                ("Only B", "n(B) − n(A∩B)"), ("Neither", "total − union")],
               note="filling any other order means guessing")
```

| Phrase in the question | Region it means |
|---|---|
| both / and | $A \cap B$ |
| at least one / either | $A \cup B$ |
| only A | $n(A) - n(A \cap B)$ |
| neither | total $- n(A \cup B)$ |
| exactly one | $n(A \cup B) - n(A \cap B)$ |

::: example A full four-mark set question
**Question.** In a class of 60 students, 38 play football, 29 play
volleyball and 12 play neither. Find (i) how many play at least one game
(ii) how many play both (iii) how many play only football.

**Answer.**
(i) At least one $= 60 - 12 = \textbf{48}$.
(ii) $n(F \cup V) = n(F) + n(V) - n(F \cap V)$, so
$48 = 38 + 29 - n(F \cap V)$, giving $n(F \cap V) = 67 - 48 = \textbf{19}$.
(iii) Only football $= 38 - 19 = \textbf{19}$.
**Check:** $19 + 19 + 10 + 12 = 60$ ✓ (only football, both, only volleyball,
neither).
:::

::: note Activity — the class survey
Ask every student in the class two yes/no questions (for example: *Do you
walk to school?* and *Do you have a kitchen garden at home?*). Fill a Venn
diagram with the four regions and check that the four numbers add up to the
class size. Then write three questions about your own diagram, of the
"only", "both" and "neither" kind, and swap them with a partner.
:::

## Chapter summary

- A set is a well-defined collection; it is written by the listing method or the
  set-builder method.
- $n(A)$ is the number of members; $\in$ and $\notin$ test membership.
- The universal set $U$ is the largest set in the problem, and $A'$ is
  everything in $U$ that is not in $A$; $n(U)=n(A)+n(A')$.
- Disjoint sets have no common member, so $n(A\cap B)=0$; overlapping sets share
  at least one.
- $n(A\cup B)=n(A)+n(B)-n(A\cap B)$, and $n(A\cap B)=n(A)+n(B)-n(A\cup B)$.
- A set with $n$ members has $2^n$ subsets and $2^n-1$ proper subsets.
- In a Venn diagram, fill the intersection first and work outwards, then check
  that all the regions add up to $n(U)$.

## Practice questions

**Group A — Objective (1 mark each)**

1. If $A=\{1,2,3\}$, then $n(A)$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 6 (d) 8
2. The number of subsets of a set with 3 members is
   <span class="marks">[1]</span>
   (a) 3 (b) 6 (c) 8 (d) 9
3. If $n(A)=20$, $n(B)=15$ and $n(A\cap B)=5$, then $n(A\cup B)$ is
   <span class="marks">[1]</span>
   (a) 40 (b) 35 (c) 30 (d) 25
4. Which of these is the empty set? <span class="marks">[1]</span>
   (a) $\{$odd numbers divisible by 2$\}$ (b) $\{0\}$
   (c) $\{$prime numbers$\}$ (d) $\{$even numbers$\}$
5. If $A$ and $B$ are disjoint, then $A\cap B$ is
   <span class="marks">[1]</span>
   (a) $A$ (b) $B$ (c) $\emptyset$ (d) $U$
6. If $n(U)=50$ and $n(A)=32$, then $n(A')$ is
   <span class="marks">[1]</span>
   (a) 18 (b) 82 (c) 32 (d) 50

::: note Answers to Group A
**1.** (b) — three members.
**2.** (c) — $2^3=8$.
**3.** (c) — $20+15-5=30$.
**4.** (a) — no odd number is divisible by 2, so the set has no members.
**5.** (c) — disjoint sets have no common member.
**6.** (a) — $50-32=18$.
:::

**Group B — Short answer (2 marks each)**

1. Write $A=\{2,4,6,8,10\}$ in set-builder form and find $n(A)$.
   <span class="marks">[2]</span>
2. If $U=\{1,2,3,\dots,12\}$ and $A=\{3,6,9,12\}$, find $A'$.
   <span class="marks">[2]</span>
3. Find the number of proper subsets of a set with 5 members.
   <span class="marks">[2]</span>
4. If $n(A)=18$, $n(B)=24$ and $n(A\cup B)=36$, find $n(A\cap B)$.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $A=\{x:x$ is an even number and $2\le x\le10\}$, and $n(A)=5$.
**2.** $A'=\{1,2,4,5,7,8,10,11\}$ — everything in $U$ except the multiples of 3.
**3.** $2^5-1=32-1=31$.
**4.** $n(A\cap B)=18+24-36=6$.
:::

**Group C — Long answer (4 marks each)**

1. In a class of 45 students, 28 take mathematics, 22 take science and 10 take
   both. Find (a) how many take at least one of the two, (b) how many take
   neither, and (c) how many take mathematics only. Draw a Venn diagram and
   check your answer. <span class="marks">[4]</span>
2. In a survey of 200 people, 120 read a newspaper, 90 listen to the radio and
   40 do both. Find the number who do neither, and the number who use exactly
   one of the two. Show the working. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) $n(M\cup S)=28+22-10=40$. (b) Neither $=45-40=5$.
(c) Mathematics only $=28-10=18$. **Venn diagram.** A rectangle for 45 holding
two overlapping circles; write 10 in the overlap, 18 in the mathematics-only
region, 12 in the science-only region, and 5 outside both circles but inside the
rectangle. **Check.** $18+10+12+5=45$ ✓.
**2.** (a) $n(N\cup R)=120+90-40=170$, so neither $=200-170=30$.
(b) Only newspaper $=120-40=80$; only radio $=90-40=50$; exactly one
$=80+50=130$. **Check.** $80+40+50+30=200$ ✓.
:::

**Extra practice**

**Group B (2 marks)**

14. If $n(A) = 24$, $n(B) = 18$ and $n(A \cup B) = 35$, find $n(A \cap B)$.
15. Write in set notation: *students who play neither game*.

**Group C (4 marks)**

16. Of 80 households, 52 keep goats, 41 keep poultry and 9 keep neither. Find
    how many keep both, and how many keep goats only.

::: note Extra practice — answers
**14.** $n(A \cap B) = 24 + 18 - 35 = 7$.
**15.** $(A \cup B)'$ — the complement of the union.
**16.** At least one $= 80 - 9 = 71$. Both $= 52 + 41 - 71 = 22$.
Goats only $= 52 - 22 = 30$. (Check: $30 + 22 + 19 + 9 = 80$.)
:::
