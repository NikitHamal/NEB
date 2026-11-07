---
subject: Mathematics
grade: BCA
unit: 14
title: Verbal and Logical Reasoning
hours: 5
area: Reasoning
---

Reasoning is worth 7–10 of the 50 mathematics questions in the published pattern, split here between this chapter and the next. These are the questions where practice beats talent: each type has a fixed method, and the same question shapes recur every year. This chapter covers the verbal side: codes, family relations, directions, ranking and syllogisms.

::: key What the paper asks from this chapter
- **Coding**: letter shift, position values, opposite letters ($A\leftrightarrow Z$ so the sum is 27).
- **Blood relations**: translate each phrase into a family tree before answering.
- **Direction**: right-angled displacement uses Pythagoras; track the facing direction after each turn.
- **Ranking**: total = rank from top + rank from bottom − 1.
- **Syllogisms**: "All A are B" does not mean "All B are A".
:::

## 14.1 Coding and decoding

- Positions: A=1, B=2, … Z=26. The opposite letter of the one at position $n$ is at $27-n$ (E↔V).
- **Shift codes**: find the shift on one letter and apply it to the rest. ROSE→TQUG is +2, so LAKE→NCMG. TABLE→UBCMF is +1, so CHAIR→DIBJS.
- **Sum codes**: add the position values (G=7, O=15, so GO=22).
- Check the first two letters before trusting a pattern; the same shift can be +1, +2, −1 in alternating positions.

```svgfig label="14.1" caption="Coding and decoding on one strip. Every letter has a value from 1 to 26 and an opposite letter whose value is 27 minus its own (A and Z, E and V). A shift code adds the same number to every letter: ROSE becomes TQUG with +2, so LAKE becomes NCMG; TABLE becomes UBCMF with +1, so CHAIR becomes DIBJS. All these results are computed in the cell, not copied from a book."
import string
A = string.ascii_uppercase
pos = lambda c: A.index(c) + 1
opp = lambda c: A[26 - pos(c)]
def sh(w, k): return "".join(A[(A.index(c) + k) % 26] for c in w)
assert sh("ROSE", 2) == "TQUG" and sh("LAKE", 2) == "NCMG" and sh("TABLE", 1) == "UBCMF" and sh("CHAIR", 1) == "DIBJS"
assert opp("E") == "V" and all(pos(c) + pos(opp(c)) == 27 for c in A)
assert sum(pos(c) for c in "CAB") == 6 and sum(pos(c) for c in "GO") == 22 and sh("CAT", 1) == "DBU" and "".join(opp(c) for c in "CAT") == "XZG"
f = Fig(780, 340)
x0 = 56
for i, c in enumerate(A):
    x = x0 + i * 27.5
    hl = c in "EV"
    f.box(x, 14, 26, 24, c, fill=("#fde68a" if hl else BLUE), stroke=NAVY, size=11, bold=True)
    f.box(x, 40, 26, 24, str(i + 1), fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10)
    f.box(x, 66, 26, 24, opp(c), fill=("#fde68a" if hl else MINT), stroke=TEAL, size=11, bold=True)
f.text(28, 31, "letter", size=10.5, color=NAVY, bold=True); f.text(28, 57, "value", size=10.5, color=SLATE, bold=True); f.text(28, 83, "opposite", size=10.5, color=TEAL, bold=True)
f.text(390, 112, "opposite pairs always add to 27:  A + Z = 1 + 26,  E + V = 5 + 22,  M + N = 13 + 14", size=10.5, color=RED, bold=True)
f.text(200, 148, "Shift code: ROSE to TQUG is +2", size=11.5, color=NAVY, bold=True)
for i, (a, b) in enumerate(zip("ROSE", sh("ROSE", 2))):
    x = 40 + i * 78
    f.box(x, 164, 40, 28, a, fill=BLUE, stroke=NAVY, size=12, bold=True)
    f.arrow([(x + 20, 193), (x + 20, 221)], color=AMBER)
    f.text(x + 36, 209, "+2", size=10.5, color=AMBER, bold=True, anchor="start")
    f.box(x, 222, 40, 28, b, fill=SAND, stroke=AMBER, size=12, bold=True)
f.text(200, 276, "Apply it:  LAKE + 2 = NCMG", size=11, color=TEAL, bold=True)
f.text(200, 298, "TABLE to UBCMF is +1, so CHAIR to DIBJS", size=10.5, color=SLATE)
f.text(200, 320, "test the SECOND letter before you trust the rule", size=10.5, color=RED, bold=True)
f.text(590, 148, "Sum and opposite codes", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("CAB = 3 + 1 + 2 = 6", SLATE), ("GO = 7 + 15 = 22", SLATE), ("next letter of CAT = DBU", SLATE), ("opposite letters of CAT = XZG", SLATE), ("opposite of D, O, G = W, L, T", SLATE), ("position of opposite = 27 - n", TEAL)]):
    f.text(450, 178 + j * 27, t, size=11, color=c, anchor="start", bold=(j == 5))
```

## 14.2 Blood relations and direction sense

- "My mother's only son" is *me or my brother*; "my father's only son" is me. "Mother's brother" is a maternal uncle; "father's sister's son" is a cousin.
- Work backwards from the person being pointed at, one link at a time, and draw generations as levels.
- **Directions**: a right turn from North faces East, then South, then West. A left turn from North faces West. A 180° turn reverses. Displacement for legs at right angles is $\sqrt{a^2+b^2}$ (3-4-5, 5-12-13, 8-6-10). At sunrise a person's shadow falls to the west.

```photogrid label="14.1" cols="2" ratio="1.35" caption="Two real objects behind two reasoning topics. (a) A family tree: each box is a person and each line is one link, exactly how you should draw a blood-relation question before answering it (Fig 14.2). (b) A compass rose set into the floor of a plaza in Lille, France: the four main directions are 90 degrees apart, and a right turn always moves one step clockwise from North to East to South to West."
@ photo id="bcamath/famtree" cap="Draw the family tree first"
focus 0.5 0.5
@ photo id="bcamath/windrose" cap="Compass rose: N, E, S, W"
focus 0.5 0.5
```

```svgfig label="14.2" caption="A blood-relation question solved by drawing the tree. Asha is the person in the question. The code below stores the tree and finds each relative by following links, so the answers are computed: her father's sister is Gita and Gita's son is Ravi (Asha's cousin); her mother's brother is Suman (maternal uncle) and his daughter is Priya (also a cousin); her mother's mother is Laxmi (maternal grandmother). Move up one generation per link and then across to the sibling, then down."
par = {"Hari": ("Dev", "Kamala"), "Gita": ("Dev", "Kamala"), "Mina": ("Bishnu", "Laxmi"), "Suman": ("Bishnu", "Laxmi"), "Asha": ("Hari", "Mina"), "Binod": ("Hari", "Mina"), "Ravi": ("", "Gita"), "Priya": ("Suman", "")}
sex = {"Hari": "M", "Suman": "M", "Binod": "M", "Ravi": "M", "Dev": "M", "Bishnu": "M", "Gita": "F", "Mina": "F", "Asha": "F", "Priya": "F", "Kamala": "F", "Laxmi": "F"}
sibs = lambda x: [y for y in par if y != x and par[y] == par[x]]
fa = par["Asha"][0]; mo = par["Asha"][1]
aunt = [s for s in sibs(fa) if sex[s] == "F"][0]
cousin1 = [y for y in par if par[y][1] == aunt and sex[y] == "M"][0]
uncle = [s for s in sibs(mo) if sex[s] == "M"][0]
cousin2 = [y for y in par if par[y][0] == uncle and sex[y] == "F"][0]
gm = par[mo][1]
assert (aunt, cousin1, uncle, cousin2, gm) == ("Gita", "Ravi", "Suman", "Priya", "Laxmi")
f = Fig(780, 340)
def pbox(x, y, n, hl=False):
    f.box(x, y, 96, 26, n, fill=("#fde68a" if hl else (BLUE if sex[n] == "M" else ROSE)), stroke=(AMBER if hl else (NAVY if sex[n] == "M" else RED)), size=11, bold=hl)
for n, x, y in [("Dev", 20, 18), ("Kamala", 130, 18), ("Bishnu", 520, 18), ("Laxmi", 630, 18), ("Gita", 20, 118), ("Hari", 150, 118), ("Mina", 420, 118), ("Suman", 620, 118), ("Ravi", 20, 218), ("Asha", 230, 218), ("Binod", 340, 218), ("Priya", 620, 218)]:
    pbox(x, y, n, n == "Asha")
f.line(116, 31, 130, 31, color=SLATE, sw=2); f.line(616, 31, 630, 31, color=SLATE, sw=2); f.line(246, 131, 420, 131, color=SLATE, sw=2)
f.text(333, 124, "married", size=10.5, color=SLATE, italic=True)
f.line(123, 31, 123, 80, color=SLATE); f.line(68, 80, 198, 80, color=SLATE); f.line(68, 80, 68, 118, color=SLATE); f.line(198, 80, 198, 118, color=SLATE)
f.line(573, 31, 573, 80, color=SLATE); f.line(468, 80, 668, 80, color=SLATE); f.line(468, 80, 468, 118, color=SLATE); f.line(668, 80, 668, 118, color=SLATE)
f.line(333, 131, 333, 180, color=SLATE); f.line(278, 180, 388, 180, color=SLATE); f.line(278, 180, 278, 218, color=SLATE); f.line(388, 180, 388, 218, color=SLATE)
f.line(68, 144, 68, 218, color=SLATE); f.line(668, 144, 668, 218, color=SLATE)
f.text(60, 262, "blue = male, pink = female", size=10.5, color=SLATE, anchor="start")
for j, (t, c) in enumerate([("Ravi = father's sister's son = cousin", NAVY), ("Suman = mother's brother = maternal uncle", TEAL), ("Priya = mother's brother's child = cousin", NAVY), ("Gita = father's sister = aunt (phupu)", TEAL), ("Laxmi = mother's mother = grandmother", NAVY)]):
    f.text(420, 262 + j * 17, t, size=10.5, color=c, anchor="start", bold=(j % 2 == 1))
f.text(180, 300, "one link at a time, one level at a time", size=10.5, color=RED, bold=True)
```

```svgfig label="14.3" caption="Direction sense, computed. Start facing North. Walk 10 m, turn right (now East) and walk 6 m, turn right again (now South) and walk 2 m. The cell tracks the position and the facing direction: the end point is 6 m east and 8 m north of the start, so the straight-line distance is the square root of 36 + 64 = 10 m, at 36.87 degrees east of north (north-east), and the walker is facing South. The middle table shows what each turn does to the facing direction. Right-angled displacements use Pythagoras: 3-4-5, 5-12-13, 8-15-17."
import math
H = ["N", "E", "S", "W"]
def turn(h, t): return H[(H.index(h) + {"R": 1, "L": -1, "U": 2}[t]) % 4]
assert turn("N", "R") == "E" and turn("N", "L") == "W" and turn("E", "R") == "S" and turn("S", "L") == "E" and turn("W", "U") == "E"
d = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
p = (0, 0); h = "N"; pts = [p]
for dist, t in [(10, None), (6, "R"), (2, "R")]:
    if t: h = turn(h, t)
    p = (p[0] + d[h][0] * dist, p[1] + d[h][1] * dist); pts.append(p)
assert pts == [(0, 0), (0, 10), (6, 10), (6, 8)] and h == "S"
dist = math.hypot(*p); ang = math.degrees(math.atan2(p[0], p[1]))
assert dist == 10 and round(ang, 2) == 36.87
assert 3 ** 2 + 4 ** 2 == 5 ** 2 and 5 ** 2 + 12 ** 2 == 13 ** 2 and 8 ** 2 + 15 ** 2 == 17 ** 2
f = Fig(780, 330)
ox, oy, s = 50, 300, 16
P = [(ox + x * s, oy - y * s) for x, y in pts]
f.line(P[0][0], P[0][1], P[3][0], P[3][1], color=RED, sw=2, dash=True)
for a, b in zip(P, P[1:]): f.arrow([a, b], color=NAVY, sw=2.4)
f.circle(P[0][0], P[0][1], 5, fill="#fde68a", stroke=AMBER); f.circle(P[3][0], P[3][1], 5, fill="#bbf7d0", stroke=TEAL)
f.text(P[0][0] + 12, P[0][1] + 4, "start", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(P[0][0] - 8, (P[0][1] + P[1][1]) / 2, "10 m", size=10.5, color=NAVY, bold=True, anchor="end")
f.text((P[1][0] + P[2][0]) / 2, P[1][1] - 10, "6 m East", size=10.5, color=NAVY, bold=True)
f.text(P[3][0] + 10, P[3][1] + 20, "end, facing S", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(P[2][0] + 12, (P[2][1] + P[3][1]) / 2 + 4, "2 m", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(P[0][0] + 56, (P[0][1] + P[3][1]) / 2 + 14, "10 m straight", size=10.5, color=RED, bold=True, anchor="start")
f.text(130, 22, "N is up, E is right", size=10.5, color=SLATE)
f.text(130, 46, "displacement = 10 m, NE", size=10.5, color=RED, bold=True)
f.text(420, 22, "What one turn does", size=11.5, color=NAVY, bold=True)
for j, hd in enumerate(["facing", "right", "left", "U-turn"]):
    f.box(250 + j * 80, 36, 76, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, hh in enumerate(H):
    for j, t in enumerate([None, "R", "L", "U"]):
        f.box(250 + j * 80, 62 + i * 28, 76, 24, hh if t is None else turn(hh, t), fill=(BLUE if t is None else SOFT), stroke="#cbd5e1", color=SLATE, size=11, bold=(t is None))
f.text(410, 192, "right = one step clockwise: N, E, S, W, N", size=10.5, color=TEAL, bold=True)
f.text(410, 212, "left = one step anticlockwise", size=10.5, color=SLATE)
f.text(410, 232, "morning: sun in the east, shadow falls WEST", size=10.5, color=SLATE)
f.text(410, 252, "evening: shadow falls EAST", size=10.5, color=SLATE)
f.text(410, 280, "right-angle legs a, b: distance = sqrt(a^2 + b^2)", size=10.5, color=NAVY, bold=True)
f.text(410, 302, "3-4-5,  5-12-13,  8-15-17,  7-24-25", size=10.5, color=RED, bold=True)
```

## 14.3 Ranking, ordering and seating

- Rank from top $T$ and from bottom $B$ gives a total of $T+B-1$. Rank from bottom $=N-T+1$.
- Position from left $L$ and right $R$ gives a row of $L+R-1$.
- For "taller than" chains, write them as $A>B>C$ and read the extremes.

```svgfig label="14.4" caption="Ranking from both ends. A class has 41 students. Ram is 12th from the top and 30th from the bottom, so the two counts overlap on Ram alone and the class size is 12 + 30 - 1 = 41. The three cards below apply the same idea: a class of 45 with rank 17 from the top gives rank 29 from the bottom (45 - 17 + 1); a person who is 7th from the left and 12th from the right means a row of 7 + 12 - 1 = 18; and the chain P > Q, Q > R, S > P orders as S > P > Q > R. Everything is computed in the cell."
T, B = 12, 30
N = T + B - 1
assert N == 41 and N - T + 1 == B
assert 45 - 17 + 1 == 29 and 7 + 12 - 1 == 18
order = ["S", "P", "Q", "R"]
assert order == sorted("SPQR", key=lambda c: {"S": 0, "P": 1, "Q": 2, "R": 3}[c])
f = Fig(780, 330)
for i in range(N):
    x = 40 + i * 17
    col = "#fde68a" if i == T - 1 else ("#bfdbfe" if i < T - 1 else "#bbf7d0")
    f.box(x, 50, 16, 24, "", fill=col, stroke=("#b45309" if i == T - 1 else "#94a3b8"))
f.text(48, 42, "1", size=10.5, color=NAVY, bold=True); f.text(40 + 11 * 17 + 8, 42, "Ram", size=10.5, color=AMBER, bold=True); f.text(40 + 40 * 17 + 8, 42, "41", size=10.5, color=TEAL, bold=True)
f.arrow([(40, 96), (40 + 12 * 17 - 2, 96)], color=NAVY, both=True); f.text(40 + 6 * 17, 116, "12 from top", size=11, color=NAVY, bold=True)
f.arrow([(40 + 11 * 17, 132), (40 + 41 * 17 - 2, 132)], color=TEAL, both=True); f.text(40 + 26 * 17, 152, "30 from bottom", size=11, color=TEAL, bold=True)
f.text(390, 20, "Total = 12 + 30 - 1 = 41  (Ram is counted twice, so subtract 1)", size=11.5, color=RED, bold=True)
cards = [(20, "Class of 45", ["rank from top = 17", "from bottom = 45 - 17 + 1", "= 29"]), (272, "A row of people", ["7th from left, 12th from right", "total = 7 + 12 - 1", "= 18 people"]), (524, "Order chain", ["P > Q, Q > R, S > P", "so S > P > Q > R", "tallest S, shortest R"])]
for x, ttl, ls in cards:
    f.box(x, 178, 236, 140, "", fill=SOFT, stroke="#cbd5e1", r=4)
    f.text(x + 118, 198, ttl, size=11.5, color=NAVY, bold=True)
    for j, t in enumerate(ls):
        f.text(x + 12, 224 + j * 20, t, size=10.5, color=(RED if j == 2 else SLATE), anchor="start", bold=(j == 2))
for j, (c, hgt) in enumerate(zip(order, [32, 24, 16, 8])):
    f.box(540 + j * 48 + 10, 312 - hgt, 34, hgt, "", fill="#bfdbfe", stroke=NAVY)
    f.text(540 + j * 48 + 27, 324, c, size=10, color=NAVY, bold=True)
```

## 14.4 Syllogisms and statement–conclusion

- **All A are B** ⇒ some B are A, but *not* all B are A. **No A is B** ⇒ no B is A. **Some A are B** ⇒ some B are A.
- **All A are B, all B are C** ⇒ all A are C. Anything beyond the statements (a universal claim from a particular one) is a trap.
- Draw circles: A inside B inside C.

```svgfig label="14.5" caption="Euler circles for three syllogisms, with every verdict computed by brute force. The cell builds all possible worlds in which each of A, B and C has at least one member (218 worlds), keeps those where the premises are true, and calls a conclusion valid only if it is true in every one of them. (a) All A are B and all B are C: All A are C and Some C are A are valid, All C are A is not. (b) All A are B and some B are C: nothing about A and C follows, because the C circle can sit away from A. (c) No A is B and all C are B: No C is A is valid."
import itertools
types = list(itertools.product([0, 1], repeat=3))
models = [m for r in range(1, 9) for m in itertools.combinations(types, r)]
ALL = lambda m, i, j: all(t[j] for t in m if t[i])
NO = lambda m, i, j: not any(t[i] and t[j] for t in m)
SOME = lambda m, i, j: any(t[i] and t[j] for t in m)
nonempty = lambda m: all(any(t[k] for t in m) for k in range(3))
def valid(prem, c): return all(c(m) for m in models if nonempty(m) and all(p(m) for p in prem))
assert len([m for m in models if nonempty(m)]) == 218
P1 = [lambda m: ALL(m, 0, 1), lambda m: ALL(m, 1, 2)]
assert valid(P1, lambda m: ALL(m, 0, 2)) and valid(P1, lambda m: SOME(m, 2, 0)) and not valid(P1, lambda m: ALL(m, 2, 0))
P2 = [lambda m: ALL(m, 0, 1), lambda m: SOME(m, 1, 2)]
assert not valid(P2, lambda m: SOME(m, 0, 2)) and not valid(P2, lambda m: ALL(m, 0, 2)) and not valid(P2, lambda m: NO(m, 0, 2))
P3 = [lambda m: NO(m, 0, 1), lambda m: ALL(m, 2, 1)]
assert valid(P3, lambda m: NO(m, 2, 0)) and not valid(P3, lambda m: SOME(m, 2, 0)) and not valid(P3, lambda m: ALL(m, 2, 0))
f = Fig(780, 340)
def lab(x, y, t, c=NAVY): f.text(x, y, t, size=12, color=c, bold=True)
f.circle(125, 130, 95, fill="none", stroke=TEAL, sw=2.2); f.circle(125, 160, 65, fill="none", stroke=NAVY, sw=2.2); f.circle(125, 190, 35, fill="none", stroke=RED, sw=2.2)
lab(125, 52, "C", TEAL); lab(125, 108, "B", NAVY); lab(125, 194, "A", RED)
ox = 260
f.circle(ox + 105, 130, 70, fill="none", stroke=NAVY, sw=2.2); f.circle(ox + 80, 138, 28, fill="none", stroke=RED, sw=2.2); f.circle(ox + 175, 130, 55, fill="none", stroke=TEAL, sw=2.2)
lab(ox + 96, 82, "B", NAVY); lab(ox + 80, 142, "A", RED); lab(ox + 198, 134, "C", TEAL)
ox = 520
f.circle(ox + 150, 130, 70, fill="none", stroke=NAVY, sw=2.2); f.circle(ox + 150, 150, 38, fill="none", stroke=TEAL, sw=2.2); f.circle(ox + 40, 130, 35, fill="none", stroke=RED, sw=2.2)
lab(ox + 150, 90, "B", NAVY); lab(ox + 150, 154, "C", TEAL); lab(ox + 40, 134, "A", RED)
rows = [(0, ["Premises: all A are B, all B are C", "All A are C: VALID", "Some C are A: VALID", "All C are A: NOT valid"], [None, TEAL, TEAL, RED]),
        (260, ["Premises: all A are B, some B are C", "Some A are C: NOT valid", "All A are C: NOT valid", "No A is C: NOT valid"], [None, RED, RED, RED]),
        (520, ["Premises: no A is B, all C are B", "No C is A: VALID", "Some C are A: NOT valid", "All C are A: NOT valid"], [None, TEAL, RED, RED])]
for x, ls, cs in rows:
    for j, (t, c) in enumerate(zip(ls, cs)):
        f.text(x + 12, 246 + j * 22, t, size=10.5, color=(c or NAVY), anchor="start", bold=True)
f.text(390, 336, "valid = true in all 218 worlds where A, B, C each have a member", size=10.5, color=SLATE)
```

## 14.5 Eight traps in verbal reasoning

Reasoning questions have one correct method and several tempting shortcuts. These eight traps account for most wrong answers in the model papers, so read each one and test it on a question.

1. **Check the rule on at least two letters.** A code such as ROSE to TQUG looks like +2, but you must test R to T, O to Q, S to U and E to G before you apply it to LAKE (Fig 14.1). Some codes alternate, for example +1, +2, +1, +2. A rule that fits only the first letter is a guess, not a rule.
2. **Opposite letters add to 27, not 26.** A is 1 and Z is 26, so the opposite of the letter at position $n$ is at $27-n$. E (5) pairs with V (22), and M (13) pairs with N (14). If you use $26-n$ you will be wrong by one letter in every option.
3. **"Only son" and "only child" are different.** "My mother's only son" is the speaker (if male) or the speaker's brother, but "my father's only son" is always the speaker himself when he is male. "My father's sister's son" is a cousin, not a brother. Write each phrase as a link on the tree before you look at the options (Fig 14.2).
4. **Draw generations on levels.** Put grandparents on the top row, parents in the middle and children at the bottom, with a short line for each marriage and each parent–child link. Then move one link at a time. Students who do the whole chain in their heads often swap "uncle" and "cousin".
5. **A right turn depends on the direction you face.** Facing North, right is East; facing East, right is South; facing South, right is West. A left turn goes the other way round the compass, and a U-turn reverses (Fig 14.3). Track the facing direction after every leg, not just the lengths.
6. **Displacement is not distance walked.** In the 10 m, 6 m, 2 m walk the distance walked is 18 m but the displacement is only 10 m from the start (Fig 14.3). For legs at right angles use $\sqrt{a^2+b^2}$ and name the direction using the final north–south and east–west moves. A shadow in the morning falls to the west.
7. **Rankings overlap by one person.** Rank 12 from the top and 30 from the bottom gives $12+30-1=41$, not 42 (Fig 14.4). The same $L+R-1$ rule holds for positions from left and right. To find the rank from the bottom use $N-T+1$.
8. **"All A are B" does not mean "All B are A".** In a syllogism accept only a conclusion that is true in every possible picture (Fig 14.5). From "all A are B, some B are C" nothing follows about A and C, because the C circle may lie outside A. Look out for options that turn a "some" statement into an "all" statement.

### 14.5.1 Worked checks

**Q. In a code CAT is written XZG. How is DOG written?**

**Answer.** Each letter is replaced by its opposite, the letter at position $27-n$: C(3) becomes X(24), A(1) becomes Z(26), T(20) becomes G(7). So D(4) becomes W(23), O(15) becomes L(12), G(7) becomes T(20). DOG is written **WLT**.

**Q. Ram is 12th from the top and 30th from the bottom of a class. How many students are in the class?**

**Answer.** Ram is counted in both ranks, so the class size is $12+30-1=41$. Check: the rank from the bottom is $41-12+1=30$, which agrees with the question (Fig 14.4).

**Q. A man walks 10 m North, turns right and walks 6 m, then turns right and walks 2 m. How far is he from the start and in which direction?**

**Answer.** After the first right turn he faces East and after the second he faces South. His position is 6 m east and $10-2=8$ m north of the start. The distance is $\sqrt{6^2+8^2}=10$ m, towards the north-east (Fig 14.3).

**Q. Statements: all pens are books; some books are cups. Does "some pens are cups" follow?**

**Answer.** No. Pens lie inside books, but the cups that are books may all sit outside the pens, so nothing definite follows about pens and cups. This is case (b) of Fig 14.5.

## Formula and fact sheet

| Type | Rule |
|---|---|
| Opposite letter | position $=27-n$ |
| Ranking | total $=T+B-1$ |
| Displacement | $\sqrt{a^2+b^2}$ |
| Syllogism | "All A are B" ⇏ "All B are A" |

## Chapter summary

- Decode with the first letter, test on the second.
- Draw the family tree; take one link at a time.
- Right turn clockwise, left turn anticlockwise.
- Rankings overlap by exactly one person.
- A conclusion must follow from the statements alone.

## Practice questions

**Set A — Recall (20 questions)**

1. If A=1, B=2, …, the sum of the values of the letters in CAB is
   (a) 5 (b) 6 (c) 7 (d) 9
2. The letter opposite to E in the alphabet (A↔Z) is
   (a) U (b) W (c) T (d) V
3. If each letter is replaced by the next, CAT is written
   (a) DBU (b) BZS (c) DAU (d) CBU
4. If MIND is coded NJOE, then BOOK is coded
   (a) CPQL (b) APNJ (c) CPPL (d) CQPL
5. Pointing to a man, a woman says, "He is the son of my mother's only son." The man is her
   (a) son (b) nephew (c) brother (d) cousin
6. My father's only sister's son is my
   (a) cousin (b) uncle (c) brother (d) nephew
7. Facing north, a person turns right and then right again. He now faces
   (a) north (b) east (c) west (d) south
8. A man walks 3 km east and then 4 km north. His distance from the start is
   (a) 7 km (b) 1 km (c) 5 km (d) 12 km
9. A student is 7th from the top and 14th from the bottom. The class has
   (a) 20 students (b) 21 students (c) 22 students (d) 19 students
10. All pens are books and all books are bags. Which conclusion follows?
    (a) All bags are pens (b) All books are pens (c) Some bags are not books (d) All pens are bags
11. "No A is B" implies
    (a) all B are A (b) no B is A (c) some A are B (d) some B are A
12. In the morning, a man's shadow falls towards the
    (a) east (b) north (c) west (d) south
13. If ROSE is TQUG, then LAKE is
    (a) NCMG (b) MBLF (c) JYIC (d) NDMH
14. Pointing to a girl, Ram says, "She is the daughter of my father's only son." The girl is Ram's
    (a) sister (b) niece (c) mother (d) daughter
15. A person facing east turns left through 90°. He now faces
    (a) south (b) east (c) north (d) west
16. A mother's brother is called a
    (a) paternal uncle (b) maternal uncle (c) cousin (d) nephew
17. Ram is 10th from the left and 15th from the right in a row. The row has
    (a) 24 persons (b) 25 persons (c) 23 persons (d) 26 persons
18. "Some A are B" implies
    (a) all A are B (b) no A is B (c) some B are A (d) all B are A
19. The direction opposite to north-east is
    (a) north-west (b) south-east (c) north (d) south-west
20. If Z=1, Y=2, …, A=26, the value of C is
    (a) 3 (b) 24 (c) 23 (d) 25

::: note Answers and explanations — Set A
**1.** (b) — 3 + 1 + 2 = 6.
**2.** (d) — E is the 5th letter; 27 − 5 = 22 is V.
**3.** (a) — C→D, A→B, T→U.
**4.** (c) — each letter moves +1: B→C, O→P, O→P, K→L.
**5.** (b) — her mother's only son is her brother; his son is her nephew.
**6.** (a) — a father's sister's child is a cousin.
**7.** (d) — right of north is east, right again is south.
**8.** (c) — √(9 + 16) = 5.
**9.** (a) — 7 + 14 − 1 = 20.
**10.** (d) — chains of "all" statements link up in the same direction.
**11.** (b) — "no A is B" is symmetric.
**12.** (c) — the sun is in the east, so the shadow points west.
**13.** (a) — shift +2 on each letter.
**14.** (d) — her father's only son is Ram himself, so she is his daughter.
**15.** (c) — a left turn from east faces north.
**16.** (b) — a mother's brother is a maternal uncle.
**17.** (a) — 10 + 15 − 1 = 24.
**18.** (c) — "some" statements are symmetric; (d) is the classic trap.
**19.** (d) — directly opposite.
**20.** (b) — C is the 24th letter from the end.
:::

**Set B — Understanding (12 questions)**

1. If TABLE is coded UBCMF, then CHAIR is coded
   (a) DHBJS (b) BGZHQ (c) DIBJS (d) DJBIS
2. In a code, the value of a word is the sum of its letter positions (A=1). The value of NO is
   (a) 29 (b) 28 (c) 30 (d) 27
3. A man walks 10 m north, turns right and walks 6 m, then turns right again and walks 10 m. His distance from the start is
   (a) 26 m (b) 10 m (c) 16 m (d) 6 m
4. A man walks 8 km west and then 6 km south. His distance from the start is
   (a) 14 km (b) 10 km (c) 2 km (d) 48 km
5. A is B's sister, C is B's mother, D is C's father and E is D's mother. A is related to D as
   (a) daughter (b) niece (c) granddaughter (d) sister
6. Pointing to a photograph, Rita says, "He is the son of the only son of my grandfather." The man is Rita's
   (a) brother (b) uncle (c) cousin (d) father
7. In a class of 40, Hari ranks 12th from the top. His rank from the bottom is
   (a) 27th (b) 28th (c) 30th (d) 29th
8. A person facing north turns 90° left and then turns 180°. He now faces
   (a) west (b) east (c) north (d) south
9. Statements: All roses are flowers. Some flowers fade. Conclusions: I. Some roses fade. II. All flowers are roses. Which follows?
   (a) neither I nor II (b) only I (c) only II (d) both I and II
10. Find the odd one out: 8, 27, 64, 100
    (a) 8 (b) 27 (c) 100 (d) 64
11. Find the odd one out: Delhi, Kathmandu, Colombo, Mumbai
    (a) Delhi (b) Kathmandu (c) Colombo (d) Mumbai
12. Ram is taller than Hari and Hari is taller than Sita. The shortest is
    (a) Ram (b) Sita (c) Hari (d) cannot be determined

::: note Answers and explanations — Set B
**1.** (c) — +1 each: C→D, H→I, A→B, I→J, R→S.
**2.** (a) — 14 + 15 = 29.
**3.** (d) — he ends 6 m east of the start: 10 north, 6 east, then 10 south.
**4.** (b) — 6-8-10 triangle.
**5.** (c) — A is B's sister and C is B's mother, so C is also A's mother; D is C's father, so A is D's granddaughter.
**6.** (a) — grandfather's only son is her father; his son is her brother.
**7.** (d) — 40 − 12 + 1 = 29.
**8.** (b) — left of north is west; turning 180° faces east.
**9.** (a) — "some flowers fade" says nothing about roses.
**10.** (c) — 8, 27 and 64 are cubes; 100 is not.
**11.** (d) — Mumbai is not a capital.
**12.** (b) — Ram > Hari > Sita.
:::

**Set C — Application (8 questions)**

1. A man walks 5 km east and then 12 km north. His shortest distance from the start is
   (a) 17 km (b) 7 km (c) 60 km (d) 13 km
2. If letters are replaced by their positions, the sum for DOG (D=4, O=15, G=7) is
   (a) 26 (b) 24 (c) 28 (d) 22
3. Hari is 15th from the top and 20th from the bottom. The class has
   (a) 35 students (b) 36 students (c) 34 students (d) 33 students
4. All lawyers are graduates and Ramesh is a lawyer. Which conclusion follows?
   (a) Ramesh is not a graduate (b) Ramesh is a graduate (c) All graduates are lawyers (d) Some graduates are not lawyers
5. A is the brother of B, B is the sister of C and C is the father of D. D is A's
   (a) son (b) brother (c) cousin (d) nephew or niece
6. A person facing east turns through 180° and then turns left. He now faces
   (a) south (b) north (c) east (d) west
7. Find the odd one out: 3, 5, 7, 9, 11
   (a) 3 (b) 5 (c) 9 (d) 11
8. Pointing to a woman, a man says, "Her mother is the only daughter of my mother." The woman is the man's
   (a) sister (b) niece (c) daughter (d) mother

::: note Answers and explanations — Set C
**1.** (d) — 5-12-13 triple.
**2.** (a) — 4 + 15 + 7 = 26.
**3.** (c) — 15 + 20 − 1 = 34.
**4.** (b) — the only valid deduction; the others reverse or extend the premises.
**5.** (d) — C is A's sibling, so D is A's nephew or niece (sex not given).
**6.** (a) — turning 180° faces west; a left turn from west faces south.
**7.** (c) — the others are prime.
**8.** (b) — his mother's only daughter is his sister, so the woman is his niece.
:::
