S = {}

S['cadd_def'] = r'''**Computer Aided Design and Drafting (CADD)** is the use of computer hardware and software to create, modify, analyse, optimise, store and plot the design and the drawings of a project. *Computer aided design* is the creative and analytical part (modelling, checking, optimising a design) and *computer aided drafting* is the production of the accurate drawings (plans, sections, details) from it. AutoCAD, Civil 3D, Revit, SW-DTM and STAAD are common examples in civil engineering.

**Advantages of CADD over manual drawing**

| Aspect | Manual drafting | CADD |
|---|---|---|
| Accuracy | limited by pencil, scale, eyesight (about 0.5 mm) | exact coordinates, precision of 8 or more decimals |
| Speed | every line and symbol drawn again | COPY, ARRAY, MIRROR, BLOCK, templates: 5 to 10 times faster |
| Editing | erase and redraw, sheet is spoiled | UNDO, MODIFY, instant changes, revisions in minutes |
| Scale | the scale is fixed at the start | drawn full size (1:1) and plotted at any scale |
| Storage and copies | bulky tracing paper, fades, torn | digital file, unlimited identical copies, backup and cloud |
| Standards | depend on the draftsman | layers, text and dimension styles, title-block templates give uniform quality |
| Sharing and integration | by post | e-mail, DWG / DXF / PDF; links to analysis, quantity estimation, GIS and 3D / BIM |
| Visualisation | perspective drawn by hand | 3D models, rendering, walk-through |'''

S['cadd_dis'] = r'''**Disadvantages of CADD:** high initial cost of hardware, licences and training; dependence on electricity and computers (data loss through power cuts, virus, hardware failure if there is no backup); skilled operators are required and there is a learning curve; file-format and version incompatibility; software piracy and licence problems; eye strain and a risk of blindly trusting the computer output without a check.

**Use in civil engineering:** architectural and structural drawings of buildings, road plan-profile and cross-sections, canal / bridge / dam drawings, drainage and pipe networks, survey and contour maps, earthwork quantities, 3D visualisation and as-built records.'''

S['fields'] = r'''**Fields where CADD is popularly used**

1. **Civil engineering and architecture:** building plans, structural details, roads, bridges, hydropower, irrigation, water supply, town planning and landscape.
2. **Surveying, mapping and GIS:** topographic maps, contour and terrain models, cadastral maps (SW-DTM, Civil 3D).
3. **Mechanical, automobile and aerospace engineering:** machine parts, assemblies, CAM / CNC machining, aircraft and car bodies.
4. **Electrical and electronics:** circuit schematics, PCB layout, panel and transmission-line drawings.
5. **Industrial and interior design:** product design, furniture, packaging, jewellery, textile patterns.
6. **Shipbuilding, mining and plant design:** hull lines, piping and instrumentation diagrams, plant layouts.
7. **Entertainment and media:** animation, films, games and advertisement (3D modelling and rendering).'''

S['uses2d'] = r'''**Specific uses of 2D drawings in civil engineering:** floor plans, elevations and sections of buildings; site, location and layout plans; foundation and structural reinforcement details; road plan and profile, cross-sections; canal, drainage and pipe-network layouts; survey and contour maps; working (construction) drawings, shop drawings and as-built drawings for submission to the municipality and for tendering.

**Common 2D CADD software:** AutoCAD, AutoCAD LT, BricsCAD, DraftSight, ZWCAD, LibreCAD, Civil 3D (2D and DTM), MicroStation, SW-DTM (survey and road design software developed in Nepal).'''

S['uses3d'] = r'''**Specific uses of 3D drawings in civil engineering:** (1) *visualisation* and client presentation (rendered images, walk-through and fly-through); (2) *design checking*, such as clash detection between architectural, structural and MEP elements; (3) *structural analysis models* (3D frames in STAAD.Pro, ETABS, SAP2000); (4) *terrain and earthwork models* (cut and fill volumes, slope analysis); (5) *quantity take-off and cost estimation*; (6) *construction sequencing (4D) and facility management* in BIM; (7) generating plans, sections and elevations automatically from one model.

**Common 3D software:** AutoCAD (3D), Revit, ArchiCAD, SketchUp, Civil 3D, Tekla Structures, 3ds Max, Rhino, Blender, Lumion / V-Ray (rendering), Navisworks, STAAD.Pro / ETABS (analysis models).'''

S['coords'] = r'''**Coordinate systems in AutoCAD**

1. **World Coordinate System (WCS):** the fixed default system with the origin (0,0,0) at the lower-left of the drawing, X to the right (east), Y upward (north) and Z out of the screen. Angles are measured counter-clockwise from the east (0°).
2. **User Coordinate System (UCS):** a movable and rotatable system defined by the user (UCS command: origin, 3 point, object, view, Z-axis, world). It is used for drawing on an inclined plane or in 3D and to make the point (0,0) convenient for the job.

**Methods of entering points (the coordinate input formats):**

| Format | Example | Meaning |
|---|---|---|
| Absolute Cartesian | `50,30` | x = 50, y = 30 from the origin |
| Relative Cartesian | `@40,0` | 40 units in X, 0 in Y from the last point |
| Absolute polar | `60<45` | distance 60 from the origin at 45° |
| Relative polar | `@50<60` | 50 units at 60° from the last point |
| Direct distance | move the cursor, type `25` | 25 units in the cursor direction (ORTHO or POLAR on) |

For 3D work, *cylindrical* (`r<θ,z`) and *spherical* (`r<θ<φ`) formats are used, and the dynamic input (DYN) shows the same values at the cursor.'''

S['block'] = r'''**Creating a block in AutoCAD (steps)**

1. Draw the object (door, window, tree, north arrow, column symbol) at full size, preferably on layer 0 so that it takes the properties of the layer on which it is inserted.
2. Type **BLOCK** (B). In the Block Definition dialog box: enter the *Name* (e.g. DOOR-900); click *Pick point* and select the *base (insertion) point*; click *Select objects* and pick the drawing, then Enter; choose *Convert to block*, *Retain* or *Delete*; set the *block unit* (mm or m) and the *Annotative / Allow exploding* options; give a description; click OK.
3. Place it with **INSERT** (I): select the block name, give the insertion point, scale (X, Y, Z) and rotation (or tick *Specify on-screen*).
4. To use the block in other drawings, save it as a file with **WBLOCK** (W: Source = Block or Objects, set the file name and path). Edit it with **BEDIT**; modify the definition and *all* inserted copies update. **EXPLODE** converts it back to simple objects. Attributes (ATTDEF) can be added to carry data, such as the text fields of a title block.

**Advantages of blocks:** the drawing needs far less memory (the geometry is stored once and each insertion is only a reference); drawing is faster because standard symbols (doors, windows, furniture, structural symbols) are reused from a library; uniform and standard symbols; changing the block definition updates every copy automatically; easy scaling, rotating and replacing; blocks with attributes give schedules and quantities automatically (data extraction); and the drawing is better organised.'''

S['layers_blocks'] = r'''**Layers.** A layer is like a transparent sheet on which one kind of object is drawn. Each layer has a name, colour, linetype, lineweight and states (on / off, freeze, lock, plot). A building drawing is divided into layers such as WALL, DOOR, WINDOW, COLUMN, BEAM, DIM, TEXT, HATCH, CENTRE, GRID and TITLE. **Blocks** are named groups of objects saved once and inserted many times (doors, windows, symbols, north arrow, title block).

**How they are used while drafting:**

1. Create the layers first (LAYER command) and make the right layer *current* before drawing; keep colour, linetype and lineweight **ByLayer**.
2. Draw the objects in the relevant layer; switch off or freeze the layers that are not needed (for example a structural plan is made by turning off furniture), lock the layers that must not be changed, and set DEFPOINTS or a viewport layer as non-plotting.
3. Create blocks of repeated items on layer **0**; when such a block is inserted on the layer WINDOW it takes the colour and linetype of WINDOW, and when the layer is switched off all the windows disappear.
4. Plot with different lineweights for different layers (thick for sections and walls, thin for dimensions and hatching), which gives a clear, standard drawing.
5. Use the layer states and the block library to modify a whole group in one step, and to keep the drawing organised for a team.'''

S['units_scales'] = r'''**Steps to change units and scales for a drawing in AutoCAD**

1. **Units.** Type **UNITS** (UN). In the Drawing Units dialog: *Length* type = Decimal and precision 0.00 (or Architectural / Engineering if needed); *Angle* type = Decimal degrees, precision 0; choose the *Insertion scale* (units for blocks and drawings inserted: Millimetres or Meters); open *Direction* and keep the base angle as East; leave *Clockwise* unticked; OK.
2. **Drawing limits / area (optional).** Type **LIMITS** and give the lower-left (0,0) and the upper-right corner = *paper size × scale factor*, then **ZOOM → All**. Always draw the object *full size (1:1)* in the chosen unit.
3. **Scale factor** = 1/(plotting scale). For 1:100 the scale factor is 100: an A3 sheet (420 × 297 mm) corresponds to 42000 × 29700 mm of the real drawing. Text height on the sheet = required plotted height × scale factor (2.5 mm text at 1:100 is drawn as 250 units).
4. **Change the size of existing objects:** **SCALE** (SC): select the objects, specify the base point, then enter the scale factor (or use *Reference* to scale a known length to the correct length).
5. **Plotting scale:** in the PLOT / page-setup dialog choose the paper size and set the scale (for example 1 mm = 100 units for a drawing in millimetres) or, better, set the viewport scale in a layout (steps in the A3 layout answer). Use the **annotation scale** (status-bar button) for annotative text, dimensions and hatches.

*Example:* a 6 m wall drawn at 1:50 is drawn as 6000 units (in mm) and plots as 6000/50 = 120 mm on the sheet.'''

S['annot_dim'] = r'''**Annotative and standard dimensioning**

| Point | Standard (non-annotative) dimensioning | Annotative dimensioning |
|---|---|---|
| Size of text and arrows | fixed in drawing units; the overall scale (DIMSCALE) must be set equal to the plot scale (for example 100 for 1:100) | defined in *paper* units (for example 2.5 mm text) and scaled automatically by the annotation scale |
| Number of styles | a separate dimension style is needed for each plotting scale | one dimension style for all scales |
| Viewports with different scales | text size changes from viewport to viewport, so manual correction is needed | each viewport shows the dimension at the correct size for its own scale |
| Setting | DIMSCALE = scale factor, in DIMSTYLE → Fit → *Use overall scale of* | tick *Annotative* in DIMSTYLE → Fit (the annotation symbol appears); set CANNOSCALE |
| Editing | if the scale changes all dimensions must be edited | add the new scale to the object (OBJECTSCALE) and the display updates |
| Best for | single-scale drawings in model space | layouts with several viewports and scales |'''

S['layer_new'] = r'''**Setting up a new layer and its properties**

1. Type **LAYER** (LA) or click *Layer Properties* on the Home tab; the Layer Properties Manager opens.
2. Click **New Layer** (the sheet icon or Alt+N); a layer named *Layer1* appears; type the new name, for example **WALL**, and press Enter.
3. **Colour:** click the colour swatch of the layer, select a colour from the Select Colour dialog (for example 1 red), OK.
4. **Linetype:** click the linetype name (Continuous); in Select Linetype click *Load*, choose from ACAD.LIN a type such as CENTER, HIDDEN or DASHED, OK, then select it.
5. **Lineweight:** click the lineweight column and select, for example, 0.50 mm for walls; 0.25 mm for dimensions.
6. Set *Transparency*, the *Plot* option (on for drawing layers, off for construction or viewport layers) and the *Plot style* if needed.
7. Select the layer and click **Set Current** (green check mark); everything drawn now takes these properties when the object properties are ByLayer. The *on / off, freeze / thaw, lock / unlock* icons control the visibility and the editing of the layer.

| Layer | Colour | Linetype | Lineweight |
|---|---|---|---|
| WALL | red | Continuous | 0.50 mm |
| CENTRE | green | CENTER | 0.18 mm |
| HIDDEN | yellow | HIDDEN | 0.25 mm |
| DIM | cyan | Continuous | 0.18 mm |
| TEXT | white / black | Continuous | 0.25 mm |'''

S['model_paper'] = r'''**Model space and layout (paper) space**

| Point | Model space | Layout (paper) space |
|---|---|---|
| Nature | the unlimited 2D / 3D working area (the *Model* tab) in which the actual objects are drawn full size | a sheet of paper (the *Layout* tabs) laid out for printing |
| Scale | always 1:1, one view | each viewport shows the model at its own scale (1:50, 1:100 and others) |
| Contents | the design: plan, sections, details, 3D model | sheet border, title block, viewports, notes, scale bar, annotative dimensions and text |
| Number | one only | many layouts (A3, A1 and others) in the same file, each with several viewports |
| Use | designing, drafting and modelling | plotting and presentation, to arrange several views at different scales on one sheet |

The viewport is a window from the layout into the model space; the model is never copied, so a change in model space is seen in all layouts at once.'''

S['layout_a3'] = r'''**Steps to create an A3 layout at scale 1:100**

1. In **Model space** draw the plan full size (1:1) in the chosen unit and on proper layers. Create a layer **VPORT** for viewports and **TITLE** for the border (set VPORT not to plot).
2. Click a **Layout** tab (or right-click → *New layout*, rename it A3-1:100). Right-click the layout tab → *Page Setup Manager → Modify*: select the plotter (for example DWG To PDF), paper size **ISO A3 (420.00 × 297.00 mm)**, plot area *Layout*, plot scale **1:1**, orientation landscape, and a plot style table (monochrome.ctb); OK.
3. Delete the default viewport. Insert the A3 border and the title block (INSERT, at 0,0, units mm) on the layer TITLE.
4. Make the layer VPORT current and create the viewport with **MVIEW** (rectangular, drag inside the border).
5. Double-click inside the viewport (model space is activated). Set the scale: type **ZOOM → 0.01xp** if the drawing is in millimetres (1:100 means 0.01 times), or **10xp** if the drawing unit is a metre (10 mm of paper per metre); or select **1:100** in the viewport scale box on the status bar. Pan to place the plan at the centre.
6. Double-click outside the viewport to return to paper space; set *Display locked = Yes* in the Properties palette so that the scale is not changed accidentally.
7. Add the annotative text and dimensions, the scale text "SCALE 1:100", the north point and the title-block attributes in the layout.
8. Turn off or set the layer VPORT to non-plot, then give **PLOT** (Ctrl+P) → preview → OK (plot scale remains 1:1 because the 1:100 scale is in the viewport).'''

S['titleblock'] = r'''A **title block** is a boxed table at the lower right corner of each drawing sheet (inside the border) that identifies the drawing and carries its administrative data. For an A3 sheet it is generally about 180 mm wide and 60 to 100 mm high. The border is about 0.5 mm thick, with a 25 mm margin at the binding (left) edge and 5 to 10 mm on the other sides.

%%FIG c_titleblock|Position of the title block on an A3 sheet and its typical divisions.%%

**Typical information in the title block:**

1. **Name of the project** and the location (for example Residential Building of Mr. X, Pokhara).
2. **Name of the client / owner**, and the name, address, registration number, logo and seal of the **consultant / designer / contractor**.
3. **Title of the drawing** (for example First Floor Plan, Section A-A, Typical Canal Section).
4. **Drawing number** and **sheet number** ("3 of 12").
5. **Scale** (and a bar scale if the sheet may be reduced), **units**.
6. **Date** (BS / AD) and the **north point** where relevant.
7. **Names and signatures of the persons who drew, designed, checked and approved** the drawing.
8. **Revision table** (revision number, date, description of change) and the status (for approval, for construction, as built).
9. General notes, legend, reference drawings and the key plan if needed.'''

S['dtm_steps'] = r'''**Creating contours and an L-section (longitudinal section) from survey data in SW-DTM**

%%FIG c_dtmflow|Work-flow in SW-DTM from the survey data to the contour map, L-section and cross-sections.%%

1. **Prepare the survey data** from the total station / GPS as a text or CSV file with the columns *point number, easting, northing, elevation, description code* (PENZD).
2. Start SW-DTM, open a *new project* and set the units and the coordinate system.
3. **Import the points** (File → Import → Points, choose the PENZD format); check the plotted points and remove wrong shots (outliers); add **break lines** (road edge, ridge, stream, retaining wall) and the **boundary** of the area.
4. **Create the DTM:** Surface → Create DTM (triangulation, TIN). Remove the long triangles outside the boundary.
5. **Generate the contours:** set the minor interval (for example 1 m) and the major interval (5 m), smoothing and labelling, then draw the contour map.
6. **Define the alignment** (road, canal, pipe, transmission line) by drawing the centre line with intersection points and curves, or by importing it.
7. **Generate the L-section:** give the chainage interval (10 or 20 m); the program interpolates the ground level of the DTM at each chainage and plots the **ground profile** with the datum, chainage and elevation table (horizontal scale 1:1000, vertical 1:100). Add the design (finished) grade line and the vertical curves.
8. Generate the **cross-sections** at each chainage for a chosen width (±20 m) and compute the cut and fill volumes.
9. **Export** to AutoCAD (DXF / DWG) or plot directly on the sheet.'''

S['dtm_uses'] = r'''**Uses of SW-DTM** (Softwel Digital Terrain Modelling software used for surveying and road design in Nepal):

1. Importing survey points (total station, GPS, level) and creating the **digital terrain model (TIN)** of the ground.
2. Producing **contour maps** at any interval, spot-height and grid maps.
3. Preparing the **longitudinal section (L-section)** and **cross-sections** along any alignment.
4. **Road, canal, pipeline and transmission-line design:** horizontal and vertical alignment, curve and widening design, super-elevation.
5. **Earthwork (cut and fill) volumes** from cross-sections or from the surface (bill of quantities).
6. Slope, aspect, catchment and drainage analysis, 3D view and surface rendering.
7. **Setting out data** (coordinates of centre line and offsets) for the construction survey.
8. Exporting drawings to AutoCAD (DXF / DWG) and plotting the drawings on standard sheets.'''

S['canal_fill'] = r'''A canal runs in **complete fill** where the natural ground is lower than the required bed level of the canal, so the canal is carried on an **embankment** built from compacted soil. The section is trapezoidal; an inspection road is provided on the top of one or both banks.

%%FIG c_canal_fill%%

| Element | Typical value (small irrigation canal) |
|---|---|
| Bed width B | 3.0 m (depends on the design discharge) |
| Full supply depth D | 1.5 m |
| Free board | 0.5 m or more above the full supply level (FSL) |
| Inner side slope | 1.5 H : 1 V (1 V : 1.5 H) |
| Outer side slope | 2 H : 1 V (flatter if the soil is poor) |
| Top width of the bank | 3.0 m (a road side up to 5 m) |
| Compaction | in 150 to 200 mm layers to at least 95 percent of maximum dry density; top soil stripped and a key / cut-off trench at the base |

Labels: natural ground level (NGL), canal bed level (CBL), full supply level (FSL), bank top level, free board, embankment, inner and outer slopes, berm / inspection path and the drain at the toe of the bank.'''

S['canal_cut'] = r'''A canal runs in **complete cut** (excavation) where the natural ground level is higher than the full supply level, so the canal trench is excavated below the ground and the ground itself forms the banks. The side slopes in cut are generally 1.5 H : 1 V or flatter in soil, and steeper in rock.

%%FIG c_canal_cut%%

| Element | Typical value |
|---|---|
| Bed width B | 3.0 m |
| Full supply depth D | 1.5 m |
| Free board | 0.5 m (ground level at least 0.5 m above FSL) |
| Side slope in cut | 1.5 H : 1 V (ordinary soil) |
| Berm / inspection path | 3.0 m (minimum) at the ground level on one or both sides; the excavated spoil is used for the banks and the side drains |

Labels: natural ground level (NGL), canal bed, full supply level (FSL), free board, side slope, berm / path, depth of cut and bed width.'''

S['road_fill'] = r'''A hill road is in **complete fill** where the road formation is higher than the natural ground across the whole width and the road is carried on an embankment, with a catch drain at the toe of the uphill fill and a toe wall / gabion on the downhill side where the fill is high.

%%FIG c_road_fill%%

| Element | Typical value (single-lane hill road) |
|---|---|
| Carriageway | 3.0 m with 0.5 m shoulders; total formation 5.0 m including the side drain |
| Crossfall / camber | 5 percent (1 in 20), inward slope towards the hill-side drain |
| Side drain | 0.6 m wide, 0.5 m deep (lined or unlined) |
| Fill slope | 1.5 H : 1 V (flatter for loose soil, protected by turfing / bio-engineering) |
| Toe wall | dry stone or gabion wall at the toe where the fill height is more than about 2 m |
| Compaction | in layers of 150 to 200 mm |'''

S['road_cutfill'] = r'''On a steep hillside the road is built in **partial cut and fill** (side-hill section): the uphill half of the formation is excavated and the excavated material is used to form the downhill half, which reduces the quantity of spoil and the volume of earthwork.

%%FIG c_road_cutfill%%

| Element | Typical value (single-lane hill road) |
|---|---|
| Formation width | 5.0 m (side drain 0.6 + shoulder 0.5 + carriageway 3.0 + shoulder / parapet 0.9) |
| Crossfall | 5 percent inward towards the drain |
| Cut slope | 1 H : 2 V in hard soil / soft rock, 1 H : 1 V in ordinary soil, 1 H : 4 V in hard rock (with breast wall where unstable) |
| Fill slope | 1.5 H : 1 V, with a toe wall / gabion; fill is placed in layers of 150 to 200 mm and compacted |
| Drains | side drain (0.6 m wide), catch drain above the top of the cut, cross-drainage (culvert / pipe) every 50 to 100 m |
| Original ground | dashed line; the cut and fill areas are hatched differently |

Labels: original ground, cut slope, side drain, carriageway and shoulders, crossfall, fill slope, toe wall, catch drain.'''

S['retaining_types'] = r'''A retaining wall holds back soil at a level difference. The common typical types are shown below.

%%FIG c_retaining|Typical sections of retaining walls: gravity, cantilever and counterfort.%%

1. **Gravity wall** (stone masonry or PCC / plain concrete): resists the earth pressure by its own weight; trapezoidal section with the base width B = 0.5 to 0.7 H and a top width of at least 0.6 m with a batter on the face; used up to about 3 to 4 m height.
2. **Cantilever RCC wall** (inverted T or L): a thin stem fixed in a base slab; the weight of the soil on the heel provides the stability; base width B = 0.5 to 0.7 H, stem thickness at the bottom about H/10 to H/12, slab thickness about H/10; economic up to about 6 m height.
3. **Counterfort wall:** a cantilever wall with vertical triangular ribs (counterforts) at 2.5 to 3.5 m spacing on the soil side that tie the stem to the heel; economic for heights above 6 m.
4. Others: **buttress wall** (ribs on the toe side), **gabion wall** (wire-mesh baskets filled with stones, flexible and self-draining, very common on Nepalese roads), **crib wall**, **reinforced-earth wall** and **sheet-pile / bridge-abutment walls**.

All walls need drainage: weep holes (100 mm at 2 m c/c), a granular filter behind the wall, and a drain at the top.'''

S['cantilever4'] = r'''A cantilever RCC retaining wall of **4 m height** has the following proportions (H = 4.0 m): base width B = 0.6H = 2.4 m; base slab thickness = H/8 = 0.5 m; stem height 3.5 m; stem thickness 0.40 m at the base and 0.25 m at the top (the batter is on the soil side); toe 0.6 m; heel 1.4 m (0.6 + 0.4 + 1.4 = 2.4 m).

%%FIG c_cantilever4%%

Details to be labelled: the main reinforcement in the stem on the earth face (tension face) and in the toe at the bottom and in the heel at the top; distribution (temperature) bars; cover (50 mm on the earth face, 75 mm under the base); weep holes of 100 mm at 2 m c/c; granular filter / drainage layer behind the stem; PCC blinding of 100 mm below the base; granular backfill; and the ground levels on both sides. The materials are grade M25 concrete and Fe500 steel. (The bar sizes in the figure are typical; the design gives the actual values.)'''

S['mun_struct'] = r'''**Drawings to be included in municipal structural drawings (for building permit and completion):**

1. Foundation plan with the column layout and the foundation (footing) details, with the section of the plinth and the DPC.
2. Column layout plan with the column schedule (sizes, main bars, stirrups) and a typical column section.
3. Plinth beam layout and floor beam layouts for each floor with the beam schedule and the typical beam sections / elevations.
4. Slab layouts with the reinforcement details (main, distribution and top bars, chairs).
5. Staircase and landing details, lintel, chhajja / sunshade and parapet details.
6. Roof and slab-cum-tank plans, water tank, septic tank and soak pit structural details; retaining and boundary wall details if any.
7. Seismic detailing (confinement zone, 135° hooks, lap splices) as per the Nepal National Building Code (NBC 105, NBC 205 / 202) and the general notes: grade of concrete and steel, cover, load assumptions, soil bearing capacity.
8. The structural design report and calculation sheets signed by the structural engineer with the council registration number.'''

S['mun_arch'] = r'''**Drawings to be included in municipal architectural drawings (building permit submission):**

1. **Location map and site plan** with the plot boundary, the road width, setbacks, the north direction, and the surrounding features.
2. **Floor plans** of the basement / ground / typical / terrace floors with dimensions, room names and areas, door and window marks.
3. **Elevations** (front, rear and side), showing the heights, finish and the ground and roof levels.
4. **Sections** (at least two: one through the staircase), showing the floor-to-floor heights, plinth, sill, lintel and parapet heights.
5. **Foundation plan and the roof plan**; the door and window schedule.
6. **Septic tank and soak pit** (or sewer connection), the water supply, drainage and electrical layouts, the rainwater harvesting and the parking layout.
7. **Calculations** of the ground coverage and the floor area ratio (FAR), the area statement, and the supporting documents (land ownership certificate, citizenship, tax receipt, blue print).'''

S['bim_def'] = r'''**Building Information Modelling (BIM)** is a process of creating and managing an intelligent, 3D digital model of a facility, in which every element (wall, beam, door, pipe) carries information about its geometry, material, cost, schedule and maintenance. Plans, sections, elevations, schedules and quantities are all extracted from the same model, so they are always consistent. Revit, ArchiCAD, Tekla Structures, Civil 3D and Navisworks are BIM tools.'''

S['bim_adv'] = r'''**Major advantages of BIM over traditional CADD**

1. **One coordinated, data-rich model:** all drawings (plans, sections, elevations) and schedules are generated from one model, so a change is updated everywhere and the drawings never contradict each other (CADD has separate unlinked lines in each view).
2. **Automatic quantity take-off and cost estimates** (5D) directly from the model.
3. **Clash detection** between architectural, structural and MEP systems before construction, which reduces rework and variations.
4. **Visualisation and analysis:** 3D walk-through, energy, daylight and structural analysis from the same model.
5. **Time and construction planning** (4D) by linking the model to the schedule.
6. **Better collaboration** by all disciplines on a shared model in a common data environment.
7. **Lifecycle use:** as-built information for operation and facility management.
8. Reduced errors and faster revisions, saving time and cost.'''

S['bim_vs_cad'] = r'''| Point | Traditional CADD (AutoCAD drafting) | BIM |
|---|---|---|
| Basic element | lines, arcs, circles and text (geometry only) | intelligent objects (wall, beam, door) with properties and relations |
| Dimensions | mostly 2D, separate drawings | 3D model plus automatically generated 2D views |
| Information | graphic only | geometry, material, cost, phase, manufacturer, maintenance data |
| Changes | each drawing edited by hand; errors and inconsistency | one change updates plans, sections, elevations and schedules |
| Quantities | measured manually or exported with effort | automatic schedules and quantity take-off |
| Collaboration | sharing of files; drawings overlaid | shared federated model in a common data environment, clash detection |
| Dimension of data | 2D / 3D | 3D plus time (4D), cost (5D), operation (6D) |
| Use | documentation of the design | whole life cycle: design, construction, operation |
| Software | AutoCAD, DraftSight | Revit, ArchiCAD, Tekla, Civil 3D |'''

S['cde'] = r'''A **Common Data Environment (CDE)** is the single, agreed source of information for a project: a cloud-based digital platform (for example Autodesk Construction Cloud / BIM 360, Aconex, Trimble Connect, SharePoint) in which all the project documents, models and drawings of all the parties are created, shared, reviewed and approved in a controlled way (ISO 19650: Work in progress, Shared, Published, Archive).

**Advantages:** one source of truth, so everybody works on the latest version; no duplicate or conflicting files; better collaboration and communication among the architect, structural, MEP engineers, contractor and client; controlled access, security and an audit trail of who changed what and when; version control and approval workflow; time and cost saved (less rework, quick design review and coordination); easy handover of the as-built records at the end of the project.'''

S['array'] = r'''**Types of Array in AutoCAD:** (1) *Rectangular array*, objects in rows and columns; (2) *Polar array*, objects around a centre point; (3) *Path array*, objects along a path (line, polyline, arc, spline). The command is **ARRAY** (AR) (the old dialog box is ARRAYCLASSIC).

**Steps**

1. **Rectangular:** type ARRAYRECT, select the object, Enter; in the ribbon enter the number of *Columns* and *Rows* and the *distance between* columns (X) and rows (Y) (a negative value reverses the direction), the *Levels* (for 3D); press Enter or *Close Array*. Example: 5 columns at 3000 mm and 4 rows at 4000 mm for a column grid.
2. **Polar:** ARRAYPOLAR, select the object, specify the *centre point*; enter the *Number of items*, the *angle to fill* (360° for a full circle) and choose *Rotate items* yes / no, *Direction* (clockwise or counter-clockwise); Enter. Example: 8 bolts on a circle.
3. **Path:** ARRAYPATH, select the objects, select the *path curve*, enter the number of items or the spacing (Divide / Measure), choose *Align items* (to follow the tangent); Enter.

The result is one associative array object: edit its count and spacing in the Properties palette, or **EXPLODE** to separate copies.'''

S['dimstyle'] = r'''**Steps to set up a new dimension style in AutoCAD**

1. Type **DIMSTYLE** (D) or choose *Dimension Style* from the Annotate panel; the Dimension Style Manager opens.
2. Click **New**; enter the new style name (for example *ARCH-100*), *Start With* a base style (Standard), and tick *Annotative* if the style is annotative; click *Continue*.
3. In the dialog tabs set the following:
   - **Lines:** dimension line colour / lineweight, *extend beyond ticks*, *offset from origin* (about 2 mm) and extension line extension (about 2 mm).
   - **Symbols and Arrows:** arrowhead type (architectural tick for buildings, closed filled arrow for mechanical), arrow size (2.5 mm), centre marks.
   - **Text:** text style (with fixed height 0 in the style), text height (2.5 mm), position above the dimension line, alignment *aligned with dimension line*.
   - **Fit:** *Use overall scale of* = 100 for a drawing plotted at 1:100 (or *Annotative*), text placement.
   - **Primary Units:** unit format Decimal, precision 0 or 0.00, decimal separator ".", *Measurement scale factor* 1 (or 0.001 for mm → m), prefix / suffix if required.
   - **Alternate Units** and **Tolerances** if needed.
4. Click **OK**, then **Set Current** and **Close**. Dimension with DIMLINEAR, DIMALIGNED, DIMANGULAR, DIMRADIUS, DIMBASELINE and DIMCONTINUE.'''

S['loc_site'] = r'''A **location map** shows where the site is in relation to the surroundings and a **site plan** shows the plot and what is built on it. They are drawn on the same sheet, as in the sketch below.

%%FIG c_locsite|Typical location map (left) and site plan (right).%%

**Information to be included**

*Location map (1:5000 or 1:10000):* the site marked clearly, the main roads with their names and widths, nearby landmarks (school, temple, hospital, river, bridge), the north point, the scale, and the distance to the main road / junction.

*Site plan (1:100, 1:200 or 1:500):* the **plot boundary** with dimensions and area; plot number (kitta number), ward and municipality; the **road width / right of way** and the road centre line; the **footprint** of the proposed building and of existing buildings with dimensions; **setbacks** from the road and from each boundary; the gate, driveway and parking; boundary wall; septic tank and soak pit, water tank, trees; the **north direction**; existing contours / ground levels; the **scale**; the neighbours' names and the plot of the adjoining owners; and the tabulated areas (plot area, ground coverage, floor area ratio, open space).'''

S['canal_fill_note'] = ''
