---
subject: Machine Learning
grade: BCA Semester 7 (Elective I)
unit: 4
title: Unsupervised Learning and Dimensionality Reduction
hours: 10
area: BCA 405 · Machine Learning · Unit 4
---

A telecom company has a million subscribers and no labels at all. It still wants to know: are there natural groups, such as heavy data users, voice-only users and occasional users? **Unsupervised learning** answers such questions without a teacher by discovering structure in unlabelled data. This unit covers clustering (k-means and hierarchical), the distance functions that define "similar", using clusters to help supervised learning, and **dimensionality reduction** with principal component analysis (PCA).

::: key What this unit gives you
- What clustering is, and how similarity is measured: Euclidean, Manhattan, Minkowski, cosine and Hamming distances.
- K-means: the algorithm, a hand-worked example, the elbow method and its limits.
- Hierarchical clustering: single, complete and average linkage, and how to read a dendrogram.
- Supervised learning after clustering, and why high dimensions are a problem.
- PCA: covariance, eigenvectors, explained variance, with a worked example.
:::

## 4.1 Introduction to clustering

**Clustering** partitions examples into groups (clusters) so that examples in the same cluster are *similar* and examples in different clusters are *dissimilar*. There is no single correct answer: the clusters depend on the features, the distance and the algorithm. Uses: customer segmentation, grouping news stories, image compression (colour clusters), detecting outliers (points far from every cluster), and organising search results.

| Family | Idea | Example |
|---|---|---|
| Partitioning | Choose k, assign points to the nearest centre | k-means, k-medoids |
| Hierarchical | Build a tree of nested clusters | Agglomerative, divisive |
| Density-based | Clusters are dense regions separated by sparse ones | DBSCAN |
| Model-based | Data comes from a mixture of distributions | Gaussian mixtures |

## 4.2 Different distance functions for clustering

For points $\mathbf{x}=(x_1,\dots,x_n)$ and $\mathbf{z}=(z_1,\dots,z_n)$:

| Distance | Formula | When to use |
|---|---|---|
| Euclidean | $\sqrt{\sum (x_i-z_i)^2}$ | Default for continuous features; straight-line distance |
| Manhattan (city block) | $\sum \lvert x_i-z_i\rvert$ | Grid-like movement; less sensitive to one large difference |
| Minkowski | $\left(\sum \lvert x_i-z_i\rvert^{p}\right)^{1/p}$ | General form: $p=1$ Manhattan, $p=2$ Euclidean |
| Chebyshev | $\max_i \lvert x_i-z_i\rvert$ | The largest single difference matters ($p\to\infty$) |
| Cosine | $1-\dfrac{\mathbf{x}\cdot\mathbf{z}}{\lVert\mathbf{x}\rVert\,\lVert\mathbf{z}\rVert}$ | Text and sparse vectors: direction, not length |
| Hamming | number of positions that differ | Binary or categorical strings |

**Mahalanobis distance** $\sqrt{(\mathbf{x}-\mathbf{z})^{T}S^{-1}(\mathbf{x}-\mathbf{z})}$ divides by the covariance $S$, so correlated features are not counted twice. Always **scale** the features first, or the largest-valued feature will decide every distance.

```python
import numpy as np
x = np.array([1.0, 2, 3]); z = np.array([4.0, 6, 3])
print("Euclidean ", np.sqrt(((x - z) ** 2).sum()))
print("Manhattan ", np.abs(x - z).sum())
print("Minkowski p=3 %.3f" % (np.abs(x - z) ** 3).sum() ** (1 / 3))
print("Chebyshev ", np.abs(x - z).max())
print("Cosine     %.4f" % (1 - x @ z / (np.linalg.norm(x) * np.linalg.norm(z))))
print("Hamming('10110','11100') =", sum(a != b for a, b in zip("10110", "11100")))
```
```output
Euclidean  5.0
Manhattan  7.0
Minkowski p=3 4.498
Chebyshev  4.0
Cosine     0.1445
Hamming('10110','11100') = 2
```
## 4.3 K-means clustering

**K-means** (Lloyd's algorithm) partitions $N$ points into $k$ clusters, each represented by its **centroid** (mean).

1. Choose $k$ and pick $k$ initial centroids (random points, or *k-means++* which spreads them out).
2. **Assign** each point to its nearest centroid.
3. **Update** each centroid to the mean of its assigned points.
4. Repeat 2 and 3 until the assignments no longer change.

It minimises the **within-cluster sum of squares** $\mathrm{WCSS}=\sum_{j=1}^{k}\sum_{\mathbf{x}\in C_j}\lVert\mathbf{x}-\boldsymbol\mu_j\rVert^{2}$. Each step lowers (or keeps) WCSS, so the algorithm always stops, but only at a *local* minimum: different starting centroids can give different clusters, so run it several times and keep the lowest WCSS.

::: example K-means on nine numbers, k = 2
Data: 2, 3, 4, 10, 11, 12, 20, 25, 30. Start with centroids $\mu_1=2$ and $\mu_2=4$. *Iteration 1:* 2 and 3 go to $\mu_1$ (3 is equidistant, ties go to the first); 4, 10, 11, 12, 20, 25, 30 go to $\mu_2$. New means: $\mu_1=2.5$, $\mu_2=112/7=16$ (WCSS 514.5). *Iteration 2:* 4 is now nearer $\mu_1$, so means become 3 and 18 (WCSS 348). *Iteration 3:* 10 moves to the first cluster: 4.75 and 19.6 (WCSS 307.9). *Iteration 4:* 11 and 12 move: means 7 and 25 (WCSS 150). *Iteration 5* changes nothing, so the algorithm stops with clusters {2, 3, 4, 10, 11, 12} and {20, 25, 30}. The program below reproduces the trace.
:::

```python
import numpy as np
X = np.array([2, 3, 4, 10, 11, 12, 20, 25, 30.0]); mu = np.array([2.0, 4.0])
for it in range(1, 10):
    assign = np.argmin(np.abs(X[:, None] - mu[None, :]), axis=1)
    new = np.array([X[assign == j].mean() for j in range(2)])
    wcss = sum(((X[assign == j] - new[j]) ** 2).sum() for j in range(2))
    print("iter", it, "clusters", [X[assign == j].tolist() for j in range(2)], "means", np.round(new, 2), "WCSS %.1f" % wcss)
    if np.allclose(new, mu): break
    mu = new
```
```output
iter 1 clusters [[2.0, 3.0], [4.0, 10.0, 11.0, 12.0, 20.0, 25.0, 30.0]] means [ 2.5 16. ] WCSS 514.5
iter 2 clusters [[2.0, 3.0, 4.0], [10.0, 11.0, 12.0, 20.0, 25.0, 30.0]] means [ 3. 18.] WCSS 348.0
iter 3 clusters [[2.0, 3.0, 4.0, 10.0], [11.0, 12.0, 20.0, 25.0, 30.0]] means [ 4.75 19.6 ] WCSS 307.9
iter 4 clusters [[2.0, 3.0, 4.0, 10.0, 11.0, 12.0], [20.0, 25.0, 30.0]] means [ 7. 25.] WCSS 150.0
iter 5 clusters [[2.0, 3.0, 4.0, 10.0, 11.0, 12.0], [20.0, 25.0, 30.0]] means [ 7. 25.] WCSS 150.0
```
**Choosing k: the elbow method.** Run k-means for $k=1,2,3,\dots$ and plot WCSS against $k$. WCSS always falls as $k$ grows; the **elbow**, where the fall slows sharply, suggests a good $k$. The **silhouette score** $s=(b-a)/\max(a,b)$ (with $a$ the mean distance to its own cluster and $b$ to the nearest other cluster) ranges from −1 to 1; higher is better.

**Limitations.** The user must choose $k$; the result depends on initialisation; clusters are assumed to be round and of similar size (k-means fails on rings or long thin shapes); one outlier can drag a centroid (**k-medoids** uses a real data point as the centre and is more robust); and categorical features need other distances.

## 4.4 Hierarchical clustering

**Hierarchical clustering** builds a tree of clusters and does not need $k$ in advance. **Agglomerative** (bottom-up): start with every point as its own cluster and repeatedly merge the two closest clusters until one remains. **Divisive** (top-down) starts with one cluster and splits. The record of merges is drawn as a **dendrogram**; cutting it at a chosen height gives a flat clustering.

The distance between two *clusters* is called the **linkage**:

| Linkage | Distance between clusters A and B | Behaviour |
|---|---|---|
| Single | smallest distance between a point of A and a point of B | Can chain along a line of points; finds long shapes; sensitive to noise |
| Complete | largest distance between a point of A and a point of B | Compact, similar-sized clusters |
| Average | mean of all pairwise distances | A compromise |
| Ward | merge that least increases the total within-cluster variance | Compact clusters; common default |

::: example Five points on a line: 1, 2, 6, 8, 15
*Single linkage.* The closest pair is {1,2} (distance 1), then {6,8} (2). The distance between {1,2} and {6,8} is $6-2=4$, so they merge at 4. The point 15 is $15-8=7$ from the nearest, so it joins at 7. *Complete linkage.* {1,2} at 1 and {6,8} at 2 as before; then {1,2} and {6,8} are $8-1=7$ apart, and 15 is $15-6=9$ from {6,8}, so they merge at 7; finally 15 joins at $15-1=14$. Cutting the single-linkage tree at height 5 gives {1,2,6,8} and {15}.
:::

```python
pts = {"A": 1, "B": 2, "C": 6, "D": 8, "E": 15}
def agglomerate(link):
    clusters = [[n] for n in pts]
    while len(clusters) > 1:
        best = None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                ds = [abs(pts[a] - pts[b]) for a in clusters[i] for b in clusters[j]]
                d = {"single": min, "complete": max, "average": lambda v: sum(v) / len(v)}[link](ds)
                if best is None or d < best[0]: best = (d, i, j)
        d, i, j = best
        print("  merge", clusters[i], "+", clusters[j], "at distance", round(d, 2))
        clusters[i] = clusters[i] + clusters[j]; del clusters[j]
for link in ("single", "complete", "average"):
    print(link); agglomerate(link)
```
```output
single
  merge ['A'] + ['B'] at distance 1
  merge ['C'] + ['D'] at distance 2
  merge ['A', 'B'] + ['C', 'D'] at distance 4
  merge ['A', 'B', 'C', 'D'] + ['E'] at distance 7
complete
  merge ['A'] + ['B'] at distance 1
  merge ['C'] + ['D'] at distance 2
  merge ['A', 'B'] + ['C', 'D'] at distance 7
  merge ['A', 'B', 'C', 'D'] + ['E'] at distance 14
average
  merge ['A'] + ['B'] at distance 1.0
  merge ['C'] + ['D'] at distance 2.0
  merge ['A', 'B'] + ['C', 'D'] at distance 5.5
  merge ['A', 'B', 'C', 'D'] + ['E'] at distance 10.75
```
```svgfig label="4.1" caption="Dendrogram for the five points 1, 2, 6, 8 and 15 with single linkage. The height of each join is the distance at which the clusters merge. A horizontal cut at height 5 (dashed) leaves two clusters, {A, B, C, D} and {E}."
f = Fig(580, 240)
ax = Axes(f, 60, 15, 300, 180, (0, 5), (0, 8))
ax.axes("", "")
xs = {"A": 0.5, "B": 1.5, "C": 2.5, "D": 3.5, "E": 4.5}
for n, x in xs.items():
    f.text(ax.X(x), 212, n, size=11, color=NAVY, bold=True)
def U(x1, y1, x2, y2, h):
    f.line(ax.X(x1), ax.Y(y1), ax.X(x1), ax.Y(h), color=NAVY, sw=2)
    f.line(ax.X(x2), ax.Y(y2), ax.X(x2), ax.Y(h), color=NAVY, sw=2)
    f.line(ax.X(x1), ax.Y(h), ax.X(x2), ax.Y(h), color=NAVY, sw=2)
U(0.5, 0, 1.5, 0, 1); U(2.5, 0, 3.5, 0, 2)
U(1.0, 1, 3.0, 2, 4); U(2.0, 4, 4.5, 0, 7)
for h in (0, 2, 4, 6, 8):
    f.text(48, ax.Y(h) + 4, str(h), size=9.5, color=SLATE, anchor="end")
ax.hline(5, color=RED)
f.text(450, 70, "cut at height 5", size=10.5, color=RED, bold=True)
f.text(450, 90, "gives 2 clusters", size=10.5, color=RED)
f.text(450, 140, "merge heights:", size=10.5, color=NAVY, bold=True)
f.text(450, 158, "1, 2, 4, 7", size=10.5, color=NAVY)
```

**Strengths and weaknesses.** No need to choose $k$ first and the dendrogram shows structure at every scale, but the cost is at least $O(N^2)$ memory and time, so it suits thousands rather than millions of points; a merge can never be undone.

## 4.5 Supervised learning after clustering

Clustering and supervised learning combine in three common ways:

1. **Cluster, then label.** Cluster all data, ask an expert to label only a few examples per cluster, and give every point the label of its cluster. This turns a few labels into many, the idea behind **semi-supervised learning**.
2. **Cluster as a feature.** Add the cluster number (or the distances to the k centroids) as new input features for a classifier. A tree or a linear model then captures non-linear groups cheaply.
3. **One model per cluster.** Train a separate regressor for each customer segment when the segments behave differently, instead of one model for everyone.

Because the clusters were found without labels, check on a labelled validation set that they help; clusters that match the labels poorly give no gain.

## 4.6 Dimensionality reduction techniques

A data set with hundreds of features is hard to visualise, slow to process and prone to over-fitting, since the volume of space grows so fast that data becomes sparse (the curse of dimensionality, Section 3.5). **Dimensionality reduction** maps the data to fewer dimensions while keeping the useful information.

- **Feature selection** keeps a subset of the original features (drop features with near-zero variance, high correlation with another feature, or low relevance to the label). Results stay interpretable.
- **Feature extraction** builds new features from combinations of the old ones. **PCA** (linear, unsupervised) is the standard; **LDA** (linear discriminant analysis) uses labels to find directions that separate the classes; **t-SNE** and **UMAP** give non-linear 2-D pictures for visualisation.

## 4.7 Principal component analysis (PCA)

PCA finds new axes, the **principal components**, such that the first points along the direction of **greatest variance**, the second along the greatest remaining variance at a right angle to the first, and so on. Keeping only the first few components compresses the data with minimum loss of variance.

**Procedure.**

1. **Centre** the data: subtract the mean of each feature (and standardise if scales differ).
2. Compute the **covariance matrix** $S=\frac{1}{N-1}X^{T}X$.
3. Find its **eigenvalues** $\lambda_1\ge\lambda_2\ge\dots$ and unit **eigenvectors** $\mathbf{v}_1,\mathbf{v}_2,\dots$ by solving $\det(S-\lambda I)=0$.
4. Choose the first $m$ components, using the **explained variance ratio** $\lambda_j/\sum\lambda$ (keep enough for, say, 95 percent).
5. **Project**: $Z = X\,V_m$ gives the new $m$-dimensional coordinates.

::: example Four points in two dimensions
Points (4,11), (8,4), (13,5), (7,14); mean (8, 8.5). Deviations: (−4, 2.5), (0, −4.5), (5, −3.5), (−1, 5.5). Variances: $s_{xx}=(16+0+25+1)/3=14$ and $s_{yy}=(6.25+20.25+12.25+30.25)/3=23$; covariance $s_{xy}=(-10+0-17.5-5.5)/3=-11$. So $S=\begin{pmatrix}14&-11\\-11&23\end{pmatrix}$. The characteristic equation is $\lambda^{2}-37\lambda+201=0$, so $\lambda=\dfrac{37\pm\sqrt{565}}{2}=30.38$ and $6.62$. The first component explains $30.38/37 = 82.1$ percent of the variance, with direction $(0.557,-0.830)$.
:::

```python
import numpy as np
X = np.array([[4, 11], [8, 4], [13, 5], [7, 14.0]])
Xc = X - X.mean(axis=0)
S = Xc.T @ Xc / (len(X) - 1)
vals, vecs = np.linalg.eigh(S)
vals, vecs = vals[::-1], vecs[:, ::-1]
print("covariance matrix:\n", S)
print("eigenvalues:", np.round(vals, 3), "explained ratio:", np.round(vals / vals.sum(), 3))
v1 = vecs[:, 0] * (1 if vecs[0, 0] > 0 else -1)
print("first component:", np.round(v1, 3))
print("projections onto PC1:", np.round(Xc @ v1, 2))
print("variance of projections:", round(float((Xc @ v1).var(ddof=1)), 3))
```
```output
covariance matrix:
 [[ 14. -11.]
 [-11.  23.]]
eigenvalues: [30.385  6.615] explained ratio: [0.821 0.179]
first component: [ 0.557 -0.83 ]
projections onto PC1: [-4.31  3.74  5.69 -5.12]
variance of projections: 30.385
```
**Uses and cautions.** PCA speeds up learning, removes correlated features, compresses images and gives 2-D plots. Components are mixtures of features and hard to interpret; PCA is linear (curved structure is missed); it is sensitive to scale (standardise first); and high variance is not the same as usefulness for predicting a label.

## 4.8 Choosing k in practice: elbow and silhouette

Real data rarely shows an obvious k, so run k-means for a range of k and look at two curves. The program builds three well-separated groups of 40 points each in two dimensions, runs k-means with several restarts for k = 1 to 6, and prints the WCSS and the mean silhouette score.

```python
import numpy as np
rng = np.random.default_rng(2)
X = np.vstack([rng.normal(c, 0.6, (40, 2)) for c in ((0, 0), (5, 1), (2, 5))])
def kmeans(X, k, restarts=8):
    best = None
    for _ in range(restarts):
        mu = X[rng.choice(len(X), k, replace=False)]
        for _ in range(100):
            lab = np.argmin(((X[:, None] - mu[None]) ** 2).sum(-1), axis=1)
            new = np.array([X[lab == j].mean(0) if (lab == j).any() else mu[j] for j in range(k)])
            if np.allclose(new, mu): break
            mu = new
        w = sum(((X[lab == j] - mu[j]) ** 2).sum() for j in range(k))
        if best is None or w < best[0]: best = (w, lab)
    return best
def silhouette(X, lab):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); s = []
    for i in range(len(X)):
        same = (lab == lab[i]) & (np.arange(len(X)) != i)
        a = D[i, same].mean() if same.any() else 0
        b = min(D[i, lab == j].mean() for j in set(lab) if j != lab[i])
        s.append((b - a) / max(a, b))
    return float(np.mean(s))
print("k   WCSS     silhouette")
for k in range(1, 7):
    w, lab = kmeans(X, k)
    print("%d  %7.1f   %s" % (k, w, "   n/a" if k == 1 else "%.3f" % silhouette(X, lab)))
```
```output
k   WCSS     silhouette
1   1133.9      n/a
2    580.4   0.538
3     86.5   0.777
4     72.3   0.636
5     62.1   0.486
6     50.8   0.369
```
The WCSS falls steeply from k = 1 to 3 and only slowly afterwards: the elbow is at **k = 3**, and the silhouette score peaks at k = 3 as well, so both methods agree with the three groups that generated the data.

```svgfig label="4.2" caption="The elbow method. Within-cluster sum of squares (WCSS) falls steeply until k = 3, the number of groups that generated the data, and then flattens. The elbow marks the best k."
import numpy as np
rng = np.random.default_rng(2)
X = np.vstack([rng.normal(c, 0.6, (40, 2)) for c in ((0, 0), (5, 1), (2, 5))])
def km(k):
    best = 1e18
    for _ in range(8):
        mu = X[rng.choice(len(X), k, replace=False)]
        for _ in range(100):
            lab = np.argmin(((X[:, None] - mu[None]) ** 2).sum(-1), axis=1)
            new = np.array([X[lab == j].mean(0) if (lab == j).any() else mu[j] for j in range(k)])
            if np.allclose(new, mu): break
            mu = new
        best = min(best, sum(((X[lab == j] - mu[j]) ** 2).sum() for j in range(k)))
    return best
W = [km(k) for k in range(1, 7)]
f = Fig(580, 230)
ax = Axes(f, 70, 15, 330, 170, (0.5, 6.5), (0, 500))
ax.grid(1, 100)
ax.axes("", "")
for k in range(1, 7):
    f.text(ax.X(k), 205, str(k), size=10.5, color=SLATE)
for k in range(1, 6):
    f.line(ax.X(k), ax.Y(W[k - 1]), ax.X(k + 1), ax.Y(W[k]), color=NAVY, sw=2.4)
for k in range(1, 7):
    ax.pt(k, W[k - 1], "", r=4.5, color=(RED if k == 3 else NAVY))
f.text(235, 226, "number of clusters k", size=10.5, color=SLATE)
f.text(490, 80, "elbow at k = 3", size=11, color=RED, bold=True)
f.text(490, 102, "WCSS drops from", size=10.5, color=SLATE)
f.text(490, 120, "%d to %d, then slowly" % (W[0], W[2]), size=10.5, color=SLATE)
```

## 4.9 Density-based clustering: DBSCAN

K-means assumes round clusters of similar size. Real groups can be crescents, rings or long chains, and real data contain outliers that should belong to no cluster. **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) defines a cluster as a dense region separated from other dense regions by sparse space. It needs two parameters: a radius $\varepsilon$ and a count $\text{minPts}$.

::: definition Core, border and noise points
A point is a **core point** if at least minPts points (itself included) lie within distance $\varepsilon$. A **border point** is not core but lies within $\varepsilon$ of a core point. Every other point is **noise**. A cluster is a maximal set of core points that are reachable from one another through chains of core points, plus their border points.
:::

The algorithm visits points in turn. When it finds an unlabelled core point it starts a new cluster and keeps absorbing every point within $\varepsilon$ of any core point already in the cluster. The number of clusters is not given; it falls out of the data. The program builds two interleaved half-moons of 150 points each plus 12 random outliers and compares k-means with DBSCAN at four radii.

```python
import numpy as np
rng = np.random.default_rng(4)
n = 150
t = rng.uniform(0, np.pi, n)
A = np.c_[np.cos(t), np.sin(t)] + rng.normal(0, 0.07, (n, 2))                # upper moon
B = np.c_[1 - np.cos(t), 0.5 - np.sin(t)] + rng.normal(0, 0.07, (n, 2))      # lower moon
X = np.vstack([A, B, rng.uniform(-1.5, 2.5, (12, 2))]); truth = np.r_[np.zeros(n), np.ones(n), -np.ones(12)].astype(int)
def kmeans(X, k, seed=0):
    r = np.random.default_rng(seed); mu = X[r.choice(len(X), k, replace=False)]
    for _ in range(100):
        lab = np.argmin(((X[:, None] - mu[None]) ** 2).sum(-1), 1)
        new = np.array([X[lab == j].mean(0) for j in range(k)])
        if np.allclose(new, mu): break
        mu = new
    return lab
def dbscan(X, eps, min_pts):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    nbr = [np.flatnonzero(D[i] <= eps) for i in range(len(X))]
    core = np.array([len(v) >= min_pts for v in nbr])
    lab = -np.ones(len(X), int); c = 0
    for i in range(len(X)):
        if lab[i] != -1 or not core[i]: continue
        lab[i] = c; stack = [i]
        while stack:
            p = stack.pop()
            if not core[p]: continue
            for q in nbr[p]:
                if lab[q] == -1: lab[q] = c; stack.append(q)
        c += 1
    return lab, core
def purity(lab, mask):
    ok = 0
    for c in set(lab[mask]) - {-1}:
        ok += np.bincount(truth[mask][lab[mask] == c]).max()
    return ok / mask.sum()
real = truth >= 0
km = kmeans(X, 2)
print("k-means (k=2): purity on the 300 moon points = %.3f" % purity(km, real))
for eps, mp in ((0.08, 5), (0.15, 5), (0.25, 5), (0.5, 5)):
    lab, core = dbscan(X, eps, mp)
    kinds = len(set(lab) - {-1})
    print("DBSCAN eps=%.2f minPts=%d: clusters=%d  noise points=%3d  core points=%3d  purity=%.3f" % (eps, mp, kinds, (lab == -1).sum(), core.sum(), purity(lab, real & (lab >= 0)) if kinds else 0))
lab, core = dbscan(X, 0.15, 5)
print("true outliers labelled noise at eps=0.15: %d of 12" % ((lab == -1) & (truth == -1)).sum())
```
```output
k-means (k=2): purity on the 300 moon points = 0.820
DBSCAN eps=0.08 minPts=5: clusters=22  noise points= 88  core points=147  purity=1.000
DBSCAN eps=0.15 minPts=5: clusters=2  noise points= 10  core points=291  purity=1.000
DBSCAN eps=0.25 minPts=5: clusters=2  noise points=  9  core points=302  purity=1.000
DBSCAN eps=0.50 minPts=5: clusters=1  noise points=  6  core points=306  purity=0.500
true outliers labelled noise at eps=0.15: 9 of 12
```

K-means cuts the plane with a straight line between two round centres and mixes the moons (purity 0.82). DBSCAN with $\varepsilon=0.15$ finds exactly two clusters, assigns 10 points to noise (9 of the 12 real outliers plus one straggler) and separates the moons perfectly. The other rows show how sensitive the method is to $\varepsilon$: at 0.08 the moons shatter into 22 fragments because the density is not reached; at 0.5 the gap between the moons is bridged and everything merges into one cluster. A standard way to choose $\varepsilon$ is the **k-distance plot**: sort each point's distance to its minPts-th neighbour and set $\varepsilon$ at the knee of the curve. DBSCAN struggles when clusters have very different densities (one $\varepsilon$ cannot suit both) and in high dimensions where distances concentrate (Section 3.9).

| Aspect | K-means | DBSCAN |
|---|---|---|
| Needs k in advance | Yes | No (needs $\varepsilon$ and minPts) |
| Cluster shape | Round, similar size | Arbitrary |
| Outliers | Pulled into clusters | Marked as noise |
| Deterministic | Depends on initial centroids | Yes (except border point ties) |
| Cost | $O(Nkt)$ | $O(N^2)$, or $O(N\log N)$ with an index |

## 4.10 Soft clustering: Gaussian mixtures and the EM algorithm

K-means assigns every point to exactly one cluster (**hard** assignment). A **Gaussian mixture model** (GMM) assumes the data come from $K$ bell curves, chosen with probabilities $\pi_k$, and gives every point a **responsibility** $r_{ik}$, the probability that component $k$ produced point $i$. A customer at the border of two segments can be 60 percent in one and 40 percent in the other.

The parameters $(\pi_k,\mu_k,\sigma_k)$ are fitted by **maximum likelihood**, but the component memberships are hidden, so the likelihood cannot be maximised in closed form. The **expectation-maximisation (EM)** algorithm alternates two steps (Mitchell, section 6.12):

1. **E-step:** with the current parameters compute $r_{ik}=\dfrac{\pi_k\,\mathcal N(x_i\mid\mu_k,\sigma_k)}{\sum_j \pi_j\,\mathcal N(x_i\mid\mu_j,\sigma_j)}$.
2. **M-step:** re-estimate $N_k=\sum_i r_{ik}$, $\pi_k=N_k/N$, $\mu_k=\sum_i r_{ik}x_i/N_k$ and $\sigma_k^2=\sum_i r_{ik}(x_i-\mu_k)^2/N_k$.

Each pair of steps never decreases the log-likelihood, so EM converges, but only to a **local** maximum; as with k-means, run it from several starts. K-means is the special case of EM with equal, spherical, vanishingly small variances, where responsibilities become 0 or 1.

The program draws 300 points from a 40/60 mixture of $N(0,1)$ and $N(4,1.2^2)$, starts EM from a deliberately poor guess (means 1 and 2) and prints the progress.

```python
import numpy as np
rng = np.random.default_rng(8)
x = np.r_[rng.normal(0, 1.0, 120), rng.normal(4, 1.2, 180)]          # true mixture: 40% N(0,1), 60% N(4,1.2^2)
pdf = lambda x, m, s: np.exp(-(x - m) ** 2 / (2 * s ** 2)) / (s * np.sqrt(2 * np.pi))
pi, mu, sd = np.array([0.5, 0.5]), np.array([1.0, 2.0]), np.array([1.0, 1.0])    # poor starting guess
print("iter  log-lik    weights       means         std devs")
for it in range(0, 31):
    dens = np.array([pi[k] * pdf(x, mu[k], sd[k]) for k in range(2)])            # shape (2, N)
    ll = np.log(dens.sum(0)).sum()
    r = dens / dens.sum(0)                                                       # E-step: responsibilities
    if it in (0, 1, 2, 3, 5, 10, 20, 30):
        print("%-4d  %8.2f   %s  %s  %s" % (it, ll, np.round(pi, 3), np.round(mu, 3), np.round(sd, 3)))
    Nk = r.sum(1)                                                                # M-step
    pi = Nk / len(x)
    mu = (r * x).sum(1) / Nk
    sd = np.sqrt((r * (x - mu[:, None]) ** 2).sum(1) / Nk)
print("true parameters used to generate the data: weights (0.4, 0.6), means (0, 4), std devs (1.0, 1.2)")
i = 100
print("point x = %.2f: responsibility of component 1 = %.3f" % (x[i], r[0, i]))
print("point x = 2.0:  responsibility of component 1 = %.3f" % (pi[0] * pdf(2.0, mu[0], sd[0]) / (pi[0] * pdf(2.0, mu[0], sd[0]) + pi[1] * pdf(2.0, mu[1], sd[1]))))
```
```output
iter  log-lik    weights       means         std devs
0     -1056.00   [0.5 0.5]  [1. 2.]  [1. 1.]
1      -658.09   [0.381 0.619]  [0.327 3.679]  [1.579 1.641]
2      -649.81   [0.387 0.613]  [0.173 3.809]  [1.395 1.499]
3      -642.55   [0.391 0.609]  [0.053 3.913]  [1.227 1.361]
5      -638.77   [0.394 0.606]  [-0.045  3.994]  [1.069 1.233]
10     -638.65   [0.39 0.61]  [-0.077  3.99 ]  [1.033 1.225]
20     -638.64   [0.387 0.613]  [-0.092  3.977]  [1.023 1.234]
30     -638.64   [0.386 0.614]  [-0.095  3.974]  [1.02  1.237]
true parameters used to generate the data: weights (0.4, 0.6), means (0, 4), std devs (1.0, 1.2)
point x = 0.94: responsibility of component 1 = 0.902
point x = 2.0:  responsibility of component 1 = 0.249
```

The log-likelihood rises from $-1056$ to $-658$ in a single iteration and then creeps up to $-638.64$; by iteration 10 the estimates are close to the truth, and at iteration 30 they are weights 0.386 and 0.614, means $-0.095$ and 3.974, standard deviations 1.02 and 1.24, all within sampling error of the generating values. The last lines show soft assignment: the point at $x=0.94$ belongs to component 1 with probability 0.90, while a point at $x=2.0$, between the two means, belongs to it with probability only 0.25. Model selection works as for $k$: fit several $K$ and choose by held-out likelihood or by the **BIC** criterion, which penalises extra parameters.

## 4.11 Linear discriminant analysis versus PCA

PCA is **unsupervised**: it keeps the directions of largest variance and never looks at labels. When the direction that separates the classes is not the direction of largest variance, PCA throws away exactly the information a classifier needs. **Linear discriminant analysis (LDA)**, Fisher's method, is **supervised**. For two classes it chooses the projection $\mathbf w$ that maximises the ratio of between-class to within-class scatter:

$$J(\mathbf w)=\frac{(\mathbf w^{T}\mathbf m_1-\mathbf w^{T}\mathbf m_0)^2}{\mathbf w^{T}S_W\mathbf w},\qquad \mathbf w\propto S_W^{-1}(\mathbf m_1-\mathbf m_0),$$

where $\mathbf m_c$ are the class means and $S_W$ is the within-class scatter matrix (the sum of the class scatter matrices). For $C$ classes LDA gives at most $C-1$ useful directions, which makes it a dimensionality reduction method that is also a classifier.

The program creates two classes that are very wide in $x$ (variance 9) but differ only in $y$ (means 0 and 2, variance 0.6), then projects onto the first PCA axis and onto the LDA direction, and classifies in one dimension with a midpoint threshold.

```python
import numpy as np
rng = np.random.default_rng(6)
cov = np.array([[9.0, 0.0], [0.0, 0.6]])
X0 = rng.multivariate_normal([0, 0], cov, 100); X1 = rng.multivariate_normal([0, 2.0], cov, 100)   # classes differ only in y
X = np.vstack([X0, X1]); y = np.r_[np.zeros(100), np.ones(100)]
m0, m1 = X0.mean(0), X1.mean(0)
Sw = np.cov(X0.T) * 99 + np.cov(X1.T) * 99
w_lda = np.linalg.solve(Sw, m1 - m0); w_lda /= np.linalg.norm(w_lda)
vals, vecs = np.linalg.eigh(np.cov(X.T)); w_pca = vecs[:, -1]
def fisher(w):
    p0, p1 = X0 @ w, X1 @ w
    return (p1.mean() - p0.mean()) ** 2 / (p0.var() + p1.var())
def threshold_acc(w):
    p = X @ w; s = np.sign(np.mean(p[y == 1]) - np.mean(p[y == 0]))
    th = (np.mean(p[y == 1]) + np.mean(p[y == 0])) / 2
    return np.mean(((p - th) * s > 0) == (y == 1))
print("class means:", np.round(m0, 2), np.round(m1, 2))
print("PCA first axis  w = (%.3f, %.3f)  Fisher ratio %.3f  1-D accuracy %.3f" % (w_pca[0], w_pca[1], fisher(w_pca), threshold_acc(w_pca)))
print("LDA direction   w = (%.3f, %.3f)  Fisher ratio %.3f  1-D accuracy %.3f" % (w_lda[0], w_lda[1], fisher(w_lda), threshold_acc(w_lda)))
print("variance along PCA axis %.2f, along LDA axis %.2f" % (np.var(X @ w_pca), np.var(X @ w_lda)))
```
```output
class means: [-0.    0.12] [-0.26  1.97]
PCA first axis  w = (-1.000, -0.018)  Fisher ratio 0.003  1-D accuracy 0.525
LDA direction   w = (-0.036, 0.999)  Fisher ratio 2.999  1-D accuracy 0.885
variance along PCA axis 9.74, along LDA axis 1.45
```

PCA picks the $x$-axis because that is where the variance is (9.74), but the classes overlap completely along it: Fisher ratio 0.003 and accuracy 0.525, a coin toss. LDA picks the $y$-axis, with ratio 3.0 and accuracy 0.885, even though the variance along it is only 1.45. The lesson: use PCA to compress features or remove noise, and LDA when the goal is class separation and labels are available. LDA assumes roughly Gaussian classes with a common covariance; with few samples and many features $S_W$ becomes singular, so combine it with PCA first or add a small ridge term.

## 4.12 Summary and exercises

Clustering groups unlabelled data using a distance; k-means alternates assignment and centroid update to reduce WCSS; hierarchical clustering merges clusters by a linkage and is read from a dendrogram; clusters can supply labels or features to supervised learners; PCA rotates the data to the directions of largest variance and keeps the first few.

1. Compute the Euclidean, Manhattan and Chebyshev distances between (2, 3, 5) and (6, 0, 5).
2. Apply k-means with k = 2 to the points 1, 2, 3, 8, 9, 10 starting from centroids 1 and 2.
3. Why can two runs of k-means give different clusters? How do you reduce this problem?
4. Explain the elbow method.
5. Perform agglomerative clustering with single linkage on 3, 4, 9, 11, 20 and draw the dendrogram.
6. Differentiate single, complete and average linkage.
7. Give two ways in which clustering can help a supervised learner.
8. Find the principal components of data with covariance matrix [[5, 2], [2, 2]] and the variance explained by the first.
9. Differentiate feature selection and feature extraction.
10. Define core, border and noise points in DBSCAN. For $\varepsilon=1$ and minPts = 3, classify each of the points 1, 1.5, 2, 5, 9 on a line.
11. Why can DBSCAN find crescent-shaped clusters that k-means cannot? State two drawbacks of DBSCAN.
12. Explain the E-step and M-step of EM for a Gaussian mixture. Why does EM only reach a local maximum?
13. Differentiate hard and soft clustering with an example from customer segmentation.
14. For two classes with means $(1,1)$ and $(3,3)$ and within-class scatter $S_W=I$, find the LDA direction.
15. When does PCA give a bad projection for classification? How does LDA fix this?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distances between (2,3,5) and (6,0,5).**

Differences are (−4, 3, 0). Euclidean $=\sqrt{16+9+0}=5$; Manhattan $=4+3+0=7$; Chebyshev $=\max(4,3,0)=4$.

**Q2 (5 marks). K-means on 1, 2, 3, 8, 9, 10 with initial centroids 1 and 2.**

Iteration 1: assignment: 1 → c1 (1); 2, 3, 8, 9, 10 → c2 (2). New centroids: 1 and (2+3+8+9+10)/5 = 6.4. Iteration 2: 1 → c1; 2 (distance 1 against 4.4) → c1; 3 (2 against 3.4) → c1; 8, 9, 10 → c2. New centroids: 2 and 9. Iteration 3: assignments are unchanged: {1,2,3} and {8,9,10}. Final centroids 2 and 9; WCSS $=2+2=4$.

**Q3 (5 marks). Agglomerative single linkage on 3, 4, 9, 11, 20.**

Distances between neighbours: 3-4 = 1, 4-9 = 5, 9-11 = 2, 11-20 = 9. Merge {3,4} at 1, {9,11} at 2, then {3,4} with {9,11} at $9-4=5$, and finally 20 at $20-11=9$. Dendrogram heights 1, 2, 5, 9; cutting at 6 gives {3,4,9,11} and {20}.

**Q4 (10 marks). Explain k-means clustering with its advantages and limitations.**

*Introduction.* K-means is the most widely used partitioning clustering method; it represents each cluster by its mean.

*Body.* (1) Choose k and initial centroids. (2) Assign each point to the nearest centroid. (3) Recompute each centroid as the mean of its points. (4) Repeat until the assignments no longer change. (5) It minimises WCSS and always converges, to a local minimum. (6) Example: Section 4.3 trace on nine numbers, WCSS 514.5 → 348 → 307.9 → 150. (7) Choosing k by the elbow or silhouette.

*Advantages.* Simple, fast ($O(Nkt)$), scales to large data. *Limitations.* k must be given; sensitive to initialisation and outliers; assumes round, equal-sized clusters; only numeric features.

*Conclusion.* Use k-means with k-means++ initialisation, several restarts and scaled features, and check the result by elbow and silhouette.

**Q5 (10 marks). Principal component analysis: steps and a worked example.**

*Introduction.* PCA is a linear method that rotates the data to new axes ordered by variance so that a few components keep most of the information.

*Steps.* Centre the data; compute the covariance matrix; find eigenvalues and eigenvectors; sort by eigenvalue; choose the number of components from the explained variance; project.

*Worked example.* For $S=\begin{pmatrix}5&2\\2&2\end{pmatrix}$ the characteristic equation is $\lambda^2-7\lambda+6=0$, so $\lambda_1=6$, $\lambda_2=1$. For $\lambda_1=6$: $(5-6)a+2b=0$, so $b=a/2$ and the unit eigenvector is $(2,1)/\sqrt5=(0.894,0.447)$. The first component explains $6/7=85.7$ percent of the variance; the second, at right angles, $(−0.447, 0.894)$, explains 14.3 percent.

*Conclusion.* Keeping only PC1 reduces two dimensions to one while retaining 85.7 percent of the variance; the rule is to keep components until the cumulative ratio reaches about 95 percent.

**Q6 (5 marks). DBSCAN labels for 1, 1.5, 2, 5, 9 with $\varepsilon=1$, minPts = 3.**

Neighbours within distance 1 (the point itself counts): point 1: {1, 1.5, 2} has 3, so core. Point 1.5: {1, 1.5, 2} has 3, core. Point 2: {1, 1.5, 2} has 3, core. Point 5: only itself, noise. Point 9: only itself, noise. The three core points are mutually reachable and form one cluster; 5 and 9 are noise. There are no border points in this data.

**Q7 (5 marks). Advantages and drawbacks of DBSCAN.**

It finds clusters of arbitrary shape because a cluster grows wherever density continues, flags outliers as noise and needs no $k$. Drawbacks: it is sensitive to $\varepsilon$ and minPts (in the moons example $\varepsilon=0.08$ gave 22 fragments and $\varepsilon=0.5$ merged everything); it cannot handle clusters of very different densities; and its distances lose meaning in high dimensions.

**Q8 (5 marks). LDA direction for means (1,1) and (3,3) with $S_W=I$.**

$\mathbf w\propto S_W^{-1}(\mathbf m_1-\mathbf m_0)=(2,2)$; normalised $\mathbf w=(1,1)/\sqrt2=(0.707,0.707)$. The projected means are $1.414$ and $4.243$, and the threshold is their midpoint $2.83$. The direction is along the line joining the means because the within-class scatter is spherical.

**Q9 (10 marks). The EM algorithm for a Gaussian mixture.**

*Introduction.* Data from several subpopulations with unknown membership are modelled as a mixture $p(x)=\sum_k\pi_k\mathcal N(x\mid\mu_k,\sigma_k)$.

*Algorithm.* Initialise $\pi,\mu,\sigma$. E-step: compute the responsibility $r_{ik}$ of each component for each point. M-step: set $N_k=\sum_i r_{ik}$, $\pi_k=N_k/N$, $\mu_k=\sum_i r_{ik}x_i/N_k$ and $\sigma_k^2=\sum_i r_{ik}(x_i-\mu_k)^2/N_k$. Repeat until the log-likelihood changes by less than a tolerance.

*Properties.* The likelihood never decreases, so EM converges, but to a local maximum that depends on the start; run several starts. In our experiment the log-likelihood went from $-1056$ to $-638.64$ and the parameters reached weights 0.386/0.614 and means $-0.095$/3.974 against the true 0.4/0.6 and 0/4. K-means is EM with hard assignments and equal spherical clusters; a GMM gives soft memberships and elliptical clusters, so use it when clusters overlap and membership probabilities are useful.
