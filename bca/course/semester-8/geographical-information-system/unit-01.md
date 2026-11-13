---
subject: Geographical Information System
grade: BCA Semester 8 (Elective III)
unit: 1
title: Introduction
hours: 6
area: BCA 453 · Geographical Information System · Unit 1
---

Almost everything that happens, happens somewhere: a landslide blocks a road, a customer orders food, a ward runs out of vaccine, a bank opens a branch. A **Geographical Information System (GIS)** is the family of tools and methods that lets a computer keep track of *where* things are, together with *what* they are, so that a question such as "which schools lie within 2 km of a flood-prone river?" can be answered in seconds instead of weeks. This unit defines GIS, its functions, applications and components, shows how a GIS is an information system like any other (with one crucial difference), describes the nature and sources of geographic data, and ends with recent trends.

::: key What this unit gives you
- A precise definition of GIS, the six core functions, and applications from disaster management to retail, with Nepali examples.
- The five components of a GIS (hardware, software, data, people, methods) and how they fit together.
- GIS as an information system: input, storage, analysis and output subsystems, spatial against attribute data, the layer idea.
- The nature of GIS data (spatial, attribute, temporal), scale, resolution, accuracy, precision, error and metadata, with three short programs.
- Recent trends: web and cloud GIS, open data, drones, GeoAI and digital twins.
:::

## 1.1 Definition, functions and applications of GIS

### 1.1.1 What a GIS is

A **geographic information system** is a computer-based system for **capturing, storing, checking, integrating, manipulating, analysing and displaying data that are related to positions on the Earth's surface**. Three words carry the meaning. *Geographic* means every record has a location that can be tied to the Earth through a coordinate system. *Information* means the records are organised and processed so that they answer questions, not merely stored. *System* means hardware, software, data, people and procedures work together.

The oldest and most-quoted example is not digital. In 1854 a cholera outbreak struck the Soho district of London. The physician John Snow plotted each death as a mark on a street map and saw that the marks clustered around the Broad Street water pump. The pump handle was removed and new cases fell. Nothing about the *data* was special (an address and an outcome); what mattered was putting them on a map and *analysing the pattern*. A GIS automates exactly this move for millions of records.

The modern history is short. In the 1960s Roger Tomlinson led the Canada Geographic Information System to inventory land resources, and is often called the father of GIS. Commercial packages followed (Esri was founded in 1969), personal computers made GIS affordable in the 1980s and 1990s, GPS (fully operational in 1995) made field positions easy to capture, and in the 2000s the open-source QGIS (first released in 2002), OpenStreetMap (2004) and web maps made GIS ordinary. Today a smartphone map is a GIS in the hand.

::: example GIS or just a map?
A printed map of Pokhara shows roads and lakes but cannot tell you the total length of road within 500 m of Phewa Lake. A GIS stores roads and the lake as data, so the same question is a *buffer* followed by an *overlay* and a *sum*. A map is one **output** of a GIS; the GIS also keeps the data behind the picture and can compute with it.
:::

### 1.1.2 Functions of a GIS

The functions are conveniently grouped as a chain from raw observations to decisions:

| Function | What it does | Typical example |
|---|---|---|
| **Capture** | Brings data in: digitising maps, GPS surveys, scanning, importing imagery and tables | Walking a road with a GPS logger |
| **Store and manage** | Keeps geometry and attributes in files or a spatial database with indexes and rules | A PostgreSQL/PostGIS table of ward polygons |
| **Query** | Answers "what is here?" and "where is it?" | Click a parcel and read its owner; select all wards with population above 20,000 |
| **Analyse** | Combines layers and derives new information | Buffer, overlay, shortest path, suitability, flood modelling |
| **Model** | Runs a process over space and time | Flow of water down a catchment, spread of a fire, travel time |
| **Visualise** | Produces maps, charts, 3-D scenes and reports | A choropleth of literacy by district |

Two properties separate GIS analysis from ordinary data analysis: **location is a key** (two tables can be joined by *where* things are, with no shared ID) and **neighbourhood matters** (a value is interpreted relative to nearby values, as in "the steepest slope near the village").

### 1.1.3 Applications

| Field | Questions a GIS answers | Nepali illustration |
|---|---|---|
| Disaster management | Which settlements lie in flood or landslide zones? Where should relief go first? | After the 2015 Gorkha earthquake volunteers mapped damaged buildings and routes on OpenStreetMap for responders |
| Urban planning | Where is land suitable for housing, roads or a hospital? | Land-use change in the Kathmandu Valley from satellite images |
| Agriculture and forestry | Crop health, soil suitability, forest cover and community-forest boundaries | Greenness from satellite images; community-forest user group maps |
| Water resources | Catchment areas, hydropower sites, irrigation reach | Delineating the catchment above a proposed micro-hydro intake |
| Health | Disease mapping, clinic access, outreach planning | Distance from each ward to the nearest health post |
| Utilities and telecom | Cable routes, transformers, tower coverage | Electricity distribution network maps |
| Transport and logistics | Shortest and fastest routes, service areas, fleet tracking | Ride-hailing and delivery apps |
| Business | Store location, market area, customer clusters | Choosing a new branch of a bank or a cooperative |
| Land administration | Parcels, ownership, taxes | Cadastral maps held by the Survey Department and local government |
| Environment and climate | Glacier retreat, land degradation, air quality | Glacier and glacial-lake monitoring in the Himalaya (ICIMOD, based in Kathmandu, works on this) |

A BCA graduate meets GIS in at least four ways: building **map-based apps** (delivery, tourism, real estate), maintaining **spatial databases**, writing **geoprocessing scripts**, and building **dashboards** that put data on a map.

```python
# A tiny "GIS" in plain Python: points with attributes, queried by place and by attribute.
import math

schools = [  # name, x_km, y_km (a local grid), students, has_library
    ("Shree Janata", 1.0, 2.0, 420, True),
    ("Saraswati",    4.5, 1.0, 150, False),
    ("Bal Bikas",    2.0, 6.5, 310, True),
    ("Adarsha",      7.0, 5.0, 520, False),
    ("Pragati",      5.5, 3.0, 260, True),
]
river_x = 5.0   # a north-south river at x = 5 km; flood zone = within 1 km of it

def dist_to_river(x):
    return abs(x - river_x)

print("Schools inside the 1 km flood strip:")
for n, x, y, s, lib in schools:
    if dist_to_river(x) <= 1.0:
        print("  %-12s %.1f km from river, %d students" % (n, dist_to_river(x), s))

at_risk = sum(s for n, x, y, s, lib in schools if dist_to_river(x) <= 1.0)
print("Students at risk:", at_risk)

# a spatial question: which school is nearest to a new clinic at (3, 3)?
cx, cy = 3.0, 3.0
nearest = min(schools, key=lambda r: math.hypot(r[1] - cx, r[2] - cy))
print("Nearest school to the clinic:", nearest[0], round(math.hypot(nearest[1] - cx, nearest[2] - cy), 2), "km")
```
```output
Schools inside the 1 km flood strip:
  Saraswati    0.5 km from river, 150 students
  Pragati      0.5 km from river, 260 students
Students at risk: 410
Nearest school to the clinic: Shree Janata 2.24 km
```
The first question mixes *position* (distance from the river) with *attribute* (students), and the second is a pure *nearest-neighbour* search. Real systems do the same with indexes, so that a million points answer in milliseconds.

## 1.2 Components of GIS

A GIS is more than software. Five components must all be present, and a weak one limits the rest.

```svgfig label="1.1" caption="The five components of a GIS. People and methods sit at the centre because they decide how hardware, software and data are used."
f = Fig(680, 300)
f.box(250, 110, 180, 70, "PEOPLE\nand METHODS", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(20, 20, 190, 62, "HARDWARE\ncomputers, GPS, drones,\nservers, printers", fill=BLUE, stroke=NAVY, size=10)
f.box(470, 20, 190, 62, "SOFTWARE\nQGIS, ArcGIS, PostGIS,\nweb mapping libraries", fill=MINT, stroke=TEAL, size=10)
f.box(20, 208, 190, 62, "DATA\nspatial + attribute,\nimagery, GPS tracks", fill=SOFT, stroke=SLATE, size=10)
f.box(470, 208, 190, 62, "NETWORK / CLOUD\nsharing, web services,\nstorage", fill=ROSE, stroke=RED, size=10)
f.arrow([(210, 60), (250, 125)], color=SLATE)
f.arrow([(470, 60), (430, 125)], color=SLATE)
f.arrow([(210, 230), (250, 165)], color=SLATE)
f.arrow([(470, 230), (430, 165)], color=SLATE)
```

### 1.2.1 Hardware

Hardware ranges from a field **smartphone or handheld GNSS receiver** (for capture), through an office **workstation** with a large display (for analysis), to **servers** and **cloud instances** (for storing and serving data to many users). Input devices include **digitisers and scanners** for paper maps; output devices include **plotters** for large printed maps. Drones carry cameras and sensors and are now a major source of very detailed images. Analysis of large rasters needs memory, fast disks and often a graphics processor.

### 1.2.2 Software

Software provides the tools to input, store, analyse and display. A full desktop package (the proprietary ArcGIS family, or the open-source **QGIS**) covers everything; a **spatial database** (PostgreSQL with PostGIS, SQLite with SpatiaLite, or GeoPackage files) stores data with spatial indexes; **libraries** (GDAL for format conversion, GEOS for geometry, PROJ for coordinate transformation, and Python packages built on them) let programmers automate; **web mapping libraries** (Leaflet, OpenLayers, MapLibre) show maps in browsers; and **servers** (GeoServer, MapServer) publish layers as web services.

### 1.2.3 Data

Data are the most expensive and longest-lived component. A GIS holds **spatial data** (where: coordinates, cells) and **attribute data** (what: names, numbers, categories). Collecting, cleaning and keeping data current usually costs far more than the software. Data must come with **metadata** (who made it, when, at what scale and accuracy, in which coordinate system).

### 1.2.4 People

People include **users** (planners, engineers, health officers), **analysts** who build workflows, **database administrators**, **developers**, and **managers** who decide priorities. The best software fails if nobody can frame a spatial question or interpret the result.

### 1.2.5 Methods

Methods are the procedures: how data are captured and checked, naming and coordinate-system conventions, quality-control rules, backup, and the analysis workflows that are repeated. A written standard (one projection for the whole organisation, one naming pattern) prevents a great deal of avoidable error.

::: caution The most common beginner failure
Mixing layers that use **different coordinate systems** without telling the software. Points that should fall on a road land in the sea off West Africa (near longitude 0, latitude 0 if values were treated as zero). Always check the coordinate reference system of every layer before analysis (Unit 2 explains why).
:::
## 1.3 GIS as an information system

### 1.3.1 What kind of information system is a GIS?

An **information system** collects data, stores them, processes them into information and presents it to support decisions. A payroll system does this for salaries; a library system for books. A GIS does it for **phenomena that have a location**. The ideas you know from DBMS apply: tables, keys, queries, integrity, users and permissions. The difference is that a GIS adds **geometry** (a column that holds a point, line or polygon), **spatial operators** (distance, intersection, containment) and **spatial indexes** to make them fast.

Seen as a pipeline, a GIS has four subsystems:

| Subsystem | Task | Examples |
|---|---|---|
| **Input** | Convert real-world observations and existing sources into digital form | Digitising, GPS, import, geocoding addresses |
| **Storage and management** | Organise, index, protect and version data | Geodatabase, shapefiles, GeoPackage, PostGIS |
| **Analysis and processing** | Transform and combine data | Query, buffer, overlay, interpolation, networks |
| **Output** | Communicate results | Maps, charts, reports, web services, 3-D views |

A GIS is therefore a **decision-support system** for spatial problems. It is also a *management information system* when it runs day-to-day operations (a municipality's property-tax map) and a *transaction* system when many users edit shared data at once (a land-registration office).

### 1.3.2 Spatial and attribute data

Every geographic **feature** (a well, a road, a ward) is described twice.

- **Spatial (geometric) data** say *where* and *what shape*: coordinates of a point, the ordered vertices of a line, the ring of a polygon, or the row and column of a raster cell.
- **Attribute (descriptive) data** say *what*: name, type, population, depth, owner, date. They are stored in table columns.

The two are linked by an internal **feature ID**. This is the central trick of a GIS: a map shows geometry, a table holds attributes, and clicking a feature opens its table row, while selecting table rows highlights features on the map.

| FID | geometry (spatial) | name | type | population |
|---|---|---|---|---|
| 1 | POINT (85.32 27.71) | Kathmandu | metropolitan | 845,767 |
| 2 | POINT (83.98 28.21) | Pokhara | metropolitan | 513,504 |
| 3 | POINT (84.43 27.68) | Bharatpur | metropolitan | 369,377 |

(Populations here are from the 2021 census as commonly cited; check the National Statistics Office for the official figures.)

There is also **temporal data** (when): a landslide date, a satellite acquisition time, a road-closure period. Many analyses are about *change*, so the date is a first-class attribute.

### 1.3.3 The layer concept

The real world is complicated; a GIS simplifies it by splitting it into **thematic layers**, each holding one kind of feature in one geometry type: roads (lines), rivers (lines), wards (polygons), schools (points), elevation (raster). All layers share a **coordinate system**, so they register exactly, like transparent sheets stacked on a light table. Analysis then **combines layers**: "schools" overlaid on "flood zone" gives "schools in the flood zone".

```svgfig label="1.2" caption="Layers of one area stacked on a common coordinate system. Overlaying the school points on the flood-zone polygon selects the schools at risk."
f = Fig(680, 270)
# three stacked 'sheets' drawn as parallelograms
f.poly([(40, 60), (230, 60), (260, 20), (70, 20)], fill=BLUE, stroke=NAVY, label="")
f.text(150, 42, "Elevation (raster)", size=10, color=NAVY, bold=True)
f.poly([(40, 140), (230, 140), (260, 100), (70, 100)], fill=MINT, stroke=TEAL)
f.text(150, 122, "Flood zone (polygon)", size=10, color=TEAL, bold=True)
f.poly([(40, 220), (230, 220), (260, 180), (70, 180)], fill=SAND, stroke=AMBER)
f.text(150, 202, "Schools (points)", size=10, color=AMBER, bold=True)
for x, y in ((100, 205), (150, 200), (200, 208), (130, 192)):
    f.circle(x, y, 3.5, fill=RED, stroke=RED)
f.arrow([(275, 40), (350, 110)], color=SLATE)
f.arrow([(275, 120), (350, 125)], color=SLATE)
f.arrow([(275, 200), (350, 140)], color=SLATE)
f.box(350, 90, 130, 60, "OVERLAY\n(same coordinate\nsystem)", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(480, 120), (530, 120)], color=NAVY)
f.poly([(535, 170), (665, 170), (665, 60), (535, 60)], fill=SOFT, stroke=SLATE)
f.poly([(560, 150), (640, 150), (640, 100), (560, 100)], fill=MINT, stroke=TEAL)
for x, y in ((580, 125), (600, 115), (625, 140)):
    f.circle(x, y, 4, fill=RED, stroke=RED)
for x, y in ((550, 75), (655, 80), (545, 160)):
    f.circle(x, y, 4, fill="#ffffff", stroke=SLATE)
f.text(600, 195, "Red: schools inside the flood zone", size=9.5, color=RED)
f.text(600, 212, "White: schools outside", size=9.5, color=SLATE)
```

The layer idea has a cost: relationships *within* the real world (a bridge belongs both to the road and to the river crossing) must be re-created by analysis, because each layer is stored separately. Modern **geodatabases** add rules and relationships (topology rules, feature datasets, relationship classes) to restore some of that structure.

```python
# Overlay by hand: which school points fall inside a rectangular flood polygon, and an attribute join.
flood = (3.0, 1.0, 6.0, 4.0)          # xmin, ymin, xmax, ymax of the flood zone (km)
schools = {1: (3.5, 2.0), 2: (4.5, 3.5), 3: (7.0, 3.0), 4: (2.0, 1.5), 5: (5.5, 0.5)}
attrs = {1: ("Janata", 420), 2: ("Saraswati", 150), 3: ("Adarsha", 520), 4: ("Bal Bikas", 310), 5: ("Pragati", 260)}

def inside(p, box):
    x, y = p
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]

hit = [fid for fid, p in schools.items() if inside(p, flood)]
print("schools in flood polygon (feature ids):", hit)
for fid in hit:                       # join geometry results back to the attribute table
    name, n = attrs[fid]
    print("  FID %d  %-10s %3d students" % (fid, name, n))
print("total students:", sum(attrs[f][1] for f in hit))
```
```output
schools in flood polygon (feature ids): [1, 2]
  FID 1  Janata     420 students
  FID 2  Saraswati  150 students
total students: 570
```
## 1.4 Nature and sources of GIS data

### 1.4.1 Nature of geographic data

Geographic data are unusual in four ways:

1. **Spatial dependence.** Nearby places tend to be alike (Tobler's first law of geography: "everything is related to everything else, but near things are more related than distant things"). That is why interpolation works and also why ordinary statistical tests that assume independence can mislead.
2. **Scale dependence.** What is visible, and how long a coastline or river looks, depends on the scale of observation. A 1:1,000,000 map shows a river as a smooth line; a 1:5,000 map shows its bends.
3. **Continuous reality, discrete records.** The world is continuous, but a computer stores finite points, vertices and cells. Every representation is an approximation.
4. **Uncertainty.** Every measurement has error, boundaries (a forest edge, a flood limit) are often fuzzy, and data age.

Two models of space organise how we record it. In the **object (entity) view** the world is empty space containing discrete things with boundaries (a building, a road): stored as **vectors**. In the **field view** a property varies continuously everywhere (temperature, elevation, rainfall): stored as **rasters** or surfaces. Unit 3 treats both in detail.

### 1.4.2 Scale, resolution, accuracy, precision

- **Scale** is the ratio between a distance on the map and the same distance on the ground (Unit 2). A *large-scale* map (1:5,000) shows a small area in detail; a *small-scale* map (1:1,000,000) shows a large area with less detail.
- **Resolution** is the smallest unit the data can distinguish: the size of a raster cell, or the smallest feature a map can hold. A 30 m cell cannot show a 5 m house.
- **Accuracy** is how close a measured value is to the **true** value. **Precision** is how close repeated measurements are to **each other** (and how many digits are recorded). A receiver may return the same wrong position every time: precise but inaccurate. A coordinate printed with eight decimals is precise on paper but not necessarily accurate.
- **Error** is the difference from truth. It can be **systematic** (a shifted datum, a bias that shifts everything the same way) or **random** (noise). Common summary measure: the **root mean square error (RMSE)**, the square root of the mean squared difference.

```python
# Accuracy against precision: three GPS "sessions" at a surveyed benchmark (true point = 0, 0), metres.
import math, statistics as st
sessions = {
    "A (accurate, precise)":    [(0.4, -0.3), (-0.2, 0.5), (0.1, 0.1), (-0.5, -0.2), (0.3, 0.4)],
    "B (precise, not accurate)":[(4.1, 3.0), (3.9, 3.2), (4.0, 2.9), (4.2, 3.1), (3.8, 3.0)],
    "C (accurate, not precise)":[(5.0, -4.0), (-5.5, 4.5), (3.0, 6.0), (-4.0, -5.0), (0.5, -0.5)],
}
for name, pts in sessions.items():
    errs = [math.hypot(x, y) for x, y in pts]                  # distance from truth
    rmse = math.sqrt(sum(e * e for e in errs) / len(errs))     # accuracy measure
    mx, my = st.mean(p[0] for p in pts), st.mean(p[1] for p in pts)
    spread = math.sqrt(sum((x - mx) ** 2 + (y - my) ** 2 for x, y in pts) / len(pts))   # precision measure
    print("%-27s RMSE %5.2f m   mean offset (%.1f, %.1f)   spread %.2f m" % (name, rmse, mx, my, spread))
```
```output
A (accurate, precise)       RMSE  0.47 m   mean offset (0.0, 0.1)   spread 0.46 m
B (precise, not accurate)   RMSE  5.03 m   mean offset (4.0, 3.0)   spread 0.17 m
C (accurate, not precise)   RMSE  5.97 m   mean offset (-0.2, 0.2)   spread 5.96 m
```
Session B has a tiny spread but a 5 m systematic offset: its **precision** is high and its **accuracy** low, which is typical of a wrong datum or a surveying bias. Session C averages close to the truth but scatters widely.

### 1.4.3 Sources of GIS data

| Source | Examples | Notes |
|---|---|---|
| **Existing maps** (paper) | Topographic sheets, cadastral maps | Scan, georeference, digitise; accuracy limited by map scale |
| **Field surveys and GNSS** | Handheld receivers, survey-grade GNSS, total station | The most accurate for small areas; costly in time |
| **Remote sensing** | Satellite images (Landsat, Sentinel), aerial photographs, drone images, LiDAR | Wide coverage and repeat visits; needs processing |
| **Existing digital data** | Government datasets (Survey Department, Department of Hydrology and Meteorology), census tables, OpenStreetMap, ICIMOD data portal | Check licence, date, scale and coordinate system |
| **Crowdsourced and sensor data** | OSM edits, mobile traces, IoT sensors, social media posts with location | Fast and current, uneven quality |
| **Attribute tables and databases** | Census, school and health-post registers, spreadsheets with addresses | Joined to geometry by an ID or **geocoded** from addresses |

Data are **primary** when you collected them for this purpose and **secondary** when someone else collected them. Secondary data save time but you inherit their errors.

### 1.4.4 Metadata

**Metadata** are data about data: title, abstract, date, creator, extent, coordinate system, scale or resolution, attribute definitions, lineage (how it was produced) and licence. Standards such as ISO 19115 organise them. Without metadata a layer cannot be trusted, compared or legally reused. Write at least five facts for every layer you create: *who, when, from what, in which coordinate system, how accurate.*

## 1.5 Recent trends and the future of GIS

- **Web and cloud GIS.** Maps are served over the web and analysis runs on remote servers; users need only a browser. Tile services and cloud-optimised formats (COG for rasters, GeoParquet and PMTiles for vectors) make very large data cheap to publish.
- **Open source and open data.** QGIS, PostGIS, GDAL and OpenStreetMap are production-grade and free. National and international programmes publish free imagery (Landsat, Sentinel) and elevation data.
- **Smaller, cheaper sensors.** Drones produce centimetre-resolution maps in an afternoon; smartphone GNSS and cheap RTK receivers deliver sub-metre or centimetre positions; satellite constellations image the world daily.
- **Real-time and IoT.** Streams from vehicles, river-level sensors and phones feed live maps and alerts.
- **GeoAI.** Machine learning detects buildings, roads, crops and landslides from imagery, and predicts risk. Quality still depends on good training data and human checking.
- **3-D, indoor and digital twins.** City models with buildings and utilities, indoor navigation, and digital-twin platforms that simulate floods or traffic.
- **Location privacy and ethics.** Location data reveal homes, routines and beliefs. Responsible GIS practice minimises collection, aggregates data, obtains consent, and thinks about misuse.
- **In Nepal.** Local governments need ward-level maps for planning and tax; community mapping groups and organisations such as Kathmandu Living Labs have shown how volunteers and students can build open datasets; disaster agencies use satellite flood maps during monsoon; a national geospatial infrastructure effort aims to make base data shareable (check the current status with the Survey Department).

## 1.6 Summary and exercises

A GIS captures, stores, analyses and displays data tied to places. Its functions are capture, storage, query, analysis, modelling and visualisation; its components are hardware, software, data, people and methods. As an information system it is organised into input, storage, analysis and output, with geometry linked to attributes and data held in thematic layers over a common coordinate system. Geographic data are spatially dependent, scale dependent, approximate and uncertain, so scale, resolution, accuracy, precision, error and metadata matter. Sources are maps, surveys, GNSS, remote sensing, existing datasets and crowdsourcing. Trends are web/cloud GIS, open data, drones, IoT, GeoAI, 3-D and privacy-aware practice.

1. Define GIS. Explain with an example why a printed map alone is not a GIS.
2. Describe the six functions of a GIS with one example of each.
3. List any five applications of GIS and give one question a GIS answers in each.
4. Explain the five components of a GIS. Which is usually the most expensive and why?
5. How does a GIS differ from an ordinary information system such as a payroll system? What do the two have in common?
6. Distinguish spatial data from attribute data. How are the two linked inside a GIS?
7. What is the layer concept? Why must layers share a coordinate system?
8. Differentiate accuracy and precision with an example. In the program of Section 1.4.2, which session has the largest systematic error?
9. A GPS receiver reports a position 3.2 m east and 2.4 m north of a benchmark. Compute the error distance.
10. Differentiate the object (entity) view and the field view of geographic data with two examples each.
11. List six sources of GIS data and one limitation of each.
12. What is metadata? List eight items a good metadata record contains.
13. Discuss three recent trends in GIS and one ethical concern.

**Answers to the numerical item.** (9) Error distance = sqrt(3.2^2 + 2.4^2) = sqrt(10.24 + 5.76) = sqrt(16) = **4.0 m**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Define GIS and list its components.**

A GIS is a computer-based system for capturing, storing, managing, analysing and displaying data that are related to positions on the Earth's surface. Its five components are hardware (computers, GNSS receivers, servers, plotters), software (a desktop package, spatial database and web tools), data (spatial and attribute data with metadata), people (users, analysts, administrators, managers) and methods (standards and procedures such as one coordinate system and quality-control rules). All five are needed; data and people are usually the costliest and most important.

**Q2 (5 marks). Distinguish spatial data from attribute data.**

Spatial data describe location and shape: coordinates of points, vertices of lines and polygons, or the position of raster cells. Attribute data describe the properties of the feature in table columns, for example name, population or soil type. A feature ID links each geometry to its table row, so selecting on the map highlights table rows and querying the table highlights features. A third kind, temporal data, records when.

**Q3 (10 marks). Explain GIS as an information system, with its subsystems and the layer concept.**

A GIS is an information system that deals with data tied to location. Like any information system it takes in data, stores them, processes them into information and communicates it for decisions. Input converts maps, surveys, GNSS and imagery into digital form. Storage holds geometry and attributes in files or a spatial database with indexes, integrity rules and user permissions. Analysis performs queries, buffers, overlays, interpolation and network analysis. Output produces maps, charts, reports and web services. What distinguishes it is the geometry column, the spatial operators and the spatial indexes that make location queries efficient.

To keep the real world manageable, the data are split into thematic layers (roads, rivers, wards, schools, elevation), each with one geometry type, all registered to the same coordinate system. Layers are combined by overlay to answer questions such as "which schools are in the flood zone". The drawback is that relationships within the real world must be re-created by analysis or by geodatabase rules. Because layers are only comparable when registered, the coordinate system and metadata of each layer must be checked before use.
