---
subject: Geographical Information System
grade: BCA Semester 8 (Elective III)
unit: 4
title: Spatial Data Modeling and Analysis
hours: 12
area: BCA 453 · Geographical Information System · Unit 4
---

Collecting and storing data is only the beginning. The reason to own a GIS is to **ask spatial questions** and get answers that a table or a picture alone cannot give. This unit first sets out how spatial data are modelled so that relationships can be computed (**spatial data modelling**), then covers the two families of analysis: **vector-based** (selection, measurement, buffer, overlay, proximity, network) and **raster-based** (map algebra, reclassification, distance, cost, suitability). Each operation is explained, shown on a small example and then programmed so that you can see exactly what the software does.

::: key What this unit gives you
- Spatial relationships (topological, directional, metric), the OGC predicates, the nine-intersection idea, and basic geometry: point-in-polygon, area, length, centroid.
- Vector analysis: attribute and spatial queries, measurement, buffers (with the effect of the CRS), clip, intersect, union, erase, spatial join, nearest-neighbour and Thiessen polygons, and network analysis with Dijkstra's algorithm.
- Raster analysis: local, focal, zonal and global operations, reclassification, distance and cost-distance surfaces, and weighted-overlay suitability modelling.
- A complete worked site-selection problem in both models.
:::

## 4.1 Spatial data modelling

### 4.1.1 What is spatial data modelling?

In Unit 3 you chose the *storage* structure. **Spatial data modelling** here means describing how features **relate to each other in space** so that a computer can reason about them. Without a model of relationships, a GIS is an electronic drawing board. With one, it can answer "which wards touch the river?", "is this well inside the protected forest?", and "what is the nearest hospital by road?".

### 4.1.2 Spatial relationships

| Kind | Describes | Examples | How computed |
|---|---|---|---|
| **Topological** | Connection and contact, unchanged by stretching | adjacent, touches, contained in, overlaps, crosses, disjoint | Geometry predicates, or stored topology |
| **Directional (orientation)** | Direction between features | north of, upstream of, uphill from | Bearings, aspect, flow direction |
| **Metric (distance)** | How far | within 500 m, nearest | Distances in a projected CRS |

The **OGC simple-features predicates** are standard tests that return true or false for two geometries A and B:

| Predicate | True when |
|---|---|
| `Equals` | Same geometry |
| `Disjoint` | Share no point |
| `Intersects` | Share at least one point (opposite of disjoint) |
| `Touches` | Meet only at boundaries; interiors do not overlap |
| `Crosses` | Interiors meet and the intersection has lower dimension (a road crosses a river) |
| `Within` | A lies entirely in B (a well within a ward) |
| `Contains` | B lies entirely in A (the converse) |
| `Overlaps` | Same dimension, interiors partly overlap, neither contains the other |

All of them come from the **dimensionally extended nine-intersection model (DE-9IM)**. Each geometry has an **interior**, a **boundary** and an **exterior**. Intersecting these three parts of A with those of B gives a 3 by 3 matrix of nine cells; each cell records the dimension of the intersection (empty, a point, a line, an area). The pattern of the matrix identifies the predicate: for `Within`, the pattern is "T*F**F***" (the interiors intersect, and no part of A touches the exterior of B). You rarely write DE-9IM by hand; you should know that the predicates are defined that way and that a spatial database lets you test custom patterns with `ST_Relate`.

```svgfig label="4.1" caption="Spatial predicates between a polygon A and other geometries. Touches and Overlaps look similar but differ in whether the interiors share area."
f = Fig(680, 250)
def panel(x, title, y=18):
    f.text(x + 55, y, title, size=10.5, color=NAVY, bold=True)
# disjoint
panel(10, "Disjoint")
f.box(15, 40, 55, 55, "A", fill=BLUE, stroke=NAVY, size=10)
f.box(85, 40, 30, 55, "B", fill=SAND, stroke=AMBER, size=10)
# touches
panel(180, "Touches")
f.box(185, 40, 55, 55, "A", fill=BLUE, stroke=NAVY, size=10)
f.box(240, 40, 40, 55, "B", fill=SAND, stroke=AMBER, size=10)
# overlaps
panel(350, "Overlaps")
f.box(355, 40, 60, 55, "A", fill=BLUE, stroke=NAVY, size=10)
f.box(395, 62, 60, 50, "B", fill=SAND, stroke=AMBER, size=10)
# within
panel(520, "Within")
f.box(525, 35, 120, 85, "B", fill=SAND, stroke=AMBER, size=10)
f.box(555, 70, 40, 35, "A", fill=BLUE, stroke=NAVY, size=10)
# crosses
panel(10, "Crosses (line, polygon)", 135)
f.box(15, 150, 100, 70, "", fill=BLUE, stroke=NAVY, size=10)
f.line(0, 215, 130, 150, color=RED, sw=3)
f.text(100, 238, "road crosses polygon A", size=9, color=RED)
# contains/point in polygon
panel(180, "Point in polygon", 135)
f.box(185, 150, 100, 70, "A", fill=BLUE, stroke=NAVY, size=10)
f.circle(235, 195, 5, fill=RED, stroke=RED)
f.circle(310, 185, 5, fill="#ffffff", stroke=RED)
f.text(310, 208, "outside", size=9, color=RED)
# line meets line
panel(350, "Connected lines", 135)
f.line(360, 220, 420, 170, color=AMBER, sw=3)
f.line(420, 170, 470, 215, color=AMBER, sw=3)
f.line(420, 170, 440, 150, color=AMBER, sw=3)
f.circle(420, 170, 5, fill=NAVY, stroke=NAVY)
f.text(450, 168, "node", size=9, color=NAVY)
f.text(585, 168, "Predicates return true or false;", size=9.5, color=SLATE)
f.text(585, 186, "analysis tools use them to select.", size=9.5, color=SLATE)
```

### 4.1.3 Geometry computations the model relies on

Everything above rests on a few algorithms:

- **Distance** between two points (Pythagoras in a projected CRS, haversine on a sphere), and point-to-segment distance for lines.
- **Point-in-polygon**: the **ray-casting** method draws a horizontal ray from the point and counts how many polygon edges it crosses. An **odd** count means inside, **even** means outside.
- **Area** by the **shoelace formula**, A = 1/2 |sum(x_i y_(i+1) - x_(i+1) y_i)|, and the **centroid** from the same terms (Unit 3).
- **Line length** as the sum of segment lengths; **bearing** with atan2.
- **Bounding boxes** (minimum rectangles) to reject most pairs quickly before the exact test.

```python
# Point-in-polygon by ray casting, point-to-segment distance, and a within-distance selection.
import math
ward = [(0, 0), (6, 0), (7, 4), (3, 6), (-1, 4)]            # a convex-ish ward polygon, km grid

def in_polygon(pt, poly):
    x, y = pt; inside = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y):                              # edge straddles the ray's height
            xcross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xcross: inside = not inside               # crossing to the right of the point
    return inside

def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

wells = {"W1": (3, 3), "W2": (8, 1), "W3": (0.5, 0.2), "W4": (-2, 5), "W5": (6.5, 3.5)}
print("wells inside the ward:", [k for k, p in wells.items() if in_polygon(p, ward)])
road = [(-3, 2), (4, 2.5), (9, 5)]
print("distance from each well to the road:")
for k, p in wells.items():
    d = min(seg_dist(p, road[i], road[i + 1]) for i in range(len(road) - 1))
    print("  %s %.2f km %s" % (k, d, "(within 1 km)" if d <= 1 else ""))
```
```output
wells inside the ward: ['W1', 'W3', 'W5']
distance from each well to the road:
  W1 0.57 km (within 1 km)
  W2 3.13 km 
  W3 2.04 km 
  W4 2.92 km 
  W5 0.22 km (within 1 km)
```
### 4.1.4 The network model

Roads, rivers, pipes and power lines are better modelled as a **network**: a graph of **edges** (line segments) joined at **junctions** (nodes). Each edge carries **impedance** (length, travel time or cost), a speed or capacity, and possibly a **direction** (one-way) and **turn restrictions**. Nodes may have barriers. Because the structure is a graph, classical algorithms apply: shortest path (Dijkstra, A*), travelling salesman and vehicle-routing heuristics, minimum spanning tree and maximum flow. A network dataset must be **connected** (no undershoots at junctions) and have **elevation rules** at bridges and tunnels (lines that cross without connecting).

### 4.1.5 Modelling continuous space

Rasters model spatial relationships implicitly through the **neighbourhood**: each cell has four (rook) or eight (queen) neighbours. Operations such as slope, focal mean and flow direction exploit this regular adjacency (Section 4.3 and Unit 5). Vector and raster modelling can be combined: points are interpolated to a raster surface, polygons are rasterised for map algebra, and results are vectorised back into zones for reporting.
## 4.2 Vector-based analysis

### 4.2.1 Queries and selection

**Attribute query** selects features by their table values, using SQL-style expressions: `population > 20000 AND district = 'Kaski'`. **Spatial query** (select by location) selects features by a spatial relationship to other features: *schools within the flood zone*, *wells that intersect the buffer of the road*, *wards that touch Ward 3*. The two combine: *flood-zone schools with more than 300 students*. The selected set can be saved as a new layer, counted or summarised (total students at risk), or used as the input of the next tool. Identify ("what is here?") and **query by pointing** are the interactive form.

Other basic vector measurements: **length** of lines, **perimeter and area** of polygons (computed in a projected CRS, in the right units), **centroid**, and **distance** between features. A **spatial join** copies attributes from one layer to another by location (attach the ward name to each school point from the ward polygon it lies in) and may summarise (count schools per ward).

### 4.2.2 Buffer

A **buffer** is the zone within a given distance of a feature: a **circle** around a point, a **stadium-shaped** strip around a line, a rounded outline around a polygon. It answers "what lies within d of this?" and is the basis of setback rules (building not within 30 m of a river), service catchments (homes within 500 m of a bus stop), and protection zones. Options: **fixed** or **variable** distance (from an attribute, such as a wider setback for bigger rivers), **dissolve** overlapping buffers into one polygon (so that shared areas are not counted twice), and **round or flat ends**.

The area of a buffer of radius r around a straight line of length L is 2rL + pi r^2 (a rectangle plus two half-circles). Two cautions: buffer distances are in the **units of the CRS**, so **never buffer in degrees**; and overlapping buffers double-count unless dissolved.

```python
# Buffer area: formula against a grid count, overlapping buffers (dissolve), and the degree trap.
import math
def dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def buffer_area(lines, r, step=0.01, dissolve=True):
    """Area (km2) of the buffer(s) by counting grid cells; dissolve=False sums each buffer separately."""
    xs = [p[0] for l in lines for p in l]; ys = [p[1] for l in lines for p in l]
    x0, x1, y0, y1 = min(xs) - r, max(xs) + r, min(ys) - r, max(ys) + r
    total_each = [0] * len(lines); union = 0
    nx, ny = int((x1 - x0) / step), int((y1 - y0) / step)
    for i in range(nx):
        for j in range(ny):
            px, py = x0 + (i + .5) * step, y0 + (j + .5) * step
            hit = [min(dist_seg(px, py, *l[k], *l[k + 1]) for k in range(len(l) - 1)) <= r for l in lines]
            for n, h in enumerate(hit): total_each[n] += h
            union += any(hit)
    return (union if dissolve else sum(total_each)) * step * step

road = [[(0, 0), (4, 0)]]
r = 0.5
print("single road L=4 km, r=0.5 km: grid %.3f km2, formula %.3f km2" % (buffer_area(road, r), 2 * r * 4 + math.pi * r * r))
two = [[(0, 0), (4, 0)], [(0, 0.6), (4, 0.6)]]               # two parallel roads 0.6 km apart
print("two parallel roads: separate sum %.2f km2, dissolved %.2f km2 (overlap counted once)" % (buffer_area(two, r, dissolve=False), buffer_area(two, r)))
# the degree trap: a "0.005 degree" buffer around Kathmandu is an ellipse, about 0.55 km north-south and 0.49 km east-west
lat = 27.7
print("0.005 degree buffer at %.1f N: %.0f m north-south but %.0f m east-west" % (lat, 0.005 * 111320, 0.005 * 111320 * math.cos(math.radians(lat))))
```
```output
single road L=4 km, r=0.5 km: grid 4.786 km2, formula 4.785 km2
two parallel roads: separate sum 9.57 km2, dissolved 7.75 km2 (overlap counted once)
0.005 degree buffer at 27.7 N: 557 m north-south but 493 m east-west
```
### 4.2.3 Overlay

**Overlay** combines two layers to produce a new one whose features carry geometry and attributes from both. It is the signature GIS operation.

| Operation | Output | Use |
|---|---|---|
| **Clip** | Part of the input inside a clip polygon, input attributes only | Cut a national layer to one district |
| **Intersect** | Only the common area, attributes of both | Land that is both agricultural and flood-prone |
| **Union** | All areas of both layers, split along boundaries, with attributes of both | Combine land-use and ownership into one layer |
| **Erase (difference)** | Input minus the area of the erase layer | Land outside protected zones |
| **Identity / symmetric difference** | Variants keeping part of one or both | Specialised updates |
| **Dissolve** | Merge adjacent polygons with equal attribute values | Wards to districts |
| **Merge / append** | Stack layers of the same kind | Combine municipal data sets |

```svgfig label="4.2" caption="Overlay operations on two polygons A (flood zone, blue) and B (farmland, amber). The shaded green region in each panel is the output."
f = Fig(680, 210)
titles = ("Intersect", "Union", "Erase (A minus B)", "Clip A by B")
for k, t in enumerate(titles):
    x = 20 + k * 165
    f.text(x + 62, 18, t, size=10.5, color=NAVY, bold=True)
    if t == "Intersect":
        f.box(x, 35, 90, 80, "", fill=SOFT, stroke=NAVY); f.box(x + 45, 60, 90, 80, "", fill=SOFT, stroke=AMBER)
        f.box(x + 45, 60, 45, 55, "", fill="#bbf7d0", stroke=TEAL)
    elif t == "Union":
        f.box(x, 35, 90, 80, "", fill="#bbf7d0", stroke=NAVY); f.box(x + 45, 60, 90, 80, "", fill="#bbf7d0", stroke=AMBER)
        f.box(x + 45, 60, 45, 55, "", fill="#bbf7d0", stroke="#bbf7d0")
    elif t == "Erase (A minus B)":
        f.box(x, 35, 90, 80, "", fill="#bbf7d0", stroke=NAVY); f.box(x + 45, 60, 90, 80, "", fill=SOFT, stroke=AMBER)
        f.box(x + 45, 60, 45, 55, "", fill=SOFT, stroke=AMBER)
    else:
        f.box(x, 35, 90, 80, "", fill=SOFT, stroke=NAVY); f.box(x + 45, 60, 90, 80, "", fill=SOFT, stroke=AMBER)
        f.box(x + 45, 60, 45, 55, "", fill="#bbf7d0", stroke=TEAL)
    f.text(x + 22, 52, "A", size=10, color=NAVY, bold=True)
    f.text(x + 118, 156, "B", size=10, color=AMBER, bold=True)
f.text(340, 192, "Inputs are the same in every panel; only the rule for the output differs.", size=9.5, color=SLATE)
```

Because overlay creates new polygons, **attributes of the output are not always meaningful**: a union polygon that covers half of the original ward must not keep the ward's whole population. Apportion by area (or better, by a finer variable) when you cut polygons, and be aware of **slivers**: tiny polygons created when two boundaries that should coincide differ by a metre. A **cluster tolerance** snaps close vertices together to avoid them.

```python
# Polygon overlay by hand: Sutherland-Hodgman clipping of a flood zone A by a rectangle, then area bookkeeping.
def clip(poly, rect):
    xmin, ymin, xmax, ymax = rect
    def cut(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            cur, prev = pts[i], pts[i - 1]
            if inside(cur):
                if not inside(prev): out.append(inter(prev, cur))
                out.append(cur)
            elif inside(prev): out.append(inter(prev, cur))
        return out
    def ix(x):  return lambda p, q: (x, p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]))
    def iy(y):  return lambda p, q: (p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1]), y)
    for inside, inter in ((lambda p: p[0] >= xmin, ix(xmin)), (lambda p: p[0] <= xmax, ix(xmax)),
                          (lambda p: p[1] >= ymin, iy(ymin)), (lambda p: p[1] <= ymax, iy(ymax))):
        poly = cut(poly, inside, inter)
        if not poly: return []
    return poly

def area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2

A = [(0, 0), (8, 0), (10, 5), (4, 9), (-1, 6)]               # flood zone (km)
B = (3, 2, 12, 8)                                            # farmland rectangle xmin ymin xmax ymax
inter = clip(A, B)
aA, aB, aI = area(A), (B[2] - B[0]) * (B[3] - B[1]), area(inter)
print("area A %.2f, area B %.2f, intersection %.2f km2" % (aA, aB, aI))
print("union %.2f km2 (A + B - intersection), erase A minus B %.2f km2" % (aA + aB - aI, aA - aI))
print("share of the flood zone that is farmland: %.0f %%" % (100 * aI / aA))
farm_value = 120000                                          # NPR per hectare per year, illustrative
print("annual crop value at risk: NPR %.1f million" % (aI * 100 * farm_value / 1e6))
```
```output
area A 71.50, area B 54.00, intersection 33.45 km2
union 92.05 km2 (A + B - intersection), erase A minus B 38.05 km2
share of the flood zone that is farmland: 47 %
annual crop value at risk: NPR 401.4 million
```
### 4.2.4 Proximity analysis

- **Nearest neighbour / near**: for each feature, find the closest feature in another layer and its distance (nearest health post to each ward centroid).
- **Thiessen (Voronoi) polygons** divide space so that every location belongs to the **nearest** of a set of points; they approximate the catchment of each school or rain gauge. Their boundaries are the perpendicular bisectors of neighbouring points. They are dual to the Delaunay triangulation of Unit 3.
- **Multiple-ring buffers** give zones at 250, 500 and 1,000 m.
- **Location-allocation** chooses sites for facilities to minimise total distance and assigns demand to them.

```python
# Thiessen allocation on a grid: each cell goes to the nearest school; population and walking distance by catchment.
import math
schools = {"Janata": (2, 2), "Saraswati": (8, 3), "Adarsha": (5, 8)}
homes = [(1, 1), (2, 4), (3, 3), (6, 2), (9, 4), (7, 6), (5, 7), (4, 9), (6, 9), (8, 1)]    # one household each
catch = {k: [] for k in schools}
for h in homes:
    d = {k: math.dist(h, p) for k, p in schools.items()}
    k = min(d, key=d.get); catch[k].append(d[k])
for k, v in catch.items():
    print("%-10s serves %d households, mean distance %.2f km, max %.2f km" % (k, len(v), sum(v) / len(v), max(v)))
too_far = sum(1 for v in catch.values() for d in v if d > 2.0)
print("households farther than 2 km from their nearest school:", too_far)
```
```output
Janata     serves 3 households, mean distance 1.61 km, max 2.00 km
Saraswati  serves 3 households, mean distance 1.88 km, max 2.24 km
Adarsha    serves 4 households, mean distance 1.66 km, max 2.83 km
households farther than 2 km from their nearest school: 2
```
### 4.2.5 Network analysis

Typical network analyses are **shortest or fastest path** between two places, **closest facility** (the nearest ambulance or fire station by travel time), **service area** (everything reachable within 10 minutes), **origin-destination cost matrix**, **vehicle routing** (several stops, time windows) and **location-allocation**. The core is **Dijkstra's algorithm**: starting from the origin, repeatedly settle the unsettled node with the smallest known cost and relax its edges. It is correct when all costs are non-negative; with a priority queue it runs in O((V + E) log V). **A\*** speeds it up with a straight-line heuristic. Networks use **travel time**, not distance, as impedance in practice, because a long highway beats a short mountain trail.

```python
# Dijkstra on a small town network (minutes): shortest path, closest facility, service area and a road closure.
import heapq
roads = {("A", "B"): 6, ("A", "C"): 4, ("B", "D"): 5, ("C", "D"): 9, ("C", "E"): 7, ("D", "F"): 6, ("E", "F"): 4, ("B", "G"): 8, ("F", "G"): 5}
def graph(closed=()):
    g = {}
    for (u, v), w in roads.items():
        if (u, v) in closed: continue
        g.setdefault(u, {})[v] = w; g.setdefault(v, {})[u] = w
    return g

def dijkstra(g, src):
    dist, prev, pq = {src: 0}, {}, [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, 1e9): continue
        for v, w in g[u].items():
            if d + w < dist.get(v, 1e9):
                dist[v], prev[v] = d + w, u; heapq.heappush(pq, (d + w, v))
    return dist, prev

def path(prev, t):
    p = [t]
    while p[-1] in prev: p.append(prev[p[-1]])
    return "-".join(reversed(p))

g = graph(); dist, prev = dijkstra(g, "A")
print("A to G: %d min via %s" % (dist["G"], path(prev, "G")))
hospitals = ["F", "G"]
best = min(hospitals, key=lambda h: dist[h])
print("closest hospital to A: %s, %d min" % (best, dist[best]))
print("service area of A within 10 min:", sorted(n for n, d in dist.items() if d <= 10))
dist2, prev2 = dijkstra(graph(closed=[("B", "G")]), "A")
print("after closing B-G: A to G takes %d min via %s" % (dist2["G"], path(prev2, "G")))
```
```output
A to G: 14 min via A-B-G
closest hospital to A: G, 14 min
service area of A within 10 min: ['A', 'B', 'C']
after closing B-G: A to G takes 20 min via A-C-E-F-G
```
## 4.3 Raster-based analysis

### 4.3.1 Map algebra

**Map algebra** (Dana Tomlin) treats each raster layer as a variable and performs arithmetic and logic on whole layers, cell by cell, as in `suitability = 0.5 * slope_score + 0.3 * road_score + 0.2 * soil_score`. Operations fall into four classes:

| Class | Output cell depends on | Examples |
|---|---|---|
| **Local** | The same cell in one or more layers | Add layers, reclassify, `if slope > 30 then 0`, NDVI |
| **Focal (neighbourhood)** | The cell and its neighbours (a 3 x 3 window, a circle) | Smoothing, slope, aspect, edge detection, majority filter, density |
| **Zonal** | All cells of a zone defined by another layer | Mean elevation per ward, area of each land-cover class per district |
| **Global** | The whole raster, often with distance | Euclidean distance, cost distance, flow accumulation, viewshed |

All input layers must share the same **extent, cell size and CRS**; otherwise resample and align first. Cells with **NoData** in any input normally become NoData in the output. Rasters are the natural tool for continuous problems and for combining many layers quickly, while their **cell size** sets the limit of precision.

```python
# Map algebra on 6x6 rasters: reclassify (local), 3x3 mean (focal) and zonal statistics.
import numpy as np
elev = np.array([[1210, 1230, 1260, 1300, 1350, 1410],
                 [1200, 1215, 1245, 1290, 1340, 1395],
                 [1190, 1200, 1230, 1270, 1320, 1370],
                 [1185, 1195, 1215, 1250, 1300, 1345],
                 [1180, 1190, 1205, 1230, 1275, 1320],
                 [1175, 1182, 1195, 1215, 1250, 1300]], dtype=float)
# local: reclassify elevation into 3 classes with np.digitize
cls = np.digitize(elev, [1250, 1320]) + 1                  # 1 low (<1250), 2 mid, 3 high (>=1320)
print("reclassified (1 low, 2 mid, 3 high):"); print(cls)
# focal: 3x3 mean with edge cells using the available neighbours
pad = np.pad(elev, 1, mode="edge")
mean3 = sum(pad[i:i + 6, j:j + 6] for i in range(3) for j in range(3)) / 9
print("focal mean at (2,2): %.1f  (raw cell %.0f)" % (mean3[2, 2], elev[2, 2]))
# zonal: two wards, left half = 1, right half = 2
zone = np.array([[1, 1, 1, 2, 2, 2]] * 6)
for z in (1, 2):
    m = zone == z
    print("ward %d: mean %.1f m, max %.0f m, area %d cells" % (z, elev[m].mean(), elev[m].max(), m.sum()))
```
```output
reclassified (1 low, 2 mid, 3 high):
[[1 1 2 2 3 3]
 [1 1 1 2 3 3]
 [1 1 1 2 3 3]
 [1 1 1 2 2 3]
 [1 1 1 1 2 3]
 [1 1 1 1 2 2]]
focal mean at (2,2): 1234.4  (raw cell 1230)
ward 1: mean 1205.7 m, max 1260 m, area 18 cells
ward 2: mean 1307.2 m, max 1410 m, area 18 cells
```
### 4.3.2 Reclassification

**Reclassification** reassigns cell values to new ones: continuous values to classes (slope in degrees to flat, gentle, steep), many categories to a few (twelve land-cover codes to *agriculture*, *forest*, *built*), or any value to a **suitability score** (1 to 5). It is the way unlike measurements are put on a **common scale** before they are combined, so that "10 degrees" and "300 m from a road" can both be scored on 1 to 5. Document the breaks and the reason for them; results change with the breaks.

### 4.3.3 Distance and cost surfaces

A **Euclidean distance** raster stores, for each cell, the straight-line distance to the nearest source (road, river, school). Buffering is the same idea thresholded (distance below 500 m). **Cost-distance** (or **least-cost path**) accounts for a **friction surface**: how hard it is to cross each cell (slope, land cover, rivers, barriers). The cost of moving to a neighbour is the average friction times the step length (1 for rook moves, about 1.414 for diagonals). Dijkstra's algorithm runs over the grid; the **accumulated cost** raster then lets you trace the cheapest route back from a destination. Applications: road and canal alignments, footpath planning, wildlife corridors, evacuation routes.

```python
# Euclidean distance and least-cost path across a friction surface.
import heapq, numpy as np
from scipy.ndimage import distance_transform_edt
road = np.zeros((8, 8), dtype=bool); road[:, 0] = True            # a road along the west edge
dist_cells = distance_transform_edt(~road)                       # distance to nearest road cell, in cells
print("distance to road (cells), row 3:", np.round(dist_cells[3], 1))
print("with 30 m cells the far east edge is %.0f m from the road" % (dist_cells[3, 7] * 30))

# friction: 1 = open ground, 5 = steep, 50 = river (nearly a barrier)
fr = np.ones((8, 8)); fr[2:6, 3] = 50; fr[0:3, 4:6] = 5; fr[5, 3] = 1            # river at column 3 with a ford at row 5
def least_cost(fr, start, goal):
    n, m = fr.shape; cost = np.full((n, m), np.inf); cost[start] = 0; prev = {}
    pq = [(0.0, start)]
    while pq:
        c, (r, q) = heapq.heappop(pq)
        if c > cost[r, q]: continue
        for dr in (-1, 0, 1):
            for dq in (-1, 0, 1):
                if (dr or dq) and 0 <= r + dr < n and 0 <= q + dq < m:
                    step = (2 ** .5 if dr and dq else 1.0) * (fr[r, q] + fr[r + dr, q + dq]) / 2
                    if c + step < cost[r + dr, q + dq]:
                        cost[r + dr, q + dq] = c + step; prev[(r + dr, q + dq)] = (r, q); heapq.heappush(pq, (c + step, (r + dr, q + dq)))
    p = [goal]
    while p[-1] != start: p.append(prev[p[-1]])
    return cost[goal], p[::-1]
c, p = least_cost(fr, (1, 0), (1, 7))
print("least-cost route from (1,0) to (1,7): cost %.1f over %d cells" % (c, len(p)))
print("route:", p)
print("a straight line along row 1 would cost %.1f" % fr[1].sum())
```
```output
distance to road (cells), row 3: [0. 1. 2. 3. 4. 5. 6. 7.]
with 30 m cells the far east edge is 210 m from the road
least-cost route from (1,0) to (1,7): cost 10.9 over 9 cells
route: [(1, 0), (2, 0), (3, 1), (4, 2), (5, 3), (4, 4), (3, 5), (2, 6), (1, 7)]
a straight line along row 1 would cost 16.0
```
The path swings south to the **ford** at row 5, accepting a longer distance to avoid the expensive river cells. A least-cost path always depends on the friction surface; a different weighting of slope and land cover gives a different road.

### 4.3.4 Weighted-overlay suitability analysis

The standard use of raster analysis is **multi-criteria suitability modelling**: where is the best place for a school, a landfill, a hospital, a hotel? The method:

1. **Define the goal and the criteria** (slope, distance to road, distance to river, land cover, distance from existing schools).
2. **Separate constraints from factors.** A *constraint* excludes areas absolutely (flood zones, protected forest): score 0 or NoData. A *factor* ranks the rest.
3. **Reclassify each factor** to a common scale such as 1 (poor) to 5 (best).
4. **Weight the factors** to reflect importance; weights sum to 1 (or 100 %). They can be assigned by judgement or derived from pairwise comparison (AHP).
5. **Combine**: score = sum of weight x factor score, then multiply by the constraint mask.
6. **Classify and check**: map the results, test sensitivity (change the weights by 10 percent and see if the winners change), and verify with fieldwork.

```python
# Site selection for a new school: weighted overlay of three factors with a flood-zone constraint.
import numpy as np
n = 10
r, c = np.indices((n, n))
slope_deg = 4 + 1.8 * np.abs(c - 3) + 0.8 * r                     # synthetic terrain: flat band near column 3
d_road_km = 0.1 * np.abs(r - 4) + 0.05 * c                         # a road along row 4
flood = (c >= 7) & (r >= 5)                                        # constraint: low flood-prone corner
def score(x, breaks):                                              # lower value = better, 5 .. 1
    return 5 - np.digitize(x, breaks)
s_slope = score(slope_deg, [6, 9, 12, 16])                         # <6 deg best
s_road = score(d_road_km, [0.2, 0.4, 0.6, 0.8])                    # <200 m best
s_pop = np.clip(5 - np.abs(r - 3) // 2 - np.abs(c - 4) // 2, 1, 5) # nearer the (3, 4) village centre is better
w = {"slope": 0.40, "road": 0.35, "village": 0.25}
suit = (w["slope"] * s_slope + w["road"] * s_road + w["village"] * s_pop) * (~flood)
print("suitability score x10 (0 = constraint):")
for row in np.round(suit * 10).astype(int): print(" ".join("%3d" % v for v in row))
best = np.unravel_index(suit.argmax(), suit.shape)
print("best cell (row, col) =", tuple(int(v) for v in best), "score %.2f of 5" % suit.max())
print("cells scoring >= 4.0:", int((suit >= 4.0).sum()), "of", n * n)
# sensitivity: change weights to 0.30/0.35/0.35 and see whether the best cell moves
suit2 = (0.30 * s_slope + 0.35 * s_road + 0.35 * s_pop) * (~flood)
print("best cell with road/village weights shifted:", tuple(int(v) for v in np.unravel_index(suit2.argmax(), suit2.shape)))
```
```output
suitability score x10 (0 = constraint):
 28  34  38  40  37  33  27  27  16  16
 31  38  34  40  36  36  27  22  20  20
 34  36  40  46  39  35  32  28  22  18
 37  40  40  42  42  38  32  28  26  22
 33  40  40  46  38  38  32  32  22  22
 30  37  34  40  36  36  26   0   0   0
 27  30  34  40  32  28  26   0   0   0
 24  27  28  30  30  26  20   0   0   0
 21  23  23  30  22  22  20   0   0   0
 17  21  18  24  20  20  10   0   0   0
best cell (row, col) = (2, 3) score 4.65 of 5
cells scoring >= 4.0: 10 of 100
best cell with road/village weights shifted: (4, 3)
```
::: caution Garbage in, weights out
A suitability map looks scientific because it is a smooth, coloured surface, but every number in it came from a decision: the classes, the scores, the weights. Publish them, run a sensitivity test, and treat the output as decision *support*. A map cannot decide a school's site without field checks, land availability and community consultation.
:::

### 4.3.5 Choosing vector or raster for an analysis

| Question | Better in | Why |
|---|---|---|
| Parcels, ownership, legal boundaries | Vector | Exact boundaries and attributes |
| Shortest road route | Vector network | Graph algorithms |
| Which houses are within 200 m of a river | Vector buffer and select | Few features, exact counting |
| Best site given slope, distance, land cover | Raster | Many continuous layers combined cell by cell |
| Spread or flow over terrain | Raster | Neighbourhood operations |
| Report by ward | Raster then zonal statistics | Combine strengths |

## 4.4 A complete worked problem

*Problem: a municipality will build one health post. It must be outside the flood zone, within 500 m of a road, and as close as possible to the largest number of unserved households.*

1. **Vector selection**: from the household points (attribute `served = no`), select the unserved ones; select roads and buffer them by 500 m, **dissolved**; **erase** the flood polygon from the road buffer. The result is the *allowed area*.
2. **Raster step**: rasterise the unserved households as a **density** surface (focal count in a 1 km circle), mask it by the allowed area.
3. **Select**: the cell with the highest density in the allowed area is the first candidate; the **top five cells** go to the field team.
4. **Network check**: compute the **service area** of the candidate along the road network within 15 minutes to show how many households will actually be served.
5. **Report**: an overlay of the candidate sites on the households, with the metadata and the assumptions (buffer 500 m, 1 km density radius, 15 minute cut-off).

Every step in this chain was met earlier in the unit: select, buffer, dissolve, erase, density, mask, service area. A real project uses the same logic with the real layers.

## 4.5 Summary and exercises

Spatial modelling describes relationships (topological, directional, metric) through predicates defined by DE-9IM, geometry algorithms (ray casting, shoelace) and the network model. Vector analysis includes attribute and spatial selection, measurement, buffer, overlay (clip, intersect, union, erase, dissolve), proximity (nearest, Thiessen) and network analysis (Dijkstra). Raster analysis uses map algebra (local, focal, zonal, global), reclassification, distance and cost surfaces, and weighted-overlay suitability with constraints and sensitivity testing. Vector suits discrete features and networks, raster suits continuous problems and many-layer combinations.

1. Distinguish topological, directional and metric spatial relationships with two examples each.
2. Define the predicates touches, overlaps, within and crosses. What is DE-9IM?
3. Explain the ray-casting method for point in polygon. A point's ray crosses five edges: inside or outside?
4. A polygon has vertices (0,0), (6,0), (6,4), (0,4). Compute its area with the shoelace formula.
5. Distinguish attribute query, spatial query and spatial join with one example each.
6. What is a buffer? Compute the area of a 600 m buffer around a straight 5 km canal.
7. Why must buffers not be created in degrees? Explain with the 27.7 N example.
8. Explain clip, intersect, union and erase. Which operation is symmetric?
9. What are slivers? How are they prevented? Why must attributes be apportioned after cutting polygons?
10. A flood zone is 28.4 km2, of which 7.1 km2 is farmland. What fraction is farmland, and what crop value is at risk at NPR 120,000 per hectare?
11. What are Thiessen polygons? State two applications.
12. State the principle of Dijkstra's algorithm and why costs must be non-negative. Use the network of Section 4.2.5 to find the shortest path A to F.
13. Differentiate local, focal, zonal and global map-algebra operations with one example each.
14. What is cost-distance? How does a friction surface change a route?
15. Describe the steps of a suitability analysis. Distinguish constraints from factors, and say why a sensitivity test is done.
16. For the school-site problem, weights 0.4, 0.35, 0.25 and scores (5, 4, 3) in a cell: compute the suitability.

**Answers to the numerical items.** (3) An odd number of crossings means **inside**. (4) Sum = (0x0 - 6x0) + (6x4 - 6x0) + (6x4 - 0x4) + (0x0 - 0x4) = 0 + 24 + 24 + 0 = 48; area = **24 square units**. (6) A = 2rL + pi r^2 = 2 x 0.6 x 5 + 3.1416 x 0.36 = 6 + 1.131 = **7.13 km2**. (10) 7.1 / 28.4 = **25 %**; 7.1 km2 = 710 ha; value = 710 x 120,000 = **NPR 85.2 million**. (12) A-C-E-F = 4 + 7 + 4 = **15 min**, against A-B-D-F = 6 + 5 + 6 = 17 min. (16) 0.40 x 5 + 0.35 x 4 + 0.25 x 3 = 2.00 + 1.40 + 0.75 = **4.15**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain buffer and overlay analysis with examples.**

A buffer creates a zone within a specified distance of a point, line or polygon; for example, a 30 m setback around rivers. Distances are in CRS units, so a projected CRS must be used, and overlapping buffers should be dissolved so that area is not double counted. Overlay combines two layers into a new one carrying the geometry and attributes of both: intersect keeps the common area, union keeps everything split along boundaries, erase removes the area of one layer from another and clip cuts a layer by a boundary. Buffering the rivers and then intersecting with the settlement layer, for example, gives the houses inside the setback. Output attributes must be apportioned for split polygons and slivers should be cleaned.

**Q2 (5 marks). What is map algebra? Name its four classes.**

Map algebra performs mathematical and logical operations on raster layers as variables, cell by cell. Local operations compute each output cell from the same cell of the inputs (sum, reclassify, NDVI). Focal operations use a neighbourhood of the cell (3 by 3 mean, slope). Zonal operations summarise the cells of a zone defined by another layer (mean elevation per ward). Global operations depend on the whole raster (Euclidean distance, cost distance, flow accumulation). Inputs must have the same extent, cell size and CRS.

**Q3 (10 marks). Describe how GIS is used to select a site for a school.**

First the goal is defined and the criteria are listed: gentle slope, close to a road, close to the village, away from flood and landslide hazard, not on farmland of high value. Constraints (flood zone, protected forest, steep slope above a limit) are rasterised as 0 and exclude areas absolutely. Each factor is converted to a raster, for example slope from the DEM, distance to the road with Euclidean distance, and distance to the village centre; each is reclassified to a common 1 to 5 scale, with the breaks documented. Weights reflecting importance, for instance slope 0.4, road 0.35 and village 0.25, are chosen by experts or pairwise comparison and sum to one. Weighted overlay computes the sum of weight times score and multiplies by the constraint mask, giving a suitability surface. The surface is classified and the highest-scoring contiguous areas become candidate sites; ownership and area are checked by overlaying the parcel layer, and a network analysis shows the number of children within a 30 minute walk. A sensitivity test with changed weights shows how stable the winners are. The final recommendation is verified in the field and by public consultation, because the model reflects the data and the value judgements built into it.
