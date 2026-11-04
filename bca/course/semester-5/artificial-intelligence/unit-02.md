---
subject: Artificial Intelligence
grade: BCA Semester 5
unit: 2
title: Problem Solving Methods
hours: 9
area: BCA 302 · Artificial Intelligence · Unit 2
---

Find the quickest route from Kathmandu to Pokhara; solve a sliding-tile puzzle; colour a map with three colours so that no neighbours match; play tic-tac-toe perfectly. These are very different problems with one structure in common: you have a **start**, a set of possible **moves** and a **goal**, and the answer is a sequence of moves. This unit turns them into a graph and searches the graph, first blindly, then guided by a heuristic, then in the presence of an opponent. Every trace in this unit was produced by `bca/tools/check_ai.py` and the programs at the end.

::: key What this unit gives you
- Problem formulation and the state space; measuring a search algorithm.
- Uninformed search: breadth-first, depth-first, uniform-cost, depth-limited, iterative deepening.
- Informed search: greedy best-first and A*, admissible and consistent heuristics; local search and simulated annealing.
- Constraint satisfaction problems and backtracking.
- Adversarial search: minimax and alpha–beta pruning.
:::

## 2.1 Formulating a search problem

A **well-defined problem** has five components: the **initial state**; the **actions** available in each state; a **transition model** (the state produced by an action); a **goal test**; and a **path cost** (usually the sum of **step costs**). A **solution** is a path from the initial state to a goal state; an **optimal** solution has the least cost. The set of all states reachable from the start is the **state space**, drawn as a graph whose nodes are states and edges are actions.

::: example Formulating the 8-puzzle
State: the position of the eight tiles and the blank (9!/2 = 181,440 reachable states). Initial state: any solvable arrangement. Actions: move the blank up, down, left or right. Transition model: swap the blank with the neighbouring tile. Goal test: tiles in order. Path cost: 1 per move. Half of the 9! = 362,880 arrangements are unreachable from any given start (parity), which is why a random arrangement may have no solution.
:::

A search algorithm builds a **search tree** from the start by *expanding* nodes (generating their successors). The **frontier** (open list) holds nodes generated but not yet expanded; the **explored set** (closed list) prevents revisiting states. Algorithms differ only in which frontier node is expanded next.

### Measuring performance

| Criterion | Question |
|---|---|
| Completeness | If a solution exists, is it always found? |
| Optimality | Is the solution found the cheapest? |
| Time complexity | How many nodes are generated? |
| Space complexity | How many nodes are stored? |

Complexity uses **b** (branching factor, successors per node), **d** (depth of the shallowest goal) and **m** (maximum depth of the space).

## 2.2 The example graph

Most traces below use one small graph so that the algorithms can be compared directly. Edge costs: S–A 2, S–B 5, A–B 2, A–C 4, B–C 1, B–D 7, C–G 3, D–G 2. Start S, goal G. Where order matters, neighbours are taken alphabetically.

## 2.3 Uninformed (blind) search

These strategies use only the problem definition, with no knowledge of how promising a state is.

### Breadth-first search (BFS)

Expand the shallowest node first, using a FIFO queue. Complete (if b is finite) and optimal *when all step costs are equal*. Time and space O(b^d): memory is the killer. On the example graph BFS expands S, A, B, C, D, G and returns S → A → C → G with **3 edges but cost 9**: it finds the path with the fewest steps, not the cheapest.

### Depth-first search (DFS)

Expand the deepest node first, using a LIFO stack. Space is only O(b·m) and it finds deep solutions quickly, but it is **not optimal** and, in infinite or cyclic spaces without an explored set, **not complete**. In the example the expansion order is S, A, B, C, G and the path S → A → B → C → G happens to cost 8; with a different neighbour order it would not.

### Uniform-cost search (UCS)

Expand the node with the lowest path cost g(n) first (a priority queue); this is Dijkstra's algorithm. Complete and optimal for non-negative step costs. In the example the nodes are expanded in the order S (0), A (2), B (4), C (5), G (8) and the optimal path S → A → B → C → G of cost 8 is found; note that B is reached first at cost 5 directly from S but later at cost 4 through A, and UCS keeps the cheaper.

### Depth-limited and iterative deepening search

**Depth-limited search** is DFS with a depth limit l, which stops infinite descent but is incomplete if l < d. **Iterative deepening DFS (IDDFS)** repeats depth-limited search with l = 0, 1, 2, … until the goal is found, combining DFS's low memory with BFS's completeness and (for equal step costs) optimality. The repeated work looks wasteful but is not, because most nodes are at the bottom level. With b = 10 and d = 5, BFS generates 1 + 10 + 100 + 1,000 + 10,000 + 100,000 = **111,111** nodes, and IDDFS generates 6 + 5×10 + 4×100 + 3×1,000 + 2×10,000 + 1×100,000 = **123,456**: only 11 % more. On the example graph IDDFS succeeds at limit 3 with S → A → C → G.

| Algorithm | Complete | Optimal | Time | Space |
|---|---|---|---|---|
| BFS | yes | yes (equal costs) | O(b^d) | O(b^d) |
| DFS | no (cycles, infinite depth) | no | O(b^m) | O(b m) |
| UCS | yes | yes | O(b^(1 + C*/ε)) | same |
| Depth-limited | no if l < d | no | O(b^l) | O(b l) |
| IDDFS | yes | yes (equal costs) | O(b^d) | O(b d) |

**Bidirectional search** runs two searches (from start and from goal) that meet in the middle, giving O(b^(d/2)) each: for b = 10 and d = 6 that is about 2 × 1,000 nodes instead of 1,000,000.

## 2.4 Informed (heuristic) search

An **evaluation function** f(n) estimates the desirability of a node. A **heuristic** h(n) estimates the cheapest cost from n to a goal (h = 0 at the goal). The example graph's heuristic is h(S) = 6, h(A) = 5, h(B) = 3, h(C) = 2, h(D) = 2, h(G) = 0.

### Greedy best-first search

f(n) = h(n): always expand the node that *looks* closest to the goal. Fast, but neither complete (it can loop) nor optimal. Here greedy expands S (6), B (3), C (2), G (0) and returns S → B → C → G with **cost 9**: it ignored the cost already paid.

### A* search

**f(n) = g(n) + h(n)**: the cost so far plus the estimated cost to go. A* is **complete** and **optimal** if the heuristic is **admissible** (never overestimates: h(n) ≤ h*(n), the true remaining cost) for tree search, and **consistent** (monotone: h(n) ≤ c(n, n′) + h(n′) for every edge) for graph search. Consistency implies admissibility and guarantees that f never decreases along a path, so the first time a node is expanded the path is optimal.

::: example A* on the example graph
The true costs to the goal are h*(S) = 8, h*(A) = 6, h*(B) = 4, h*(C) = 3, h*(D) = 2, so h ≤ h* everywhere (admissible) and every edge satisfies h(n) ≤ c + h(n′) in both directions (consistent). The expansions:

| Expanded | g | h | f = g + h | Note |
|---|---|---|---|---|
| S | 0 | 6 | 6 | frontier: A (7), B (5 + 3 = 8) |
| A | 2 | 5 | 7 | B improves to g = 4, f = 7; C: g = 6, f = 8 |
| B | 4 | 3 | 7 | C improves to g = 5, f = 7; D: g = 11, f = 13 |
| C | 5 | 2 | 7 | G: g = 8, f = 8 |
| G | 8 | 0 | 8 | goal: path S → A → B → C → G, cost **8** |

A* found the optimum (8) where greedy found 9, expanding fewer nodes than UCS would on a large graph.
:::

### Designing heuristics: the 8-puzzle

Two classic admissible heuristics: **h₁ = number of misplaced tiles** and **h₂ = sum of Manhattan distances** of the tiles from their goal squares. Both are exact costs of **relaxed problems** (tiles may jump anywhere; tiles may move onto occupied squares) and h₂ ≥ h₁, so h₂ **dominates** h₁ and is never worse. For the start state 2 6 5 / 4 3 8 / 7 1 _ (goal 1 2 3 / 4 5 6 / 7 8 _), h₁ = 6 and h₂ = 12; the optimal solution has 16 moves. A* expanded **144 nodes with h₂**, **565 with h₁** and **8,166 with h = 0** (which is uniform-cost search): a better heuristic prunes more. The hardest 8-puzzle positions need 31 moves; A* with Manhattan distance expands 21,198 nodes for one of them. The effective branching factor shows the same story: the better the heuristic, the nearer to 1.

::: note Combining heuristics
If h₁ and h₂ are both admissible, so is max(h₁, h₂), and it dominates both. Heuristics can also come from **pattern databases** (exact costs of solving a subset of the tiles).
:::

### Memory-bounded variants

**IDA\*** performs iterative deepening on the f-limit; **RBFS** and **SMA\*** keep memory bounded. **Weighted A\*** (f = g + w·h with w > 1) trades optimality for speed.

## 2.5 Local search and optimisation

When the path does not matter, only the final state does (n-queens, timetables, circuit layout), **local search** keeps a *single* current state and moves to neighbours, using constant memory.

- **Hill climbing**: move to the best neighbour; stop when none is better. It gets stuck on **local maxima**, **plateaus** and **ridges**. Remedies: random restarts, sideways moves, stochastic hill climbing.
- **Simulated annealing**: accept a worsening move of size ΔE with probability e^(−ΔE/T), and lower the temperature T slowly. At high T it explores (ΔE = 2 is accepted with probability e^(−2/10) = 0.8187 when T = 10); at low T it is nearly greedy (e^(−2/1) = 0.1353 when T = 1). With a slow enough cooling schedule it finds the global optimum with probability approaching 1.
- **Local beam search** keeps k states; **genetic algorithms** (Unit 4) combine pairs of states.

## 2.6 Constraint satisfaction problems

A **CSP** has variables X₁ … Xₙ, a **domain** for each and **constraints** over subsets. A solution assigns every variable a value satisfying all constraints. Because the structure is explicit, algorithms can reject whole branches early.

::: example Map colouring
Variables: the regions WA, NT, SA, Q, NSW, V, T of the classic Australian map. Domain: {red, green, blue}. Constraints: neighbouring regions differ (WA–NT, WA–SA, NT–SA, NT–Q, SA–Q, SA–NSW, SA–V, Q–NSW, NSW–V). With three colours there are exactly **18** solutions (6 for the mainland times 3 for isolated Tasmania); with two colours there are none, because WA, NT and SA form a triangle.
:::

**Backtracking search** assigns one variable at a time and backtracks when a constraint is violated; in the fixed order WA, NT, SA, Q, NSW, V, T it makes a solution in **8 search nodes** (the root plus 7 assignments) without ever having to backtrack. Better ordering and pruning:

- **MRV** (minimum remaining values): choose the variable with the fewest legal values (fail first).
- **Degree heuristic**: choose the variable involved in most constraints.
- **Least-constraining value**: try the value that rules out the fewest values for neighbours.
- **Forward checking**: after an assignment, delete inconsistent values from neighbours' domains; fail if a domain empties. **Arc consistency (AC-3)** goes further.

Other CSPs: Sudoku, scheduling exams so no student has two at once, assigning Nepali radio frequencies so near stations differ.

## 2.7 Adversarial search and games

In a two-player, zero-sum, perfect-information game (chess, tic-tac-toe) the players alternate. A game is defined by an initial state, the player to move, actions, a transition model, a **terminal test** and a **utility** (+1 win, 0 draw, −1 loss for MAX).

### Minimax

MAX tries to maximise the utility, MIN to minimise it, and both play optimally. The **minimax value** of a node: the utility if terminal; the maximum of the children's values at a MAX node; the minimum at a MIN node. The algorithm is a depth-first recursion; time O(b^m), space O(b m).

::: example Minimax on an eight-leaf tree
The tree is MAX (root) → two MIN nodes → each with two MAX nodes → each with two leaves: leaves 3, 5 | 6, 9 | 1, 2 | 0, −1. The lowest MAX nodes take maxima 5, 9, 2, 0; the MIN nodes take minima min(5, 9) = 5 and min(2, 0) = 0; the root takes max(5, 0) = **5**.
:::

### Alpha–beta pruning

Keep two bounds: **α** (the best value MAX can already guarantee on the path) and **β** (the best MIN can guarantee). If at any node α ≥ β, the remaining children cannot influence the result and are **pruned**. The result is *identical* to minimax, with fewer nodes evaluated.

::: example Alpha–beta on the same tree
Evaluating left to right: the first MAX node reads 3, 5 and returns 5, so the first MIN node has β = 5. The second MAX node reads 6: α = 6 ≥ β = 5, so the leaf **9 is pruned**. The root now has α = 5. In the right subtree, the first MAX node reads 1 and 2 and returns 2, so the MIN node has β = 2; now α = 5 ≥ β = 2, so the whole MAX node (0, −1) is **pruned**. Value 5, with **5 of the 8 leaves** examined (3, 5, 6, 1, 2).
:::

A second example is the 2-ply tree MAX → three MIN nodes with leaves (3, 12, 8), (2, 4, 6), (14, 5, 2). Minimax gives min values 3, 2, 2 and root value **3**. With alpha–beta the leaves 3, 12, 8, 2, 14, 5, 2 are examined (7 of 9): after reading 2 in the second MIN node (2 < α = 3) the leaves 4 and 6 are skipped. A larger 27-leaf tree evaluates 22 leaves and returns the same value, 10.

With **perfect move ordering** alpha–beta examines O(b^(m/2)) nodes, effectively doubling the search depth (or letting b become √b). Tic-tac-toe shows the effect: the complete game tree has **549,946** nodes (**255,168** complete games) and minimax visits all of them, finding the value **0** (a draw with optimal play). Alpha–beta with the plain left-to-right move order visits **18,297** nodes, about 3.3 % of that. Real game programs use an **evaluation function** at a depth cutoff, iterative deepening, transposition tables and good move ordering. **Stochastic games** (backgammon) add chance nodes and use *expectiminimax*; **Monte-Carlo tree search** (AlphaGo) replaces the exact evaluation by random playouts.

## Practising the commands

The first program runs the five search algorithms and A* on the example graph and prints the expansion order and path cost of each.

```python
import heapq
from collections import deque
E = {("S","A"):2, ("S","B"):5, ("A","B"):2, ("A","C"):4, ("B","C"):1, ("B","D"):7, ("C","G"):3, ("D","G"):2}
G = {}
for (a, b), c in E.items(): G.setdefault(a, {})[b] = c; G.setdefault(b, {})[a] = c
H = {"S": 6, "A": 5, "B": 3, "C": 2, "D": 2, "G": 0}
cost = lambda p: sum(G[a][b] for a, b in zip(p, p[1:]))
def bfs():
    q = deque([["S"]]); seen = {"S"}; order = []
    while q:
        p = q.popleft(); order.append(p[-1])
        if p[-1] == "G": return p, order
        for m in sorted(G[p[-1]]):
            if m not in seen: seen.add(m); q.append(p + [m])
def dfs():
    st = [["S"]]; seen = set(); order = []
    while st:
        p = st.pop()
        if p[-1] in seen: continue
        seen.add(p[-1]); order.append(p[-1])
        if p[-1] == "G": return p, order
        for m in sorted(G[p[-1]], reverse=True):
            if m not in seen: st.append(p + [m])
def best_first(f):
    pq = [(f("S", 0), 0, ["S"])]; best = {}; order = []; tie = 0
    while pq:
        _, _, p = heapq.heappop(pq); n = p[-1]; g = cost(p)
        if n in best and best[n] <= g: continue
        best[n] = g; order.append((n, g))
        if n == "G": return p, order
        for m in sorted(G[n]):
            tie += 1; heapq.heappush(pq, (f(m, g + G[n][m]), tie, p + [m]))
for name, (path, order) in [("BFS", bfs()), ("DFS", dfs()), ("UCS", best_first(lambda n, g: g)),
                            ("Greedy", best_first(lambda n, g: H[n])), ("A*", best_first(lambda n, g: g + H[n]))]:
    print(f"{name:7s} path={'-'.join(path)} cost={cost(path)} expanded={order}")
```
```output
BFS     path=S-A-C-G cost=9 expanded=['S', 'A', 'B', 'C', 'D', 'G']
DFS     path=S-A-B-C-G cost=8 expanded=['S', 'A', 'B', 'C', 'G']
UCS     path=S-A-B-C-G cost=8 expanded=[('S', 0), ('A', 2), ('B', 4), ('C', 5), ('G', 8)]
Greedy  path=S-B-C-G cost=9 expanded=[('S', 0), ('B', 5), ('C', 6), ('G', 9)]
A*      path=S-A-B-C-G cost=8 expanded=[('S', 0), ('A', 2), ('B', 4), ('C', 5), ('G', 8)]
```
The second program checks the minimax and alpha–beta examples and counts the nodes of the whole tic-tac-toe game tree with and without pruning.

```python
import math
def minimax(t, maxp):
    if not isinstance(t, list): return t
    vals = [minimax(c, not maxp) for c in t]
    return max(vals) if maxp else min(vals)
seen = []
def alphabeta(t, maxp, a, b):
    if not isinstance(t, list): seen.append(t); return t
    v = -math.inf if maxp else math.inf
    for c in t:
        r = alphabeta(c, not maxp, a, b)
        if maxp: v = max(v, r); a = max(a, v)
        else: v = min(v, r); b = min(b, v)
        if a >= b: break
    return v
for tree in ([[[3, 5], [6, 9]], [[1, 2], [0, -1]]], [[3, 12, 8], [2, 4, 6], [14, 5, 2]]):
    seen.clear(); print("minimax", minimax(tree, True), "alpha-beta", alphabeta(tree, True, -math.inf, math.inf), "leaves read", seen)
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(b):
    for x, y, z in LINES:
        if b[x] and b[x] == b[y] == b[z]: return b[x]
def solve(use_ab):
    count = [0]
    def rec(b, p, a, bt):
        count[0] += 1; w = winner(b)
        if w: return 1 if w == "X" else -1
        if all(b): return 0
        v = -2 if p == "X" else 2
        for i in range(9):
            if not b[i]:
                b[i] = p; r = rec(b, "O" if p == "X" else "X", a, bt); b[i] = None
                if p == "X": v = max(v, r); a = max(a, v)
                else: v = min(v, r); bt = min(bt, v)
                if use_ab and a >= bt: break
        return v
    return rec([None] * 9, "X", -2, 2), count[0]
print("tic-tac-toe minimax (value, nodes):", solve(False)); print("with alpha-beta:", solve(True))
```
```output
minimax 5 alpha-beta 5 leaves read [3, 5, 6, 1, 2]
minimax 3 alpha-beta 3 leaves read [3, 12, 8, 2, 14, 5, 2]
tic-tac-toe minimax (value, nodes): (0, 549946)
with alpha-beta: (0, 18297)
```
## 2.8 Seeing the ideas: puzzles, people, games and traced searches

Search is easiest to understand when you can watch it run. Plate 2.1 shows four everyday search problems as real objects: a garden maze, Claude Shannon's maze-solving mouse, a country road between two towns and a sliding puzzle. Plate 2.2 shows three people behind the algorithms of this unit: Edsger Dijkstra (shortest paths), Claude Shannon (the first chess-programming paper) and the Shakey team at SRI, where A* was invented. Plates 2.3 and 2.4 show the board games on which adversarial search is tested. Figures 2.1 to 2.11 then run the algorithms: every count, path and value printed on them is computed by the figure code itself.

```photogrid label="2.1" cols="4" ratio="1.0" caption="Four search problems. (a) The hedge maze at Glendurgan Garden, Cornwall (CC0): a maze is a graph whose nodes are junctions and whose edges are paths, and depth-first search is exactly what a walker does when she keeps turning left. (b) Claude Shannon's 1952 maze-solving mouse Theseus in the MIT Museum (CC0): the first machine that learned a maze by trial and error and then ran it without a mistake. (c) The Prithvi Highway near Malekhu (CC BY-SA 4.0), part of the Kathmandu to Pokhara route: a map application turns such roads into a weighted graph and runs a shortest-path search. (d) A sliding puzzle (CC0): each arrangement is a state, each slide is an action, and the state space is searched for the goal arrangement."
@ photo id="bca302/maze" cap="Hedge maze: paths as a graph"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/theseus" cap="Shannon's mouse Theseus (1952)"
fit 1.0
focus 0.55 0.45
@ photo id="bca302/highway" cap="Prithvi Highway, Malekhu"
fit 1.0
focus 0.5 0.6
@ photo id="bca302/sliding" cap="Sliding puzzle: states and moves"
fit 1.0
focus 0.4 0.4
```

```photogrid label="2.2" cols="3" ratio="1.0" caption="Three people behind the algorithms. (a) Edsger Dijkstra, who published the shortest-path algorithm in 1959; uniform-cost search is its form for implicit graphs (CC BY-SA 4.0). (b) Claude Shannon in 1958 (public domain), whose 1950 paper 'Programming a Computer for Playing Chess' described minimax evaluation of positions. (c) Members of the Shakey team at the 2017 IEEE plaque dedication (CC BY-SA 4.0): the A* algorithm (Hart, Nilsson and Raphael, 1968) was invented at SRI to let the Shakey robot plan its routes."
@ photo id="bca301/dijkstra" cap="Edsger Dijkstra: shortest paths"
fit 1.0
focus 0.35 0.45
@ photo id="bca302/shannon" cap="Claude Shannon: minimax for chess"
fit 1.0
focus 0.4 0.4
@ photo id="bca302/shakeyteam" cap="Shakey team: birthplace of A*"
fit 1.0
focus 0.5 0.4
```

```photogrid label="2.3" cols="2" ratio="1.0" caption="A search space you can hold. (a) A chessboard seen from above (CC0): 8 rows and 8 columns of squares. The eight-queens problem asks for eight queens that attack no other queen. (b) The first solution found by the backtracking search of Fig. 2.7, computed by the figure code: queens in columns 1, 5, 8, 6, 3, 7, 2 and 4 of rows 1 to 8, so no two share a row, a column or a diagonal. Of the 16,777,216 ways to put one queen in each row, only 92 are solutions."
@ photo id="bca302/chess" cap="Chessboard: 8 x 8 squares"
fit 1.0
focus 0.5 0.5
call 0.6 0.94 0.5 0.8 "row 1"
@ svg cap="First backtracking solution"
f = Fig(300, 300)
cols = []
def ok(c, r):
    return all(c != cc and abs(c - cc) != r - rr for rr, cc in enumerate(cols))
def place(r):
    if r == 8: return True
    for c in range(8):
        if ok(c, r):
            cols.append(c)
            if place(r + 1): return True
            cols.pop()
    return False
assert place(0) and cols == [0, 4, 7, 5, 2, 6, 1, 3]
for r in range(8):
    for c in range(8):
        f.box(30 + c * 30, 6 + r * 30, 30, 30, "", fill="#e2e8f0" if (r + c) % 2 else "#ffffff", stroke="#94a3b8", r=0, sw=0.8)
    f.circle(30 + cols[r] * 30 + 15, 6 + r * 30 + 15, 11, fill=NAVY, stroke=NAVY, label="Q", size=12, color="#ffffff")
for k in range(8):
    f.text(30 + k * 30 + 15, 262, str(k + 1), size=12, color=SLATE, bold=True)
f.text(150, 284, "column of the queen in rows 1 to 8", size=12, color=NAVY, bold=True)
```

```photogrid label="2.4" cols="3" ratio="1.0" caption="Games as search trees. (a) A tic-tac-toe set (CC BY-SA 4.0). (b) Garry Kasparov (left) playing Anatoly Karpov in Amsterdam (CC0): chess has about 35 legal moves per position and games of about 80 plies, so a full game tree is impossible and programs search a few plies with an evaluation function and alpha-beta pruning. (c) A real tic-tac-toe position computed by the figure code with minimax: X has 0 and 1, O has 3 and 4, and it is X's move. Playing at square 2 wins (+1), blocking at square 5 draws (0), and any other move loses (-1) because O then completes 3-4-5."
@ photo id="bca302/tictactoe" cap="Tic-tac-toe: a small game tree"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/kasparov" cap="Kasparov vs Karpov: a huge game tree"
fit 1.0
focus 0.5 0.5
@ svg cap="Minimax value of each move"
f = Fig(300, 300)
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def win(b):
    for x, y, z in LINES:
        if b[x] and b[x] == b[y] == b[z]: return b[x]
def val(b, p):
    w = win(b)
    if w: return 1 if w == "X" else -1
    if all(b): return 0
    r = [val(b[:i] + [p] + b[i+1:], "O" if p == "X" else "X") for i in range(9) if not b[i]]
    return max(r) if p == "X" else min(r)
b0 = ["X", "X", None, "O", "O", None, None, None, None]
vals = {i: val(b0[:i] + ["X"] + b0[i+1:], "O") for i in range(9) if not b0[i]}
assert vals == {2: 1, 5: 0, 6: -1, 7: -1, 8: -1}
for i in range(9):
    x, y = 24 + (i % 3) * 84, 18 + (i // 3) * 84
    if b0[i]:
        f.box(x, y, 78, 78, b0[i], fill="#f1f5f9", stroke="#94a3b8", r=6, size=34, bold=True, color=NAVY if b0[i] == "X" else RED)
    else:
        v = vals[i]
        fl, st = ("#bbf7d0", TEAL) if v == 1 else (SAND, AMBER) if v == 0 else ("#fecaca", RED)
        f.box(x, y, 78, 78, "", fill=fl, stroke=st, r=6, sw=2)
        f.text(x + 39, y + 28, "X at %d" % i, size=12, color=NAVY, bold=True)
        f.text(x + 39, y + 56, "%+d" % v if v else "0", size=22, color=st, bold=True)
f.text(150, 284, "squares 0 to 8, left to right, top to bottom", size=12, color=SLATE)
```

```svgfig label="2.1" caption="The example graph of Section 2.2 and what each algorithm does with it. Each circle is a state with its heuristic h(n) in red; edge labels are step costs. The table runs the five algorithms in the figure code, with neighbours taken alphabetically: breadth-first search expands 6 nodes and returns S-A-C-G of cost 9 (the fewest edges, 3, but not the cheapest path); depth-first search happens to find the optimal cost 8 after 5 expansions, but only by luck of ordering; uniform-cost search and A* both return the optimal S-A-B-C-G of cost 8 with 5 expansions; greedy best-first search follows the smallest h and returns S-B-C-G of cost 9 with only 4 expansions. Fast and optimal are different properties."
f = Fig(580, 262)
dq = __import__("collections").deque
hp = __import__("heapq")
G = {"S": {"A": 2, "B": 5}, "A": {"S": 2, "B": 2, "C": 4}, "B": {"S": 5, "A": 2, "C": 1, "D": 7}, "C": {"A": 4, "B": 1, "G": 3}, "D": {"B": 7, "G": 2}, "G": {"C": 3, "D": 2}}
H = {"S": 6, "A": 5, "B": 3, "C": 2, "D": 2, "G": 0}
def cost(p): return sum(G[a][b] for a, b in zip(p, p[1:]))
def bfs():
    q = dq([["S"]]); seen = {"S"}; order = []
    while q:
        p = q.popleft(); order.append(p[-1])
        if p[-1] == "G": return p, order
        for m in sorted(G[p[-1]]):
            if m not in seen: seen.add(m); q.append(p + [m])
def dfs():
    st = [["S"]]; seen = set(); order = []
    while st:
        p = st.pop()
        if p[-1] in seen: continue
        seen.add(p[-1]); order.append(p[-1])
        if p[-1] == "G": return p, order
        for m in sorted(G[p[-1]], reverse=True):
            if m not in seen: st.append(p + [m])
def bestfirst(fn):
    pq = [(fn("S", 0), 0, ["S"])]; best = {}; order = []; tie = 0
    while pq:
        _, _, p = hp.heappop(pq); n = p[-1]; g = cost(p)
        if n in best and best[n] <= g: continue
        best[n] = g; order.append(n)
        if n == "G": return p, order
        for m in sorted(G[n]):
            tie += 1; hp.heappush(pq, (fn(m, g + G[n][m]), tie, p + [m]))
runs = [("BFS", bfs()), ("DFS", dfs()), ("UCS", bestfirst(lambda n, g: g)), ("Greedy", bestfirst(lambda n, g: H[n])), ("A*", bestfirst(lambda n, g: g + H[n]))]
res = {k: ("-".join(p), cost(p), len(o)) for k, (p, o) in runs}
assert res["BFS"] == ("S-A-C-G", 9, 6) and res["DFS"] == ("S-A-B-C-G", 8, 5) and res["UCS"] == ("S-A-B-C-G", 8, 5) and res["Greedy"] == ("S-B-C-G", 9, 4) and res["A*"] == ("S-A-B-C-G", 8, 5)
pos = {"S": (34, 128), "A": (116, 44), "B": (116, 214), "C": (220, 128), "D": (230, 224), "G": (306, 128)}
done = set()
for a in G:
    for b, c in G[a].items():
        if (b, a) in done: continue
        done.add((a, b))
        f.line(pos[a][0], pos[a][1], pos[b][0], pos[b][1], color="#64748b", sw=1.8)
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        f.box(mx - 9, my - 9, 18, 18, str(c), fill="#ffffff", stroke="#cbd5e1", size=10.5, r=9, bold=True, color=AMBER, sw=1)
for n, (x, y) in pos.items():
    f.circle(x, y, 17, fill=MINT if n == "G" else SAND if n == "S" else BLUE, stroke=TEAL if n == "G" else AMBER if n == "S" else NAVY, label=n, size=13, sw=2)
    f.text(x, y + 30, "h=%d" % H[n], size=10, color=RED, bold=True)
f.text(170, 16, "states, step costs and heuristic h (start S, goal G)", size=10.5, color=NAVY, bold=True)
f.text(462, 16, "algorithm results (computed)", size=10.5, color=NAVY, bold=True)
for j, hd in enumerate([("algorithm", 352, "start"), ("path", 418, "start"), ("cost", 516, "middle"), ("nodes", 554, "middle")]):
    f.text(hd[1], 40, hd[0], size=10, color=SLATE, bold=True, anchor=hd[2])
for i, (k, _) in enumerate(runs):
    y = 52 + i * 34
    path, c, n = res[k]
    f.box(348, y, 228, 28, "", fill=MINT if c == 8 else SAND, stroke=TEAL if c == 8 else AMBER, r=5, sw=1.2)
    f.text(354, y + 14, k, size=11, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(418, y + 14, path, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(516, y + 14, str(c), size=12, color=TEAL if c == 8 else AMBER, bold=True, vmid=True)
    f.text(554, y + 14, str(n), size=11, color=NAVY, bold=True, vmid=True)
f.text(462, 236, "green = optimal (cost 8), amber = cost 9", size=10, color=SLATE, bold=True)
f.text(462, 252, "nodes = expansions before the goal is selected", size=10, color=SLATE)
```

```svgfig label="2.2" caption="The same binary tree (depth 3, 15 nodes) expanded by breadth-first and depth-first search; the number in each node is the order of expansion, computed by simulating a FIFO queue and a LIFO stack. BFS goes level by level (1, 2-3, 4-7, 8-15), so its frontier grows to 8 nodes, the whole bottom level, which is b to the power d. DFS dives down the left branch (1, 2, 3, 4), backs up and tries the next branch, and its frontier never holds more than 4 nodes, which is why DFS needs memory proportional to b times m while BFS needs b to the power d. Colours show the level for BFS and the subtree for DFS."
f = Fig(580, 262)
dq = __import__("collections").deque
def children(i): return [2 * i, 2 * i + 1] if 2 * i + 1 <= 15 else []
q = dq([1]); border = []; peak_b = 1
while q:
    i = q.popleft(); border.append(i)
    for c in children(i): q.append(c)
    peak_b = max(peak_b, len(q))
st = [1]; dorder = []; peak_d = 1
while st:
    i = st.pop(); dorder.append(i)
    st.extend(reversed(children(i)))
    peak_d = max(peak_d, len(st))
assert border == list(range(1, 16)) and dorder[:5] == [1, 2, 4, 8, 9] and peak_b == 8 and peak_d == 4, (peak_b, peak_d)
def xy(i, ox):
    lvl = i.bit_length() - 1
    j = i - 2 ** lvl
    return ox + (j + 0.5) * 270 / 2 ** lvl, 30 + lvl * 56
for ox, title, order in [(10, "breadth-first (FIFO queue)", border), (300, "depth-first (LIFO stack)", dorder)]:
    f.text(ox + 135, 12, title, size=10.5, color=NAVY, bold=True)
    for i in range(2, 16):
        a = xy(i // 2, ox); b = xy(i, ox)
        f.line(a[0], a[1], b[0], b[1], color="#94a3b8", sw=1.4)
    for i in range(1, 16):
        x, y = xy(i, ox)
        n = order.index(i) + 1
        lvl = i.bit_length() - 1
        if ox == 10:
            fl = [SAND, BLUE, MINT, "#fce7f3"][lvl]; st_ = [AMBER, NAVY, TEAL, "#be185d"][lvl]
        else:
            top = i
            while top > 3: top //= 2
            fl = SAND if i == 1 else (BLUE if top == 2 else MINT); st_ = AMBER if i == 1 else (NAVY if top == 2 else TEAL)
        f.circle(x, y, 12, fill=fl, stroke=st_, label=str(n), size=10.5, sw=1.6)
f.box(10, 210, 270, 40, "frontier peak: %d nodes (= b^d = 2^3)\nmemory O(b^d): the bottom level is stored" % peak_b, fill=SAND, stroke=AMBER, size=10, r=5, color=NAVY)
f.box(300, 210, 270, 40, "frontier peak: %d nodes (about b*m)\nmemory O(b*m): one branch is stored" % peak_d, fill=MINT, stroke=TEAL, size=10, r=5, color=NAVY)
```

```svgfig label="2.3" caption="Why memory, not time, is the killer for breadth-first search. Left: nodes generated (log scale) by BFS, iterative deepening and bidirectional search for branching factor b = 10 and depth d = 2, 4, 6, 8, 10. Iterative deepening repeats the upper levels but generates only 11 percent more nodes than BFS at every depth (123,456,789 against 111,111,111 at d = 8), while bidirectional search needs about the square root of the nodes. Right: BFS must store every node of the frontier; at one million nodes per second and 1 KB per node, depth 10 takes 3.1 hours and 11.1 TB of memory, and depth 14 takes 3.5 years and 111 PB. The computer runs out of memory long before the user runs out of patience."
f = Fig(580, 262)
cm = __import__("math")
b = 10
def bfs_n(d): return sum(b ** i for i in range(d + 1))
def id_n(d): return sum((d + 1 - i) * b ** i for i in range(d + 1))
def bi_n(d): return 2 * sum(b ** i for i in range(d // 2 + 1))
assert bfs_n(8) == 111111111 and id_n(8) == 123456789 and bi_n(6) == 2222
def short(n):
    return str(n) if n < 1000 else "%.1fK" % (n / 1e3) if n < 1e6 else "%.1fM" % (n / 1e6) if n < 1e9 else "%.1fB" % (n / 1e9)
f.text(180, 12, "nodes generated, log scale (b = 10)", size=10.5, color=NAVY, bold=True)
for gi, d in enumerate([2, 4, 6, 8, 10]):
    y0 = 24 + gi * 47
    f.text(6, y0 + 20, "d=%d" % d, size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    for k, (nm, n, fl, st_) in enumerate([("BFS", bfs_n(d), BLUE, NAVY), ("IDDFS", id_n(d), SAND, AMBER), ("bidir", bi_n(d), MINT, TEAL)]):
        w = max(2, cm.log10(n) * 22)
        f.box(40, y0 + k * 14, w, 12, "", fill=fl, stroke=st_, r=2, sw=1)
        f.text(40 + w + 4, y0 + k * 14 + 6, "%s %s" % (nm, short(n)), size=9.5, color=st_, bold=True, anchor="start", vmid=True)
f.text(462, 12, "BFS time and memory (1M nodes/s, 1 KB/node)", size=10.5, color=NAVY, bold=True)
def tfmt(s):
    return "%.1f ms" % (s * 1000) if s < 1 else "%.1f s" % s if s < 60 else "%.1f min" % (s / 60) if s < 3600 else "%.1f h" % (s / 3600) if s < 86400 else "%.1f days" % (s / 86400) if s < 365 * 86400 else "%.1f years" % (s / 31536000)
def mfmt(x):
    for u in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if x < 1000: return "%.0f %s" % (x, u) if x >= 100 or u == "B" else "%.1f %s" % (x, u)
        x /= 1000
    return "%.0f EB" % x
assert tfmt(bfs_n(10) / 1e6) == "3.1 h" and mfmt(bfs_n(10) * 1000) == "11.1 TB" and tfmt(bfs_n(14) / 1e6) == "3.5 years" and mfmt(bfs_n(14) * 1000) == "111 PB"
for j, hd in enumerate([("depth", 372), ("time", 462), ("memory", 538)]):
    f.text(hd[1], 34, hd[0], size=10, color=SLATE, bold=True)
for i, d in enumerate([2, 6, 10, 12, 14]):
    y = 42 + i * 40
    bad = d >= 10
    f.box(340, y, 236, 34, "", fill="#fee2e2" if bad else MINT, stroke=RED if bad else TEAL, r=5, sw=1.2)
    f.text(372, y + 17, "d = %d" % d, size=10.5, color=NAVY, bold=True, vmid=True)
    f.text(462, y + 17, tfmt(bfs_n(d) / 1e6), size=10.5, color=SLATE, bold=True, vmid=True)
    f.text(538, y + 17, mfmt(bfs_n(d) * 1000), size=10.5, color=RED if bad else TEAL, bold=True, vmid=True)
```

```svgfig label="2.4" caption="Breadth-first search, greedy best-first search and A* on a 16 by 9 grid, computed in the figure code with a Manhattan-distance heuristic. Blue cells were expanded, the red line is the path found, S is the start and G the goal. In the open field (top) all three find a path of 13 steps, but BFS expands 107 cells in every direction while greedy and A* expand only 14, the cells on the straight line. With a wall that has a gap at the bottom (below) the heuristic points straight into the wall: BFS expands 117 cells, greedy 37 and A* 105, and all find the shortest path of 21 steps. A* still wins, but a heuristic that is misled by obstacles saves much less than one that points the right way."
f = Fig(580, 322)
hp = __import__("heapq")
W, Hh = 16, 9
def run(walls, kind, S=(1, 4), Gl=(14, 4)):
    def hm(c): return abs(c[0] - Gl[0]) + abs(c[1] - Gl[1])
    def nb(c):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < Hh and n not in walls: yield n
    pq = [(0, 0, S)]; g = {S: 0}; par = {S: None}; closed = []; t = 0
    while pq:
        _, _, c = hp.heappop(pq)
        if c in closed: continue
        closed.append(c)
        if c == Gl: break
        for n in nb(c):
            ng = g[c] + 1
            if kind == "greedy":
                if n not in g: g[n] = ng; par[n] = c; t += 1; hp.heappush(pq, (hm(n), t, n))
            elif n not in g or ng < g[n]:
                g[n] = ng; par[n] = c; t += 1; hp.heappush(pq, (ng if kind == "bfs" else ng + hm(n), t, n))
    p = []; c = Gl
    while c: p.append(c); c = par[c]
    return closed, p
wall = set((9, y) for y in range(0, 8))
exp = {}
for sc, walls in (("open", set()), ("wall", wall)):
    for kind in ("bfs", "greedy", "astar"):
        exp[(sc, kind)] = run(walls, kind) + (walls,)
assert [len(exp[("open", k)][0]) for k in ("bfs", "greedy", "astar")] == [107, 14, 14]
assert [len(exp[("wall", k)][0]) for k in ("bfs", "greedy", "astar")] == [117, 37, 105]
assert all(len(exp[k][1]) - 1 == (13 if k[0] == "open" else 21) for k in exp)
names = {"bfs": "BFS", "greedy": "greedy", "astar": "A*"}
for r, sc in enumerate(("open", "wall")):
    y0 = 30 + r * 152
    f.text(290, y0 - 14, "open field" if sc == "open" else "wall with a gap at the bottom (column 9, row 8)", size=10.5, color=NAVY, bold=True)
    for c, kind in enumerate(("bfs", "greedy", "astar")):
        closed, path, walls = exp[(sc, kind)]
        x0 = 8 + c * 192
        f.box(x0, y0, 176, 99, "", fill="#ffffff", stroke="#94a3b8", r=0, sw=1)
        for (x, y) in closed:
            f.box(x0 + x * 11, y0 + y * 11, 11, 11, "", fill="#bfdbfe", stroke="#ffffff", r=0, sw=0.5)
        for (x, y) in walls:
            f.box(x0 + x * 11, y0 + y * 11, 11, 11, "", fill="#334155", stroke="#334155", r=0, sw=0.5)
        f.raw('<polyline points="%s" fill="none" stroke="#dc2626" stroke-width="2.4"/>' % " ".join("%.1f,%.1f" % (x0 + x * 11 + 5.5, y0 + y * 11 + 5.5) for x, y in path))
        f.circle(x0 + 1 * 11 + 5.5, y0 + 4 * 11 + 5.5, 5.5, fill="#16a34a", stroke="#ffffff", label="S", size=9, color="#ffffff", sw=1)
        f.circle(x0 + 14 * 11 + 5.5, y0 + 4 * 11 + 5.5, 5.5, fill=AMBER, stroke="#ffffff", label="G", size=9, color="#ffffff", sw=1)
        f.text(x0 + 88, y0 + 114, "%s: %d expanded, path %d" % (names[kind], len(closed), len(path) - 1), size=10, color=NAVY, bold=True)
```

```svgfig label="2.5" caption="Heuristics for the 8-puzzle, computed by running A* three times on the start state 2 6 5 / 4 3 8 / 7 1 _. In the start board (left) each misplaced tile is amber with its Manhattan distance to its goal square in red: the six misplaced tiles give h1 = 6 and the distances 1 + 2 + 2 + 0 + 2 + 2 + 0 + 3 give h2 = 12. All three searches find the optimal 16-move solution, but the number of nodes expanded differs by a factor of 52: uniform-cost search (h = 0) expands 7,495 nodes, A* with h1 expands 565 and A* with h2 expands 144. h2 is never smaller than h1, so it dominates h1 and prunes more."
f = Fig(580, 210)
hp = __import__("heapq")
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0); start = (2, 6, 5, 4, 3, 8, 7, 1, 0)
def h1(s): return sum(1 for i in range(9) if s[i] and s[i] != goal[i])
def dist(s, i):
    j = goal.index(s[i]); return abs(i // 3 - j // 3) + abs(i % 3 - j % 3)
def h2(s): return sum(dist(s, i) for i in range(9) if s[i])
def nbrs(s):
    z = s.index(0); r, c = divmod(z, 3)
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            l = list(s); k = nr * 3 + nc; l[z], l[k] = l[k], l[z]; yield tuple(l)
def astar(h):
    pq = [(h(start), 0, start)]; g = {start: 0}; cl = set(); n = 0; t = 0
    while pq:
        _, _, s = hp.heappop(pq)
        if s in cl: continue
        cl.add(s); n += 1
        if s == goal: return g[s], n
        for m in nbrs(s):
            if m not in g or g[s] + 1 < g[m]: g[m] = g[s] + 1; t += 1; hp.heappush(pq, (g[m] + h(m), t, m))
r0, rh1, rh2 = astar(lambda s: 0), astar(h1), astar(h2)
assert h1(start) == 6 and h2(start) == 12 and r0 == (16, 7495) and rh1 == (16, 565) and rh2 == (16, 144)
def board(x0, y0, s, show):
    for i in range(9):
        x, y = x0 + (i % 3) * 38, y0 + (i // 3) * 38
        if s[i] == 0:
            f.box(x, y, 36, 36, "", fill="#e2e8f0", stroke="#94a3b8", r=4, sw=1); continue
        bad = s[i] != goal[i] and show
        f.box(x, y, 36, 36, str(s[i]), fill=SAND if bad else MINT, stroke=AMBER if bad else TEAL, r=4, size=15, bold=True, color=NAVY, sw=1.6)
        if bad: f.text(x + 29, y + 9, str(dist(s, i)), size=10, color=RED, bold=True)
f.text(63, 16, "start", size=11, color=NAVY, bold=True)
f.text(183, 16, "goal", size=11, color=NAVY, bold=True)
board(8, 26, start, True); board(128, 26, goal, False)
f.text(120, 154, "h1 = misplaced tiles = %d" % h1(start), size=10.5, color=AMBER, bold=True)
f.text(120, 172, "h2 = sum of distances = %d" % h2(start), size=10.5, color=RED, bold=True)
f.text(120, 192, "optimal solution = %d moves" % r0[0], size=10.5, color=TEAL, bold=True)
f.text(450, 16, "nodes expanded by A* (log scale)", size=11, color=NAVY, bold=True)
for i, (nm, n, fl, st_) in enumerate([("h = 0 (UCS)", r0[1], SAND, AMBER), ("h1", rh1[1], BLUE, NAVY), ("h2", rh2[1], MINT, TEAL)]):
    y = 38 + i * 52
    w = __import__("math").log10(n) * 36
    f.text(330, y + 20, nm, size=10.5, color=SLATE, bold=True, anchor="end", vmid=True)
    f.box(338, y, w, 40, "", fill=fl, stroke=st_, r=3, sw=1.4)
    f.text(338 + w + 6, y + 20, "{:,}".format(n), size=12, color=st_, bold=True, anchor="start", vmid=True)
```

```svgfig label="2.6" caption="Local search on a bumpy landscape, computed in the figure code. Left: f(x) = 2 sin x + sin(3x + 1) + 0.5 sin 7x + 0.15 x has nine local maxima (green); the highest (red) is f = 4.28 at x = 8.35. Hill climbing, which always moves to a better neighbour and stops when none exists, ends on one of the nine peaks depending on where it starts: from 101 evenly spaced starting points only 19 (18.8 percent) reach the highest peak. Right: simulated annealing accepts a worse move of size ΔE with probability e to the power of minus ΔE over T. At ΔE = 2 the probability is 0.8187 when T = 10 (explore freely), 0.5134 when T = 3 and 0.1353 when T = 1 (almost greedy). Cooling T from 3 by half a percent per step, 10 of 20 runs (50 percent) finish on the highest peak, so the occasional downhill move is what lets annealing escape."
f = Fig(580, 280)
cm = __import__("math"); rnd = __import__("random")
def land(x): return cm.sin(x) * 2 + cm.sin(3 * x + 1) + 0.5 * cm.sin(7 * x) + 0.15 * x
def hill(x):
    while True:
        b = max((x - 0.05, x + 0.05), key=land)
        if land(b) <= land(x): return x
        x = b
starts = [i * 0.1 for i in range(101)]
ends = [hill(x) for x in starts]
peaks = sorted(set(round(p, 2) for p in ends))
top = max(peaks, key=land)
hits = sum(1 for p in ends if abs(land(p) - land(top)) < 0.05)
def sa(x, seed):
    r = rnd.Random(seed); T = 3.0
    while T > 0.01:
        y = min(10.2, max(0, x + r.uniform(-0.6, 0.6))); d = land(y) - land(x)
        if d > 0 or r.random() < cm.exp(d / T): x = y
        T *= 0.995
    return x
sah = sum(1 for i in range(20) if land(sa(0.5 + i * 0.45, i)) > 4.1)
assert len(peaks) == 9 and top == 8.35 and round(land(top), 2) == 4.28 and hits == 19 and sah == 10, (peaks, top, hits, sah)
ax = Axes(f, 40, 30, 300, 160, (0, 10.5), (-3.5, 5))
ax.grid(2, 2)
ax.curve(land, color=NAVY, sw=2.2)
for p in peaks:
    g = abs(p - top) < 0.01
    f.circle(ax.X(p), ax.Y(land(p)), 6 if g else 4.5, fill=RED if g else "#22c55e", stroke="#ffffff", sw=1.2)
f.text(ax.X(top) - 10, ax.Y(land(top)) - 12, "highest peak 4.28", size=10, color=RED, bold=True, anchor="end")
f.text(190, 14, "landscape with 9 local maxima (x from 0 to 10.5)", size=10.5, color=NAVY, bold=True)
ax2 = Axes(f, 400, 30, 160, 160, (0, 6), (0, 1))
ax2.grid(2, 0.5)
for T, col in [(10, TEAL), (3, AMBER), (1, RED)]:
    ax2.curve(lambda x, T=T: cm.exp(-x / T), color=col, sw=2.2)
    p = cm.exp(-2 / T)
    f.circle(ax2.X(2), ax2.Y(p), 4, fill=col, stroke="#ffffff", sw=1)
    f.text(ax2.X(2) + 8, ax2.Y(p) - 5, "T=%d: %.4f" % (T, p) if T != 3 else "T=3: %.4f" % p, size=10, color=col, bold=True, anchor="start")
f.text(480, 14, "acceptance probability e^(-ΔE/T)", size=10.5, color=NAVY, bold=True)
f.text(480, 212, "ΔE (how much worse the move is)", size=10, color=SLATE)
f.box(8, 226, 276, 44, "hill climbing, 101 starting points:\n%d reach the highest peak (%.1f%%)" % (hits, hits / 1.01), fill=SAND, stroke=AMBER, size=10.5, r=6, color=NAVY, bold=True)
f.box(296, 226, 276, 44, "simulated annealing, 20 runs:\n%d reach the highest peak (%d%%)" % (sah, sah * 5), fill=MINT, stroke=TEAL, size=10.5, r=6, color=NAVY, bold=True)
```

```svgfig label="2.7" caption="Why the eight-queens problem needs a smarter search than guessing, all counts computed in the figure code. Putting one queen in every row with any column gives 8 to the power 8 = 16,777,216 boards. Insisting on different columns leaves 8! = 40,320. Backtracking, which abandons a partial placement as soon as two queens attack each other, visits only 2,057 nodes (counting the empty board) to find all 92 solutions. The 92 solutions are only 12 genuinely different boards: every other solution is a rotation or a reflection of one of the 12."
f = Fig(580, 188)
cm = __import__("math")
sols = []; nodes = [0]
def q(row, cols):
    nodes[0] += 1
    if row == 8: sols.append(tuple(cols)); return
    for c in range(8):
        if all(c != cc and abs(c - cc) != row - rr for rr, cc in enumerate(cols)):
            q(row + 1, cols + [c])
q(0, [])
def canon(s):
    pts = [(r, c) for r, c in enumerate(s)]
    out = []
    for _ in range(4):
        pts = [(c, 7 - r) for r, c in pts]
        out.append(tuple(sorted(pts))); out.append(tuple(sorted((r, 7 - c) for r, c in pts)))
    return min(out)
fund = len(set(canon(s) for s in sols))
assert len(sols) == 92 and nodes[0] == 2057 and fund == 12 and 8 ** 8 == 16777216 and cm.factorial(8) == 40320
f.text(290, 14, "boards or nodes examined, log scale", size=10.5, color=NAVY, bold=True)
rows = [("one queen per row, any column", 8 ** 8, "#fee2e2", RED), ("different columns too (8!)", cm.factorial(8), SAND, AMBER), ("backtracking nodes", nodes[0], MINT, TEAL), ("solutions found", len(sols), BLUE, NAVY)]
for i, (nm, n, fl, st_) in enumerate(rows):
    y = 26 + i * 34
    w = max(4, cm.log10(n) * 38)
    f.text(206, y + 14, nm, size=10.5, color=SLATE, bold=True, anchor="end", vmid=True)
    f.box(214, y, w, 28, "", fill=fl, stroke=st_, r=3, sw=1.4)
    f.text(214 + w + 6, y + 14, "{:,}".format(n), size=11, color=st_, bold=True, anchor="start", vmid=True)
f.text(290, 172, "92 solutions = %d fundamental boards, each with its rotations and reflections" % fund, size=10.5, color=RED, bold=True)
```

```svgfig label="2.8" caption="Map colouring as a constraint satisfaction problem, with every count computed. Left: the constraint graph of the seven Australian regions (an edge joins neighbours that must differ) coloured with the first solution that backtracking finds when it assigns WA, NT, SA, Q, NSW, V, T in that order and tries red, green, blue: it needs only 8 search nodes (the empty assignment plus 7 assignments) and never backtracks. Trying all 3 to the power 7 = 2,187 colourings shows that exactly 18 are valid. Right: forward checking removes a colour from a neighbour's domain whenever a region takes it. After WA = red, NT = green and SA = blue, Q is left with only red, NSW and V with red or green, and no domain is empty, so no dead end is possible yet."
f = Fig(580, 300)
it = __import__("itertools")
regs = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
adj = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]
nbr = {r: set() for r in regs}
for a, b in adj: nbr[a].add(b); nbr[b].add(a)
cols = ["R", "G", "B"]
cnt = sum(1 for c in it.product(range(3), repeat=7) if all(c[regs.index(a)] != c[regs.index(b)] for a, b in adj))
nodes = [0]; asg = {}
def bt(i):
    nodes[0] += 1
    if i == 7: return True
    for c in cols:
        if all(asg.get(m) != c for m in nbr[regs[i]]):
            asg[regs[i]] = c
            if bt(i + 1): return True
            del asg[regs[i]]
    return False
assert bt(0) and cnt == 18 and nodes[0] == 8 and asg == {"WA": "R", "NT": "G", "SA": "B", "Q": "R", "NSW": "G", "V": "R", "T": "R"}
FILL = {"R": "#fca5a5", "G": "#86efac", "B": "#93c5fd"}; EDGE = {"R": RED, "G": TEAL, "B": NAVY}
pos = {"WA": (44, 140), "NT": (124, 60), "SA": (134, 170), "Q": (222, 60), "NSW": (240, 150), "V": (196, 228), "T": (262, 262)}
for a, b in adj:
    f.line(pos[a][0], pos[a][1], pos[b][0], pos[b][1], color="#64748b", sw=1.8)
for r in regs:
    x, y = pos[r]
    f.circle(x, y, 20, fill=FILL[asg[r]], stroke=EDGE[asg[r]], label=r, size=10.5, color=NAVY, sw=2)
f.text(150, 14, "constraint graph and first solution found", size=10.5, color=NAVY, bold=True)
dom = {r: set(cols) for r in regs}
steps = [("start", dict(dom))]
snap = {r: set(v) for r, v in dom.items()}
snaps = [snap]
for r, c in [("WA", "R"), ("NT", "G"), ("SA", "B")]:
    snap = {k: set(v) for k, v in snap.items()}
    snap[r] = {c}
    for m in nbr[r]:
        if m != r and len(snap[m]) > 1: snap[m].discard(c)
    snaps.append(snap)
assert snaps[3]["Q"] == {"R"} and snaps[3]["NSW"] == {"R", "G"} and snaps[3]["V"] == {"R", "G"} and snaps[3]["T"] == set(cols) and all(snaps[3][r] for r in regs)
f.text(450, 14, "domains under forward checking", size=10.5, color=NAVY, bold=True)
for k, hd in enumerate(["start", "WA=R", "NT=G", "SA=B"]):
    f.text(377 + k * 58, 36, hd, size=10, color=SLATE, bold=True)
for i, r in enumerate(regs):
    y = 48 + i * 30
    f.text(340, y + 11, r, size=10.5, color=NAVY, bold=True, anchor="end", vmid=True)
    for k in range(4):
        for j, c in enumerate(cols):
            x = 355 + k * 58 + j * 14
            have = c in snaps[k][r]
            f.box(x, y + 2, 12, 18, "", fill=FILL[c] if have else "#ffffff", stroke=EDGE[c] if have else "#cbd5e1", r=2, sw=1.2)
f.box(340, 262, 232, 28, "filled = colour still allowed; Q is forced to red", fill=SAND, stroke=AMBER, size=10, r=5, color=NAVY)
f.text(150, 292, "8 nodes, no backtracking; 18 of 2,187 colourings valid", size=10, color=RED, bold=True)
```

```svgfig label="2.9" caption="Minimax with alpha-beta pruning on the tree of Section 2.7, computed in the figure code. Upward triangles are MAX nodes and downward triangles are MIN nodes; the leaves are the payoffs 3, 5, 6, 9, 1, 2, 0, -1. The left MIN node takes the smaller of 5 and 6 and gets 5, so the root has a value of at least 5. While the left MIN node examines its second MAX child, it reads 6, which is already above the 5 that MIN can get elsewhere, so the leaf 9 cannot matter (alpha = 6 is not below beta = 5). On the right, MIN gets 2 from the first MAX child, below the 5 that MAX already has, so the whole subtree 0, -1 is skipped. Five of eight leaves are read, and the root value 5 equals the full minimax value. Grey dashed items were never examined."
f = Fig(580, 296)
cm = __import__("math")
tree = [[[3, 5], [6, 9]], [[1, 2], [0, -1]]]
vis = {}; cuts = []
def ab(t, maxp, a, b, path):
    vis[path] = None
    if not isinstance(t, list):
        vis[path] = t; return t
    v = -cm.inf if maxp else cm.inf
    for k, c in enumerate(t):
        r = ab(c, not maxp, a, b, path + (k,))
        if maxp: v = max(v, r); a = max(a, v)
        else: v = min(v, r); b = min(b, v)
        if a >= b:
            cuts.append((path, a, b)); break
    vis[path] = v
    return v
def mm(t, maxp):
    if not isinstance(t, list): return t
    r = [mm(c, not maxp) for c in t]
    return max(r) if maxp else min(r)
assert ab(tree, True, -cm.inf, cm.inf, ()) == 5 == mm(tree, True) and cuts == [((0, 1), 6, 5), ((1,), 5, 2)]
leaves = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
assert sum(1 for p in leaves if p in vis) == 5
def val(path):
    t = tree
    for k in path: t = t[k]
    return t
def P(path):
    L = len(path)
    idx0 = sum(p * (8 >> (k + 1)) for k, p in enumerate(path))
    span = 8 >> L
    return 45 + 70 * (idx0 + (span - 1) / 2), [40, 112, 184, 252][L]
allp = [()] + [(a,) for a in (0, 1)] + [(a, b) for a in (0, 1) for b in (0, 1)] + leaves
for p in allp:
    if not p: continue
    (x1, y1), (x2, y2) = P(p[:-1]), P(p)
    seen = p in vis
    f.line(x1, y1 + 14, x2, y2 - (12 if len(p) == 3 else 14), color=NAVY if seen else "#cbd5e1", sw=1.8 if seen else 1.4, dash=not seen)
    if not seen:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        f.line(mx - 7, my - 7, mx + 7, my + 7, color=RED, sw=2.4)
cutnodes = {c[0]: c for c in cuts}
for p in allp:
    x, y = P(p); seen = p in vis; L = len(p)
    if L == 3:
        f.box(x - 17, y - 12, 34, 24, str(val(p)), fill=BLUE if seen else "#f1f5f9", stroke=NAVY if seen else "#cbd5e1", r=4, size=12, bold=True, color=NAVY if seen else "#94a3b8", dash=not seen, sw=1.5)
        continue
    mx = L in (0, 2)
    pts = [(x - 20, y + 15), (x + 20, y + 15), (x, y - 17)] if mx else [(x - 20, y - 15), (x + 20, y - 15), (x, y + 17)]
    if seen:
        lab = str(vis[p])
        if p in cutnodes: lab = ("≥" if mx else "≤") + lab
        f.poly(pts, fill=SAND if mx else BLUE, stroke=AMBER if mx else NAVY, sw=1.8, label=lab, lx=x, ly=y + (5 if mx else -3), size=10.5, color=NAVY)
    else:
        f.poly(pts, fill="#f1f5f9", stroke="#cbd5e1", sw=1.4, label="", lx=x, ly=y)
for L, nm in enumerate(["MAX", "MIN", "MAX"]):
    f.text(4, [40, 112, 184][L], nm, size=10, color=SLATE, bold=True, anchor="start")
f.text(290, 14, "5 of 8 leaves read; root value 5 = full minimax", size=10.5, color=NAVY, bold=True)
f.text(150, 284, "alpha=6 ≥ beta=5: leaf 9 skipped", size=10, color=RED, bold=True)
f.text(430, 284, "alpha=5 ≥ beta=2: subtree (0, -1) skipped", size=10, color=RED, bold=True)
```

```svgfig label="2.10" caption="The size of the tic-tac-toe game tree, counted by the figure code. Plain minimax visits 549,946 nodes and sees 255,168 complete games; the value of the game is 0 (a draw) for every one of the nine opening moves, so perfect play by both sides always ends level. Alpha-beta pruning gives the same value after only 18,297 nodes when moves are tried in the order 0 to 8, a saving of 96.7 percent, and 7,275 nodes when the centre is tried first and then the corners: good move ordering is what makes pruning powerful. The same idea scales to chess only with a depth limit and an evaluation function."
f = Fig(580, 270)
cm = __import__("math")
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def win(b):
    for x, y, z in LINES:
        if b[x] and b[x] == b[y] == b[z]: return b[x]
def solve(b, p, order, ab, a, bt, cnt):
    cnt[0] += 1; w = win(b)
    if w: cnt[2] += 1; return 1 if w == "X" else -1
    if all(b): cnt[2] += 1; return 0
    v = -2 if p == "X" else 2
    for i in order:
        if not b[i]:
            b[i] = p; r = solve(b, "O" if p == "X" else "X", order, ab, a, bt, cnt); b[i] = None
            if p == "X": v = max(v, r); a = max(a, v)
            else: v = min(v, r); bt = min(bt, v)
            if ab and a >= bt: break
    return v
def run(order, ab):
    c = [0, 0, 0]; v = solve([None] * 9, "X", order, ab, -2, 2, c); return v, c[0], c[2]
full = run(range(9), False); a1 = run(range(9), True); a2 = run([4, 0, 2, 6, 8, 1, 3, 5, 7], True)
assert full == (0, 549946, 255168) and a1[:2] == (0, 18297) and a2[:2] == (0, 7275)
opening = []
for i in range(9):
    b = [None] * 9; b[i] = "X"; c = [0, 0, 0]
    opening.append(solve(b, "O", range(9), False, -2, 2, c))
assert opening == [0] * 9
f.text(160, 14, "nodes visited (log scale)", size=10.5, color=NAVY, bold=True)
for i, (nm, n, fl, st_) in enumerate([("plain minimax", full[1], "#fee2e2", RED), ("alpha-beta, order 0 to 8", a1[1], SAND, AMBER), ("alpha-beta, centre first", a2[1], MINT, TEAL)]):
    y = 34 + i * 62
    w = cm.log10(n) * 42
    f.text(8, y + 6, nm, size=10.5, color=SLATE, bold=True, anchor="start")
    f.box(8, y + 14, w, 28, "", fill=fl, stroke=st_, r=3, sw=1.4)
    f.text(8 + w + 6, y + 28, "{:,}".format(n), size=11, color=st_, bold=True, anchor="start", vmid=True)
f.text(160, 232, "255,168 complete games; saving %.1f%% with alpha-beta" % (100 * (1 - a1[1] / full[1])), size=10.5, color=NAVY, bold=True)
f.text(160, 252, "every opening move has value 0", size=10.5, color=TEAL, bold=True)
f.text(462, 14, "value of X's opening move", size=10.5, color=NAVY, bold=True)
for i in range(9):
    x0, y0 = 352 + (i % 3) * 76, 26 + (i // 3) * 80
    f.box(x0, y0, 66, 66, "", fill=MINT, stroke=TEAL, r=4, sw=1.4)
    f.line(x0 + 22, y0 + 4, x0 + 22, y0 + 62, color="#64748b", sw=1.2); f.line(x0 + 44, y0 + 4, x0 + 44, y0 + 62, color="#64748b", sw=1.2)
    f.line(x0 + 4, y0 + 22, x0 + 62, y0 + 22, color="#64748b", sw=1.2); f.line(x0 + 4, y0 + 44, x0 + 62, y0 + 44, color="#64748b", sw=1.2)
    f.text(x0 + 11 + (i % 3) * 22, y0 + 11 + (i // 3) * 22, "X", size=14, color=NAVY, bold=True, vmid=True)
    f.text(x0 + 33, y0 + 76, "value %d" % opening[i], size=10, color=TEAL, bold=True)
```

```svgfig label="2.11" caption="Choosing a search method. Start at the top and answer each question; the first 'yes' names the family of algorithms. If an opponent moves, use adversarial search; if only the final state matters (timetables, circuit layout), local search; if the problem is variables with constraints, constraint satisfaction with backtracking; otherwise if a good admissible heuristic exists, A*; otherwise breadth-first search when step costs are equal (iterative deepening when memory is short) and uniform-cost search when they differ. Real systems combine these: a map application uses A* with a straight-line heuristic, a timetable uses CSP then local search to improve, and a game engine uses alpha-beta with iterative deepening."
f = Fig(580, 330)
qs = ["Does an opponent move\nagainst you?", "Does only the final state\nmatter (optimise)?", "Variables with constraints\n(timetable, colouring)?", "Is a good admissible\nheuristic h(n) available?", "Are all step costs equal?"]
ans = ["Adversarial search:\nminimax + alpha-beta pruning", "Local search: hill climbing,\nsimulated annealing, genetic", "CSP: backtracking with MRV\nand forward checking", "A* search (IDA* if memory\nis short; weighted A* for speed)", "BFS (IDDFS if memory is\nshort): fewest steps"]
for i in range(5):
    y = 8 + i * 52
    f.box(10, y, 250, 40, qs[i], fill=BLUE, stroke=NAVY, size=10.5, r=7, bold=True, color=NAVY)
    f.box(330, y, 242, 40, ans[i], fill=MINT, stroke=TEAL, size=10.5, r=7, color=NAVY, bold=True)
    f.arrow([(260, y + 20), (330, y + 20)], color=TEAL, sw=2, label="yes", lpos=(295, y + 13), lsize=10.5)
    f.arrow([(135, y + 40), (135, y + 60)], color=RED, sw=2, label="no", lpos=(152, y + 53), lsize=10.5)
f.box(10, 268, 250, 40, "Uniform-cost search\n(Dijkstra): cheapest path", fill=SAND, stroke=AMBER, size=10.5, r=7, bold=True, color=NAVY)
f.text(290, 324, "tip: start with the simplest method that fits, then add a heuristic or pruning", size=10, color=SLATE, italic=True)
```

### 2.8.1 Eight uses of search in Nepal

1. **Finding the way on a map.** When you ask a map application for the best route from Kathmandu to Pokhara, it treats the roads as a weighted graph and searches it. The straight-line distance to the destination is an admissible heuristic, so A* can find the cheapest route while looking at only a small part of the national road network. Road closures, landslides and traffic change the edge costs, and the search is simply run again.
2. **Exam routines and class timetables.** A university such as Tribhuvan University or a school must give every subject a room, a teacher and a time so that no student, teacher or room is used twice at once. This is a constraint satisfaction problem: the variables are the exams, the domains are the time slots and the constraints are the clashes. Backtracking with the most-constrained-first rule finds a valid routine quickly, and local search can then improve it, for example by spreading exams out.
3. **Delivery and ride dispatch.** Food and parcel delivery companies and ride-hailing apps in Kathmandu must choose which rider takes which order and in what stop order. Finding the best order of many stops is the travelling-salesman problem, which is too large to solve exactly, so the apps use local search and heuristics to reach a very good route in a second. The result is a lower fuel cost and a shorter wait for the customer.
4. **Routing packets in networks.** Internet providers and Nepal Telecom run link-state routing protocols in which every router runs Dijkstra's algorithm, the uniform-cost search of this unit, on a graph of links with costs. The result is a shortest-path tree that tells each router where to send each packet. When a link fails, the costs change and every router searches again, as the Networking book explains.
5. **Game-playing programs.** Computer opponents in chess, Ludo or carrom-style games choose moves by minimax with alpha-beta pruning, looking a few moves ahead and scoring the positions with an evaluation function. Move ordering decides how many positions are pruned (Fig. 2.10), so good programs try the most promising moves first. A difficulty level in a game is often just the search depth.
6. **Puzzles and learning apps.** Sudoku, sliding-tile and maze apps check a player's move or give a hint by searching the puzzle. Sudoku is a constraint problem like map colouring, and a sliding puzzle is solved with A* and the Manhattan-distance heuristic of Fig. 2.5. A hint is just the first step of the best solution found.
7. **Robot and drone navigation.** A warehouse robot, a robot vacuum or a survey drone moves on a grid of free and blocked cells and plans a path around obstacles with A*, as in Fig. 2.4. Drone surveys of floods or landslides in hill districts use the same idea to plan flight lines that cover the area with the fewest turns. The path is recomputed when a new obstacle appears.
8. **Planning shifts, buses and resources.** A hospital must give nurses and doctors shifts, and a bus company such as Sajha Yatayat must assign buses and drivers to routes, with rules about rest, skills and demand. These are large optimisation problems where the path does not matter, only the final plan, so local search and simulated annealing are used to improve the plan step by step. A planner accepts a slightly worse plan sometimes to escape a local maximum, exactly as in Fig. 2.6.

## Formula and fact sheet

- BFS O(b^d) time and space; DFS O(b^m) time, O(bm) space; IDDFS O(b^d) time, O(bd) space. Nodes by BFS at b = 10, d = 5: 111,111; IDDFS: 123,456.
- UCS expands by g(n); greedy by h(n); A* by f(n) = g(n) + h(n).
- Admissible: h(n) ≤ h*(n). Consistent: h(n) ≤ c(n, n′) + h(n′). Consistent ⇒ admissible.
- Simulated annealing: accept a worse move with probability e^(−ΔE/T).
- Minimax value = max at MAX nodes, min at MIN nodes. Alpha–beta prunes when α ≥ β; best case O(b^(m/2)).
- CSP heuristics: MRV, degree, least-constraining value, forward checking, AC-3.

## Chapter summary

- A search problem is defined by states, actions, a goal test and path costs; the algorithm determines which frontier node is expanded next.
- BFS, UCS and IDDFS are complete; BFS and IDDFS are optimal for equal step costs and UCS for any positive costs; DFS saves memory but is neither.
- A* with an admissible (tree) or consistent (graph) heuristic is optimal and more efficient than blind search; a dominant heuristic expands fewer nodes.
- Local search keeps one state and suits optimisation; simulated annealing escapes local maxima by occasionally accepting worse moves.
- CSPs are solved by backtracking with MRV and forward checking. Games are searched by minimax; alpha–beta gives the same answer with far fewer nodes.

## Practice

1. List the five components of a search problem and formulate the 8-puzzle.
2. On the example graph, give the path and cost found by BFS, UCS, greedy and A*. Why does BFS not find the cheapest path?
3. Why is IDDFS not wasteful? Compute the node counts for b = 10, d = 5.
4. Define admissible and consistent heuristics. Show h is admissible on the example graph.
5. For the 8-puzzle start 2 6 5 / 4 3 8 / 7 1 _ compute h₁ and h₂ and explain which dominates.
6. Compare hill climbing and simulated annealing. What is the acceptance probability for ΔE = 2 at T = 1 and T = 10?
7. Formulate Australia map colouring as a CSP. How many solutions with three colours?
8. Apply minimax and alpha–beta to the tree with leaves 3, 5 | 6, 9 | 1, 2 | 0, −1 and state which leaves are pruned.
9. Why does alpha–beta not change the minimax result? What is its best-case complexity?
10. How many nodes are in the full tic-tac-toe tree, and what is the game's minimax value?

::: note Answers and worked solutions
**1.** Initial state, actions, transition model, goal test, path cost. 8-puzzle: states are tile arrangements; actions move the blank; transition swaps blank and tile; goal is the ordered arrangement; cost 1 per move.
**2.** BFS: S → A → C → G, cost 9 (fewest edges). UCS: S → A → B → C → G, cost 8. Greedy: S → B → C → G, cost 9. A*: S → A → B → C → G, cost 8. BFS counts steps, not costs.
**3.** Most nodes are at the deepest level, so the repeated shallow levels are cheap. BFS: 111,111 nodes; IDDFS: 6 + 50 + 400 + 3,000 + 20,000 + 100,000 = 123,456.
**4.** Admissible: h(n) never exceeds the true remaining cost; consistent: h(n) ≤ c(n, n′) + h(n′). On the example h* = (S 8, A 6, B 4, C 3, D 2, G 0) and h = (6, 5, 3, 2, 2, 0) ≤ h*, so it is admissible.
**5.** h₁ = 6 misplaced tiles; h₂ = 12 (Manhattan). h₂ ≥ h₁ for every state, so h₂ dominates and A* expands fewer nodes (144 versus 565 in the test).
**6.** Hill climbing only improves and sticks in local maxima; annealing accepts worse moves with probability e^(−ΔE/T). For ΔE = 2: T = 1 gives 0.1353, T = 10 gives 0.8187.
**7.** Variables: seven regions; domain: three colours; constraints: adjacent regions differ. There are 18 solutions.
**8.** Minimax = 5. Alpha–beta prunes the leaf 9 (after 6, with α = 6 ≥ β = 5) and the subtree (0, −1) (after the right MIN node's β becomes 2 ≤ α = 5); 5 of 8 leaves are read.
**9.** A pruned branch cannot change the value at the root because MAX or MIN already has a better option elsewhere. Best case O(b^(m/2)).
**10.** 549,946 nodes (255,168 complete games); the value is 0 (draw). Alpha–beta with plain ordering visits 18,297 nodes.
:::

## Model answers for Unit 2

**Q1. Explain the uninformed search strategies. Compare breadth-first, depth-first, uniform-cost and iterative-deepening search. (10 marks)**

**Introduction.** Uninformed (blind) search strategies use only the problem definition: the states, the actions, the goal test and the step costs. They have no idea which state is promising, and they differ only in which node of the frontier they expand next. They are judged by completeness, optimality, time and space, using the branching factor b, the depth d of the shallowest goal and the maximum depth m.

**The strategies.**

1. **Breadth-first search (BFS)** expands the shallowest node first with a FIFO queue (Fig. 2.2). It is complete and, when all step costs are equal, optimal, but it stores a whole level, so time and space are O(b^d). On the example graph it returns S-A-C-G of cost 9: the path with the fewest edges, not the cheapest (Fig. 2.1).
2. **Depth-first search (DFS)** expands the deepest node first with a LIFO stack. Its memory is only O(b·m), but it is not optimal, and in a cyclic or infinite space without an explored set it may never finish.
3. **Uniform-cost search (UCS)** expands the node with the smallest path cost g(n) using a priority queue; it is Dijkstra's algorithm. It is complete and optimal for positive step costs and returns S-A-B-C-G of cost 8.
4. **Depth-limited search** is DFS with a depth limit l; it stops infinite descent but is incomplete when l < d.
5. **Iterative-deepening search (IDDFS)** repeats depth-limited search with l = 0, 1, 2 and so on. It has the memory of DFS, O(b·d), and the completeness of BFS. The repeated work is small: for b = 10 and d = 8 it generates 123,456,789 nodes against 111,111,111 for BFS (Fig. 2.3).

**Comparison.**

| Algorithm | Complete | Optimal | Time | Space |
|---|---|---|---|---|
| BFS | yes | yes, if costs are equal | O(b^d) | O(b^d) |
| DFS | no | no | O(b^m) | O(b·m) |
| UCS | yes | yes | O(b^(1 + C*/ε)) | same |
| Depth-limited | no, if l < d | no | O(b^l) | O(b·l) |
| IDDFS | yes | yes, if costs are equal | O(b^d) | O(b·d) |

**Memory is the real limit.** At one million nodes per second and 1 KB per node, BFS to depth 10 needs 3.1 hours and 11.1 TB (Fig. 2.3), so it runs out of memory long before the user runs out of patience. Bidirectional search reduces the cost to about O(b^(d/2)).

**Conclusion.** Use BFS or IDDFS when costs are equal, UCS when costs differ, and DFS only when memory is tiny and any solution will do. All blind methods fail on large spaces, which is why heuristics are needed.

**Q2. Explain A\* search. What is an admissible heuristic? Trace A\* on the example graph and compare it with greedy search. (10 marks)**

**Introduction.** A* is the best-known informed search. It ranks frontier nodes by f(n) = g(n) + h(n), where g(n) is the cost already paid to reach n and h(n) is a heuristic estimate of the cheapest cost from n to a goal. Using both parts balances the cost behind with the cost ahead.

**Conditions for optimality.** A heuristic is **admissible** if it never overestimates: h(n) ≤ h*(n), the true remaining cost. A* with an admissible heuristic is optimal for tree search. A heuristic is **consistent** if h(n) ≤ c(n, n′) + h(n′) for every edge; this guarantees that f never decreases along a path, so the first time a node is expanded its path is optimal (graph search). Consistency implies admissibility.

**Trace on the example graph (Fig. 2.1).** With h(S) = 6, h(A) = 5, h(B) = 3, h(C) = 2, h(D) = 2 and h(G) = 0:

| Expanded | g | h | f | Frontier note |
|---|---|---|---|---|
| S | 0 | 6 | 6 | A (7), B (8) |
| A | 2 | 5 | 7 | B improves to g = 4, f = 7 |
| B | 4 | 3 | 7 | C improves to g = 5, f = 7 |
| C | 5 | 2 | 7 | G: g = 8, f = 8 |
| G | 8 | 0 | 8 | goal: S-A-B-C-G, cost 8 |

**Comparison with greedy search.** Greedy best-first search uses f(n) = h(n) alone. On the same graph it expands S, B, C and G and returns S-B-C-G of cost 9: it is fast (4 expansions) but it ignores the cost already paid, so it is neither optimal nor complete in general. A* needs 5 expansions and returns the optimal cost 8.

**Effect of the heuristic.** A better heuristic expands fewer nodes. On the 8-puzzle start state of Fig. 2.5, uniform-cost search (h = 0) expands 7,495 nodes, A* with misplaced tiles (h1 = 6) expands 565 and A* with Manhattan distance (h2 = 12) expands 144, all finding the 16-move optimum. On a grid with a wall, a heuristic that points into the wall helps much less (Fig. 2.4).

**Conclusion.** A* is complete and optimal with an admissible (tree) or consistent (graph) heuristic, and it is the standard choice for route finding; its weakness is memory, which IDA* and weighted A* reduce.

**Q3. Explain minimax and alpha-beta pruning with an example. (10 marks)**

**Introduction.** In a two-player game with perfect information, such as tic-tac-toe or chess, the best move depends on the reply of an opponent who is also trying to win. Adversarial search models this with a game tree in which MAX (the player) and MIN (the opponent) move alternately.

**Minimax.** The value of a leaf is its utility for MAX (+1 win, 0 draw, -1 loss in tic-tac-toe). The value of a MAX node is the maximum of its children and the value of a MIN node is the minimum. MAX picks the move whose child has the highest value, assuming MIN replies as well as possible. It is complete on a finite tree and optimal against an optimal opponent. Its time is O(b^m) and its space O(b·m).

**Worked example (Fig. 2.9).** For the tree with leaves 3, 5 | 6, 9 | 1, 2 | 0, -1, the lower MAX nodes are 5, 9, 2 and 0, the MIN nodes are 5 and 0, and the root is 5.

**Alpha-beta pruning.** Alpha is the best value MAX can already guarantee on the path and beta is the best value MIN can guarantee. A branch is cut as soon as α ≥ β, because the player above would never allow that position. In Fig. 2.9 the leaf 9 is skipped (α = 6 ≥ β = 5) and the subtree 0, -1 is skipped (α = 5 ≥ β = 2). Five of eight leaves are read and the root is still 5.

| Method | Tic-tac-toe nodes | Note |
|---|---|---|
| Plain minimax | 549,946 | 255,168 complete games |
| Alpha-beta, order 0 to 8 | 18,297 | 96.7 percent saved |
| Alpha-beta, centre first | 7,275 | good ordering helps |

**Complexity.** With perfect ordering alpha-beta searches O(b^(m/2)) nodes, doubling the reachable depth. For games such as chess, programs also use a depth limit, an evaluation function and iterative deepening.

**Conclusion.** Alpha-beta returns exactly the minimax value with far fewer nodes, which is why it is the basis of game-playing programs.

**Q4. What is a constraint satisfaction problem? Explain backtracking with map colouring. (10 marks)**

**Introduction.** A constraint satisfaction problem (CSP) has variables X1 to Xn, a domain of values for each variable and constraints that restrict which combinations are allowed. A solution assigns every variable a value so that all constraints hold. Because the structure is explicit, a solver can reject whole branches early instead of searching blindly.

**Example (Fig. 2.8).** Map colouring: the variables are the seven regions WA, NT, SA, Q, NSW, V and T, the domain is {red, green, blue} and the constraints say that neighbouring regions differ. There are 3^7 = 2,187 colourings and exactly 18 are valid. With two colours there is none, because WA, NT and SA form a triangle.

**Backtracking search.** It assigns one variable at a time, checks the constraints against the variables already assigned, and goes back to the previous variable when no value fits. In the fixed order WA, NT, SA, Q, NSW, V, T with colours red, green, blue it finds a solution in 8 nodes without any backtracking: WA = red, NT = green, SA = blue, Q = red, NSW = green, V = red, T = red.

**Improvements.**
1. **Minimum remaining values (MRV)** chooses the variable with the fewest legal values.
2. **Degree heuristic** chooses the variable involved in the most constraints.
3. **Least-constraining value** tries first the value that rules out the fewest choices for neighbours.
4. **Forward checking** removes a value from a neighbour's domain when a variable takes it. After WA = red, NT = green and SA = blue, Q is forced to red (Fig. 2.8), and an empty domain would force an immediate backtrack.
5. **Arc consistency (AC-3)** repeatedly removes values that have no support in a neighbouring variable.

| Method | Idea | Effect |
|---|---|---|
| Plain backtracking | assign, check, retreat | avoids bad branches |
| Forward checking | prune neighbour domains | detects dead ends early |
| MRV + degree | choose the hardest variable first | smaller tree |

**Conclusion.** CSP solvers combine backtracking with constraint propagation and variable-ordering heuristics, and they handle timetables, Sudoku and scheduling.

**Q5. Compare hill climbing with simulated annealing. (5 marks)**

Both are local search methods: they keep a single current state, use constant memory and are used when only the final state matters, such as timetables, n-queens or circuit layout. **Hill climbing** moves to the best neighbour and stops when no neighbour is better. It is fast, but it stops at a local maximum, on a plateau or on a ridge. On the landscape of Fig. 2.6, which has nine local maxima, hill climbing from 101 evenly spaced starting points reaches the highest peak only 19 times (18.8 percent). Remedies are random restarts, sideways moves and stochastic hill climbing.

**Simulated annealing** also accepts a worse move of size ΔE with probability e^(−ΔE/T), where the temperature T is lowered slowly. For ΔE = 2 the probability is 0.8187 at T = 10, so the search explores freely, and 0.1353 at T = 1, so it is almost greedy. In the same landscape, cooling from T = 3 reached the highest peak in 10 of 20 runs (50 percent). With a slow enough cooling schedule it finds the global optimum with probability approaching 1.

| | Hill climbing | Simulated annealing |
|---|---|---|
| Moves accepted | only better | better always, worse with probability e^(−ΔE/T) |
| Local maxima | gets stuck | can escape |
| Speed | very fast | slower, depends on cooling |

**Q6. Explain heuristics for the 8-puzzle. Which one dominates? (5 marks)**

A heuristic h(n) estimates the cost from a state to the goal. Good heuristics for the 8-puzzle come from **relaxed problems**, which are the puzzle with some rules removed. If a tile may jump to any square, the exact cost is the number of misplaced tiles, h1. If a tile may move onto an occupied neighbouring square, the exact cost is the sum of the Manhattan distances of the tiles from their goal squares, h2. Because the relaxed cost can never exceed the real cost, both heuristics are admissible.

For the start state 2 6 5 / 4 3 8 / 7 1 _ and the goal 1 2 3 / 4 5 6 / 7 8 _, six tiles are misplaced, so h1 = 6, and the Manhattan distances 1, 2, 2, 0, 2, 2, 0 and 3 give h2 = 12 (Fig. 2.5). The optimal solution has 16 moves, and both values are below it.

h2 is never smaller than h1 for any state, so h2 **dominates** h1: A* with h2 expands no more nodes than A* with h1. The experiment of Fig. 2.5 confirms it: uniform-cost search expands 7,495 nodes, A* with h1 expands 565 and A* with h2 expands 144. If two admissible heuristics are available, max(h1, h2) is admissible and dominates both, and pattern databases can give even better estimates.

**Q7. Define a well-defined search problem and formulate the 8-puzzle. How is the performance of a search algorithm measured? (5 marks)**

A well-defined problem has five components. The **initial state** is where the agent starts. The **actions** are what the agent can do in each state. The **transition model** gives the state that results from an action. The **goal test** checks whether a state is a goal. The **path cost** adds up the step costs along a path, and a **solution** is a path from the initial state to a goal state; it is optimal if its cost is the lowest.

For the 8-puzzle the state is the position of the eight tiles and the blank. The initial state is any solvable arrangement, the actions move the blank up, down, left or right, the transition model swaps the blank with its neighbour, the goal test checks the order 1 to 8, and each move costs 1. There are 9! = 362,880 arrangements, but only half, 181,440, are reachable from a given start, because of parity.

Performance is measured by four criteria: **completeness** (is a solution always found if one exists), **optimality** (is it the cheapest), **time complexity** (nodes generated) and **space complexity** (nodes stored). They are expressed with the branching factor b, the depth d of the shallowest goal and the maximum depth m.

**Q8. Distinguish between admissible and consistent heuristics with an example. (5 marks)**

A heuristic h is **admissible** if it never overestimates the true cheapest remaining cost: h(n) ≤ h*(n) for every state n. It is **consistent** (or monotone) if for every state n and every successor n′ reached by an action of cost c(n, n′), h(n) ≤ c(n, n′) + h(n′). This is a triangle inequality: the estimate from n is never more than the cost of one step plus the estimate from the next state.

**Example.** In the example graph of Fig. 2.1 the true costs to G are h*(S) = 8, h*(A) = 6, h*(B) = 4, h*(C) = 3, h*(D) = 2 and h*(G) = 0. The heuristic h = (6, 5, 3, 2, 2, 0) is below these values everywhere, so it is admissible. It is also consistent: for the edge B-C of cost 1, h(B) = 3 ≤ 1 + h(C) = 3, and for A-B of cost 2, h(A) = 5 ≤ 2 + 3 = 5.

**Why it matters.** Every consistent heuristic is admissible, but not every admissible heuristic is consistent. For tree search, admissibility is enough for A* to be optimal. For graph search with an explored set, consistency is needed: it guarantees that f(n) = g(n) + h(n) never decreases along a path, so the first time A* expands a node it has found the cheapest path to it and never has to reopen it.

**Q9. Explain how the eight-queens problem is solved by backtracking. How many boards are examined? (5 marks)**

The eight-queens problem asks for eight queens on a chessboard so that no two attack each other: no two share a row, a column or a diagonal. It is a constraint satisfaction problem whose variables are the eight rows, whose values are the columns 1 to 8 and whose constraints forbid shared columns and diagonals.

A blind search that puts one queen in each row in any column examines 8^8 = 16,777,216 boards. Insisting on different columns leaves 8! = 40,320 permutations. **Backtracking** places one queen per row from row 1 downwards and tries the columns in order. Before placing a queen it checks the queens already on the board. If no column is safe, it goes back to the previous row and moves that queen. The first solution found has queens in columns 1, 5, 8, 6, 3, 7, 2 and 4 (Plate 2.3).

Counted by the program of Fig. 2.7, backtracking visits only 2,057 nodes, including the empty board, to find all 92 solutions. Of these, only 12 are fundamentally different: the other 80 are rotations or reflections of those 12. The saving comes from rejecting a whole group of boards as soon as the first two queens attack each other, which is the idea behind every constraint solver.
