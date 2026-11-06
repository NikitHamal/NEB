---
subject: Mental Agility Test
grade: CEE
unit: 1
title: Verbal Reasoning
hours: 5
area: Mental Agility Test
---

Verbal reasoning is the first block of the Mental Agility Test: **5 of the 20 MAT
questions**, each worth one mark, with 0.25 deducted for a wrong answer. The questions
are short puzzles written in words — a walk with turns, a family relation, a coded
word, a pair of related words, a queue or a table of people, a pair of statements. None
needs any fact from outside the question. Each type has a fixed method, and once you
draw the right picture (a path, a family tree, a row, a circle, a Venn diagram) most
questions take under a minute. The official MEC sample question for this block is a
direction walk, so that type opens the chapter.

::: key What the paper asks from this chapter
- **Direction sense**: a right turn is a quarter-turn clockwise, a left turn a
  quarter-turn anticlockwise; add up the east–west and north–south legs separately,
  then use Pythagoras (3-4-5, 5-12-13, 6-8-10) for the straight-line distance.
- **Shadows**: in the morning the sun is in the east, so shadows fall to the west; in
  the evening they fall to the east.
- **Blood relations**: draw a family tree; never assume a person's gender from a
  name or a letter.
- **Coding**: letter positions A = 1 … Z = 26 (learn E J O T Y = 5, 10, 15, 20, 25);
  opposite letters add to 27 (A↔Z, M↔N).
- **Analogy and odd one out**: say the relation of the first pair as a sentence and
  apply exactly that sentence to the second pair.
- **Ranking**: total = rank from one end + rank from the other end − 1.
- **Seating**: around a table, people facing the centre have their *left* in the
  clockwise direction.
- **Syllogisms**: draw the smallest Venn diagram the statements allow; a conclusion
  follows only if it is true in *every* diagram the statements allow.
:::

## 1.1 Direction sense and distance

### The compass and the turns

There are four main directions — north (N), east (E), south (S), west (W) — and four
in-between ones: north-east (NE), south-east (SE), south-west (SW) and north-west (NW).
On paper, north is up and east is to the right.

| You face | After a right turn | After a left turn | After an about-turn |
|---|---|---|---|
| North | East | West | South |
| East | South | North | West |
| South | West | East | North |
| West | North | South | East |

A **right turn** is 90° clockwise; a **left turn** is 90° anticlockwise. A turn of 45°
takes you from a main direction to the in-between one next to it (N → NE for 45°
clockwise).

```figure caption="Left: the eight directions; a right turn is a quarter-turn clockwise. Right: the MEC sample walk — 30 km north, right 20 km, right 30 km — ends 20 km east of the start."
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.9), gridspec_kw=dict(width_ratios=[1, 1.08]))
for ang, lab in [(90,'N'),(45,'NE'),(0,'E'),(-45,'SE'),(-90,'S'),(-135,'SW'),(180,'W'),(135,'NW')]:
    main = len(lab) == 1
    r = 1.0 if main else 0.72
    c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    a1.annotate('', xy=(r*c, r*s), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color=INK if main else MUTED, lw=1.3 if main else 0.9))
    a1.text((r+0.2)*c, (r+0.2)*s, lab, ha='center', va='center',
            fontsize=10 if main else 8.5, color=INK if main else MUTED,
            fontweight='bold' if main else 'normal')
th = np.linspace(np.radians(84), np.radians(8), 50)
a1.plot(0.42*np.cos(th), 0.42*np.sin(th), color=SERIES[1], lw=1.6)
a1.annotate('', xy=(0.42*np.cos(th[-1]), 0.42*np.sin(th[-1])),
            xytext=(0.42*np.cos(th[-4]), 0.42*np.sin(th[-4])),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6))
a1.text(0, -1.55, 'right turn = 90° clockwise\nleft turn = 90° anticlockwise',
        ha='center', va='center', fontsize=8.5, color=SERIES[1])
a1.set_xlim(-1.45, 1.45); a1.set_ylim(-1.9, 1.35); a1.set_aspect('equal'); a1.axis('off')
pts = [(0, 0), (0, 30), (20, 30), (20, 0)]
for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
    a2.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, shrinkA=0, shrinkB=0))
a2.plot([0, 20], [0, 0], ls='--', color=SERIES[2], lw=1.6)
a2.text(10, -2.6, '20 km east', ha='center', va='top', fontsize=8.8, color=SERIES[2], fontweight='bold')
a2.text(-1.5, 15, '30 km\nnorth', ha='right', va='center', fontsize=8.5)
a2.text(10, 31.5, '20 km (right turn: now east)', ha='center', va='bottom', fontsize=8.2)
a2.text(21.5, 15, '30 km\nsouth', ha='left', va='center', fontsize=8.5)
a2.plot([0], [0], 'o', color=INK, ms=4.5); a2.plot([20], [0], 'o', color=SERIES[1], ms=4.5)
a2.text(-1.2, -1.2, 'start', ha='right', va='top', fontsize=8.5)
a2.text(21.2, -1.2, 'end', ha='left', va='top', fontsize=8.5, color=SERIES[1])
a2.set_xlim(-12, 33); a2.set_ylim(-8, 38); a2.set_aspect('equal'); a2.axis('off')
fig.tight_layout()
```

### The method (works for every walk)

1. Put the start at the origin. East is +x, north is +y.
2. Track the **facing direction** after every turn (use the table above).
3. Add each leg to the running totals: net east (x) and net north (y). Opposite legs
   cancel — 30 km north and then 30 km south is zero.
4. Distance from the start $= \sqrt{x^2 + y^2}$. If one of x, y is zero, the distance
   is simply the other one.
5. Direction from the start: read the signs. x > 0, y > 0 is north-east; x > 0, y = 0
   is due east; x < 0, y < 0 is south-west, and so on.

**Fast trick.** Most walks are built on Pythagorean triples: 3-4-5, 6-8-10, 5-12-13,
8-15-17, 9-12-15, 12-16-20. When you see two net legs like 12 and 5, the answer 13 is
already among the options.

::: example The MEC sample question
**Problem.** Rita goes 30 km towards north from a fixed point, then after turning to
her right she goes 20 km. After this she goes 30 km after turning to her right. How far
and in what direction is she from her starting point?

**Solution.** Facing north, 30 km: y = 30. Right turn → facing east, 20 km: x = 20.
Right turn → facing south, 30 km: y = 30 − 30 = 0. Net displacement: 20 km east,
0 km north. She is **20 km east** of the start (key C in the official sample).
:::

::: example A 3-4-5 walk
**Problem.** Dinesh walks 6 km east, turns left and walks 4 km, then turns left again
and walks 9 km. Where is he now with respect to his starting point?

**Solution.** East 6 → x = 6. Left of east is north: y = 4. Left of north is west,
9 km: x = 6 − 9 = −3. Net: 3 km west, 4 km north. Distance $\sqrt{3^2 + 4^2}$ = 5 km;
x < 0 and y > 0, so he is **5 km north-west** of the start.
:::

### Shadows

The sun rises in the east and sets in the west, and a shadow always points **away
from the sun**:

| Time | Sun in the | Shadow falls towards the |
|---|---|---|
| Morning (after sunrise) | east | west |
| Evening (before sunset) | west | east |

(Nepal lies north of the Tropic of Cancer, so at noon the sun is due south and a
shadow points north — but noon shadows are rarely asked.)

::: example Two people and one shadow
**Problem.** One morning Ram and Shyam stood face to face. Ram's shadow fell exactly
to his right. Which direction was Shyam facing?

**Solution.** Morning → shadows fall to the west. Ram's right hand points west, so Ram
faces **south** (facing south, your right is west). Shyam faces Ram, so Shyam faces
**north**.
:::

::: caution Three traps examiners set
- "Which direction is he **facing**?" and "In which direction is he **from the start**?"
  are different questions. Rita (above) ends 20 km east of the start but is *facing*
  south.
- "Where is the **start** from him?" is the reverse direction: if he is south-east of
  the start, the start is north-west of him.
- In rotated-compass questions ("if south-east becomes north…"), every direction turns
  through the *same* angle and the same way. SE → N is 135° anticlockwise, so W → SE.
:::

```photogrid label="1.1" cols="2" ratio="1.2" caption="Direction sense is geometry. (a) A magnetic compass: the red end of the needle points to magnetic north and the card is read in eight principal directions 45 degrees apart (N, NE, E, SE, S, SW, W, NW). (b) A walk of 15 km north, 12 km east and 6 km south ends 12 km east and 15 - 6 = 9 km north of the start, so the shortest distance is the hypotenuse of a 12-9 right triangle: d = sqrt(12^2 + 9^2) = 15 km, on a bearing of 53 degrees east of north (N 53 E). The path actually walked is 15 + 12 + 6 = 33 km, so always separate the distance travelled from the displacement. Draw the path, mark the end point, and join it to the start before you answer."
@ photo id="ceemat/compass" cap="A magnetic compass with the card marked in degrees"
fit 1.2
focus 0.5 0.5
@ svg cap="Walk 15 N, 12 E, 6 S: net displacement"
import math
legs = (("N", 15), ("E", 12), ("S", 6))
x = y = 0
for d, k in legs:
    if d == "N": y += k
    elif d == "E": x += k
    else: y -= k
dist = math.hypot(x, y)
walked = sum(k for _, k in legs)
brg = math.degrees(math.atan2(x, y))
assert (x, y) == (12, 9) and abs(dist - 15) < 1e-9 and walked == 33 and round(brg) == 53
f = Fig(300, 236)
f.text(150, 12, "Walk 15 km N, 12 km E, 6 km S", size=10.5, color=NAVY, bold=True)
s = 9; ox, oy = 62, 188
P = lambda a, b: (ox + a * s, oy - b * s)
O, A, B, C = P(0, 0), P(0, 15), P(12, 15), P(12, 9)
f.arrow([O, A], color=NAVY, sw=2)
f.arrow([A, B], color=NAVY, sw=2)
f.arrow([B, C], color=NAVY, sw=2)
f.arrow([O, C], color=RED, sw=2, dash=True)
f.circle(O[0], O[1], 4, fill=MINT, stroke=TEAL)
f.text(ox - 8, oy + 2, "Start", size=10.5, color=TEAL, bold=True, anchor="end")
f.text(ox - 8, 122, "15 km N", size=10.5, color=NAVY, bold=True, anchor="end")
f.text(116, 46, "12 km E", size=10.5, color=NAVY, bold=True)
f.text(C[0] + 8, 82, "6 km S", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(C[0] + 8, C[1] + 4, "End", size=10.5, color=RED, bold=True, anchor="start")
f.text(136, 178, "d = 15 km", size=10.5, color=RED, bold=True)
f.arrow([(268, 62), (268, 34)], color=SLATE, sw=2)
f.text(268, 26, "N", size=10.5, color=SLATE, bold=True)
f.text(150, 206, "Net: 12 east, 9 north, so d = 15 km, N 53 E", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "path walked = 33 km (not the distance)", size=10.5, color=SLATE, bold=True)
```

## 1.2 Blood relations

### The vocabulary

| Relation | Means | Nepali term |
|---|---|---|
| Paternal grandfather / grandmother | father's father / father's mother | हजुरबुबा / हजुरआमा |
| Maternal uncle | mother's brother | मामा |
| Paternal aunt | father's sister | फुपू |
| Uncle (father's brother) | elder / younger brother of father | ठूलोबुबा / काका |
| Nephew / niece | son / daughter of your brother or sister | भतिजा, भान्जा / भतिजी, भान्जी |
| Cousin | child of your uncle or aunt | — |
| Brother-in-law | spouse's brother, or sister's husband | — |
| Sister-in-law | spouse's sister, or brother's wife | — |
| Son-in-law / daughter-in-law | daughter's husband / son's wife | ज्वाइँ / बुहारी |

Two phrases decide many questions:

- **"The only son of my father"** — if the speaker is male, that son is the speaker
  himself. **"The only daughter of my mother"**, said by a woman, is the speaker herself.
- **"The only son of my father's father"** is the speaker's own father.

### The method: draw the tree

Use one symbol for each person: a **square for a male**, a **circle for a female**,
and a plain label when the gender is not known. A double line joins a married couple;
a vertical line goes down one generation; a horizontal line joins brothers and sisters.
Read each sentence once, add it to the drawing, and answer from the drawing — never in
your head.

```figure caption="Family tree for the worked example. Squares are males, circles females; the double line is a marriage, vertical lines go down one generation, the horizontal bar joins brothers and sisters."
fig, ax = plt.subplots(figsize=(4.6, 2.9))
def male(x, y, t):
    ax.add_patch(Rectangle((x-0.32, y-0.32), 0.64, 0.64, fc='#dbe8f6', ec=ACCENT, lw=1.3))
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold')
def female(x, y, t):
    ax.add_patch(Circle((x, y), 0.34, fc='#f8dede', ec=SERIES[1], lw=1.3))
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold')
female(3.0, 4.0, 'M')
ax.plot([3.0, 3.0], [3.66, 3.05], color=INK, lw=1.1)
ax.plot([1.5, 4.5], [3.05, 3.05], color=INK, lw=1.1)
ax.plot([1.5, 1.5], [3.05, 2.34], color=INK, lw=1.1)
ax.plot([4.5, 4.5], [3.05, 2.32], color=INK, lw=1.1)
female(1.5, 2.0, 'N'); male(0.0, 2.0, 'Q'); male(4.5, 2.0, 'P')
ax.plot([0.32, 1.16], [2.06, 2.06], color=INK, lw=1.1)
ax.plot([0.32, 1.16], [1.94, 1.94], color=INK, lw=1.1)
ax.plot([0.75, 0.75], [1.94, 0.34], color=INK, lw=1.1)
male(0.75, 0.0, 'R')
ax.plot([4.5, 4.5], [1.68, 0.34], color=INK, lw=1.1)
female(4.5, 0.0, 'S')
ax.text(3.5, 4.0, 'mother of N and P', va='center', fontsize=8.3, color=MUTED)
ax.text(5.0, 2.0, 'man; N\'s brother', va='center', fontsize=8.3, color=MUTED)
ax.text(1.2, 0.0, 'son of Q and N', va='center', fontsize=8.3, color=MUTED)
ax.text(5.0, 0.0, 'daughter of P', va='center', fontsize=8.3, color=MUTED)
ax.text(-0.45, 2.0, 'N\'s\nhusband', ha='right', va='center', fontsize=8.3, color=MUTED)
ax.set_xlim(-1.9, 7.4); ax.set_ylim(-0.55, 4.5); ax.set_aspect('equal'); ax.axis('off')
```

::: example Reading a tree
**Problem.** M is the mother of N and P. N is married to Q. R is the son of N and Q,
and S is the daughter of P. Q is the father of R, and P is a man. How is P related to R,
and how is S related to R?

**Solution.** Draw it (figure above). N is R's mother, and P is N's brother, so P is
R's **mother's brother — maternal uncle** (mama). S is the daughter of R's maternal
uncle, so S is R's **cousin**.
:::

### Coded relations

Some questions code the relations with symbols. Translate each symbol into words,
left to right, then draw.

::: example A coded relation
**Problem.** A + B means "A is the brother of B", A − B means "A is the sister of B"
and A × B means "A is the father of B". What does M − N × O mean?

**Solution.** M − N: M is the sister of N. N × O: N is the father of O. So M is the
sister of O's father: M is O's **paternal aunt** (phupu).
:::

::: caution Gender is never assumed
"A is the child of B" does not say whether A is a son or a daughter, and "P is the
parent of Q" does not say father or mother. If an option needs the gender and the
question does not fix it, the answer is "cannot be determined" or a word without gender
(child, sibling, cousin). Names do not settle it either unless the question uses *he*
or *she*.
:::

## 1.3 Coding and decoding

### Letter positions — learn them cold

| Letter | A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| Reverse position | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 14 |

| Letter | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Position | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| Reverse position | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |

::: memory EJOTY and the 27 rule
**E J O T Y** = 5, 10, 15, 20, 25. From these anchors any letter is one or two steps
away: R = T − 2 = 18. **Opposite letters add to 27**: A↔Z, B↔Y, C↔X, D↔W, E↔V, F↔U,
G↔T, H↔S, I↔R, J↔Q, K↔P, L↔O, M↔N. The opposite of a letter at position p is at 27 − p.
:::

### The common code types

| Type | What happens | Example |
|---|---|---|
| Shift | every letter moves the same number of places | COLD → DPME (+1) |
| Changing shift | the shift grows: +1, +2, +3 … | ABC → BDF |
| Opposite letter | each letter replaced by its partner (sum 27) | GOD → TLW |
| Reversal | the word is written backwards | PAPER → REPAP |
| Pair swap | letters swapped in pairs | MOTHER → OMHTRE |
| Letter to number | sum (or product) of the positions | CAT → 3 + 1 + 20 = 24 |
| Letter to digit | each letter has a fixed digit | ROSE → 6821 |
| Substitution | one word is "called" another | sky is called sea … |
| Sentence code | words of sentences coded as code words | "pit na sor" = "drink clean water" |

**Method.** Write the word and its code one above the other, letter by letter, and
write the position change under each pair (+1, +1, +1 … or 26 − … ). The pattern shows
itself at once. Then apply the *same* rule to the new word.

::: example Shift code
**Problem.** If GREEN is coded HSFFO, how is BLACK coded?

**Solution.** G→H, R→S, E→F, E→F, N→O: every letter +1. B→C, L→M, A→B, C→D, K→L, so
BLACK is **CMBDL**.
:::

::: example Sentence code: the common-word method
**Problem.** In a code language, "ka la ta" means "eat green vegetables", "pa ka ma"
means "eat ripe fruit" and "ta sa pa" means "green fruit juice". What is the code for
"ripe"?

**Solution.** A word common to two sentences has its code common to the same two
sentences. Sentences 1 and 2 share *eat* and *ka*: eat = ka. Sentences 1 and 3 share
*green* and *ta*: green = ta. Sentences 2 and 3 share *fruit* and *pa*: fruit = pa.
Sentence 2 is "pa ka ma" = "eat ripe fruit", so **ripe = ma**.
:::

::: caution Substitution questions
In "sky is called sea, sea is called water, water is called air…", the question asks
for the *code name* of the real thing. We drink water, and water is called **air** —
the answer is "air", not "water".
:::

```photogrid label="1.2" cols="2" ratio="1.2" caption="Coding is a rule applied letter by letter. (a) A cipher disc: two concentric alphabets, the inner one turned to choose a shift. (b) Two standard codes for the word NEPAL. A shift code moves each letter the same number of places along the alphabet: +3 gives N-Q, E-H, P-S, A-D, L-O, so NEPAL becomes QHSDO, and the same rule backwards (-3) decodes it. An opposite-letter code pairs A with Z, B with Y and so on: the positions of a letter and its partner always add up to 27 (N is 14 and M is 13), so NEPAL becomes MVKZO. Find the rule on the first letter, test it on the second, and only then apply it to the answer word."
@ photo id="ceemat/cipher" cap="A substitution cipher disc"
fit 1.2
focus 0.5 0.5
@ svg cap="NEPAL under a +3 shift and the opposite-letter code"
import string
A = string.ascii_uppercase
word = "NEPAL"
sh = lambda c, k: A[(A.index(c) + k) % 26]
opp = lambda c: A[25 - A.index(c)]
r2 = "".join(sh(c, 3) for c in word)
r3 = "".join(opp(c) for c in word)
assert r2 == "QHSDO" and r3 == "MVKZO"
assert "".join(sh(c, -3) for c in r2) == word
assert all((A.index(c) + 1) + (A.index(opp(c)) + 1) == 27 for c in word)
f = Fig(300, 236)
f.text(150, 12, "Two codes for NEPAL", size=10.5, color=NAVY, bold=True)
rows = (("Plain", word, MINT, TEAL), ("Shift +3", r2, BLUE, NAVY), ("Opposite", r3, SAND, AMBER))
for j, (nm, w, fl, st) in enumerate(rows):
    y = 30 + j * 54
    f.text(8, y + 14, nm, size=10.5, color=st, bold=True, anchor="start", vmid=True)
    for i, c in enumerate(w):
        f.box(86 + i * 42, y, 34, 28, c, fill=fl, stroke=st, size=13, bold=True)
for i in range(5):
    cx = 103 + i * 42
    f.arrow([(cx, 60), (cx, 82)], color=NAVY, sw=1.5)
f.text(150, 186, "N (14) + M (13) = 27, always", size=10.5, color=AMBER, bold=True)
f.text(150, 206, "decode a shift code by shifting back (-3)", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "only 25 shifts exist: Caesar used +3", size=10.5, color=SLATE, bold=True)
```

## 1.4 Analogy and classification (odd one out)

### Analogy

An analogy A : B :: C : ? says "C is related to the answer in the same way that A is
related to B". Put the first relation into a short sentence — "a doctor uses a
stethoscope", "a nephrologist treats the kidney" — and test each option in exactly that
sentence. Only one option fits as precisely.

| Relation | Example pair |
|---|---|
| worker : tool | carpenter : saw, surgeon : scalpel, mason : trowel |
| specialist : organ | cardiologist : heart, nephrologist : kidney, ophthalmologist : eye |
| instrument : quantity measured | thermometer : temperature, barometer : atmospheric pressure, hygrometer : humidity, ammeter : current |
| unit : quantity | ohm : resistance, pascal : pressure, joule : energy |
| cause : effect | virus : infection, drought : famine |
| part : whole | petal : flower, chapter : book |
| animal : young one | cow : calf, frog : tadpole, horse : foal |
| animal : home | bee : hive, horse : stable, spider : web |
| country : capital | Nepal : Kathmandu, Bhutan : Thimphu |
| word : synonym / antonym | brave : bold, ancient : modern |
| number rule | 3 : 27 (cube), 6 : 35 ($n^2 - 1$), 7 : 50 ($n^2 + 1$) |
| letter rule | ACE : BDF (each +1) |

For numbers, test in this order: square, cube, $n^2 \pm 1$, $n^3 \pm 1$, $n(n+1)$,
double, double plus one. For letters, write the positions.

::: example Number analogy
**Problem.** 6 : 35 :: 8 : ?

**Solution.** 35 = 5 × 7 = (6 − 1)(6 + 1) = $6^2 - 1$. So the answer is
$8^2 - 1$ = 7 × 9 = **63**.
:::

### Classification (odd one out)

Three items share a property; the fourth does not. Find the property that splits
**exactly three from one**.

| Items | Usual sorting properties |
|---|---|
| Words | category (organ, instrument, metal, planet), function, living / non-living |
| Numbers | prime, even/odd, perfect square, perfect cube, $n^2 \pm 1$, $n^3 \pm 1$, digit sum, divisible by 7 or 11 |
| Letter groups | gaps between the letters, vowels, opposite-letter pairs, positions |

::: tip When two properties seem to work
If one property splits the items 3 : 1 and another splits them 2 : 2, the 3 : 1 split
is the answer. If two different properties each give a 3 : 1 split with a different
odd item, prefer the more specific one (perfect cube beats odd number), and re-read the
options: the setter usually intends only one.
:::

## 1.5 Ranking, ordering and seating arrangement

### Ranking in a row or a class

If a person is $L$-th from the left (or top) and $R$-th from the right (or bottom) in
a row of $N$ people:

$$ N = L + R - 1 $$

and the rank from the other end is $N - L + 1$. The 1 is subtracted because the person
is counted from both ends.

::: example Two people in one row
**Problem.** In a row of 45 children, Rina is 17th from the left and Hari is 20th from
the right. How many children sit between them?

**Solution.** Hari from the left = 45 − 20 + 1 = 26th. Between 17th and 26th there are
26 − 17 − 1 = **8** children.
:::

When two people **exchange places**, the new rank of one of them equals the old rank of
the other — this links the two ends of the row (Set C, question 8).

### Ordering by comparison

"P is taller than Q but shorter than R" gives a chain Q < P < R. Write every clue as a
chain with < signs and join the chains. Who is tallest, who is in the middle, and who is
second from the top can then be read off directly. If two people are never compared,
their order is unknown — and "cannot be determined" becomes a live option.

### Seating in a row

People in a row usually face north (towards you, the reader, they face away from you).
For a person facing north, **left is west and right is east**: their left and right are
the same as yours. If they face south, their left and right are the reverse of yours.

### Seating around a table

For people seated round a table **facing the centre**, **left = clockwise** and
**right = anticlockwise** (picture yourself at the bottom of the table, facing up: your
left hand points to the next seat clockwise). If everyone faces outwards, both are
reversed. "Second to the left of X" means two seats clockwise from X.

```figure caption="Six people round a table, all facing the centre (small arrows). For each of them the next seat clockwise is on their left. This is the solved arrangement of the worked example."
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax.add_patch(Circle((0, 0), 0.62, fc='#eef2f7', ec=MUTED, lw=1.0))
ax.text(0, 0, 'table', ha='center', va='center', fontsize=8.5, color=MUTED)
names = ['P', 'Q', 'R', 'T', 'S', 'U']
for k, nm in enumerate(names):
    a = np.radians(270 - 60*k)
    x, y = 1.12*np.cos(a), 1.12*np.sin(a)
    ax.add_patch(Circle((x, y), 0.2, fc='white', ec=INK, lw=1.2))
    ax.text(x, y, nm, ha='center', va='center', fontsize=10, fontweight='bold')
    ax.annotate('', xy=(0.74*np.cos(a), 0.74*np.sin(a)), xytext=(0.90*np.cos(a), 0.90*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0))
th = np.linspace(np.radians(205), np.radians(110), 60)
ax.plot(1.62*np.cos(th), 1.62*np.sin(th), color=SERIES[1], lw=1.6)
ax.annotate('', xy=(1.62*np.cos(th[-1]), 1.62*np.sin(th[-1])),
            xytext=(1.62*np.cos(th[-4]), 1.62*np.sin(th[-4])),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6))
ax.text(-1.95, 0.95, 'clockwise\n= to the LEFT\nof each person', ha='right', va='center',
        fontsize=8.5, color=SERIES[1])
ax.text(1.75, -0.55, 'Q is opposite S\nP is right of Q\nR is 2nd left of P', ha='left',
        va='center', fontsize=8.2, color=MUTED)
ax.set_xlim(-3.2, 3.3); ax.set_ylim(-1.55, 1.95); ax.set_aspect('equal'); ax.axis('off')
```

::: example Circular seating
**Problem.** P, Q, R, S, T and U sit round a table facing the centre. Q sits opposite
S. P is to the immediate right of Q. R is second to the left of P. T is not to the
immediate left of S. Who sits opposite P?

**Solution.** Fix P at the bottom. Q is to the left of P (P is on Q's right), so Q is
the next seat clockwise from P. R is two seats clockwise from P — next to Q. S is
opposite Q, three seats on from Q. Two seats remain: the one between R and S, and the
one between S and P. The seat between S and P is S's immediate left, so T cannot sit
there: T sits between R and S, and U between S and P. Clockwise from P: P, Q, R, T, S,
U. Opposite P is **T**.
:::

::: tip Start from the fixed clue
Begin with the clue that pins a person to a seat (an end of the row, "opposite", "at
the extreme left"), then add the "immediate" clues, and leave the "not" clues to the
end — they only decide between the cases left over.
:::

```photogrid label="1.3" cols="2" ratio="1.2" caption="Seating problems are counting problems. (a) Delegates in a row at a conference table. (b) n people can be seated in a row in n! ways but around a circle in only (n - 1)! ways, because turning everyone one seat round gives the same circle (the bars use a log scale). For five people the cell enumerates every case: 120 arrangements in a row, 24 in a circle, and 2 x 4! = 48 in a row when two named people must sit together (glue them into one block, arrange the 4 units, then swap the pair). Constraints such as 'A is next to B' or 'C sits opposite D' cut these totals down, which is why a careful diagram beats trial and error."
@ photo id="ceemat/roundtable" cap="Delegates seated along a conference table"
fit 1.2
focus 0.45 0.5
@ svg cap="Seatings of n people: row n! against circle (n-1)!"
import math, itertools
row5 = list(itertools.permutations(range(5)))
adj = sum(1 for p in row5 if abs(p.index(0) - p.index(1)) == 1)
canon = lambda p: p[p.index(0):] + p[:p.index(0)]
circ = len({canon(p) for p in row5})
assert len(row5) == 120 and adj == 48 and circ == 24
ns = (3, 4, 5, 6, 7)
rw = [math.factorial(n) for n in ns]
cw = [math.factorial(n - 1) for n in ns]
assert rw == [6, 24, 120, 720, 5040] and cw == [2, 6, 24, 120, 720]
W = lambda v: 6 + math.log10(v) / math.log10(5040) * 166
f = Fig(300, 236)
f.text(150, 12, "Seatings of n people (log scale)", size=10.5, color=NAVY, bold=True)
for i, n in enumerate(ns):
    y = 28 + i * 33
    f.text(8, y + 14, "n = %d" % n, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(50, y, W(rw[i]), 13, fill=BLUE, stroke=NAVY, r=2)
    f.text(50 + W(rw[i]) + 5, y + 7, "{:,}".format(rw[i]), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(50, y + 15, W(cw[i]), 13, fill=SAND, stroke=AMBER, r=2)
    f.text(50 + W(cw[i]) + 5, y + 22, "{:,}".format(cw[i]), size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.box(52, 196, 10, 8, fill=BLUE, stroke=NAVY, r=1)
f.text(66, 200, "row: n!", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.box(136, 196, 10, 8, fill=SAND, stroke=AMBER, r=1)
f.text(150, 200, "circle: (n-1)!", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(150, 222, "5 people: row 120, circle 24, A-B together 48", size=10.5, color=SLATE, bold=True)
```

## 1.6 Syllogisms and statement–conclusion reasoning

### The four statement forms

| Form | Statement | Venn picture | What it gives for certain |
|---|---|---|---|
| All | All A are B | A inside B | Some A are B; Some B are A |
| No | No A is B | A and B apart | No B is A; Some A are not B |
| Some | Some A are B | A and B overlap | Some B are A |
| Some … not | Some A are not B | part of A outside B | nothing about B |

```figure caption="The four statement forms as Venn diagrams. In the last one only the shaded part of A is certain to exist; whether the rest of A overlaps B is not known."
fig, axs = plt.subplots(1, 4, figsize=(5.2, 2.3))
titles = ['All A are B', 'No A is B', 'Some A are B', 'Some A are not B']
for ax, t in zip(axs, titles):
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.55, 1.25); ax.set_aspect('equal'); ax.axis('off')
    ax.text(0, -1.42, t, ha='center', va='center', fontsize=8.6)
ax = axs[0]
ax.add_patch(Circle((0, 0), 1.0, fc='none', ec=SERIES[2], lw=1.5))
ax.add_patch(Circle((-0.2, -0.15), 0.48, fc='#dbe8f6', ec=ACCENT, lw=1.5))
ax.text(-0.2, -0.15, 'A', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(0.45, 0.6, 'B', ha='center', va='center', fontsize=10, fontweight='bold', color=SERIES[2])
ax = axs[1]
ax.add_patch(Circle((-0.75, 0), 0.62, fc='#dbe8f6', ec=ACCENT, lw=1.5))
ax.add_patch(Circle((0.75, 0), 0.62, fc='none', ec=SERIES[2], lw=1.5))
ax.text(-0.75, 0, 'A', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(0.75, 0, 'B', ha='center', va='center', fontsize=10, fontweight='bold', color=SERIES[2])
for k, ax in enumerate(axs[2:]):
    if k == 1:
        ax.add_patch(Wedge((-0.45, 0), 0.8, 0, 360, fc='#f8dede', ec='none'))
        ax.add_patch(Circle((0.45, 0), 0.8, fc='white', ec='none'))
    ax.add_patch(Circle((-0.45, 0), 0.8, fc='none', ec=ACCENT, lw=1.5))
    ax.add_patch(Circle((0.45, 0), 0.8, fc='none', ec=SERIES[2], lw=1.5))
    ax.text(-0.8, 0, 'A', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(0.8, 0, 'B', ha='center', va='center', fontsize=10, fontweight='bold', color=SERIES[2])
fig.subplots_adjust(wspace=0.05)
```

### Combining two statements

Two statements share a middle term (B below). Put them in the order "A–B, B–C" and
read the result:

| First | Second | Definite conclusion |
|---|---|---|
| All A are B | All B are C | All A are C |
| All A are B | No B is C | No A is C |
| Some A are B | All B are C | Some A are C |
| Some A are B | No B is C | Some A are not C |
| No A is B | All B are C | Some C are not A |
| All A are B | Some B are C | **no definite conclusion** about A and C |
| Some A are B | Some B are C | **no definite conclusion** |
| No A is B | No B is C | **no definite conclusion** |

### The two rules that settle every question

1. **Draw the smallest picture.** Draw only the overlaps the statements force. Then ask:
   *can I redraw the circles, still obeying every statement, so that this conclusion is
   false?* If yes, the conclusion does not follow.
2. **Converse rules.** "Some A are B" ⇔ "Some B are A". "No A is B" ⇔ "No B is A".
   "All A are B" gives only "Some B are A" — never "All B are A".

**Either–or.** When neither of two conclusions follows on its own, but they are a
complementary pair about the *same two terms* — "Some A are B" with "No A is B", or
"All A are B" with "Some A are not B" — then one of them must be true, and the answer is
"either I or II follows".

::: example A standard syllogism
**Problem.** Statements: All doctors are graduates. Some graduates are singers.
Conclusions: I. Some doctors are singers. II. Some singers are graduates.

**Solution.** Draw *doctors* inside *graduates* and let *singers* overlap *graduates*.
The singers can be drawn to touch only the part of graduates that holds no doctor, so I
does **not** follow. II is the converse of the second statement, so II **follows**.
Answer: only II.
:::

### Statement and conclusion (everyday statements)

A conclusion **follows** only if it is *directly* supported by the statement, without
outside knowledge and without going beyond what is said. Words like *only, all, never,
always, definitely* in a conclusion usually make it go too far. "Exercise lowers the
risk of heart disease" supports "his risk is lower", not "he will never get heart
disease".

::: caution "Some" means "at least one, possibly all"
"Some A are B" does not mean "some A are not B". If the question proves that all A are
B, the conclusion "Some A are B" is still true. Do not read the everyday meaning of
"some" ("not all") into a syllogism.
:::

## Formula and fact sheet

| Topic | Rule |
|---|---|
| Turns | right = 90° clockwise, left = 90° anticlockwise, about-turn = 180° |
| Distance | net x (east +), net y (north +); distance $= \sqrt{x^2 + y^2}$ |
| Triples | 3-4-5, 6-8-10, 5-12-13, 8-15-17, 9-12-15, 12-16-20, 7-24-25 |
| Shadows | morning → shadow to the west; evening → shadow to the east |
| Reverse direction | the start as seen from the end is the opposite direction (SE ↔ NW) |
| Speaker clues | "only son of my father" (male speaker) = himself; "only son of my father's father" = my father |
| Letter positions | E J O T Y = 5 10 15 20 25; opposite letter = 27 − position |
| Ranking | N = L + R − 1; rank from the other end = N − L + 1 |
| Between two people | (larger position − smaller position) − 1, both counted from the same end |
| Circular seating | facing the centre: left = clockwise, right = anticlockwise |
| Row seating | facing north: their left = your left; facing south: reversed |
| All A are B | gives "Some A are B" and "Some B are A", never "All B are A" |
| No A is B | gives "No B is A" and "Some A are not B" |
| Some A are B | gives "Some B are A" |
| Either–or | the pair "Some A are B" / "No A is B" (or "All A are B" / "Some A are not B") |

## Chapter summary

- Verbal reasoning carries 5 of the 20 MAT questions; the MEC sample is a direction walk.
- Direction walks: track the facing direction, add east–west and north–south legs
  separately, and finish with Pythagoras; right = clockwise.
- Morning shadows point west, evening shadows east; "facing" and "is from the start"
  are different questions.
- Blood relations: draw the tree with squares (male), circles (female) and double
  lines (marriage); never assume gender.
- Coding: write the code under the word, find the change letter by letter
  (shift, opposite letter with sum 27, reversal, pair swap, sum of positions).
- Analogy: turn the first pair into a sentence and apply it; odd one out: find the
  property that splits the items exactly 3 : 1.
- Ranking: N = L + R − 1. Around a table facing the centre, left is clockwise.
- Syllogisms: draw the least the statements force; a conclusion follows only if no
  allowed drawing makes it false; use "either–or" for a complementary pair.

## Practice questions

**Set A — Recall (25 questions)**

1. A man is facing north. He turns right, then right again, then left. Which direction is he facing now?
   (a) North (b) South (c) East (d) West
2. Sunita walks 12 m east, then turns left and walks 5 m. How far is she from her starting point?
   (a) 13 m (b) 17 m (c) 7 m (d) 12 m
3. A person facing west turns 90° clockwise. Which direction is he facing now?
   (a) South (b) North (c) East (d) South-west
4. Soon after sunrise, Hari stood facing his own shadow. Which direction was he facing?
   (a) East (b) North (c) South (d) West
5. From her home, Asha walks 4 km north and then 3 km west. Where is she now with respect to her home?
   (a) 7 km north-west (b) 5 km north-east (c) 5 km north-west (d) 1 km west
6. Pointing to a boy, Gita said, "His mother is the only daughter of my mother." How is Gita related to the boy?
   (a) sister (b) aunt (c) grandmother (d) mother
7. Introducing a girl, Raju said, "She is the daughter of the only son of my father." How is the girl related to Raju?
   (a) daughter (b) sister (c) niece (d) cousin
8. A is B's brother. C is A's mother. D is C's father. How is D related to B?
   (a) father (b) uncle (c) grandfather (d) brother
9. If P × Q means "P is the father of Q" and P + Q means "P is the sister of Q", then A + B × C means
   (a) A is the mother of C (b) A is the aunt of C (c) A is the sister of C (d) A is the grandmother of C
10. If COLD is written as DPME in a code, how is WARM written in that code?
   (a) XBTN (b) VZQL (c) YCTO (d) XBSN
11. If each letter is replaced by its opposite letter of the alphabet (A↔Z, B↔Y, C↔X, …), HEART is written as
   (a) SVAIG (b) SVZIG (c) TVZIG (d) SUZIG
12. If A = 1, B = 2, …, Z = 26 and CAT = 24, then DOG =
   (a) 26 (b) 24 (c) 27 (d) 30
13. If PAPER is written as REPAP in a code, how is NURSE written in that code?
   (a) ERSUN (b) ESRNU (c) ESRUN (d) NESRU
14. If "sky" is called "sea", "sea" is called "water", "water" is called "air", "air" is called "cloud" and "cloud" is called "rain", what do we drink when thirsty?
   (a) water (b) sea (c) cloud (d) air
15. Doctor : Stethoscope :: Carpenter : ?
   (a) Saw (b) Needle (c) Scalpel (d) Trowel
16. Kidney : Nephrologist :: Heart : ?
   (a) Neurologist (b) Dermatologist (c) Cardiologist (d) Hepatologist
17. 4 : 64 :: 6 : ?
   (a) 36 (b) 216 (c) 180 (d) 125
18. Choose the odd one out.
   (a) Thermometer (b) Barometer (c) Hygrometer (d) Microscope
19. Choose the odd one out.
   (a) 51 (b) 29 (c) 37 (d) 43
20. Choose the odd one out.
   (a) CEG (b) GIK (c) PRU (d) MOQ
21. In a row of students, Kiran is 12th from the left and 17th from the right. How many students are in the row?
   (a) 29 (b) 28 (c) 27 (d) 30
22. In a class of 40 students, Mina is 9th from the top. What is her rank from the bottom?
   (a) 31 (b) 33 (c) 30 (d) 32
23. P is taller than Q but shorter than R. S is taller than R, and T is the shortest of the five. Who is the tallest?
   (a) R (b) S (c) P (d) Q
24. Statements: All roses are flowers. All flowers are plants. Which conclusion follows?
   (a) All roses are plants (b) All plants are roses (c) Some plants are not flowers (d) No rose is a plant
25. Statement: No doctor is a lawyer. Which of the following must be true?
   (a) Some lawyers are doctors (b) No lawyer is a doctor (c) All lawyers are doctors (d) Some doctors are lawyers

::: note Answers and explanations — Set A
**1.** (c) — North → right → east → right → south → left → east. Facing south, a left turn points east.
**2.** (a) — The legs are 12 m east and 5 m north: $\sqrt{12^2 + 5^2}$ = 13 m (the 5-12-13 triple). 17 m is the path length, not the distance.
**3.** (b) — Clockwise from west is north (W → N → E → S → W).
**4.** (d) — In the morning the sun is in the east, so his shadow falls to the west; facing the shadow means facing west.
**5.** (c) — 4 km north and 3 km west: $\sqrt{4^2 + 3^2}$ = 5 km, and north + west = north-west. 7 km adds the legs.
**6.** (d) — The only daughter of Gita's mother is Gita herself, so Gita is the boy's mother.
**7.** (a) — The only son of Raju's father is Raju himself; the girl is the daughter of Raju.
**8.** (c) — C is the mother of A and B (they are brothers/sisters); D is C's father, so D is B's (maternal) grandfather.
**9.** (b) — A is the sister of B, and B is the father of C: A is C's father's sister — C's aunt.
**10.** (d) — COLD → DPME moves every letter one place on (+1). W→X, A→B, R→S, M→N: XBSN.
**11.** (b) — Opposite letters add to 27: H(8)→S(19), E(5)→V(22), A→Z, R(18)→I(9), T(20)→G(7): SVZIG.
**12.** (a) — CAT = 3 + 1 + 20 = 24, so the code is the sum of positions. DOG = 4 + 15 + 7 = 26.
**13.** (c) — The word is written backwards. NURSE reversed is ESRUN.
**14.** (d) — We drink water, and in this code water is called "air". Option (a) is the real name, not the code name.
**15.** (a) — A doctor's working tool is the stethoscope; a carpenter's is the saw. A trowel is a mason's tool, a scalpel a surgeon's.
**16.** (c) — A nephrologist is the specialist for the kidney; a cardiologist for the heart.
**17.** (b) — 64 = $4^3$, so the answer is $6^3$ = 216. 36 is the square; 125 is the cube of the wrong number.
**18.** (d) — The thermometer, barometer and hygrometer measure temperature, pressure and humidity; a microscope only magnifies.
**19.** (a) — 29, 37 and 43 are prime; 51 = 3 × 17 is not.
**20.** (c) — CEG, GIK and MOQ step +2, +2 (C 3, E 5, G 7). PRU steps +2, +3 (P 16, R 18, U 21).
**21.** (b) — N = L + R − 1 = 12 + 17 − 1 = 28. Adding without the −1 gives 29, which counts Kiran twice.
**22.** (d) — Rank from the other end = 40 − 9 + 1 = 32.
**23.** (b) — The chain is T < Q < P < R < S, so S is the tallest.
**24.** (a) — Roses ⊂ flowers ⊂ plants, so all roses are plants. "All plants are roses" reverses the "all" statement, which is never allowed.
**25.** (b) — A "no" statement converts both ways: no doctor is a lawyer ⇔ no lawyer is a doctor.
:::

**Set B — Understanding (15 questions)**

1. If south-east becomes north, north-east becomes west, and all other directions change in the same way, what does west become?
   (a) North-east (b) South (c) South-east (d) North-west
2. Bikash walks 10 m south, turns left and walks 12 m, then turns left again and walks 15 m. How far and in which direction is he from his starting point?
   (a) 13 m north-east (b) 13 m south-east (c) 17 m north-east (d) 37 m east
3. A man facing north turns 45° clockwise, then 180° clockwise, then 270° anticlockwise. Which direction is he facing now?
   (a) North-east (b) South-west (c) South-east (d) North-west
4. One evening before sunset, Sita and Bina stood talking face to face. Bina's shadow fell exactly to Bina's left. Which direction was Sita facing?
   (a) East (b) North (c) West (d) South
5. Pointing to a woman in a photograph, Arjun said, "Her mother's only son is my father." How is the woman related to Arjun?
   (a) mother (b) sister (c) grandmother (d) paternal aunt
6. A is the son of B. C, the sister of B, has a son D and a daughter E. How is A related to D?
   (a) brother (b) cousin (c) nephew (d) uncle
7. A @ B means "A is the brother of B", A # B means "A is the mother of B" and A % B means "A is the daughter of B". In P # Q @ R % S, how is P related to S?
   (a) sister (b) mother (c) wife (d) daughter
8. In a code language, "pit na sor" means "drink clean water", "sor tak lim" means "water is life" and "ral pit na" means "drink clean milk". Which code word means "milk"?
   (a) pit (b) ral (c) na (d) tak
9. If TEACHER is written as VGCEJGT in a code, how is DOCTOR written in that code?
   (a) FQEVQT (b) FQDVQT (c) EPDUPS (d) FQEUQT
10. In a code, CAB = 6 and DAB = 8. What is the code for BED?
   (a) 11 (b) 40 (c) 20 (d) 30
11. 7 : 50 :: 9 : ?
   (a) 81 (b) 72 (c) 90 (d) 82
12. BDF : CEG :: MOQ : ?
   (a) NPR (b) NOP (c) LNP (d) OQS
13. Choose the odd one out.
   (a) 28 (b) 126 (c) 63 (d) 217
14. In a row of 45 children, Rina is 17th from the left and Hari is 20th from the right. How many children sit between Rina and Hari?
   (a) 7 (b) 9 (c) 8 (d) 10
15. Statements: Some doctors are singers. All singers are dancers. Conclusions: I. Some doctors are dancers. II. All dancers are singers.
   (a) Only I follows (b) Only II follows (c) Both I and II follow (d) Neither I nor II follows

::: note Answers and explanations — Set B
**1.** (c) — SE (135°) has become N (0°): every direction turns 135° anticlockwise. Check: NE (45°) → 45° − 135° = 270° = W, as stated. West (270°) → 135° = south-east.
**2.** (a) — South 10, left → east 12, left → north 15: net 12 m east and 15 − 10 = 5 m north. $\sqrt{12^2 + 5^2}$ = 13 m, north-east.
**3.** (d) — Net turn = +45 + 180 − 270 = −45°, i.e. 45° anticlockwise from north: north-west.
**4.** (b) — Evening sun is in the west, so shadows point east. Bina's left is east, so Bina faces south; Sita faces her, so Sita faces north.
**5.** (d) — The woman's mother's only son is the woman's brother, and he is Arjun's father. So she is Arjun's father's sister — his paternal aunt (phupu).
**6.** (b) — A is the child of B, and D is the child of B's sister C: children of a brother and sister are cousins.
**7.** (c) — P is the mother of Q; Q and R are siblings, so P is R's mother too; R is the daughter of S, so S is R's other parent, the father. P is S's wife.
**8.** (b) — Sentences 1 and 3 share "drink clean" and the codes pit, na; the only new word in sentence 3 is "milk" and the only new code is ral.
**9.** (a) — Each letter moves +2: T→V, E→G, A→C … So D→F, O→Q, C→E, T→V, O→Q, R→T: FQEVQT.
**10.** (b) — The sum rule gives CAB = 6 but DAB = 7, so the code is the product of positions: 4 × 1 × 2 = 8. BED = 2 × 5 × 4 = 40. Option (a) is the sum.
**11.** (d) — 50 = $7^2 + 1$, so the answer is $9^2 + 1$ = 82. 81 forgets the +1.
**12.** (a) — Each letter of BDF moves +1 to give CEG; MOQ +1 gives NPR.
**13.** (c) — 28 = $3^3 + 1$, 126 = $5^3 + 1$, 217 = $6^3 + 1$, but 63 = $4^3 - 1$. (All four are multiples of 7, so divisibility does not separate them.)
**14.** (c) — Hari from the left = 45 − 20 + 1 = 26th. Between the 17th and the 26th: 26 − 17 − 1 = 8.
**15.** (a) — Some doctors are singers and all singers are dancers, so those doctors are dancers: I follows. II reverses an "all" statement, so it does not follow.
:::

**Set C — Application (11 questions)**

1. Ramesh walks 20 m north, turns right and walks 30 m, turns right and walks 35 m, turns left and walks 15 m, and finally turns left and walks 15 m. How far and in which direction is he from his starting point?
   (a) 15 m east (b) 30 m north-east (c) 45 m west (d) 45 m east
2. Kamal walks 8 km south, then turns east and walks 6 km. In which direction, and how far, is his starting point from where he now stands?
   (a) 10 km south-east (b) 14 km north-west (c) 10 km north-east (d) 10 km north-west
3. In a family, R is the son of P. Q is the father of P, and S is the wife of Q. T is the brother of R, and U is the sister of P. How is S related to T?
   (a) mother (b) aunt (c) grandmother (d) sister
4. If ROSE is coded as 6821, CHAIR as 73456 and PREACH as 961473, what is the code for SEARCH?
   (a) 214673 (b) 214763 (c) 241673 (d) 216473
5. In a certain code, MOTHER is written as OMHTRE. How is SISTER written in that code?
   (a) ISSTRE (b) ISTSRE (c) SITSER (d) ISTSER
6. Five students P, Q, R, S and T sit in a row facing north. S sits at one end. R is second to the right of S. P is to the immediate left of Q. T does not sit at an end. Who sits in the middle of the row?
   (a) T (b) P (c) R (d) Q
7. Six friends A, B, C, D, E and F sit around a round table facing the centre. A sits opposite D. B is to the immediate left of A. F is to the immediate right of D. C is to the immediate right of A. Who sits opposite B?
   (a) E (b) F (c) C (d) D
8. In a row, Anil is 10th from the left and Bimal is 9th from the right. When they exchange places, Anil becomes 15th from the left. How many people are in the row?
   (a) 22 (b) 24 (c) 25 (d) 23
9. Statements: All cats are dogs. Some dogs are rats. Conclusions: I. Some rats are cats. II. No rat is a cat.
   (a) Only I follows (b) Only II follows (c) Either I or II follows (d) Neither I nor II follows
10. Statements: Regular exercise lowers the risk of heart disease. Ramesh exercises regularly. Conclusions: I. Ramesh will never get heart disease. II. Ramesh's risk of heart disease is lower than it would be without exercise.
   (a) Only I follows (b) Only II follows (c) Both I and II follow (d) Neither I nor II follows
11. Statements: Some pens are books. No book is a bag. Conclusions: I. Some pens are not bags. II. Some bags are pens.
   (a) Only I follows (b) Only II follows (c) Both I and II follow (d) Neither I nor II follows

::: note Answers and explanations — Set C
**1.** (d) — North 20 (y = 20); right → east 30 (x = 30); right → south 35 (y = −15); left → east 15 (x = 45); left → north 15 (y = 0). He is 45 m due east of the start.
**2.** (d) — Kamal is 6 km east and 8 km south of the start, i.e. 10 km south-east of it (6-8-10). The start, seen from Kamal, is in the opposite direction: 10 km north-west. Option (a) is the trap.
**3.** (c) — S is the wife of P's father, so S is P's mother. T is R's brother, so T is also P's child. S is therefore T's grandmother.
**4.** (a) — From the three words: R = 6, O = 8, S = 2, E = 1, C = 7, H = 3, A = 4, I = 5, P = 9 (R = 6 in all three, which confirms the code). SEARCH = 2 1 4 6 7 3.
**5.** (b) — MO TH ER → OM HT RE: each pair of letters is swapped. SI ST ER → IS TS RE = ISTSRE.
**6.** (c) — R cannot be second to the right of S if S is at the right end, so S is at the left end and R is third. P and Q must be adjacent, so they take places 4 and 5, and T takes place 2: S T R P Q. R is in the middle.
**7.** (a) — Going clockwise (= leftwards for people facing the centre) from A: A, B (A's left), F, D (opposite A), then E, C (C is A's right, the seat before A). B is opposite E.
**8.** (d) — After the exchange Anil stands in Bimal's old place, which is 9th from the right, and he is now 15th from the left: N = 15 + 9 − 1 = 23.
**9.** (c) — The rats may or may not overlap the cats, so neither I nor II follows alone. But "Some rats are cats" and "No rat is a cat" are a complementary pair about the same two terms — one of them must be true.
**10.** (b) — The statement supports only a lower risk. "Never" goes beyond what is said.
**11.** (a) — The pens that are books cannot be bags (no book is a bag), so some pens are not bags: I follows. Whether any bag is a pen is not known.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain a step-by-step method for direction-sense and blood-relation questions and solve two worked problems of each kind. <span class="marks">[10]</span>
2. Explain methods for coding–decoding, ranking, circular seating and syllogisms, with a worked problem of each kind. <span class="marks">[10]</span>

### Model answer D1: Direction sense and blood relations (10 marks)

**Introduction.** Both types are solved best by **drawing**, not by thinking in words. Direction problems need a small coordinate sketch, and relation problems need a family tree with symbols.

**Method for direction sense.**

1. Place the start at the origin and mark **N** at the top of the page.
2. Draw each move as an arrow: left and right depend on the direction the person is **facing**, not on the page.
3. Turn right = clockwise (N→E→S→W); turn left = anticlockwise.
4. At the end, find the net distance by Pythagoras and the direction from the net east–west and north–south change.
5. **Shadow rule:** in the morning the sun is in the east, so shadows fall to the **west**; in the evening shadows fall to the **east**.

**Worked problem 1.** Ram walks 10 m north, turns left and walks 5 m, then turns left and walks 15 m. How far and in which direction is he from the start?

| Move | Position (x east, y north) |
|---|---|
| Start | (0, 0) |
| 10 m north | (0, 10) |
| Turn left (west) 5 m | (−5, 10) |
| Turn left (south) 15 m | (−5, −5) |

Distance = √(5² + 5²) = √50 = **7.07 m**, and he is to the **south-west** of the start.

**Worked problem 2.** A man faces east, turns 90° clockwise, then 135° anticlockwise. Which way does he face? East → clockwise 90° = south; anticlockwise 135° from south = south → east (90°) → north-east (45°). He faces **north-east**.

**Method for blood relations.**

1. Draw **male as a square (□) and female as a circle (○)**, with a horizontal line for marriage and vertical lines for children.
2. Translate each clue into one link; use *only* the information given.
3. Remember: mother's brother = maternal uncle; father's sister = aunt; sister's son = nephew; brother's wife = sister-in-law.

**Worked problem 3.** Pointing to a man, Gita says, "His mother is the only daughter of my mother." The only daughter of Gita's mother is **Gita herself**, so the man's mother is Gita, and the man is **Gita's son**.

**Worked problem 4.** A is the father of B; B is the sister of C; C is the mother of D. How is A related to D? A is father of B and C (B and C are siblings), so A is the **maternal grandfather** of D.

| Clue | Meaning |
|---|---|
| Only daughter of my mother | I myself (if I am a woman) |
| Son of my father's only brother | My cousin |
| Mother's mother's husband | Maternal grandfather |

**Conclusion.** A neat diagram removes confusion about left, right and generation, so every problem becomes a short reading of the sketch.

### Model answer D2: Coding, ranking, seating and syllogisms (10 marks)

**Introduction.** These problems test whether you can find a rule and apply it without error.

**1. Coding–decoding.** Write the alphabet positions A=1 … Z=26. Typical rules: a fixed **shift**, **reverse position** (A↔Z, so the code of a letter is 27 minus its position), or a **sum** of positions. Example: if each letter is shifted two places forward, MAT → OCV. Example: CAT = 3 + 1 + 20 = 24.

**2. Ranking.** Total = (rank from top) + (rank from bottom) − 1. If Rita is 12th from the top and 25th from the bottom, there are 12 + 25 − 1 = **36** students.

**3. Circular seating.** Six persons sit round a table facing the centre. A is opposite D. B is immediately clockwise of A, C is opposite B, and E is immediately anticlockwise of A. Number the seats 1–6 clockwise: A = 1, so D = 4; B = 2, so C = 5; E = 6, so F = 3. The clockwise order is A, B, F, D, C, E. The person between B and D is **F**. The number of ways to seat n persons around a table is (n − 1)!, which for 6 persons is 5! = **120**; in a row it is n!.

**4. Syllogisms (Venn method).** Draw a circle for each term.

| Statement | Diagram rule |
|---|---|
| All A are B | Circle A inside circle B |
| Some A are B | Circles overlap |
| No A is B | Separate circles |

**Example.** Statements: All cats are animals. Some animals are dogs. Conclusions: I. Some cats are dogs. II. Some dogs are animals. The cat circle lies inside the animal circle, and the dog circle overlaps the animal circle, but it may or may not reach the cat circle. So **I does not follow** (a possibility, not a certainty) and **II follows** (the dog circle overlaps the animal circle).

**Rules of thumb.** Take the statements as true even if they look false in real life; a conclusion must be true in **every** possible diagram.

**Conclusion.** Each type needs a table or a diagram, and the answer is read from the picture, never guessed.
