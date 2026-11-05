---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 11
title: Algorithms
hours: 5
area: BCA 201 · Data Structure and Algorithms · Unit 11
---

This closing unit steps back from individual data structures to the **styles of algorithm**: deterministic and non-deterministic, divide and conquer, serial and parallel, and heuristic and approximate. Knowing the styles helps you pick a strategy for a new problem.

::: key What this unit gives you
- Deterministic versus non-deterministic algorithms and the meaning of P and NP.
- Divide and conquer, its recurrences and the Master theorem.
- Series (serial) and parallel algorithms, speed-up and Amdahl's law.
- Heuristic and approximate algorithms, with tested examples.
:::

## 11.1 Deterministic and non-deterministic algorithms

A **deterministic algorithm** has one defined next step at every point; the same input always follows the same path and gives the same output. All the algorithms in this book so far are deterministic.

A **non-deterministic algorithm** is a theoretical model in which a special `choice` step can "guess" the right option among several, and the algorithm succeeds if *some* sequence of guesses reaches a solution. No real computer does this; it is a tool for classifying problems. The practical reading: a non-deterministic algorithm **guesses a certificate** and then **verifies** it with an ordinary deterministic procedure.

| Class | Meaning | Examples |
|---|---|---|
| **P** | solvable in polynomial time by a deterministic algorithm | sorting, shortest path, MST |
| **NP** | a proposed solution can be **verified** in polynomial time (equivalently, solvable in polynomial time non-deterministically) | subset sum, Hamiltonian cycle, SAT |
| **NP-complete** | the hardest problems in NP: if one is in P, all NP is in P | SAT, travelling salesman (decision), vertex cover, knapsack (decision) |

P ⊆ NP; whether P = NP is the best-known open question in computer science. For NP-complete problems no polynomial algorithm is known, so in practice we use exponential search for small inputs, or heuristic and approximate algorithms (11.5).

::: example Worked example: subset sum
Given {3, 34, 4, 12, 5, 2}, is there a subset with sum 9? **Verification** of the certificate {4, 5} is trivial: 4 + 5 = 9, a linear-time check. **Finding** it deterministically means trying subsets: up to 2ⁿ of them (64 here). The non-deterministic algorithm simply "guesses" the right subset then verifies.
:::

## 11.2 Divide and conquer

**Divide and conquer** solves a problem in three steps: **divide** it into smaller subproblems of the same kind, **conquer** them recursively (solving the smallest directly), and **combine** the answers. Its cost follows a recurrence T(n) = a·T(n/b) + f(n).

**Master theorem** (for f(n) = Θ(n^d)): if a < b^d then T(n) = Θ(n^d); if a = b^d then Θ(n^d log n); if a > b^d then Θ(n^(log_b a)).

| Algorithm | Recurrence | Result |
|---|---|---|
| Binary search | T(n) = T(n/2) + 1 | O(log n) |
| Merge sort | T(n) = 2T(n/2) + n | O(n log n) |
| Quick sort (balanced) | T(n) = 2T(n/2) + n | O(n log n) |
| Max and min together | T(n) = 2T(n/2) + 2 | 3n/2 − 2 comparisons |
| Strassen matrix multiply | T(n) = 7T(n/2) + n² | O(n^2.81) |
| Naive recursive Fibonacci | T(n) = T(n−1) + T(n−2) | exponential: **not** a true divide and conquer, subproblems overlap |

When subproblems **overlap**, divide and conquer repeats work; **dynamic programming** stores the answers instead.

## 11.3 Series (serial) and parallel algorithms

A **serial algorithm** executes one step at a time on one processor. A **parallel algorithm** splits the work among p processors that execute at the same time. Measures: **speed-up** S = T₁ / T_p (best serial time over parallel time) and **efficiency** E = S / p.

**Amdahl's law.** If a fraction f of the work must stay serial, the speed-up on p processors is at most **S = 1 / (f + (1 − f)/p)** and never exceeds 1/f however many processors are used.

::: example Worked example
A job is 90% parallelisable (f = 0.1). On 8 processors: S = 1 / (0.1 + 0.9/8) = 1 / 0.2125 = **4.71**, efficiency 59%. With infinitely many processors S → 10.
**Parallel sum:** to add 8 numbers, round 1 adds four pairs at the same time, round 2 adds two pairs, round 3 adds the last pair: 3 = log₂ 8 steps on 4 processors instead of 7 serial additions.
:::

Parallel problems are limited by **dependencies** (a step needing a previous result), communication and synchronisation costs. Merge sort, matrix multiplication, BFS levels and Monte-Carlo simulations parallelise well; computing a chain of dependent values does not.

## 11.4 Heuristic algorithms

A **heuristic** is a rule of thumb that finds a *good* solution quickly with **no guarantee** of optimality (or sometimes of success). Used when exact methods are too slow: route planning, scheduling, game playing, constraint solving. Examples: nearest-neighbour for travelling salesman, greedy colouring, hill climbing, best-first search with an estimate function (A*, which is optimal when its estimate never overestimates).

**Greedy can fail.** Coins {1, 3, 4}, make 6: greedy takes 4 + 1 + 1 = 3 coins; the optimum is 3 + 3 = 2 coins.

## 11.5 Approximate algorithms

An **approximation algorithm** runs in polynomial time on an NP-hard optimisation problem and **guarantees** that its answer is within a known factor of optimal (the **approximation ratio**).

- **Vertex cover, 2-approximation:** repeatedly pick any uncovered edge (u, v), put **both** u and v in the cover, delete all edges touching them. The picked edges share no vertex, and any cover must contain at least one endpoint of each, so |optimal| ≥ number of picked edges and our cover ≤ 2 × optimal.
- **Metric TSP, 2-approximation:** build an MST, walk it twice (a closed tour of weight 2·MST ≤ 2·OPT), skip repeated cities by triangle inequality.

**Heuristic vs approximate:** both trade optimality for speed; only an approximation algorithm *proves* how far it can be from the best.

```c
#include <stdio.h>
#include <string.h>

/* 1. divide and conquer: max and min together */
int cmpc;
void maxmin(const int a[], int lo, int hi, int *mx, int *mn) {
    if (lo == hi) { *mx = *mn = a[lo]; return; }
    if (hi == lo + 1) { cmpc++; if (a[lo] > a[hi]) { *mx = a[lo]; *mn = a[hi]; } else { *mx = a[hi]; *mn = a[lo]; } return; }
    int mid = (lo + hi) / 2, mx1, mn1, mx2, mn2;
    maxmin(a, lo, mid, &mx1, &mn1); maxmin(a, mid + 1, hi, &mx2, &mn2);
    cmpc += 2; *mx = mx1 > mx2 ? mx1 : mx2; *mn = mn1 < mn2 ? mn1 : mn2;
}

/* 2. non-deterministic style: verify a certificate vs brute force */
int verify(const int s[], int n, unsigned mask, int target) {
    int sum = 0; for (int i = 0; i < n; i++) if (mask >> i & 1) sum += s[i];
    return sum == target;
}

/* 3. greedy vs optimal coin change */
int greedy_coins(int amt) { int c[] = {4, 3, 1}, n = 0; for (int i = 0; i < 3; i++) { n += amt / c[i]; amt %= c[i]; } return n; }
int dp_coins(int amt)     { int dp[100] = {0}, c[] = {1, 3, 4};
    for (int a = 1; a <= amt; a++) { dp[a] = 1000; for (int i = 0; i < 3; i++) if (a >= c[i] && dp[a - c[i]] + 1 < dp[a]) dp[a] = dp[a - c[i]] + 1; }
    return dp[amt]; }

/* 4. 2-approximate vertex cover; 5. nearest-neighbour vs optimal tour */
#define V 6
#define C 5
int D[C][C] = {{0,2,9,10,7},{2,0,6,4,3},{9,6,0,8,5},{10,4,8,0,6},{7,3,5,6,0}};
int best = 1 << 30, perm[C];
void permute(int k, int len) {                       /* brute-force over tours starting at city 0 */
    if (k == C) { len += D[perm[C-1]][0]; if (len < best) best = len; return; }
    for (int i = k; i < C; i++) {
        int t = perm[k]; perm[k] = perm[i]; perm[i] = t;
        permute(k + 1, len + D[perm[k-1]][perm[k]]);
        t = perm[k]; perm[k] = perm[i]; perm[i] = t;
    }
}

int main(void) {
    int a[] = {23, 7, 91, 15, 62, 4, 38, 55};
    int mx, mn; maxmin(a, 0, 7, &mx, &mn);
    printf("max = %d, min = %d, comparisons = %d (naive would use 14)\n", mx, mn, cmpc);

    int s[] = {3, 34, 4, 12, 5, 2};
    printf("certificate {4,5} valid for 9? %s\n", verify(s, 6, (1u << 2) | (1u << 4), 9) ? "yes" : "no");
    int found = 0; unsigned tried = 0;
    for (unsigned m = 0; m < (1u << 6) && !found; m++) { tried++; found = verify(s, 6, m, 9); }
    printf("brute force tried %u of 64 subsets before success\n", tried);

    printf("make 6 from {1,3,4}: greedy %d coins, optimal %d coins\n", greedy_coins(6), dp_coins(6));

    int E[][2] = {{0,1},{0,2},{1,3},{2,3},{3,4},{4,5}}, covered[V] = {0}, size = 0;
    for (int i = 0; i < 6; i++)
        if (!covered[E[i][0]] && !covered[E[i][1]]) { covered[E[i][0]] = covered[E[i][1]] = 1; size += 2; }
    printf("2-approx vertex cover size = %d (optimal for this graph is 3)\n", size);

    int visited[C] = {1}, cur = 0, len = 0;
    printf("nearest neighbour tour: 0");
    for (int step = 1; step < C; step++) {
        int nxt = -1;
        for (int j = 0; j < C; j++) if (!visited[j] && (nxt < 0 || D[cur][j] < D[cur][nxt])) nxt = j;
        visited[nxt] = 1; len += D[cur][nxt]; cur = nxt; printf(" -> %d", cur);
    }
    len += D[cur][0]; printf(" -> 0, length %d\n", len);
    for (int i = 0; i < C; i++) perm[i] = i;
    permute(1, 0);
    printf("optimal tour length (brute force over %d tours) = %d\n", 24, best);
    return 0;
}
```
```output
max = 91, min = 4, comparisons = 10 (naive would use 14)
certificate {4,5} valid for 9? yes
brute force tried 21 of 64 subsets before success
make 6 from {1,3,4}: greedy 3 coins, optimal 2 coins
2-approx vertex cover size = 6 (optimal for this graph is 3)
nearest neighbour tour: 0 -> 1 -> 4 -> 2 -> 3 -> 0, length 28
optimal tour length (brute force over 24 tours) = 26
```

## Formula and fact sheet

- P ⊆ NP; NP-complete = hardest in NP; verifying a certificate is polynomial.
- Master theorem: T(n) = aT(n/b) + Θ(n^d): a < b^d → n^d; a = b^d → n^d log n; a > b^d → n^(log_b a).
- Speed-up S = T₁/T_p; Amdahl: S ≤ 1/(f + (1−f)/p) ≤ 1/f.
- Heuristic: no guarantee. Approximation: guaranteed ratio (vertex cover 2).
- Greedy optimal for Huffman, MST, Dijkstra; not for arbitrary coin systems.

## Chapter summary

- Deterministic algorithms follow one path; non-deterministic ones guess and verify, which defines NP.
- Divide and conquer splits, solves and combines; recurrences and the Master theorem give the cost.
- Parallel algorithms speed up only the parallelisable fraction (Amdahl's law).
- For hard problems we accept heuristics (no guarantee) or approximation algorithms (guaranteed ratio).

## Practice

1. Differentiate deterministic and non-deterministic algorithms.
2. Define P, NP and NP-complete; give an example of each.
3. Solve T(n) = 4T(n/2) + n and T(n) = 2T(n/2) + n² using the Master theorem.
4. Explain the divide, conquer and combine steps of merge sort on 6 4 9 1.
5. A program is 80% parallelisable. Find the maximum speed-up on 4 processors and with infinite processors.
6. Compare heuristic and approximate algorithms.
7. Show that greedy coin change fails for coins {1, 3, 4} and amount 6.
8. Explain why the 2-approximation for vertex cover is within a factor of 2.
9. When is divide and conquer a poor choice?

::: note Answers and worked solutions
**1.** Deterministic: every step is fully determined, so one run per input. Non-deterministic: may choose among options, accepting if any choice sequence succeeds; used as a theoretical model.
**2.** P: solvable in polynomial time (sorting). NP: solutions verifiable in polynomial time (subset sum). NP-complete: NP problems to which every NP problem reduces (SAT, decision TSP).
**3.** a = 4, b = 2, d = 1: a > b^d (4 > 2) → Θ(n^(log₂4)) = **Θ(n²)**. Second: a = 2, b = 2, d = 2: a < b^d (2 < 4) → **Θ(n²)**.
**4.** Divide: [6 4] [9 1]. Conquer: sort each: [4 6] [1 9]. Combine: merge → [1 4 6 9].
**5.** f = 0.2. p = 4: 1/(0.2 + 0.8/4) = 1/0.4 = **2.5**. p → ∞: 1/0.2 = **5**.
**6.** Both are used for hard problems and trade exactness for speed. A heuristic gives no bound on how far it can be from the optimum; an approximation algorithm guarantees a ratio.
**7.** Greedy: 4 + 1 + 1 = 3 coins. Optimal: 3 + 3 = 2 coins.
**8.** The edges selected share no endpoint (a matching of size k). Any cover needs one endpoint per selected edge, so OPT ≥ k, while the algorithm uses 2k vertices ≤ 2·OPT.
**9.** When the subproblems overlap heavily (naive Fibonacci), repeating the work makes it exponential; use dynamic programming instead. It is also unhelpful when dividing and combining cost more than solving directly.
:::
