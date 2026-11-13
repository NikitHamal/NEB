---
subject: Geographical Information System
grade: BCA Semester 8 (Elective III)
unit: 5
title: GIS Data Modeling and Creating Maps
hours: 9
area: BCA 453 · Geographical Information System · Unit 5
---

The last unit applies GIS to the physical landscape and then to the final product. **Surface modelling** turns scattered elevation samples into a continuous surface and derives slope, aspect, shading, contours, profiles, volumes and visibility. **Hydrology modelling** uses the surface to find how water flows, where streams form and which area drains to a point: essential in a mountainous country with monsoon floods and landslides. Finally, **designing and printing the map** puts the result in front of a reader, and the unit closes with a complete basic GIS project of the kind the syllabus asks you to build in the laboratory.

::: key What this unit gives you
- Surface models (DEM, DSM, DTM, TIN, contours), interpolation (nearest, IDW with leave-one-out validation, spline and kriging explained), and derivatives: slope, aspect (Horn's method), hillshade, profile, cut-and-fill volume, line-of-sight.
- Hydrology: sink filling, D8 flow direction, flow accumulation, stream extraction and order, watershed delineation, with executed code on a small DEM.
- Map design and printing: layout, the elements, classification, colour, lettering, scale and resolution calculations, export formats and a design checklist.
- A step-by-step basic GIS project (the laboratory work) with a data list, workflow and report outline.
:::

## 5.1 Surface modelling

### 5.1.1 Representing surfaces

A **surface** has a value (z) at every (x, y): elevation, rainfall, temperature, population density, noise. It is stored as a **raster** (a grid of cell values), a **TIN** (triangles through sample points), or **contours** (lines of equal value). For terrain the products have names:

| Term | Meaning |
|---|---|
| **DEM** (digital elevation model) | General term for a gridded elevation surface |
| **DTM** (digital terrain model) | Bare-earth surface, with buildings and trees removed |
| **DSM** (digital surface model) | Top of everything: canopy, roofs |
| **Contour** | Line joining points of equal elevation; the **contour interval** is the vertical spacing; closely spaced lines mean steep ground |
| **Spot height** | A single measured elevation |

Free global DEMs are widely used in Nepal: **SRTM** (30 m), **ASTER GDEM** (30 m) and **Copernicus DEM** (30 m). Local surveys with total stations, GNSS, drones or **LiDAR** give finer surfaces. Accuracy in steep Himalayan terrain is worse than on plains, with vertical errors of several metres to tens of metres, and radar DEMs can show errors in forest and snow, so important engineering work needs a surveyed DEM.

### 5.1.2 Interpolation

**Interpolation** estimates the surface value at unsampled locations from samples. It rests on Tobler's law: nearby points are more alike.

| Method | Idea | Properties |
|---|---|---|
| **Nearest neighbour** (Thiessen) | Take the value of the closest sample | Stepped surface; keeps values |
| **Inverse distance weighting (IDW)** | Weighted average, weights 1 / d^p | Never exceeds sample range; creates "bull's eyes"; power p (often 2) controls locality |
| **Trend surface** | Fit a smooth polynomial to all points | Shows regional trend; poor locally |
| **Spline** | Minimum-curvature smooth surface through points | Smooth, can overshoot beyond the sample range |
| **Kriging** | Weights from a fitted **semivariogram** (how similarity falls with distance), giving also the estimation variance | Statistically optimal under assumptions; needs enough data and modelling |
| **TIN / linear** | Plane through the three surrounding nodes | Exact at nodes; no smoothing |

IDW estimates z at a point as z = sum(w_i z_i) / sum(w_i) with w_i = 1 / d_i^p. A higher p gives nearer points more influence. No method is best everywhere; compare them by **cross-validation**: remove one sample at a time, predict it from the rest and compute the RMSE of the errors.

```python
# IDW interpolation and leave-one-out cross-validation for the power parameter.
import math
rain = [(10, 10, 1800), (80, 20, 2100), (50, 55, 2600), (15, 80, 1500), (85, 85, 2900), (40, 20, 2000), (70, 60, 2700), (30, 55, 1900)]   # x, y (km), annual rainfall (mm)

def idw(x, y, pts, p):
    num = den = 0.0
    for px, py, z in pts:
        d = math.hypot(x - px, y - py)
        if d == 0: return z
        w = 1 / d ** p; num += w * z; den += w
    return num / den

print("estimate at (50, 40):", {p: round(idw(50, 40, rain, p)) for p in (1, 2, 3)})
for p in (1, 2, 3, 4):
    errs = []
    for i, (x, y, z) in enumerate(rain):
        rest = rain[:i] + rain[i + 1:]
        errs.append(idw(x, y, rest, p) - z)
    rmse = math.sqrt(sum(e * e for e in errs) / len(errs))
    print("power %d: leave-one-out RMSE %.0f mm" % (p, rmse))
```
```output
estimate at (50, 40): {1: 2243, 2: 2313, 3: 2382}
power 1: leave-one-out RMSE 460 mm
power 2: leave-one-out RMSE 400 mm
power 3: leave-one-out RMSE 358 mm
power 4: leave-one-out RMSE 335 mm
```
### 5.1.3 Slope, aspect, hillshade

Neighbourhood operations on a DEM give the common **derived surfaces**:

- **Slope** is the steepness: the angle (or percent, 100 x rise / run) of the steepest descent. It matters for landslide risk, road cost, farming terraces and solar panels.
- **Aspect** is the compass direction the slope faces (0 to 360 degrees, clockwise from north); it controls sunshine, snow melt and crop choice.
- **Hillshade** simulates sunlight from a chosen azimuth and altitude (default 315 degrees, 45 degrees) to give a 3-D look to a flat map.
- **Curvature** says whether the surface is convex (ridge) or concave (valley).

**Horn's method** (used by ArcGIS and QGIS) estimates the gradient at a cell from the eight neighbours, weighting the nearer ones twice. With neighbours labelled a b c / d e f / g h i (row by row) and cell size s:

- dz/dx = ((c + 2f + i) - (a + 2d + g)) / (8 s)
- dz/dy = ((a + 2b + c) - (g + 2h + i)) / (8 s)  (north is positive, rows run north to south)
- slope = arctan(sqrt((dz/dx)^2 + (dz/dy)^2))

```python
# Slope, aspect and hillshade at the centre of a 3x3 window (Horn's method), 30 m cells.
import numpy as np
z = np.array([[1260, 1255, 1250],
              [1268, 1262, 1257],
              [1275, 1270, 1264]], dtype=float)                # rows run north (top) to south (bottom)
s = 30.0
a, b, c, d, e, f, g, h, i = z.ravel()
dzdx = ((c + 2 * f + i) - (a + 2 * d + g)) / (8 * s)           # east is +x
dzdy = ((a + 2 * b + c) - (g + 2 * h + i)) / (8 * s)           # north is +y
slope = np.degrees(np.arctan(np.hypot(dzdx, dzdy)))
aspect = (np.degrees(np.arctan2(-dzdx, -dzdy)) + 360) % 360    # compass bearing of the downhill direction
points = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
facing = points[int(((aspect + 22.5) % 360) // 45)]
az, alt = np.radians(315), np.radians(45)                       # sun from the north-west, 45 degrees up
sl, asp = np.radians(slope), np.radians(aspect)
hill = 255 * (np.cos(alt) * np.cos(sl) + np.sin(alt) * np.sin(sl) * np.cos(az - asp))
print("dz/dx %.3f, dz/dy %.3f -> slope %.1f deg (%.0f %%), aspect %.0f deg (%s-facing), hillshade %.0f / 255" %
      (dzdx, dzdy, slope, 100 * np.tan(np.radians(slope)), aspect, facing, max(hill, 0)))
```
```output
dz/dx -0.179, dz/dy -0.246 -> slope 16.9 deg (30 %), aspect 36 deg (north-east-facing), hillshade 181 / 255
```
### 5.1.4 Contours, profiles, volumes and visibility

- **Contours** are drawn through points of equal height by interpolating along cell edges or TIN triangles. An **index contour** (every fifth line) is drawn thicker and labelled. **Contour interval** is chosen by scale and relief (20 m on a 1:25,000 map of hills).
- A **profile** (cross-section) plots elevation against distance along a line: used for road, canal and power-line alignment, and for checking line of sight.
- **Volume** between a surface and a reference level is the sum of cell area x height. **Cut-and-fill** compares the ground with a design platform: material above the platform is *cut*, material below it is *fill*; a good design balances them to avoid hauling soil in or out.
- **Viewshed** analysis finds which cells are visible from an observer point (watchtower, mobile-phone mast, hotel) by testing the **line of sight** to each cell: a cell is hidden if any cell between observer and target rises above the sight line. Tools allow for observer height and the Earth's curvature.

```python
# Cut-and-fill volume for a building platform, and line of sight along a terrain profile.
import numpy as np
cell = 10.0                                                    # 10 m cells => 100 m2 each
dem = np.array([[1203, 1205, 1208, 1212],
                [1202, 1204, 1206, 1210],
                [1200, 1202, 1204, 1207],
                [1198, 1200, 1202, 1205]], dtype=float)
platform = 1204.0
diff = dem - platform                                          # positive = above platform = cut
cut = diff[diff > 0].sum() * cell * cell
fill = -diff[diff < 0].sum() * cell * cell
print("cut %.0f m3, fill %.0f m3, net %+.0f m3 (positive = surplus soil to remove)" % (cut, fill, cut - fill))
for lvl in (1203, 1204, 1205):                                # search for the level that balances cut and fill
    d = dem - lvl
    print("platform %d m: cut %.0f, fill %.0f" % (lvl, d[d > 0].sum() * 100, -d[d < 0].sum() * 100))

# line of sight along a profile (distance m, ground height m); observer on a 12 m mast at the first point
dist = np.array([0, 100, 200, 300, 400, 500, 600, 700]); h = np.array([1500, 1510, 1535, 1520, 1500, 1545, 1540, 1480], dtype=float)
eye = h[0] + 12
visible = []
max_slope = -np.inf
for k in range(1, len(dist)):
    sl = (h[k] - eye) / dist[k]                                # angle (as gradient) from the eye to the ground at k
    visible.append(bool(sl >= max_slope))
    max_slope = max(max_slope, sl)
print("visible from the mast (distances 100..700 m):", visible)
```
```output
cut 2500 m3, fill 2100 m3, net +400 m3 (positive = surplus soil to remove)
platform 1203 m: cut 3400, fill 1400
platform 1204 m: cut 2500, fill 2100
platform 1205 m: cut 1800, fill 3000
visible from the mast (distances 100..700 m): [True, True, False, False, False, False, False]
```
## 5.2 Hydrology modelling

### 5.2.1 Why model water with a DEM?

Water runs downhill, so a DEM contains almost everything needed to predict **where water goes**: which cells drain into which, where flow concentrates into streams, and which area feeds a given point. The results give **catchment (watershed) boundaries** for hydropower and water supply intakes, **drainage networks** for road culverts, **flood-prone valleys** and **erosion** hot spots. In Nepal's steep, monsoon-fed rivers this is routine work for hydropower, irrigation, bridge and road design, and landslide and flood hazard maps. Hydrology models from a DEM are first estimates; they miss culverts, canals, and underground flow, and need calibration with gauged data from the Department of Hydrology and Meteorology.

### 5.2.2 The D8 workflow

The classical workflow has five steps, each producing a raster:

1. **Fill sinks.** A **sink** (pit) is a cell lower than all its neighbours with no outlet, usually a data error. Raise it to the level of its lowest neighbour (iteratively) so that water can leave. Natural depressions such as lakes are kept by hand.
2. **Flow direction (D8).** Each cell drains to **one** of its **eight** neighbours, the one with the **steepest descent**, where drop = (z cell - z neighbour) / distance, with distance 1 cell for rook moves and 1.414 cells for diagonals. The result is a direction code (1, 2, 4, 8, 16, 32, 64, 128 in the Esri convention).
3. **Flow accumulation.** Each cell's value is the **number of upstream cells** that drain through it (including itself, or excluding it, depending on software). Multiply by cell area to get the **contributing area**.
4. **Stream extraction.** Cells whose accumulation exceeds a **threshold** (for example 1,000 cells or a contributing area of 1 km2) are **streams**. The threshold controls drainage density: low gives a dense network. Streams are ordered by **Strahler order**: headwater streams are order 1; when two streams of order n meet, the result is n + 1; a lower order joining a higher one does not change it.
5. **Watershed delineation.** Choose an **outlet (pour point)** on a stream; the watershed is the set of all cells whose flow path ends at that point.

D8 sends all water from a cell to a single neighbour, which makes parallel straight flow on planar slopes. Multiple-flow-direction methods (**D-infinity**, **MFD**) split flow among several lower neighbours and give more natural results on hillslopes, while D8 remains the standard for streams and watersheds.

```svgfig label="5.1" caption="D8 flow routing on a 5 by 5 window. Left: elevations and the steepest-descent arrow from each cell. Right: flow accumulation (cells draining through each cell); shaded cells exceed the stream threshold."
f = Fig(680, 270)
elev = [[50, 48, 46, 48, 50], [45, 42, 40, 42, 45], [40, 36, 34, 36, 40], [34, 30, 28, 30, 34], [30, 26, 22, 26, 30]]
down = {}
for r in range(5):
    for c in range(5):
        best, tgt = 0.0, None
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                a, b = r + dr, c + dc
                if (dr or dc) and 0 <= a < 5 and 0 <= b < 5:
                    drop = (elev[r][c] - elev[a][b]) / (1.414 if dr and dc else 1.0)
                    if drop > best:
                        best, tgt = drop, (a, b)
        down[(r, c)] = tgt
acc = [[1] * 5 for _ in range(5)]
for cell in sorted(down, key=lambda k: -elev[k[0]][k[1]]):
    if down[cell]:
        acc[down[cell][0]][down[cell][1]] += acc[cell[0]][cell[1]]
f.text(160, 16, "Elevation (m) and flow arrows", size=11, color=NAVY, bold=True)
f.text(510, 16, "Flow accumulation (cells)", size=11, color=NAVY, bold=True)
for r in range(5):
    for c in range(5):
        f.box(40 + c * 50, 28 + r * 46, 50, 46, str(elev[r][c]), fill=SOFT, stroke=SLATE, size=10)
        stream = acc[r][c] >= 10
        f.box(390 + c * 50, 28 + r * 46, 50, 46, str(acc[r][c]), fill=("#bfdbfe" if stream else SOFT), stroke=(NAVY if stream else SLATE), size=10, bold=stream)
        if down[(r, c)]:
            a, b = down[(r, c)]
            f.arrow([(65 + c * 50 + (c - c) * 0, 51 + r * 46 + 9), (65 + c * 50 + (b - c) * 17, 51 + r * 46 + 9 + (a - r) * 15)], color=AMBER, sw=1.4)
f.text(160, 260, "outlet: the lowest cell, bottom of the middle column", size=9.5, color=SLATE)
f.text(510, 260, "threshold 10 cells marks the stream (shaded)", size=9.5, color=SLATE)
```

```python
# D8 hydrology on a 7x7 DEM with two valleys: flow direction, accumulation, streams and watersheds.
import numpy as np
n = 7
r, c = np.indices((n, n))
z = 60.0 - 6 * r + 5 * np.minimum(abs(c - 1), abs(c - 5))              # valleys at columns 1 and 5, ridge at column 3
nbrs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
down = {}                                                              # cell -> receiving cell (None = outlet)
for i in range(n):
    for j in range(n):
        best, tgt = 0.0, None
        for di, dj in nbrs:
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < n:
                drop = (z[i, j] - z[a, b]) / (2 ** .5 if di and dj else 1)
                if drop > best: best, tgt = drop, (a, b)
        down[(i, j)] = tgt
acc = np.ones((n, n), dtype=int)
for cell in sorted(down, key=lambda k: -z[k]):                         # process high cells first
    if down[cell]: acc[down[cell]] += acc[cell]
print("flow accumulation:"); print(acc)
stream = acc >= 8
print("stream cells (accumulation >= 8):", int(stream.sum()), "->", sorted(tuple(int(v) for v in k) for k in zip(*np.nonzero(stream)))[:8], "...")
def outlet(cell):
    while down[cell]: cell = down[cell]
    return cell
ws = {}
for cell in down: ws.setdefault(outlet(cell), []).append(cell)
for o in sorted(ws): print("watershed draining to outlet %s: %d cells = %.1f ha at 30 m cells" % (tuple(int(v) for v in o), len(ws[o]), len(ws[o]) * 0.09))
big = max(acc.ravel())
print("largest accumulation %d cells = %.2f km2 contributing area" % (big, big * 900 / 1e6))
```
```output
flow accumulation:
[[ 1  1  1  1  1  1  1]
 [ 1  4  2  1  1  4  1]
 [ 1  8  2  1  1  7  1]
 [ 1 12  2  1  1 10  1]
 [ 1 16  2  1  1 13  1]
 [ 1 20  2  1  1 16  1]
 [ 1 28  3  1  1 21  1]]
stream cells (accumulation >= 8): 9 -> [(2, 1), (3, 1), (3, 5), (4, 1), (4, 5), (5, 1), (5, 5), (6, 1)] ...
watershed draining to outlet (6, 1): 28 cells = 2.5 ha at 30 m cells
watershed draining to outlet (6, 5): 21 cells = 1.9 ha at 30 m cells
largest accumulation 28 cells = 0.03 km2 contributing area
```
### 5.2.3 Other hydrology products

- **Stream length and gradient** (a long profile), **drainage density** (stream length per area), and **stream power** (a rough indicator of erosive power: contributing area x slope).
- **Topographic Wetness Index** (TWI) = ln(upslope contributing area per unit width / tan slope) highlights cells that tend to be wet, used for landslide and soil moisture maps.
- **Flood inundation**: simple "bathtub" mapping marks all cells below a flood level connected to the river; **HAND** (height above nearest drainage) refines this; hydraulic models (HEC-RAS) route actual discharge. Satellite radar after a flood gives the observed extent.
- **Runoff** by the **SCS curve number** method combines rainfall, land cover and soil group into a runoff depth for each cell.

::: caution Limits of the DEM
A 30 m DEM cannot see a 5 m wide culvert, a terrace wall or a road embankment; flat river plains (the Terai) give uncertain flow directions; and tall forests or snow bias radar DEMs. Always compare the extracted stream network with imagery and local knowledge before using it.
:::

## 5.3 Designing and printing the map

### 5.3.1 Layout and elements

A clear map is *designed*. The reader should see the **subject first**, then the supporting information, in this **visual hierarchy**: title and main map, then legend and scale bar, then credits and notes. A layout (page composition) contains:

| Element | Rule |
|---|---|
| **Title** | States what, where and when ("Flood-prone schools in Ward 5, 2025"), the largest text |
| **Main map (data frame)** | Occupies most of the page; features centred; enough margin |
| **Legend** | Only the symbols used, in plain words, with units and class limits |
| **Scale bar** (and RF) | Graphic bar in round numbers (0, 1, 2 km); never only a ratio on a printed map that may be rescaled |
| **North arrow** | Needed when north is not up or the map is a plan; simple, not decorative |
| **Graticule or grid** | Labelled coordinates with the CRS |
| **Inset (locator) map** | Shows where the area lies in the country |
| **Source, date, author, projection** | Small text at the foot |
| **Border and neatline** | Frames the map; keep margins even |

```svgfig label="5.2" caption="A standard map layout on landscape paper: the main map takes the most space, supporting elements sit around it in a consistent order."
f = Fig(680, 290)
f.box(20, 20, 640, 250, "", fill=SOFT, stroke=SLATE)
f.box(35, 30, 440, 36, "TITLE: what, where, when", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(35, 76, 440, 170, "MAIN MAP\n(data frame, graticule labels)", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(490, 30, 160, 70, "LOCATOR\nINSET MAP", fill=MINT, stroke=TEAL, size=10)
f.box(490, 112, 160, 78, "LEGEND\nsymbols and class limits", fill=SOFT, stroke=SLATE, size=10)
f.box(490, 202, 160, 26, "North arrow", fill=SOFT, stroke=SLATE, size=10)
f.box(35, 252, 160, 14, "", fill=SOFT, stroke=SLATE)
f.text(115, 262, "Scale bar 0 - 1 - 2 km", size=8.5, color=SLATE)
f.text(560, 245, "Source, date, CRS, author", size=8.5, color=SLATE)
```

### 5.3.2 Cartographic design principles

- **Purpose and audience first.** A map for a ward meeting needs bigger lettering and fewer layers than one for engineers.
- **Contrast and figure-ground.** The theme (flood zones) should stand out; the base (roads, rivers, labels) should recede in light greys and thin lines.
- **Hierarchy through the visual variables.** Larger and darker means more important or greater.
- **Simplicity.** Show only what supports the message; generalise; avoid clutter and decorative effects.
- **Colour.** Use sequential single-hue schemes for ordered data, diverging for data with a midpoint (change in population), qualitative for categories (land use). Do not use red and green alone; test in greyscale if the map may be photocopied (ColorBrewer gives safe schemes). Blue for water and green for vegetation are conventions worth keeping.
- **Typography.** One or two typefaces; labels for rivers italic blue and curved along the line; place names horizontal, not overlapping; minimum text size about 6 to 7 points in print.
- **Balance and alignment.** Keep elements aligned and white space even.
- **Honesty.** Show scale, projection and source, report classification, do not truncate scales to exaggerate, and label estimated or modelled data as such.

### 5.3.3 Printing and exporting

Printing multiplies the choices: **paper size** (A4 is 210 x 297 mm, A3 is 297 x 420 mm, A1 is 594 x 841 mm), **scale**, **resolution**, **colour model** and **file format**.

- **Resolution**: rasters need **300 dpi** (dots per inch) for a good printed image, 150 dpi for a draft; a 12-inch wide print at 300 dpi needs 3,600 pixels across. Screen maps need only 72 to 96 dpi.
- **Colour model**: screens use **RGB**, printing presses use **CMYK**, so saturated screen blues and greens print duller; proof a test print.
- **Vector formats** (PDF, SVG, EPS) keep text and lines sharp at any size and are best for printing and editing; **raster formats** (PNG for sharp graphics, JPEG for photographs and imagery, TIFF/GeoTIFF for geo-referenced images) are for the web and for embedding.
- **Fonts and layers**: embed fonts in PDF; check that the **scale bar updates** when the map extent changes; export a **GeoPDF** or **web map** when readers need to measure.
- **Web maps** swap fixed scale for zoom: use tiles, pop-ups for attributes and a basemap with attribution.

```python
# Layout arithmetic: choose a scale for the page, build a scale bar, check text and pixel sizes.
extent_w_km, extent_h_km = 12.0, 8.0                    # ground area to map (km)
page_w_mm, page_h_mm = 297, 210                          # A4 landscape
frame_w, frame_h = page_w_mm - 2 * 15 - 90, page_h_mm - 2 * 15 - 40   # map frame after margins, legend column and title
need = max(extent_w_km * 1e6 / frame_w, extent_h_km * 1e6 / frame_h)     # denominator (km -> mm) so both sides fit
nice = [5000, 10000, 20000, 25000, 50000, 75000, 100000, 150000, 250000]
scale = next(s for s in nice if s >= need)
print("frame %d x %d mm; the minimum denominator is %.0f -> use 1:%d" % (frame_w, frame_h, need, scale))
print("map size on paper: %.0f x %.0f mm" % (extent_w_km * 1e6 / scale, extent_h_km * 1e6 / scale))
bar_km = 2.0
print("a %.0f km scale bar is %.1f mm long" % (bar_km, bar_km * 1e6 / scale))
cell_m, dpi = 30, 300
print("a %d m raster cell is %.2f mm on paper at 1:%d, i.e. %.1f printer dots across at %d dpi" % (cell_m, cell_m * 1000 / scale, scale, cell_m * 1000 / scale / 25.4 * dpi, dpi))
print("pixels needed for the whole frame at %d dpi: %d x %d" % (dpi, round(frame_w / 25.4 * dpi), round(frame_h / 25.4 * dpi)))
print("line width 0.25 mm stands for %.1f m on the ground at this scale" % (0.25 * scale / 1000))
```
```output
frame 177 x 140 mm; the minimum denominator is 67797 -> use 1:75000
map size on paper: 160 x 107 mm
a 2 km scale bar is 26.7 mm long
a 30 m raster cell is 0.40 mm on paper at 1:75000, i.e. 4.7 printer dots across at 300 dpi
pixels needed for the whole frame at 300 dpi: 2091 x 1654
line width 0.25 mm stands for 18.8 m on the ground at this scale
```
## 5.4 Laboratory work: a basic GIS project

The course asks each student to build **a basic GIS project** using the concepts of the five units. The plan below is a complete model project; replace the study area and theme to suit your own, but keep the stages. It is designed to run on free software (**QGIS**, with **OpenStreetMap**, SRTM or Copernicus DEM, and census or school-register tables) on an ordinary laptop.

**Title:** *School access and flood exposure in a ward (municipality of your choice).*

**Questions.** (1) Where are the schools and how many children live within 1 km of each? (2) Which schools lie inside the flood-prone zone? (3) Where would a new school give the largest improvement in access, outside the flood zone?

| Stage | What you do | Unit |
|---|---|---|
| 1. Study area and plan | Choose the ward or municipality, write questions, list layers, choose the CRS (UTM 44N or 45N, or MUTM) | 1, 2 |
| 2. Data collection | Ward boundary (local government or Survey Department), roads and buildings (OSM), schools (field survey with a phone GNSS app or a register), DEM (SRTM/Copernicus), flood-prone zone (your own derivation or a published hazard map) | 1, 3 |
| 3. Preparation | Reproject everything to one CRS, clip to the study area, clean topology, georeference any scanned map, create a metadata sheet | 2, 3 |
| 4. Database | Create a GeoPackage with layers `ward`, `school`, `road`, `building`, `flood_zone`, tables for census and school attributes joined by ward ID | 3 |
| 5. Analysis | Buffer schools 1 km (dissolve), count buildings inside; select schools in the flood zone (spatial query); Thiessen polygons; slope and flood zone from the DEM and flow accumulation; weighted-overlay suitability for the new school | 4, 5 |
| 6. Cartography | At least three maps: (a) base map with schools, (b) flood exposure, (c) suitability and recommended sites; each with title, legend, scale bar, north arrow, CRS and source | 2, 5 |
| 7. Report | Introduction, data and methods (with a flow chart), results, limits (data age, DEM resolution, assumptions), conclusions | all |
| 8. Presentation | Five minutes with the maps; demonstrate one repeatable QGIS model or a short Python script | all |

**Suggested QGIS workflow.** *Layer > Add Layer* for the data; *Project > Properties > CRS* to set the project CRS; *Vector > Geoprocessing Tools > Buffer*, *Clip*, *Intersection*, *Dissolve*; *Processing > Toolbox* for *Raster terrain analysis* (slope, aspect, hillshade), *Fill sinks*, *Flow accumulation* and *Watershed* (from GRASS or SAGA), and *Raster calculator* for map algebra; *Layer > Export > Save As* to GeoPackage; *Project > New Print Layout* for the map. Record each step so the work is reproducible; the same pipeline can be scripted with PyQGIS or with Python packages such as GeoPandas, Shapely and Rasterio.

**Evaluation checklist.** All layers share one CRS and have metadata; geometry is valid (no self-intersections, no slivers); attribute names are clean; every analysis step is documented with its parameters; maps follow the design rules of Section 5.3; limitations and assumptions are stated honestly; results can be reproduced from the files.

::: example Typical conclusions that a good report states
"Four of the eleven schools lie in the 5 m flood zone; they enrol 1,260 children (24 percent of the ward). Sixty-two households are more than 2 km from any school. The best new site by weighted overlay lies outside the flood zone beside the Ward 5 road, 1.2 km from two flood-zone schools. The result depends on the slope weight; with equal weights the site shifts 300 m north. A field check of land ownership is required before the choice is final."
:::

## 5.5 Summary and exercises

A surface (DEM, DSM, DTM, TIN or contour set) stores a value everywhere; interpolation (IDW, spline, kriging) estimates unsampled values and is compared by cross-validation. Slope, aspect, hillshade, curvature, profile, volume and viewshed are derived by neighbourhood and line-of-sight operations. Hydrology modelling fills sinks, assigns D8 flow directions, accumulates flow, thresholds streams (Strahler order) and delineates watersheds from pour points. A good map has a purpose, hierarchy, honest classes, legible type and colour, the standard elements, and is exported at the right resolution and format. A basic GIS project follows plan, data, preparation, database, analysis, cartography, report and presentation.

1. Differentiate DEM, DSM and DTM. Name two free global DEMs.
2. Explain IDW interpolation. How does the power parameter affect the result? How is it chosen?
3. Compare IDW, spline and kriging in three points each.
4. Define slope and aspect. A cell has a gradient of 0.20 (20 percent). What is the slope in degrees?
5. Describe how a viewshed is computed. State two practical uses in Nepal.
6. Compute the cut and fill volume for a 4 x 4 grid of 10 m cells in which the heights above the platform sum to +180 m and below to -140 m.
7. Explain the D8 algorithm and its limitations. How are flow accumulation and streams related?
8. List the steps of watershed delineation and the data needed. What is a pour point?
9. What is Strahler stream order? A stream of order 2 meets a stream of order 2; of order 2 meets order 1. What orders result?
10. Why must sinks be filled? When should a sink be kept?
11. A flow accumulation value of 4,500 cells in a 30 m DEM: what is the contributing area in km2?
12. List the elements of a map layout and the rules for a legend and a scale bar.
13. Discuss colour choice for a choropleth of literacy and for a land-use map.
14. A ground area 12 km wide must fit a map frame 200 mm wide. What scale denominator at minimum, and what round scale do you choose?
15. How many pixels are needed to print a 25 cm wide image at 300 dpi? Why is RGB not the same as CMYK in print?
16. Outline a basic GIS project from data collection to presentation and state four items of the evaluation checklist.

**Answers to the numerical items.** (4) slope = arctan(0.20) = **11.3 degrees**. (6) Cut = 180 x 100 m2 = **18,000 m3**; fill = 140 x 100 = **14,000 m3**; net = **+4,000 m3** surplus. (9) 2 + 2 gives **order 3**; 2 + 1 stays **order 2**. (11) 4,500 x 900 m2 = 4,050,000 m2 = **4.05 km2**. (14) 12 km / 200 mm = 12,000,000 mm / 200 mm = **1:60,000** at minimum; choose **1:75,000** (a round value; 1:60,000 does not leave a margin and is not a standard scale). (15) 25 cm = 9.84 in; 9.84 x 300 = **2,953 pixels**; RGB is the additive model of screens, CMYK is the subtractive model of inks, and some saturated RGB colours cannot be printed.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain flow direction and flow accumulation.**

Flow direction assigns each DEM cell the direction of the steepest descent to one of its eight neighbours (D8), found by comparing drops divided by distance (diagonal distance is 1.414 cells). It is coded with powers of two. Flow accumulation then counts, for each cell, the number of cells whose flow passes through it, found by adding the counts of upstream cells in order from high to low; multiplied by the cell area it is the contributing area. Cells with accumulation above a chosen threshold form the stream network, and the lowest cells are outlets.

**Q2 (5 marks). What is interpolation? Describe IDW.**

Interpolation estimates the value of a variable at unsampled locations from nearby samples, based on the assumption that near things are more related. In inverse distance weighting each estimate is a weighted average of the sample values with weights proportional to 1 / d^p, so closer samples count more. A higher power makes the surface more local and gives flat areas around sample points ("bull's eyes"), a lower power makes it smoother. The power can be chosen by leave-one-out cross-validation, comparing the RMSE of predicted and actual values. IDW cannot produce values beyond the sample range.

**Q3 (10 marks). Describe the steps of designing and printing a thematic map of a ward.**

Define the purpose and audience, for example flood exposure of schools for a ward meeting. Prepare the data in one projected CRS (UTM or MUTM), classify values with a stated method into four to six classes, and symbolise with a sequential hue for ordered data and a qualitative palette for categories, avoiding red-green pairs. Compose the layout with the title stating what, where and when, the main map as the dominant element, the legend with exact class limits, a graphic scale bar, a north arrow where needed, graticule or coordinate labels with the CRS, a locator inset, and the source, date and author. Apply cartographic principles: figure-ground contrast with light base layers, legible labels of at least six to seven points placed without overlap, simplified geometry, and an honest presentation. Choose the paper size and scale so that the frame fits (for example 1:10,000 on A3) and export a vector PDF with embedded fonts for printing, or a 300 dpi raster if images are used; proof a test print because RGB screen colours change in CMYK. Finally ask a colleague to read the map without explanation and revise if the message is not clear.
