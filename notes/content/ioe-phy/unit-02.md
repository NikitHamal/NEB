---
subject: Physics
grade: IOE
unit: 2
title: Heat and Thermodynamics
hours: 4
area: Physics
---

Heat and thermodynamics carry about **4 questions** (our estimate). Calorimetry (mixing hot and cold substances, ice), thermal expansion, radiation ($T^4$), the first law on a gas process, kinetic-theory averages and the efficiency of a Carnot or Otto engine are the standard shapes. Numerical questions are mostly one formula with careful unit handling (kelvin, not Celsius, in $T^4$ and in engine efficiency).

::: key What the paper asks from this chapter
- Calorimetry: $Q=mc\Delta T$, $Q=mL$; the final temperature of a mixture; triple point $273.16$ K.
- Expansion: $\Delta L=L\alpha\Delta T$, $\gamma=3\alpha$ for solids; thermal stress $Y\alpha\Delta T$.
- Conduction $\frac{Q}{t}=\frac{kA\Delta T}{L}$; radiation $P=\sigma AT^4$; Newton's law of cooling.
- Kinetic theory: $\bar K=\frac{3}{2}kT$, $v_{rms}=\sqrt{\frac{3RT}{M}}$, $U=\frac{f}{2}nRT$, $C_p-C_v=R$.
- First law $\Delta U=Q-W$ on isothermal, adiabatic, isobaric and isochoric processes; $PV^\gamma=$ const.
- Heat engines: $\eta=1-\frac{T_2}{T_1}$ (Carnot), Otto $\eta=1-r^{1-\gamma}$, refrigerator COP, entropy.
:::

## 2.1 Temperature and quantity of heat

**Thermal equilibrium** is the content of the zeroth law: bodies in equilibrium with a third are in equilibrium with each other, which defines temperature. Scales: $\frac{C}{5}=\frac{F-32}{9}=\frac{K-273}{5}$ (the same reading $-40$ on Celsius and Fahrenheit). **Triple point of water:** $273.16$ K, 0.01 °C, 611.7 Pa (the fixed point of the Kelvin scale).

**Heat** is energy in transit. $Q=mc\Delta T$; heat capacity $C=mc$; $Q=mL$ ($L_f=336$ kJ kg⁻¹ for ice, $L_v=2256$ kJ kg⁻¹ for steam; $c_{water}=4200$ J kg⁻¹ K⁻¹, $c_{ice}\approx2100$). **Method of mixtures:** heat lost = heat gained; check first whether all the ice melts. **Measuring $c$** by mixtures; **$L$** by the electrical method $VIt=mL$ (Joule's constant $J=4.18$ J cal⁻¹).

**Newton's law of cooling:** rate of cooling $\propto(T-T_s)$ for a small excess; $T=T_s+(T_0-T_s)e^{-kt}$; for the average values $\frac{T_1-T_2}{t}=K\Big(\frac{T_1+T_2}{2}-T_s\Big)$.

## 2.2 Thermal expansion

Linear $\Delta L=L\alpha\Delta T$; area $\beta=2\alpha$; volume $\gamma=3\alpha$ ($\alpha:\beta:\gamma=1:2:3$). Liquids have real expansion $\gamma_r=\gamma_a+\gamma_{vessel}$. Water contracts from 0 to 4 °C, so its density is maximum at 4 °C (ice floats; lakes freeze from the top). If an expansion is prevented, the **thermal stress** is $Y\alpha\Delta T$. A pendulum clock runs slow in summer ($l$ increases). The Bimetallic strip bends towards the metal of lower $\alpha$. Gas expansion: $PV=nRT$; Charles ($V\propto T$ at constant $P$), Boyle ($PV$ const at constant $T$), Gay-Lussac ($P\propto T$).

## 2.3 Transfer of heat

**Conduction:** $\dfrac{Q}{t}=\dfrac{kA(T_1-T_2)}{L}$ ($k$ in W m⁻¹ K⁻¹). Rods of different material in series: $R=\sum\frac{L}{kA}$ (thermal resistance); in parallel the conductances add. Interface temperature of two slabs in series: $T=\frac{k_1T_1/L_1+k_2T_2/L_2}{k_1/L_1+k_2/L_2}$. **Convection** moves heat with a fluid (sea breeze, boiling). **Radiation** needs no medium.

A **black body** absorbs all radiation. **Stefan–Boltzmann:** $E=\sigma T^4$, $\sigma=5.67\times10^{-8}$ W m⁻² K⁻⁴; net power from a body at $T$ in surroundings $T_s$: $P=e\sigma A(T^4-T_s^4)$. Doubling $T$ multiplies the radiated power by 16. **Wien:** $\lambda_mT=2.9\times10^{-3}$ m K. Kirchhoff: a good absorber is a good emitter. Thermos flask: silvering reduces radiation, vacuum stops conduction and convection.

## 2.4 Thermal properties of matter and kinetic theory

**Ideal gas:** $PV=nRT=NkT$, $R=8.314$ J mol⁻¹ K⁻¹, $k=1.38\times10^{-23}$ J K⁻¹, $N_A=6.02\times10^{23}$. **Kinetic theory:** $P=\frac{1}{3}\rho\overline{v^2}$; average translational KE of a molecule $\frac{3}{2}kT$ (independent of the gas); $v_{rms}=\sqrt{\frac{3RT}{M}}=\sqrt{\frac{3P}{\rho}}$, mean $v_{av}=\sqrt{\frac{8RT}{\pi M}}$, most probable $\sqrt{\frac{2RT}{M}}$ ($v_{mp}:v_{av}:v_{rms}=\sqrt{2}:\sqrt{8/\pi}:\sqrt{3}$). $v_{rms}\propto\sqrt{T/M}$: hydrogen is 4 times faster than oxygen at the same temperature. Mean free path $\lambda=\frac{1}{\sqrt{2}\pi d^2n}$.

**Degrees of freedom $f$** (3 monatomic, 5 diatomic at ordinary temperature, 6 non-linear polyatomic); energy per molecule $\frac{f}{2}kT$, so $U=\frac{f}{2}nRT$, $C_v=\frac{f}{2}R$, $C_p=C_v+R$ (Mayer), $\gamma=\frac{C_p}{C_v}=1+\frac{2}{f}$ (5/3, 7/5, 4/3). **Solids** (Dulong–Petit): molar heat capacity $\approx3R=25$ J mol⁻¹ K⁻¹. Vapour pressure, humidity, dew point, boiling at lower pressure on mountains (water boils below 100 °C at the summit of Everest).

## 2.5 Laws of thermodynamics

**First law:** $\Delta U=Q-W$ (heat added to the system, work done *by* it); $W=\int P\,dV$ (area under the $P$–$V$ curve).

| Process | Condition | $W$ | $Q$ | $\Delta U$ |
|---|---|---|---|---|
| isothermal | $T$ const, $PV$ const | $nRT\ln\frac{V_2}{V_1}$ | $=W$ | 0 |
| isobaric | $P$ const | $P\Delta V$ | $nC_p\Delta T$ | $nC_v\Delta T$ |
| isochoric | $V$ const | 0 | $nC_v\Delta T$ | $=Q$ |
| adiabatic | $Q=0$ | $\frac{P_1V_1-P_2V_2}{\gamma-1}$ | 0 | $-W$ |

Adiabatic: $PV^\gamma=$ const, $TV^{\gamma-1}=$ const, $T^\gamma P^{1-\gamma}=$ const. Compressing a gas adiabatically 8-fold (monatomic) raises $P$ by $8^{5/3}=32$. A cyclic process returns $\Delta U=0$; the work is the enclosed area.

**Second law** (Kelvin–Planck: no engine converts heat wholly into work; Clausius: heat does not flow spontaneously from cold to hot). **Heat engine:** $\eta=\frac{W}{Q_1}=1-\frac{Q_2}{Q_1}$. **Carnot cycle** (two isotherms, two adiabats): $\eta=1-\frac{T_2}{T_1}$ (kelvin), the maximum possible between two temperatures, reversible. **Otto** (petrol): $\eta=1-\frac{1}{r^{\gamma-1}}$ ($r=8$, $\gamma=1.4$: 56.5 %). **Diesel:** higher compression ratio, injection at constant pressure. **Refrigerator:** COP $=\frac{Q_2}{W}=\frac{T_2}{T_1-T_2}$. **Entropy** $\Delta S=\frac{Q}{T}$; the entropy of an isolated system never decreases; melting at $T$: $\Delta S=\frac{mL}{T}$.

::: caution Thermodynamic traps
Use kelvin in $T^4$, efficiency and $v_{rms}$. In $\Delta U=Q-W$, $W$ is work done *by* the gas. Efficiency of any real engine is below Carnot. Specific heat capacity of an isothermal process is infinite; of an adiabatic one, zero.
:::

## Formula and fact sheet

| Topic | Result |
|---|---|
| mixture | $\sum mc\Delta T=0$ (with latent heat if a phase changes) |
| expansion | $\Delta L=L\alpha\Delta T$; $\gamma=3\alpha$ |
| conduction | $\frac{kA\Delta T}{L}$ |
| radiation | $\sigma AT^4$; $\lambda_mT=2.9\times10^{-3}$ |
| kinetic | $\frac{3}{2}kT$; $v_{rms}=\sqrt{3RT/M}$ |
| gas energy | $U=\frac{f}{2}nRT$; $C_p-C_v=R$ |
| isothermal work | $nRT\ln\frac{V_2}{V_1}$ |
| Carnot $\eta$ | $1-T_2/T_1$ |

## Chapter summary

- Heat lost = heat gained; check for a phase change first.
- $\gamma=3\alpha$; blocked expansion gives stress $Y\alpha\Delta T$.
- Radiation scales as $T^4$ (kelvin), conduction as $\Delta T/L$.
- $\bar K=\frac{3}{2}kT$ for every ideal gas; $v_{rms}\propto\sqrt{T/M}$.
- Know the four processes' $W$, $Q$ and $\Delta U$; adiabatic means $PV^\gamma=$ const.
- No engine beats Carnot; entropy of an isolated system never decreases.

## Practice questions

**Set A — Recall (10 questions)**

1. The temperature of the triple point of water is
   (a) 273.15 K (b) 273.16 K (c) 0 K (d) 373.15 K
2. The heat required to raise 2 kg of water by 10 °C ($c=4200$ J kg⁻¹ K⁻¹) is
   (a) 8400 J (b) 42000 J (c) 84000 J (d) 840 J
3. If the absolute temperature of a black body is doubled, the radiated power becomes
   (a) 2 times (b) 4 times (c) 8 times (d) 16 times
4. For a solid, the coefficients of linear and volume expansion are related by
   (a) $\gamma=3\alpha$ (b) $\gamma=2\alpha$ (c) $\gamma=\alpha/3$ (d) $\gamma=\alpha$
5. In an isothermal process of an ideal gas
   (a) $Q=0$ (b) $W=0$ (c) $\Delta U=0$ (d) $\Delta P=0$
6. For an ideal gas $C_p-C_v$ equals
   (a) $R$ (b) $R/2$ (c) $2R$ (d) 0
7. The efficiency of a Carnot engine working between 600 K and 300 K is
   (a) 25 % (b) 50 % (c) 75 % (d) 100 %
8. The mean translational kinetic energy of a gas molecule at temperature $T$ is
   (a) $\frac{1}{2}kT$ (b) $kT$ (c) $\frac{3}{2}kT$ (d) $3kT$
9. In a spontaneous process the entropy of the universe
   (a) increases (b) decreases (c) is zero (d) stays constant
10. The SI unit of thermal conductivity is
    (a) W m⁻² (b) J K⁻¹ (c) W K (d) W m⁻¹ K⁻¹

::: note Answers and explanations — Set A
**1.** (b) — $273.16$ K (0.01 °C), the defining fixed point.
**2.** (c) — $2\times4200\times10$.
**3.** (d) — $P\propto T^4$, $2^4=16$.
**4.** (a) — $\gamma=3\alpha$ ($\beta=2\alpha$ is the area coefficient).
**5.** (c) — constant temperature means no change in internal energy; $Q=W$.
**6.** (a) — Mayer's relation.
**7.** (b) — $1-\frac{300}{600}$.
**8.** (c) — $\frac{3}{2}kT$, independent of the gas.
**9.** (a) — second law.
**10.** (d) — from $Q/t=kA\Delta T/L$.
:::

**Set B — Understanding (7 questions)**

1. 100 g of ice at 0 °C is added to 0.5 kg of water at 40 °C ($L_f=336$ kJ kg⁻¹, $c=4.2$ kJ kg⁻¹ K⁻¹). The final temperature is
   (a) 10 °C (b) 25 °C (c) 20 °C (d) 30 °C
2. A 1 m rod expands by 1.2 mm when heated through 100 °C. Its coefficient of linear expansion is
   (a) $1.2\times10^{-6}$ K⁻¹ (b) $1.2\times10^{-5}$ K⁻¹ (c) $1.2\times10^{-4}$ K⁻¹ (d) $1.2\times10^{-3}$ K⁻¹
3. A slab of $k=0.8$ W m⁻¹ K⁻¹, area 2 m² and thickness 0.1 m has 25 K across it. The heat conducted per second is
   (a) 200 W (b) 800 W (c) 400 W (d) 40 W
4. A monatomic ideal gas ($\gamma=\frac{5}{3}$) is compressed adiabatically to $\frac{1}{8}$ of its volume. Its pressure rises by a factor
   (a) 8 (b) 32 (c) 16 (d) 40
5. One mole of an ideal gas at 300 K expands isothermally to twice its volume. The work done is nearly
   ($R=8.314$)
   (a) 1.73 kJ (b) 2.49 kJ (c) 0.86 kJ (d) 3.46 kJ
6. A refrigerator keeps its inside at 270 K in a room at 300 K. Its maximum coefficient of performance is
   (a) 9 (b) 0.9 (c) 10 (d) 1/9
7. The ratio of $v_{rms}$ of hydrogen to oxygen at the same temperature is
   (a) 16 (b) 2 (c) 8 (d) 4

::: note Answers and explanations — Set B
**1.** (c) — water gives $0.5\times4200\times40=84000$ J to reach 0 °C; melting uses $0.1\times336000=33600$ J; the rest, $50400$ J, warms $0.6$ kg: $\Delta T=\frac{50400}{2520}=20$ °C.
**2.** (b) — $\alpha=\frac{\Delta L}{L\Delta T}=\frac{1.2\times10^{-3}}{100}$.
**3.** (c) — $\frac{0.8\times2\times25}{0.1}=400$ W.
**4.** (b) — $P_2/P_1=8^{5/3}=2^5=32$.
**5.** (a) — $RT\ln2=8.314\times300\times0.693\approx1729$ J.
**6.** (a) — $\frac{T_2}{T_1-T_2}=\frac{270}{30}$.
**7.** (d) — $\sqrt{M_O/M_H}=\sqrt{32/2}=4$.
:::

**Set C — Application (5 questions)**

1. A Carnot engine between 500 K and 300 K absorbs 1000 J per cycle. The work done per cycle is
   (a) 600 J (b) 400 J (c) 200 J (d) 500 J
2. A 0.5 kg metal block at 100 °C is dropped into 1 kg of water at 20 °C and the final temperature is 25 °C ($c_w=4200$). The specific heat of the metal is
   (a) 560 J kg⁻¹ K⁻¹ (b) 420 (c) 840 (d) 280
3. An Otto engine has compression ratio 8 and $\gamma=1.4$. Its efficiency is about
   (a) 43.5 % (b) 65 % (c) 87.5 % (d) 56.5 %
4. A steel rail fixed at both ends is heated by 20 °C ($Y=2\times10^{11}$ Pa, $\alpha=12\times10^{-6}$ K⁻¹). The thermal stress is
   (a) $4.8\times10^7$ Pa (b) $2.4\times10^7$ Pa (c) $4.8\times10^6$ Pa (d) $9.6\times10^7$ Pa
5. The internal energy of 2 mol of a monatomic ideal gas at 300 K is nearly
   (a) 5.0 kJ (b) 12.5 kJ (c) 7.5 kJ (d) 3.7 kJ

::: note Answers and explanations — Set C
**1.** (b) — $\eta=1-\frac{300}{500}=0.4$; $W=400$ J.
**2.** (a) — $0.5\,c\,(75)=1\times4200\times5\Rightarrow c=560$.
**3.** (d) — $1-8^{-0.4}=1-0.435$.
**4.** (a) — $Y\alpha\Delta T=2\times10^{11}\times12\times10^{-6}\times20$.
**5.** (c) — $U=\frac{3}{2}nRT=1.5\times2\times8.314\times300\approx7.5$ kJ.
:::
