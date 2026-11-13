---
subject: Geographical Information System
grade: BCA Semester 8 (Elective III)
unit: 3
title: GIS Data Sources and Structures
hours: 12
area: BCA 453 · Geographical Information System · Unit 3
---

A GIS is only as good as its data. This unit follows the data from the field to the database: how they are **captured**, the four main **sources** (maps, GPS, images and databases), the three computer **structures** used to hold them (vector, raster and TIN), how a real-world area is turned into a **data model**, and how a **GIS database** is designed. Every idea is backed by a short program: georeferencing a scanned map, solving a GPS position, computing a vegetation index, joining tables in SQL, parsing geometry, compressing a raster and indexing space.

::: key What this unit gives you
- Methods of capturing GIS data and the checks needed after capture.
- Sources: scanned maps and georeferencing (affine fit and RMSE), GPS and GNSS (position by ranging, DOP, NMEA), images (resolutions, NDVI), and databases (SQL joins, geocoding).
- Structures: vector (points, lines, polygons, topology, file formats), raster (cells, resolution, compression, quadtree) and TIN (Delaunay triangulation), with a comparison.
- Data modelling (conceptual, logical, physical; object against field) and GIS database design including spatial indexing.
:::

## 3.1 Capturing GIS data

**Data capture** is the conversion of observations or existing information into digital, georeferenced form. It is usually the slowest and costliest stage, and mistakes made here propagate to every later analysis. There are two broad routes.

**Primary capture** collects data directly: field survey with GNSS or a total station, remote sensing with satellites, aircraft or drones, laser scanning (LiDAR), and sensors. **Secondary capture** converts existing material: **digitising** paper maps, **scanning** and vectorising, importing files, transcribing tables, and **geocoding** addresses.

| Method | Output | Good for | Typical limit |
|---|---|---|---|
| **Manual (table) digitising** | Vectors traced on a digitising tablet | Small number of maps | Slow, operator error |
| **Heads-up (on-screen) digitising** | Vectors traced on a scanned map or an image | Most common today | Limited by image quality and by scale |
| **Scanning** | Raster image of a map | Archiving, background | A scan is just a picture until georeferenced or vectorised |
| **Automatic vectorisation** | Lines from a scanned map | Clean contour maps | Needs editing, text and symbols confuse it |
| **GNSS survey** | Points, tracks | Field features, boundaries | Needs open sky; accuracy depends on receiver |
| **Remote sensing** | Raster images | Large areas, repeated | Needs processing and classification |
| **Keyboard entry / import** | Attribute tables | Census, registers | Typing errors, inconsistent codes |

**Quality checks after capture** are part of capture, not an extra: *completeness* (is every feature there?), *positional accuracy* (compare with control points), *attribute accuracy* (spot checks against the source), *topological consistency* (no gaps or overlaps between polygons, lines that should meet do meet), *logical consistency* (codes belong to the allowed list) and *currency*. Typical **digitising errors** are **undershoots** (a line stops short of the node), **overshoots** (it passes beyond), **slivers** (thin false polygons where two boundaries were traced twice with slightly different paths), **duplicate** features and **missing labels**.

## 3.2 Sources: maps, GPS, images and databases

### 3.2.1 Maps: scanning and georeferencing

A scanned map is a grid of pixels with row and column numbers and no relation to the Earth. **Georeferencing** attaches real-world coordinates to it by choosing **ground control points (GCPs)**: places identifiable on both the scan and in the real coordinate system (graticule intersections, road crossings, survey pillars). The software fits a **transformation** that maps pixel (c, r) to ground (E, N). The usual choice for a clean scan is the **affine** transformation:

- E = a c + b r + e
- N = d c + f r + g

It has six parameters (scale, rotation and skew in two directions, plus a shift), so three GCPs fix it and **four or more** allow a least-squares fit whose **residuals** reveal blunders. The **RMSE** of the residuals measures fit quality; for a map at 1:25,000 an RMSE of about one pixel (a few metres) is good. Higher-order polynomial or thin-plate-spline transformations are used for warped old maps but can distort between GCPs.

```python
# Georeference a map scan with 6 ground control points: fit an affine transform by least squares.
import numpy as np
# (col, row) pixel -> (Easting, Northing) in metres; GCP 5 carries a deliberate blunder of +25 m in Easting
gcp = np.array([
    [ 120,  150, 330134.6, 3070421.9],
    [2310,  140, 334769.1, 3070444.2],
    [2300, 1980, 334748.9, 3066548.3],
    [ 130, 1990, 330154.7, 3066528.5],
    [1215, 1065, 332476.8, 3068485.2],
    [1200,  150, 332419.3, 3070423.0],
])
def fit(g):
    cols, rows, E, N = g.T
    M = np.column_stack([cols, rows, np.ones(len(cols))])
    cx, *_ = np.linalg.lstsq(M, E, rcond=None)
    cy, *_ = np.linalg.lstsq(M, N, rcond=None)
    res = np.hypot(M @ cx - E, M @ cy - N)
    return cx, cy, res
cx, cy, res = fit(gcp)
print("E = %.4f c + %.4f r + %.1f" % tuple(cx))
print("N = %.4f c + %.4f r + %.1f" % tuple(cy))
for i, r in enumerate(res, 1):
    print("GCP %d residual %5.2f m" % (i, r))
print("RMSE with all six = %.2f m; largest residual is GCP %d" % (np.sqrt((res ** 2).mean()), res.argmax() + 1))
keep = np.delete(gcp, res.argmax(), axis=0)          # re-check the point, find the blunder, drop it, refit
cx, cy, res2 = fit(keep)
print("RMSE after removing it = %.2f m" % np.sqrt((res2 ** 2).mean()))
print("pixel size ~ %.2f m (1:25,000 scanned at 300 dpi gives %.2f m)" % (np.hypot(cx[0], cy[0]), 0.0254 / 300 * 25000))
```
```output
E = 2.1167 c + 0.0011 r + 329883.1
N = -0.0001 c + -2.1168 r + 3070740.1
GCP 1 residual  2.77 m
GCP 2 residual  3.76 m
GCP 3 residual  4.72 m
GCP 4 residual  5.74 m
GCP 5 residual 20.79 m
GCP 6 residual  4.03 m
RMSE with all six = 9.36 m; largest residual is GCP 5
RMSE after removing it = 0.80 m
pixel size ~ 2.12 m (1:25,000 scanned at 300 dpi gives 2.12 m)
```
Read the residuals: one large residual tells the operator to re-check that GCP (here the deliberate blunder). Remove it only if a reason is found, then refit. Never use fewer GCPs than the transformation needs, and spread them over the whole map including the corners, because a transformation is only trustworthy *inside* the polygon of its GCPs.

### 3.2.2 GPS and GNSS

**GNSS** (global navigation satellite system) is the general name; **GPS** (USA) is one system, alongside **GLONASS** (Russia), **Galileo** (EU), **BeiDou** (China) and the regional **NavIC** (India). GPS has at least 24 satellites in six orbital planes at about 20,200 km altitude, each broadcasting its position and the precise time. A receiver measures the signal travel time to each satellite and multiplies by the speed of light to get a **range**. One range places the receiver on a sphere around that satellite; with ranges to several satellites the spheres intersect at the receiver.

Three unknowns (x, y, z) would need three satellites, but a cheap receiver clock is wrong by an unknown amount, and because light travels 300 km in a millisecond that error is huge. The clock error is a **fourth unknown**, so **at least four satellites** are needed. The measured distances are therefore called **pseudoranges**, and the receiver solves the position and clock bias by iterative least squares. More satellites give a better solution.

```svgfig label="3.1" caption="GNSS positioning. The receiver measures pseudoranges to four or more satellites and solves for x, y, z and its own clock error. Accuracy depends on satellite geometry (DOP) as well as on the range errors."
f = Fig(680, 270)
sats = ((120, 40), (300, 25), (480, 40), (600, 70))
f.box(280, 205, 120, 40, "Receiver\n(x, y, z, clock)", fill=SAND, stroke=AMBER, size=10)
for i, (x, y) in enumerate(sats, 1):
    f.circle(x, y, 17, fill=BLUE, stroke=NAVY, label="S%d" % i, size=10)
    f.arrow([(x, y + 17), (340 + (x - 340) * 0.25, 205)], color=SLATE, dash=True, label="range %d" % i, lpos=(x + (340 - x) * 0.45 + (22 if x < 340 else 40), y + 92 - (12 if i == 2 else 0)), lsize=9)
f.text(340, 262, "Four unknowns (x, y, z, clock bias) need at least four satellites", size=10, color=SLATE)
```

**Accuracy sources.** Typical consumer receivers give about 3 to 5 m horizontal accuracy in open sky. Errors come from the atmosphere (ionosphere and troposphere delay the signal), satellite orbit and clock error, **multipath** (signals bouncing off buildings and cliffs, a serious problem in narrow Himalayan valleys and city streets), receiver noise, and **geometry**. **DOP** (dilution of precision) is the number that scales range error into position error: smaller is better, below 2 is good, above 6 is poor. It is large when satellites are bunched together or close to the horizon.

**Improving accuracy.** **Differential GPS (DGPS)** and **RTK** use a reference station at a known position to compute corrections; **PPP** applies precise orbit and clock products; **SBAS** broadcasts corrections by geostationary satellite; dual-frequency receivers cancel most ionospheric delay. Survey-grade RTK reaches centimetres.

```python
# Solve a GNSS position with 4 pseudoranges by Gauss-Newton and compare good and poor satellite geometry (DOP).
import numpy as np
rng = np.random.default_rng(7)
R_E, R_S = 6371.0, 26560.0                          # km: Earth radius, GPS orbit radius
rx_true = np.array([R_E, 0.0, 0.0])                 # receiver on the surface (km)
bias_km = 0.0001 * 299792.458                       # receiver clock error 0.1 ms = 29.98 km (!)

def sat(az_deg, el_deg):
    """Satellite position for an azimuth/elevation seen from the receiver (local frame x=up, y=east, z=north)."""
    az, el = np.radians(az_deg), np.radians(el_deg)
    d = np.array([np.sin(el), np.cos(el) * np.sin(az), np.cos(el) * np.cos(az)])
    # distance along the line of sight to a sphere of radius R_S
    b = rx_true @ d; t = -b + np.sqrt(b * b - (rx_true @ rx_true - R_S ** 2))
    return rx_true + t * d

def solve(sats, noise_m):
    rho = np.array([np.linalg.norm(s - rx_true) + bias_km for s in sats]) + rng.normal(0, noise_m / 1000, len(sats))
    x = np.array([0.0, 0.0, 0.0, 0.0])              # start at Earth's centre
    for _ in range(12):
        d = np.array([np.linalg.norm(s - x[:3]) for s in sats])
        G = np.array([list((x[:3] - s) / dd) + [1.0] for s, dd in zip(sats, d)])
        dx, *_ = np.linalg.lstsq(G, rho - (d + x[3]), rcond=None)
        x += dx
    return x, G

def dop(G):
    return np.sqrt(np.trace(np.linalg.inv(G.T @ G)))

good = [sat(0, 80), sat(90, 40), sat(180, 40), sat(270, 40)]      # spread around the sky
poor = [sat(20, 45), sat(30, 50), sat(25, 40), sat(35, 55)]       # bunched together
for name, ss in (("good geometry", good), ("poor geometry", poor)):
    errs = []
    for _ in range(200):
        x, G = solve(ss, 5.0)                                     # 5 m range noise
        errs.append(np.linalg.norm(x[:3] - rx_true) * 1000)
    print("%-14s DOP %5.1f   mean position error over 200 trials: %6.1f m" % (name, dop(G), np.mean(errs)))
x, G = solve(good, 0.0)
print("noise-free solution: position error %.3f m, recovered clock bias %.2f km" % (np.linalg.norm(x[:3] - rx_true) * 1000, x[3]))
```
```output
good geometry  DOP   5.3   mean position error over 200 trials:   16.8 m
poor geometry  DOP 190.2   mean position error over 200 trials:  561.2 m
noise-free solution: position error 0.000 m, recovered clock bias 29.98 km
```
**NMEA sentences.** Receivers output text lines in the **NMEA 0183** format, such as `$GPGGA,...`, with time, latitude, longitude, fix quality, number of satellites, **HDOP** and altitude. Latitude is written as degrees and decimal minutes (ddmm.mmmm) and must be converted to decimal degrees: degrees + minutes / 60. The text between `$` and `*` is XOR-ed to give a two-digit checksum that detects corrupted lines.

```python
# Parse a GGA sentence: checksum, decimal degrees, quality.
s = "$GPGGA,051523.00,2743.0310,N,08519.4440,E,1,08,1.1,1350.0,M,-33.0,M,,"
body = s[1:]
cs = 0
for ch in body:
    cs ^= ord(ch)
sentence = s + "*%02X" % cs
print(sentence)
f = s.split(",")
def dm_to_deg(v, hemi):
    deg = int(float(v) // 100); minutes = float(v) - deg * 100
    d = deg + minutes / 60
    return -d if hemi in "SW" else d
lat, lon = dm_to_deg(f[2], f[3]), dm_to_deg(f[4], f[5])
print("time %s:%s:%s UTC, lat %.5f, lon %.5f, fix quality %s, %s satellites, HDOP %s, altitude %s m" %
      (f[1][:2], f[1][2:4], f[1][4:6], lat, lon, f[6], f[7], f[8], f[9]))
```
```output
$GPGGA,051523.00,2743.0310,N,08519.4440,E,1,08,1.1,1350.0,M,-33.0,M,,*7F
time 05:15:23 UTC, lat 27.71718, lon 85.32407, fix quality 1, 08 satellites, HDOP 1.1, altitude 1350.0 m
```
The "good geometry" figure above is a **GDOP** (it includes the clock term) for exactly four satellites. Real receivers see eight to twelve satellites, which lowers DOP considerably; the point of the experiment is the factor of about 35 between spread-out and bunched satellites, which turns a few metres of range noise into hundreds of metres of position error.

### 3.2.3 Images: remote sensing and aerial photographs

**Remote sensing** records the energy reflected or emitted by the Earth's surface from a distance, using sensors on satellites, aircraft or drones. Images supply **land cover**, **change over time** and **elevation** (stereo pairs, radar, LiDAR) for areas that are too large, remote or dangerous to survey on foot, which describes much of the Himalaya. Four kinds of **resolution** describe an image:

| Resolution | Meaning | Example |
|---|---|---|
| **Spatial** | Ground size of one pixel | 10 m (Sentinel-2 visible and near-infrared), 30 m (Landsat), 0.5 m (commercial), 3 cm (drone) |
| **Spectral** | Number and width of wavelength bands | Landsat 8 and 9 carry 11 bands, Sentinel-2 has 13 |
| **Temporal** | How often the same place is imaged | Landsat every 16 days per satellite, Sentinel-2 every 5 days with two satellites |
| **Radiometric** | Number of brightness levels recorded | 8-bit (256 levels), 12-bit (4,096 levels) |

A basic trade-off: finer spatial resolution means a smaller swath and a smaller area per image. Cloud cover in the monsoon is a major limit for optical sensors in Nepal; **radar** (such as Sentinel-1) sees through cloud, which is why it is used for flood mapping.

**Aerial photographs** taken from aircraft or drones are processed into an **orthophoto**, an image corrected for the tilt of the camera and for **relief displacement** (tall or high features appear to lean away from the centre of the photo). Overlapping photographs also yield a 3-D **point cloud** and a **digital surface model** by photogrammetry.

**Image processing steps:** preprocessing (radiometric and atmospheric correction, georeferencing), **enhancement** (contrast stretch, filters), **band combinations** (false-colour composites show vegetation in red), **indices**, and **classification**, which turns pixel values into classes. In **supervised classification** the analyst gives training areas of known classes (forest, water, built-up) and the computer assigns each pixel to the nearest class; in **unsupervised classification** the computer groups pixels (for example by k-means) and the analyst names the groups afterwards. Accuracy is assessed with a **confusion matrix** from independent reference points.

The commonest index is the **Normalised Difference Vegetation Index**:

**NDVI = (NIR - Red) / (NIR + Red)**

Healthy plants reflect strongly in the near-infrared (NIR) and absorb red light, so NDVI is close to +0.6 to +0.9 for dense vegetation, about 0.2 to 0.4 for sparse crops or grass, near 0 for bare soil and built-up land, and negative for water.

```python
# NDVI from two 4x6 reflectance rasters (Sentinel-2 band 8 = NIR, band 4 = red) and a threshold classification.
import numpy as np
nir = np.array([[0.45, 0.50, 0.48, 0.22, 0.20, 0.05],
                [0.47, 0.52, 0.40, 0.25, 0.18, 0.04],
                [0.30, 0.35, 0.28, 0.24, 0.26, 0.03],
                [0.26, 0.22, 0.21, 0.30, 0.33, 0.03]])
red = np.array([[0.06, 0.05, 0.07, 0.15, 0.17, 0.06],
                [0.06, 0.04, 0.09, 0.17, 0.16, 0.05],
                [0.14, 0.12, 0.15, 0.18, 0.15, 0.04],
                [0.19, 0.18, 0.17, 0.12, 0.10, 0.04]])
ndvi = (nir - red) / (nir + red)
print(np.round(ndvi, 2))
cls = np.select([ndvi < 0.0, ndvi < 0.2, ndvi < 0.5], [0, 1, 2], default=3)   # water, bare/built, sparse, dense
names = ["water", "bare or built-up", "sparse vegetation", "dense vegetation"]
cell_ha = 10 * 10 / 10000                                                  # a 10 m cell is 0.01 ha
for i, n in enumerate(names):
    print("%-18s %2d cells = %.2f ha" % (n, (cls == i).sum(), (cls == i).sum() * cell_ha))
```
```output
[[ 0.76  0.82  0.75  0.19  0.08 -0.09]
 [ 0.77  0.86  0.63  0.19  0.06 -0.11]
 [ 0.36  0.49  0.3   0.14  0.27 -0.14]
 [ 0.16  0.1   0.11  0.43  0.53 -0.14]]
water               4 cells = 0.04 ha
bare or built-up    8 cells = 0.08 ha
sparse vegetation   5 cells = 0.05 ha
dense vegetation    7 cells = 0.07 ha
```
### 3.2.4 Databases and tables

Much GIS data starts life in a table, not on a map: census counts, a register of schools, an attendance sheet. A **relational database** stores these as tables, and the GIS joins them to geometry through a **key** (a ward code, district ID). This **attribute join** is the most frequent GIS operation of all. SQL expresses it directly.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE ward (ward_id INTEGER PRIMARY KEY, name TEXT, area_km2 REAL);          -- geometry would sit here too
CREATE TABLE census (ward_id INTEGER, population INTEGER, households INTEGER);
CREATE TABLE school (school_id INTEGER PRIMARY KEY, ward_id INTEGER, name TEXT, students INTEGER);
INSERT INTO ward VALUES (1,'Ward 1',3.2),(2,'Ward 2',1.8),(3,'Ward 3',5.5),(4,'Ward 4',2.4);
INSERT INTO census VALUES (1,9800,2400),(2,15200,3900),(3,7600,1800),(4,12100,3100);
INSERT INTO school VALUES (1,1,'Janata',420),(2,2,'Saraswati',510),(3,2,'Adarsha',330),(4,4,'Pragati',260);
""")
q = """SELECT w.name, c.population,
              ROUND(c.population / w.area_km2) AS density,
              COALESCE(SUM(s.students), 0) AS pupils,
              COUNT(s.school_id) AS schools
       FROM ward w JOIN census c ON c.ward_id = w.ward_id
                   LEFT JOIN school s ON s.ward_id = w.ward_id
       GROUP BY w.ward_id ORDER BY density DESC"""
print("%-8s %10s %8s %7s %8s" % ("ward", "population", "density", "pupils", "schools"))
for r in con.execute(q):
    print("%-8s %10d %8d %7d %8d" % r)
print("wards with no school:", [r[0] for r in con.execute("SELECT name FROM ward WHERE ward_id NOT IN (SELECT ward_id FROM school)")])
```
```output
ward     population  density  pupils  schools
Ward 2        15200     8444     840        2
Ward 4        12100     5042     260        1
Ward 1         9800     3063     420        1
Ward 3         7600     1382       0        0
wards with no school: ['Ward 3']
```
Notice the **LEFT JOIN**: Ward 3 has no school but must still appear, with zero. An inner join would silently drop it, a classic GIS mistake that makes a gap in service invisible.

**Geocoding** turns an address or place name into coordinates, by matching it against a reference list (street segments with address ranges, or point addresses) and interpolating a position. **Reverse geocoding** does the opposite. Quality varies: Nepal's informal addressing means landmarks and ward numbers often replace street numbers, and results need a **match score** and a manual check of low-score records. A **spatial database** (PostgreSQL with **PostGIS**, SQLite with SpatiaLite) adds geometry types and functions such as `ST_Distance`, `ST_Within`, `ST_Intersects`, `ST_Buffer` and `ST_Area`, plus spatial indexes (Section 3.5).

## 3.3 Data structures: vector, raster and TIN

A **data structure** is the way the computer stores the geometry of features. There are three.

### 3.3.1 Vector

The vector structure stores **discrete features** as exact coordinates:

| Geometry | Stored as | Examples |
|---|---|---|
| **Point** | One (x, y) pair | Well, school, tree, GPS fix |
| **Line (polyline)** | An ordered list of vertices | Road, river, pipeline |
| **Polygon** | A closed ring of vertices (with optional holes) | Ward, lake, parcel |

Each geometry has an ID that links it to a row of attributes. **Multi-part** features exist (a district made of two separate pieces, an island chain). Vector data are compact, give crisp boundaries at any zoom, suit the object view and make it easy to attach many attributes, but overlay is computationally heavy and surfaces such as elevation are awkward.

**Topology** is the study of spatial relationships that do not change when the map is stretched: **connectivity** (which lines meet at which nodes), **adjacency** (which polygons share an edge), and **containment** (a lake inside a district; an island inside a lake). A **topological data structure** (the arc-node model) stores each boundary line once as an **arc** with a start node, an end node and the polygon on its left and right. It saves space, prevents slivers (a shared boundary cannot be digitised twice), and speeds up questions like "which wards neighbour Ward 3?" and "can the ambulance travel from A to B?". A **non-topological** format, such as the simple features model used in shapefiles and GeoJSON, stores every polygon's full ring independently (simple, but shared edges can disagree). Topology rules (no gaps, no overlaps, lines must not self-intersect) are then checked by software.

```svgfig label="3.2" caption="The same landscape in three structures. Vector: a road (line), a lake (polygon) and a well (point) with exact coordinates. Raster: the same scene as a grid of cells, each holding one class. TIN: elevation sample points joined into non-overlapping triangles."
f = Fig(680, 230)
# vector panel
f.text(90, 18, "Vector", size=12, color=NAVY, bold=True)
f.poly([(20, 160), (160, 160), (160, 30), (20, 30)], fill=SOFT, stroke=SLATE)
f.poly([(70, 60), (125, 55), (140, 95), (95, 120), (60, 100)], fill="#bfdbfe", stroke=NAVY)
f.line(20, 140, 70, 125, color=AMBER, sw=3)
f.line(70, 125, 130, 140, color=AMBER, sw=3)
f.line(130, 140, 160, 120, color=AMBER, sw=3)
f.circle(130, 45, 5, fill=RED, stroke=RED)
f.text(90, 185, "points, lines, polygons", size=9.5, color=SLATE)
# raster panel
f.text(340, 18, "Raster", size=12, color=NAVY, bold=True)
grid = ["....L..", "..LLLL.", ".LLLLL.", "..LLL..", ".......", "RRRRRRR"]
for r, row in enumerate(grid):
    for c, ch in enumerate(row):
        fill = "#bfdbfe" if ch == "L" else (SAND if ch == "R" else SOFT)
        f.box(255 + c * 24, 30 + r * 22, 24, 22, "", fill=fill, stroke=SLATE)
f.text(340, 185, "rows and columns of cells", size=9.5, color=SLATE)
# TIN panel
f.text(590, 18, "TIN", size=12, color=NAVY, bold=True)
pts = [(510, 160), (600, 165), (670, 150), (520, 100), (590, 90), (660, 105), (545, 40), (625, 35)]
tri = [(0, 1, 3), (1, 3, 4), (1, 4, 5), (1, 2, 5), (3, 4, 6), (4, 6, 7), (4, 5, 7)]
for a, b, c in tri:
    f.poly([pts[a], pts[b], pts[c]], fill=MINT, stroke=TEAL, sw=1.1)
for p in pts:
    f.circle(p[0], p[1], 3, fill=NAVY, stroke=NAVY)
f.text(590, 185, "triangles joining sample points", size=9.5, color=SLATE)
```

**Common vector file formats.** The **shapefile** (Esri; at least `.shp` geometry, `.shx` index and `.dbf` attributes, plus `.prj` for the CRS) is universal but old: it holds one geometry type per file, truncates field names to 10 characters, and stops at 2 GB. **GeoJSON** (RFC 7946) is JSON text, always longitude-latitude in WGS 84, ideal for the web. **GeoPackage** (`.gpkg`) is an OGC standard built on SQLite, holding many layers, rasters and attributes in one file, and is the recommended modern format. **KML** is used by Google Earth, and **GML** is an XML standard. **WKT** and **WKB** (well-known text and binary) are the formats spatial databases use for single geometries.

```python
# Parse WKT geometries and compute length, area (shoelace formula) and centroid.
import math, re
def parse(wkt):
    kind = wkt.split("(", 1)[0].strip().upper()
    nums = [tuple(map(float, p.split())) for p in re.findall(r"(-?[\d.]+ -?[\d.]+)", wkt)]
    return kind, nums

def length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def area_centroid(ring):
    a = cx = cy = 0.0
    for i in range(len(ring) - 1):
        (x1, y1), (x2, y2) = ring[i], ring[i + 1]
        cr = x1 * y2 - x2 * y1
        a += cr; cx += (x1 + x2) * cr; cy += (y1 + y2) * cr
    a /= 2
    return abs(a), cx / (6 * a), cy / (6 * a)

for w in ("POINT (85.32 27.71)",
          "LINESTRING (0 0, 300 400, 300 1000)",
          "POLYGON ((0 0, 4000 0, 4000 3000, 0 3000, 0 0))"):
    kind, pts = parse(w)
    if kind == "POINT": print(kind, "at", pts[0])
    elif kind == "LINESTRING": print(kind, "with %d vertices, length %.0f m" % (len(pts), length(pts)))
    else:
        a, cx, cy = area_centroid(pts)
        print(kind, "area %.0f m2 = %.1f ha, perimeter %.0f m, centroid (%.0f, %.0f)" % (a, a / 1e4, length(pts), cx, cy))
```
```output
POINT at (85.32, 27.71)
LINESTRING with 3 vertices, length 1100 m
POLYGON area 12000000 m2 = 1200.0 ha, perimeter 14000 m, centroid (2000, 1500)
```
### 3.3.2 Raster

A **raster** divides the area into a regular grid of **cells (pixels)**, each storing one value: a class code, a measurement, or a colour. Position is implicit (row and column plus the origin and **cell size**), so no coordinates are stored. Raster suits the **field view**: elevation, temperature, rainfall, satellite images and any continuous or classified surface.

Key properties: **cell size (resolution)**, **extent** (number of rows and columns), **number of bands** (a satellite image has several), **data type** (integer for classes, float for measurements) and **NoData** value for missing cells. The cell value should be interpreted: a **categorical** raster (land-cover codes) must not be averaged when resampled, use *nearest neighbour*; a **continuous** raster can use *bilinear* or *cubic* interpolation.

**Trade-off.** Smaller cells give better detail but the number of cells grows with the **square** of the resolution: halving the cell size quadruples the cells. **Compression** is therefore essential: **run-length encoding (RLE)** stores a value and how many times it repeats along a row, which works for large uniform areas such as land cover; a **quadtree** repeatedly splits the grid into four quadrants until each quadrant is uniform, which stores a large uniform block as one node; image formats such as **GeoTIFF** support LZW or deflate compression and **Cloud-Optimised GeoTIFF** supports reading only the needed tiles.

```python
# Raster storage: size of Nepal at several resolutions, run-length encoding and a quadtree.
AREA_KM2 = 147181                                    # Nepal, approximate
for cell in (1000, 250, 90, 30, 10):
    cells = AREA_KM2 * 1e6 / cell ** 2
    print("cell %4d m: %10.1f million cells, %8.1f MB at 1 byte per cell, %9.1f MB at 4 bytes" % (cell, cells / 1e6, cells / 1e6, cells * 4 / 1e6))

r = ["WWWWWWWW", "WWWWWWWW", "WWWWFFFF", "WWWWFFFF", "FFFFFFFF", "FFFFFFFF", "FFFFBBFF", "FFFFBBFF"]   # W water F forest B built
def rle(row):
    out, prev, n = [], row[0], 0
    for ch in row:
        if ch == prev: n += 1
        else: out.append((prev, n)); prev, n = ch, 1
    out.append((prev, n)); return out
runs = sum(len(rle(row)) for row in r)
print("RLE: 64 cells stored as %d (value, count) pairs" % runs)

def quad(x, y, size):
    vals = {r[y + j][x + i] for j in range(size) for i in range(size)}
    if len(vals) == 1: return 1                      # one leaf
    h = size // 2
    return 1 + sum(quad(x + dx, y + dy, h) for dy in (0, h) for dx in (0, h))
print("quadtree: %d nodes (leaves and splits) for the same 64 cells" % quad(0, 0, 8))
```
```output
cell 1000 m:        0.1 million cells,      0.1 MB at 1 byte per cell,       0.6 MB at 4 bytes
cell  250 m:        2.4 million cells,      2.4 MB at 1 byte per cell,       9.4 MB at 4 bytes
cell   90 m:       18.2 million cells,     18.2 MB at 1 byte per cell,      72.7 MB at 4 bytes
cell   30 m:      163.5 million cells,    163.5 MB at 1 byte per cell,     654.1 MB at 4 bytes
cell   10 m:     1471.8 million cells,   1471.8 MB at 1 byte per cell,    5887.2 MB at 4 bytes
RLE: 64 cells stored as 14 (value, count) pairs
quadtree: 13 nodes (leaves and splits) for the same 64 cells
```
### 3.3.3 TIN

A **triangulated irregular network (TIN)** models a surface as a set of **non-overlapping triangles** whose corners are irregularly spaced sample points (**nodes**) with known elevation. Each triangle is a flat facet, so its slope and aspect are constant, and the surface passes exactly through every node. The standard way to choose the triangles is **Delaunay triangulation**: no node lies inside the circumscribed circle of any triangle. This maximises the smallest angle and avoids long thin triangles.

A TIN puts points where the terrain changes (ridges, streams, breaks of slope) and few where it is flat, so it needs **fewer values than a raster** of comparable accuracy and keeps **exact heights** at survey points, but it is more complex to build and update, and less suited to map algebra. The elevation of any point inside a triangle follows from **barycentric (plane) interpolation**.

```python
# Delaunay TIN of 9 survey points: facets, plane interpolation and facet slope.
import numpy as np
from scipy.spatial import Delaunay
pts = np.array([[0, 0, 100], [100, 0, 110], [200, 0, 130], [0, 100, 105], [100, 100, 125],
                [200, 100, 150], [0, 200, 120], [100, 200, 140], [200, 200, 175]], dtype=float)   # x, y (m), z (m)
tin = Delaunay(pts[:, :2])
print("triangles:", len(tin.simplices))

def facet_plane(tri):
    """Plane z = a x + b y + c through the three nodes."""
    A = np.column_stack([pts[tri, 0], pts[tri, 1], np.ones(3)])
    return np.linalg.solve(A, pts[tri, 2])

for i, tri in enumerate(tin.simplices[:4]):
    a, b, c = facet_plane(tri)
    slope = np.degrees(np.arctan(np.hypot(a, b)))
    aspect = (np.degrees(np.arctan2(-a, -b)) + 360) % 360          # downslope direction, degrees clockwise from north
    print("facet %d nodes %s slope %.1f deg aspect %.0f deg" % (i, list(map(int, tri)), slope, aspect))

q = np.array([[130.0, 60.0]])
t = tin.find_simplex(q)[0]
a, b, c = facet_plane(tin.simplices[t])
print("elevation at (130, 60) by TIN interpolation: %.1f m" % (a * 130 + b * 60 + c))
```
```output
triangles: 8
facet 0 nodes [3, 1, 4] slope 14.0 deg aspect 233 deg
facet 1 nodes [1, 3, 0] slope 6.4 deg aspect 243 deg
facet 2 nodes [7, 3, 4] slope 14.0 deg aspect 233 deg
facet 3 nodes [3, 7, 6] slope 14.0 deg aspect 233 deg
elevation at (130, 60) by TIN interpolation: 126.5 m
```
### 3.3.4 Choosing between structures

| Aspect | Vector | Raster | TIN |
|---|---|---|---|
| View of space | Object | Field | Field (surface) |
| Position | Exact coordinates | Cell centre; resolution-limited | Exact at nodes |
| Storage | Compact for few features | Large (cells squared) unless compressed | Compact for terrain |
| Boundaries | Sharp, scale-free | Stair-stepped, depends on cell size | Edges of facets |
| Overlay and map algebra | Slow (geometry) | Fast (cell by cell) | Specialised |
| Network and topology | Excellent | Poor | n/a |
| Best for | Roads, parcels, wards, services | Elevation, imagery, land cover, suitability | Terrain, volumes, 3-D |
| Typical formats | GeoPackage, shapefile, GeoJSON | GeoTIFF, COG, ASCII grid | Esri TIN, LandXML |

No structure wins everywhere, so real projects mix them and **convert** (rasterise, vectorise, interpolate) when necessary, always paying attention to the information lost in conversion.

## 3.4 GIS data modelling

### 3.4.1 From the real world to the database

A **data model** is a set of rules for describing the real world in a form a computer can store. Modelling is stepwise, moving from idea to implementation:

1. **Reality**: the actual landscape with all its detail.
2. **Conceptual model**: *what* matters for this purpose, in the users' words: the kinds of **entities** (ward, road, school), their **attributes** and their **relationships** (a school *is in* a ward). Drawn as an entity-relationship diagram.
3. **Logical model**: the data structure used by the GIS software: tables, geometry types, keys, topology, domains (allowed values).
4. **Physical model**: files, formats, storage, indexes, coordinate system, naming; the actual implementation.

Spatial modelling decides **what is a feature, what is a layer and what is a surface**, and how fine to go. The same river can be a line (for navigation), a polygon (for flood analysis) or a set of cells (in a hydrological raster).

### 3.4.2 Object and field models

| Model | Idea | Representation | Example |
|---|---|---|---|
| **Object (entity)** | Discrete things with identity and geometry | Vector points, lines, polygons, networks | Buildings, roads, parcels |
| **Field** | A property with a value at every location | Raster, TIN, contour | Elevation, temperature, rainfall |
| **Network** | Linked nodes and edges with flow and cost | Graph with turn rules | Road and pipe networks |
| **Temporal** | Features with history | Time-stamped records | Land-ownership change |

Beyond the vector and raster structures there are richer **GIS data models** used in software: the **coverage** model (the older arc-node topology), the **shapefile** simple-features model, the **geodatabase** (object-oriented: feature classes, feature datasets, relationship classes, subtypes, domains and topology rules), and the **OGC Simple Features** specification, which defines geometry types and the spatial predicates that PostGIS and GeoPackage implement.

### 3.4.3 Worked modelling example

*Problem: a municipality wants to keep school locations, ward boundaries, roads and flood zones to plan evacuation.*

| Entity | Geometry | Key attributes | Relationship |
|---|---|---|---|
| Ward | Polygon | ward_id, name, population | Contains schools |
| School | Point | school_id, name, students, ward_id | Belongs to one ward |
| Road | Line | road_id, name, surface, width, one_way | Connects at nodes; network |
| Flood zone | Polygon | zone_id, return_period | Overlaps wards and roads |
| Elevation | Raster (10 m) | metres | Field underlying all |

Decisions to record: all layers in one CRS (for example UTM 45N), scale of use about 1:10,000 so polygon vertices are within 5 m, the `ward_id` as a foreign key so census tables can be joined, and a domain for `surface` limited to *blacktop, gravel, earth*.

## 3.5 GIS database design

### 3.5.1 Steps

Designing a GIS database follows the same stages as any database, with spatial extras:

1. **Requirements**: users, questions, outputs, accuracy, update frequency.
2. **Conceptual design**: entities, attributes, relationships.
3. **Logical design**: map entities to layers and tables, choose geometry types, normalise attributes, define keys, domains and topology rules.
4. **Physical design**: choose format or DBMS, coordinate system, indexes, tiling and partitioning, backup.
5. **Implementation and loading**: capture or convert data, run quality checks.
6. **Maintenance**: updates, versioning, metadata, security.

Spatial design choices that are easy to get wrong: **one CRS for the database**, **geometry type per layer**, **precision** (do not store coordinates to the micrometre), **a stable key** for every feature, **separate current and historical data**, and **a metadata record per layer**. Attributes should be **normalised** (no repeating the district name in every ward row; store a district code and a lookup table) exactly as in a relational design, with the geometry in its own column.

### 3.5.2 Spatial indexing

Finding the features near a point by checking every feature is O(n). A **spatial index** narrows the search to a few candidates using **bounding boxes (MBRs)**, then the exact geometry test is applied only to those candidates (a *filter-and-refine* scheme).

| Index | Idea |
|---|---|
| **Grid** | Divide space into fixed cells; each cell lists the features that touch it. Simple, works for evenly spread data |
| **Quadtree** | Recursively split into four quadrants where data are dense |
| **R-tree** | A balanced tree of nested bounding boxes (Guttman, 1984); the default in PostGIS (as GiST), SQLite and GeoPackage |
| **Geohash / H3** | Hierarchical grid codes that turn location into a sortable string or number |

```python
# A grid index against a brute-force scan, then SQLite's built-in R-tree.
import random, sqlite3, time
random.seed(3)
pts = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20000)]    # 20,000 points in a 100 x 100 km area
box = (40, 40, 42, 42)                                                             # window query
def inside(p):
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]

t0 = time.perf_counter(); brute = [i for i, p in enumerate(pts) if inside(p)]; t_brute = time.perf_counter() - t0

CELL = 2.0
grid = {}
for i, (x, y) in enumerate(pts):
    grid.setdefault((int(x // CELL), int(y // CELL)), []).append(i)
t0 = time.perf_counter()
cand = [i for gx in range(int(box[0] // CELL), int(box[2] // CELL) + 1) for gy in range(int(box[1] // CELL), int(box[3] // CELL) + 1) for i in grid.get((gx, gy), [])]
fast = [i for i in cand if inside(pts[i])]; t_grid = time.perf_counter() - t0
print("brute force found %d points examining 20000; grid index examined %d candidates and found %d (same result: %s)" % (len(brute), len(cand), len(fast), sorted(brute) == sorted(fast)))

con = sqlite3.connect(":memory:")
con.execute("CREATE VIRTUAL TABLE idx USING rtree(id, minx, maxx, miny, maxy)")
con.executemany("INSERT INTO idx VALUES (?,?,?,?,?)", [(i, x, x, y, y) for i, (x, y) in enumerate(pts)])
rt = [r[0] for r in con.execute("SELECT id FROM idx WHERE minx>=? AND maxx<=? AND miny>=? AND maxy<=?", (box[0], box[2], box[1], box[3]))]
print("SQLite R-tree returned %d points (same result: %s)" % (len(rt), sorted(rt) == sorted(brute)))
```
```output
brute force found 9 points examining 20000; grid index examined 34 candidates and found 9 (same result: True)
SQLite R-tree returned 9 points (same result: True)
```
### 3.5.3 Quality, security and sharing

A good GIS database enforces **integrity rules** (domains, required fields, topology rules such as "wards must not overlap and must not leave gaps"), keeps **lineage** and **metadata**, supports **versioning** and **multi-user editing** (so two editors do not overwrite each other), manages **permissions** (field staff edit, public view), and publishes through **standard web services** (OGC WMS for map images, WFS for features, WMTS for tiles) so other systems can use it without copying files. Backup and a documented update cycle matter more than the choice of software.

## 3.6 Summary and exercises

Data are captured by primary (survey, GNSS, remote sensing) or secondary (digitising, scanning, import, geocoding) methods and must be checked for completeness, accuracy and topology. Sources are maps (georeferenced by an affine fit to ground control points, judged by RMSE), GPS (four or more pseudoranges give x, y, z and clock bias; geometry is summarised by DOP), images (four resolutions; NDVI = (NIR - Red) / (NIR + Red)) and databases (joins on keys, geocoding). The vector structure stores exact points, lines and polygons with attributes and topology; the raster stores a grid of cells (size grows with the square of the resolution, compression by RLE and quadtree); the TIN is a Delaunay triangulation of surface points. Modelling moves from conceptual to logical to physical, using object and field views. Database design chooses one CRS, stable keys, normalised attributes, metadata and a spatial index (grid, quadtree or R-tree) using filter and refine.

1. Distinguish primary and secondary data capture with two methods of each.
2. List five digitising errors and five post-capture quality checks.
3. What is georeferencing? Explain GCPs, the affine transformation and RMSE. Why should GCPs be spread over the map?
4. A 1:25,000 map is scanned at 300 dpi. Find the ground size of a pixel.
5. Explain how GPS finds a position. Why are four satellites needed, not three?
6. Define DOP. Why does bunching of satellites increase position error? List four sources of GPS error.
7. Convert 2743.0310 N (ddmm.mmmm) to decimal degrees.
8. List and explain four kinds of resolution of an image with an example for each.
9. A pixel has NIR 0.40 and red 0.10. Compute NDVI and say what the surface probably is.
10. Why does an inner join hide wards that have no school? Which join keeps them?
11. Compare vector and raster data under six headings.
12. What is topology? Explain the arc-node model and three benefits.
13. A 30 m raster covers a 90 km by 60 km district. How many cells, and how many MB at 2 bytes per cell? What happens to the count at 10 m?
14. Explain run-length encoding and a quadtree. Which suits a land-cover map and why?
15. What is a TIN? State the Delaunay criterion and two advantages over a raster for terrain.
16. Differentiate conceptual, logical and physical data models. Draw an entity list for a school-mapping database.
17. Why is a spatial index needed? Describe the filter-and-refine approach.

**Answers to the numerical items.** (4) Pixel = 0.0254 m / 300 x 25,000 = **2.12 m**. (7) 27 + 43.0310 / 60 = **27.71718 degrees N**. (9) NDVI = (0.40 - 0.10) / (0.40 + 0.10) = **0.60**, dense healthy vegetation. (13) Area = 90,000 m x 60,000 m = 5.4 x 10^9 m2; cells = 5.4 x 10^9 / 900 = **6.0 million**; size = 6.0 million x 2 = **12 MB**; at 10 m the cell area is 100 m2, so cells = 54 million (9 times more), 108 MB.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare vector and raster data structures.**

Vector stores discrete features as points, lines and polygons with exact coordinates and linked attributes; it is compact, gives sharp boundaries at any scale, supports topology and networks, and suits roads, parcels and wards. Raster stores a grid of equal cells with one value each, with position implied by row and column; it suits continuous fields such as elevation, imagery and land cover, makes overlay and map algebra fast, but its size grows with the square of resolution and boundaries look stair-stepped. Vector suits the object view, raster the field view; projects often convert between the two.

**Q2 (5 marks). Explain georeferencing a scanned map.**

A scan has only pixel coordinates. Georeferencing chooses ground control points identifiable on both the scan and in a reference coordinate system, such as graticule intersections or survey pillars, and fits a transformation (usually affine, with six parameters) from pixel (column, row) to ground (E, N). With more points than the minimum, least squares gives residuals for each point and an overall RMSE; a large residual signals a blunder to be rechecked. Points should be spread over the whole sheet because the transformation is reliable only inside the area they enclose. The result is then resampled or used to digitise features.

**Q3 (10 marks). Describe the principle, errors and accuracy of GPS positioning.**

Each GPS satellite broadcasts its position and time. The receiver measures the signal travel time and multiplies by the speed of light to get a pseudorange. A range puts the receiver on a sphere about the satellite, and the intersection of several spheres gives the position. Because the receiver clock is inexact and a millisecond of clock error means 300 km, the clock bias is a fourth unknown, so at least four satellites are needed; more give a least-squares solution with better reliability.

Errors arise from ionospheric and tropospheric delay, satellite orbit and clock errors, multipath from buildings and mountain walls, receiver noise and satellite geometry. The DOP number multiplies range error into position error; satellites spread across the sky give a low DOP while bunched satellites give a high one, as the experiment of this unit showed (error rising from tens to hundreds of metres). Consumer receivers reach 3 to 5 m in open sky. Differential GPS, RTK and PPP use corrections from reference stations or precise products, and dual-frequency receivers remove most ionospheric delay, bringing accuracy to the decimetre or centimetre level.
