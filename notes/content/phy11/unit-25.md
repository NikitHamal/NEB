---
subject: Physics
grade: 11
unit: 25
title: Solids
hours: 3
area: Modern Physics
---

In a single isolated atom an electron may occupy only certain sharp energy
levels. Push $10^{29}$ atoms together into a crystal and those sharp levels
smear out into continuous **bands** of allowed energy separated by **forbidden
gaps**. One number — the width of the gap above the highest filled band —
decides whether the solid is a copper wire, a slab of mica, or the silicon chip
inside a mobile phone. This short unit builds that picture and uses it to
explain doping.

::: key What the examiner wants
Four things, almost every year: a labelled band diagram distinguishing
conductor, semiconductor and insulator; the reason a semiconductor's resistance
*falls* as it is heated; the covalent-bond (lattice) diagrams of n-type and
p-type silicon; and a clear comparison of the two. Learn the diagrams as
diagrams — they are worth full marks on their own.
:::

## 25.1 Energy bands in solids (qualitative ideas)

An electron in an isolated atom has discrete energies $E_1, E_2, E_3, \dots$
given by quantum theory. The **Pauli exclusion principle** allows at most two
electrons (opposite spin) in any one state.

Now bring $N$ identical atoms close together to build a crystal. When the atoms
are far apart, each of the $N$ atoms has its own identical $3s$ level, so that
energy is $N$-fold repeated. As the separation shrinks, the outer electron
clouds overlap; the electron of one atom now feels the nuclei of its neighbours.
Pauli's principle forbids $N$ electrons from sharing one identical state, so the
single level **splits into $N$ very closely spaced levels**.

How closely spaced? Take one cubic metre of solid, so $N \approx 10^{29}$, and
let the whole set of split levels spread over about $1\ \text{eV}$. The average
step from one level to the next is then

$$ \Delta E \approx \frac{1\ \text{eV}}{10^{29}} = 10^{-29}\ \text{eV} $$

No instrument can resolve a step that small, and no experiment can tell it apart
from zero. The set of levels therefore behaves as one continuous **energy
band**. Inner-shell electrons are buried deep inside the atom, their orbitals
barely overlap, and their levels hardly split at all — only the outermost
(valence) levels broaden into wide bands.

```figure caption="A single sharp atomic level splits into a band of $N$ closely packed levels as the atoms are brought together. At the real lattice spacing $r_0$ the two bands are separated by the forbidden gap $E_g$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
x = np.linspace(0, 1, 300)
for E0, w, c in [(1.0, 0.62, ACCENT), (2.9, 0.95, SERIES[1])]:
    ax.fill_between(x, E0 - w*x**3, E0 + w*x**3, color=c, alpha=0.13)
    for f in np.linspace(-1, 1, 9):
        ax.plot(x, E0 + f*w*x**3, color=c, lw=0.7, alpha=0.8)
r0 = 0.82
ax.plot([r0, r0], [0.06, 4.05], color=INK, lw=0.9, ls=(0,(4,3)))
lo = 1.0 + 0.62*r0**3; hi = 2.9 - 0.95*r0**3
ax.annotate('', xy=(r0+0.07, hi), xytext=(r0+0.07, lo),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.2, mutation_scale=9))
ax.text(r0+0.115, (lo+hi)/2, '$E_g$', color=INK, fontsize=10, va='center')
ax.text(r0, -0.10, '$r_0$', color=INK, fontsize=9.5, ha='center', va='top')
ax.text(0.03, 3.08, 'conduction band', color=SERIES[1], fontsize=9, va='bottom')
ax.text(0.03, 0.72, 'valence band', color=ACCENT, fontsize=9, va='top')
ax.text(0.03, 1.72, 'isolated atoms:\nsharp levels', color=MUTED, fontsize=8.6,
        va='center')
ax.set_xlabel('interatomic separation decreasing  $\\longrightarrow$')
ax.set_ylabel('electron energy  $E$')
ax.set_xlim(0, 1.05); ax.set_ylim(-0.45, 4.2)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

Two bands matter:

::: definition Valence band and conduction band
The **valence band** is the highest energy band that is completely or partly
filled by the valence electrons of the atoms at $0\ \text{K}$. The
**conduction band** is the next allowed band above it; an electron in the
conduction band is no longer tied to one atom and can drift through the whole
crystal when a field is applied.

The energy range between the top of the valence band and the bottom of the
conduction band contains no allowed states. It is the **forbidden energy gap**
$E_g$.
:::

A current flows only if electrons can gain small amounts of energy from the
applied field, i.e. only if there are **empty states immediately above occupied
states**. A completely full band carries no net current however strong the
field, because every electron that moves one way is matched by one moving the
other. This single sentence explains the whole of the next section.

## 25.2 Difference between metals, insulators and semi-conductors using band theory

```figure caption="Band structure at room temperature, all three drawn to the same energy scale. Shading shows how full a band is; filled dots are electrons and open circles are holes. Every solid has both bands — only the gap between them changes."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgba
fig, axs = plt.subplots(1, 3, figsize=(5.1,3.0))
X0, W = 0.10, 0.80
def rect(ax, y0, a):
    ax.add_patch(Rectangle((X0, y0), W, 1.0, facecolor=to_rgba(ACCENT, a),
                           edgecolor=INK, lw=1.0, zorder=2))
def panel(ax, cb_bot, title, foot, overlap=False, carriers=False):
    rect(ax, 0.0, 0.40)                                   # valence band
    rect(ax, cb_bot, 0.40 if overlap else (0.12 if carriers else 0.0))
    ax.text(0.5, 0.30, 'VB', ha='center', va='center', fontsize=8.6, color=INK,
            zorder=5)
    ax.text(0.5, cb_bot + (0.74 if carriers else 0.50), 'CB', ha='center',
            va='center', fontsize=8.6, color=INK, zorder=5)
    if not overlap:
        ax.annotate('', xy=(0.97, cb_bot), xytext=(0.97, 1.0),
                    arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1,
                                    mutation_scale=8))
        ax.text(1.03, (cb_bot+1.0)/2, '$E_g$', color=SERIES[1], fontsize=8.6,
                va='center', ha='left')
    if carriers:
        ex = [0.22, 0.38, 0.54, 0.70, 0.84]
        ey = [0.30, 0.17, 0.33, 0.21, 0.28]
        ax.plot(ex, [cb_bot+d for d in ey], 'o', color=INK, ms=3.6, mec='none',
                zorder=5, ls='none')
        ax.plot([0.25, 0.42, 0.58, 0.75], [0.71, 0.82, 0.71, 0.81], 'o',
                mfc='none', mec=INK, ms=3.8, mew=0.9, zorder=5, ls='none')
    ax.text(0.5, -0.52, foot, ha='center', va='top', fontsize=8.0, color=MUTED)
    ax.set_xlim(-0.25, 1.25); ax.set_ylim(-1.55, 4.75); ax.axis('off')
    ax.set_title(title, fontsize=9.2)
panel(axs[0], 0.72, 'Conductor', 'bands overlap\n$E_g = 0$', overlap=True)
panel(axs[1], 1.85, 'Semiconductor', '$E_g \\approx 1$ eV\n(Si 1.1, Ge 0.7)',
      carriers=True)
panel(axs[2], 3.40, 'Insulator', '$E_g > 3$ eV\n(diamond 5.5)')
```

**Conductors (metals).** The valence band is only partly filled (sodium), or a
filled valence band **overlaps** the empty conduction band (magnesium, zinc).
Either way there is no gap: empty states sit immediately above occupied ones, a
huge number of free electrons ($\sim 10^{28}\ \text{m}^{-3}$) is available, and
the resistivity is tiny.

**Insulators.** The valence band is completely full, the conduction band
completely empty, and $E_g$ is large — $5.47\ \text{eV}$ for diamond. At
$300\ \text{K}$ the average thermal energy of a particle is only about
$kT \approx 0.026\ \text{eV}$, so practically no electron can be lifted across.

**Semiconductors.** The band picture is the same as an insulator's, but $E_g$ is
small: $1.1\ \text{eV}$ for silicon, $0.7\ \text{eV}$ for germanium. At
$0\ \text{K}$ a semiconductor is a perfect insulator. At room temperature a
small fraction of the bonds break, electrons jump the gap into the conduction
band and leave holes behind in the valence band, and conduction begins.

| Property | Conductor | Semiconductor | Insulator |
|---|---|---|---|
| Forbidden gap $E_g$ | zero (bands overlap) | $\leq 3\ \text{eV}$ (Ge 0.7, Si 1.1) | $> 3\ \text{eV}$ (diamond 5.47) |
| Resistivity at 300 K | $10^{-8}$–$10^{-6}\ \Omega\,\text{m}$ | $10^{-5}$–$10^{6}\ \Omega\,\text{m}$ | $10^{8}$–$10^{16}\ \Omega\,\text{m}$ |
| Carrier density | $\sim 10^{28}\ \text{m}^{-3}$ | $10^{16}$–$10^{19}\ \text{m}^{-3}$ | negligible |
| Temperature coefficient of resistance | positive | negative | negative |
| Behaviour at $0\ \text{K}$ | still conducts | perfect insulator | perfect insulator |
| Examples | Cu, Ag, Al | Si, Ge, GaAs | diamond, mica, glass |

The **negative temperature coefficient** is the giveaway property of a
semiconductor. Heating a metal makes the lattice ions vibrate more, electrons
are scattered more often, and resistance rises. Heating a semiconductor does
that too, but it also breaks far more bonds. In a pure semiconductor the Fermi
level (the energy at which a state is half likely to be occupied) sits in the
middle of the gap, so on the Boltzmann scale an electron only has to climb
$E_g/2$ to reach the conduction band. The number of carriers therefore grows
like $e^{-E_g/2kT}$, and this exponential growth easily overwhelms the extra
scattering, so the resistivity falls.

```figure caption="Resistivity against temperature, plotted relative to its value at 300 K. The metal rises gently and linearly; the semiconductor ($E_g = 1.1$ eV) falls by orders of magnitude."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
T = np.linspace(250, 500, 300); k = 8.617e-5; Eg = 1.1
ax.semilogy(T, 1 + 0.0043*(T-300), color=ACCENT, lw=1.9, label='metal (Cu)')
ax.semilogy(T, np.exp(Eg/(2*k*T) - Eg/(2*k*300)), color=SERIES[1], lw=1.9,
            label='semiconductor (Si)')
ax.axhline(1, color=MUTED, lw=0.8, ls=':')
ax.set_xlabel('temperature  $T$  (K)')
ax.set_ylabel('$\\rho / \\rho_{300}$')
ax.set_xlim(250, 500); ax.set_ylim(1e-4, 1e2)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5, which='major'); ax.legend(loc='upper right')
```

::: example Worked example 25.1
**Problem.** The forbidden gap of silicon is $1.1\ \text{eV}$. Find the longest
wavelength of light that can lift an electron from its valence band into its
conduction band. Take $h = 6.63\times10^{-34}\ \text{J s}$,
$c = 3\times10^{8}\ \text{m s}^{-1}$, $e = 1.6\times10^{-19}\ \text{C}$.

**Solution.** One photon carries energy $hc/\lambda$. A long wavelength means a
small energy, so the *longest* usable wavelength is the one whose photon energy
is exactly $E_g$:

$$ \frac{hc}{\lambda_{\max}} = E_g $$

Make $\lambda_{\max}$ the subject by cross-multiplying:

$$ \lambda_{\max} = \frac{hc}{E_g} $$

First change $E_g$ from electron-volts to joules by multiplying by the
electronic charge:

$$ E_g = 1.1 \times 1.6\times10^{-19} = 1.76\times10^{-19}\ \text{J} $$

Next work out the numerator $hc$:

$$ hc = 6.63\times10^{-34}\times3\times10^{8} = 1.989\times10^{-25}\ \text{J m} $$

Now divide:

$$ \lambda_{\max} = \frac{1.989\times10^{-25}}{1.76\times10^{-19}}
= 1.13\times10^{-6}\ \text{m} $$

That is $1130\ \text{nm}$, in the infrared. Visible light (400–700 nm) has a
shorter wavelength and therefore more energy than this, which is why a silicon
solar cell works in sunlight.
:::

## 25.3 Intrinsic and extrinsic semi-conductors

### Intrinsic semiconductors

A **pure** semiconductor is called intrinsic. Silicon and germanium are
tetravalent: each atom shares its four valence electrons in covalent bonds with
four neighbours, so at $0\ \text{K}$ every bond is complete and the crystal does
not conduct.

At room temperature thermal energy breaks a few bonds. Each broken bond frees
one electron into the conduction band and leaves behind a vacancy in the valence
band — a **hole**. A neighbouring bound electron can hop into the vacancy,
moving the vacancy the other way, so the hole behaves like a mobile particle of
charge $+e$.

Because carriers are created only in pairs,

$$ n_e = n_h = n_i $$

where $n_i$ is the **intrinsic carrier concentration**:
$1.5\times10^{16}\ \text{m}^{-3}$ for Si and $2.4\times10^{19}\ \text{m}^{-3}$
for Ge at $300\ \text{K}$. Compare this with roughly
$5\times10^{28}$ silicon atoms per cubic metre: only about one atom in
$10^{12}$ contributes a carrier.

::: derivation Conductivity of a semiconductor
**Step 1 — put the sample in a field.** Take a bar of cross-section $A$ and
apply an electric field $E$ along it. By the definition of **mobility**, the
average (drift) speed a carrier picks up is mobility $\times$ field:

$$ v_e = \mu_e E \qquad \text{and} \qquad v_h = \mu_h E $$

**Step 2 — count the electrons that cross a line in time $t$.** Every electron
within a distance $v_e t$ of a chosen cross-section will reach it in time $t$.
That slab has volume $A v_e t$, so the number of electrons in it is

$$ N_e = n_e \times (A v_e t) $$

**Step 3 — turn that into charge, then into current.** Each electron carries
charge $e$, so the charge crossing is $q = e\,n_e A v_e t$. Current is charge
per unit time, so divide by $t$:

$$ I_e = \frac{e\,n_e A v_e t}{t} = e\,n_e A v_e $$

**Step 4 — divide by the area to get current density.**

$$ J_e = \frac{I_e}{A} = e\,n_e v_e $$

**Step 5 — put the drift speed of Step 1 back in.**

$$ J_e = e\,n_e (\mu_e E) = e\,n_e \mu_e E $$

**Step 6 — do the same for holes.** Holes drift the opposite way but carry the
opposite (positive) charge, so their current points the *same* way as the
electron current and the two simply add:

$$ J_h = e\,n_h \mu_h E, \qquad J = J_e + J_h $$

**Step 7 — add and take out the common factors $e$ and $E$.**

$$ J = e\,n_e \mu_e E + e\,n_h \mu_h E = e\left(n_e\mu_e + n_h\mu_h\right)E $$

**Step 8 — compare with Ohm's law.** In point form Ohm's law reads
$J = \sigma E$. Comparing the two expressions for $J$, the bracket must be the
conductivity:

$$ \sigma = e\left(n_e\mu_e + n_h\mu_h\right) $$

**Step 9 — specialise to a pure sample.** Putting $n_e = n_h = n_i$ and taking
$n_i$ out as a common factor,

$$ \sigma_i = e\,n_i\mu_e + e\,n_i\mu_h = e\,n_i(\mu_e + \mu_h),
\qquad \rho_i = \frac{1}{\sigma_i} $$
:::

Here $\mu_e$ and $\mu_h$ are the electron and hole **mobilities** (drift
velocity per unit field, in m² V⁻¹ s⁻¹). Electrons move through the lattice
more easily than holes, so $\mu_e > \mu_h$ always.

::: example Worked example 25.2
**Problem.** For intrinsic germanium at $300\ \text{K}$,
$n_i = 2.4\times10^{19}\ \text{m}^{-3}$,
$\mu_e = 0.39\ \text{m}^{2}\,\text{V}^{-1}\text{s}^{-1}$ and
$\mu_h = 0.19\ \text{m}^{2}\,\text{V}^{-1}\text{s}^{-1}$. Find its conductivity
and resistivity.

**Solution.** The sample is pure, so $n_e = n_h = n_i$ and Step 9 above applies:

$$ \sigma = e\,n_i(\mu_e + \mu_h) $$

Add the two mobilities first:

$$ \mu_e + \mu_h = 0.39 + 0.19 = 0.58\ \text{m}^{2}\,\text{V}^{-1}\text{s}^{-1} $$

Now multiply $e$ by $n_i$. The powers of ten cancel
($10^{-19}\times10^{19} = 10^{0} = 1$):

$$ e\,n_i = 1.6\times10^{-19} \times 2.4\times10^{19} = 3.84\ \text{C m}^{-3} $$

Multiply the two results:

$$ \sigma = 3.84 \times 0.58 = 2.23\ \Omega^{-1}\text{m}^{-1} $$

Finally invert to get resistivity:

$$ \rho = \frac{1}{\sigma} = \frac{1}{2.23} = 0.45\ \Omega\,\text{m} $$

This lies neatly between copper ($1.7\times10^{-8}\ \Omega\,\text{m}$) and glass.
:::

### Extrinsic semiconductors

Intrinsic material is far too resistive to be useful. Adding a controlled trace
of impurity — typically one atom in $10^{6}$ to $10^{8}$ — is called **doping**,
and the result is an **extrinsic** semiconductor.

**n-type.** Dope silicon with a **pentavalent** atom (P, As, Sb, Bi). The
impurity takes the place of a silicon atom in the lattice. Four of its five
valence electrons pair up with electrons of the four silicon neighbours and make
four ordinary covalent bonds. The fifth electron has no partner to bond with. It
is held only weakly by its parent atom, and about $0.045\ \text{eV}$ in silicon
(about $0.01\ \text{eV}$ in germanium) is enough to set it free — far less than
the $1.1\ \text{eV}$ needed to break a bond. Since $kT \approx 0.026\ \text{eV}$
at $300\ \text{K}$, practically every impurity atom has already given up its
fifth electron at room temperature. The impurity **donates** an electron, so it
is called a **donor**, and electrons become the **majority carriers**.

```figure caption="n-type silicon. One silicon atom has been replaced by a pentavalent phosphorus atom. Four of the five valence electrons of P complete the four covalent bonds with its silicon neighbours; the fifth has no bond to join and is free to wander through the crystal."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.1,3.3))
fig.subplots_adjust(0, 0, 1, 1)
S, R, PAD, SEP = 1.5, 0.26, 0.06, 0.14
SIFC = '#dce9f6'

def atom(x, y, sym, dop=False, r=R, fs=9.8):
    ax.add_patch(Circle((x, y), r, facecolor=DOPFC if dop else SIFC,
                        edgecolor=DOPEC if dop else ACCENT, lw=1.3, zorder=4))
    ax.text(x, y, sym, ha='center', va='center', zorder=5, fontsize=fs,
            color=DOPEC if dop else INK,
            fontweight='bold' if dop else 'normal')

def bond(p, q, skip=0):
    p = np.asarray(p, float); q = np.asarray(q, float)
    d = q - p; L = float(np.hypot(d[0], d[1])); u = d / L
    n = np.array([-u[1], u[0]])
    a, b = p + u*(R+PAD), q - u*(R+PAD)
    for s in (1, -1):
        if s == skip:
            continue
        o = n*(SEP/2)*s
        ax.plot([a[0]+o[0], b[0]+o[0]], [a[1]+o[1], b[1]+o[1]], color=INK,
                lw=1.2, zorder=3, solid_capstyle='round')

def legend_row(y, text):
    ax.text(3.88, y, text, va='center', ha='left', fontsize=8.0, color=INK,
            linespacing=1.4)

def legend_bond(y):
    for s in (1, -1):
        ax.plot([3.50, 3.78], [y+s*SEP/2]*2, color=INK, lw=1.2,
                solid_capstyle='round')

def finish():
    ax.set_aspect('equal')
    ax.set_xlim(-0.42, 5.52); ax.set_ylim(-0.42, 3.42); ax.axis('off')

DOPFC, DOPEC = '#fbdedd', SERIES[1]
for i in range(3):
    for j in range(3):
        if i < 2: bond((i*S, j*S), ((i+1)*S, j*S))
        if j < 2: bond((i*S, j*S), (i*S, (j+1)*S))
for i in range(3):
    for j in range(3):
        atom(i*S, j*S, 'P' if (i, j) == (1, 1) else 'Si', dop=(i, j) == (1, 1))

ax.plot([1.69, 1.85], [1.69, 1.85], color=MUTED, lw=1.1, ls=(0, (2, 2)), zorder=2)
ax.plot([1.92], [1.92], 'o', color=INK, ms=8.5, zorder=6)
ax.annotate('', xy=(2.05, 1.99), xytext=(2.32, 2.10),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(2.42, 2.40, 'surplus 5th\nelectron:\nfree to move', ha='center',
        va='center', fontsize=7.8, color=INK, linespacing=1.45)

atom(3.64, 2.95, 'Si', r=0.155, fs=6.6)
legend_row(2.95, 'silicon atom:\n4 valence electrons')
atom(3.64, 2.10, 'P', dop=True, r=0.155, fs=6.6)
legend_row(2.10, 'phosphorus dopant:\n5 valence electrons')
legend_bond(1.25)
legend_row(1.25, 'covalent bond:\n2 shared electrons')
ax.plot([3.64], [0.40], 'o', color=INK, ms=8.5)
legend_row(0.40, 'free electron')
finish()
```
**p-type.** Dope silicon with a **trivalent** atom (B, Al, Ga, In). This atom
brings only three valence electrons, so it can complete only three of the four
bonds with its silicon neighbours. The fourth bond is left with a single
electron instead of a pair. That empty half-bond is a **hole**. A bound electron
from a neighbouring bond needs only about $0.05\ \text{eV}$ to jump across and
fill it, which moves the hole to where that electron came from. Because the
impurity **accepts** an electron it is called an **acceptor**, and holes become
the majority carriers.

```figure caption="p-type silicon. One silicon atom has been replaced by a trivalent aluminium atom. Al can complete only three covalent bonds; the fourth bond is one electron short, and that vacancy is a hole which moves like a positive charge."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.1,3.3))
fig.subplots_adjust(0, 0, 1, 1)
S, R, PAD, SEP = 1.5, 0.26, 0.06, 0.14
SIFC = '#dce9f6'

def atom(x, y, sym, dop=False, r=R, fs=9.8):
    ax.add_patch(Circle((x, y), r, facecolor=DOPFC if dop else SIFC,
                        edgecolor=DOPEC if dop else ACCENT, lw=1.3, zorder=4))
    ax.text(x, y, sym, ha='center', va='center', zorder=5, fontsize=fs,
            color=DOPEC if dop else INK,
            fontweight='bold' if dop else 'normal')

def bond(p, q, skip=0):
    p = np.asarray(p, float); q = np.asarray(q, float)
    d = q - p; L = float(np.hypot(d[0], d[1])); u = d / L
    n = np.array([-u[1], u[0]])
    a, b = p + u*(R+PAD), q - u*(R+PAD)
    for s in (1, -1):
        if s == skip:
            continue
        o = n*(SEP/2)*s
        ax.plot([a[0]+o[0], b[0]+o[0]], [a[1]+o[1], b[1]+o[1]], color=INK,
                lw=1.2, zorder=3, solid_capstyle='round')

def legend_row(y, text):
    ax.text(3.88, y, text, va='center', ha='left', fontsize=8.0, color=INK,
            linespacing=1.4)

def legend_bond(y):
    for s in (1, -1):
        ax.plot([3.50, 3.78], [y+s*SEP/2]*2, color=INK, lw=1.2,
                solid_capstyle='round')

def finish():
    ax.set_aspect('equal')
    ax.set_xlim(-0.42, 5.52); ax.set_ylim(-0.42, 3.42); ax.axis('off')

DOPFC, DOPEC = '#dcefe3', SERIES[2]
for i in range(3):
    for j in range(3):
        if i < 2: bond((i*S, j*S), ((i+1)*S, j*S), skip=1 if (i, j) == (1, 1) else 0)
        if j < 2: bond((i*S, j*S), (i*S, (j+1)*S))
for i in range(3):
    for j in range(3):
        atom(i*S, j*S, 'Al' if (i, j) == (1, 1) else 'Si', dop=(i, j) == (1, 1))

ax.plot([2.25], [S+SEP/2], 'o', mfc='white', mec=INK, mew=1.4, ms=9.0, zorder=6)
ax.annotate('', xy=(2.27, 1.72), xytext=(2.40, 2.16),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(2.46, 2.52, 'hole:\none electron\nmissing', ha='center',
        va='center', fontsize=7.8, color=INK, linespacing=1.45)

atom(3.64, 2.95, 'Si', r=0.155, fs=6.6)
legend_row(2.95, 'silicon atom:\n4 valence electrons')
atom(3.64, 2.10, 'Al', dop=True, r=0.155, fs=5.8)
legend_row(2.10, 'aluminium dopant:\n3 valence electrons')
legend_bond(1.25)
legend_row(1.25, 'covalent bond:\n2 shared electrons')
ax.plot([3.64], [0.40], 'o', mfc='white', mec=INK, mew=1.4, ms=9.0)
legend_row(0.40, 'hole (missing electron)')
finish()
```
In band language the two dopants create new allowed levels inside the forbidden
gap. A donor level sits only $0.045\ \text{eV}$ below the bottom of the
conduction band, so its electron needs almost no help to get in. An acceptor
level sits only about $0.05\ \text{eV}$ above the top of the valence band, so a
valence electron can hop up into it and leave a hole behind.

```figure caption="Donor levels sit just below the conduction band in n-type material; acceptor levels just above the valence band in p-type material. Filled circles are electrons, open circles are holes. The grey arrow shows the tiny jump an electron makes at room temperature."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgba
fig, axs = plt.subplots(1, 2, figsize=(5.0,2.9))
def panel(ax, kind):
    ax.add_patch(Rectangle((0.05,0.0), 0.90, 1.0,
                           facecolor=to_rgba(ACCENT, 0.38), edgecolor=INK, lw=1.0))
    ax.add_patch(Rectangle((0.05,3.0), 0.90, 1.0, facecolor='none',
                           edgecolor=INK, lw=1.0))
    ax.text(0.5, 3.72, 'conduction\nband', ha='center', va='center',
            fontsize=8.0, linespacing=1.3)
    ax.text(0.5, 0.28, 'valence\nband', ha='center', va='center',
            fontsize=8.0, linespacing=1.3)
    xs = [0.20, 0.35, 0.65, 0.80]
    if kind == 'n':
        for x in xs:
            ax.plot([x-0.06, x+0.06], [2.78, 2.78], color=SERIES[1], lw=1.6)
        ax.text(1.06, 2.78, 'donor level:\n0.045 eV below CB', fontsize=7.8,
                color=SERIES[1], va='center', ha='left', linespacing=1.35)
        ax.plot(xs, [3.14]*4, 'o', color=INK, ms=4.2, ls='none')
        ax.annotate('', xy=(0.50,3.08), xytext=(0.50,2.84),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                                    mutation_scale=8))
        ax.text(0.5, 4.45, 'n-type (pentavalent donor)', ha='center',
                va='center', fontsize=9.0, fontweight='bold')
    else:
        for x in xs:
            ax.plot([x-0.06, x+0.06], [1.22, 1.22], color=SERIES[2], lw=1.6)
        ax.text(1.06, 1.22, 'acceptor level:\n0.05 eV above VB', fontsize=7.8,
                color=SERIES[2], va='center', ha='left', linespacing=1.35)
        ax.plot(xs, [0.80]*4, 'o', mfc='none', mec=INK, ms=4.4, mew=1.0,
                ls='none')
        ax.annotate('', xy=(0.50,1.16), xytext=(0.50,0.90),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                                    mutation_scale=8))
        ax.text(0.5, 4.45, 'p-type (trivalent acceptor)', ha='center',
                va='center', fontsize=9.0, fontweight='bold')
    ax.set_xlim(-0.15, 2.10); ax.set_ylim(-0.25, 4.75); ax.axis('off')
panel(axs[0], 'n'); panel(axs[1], 'p')
```
::: derivation Law of mass action, $n_e n_h = n_i^2$
**Step 1 — what makes carriers.** Heat breaks bonds and creates
electron–hole pairs. How fast pairs appear (the generation rate $g$) depends
only on the temperature and the gap $E_g$ — it does not care how much impurity
we added.

**Step 2 — what destroys carriers.** A free electron disappears only when it
meets a hole and drops into it. The chance of a meeting is proportional to how
many electrons there are *and* to how many holes there are, so the
recombination rate is

$$ r = C\,n_e n_h $$

where $C$ is a constant fixed by the material and the temperature.

**Step 3 — steady state.** At a fixed temperature the carrier numbers are not
changing, so pairs must be destroyed exactly as fast as they are made:

$$ g = C\,n_e n_h $$

**Step 4 — make the product the subject.** Divide both sides by $C$:

$$ n_e n_h = \frac{g}{C} $$

The right-hand side contains only $g$ and $C$, and both depend on temperature
alone. So the *product* $n_e n_h$ is the same number for every sample of that
material at that temperature, however it is doped.

**Step 5 — evaluate that number using the pure sample.** In pure material at
the same temperature, $n_e = n_h = n_i$, so

$$ n_e n_h = n_i \times n_i = n_i^{2} $$

**Step 6 — combine.** Since the product is the same for all doping levels and
equals $n_i^2$ for the pure sample, it must equal $n_i^2$ always:

$$ n_e n_h = n_i^{2} $$
:::

So doping to raise one carrier density automatically suppresses the other: push
$n_e$ up by a factor of a million and $n_h$ falls by the same factor.

| Feature | n-type | p-type |
|---|---|---|
| Dopant valency | pentavalent (P, As, Sb) | trivalent (B, Al, Ga, In) |
| Bonds formed by dopant | 4 complete bonds + 1 spare electron | 3 complete bonds + 1 hole |
| Impurity level created | donor, just below CB | acceptor, just above VB |
| Majority carriers | electrons | holes |
| Minority carriers | holes | electrons |
| Carrier relation | $n_e \gg n_h$, $n_e \approx N_d$ | $n_h \gg n_e$, $n_h \approx N_a$ |
| Net charge on crystal | zero | zero |

::: caution A doped crystal is still electrically neutral
"n-type is negatively charged" is wrong, and it costs marks every year. A donor
atom releases one electron but is left as a fixed positive ion, so the totals
still balance. The labels n and p name the **majority carrier**, not a charge on
the block.
:::

::: caution A hole is not a positron
A hole is the *absence* of an electron in a bond — a bookkeeping device for the
motion of the many remaining valence electrons. It exists only inside the
crystal, whereas a positron is a real particle that can travel through vacuum.
:::

::: example Worked example 25.3
**Problem.** Pure silicon has $n_i = 1.5\times10^{16}\ \text{m}^{-3}$ at
$300\ \text{K}$. It is doped with $10^{22}$ donor atoms per m³, all ionised.
Find the electron and hole concentrations, and say which are the minority
carriers.

**Solution.** Every ionised donor hands one electron to the conduction band, and
$N_d = 10^{22}$ is far bigger than $n_i = 1.5\times10^{16}$, so the thermally
generated electrons are negligible in comparison:

$$ n_e \approx N_d = 1\times10^{22}\ \text{m}^{-3} $$

Now use the law of mass action, $n_e n_h = n_i^2$. Make $n_h$ the subject by
dividing both sides by $n_e$:

$$ n_h = \frac{n_i^{2}}{n_e} $$

Square $n_i$ first — square the number and double the power of ten:

$$ n_i^{2} = (1.5\times10^{16})^{2} = 2.25\times10^{32}\ \text{m}^{-6} $$

Then divide, subtracting the powers of ten ($32 - 22 = 10$):

$$ n_h = \frac{2.25\times10^{32}}{1\times10^{22}}
= 2.25\times10^{10}\ \text{m}^{-3} $$

Holes are the minority carriers. Note that one impurity atom per $5\times10^{6}$
silicon atoms has raised the electron density by a factor of about $10^{6}$ —
that is the whole point of doping.
:::

## Chapter summary

- Bringing $N$ atoms together splits each sharp atomic level into $N$ levels so
  close ($\sim 10^{-29}\ \text{eV}$ apart) that they form a continuous **energy
  band**; between bands lie **forbidden gaps**.
- The **valence band** is the highest band filled at $0\ \text{K}$; the
  **conduction band** is the empty band above it; their separation is $E_g$.
- A completely filled band carries no current. Conduction needs empty states
  just above occupied ones.
- Conductor: bands overlap, $E_g = 0$. Semiconductor: $E_g \leq 3\ \text{eV}$
  (Ge 0.7 eV, Si 1.1 eV). Insulator: $E_g > 3\ \text{eV}$ (diamond 5.47 eV).
- Semiconductors have a **negative** temperature coefficient of resistance
  because carrier number grows like $e^{-E_g/2kT}$.
- Intrinsic: $n_e = n_h = n_i$, and $\sigma = e(n_e\mu_e + n_h\mu_h)$ reduces to
  $\sigma_i = e\,n_i(\mu_e+\mu_h)$, with $\rho = 1/\sigma$.
- Extrinsic: a pentavalent dopant makes four bonds and leaves one spare electron
  (n-type, donor level below CB, electrons majority); a trivalent dopant makes
  three bonds and leaves one hole (p-type, acceptor level above VB, holes
  majority). Both crystals remain electrically neutral.
- Law of mass action: $n_e n_h = n_i^{2}$ at a given temperature.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In an intrinsic semiconductor at room temperature <span class="marks">[1]</span>
   (a) $n_e > n_h$ (b) $n_e < n_h$ (c) $n_e = n_h$ (d) $n_h = 0$
2. The forbidden energy gap of germanium is about <span class="marks">[1]</span>
   (a) $0.7\ \text{eV}$ (b) $1.1\ \text{eV}$ (c) $3.0\ \text{eV}$ (d) $5.5\ \text{eV}$
3. On heating a semiconductor its resistance <span class="marks">[1]</span>
   (a) increases (b) decreases (c) stays constant (d) first rises then falls
4. Silicon doped with indium becomes <span class="marks">[1]</span>
   (a) n-type (b) p-type (c) intrinsic (d) an insulator
5. A pure semiconductor at $0\ \text{K}$ behaves as <span class="marks">[1]</span>
   (a) a conductor (b) a superconductor (c) a perfect insulator (d) an n-type semiconductor
6. In n-type silicon the phosphorus atom forms <span class="marks">[1]</span>
   (a) 5 covalent bonds (b) 4 covalent bonds and has 1 spare electron (c) 3 covalent bonds and 1 hole (d) no bonds

::: note Answers to Group A
**1.** (c) — carriers are produced only in electron–hole pairs.
**2.** (a) — Ge 0.7 eV, Si 1.1 eV.
**3.** (b) — the exponential rise in carrier number beats the extra scattering.
**4.** (b) — indium is trivalent, so it supplies acceptor levels.
**5.** (c) — every covalent bond is intact, so both bands are full or empty.
**6.** (b) — silicon offers only four neighbours, so the fifth electron of P has no bond to join.
:::

**Group B — Short answer (5 marks each)**

1. Explain qualitatively how the discrete energy levels of isolated atoms become
   energy bands in a solid. <span class="marks">[5]</span>
2. Using band diagrams, distinguish between a conductor, a semiconductor and an
   insulator. <span class="marks">[5]</span>
3. Why does the resistance of a metal increase but that of a semiconductor
   decrease with rise in temperature? <span class="marks">[5]</span>
4. The energy gap of a certain semiconductor is $0.72\ \text{eV}$. Calculate the
   maximum wavelength of radiation it can absorb.
   ($h = 6.63\times10^{-34}\ \text{J s}$) <span class="marks">[5]</span>
5. Intrinsic silicon has $n_i = 1.5\times10^{16}\ \text{m}^{-3}$. After doping,
   the hole concentration becomes $4.5\times10^{21}\ \text{m}^{-3}$. Find the
   electron concentration and name the type of the semiconductor. <span class="marks">[5]</span>
6. Draw the covalent-bond diagram of silicon doped with a pentavalent atom and
   use it to explain why the material is called n-type although the crystal as a
   whole is neutral. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: sharp levels in an isolated atom → Pauli exclusion forbids $N$
identical states → overlapping of outer orbitals on bringing $N$ atoms together
splits each level into $N$ sub-levels → with $N \sim 10^{29}\ \text{m}^{-3}$ the
spacing is $\sim 10^{-29}\ \text{eV}$, so the set is effectively a continuous
band, separated from the next by a forbidden gap.

**3.** Outline: in a metal the carrier number is fixed, so more violent lattice
vibrations scatter electrons more and $\rho$ rises. In a semiconductor the
carrier number grows like $e^{-E_g/2kT}$; this exponential increase dominates the
extra scattering, so $\rho$ falls (negative temperature coefficient).

**4.** First convert the gap to joules:
$$ E_g = 0.72\times1.6\times10^{-19} = 1.152\times10^{-19}\ \text{J} $$
Then $\lambda_{\max} = hc/E_g$ with $hc = 1.989\times10^{-25}\ \text{J m}$:
$$ \lambda_{\max} = \frac{1.989\times10^{-25}}{1.152\times10^{-19}}
= 1.73\times10^{-6}\ \text{m} = 1730\ \text{nm} $$

**5.** By the law of mass action, $n_e = n_i^2 / n_h$. Square $n_i$ first:
$$ n_i^{2} = (1.5\times10^{16})^{2} = 2.25\times10^{32}\ \text{m}^{-6} $$
Then divide:
$$ n_e = \frac{2.25\times10^{32}}{4.5\times10^{21}} = 5\times10^{10}\ \text{m}^{-3} $$
Holes greatly outnumber electrons, so the material is **p-type**.

**6.** Outline: draw the lattice of the n-type figure — P on a silicon site,
four double-line covalent bonds to four Si neighbours, one extra electron drawn
outside any bond. That spare electron is easily freed (0.045 eV), so electrons
are the majority carriers and the material is called n-type. But the phosphorus
atom that lost the electron is left behind as a *fixed* positive ion inside the
lattice, so the positive and negative charges still balance exactly and the
block is neutral.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define valence band, conduction band and forbidden energy gap. <span class="marks">[3]</span>
   (b) Draw band diagrams for a conductor, a semiconductor and an insulator and
   use them to explain the enormous difference in their resistivities. <span class="marks">[5]</span>
2. (a) Distinguish between intrinsic and extrinsic semiconductors. <span class="marks">[2]</span>
   (b) Draw the covalent-bond lattice of n-type and p-type silicon, showing the
   free electron and the hole, and name the majority carriers in each. <span class="marks">[4]</span>
   (c) A germanium sample has $n_i = 2.4\times10^{19}\ \text{m}^{-3}$,
   $\mu_e = 0.39$ and $\mu_h = 0.19\ \text{m}^{2}\text{V}^{-1}\text{s}^{-1}$.
   Find the resistivity of the pure sample. <span class="marks">[2]</span>

::: note Answer to Group C question 2(c)
Add the mobilities: $\mu_e + \mu_h = 0.39+0.19 = 0.58$. Then
$$ \sigma = e\,n_i(\mu_e+\mu_h) = 1.6\times10^{-19}\times2.4\times10^{19}\times0.58 $$
$$ \sigma = 3.84\times0.58 = 2.23\ \Omega^{-1}\text{m}^{-1} $$
$$ \rho = \frac{1}{\sigma} = \frac{1}{2.23} = 0.45\ \Omega\,\text{m} $$
:::
