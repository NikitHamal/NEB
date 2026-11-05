---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 10
title: Graphs
hours: 5
area: BCA 201 · Data Structure and Algorithms · Unit 10
---

A **graph** G = (V, E) is a set of **vertices** (nodes) and a set of **edges** joining pairs of vertices. Graphs model road maps, networks, social connections, dependencies and the web. This unit covers representations, closure, traversal, spanning trees and shortest paths.

::: key What this unit gives you
- The graph ADT, terminology and types of graph.
- Adjacency matrix and list; transitive closure by Warshall's algorithm.
- BFS and DFS traversals, spanning forests.
- Kruskal's and round-robin minimum spanning tree algorithms, Dijkstra's shortest path, the greedy method.
:::

## 10.1 Graphs as an ADT; types of graph

**Operations:** add/remove vertex, add/remove edge, adjacent(u, v), neighbours(v), traverse.

| Term | Meaning |
|---|---|
| **Undirected / directed (digraph)** | edges have no direction / edges are ordered pairs u → v |
| **Weighted** | each edge carries a cost or length |
| **Degree** | edges at a vertex (digraph: in-degree and out-degree). Σ degrees = 2|E| |
| **Path / cycle** | sequence of edges / a path that returns to its start |
| **Connected** | a path exists between every pair (digraph: *strongly* connected if in both directions) |
| **Tree** | connected graph with no cycles: |E| = |V| − 1 |
| **Complete graph** | every pair adjacent: |E| = n(n−1)/2 |
| **Simple / multigraph** | no loops or parallel edges / allows them |
| **DAG** | directed acyclic graph (task dependencies, topological order) |
| **Sparse / dense** | |E| ≪ |V|² / |E| ≈ |V|² |

## 10.2 Representations

| | **Adjacency matrix** | **Adjacency list** |
|---|---|---|
| Structure | n × n array, A[i][j] = 1 (or weight) if edge i–j | array of linked lists of neighbours |
| Space | O(n²) | O(n + e) |
| Edge test (u, v) | **O(1)** | O(degree) |
| List all neighbours | O(n) | O(degree) |
| Best for | dense graphs, Warshall | sparse graphs, traversal |

For an undirected graph the matrix is symmetric.

## 10.3 Transitive closure and Warshall's algorithm

The **transitive closure** of a digraph has an edge u → v whenever a path from u to v exists. It answers "is v reachable from u?" for all pairs. **Warshall's algorithm** starts with the adjacency matrix R and, for each intermediate vertex k in turn, sets `R[i][j] = R[i][j] OR (R[i][k] AND R[k][j])`. After processing k, R[i][j] = 1 iff there is a path from i to j using only vertices 0..k as intermediates. Time O(n³), space O(n²).

::: example Worked example
Digraph 0 → 1, 1 → 2, 2 → 3. k = 0: nothing is routed through 0 except into it (no new edges). k = 1: 0 → 1 and 1 → 2 give 0 → 2. k = 2: 0 → 2, 1 → 2 and 2 → 3 give 0 → 3 and 1 → 3. k = 3: no new edges. The closure has six edges: 0→1, 0→2, 0→3, 1→2, 1→3, 2→3.
:::

## 10.4 Traversal and spanning forests

**Breadth-first search (BFS):** visit the start vertex, then all its neighbours, then their neighbours, level by level, using a **queue**. It finds the **fewest-edge** path in an unweighted graph. **Depth-first search (DFS):** go as deep as possible along one path, then backtrack, using a **stack** (or recursion). It detects cycles and underlies topological sorting and connected components. Both take **O(n + e)** with adjacency lists (O(n²) with a matrix).

The edges used to discover new vertices form a **spanning tree** of the component (the BFS tree or DFS tree). If the graph is disconnected, restarting the search from each unvisited vertex produces a **spanning forest**: one tree per component.

## 10.5 Minimum spanning trees (Kruskal and round-robin)

A **spanning tree** connects all n vertices with n − 1 edges and no cycle. In a weighted graph the **minimum spanning tree (MST)** has the least total weight (cabling a network at minimum cost).

**Kruskal's algorithm.** Sort the edges by weight; take each edge in turn unless it would form a cycle with edges already chosen (tested with **union-find**); stop at n − 1 edges. O(e log e).

**Round-robin algorithm (Sollin/Borůvka family).** Keep a **queue of trees**, initially every vertex alone. Repeatedly remove the tree at the front, find the **cheapest edge leaving it**, add that edge (merging it with another tree) and put the merged tree at the back. Stop when one tree remains. It is correct because the cheapest edge leaving any tree always belongs to some MST (the *cut property*).

**Prim's algorithm** grows one tree from a start vertex by repeatedly adding the cheapest edge to a new vertex.

## 10.6 Shortest paths: the greedy method and Dijkstra

A **greedy algorithm** builds a solution by always taking the best-looking choice at the moment, never reconsidering. It is correct only for problems with the *greedy-choice property* (Huffman, Kruskal, Prim, Dijkstra, fractional knapsack); for others it only approximates (Unit 11).

**Dijkstra's algorithm** finds shortest paths from one source in a graph with **non-negative** weights. Keep dist[v] (∞ initially, 0 for the source). Repeat: pick the unfinished vertex u with the smallest dist; mark it final; for each neighbour v relax: if dist[u] + w(u, v) < dist[v], update dist[v] and set the predecessor. O(n²) with an array, O((n + e) log n) with a heap. It fails with negative edges (use Bellman-Ford).

::: example Worked example
Graph (undirected, weights): 0–1: 7, 0–2: 9, 0–5: 14, 1–2: 10, 1–3: 15, 2–3: 11, 2–5: 2, 3–4: 6, 4–5: 9. Source 0.
Start dist = [0, ∞, ∞, ∞, ∞, ∞]. Finalise 0: dist 1 = 7, 2 = 9, 5 = 14. Finalise 1 (7): 3 = 22 (7 + 15); 2 stays 9 (7 + 10 = 17). Finalise 2 (9): 3 = 20, 5 = 11. Finalise 5 (11): 4 = 20. Finalise 3 (20) and 4 (20). **Final distances:** 1: 7, 2: 9, 3: 20, 4: 20, 5: 11. Path to 4: 0 → 2 → 5 → 4.
**Kruskal on the same graph:** edges by weight 2 (2–5), 6 (3–4), 7 (0–1), 9 (0–2), 9 (4–5), 10 (1–2, cycle), 11 (2–3, cycle), …. Chosen: 2–5, 3–4, 0–1, 0–2, 4–5: total **33** with 5 edges for 6 vertices.
**Round robin:** queue {0},{1},{2},{3},{4},{5}. {0} takes its cheapest edge 0–1 (7); the merged tree {0,1} goes to the back and {1} leaves the queue. {2} takes 2–5 (2) → {2,5}. {3} takes 3–4 (6) → {3,4}. {0,1} takes its cheapest leaving edge 0–2 (9) → {0,1,2,5}. {3,4} takes 4–5 (9) and everything is joined. Same five edges, total 33.
:::

## 10.7 Programs: BFS, DFS, Dijkstra, Kruskal, Warshall

The first program builds the example graph and runs BFS, DFS and Dijkstra; the second runs Kruskal's algorithm and Warshall's closure.

```c
#include <stdio.h>
#define N 6
#define INF 1000000
int w[N][N];                         /* weighted adjacency matrix, 0 = no edge */
void add(int u, int v, int c) { w[u][v] = w[v][u] = c; }
void graph(void) {
    add(0,1,7); add(0,2,9); add(0,5,14); add(1,2,10); add(1,3,15);
    add(2,3,11); add(2,5,2); add(3,4,6); add(4,5,9);
}

void bfs(int s) {
    int q[N], f = 0, r = 0, seen[N] = {0};
    q[r++] = s; seen[s] = 1;
    while (f < r) {
        int u = q[f++]; printf("%d ", u);
        for (int v = 0; v < N; v++) if (w[u][v] && !seen[v]) { seen[v] = 1; q[r++] = v; }
    }
}
int vis[N];
void dfs(int u) {
    vis[u] = 1; printf("%d ", u);
    for (int v = 0; v < N; v++) if (w[u][v] && !vis[v]) dfs(v);
}
void dijkstra(int s) {
    int d[N], done[N] = {0}, pred[N];
    for (int i = 0; i < N; i++) { d[i] = INF; pred[i] = -1; }
    d[s] = 0;
    for (int it = 0; it < N; it++) {
        int u = -1;
        for (int i = 0; i < N; i++) if (!done[i] && (u < 0 || d[i] < d[u])) u = i;
        done[u] = 1;
        for (int v = 0; v < N; v++)
            if (w[u][v] && d[u] + w[u][v] < d[v]) { d[v] = d[u] + w[u][v]; pred[v] = u; }
    }
    for (int i = 0; i < N; i++) {
        printf("  to %d: dist %2d, path:", i, d[i]);
        int path[N], k = 0; for (int x = i; x != -1; x = pred[x]) path[k++] = x;
        while (k--) printf(" %d", path[k]);
        printf("\n");
    }
}

int main(void) {
    graph();
    printf("BFS from 0: "); bfs(0);
    printf("\nDFS from 0: "); dfs(0);
    printf("\nDijkstra from 0:\n"); dijkstra(0);
    return 0;
}
```
```output
BFS from 0: 0 1 2 5 3 4 
DFS from 0: 0 1 2 3 4 5 
Dijkstra from 0:
  to 0: dist  0, path: 0
  to 1: dist  7, path: 0 1
  to 2: dist  9, path: 0 2
  to 3: dist 20, path: 0 2 3
  to 4: dist 20, path: 0 2 5 4
  to 5: dist 11, path: 0 2 5
```

```c
#include <stdio.h>
#define N 6
#define INF 1000000
int w[N][N];                         /* weighted adjacency matrix, 0 = no edge */
void add(int u, int v, int c) { w[u][v] = w[v][u] = c; }
void graph(void) {
    add(0,1,7); add(0,2,9); add(0,5,14); add(1,2,10); add(1,3,15);
    add(2,3,11); add(2,5,2); add(3,4,6); add(4,5,9);
}

int parent[N];
int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }

int main(void) {
    graph();
    int eu[20], ev[20], ec[20], m = 0;                 /* collect and sort the edges by weight */
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) if (w[i][j]) { eu[m] = i; ev[m] = j; ec[m] = w[i][j]; m++; }
    for (int i = 0; i < m; i++) for (int j = 0; j < m - 1 - i; j++) if (ec[j] > ec[j+1]) {
        int t; t = eu[j]; eu[j] = eu[j+1]; eu[j+1] = t; t = ev[j]; ev[j] = ev[j+1]; ev[j+1] = t; t = ec[j]; ec[j] = ec[j+1]; ec[j+1] = t; }
    for (int i = 0; i < N; i++) parent[i] = i;
    int total = 0;
    printf("Kruskal MST edges:");
    for (int i = 0; i < m; i++) {
        int x = find(eu[i]), y = find(ev[i]);
        if (x != y) { parent[x] = y; total += ec[i]; printf(" (%d-%d:%d)", eu[i], ev[i], ec[i]); }
    }
    printf("\nMST total weight = %d\n", total);

    int R[4][4] = {{0,1,0,0},{0,0,1,0},{0,0,0,1},{0,0,0,0}};      /* Warshall: digraph 0->1->2->3 */
    for (int k = 0; k < 4; k++) for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++)
        R[i][j] = R[i][j] || (R[i][k] && R[k][j]);
    printf("Warshall closure:\n");
    for (int i = 0; i < 4; i++) { printf("  "); for (int j = 0; j < 4; j++) printf("%d ", R[i][j]); printf("\n"); }
    return 0;
}
```
```output
Kruskal MST edges: (2-5:2) (3-4:6) (0-1:7) (0-2:9) (4-5:9)
MST total weight = 33
Warshall closure:
  0 1 1 1 
  0 0 1 1 
  0 0 0 1 
  0 0 0 0 
```

## Formula and fact sheet

- Σ deg(v) = 2|E|. Complete graph: n(n−1)/2 edges. Tree: n − 1 edges.
- Matrix O(n²) space; list O(n + e). BFS/DFS O(n + e) with lists.
- BFS = queue, shortest in edges; DFS = stack/recursion.
- Warshall: R[i][j] |= R[i][k] & R[k][j]; O(n³).
- MST: Kruskal O(e log e); cut property justifies Kruskal, Prim and round robin.
- Dijkstra: non-negative weights; relax dist[v] = min(dist[v], dist[u] + w).

## Chapter summary

- Graphs generalise trees; representation decides the cost of each operation.
- Warshall's algorithm computes reachability; BFS and DFS traverse in O(n + e) and produce spanning trees or forests.
- Kruskal and round-robin build minimum spanning trees greedily; Dijkstra computes shortest paths greedily.
- Greedy works only when the greedy-choice property holds.

## Practice

1. Define graph, degree, path, cycle, connected graph, tree.
2. A graph has degrees 3, 3, 2, 2, 2. How many edges? Draw an adjacency matrix for the triangle 1–2–3.
3. Compare adjacency matrix and list for a graph with 1,000 vertices and 3,000 edges.
4. Perform BFS and DFS from A on edges A–B, A–C, B–D, C–D, D–E (neighbours in alphabetical order).
5. Apply Warshall's algorithm to the digraph 0→1, 1→2, 2→0, 2→3.
6. Find the MST of: A–B 4, A–C 1, B–C 2, B–D 5, C–D 8, C–E 10, D–E 2 using Kruskal.
7. Run Dijkstra from A on A–B 4, A–C 2, B–C 1, B–D 5, C–D 8, D–E 3.
8. Why does Dijkstra fail with negative edges? Give an example.
9. State the cut property and say how it justifies Kruskal's algorithm.

::: note Answers and worked solutions
**1.** Graph: vertices plus edges. Degree: edges at a vertex. Path: sequence of adjacent edges. Cycle: path returning to its start. Connected: a path between every pair. Tree: connected and acyclic.
**2.** Σ degrees = 12, so |E| = **6**. Triangle matrix rows: 1: 0 1 1; 2: 1 0 1; 3: 1 1 0.
**3.** Matrix: 10⁶ cells. List: about 1,000 + 2·3,000 = 7,000 entries. The list is far smaller; the matrix tests a single edge in O(1).
**4.** BFS: A, B, C, D, E. DFS: A, B, D, C, E (A → B → D → then C via D, back, then E from D: visiting order A B D C E).
**5.** Edges 0→1, 1→2, 2→0, 2→3. Following paths: 0 reaches 1, 2, 0 (around the cycle) and 3; 1 reaches 2, 0, 1 and 3; 2 reaches 0, 1, 2 and 3; 3 reaches nothing. So the closure matrix has every entry 1 in rows 0–2 and a zero row for vertex 3. (Warshall reaches this by adding 2→1 at k = 0, then 0→2, 2→2 at k = 1, and the remaining pairs at k = 2.)
**6.** Edges by weight: A–C 1, B–C 2, D–E 2, B–D 5 (A–B 4 would form a cycle A–C–B, skip), then B–D joins {A,B,C} with {D,E}. Chosen: A–C, B–C, D–E, B–D: total 1 + 2 + 2 + 5 = **10**.
**7.** A 0; C 2 (A–C); B 3 (via C: 2 + 1); D 8 (via B: 3 + 5; via C: 2 + 8 = 10); E 11 (8 + 3). Paths: A–C–B–D–E.
**8.** Dijkstra finalises a vertex when it is the closest unfinished one, assuming later paths can only be longer; a negative edge can make a later path shorter. Example: A→B 2, A→C 3, C→B −2: Dijkstra finalises B at 2 but the true shortest A→B is 1.
**9.** For any cut of the vertices, the lightest edge crossing it belongs to some MST. Kruskal's next edge is the lightest edge between two different components, i.e. across a cut separating them, so it is always safe.
:::
