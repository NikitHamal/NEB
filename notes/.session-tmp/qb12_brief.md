# SHARED BRIEF — NEBians "Question Bank, Grade 12" (Physics & Chemistry chapters)

You are writing ONE chapter of this book. This brief is the verified research and
the house rules. `/data/workspace/NEB/notes/AUTHORING.md` is the binding contract —
**read all 14 sections of it yourself before writing a line.** This brief does not
replace it; it adds the book-specific facts.

---

## 0. Your file and its EXACT frontmatter

The curriculum spine `/data/workspace/NEB/notes/curriculum/qbank12.md` is LAW.
`title` verbatim; `area` from the enclosing `# PART:` line; `[R]` means no hours,
so `hours: 0`.

| File | Frontmatter |
|---|---|
| `notes/content/qbank12/unit-02.md` | subject: Question Bank / grade: 12 / unit: 2 / title: "Physics: Unit-wise Objective Question Bank" / hours: 0 / area: Physics |
| `notes/content/qbank12/unit-03.md` | unit: 3 / title: "Physics: Unit-wise Subjective Question Bank" / area: Physics |
| `notes/content/qbank12/unit-04.md` | unit: 4 / title: "Physics: Model Question Sets and Predicted Questions" / area: Physics |
| `notes/content/qbank12/unit-05.md` | unit: 5 / title: "Chemistry: Unit-wise Objective Question Bank" / area: Chemistry |
| `notes/content/qbank12/unit-06.md` | unit: 6 / title: "Chemistry: Unit-wise Subjective Question Bank" / area: Chemistry |
| `notes/content/qbank12/unit-07.md` | unit: 7 / title: "Chemistry: Model Question Sets and Predicted Questions" / area: Chemistry |

Always `subject: Question Bank`, `grade: 12`, `hours: 0`.

Write titles without quotes if they contain no colon problem — actually they DO
contain a colon, so write them quoted:
`title: "Physics: Unit-wise Objective Question Bank"` — the parser strips quotes.

---

## 1. VERIFIED exam pattern (both subjects)

From the **official NEB model-question PDFs** (Physics Sub. code 1021, Chemistry
Sub.Code 3021), fetched this session:

```
Time: 3 hrs.        Full Marks: 75      Pass Marks: 32
Attempt all the questions.
Group A   Rewrite the correct options of each question in your answer sheet.  (11 x 1 = 11)
Group B   Short answer questions                                              (8 x 5 = 40)
Group C   Long answer questions                                               (3 x 8 = 24)
```

- **All questions are compulsory** — "Attempt all the questions". There is **no
  free choice between questions.**
- Choice exists **only as internal "Or" alternatives**. Observed: about **2 "Or"
  questions in Group B and 2 in Group C** (occasionally 1). Real positions seen:
  Physics 2079-model Q17, Q19 (B) and Q21, Q22 (C); Physics 2081 Q12, Q18 (B) and
  Q20, Q21 (C); Chemistry 2081 Q12, Q17 (B) and Q20, Q21 (C); Chemistry 2082 Q14,
  Q15 (B) and Q20 (C).
- Group B questions are split internally **1+2+2, 2+3, 1+1+3 or 1+4**.
  Group C splits are commonly **2+2+2+2, 3+3+2, 5+3, 2+3+3**.
- Written paper 75 + internal 25 (practical 16, trimester 6, class participation 3).
- In recent years (2082) the Group A MCQ booklet is **handed out 30 minutes after
  the exam starts**; answers still go on the same answer sheet.

## 2. VERIFIED specification grid

**There is NO published per-unit marks grid.** moecdc.gov.np publishes
specification grids only for Grades 9/10. The only real CDC "SG" figure found is
the **cognitive-level weightage**, printed on page 6 of the official NEB Chemistry
Model Question 2079 PDF:

| Cognitive level | Weightage in SG | Marks in paper | % |
|---|---|---|---|
| Knowledge | 12 | 12 | 16% |
| Understanding | 18 | 18 | 24% |
| Application | 21 | 21 | 28% |
| Higher ability (analyse/evaluate/create) | 24 | 24 | 32% |
| **Total** | **100** | **75** | **100%** |

In that sample paper the Higher-ability marks sat on Group A Q11, Group B Q13, Q14,
Q17 and Group C Q21. Knowledge sat on Q6, Q7 (A) and Q12c, Q15, Q19 (B).

Any "marks per unit" table on a coaching site is **unverified** — never present one
as CDC's. What you MAY use, because it is in the official CDC curriculum, is the
**teaching-hour weight** per unit (below). Say plainly that hours are a proxy for
marks, not a published grid.

## 3. VERIFIED CDC teaching hours

**Physics 12 (total theory 128 h + 32 practical = 160)**

| Area | Hours | Units |
|---|---|---|
| Mechanics | 22 | Rotational dynamics 7, Periodic motion 6, Fluid statics 9 |
| Heat & Thermodynamics | 12 | First law 6, Second law 6 |
| Waves & Optics | 26 | Wave motion 2, Mechanical waves 4, Waves in pipes & strings 4, Acoustic phenomena 5, Nature & propagation of light 3, Interference 2, Diffraction 3, Polarization 3 |
| Electricity & Magnetism | 35 | Electrical circuits 6, Thermoelectric effects 3, Magnetic field 9, Magnetic properties of materials 5, Electromagnetic induction 6, Alternating currents 6 |
| Modern Physics | 33 | Electrons 4, Photons 3, Semiconductor devices 6, Quantization of energy 8, Radioactivity & nuclear reaction 6, Recent trends 6 |

**Chemistry 12 (total theory 128 h + 32 practical = 160)**

Volumetric Analysis 8, Ionic Equilibrium 10, Chemical Kinetics 7, Thermodynamics 8,
Electrochemistry 7, Transition Metals 5, Studies of Heavy Metals 15, Haloalkanes 8,
Haloarenes 3, Alcohols 7, Phenols 4, Ethers 2, Aldehydes & Ketones 10, Carboxylic
Acid & Derivatives 9, Nitro Compounds 3, Amines 7, Organometallic Compounds 2,
Chemistry in the Service of Mankind 4, Cement 4, Paper & Pulp 3, Nuclear Chemistry 2.

By area: **General & Physical 40 · Inorganic 20 · Organic 55 · Applied 13.**
Organic Chemistry is 43% of the course. Electricity & Magnetism + Modern Physics
together are 53% of Physics.

---

## 4. YEAR TAGGING — the rule you must not break

Tag a question `(NEB 2081)` **only** if it is in the verified list in §5/§6 below,
using the year stated there. Everything else carries **no year tag at all** — keep
the question, drop the year. Never invent a year. Never write "(NEB 2080)" on a
question you composed.

Acceptable tag forms:
- `(NEB 2081)` — appeared in that board paper.
- `(NEB 2079 model)` — appeared in the official NEB model question set.
- `(NEB 2078, 2082)` — appeared in both.

**Caveat to honour:** the paper nebexam.com labels "Physics 2078 Old Question" is
published elsewhere as the 2078 *model* question. Where you use it, tag it
`(NEB 2078 — board/model, label disputed)` or just `(NEB 2078)` once; if you have a
"sources and verification" note in your chapter, mention the dispute there.

---

## 5. VERIFIED PHYSICS past questions (use these, with these years)

### 2079 MODEL (official NEB PDF, Sub. code 1021)
**Group A:** product of moment of inertia and angular velocity; simple pendulum bob
0.40 kg, T = 2.0 s, amplitude 0.15 m, PE at extreme 0.044 J → KE at mean point; what
causes earthquakes; percentage of original radioactive atoms left after 4 half-lives;
two wave pulses travelling toward each other — which diagram is the superposition;
which property of sound is affected by change in air temperature; internal energy of
an ideal gas depends on what; in which process is work done by the gas maximum;
neutral temperature 500 °C with cold junction 0 °C — % change in inversion
temperature when cold junction becomes 20 °C; in which circuit is maximum power
dissipated; why are laminated cores used in transformers.
**Group B:** Q12 define SHM [1], derive T for mass m on a vertical spring of force
constant k [3], time period inside a satellite [1]; Q13 Bernoulli's principle [1],
liquid ρ = 1200 kg/m³, A = 1.0 cm², B = 20 mm², v_A = 10 cm/s → speed at B [2] and
pressure difference [2]; Q14 p–V diagram of a petrol engine and its working [3],
compare petrol and diesel efficiency via compression ratio [2]; Q15 sonometer wire
75 cm resonates with a fork, shortened by 0.5 cm gives 3 beats → fork frequency [3],
vibrator 120 Hz standing wave → speed of the progressive wave [2]; Q16 state Lenz's
law and justify that it supports conservation of energy [1+2], magnet moved between
coils C₁ and C₂ → direction of induced current in each [2]; Q17 principle of
potentiometer and why it acts as a voltmeter of infinite resistance [1+1], meter
bridge balance at 20 cm, R and X doubled then interchanged → new balance point [2],
galvanometer and battery interchanged [1] — **Or** Kirchhoff's two laws [2], meter
bridge null at 60.0 cm, 5 Ω in series with S gives null at 50 cm → find R and S [3];
Q18 graph of maximum KE vs frequency for sodium → threshold frequency [1], work
function [2], Planck's constant from the graph [2]; Q19 Millikan oil drop:
expression for the charge on a drop of radius r falling at constant velocity v with
a free-body diagram [2], expression when the electric force exceeds the weight [1],
field that balances a drop of mass 1.3×10⁻¹⁴ kg carrying 4 electrons [2] — **Or**
which diode characteristic is used in rectification [1], full-wave rectifier circuit
[1], truth table for a NOR/OR/AND/NAND network including states at E, F, G [3].
**Group C:** Q20 significance of the negative energy of an electron in an orbit [1],
which transition emits λ = 275 nm [3], expression for λ when an electron jumps
n₂ → n₁ [2], wavelength of the second Balmer line with R = 1.09×10⁷ m⁻¹ [2]; Q21
green light 546 nm, double slit d = 0.50 mm, screen 0.80 m, ten fringes; alternative
grating 3000 lines/cm → width of ten fringes [2], angle of the second-order maximum
[2], which experiment is more accurate [1]; how to tell a polaroid from a
non-polaroid pair of sunglasses [1]; angle of incidence for complete polarization
from water μ = 1.3 [2] — **Or** how does intensity change if the distance increases
four times [1]; train at 30 m/s sounding 262 Hz, another train at 18 m/s in the
opposite direction → frequency heard approaching and receding [2+2]; maximum
pressure variation 3.0×10⁻² Pa, f = 1000 Hz, v = 344 m/s, bulk modulus 1.42×10⁵ Pa
→ maximum displacement [3]; Q22 what is a choke coil [1], why it is preferred to a
resistor in a.c. [2], three a.c. circuits carrying equal currents: effect of
increasing the frequency [3] and the difference in opposition if the a.c. emf is
replaced by an equivalent d.c. [2] — **Or** define one ampere from the force between
parallel conductors [1], explain the contraction of a solenoid when current flows
[2], conductor of linear mass density 0.2 g/m with zero tension in a 1 T field →
current [3], torque on a 100-turn 100 cm² coil in 10 T [2].

### 2078 (board/model, label disputed)
**Group A:** correct formula for radius of gyration; horizontal stream of air blown
under one pan of a beam balance; height of capillary rise on the Moon if it is h on
Earth; coefficient of performance of an ideal refrigerator between the ice point and
room temperature; p–V diagram A→B via C and back via D — which area is the total
work done; which directly affects the quality of sound; diffraction pattern when red
light is replaced by white light; circular coil of N turns, radius r, current I —
which quantity is the product; coil of N turns, area A, current I — what does NIA
represent; what happens to the neutral temperature if the cold junction temperature
is decreased; the point where seismic waves start.
**Group B:** Q12 define surface tension [1], relation with surface energy [2], two
coalescing raindrops and terminal velocity [2]; Q13 define moment of inertia [1],
why the Earth's angular velocity increases near the Sun [2], the Earth shrinks
suddenly → length of the day [2] — **Or** Bernoulli's principle [1], derive
Bernoulli's equation [2], why water squirts further when the hose is partly covered
by a thumb [2]; Q14 define harmonics in music [1], frequency of a 30 cm flute open
at both ends in the first harmonic, v = 330 m/s [2], change of pitch when the bus
starts moving [2]; Q15 second law of thermodynamics [1], does a refrigerator violate
it [2], heat engine with Q₁/T₁ → Q₂/T₂: efficiency expression [1] and when the
efficiency is zero [1]; Q16 magnetic flux density between two weak bar magnets on a
steel yoke (0.02–0.04 T): define B, why a Hall probe is unsuitable, how to determine
B with a current-carrying wire; Q17 ε = −N(dφ/dt): what the symbols mean [2],
significance of the negative sign [1], why a copper ball P falls more slowly than Q
through a magnetic field [2]; Q18 UV of frequency 1.5×10¹⁵ Hz on aluminium of work
function 6.6×10⁻¹⁹ J — show v_max = 8.6×10⁵ m/s [3], effect of increasing intensity
on v_max [2]; Q19 Bohr's postulates [3], Lyman series: frequency of the photon for
the second excited state → ground state [2] — **Or** p–n junction diode symbol and
polarity [1], complete a bridge rectifier by adding diodes [2], effect if one diode
stops conducting, with a sketch of V across R_L [2].
**Group C:** Q20 earthquake, restoring force F = −Ax: prove the motion is SHM [2],
show v = ±ω√(A²−x²) [2], maximum speed of a building shaken by 21 Hz S-waves of
amplitude 0.05 m [2], why tall buildings are more susceptible to low-frequency
S-waves [2] — **Or** potentiometer to measure the emf of a test cell: why there is
no balance point and what to change [2], how to recognise the balance point [1],
standard cell 1.50 V at 37.5 cm and the test cell at 25.0 cm → emf [2], why it is
more precise than an ordinary voltmeter [2]; Q21 LRC circuit emf/current vs time
graph: sign of the phase constant [2], phasor diagram [2], is the circuit more
inductive or capacitive [2], should the inductance be raised or lowered to increase
the power in the load [2]; Q22 meaning of quantization of charge [2], Millikan drop
of weight 1.5×10⁻¹⁴ N held between plates 10 mm apart at 470 V: condition for the
drop to be stationary with the forces [2], charge on the drop [2], effect of a stray
alpha particle [2] — **Or** derive N = N₀e^(−λt).

### 2080 (board)
**Group B:** Q12 define radius of gyration [1], MI of a thin uniform rod about a
perpendicular axis through its centre [2], teacher on a rotating platform 1.5 → 5.0
rad/s, ratio of final to initial KE [2] — **Or** y = r sin ωt: define amplitude and
calculate the acceleration [1+2], a uniform spring cut in half — force constant and
frequency [1+1]; Q13 Stokes' law: define coefficient of viscosity and how to
determine η by this method [1+2], horizontal pipe 25 cm² at 3 m/s feeding 15 cm² →
pressure change [2]; Q14 first law of thermodynamics [1], derive C_p − C_v = R [2],
efficiency of a heat engine [2]; Q15 thermo-emf vs hot-junction temperature graph:
what is the thermoelectric effect, define θ_n and θ_i, effect on θ_i if the cold
junction moves to −10 °C, one application [1+2+1+1]; Q16 Biot–Savart law: state it
[1], B at the centre of a circular coil [3], direction [1]; Q17 first overtone of a
stretched string: define harmonic and overtone [1], frequency of this mode [2],
frequency if the tension is quadrupled [2] — **Or** Newton's formula for the
velocity of sound and its discrepancy [2], Laplace's correction [2], why sound waves
are called pressure waves [1]; Q18 p–n junction: formation of the potential barrier
[2], why a large current flows under forward bias [1], truth table for outputs Y₁
and Y₂ [2]; Q19 compare β-particles and γ-rays (mass, charge, ionizing, penetrating)
[2], define decay constant [1], activity of 10²² carbon-14 nuclei with t½ = 5700 yr [2].
**Group C:** Q20 YDSE: define interference [1], calculate the fringe width β [3],
effect of immersing the apparatus in a liquid [2], grating of 5000 lines/cm with the
second order at 30° → wavelength [2]; Q21 Bohr's postulates [2], radius of the nth
orbit of hydrogen [3], photoelectric KE-vs-frequency graph → threshold frequency,
Planck's constant and work function in eV — **Or** electron beam between parallel
plates: show the path is a parabola [3], what is a cross field and one use [2],
Bragg's law [1], largest interplanar distance 10 Å → upper limit of X-ray wavelength
[2]; Q22 define the rms value of an a.c. [2], series LCR: impedance expression [2],
resonance [1], resonant frequency [2], quality factor [1] — **Or** Lenz's law and
conservation of energy [1+2], energy stored in an inductor [3], step-down 2200 V →
220 V with 5000 primary turns, 90% efficiency and 8 kW output → secondary turns and
input power [1+1].

### 2081 (board)
**Group A:** rotational KE = E and MI = I → angular momentum; displacement–time
graph of SHM → maximum velocity; capillary tubes of radii 4 mm and 2 mm → ratio of
rise; isochoric process 127 °C → 227 °C, ratio of initial to final pressure; block
diagram of a heat engine → efficiency; distance between two consecutive particles in
the same phase; a polarizer is used to …; which material is ferromagnetic; inversion
temperature 600 °C and neutral temperature 310 °C → cold-junction temperature;
Nepal's 220 V supply → peak voltage; P-wave passing from solid to liquid → velocity.
**Group B:** Q12 define moment of inertia [1], MI of a uniform rod about one end
perpendicular to its length [2], flywheel I = 0.32 kg m² at 120 rad/s driven by a
50 W motor → KE and frictional couple [2] — **Or** spring k = 18 N/m, m = 0.15 kg,
extension +4 cm: define SHM [1], maximum acceleration and time period [2], total
energy expression with KE/PE graph [2]; Q13 relation between surface tension and
surface energy [2], N drops of terminal velocity v₁ coalesce → relation for v₂ [2]
and its value for N = 2, v₁ = 0.4 m/s [1]; Q14 p–V diagram of a cyclic process:
define an indicator diagram [1], work done in process II [2], identify processes
I–IV [2]; Q15 Laplace's correction to Newton's formula and the corrected formula
[3], wavelength in air at 25 °C for 256 Hz given v₀ = 330 m/s [2]; Q16 potentiometer
circuit — derive the internal resistance r [3], converting a galvanometer into an
ammeter [2]; Q17 B due to a straight conductor by Ampère's circuital law [3], 0.5 m
wire carrying 2 A in 0.4 T → maximum and minimum force [2]; Q18 explain quantization
of charge [2], ion of specific charge 4.40×10⁷ C/kg in 0.4 T at 3.52×10⁵ m/s →
radius [2], why X-rays are used in Millikan's experiment [1] — **Or** define
half-life and mean life [2], 2 g of material with t½ = 50 yr → mean life [2], decay
graph with t½ = 10 yr → estimate T₃ [1]; Q19 what is rectification and full-wave
rectification with two diodes [1+2], truth table for A′, B′ and Y [2].
**Group C:** Q20 open organ pipe standing wave: nodes and antinodes [1], derive the
frequency [2], effect on the transverse wave velocity if the string radius is
doubled [2], horn of 400 Hz with Δf = 60 Hz as a car crosses → car velocity, v = 340
m/s [3] — **Or** plane wavefront → spherical wavefront [2], interference and the
resultant intensity for constructive and destructive superposition of two waves of
intensity I [3], 5890 Å on a grating of 6000 lines/cm → angle of the second order and
whether the third order is possible [2+1]; Q21 voltage sensitivity of a moving-coil
galvanometer and the factors it depends on, and why a radial field is used [2+1],
Faraday's laws and the instantaneous emf at t = 3 s from φ(t) [3], energy stored in
an inductor [2] — **Or** B at the centre of a circular coil by Biot–Savart [3],
indium antimonide slice 2.5 mm thick, 150 mA, 0.5 T, Hall voltage 8.75 mV → carrier
density [2], force per unit length between parallel conductors and the definition of
one ampere [3]; Q22 photoelectric effect and Einstein's equation [2], velocity of an
electron in the first excited state [2], de Broglie wavelength of an electron
accelerated through 300 V [3].

### 2082 (board)
**Group A:** difference between the MI of a rod about one end and about its centre;
displacement–time curve → velocity at the mean position; two equal raindrops falling
at 0.15 m/s combine → new terminal velocity; what happens in an adiabatic process;
efficiency of a Carnot engine between the steam point and the ice point; example of
a transverse wave; which phenomenon is NOT explained by Huygens' construction; B at
the centre of a circular coil of radius R carrying I; relative permeability in terms
of susceptibility χ; square coil of 10⁻² m² perpendicular to 10³ T → flux; the point
where seismic waves start.
**Group B:** Q12 why a ballet dancer stretches and folds her arms [2], relation
between torque and moment of inertia [2], why a wrench with a longer arm [1] — **Or**
show the total energy in SHM is constant [3], PE-vs-displacement graph [1], time
period of a simple pendulum on the Moon [1]; Q13 define laminar and turbulent flow
[2], p = 4×10⁴ N/m² at v = 2 m/s with A = 200 cm² → pressure where A = 50 cm² [3];
Q14 Carnot engine of 25% efficiency with sink at 9 °C — by how much must the source
temperature rise for 50% [3], first law and conservation of energy [2]; Q15 effect of
temperature and pressure on the velocity of sound [2], train at 10 m/s towards a
cliff sounding 600 Hz → frequency of the echo heard by the driver [3]; Q16 the two
Kirchhoff's laws [2], balanced Wheatstone bridge from Kirchhoff's laws [3]; Q17
Lenz's law [1], graph of induced emf vs time for a rotating coil [1], energy stored
in an inductor [2]; Q18 symbol and truth table of a NAND gate [2], full-wave
rectification with two diodes [3]; Q19 oil drop m = 3×10⁻¹¹ g, r = 2×10⁻⁶ cm with 10
excess electrons — terminal velocity with no field and in 3×10⁵ V/m downward [1+1],
why E ⊥ B in Thomson's method [2], use of X-rays in Millikan's experiment [1] —
**Or** define decay constant and half-life [2], derive N = N₀e^(−λt) [3].
**Group C:** Q20 stationary waves, prove the node spacing is λ/2 [3], guitar string
1.5 m, ρ = 7800 kg/m³, Y = 2×10¹¹ N/m², strain 1% → stress and second-mode frequency
[3], open organ pipe figure: which mode and its frequency [1+1] — **Or** bright and
dark fringes are equally spaced in YDSE [3], grating of 500 lines/mm with the second
order at 30° → wavelength [3], state and prove Brewster's law [2]; Q21 series LCR at
f = 500/π Hz: phase angle and which leads [2+1], meaning of impedance [1], two
parallel wires carrying I₁ and I₂ at separation r: force per unit length [2], nature
of the force [1], force if r is halved [1] — **Or** variation of thermo-emf with
hot-junction temperature [3], potentiometer circuit [3].

### 2082 MODEL
**Group A:** torque due to gravity about the centre of mass; l vs T² graph for a
simple pendulum; angle of contact when a liquid neither rises nor falls; cyclic
process ABCDA with a semicircular ABC — work done; Q added, U increases and W
positive → which process; closed organ pipe with fundamental 330 Hz → second mode;
μ = 1.5 → polarizing angle; inversion 600 °C and neutral 320 °C → cold junction; rms
value from a peak voltage; oil-drop field to move the drop upward at the same speed;
region of initiation of seismic energy.

### PHYSICS repeats evidenced across two or more verified papers (genuinely high-yield)
- "Point where seismic waves start" — 2078, 2082, 2082-model
- Moment of inertia / radius of gyration definition — 2078, 2080, 2081, 2082-model
- Surface tension ↔ surface energy relation — 2078, 2081
- Terminal velocity of coalescing raindrops — 2078, 2081, 2082 (MCQ)
- Lenz's law + conservation of energy — 2078, 2080, 2082
- Energy stored in an inductor — 2081, 2082
- Full-wave rectification with two diodes / bridge rectifier — 2078, 2080, 2081, 2082
- Millikan oil drop and "why X-rays" — 2079-model, 2081, 2082
- Bohr postulates + nth-orbit radius — 2078, 2080, 2081
- Thermocouple neutral / inversion temperature — 2078, 2079-model, 2080, 2081, 2082-model
- Wheatstone / meter bridge from Kirchhoff's laws — 2079-model, 2082, 2082-model
- Biot–Savart + B at the centre of a circular coil — 2080, 2081, 2082-model
- Laplace's correction to Newton's formula — 2080, 2081
- Doppler effect numerical — 2078, 2079-model, 2081, 2082
- Diffraction-grating order/wavelength numerical — 2079-model, 2080, 2081, 2082
- Derivation of N = N₀e^(−λt) — 2078, 2082

---

## 6. VERIFIED CHEMISTRY past questions (use these, with these years)

### 2079 MODEL (official NEB PDF, Sub.Code 3021)
**Group A:** equivalent weight of K₂Cr₂O₇ in K₂Cr₂O₇ + 3H₂SO₄ + 5(COOH)₂ → …; at
equilibrium what happens to [H⁺] if [OH⁻] increases; rate doubles per 10 °C rise —
how many times from 10 °C to 100 °C; from C + O₂ → CO₂ (ΔH = −x) and 2CO + O₂ →
2CO₂ (ΔH = −y), the enthalpy of formation of CO; product when a red-hot copper wire
reacts with steam; for which manufacturing process is a Bessemer converter used;
sodium phenoxide + methyl bromide gives …; identify X in a nitrobenzene → aniline
reduction; reagent to distinguish a phenol from a carboxylic acid; colourless
sweet-smelling liquid A that forms phosgene in air and a sleep-inducing drug with
acetone — product on reduction in neutral medium; oxygen-containing compound
oxidised to a carboxylic acid of molecular mass higher by 14 units.
**Group B:** Q12 HCl labelled 2 M: what it means, molarity vs molality, significance
of the normality factor, liquor ammonia 25% (w/w) of specific gravity 0.91 →
molarity [1+1+1+2]; Q13 (a) rate of reaction vs rate constant [2] (b) 2A + B →
product, a three-experiment kinetics table → order with respect to A and B, the rate
constant, and the rate at [A] = 0.5 M, [B] = 0.4 M — **Or** four metals A, B, C, D
and their displacement behaviour → activity series; galvanic cell from E° = −0.76 V
and +0.77 V, its EMF, and the feasibility of C²⁺ + 2D²⁺ → C + D³⁺; Q14 ammonia added
to the sulphate of a coinage metal A gives a blue precipitate B dissolving to a deep
blue solution C: identify A, B, C with reactions [3], electronic configuration of A
[1], method of purification [1]; Q15 what is a d–d electron transition and the
characteristics of transition metals [1+4]; Q16 structural formula and IUPAC name of
the tertiary alcohol C₄H₁₀O, and Victor Meyer's method to distinguish 1-propanol
from 2-propanol [1+4]; Q17 X + CH₃MgBr then acidic hydrolysis → Y; Y + acidified
KMnO₄ → Z; all give a positive iodoform test: identify X, Y, Z with IUPAC names [3],
product of Z with dilute NaOH [2] — **Or** X heated with acetone gives a hypnotic
drug and forms carbonyl chloride in air: identify X [1], formation of X from ethanol
[2], product with conc. HNO₃ [1], convert X into acetylene [1]; Q18 (a) why the nitro
group is meta-directing, and nitrobenzene with (i) Zn/NH₄Cl (ii) LiAlH₄ [2+2] (b)
isomers of C₂H₇N [1]; Q19 give one example each of Reimer–Tiemann, Perkin
condensation, Williamson ether synthesis, Cannizzaro and Sandmeyer reactions [5×1].
**Group C:** Q20 Ostwald's dilution law α = √(Ka/C): derive it [3], what it tells you
[2], do strong electrolytes obey it [1], 0.1 M ethanoic acid 1.34% ionized →
dissociation constant [2] — **Or** Hess's law with an illustration [2], from ΔH_c of
C, H₂ and C₂H₂ (−394, −286, −1300 kJ/mol) find ΔH_f of acetylene [4], energy profile
diagrams of exothermic and endothermic reactions [1+1]; Q21 C₂H₄O₂ has functional
isomers A (turns blue litmus red) and B (fruity smell): formation of A via a Grignard
reagent [1], convert A into B [2], a test to distinguish A from methanoic acid [1],
arrange CH₃COOH, ClCH₂COOH, FCH₂COOH, C₆H₅COOH in decreasing acidic strength [2],
identify A and B [2] — **Or** amines: a test to distinguish an alkyl from an aryl
amine [2], separate ethylamine and dimethylamine by Hoffmann's method [3], increasing
basic strength of propylamine, ethylmethylamine and trimethylamine [1], convert
ethanamine into methanamine [2]; Q22 (a) classification of cement on the basis of
hardening and setting [2] (b) differentiate paper and pulp [2], artificial and
natural radioactivity [2], addition and condensation polymers [2].

### 2078 MODEL (Sub. code 3021)
**Group A:** equivalent weight of H₃PO₃ in 2NaOH + H₃PO₃ → Na₂HPO₃ + 2H₂O; K_sp of
chalk 9.3×10⁻⁸ → solubility in g/L; first-order reaction with rate 2.4×10⁻⁵ mol/L
and k = 3.0×10⁻⁵ s⁻¹ → concentration; what happens when a lead storage battery is
discharged; general electronic configuration of transition metals; which ore is
concentrated by froth flotation; product when nitrobenzene is electrolytically
reduced; which is the π-bonded organometallic compound with ethene first
synthesised; effect of calcium sulphate on cement; removal of which component
increases fibre–fibre bonding strength in paper; α/β/γ deviation figure.
**Group B:** Q12 Na₂CO₃ standard solution against H₂SO₄: how completion is detected,
is it a primary standard and why [1+1], 2.16 g Na₂CO₃ into 400 mL deci-normal H₂SO₄
— further H₂SO₄ needed [3] — **Or** derive k = (2.303/t) log(a/(a−x)) and show t½ is
independent of the initial concentration [3], first-order reaction 50% in 10 s →
time for 90% [2]; Q13 H₂O(l) → H₂O(s) entropy table at −1/0/+1 °C: ΔS_universe at
condition 3 [1], spontaneity at 0 °C [1], K for the fusion of ice at 1 °C and the
effect of temperature [3]; Q14 octahedral distortion figure: why it occurs by CFT
[2], why [Cu(H₂O)₆]²⁺ is blue [1], Fe³⁺ vs Fe²⁺ stability [1], why such elements are
good catalysts [1]; Q15 ore X: calcination gives a black precipitate W (group II
basic radical) and roasting gives metal M plus a gas that turns acidified K₂Cr₂O₇
green — identify M, the calcination reaction, the action of the gas on K₂Cr₂O₇, and
convert X into its vitriol; Q16 table P = C₃H₇Br, Q = C₆H₁₄, R = CH₂O, S = C₂H₄O,
T = C₃H₈O — convert P → Q, obtain P from T, and the reactions P → R and P → S [5] —
**Or** aromatic A (one Cl on the ring) + trichloroethanal/conc. H₂SO₄ → insecticide
B; A + a two-carbon acid chloride/anhyd. AlCl₃ → C: obtain A from benzenediazonium
chloride, identify B and C, and explain why aqueous NaOH reacts less readily with A
than with chloroethane; Q17 from p-hydroxyazobenzene, C₆H₅N₂Cl, C₆H₅NH₂, C₆H₅NO₂,
C₆H₆ build a reaction chain with conditions [5]; Q18 isomeric alcohols of C₃H₈O with
IUPAC names and Victor Meyer's test to distinguish them [2+3]; Q19 (a) define
condensation polymerization and give the monomer structures of Bakelite (b)
differentiate OPC and PPC cement.
**Group C:** Q20 (a) is Zn(OH)₂ precipitated when 100 mL containing 0.22 g NaOH is
added to 1 L of saturated Zn(OH)₂ (K_sp = 1.8×10⁻¹⁴), and why [5] (b) KOH of pH 8
diluted 1000 times → pH [3] — **Or** heat of formation of ethyl alcohol from
ΔH_c(EtOH) = −330 kcal, ΔH_f(CO₂) = −94 and ΔH_f(H₂O) = −68.5 [4]; from
E°(Cu²⁺/Cu) = +0.34 V and E°(Ag⁺/Ag) = +0.80 V write the cell notation with anode and
cathode, the cell potential at 1 M/25 °C/1 atm, and whether AgNO₃ can be stored in a
copper vessel; Q21 primary alcohol of molecular mass 46 with NaOH/I₂, with ethanoic
acid/conc. H₂SO₄, with conc. H₂SO₄, and how to distinguish it from methanol [5].

### 2081 (board)
**Group A:** equivalent weight in a given reaction; dissociation constant of acetic
acid at a given % ionisation; if the rate equals the rate constant, what is the
order; E° of four metals P, Q, R, S → decreasing reactivity; what feature of
transition metals makes them catalysts; which metal ion is green in its salts;
Benzene → X → Y, and Y with an acid anhydride and sodium acetate gives which acid;
which compound gives a positive Tollens' AND iodoform test; which is the most basic;
which compound reacts with chlorobenzene to form DDT; to prepare a primary alcohol
via a Grignard reagent, start from which compound.
**Group B:** Q12 from two standard reduction potentials write the cell notation with
anode and cathode [1], the standard emf [2], and the complete cell reaction [2] —
**Or** define heat of combustion [1], and from ΔH_c of C, S and CS₂ calculate ΔH_f
of CS₂ [4]; Q13 define pH, find [OH⁻] of a solution of pH 4.7, and the weight of
NaOH needed to produce these ions in 1 L [1+4]; Q14 coinage metal M of group IB: draw
the blast furnace used in smelting [2] and the reactions during matte formation [3];
Q15 preparation of corrosive sublimate [1], its action with KI, SnCl₂ and NH₃
solutions [3], and two uses [1]; Q16 benzene → nitrobenzene, then convert
nitrobenzene into azoxybenzene, p-aminophenol, aniline and azobenzene; Q17 identify
A and B [2], obtain 2,3-dimethylbutane from A [1], convert B into propene [1], and
give the product of A with sodium methoxide [1] — **Or** sequence the reactions among
benzoin, toluene, benzenediazonium chloride, phenol, benzaldehyde and benzene; Q18
write equations for carbonylation, Fehling's test, aldol condensation, Williamson
ether synthesis and the 2,4-DNP test [5]; Q19 give an example of a 1° and a 2°
alcohol and use Victor Meyer's test to distinguish them [1+4].
**Group C:** Q20 (a) is the solution a primary standard and why [2] (b) equivalence
point vs end point [2] (c) a numerical [4] — **Or** define half-life and deduce that
t½ ∝ initial concentration (zero order) [1+2], a four-experiment rate table → the
rate law, k and its unit, and the missing value [2+2+1]; Q21 compound A whose vapour
causes loss of consciousness and which with conc. HNO₃ gives a tear-gas component:
prepare A from an isomer of a given formula [2], what happens when A is (a) exposed
to air (b) heated with Ag powder (c) condensed with acetone (d) heated with aniline
in alcoholic KOH [4], why ether is stored in a bottle containing iron wire and why
ethanol is water-soluble [2] — **Or** A is a carboxylic acid giving ethanoic
anhydride on heating with P₂O₅: identify A–E with reactions [5], the HVZ reaction on
A [1], B + ethanol [1], convert E into methanal [1]; Q22 (a) what is Portland cement …

### 2082 (board)
**Group A:** which solution can estimate chloride ion in tap water; t½ = 50 s
independent of the initial concentration → order; Gibbs–Helmholtz: for what value of
ΔG is a reaction spontaneous; E° of P, Q, R, S (+0.34, −0.76, 0.00, −3.05 V) → order
of reducing power; deep blue complex from conc. NH₄OH + CuSO₄ — its formula; maximum
possible oxidation state in the 3d series; which of CH₃MgI, Ni(CO)₄, C₂H₅Li,
C₂H₅ONa, (C₄H₉)₂SnCl₂ are organometallic; X boiled with water gives phenol —
identify X; which gives a positive carbylamine reaction; C₃H₄O₄ → Y + CO₂ and
Y + P₂O₅ → X + H₂O — identify X; Benzene → A → B → C, name the reaction converting
B to C.
**Group B:** Q12 define instantaneous rate, write the rate expressions for
2N₂O₅ → 4NO₂ + O₂, and from 2.24 L of O₂ at NTP in 30 min find the rate of
disappearance of N₂O₅ [5]; Q13 define standard heat of formation and calculate the
heat of formation of acetic acid from three given ΔH values [5]; Q14 E°(Zn²⁺/Zn) =
−0.76 V and E°(Mg²⁺/Mg) = −2.38 V: what is a standard electrode potential [1], cell
notation with anode and cathode [2], the complete cell reaction [1], the cell
potential at 25 °C [1] — **Or** CH₃CH₂CH₂Br + aq. KOH → B + KBr: identify B [1],
which substitution mechanism and why [1], the product with alcoholic KOH [2], and
obtain nitropropane from A [1]; Q15 build the chain among p-aminoazobenzene,
benzenediazonium chloride, aniline, nitrobenzene, phenol and benzene [5] — **Or**
write equations for the 2,4-DNP test, Reimer–Tiemann, Williamson, Perkin
condensation and Wurtz–Fittig; Q16 A + SOCl₂ → B; B + NH₃ → C; C + Br₂/KOH → D;
D + NaNO₂/HCl (cold) → E, a primary alcohol giving a positive iodoform test —
identify A–E with reactions [5]; Q17 separate CH₃CH₂CH₂NH₂ and CH₃CH₂NHCH₃ by
Hoffmann's method and distinguish them by the nitrous acid test [5]; Q18 metal M =
[Ar]3d¹⁰4s², group IIB, called "Jasta": identify M and its main ore [1], why it is
not a transition element [1], draw the vertical retort and give the reduction
reaction [2], what happens on long exposure to air [1]; Q19 what is rusting, the
electrochemical theory of the rusting of iron, and two prevention methods [5].
**Group C:** Q20 (a) deduce N₁V₁ = N₂V₂ [3] (b) oxalic acid vs KMnO₄ titration data
table: name the titration, the equivalent weight of KMnO₄, the normality of KMnO₄,
why dilute H₂SO₄ is added, and identify the titrant and titrand [5×1] — **Or**
applications of the solubility product and common ion effect in qualitative analysis
[3], Bronsted–Lowry vs Lewis bases [2], degree of ionization, [H⁺] and pH of 0.01 M
HCN with Ka = 4.8×10⁻¹⁰ [3]; Q21 X + a Grignard reagent → Y, oxidation → Z, all
giving a positive iodoform test: identify X, Y, Z [2] …

### CHEMISTRY repeats evidenced across two or more verified papers
- **Victor Meyer's test to distinguish 1°/2°/3° alcohols** — 2078-model, 2079-model, 2081 (three papers)
- Williamson's ether synthesis and the 2,4-DNP test in a "write the equations" list — 2081, 2082
- Reimer–Tiemann and Perkin condensation in the same list — 2079-model, 2082
- Iodoform-test identification chain X/Y/Z via Grignard + oxidation — 2079-model, 2081, 2082
- Hoffmann's method to separate amines — 2079-model, 2082
- Cell notation + anode/cathode + cell potential from two E° values — 2078-model, 2081, 2082
- Equivalent weight in a given redox reaction as MCQ 1 — 2078-model, 2079-model, 2081
- Copper extraction, coinage metal, blue vitriol — 2078-model, 2079-model, 2081
- Chloroform (forms phosgene in air, sedative with acetone) — 2079-model, 2081
- OPC vs PPC cement — 2078-model, 2079-model, 2082

---

## 7. Sources actually reached (quote these if your chapter cites sources)

Official / primary: `neb.gov.np`; NEB Google-Drive model-question folders;
CDC Secondary Education Curriculum 2076 PDFs for Physics and Chemistry (Grade 11–12)
— both read for the scope-and-sequence hour tables and the Student Assessment
section; the official **NEB Grade 12 Physics Model Question 2079** PDF
(`media.collegeinfonepal.com/information_docs/NEB-Class-12-Physics-Model-Question-2080.pdf`,
mirrored at `madhusudangaire.com.np/.../Physics-Set1.pdf`); the official **NEB Grade
12 Chemistry Model Question 2079** PDF
(`media.collegeinfonepal.com/information_docs/Class-12-Chemistry-Model-Question-2080.pdf`,
mirrored at `.../Chemistry-Set1.pdf`) — this one carries the cognitive-level
weightage grid on page 6.

Question-text transcriptions: `nebexam.com/class-12/physics/question-bank/…`
(2078, 2080, 2081, 2082, 2083, plus model sets) and
`nebexam.com/class-12/chemistry/question-bank/…` (2081, 2082, 2083, plus model
sets); `dhanraj.com.np` for Physics 2079/2080/2082 and Chemistry 2079/2081.

Unverified leads (teacher/blog "important question" lists, used only as leads):
`jayantbist.com.np`, `webnotee.com`, `nepalieducate.com`.

Could not reach: `moecdc.gov.np` specification-grid pages (404 — no Grade 11/12 grid
is published); NEB 2082 scanned papers (image-only PDFs, no extractable text);
Chemistry board papers for 2078, 2079 and 2080 (not transcribed on any site reached).

---

## 8. House rules digest — the ones that break the build

Read AUTHORING.md for all of it. These are the ones that bite hardest in a
question bank:

1. **mathtext, not LaTeX.** No `\begin{align}`, `\mathbf`, `\ce{}`, `\xrightarrow`,
   `\overset`, matrices, `\substack`, `\SI{}`. No `\\command` (double backslash).
   `\lvert`/`\rvert` are banned — use plain `|`.
2. **Chemistry equations are PLAIN TEXT, never math.** Use Unicode subscripts
   ₀₁₂₃₄₅₆₇₈₉, superscripts ⁺⁻²³, arrows → ⇌ ↑ ↓, and the `--reagent-->` form:
   `CH₃CH₂OH --Cu, 573 K--> CH₃CHO + H₂`. Never put a chemical formula inside `$…$`.
3. **Inline math must pair.** `check.py` reports `UNPAIRED $` and fails the file.
   An inline `$…$` may wrap over up to four source lines but must not cross a blank
   line, a heading, a table row or a `:::` fence.
4. **Display equations must fit 6.93 inches.** check.py fails anything wider. Break
   long ones at an `=` into two `$$…$$` blocks.
5. **MCQ options go on one line** after the stem, indented under it:
   ```
   1. Question text <span class="marks">[1]</span>
      (a) option (b) option (c) option (d) option
   ```
   The build lays the options out itself. Never hand-build a table or list of
   options. Options must run (a)(b)(c)(d) in order or the layout falls back to
   stacked sub-parts. Keep the longest option under about 38 characters if you want
   a two-column grid, under 15 for four columns; longer is fine but stacks.
6. **Marks:** `<span class="marks">[5]</span>` on every subjective question.
7. **Answer keys**: `**1.** ...` on consecutive lines inside a `::: note` box; the
   build gives each its own line.
8. **Figures**: ```figure caption="…"` blocks, real matplotlib, must leave `fig`.
   `figsize` width 4.0–5.2 in, height 2.2–3.4 in (diagrams up to 4.6 in tall).
   `plt`, `np`, `matplotlib`, `INK`, `MUTED`, `GRID`, `ACCENT`, `SERIES` are in
   scope. **Inside figure code use Unicode ≥ ≤ ≠ → | — LaTeX `\ge` etc. crashes
   savefig.** `np.trapz` is gone; use `np.trapezoid`.
9. **Callout types**: `key`, `definition`, `derivation`, `example`, `caution`,
   `tip`, `note`, `memory`. Use `::: note` for answer keys. An "examiner's note" box
   should be `::: tip Examiner's note — <unit name>`.
10. `## Chapter summary` is auto-framed — use that exact heading if you use it.
11. Photos: `python3 assets.py search "…"` then `assets.py get qbank/<name> "File:…"
    --width 1400`; only `FREE` files can be fetched. Place with a ```photo block.
    Asset ids must be prefixed `qbank/`.

## 9. QA GATE — you are not done until this passes

```
cd /data/workspace/NEB/notes/pipeline
python3 check.py ../content/qbank12/unit-0N.md          # must print OK
python3 preview.py ../content/qbank12/unit-0N.md /tmp/qb12_<yourfile>
python3 photoprev.py ../content/qbank12/unit-0N.md /tmp/qb12_<yourfile>_photo
```

Then **Read every PNG** produced and judge it against AUTHORING.md §12 — no
overlapping text, no clipped labels, no arrow ending inside a label, no legend over
data, physics/chemistry actually correct in the drawing. Fix and re-render until
each one is clean. A figure that renders is not a figure that is done.

## 10. Scope discipline

Touch **only** `notes/content/qbank12/` and `notes/assets/`. Do not git commit. Do
not edit any other chapter, the curriculum spines, or the pipeline.
