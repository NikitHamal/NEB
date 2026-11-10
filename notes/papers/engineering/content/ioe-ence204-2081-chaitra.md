---
file: NEBians-IOE-Past-Paper-Computer-Aided-Civil-Drawing-ENCE204-2081-Chaitra.pdf
subject: Computer Aided Civil Drawing
level: BE · Year II / Part I
code: ENCE 204
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 1.5 hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
Define computer aided design & drafting. List out the advantage & disadvantage of CADD in civil engineering. [[3]]

@q 2
Write specific use of 3D drawings in engineering and list out common 3D, CADD software. [[2]]

@q 3
Explain the steps to change units and scales for a drawing in AutoCAD. [[2]]

@q 4
What are layers and blocks in AutoCAD? Explain how do you use block and layers while drafting. [[3]]

@q 5
Write the steps to set up a new dimension style in AutoCAD. [[2]]

@q 6
Write the steps to create different types of Array in AutoCAD. [[2]]

@q 7
Sketch a typical location map and site plan with detail information to be included. [[4]]

@q 8
List out the uses of SW-DTM. [[2]]

@q 9
Sketch and label a typical canal section in complete cut. [[2]]

@q 10
Sketch and label a typical hill road section in partial cut and fill. [[2]]

@q 11
List out the drawings to be included in municipal architectural drawings. [[2]]

@q 12
How is BIM different from traditional CAD-based drafting? [[2]]

@q 13
What is common data environment? Write its advantages. [[2]]
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

**Disadvantages of CADD:** high initial cost of hardware, licences and training; dependence on electricity and computers (data loss through power cuts, virus, hardware failure if there is no backup); skilled operators are required and there is a learning curve; file-format and version incompatibility; software piracy and licence problems; eye strain and a risk of blindly trusting the computer output without a check.

**Use in civil engineering:** architectural and structural drawings of buildings, road plan-profile and cross-sections, canal / bridge / dam drawings, drainage and pipe networks, survey and contour maps, earthwork quantities, 3D visualisation and as-built records.

@s 2
**Specific uses of 3D drawings in civil engineering:** (1) *visualisation* and client presentation (rendered images, walk-through and fly-through); (2) *design checking*, such as clash detection between architectural, structural and MEP elements; (3) *structural analysis models* (3D frames in STAAD.Pro, ETABS, SAP2000); (4) *terrain and earthwork models* (cut and fill volumes, slope analysis); (5) *quantity take-off and cost estimation*; (6) *construction sequencing (4D) and facility management* in BIM; (7) generating plans, sections and elevations automatically from one model.

**Common 3D software:** AutoCAD (3D), Revit, ArchiCAD, SketchUp, Civil 3D, Tekla Structures, 3ds Max, Rhino, Blender, Lumion / V-Ray (rendering), Navisworks, STAAD.Pro / ETABS (analysis models).

@s 3
**Steps to change units and scales for a drawing in AutoCAD**

1. **Units.** Type **UNITS** (UN). In the Drawing Units dialog: *Length* type = Decimal and precision 0.00 (or Architectural / Engineering if needed); *Angle* type = Decimal degrees, precision 0; choose the *Insertion scale* (units for blocks and drawings inserted: Millimetres or Meters); open *Direction* and keep the base angle as East; leave *Clockwise* unticked; OK.
2. **Drawing limits / area (optional).** Type **LIMITS** and give the lower-left (0,0) and the upper-right corner = *paper size × scale factor*, then **ZOOM → All**. Always draw the object *full size (1:1)* in the chosen unit.
3. **Scale factor** = 1/(plotting scale). For 1:100 the scale factor is 100: an A3 sheet (420 × 297 mm) corresponds to 42000 × 29700 mm of the real drawing. Text height on the sheet = required plotted height × scale factor (2.5 mm text at 1:100 is drawn as 250 units).
4. **Change the size of existing objects:** **SCALE** (SC): select the objects, specify the base point, then enter the scale factor (or use *Reference* to scale a known length to the correct length).
5. **Plotting scale:** in the PLOT / page-setup dialog choose the paper size and set the scale (for example 1 mm = 100 units for a drawing in millimetres) or, better, set the viewport scale in a layout (steps in the A3 layout answer). Use the **annotation scale** (status-bar button) for annotative text, dimensions and hatches.

*Example:* a 6 m wall drawn at 1:50 is drawn as 6000 units (in mm) and plots as 6000/50 = 120 mm on the sheet.

@s 4
**Layers.** A layer is like a transparent sheet on which one kind of object is drawn. Each layer has a name, colour, linetype, lineweight and states (on / off, freeze, lock, plot). A building drawing is divided into layers such as WALL, DOOR, WINDOW, COLUMN, BEAM, DIM, TEXT, HATCH, CENTRE, GRID and TITLE. **Blocks** are named groups of objects saved once and inserted many times (doors, windows, symbols, north arrow, title block).

**How they are used while drafting:**

1. Create the layers first (LAYER command) and make the right layer *current* before drawing; keep colour, linetype and lineweight **ByLayer**.
2. Draw the objects in the relevant layer; switch off or freeze the layers that are not needed (for example a structural plan is made by turning off furniture), lock the layers that must not be changed, and set DEFPOINTS or a viewport layer as non-plotting.
3. Create blocks of repeated items on layer **0**; when such a block is inserted on the layer WINDOW it takes the colour and linetype of WINDOW, and when the layer is switched off all the windows disappear.
4. Plot with different lineweights for different layers (thick for sections and walls, thin for dimensions and hatching), which gives a clear, standard drawing.
5. Use the layer states and the block library to modify a whole group in one step, and to keep the drawing organised for a team.

(The step-by-step procedure for making a block is: draw the object on layer 0, give BLOCK, enter the name, pick the base point, select the objects and click OK; insert it with INSERT and save it as a file with WBLOCK.)

@s 5
**Steps to set up a new dimension style in AutoCAD**

1. Type **DIMSTYLE** (D) or choose *Dimension Style* from the Annotate panel; the Dimension Style Manager opens.
2. Click **New**; enter the new style name (for example *ARCH-100*), *Start With* a base style (Standard), and tick *Annotative* if the style is annotative; click *Continue*.
3. In the dialog tabs set the following:
   - **Lines:** dimension line colour / lineweight, *extend beyond ticks*, *offset from origin* (about 2 mm) and extension line extension (about 2 mm).
   - **Symbols and Arrows:** arrowhead type (architectural tick for buildings, closed filled arrow for mechanical), arrow size (2.5 mm), centre marks.
   - **Text:** text style (with fixed height 0 in the style), text height (2.5 mm), position above the dimension line, alignment *aligned with dimension line*.
   - **Fit:** *Use overall scale of* = 100 for a drawing plotted at 1:100 (or *Annotative*), text placement.
   - **Primary Units:** unit format Decimal, precision 0 or 0.00, decimal separator ".", *Measurement scale factor* 1 (or 0.001 for mm → m), prefix / suffix if required.
   - **Alternate Units** and **Tolerances** if needed.
4. Click **OK**, then **Set Current** and **Close**. Dimension with DIMLINEAR, DIMALIGNED, DIMANGULAR, DIMRADIUS, DIMBASELINE and DIMCONTINUE.

@s 6
**Types of Array in AutoCAD:** (1) *Rectangular array*, objects in rows and columns; (2) *Polar array*, objects around a centre point; (3) *Path array*, objects along a path (line, polyline, arc, spline). The command is **ARRAY** (AR) (the old dialog box is ARRAYCLASSIC).

**Steps**

1. **Rectangular:** type ARRAYRECT, select the object, Enter; in the ribbon enter the number of *Columns* and *Rows* and the *distance between* columns (X) and rows (Y) (a negative value reverses the direction), the *Levels* (for 3D); press Enter or *Close Array*. Example: 5 columns at 3000 mm and 4 rows at 4000 mm for a column grid.
2. **Polar:** ARRAYPOLAR, select the object, specify the *centre point*; enter the *Number of items*, the *angle to fill* (360° for a full circle) and choose *Rotate items* yes / no, *Direction* (clockwise or counter-clockwise); Enter. Example: 8 bolts on a circle.
3. **Path:** ARRAYPATH, select the objects, select the *path curve*, enter the number of items or the spacing (Divide / Measure), choose *Align items* (to follow the tangent); Enter.

The result is one associative array object: edit its count and spacing in the Properties palette, or **EXPLODE** to separate copies.

@s 7
A **location map** shows where the site is in relation to the surroundings and a **site plan** shows the plot and what is built on it. They are drawn on the same sheet, as in the sketch below.

```figure caption="Typical location map (left) and site plan (right)."
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
a=fig.add_axes([0.01,0.02,0.47,0.88]); a.set_xlim(0,10); a.set_ylim(0,8); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title("Location map (1:5000, key to the site)",fontsize=7.4)
a.plot([0,10],[3.2,3.2],color=INK,lw=3); a.plot([6,6],[0,8],color=INK,lw=2); a.plot([0,6],[6.5,6.5],color=MUTED,lw=1.2)
xx=np.linspace(0,10,60); a.plot(xx,1.1+0.5*np.sin(xx*0.8),color="#1d6fb8",lw=3); tx(a,1.6,0.5,"river",size=6.4,color="#1d6fb8")
a.add_patch(plt.Rectangle((6.5,3.6),0.9,0.9,fc="#e5483f",ec=INK,lw=1)); ld(a,"SITE (plot no. 12)",(7.4,4.4),(8.0,6.0),size=6.6)
a.add_patch(plt.Rectangle((2.4,3.7),1.0,0.8,fc="#d9d9d9",ec=INK,lw=0.8)); tx(a,2.9,4.1,"school",size=5.8)
a.add_patch(plt.Rectangle((7.8,1.9),1.0,0.8,fc="#d9d9d9",ec=INK,lw=0.8)); tx(a,8.3,2.3,"temple",size=5.8)
tx(a,1.5,3.55,"Main road (12 m ROW)",size=5.8,ha="left"); tx(a,6.1,7.5,"Ring Road",size=5.8,ha="left",rotation=90)
a.annotate("N",xy=(9.2,7.5),xytext=(9.2,6.4),fontsize=8,ha="center",arrowprops=dict(arrowstyle="-|>",lw=1.2)); tx(a,1.2,7.4,"Scale 1:5000",size=6.4)
b=fig.add_axes([0.52,0.02,0.47,0.88]); b.set_xlim(0,14); b.set_ylim(0,11); b.set_aspect('equal'); b.set_xticks([]); b.set_yticks([]); b.set_title("Site plan (1:200)",fontsize=7.4)
b.add_patch(plt.Rectangle((0,0),14,2.2,fc="#e6e6e6",ec="none")); tx(b,7,1.1,"ROAD  (ROW 8 m)",size=6.6)
b.add_patch(plt.Polygon([(1,2.8),(13,2.8),(13,10.4),(1,10.4)],fc="none",ec=INK,lw=1.6,ls="-")); tx(b,7,10.75,"plot boundary 12.0 m × 7.6 m (boundary wall)",size=5.6)
b.add_patch(plt.Rectangle((2.8,4.8),6.4,4.2,fc="#cfd4dc",ec=INK,lw=1.4)); tx(b,6,7.3,"proposed\nbuilding",size=6.6)
dm(b,(1,3.4),(2.8,3.4),"",off=(0,0)); tx(b,1.9,3.65,"1.8",size=5.8)
dm(b,(9.2,3.4),(13,3.4),"",off=(0,0)); tx(b,11.1,3.65,"3.8",size=5.8)
dm(b,(5.4,2.8),(5.4,4.8),"front setback 2.0 m",off=(0.15,0),size=5.6,ha="left"); dm(b,(6.0,9.0),(6.0,10.4),"",off=(0,0)); tx(b,6.5,9.7,"rear 1.4",size=5.6,ha="left")
b.add_patch(plt.Rectangle((10.0,5.4),2.2,2.0,fc="#d9e6d2",ec=INK,lw=1)); tx(b,11.1,6.4,"septic\ntank",size=5.8)
b.plot([3.4,4.6],[2.8,2.8],color="#f4f4f4",lw=4); tx(b,4.0,3.15,"gate",size=5.4)
b.annotate("N",xy=(12.6,10.0),xytext=(12.6,8.9),fontsize=8,ha="center",arrowprops=dict(arrowstyle="-|>",lw=1.2))
```

**Information to be included**

*Location map (1:5000 or 1:10000):* the site marked clearly, the main roads with their names and widths, nearby landmarks (school, temple, hospital, river, bridge), the north point, the scale, and the distance to the main road / junction.

*Site plan (1:100, 1:200 or 1:500):* the **plot boundary** with dimensions and area; plot number (kitta number), ward and municipality; the **road width / right of way** and the road centre line; the **footprint** of the proposed building and of existing buildings with dimensions; **setbacks** from the road and from each boundary; the gate, driveway and parking; boundary wall; septic tank and soak pit, water tank, trees; the **north direction**; existing contours / ground levels; the **scale**; the neighbours' names and the plot of the adjoining owners; and the tabulated areas (plot area, ground coverage, floor area ratio, open space).

@s 8
**Uses of SW-DTM** (Softwel Digital Terrain Modelling software used for surveying and road design in Nepal):

1. Importing survey points (total station, GPS, level) and creating the **digital terrain model (TIN)** of the ground.
2. Producing **contour maps** at any interval, spot-height and grid maps.
3. Preparing the **longitudinal section (L-section)** and **cross-sections** along any alignment.
4. **Road, canal, pipeline and transmission-line design:** horizontal and vertical alignment, curve and widening design, super-elevation.
5. **Earthwork (cut and fill) volumes** from cross-sections or from the surface (bill of quantities).
6. Slope, aspect, catchment and drainage analysis, 3D view and surface rendering.
7. **Setting out data** (coordinates of centre line and offsets) for the construction survey.
8. Exporting drawings to AutoCAD (DXF / DWG) and plotting the drawings on standard sheets.

@s 9
A canal runs in **complete cut** (excavation) where the natural ground level is higher than the full supply level, so the canal trench is excavated below the ground and the ground itself forms the banks. The side slopes in cut are generally 1.5 H : 1 V or flatter in soil, and steeper in rock.

```figure caption="Typical canal section in complete cut."
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
fig,ax=plt.subplots(figsize=(7.4,2.9)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-14,14); ax.set_ylim(-3.4,2.4)
ax.add_patch(plt.Polygon([(-13,0),(-4.5,0),(-1.5,-2),(1.5,-2),(4.5,0),(13,0),(13,-3.0),(-13,-3.0)],closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.add_patch(plt.Polygon([(-1.5,-2),(1.5,-2),(3.75,-0.5),(-3.75,-0.5)],fc="#bcd7f2",ec="none"))
ax.plot([-4.5,4.5],[-0.5,-0.5],color="#1d6fb8",lw=1.1,ls="--")
ax.plot([-4.5,4.5],[0,0],color=INK,lw=1.4); ax.plot([-13,13],[0,0],color=INK,lw=1.4)
dm(ax,(-1.5,-1.55),(1.5,-1.55),"B = 3.0 m",off=(0,0.0),size=6.6)
dm(ax,(5.4,-2.0),(5.4,-0.5),"D = 1.5 m",off=(0.2,0),size=6.8,ha="left")
dm(ax,(-8.0,-0.5),(-8.0,0),"",off=(0,0)); ld(ax,"free board 0.5 m",(-8.0,-0.25),(-9.5,1.2))
ld(ax,"FSL",(3.5,-0.5),(7.5,0.9)); ld(ax,"side slope 1.5 H : 1 V (in cut)",(3.0,-1.0),(8.8,-1.6),ha="left")
dm(ax,(4.5,0.5),(10.5,0.5),"inspection path / berm 3.0 m (min.)",off=(0,0.45),size=6.6)
dm(ax,(-10.5,0.5),(-4.5,0.5),"berm 3.0 m",off=(0,0.45),size=6.6)
ld(ax,"canal bed (CBL)",(0.0,-2.0),(0.0,-2.8)); tx(ax,-9.5,-2.4,"natural ground (cut in ordinary soil)",size=6.6)
ld(ax,"NGL = bank level",(10.5,0.0),(12.0,1.5),ha="center")
ax.set_title("Typical canal section in complete cut",fontsize=8)
```

| Element | Typical value |
|---|---|
| Bed width B | 3.0 m |
| Full supply depth D | 1.5 m |
| Free board | 0.5 m (ground level at least 0.5 m above FSL) |
| Side slope in cut | 1.5 H : 1 V (ordinary soil) |
| Berm / inspection path | 3.0 m (minimum) at the ground level on one or both sides; the excavated spoil is used for the banks and the side drains |

Labels: natural ground level (NGL), canal bed, full supply level (FSL), free board, side slope, berm / path, depth of cut and bed width.

@s 10
On a steep hillside the road is built in **partial cut and fill** (side-hill section): the uphill half of the formation is excavated and the excavated material is used to form the downhill half, which reduces the quantity of spoil and the volume of earthwork.

```figure caption="Typical hill-road section in partial cut and fill."
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
fig,ax=plt.subplots(figsize=(7.4,3.1)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-12,13); ax.set_ylim(-5.0,5.0)
yl=lambda x:-0.3*x
xs=np.array([-11,11]); ax.plot(xs,yl(xs),color=INK,lw=1.0,ls="--")
xl=-2.5; xr=2.5; yp_l=0.0; yp_r=0.0+0.22
# cut face from (xl,0) going up-left at 0.5H:1V : point (xl-0.5t, t)
t=(-yl(xl)+0.0)  # placeholder
tc=(0-(-0.3)*(-xl))  # unused
# solve cut: ground y=-0.3x ; point (xl-0.5t, t): t=-0.3(xl-0.5t) -> t=-0.3xl+0.15t -> t=-0.3xl/0.85
tc=-0.3*xl/0.85; C=(xl-0.5*tc,tc)
# solve fill: (xr+1.5s, yp_r - s): yp_r-s=-0.3(xr+1.5s) -> yp_r-s=-0.3xr-0.45s -> s=(yp_r+0.3xr)/0.55
sf=(yp_r+0.3*xr)/0.55; Fp=(xr+1.5*sf,yp_r-sf)
ax.add_patch(plt.Polygon([(xl,yl(xl)),C,(xl,0)],closed=True,fc="#f3c9c4",ec="none"))
ax.add_patch(plt.Polygon([(xr,yl(xr)),(xr,yp_r),Fp],closed=True,fc="#d7e6c9",ec="none"))
prof=[(-11,yl(-11)),C,(xl,0),(-2.2,-0.38),(-1.9,0),(xr,yp_r),Fp,(11,yl(11))]
ax.plot([p[0] for p in prof],[p[1] for p in prof],color=INK,lw=1.6)
ax.plot([-1.9,xr],[0,yp_r],color=INK,lw=2.4)
tx(ax,C[0]+0.2,C[1]*0.35,"CUT",size=7,color="#b0413e"); tx(ax,3.2,-0.5,"FILL",size=7,color="#3d7a2e")
ld(ax,"catch drain (top of cut)",(C[0]-0.6,C[1]+0.05),(-9.0,3.6),ha="center")
ld(ax,"cut slope 0.5 H : 1 V (rock) / 1 H : 1 V (soil)",(-2.75,0.4),(-8.6,4.4),ha="left") if False else ld(ax,"cut slope 1 H : 2 V in hard soil / rock, 1 H : 1 V in ordinary soil",(C[0]+0.3,C[1]*0.55),(-3.0,4.5),ha="left")
ld(ax,"side drain 0.6 m",(-2.2,-0.38),(-7.2,-2.4)); ld(ax,"carriageway 3.0 m with 0.5 m shoulders, crossfall 5 %",(0.2,0.05),(4.0,3.0),ha="left")
ld(ax,"fill slope 1.5 H : 1 V",((xr+Fp[0])/2,(yp_r+Fp[1])/2),(8.4,1.2),ha="left"); ld(ax,"toe wall (dry stone / gabion)",Fp,(8.6,-3.9),ha="center")
dm(ax,(-2.5,-1.3),(2.5,-1.3),"formation width 5.0 m",off=(0,-0.4),size=6.6)
ld(ax,"original ground (NGL)",(-9.0,2.7),(-10.0,0.8),ha="center")
ax.set_title("Typical hill-road section in partial cut and fill (side-hill)",fontsize=8)
```

| Element | Typical value (single-lane hill road) |
|---|---|
| Formation width | 5.0 m (side drain 0.6 + shoulder 0.5 + carriageway 3.0 + shoulder / parapet 0.9) |
| Crossfall | 5 percent inward towards the drain |
| Cut slope | 1 H : 2 V in hard soil / soft rock, 1 H : 1 V in ordinary soil, 1 H : 4 V in hard rock (with breast wall where unstable) |
| Fill slope | 1.5 H : 1 V, with a toe wall / gabion; fill is placed in layers of 150 to 200 mm and compacted |
| Drains | side drain (0.6 m wide), catch drain above the top of the cut, cross-drainage (culvert / pipe) every 50 to 100 m |
| Original ground | dashed line; the cut and fill areas are hatched differently |

Labels: original ground, cut slope, side drain, carriageway and shoulders, crossfall, fill slope, toe wall, catch drain.

@s 11
**Drawings to be included in municipal architectural drawings (building permit submission):**

1. **Location map and site plan** with the plot boundary, the road width, setbacks, the north direction, and the surrounding features.
2. **Floor plans** of the basement / ground / typical / terrace floors with dimensions, room names and areas, door and window marks.
3. **Elevations** (front, rear and side), showing the heights, finish and the ground and roof levels.
4. **Sections** (at least two: one through the staircase), showing the floor-to-floor heights, plinth, sill, lintel and parapet heights.
5. **Foundation plan and the roof plan**; the door and window schedule.
6. **Septic tank and soak pit** (or sewer connection), the water supply, drainage and electrical layouts, the rainwater harvesting and the parking layout.
7. **Calculations** of the ground coverage and the floor area ratio (FAR), the area statement, and the supporting documents (land ownership certificate, citizenship, tax receipt, blue print).

@s 12
| Point | Traditional CADD (AutoCAD drafting) | BIM |
|---|---|---|
| Basic element | lines, arcs, circles and text (geometry only) | intelligent objects (wall, beam, door) with properties and relations |
| Dimensions | mostly 2D, separate drawings | 3D model plus automatically generated 2D views |
| Information | graphic only | geometry, material, cost, phase, manufacturer, maintenance data |
| Changes | each drawing edited by hand; errors and inconsistency | one change updates plans, sections, elevations and schedules |
| Quantities | measured manually or exported with effort | automatic schedules and quantity take-off |
| Collaboration | sharing of files; drawings overlaid | shared federated model in a common data environment, clash detection |
| Dimension of data | 2D / 3D | 3D plus time (4D), cost (5D), operation (6D) |
| Use | documentation of the design | whole life cycle: design, construction, operation |
| Software | AutoCAD, DraftSight | Revit, ArchiCAD, Tekla, Civil 3D |

@s 13
A **Common Data Environment (CDE)** is the single, agreed source of information for a project: a cloud-based digital platform (for example Autodesk Construction Cloud / BIM 360, Aconex, Trimble Connect, SharePoint) in which all the project documents, models and drawings of all the parties are created, shared, reviewed and approved in a controlled way (ISO 19650: Work in progress, Shared, Published, Archive).

**Advantages:** one source of truth, so everybody works on the latest version; no duplicate or conflicting files; better collaboration and communication among the architect, structural, MEP engineers, contractor and client; controlled access, security and an audit trail of who changed what and when; version control and approval workflow; time and cost saved (less rework, quick design review and coordination); easy handover of the as-built records at the end of the project.
