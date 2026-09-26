---
subject: Chemistry
grade: 11
unit: 17
title: Modern Chemical Manufactures
hours: 11
area: Applied Chemistry
---

Unit 16 gave you the grammar of industrial chemistry — stages, costs, batch
versus continuous, pollution. This unit gives you the sentences. Six
manufactures are named in the syllabus, and between them they make the four
"heavy chemicals" on which every other industry rests: ammonia, nitric acid,
sulphuric acid and alkali. A country's sulphuric acid output was once used as a
one-number index of how industrialised it was. Nepal makes none of these at
scale, which is exactly why the bag of urea a farmer in Bardiya buys has
crossed a border to get there.

::: key What the examiner wants from this unit
For **every** process: (i) the raw materials, (ii) the balanced equations,
(iii) the catalyst, temperature and pressure with a *reason* for each,
(iv) a labelled flow sheet, (v) the by-products and uses. The reasons are where
the marks hide. "450 °C" alone earns nothing; "450 °C — a compromise, because
the forward reaction is exothermic so a low temperature gives a better yield but
too slow a rate" earns the mark. Expect one 8-mark question from this unit in
almost every paper, plus stoichiometry numericals.
:::

## 17.1 Ammonia by Haber's process

Nitrogen is 78% of the air and utterly useless to most living things, because
the N≡N triple bond (945 kJ mol⁻¹) is one of the strongest in chemistry.
Fritz Haber's achievement in 1909, scaled up by Carl Bosch, was to break it with
a catalyst and so make **fixed nitrogen** — nitrogen in a combinable form —
available by the million tonnes. Roughly half the nitrogen atoms in your body
passed through a Haber plant.

### Raw materials

- **Nitrogen** — from the fractional distillation of liquid air.
- **Hydrogen** — from the steam reforming of natural gas:
  CH₄ + H₂O --Ni, 750 °C--> CO + 3H₂, followed by the water–gas shift
  CO + H₂O --Fe₂O₃--> CO₂ + H₂. The CO₂ is scrubbed out with a base and, in a
  fertilizer complex, sent next door to the urea plant.

The two gases are mixed in the stoichiometric ratio **N₂ : H₂ = 1 : 3 by
volume**, which is the ratio that gives the highest equilibrium conversion.

### The principle

$$ \mathrm{N_2(g) + 3H_2(g) \rightleftharpoons 2NH_3(g)} \qquad \Delta H = -92.4\ \mathrm{kJ\ mol^{-1}} $$

Three features of this equation dictate the whole plant:

1. It is **reversible**, so ammonia can never be made in 100% yield in one pass.
2. It is **exothermic**, so by Le Chatelier's principle a *low* temperature
   shifts the equilibrium to the right.
3. It goes from **4 moles of gas to 2**, so a *high* pressure shifts the
   equilibrium to the right.

::: derivation Equilibrium yield as a function of pressure
Start with 1 mol N₂ and 3 mol H₂ and let $x$ mol of N₂ react. At equilibrium:

| Species | Moles | Mole fraction |
|---|---|---|
| N₂ | $1-x$ | $(1-x)/(4-2x)$ |
| H₂ | $3(1-x)$ | $3(1-x)/(4-2x)$ |
| NH₃ | $2x$ | $2x/(4-2x)$ |
| total | $4-2x$ | 1 |

With partial pressure $p_i = y_i P$,

$$ K_p = \frac{p_{NH_3}^{2}}{p_{N_2}\,p_{H_2}^{3}} = \frac{4x^2(4-2x)^2}{27(1-x)^4}\cdot\frac{1}{P^{2}} $$

so $K_p P^{2}$ fixes $x$, and the ammonia content of the exit gas is
$y_{NH_3} = x/(2-x)$. Because $K_p$ falls steeply as $T$ rises (exothermic) and
the left-hand side carries $P^2$, **yield improves with pressure and worsens
with temperature** — the two curves you must be able to sketch.
:::

```figure caption="Equilibrium yield in the two great gas-phase syntheses. Both are exothermic, so every curve falls with temperature; ammonia also gains strongly with pressure because 4 mol of gas become 2, while $\mathrm{SO_2}$ oxidation is already above 97% at 2 atm so there is nothing to buy with extra pressure."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2,2.9))
R = 8.314

def solve(f, target, lo=1e-9, hi=1-1e-9):
    for _ in range(90):
        m = 0.5*(lo+hi)
        if f(m) < target: lo = m
        else: hi = m
    return 0.5*(lo+hi)

# ---- ammonia: N2 + 3H2 -> 2NH3 ----
T = np.linspace(573, 923, 220)
dH = -91800.0 - 45.3*(T-298.0)
dS = -198.1 - 45.3*np.log(T/298.0)
Kp = np.exp(-(dH - T*dS)/(R*T))                      # atm^-2
fA = lambda x: 4*x**2*(4-2*x)**2/(27*(1-x)**4)
for P, c in zip([50, 100, 200, 400], [SERIES[0], SERIES[2], SERIES[1], SERIES[3]]):
    y = [100*(lambda x: x/(2-x))(solve(fA, k*P*P)) for k in Kp]
    a1.plot(T-273.15, y, color=c, lw=1.7, label=f'{P} atm')
a1.axvline(450, color=MUTED, lw=0.9, ls=(0,(3,2)))
kop = np.interp(723.15, T, Kp); yop = 100*(lambda x: x/(2-x))(solve(fA, kop*200*200))
a1.plot([450], [yop], 'o', color=INK, ms=4.5, zorder=5)
a1.annotate(f'plant runs here\n450 °C, 200 atm\n≈ {yop:.0f} mol %', (450, yop),
            textcoords='offset points', xytext=(9, 20), fontsize=6.8, color=INK,
            linespacing=1.3,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
a1.set_xlabel('temperature  (°C)'); a1.set_ylabel('NH₃ at equilibrium  (mol %)')
a1.set_xlim(300, 650); a1.set_ylim(0, 100)
a1.legend(title='pressure', fontsize=7.0, title_fontsize=7.0, loc='upper right',
          labelspacing=0.28, handlelength=1.3)
a1.spines[['top','right']].set_visible(False); a1.grid(True, alpha=.5)
a1.set_title('Haber process', fontsize=8.6)

# ---- sulphur trioxide: 2SO2 + O2 -> 2SO3 ----
T2 = np.linspace(600, 1100, 220)
dH2 = -197800.0 - 7.8*(T2-298.0)
dS2 = -188.0 - 7.8*np.log(T2/298.0)
Kp2 = np.exp(-(dH2 - T2*dS2)/(R*T2))                 # atm^-1
fB = lambda a: a**2*(3-a)/(1-a)**3
for P, c in zip([1, 2, 10], [SERIES[0], SERIES[1], SERIES[2]]):
    y = [100*solve(fB, k*P) for k in Kp2]
    a2.plot(T2-273.15, y, color=c, lw=1.7, label=f'{P} atm')
a2.axvline(450, color=MUTED, lw=0.9, ls=(0,(3,2)))
k2op = np.interp(723.15, T2, Kp2); aop = 100*solve(fB, k2op*2)
a2.plot([450], [aop], 'o', color=INK, ms=4.5, zorder=5)
a2.annotate(f'plant runs here\n450 °C, 2 atm\n≈ {aop:.0f} %', (450, aop),
            textcoords='offset points', xytext=(9, -34), fontsize=6.8, color=INK,
            linespacing=1.3,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
a2.set_xlabel('temperature  (°C)'); a2.set_ylabel('SO₂ converted to SO₃  (%)')
a2.set_xlim(350, 800); a2.set_ylim(0, 102)
a2.legend(title='pressure', fontsize=7.0, title_fontsize=7.0, loc='lower left',
          labelspacing=0.28, handlelength=1.3)
a2.spines[['top','right']].set_visible(False); a2.grid(True, alpha=.5)
a2.set_title('Contact process', fontsize=8.6)
fig.tight_layout()
```

### Choosing the conditions

| Variable | Equilibrium wants | Rate wants | Plant uses | Why |
|---|---|---|---|---|
| Temperature | low | high | **450–500 °C** | a *compromise*: below ~400 °C the catalyst is too slow to be economic |
| Pressure | high | high | **200 atm** | both want high; the limit is the cost and safety of thick-walled vessels |
| Catalyst | no effect | high | **finely divided Fe with Mo or K₂O/Al₂O₃ promoters** | speeds both directions equally, so equilibrium is *reached sooner*, not shifted |
| Removal of NH₃ | shifts right | — | condensed out at −30 °C | Le Chatelier: removing a product pulls the equilibrium forward |

A single pass converts only about 15%. What makes the process economic is the
**recycle loop**: unreacted N₂ and H₂ are returned to the converter, so the
overall conversion of feed to ammonia exceeds 97%.

::: caution "A catalyst increases the yield"
It does not. A catalyst lowers the activation energy of the forward *and* the
reverse reaction by the same amount, so $K_p$ is unchanged. Iron lets the
converter reach equilibrium in seconds instead of years — it changes **how fast**
you get the yield, never **how much**. Write "the catalyst allows an acceptable
rate at a lower temperature, and the lower temperature is what improves the
yield."
:::

```figure caption="Flow sheet for the Haber process. The recycle loop is the commercially important part: single-pass conversion is only about 15%, but almost nothing is wasted."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.5))

def box(x, y, w, h, title, sub='', ec=ACCENT, fc='#eef3f9'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc=fc, ec=ec, lw=1.25))
    if sub:
        ax.text(x+w/2, y+h*0.68, title, fontsize=7.2, color=INK, ha='center', va='center')
        ax.text(x+w/2, y+h*0.27, sub, fontsize=6.4, color=MUTED, ha='center',
                va='center', linespacing=1.25)
    else:
        ax.text(x+w/2, y+h/2, title, fontsize=7.2, color=INK, ha='center', va='center')

def arr(p, q, c=INK, lw=1.4, ls='-'):
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, linestyle=ls,
                                mutation_scale=11))

W, H = 2.00, 0.86
yt, yb = 2.30, 0.50
x1, x2, x3 = 0.10, 2.50, 4.90

box(x1, yt, W, H, 'Purifier',   'removes S, CO,\nCO₂ and H₂O')
box(x2, yt, W, H, 'Compressor', '200 atm')
box(x3, yt, W, H, 'Catalyst chamber', 'Fe + Mo promoter\n450–500 °C')
box(x3, yb, W, H, 'Condenser',  'cooled to −30 °C')
box(x2, yb, W, H, 'Separator',  'liquid NH₃ run off')

arr((-1.05, yt+H/2), (0.10, yt+H/2), '#2e8b57')
ax.text(-1.62, yt+H+0.66, 'N₂ : H₂ = 1 : 3', fontsize=7.2, color='#2e8b57', ha='left')
ax.text(-1.62, yt+H+0.42, 'N₂ from liquid air;  H₂ from', fontsize=6.5, color=MUTED, ha='left')
ax.text(-1.62, yt+H+0.20, 'steam reforming of CH₄', fontsize=6.5, color=MUTED, ha='left')

arr((x1+W, yt+H/2), (x2-0.05, yt+H/2))
arr((x2+W, yt+H/2), (x3-0.05, yt+H/2))
arr((x3+W/2+0.42, yt-0.03), (x3+W/2+0.42, yb+H+0.05), '#d9534f')
ax.text(x3+W/2+0.55, (yt+yb+H)/2, 'NH₃ +\nunreacted\nN₂ , H₂', fontsize=6.5,
        color='#d9534f', ha='left', va='center', linespacing=1.25)
arr((x3-0.05, yb+H/2), (x2+W, yb+H/2))
arr((x2+0.45, yb-0.05), (x2+0.45, -0.35), '#8a6d1f')
ax.text(x2+0.60, -0.30, 'liquid ammonia  (b.p. −33 °C)', fontsize=7.0,
        color='#8a6d1f', ha='left', va='center')

arr((x3-0.42, yb+H+0.05), (x3-0.42, yt-0.03), MUTED, lw=1.2, ls=(0,(4,2)))
ax.text(x3-0.55, (yt+yb+H)/2, 'unreacted gas\nrecycled', fontsize=6.5, color=MUTED,
        ha='right', va='center', linespacing=1.25)

ax.text(2.85, 4.00, 'N₂ + 3H₂  ⇌  2NH₃      ΔH = −92.4 kJ mol⁻¹',
        fontsize=7.8, color=INK, ha='center')
ax.set_position([0,0,1,1])
ax.set_xlim(-1.70, 7.40); ax.set_ylim(-0.62, 4.22); ax.axis('off')
```

| Haber process at a glance | |
|---|---|
| Raw materials | air (N₂), natural gas + steam (H₂) |
| Conditions | 450–500 °C, 200 atm, 1 : 3 N₂ : H₂ |
| Catalyst | finely divided iron, promoted with molybdenum (or K₂O + Al₂O₃) |
| Key reaction | N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92.4 kJ mol⁻¹ |
| By-products | CO₂ from the reforming step (used to make urea); purge gas burnt as fuel |
| Uses | urea and other fertilizers, nitric acid, explosives, nylon, refrigerant, cleaning agents |

::: example Limiting reactant and percentage yield in a converter
**Problem.** A converter is charged with 1400 kg of N₂ and 240 kg of H₂. The
plant recovers 1088 kg of ammonia. Find the limiting reactant, the theoretical
yield and the percentage yield. (N = 14, H = 1)

**Solution.**
Moles of N₂ = 1400 kg ÷ 28 kg kmol⁻¹ = 50 kmol.
Moles of H₂ = 240 kg ÷ 2 kg kmol⁻¹ = 120 kmol.

The equation needs 3 mol H₂ per mol N₂, so 50 kmol of N₂ would need
3 × 50 = 150 kmol of H₂. Only 120 kmol is available, so **hydrogen is the
limiting reactant** (and 40 kmol of N₂ is in excess).

From 2NH₃ per 3H₂: n(NH₃) = 120 × 2/3 = 80 kmol.
Theoretical yield = 80 kmol × 17 kg kmol⁻¹ = **1360 kg**.

$$ \text{percentage yield} = \frac{1088}{1360}\times 100 = 80\% $$
:::

## 17.2 Nitric acid by Ostwald's process

Before 1900 the world's nitric acid came from Chilean saltpetre. Wilhelm
Ostwald's process (1902) makes it from ammonia and air instead, so a Haber plant
and an Ostwald plant together turn atmospheric nitrogen into nitrate. The two
are almost always built on the same site.

The manufacture is three oxidations in series.

**Step 1 — catalytic oxidation of ammonia.** One volume of ammonia to 8–10
volumes of air is passed through a glowing platinum–rhodium (90 : 10) gauze at
**800 °C**. The contact time is about 10⁻³ s:

4NH₃ + 5O₂ --Pt/Rh, 800 °C--> 4NO + 6H₂O,  ΔH = −905 kJ mol⁻¹

The reaction is so exothermic that once lit the gauze stays red hot without
external heating. The contact time must be very short, because if the gases
linger the nitric oxide decomposes back to nitrogen and oxygen.

**Step 2 — oxidation of nitric oxide.** The gas is cooled in a heat exchanger
(raising steam for the rest of the plant) to about 50 °C and mixed with more
air:

2NO + O₂ ⇌ 2NO₂,  ΔH = −114 kJ mol⁻¹

This is an unusual reaction — it goes *faster at lower temperature* — so cooling
helps both the rate and the equilibrium.

**Step 3 — absorption in water.** The nitrogen dioxide is passed up an
absorption tower packed with quartz, against a downward spray of warm water, in
the presence of excess air:

3NO₂ + H₂O → 2HNO₃ + NO   and   4NO₂ + O₂ + 2H₂O → 4HNO₃

The NO released in the first of these is swept back into the oxidation chamber,
so with enough air the overall equation is simply

NH₃ + 2O₂ → HNO₃ + H₂O

The tower produces about **68% nitric acid**, which is the constant-boiling
(azeotropic) mixture and cannot be concentrated further by distillation alone.
To reach 98% "fuming" acid the 68% acid is distilled with a dehydrating agent —
concentrated sulphuric acid or magnesium nitrate.

```figure caption="Flow sheet for the Ostwald process. Nitrogen is oxidised in three stages: $\mathrm{NH_3 \to NO \to NO_2 \to HNO_3}$, with the NO made in the absorber recycled."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.0))

def box(x, y, w, h, title, sub='', rxn=''):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc='#eef3f9', ec=ACCENT, lw=1.25))
    ax.text(x+w/2, y+h*0.76, title, fontsize=7.2, color=INK, ha='center', va='center')
    if sub:
        ax.text(x+w/2, y+h*0.48, sub, fontsize=6.2, color=MUTED, ha='center', va='center')
    if rxn:
        ax.text(x+w/2, y+h*0.18, rxn, fontsize=6.2, color='#1d6fb8', ha='center', va='center')

def arr(p, q, c=INK, lw=1.4, ls='-'):
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, linestyle=ls,
                                mutation_scale=11))

W, H = 2.45, 1.15
yt, yb = 2.35, 0.50
x1, x2, x3 = 0.10, 2.95, 5.80

box(x1, yt, W, H, 'Catalytic chamber', 'Pt–Rh gauze, 800 °C, ~10⁻³ s',
    '4NH₃ + 5O₂ → 4NO + 6H₂O')
box(x2, yt, W, H, 'Cooler / heat exchanger', 'gas cooled to 50 °C', 'steam raised for the plant')
box(x3, yt, W, H, 'Oxidation chamber', 'excess air, 50 °C', '2NO + O₂ → 2NO₂')
box(x3, yb, W, H, 'Absorption tower', 'water down, air up', '3NO₂ + H₂O → 2HNO₃ + NO')
box(x2, yb, W, H, 'Concentrator', 'distil to 68%, then', 'dehydrate with conc. H₂SO₄')

arr((-0.72, yt+H*0.72), (0.05, yt+H*0.72), '#2e8b57')
arr((-0.72, yt+H*0.30), (0.05, yt+H*0.30), '#2e8b57')
ax.text(-0.78, yt+H*0.72, 'NH₃', fontsize=7.0, color='#2e8b57', ha='right', va='center')
ax.text(-0.78, yt+H*0.30, 'air', fontsize=7.0, color='#2e8b57', ha='right', va='center')
ax.text(-1.12, yt+H+0.22, '1 vol NH₃ : 8–10 vol air', fontsize=6.4, color=MUTED, ha='left')

arr((x1+W, yt+H/2), (x2-0.05, yt+H/2))
arr((x2+W, yt+H/2), (x3-0.05, yt+H/2))
arr((x3+W/2, yt-0.03), (x3+W/2, yb+H+0.05), '#d9534f')
ax.text(x3+W/2+0.10, (yt+yb+H)/2, 'NO₂', fontsize=6.8, color='#d9534f', ha='left', va='center')
arr((x3-0.05, yb+H/2), (x2+W, yb+H/2))
arr((x2+W/2, yb-0.05), (x2+W/2, -0.62), '#8a6d1f')
ax.text(x2+W/2+0.12, -0.55, '98% nitric acid', fontsize=7.0, color='#8a6d1f',
        ha='left', va='center')
arr((x3+W, yb+H*0.70), (x3+W+0.55, yb+H*0.70), MUTED, lw=1.2, ls=(0,(4,2)))
ax.text(x3+W+0.62, yb+H*0.70, 'NO recycled', fontsize=6.4, color=MUTED, ha='left', va='center')

ax.text(3.65, 4.10, 'Overall:   NH₃ + 2O₂  →  HNO₃ + H₂O', fontsize=7.4, color=INK, ha='center')
ax.set_position([0,0,1,1])
ax.set_xlim(-1.25, 9.05); ax.set_ylim(-0.90, 4.32); ax.axis('off')
```

| Ostwald process at a glance | |
|---|---|
| Raw materials | ammonia, air, water |
| Conditions | 800 °C and 4–10 atm at the gauze; ~50 °C in the oxidiser and absorber |
| Catalyst | platinum–rhodium (90 : 10) gauze |
| Key reactions | 4NH₃ + 5O₂ → 4NO + 6H₂O; 2NO + O₂ ⇌ 2NO₂; 3NO₂ + H₂O → 2HNO₃ + NO |
| By-products | high-pressure steam (sold or used); tail gas containing NOₓ, which must be abated |
| Uses | ammonium nitrate and NPK fertilizers, explosives (TNT, nitroglycerine), dyes, nitration in organic synthesis, metal pickling |

::: example From ammonia to bottled acid
**Problem.** An Ostwald unit is fed 170 kg of ammonia per hour. The overall
conversion of NH₃ to HNO₃ is 90%. Calculate (a) the mass of pure HNO₃ made per
hour, and (b) the mass of 68% (by mass) acid this corresponds to.
(H = 1, N = 14, O = 16)

**Solution.**
(a) Overall: NH₃ + 2O₂ → HNO₃ + H₂O, a 1 : 1 mole ratio.

n(NH₃) = 170 kg ÷ 17 kg kmol⁻¹ = 10 kmol.
Theoretical n(HNO₃) = 10 kmol, so theoretical mass = 10 × 63 = 630 kg.
At 90%: mass of pure HNO₃ = 0.90 × 630 = **567 kg per hour**.

(b) If 100 kg of product acid contains 68 kg of HNO₃,

$$ \text{mass of 68\% acid} = \frac{567}{0.68} = 833.8\ \mathrm{kg\ per\ hour} $$
:::

## 17.3 Sulphuric acid by contact process

Sulphuric acid is the most-produced chemical in the world by mass. It is cheap,
a strong acid, a dehydrating agent, an oxidising agent at high concentration and
a high-boiling liquid — so it turns up in fertilizer manufacture (its largest
single use), detergents, dyes, paints, batteries and metal processing. The
**contact process** is named for the contact between the gases and the solid
catalyst.

### Stage 1 — making sulphur dioxide

Either by burning sulphur in dry air,

S + O₂ → SO₂,  ΔH = −297 kJ mol⁻¹

or by roasting iron pyrites,

4FeS₂ + 11O₂ --Δ--> 2Fe₂O₃ + 8SO₂

### Stage 2 — purifying the gas

This is the stage students forget, and it carries marks. The V₂O₅ catalyst is
poisoned by arsenic oxide and fouled by dust and moisture, so the burner gas is
put through, in order: a **dust chamber** (steam, and electrostatic
precipitation, to settle solid particles), **cooling pipes**, a **washing
tower** (water spray removes soluble impurities), an **arsenic purifier**
(ferric hydroxide adsorbs As₂O₃), a **testing box**, and finally a **drying
tower** where concentrated sulphuric acid removes water vapour.

### Stage 3 — the catalytic oxidation

$$ \mathrm{2SO_2(g) + O_2(g) \rightleftharpoons 2SO_3(g)} \qquad \Delta H = -196\ \mathrm{kJ\ mol^{-1}} $$

Exothermic, and 3 mol of gas become 2 — the same shape of problem as the Haber
process, so the same reasoning applies. But look again at the right-hand panel
of the yield figure: at 450 °C and only **2 atm** the equilibrium conversion is
already about 97%. There is almost nothing left to gain from high pressure, so
the plant runs at a little above atmospheric pressure and saves the cost of
compressors and pressure vessels. **This contrast with the Haber process is a
favourite examination question.**

Vanadium(V) oxide is used rather than the faster platinum because it is far
cheaper and is not poisoned by traces of arsenic.

### Stage 4 — absorption

SO₃ is not absorbed directly in water. Doing so produces a dense, persistent
acid mist that neither settles nor dissolves, and most of the SO₃ escapes up the
stack. Instead it is absorbed in 98% sulphuric acid to give **oleum**
(fuming sulphuric acid, pyrosulphuric acid), which is then diluted:

SO₃ + H₂SO₄ → H₂S₂O₇   then   H₂S₂O₇ + H₂O → 2H₂SO₄

::: caution Never write "SO₃ + H₂O → H₂SO₄" as the plant step
That reaction is thermodynamically fine and completely useless industrially,
because it produces an uncondensable mist. The mark scheme wants the **two-step
oleum route** and the reason for it. The same mistake in reverse: do not add
water to concentrated acid in the laboratory — always acid to water.
:::

```figure caption="Flow sheet for the contact process. The long purification train exists to protect the vanadium(V) oxide catalyst from dust, moisture and arsenic."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.3))

def box(x, y, w, h, title, sub='', ec=ACCENT, fc='#eef3f9'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc=fc, ec=ec, lw=1.25))
    ax.text(x+w/2, y+h*0.68, title, fontsize=6.9, color=INK, ha='center', va='center')
    ax.text(x+w/2, y+h*0.26, sub, fontsize=5.9, color=MUTED, ha='center', va='center')

def arr(p, q, c=INK, lw=1.3, ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                                    linestyle=ls, mutation_scale=10))

W, H, g = 2.00, 0.92, 0.28
xs = [0.15 + i*(W+g) for i in range(4)]
yA, yB, yC = 3.55, 1.95, 0.35

box(xs[0], yA, W, H, 'Burner',        'S or FeS₂ + air')
box(xs[1], yA, W, H, 'Dust chamber',  'steam + hot plates')
box(xs[2], yA, W, H, 'Cooling pipes', 'cooled to ~100 °C')
box(xs[3], yA, W, H, 'Washing tower', 'water spray')

box(xs[3], yB, W, H, 'Drying tower',     'conc. H₂SO₄')
box(xs[2], yB, W, H, 'Arsenic purifier', 'Fe(OH)₃ removes As₂O₃')
box(xs[1], yB, W, H, 'Testing box',      'purity checked')
box(xs[0], yB, W, H, 'Contact tower',    'V₂O₅, 450 °C, 2 atm')

box(xs[0], yC, W, H, 'Absorption tower', '98% H₂SO₄ → oleum')
box(xs[1], yC, W, H, 'Dilution tank',    'H₂S₂O₇ + H₂O')

arr((-0.70, yA+H/2), (0.10, yA+H/2), '#2e8b57')
ax.text(-0.76, yA+H/2, 'air', fontsize=6.8, color='#2e8b57', ha='right', va='center')
for i in range(3):
    arr((xs[i]+W, yA+H/2), (xs[i+1]-0.04, yA+H/2))
arr((xs[3]+W/2, yA-0.03), (xs[3]+W/2, yB+H+0.04), '#d9534f')
ax.text(xs[3]+W/2+0.10, (yA+yB+H)/2, 'SO₂', fontsize=6.4, color='#d9534f', ha='left', va='center')
for i in (3, 2, 1):
    arr((xs[i]-0.04, yB+H/2), (xs[i-1]+W, yB+H/2))
arr((xs[0]+W/2, yB-0.03), (xs[0]+W/2, yC+H+0.04), '#d9534f')
ax.text(xs[0]+W/2+0.10, (yB+yC+H)/2, 'SO₃', fontsize=6.4, color='#d9534f', ha='left', va='center')
arr((xs[0]+W, yC+H/2), (xs[1]-0.04, yC+H/2))
arr((xs[1]+W, yC+H/2), (xs[1]+W+0.75, yC+H/2), '#8a6d1f')
ax.text(xs[1]+W+0.82, yC+H/2, '98% H₂SO₄', fontsize=6.9, color='#8a6d1f', ha='left', va='center')

ax.text(0.15, 4.92, 'S + O₂ → SO₂        4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂', fontsize=6.6,
        color=INK, ha='left')
ax.text(0.15, 4.66, '2SO₂ + O₂ ⇌ 2SO₃   ΔH = −196 kJ mol⁻¹', fontsize=6.6,
        color=INK, ha='left')
ax.text(5.55, 4.92, 'SO₃ + H₂SO₄ → H₂S₂O₇', fontsize=6.6, color=INK, ha='left')
ax.text(5.55, 4.66, 'H₂S₂O₇ + H₂O → 2H₂SO₄', fontsize=6.6, color=INK, ha='left')
ax.text(6.55, yC+H*0.52, 'purification: the SO₂ must be\nfree of dust, moisture and\narsenic — As₂O₃ poisons the\nV₂O₅ catalyst',
        fontsize=6.2, color=MUTED, ha='left', va='center', linespacing=1.35)

ax.set_position([0,0,1,1])
ax.set_xlim(-1.20, 9.45); ax.set_ylim(0.05, 5.15); ax.axis('off')
```

| Contact process at a glance | |
|---|---|
| Raw materials | sulphur (or iron pyrites), dry air, water |
| Conditions | 450 °C, 2 atm, purified and dried gas |
| Catalyst | vanadium(V) oxide, V₂O₅, on a silica support |
| Key reaction | 2SO₂ + O₂ ⇌ 2SO₃, ΔH = −196 kJ mol⁻¹ |
| By-products | Fe₂O₃ (cinder, to the steel industry) when pyrites is used; waste heat recovered as steam; unabsorbed SO₂ in the tail gas |
| Uses | fertilizers (superphosphate, ammonium sulphate), detergents, dyes, paints, lead–acid batteries, pickling of steel, petroleum refining |

::: example Sulphuric acid from pyrites
**Problem.** 1.20 tonnes of iron pyrites, FeS₂, is roasted. Every sulphur atom
is eventually converted to sulphuric acid with an overall efficiency of 95%.
Calculate the mass of H₂SO₄ obtained. (Fe = 56, S = 32, O = 16, H = 1)

**Solution.**
Molar mass of FeS₂ = 56 + 2(32) = 120 g mol⁻¹.
n(FeS₂) = 1200 kg ÷ 120 kg kmol⁻¹ = 10 kmol.

From 4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂, each FeS₂ gives 2 SO₂:
n(SO₂) = 20 kmol. Then 2SO₂ + O₂ → 2SO₃ and SO₃ → H₂SO₄ are both 1 : 1, so
theoretical n(H₂SO₄) = 20 kmol.

Theoretical mass = 20 kmol × 98 kg kmol⁻¹ = 1960 kg.
Actual mass = 0.95 × 1960 = **1862 kg = 1.862 tonnes**.
:::

## 17.4 Sodium hydroxide by Diaphragm Cell

Sodium hydroxide (caustic soda) and chlorine are made together by electrolysing
brine — the **chlor-alkali industry**. The awkward part is not the electrolysis
but keeping the two products apart: if hydroxide ions reach the chlorine, they
react at once to give bleach and then chlorate,

Cl₂ + 2NaOH → NaCl + NaOCl + H₂O

so the cell must be designed to prevent mixing. The **diaphragm cell** does this
with a porous barrier and a difference in liquid level.

### Construction and action

The cell is a steel tank divided by a **diaphragm of asbestos** (now usually a
polymer-modified asbestos or a synthetic fibre) deposited on a **perforated
steel cathode**. The anode is **titanium coated with a ruthenium oxide**
(graphite in older plants). Saturated purified brine (about 25% NaCl) is fed
continuously into the anode compartment and kept at a *higher level* than the
liquid in the cathode compartment, so the flow of liquid through the diaphragm
is always from anode to cathode.

At the anode (oxidation):  2Cl⁻ → Cl₂ + 2e⁻

At the cathode (reduction):  2H₂O + 2e⁻ → H₂ + 2OH⁻

Overall:  2NaCl + 2H₂O --electrolysis--> 2NaOH + H₂ + Cl₂

Sodium ions migrate through the diaphragm to the cathode compartment to balance
the charge; hydroxide ions try to migrate the opposite way, but the bulk flow of
brine through the diaphragm sweeps them back. That is the whole trick.

::: caution Sodium metal is *not* formed at the cathode
Na⁺ has a far more negative discharge potential than water, so in aqueous
solution water is reduced instead and hydrogen comes off. Sodium metal is made
by electrolysing *molten* NaCl (Down's cell), not brine. Cells are also never
run hot and never allowed to leak gas between compartments, because a
hydrogen–chlorine mixture explodes in light.
:::

```figure caption="The diaphragm cell. The brine level on the anode side is deliberately kept higher, so percolation through the diaphragm carries $\mathrm{Na^+}$ across while sweeping $\mathrm{OH^-}$ away from the chlorine."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.6))

ax.add_patch(Rectangle((0.50,0.50), 6.60, 2.95, fc='#f4f6f9', ec=INK, lw=1.6))
ax.add_patch(Rectangle((0.56,0.56), 3.00, 2.62, fc=ACCENT, alpha=0.13, ec='none'))
ax.add_patch(Rectangle((3.92,0.56), 3.12, 2.22, fc=ACCENT, alpha=0.13, ec='none'))
ax.plot([0.56,3.56],[3.18,3.18], color=ACCENT, lw=1.0)
ax.plot([3.92,7.04],[2.78,2.78], color=ACCENT, lw=1.0)

# diaphragm + cathode
ax.add_patch(Rectangle((3.60,0.56), 0.14, 2.62, fc='#e6e9ef', ec=MUTED, lw=0.9, hatch='///'))
ax.add_patch(Rectangle((3.74,0.56), 0.16, 2.62, fc='#9aa2ae', ec=INK, lw=1.0))
# anode
ax.add_patch(Rectangle((1.00,0.70), 0.18, 2.35, fc='#8a6d1f', ec=INK, lw=1.0))

# electrode leads and terminals
ax.plot([1.09,1.09],[3.05,3.62], color='#8a6d1f', lw=1.4)
ax.plot([3.82,3.82],[3.18,3.62], color=INK, lw=1.4)
ax.text(1.09, 3.80, '+', fontsize=11, color='#8a6d1f', ha='center', va='center')
ax.text(3.82, 3.80, '−', fontsize=11, color=INK, ha='center', va='center')
ax.text(1.24, 3.80, 'anode\n(titanium)', fontsize=6.5, color='#8a6d1f', ha='left',
        va='center', linespacing=1.25)

ax.annotate('', xy=(0.82,3.02), xytext=(-0.70,3.95),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.5, mutation_scale=11))
ax.text(-0.90, 4.14, 'saturated brine, 25% NaCl', fontsize=6.6, color='#2e8b57',
        ha='left', va='center')
ax.annotate('', xy=(2.45,4.05), xytext=(2.45,3.30),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5, mutation_scale=11))
ax.text(2.53,4.00,'Cl₂', fontsize=7.4, color='#d9534f', ha='left', va='top')
ax.annotate('', xy=(6.35,4.05), xytext=(6.35,3.00),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.5, mutation_scale=11))
ax.text(6.43,4.00,'H₂', fontsize=7.4, color='#2e8b57', ha='left', va='top')

# diaphragm label placed below the cell with a short leader
ax.plot([3.67,3.67],[0.50,-0.06], color=MUTED, lw=0.7, ls=(0,(3,2)))
ax.text(3.67, -0.12, 'asbestos diaphragm on perforated steel cathode',
        fontsize=6.0, color=MUTED, ha='center', va='top')

ax.annotate('', xy=(8.05,0.85), xytext=(7.05,0.85),
            arrowprops=dict(arrowstyle='-|>', color='#8a6d1f', lw=1.5, mutation_scale=11))
ax.text(8.10,0.85,'cell liquor\n11% NaOH + 16% NaCl', fontsize=6.6, color='#8a6d1f',
        ha='left', va='center', linespacing=1.25)
ax.annotate('', xy=(3.40,3.24), xytext=(7.22,3.24),
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, ls=(0,(3,2))))
ax.text(7.28, 3.05, 'the brine level is kept\nhigher on the anode side,\nso liquid percolates through\nthe diaphragm and OH⁻\nnever reaches the anode',
        fontsize=6.3, color=MUTED, ha='left', va='center', linespacing=1.35)

ax.text(1.32, 2.40, 'anolyte\n2Cl⁻ → Cl₂ + 2e⁻', fontsize=6.7, color=INK, ha='left',
        va='center', linespacing=1.3)
ax.text(4.05, 2.35, 'catholyte\n2H₂O + 2e⁻ → H₂ + 2OH⁻', fontsize=6.7, color=INK,
        ha='left', va='center', linespacing=1.3)

ax.annotate('', xy=(4.25,1.45), xytext=(2.35,1.45),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=10))
ax.text(2.10,1.58,'Na⁺ migrates', fontsize=6.2, color=ACCENT, ha='left', va='bottom')
ax.annotate('', xy=(3.45,0.95), xytext=(4.60,0.95),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.3, mutation_scale=10))
ax.plot([3.52,3.52],[0.80,1.10], color='#d9534f', lw=2.0)
ax.text(4.68,0.95,'OH⁻ held back', fontsize=6.5, color='#d9534f', ha='left', va='center')

ax.text(3.55, -0.72, 'Overall:   2NaCl + 2H₂O  →  2NaOH + H₂ + Cl₂', fontsize=7.2,
        color=INK, ha='center', va='center')
ax.set_position([0,0,1,1])
ax.set_xlim(-0.95, 10.60); ax.set_ylim(-1.00, 4.42); ax.axis('off')
```

The liquid drawn from the cathode compartment is called **cell liquor** and is
only about 11% NaOH contaminated with 16% NaCl. It is evaporated in multiple
effect evaporators; sodium chloride is much less soluble in strong alkali and
crystallises out, and is returned to the brine feed. The product is 50% caustic
soda liquor, from which solid flakes can be obtained.

| Diaphragm cell at a glance | |
|---|---|
| Raw materials | saturated purified brine (25% NaCl), electricity |
| Conditions | 60–70 °C, 3.5–4 V per cell, current densities of a few kA m⁻² |
| Catalyst | none — an electrolytic process; the anode coating (RuO₂ on Ti) is an electrocatalyst |
| Key reactions | anode 2Cl⁻ → Cl₂ + 2e⁻; cathode 2H₂O + 2e⁻ → H₂ + 2OH⁻ |
| By-products | chlorine and hydrogen (both sold; often burnt together to make HCl) |
| Uses | soap and detergents, paper pulping, alumina from bauxite, rayon, petroleum refining, drain cleaner, laboratory reagent |

::: example A day's output from one cell
**Problem.** A diaphragm cell carries a current of 30 000 A for 24 hours with a
current efficiency of 96%. Calculate (a) the mass of NaOH produced and (b) the
volume of chlorine at STP. (Na = 23, O = 16, H = 1; F = 96 500 C mol⁻¹;
molar volume at STP = 22.4 L mol⁻¹)

**Solution.**
Charge passed, Q = I t = 30 000 A × (24 × 3600) s = 2.592 × 10⁹ C.

$$ n(e^-)\ \text{available} = \frac{2.592\times 10^{9}}{96\,500} = 2.686\times 10^{4}\ \mathrm{mol} $$

Useful electrons = 0.96 × 2.686 × 10⁴ = 2.579 × 10⁴ mol.

(a) The cathode reaction 2H₂O + 2e⁻ → H₂ + 2OH⁻ gives **one OH⁻ per electron**,
and each OH⁻ pairs with an Na⁺, so n(NaOH) = 2.579 × 10⁴ mol.

mass = 2.579 × 10⁴ mol × 40 g mol⁻¹ = 1.031 × 10⁶ g = **1031 kg**

(b) The anode reaction 2Cl⁻ → Cl₂ + 2e⁻ needs **two electrons per Cl₂**:

n(Cl₂) = ½ × 2.579 × 10⁴ = 1.289 × 10⁴ mol
V = 1.289 × 10⁴ × 22.4 = 2.888 × 10⁵ L = **288.8 m³**
:::

## 17.5 Sodium carbonate by ammonia soda (Solvay) process

Sodium carbonate (soda ash, washing soda as the decahydrate Na₂CO₃·10H₂O) is
needed by the glass industry above all — roughly half of world output goes into
glass — and also for soaps, paper, water softening and detergent builders.
Ernest Solvay's 1861 process makes it from two of the cheapest raw materials on
Earth, common salt and limestone, using ammonia that is recovered and used over
and over again. The **overall** equation is deceptively simple:

2NaCl + CaCO₃ → Na₂CO₃ + CaCl₂

This reaction will not happen if you simply mix the two solids — it is the wrong
way round thermodynamically in solution. Solvay's insight was to reach the same
result through four steps that each *do* work.

**1. Ammoniation.** Purified, saturated brine is run down an **ammoniation
tower** against a rising stream of ammonia gas. Any Ca²⁺ and Mg²⁺ in the brine
is precipitated here and filtered off, which also purifies the feed.

**2. Carbonation.** The ammoniated brine is run down a **carbonating (Solvay)
tower** fitted with perforated mushroom-shaped baffles, against carbon dioxide
rising from below. The tower is warm at the top (about 40 °C) and cooled to
about 20 °C at the bottom:

NH₃ + H₂O + CO₂ → NH₄HCO₃

NH₄HCO₃ + NaCl → NaHCO₃↓ + NH₄Cl

Sodium hydrogencarbonate is the **least soluble** substance present, so it
crystallises out. Everything turns on that one solubility fact.

**3. Filtration and calcination.** The NaHCO₃ is filtered on a rotary vacuum
filter and heated to about 150–200 °C in a calciner:

2NaHCO₃ --Δ--> Na₂CO₃ + H₂O + CO₂↑

Half the carbon dioxide needed by the tower comes back from this step.

**4. Ammonia recovery.** The filtrate is ammonium chloride solution. It is
warmed with milk of lime:

2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2NH₃↑ + 2H₂O

The ammonia goes straight back to the ammoniation tower, which is why the
process consumes almost no ammonia — only make-up for losses.

The lime and the remaining CO₂ come from a **lime kiln** burning limestone with
coke:

CaCO₃ --1000 °C--> CaO + CO₂↑   and   CaO + H₂O → Ca(OH)₂

```figure caption="Flow sheet for the Solvay (ammonia-soda) process. Two closed loops — ammonia and carbon dioxide — make an apparently impossible overall reaction economic; the only waste is calcium chloride solution."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.4))

def box(x, y, w, h, title, sub=''):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc='#eef3f9', ec=ACCENT, lw=1.25))
    ax.text(x+w/2, y+h*0.68, title, fontsize=6.4, color=INK, ha='center', va='center')
    ax.text(x+w/2, y+h*0.26, sub, fontsize=5.8, color=MUTED, ha='center', va='center')

def arr(p, q, c=INK, lw=1.3, ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                                    linestyle=ls, mutation_scale=10))

def path(pts, c, ls=(0,(4,2)), lw=1.15):
    ax.plot([p[0] for p in pts[:-1]], [p[1] for p in pts[:-1]], color=c, lw=lw, ls=ls)
    arr(pts[-2], pts[-1], c, lw=lw, ls=ls)

W, H, g = 2.00, 0.92, 0.28
xs = [0.15 + i*(W+g) for i in range(4)]
yA, yB = 2.80, 0.55

box(xs[0], yA, W, H, 'Brine saturator',   'saturated, purified')
box(xs[1], yA, W, H, 'Ammoniation tower', 'NaCl + NH₃ solution')
box(xs[2], yA, W, H, 'Carbonating tower', 'CO₂ up, 40 → 20 °C')
box(xs[3], yA, W, H, 'Rotary filter',     'NaHCO₃ filtered off')
box(xs[0], yB, W, H, 'Ammonia recovery',  '2NH₄Cl + Ca(OH)₂')
box(xs[2], yB, W, H, 'Lime kiln',         'CaCO₃ → CaO + CO₂')
box(xs[3], yB, W, H, 'Calciner, 150 °C',  '2NaHCO₃ → Na₂CO₃')

arr((-0.72, yA+H/2), (0.10, yA+H/2), '#2e8b57')
ax.text(-0.78, yA+H/2, 'NaCl', fontsize=6.8, color='#2e8b57', ha='right', va='center')
for i in range(3):
    arr((xs[i]+W, yA+H/2), (xs[i+1]-0.04, yA+H/2))
ax.text(xs[2]+W/2, yA+H+0.18, 'NaCl + NH₃ + CO₂ + H₂O → NaHCO₃↓ + NH₄Cl',
        fontsize=6.3, color=INK, ha='center')

arr((8.49, yA-0.03), (8.49, yB+H+0.04), '#d9534f')
ax.text(8.57, (yA+yB+H)/2, 'NaHCO₃', fontsize=6.3, color='#d9534f', ha='left', va='center')
arr((7.54, yB-0.03), (7.54, -0.45), '#8a6d1f')
ax.text(7.64, -0.40, 'Na₂CO₃  (soda ash)', fontsize=6.8, color='#8a6d1f', ha='left', va='center')

arr((xs[2]+W/2, yB-0.48), (xs[2]+W/2, yB-0.04), '#2e8b57')
ax.text(xs[2]+W/2, yB-0.56, 'CaCO₃ + coke', fontsize=6.4, color='#2e8b57',
        ha='center', va='top')
arr((5.26, yB+H+0.04), (5.26, yA-0.03), MUTED)
ax.text(5.18, (yA+yB+H)/2, 'CO₂', fontsize=6.3, color=MUTED, ha='right', va='center')
path([(7.30, yB+H+0.04), (7.30, 2.15), (6.16, 2.15), (6.16, yA-0.03)], MUTED)
ax.text(7.38, 2.20, 'CO₂ recycled', fontsize=6.2, color=MUTED, ha='left', va='bottom')
arr((xs[2]-0.04, yB+H/2), (xs[0]+W, yB+H/2))
ax.text((xs[0]+W+xs[2])/2, yB+H/2+0.15, 'CaO + H₂O → Ca(OH)₂', fontsize=6.3,
        color=INK, ha='center')
path([(1.60, yB+H+0.04), (1.60, 2.15), (3.13, 2.15), (3.13, yA-0.03)], '#2e8b57')
ax.text(1.68, 2.20, 'NH₃ recycled', fontsize=6.2, color='#2e8b57', ha='left', va='bottom')
path([(xs[3]+W, yA+H*0.30), (9.62, yA+H*0.30), (9.62, -0.92), (0.70, -0.92),
      (0.70, yB-0.03)], '#1d6fb8', ls='-')
ax.text(4.60, -1.04, 'NH₄Cl solution (filtrate)', fontsize=6.3, color='#1d6fb8',
        ha='center', va='top')
arr((xs[0]-0.04, yB+H*0.28), (xs[0]-0.72, yB+H*0.28), '#8a6d1f')
ax.text(xs[0]-0.78, yB+H*0.28, 'CaCl₂\nwaste', fontsize=6.3, color='#8a6d1f',
        ha='right', va='center', linespacing=1.25)

ax.text(4.55, 4.30, 'Overall:   2NaCl + CaCO₃  →  Na₂CO₃ + CaCl₂', fontsize=7.2,
        color=INK, ha='center')
ax.set_position([0,0,1,1])
ax.set_xlim(-1.70, 10.10); ax.set_ylim(-1.55, 4.55); ax.axis('off')
```

| Solvay process at a glance | |
|---|---|
| Raw materials | brine (NaCl), limestone (CaCO₃), coke; ammonia is recycled, not consumed |
| Conditions | carbonating tower 40 °C falling to 20 °C; calciner 150–200 °C; lime kiln ~1000 °C |
| Catalyst | none |
| Key reactions | NaCl + NH₃ + CO₂ + H₂O → NaHCO₃↓ + NH₄Cl; 2NaHCO₃ → Na₂CO₃ + H₂O + CO₂ |
| By-products | calcium chloride solution (the only large waste — de-icing salt, dust suppressant, but mostly discharged) |
| Uses | glass manufacture, soaps and detergents, paper, water softening, sodium salts, textile processing |

::: example Yield of soda ash
**Problem.** A Solvay plant processes 1170 kg of sodium chloride. If the overall
yield of sodium carbonate is 90%, what mass of Na₂CO₃ is obtained?
(Na = 23, Cl = 35.5, C = 12, O = 16)

**Solution.**
Molar mass of NaCl = 58.5 g mol⁻¹; n(NaCl) = 1170 ÷ 58.5 = 20 kmol.

From the overall equation 2NaCl + CaCO₃ → Na₂CO₃ + CaCl₂, two moles of NaCl
give one mole of Na₂CO₃, so theoretical n(Na₂CO₃) = 10 kmol.

Molar mass of Na₂CO₃ = 2(23) + 12 + 3(16) = 106 g mol⁻¹.
Theoretical mass = 10 × 106 = 1060 kg.
Actual mass = 0.90 × 1060 = **954 kg**.
:::

## 17.6 Fertilizers: chemical fertilizers, types, production of urea

::: definition Fertilizer
A **fertilizer** is a substance, natural or manufactured, added to soil to
supply one or more of the elements that plants need for growth in a form the
roots can absorb.
:::

Plants need sixteen elements. Carbon, hydrogen and oxygen come free from air and
water. Of the rest, three are needed in bulk and are almost always the limiting
ones, so they are called the **primary nutrients**:

| Nutrient | Symbol | What it does | Deficiency sign |
|---|---|---|---|
| Nitrogen | N | proteins, chlorophyll, vegetative growth | older leaves yellow (chlorosis), stunting |
| Phosphorus | P | ATP, nucleic acids, root and seed development | dark green to purple leaves, poor rooting |
| Potassium | K | enzyme activation, stomatal control, disease resistance | scorched leaf margins, weak stems, lodging |

Secondary nutrients are Ca, Mg and S; micronutrients (Fe, Mn, Zn, Cu, B, Mo, Cl)
are needed in traces.

### Types of chemical fertilizer

| Type | Examples | N–P₂O₅–K₂O grade | Notes |
|---|---|---|---|
| Nitrogenous | urea NH₂CONH₂ | 46–0–0 | highest N content of any solid fertilizer; hygroscopic |
| | ammonium sulphate (NH₄)₂SO₄ | 21–0–0 | also supplies S; acidifies the soil |
| | ammonium nitrate NH₄NO₃ | 35–0–0 | quick-acting; an explosive hazard in bulk |
| | calcium ammonium nitrate | 26–0–0 | safer, non-acidifying version of the above |
| Phosphatic | single superphosphate | 0–16–0 | Ca(H₂PO₄)₂ + CaSO₄, made with H₂SO₄ |
| | triple superphosphate | 0–46–0 | made with H₃PO₄, no gypsum diluent |
| Potassic | muriate of potash, KCl | 0–0–60 | cheapest K source; avoid on chloride-sensitive crops |
| | sulphate of potash, K₂SO₄ | 0–0–50 | for tobacco, potato, fruit |
| Mixed / complex | DAP (NH₄)₂HPO₄ | 18–46–0 | one compound supplying two nutrients |
| | NPK blends | e.g. 20–20–0 | physically blended or chemically granulated |

The three numbers printed on every bag — the **grade** — are the percentages by
mass of N, of P as P₂O₅, and of K as K₂O. They are a trade convention, not a
statement that the bag contains P₂O₅ molecules.

**Straight** fertilizers supply one primary nutrient; **complex** (or mixed)
fertilizers supply two or three. Fertilizers are also classed as *quick-acting*
(nitrate salts, which are freely soluble and leach fast) or *slow-acting*
(urea, which must first be hydrolysed by soil urease to ammonium carbonate).

::: caution Excess fertilizer is not harmless
Nitrate is very soluble, so whatever the crop does not take up is washed into
streams, where it feeds algae. The algae die, bacteria decompose them and use up
the dissolved oxygen, and fish suffocate — **eutrophication**. Ammonium
fertilizers also acidify soil over years, and nitrogenous fertilizer beds emit
N₂O, a greenhouse gas about 270 times more potent than CO₂ per molecule. The
correct exam answer to "why is fertilizer a problem?" is always eutrophication
plus soil acidification, never "it is a chemical".
:::

```figure caption="Left: the printed N–P₂O₅–K₂O grade of common fertilizers — urea leads on nitrogen, DAP and TSP on phosphate, MOP on potash. Right: Nepal manufactures no chemical fertilizer, so the gap between estimated demand and what is actually landed and sold is met by the grey market."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.9),
                               gridspec_kw={'width_ratios':[1.55,1.0]})

names = ['Urea', '(NH₄)₂SO₄', 'CAN', 'DAP', 'TSP', 'MOP']
N   = [46, 21, 26, 18,  0,  0]
P   = [ 0,  0,  0, 46, 46,  0]
K   = [ 0,  0,  0,  0,  0, 60]
x = np.arange(len(names)); w = 0.27
ax1.bar(x-w, N, w, color=SERIES[0], label='N')
ax1.bar(x,   P, w, color=SERIES[2], label='P₂O₅')
ax1.bar(x+w, K, w, color=SERIES[3], label='K₂O')
for xi, v in zip(x-w, N):
    if v: ax1.text(xi, v+1.2, str(v), fontsize=5.6, color=SERIES[0], ha='center')
for xi, v in zip(x, P):
    if v: ax1.text(xi, v+1.2, str(v), fontsize=5.6, color=SERIES[2], ha='center')
for xi, v in zip(x+w, K):
    if v: ax1.text(xi, v+1.2, str(v), fontsize=5.6, color=SERIES[3], ha='center')
ax1.set_xticks(x); ax1.set_xticklabels(names, fontsize=6.0)
ax1.set_ylabel('per cent by mass', fontsize=7.0)
ax1.set_ylim(0, 72); ax1.tick_params(labelsize=6.4)
ax1.legend(fontsize=6.0, frameon=False, ncol=3, loc='upper left',
           handlelength=1.0, columnspacing=0.9)
ax1.set_title('Grade of common fertilizers', fontsize=7.2, color=INK)
ax1.grid(axis='y', color=GRID, lw=0.7); ax1.set_axisbelow(True)
ax1.spines[['top','right']].set_visible(False)

lab = ['estimated\ndemand', 'imported\n2022/23', 'sold by\nstate firms']
val = [700, 426, 342]
col = [MUTED, SERIES[0], SERIES[1]]
ax2.bar(np.arange(3), val, 0.55, color=col)
for i, v in enumerate(val):
    ax2.text(i, v+14, str(v), fontsize=6.4, color=col[i], ha='center')
ax2.set_xticks(np.arange(3)); ax2.set_xticklabels(lab, fontsize=5.9, linespacing=1.3)
ax2.set_ylabel('thousand tonnes', fontsize=7.0)
ax2.set_ylim(0, 830); ax2.tick_params(labelsize=6.4)
ax2.set_title('Nepal: no home production', fontsize=7.2, color=INK)
ax2.grid(axis='y', color=GRID, lw=0.7); ax2.set_axisbelow(True)
ax2.spines[['top','right']].set_visible(False)
fig.tight_layout()
```

### Fertilizer in Nepal

Nepal has no chemical fertilizer factory. Every kilogram is imported, mostly
from India and the Gulf, by two state undertakings — Agriculture Inputs Company
Limited and Salt Trading Corporation — and sold at a subsidised price. In the
fiscal year 2022/23 Nepal imported **426,007 tonnes** of chemical fertilizer
worth about **Rs 40.65 billion**, against a government estimate of annual demand
of roughly **700,000 tonnes**; the two state firms sold 342,462 tonnes of it.
The shortfall is the reason for the queues outside depots before the paddy
planting season. This is the applied-chemistry argument for building an urea
plant at home, and the reason this section matters more in Nepal than the
syllabus line suggests.

### Production of urea

Urea, NH₂CONH₂, is made by the **Bosch–Meiser process** directly from the two
products of an ammonia plant — ammonia itself, and the carbon dioxide stripped
out of the reformer gas. That is why urea plants are always built beside
ammonia plants.

**Step 1 (fast, exothermic).** Liquid ammonia and carbon dioxide are compressed
to 150–200 atm and fed to an **autoclave** at 180–190 °C, where they combine to
ammonium carbamate:

2NH₃ + CO₂ → NH₂COONH₄,  ΔH = −117 kJ mol⁻¹

**Step 2 (slow, endothermic, reversible).** The carbamate loses water:

NH₂COONH₄ ⇌ NH₂CONH₂ + H₂O,  ΔH = +15.5 kJ mol⁻¹

The high pressure is needed to keep the carbamate in the liquid phase; the high
temperature drives the second, endothermic step. Conversion per pass is about
50–70%.

**Step 3.** The melt leaving the autoclave is let down to about 2 atm in a
**decomposer (stripper)**, where the unconverted carbamate splits back into NH₃
and CO₂. These gases are compressed and recycled to the autoclave, so the
overall conversion is nearly complete.

**Step 4.** The urea solution is concentrated in a vacuum **evaporator** at
about 135 °C to a melt containing 99.7% urea.

**Step 5.** The melt is sprayed from the top of a **prilling tower** through a
rotating perforated bucket. The droplets solidify as they fall against an
up-draught of cold air, forming the near-spherical **prills** sold in bags.
Modern plants granulate instead, giving harder, larger particles.

Combining steps 1 and 2:

2NH₃ + CO₂ → NH₂CONH₂ + H₂O

```figure caption="Flow sheet for urea manufacture. The carbamate that fails to dehydrate is decomposed at low pressure and returned to the autoclave, so the only losses are in the prilling tower."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.6))

def box(x, y, w, h, title, sub=''):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc='#eef3f9', ec=ACCENT, lw=1.25))
    ax.text(x+w/2, y+h*0.74, title, fontsize=7.0, color=INK, ha='center', va='center')
    ax.text(x+w/2, y+h*0.30, sub, fontsize=5.9, color=MUTED, ha='center',
            va='center', linespacing=1.3)

def arr(p, q, c=INK, lw=1.4, ls='-'):
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, linestyle=ls,
                                mutation_scale=11))

def path(pts, c=MUTED, lw=1.1, ls=(0,(4,2))):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color=c, lw=lw, ls=ls, solid_capstyle='butt')
    arr(pts[-2], pts[-1], c=c, lw=lw, ls=ls)

W, H = 2.35, 1.05
yA, yB = 2.50, 0.45
x1, x2, x3 = 0.10, 2.85, 5.60

box(x1, yA, W, H, 'Compressors',  'NH₃ and CO₂ raised\nto 150–200 atm')
box(x2, yA, W, H, 'Autoclave',    '180–190 °C, 200 atm\n2NH₃ + CO₂ → NH₂COONH₄')
box(x3, yA, W, H, 'Decomposer',   '2 atm, 150 °C\ncarbamate split off')
box(x3, yB, W, H, 'Evaporator',   'vacuum, 135 °C\nurea melt 99.7%')
box(x2, yB, W, H, 'Prilling tower', 'melt sprayed down\nagainst cold air')

# feeds
arr((-1.15, yA+H*0.66), (x1-0.03, yA+H*0.66), '#2e8b57')
arr((-1.15, yA+H*0.30), (x1-0.03, yA+H*0.30), '#2e8b57')
ax.text(-1.22, yA+H*0.66, 'NH₃', fontsize=7.0, color='#2e8b57', ha='right', va='center')
ax.text(-1.22, yA+H*0.30, 'CO₂', fontsize=7.0, color='#2e8b57', ha='right', va='center')
ax.text(-1.25, yA+H+0.52, 'both feeds come from the\nadjacent ammonia plant',
        fontsize=6.2, color=MUTED, ha='left', va='center', linespacing=1.3)

arr((x1+W, yA+H/2), (x2-0.03, yA+H/2))
arr((x2+W, yA+H/2), (x3-0.03, yA+H/2))
ax.text(x2+W+0.20, yA+H+0.12, 'melt:  urea + H₂O + carbamate', fontsize=5.9,
        color=MUTED, ha='center', va='bottom')

# reactor effluent down to evaporator
arr((x3+W-0.45, yA-0.03), (x3+W-0.45, yB+H+0.04))
ax.text(x3+W-0.35, (yA+yB+H)/2, 'urea\nsolution', fontsize=6.1, color=INK,
        ha='left', va='center', linespacing=1.3)
# carbamate gases recycled to the autoclave
path([(x3+0.45, yA-0.03), (x3+0.45, 1.95), (x2+W*0.55, 1.95),
      (x2+W*0.55, yA-0.03)], c='#d9534f')
ax.text((x2+W*0.55+x3+0.45)/2, 1.86, 'NH₃ + CO₂ recycled', fontsize=6.2,
        color='#d9534f', ha='center', va='top')

arr((x3-0.03, yB+H/2), (x2+W+0.03, yB+H/2))
arr((x3+W+0.04, yB+H*0.72), (x3+W+1.05, yB+H*0.72), MUTED, lw=1.1)
ax.text(x3+W+1.12, yB+H*0.72, 'water\nvapour', fontsize=6.1, color=MUTED,
        ha='left', va='center', linespacing=1.3)

arr((x2+0.55, yB-0.03), (x2+0.55, -0.52), '#8a6d1f')
ax.text(x2+0.70, -0.46, 'urea prills,  46% N', fontsize=7.0, color='#8a6d1f',
        ha='left', va='center')

ax.text(-1.25, -0.46, 'NH₂COONH₄  ⇌  NH₂CONH₂ + H₂O', fontsize=6.8,
        color=INK, ha='left', va='center')
ax.set_position([0,0,1,1])
ax.set_xlim(-2.35, 9.85); ax.set_ylim(-0.95, 4.40); ax.axis('off')
```

| Urea manufacture at a glance | |
|---|---|
| Raw materials | ammonia and carbon dioxide (both from the ammonia plant) |
| Conditions | autoclave 180–190 °C and 150–200 atm; decomposer 2 atm; evaporator 135 °C under vacuum |
| Catalyst | none — high pressure and temperature only |
| Key reactions | 2NH₃ + CO₂ → NH₂COONH₄; NH₂COONH₄ ⇌ NH₂CONH₂ + H₂O |
| By-products | water; biuret (NH₂CONHCONH₂), an impurity that must be kept below ~1% because it damages leaves |
| Uses | fertilizer (about 90% of output), cattle feed supplement, urea–formaldehyde resins, melamine, medical creams, NOₓ abatement in diesel exhaust |

::: example Sizing a urea plant
**Problem.** A urea unit receives 1.00 tonne of ammonia per hour, all of which
reacts. Calculate (a) the mass of CO₂ required per hour, (b) the maximum mass of
urea produced per hour, and (c) the mass of nitrogen delivered to the field in
that urea. (H = 1, C = 12, N = 14, O = 16)

**Solution.**
The overall equation is 2NH₃ + CO₂ → NH₂CONH₂ + H₂O.

n(NH₃) = 1000 kg ÷ 17 kg kmol⁻¹ = 58.82 kmol.

(a) n(CO₂) = ½ × 58.82 = 29.41 kmol; mass = 29.41 × 44 = **1294 kg**.

(b) n(urea) = ½ × 58.82 = 29.41 kmol; molar mass of NH₂CONH₂ = 60 g mol⁻¹, so
mass = 29.41 × 60 = **1765 kg**.

(c) Each mole of urea carries 2 mol of N (28 g):

$$ \%\,\mathrm{N} = \frac{28}{60}\times 100 = 46.7\% $$

mass of N = 0.467 × 1765 = **824 kg per hour**.
:::

## Chapter summary

- **Haber:** N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92.4 kJ mol⁻¹; Fe + Mo promoter, 450–500 °C,
  200 atm, 1 : 3 feed; ammonia condensed out at −30 °C and unreacted gas
  recycled. Temperature is a *compromise* between yield and rate.
- **Ostwald:** 4NH₃ + 5O₂ → 4NO + 6H₂O over Pt–Rh gauze at 800 °C in ~10⁻³ s;
  2NO + O₂ ⇌ 2NO₂ on cooling; 3NO₂ + H₂O → 2HNO₃ + NO in the absorber.
  Overall NH₃ + 2O₂ → HNO₃ + H₂O, giving 68% acid, concentrated with conc. H₂SO₄.
- **Contact:** S + O₂ → SO₂ (or 4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂); purify and dry;
  2SO₂ + O₂ ⇌ 2SO₃ over V₂O₅ at 450 °C and 2 atm, ΔH = −196 kJ mol⁻¹; absorb in
  98% H₂SO₄ to oleum (SO₃ + H₂SO₄ → H₂S₂O₇) and dilute. Low pressure suffices
  because conversion is already ~97%.
- **Diaphragm cell:** anode 2Cl⁻ → Cl₂ + 2e⁻, cathode 2H₂O + 2e⁻ → H₂ + 2OH⁻,
  overall 2NaCl + 2H₂O → 2NaOH + H₂ + Cl₂. The asbestos diaphragm plus a higher
  anolyte level keeps OH⁻ away from Cl₂. Cell liquor is 11% NaOH + 16% NaCl.
- **Solvay:** NaCl + NH₃ + CO₂ + H₂O → NaHCO₃↓ + NH₄Cl, then
  2NaHCO₃ → Na₂CO₃ + H₂O + CO₂, with 2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2NH₃ + 2H₂O
  recovering the ammonia. Overall 2NaCl + CaCO₃ → Na₂CO₃ + CaCl₂; CaCl₂ is the
  only waste.
- **Fertilizers:** graded N–P₂O₅–K₂O. Urea 46–0–0, (NH₄)₂SO₄ 21–0–0, DAP 18–46–0,
  TSP 0–46–0, MOP 0–0–60. Excess causes eutrophication and soil acidification.
- **Urea:** 2NH₃ + CO₂ → NH₂COONH₄ ⇌ NH₂CONH₂ + H₂O at 180–190 °C and 200 atm;
  carbamate recycled from the decomposer; melt prilled. Nitrogen content
  28/60 = 46.7%.
- A catalyst never changes $K_p$; it changes the time taken to reach
  equilibrium, which is what lets a plant use a lower, yield-friendly
  temperature.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The catalyst used in the contact process is <span class="marks">[1]</span>
   (a) finely divided iron (b) platinum–rhodium gauze (c) vanadium(V) oxide (d) nickel
2. In the Haber process, increasing the pressure increases the yield of ammonia because <span class="marks">[1]</span>
   (a) the reaction is exothermic (b) the number of gas molecules decreases (c) the catalyst works better (d) ammonia is a liquid
3. Sulphur trioxide is absorbed in concentrated sulphuric acid rather than water because <span class="marks">[1]</span>
   (a) water does not react with SO₃ (b) the reaction with water is endothermic (c) a persistent acid mist is formed with water (d) SO₃ is insoluble in water
4. In the diaphragm cell the product formed at the cathode is <span class="marks">[1]</span>
   (a) sodium metal (b) chlorine (c) hydrogen (d) oxygen
5. The least soluble substance formed in the carbonating tower of the Solvay process is <span class="marks">[1]</span>
   (a) NaHCO₃ (b) NH₄Cl (c) Na₂CO₃ (d) NH₄HCO₃
6. The percentage of nitrogen in urea is closest to <span class="marks">[1]</span>
   (a) 21% (b) 35% (c) 46% (d) 60%

::: note Answers to Group A
**1.** (c) — V₂O₅ is cheap and, unlike platinum, is not poisoned by traces of arsenic.
**2.** (b) — 4 mol of gas become 2, so by Le Chatelier's principle higher pressure shifts the equilibrium right.
**3.** (c) — direct absorption in water gives a fine mist of H₂SO₄ that will not condense and escapes up the stack.
**4.** (c) — water is reduced in preference to Na⁺, so hydrogen is evolved; sodium metal needs molten NaCl.
**5.** (a) — sodium hydrogencarbonate crystallises out, which is what drives the whole process.
**6.** (c) — 28/60 × 100 = 46.7%.
:::

**Group B — Short answer (5 marks each)**

1. State Le Chatelier's principle and use it to explain the choice of temperature and pressure in the Haber process. Why is a catalyst used even though it cannot change the yield? <span class="marks">[5]</span>
2. Describe, with equations, the purification of the gas in the contact process, and state why each impurity must be removed. <span class="marks">[5]</span>
3. Explain the function of the diaphragm and of the difference in brine level in a diaphragm cell. Write the electrode reactions and name the by-products. <span class="marks">[5]</span>
4. 2.8 tonnes of nitrogen is passed through a Haber converter with excess hydrogen. If the percentage yield is 85%, calculate the mass of ammonia produced. <span class="marks">[5]</span>
5. A farmer needs to apply 140 kg of nitrogen to one hectare. Calculate the mass of urea required, and state two reasons why applying twice this amount would be harmful. <span class="marks">[5]</span>
6. Why is ammonia not consumed in the Solvay process? Write the equations for the two steps in which it is used and recovered, and name the only large waste product. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Le Chatelier: *if a system at equilibrium is disturbed, the equilibrium shifts in the direction that opposes the disturbance.* The forward reaction N₂ + 3H₂ ⇌ 2NH₃ is exothermic, so a low temperature would give the highest equilibrium yield; but at low temperature the rate is uneconomically slow, so 450–500 °C is chosen as a compromise. Four moles of gas become two, so a high pressure shifts the equilibrium right *and* speeds the reaction — 200 atm is used, limited only by the cost and safety of the vessels. The iron catalyst lowers the activation energy of forward and reverse reactions equally, so $K_p$ is unchanged; its value is that equilibrium is reached quickly at a temperature low enough to give a useful yield.

**2.** Burner gas is passed through: a **dust chamber** (steam and electrostatic precipitation) to settle dust, which would coat and deactivate the catalyst; **cooling pipes**, to drop the temperature to about 100 °C and recover heat; a **washing tower** (water spray) to dissolve out soluble impurities; an **arsenic purifier** where Fe(OH)₃ adsorbs As₂O₃, because arsenic is a permanent catalyst **poison**; a **testing box** to confirm purity; and a **drying tower** where concentrated H₂SO₄ removes water vapour, which would otherwise form acid mist and dilute the product. The reaction to be protected is 2SO₂ + O₂ ⇌ 2SO₃ over V₂O₅.

**3.** The diaphragm is a porous asbestos layer on the perforated steel cathode. It lets ions and liquid through but prevents bulk mixing of the anolyte and catholyte, which is essential because Cl₂ + 2NaOH → NaCl + NaOCl + H₂O would destroy both products. The anode compartment is kept at a *higher liquid level*, so brine percolates continuously from anode side to cathode side; this bulk flow opposes the electrical migration of OH⁻ towards the anode and sweeps hydroxide away from the chlorine. Electrode reactions: anode 2Cl⁻ → Cl₂ + 2e⁻; cathode 2H₂O + 2e⁻ → H₂ + 2OH⁻. By-products: chlorine and hydrogen.

**4.** n(N₂) = 2800 kg ÷ 28 kg kmol⁻¹ = 100 kmol. From N₂ + 3H₂ → 2NH₃ (hydrogen in excess, so N₂ is limiting), theoretical n(NH₃) = 200 kmol. Theoretical mass = 200 × 17 = 3400 kg. Actual mass = 0.85 × 3400 = **2890 kg = 2.89 tonnes**.

**5.** Urea is NH₂CONH₂, molar mass 60 g mol⁻¹, containing 2 N (28 g) per mole.
mass of urea = 140 × 60/28 = **300 kg**.
Harm from over-application: (i) the excess nitrate is leached into streams and causes **eutrophication** — algal bloom, oxygen depletion, fish kill; (ii) repeated ammonium application **acidifies the soil**, and high salt concentration can scorch roots ("fertilizer burn"); emission of N₂O, a potent greenhouse gas, is also increased.

**6.** Ammonia is used in the ammoniation/carbonation step,
NaCl + NH₃ + CO₂ + H₂O → NaHCO₃↓ + NH₄Cl,
and is recovered from the filtrate by warming with milk of lime,
2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2NH₃↑ + 2H₂O.
The recovered ammonia is returned to the ammoniation tower, so only make-up ammonia for mechanical losses is bought. The only large waste is **calcium chloride solution**.
:::

**Group C — Long answer (8 marks each)**

1. Describe the manufacture of sulphuric acid by the contact process. Include a labelled flow sheet, all balanced equations, the conditions with reasons, and explain why a much lower pressure is used than in the Haber process. <span class="marks">[8]</span>
2. (a) With a labelled diagram, describe the manufacture of sodium hydroxide by the diaphragm cell, giving the electrode reactions and the composition of the cell liquor. (b) A cell carries 50 kA for 10 hours at 95% current efficiency. Calculate the mass of NaOH produced and the volume of chlorine at STP. <span class="marks">[8]</span>
3. (a) What is a chemical fertilizer? Classify chemical fertilizers with one example and the N–P₂O₅–K₂O grade of each class. (b) Describe the manufacture of urea from ammonia and carbon dioxide with a flow-sheet diagram and balanced equations. (c) Calculate the mass of urea that can be made from 340 kg of ammonia if the conversion is 75%. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Outline.* **Stage 1:** S + O₂ → SO₂ (or 4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂) in the burner. **Stage 2 — purification:** dust chamber → cooling pipes → washing tower → arsenic purifier (Fe(OH)₃ removes As₂O₃, a catalyst poison) → testing box → drying tower (conc. H₂SO₄). **Stage 3:** 2SO₂ + O₂ ⇌ 2SO₃, ΔH = −196 kJ mol⁻¹, over V₂O₅ at 450 °C and 2 atm. Temperature is a compromise: the reaction is exothermic so a low temperature favours SO₃, but below ~400 °C the catalyst is too slow. **Stage 4:** SO₃ + H₂SO₄ → H₂S₂O₇ (oleum), then H₂S₂O₇ + H₂O → 2H₂SO₄; direct absorption in water is avoided because it forms an uncondensable acid mist. *Pressure:* both reactions reduce the number of gas moles, so both are helped by pressure — but at 450 °C and only 2 atm the SO₂ conversion is already about 97%, so higher pressure would buy at most 2–3% more product and could not pay for compressors and pressure vessels. In the Haber process the equilibrium at the operating temperature is so unfavourable that 200 atm is worth paying for. Credit a flow sheet matching the figure in the text.

**2.** (a) Steel tank; titanium (RuO₂-coated) anode; perforated steel cathode carrying an asbestos diaphragm; saturated 25% brine fed to the anode compartment and held at a higher level. Anode: 2Cl⁻ → Cl₂ + 2e⁻. Cathode: 2H₂O + 2e⁻ → H₂ + 2OH⁻. Overall: 2NaCl + 2H₂O → 2NaOH + H₂ + Cl₂. The diaphragm and the level difference keep OH⁻ away from Cl₂. Cell liquor drawn off contains about **11% NaOH and 16% NaCl**; it is evaporated, the less soluble NaCl crystallises and is recycled, and 50% caustic liquor is obtained.
(b) Q = 50 000 A × 36 000 s = 1.8 × 10⁹ C.
n(e⁻) = 1.8 × 10⁹ ÷ 96 500 = 1.865 × 10⁴ mol; useful = 0.95 × 1.865 × 10⁴ = 1.772 × 10⁴ mol.
NaOH: 1 mol per electron → 1.772 × 10⁴ × 40 = 7.088 × 10⁵ g = **708.8 kg**.
Cl₂: 1 mol per 2 electrons → 8.860 × 10³ mol; V = 8.860 × 10³ × 22.4 = 1.985 × 10⁵ L = **198.5 m³**.

**3.** (a) A fertilizer is a substance added to soil to supply one or more elements needed for plant growth in an absorbable form. Classes: **nitrogenous** — urea, 46–0–0; **phosphatic** — triple superphosphate, 0–46–0; **potassic** — muriate of potash (KCl), 0–0–60; **mixed/complex** — DAP, 18–46–0. (Straight versus complex, and quick- versus slow-acting, are acceptable alternative classifications.)
(b) NH₃ and CO₂ from the adjacent ammonia plant are compressed to 150–200 atm and fed to an autoclave at 180–190 °C: 2NH₃ + CO₂ → NH₂COONH₄ (fast, exothermic), then NH₂COONH₄ ⇌ NH₂CONH₂ + H₂O (slow, endothermic). The melt is let down to 2 atm in a decomposer where unconverted carbamate splits back to NH₃ + CO₂, which are recycled; the urea solution is concentrated to a 99.7% melt in a vacuum evaporator at 135 °C and sprayed down a prilling tower against cold air to give prills. Credit a flow sheet matching the figure in the text.
(c) n(NH₃) = 340 ÷ 17 = 20 kmol. From 2NH₃ + CO₂ → NH₂CONH₂ + H₂O, theoretical n(urea) = 10 kmol = 10 × 60 = 600 kg. At 75%: mass = **450 kg**.
:::
