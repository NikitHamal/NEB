---
subject: Physics
grade: CEE
unit: 8
title: Heat, Temperature and Heat Transfer
hours: 2
area: Heat and Thermodynamics
---

Heat is the first idea in physics that everyone thinks they understand and almost
everyone gets slightly wrong. Heat is not temperature, temperature is not "how hot
something feels", and a bathtub of warm water contains far more thermal energy than
a cup of boiling tea. Of the **7 Heat and Thermodynamics questions** in the paper, with about **2** questions from this chapter. They are
usually one definition (the zeroth law, a thermometric property), one comparison
(which thermometer for which job), and one calculation — a Stefan-law ratio, a
composite slab, or a cooling curve.

::: key What the paper asks from this chapter
- Heat is energy **in transit** because of a temperature difference (J); temperature measures the **average** molecular kinetic energy; thermal energy is the **total** internal energy.
- Zeroth law: if A is in equilibrium with B and B with C, then A is in equilibrium with C — the basis of thermometry.
- $T(\text{K}) = \theta(^\circ\text{C}) + 273$, $\theta_F = \frac{9}{5}\theta_C + 32$; $-40^\circ$ is the same on both scales.
- Thermometers: liquid-in-glass (apparent expansion), resistance ($R=R_0(1+\alpha\theta)$), thermocouple (Seebeck emf), radiation (Stefan–Boltzmann). Know one advantage and one limitation of each.
- Conduction: $H=\frac{Q}{t}=\frac{kA(\theta_1-\theta_2)}{L}$; thermal resistance $L/kA$ adds in series.
- Stefan–Boltzmann: $P=\varepsilon\sigma AT^4$, $\sigma=5.67\times10^{-8}$ W m⁻² K⁻⁴; net loss $\varepsilon\sigma A(T^4-T_s^4)$.
- Wien's law: $\lambda_{max}T=2.9\times10^{-3}$ m K.
- Newton's law of cooling: rate of loss $\propto$ (body temperature − surroundings), giving an exponential fall.
:::

## 8.1 Thermal energy, heat and temperature; thermal equilibrium and the zeroth law

### Three words that are not the same

| Quantity | What it is | Unit | Depends on |
|---|---|---|---|
| **Temperature** | a measure of the **average** kinetic energy of the molecules of a body | K (or °C) | how fast the molecules move |
| **Thermal energy** | the **total** internal energy of the body — the sum of the kinetic and potential energies of all its molecules | J | temperature, **mass**, state |
| **Heat** | energy **in transit** from one body to another because of a temperature difference | J | the process, not the body |

Temperature is a **state** variable: a body "has" a temperature. Heat is not
something a body contains — it is energy crossing a boundary, so a body "gains" or
"loses" heat, it does not "have" heat. What a body contains is internal (thermal)
energy.

This is why a bathtub of water at 40 °C has far more thermal energy than a cup of
tea at 90 °C: it has many more molecules, even though each molecule moves more slowly.

For a gas, temperature is directly tied to molecular motion:

$$ \frac{1}{2}m\overline{v^2} = \frac{3}{2}kT $$

so the **root-mean-square speed** grows as $\sqrt{T}$. Doubling the absolute
temperature multiplies the average kinetic energy per molecule by 2, and the rms
speed by $\sqrt{2}$.

::: caution Heat is not "hotness"
Two statements that are wrong and appear as options every year:
- "A body contains heat." No — it contains internal energy; heat is energy being transferred.
- "Temperature is the total kinetic energy." No — it is the **average** kinetic energy per molecule.
:::

### Thermal contact and thermal equilibrium

When two bodies at different temperatures are placed in **thermal contact** (so
energy can pass between them), energy flows from the hotter to the colder one until
both reach the **same temperature**. At that point there is **no net** transfer of
energy and the bodies are in **thermal equilibrium**. The molecules are still moving
and energy is still exchanged at the microscopic level — the exchange rates are
simply equal in both directions.

::: definition Zeroth law of thermodynamics
If body A is in thermal equilibrium with body B, and body B is in thermal
equilibrium with body C, then A is in thermal equilibrium with C.
:::

The law looks obvious, but it is what makes temperature a meaningful quantity: it
says that "being at the same temperature" is transitive. Its practical use is
**thermometry** — a thermometer (B) placed in contact with a patient (A) reaches
equilibrium with the patient; the thermometer's reading then tells us the patient's
temperature, and two patients that both match the same thermometer match each other.

### Temperature scales

| Scale | Ice point | Steam point | Absolute zero | Size of one degree |
|---|---|---|---|---|
| Celsius | 0 °C | 100 °C | −273.15 °C | 1 °C |
| Fahrenheit | 32 °F | 212 °F | −459.67 °F | 1 °F = 5/9 °C |
| Kelvin | 273.15 K | 373.15 K | 0 K | 1 K = 1 °C |

$$ \theta_F = \frac{9}{5}\theta_C + 32, \qquad T = \theta_C + 273.15 $$

The two fixed points give the conversion by proportion:

$$ \frac{\theta_C}{100} = \frac{\theta_F - 32}{180} = \frac{T - 273.15}{100} $$

Only **one** temperature is numerically the same on the Celsius and Fahrenheit
scales: put $\theta_C = \theta_F = x$ in the conversion:

$$ x = \frac{9}{5}x + 32 \quad\Longrightarrow\quad -\frac{4}{5}x = 32 \quad\Longrightarrow\quad x = -40 $$

so −40 °C = −40 °F.

```figure caption="The same interval drawn on the three scales. From the ice point to the steam point is 100 Celsius degrees, 180 Fahrenheit degrees and 100 kelvin, so a Fahrenheit degree is 5/9 of a Celsius degree."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.1))
ax.axis('off')
info = [(0,'°C',0,100), (1,'°F',32,212), (2,'K',273,373)]
for x, name, b, t in info:
    ax.plot([x,x],[0,1], color=INK, lw=1.3)
    ax.text(x, 1.10, name, ha='center', fontsize=9.5, color=INK)
    for i in range(6):
        y = i/5
        ax.plot([x-0.07,x+0.07],[y,y], color=INK, lw=0.9)
        ax.text(x-0.11, y, f'{b + (t-b)*i/5:g}', ha='right', va='center',
                fontsize=7.6, color=MUTED)
ax.text(1.0, -0.16, 'ice point to steam point:  100 °C  =  180 °F  =  100 K',
        ha='center', fontsize=8.0, color=INK)
ax.set_xlim(-0.75, 2.45); ax.set_ylim(-0.28, 1.22)
```

### Absolute zero and the Kelvin scale

Cooling a gas at constant volume lowers its pressure in proportion to the
temperature on the Celsius scale. Extrapolating to zero pressure gives
−273.15 °C, the lowest temperature possible — **absolute zero**. On the Kelvin
scale this is 0 K, and no temperature can be lower because a negative absolute
temperature would mean negative molecular kinetic energy.

The Kelvin scale is the SI scale because its zero is a true zero: ratios of
temperatures are meaningful, which is exactly what the Stefan and Wien laws need.
"The temperature doubled" only has a meaning in kelvin.

The **triple point** of water — the temperature and pressure at which ice, water and
vapour coexist — is 273.16 K, and it is the modern fixed point that defines the
kelvin.

::: example Worked example 8.1 — converting a temperature
**Problem.** Normal body temperature is 37 °C. Express it in °F and in K. At what
temperature do the Celsius and Fahrenheit readings agree?

**Solution.** $\theta_F = \frac{9}{5}(37) + 32 = 66.6 + 32 = 98.6$ °F.
$T = 37 + 273 = 310$ K.

For equal readings, $\theta_F = \theta_C$:
$\theta = \frac{9}{5}\theta + 32$, so $\theta = -40$. The two scales agree at
−40 degrees.
:::

## 8.2 Thermometers

### What a thermometer must do

A thermometer works through a **thermometric property** — a physical property that
changes steadily and reproducibly with temperature. The common ones are the length
of a liquid column, the electrical resistance of a metal, the emf of a thermocouple,
the pressure of a gas at constant volume, and the radiation emitted by a surface.

A good thermometer should be:

1. **sensitive** — a large change in the property for a small change in temperature;
2. **accurate and reproducible** — the same temperature gives the same reading every time;
3. **linear** — equal temperature steps give equal scale steps, or the non-linearity must be calibrated out;
4. **quick** — a small heat capacity and good thermal contact, so it does not disturb what it measures;
5. **wide in range**, robust, and safe.

No single instrument has all of these, which is why the paper asks "which thermometer
would you use for …".

### Liquid-in-glass thermometer

**Principle.** A liquid expands more than the glass that contains it. What we read is
the **apparent expansion** of the liquid, which is its real expansion minus the
expansion of the glass bulb and tube. Because the glass also expands, two
thermometers made of different glasses can read slightly differently at the same
temperature — a real limitation.

| Liquid | Range | Advantages | Limitations |
|---|---|---|---|
| Mercury | −39 °C to 357 °C | opaque, does not wet glass, good conductor, wide range | toxic, expensive, freezes at −39 °C, cannot read low temperatures |
| Alcohol | −115 °C to 78 °C | cheap, very low freezing point, large expansion | coloured (needs dye), wets the glass, evaporates, cannot read high temperatures |

Other limitations of any liquid-in-glass thermometer: fragile; slow to respond; must
be read where it is (no remote reading); parallax error; the stem must be immersed to
the correct depth; a large bulb takes heat from a small sample.

The **clinical thermometer** is a special mercury thermometer with a range of only
35–42 °C, a **constriction** just above the bulb so that the mercury does not run
back when it is removed from the patient, and a least count of 0.1 °C. It must be
shaken down before use.

### Resistance thermometer

**Principle.** The electrical resistance of a metal rises with temperature:

$$ R = R_0(1 + \alpha\theta) $$

where $R_0$ is the resistance at 0 °C and $\alpha$ the temperature coefficient of
resistance. Platinum is used because it is chemically stable and its resistance
changes very reproducibly over a wide range.

- **Range:** about −200 °C to 850 °C.
- **Advantages:** very accurate and reproducible; wide range; the reading can be sent
  down a cable and recorded automatically; no parallax; can be made very stable over
  years.
- **Limitations:** needs a power supply and a bridge circuit; the current heats the
  element slightly (**self-heating**); slower than a thermocouple; more expensive;
  $\alpha$ is not perfectly constant over the whole range.

### Thermocouple thermometer

**Principle.** Join two different metals at both ends. If the two junctions are at
different temperatures, a small emf appears in the circuit — the **Seebeck effect**.
The emf is roughly proportional to the temperature difference between the junctions:

$$ \varepsilon \approx \alpha(T_{hot} - T_{cold}) $$

- **Range:** about −200 °C to 1600 °C, depending on the metal pair.
- **Advantages:** the junction can be tiny, so it responds quickly, has a very small
  heat capacity and can measure the temperature of a single point; it is rugged,
  cheap, and can be read remotely.
- **Limitations:** the emf is only a few tens of microvolts per degree, so
  amplification is needed; the **cold junction** must be kept at a known temperature
  (or electronically compensated); the relation is non-linear; the calibration drifts
  as the metals age.

### Radiation thermometer (pyrometer)

**Principle.** Every hot body radiates energy at a rate that grows very rapidly with
temperature. A pyrometer measures the radiation received and converts it to a
temperature using the Stefan–Boltzmann law (total radiation pyrometer) or by
comparing the intensities at two wavelengths (ratio pyrometer).

- **Range:** about 800 °C to 3000 °C and beyond.
- **Advantages:** **no contact**, so it can measure a moving furnace belt, molten
  metal, a rotating shaft or a distant star; it does not disturb the object; it can be
  very fast.
- **Limitations:** it needs the **emissivity** of the surface to be known (a shiny
  surface reads too low); it needs a clear line of sight (smoke, dust and steam
  interfere); it is not usable at low temperatures where the radiated power is small;
  it is expensive.

### Comparison

| Thermometer | Principle | Typical range | Main advantage | Main limitation |
|---|---|---|---|---|
| Mercury in glass | apparent expansion | −39 to 357 °C | simple, cheap, direct reading | fragile, limited range, not remote |
| Alcohol in glass | apparent expansion | −115 to 78 °C | works at very low temperatures | wets glass, cannot go high |
| Platinum resistance | $R=R_0(1+\alpha\theta)$ | −200 to 850 °C | very accurate and reproducible | needs power, slow, self-heating |
| Thermocouple | Seebeck emf | −200 to 1600 °C | tiny junction, fast, wide range | needs cold-junction compensation, small emf |
| Radiation pyrometer | Stefan–Boltzmann | 800 to 3000 °C | no contact, very high temperatures | depends on emissivity, line of sight |

::: tip Choosing a thermometer in an MCQ
Ask three questions in order: **How hot?** (range), **Can I touch it?** (contact or
not), **How fast and how small?** (response). A furnace wall that is moving → pyrometer.
The temperature inside a grain store, logged for a month → resistance. The
temperature at one point inside a running engine → thermocouple. A patient → clinical
mercury thermometer.
:::

## 8.3 Conduction, convection and radiation; black-body radiation and the Stefan–Boltzmann law

Heat always moves from a hotter region to a colder one, and it does so by three
mechanisms that can act together.

| Mode | What moves | Needs a medium? | Example |
|---|---|---|---|
| Conduction | energy passed from molecule to molecule (and by free electrons in metals) | yes | a metal spoon in hot tea |
| Convection | the hot fluid itself moves | yes, a fluid | sea breeze, boiling water |
| Radiation | electromagnetic waves | **no** | heat from the Sun reaching the Earth |

### Conduction and the temperature gradient

In steady state, the temperature at each point of a rod no longer changes with time,
and the rate of heat flow is

$$ H = \frac{Q}{t} = \frac{kA(\theta_1-\theta_2)}{L} $$

where $k$ is the **thermal conductivity** of the material (W m⁻¹ K⁻¹), $A$ the
cross-section, $L$ the length and $\theta_1-\theta_2$ the temperature difference
between the ends.

The quantity $(\theta_1-\theta_2)/L$ is the **temperature gradient**; in the limit of
a thin slice,

$$ H = -kA\frac{d\theta}{dx} $$

The minus sign says heat flows **down** the temperature gradient, from hot to cold.

| Material | $k$ (W m⁻¹ K⁻¹) |
|---|---|
| Silver | 406 |
| Copper | 385 |
| Aluminium | 205 |
| Steel | 50 |
| Glass | 0.8 |
| Water | 0.6 |
| Wood | 0.15 |
| Air | 0.024 |

Metals conduct well because their **free electrons** carry energy quickly through the
lattice as well as the vibrating ions. Air conducts very poorly, which is why wool,
feathers, thermocol and double glazing — all of which trap air — are good insulators.

### Composite slabs and thermal resistance

A slab of thickness $L$ and conductivity $k$ has a **thermal resistance**

$$ R_{th} = \frac{L}{kA} $$

and the conduction equation becomes $H = \Delta\theta/R_{th}$ — exactly the form of
Ohm's law, with $H$ playing the part of current and $\Delta\theta$ of voltage. For
slabs in **series** (heat crosses them one after another) the resistances add:

$$ H = \frac{A(\theta_1-\theta_n)}{\frac{L_1}{k_1}+\frac{L_2}{k_2}+\cdots+\frac{L_n}{k_n}} $$

For rods in **parallel**, the conductances $kA/L$ add.

```figure caption="Steady conduction through two slabs in series. The heat current is the same in both, so the temperature falls fastest where the conductivity is lowest — here almost the whole 100 °C drop is across the wood."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
ax.plot([0,1],[100,90.9], color=ACCENT, lw=2.4)
ax.plot([1,2],[90.9,0], color='#A8271F', lw=2.4)
ax.axvline(1, color=MUTED, lw=0.8, ls=':')
ax.text(0.5, 104, 'steel   k = 50', ha='center', fontsize=8.4, color=ACCENT)
ax.text(1.5, 104, 'wood   k = 5', ha='center', fontsize=8.4, color='#A8271F')
ax.text(0.5, 70, 'small drop', ha='center', fontsize=8.0, color=ACCENT)
ax.text(1.28, 72, 'large drop', ha='left', fontsize=8.0, color='#A8271F')
ax.plot([1],[90.9],'o',color=INK,ms=3.5,zorder=5)
ax.annotate('90.9 °C', xy=(1,90.9), xytext=(1.08,93), fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(2.04, 0, '0 °C', ha='left', va='center', fontsize=8.2, color=INK)
ax.set_xlabel('distance through the slabs'); ax.set_ylabel('temperature  (°C)')
ax.set_xlim(-0.25, 2.35); ax.set_ylim(-8, 114)
ax.set_xticks([0,1,2]); ax.set_xticklabels(['0','L','2L'])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
```

::: example Worked example 8.2 — a composite wall
**Problem.** A wall consists of a 2.0 cm copper layer ($k=400$ W m⁻¹ K⁻¹) and a
2.0 cm insulating layer ($k=0.40$ W m⁻¹ K⁻¹), each of area 1.0 m². The outside faces
are at 100 °C and 0 °C. Find the heat current and the temperature at the interface.

**Solution.** In series,

$$ H = \frac{A\,\Delta\theta}{\frac{L_1}{k_1}+\frac{L_2}{k_2}} = \frac{(1.0)(100)}{0.020/400 + 0.020/0.40} = \frac{100}{5.0\times10^{-5}+0.050} \approx 2.0\times10^3\ \text{W} $$

Across the copper the drop is
$H L_1/(k_1A) = 2000\times5.0\times10^{-5} = 0.10$ °C, so the interface is at
**99.9 °C**. Almost the whole 100 °C falls across the insulator: the temperature
profile is steepest in the poorer conductor.
:::

### Convection

In **convection** the fluid itself moves and carries its thermal energy with it.

- **Natural convection** occurs because a warmed fluid expands, becomes less dense and
  rises, while cooler, denser fluid sinks to take its place. It needs **gravity** (or
  an equivalent acceleration); in a freely falling lift or an orbiting spacecraft
  there is no natural convection.
- **Forced convection** uses a pump or a fan: central heating, a car radiator, blood
  circulation.

| Example | What happens |
|---|---|
| Sea breeze (day) | land heats faster than the sea; air over the land rises; cooler air flows in from the sea |
| Land breeze (night) | the sea stays warmer; air over the sea rises; air flows out from the land |
| Room heater | placed low, so warm air rises and circulates through the room |
| Air conditioner | placed high, so cool dense air sinks through the room |
| Chimney | hot smoke rises, drawing fresh air in at the bottom |
| Monsoon | summer heating of the land draws moist air in from the Indian Ocean |

### Newton's law of cooling

For a body cooling in air, when the excess temperature over the surroundings is
small, the rate of loss of heat is proportional to that excess:

$$ \frac{dQ}{dt} = -k(\theta - \theta_s) $$

Since $dQ = mc\,d\theta$ for the body,

$$ mc\frac{d\theta}{dt} = -k(\theta-\theta_s) \quad\Longrightarrow\quad \theta = \theta_s + (\theta_0-\theta_s)e^{-kt/mc} $$

The temperature falls **exponentially** towards the surroundings' temperature, never
quite reaching it. Equal time intervals remove equal **fractions** of the remaining
excess, not equal numbers of degrees.

```figure caption="Newton's law of cooling: the excess temperature falls exponentially. In each equal interval the body loses the same fraction of its remaining excess over the surroundings (here 60 → 50 → 42.9 °C with the room at 25 °C)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t = np.linspace(0, 40, 400)
th = 25 + 35*np.exp(-0.03365*t)
ax.plot(t, th, color=ACCENT, lw=2.0)
ax.axhline(25, color=MUTED, lw=0.9, ls='--')
ax.plot([0,10,20],[60,50,42.9],'o',color='#A8271F',ms=4.5,zorder=5)
for tt, vv in [(0,60),(10,50),(20,42.9)]:
    ax.annotate(f'{vv:g} °C', xy=(tt,vv), xytext=(tt+1.6, vv+2.4), fontsize=8.0, color='#A8271F')
ax.text(26, 27.2, 'surroundings 25 °C', fontsize=8.2, color=MUTED)
ax.set_xlabel('time  t  (min)'); ax.set_ylabel('temperature  (°C)')
ax.set_xlim(0,40); ax.set_ylim(20,64)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: caution Newton's law is only for small excess temperatures
The law assumes the heat is carried away by natural convection and radiation together
in a way that is roughly linear in the excess temperature. At large excess
temperatures radiation dominates (and goes as $T^4$), so the simple exponential
fails. It also assumes the surroundings do not warm up, and no evaporation.
:::

### Radiation

**Thermal radiation** is electromagnetic radiation emitted by every body because of
its temperature. Its properties:

- it needs **no medium** — it crosses a vacuum, which is how the Sun's energy reaches us;
- it travels at the speed of light and obeys the same laws as light (reflection,
  refraction, polarisation);
- at everyday temperatures it is mostly **infrared**; above about 500 °C a body glows
  dull red, and at about 1500 °C it is white-hot.

**Prevost's theory:** every body emits radiation at all times, whatever its
temperature, and also absorbs radiation from its surroundings. If it emits faster
than it absorbs, it cools; if it absorbs faster, it warms; at equal temperatures the
two rates are equal.

### Black body and emissivity

::: definition Black body
A **black body** is an ideal body that absorbs **all** radiation of every wavelength
falling on it — its absorptivity is 1 — and, at a given temperature, emits more
energy than any other body.
:::

A small hole in a hollow cavity is the closest practical black body: radiation that
enters the hole is reflected many times inside and is almost completely absorbed. Soot
and lampblack come close ($\varepsilon\approx0.95$).

The **emissivity** $\varepsilon$ of a real surface is the ratio of the energy it emits
to the energy a black body of the same area and temperature would emit:

$$ \varepsilon = \frac{P_{real}}{P_{black}} \qquad (0 \le \varepsilon \le 1) $$

::: caution Emissivity and absorptivity
**Kirchhoff's law:** at a given temperature and wavelength, a good absorber is also a
good emitter, so $\varepsilon=\alpha$. A blackened surface (high $\varepsilon$, high
$\alpha$) heats quickly in sunshine **and** cools quickly at night. A shiny white
surface (low $\varepsilon$, low $\alpha$) stays cooler in the sun **and** cools slowly
after sunset. Do not mix the two: absorptivity is about radiation arriving,
emissivity about radiation leaving.
:::

### Stefan–Boltzmann law

The total energy radiated per second by a black body of area $A$ at absolute
temperature $T$ is

$$ P = \sigma A T^4 $$

and for a real surface

$$ P = \varepsilon\sigma A T^4 $$

with the **Stefan constant**

$$ \sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4} $$

A body at temperature $T$ in surroundings at $T_s$ both emits and absorbs, so its
**net** loss is

$$ P_{net} = \varepsilon\sigma A(T^4 - T_s^4) $$

The fourth power makes the law dramatic: doubling the absolute temperature multiplies
the radiated power by $2^4=16$; trebling it multiplies it by 81.

```figure caption="Black-body spectra at three temperatures. As $T$ rises the whole curve rises (area $\propto T^4$) and the peak moves to shorter wavelength, $\lambda_{max}T=2.9\times10^{-3}$ m K."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
lam = np.linspace(0.15, 3.0, 600)*1e-6
def planck(T):
    return 1/(lam**5*(np.exp(1.4388e-2/(lam*T)) - 1))
for T, c in [(3000, SERIES[1]), (4000, SERIES[2]), (5000, ACCENT)]:
    y = planck(T); y = y/y.max()
    ax.plot(lam*1e6, y, color=c, lw=1.9, label=f'{T} K')
    ax.plot([2898/T],[1.0],'o',color=c,ms=3.5)
ax.legend(loc='upper right', fontsize=8.0, frameon=False, handlelength=1.6)
ax.set_xlabel('wavelength  λ  (μm)'); ax.set_ylabel('relative intensity')
ax.set_xlim(0.2,3.0); ax.set_ylim(0,1.20)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
```

Note that the curves are drawn **normalised to their own peaks** so that the shapes
can be compared. In reality the total area under the 5000 K curve is
$(5/3)^4 = 7.7$ times larger than under the 3000 K curve, and the peak intensity
itself grows even faster, as $T^5$.

### Wien's law

The wavelength at which the emission is strongest is inversely proportional to the
absolute temperature:

$$ \lambda_{max}T = b = 2.9\times10^{-3}\ \text{m K} $$

| Body | $T$ (K) | $\lambda_{max}$ | Region |
|---|---|---|---|
| Sun's surface | 5800 | 500 nm | visible (green-blue) |
| Tungsten filament | 2800 | 1.0 μm | near infrared |
| Human skin | 310 | 9.4 μm | infrared |
| Earth's surface | 288 | 10 μm | infrared |

This is why the Sun looks white-yellow while a warm radiator glows dull red, and why
infrared cameras can see people in the dark. It is also the basis of the greenhouse
effect: the Sun's visible light passes through glass and the atmosphere, but the
Earth's 10 μm infrared is absorbed by water vapour and carbon dioxide.

::: example Worked example 8.3 — the Sun's peak wavelength
**Problem.** The Sun's surface is at about 5800 K. At what wavelength does it radiate
most strongly?

**Solution.** $\lambda_{max} = 2.9\times10^{-3}/5800 = 5.0\times10^{-7}$ m
$= 500$ nm — green light, in the middle of the visible spectrum. Our eyes have
evolved to be most sensitive near the peak of sunlight.
:::

::: example Worked example 8.4 — net radiation from a person
**Problem.** A person of surface area 1.5 m² and skin temperature 37 °C
(310 K) stands in a room at 17 °C (290 K). Taking the emissivity of skin as 0.80,
find the net rate of radiative heat loss.

**Solution.**

$$ P = \varepsilon\sigma A(T^4-T_s^4) = (0.80)(5.67\times10^{-8})(1.5)(310^4-290^4) $$

$310^4 = 9.24\times10^9$ and $290^4 = 7.07\times10^9$, so the bracket is
$2.16\times10^9$ K⁴.

$P = 0.80\times5.67\times10^{-8}\times1.5\times2.16\times10^9 \approx 1.5\times10^2$ W.

About 150 W — a useful check on why a room full of people warms up.
:::

### Putting the three modes to work

| Device | How it works |
|---|---|
| Thermos flask | vacuum between the walls stops conduction and convection; the silvered walls have low emissivity, so radiation is reflected back |
| Double glazing | the trapped air conducts poorly and the narrow gap suppresses convection |
| Solar cooker | black absorbing surface, glass cover to trap radiation, insulation below |
| White clothes in summer | low absorptivity, so most sunlight is reflected |
| Dark clothes in winter | high absorptivity, so more solar energy is absorbed |
| Greenhouses | glass transmits visible light but absorbs the outgoing infrared |

```photogrid label="8.1" cols="2" ratio="1.2" caption="Radiation from the Sun. (a) A solar flare seen in ultraviolet light: the Sun loses energy only by radiation. (b) Stefan's law gives the power radiated per square metre, E = sigma T^4. For the surface temperature T = 5,772 K, E = 6.29 x 10^7 W/m^2. Multiplying by the area of a sphere of radius 6.957 x 10^8 m gives a luminosity L = 3.83 x 10^26 W. Spread over a sphere of radius 1.496 x 10^11 m (the Earth's orbit) this is 1,361 W/m^2, the solar constant. Wien's law lambda_max = b / T with b = 2.898 x 10^-3 m K gives a peak at 502 nm, in the green-yellow part of the visible spectrum."
@ photo id="sci10/sun-flare" cap="The Sun in extreme ultraviolet: a hot body radiating"
fit 1.2
focus 0.5 0.5
@ svg cap="Stefan, Wien and the solar constant, computed"
import math
sig, b = 5.670374e-8, 2.897772e-3
T, Rs, d = 5772.0, 6.957e8, 1.496e11
E = sig * T ** 4; L = 4 * math.pi * Rs ** 2 * E; S = L / (4 * math.pi * d ** 2); lam = b / T
assert abs(E / 1e7 - 6.294) < 0.01 and abs(L / 1e26 - 3.83) < 0.02 and abs(S - 1361) < 5 and abs(lam * 1e9 - 502) < 1
facts = dict(E="%.2f" % (E / 1e7), L="%.2f" % (L / 1e26), S="{:,.0f}".format(S), lam="%.0f" % (lam * 1e9))
f = Fig(300, 236)
f.text(150, 14, "black-body curve of the Sun, T = 5,772 K", size=10.5, color=NAVY, bold=True)
planck = lambda l, T: 1 / (l ** 5 * (math.exp(1.4388e-2 / (l * T)) - 1))
ls = [i * 1e-8 for i in range(10, 200)]; pm = max(planck(l, T) for l in ls)
X = lambda l: 24 + (l * 1e9 - 100) / 1900 * 256; Y = lambda p: 150 - p / pm * 100
f.line(X(1e-7), Y(0), 284, Y(0), color=SLATE, sw=1.2)
sx = [(380, 450, "#c4b5fd"), (450, 495, "#93c5fd"), (495, 570, "#86efac"), (570, 590, "#fde68a"), (590, 620, "#fdba74"), (620, 750, "#fca5a5")]
for a, bb, c in sx: f.box(X(a * 1e-9), 150, X(bb * 1e-9) - X(a * 1e-9), 8, "", fill=c, stroke=c, r=0, sw=0)
pts = [(l, planck(l, T)) for l in [i * 1e-8 * 2 for i in range(5, 100)]]
for (a, bb), (c, d_) in zip(pts, pts[1:]): f.line(X(a), Y(bb), X(c), Y(d_), color=NAVY, sw=2.4)
f.line(X(lam), Y(pm), X(lam), Y(0), color=RED, sw=1.2, dash=True); f.text(X(lam) + 6, 44, "peak %.0f nm" % (lam * 1e9), size=10.5, color=RED, bold=True, anchor="start")
for l in (500, 1000, 1500, 2000): f.text(X(l * 1e-9), 174, "%d" % l, size=10.5, color=SLATE)
f.text(150, 188, "wavelength (nm); colour strip = visible light", size=10.5, color=SLATE)
f.text(150, 204, "sigma T^4 = %.2f x 10^7 W/m^2,  L = %.2f x 10^26 W" % (E / 1e7, L / 1e26), size=10.5, color=NAVY, bold=True)
f.text(150, 220, "solar constant L / 4 pi d^2 = %s W/m^2" % "{:,.0f}".format(S), size=10.5, color=AMBER, bold=True)
```

```photogrid label="8.2" cols="2" ratio="1.2" caption="We glow in the infrared. (a) A thermal camera forms an image from the radiation emitted by a surface, with the warmest parts shown in the brightest colours. (b) The cell applies the Stefan-Boltzmann law to bare skin at 34 degrees C (307 K) with emissivity 0.97 and an area of 1.5 m2. In a room at 20 degrees C the body loses a net 125 W by radiation alone; in air at 0 degrees C the loss is 275 W, and at 30 degrees C only 38 W. Wien's displacement law puts the peak of the emission at 9.4 micrometres, deep in the infrared, so ordinary cameras cannot see it but a thermal camera can."
@ photo id="ceephy3/thermal" cap="A thermographic (infrared) image of a person"
fit 1.2
focus 0.5 0.5
@ svg cap="Heat radiated by the human body"
sig, eps, A, Ts = 5.67e-8, 0.97, 1.5, 307.15
rows = []
for tc in (0, 10, 20, 30):
    Ta = tc + 273.15
    rows.append(("%d C" % tc, eps * sig * A * (Ts ** 4 - Ta ** 4)))
lam = 2.898e-3 / Ts * 1e6
assert 120 < rows[2][1] < 130
f = Fig(300, 236)
f.text(150, 12, "Net radiated power of skin at 34 C, watts", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=300, fmt="%.0f", x0=52, y0=30, bw=170, gap=30,
      colors=[(BLUE, NAVY), (MINT, TEAL), (SAND, AMBER), (ROSE, RED)])
f.text(150, 158, "surroundings at the temperature shown", size=10, color=SLATE, bold=True)
f.text(150, 180, "P = e sigma A (Ts^4 - Ta^4), A = 1.5 m2", size=10.5, color=NAVY, bold=True)
f.text(150, 200, "Wien peak: %.1f micrometres (infrared)" % lam, size=10.5, color=NAVY, bold=True)
f.text(150, 218, "a camera maps T from this radiation", size=10, color=SLATE, bold=True)
facts = dict(p0=rows[0][1], p20=rows[2][1], p30=rows[3][1], lam=lam)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Temperature conversion | $\theta_F=\frac{9}{5}\theta_C+32$; $T=\theta_C+273$; $\frac{\theta_C}{100}=\frac{\theta_F-32}{180}$ |
| Fixed points | ice 0 °C = 32 °F = 273 K; steam 100 °C = 212 °F = 373 K; absolute zero −273.15 °C |
| Same reading | −40 °C = −40 °F |
| Molecular energy | $\frac{1}{2}m\overline{v^2}=\frac{3}{2}kT$ |
| Zeroth law | A~B and B~C $\Rightarrow$ A~C; the basis of thermometry |
| Resistance thermometer | $R=R_0(1+\alpha\theta)$; range −200 to 850 °C |
| Thermocouple | emf $\approx\alpha(T_{hot}-T_{cold})$; Seebeck effect; range to 1600 °C |
| Pyrometer | uses Stefan–Boltzmann; 800–3000 °C; no contact |
| Conduction | $H=\frac{kA(\theta_1-\theta_2)}{L}=-kA\frac{d\theta}{dx}$ |
| Thermal resistance | $R_{th}=\frac{L}{kA}$; series: add $L/k$; parallel: add $kA/L$ |
| Conductivity values | silver 406, copper 385, steel 50, glass 0.8, wood 0.15, air 0.024 W m⁻¹ K⁻¹ |
| Newton's cooling | $\frac{d\theta}{dt}\propto-(\theta-\theta_s)$; $\theta=\theta_s+(\theta_0-\theta_s)e^{-kt/mc}$ |
| Stefan–Boltzmann | $P=\varepsilon\sigma AT^4$; $\sigma=5.67\times10^{-8}$ W m⁻² K⁻⁴ |
| Net radiation | $P_{net}=\varepsilon\sigma A(T^4-T_s^4)$ |
| Wien | $\lambda_{max}T=2.9\times10^{-3}$ m K |
| Emissivity | $0\le\varepsilon\le1$; $\varepsilon=\alpha$ at the same temperature and wavelength |
| Black body | absorptivity 1, emissivity 1; a cavity with a small hole is a good approximation |

## Chapter summary

- Temperature measures the **average** kinetic energy of molecules; thermal energy is
  the **total** internal energy (so it depends on mass); heat is energy **in transit**
  because of a temperature difference.
- Two bodies in thermal contact reach the same temperature — thermal equilibrium — with
  no net heat flow. The zeroth law makes "same temperature" transitive and so makes
  thermometry possible.
- $T=\theta_C+273$ and $\theta_F=\frac{9}{5}\theta_C+32$; the scales agree at −40°;
  absolute zero is −273.15 °C.
- Liquid-in-glass thermometers read the apparent expansion of the liquid; mercury
  covers −39 to 357 °C, alcohol −115 to 78 °C.
- Resistance thermometers use $R=R_0(1+\alpha\theta)$ and are the most accurate over a
  wide range; thermocouples use the Seebeck emf and are small, fast and wide-ranging;
  pyrometers measure radiation without contact.
- Conduction obeys $H=kA\Delta\theta/L$; the temperature gradient is steepest in the
  poorer conductor, and thermal resistances $L/kA$ add in series.
- Convection is heat carried by a moving fluid; it needs gravity for the natural case.
- Newton's law of cooling gives an exponential approach to the surroundings'
  temperature, with equal fractions of the excess lost in equal times.
- A black body absorbs everything and is the best emitter; $\varepsilon=\alpha$.
  $P=\varepsilon\sigma AT^4$, and doubling $T$ multiplies the power by 16.
- Wien's law $\lambda_{max}T=2.9\times10^{-3}$ m K puts the Sun's peak at 500 nm and a
  human's at about 9 μm.

## Practice questions

**Set A — Recall (23 questions)**

1. The SI unit of heat is
   (a) J (b) W (c) K (d) J kg⁻¹
2. One calorie is equal to
   (a) 0.239 J (b) 42 J (c) 4.186 J (d) 4186 J
3. The temperature of a body is a measure of the
   (a) total heat in it (b) total internal energy (c) mass of its molecules (d) average kinetic energy of its molecules
4. If body A is in thermal equilibrium with B, and B with C, then the zeroth law says
   (a) A and C are at different temperatures (b) A and C are in thermal equilibrium (c) B is hotter than both (d) heat flows from A to C
5. Absolute zero on the Celsius scale is
   (a) 0 °C (b) −100 °C (c) −273.15 °C (d) −373 °C
6. The ice point of water on the Kelvin scale is
   (a) 273 K (b) 373 K (c) 0 K (d) 100 K
7. The steam point of water on the Fahrenheit scale is
   (a) 100 °F (b) 212 °F (c) 273 °F (d) 32 °F
8. The temperature at which the Celsius and Fahrenheit readings are equal is
   (a) 40° (b) 0° (c) −32° (d) −40°
9. The range of a clinical thermometer is about
   (a) 0–100 °C (b) 35–42 °C (c) 30–50 °C (d) 32–45 °C
10. Mercury freezes at about
   (a) −39 °C (b) 0 °C (c) −115 °C (d) 357 °C
11. A liquid-in-glass thermometer works on the
   (a) expansion of the glass only (b) contraction of the liquid (c) apparent expansion of the liquid (d) change in air pressure
12. A resistance thermometer uses the change of
   (a) length with temperature (b) colour with temperature (c) pressure with temperature (d) resistance with temperature
13. A thermocouple thermometer works on the
   (a) Seebeck effect (b) Peltier effect (c) Joule effect (d) Thomson effect
14. A radiation pyrometer measures temperature using the
   (a) Ohm's law (b) Wien's displacement law only (c) Stefan–Boltzmann law (d) Boyle's law
15. The SI unit of thermal conductivity is
   (a) J K⁻¹ (b) W m⁻¹ K⁻¹ (c) W m⁻² K⁻⁴ (d) J kg⁻¹ K⁻¹
16. Which of the following is the best conductor of heat?
   (a) silver (b) copper (c) iron (d) water
17. The absorptivity of a perfect black body is
   (a) 0 (b) 0.5 (c) 2 (d) 1
18. The emissivity of a perfect black body is
   (a) 0 (b) 0.5 (c) 1 (d) infinite
19. The SI unit of Stefan's constant is
   (a) W m⁻² K⁻⁴ (b) W m⁻¹ K⁻¹ (c) J K⁻¹ (d) W m⁻²
20. Wien's constant is about
   (a) 2.9 × 10⁻² m K (b) 2.9 × 10⁻³ m K (c) 3 × 10⁸ m K (d) 6.6 × 10⁻³⁴ m K
21. Heat can travel through a vacuum by
   (a) conduction (b) convection (c) both conduction and convection (d) radiation
22. Newton's law of cooling states that the rate of loss of heat is proportional to the
   (a) temperature of the body (b) time (c) excess temperature over the surroundings (d) surface area alone
23. Convection in a liquid is caused mainly by the
   (a) difference in density (b) surface tension (c) radiation from the walls (d) conduction along the container

::: note Answers and explanations — Set A
**1.** (a) — heat is energy, so its unit is the joule. The watt is power and the kelvin is temperature.
**2.** (c) — 1 cal = 4.186 J; the calorie is the older unit of heat.
**3.** (d) — temperature measures the mean kinetic energy per molecule; the total internal energy also depends on the number of molecules.
**4.** (b) — the zeroth law makes thermal equilibrium transitive, so A and C must be at the same temperature.
**5.** (c) — absolute zero is 0 K, which is −273.15 °C.
**6.** (a) — 0 °C + 273 = 273 K.
**7.** (b) — 100 °C corresponds to 212 °F.
**8.** (d) — solving $x=\frac{9}{5}x+32$ gives $x=-40$.
**9.** (b) — a clinical thermometer covers only the narrow range of body temperature, 35–42 °C.
**10.** (a) — mercury solidifies at about −39 °C, which is why it cannot be used in very cold places; −115 °C is alcohol's freezing point.
**11.** (c) — the liquid expands more than the glass, so the thread rises; the reading is the apparent expansion.
**12.** (d) — $R=R_0(1+\alpha\theta)$; the resistance is the thermometric property.
**13.** (a) — two junctions at different temperatures produce an emf by the Seebeck effect.
**14.** (c) — the total radiated power depends on $T^4$, so measuring it gives the temperature without contact.
**15.** (b) — from $H=kA\Delta\theta/L$, $k$ has units W m⁻¹ K⁻¹.
**16.** (a) — silver has the highest thermal conductivity of the four, about 406 W m⁻¹ K⁻¹.
**17.** (d) — a black body absorbs all radiation of every wavelength.
**18.** (c) — it is also the perfect emitter, by definition.
**19.** (a) — from $P=\sigma AT^4$, $\sigma=P/(AT^4)$, W m⁻² K⁻⁴.
**20.** (b) — $\lambda_{max}T=2.9\times10^{-3}$ m K.
**21.** (d) — radiation needs no medium; conduction and convection both need matter.
**22.** (c) — the rate is proportional to $(\theta-\theta_s)$, not to the temperature itself.
**23.** (a) — the warmer liquid expands, becomes less dense and rises, and the cooler liquid sinks.
:::

**Set B — Understanding (15 questions)**

1. The same quantity of heat is given to 1 kg and to 2 kg of water. Then
   (a) both rise by the same temperature (b) the 2 kg rises twice as much (c) neither rises (d) the 1 kg rises twice as much
2. The zeroth law of thermodynamics is the basis of
   (a) thermometry (b) calorimetry (c) conduction (d) radiation
3. Two bodies are in thermal equilibrium. It follows that
   (a) they have equal thermal energy (b) they have equal mass (c) there is no net heat flow between them (d) they have equal specific heat
4. A bathtub of water at 40 °C and a cup of tea at 90 °C are compared. The greater thermal energy is in
   (a) the cup (b) both the same (c) the bathtub (d) impossible to compare
5. Mercury is preferred to alcohol in a thermometer because mercury
   (a) is cheaper (b) does not wet glass (c) freezes at −115 °C (d) is coloured
6. Alcohol is used in thermometers in very cold places because it has
   (a) a low freezing point (b) a high boiling point (c) a dark colour (d) a low cost
7. A platinum resistance thermometer is used for precise work because
   (a) it is cheap (b) it needs no power supply (c) its resistance changes reproducibly over a wide range (d) it responds instantly
8. A thermocouple is best suited for
   (a) small, fast measurements at a point (b) very high accuracy at fixed points (c) measurement without contact (d) temperatures below −200 °C
9. A radiation pyrometer is best suited for
   (a) moving or inaccessible hot objects (b) clinical use (c) ocean depths (d) very low temperatures
10. Metals conduct heat better than wood mainly because metals have
   (a) free electrons (b) greater density (c) shiny surfaces (d) larger atoms
11. Double-glazed windows reduce heat loss because
   (a) glass is a good conductor (b) the air gap conducts poorly and suppresses convection (c) glass reflects all heat (d) the gap radiates heat away
12. In a composite slab in steady state, the temperature falls most rapidly in
   (a) the better conductor (b) the thicker layer only (c) the poorer conductor (d) both equally
13. A black body at 600 K radiates compared with the same body at 300 K
   (a) twice as much (b) four times as much (c) eight times as much (d) sixteen times as much
14. A good absorber of radiation is
   (a) a poor emitter (b) neither a good nor a poor emitter (c) a good emitter (d) a perfect reflector
15. White clothes are preferred in summer because they
   (a) absorb more radiation (b) conduct heat away quickly (c) emit more radiation (d) reflect most of the radiation

::: note Answers and explanations — Set B
**1.** (d) — the same heat gives $\Delta\theta=Q/mc$, so the smaller mass has the larger rise; 1 kg rises twice as much.
**2.** (a) — it guarantees that a thermometer in equilibrium with a body reads that body's temperature.
**3.** (c) — equilibrium means equal temperatures, so the exchange rates are equal and there is no net flow; thermal energies can differ.
**4.** (c) — thermal energy depends on mass as well as temperature, and the bathtub has far more water.
**5.** (b) — mercury does not wet glass, so its thread stays clean and reads clearly. Alcohol wets glass and needs a dye.
**6.** (a) — alcohol freezes at about −115 °C, well below mercury's −39 °C.
**7.** (c) — platinum's resistance is stable and reproducible, so it can be calibrated to high accuracy over a wide range.
**8.** (a) — the junction is tiny, so it has a small heat capacity and responds quickly.
**9.** (a) — it needs no contact, so it can measure a moving belt or molten metal.
**10.** (a) — free electrons carry energy through the metal far faster than molecular vibration alone.
**11.** (b) — air has a very low conductivity, and a narrow gap prevents convection currents.
**12.** (c) — the heat current is the same through both, so $\Delta\theta=HL/(kA)$ is largest where $k$ is smallest.
**13.** (d) — $P\propto T^4$, and $(600/300)^4=16$.
**14.** (c) — Kirchhoff's law: at the same temperature and wavelength, absorptivity equals emissivity.
**15.** (d) — a white surface has low absorptivity, so it reflects most sunlight and stays cooler.
:::

**Set C — Application (9 questions)**

1. Normal body temperature 37 °C, expressed in °F and in K, is
   (a) 98.6 °F and 310 K (b) 98.6 °F and 236 K (c) 37 °F and 310 K (d) 100 °F and 310 K
2. A body cools from 60 °C to 50 °C in 10 minutes in a room at 25 °C. Its temperature after another 10 minutes is about
   (a) 45 °C (b) 43 °C (c) 40 °C (d) 35 °C
3. A wall has a 2.0 cm copper layer (k = 400 W m⁻¹ K⁻¹) and a 2.0 cm insulating layer (k = 0.40 W m⁻¹ K⁻¹), area 1.0 m², with faces at 100 °C and 0 °C. The heat current is about
   (a) 20 W (b) 2.0 kW (c) 200 W (d) 20 kW
4. For that wall, the temperature at the copper–insulator interface is about
   (a) 50 °C (b) 90.9 °C (c) 99.9 °C (d) 0 °C
5. A black body of area 0.50 m² at 300 K radiates a power of about
   (a) 115 W (b) 460 W (c) 2.3 kW (d) 230 W
6. A person of area 1.5 m², skin temperature 310 K, emissivity 0.80, stands in a room at 290 K. The net radiative loss is about
   (a) 147 W (b) 184 W (c) 74 W (d) 1.5 kW
7. The Sun's surface is at about 5800 K. Its radiation peaks at about
   (a) 500 nm (b) 290 nm (c) 5 μm (d) 58 nm
8. A star's radiation peaks at 290 nm. Its surface temperature is about
   (a) 1000 K (b) 5000 K (c) 10,000 K (d) 100,000 K
9. A glass window of area 2.0 m² and thickness 5.0 mm has k = 0.80 W m⁻¹ K⁻¹. With a temperature difference of 20 °C across it, the heat current is about
   (a) 64 W (b) 640 W (c) 64 kW (d) 6.4 kW

::: note Answers and explanations — Set C
**1.** (a) — $\theta_F=\frac{9}{5}(37)+32=98.6$ °F and $T=37+273=310$ K. Option (b) uses 273 − 37 by mistake.
**2.** (b) — the excess falls from 35 to 25 in 10 min, a factor 5/7. Another 10 min takes it to $25\times5/7=17.9$, so $\theta=25+17.9=42.9\approx43$ °C.
**3.** (b) — $H=\frac{A\Delta\theta}{L_1/k_1+L_2/k_2}=\frac{100}{5.0\times10^{-5}+0.050}\approx2.0\times10^3$ W.
**4.** (c) — the drop across the copper is $H L_1/(k_1A)=2000\times5.0\times10^{-5}=0.1$ °C, so the interface is at 99.9 °C. Nearly all the drop is across the insulator.
**5.** (d) — $P=\sigma AT^4=(5.67\times10^{-8})(0.50)(300)^4=2.3\times10^2$ W.
**6.** (a) — $P=\varepsilon\sigma A(T^4-T_s^4)=0.80(5.67\times10^{-8})(1.5)(2.16\times10^9)\approx147$ W.
**7.** (a) — $\lambda_{max}=2.9\times10^{-3}/5800=5.0\times10^{-7}$ m = 500 nm, in the visible.
**8.** (c) — $T=2.9\times10^{-3}/290\times10^{-9}=1.0\times10^4$ K.
**9.** (d) — $H=kA\Delta\theta/L=(0.80)(2.0)(20)/0.005=6.4\times10^3$ W. Real windows do better only because of the air films on both surfaces.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain conduction and thermal conductivity, and solve a problem on a composite rod. Compare conduction, convection and radiation. <span class="marks">[10]</span>
2. State and explain Stefan's law, Wien's law and Newton's law of cooling with numericals. <span class="marks">[10]</span>

```photogrid label="8.H" cols="3" ratio="1.25" caption="Heat transfer around us. (a) A thermal image of a house or person shows radiation from warm surfaces. (b) An electric kettle heats water by conduction through the element and by convection currents in the water. (c) A cooktop heats the pan by conduction and radiation."
@ photo id="ceephy3/thermal" cap="(a) Thermal image"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy3/kettle" cap="(b) Kettle"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy/cooktop" cap="(c) Cooktop"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: modes of heat transfer and conduction (10 marks)

**Introduction.** Heat flows from a hot body to a cold one by three modes: conduction, convection and radiation.

**Conduction.** In steady state, the heat flowing through a slab of area $A$ and thickness $d$ in time $t$ is $Q = \dfrac{kA(\theta_1 - \theta_2)t}{d}$, where $k$ is the **thermal conductivity** (W m⁻¹ K⁻¹). Metals have large $k$ (copper about $400$) because free electrons carry the heat. Air has $k \approx 0.026$, which is why wool, foam and double-glazed windows insulate.

**Composite conductors.**

1. In **series**, the same heat current flows through both: $\dfrac{k_1A(\theta_1 - \theta)}{l_1} = \dfrac{k_2A(\theta - \theta_2)}{l_2}$, where $\theta$ is the interface temperature. The equivalent conductivity is $k = \dfrac{l_1 + l_2}{l_1/k_1 + l_2/k_2}$.
2. In **parallel**, the heat currents add: $k = \dfrac{k_1A_1 + k_2A_2}{A_1 + A_2}$.

| Feature | Conduction | Convection | Radiation |
|---|---|---|---|
| Medium needed | Yes (solid) | Yes (fluid) | No |
| Particle motion | Vibration, no bulk movement | Bulk movement of fluid | None |
| Speed | Slow | Moderate | Speed of light |
| Example | Spoon in hot tea | Sea breeze | Sunlight on earth |

**Numerical.** A copper rod ($k = 400$) and a steel rod ($k = 50$), each $0.5\ \text{m}$ long and of equal area, are joined end to end, with the free ends at $100^{\circ}\text{C}$ (copper side) and $0^{\circ}\text{C}$. In steady state, $400(100 - \theta) = 50(\theta - 0)$, so $\theta = 40000/450 = 88.9^{\circ}\text{C}$. Almost all of the temperature drop is across the poor conductor, steel.

**Conclusion.** The rate of conduction is proportional to $kA\,\Delta\theta/d$. In series the poorer conductor controls the interface temperature.

### Model answer D2: radiation laws and Newton's law of cooling (10 marks)

**Introduction.** A **black body** absorbs all radiation that falls on it, and when hot it emits the maximum possible radiation at every wavelength.

**Laws.**

1. **Stefan-Boltzmann law.** The total energy emitted per second per unit area is $E = \sigma T^4$, with $\sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4}$. For a body at $T$ in surroundings at $T_0$, the net loss is $\sigma A(T^4 - T_0^4)$, and with emissivity $e$, $e\sigma A(T^4 - T_0^4)$.
2. **Wien's displacement law.** $\lambda_mT = b = 2.9\times10^{-3}\ \text{m K}$. As the temperature rises, the peak of the spectrum shifts to shorter wavelengths: red-hot, then white-hot.
3. **Newton's law of cooling.** For a small excess temperature, the rate of loss of heat is proportional to the excess over the surroundings: $-\dfrac{d\theta}{dt} = k(\theta - \theta_0)$. In practice $\dfrac{\theta_1 - \theta_2}{t} = k\left(\dfrac{\theta_1 + \theta_2}{2} - \theta_0\right)$.

**Other points.** Good absorbers are also good emitters (Kirchhoff's law). A polished surface reflects heat and is a poor emitter, so a thermos flask is silvered. Doubling the Kelvin temperature increases the radiated power sixteen times.

| Law | Gives | Graph / use |
|---|---|---|
| Stefan | total power $\propto T^4$ | temperature of stars |
| Wien | $\lambda_m \propto 1/T$ | colour and temperature |
| Newton | cooling rate $\propto$ excess temperature | cooling curve (exponential) |

**Numerical.**

- The sun's spectrum peaks near $500\ \text{nm}$, so $T = \dfrac{2.9\times10^{-3}}{5\times10^{-7}} = 5800\ \text{K}$. The power per unit area is $5.67\times10^{-8}\times(5800)^4 = 6.4\times10^{7}\ \text{W m}^{-2}$.
- A liquid cools from $80^{\circ}\text{C}$ to $70^{\circ}\text{C}$ in $5\ \text{min}$ in surroundings of $30^{\circ}\text{C}$. Then $k = \dfrac{10/5}{75 - 30} = \dfrac{2}{45}\ \text{min}^{-1}$. From $70^{\circ}\text{C}$ to $60^{\circ}\text{C}$: $t = \dfrac{10}{k(65 - 30)} = \dfrac{10\times45}{2\times35} = 6.4\ \text{min}$, slower because the excess temperature is lower.

**Conclusion.** Radiated power rises as $T^4$, the peak wavelength falls as $1/T$, and cooling slows down as the body approaches the surroundings.
