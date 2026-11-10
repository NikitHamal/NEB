---
file: NEBians-IOE-Past-Paper-Computer-Aided-Civil-Drawing-ENCE204-2082-Chaitra.pdf
subject: Computer Aided Civil Drawing
level: BE · Year II / Part I
code: ENCE 204
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 1.5 hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
What is Computer Aided Design and Drafting? Explain its uses in civil engineering. [[3]]

@q 2
Write specific use of 2D drawings in civil engineering and list out common 2D, CADD software. [[2]]

@q 3
Explain different types of coordinate system in AutoCAD. [[2]]

@q 4
Write in details how to create a block in AutoCAD. Explain its advantages. [[3]]

@q 5
Differentiate between model space and layout space and their uses in AutoCAD. [[3]]

@q 6
Sketch and label typical canal cross section in complete fill. [[2]]

@q 7
Sketch and label typical hill road section in complete fill. [[2]]

@q 8
List out the detail information to be included in location map and site plan. [[2]]

@q 9
Sketch and label typical section of 4 m height cantilever retaining wall. [[2]]

@q 10
How will you create L-section and Cross section from contour map using SW-DTM? Write in detail steps. [[5]]

@q 11
Define Building Information Modeling (BIM) and common data environment (CDE). [[2]]

@q 12
What are the differences between BIM and Computer Aided Design and Drafting? [[2]]
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
**Specific uses of 2D drawings in civil engineering:** floor plans, elevations and sections of buildings; site, location and layout plans; foundation and structural reinforcement details; road plan and profile, cross-sections; canal, drainage and pipe-network layouts; survey and contour maps; working (construction) drawings, shop drawings and as-built drawings for submission to the municipality and for tendering.

**Common 2D CADD software:** AutoCAD, AutoCAD LT, BricsCAD, DraftSight, ZWCAD, LibreCAD, Civil 3D (2D and DTM), MicroStation, SW-DTM (survey and road design software developed in Nepal).

@s 3
**Coordinate systems in AutoCAD**

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

For 3D work, *cylindrical* (`r<θ,z`) and *spherical* (`r<θ<φ`) formats are used, and the dynamic input (DYN) shows the same values at the cursor.

@s 4
**Creating a block in AutoCAD (steps)**

1. Draw the object (door, window, tree, north arrow, column symbol) at full size, preferably on layer 0 so that it takes the properties of the layer on which it is inserted.
2. Type **BLOCK** (B). In the Block Definition dialog box: enter the *Name* (e.g. DOOR-900); click *Pick point* and select the *base (insertion) point*; click *Select objects* and pick the drawing, then Enter; choose *Convert to block*, *Retain* or *Delete*; set the *block unit* (mm or m) and the *Annotative / Allow exploding* options; give a description; click OK.
3. Place it with **INSERT** (I): select the block name, give the insertion point, scale (X, Y, Z) and rotation (or tick *Specify on-screen*).
4. To use the block in other drawings, save it as a file with **WBLOCK** (W: Source = Block or Objects, set the file name and path). Edit it with **BEDIT**; modify the definition and *all* inserted copies update. **EXPLODE** converts it back to simple objects. Attributes (ATTDEF) can be added to carry data, such as the text fields of a title block.

**Advantages of blocks:** the drawing needs far less memory (the geometry is stored once and each insertion is only a reference); drawing is faster because standard symbols (doors, windows, furniture, structural symbols) are reused from a library; uniform and standard symbols; changing the block definition updates every copy automatically; easy scaling, rotating and replacing; blocks with attributes give schedules and quantities automatically (data extraction); and the drawing is better organised.

@s 5
**Model space and layout (paper) space**

| Point | Model space | Layout (paper) space |
|---|---|---|
| Nature | the unlimited 2D / 3D working area (the *Model* tab) in which the actual objects are drawn full size | a sheet of paper (the *Layout* tabs) laid out for printing |
| Scale | always 1:1, one view | each viewport shows the model at its own scale (1:50, 1:100 and others) |
| Contents | the design: plan, sections, details, 3D model | sheet border, title block, viewports, notes, scale bar, annotative dimensions and text |
| Number | one only | many layouts (A3, A1 and others) in the same file, each with several viewports |
| Use | designing, drafting and modelling | plotting and presentation, to arrange several views at different scales on one sheet |

The viewport is a window from the layout into the model space; the model is never copied, so a change in model space is seen in all layouts at once.

@s 6
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

@s 7
A hill road is in **complete fill** where the road formation is higher than the natural ground across the whole width and the road is carried on an embankment, with a catch drain at the toe of the uphill fill and a toe wall / gabion on the downhill side where the fill is high.

```figure caption="Typical hill-road section in complete fill."
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
fig,ax=plt.subplots(figsize=(7.4,3.0)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-12,13); ax.set_ylim(-5.6,4.2)
xs=np.array([-11,11]); ax.plot(xs,-0.3*xs,color=INK,lw=1.0,ls="--")
yl=lambda x:-0.3*x
top=1.5; xl=-2.5; xr=2.5
# fill slopes 1.5:1 from platform edges down to ground
gl=(xl-1.5*0+0,top)
# uphill toe: solve ground y=-0.3x with slope from (xl,top) going left-down at 1.5H:1V
def toe(x0,y0,s):
    # point (x0+s*t, y0-t) on ground  -0.3(x0+s*t)=y0-t
    t=(y0+0.3*x0)/(0.3*s-1)*-1 if False else (-0.3*x0-y0)/(1-0.3*s)*-1
    return None
import numpy as _n
def solve(x0,y0,s):
    # s=+1.5 for downhill (right), -1.5 for left; ground y=-0.3x ; point=(x0+s*t, y0-t)
    t=(y0+0.3*x0)/(1-0.3*s)
    return (x0+s*t,y0-t)
L=solve(xl,top,-1.5); R=solve(xr,top,1.5)
ax.add_patch(plt.Polygon([L,(xl,top),(xr,top),R],closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.plot([-11,L[0]],[yl(-11),L[1]],color=INK,lw=1.4); ax.plot([R[0],11],[R[1],yl(11)],color=INK,lw=1.4)
ax.plot([xl,xr],[top,top],color=INK,lw=2.2)
tx(ax,0,top-0.6,"compacted fill",size=7); 
dm(ax,(xl,top+0.45),(xr,top+0.45),"formation width 5.0 m",off=(0,0.5),size=6.6)
ld(ax,"side drain 0.6 m",(-2.3,top),(-6.0,3.3)); ld(ax,"fill slope 1.5 H : 1 V",(R[0]-1.2,R[1]+0.9),(8.8,1.5),ha="left")
ld(ax,"camber / crossfall 5 % (inward)",(0.5,top+0.04),(7.0,3.4),ha="left")
ld(ax,"toe wall / gabion (if fill > 2 m)",R,(9.8,-4.2),ha="center")
ld(ax,"catch drain",(L[0]-0.3,L[1]),(-9.0,-1.6)); ld(ax,"original ground (NGL)",(-9.0,2.7),(-9.5,3.9),ha="center")
ax.set_title("Typical hill-road section in complete fill",fontsize=8)
```

| Element | Typical value (single-lane hill road) |
|---|---|
| Carriageway | 3.0 m with 0.5 m shoulders; total formation 5.0 m including the side drain |
| Crossfall / camber | 5 percent (1 in 20), inward slope towards the hill-side drain |
| Side drain | 0.6 m wide, 0.5 m deep (lined or unlined) |
| Fill slope | 1.5 H : 1 V (flatter for loose soil, protected by turfing / bio-engineering) |
| Toe wall | dry stone or gabion wall at the toe where the fill height is more than about 2 m |
| Compaction | in layers of 150 to 200 mm |

@s 8
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

@s 9
A cantilever RCC retaining wall of **4 m height** has the following proportions (H = 4.0 m): base width B = 0.6H = 2.4 m; base slab thickness = H/8 = 0.5 m; stem height 3.5 m; stem thickness 0.40 m at the base and 0.25 m at the top (the batter is on the soil side); toe 0.6 m; heel 1.4 m (0.6 + 0.4 + 1.4 = 2.4 m).

```figure caption="Typical 4 m cantilever retaining wall with dimensions and details."
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
fig,ax=plt.subplots(figsize=(7.4,3.5)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.2,7.4); ax.set_ylim(-1.4,5.2)
ax.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(5.6,4.0),(5.6,0.5)],fc="#eadfc9",ec="none")); hatch(ax,1.0,5.5,3.95,n=14,l=0.4)
ax.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.5))
ax.add_patch(plt.Rectangle((-0.1,-0.1),2.6,0.1,fc="#9a9a9a",ec=INK,lw=0.6)); ax.plot([-1.0,5.6],[0.5,0.5],color=INK,lw=0.9)
ax.add_patch(plt.Rectangle((1.2,-0.4),0.3,0.3,fc="#cfd4dc",ec=INK,lw=0.9))
ax.add_patch(plt.Rectangle((1.9,0.55),0.5,1.0,fc="#d9e6d2",ec="none")); tx(ax,4.0,2.0,"granular filter (drainage layer)",size=6.4)
ax.plot([0.6,0.6],[0.5,3.9],color=INK,lw=0.0); ax.plot([0.62,0.62],[0.62,3.9],color="#b0413e",lw=0.8,ls="--")
ax.plot([0.12,0.12,2.3],[0.5,0.12,0.12],color="#b0413e",lw=0.8,ls="--")
dm(ax,(-1.9,0.0),(-1.9,4.0),"H = 4.0 m",off=(-0.15,0),size=7,ha="right"); dm(ax,(-0.5,0.5),(-0.5,4.0),"stem 3.5 m",off=(-0.15,0),size=6.6,ha="right")
dm(ax,(0,-0.55),(0.6,-0.55),"0.60",off=(0,-0.3),size=6.2); dm(ax,(0.6,-0.55),(1.0,-0.55),"0.40",off=(0,-0.3),size=6.2); dm(ax,(1.0,-0.55),(2.4,-0.55),"1.40",off=(0,-0.3),size=6.2)
dm(ax,(0,-1.15),(2.4,-1.15),"B = 2.40 m (toe 0.60 + stem 0.40 + heel 1.40)",off=(1.6,0),size=6.4,ha="left")
dm(ax,(2.6,0.0),(2.6,0.5),"",off=(0,0)); tx(ax,2.7,0.12,"slab 0.50 m",size=6.2,ha="left")
dm(ax,(0.6,4.35),(0.85,4.35),"top 0.25",off=(0,0.3),size=6.2)
ld(ax,"weep holes 100 mm @ 2 m c/c",(0.95,1.0),(-1.6,1.8),ha="center") if False else ld(ax,"weep hole 100 mm dia. @ 2 m c/c (PVC)",(0.80,0.85),(4.6,0.95),ha="left")
ld(ax,"PCC 1:3:6 blinding, 100 mm",(2.0,-0.05),(4.8,-0.45),ha="center"); ld(ax,"shear key (optional)",(1.35,-0.25),(4.3,-1.0),ha="center") if False else None
ld(ax,"main bars at the earth face (tension)",(0.9,2.4),(5.9,2.6),ha="center") if False else tx(ax,4.6,3.0,"backfill (granular)",size=6.6)
ld(ax,"RCC M25, Fe500: main bars 16 @ 150 at back face,\ndistribution 10 @ 200, cover 50 mm (earth face)",(0.66,2.9),(4.4,4.7),ha="center")
ax.set_title("Typical section of a 4 m high cantilever retaining wall",fontsize=8)
```

Details to be labelled: the main reinforcement in the stem on the earth face (tension face) and in the toe at the bottom and in the heel at the top; distribution (temperature) bars; cover (50 mm on the earth face, 75 mm under the base); weep holes of 100 mm at 2 m c/c; granular filter / drainage layer behind the stem; PCC blinding of 100 mm below the base; granular backfill; and the ground levels on both sides. The materials are grade M25 concrete and Fe500 steel. (The bar sizes in the figure are typical; the design gives the actual values.)

@s 10
If only a contour map (a drawing with contour lines) is available, first scan / digitise it, or import the contour polylines as DXF with their elevations, and use *Surface → Create DTM from contours*; then continue with the steps below to get the contours (re-generated at the required interval), the L-section and the cross-sections.

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

@s 11
**Building Information Modelling (BIM)** is a process of creating and managing an intelligent, 3D digital model of a facility, in which every element (wall, beam, door, pipe) carries information about its geometry, material, cost, schedule and maintenance. Plans, sections, elevations, schedules and quantities are all extracted from the same model, so they are always consistent. Revit, ArchiCAD, Tekla Structures, Civil 3D and Navisworks are BIM tools.

A **Common Data Environment (CDE)** is the single, agreed source of information for a project: a cloud-based digital platform (for example Autodesk Construction Cloud / BIM 360, Aconex, Trimble Connect, SharePoint) in which all the project documents, models and drawings of all the parties are created, shared, reviewed and approved in a controlled way (ISO 19650: Work in progress, Shared, Published, Archive).

**Advantages:** one source of truth, so everybody works on the latest version; no duplicate or conflicting files; better collaboration and communication among the architect, structural, MEP engineers, contractor and client; controlled access, security and an audit trail of who changed what and when; version control and approval workflow; time and cost saved (less rework, quick design review and coordination); easy handover of the as-built records at the end of the project.

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
