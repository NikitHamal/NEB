# Geographical Information System - BCA (Semester VIII elective, 3 credits)

Study notes for the TU Geographical Information System elective (course code CACS454 in the TU outline, Year IV, 5 hours a week: 3 theory and 2 practical). Five units follow the outline in its order. The outline gives no hours per unit; the hours here (6, 6, 12, 12, 9 of about 45 theory hours) are our estimate from the topic load.

| Unit | Title | Hours | Outline topics covered |
|---|---|---|---|
| 1 | Introduction | 6 | definition, functions and applications; components; GIS as an information system; nature and sources of GIS data; recent trends and future |
| 2 | GIS and Map | 6 | map and its characteristics; mapping concepts and techniques; map projection (datum, UTM, Nepal's modified UTM) |
| 3 | GIS Data Sources and Structures | 12 | capturing GIS data; sources (maps, GPS, images, databases); vector, raster and TIN structures; GIS data modelling; GIS database design |
| 4 | Spatial Data Modeling and Analysis | 12 | spatial data modelling; vector-based analysis; raster-based analysis |
| 5 | GIS Data Modeling and Creating Maps | 9 | surface modelling; hydrology modelling; designing and printing the map; the basic GIS laboratory project |

## Verification

Every program is executed by `bca/tools/fill_script_outputs.py`, so the printed output is real: scale and buffer areas, classification breaks, Mercator and UTM (the Kathmandu UTM easting and northing were cross-checked against `pyproj`: 334,770 E, 3,067,000 N in zone 45N), georeferencing residuals, a GNSS Gauss-Newton solution with DOP, NDVI, SQL joins, R-tree and grid indexes, Delaunay TIN, overlay by Sutherland-Hodgman clipping, Dijkstra, least-cost paths, weighted overlay, IDW, Horn slope, cut and fill, D8 hydrology and layout arithmetic. Figure 5.1 computes its own D8 arrows and accumulation.

## Source and honesty

Units and topics follow the TU CACS454 outline as reproduced at notebahadur.com; the wording, examples and numbers are original. Nepal specifics (the Survey Department's modified UTM belts and scale factor, the local datum, the use of OpenStreetMap, ICIMOD and Kathmandu Living Labs) are stated as commonly taught or from public descriptions; check the current Survey Department documents for transformation parameters before survey-grade work. Populations of cities are the 2021 census figures as commonly cited. Crop values and costs are illustrative. The laboratory plan in 5.4 maps the outline's one-line "basic GIS project" to a concrete example; it is not a printed college manual. No subject-teacher review.
