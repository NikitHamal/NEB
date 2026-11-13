---
subject: Geographical Information System
grade: BCA Semester 8 (Elective III)
unit: 2
title: GIS and Map
hours: 6
area: BCA 453 · Geographical Information System · Unit 2
---

The map is the oldest GIS output and still the most important one. A GIS stores numbers, but people understand pictures, and the picture is only honest if the map-maker understands **scale**, **symbols**, **generalisation** and above all **map projection**: the mathematics of flattening a curved Earth onto a flat sheet or screen. This unit covers the characteristics of maps, the concepts and techniques of mapping, and map projections, including the coordinate systems you will meet in Nepal (WGS 84, UTM, and the modified UTM used by the Survey Department).

::: key What this unit gives you
- Map definition, types and characteristics: scale (three forms), symbols, generalisation, accuracy, and the standard map elements.
- Mapping concepts and techniques: the cartographic process, visual variables, classification of data for choropleth maps (four methods compared by program), and map design.
- Map projections: geoid, ellipsoid and datum, geographic and projected coordinates, families and properties, distortion, UTM and the Nepal grid, and Mercator, haversine and UTM computed in Python.
:::

## 2.1 Maps and their characteristics

### 2.1.1 What a map is

A **map** is a graphic, scaled and selective representation of part of the Earth (or any space) on a flat surface, showing the position and attributes of chosen features through symbols. Each word matters. *Graphic*: it is a picture. *Scaled*: distances are in proportion. *Selective*: it leaves things out on purpose. *Symbols*: it uses signs, not photographs. The map is a **model**, never the territory.

In a GIS the data layers are the **database**; a map is a **view** of that database for a purpose. One database can give a road map, a flood map and a population map by choosing different layers and symbols.

Maps are classified by purpose:

| Type | Purpose | Example |
|---|---|---|
| **Reference (general)** | Show many kinds of features so users can find things | Topographic maps at 1:25,000 and 1:50,000 from the Survey Department; road atlases |
| **Thematic** | Show the distribution of one subject | Population density by district, rainfall, land use |
| **Cadastral** | Show land parcels and ownership | Plot (kitta) maps used for land registration |
| **Navigation / charts** | Support movement | Aeronautical charts, trekking route maps |
| **Digital / web maps** | Interactive, zoomable, layered | OpenStreetMap, Google Maps, municipal web portals |

### 2.1.2 Scale

**Scale** relates distance on the map to distance on the ground. It is expressed three ways:

1. **Representative fraction (RF)** or ratio, such as **1:50,000**: one unit on the map equals 50,000 of the same unit on the ground. It has no units, so it works in any measuring system.
2. **Verbal scale**: "1 centimetre represents 500 metres".
3. **Graphic (bar) scale**: a line marked with ground distances. It is the only form that stays correct when a map is photocopied, enlarged or shown on screens of different sizes, so a printed map should always include one.

RF = map distance / ground distance, with both in the same unit. So `ground = map x denominator`. A 1:50,000 map has 1 cm = 50,000 cm = 500 m = 0.5 km.

Large and small scale are about the **fraction**, not the paper: 1:5,000 is a larger fraction than 1:50,000, so it is a *larger scale* and shows less ground in more detail. The distinction matters for generalisation and for data accuracy (Section 1.4.2): a feature drawn on a 1:50,000 map has a position uncertainty of about 0.5 mm x 50,000 = 25 m on the ground, since a pencil line is roughly half a millimetre wide.

```python
# Scale calculations: RF, verbal scale, areas and the positional error of a printed map.
def ground_from_map(map_cm, denom):
    return map_cm * denom / 100.0           # metres

def map_from_ground(ground_m, denom):
    return ground_m * 100.0 / denom         # centimetres

print("1:50,000, 7.4 cm on map ->", ground_from_map(7.4, 50000), "m on the ground")
print("1:25,000, 3 km of road   ->", map_from_ground(3000, 25000), "cm on the map")
print("1 cm = %.0f m at 1:50,000 and %.0f m at 1:25,000" % (ground_from_map(1, 50000), ground_from_map(1, 25000)))

# Areas scale with the SQUARE of the scale denominator
map_area_cm2 = 12.0
for d in (25000, 50000):
    km2 = map_area_cm2 * (d / 100000.0) ** 2
    print("12 cm2 on a 1:%d map = %.2f km2 on the ground" % (d, km2))

# Positional uncertainty of a 0.5 mm line
for d in (5000, 25000, 50000, 250000):
    print("1:%-7d 0.5 mm line = %6.1f m on the ground" % (d, 0.0005 * d))

# A map is enlarged 2x by a photocopier: the old RF no longer holds
old = 50000
print("after 2x enlargement the true RF is 1:%d (the printed 1:50,000 is now wrong)" % (old // 2))
```
```output
1:50,000, 7.4 cm on map -> 3700.0 m on the ground
1:25,000, 3 km of road   -> 12.0 cm on the map
1 cm = 500 m at 1:50,000 and 250 m at 1:25,000
12 cm2 on a 1:25000 map = 0.75 km2 on the ground
12 cm2 on a 1:50000 map = 3.00 km2 on the ground
1:5000    0.5 mm line =    2.5 m on the ground
1:25000   0.5 mm line =   12.5 m on the ground
1:50000   0.5 mm line =   25.0 m on the ground
1:250000  0.5 mm line =  125.0 m on the ground
after 2x enlargement the true RF is 1:25000 (the printed 1:50,000 is now wrong)
```
### 2.1.3 Other characteristics of a map

- **Symbols.** Points (a school), lines (a road) and areas (a forest) are drawn with symbols that should be *self-explanatory* where possible and always listed in a **legend**.
- **Generalisation.** Reducing detail as scale gets smaller: simplify a coastline, merge small lakes, drop minor roads, displace features that would overlap, exaggerate the width of a road so that it stays visible (a 6 m road at 1:50,000 would be 0.12 mm wide, invisible, so it is drawn about 0.5 mm wide, which stands for 25 m).
- **Projection and coordinate system.** How the curved Earth was flattened (Section 2.3).
- **Accuracy.** Horizontal and vertical accuracy are limited by survey method and by scale.
- **Currency.** The date of the data; a map is a snapshot.
- **Orientation.** Usually north is up, shown with a north arrow, or grid lines.

The **standard elements** of a finished map are: title, main map (the data frame), legend, scale bar, north arrow, coordinate grid or graticule labels, source and date, projection and datum note, author or organisation, and often an inset or locator map. Section 5.3 returns to layout.

## 2.2 Mapping concepts and techniques

### 2.2.1 The cartographic process

Making a map is a chain of decisions, not a button press:

1. **Define the purpose and audience.** Who will use the map and for what decision?
2. **Choose and prepare data.** Select layers, check coordinate systems and quality, join attributes.
3. **Choose the projection and scale** to suit the area and the use.
4. **Generalise and classify.** Simplify geometry; group continuous data into classes.
5. **Symbolise.** Assign colour, size, shape and pattern.
6. **Compose the layout** with the required elements, balance and hierarchy.
7. **Test and revise.** Ask a user to read it without help; print it to check.

### 2.2.2 Visual variables

Cartographers use six **visual variables** to encode data: **position**, **size**, **shape**, **colour hue**, **colour value (lightness)** and **texture/pattern**. Choose by the *level of measurement* of the data:

| Data type | Example | Good variables | Poor variables |
|---|---|---|---|
| **Nominal** (categories) | Land-use type | Hue, shape, pattern | Lightness (suggests order) |
| **Ordinal** (ranked) | Low, medium, high risk | Lightness, size | Random hues |
| **Interval or ratio** (numbers) | Population, rainfall | Lightness steps, proportional size | Rainbow colours with no order |

### 2.2.3 Thematic mapping techniques

| Technique | Data | What it shows | Watch out for |
|---|---|---|---|
| **Choropleth** | Rates, densities, ratios by area | Shaded polygons by class | Use **rates**, not raw totals (a big district looks dark simply because it is big); unequal areas mislead |
| **Proportional symbol** | Counts at points or areas | Circle size proportional to value | Overlap; scale by area, not diameter |
| **Dot density** | Counts | Each dot stands for a fixed quantity | Dot size and value must be stated |
| **Isoline (contour)** | A continuous surface | Lines of equal value (elevation, rainfall) | Needs enough sample points |
| **Dasymetric** | Population within meaningful zones | Redistributes counts inside habitable land | Needs ancillary data |
| **Flow** | Movements | Lines with width proportional to volume | Clutter |
| **Cartogram** | Any statistic | Areas distorted in proportion to value | Unfamiliar shapes |

### 2.2.4 Classifying data for a choropleth map

A choropleth cannot show a different shade for every value, so numeric data are grouped into classes (typically 4 to 7). The method chosen changes the story the map tells.

| Method | Rule | Good for | Weakness |
|---|---|---|---|
| **Equal interval** | Equal-width ranges | Data spread evenly; easy legend | Empty classes if data are skewed |
| **Quantile** | Same number of features per class | Ranking, comparison | Similar values may be split; very different values may be merged |
| **Natural breaks (Jenks)** | Minimises variance within classes | Finds natural gaps | Legend is hard to compare across maps |
| **Standard deviation** | Classes in steps from the mean | Shows departure from average | Needs roughly normal data |
| **Manual / defined** | Policy thresholds (for example poverty line) | Meaningful decisions | Subjective |

```python
# Classify literacy rates (%) of twelve districts by four methods and compare the class breaks.
import statistics as st
vals = sorted([52.1, 55.4, 57.0, 58.8, 60.2, 61.5, 63.9, 66.3, 70.5, 74.8, 80.1, 85.6])
k = 4
lo, hi = vals[0], vals[-1]

# equal interval
width = (hi - lo) / k
eq = [round(lo + width * i, 1) for i in range(1, k)]
# quantile: break at positions n*i/k
q = [round(vals[len(vals) * i // k - 1], 1) for i in range(1, k)]
# standard deviation: mean +/- 0.5 sd and +1 sd
m, s = st.mean(vals), st.pstdev(vals)
sd = [round(m - 0.5 * s, 1), round(m, 1), round(m + 0.5 * s, 1)]

def jenks(data, k):
    """Optimal k classes minimising within-class sum of squared deviations (dynamic programming)."""
    n = len(data)
    def cost(i, j):
        seg = data[i:j + 1]; mu = sum(seg) / len(seg)
        return sum((x - mu) ** 2 for x in seg)
    INF = float("inf")
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    cut = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for j in range(1, n + 1):
        for c in range(1, min(k, j) + 1):
            for i in range(c - 1, j):
                v = dp[i][c - 1] + cost(i, j - 1)
                if v < dp[j][c]:
                    dp[j][c], cut[j][c] = v, i
    br, j = [], n
    for c in range(k, 0, -1):
        i = cut[j][c]; br.append(data[i - 1] if i > 0 else None); j = i
    return [b for b in reversed(br) if b is not None]

print("equal interval breaks:", eq)
print("quantile breaks      :", q)
print("std deviation breaks :", sd)
print("natural (Jenks) upper limits of classes 1-3:", jenks(vals, k))
```
```output
equal interval breaks: [60.5, 68.8, 77.2]
quantile breaks      : [57.0, 61.5, 70.5]
std deviation breaks : [60.6, 65.5, 70.5]
natural (Jenks) upper limits of classes 1-3: [58.8, 66.3, 74.8]
```
::: caution Honest maps
The same data can look alarming or calm depending on the classes. Report the method, show the legend with exact limits, avoid red-green pairs (about one man in twelve has red-green colour-vision deficiency), and prefer **sequential** single-hue schemes for ordered data, **diverging** schemes for data with a meaningful midpoint, and **qualitative** schemes for categories.
:::
## 2.3 Map projection

### 2.3.1 Why projections are needed

The Earth is almost a sphere, a slightly flattened one, and no curved surface can be flattened without stretching, tearing or compressing it (peel an orange and try). A **map projection** is a mathematical rule that converts positions on the curved surface, given as latitude and longitude, to positions (x, y) on a plane. Every projection **distorts** at least one of four properties: **shape** (angles), **area**, **distance** and **direction**. Choosing a projection means choosing what to keep right.

Before projecting, the Earth itself needs a mathematical shape:

| Surface | Meaning |
|---|---|
| **Geoid** | The irregular surface of mean sea level extended under the continents; what "height above sea level" refers to. Bumpy by up to about 100 m |
| **Ellipsoid (spheroid)** | A smooth ellipse of revolution fitted to the geoid; defined by the semi-major axis a and flattening f. For WGS 84, a = 6,378,137 m and 1/f = 298.257223563; the polar radius is about 21 km shorter |
| **Sphere** | A good enough model for small-scale maps (radius about 6,371 km) |
| **Datum** | An ellipsoid **plus** its position and orientation relative to the real Earth. A local datum fits one region best; a global datum (WGS 84, used by GPS) fits the whole Earth |

Two receivers using different datums report different coordinates for the same spot, sometimes by hundreds of metres. Nepal's older maps are based on an **Everest-type ellipsoid** fitted to the region, while GPS reports **WGS 84**; data from the two must be *transformed*, not just overlaid. (The Survey Department publishes the transformation parameters; check the current ones.)

### 2.3.2 Geographic and projected coordinates

**Geographic coordinates** are **latitude** (angle north or south of the equator, 0 to 90) and **longitude** (angle east or west of the prime meridian, 0 to 180), in degrees. They are angles on a curved surface, so a degree of longitude shrinks with latitude: about 111.3 km at the equator, 98 km at Kathmandu's latitude (27.7 N), and zero at the poles. Because of this, you cannot measure distance or area directly in degrees.

**Projected coordinates** are (x, y) in metres on a plane, with a defined origin. They allow ordinary geometry: distances, areas and buffers in metres. A coordinate reference system (CRS) is named by a code (EPSG number), such as **EPSG:4326** (WGS 84 geographic), **EPSG:3857** (Web Mercator, used by web maps), **EPSG:32644** and **EPSG:32645** (WGS 84 / UTM zones 44N and 45N).

### 2.3.3 Families and properties

A projection is imagined as casting the globe's graticule onto a **developable surface** that can be unrolled flat: a **cylinder**, a **cone** or a **plane**. The surface can touch the globe (tangent) or cut through it (secant); lines of contact have no distortion.

```svgfig label="2.1" caption="The three projection families. A cylinder touches the globe along the equator, a cone along a parallel, and a plane at a point. Distortion is zero only where the surface touches (the standard line or point) and grows away from it."
f = Fig(680, 280)
for cx, title, note in ((115, "Cylindrical", "tangent at the equator"), (340, "Conic", "tangent along a parallel"), (565, "Azimuthal (planar)", "tangent at a point")):
    f.circle(cx, 125, 55, fill=BLUE, stroke=NAVY, label="")
    f.text(cx, 24, title, size=12, color=NAVY, bold=True)
    f.text(cx, 255, note, size=10, color=SLATE)
# cylinder: rectangle around the globe, equator touching
f.line(60, 70, 60, 180, color=AMBER, sw=2)
f.line(170, 70, 170, 180, color=AMBER, sw=2)
f.line(60, 70, 170, 70, color=AMBER, sw=2, dash=True)
f.line(60, 180, 170, 180, color=AMBER, sw=2, dash=True)
f.line(60, 125, 170, 125, color=RED, sw=2.2)
# cone: triangle apex above, touching along a parallel
f.line(340, 38, 285, 160, color=AMBER, sw=2)
f.line(340, 38, 395, 160, color=AMBER, sw=2)
f.line(285, 160, 395, 160, color=AMBER, sw=2, dash=True)
f.line(298, 130, 382, 130, color=RED, sw=2.2)
# plane: tangent at the north pole
f.line(485, 70, 645, 70, color=AMBER, sw=2)
f.circle(565, 70, 4, fill=RED, stroke=RED)
f.text(115, 205, "Mercator, UTM (transverse)", size=9.5, color=SLATE)
f.text(340, 205, "Lambert conformal conic, Albers", size=9.5, color=SLATE)
f.text(565, 205, "Stereographic, polar maps", size=9.5, color=SLATE)
```

Projections are also classified by what they **preserve**:

| Property preserved | Name | Distorts | Use |
|---|---|---|---|
| **Angles and local shapes** | **Conformal** (Mercator, transverse Mercator, Lambert conformal conic) | Area, especially far from the standard lines | Navigation, topographic and cadastral maps, web maps |
| **Area** | **Equal-area** (Albers, Lambert azimuthal equal-area, Mollweide) | Shape | Thematic maps that compare areas: population density, land use |
| **Distance** (along certain lines) | **Equidistant** | Shape and area | Distances from a centre, such as radio ranges |
| **Compromise** | Robinson, Winkel Tripel | A little of everything | World maps for display |

No flat map is both conformal and equal-area. Rule of thumb for an analyst: **measure area on an equal-area projection, distance on an equidistant or a local conformal one, and store data in a geographic CRS.**

### 2.3.4 The Mercator family

The **Mercator projection** (1569) puts the globe inside a cylinder tangent at the equator. For a sphere of radius R, longitude lambda and latitude phi (radians):

- x = R (lambda - lambda0)
- y = R ln tan(pi/4 + phi/2)

It is conformal, and a line of constant compass bearing is straight, which made it the sailor's map. But the **local scale factor is sec(phi) = 1/cos(phi)**, so areas are inflated by sec^2(phi): Greenland looks as large as Africa although Africa is about 14 times bigger. **Web Mercator** (EPSG:3857) uses the same formulas on a sphere with the WGS 84 radius and is cut off near 85 degrees north and south; it is excellent for browsing and poor for measuring.

The **Transverse Mercator** turns the cylinder through 90 degrees so that it touches along a **meridian** instead of the equator. Distortion is then small in a **narrow north-south strip** around that central meridian, which suits countries elongated north-south. The **Universal Transverse Mercator (UTM)** system divides the world between 80 S and 84 N into **60 zones**, each **6 degrees** wide, numbered from 1 starting at 180 W. The central meridian of zone n is **6n - 183** degrees. Each zone uses scale factor **k0 = 0.9996** on the central meridian, a **false easting of 500,000 m** (so that eastings are positive) and, in the southern hemisphere, a false northing of 10,000,000 m.

```svgfig label="2.2" caption="Nepal across UTM zones 44 and 45 (6-degree zones, central meridians 81 and 87) and the three 3-degree belts of the modified UTM used by the Survey Department (central meridians 81, 84 and 87)."
f = Fig(680, 250)
def X(lon):
    return 40 + (lon - 78) * 50
f.box(X(78), 70, 300, 38, "UTM zone 44  (78 E to 84 E)", fill=BLUE, stroke=NAVY, size=10.5)
f.box(X(84), 70, 300, 38, "UTM zone 45  (84 E to 90 E)", fill=MINT, stroke=TEAL, size=10.5)
f.box(X(79.5), 138, 150, 34, "MUTM 81 E belt", fill=SAND, stroke=AMBER, size=10)
f.box(X(82.5), 138, 150, 34, "MUTM 84 E belt", fill=SAND, stroke=AMBER, size=10)
f.box(X(85.5), 138, 150, 34, "MUTM 87 E belt", fill=SAND, stroke=AMBER, size=10)
f.line(X(80.06), 195, X(88.2), 195, color=RED, sw=3)
f.text((X(80.06) + X(88.2)) / 2, 218, "Nepal: about 80.06 E to 88.2 E", size=10.5, color=RED, bold=True)
for lon in (78, 81, 84, 87, 90):
    f.line(X(lon), 52, X(lon), 62, color=SLATE)
    f.text(X(lon), 44, "%d E" % lon, size=10, color=SLATE)
f.text(340, 20, "Central meridian of each belt marks where scale is smallest", size=9.5, color=SLATE)
```

**Nepal's grid.** Nepal spans about 800 km east-west and only 150 to 240 km north-south, so one 6-degree UTM zone cannot cover it with small distortion (the country straddles zones 44 and 45). The Survey Department therefore uses a **Modified UTM (MUTM)** with three belts centred on **81, 84 and 87 degrees east**, a scale factor of **0.9999** on each central meridian, false easting 500,000 m and false northing 0, referred to a local Everest-type datum for traditional topographic maps. GPS-based projects often use WGS 84 / UTM 44N or 45N instead. *Always read the CRS in the layer's metadata*: mixing MUTM and UTM data without transformation shifts features by hundreds of metres.

### 2.3.5 Distortion and choice of projection

For a transverse Mercator the scale factor at distance x (km) east or west of the central meridian is approximately k = k0 (1 + x^2 / (2 R^2)) with R = 6,371 km. At the central meridian of UTM, k = 0.9996 (a 0.04 percent shrink); it equals 1 about 180 km from the centre (the secant lines) and reaches about 1.0010 at the edge of a zone on the equator, meaning a 1 km measurement is 1 m too long there. For most work this is negligible, but for surveying it is not.

Choosing a projection: for **Nepal-wide thematic maps** use an equal-area or a conic projection; for **ward-level engineering** use MUTM or UTM; for **web display** use Web Mercator, but compute lengths and areas after reprojecting to a local metric CRS; for **storage and exchange** keep WGS 84 geographic (EPSG:4326), as GeoJSON requires.

```python
# Mercator, haversine and a UTM forward projection (Snyder's series, WGS 84), coded from the formulas.
import math
A, F = 6378137.0, 1 / 298.257223563
E2 = F * (2 - F); EP2 = E2 / (1 - E2)

def mercator(lon, lat, R=6378137.0):
    x = R * math.radians(lon)
    y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y

def haversine(lat1, lon1, lat2, lon2, R=6371.0088):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def utm(lon, lat, k0=0.9996, lon0=None):
    zone = int((lon + 180) // 6) + 1
    lon0 = math.radians(6 * zone - 183) if lon0 is None else math.radians(lon0)
    p, l = math.radians(lat), math.radians(lon)
    N = A / math.sqrt(1 - E2 * math.sin(p) ** 2)
    T, C, Aa = math.tan(p) ** 2, EP2 * math.cos(p) ** 2, math.cos(p) * (l - lon0)
    M = A * ((1 - E2 / 4 - 3 * E2**2 / 64 - 5 * E2**3 / 256) * p - (3 * E2 / 8 + 3 * E2**2 / 32 + 45 * E2**3 / 1024) * math.sin(2 * p)
             + (15 * E2**2 / 256 + 45 * E2**3 / 1024) * math.sin(4 * p) - (35 * E2**3 / 3072) * math.sin(6 * p))
    x = k0 * N * (Aa + (1 - T + C) * Aa**3 / 6 + (5 - 18 * T + T**2 + 72 * C - 58 * EP2) * Aa**5 / 120) + 500000
    y = k0 * (M + N * math.tan(p) * (Aa**2 / 2 + (5 - T + 9 * C + 4 * C**2) * Aa**4 / 24 + (61 - 58 * T + T**2 + 600 * C - 330 * EP2) * Aa**6 / 720))
    return zone, x, y

ktm = (27.7172, 85.3240); pkr = (28.2096, 83.9856)
print("Kathmandu Mercator x,y (km): %.1f, %.1f" % tuple(v / 1000 for v in mercator(ktm[1], ktm[0])))
print("great-circle Kathmandu-Pokhara: %.1f km" % haversine(*ktm, *pkr))
print("Mercator scale factor sec(lat) at 27.7 N: %.3f -> area inflated x%.2f" % (1 / math.cos(math.radians(27.7)), 1 / math.cos(math.radians(27.7)) ** 2))
for name, (la, lo) in (("Kathmandu", ktm), ("Pokhara", pkr)):
    z, x, y = utm(lo, la)
    print("%-9s UTM zone %dN  E %.0f  N %.0f" % (name, z, x, y))
# distance on the plane using UTM (both in zone 45 here) against the great-circle value
z1, x1, y1 = utm(ktm[1], ktm[0], lon0=87)
z2, x2, y2 = utm(pkr[1], pkr[0], lon0=87)
print("plane distance in zone-45 UTM: %.1f km" % (math.hypot(x2 - x1, y2 - y1) / 1000))
print("one degree of longitude at 27.7 N = %.1f km, at the equator = %.1f km" % (haversine(27.7, 0, 27.7, 1), haversine(0, 0, 0, 1)))
for xkm in (0, 180, 333):
    print("scale factor %3d km from the central meridian: %.5f" % (xkm, 0.9996 * (1 + (xkm / 6371.0) ** 2 / 2)))
```
```output
Kathmandu Mercator x,y (km): 9498.2, 3213.4
great-circle Kathmandu-Pokhara: 142.4 km
Mercator scale factor sec(lat) at 27.7 N: 1.129 -> area inflated x1.28
Kathmandu UTM zone 45N  E 334770  N 3067000
Pokhara   UTM zone 44N  E 793056  N 3124033
plane distance in zone-45 UTM: 142.6 km
one degree of longitude at 27.7 N = 98.5 km, at the equator = 111.2 km
scale factor   0 km from the central meridian: 0.99960
scale factor 180 km from the central meridian: 1.00000
scale factor 333 km from the central meridian: 1.00097
```
Read the output carefully. Kathmandu (85.3 E) is in zone 45 with an easting of about 334,770 m (west of the 87 E meridian). Pokhara (83.99 E) lies just west of the 84 E zone boundary, so it is in **zone 44**, and its easting of about 793,000 m is far outside the usual 166,000 to 834,000 m range of a zone's useful width. The two cities cannot be compared by their raw eastings and northings. The program therefore recomputes both in zone 45 (forcing the central meridian to 87 E) before taking the plane distance, which agrees with the great-circle distance to about 0.2 km. This is exactly the problem that makes a single UTM zone awkward for a country as long as Nepal.

::: example Why a degree is not a distance
At Kathmandu one degree of latitude is about 111 km but one degree of longitude is only about 98 km. A "0.01 degree buffer" around a point is therefore not a circle but an ellipse, and an "area" computed from degrees is meaningless. Reproject to a metric CRS (UTM or MUTM) before buffering or measuring.
:::

### 2.3.6 Reprojection and good practice

- **Define** a CRS when a layer has none (using the metadata) and **transform** (reproject) when you need another. Defining does not move coordinates; transforming does.
- Set the **project CRS** of a GIS session deliberately; most packages reproject layers on the fly for display, but analysis tools often assume one CRS.
- Store a copy of the original data and note every transformation (lineage).
- If layers do not overlap, suspect a CRS problem first: check units (degrees against metres) and the datum.
- Always put the **projection and datum** on the finished map.

## 2.4 Summary and exercises

A map is a scaled, selective, symbolised representation; scale is given as a representative fraction, a verbal statement or a bar scale (only the bar survives enlargement). Mapping is a process of choosing purpose, data, projection, generalisation, classification, symbols and layout. Visual variables are chosen by level of measurement; choropleth maps need rates and a stated classification method. Projections flatten an ellipsoid on a datum and always distort shape, area, distance or direction. Families are cylindrical, conic and azimuthal; properties are conformal, equal-area, equidistant. UTM has 60 zones of 6 degrees with k0 = 0.9996; Nepal uses a modified UTM with 81, 84 and 87 degree belts.

1. Define a map. How does a map differ from the database of a GIS?
2. Name the three ways of expressing scale and say which survives photocopying. Why?
3. A distance of 7.4 cm is measured on a 1:50,000 map. What is the ground distance in km?
4. A road is 3 km long. How long is it on a 1:25,000 map?
5. A lake covers 12 cm2 on a 1:25,000 map. Find its ground area in km2.
6. Explain generalisation with three operations, and why a 6 m wide road is drawn wider than scale.
7. List the standard elements of a finished map.
8. Compare choropleth and proportional-symbol maps. Why must a choropleth use rates?
9. Compare equal-interval, quantile and natural-breaks classification, with one weakness each.
10. Distinguish the geoid, ellipsoid and datum. Why do local datums exist?
11. Distinguish geographic and projected coordinates. Why can a buffer not be computed in degrees?
12. Explain the three projection families and the properties conformal, equal-area and equidistant. Give a use for each.
13. State the UTM parameters. Find the zone and central meridian for longitude 85.3 E.
14. Why is Web Mercator unsuitable for measuring areas? At latitude 60 degrees by what factor is the scale stretched, and areas?
15. Why does Nepal use a modified UTM? State its belts and scale factor.

**Answers to the numerical items.** (3) 7.4 x 50,000 = 370,000 cm = **3.7 km**. (4) 3,000 m = 300,000 cm; 300,000 / 25,000 = **12 cm**. (5) 1 cm = 250 m, so 1 cm2 = 62,500 m2 = 0.0625 km2; 12 cm2 = **0.75 km2**. (13) Zone = int((85.3 + 180) / 6) + 1 = int(44.2) + 1 = **45**; central meridian 6 x 45 - 183 = **87 E**. (14) Scale factor sec 60 = **2**, area factor sec^2 60 = **4**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the three ways of expressing map scale.**

The representative fraction (for example 1:50,000) says one map unit equals 50,000 ground units in the same unit, so it is unitless. The verbal scale states it in words ("1 cm represents 500 m"). The graphic or bar scale is a line marked with ground distances. Only the bar scale remains correct when a map is enlarged, reduced or displayed on screens of different sizes, so a printed map should always carry one. Ground distance = map distance x scale denominator.

**Q2 (5 marks). What is a map projection? Why does every projection distort?**

A map projection is a mathematical rule that converts latitude and longitude on the curved Earth to x, y on a plane. A curved surface that is not developable, such as a sphere or an ellipsoid, cannot be flattened without stretching or compressing parts of it. Therefore every projection distorts at least one of shape, area, distance and direction; the designer decides which to preserve. No projection is both conformal and equal-area.

**Q3 (10 marks). Describe the UTM system and the coordinate system used in Nepal.**

UTM divides the Earth between 80 S and 84 N into 60 zones, each 6 degrees of longitude wide and numbered from 1 at 180 W; the central meridian of zone n is 6n - 183. It uses a transverse Mercator projection on the WGS 84 ellipsoid with scale factor 0.9996 on the central meridian, a false easting of 500,000 m, and a false northing of 10,000,000 m in the southern hemisphere. Scale is exact on two lines about 180 km from the centre and grows to about 1.0010 at the zone edge. Coordinates are in metres, so distances and areas can be computed with plane geometry.

Nepal extends from about 80 to 88 E and is long east-west, so it falls in zones 44 and 45. To reduce distortion the Survey Department uses a modified UTM with three 3-degree belts centred on 81, 84 and 87 E, scale factor 0.9999, false easting 500,000 m and false northing 0, on a local datum for traditional topographic maps. GPS data are in WGS 84, so layers must be transformed before they are combined, otherwise features shift by tens to hundreds of metres. The CRS must always be read from the metadata and printed on the map.
