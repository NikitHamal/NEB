---
file: NEBians-IOE-Past-Paper-Civil-Engineering-Materials-CE103-2081-Kartik.pdf
subject: Civil Engineering Materials
level: BE · Year I / Part I
code: CE 103
year_bs: 2081 Kartik
cal: BS
year_ad: 2024
stream: BCE
time: 1½ hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course, 2080 batch). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
How does the weathering affect the civil engineering materials? What is the major difference between ductile and brittle failure of materials? [[1+1]]

@q 2
Explain about why and where the use of stone is preferred in engineering constructions. [[3]]

@q 3
Write the essential constituents of good brick earth with their percentage composition and function. Define glazing with its function. [[2+1]]

@q 4
Define hydraulicity of lime. Write a short note on lean lime. [[1+1]]

@q 5
Explain briefly the manufacturing of cement by WET PROCESS with its flow diagram. In what conditions it is considered a better process than the dry process? [[3+1]]

@q 6
What are the things to be considered while using ordinary cement mortar for constructions? [[2]]

@q 7
What does a seasoning of timber mean and why is it necessary? Write the distinctive properties of hard wood and soft wood. [[1.5+1.5]]

@q 8
What is main principle of heat treatment of metal? Describe annealing, normalizing and quenching. [[1+1+1+1]]

@q 9
Differentiate between the paint and varnish. Write down the process of application of paint in new wood surface. [[1.5+1.5]]

@q 10
Compare between bitumen and tar. Describe about anti-termite treatments. [[2+2]]

<!-- SOLUTIONS -->

@s 1
**Effects of weathering.** Weathering is the combined action of rain, humidity, temperature changes, frost, wind, sunlight (UV) and atmospheric gases on exposed materials. Its effects on civil engineering materials are:

| Material | Effect of weathering |
|---|---|
| Stone | Disintegration and surface flaking by frost, thermal cycles and acid rain; leaching of the cementing matter; loss of polish |
| Brick and masonry | Efflorescence, spalling, loss of mortar, softening of under-burnt bricks |
| Concrete | Frost scaling, cracking from wetting and drying, carbonation, sulphate and chloride attack, and corrosion of reinforcement |
| Steel | Rusting (corrosion), loss of section, and loss of paint |
| Timber | Shrinking, swelling, cracking, fungal decay and insect attack |
| Paint, plastics, bitumen | Fading, chalking, embrittlement and oxidation (hardening, cracking) |

Weathering lowers strength, durability and appearance, so materials are selected, protected (coatings, damp-proofing) and maintained accordingly.

**Ductile and brittle failure**

```figure caption="Stress-strain behaviour: a ductile material (mild steel) yields, strains plastically and necks before breaking; a brittle material (cast iron, concrete, glass) fractures suddenly at small strain."
import numpy as _np
fig,axs=plt.subplots(1,2,figsize=(6.0,2.3))
e=_np.linspace(0,0.25,300)
s=_np.where(e<0.002,250/0.002*e,_np.where(e<0.02,250,_np.where(e<0.17,250+150*(1-_np.exp(-(e-0.02)*25))-0*(e-0.02),400-(e-0.17)*1500)))
s=_np.where(e>0.23,_np.nan,s)
axs[0].plot(e,s,color="#2c6fb0",lw=1.6); axs[0].set_title("Ductile (mild steel)",fontsize=8); axs[0].annotate("yield",(0.01,250),(0.05,120),fontsize=7,arrowprops=dict(arrowstyle="->",lw=0.6))
axs[0].annotate("necking, fracture",(0.22,300),(0.12,60),fontsize=7,arrowprops=dict(arrowstyle="->",lw=0.6))
eb=_np.linspace(0,0.004,50); axs[1].plot(eb,300/0.004*eb,color="#c0392b",lw=1.6); axs[1].set_title("Brittle (cast iron, glass)",fontsize=8)
axs[1].annotate("sudden fracture, no yield",(0.004,300),(0.0008,120),fontsize=7,arrowprops=dict(arrowstyle="->",lw=0.6))
for a in axs: a.set_xlabel("strain",fontsize=7); a.set_ylabel("stress (MPa)",fontsize=7); a.tick_params(labelsize=6); a.grid(alpha=0.25)
fig.tight_layout()
```

| | Ductile failure | Brittle failure |
|---|---|---|
| Deformation before fracture | Large plastic deformation, elongation and necking | Almost none (small elastic strain only) |
| Warning | Gives visible warning (deflection, cracking) | Sudden, without warning |
| Energy absorbed | Large (toughness) | Small |
| Fracture surface | Cup-and-cone, fibrous, dull | Flat, granular, bright |
| Examples | Mild steel, copper, aluminium | Cast iron, concrete, glass, stone, brick |

@s 2
**Why stone is preferred.** Stone is used because it

- has high compressive strength and hardness (granite 100 to 250 MPa),
- is very durable and resists weather, wear, fire and chemicals, with little maintenance,
- has a natural, pleasing and dignified appearance and takes a polish,
- is available locally in hilly and mountainous regions like Nepal, so transport cost is low,
- has large mass, which gives stability against overturning and sliding to gravity structures,
- can be dressed to any shape and gives a long life (monuments, temples and old bridges survive for centuries).

**Where it is used**

| Use | Stone |
|---|---|
| Foundations and retaining walls, breast walls, gabions | Rubble, boulders, granite |
| Walls and masonry (random rubble, coursed rubble, ashlar) | Sandstone, limestone, granite |
| Dams, bridge piers and abutments, culverts, canal linings, river training works | Hard, dense stone, rubble masonry |
| Roads: road metal, railway ballast; aggregate for concrete | Crushed basalt, quartzite, granite |
| Flooring, stairs, steps, paving, cladding, skirting and facing | Marble, granite, slate |
| Roofing (slate), lintels, columns, kerbs, monuments | Slate, sandstone, marble |

Stone is not preferred where light weight, tension or seismic flexibility is required (it is heavy and weak in tension), and where cheap bricks are readily at hand.

@s 3
**Constituents of good brick earth**

| Constituent | Percentage | Function |
|---|---|---|
| Alumina (clay) | 20 to 30 % | Gives plasticity, so the earth can be moulded; binds the particles; excess causes shrinkage, warping and cracks on drying |
| Silica (sand) | 50 to 60 % | Gives strength, hardness, and prevents shrinkage, cracking and warping; maintains shape. Excess makes the brick brittle and weak because the particles are not bound together |
| Lime | 3 to 5 % (not above 10 %) | Acts as a flux, binds silica particles at kiln temperature; must be in fine powder (lumps cause lime blowing and popping); excess melts the brick and it loses shape |
| Iron oxide | 5 to 6 % | Acts as a flux that helps fusing silica, gives the red colour and hardness and strength; excess gives dark blue or black colour |
| Magnesia | about 1 % | Gives a yellow tint, decreases shrinkage, and improves soundness; excess causes decay |

Harmful ingredients: alkalies (efflorescence and fusing), pebbles and gravel (not uniform, weak), organic matter (leaves holes when burnt), gypsum and sulphates (efflorescence, cracks).

**Glazing** is the process of coating the surface of burnt clay products (tiles, bricks, sanitary ware, pipes) with a thin layer of glass-like material. It is done by throwing common salt into the kiln at the end of burning (salt glazing) or by applying a slip of glass-forming material (felspar, quartz, lead oxide) and fusing it. Function: makes the surface smooth, glossy, impervious, hygienic, stain, acid and weather resistant, gives decoration and colour, and makes cleaning easy.

@s 4
**Hydraulicity of lime** is the property of lime to set and harden under water, or in the absence of air, by the action of water on the clay (silica, alumina) impurities it contains: the clay combines with the lime to form insoluble calcium silicates and aluminates. Depending on the clay content, hydraulic limes are classified as

| Class | Clay content | Setting |
|---|---|---|
| Feebly hydraulic | 5 to 10 % | 20 to 30 days |
| Moderately hydraulic | 11 to 20 % | 10 to 20 days |
| Eminently hydraulic | 21 to 30 % | 2 to 7 days |

(Fat lime has less than 5 % clay and is non-hydraulic.)

**Lean lime** (poor, impure or meagre lime). It is made by burning limestone that has more than 30 % clay and other impurities. Properties: slakes very slowly and with little heat; the paste is thin and gives a small increase in volume; sets slowly, hardens weakly, poor binding and adhesion; the colour is muddy white or grey; low strength. Uses: inferior mortar for ordinary masonry, plastering in dry situations, and as a filler or cheap ground work; it is not used for good-quality work.

@s 5
**Wet process of manufacture of cement.** In the wet process the raw materials are made into a slurry with water. Steps:

1. **Raw materials** are limestone (calcareous: about 75 to 80 %) and clay (argillaceous: about 20 to 25 %).
2. **Crushing and mixing with water.** Limestone is crushed in crushers to small pieces; clay is washed in a wash mill with water to form a slurry. Both are ground in a ball or tube mill into a fine slurry containing 35 to 50 % water.
3. **Blending in slurry tanks.** The slurry is stored in tanks, the lime content is tested and corrected by adding clay or limestone, and the mix is kept homogeneous by compressed air or agitators.
4. **Burning in the rotary kiln.** The corrected slurry is fed to the upper end of a long inclined rotating kiln (about 4 m diameter, 120 to 150 m long, 1 to 3 rpm). Hot gases (from pulverised coal, oil or gas) flow in the opposite direction. In the drying zone (up to about 400 °C) the water evaporates; in the calcining zone (about 800 to 900 °C) limestone gives CaO and CO$_2$; in the burning (clinkering) zone (1400 to 1500 °C) lime combines with silica, alumina and iron oxide to form clinker nodules, 3 to 20 mm in size.
5. **Cooling and grinding.** The hot clinker is cooled in a cooler, stored, and then ground in a ball mill with 2 to 4 % gypsum, which controls the setting (retards the flash set of C$_3$A).
6. **Storage and packing.** The cement is stored in silos, tested and packed in 50 kg bags.

```figure caption="Wet process of manufacture of cement (flow diagram)."
fig,ax=plt.subplots(figsize=(4.4,5.6)); ax.axis("off")
steps=["Raw materials: limestone (calcareous) + clay (argillaceous)",
"Crushing; clay washed with water in the wash mill (slurry of 35-50 % water)",
"Slurry tanks: blending and correction of the lime : clay ratio",
"Rotary kiln: drying, calcination (800-900 °C), clinkering (1400-1500 °C)",
"Cooling of clinker, storage of clinker",
"Ball / tube mill: clinker + 2-4 % gypsum ground to fine powder",
"Storage silos, testing and packing in bags (50 kg)"]
n=len(steps)
for i,s in enumerate(steps):
    y=0.95-i*0.152
    ax.text(0.5,y,s,ha="center",va="center",fontsize=7.6,wrap=True,transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.5",fc="#eef2f8" if i%2==0 else "#dbe7f5",ec=INK,lw=0.9))
    if i<n-1: ax.annotate("",xy=(0.5,y-0.1),xytext=(0.5,y-0.052),xycoords="axes fraction",arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.1))
ax.set_xlim(0,1); ax.set_ylim(0,1)
```

**When the wet process is the better process.** The wet process is preferred when

- the raw materials are soft and naturally wet or can be easily slurried (chalk, marl, soft limestone and clay), so crushing and drying are not needed,
- the composition of the raw material varies, because the slurry can be sampled, tested and corrected easily and mixed more uniformly, giving better quality and uniform cement,
- the raw material contains much moisture, clay is plastic and sticky, or the quarry is next to a water source,
- fuel is cheap and the dust nuisance must be small (less dust), and the quality control is more important than fuel economy.

Its disadvantages are the large fuel consumption (to evaporate the water), a longer kiln and a lower output compared with the dry process.

@s 6
**Points to be considered while using ordinary cement mortar**

1. **Proportion:** select the cement : sand ratio for the work (1:3 to 1:4 for plastering and foundations, 1:4 to 1:6 for superstructure walls), measured by volume in boxes.
2. **Materials:** use fresh cement (not lumpy), clean, sharp, well graded sand free from silt, clay and organic matter, and clean potable water (no oil, acid, alkali or salt).
3. **Mixing:** mix dry sand and cement to a uniform colour, then add water and mix to the right workability. Water-cement ratio about 0.4 to 0.5 (just enough to be workable); avoid too much water.
4. **Use within time:** mortar must be used within 30 minutes of adding water (the initial setting time); mortar that has started to set must not be retempered or used again. Prepare in small batches.
5. **Wetting units:** soak bricks (and stones) in water before use so they do not absorb the mortar water. Joints are usually 10 mm thick, filled completely, and the units are bedded properly.
6. **Curing:** keep the masonry and plaster wet for at least 7 days (10 days for plaster in hot weather) and protect it from sun, wind, rain and frost.
7. **Others:** do not use cement mortar with hot cement; take care of compatibility with the lime; and for water retaining works use waterproofing admixtures.

@s 7
**Seasoning of timber** is the process of removing the moisture (sap) from freshly felled green timber (moisture content 30 to 200 %) in a controlled way to bring it down to a level near the equilibrium moisture content in service, usually 10 to 15 %. It is done by natural (air) seasoning or by artificial methods (kiln, water seasoning, chemical, electrical seasoning).

It is necessary because it reduces shrinkage, warping, twisting and cracking in use; increases strength, hardness and stiffness; makes the timber lighter; prevents attack of fungi and insects (they need more than 20 % moisture); makes it easier to saw, join, paint and polish; and allows preservatives to penetrate.

**Hardwood and softwood**

| Property | Hardwood | Softwood |
|---|---|---|
| Source | Broad-leaved (deciduous) trees | Cone-bearing (coniferous) trees |
| Growth | Slow growing | Fast growing |
| Weight and density | Heavy, dense | Light |
| Strength | Strong in tension, compression and shear, durable | Weaker, lower durability (except some, e.g. deodar) |
| Annual rings | Distinct, close, dark | Less distinct, wide, light colour |
| Grain | Close grained, difficult to work | Straight, open grained, easily worked |
| Resin | Little or none | Resinous |
| Fire | Burns slowly, resistant | Burns easily |
| Examples | Sal, teak, shisham, oak, mahogany | Pine, deodar, spruce, fir, chir |
| Uses | Doors, windows, beams, columns, furniture, flooring | Roof trusses, shuttering, partitions, packing, light framing |

@s 8
**Principle of heat treatment.** Heat treatment is the controlled heating of a metal in the solid state to a definite temperature, holding it there (soaking) until the temperature is uniform, and then cooling it at a suitable rate, in order to change its microstructure (phase transformation, grain size, carbide distribution) and thereby its properties, such as hardness, strength, ductility, toughness, machinability and internal stresses, without changing the shape and the chemical composition.

**Annealing.** The steel is heated to about 30 to 50 °C above the upper critical temperature (about 800 to 900 °C for medium carbon steel), soaked, and cooled very slowly in the furnace (switch off the furnace). Result: coarse pearlite, soft, ductile structure; removes internal stresses, refines grain, improves machinability and ductility, and prepares the metal for cold working.

**Normalizing.** Heated to 30 to 50 °C above the upper critical temperature, soaked, and cooled in still air. The faster cooling gives a fine pearlite structure with uniform fine grain; the metal is harder and stronger than the annealed steel but less than the quenched; removes internal stress from casting, forging and rolling and refines the structure.

**Quenching.** Heating to above the critical temperature (about 800 to 900 °C), soaking, and then rapid cooling by plunging into water, brine or oil. Austenite transforms to martensite, so the steel becomes very hard, strong and brittle with high internal stress; hence it is generally followed by tempering (reheating to 150 to 650 °C) to restore some toughness. Used for tools, springs, gears and cutting edges.

@s 9
**Paint and varnish**

| | Paint | Varnish |
|---|---|---|
| Composition | Pigment and base in a vehicle (oil), with drier and thinner | Resin (shellac, copal, amber, synthetic) dissolved in oil, turpentine, or spirit; no pigment |
| Appearance | Opaque, coloured film that hides the surface | Transparent film that shows the grain of the wood |
| Purpose | Protect and decorate, and conceal the surface | Protect and enhance the natural beauty (polish) |
| Durability | Good against weather | Less durable outdoors, may crack in sunlight |
| Use | Walls, metal, wood, doors and windows | Furniture, interior wood, doors, floors |

**Process of applying paint on a new wood surface**

1. **Preparation:** the timber must be well seasoned and dry. Clean the surface and rub it with sand paper (glass paper) to make it smooth; remove dust, dirt and oil.
2. **Knotting:** the knots are treated with a coat of shellac (knotting varnish) or red lead to stop resin bleeding.
3. **Priming:** apply one coat of priming paint (a ready-mixed wood primer, or pigment, red lead and linseed oil) with a brush to fill the pores, to give a base and to give good adhesion. Allow it to dry for 24 hours.
4. **Stopping:** fill the nail holes, cracks and dents with putty (whiting and linseed oil), then rub down with fine sand paper when dry.
5. **Undercoat:** apply one or two undercoats of paint of the matching colour in thin coats, drying and rubbing down lightly in between.
6. **Finishing coat:** apply the final coat of paint (flat, semi gloss or glossy) with a brush in even strokes, in the direction of the grain, after the undercoat has dried. Two coats may be required for a smooth, uniform finish. The surface is protected from dust and moisture while drying.

@s 10
**Bitumen and tar**

| Bitumen | Tar |
|---|---|
| Residue of distillation of crude petroleum (or natural deposit) | Product of destructive distillation of coal, wood or peat |
| Contains hydrocarbons, soluble in carbon disulphide | Contains hydrocarbons together with phenols and free carbon; soluble in toluene, less in carbon disulphide |
| Dark brown to black, solid or semi-solid, higher viscosity | Black, more fluid, thinner (graded as road tars RT-1 to RT-5) |
| Less temperature susceptible, durable, higher softening point | More temperature susceptible (soft in heat, brittle in cold), ages faster |
| Poorer adhesion to wet aggregate, but better weathering | Better adhesion to aggregate, weaker durability, hardens fast |
| Not poisonous, little odour | Poisonous, strong smell (phenols) |
| Used in road surfacing and roofing, waterproofing, damp-proof courses | Used in surface dressing, priming coats, timber preservation, pipe coating |

**Anti-termite treatment** protects the building against subterranean termites, which eat timber and cellulose materials and travel through mud tubes.

*(a) Pre-construction treatment (soil poisoning).* Chemical emulsion (1 % chlorpyrifos, or imidacloprid, or others as per IS 6313) is applied in the excavated foundation at the bottom and the sides (about 5 litres per m²), to the backfill and plinth filling, along the junction of the wall and the floor, around pipes and services and as a continuous chemical barrier all around the building (apron, 1 m wide).

*(b) Post-construction treatment.* Holes of 12 mm diameter are drilled at 300 mm c/c along the plinth, floor joints and the wall, at about 50 mm from the wall, and the chemical is injected under pressure. Trenches are dug along the walls, treated and refilled; infested wood is removed and treated.

*(c) Other measures.* Treat timber with preservatives (boric acid, borax, creosote, CCA); use physical barriers such as a stainless steel mesh, GI sheets (termite shields), or a rich concrete apron; keep timber and cellulose materials away from the ground and moist places, remove tree stumps and old wood from the site, ensure drainage and ventilation and carry out periodic inspections. Termite treatment should be repeated every 5 years or so.
