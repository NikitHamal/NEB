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
