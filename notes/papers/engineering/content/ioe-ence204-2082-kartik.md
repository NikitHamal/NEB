---
file: NEBians-IOE-Past-Paper-Computer-Aided-Civil-Drawing-ENCE204-2082-Kartik.pdf
subject: Computer Aided Civil Drawing
level: BE · Year II / Part I
code: ENCE 204
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BCE
time: 1.5 hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (new course). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
Define Computer Aided Design & drafting. Write down advantages of CADD over manual drawings. [[3]]

@q 2
What are the fields where CADD is popularly used? [[2]]

@q 3
Explain the steps to change units and scales for a drawing in AutoCAD. [[2]]

@q 4
What are differences between annotative and standard dimensioning in AutoCAD? [[2]]

@q 5
Write the steps to set up a new layer and new layer properties in AutoCAD. [[2]]

@q 6
Write steps to create A3 layouts in AutoCAD with scale of 1:100. [[2]]

@q 7
Sketch a typical title block and write typical information to be included in it. [[4]]

@q 8
How can you create contour and L-sections from a survey data using SW-DTM? [[2]]

@q 9
Sketch and label a typical canal section in complete fill. [[2]]

@q 10
Sketch and label common typical section of retaining walls. [[2]]

@q 11
List out the drawings to be included in municipal Structural drawings. [[3]]

@q 12
What are the major advantages of BIM over traditional CADD? [[2]]

@q 13
What is common data environment and write its advantages. [[2]]
<!-- SOLUTIONS -->

@s 1
**Computer Aided Design and Drafting (CADD)** is the use of computer hardware and software to create, modify, analyse, optimise, store and plot the design and the drawings of a project. *Computer aided design* is the creative and analytical part (modelling, checking, optimising a design) and *computer aided drafting* is the production of the accurate drawings (plans, sections, details) from it. AutoCAD, Civil 3D, Revit, SW-DTM and STAAD are common examples in civil engineering.

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
| Visualisation | perspective drawn by hand | 3D models, rendering, walk-through |

@s 2
**Fields where CADD is popularly used**

1. **Civil engineering and architecture:** building plans, structural details, roads, bridges, hydropower, irrigation, water supply, town planning and landscape.
2. **Surveying, mapping and GIS:** topographic maps, contour and terrain models, cadastral maps (SW-DTM, Civil 3D).
3. **Mechanical, automobile and aerospace engineering:** machine parts, assemblies, CAM / CNC machining, aircraft and car bodies.
4. **Electrical and electronics:** circuit schematics, PCB layout, panel and transmission-line drawings.
5. **Industrial and interior design:** product design, furniture, packaging, jewellery, textile patterns.
6. **Shipbuilding, mining and plant design:** hull lines, piping and instrumentation diagrams, plant layouts.
7. **Entertainment and media:** animation, films, games and advertisement (3D modelling and rendering).

@s 3
**Steps to change units and scales for a drawing in AutoCAD**

1. **Units.** Type **UNITS** (UN). In the Drawing Units dialog: *Length* type = Decimal and precision 0.00 (or Architectural / Engineering if needed); *Angle* type = Decimal degrees, precision 0; choose the *Insertion scale* (units for blocks and drawings inserted: Millimetres or Meters); open *Direction* and keep the base angle as East; leave *Clockwise* unticked; OK.
2. **Drawing limits / area (optional).** Type **LIMITS** and give the lower-left (0,0) and the upper-right corner = *paper size × scale factor*, then **ZOOM → All**. Always draw the object *full size (1:1)* in the chosen unit.
3. **Scale factor** = 1/(plotting scale). For 1:100 the scale factor is 100: an A3 sheet (420 × 297 mm) corresponds to 42000 × 29700 mm of the real drawing. Text height on the sheet = required plotted height × scale factor (2.5 mm text at 1:100 is drawn as 250 units).
4. **Change the size of existing objects:** **SCALE** (SC): select the objects, specify the base point, then enter the scale factor (or use *Reference* to scale a known length to the correct length).
5. **Plotting scale:** in the PLOT / page-setup dialog choose the paper size and set the scale (for example 1 mm = 100 units for a drawing in millimetres) or, better, set the viewport scale in a layout (steps in the A3 layout answer). Use the **annotation scale** (status-bar button) for annotative text, dimensions and hatches.

*Example:* a 6 m wall drawn at 1:50 is drawn as 6000 units (in mm) and plots as 6000/50 = 120 mm on the sheet.

@s 4
**Annotative and standard dimensioning**

| Point | Standard (non-annotative) dimensioning | Annotative dimensioning |
|---|---|---|
| Size of text and arrows | fixed in drawing units; the overall scale (DIMSCALE) must be set equal to the plot scale (for example 100 for 1:100) | defined in *paper* units (for example 2.5 mm text) and scaled automatically by the annotation scale |
| Number of styles | a separate dimension style is needed for each plotting scale | one dimension style for all scales |
| Viewports with different scales | text size changes from viewport to viewport, so manual correction is needed | each viewport shows the dimension at the correct size for its own scale |
| Setting | DIMSCALE = scale factor, in DIMSTYLE → Fit → *Use overall scale of* | tick *Annotative* in DIMSTYLE → Fit (the annotation symbol appears); set CANNOSCALE |
| Editing | if the scale changes all dimensions must be edited | add the new scale to the object (OBJECTSCALE) and the display updates |
| Best for | single-scale drawings in model space | layouts with several viewports and scales |

@s 5
**Setting up a new layer and its properties**

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
| TEXT | white / black | Continuous | 0.25 mm |

@s 6
**Steps to create an A3 layout at scale 1:100**

1. In **Model space** draw the plan full size (1:1) in the chosen unit and on proper layers. Create a layer **VPORT** for viewports and **TITLE** for the border (set VPORT not to plot).
2. Click a **Layout** tab (or right-click → *New layout*, rename it A3-1:100). Right-click the layout tab → *Page Setup Manager → Modify*: select the plotter (for example DWG To PDF), paper size **ISO A3 (420.00 × 297.00 mm)**, plot area *Layout*, plot scale **1:1**, orientation landscape, and a plot style table (monochrome.ctb); OK.
3. Delete the default viewport. Insert the A3 border and the title block (INSERT, at 0,0, units mm) on the layer TITLE.
4. Make the layer VPORT current and create the viewport with **MVIEW** (rectangular, drag inside the border).
5. Double-click inside the viewport (model space is activated). Set the scale: type **ZOOM → 0.01xp** if the drawing is in millimetres (1:100 means 0.01 times), or **10xp** if the drawing unit is a metre (10 mm of paper per metre); or select **1:100** in the viewport scale box on the status bar. Pan to place the plan at the centre.
6. Double-click outside the viewport to return to paper space; set *Display locked = Yes* in the Properties palette so that the scale is not changed accidentally.
7. Add the annotative text and dimensions, the scale text "SCALE 1:100", the north point and the title-block attributes in the layout.
8. Turn off or set the layer VPORT to non-plot, then give **PLOT** (Ctrl+P) → preview → OK (plot scale remains 1:1 because the 1:100 scale is in the viewport).

@s 7
A **title block** is a boxed table at the lower right corner of each drawing sheet (inside the border) that identifies the drawing and carries its administrative data. For an A3 sheet it is generally about 180 mm wide and 60 to 100 mm high. The border is about 0.5 mm thick, with a 25 mm margin at the binding (left) edge and 5 to 10 mm on the other sides.

```figure caption="Position of the title block on an A3 sheet and its typical divisions."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
def dm(ax,p,q,t,off=(0,0.35),size=7,ha='center',color=INK):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="<->",color=color,lw=0.8,shrinkA=0,shrinkB=0))
    ax.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha=ha,va='center',fontsize=size,color=color)
def tx(ax,x,y,t,size=7,ha='center',color=INK,**k): ax.text(x,y,t,ha=ha,va='center',fontsize=size,color=color,**k)
def ld(ax,t,xy,xyt,size=7,ha='center'):
    ax.annotate(t,xy=xy,xytext=xyt,fontsize=size,ha=ha,va='center',arrowprops=dict(arrowstyle="-",lw=0.6,color=MUTED))
def hatch(ax,x0,x1,y,n=40,l=0.5):
    for x in np.linspace(x0,x1,n): ax.plot([x,x-l],[y,y-l],color=MUTED,lw=0.5)
fig=plt.figure(figsize=(7.4,3.2))
a=fig.add_axes([0.0,0.02,0.40,0.92]); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-2,44); a.set_ylim(-2,32)
a.add_patch(plt.Rectangle((0,0),42,29.7,fc="white",ec=INK,lw=1.2)); a.add_patch(plt.Rectangle((2.5,0.5),39,28.7,fc="none",ec=INK,lw=1.8))
a.add_patch(plt.Rectangle((23.5,0.5),18,8,fc="#e8eefb",ec=INK,lw=1.2)); tx(a,32.5,4.5,"title\nblock",size=7)
tx(a,13,18,"DRAWING AREA\n(border line 0.5 mm,\nmargin 25 mm left /\n5 mm others)",size=6.6); tx(a,21,31,"A3 sheet 420 × 297 mm",size=7)
b=fig.add_axes([0.42,0.02,0.57,0.92]); b.set_aspect('equal'); b.axis('off'); b.set_xlim(-0.5,18.5); b.set_ylim(-1.5,12.5)
b.add_patch(plt.Rectangle((0,0),18,10,fc="white",ec=INK,lw=1.6))
for y in (2,4,6,8): b.plot([0,18],[y,y],color=INK,lw=0.9)
b.plot([6,6],[8,10],color=INK,lw=0.9); b.plot([12,12],[4,6],color=INK,lw=0.9)
for x in (4.5,9,13.5): b.plot([x,x],[0,2],color=INK,lw=0.9)
for x in (4,8,12): b.plot([x,x],[2,4],color=INK,lw=0.9)
tx(b,3,9.0,"CONSULTANT\nname · address · logo",size=6.2); tx(b,12,9.0,"CLIENT / OWNER",size=6.4)
tx(b,9,7.0,"PROJECT:  name and location of the project",size=6.4); tx(b,6,5.0,"DRAWING TITLE (e.g. Typical canal section)",size=6.2); tx(b,15,5.0,"DRAWING No.",size=6.2)
for x,t in ((2,"SCALE\n1:100"),(6,"DATE\n2082/06/15"),(10,"SHEET\n3 of 12"),(15,"REVISION / STATUS")): tx(b,x,3.0,t,size=5.8)
for x,t in ((2.25,"DRAWN"),(6.75,"DESIGNED"),(11.25,"CHECKED"),(15.75,"APPROVED")): tx(b,x,1.0,t+"\n(sign / date)",size=5.6)
tx(b,9,11.2,"Typical title block (A3, 180 × 100 mm), drawn in the lower right corner",size=6.8)
dm(b,(0,-0.7),(18,-0.7),"180 mm",off=(0,-0.35),size=6.4)
```

**Typical information in the title block:**

1. **Name of the project** and the location (for example Residential Building of Mr. X, Pokhara).
2. **Name of the client / owner**, and the name, address, registration number, logo and seal of the **consultant / designer / contractor**.
3. **Title of the drawing** (for example First Floor Plan, Section A-A, Typical Canal Section).
4. **Drawing number** and **sheet number** ("3 of 12").
5. **Scale** (and a bar scale if the sheet may be reduced), **units**.
6. **Date** (BS / AD) and the **north point** where relevant.
7. **Names and signatures of the persons who drew, designed, checked and approved** the drawing.
8. **Revision table** (revision number, date, description of change) and the status (for approval, for construction, as built).
9. General notes, legend, reference drawings and the key plan if needed.

@s 8
**Creating contours and an L-section (longitudinal section) from survey data in SW-DTM**

```figure caption="Work-flow in SW-DTM from the survey data to the contour map, L-section and cross-sections."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
def dm(ax,p,q,t,off=(0,0.35),size=7,ha='center',color=INK):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="<->",color=color,lw=0.8,shrinkA=0,shrinkB=0))
    ax.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha=ha,va='center',fontsize=size,color=color)
def tx(ax,x,y,t,size=7,ha='center',color=INK,**k): ax.text(x,y,t,ha=ha,va='center',fontsize=size,color=color,**k)
def ld(ax,t,xy,xyt,size=7,ha='center'):
    ax.annotate(t,xy=xy,xytext=xyt,fontsize=size,ha=ha,va='center',arrowprops=dict(arrowstyle="-",lw=0.6,color=MUTED))
def hatch(ax,x0,x1,y,n=40,l=0.5):
    for x in np.linspace(x0,x1,n): ax.plot([x,x-l],[y,y-l],color=MUTED,lw=0.5)
fig=blockchain([("1  Survey data","P, E, N, Z, D (.txt/.csv)"),("2  Import points","PENZD, set units"),("3  Break lines","ridge, road edge, stream"),("4  Create DTM","triangulate, clip boundary"),("5  Contours","interval 1 m, major 5 m"),("6  Alignment","centre line (IPs, curves)"),("7  L-section","ground profile, scales 1:1000 / 1:100"),("8  Cross-sections","every 20 m, ±20 m"),("9  Export","DXF / DWG to AutoCAD, plot")],cols=3,figsize=(7.2,3.1))
```

1. **Prepare the survey data** from the total station / GPS as a text or CSV file with the columns *point number, easting, northing, elevation, description code* (PENZD).
2. Start SW-DTM, open a *new project* and set the units and the coordinate system.
3. **Import the points** (File → Import → Points, choose the PENZD format); check the plotted points and remove wrong shots (outliers); add **break lines** (road edge, ridge, stream, retaining wall) and the **boundary** of the area.
4. **Create the DTM:** Surface → Create DTM (triangulation, TIN). Remove the long triangles outside the boundary.
5. **Generate the contours:** set the minor interval (for example 1 m) and the major interval (5 m), smoothing and labelling, then draw the contour map.
6. **Define the alignment** (road, canal, pipe, transmission line) by drawing the centre line with intersection points and curves, or by importing it.
7. **Generate the L-section:** give the chainage interval (10 or 20 m); the program interpolates the ground level of the DTM at each chainage and plots the **ground profile** with the datum, chainage and elevation table (horizontal scale 1:1000, vertical 1:100). Add the design (finished) grade line and the vertical curves.
8. Generate the **cross-sections** at each chainage for a chosen width (±20 m) and compute the cut and fill volumes.
9. **Export** to AutoCAD (DXF / DWG) or plot directly on the sheet.

@s 9
A canal runs in **complete fill** where the natural ground is lower than the required bed level of the canal, so the canal is carried on an **embankment** built from compacted soil. The section is trapezoidal; an inspection road is provided on the top of one or both banks.

```figure caption="Typical canal section in complete fill (embankment)."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
def dm(ax,p,q,t,off=(0,0.35),size=7,ha='center',color=INK):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="<->",color=color,lw=0.8,shrinkA=0,shrinkB=0))
    ax.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha=ha,va='center',fontsize=size,color=color)
def tx(ax,x,y,t,size=7,ha='center',color=INK,**k): ax.text(x,y,t,ha=ha,va='center',fontsize=size,color=color,**k)
def ld(ax,t,xy,xyt,size=7,ha='center'):
    ax.annotate(t,xy=xy,xytext=xyt,fontsize=size,ha=ha,va='center',arrowprops=dict(arrowstyle="-",lw=0.6,color=MUTED))
def hatch(ax,x0,x1,y,n=40,l=0.5):
    for x in np.linspace(x0,x1,n): ax.plot([x,x-l],[y,y-l],color=MUTED,lw=0.5)
fig,ax=plt.subplots(figsize=(7.4,3.1)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-17,17); ax.set_ylim(-1.9,5.6)
emb=[(-13.5,0),(-7.5,3),(-4.5,3),(-1.5,1),(1.5,1),(4.5,3),(7.5,3),(13.5,0)]
ax.add_patch(plt.Polygon(emb,closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.add_patch(plt.Polygon([(-1.5,1),(1.5,1),(3.75,2.5),(-3.75,2.5)],fc="#bcd7f2",ec="none"))
ax.plot([-4.5,4.5],[2.5,2.5],color="#1d6fb8",lw=1.1,ls="--")
ax.plot([-16,16],[0,0],color=INK,lw=1.0); hatch(ax,-15.5,15.5,0,n=52,l=0.6)
dm(ax,(-1.5,1.35),(1.5,1.35),"B = 3.0 m",off=(0,0.4),size=6.8)
ld(ax,"FSL (full supply level)",(3.2,2.5),(9.8,4.9),ha="left")
ld(ax,"canal bed (CBL)",(-1.4,1.0),(-9.0,0.55))
dm(ax,(6.2,1.0),(6.2,2.5),"D = 1.5 m",off=(0.15,0.0),size=6.8,ha="left")
dm(ax,(-6.0,2.5),(-6.0,3.0),"",off=(0,0))
ld(ax,"free board 0.5 m",(-6.0,2.75),(-10.6,4.5),ha="center")
dm(ax,(-7.5,3.5),(-4.5,3.5),"top width 3.0 m",off=(0,0.45),size=6.8)
dm(ax,(4.5,3.5),(7.5,3.5),"top width 3.0 m",off=(0,0.45),size=6.8)
tx(ax,3.9,1.15,"",size=6); ld(ax,"inner slope 1.5 H : 1 V",(3.0,2.0),(11.8,2.2),ha="left")
ld(ax,"outer slope 2 H : 1 V",(10.5,1.5),(14.2,3.1),ha="left")
tx(ax,2.0,0.45,"compacted embankment",size=6.6)
tx(ax,-16.5,-1.15,"natural ground level (NGL), top soil stripped; fill in 150-200 mm layers, 95 % MDD",size=6.4,ha="left")
ax.set_title("Typical canal section in complete fill (embankment)",fontsize=8)
```

| Element | Typical value (small irrigation canal) |
|---|---|
| Bed width B | 3.0 m (depends on the design discharge) |
| Full supply depth D | 1.5 m |
| Free board | 0.5 m or more above the full supply level (FSL) |
| Inner side slope | 1.5 H : 1 V (1 V : 1.5 H) |
| Outer side slope | 2 H : 1 V (flatter if the soil is poor) |
| Top width of the bank | 3.0 m (a road side up to 5 m) |
| Compaction | in 150 to 200 mm layers to at least 95 percent of maximum dry density; top soil stripped and a key / cut-off trench at the base |

Labels: natural ground level (NGL), canal bed level (CBL), full supply level (FSL), bank top level, free board, embankment, inner and outer slopes, berm / inspection path and the drain at the toe of the bank.

@s 10
A retaining wall holds back soil at a level difference. The common typical types are shown below.

```figure caption="Typical sections of retaining walls: gravity, cantilever and counterfort."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
def dm(ax,p,q,t,off=(0,0.35),size=7,ha='center',color=INK):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="<->",color=color,lw=0.8,shrinkA=0,shrinkB=0))
    ax.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha=ha,va='center',fontsize=size,color=color)
def tx(ax,x,y,t,size=7,ha='center',color=INK,**k): ax.text(x,y,t,ha=ha,va='center',fontsize=size,color=color,**k)
def ld(ax,t,xy,xyt,size=7,ha='center'):
    ax.annotate(t,xy=xy,xytext=xyt,fontsize=size,ha=ha,va='center',arrowprops=dict(arrowstyle="-",lw=0.6,color=MUTED))
def hatch(ax,x0,x1,y,n=40,l=0.5):
    for x in np.linspace(x0,x1,n): ax.plot([x,x-l],[y,y-l],color=MUTED,lw=0.5)
fig=plt.figure(figsize=(7.4,2.9))
def panel(i,title):
    a=fig.add_axes([0.01+i*0.335,0.04,0.32,0.84]); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-0.8,5.2); a.set_ylim(-0.6,5.1); a.set_title(title,fontsize=7.4); return a
a=panel(0,"(a) gravity (stone masonry / PCC)")
a.add_patch(plt.Polygon([(2.4,0),(1.8,4),(4.9,4),(4.9,0)],fc="#eadfc9",ec="none")); hatch(a,2.0,4.8,3.9,n=12,l=0.5)
a.add_patch(plt.Polygon([(0,0),(2.4,0),(1.8,4),(1.1,4)],fc="#cfd4dc",ec=INK,lw=1.3)); a.plot([-0.5,0.0],[0.4,0.4],color=INK); a.plot([-0.5,-0.5],[0.4,0.4],color=INK)
a.plot([-0.7,0.0],[0.5,0.5],color=INK,lw=1.0); a.plot([0,0.2],[0.5,0.5],color=INK,lw=1.0)
tx(a,1.45,2.0,"masonry / PCC",size=6.4); tx(a,3.5,2.0,"backfill",size=6.6); dm(a,(0,-0.3),(2.4,-0.3),"B = 0.5–0.7 H",off=(0,-0.25),size=6.2); dm(a,(1.1,4.35),(1.8,4.35),"0.6 m",off=(0,0.25),size=6.2); a.plot([-0.7,5.1],[0,0],color=INK,lw=0.8)
tx(a,0.35,4.8,"H",size=7); a.annotate("",xy=(-0.35,4.0),xytext=(-0.35,0.5),arrowprops=dict(arrowstyle="<->",lw=0.7)); tx(a,-0.55,2.3,"H",size=7)
b=panel(1,"(b) cantilever RCC (inverted T)")
b.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(4.9,4.0),(4.9,0.5)],fc="#eadfc9",ec="none")); hatch(b,1.0,4.8,3.9,n=12,l=0.5)
b.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.3))
b.plot([-0.7,5.1],[0.5,0.5],color=INK,lw=0.8,ls="--"); tx(b,3.4,2.2,"backfill",size=6.6); tx(b,0.1,-0.35,"toe",size=6.2); tx(b,1.9,-0.35,"heel",size=6.2); dm(b,(0,-0.75),(2.4,-0.75),"B = 0.5–0.7 H",off=(0,-0.2),size=6.2)
tx(b,0.72,4.45,"stem",size=6.4); tx(b,1.3,0.25,"base slab",size=5.6)
c=panel(2,"(c) counterfort (section through a counterfort)")
c.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(4.9,4.0),(4.9,0.5)],fc="#eadfc9",ec="none"))
c.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.3))
c.add_patch(plt.Polygon([(0.85,4.0),(2.4,0.5),(1.0,0.5)],fc="#b9c2cf",ec=INK,lw=1.0,ls="--")); tx(c,1.45,1.55,"counterfort",size=5.8); tx(c,3.4,2.2,"backfill",size=6.6); c.plot([-0.7,5.1],[0.5,0.5],color=INK,lw=0.8,ls="--")
tx(c,2.6,-0.35,"used for H > 6 m, counterforts at 2.5-3.5 m c/c",size=5.6)
```

1. **Gravity wall** (stone masonry or PCC / plain concrete): resists the earth pressure by its own weight; trapezoidal section with the base width B = 0.5 to 0.7 H and a top width of at least 0.6 m with a batter on the face; used up to about 3 to 4 m height.
2. **Cantilever RCC wall** (inverted T or L): a thin stem fixed in a base slab; the weight of the soil on the heel provides the stability; base width B = 0.5 to 0.7 H, stem thickness at the bottom about H/10 to H/12, slab thickness about H/10; economic up to about 6 m height.
3. **Counterfort wall:** a cantilever wall with vertical triangular ribs (counterforts) at 2.5 to 3.5 m spacing on the soil side that tie the stem to the heel; economic for heights above 6 m.
4. Others: **buttress wall** (ribs on the toe side), **gabion wall** (wire-mesh baskets filled with stones, flexible and self-draining, very common on Nepalese roads), **crib wall**, **reinforced-earth wall** and **sheet-pile / bridge-abutment walls**.

All walls need drainage: weep holes (100 mm at 2 m c/c), a granular filter behind the wall, and a drain at the top.

@s 11
**Drawings to be included in municipal structural drawings (for building permit and completion):**

1. Foundation plan with the column layout and the foundation (footing) details, with the section of the plinth and the DPC.
2. Column layout plan with the column schedule (sizes, main bars, stirrups) and a typical column section.
3. Plinth beam layout and floor beam layouts for each floor with the beam schedule and the typical beam sections / elevations.
4. Slab layouts with the reinforcement details (main, distribution and top bars, chairs).
5. Staircase and landing details, lintel, chhajja / sunshade and parapet details.
6. Roof and slab-cum-tank plans, water tank, septic tank and soak pit structural details; retaining and boundary wall details if any.
7. Seismic detailing (confinement zone, 135° hooks, lap splices) as per the Nepal National Building Code (NBC 105, NBC 205 / 202) and the general notes: grade of concrete and steel, cover, load assumptions, soil bearing capacity.
8. The structural design report and calculation sheets signed by the structural engineer with the council registration number.

@s 12
**Major advantages of BIM over traditional CADD**

1. **One coordinated, data-rich model:** all drawings (plans, sections, elevations) and schedules are generated from one model, so a change is updated everywhere and the drawings never contradict each other (CADD has separate unlinked lines in each view).
2. **Automatic quantity take-off and cost estimates** (5D) directly from the model.
3. **Clash detection** between architectural, structural and MEP systems before construction, which reduces rework and variations.
4. **Visualisation and analysis:** 3D walk-through, energy, daylight and structural analysis from the same model.
5. **Time and construction planning** (4D) by linking the model to the schedule.
6. **Better collaboration** by all disciplines on a shared model in a common data environment.
7. **Lifecycle use:** as-built information for operation and facility management.
8. Reduced errors and faster revisions, saving time and cost.

@s 13
A **Common Data Environment (CDE)** is the single, agreed source of information for a project: a cloud-based digital platform (for example Autodesk Construction Cloud / BIM 360, Aconex, Trimble Connect, SharePoint) in which all the project documents, models and drawings of all the parties are created, shared, reviewed and approved in a controlled way (ISO 19650: Work in progress, Shared, Published, Archive).

**Advantages:** one source of truth, so everybody works on the latest version; no duplicate or conflicting files; better collaboration and communication among the architect, structural, MEP engineers, contractor and client; controlled access, security and an audit trail of who changed what and when; version control and approval workflow; time and cost saved (less rework, quick design review and coordination); easy handover of the as-built records at the end of the project.
