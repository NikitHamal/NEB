---
file: NEBians-IOE-Past-Paper-Electronics-Circuit-EX154-2082-Baishakh.pdf
subject: Electronics Circuit
level: BE · Year I / Part II
code: EX 154
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
What are the large signal models of PN junction diode? Explain with necessary figures and examples. [[4]]

@q 2
Explain the operation of light emitting diode (LED). Draw the circuit diagram of center-tapped full wave rectifier. [[4]]

@q 3
Explain the operation of NPN transistor in active mode. Also derive the relationship between α and β. [[6]]

@q 4
Find input impedance, output impedance, and voltage gain for the following amplifier circuit. Given: r$_e$ = 20 Ω, β = 200. [[6]]

```figure caption="Question 4: voltage-divider biased CE amplifier, V$_{CC}$ = +10 V, R$_1$ = R$_2$ = 10 kΩ, R$_C$ = 2 kΩ, R$_E$ = 4.3 kΩ (bypassed by C$_E$), R$_s$ = 600 Ω, R$_L$ = 10 kΩ."
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
fig,ax=ckt_canvas(5.6,4.0,xlim=(-2.0,10.0),ylim=(-0.9,8.2))
wire(ax,[(2.6,7.0),(6.2,7.0)]); terminal(ax,(6.2,7.0)); label(ax,(6.7,7.0),"V$_{CC}$ = +10 V",ha="left",size=8)
res(ax,(2.6,7.0),(2.6,4.8),"R$_1$ = 10 kΩ",side=-1,off=0.2); label(ax,(1.0,5.9),"",size=1)
wire(ax,[(2.6,4.8),(2.6,3.8)]); node(ax,(2.6,3.8)); wire(ax,[(2.6,3.8),(3.5,3.8)])
wire(ax,[(2.6,3.8),(2.6,2.8)]); res(ax,(2.6,2.8),(2.6,0.9),"R$_2$ = 10 kΩ",side=-1,off=0.2); gnd(ax,(2.6,0.9))
bj=bjt(ax,4.2,3.8)
wire(ax,[(4.8,7.0),(4.8,6.6)]); node(ax,(4.8,7.0)); res(ax,(4.8,7.0),(4.8,5.4),"R$_C$ = 2 kΩ",side=1,off=0.15); wire(ax,[(4.8,5.4),(4.8,4.9)])
node(ax,(4.8,5.15)); wire(ax,[(4.8,5.15),(6.0,5.15)]); cap(ax,(6.0,5.15),(6.8,5.15)); wire(ax,[(6.8,5.15),(8.4,5.15)]); node(ax,(8.4,5.15)); terminal(ax,(8.4,5.15))
wire(ax,[(8.4,5.15),(8.4,4.6)]); res(ax,(8.4,5.15),(8.4,3.1),"R$_L$ = 10 kΩ",side=1,off=0.15); gnd(ax,(8.4,3.1))
wire(ax,[(4.8,2.7),(4.8,2.3)]); node(ax,(4.8,2.3)); res(ax,(4.8,2.3),(4.8,0.9),"R$_E$ = 4.3 kΩ",side=1,off=0.15,body=0.8); gnd(ax,(4.8,0.9))
wire(ax,[(4.8,2.3),(7.6,2.3)]); cap(ax,(7.6,2.3),(7.6,0.9)); wire(ax,[(7.6,0.9),(4.8,0.9)])
label(ax,(8.1,1.6),"C$_E$",ha="left",size=8)
wire(ax,[(2.6,3.8),(1.9,3.8)]); cap(ax,(1.9,3.8),(1.1,3.8)); wire(ax,[(1.1,3.8),(0.4,3.8)]); res(ax,(0.4,3.8),(-1.2,3.8),"R$_s$ = 600 Ω",side=1,off=0.5)
wire(ax,[(-1.2,3.8),(-1.6,3.8),(-1.6,3.0)]); acsrc(ax,(-1.6,1.6),(-1.6,3.0),"v$_s$",side=-1,off=0.6); gnd(ax,(-1.6,1.6))
```

@q 5
Explain the construction and operation of an n-channel depletion type MOSFET with necessary diagrams. [[6]]

@q 6
Find the drain current (I$_D$) and drain to source voltage (V$_{DS}$) for the following circuit. The given parameters are V$_t$ = 1 V and K = 0.5 mA/V$^2$. [[6]]

```figure caption="Question 6: enhancement MOSFET, V$_{DD}$ = +10 V, R$_1$ = R$_2$ = 10 MΩ, R$_D$ = 6 kΩ, R$_S$ = 6 kΩ."
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
fig,ax=ckt_canvas(4.4,3.9,xlim=(-1.2,7.0),ylim=(-0.8,8.0))
wire(ax,[(1.2,7.0),(5.2,7.0)]); terminal(ax,(5.2,7.0)); label(ax,(5.6,7.0),"+10 V",ha="left",size=8.2)
res(ax,(1.2,7.0),(1.2,4.7),"R$_1$ = 10 MΩ",side=-1,off=0.2); wire(ax,[(1.2,4.7),(1.2,3.5)]); node(ax,(1.2,3.5)); wire(ax,[(1.2,3.5),(2.3,3.5)])
wire(ax,[(1.2,3.5),(1.2,2.6)]); res(ax,(1.2,2.6),(1.2,0.7),"R$_2$ = 10 MΩ",side=-1,off=0.2); gnd(ax,(1.2,0.7))
m=mosfet(ax,3.0,3.5,"n","enh")
wire(ax,[(4.0,7.0),(4.0,6.6)]); node(ax,(4.0,7.0)); res(ax,(4.0,7.0),(4.0,5.4),"R$_D$ = 6 kΩ",side=1,off=0.2); wire(ax,[(4.0,5.4),(4.0,4.6)])
wire(ax,[(4.0,2.4),(4.0,2.0)]); res(ax,(4.0,2.0),(4.0,0.7),"R$_S$ = 6 kΩ",side=1,off=0.2,body=0.8); gnd(ax,(4.0,0.7))
label(ax,(-0.5,7.5),"",ha="left",size=7.6)
```

@q 7
Write any four properties of ideal Op-Amp. Design a circuit diagram for summing amplifier to generate output voltage V$_o$ = 2V$_1$ − 4V$_2$ + 5V$_3$, where V$_1$, V$_2$, V$_3$ are input signals. [[4]]

@q 8
Draw and explain the circuit diagram of Wien bridge oscillator. Also derive the expression for frequency of oscillation. [[4]]

@q 9
Draw the circuit diagram of the series fed class A amplifier and calculate its maximum efficiency. [[6]]

@q 10
Draw a class A tuned amplifier circuit and find its 3 dB bandwidth. [[6]]

@q 11
Find the Zener current in the given circuit. Assume V$_Z$ = 10 V. [[4]]

```figure caption="Question 11: Zener shunt circuit, V$_S$ = 18 V, R = 100 Ω, R$_L$ = 1.2 kΩ, V$_o$ = 10 V."
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
fig,ax=ckt_canvas(4.6,2.5,xlim=(-1.4,8.4),ylim=(-0.2,5.0))
wire(ax,[(0.0,0.6),(6.4,0.6)]); vsrc(ax,(0.0,0.6),(0.0,3.4),"V$_S$ = 18 V",side=-1,off=0.9); wire(ax,[(0.0,3.4),(0.0,4.2),(1.0,4.2)])
res(ax,(1.0,4.2),(3.0,4.2),"R$_S$ = 100 Ω",side=1,off=0.45,body=1.4); wire(ax,[(3.0,4.2),(6.4,4.2)])
node(ax,(4.2,4.2)); node(ax,(4.2,0.6)); diode(ax,(4.2,0.6),(4.2,4.2),"D$_Z$ (10 V)",side=1,off=0.5,zener=True,body=0.7)
node(ax,(6.4,4.2)); wire(ax,[(6.4,4.2),(6.4,3.9)]); res(ax,(6.4,3.9),(6.4,0.6),"R$_L$ = 1.2 kΩ",side=1,off=0.2,body=1.4)
gnd(ax,(0.0,0.6))
```

@q 12
Draw the series dc voltage regulator with current limiting element and explain how it works. [[4]]
<!-- SOLUTIONS -->

@s 1
**Why a large-signal model is needed.** The diode current follows the Shockley equation i$_D$ = I$_S$(e$^{v_D/nV_T}$ − 1), which is non-linear. When the signal is large compared with the thermal voltage (V$_T$ ≈ 26 mV), the diode cannot be linearised about one Q-point, so the exponential curve is replaced by straight-line (piece-wise linear) approximations called **large-signal models**. Each model is a combination of an ideal diode (a switch that is closed for forward bias and open for reverse bias) with a battery and a resistor.

```figure caption="Large-signal models of the PN junction diode compared with the real characteristic."
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
fig,axs=plt.subplots(1,4,figsize=(7.6,2.3))
v=np.linspace(-0.3,1.0,400)
def real(v): return 1e-3*(np.exp((v-0.62)/0.052)-1)
for a,t in zip(axs,["(a) real diode","(b) ideal model","(c) constant-drop model","(d) piece-wise linear model"]):
    a.axhline(0,color=MUTED,lw=0.6); a.axvline(0,color=MUTED,lw=0.6); a.set_title(t,fontsize=7.2)
    a.set_xlim(-0.3,1.0); a.set_ylim(-0.1,1.1); a.set_xticks([]); a.set_yticks([])
    a.set_xlabel("v$_D$",fontsize=7.4); a.set_ylabel("i$_D$",fontsize=7.4)
    for s in ("top","right"): a.spines[s].set_visible(False)
axs[0].plot(v,np.clip(real(v),-0.1,1.1),color=INK,lw=1.4)
axs[1].plot([-0.3,0],[0,0],color=INK,lw=1.5); axs[1].plot([0,0],[0,1.0],color=INK,lw=1.5)
axs[2].plot([-0.3,0.7],[0,0],color=INK,lw=1.5); axs[2].plot([0.7,0.7],[0,1.0],color=INK,lw=1.5); axs[2].text(0.70,-0.07,"V$_D$ = 0.7 V",fontsize=6.4,ha="center")
axs[3].plot([-0.3,0.55],[0,0],color=INK,lw=1.5); axs[3].plot([0.55,0.9],[0,1.0],color=INK,lw=1.5); axs[3].text(0.55,-0.07,"V$_γ$",fontsize=6.8,ha="center"); axs[3].text(0.62,0.62,"slope = 1/r$_d$",fontsize=6.2,color=ACCENT)
axs[3].plot(v,np.clip(real(v),-0.1,1.1),color=MUTED,lw=0.9,ls="--")
fig.tight_layout()
```

| Model | Forward (v$_D$ > threshold) | Reverse | Use |
|---|---|---|---|
| **Ideal diode** | short circuit, v$_D$ = 0 | open circuit, i$_D$ = 0 | quick hand analysis when the supply is much larger than 0.7 V |
| **Constant-voltage-drop** | ideal diode in series with a battery V$_D$ = 0.7 V (Si) | open circuit | the usual model, error below a few percent |
| **Piece-wise linear** | ideal diode + battery V$_γ$ (cut-in voltage, 0.5 to 0.65 V) + resistor r$_d$ (slope 1/r$_d$) | open circuit | when the forward resistance matters |

**Example.** A silicon diode is in series with R = 1 kΩ and a 5 V supply.

$$\begin{gathered}
\text{Ideal: } I=\frac{5}{1\ \text{k}\Omega}=5.00\ \text{mA} \\
\text{Constant drop: } I=\frac{5-0.7}{1\ \text{k}\Omega}=4.30\ \text{mA} \\
\text{Piece-wise linear } (V_\gamma=0.65\ \text{V},\ r_d=20\ \Omega):\ I=\frac{5-0.65}{1000+20}=4.26\ \text{mA}
\end{gathered}$$

The ideal model is about 16 percent high, while the last two answers agree within 1 percent. With a 1 V supply the ideal model would give 1 mA against 0.30 mA from the constant-drop model, which shows why the drop must be kept for small supplies.

@s 2
**Operation of the LED.** An LED is a p-n junction made of a direct-band-gap compound semiconductor (GaAs, GaAsP, GaP, AlGaInP, GaN). When it is **forward biased**, the barrier falls and electrons from the n-side and holes from the p-side are injected across the junction. Near the junction the injected electrons **recombine** with holes, and in a direct-gap material each recombination releases the energy as a **photon**:

$$\begin{gathered}E=h\nu\approx E_g \\ \lambda\ (\mu\text{m})=\frac{1.24}{E_g\ (\text{eV})}\end{gathered}$$

So the colour is set by the band gap: GaAs (1.4 eV) is infrared, GaAsP red (about 1.8 V forward drop), GaP green, GaN blue (about 3.2 V). In reverse bias no current flows and no light is emitted. An LED needs a **series resistor** to limit the current, R$_S$ = (V$_S$ − V$_F$)/I$_F$; for example V$_S$ = 5 V, V$_F$ = 2 V and I$_F$ = 10 mA give R$_S$ = 300 Ω. The light output is proportional to the forward current; the response is fast (nanoseconds) and the efficiency is high, which is why LEDs are used as indicators, displays, optocouplers and fibre-optic sources.

```figure caption="LED circuit (left) and recombination at the forward-biased junction (right)."
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
fig=plt.figure(figsize=(7.2,2.6))
ax=fig.add_axes([0.0,0.0,0.52,1.0]); ax.set_xlim(-0.6,8.4); ax.set_ylim(-0.6,4.6); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.0,0.2),(1.0,0.8)]); batt(ax,(1.0,0.2),(1.0,3.0),"V$_S$",side=-1,off=0.7)
wire(ax,[(1.0,3.0),(1.0,4.0),(3.0,4.0)]); res(ax,(3.0,4.0),(5.0,4.0),"R$_S$",side=1,off=0.45)
wire(ax,[(5.0,4.0),(6.4,4.0),(6.4,3.3)]); diode(ax,(6.4,3.3),(6.4,1.1),"LED",side=1,off=0.9,body=0.7)
wire(ax,[(6.4,1.1),(6.4,0.2),(1.0,0.2)])
for dx in (0.0,0.45):
    ax.annotate("",xy=(7.7+dx*0.6,2.9+dx),xytext=(7.0+dx*0.6,2.2+dx),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.4,mutation_scale=9))
label(ax,(7.9,1.8),"light",ha="left",size=7.6,color=ACCENT)
b=fig.add_axes([0.60,0.2,0.38,0.7]); b.set_xlim(0,10); b.set_ylim(0,6); b.axis('off')
b.add_patch(Rectangle((0.5,0.8),3.6,3.6,fc="#cfe0f5",ec=INK,lw=1)); b.add_patch(Rectangle((5.9,0.8),3.6,3.6,fc="#f5d9d4",ec=INK,lw=1))
b.text(2.3,2.6,"n-region\n(electrons)",ha="center",va="center",fontsize=7); b.text(7.7,2.6,"p-region\n(holes)",ha="center",va="center",fontsize=7)
b.annotate("",xy=(5.9,3.3),xytext=(4.1,3.3),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); b.annotate("",xy=(4.1,1.8),xytext=(5.9,1.8),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2))
b.text(5.0,2.55,"recombination\n→ photon hν",ha="center",va="center",fontsize=6.4,color=ACCENT)
b.text(2.3,5.1,"n (cathode, −)",ha="center",fontsize=7.4); b.text(7.7,5.1,"p (anode, +)",ha="center",fontsize=7.4)
```

**Centre-tapped full-wave rectifier.** The transformer secondary has a centre tap that is the common (zero) reference. Each half of the secondary gives a peak voltage V$_m$ with respect to the tap. During the positive half cycle D$_1$ conducts (D$_2$ is reverse biased), during the negative half cycle D$_2$ conducts, and the current through R$_L$ always has the same direction.

```figure caption="Centre-tapped full-wave rectifier and its waveforms."
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
fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.56,1.0]); ax.set_xlim(-1.2,11.2); ax.set_ylim(-1.2,6.2); ax.set_aspect('equal'); ax.axis('off')
t=transformer(ax,1.0,0.6,w=1.8,h=3.4,turns=7)
acsrc(ax,(-0.6,1.2),(-0.6,3.2),"v$_i$",side=-1,off=0.6)
wire(ax,[(-0.6,3.2),(-0.6,t["p_top"][1]),t["p_top"]]); wire(ax,[(-0.6,1.2),(-0.6,t["p_bot"][1]),t["p_bot"]])
yt=t["s_top"][1]; yb=t["s_bot"][1]; ym=(yt+yb)/2; x0=t["s_top"][0]
diode(ax,(x0,yt),(x0+3.0,yt),"D$_1$",side=1,off=0.5); diode(ax,(x0,yb),(x0+3.0,yb),"D$_2$",side=-1,off=0.5)
xb=x0+4.0; wire(ax,[(x0+3.0,yt),(xb,yt),(xb,yb),(x0+3.0,yb)]); node(ax,(xb,ym))
wire(ax,[(xb,ym),(xb+1.6,ym)]); res(ax,(xb+1.6,ym),(xb+1.6,ym-2.2),"R$_L$",side=1,off=0.45); gnd(ax,(xb+1.6,ym-2.2))
wire(ax,[(x0,ym),(x0+0.5,ym)]); gnd(ax,(x0+0.5,ym)); label(ax,(x0+0.6,ym+0.4),"CT",size=7.4,ha="center")
b=fig.add_axes([0.66,0.55,0.32,0.38]); x=np.linspace(0,4*np.pi,400); b.plot(x,np.sin(x),color=INK,lw=1.2); b.set_xticks([]); b.set_yticks([]); b.set_title("secondary half v$_s$ (each half)",fontsize=7); b.axhline(0,color=MUTED,lw=0.6)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.66,0.08,0.32,0.38]); c.plot(x,np.abs(np.sin(x)),color=ACCENT,lw=1.4); c.set_xticks([]); c.set_yticks([]); c.set_title("load voltage v$_L$ (D$_1$, D$_2$ alternately)",fontsize=7)
for s in ("top","right"): c.spines[s].set_visible(False)
```

$$\begin{gathered}V_{dc}=\frac{2V_m}{\pi}=0.636\,V_m,\qquad V_{rms}=\frac{V_m}{\sqrt2} \\
\text{ripple factor }r=\sqrt{\frac{\pi^2}{8}-1}=0.482,\qquad \eta_{max}=\frac{8}{\pi^2}=81.2\ \text{percent} \\
\text{PIV}=2V_m,\qquad f_{ripple}=2f
\end{gathered}$$

@s 3
**Active mode.** In the active region the emitter-base junction is **forward biased** (V$_{BE}$ ≈ 0.7 V) and the collector-base junction is **reverse biased** (V$_{CB}$ > 0). Operation of the n-p-n transistor:

1. The heavily doped n-type emitter injects a large number of **electrons** into the thin p-type base (I$_{nE}$); a very small number of holes go from base to emitter (I$_{pE}$, made small by the doping ratio).
2. The base is thin and lightly doped, so only a few electrons (a few percent) recombine with holes there. The recombination current and the hole injection form the **base current I$_B$**.
3. The remaining electrons diffuse to the collector-base depletion region, where the strong reverse field sweeps them into the collector. This is the **collector current I$_C$**, which hardly depends on V$_{CB}$.
4. A small reverse saturation current I$_{CBO}$ (thermally generated minority carriers) also flows across the reverse-biased collector junction.

```figure caption="Carrier flow in an n-p-n transistor in the active region."
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
fig=plt.figure(figsize=(7.0,2.7))
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,14); ax.set_ylim(0,5.4); ax.axis('off')
ax.add_patch(Rectangle((1.2,1.5),3.4,2.2,fc="#cfe0f5",ec=INK,lw=1.2)); ax.add_patch(Rectangle((4.6,1.5),1.4,2.2,fc="#f5d9d4",ec=INK,lw=1.2)); ax.add_patch(Rectangle((6.0,1.5),3.4,2.2,fc="#cfe0f5",ec=INK,lw=1.2))
ax.text(2.9,2.6,"n  emitter\n(heavily doped)",ha="center",va="center",fontsize=7.4); ax.text(5.3,2.6,"p\nbase",ha="center",va="center",fontsize=7.4); ax.text(7.7,2.6,"n  collector",ha="center",va="center",fontsize=7.4)
ax.add_patch(Rectangle((4.6,1.5),0.0,2.2,fc="none")); ax.text(4.6,3.95,"E–B junction\nforward biased",ha="center",fontsize=6.6); ax.text(6.0,3.95,"C–B junction\nreverse biased",ha="center",fontsize=6.6)
ax.annotate("",xy=(5.0,2.9),xytext=(3.6,2.9),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6)); ax.annotate("",xy=(8.2,2.9),xytext=(5.6,2.9),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6))
ax.text(5.5,3.15,"I$_{nE}$ electrons",fontsize=6.4,color=ACCENT,ha="center")
ax.annotate("",xy=(4.8,1.3),xytext=(5.3,0.4),arrowprops=dict(arrowstyle="<|-",color=INK,lw=1.2)); ax.text(5.5,0.3,"I$_B$ (recombination + hole injection)",fontsize=6.6,va="center")
ax.plot([1.2,1.2,0.6],[2.6,2.6,2.6],color=INK); ax.text(0.4,2.6,"E",fontsize=9,ha="right",va="center"); ax.plot([9.4,10.0],[2.6,2.6],color=INK); ax.text(10.1,2.6,"C",fontsize=9,va="center")
ax.plot([5.3,5.3],[1.5,1.0],color=INK); ax.text(5.3,0.85,"",fontsize=1)
ax.text(11.3,4.6,"V$_{EB}$ ≈ +0.7 V forward",fontsize=7,ha="left"); ax.text(11.3,3.9,"V$_{CB}$ > 0 reverse",fontsize=7,ha="left")
ax.text(11.3,2.8,"I$_E$ = I$_B$ + I$_C$",fontsize=8,ha="left",color=ACCENT)
ax.text(11.3,2.0,"I$_C$ = αI$_E$ + I$_{CBO}$",fontsize=8,ha="left")
```

**Relation between α and β.** By Kirchhoff's current law for the whole transistor,

$$I_E=I_B+I_C$$

The d.c. current gains are defined as

$$\begin{gathered}\alpha=\frac{I_C}{I_E}\ (<1,\ 0.95\text{ to }0.995) \\ \beta=\frac{I_C}{I_B}\ (50\text{ to }300)\end{gathered}$$

Dividing I$_E$ = I$_B$ + I$_C$ by I$_C$:

$$\frac{1}{\alpha}=\frac{I_E}{I_C}=\frac{I_B}{I_C}+1=\frac{1}{\beta}+1$$

$$\boxed{\ \beta=\frac{\alpha}{1-\alpha},\qquad \alpha=\frac{\beta}{1+\beta},\qquad I_E=(\beta+1)I_B\ }$$

*Example:* α = 0.98 gives β = 0.98/0.02 = 49; β = 200 gives α = 200/201 = 0.995. Including the leakage, I$_C$ = αI$_E$ + I$_{CBO}$ = βI$_B$ + (β + 1)I$_{CBO}$.

@s 4
The emitter resistor R$_E$ is bypassed by C$_E$, so for a.c. the emitter is grounded and the hybrid-π model of the stage is the one below (r$_o$ is neglected, no value is given).

```figure caption="Small-signal model of the CE stage (R$_B$ = R$_1$ ∥ R$_2$)."
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
fig,ax=ckt_canvas(6.0,2.6,xlim=(-0.9,10.4),ylim=(-0.6,4.2))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.5,1.5),"v$_i$",size=9)
wire(ax,[(0,3),(1.2,3)]); node(ax,(1.2,3)); res(ax,(1.2,3),(1.2,0),"R$_B$",side=-1,off=0.55)
wire(ax,[(1.2,3),(2.8,3)]); res(ax,(2.8,3),(2.8,0),"r$_π$",side=-1,off=0.55,body=1.0)
wire(ax,[(2.8,3),(8.6,3)]); node(ax,(2.8,3)); node(ax,(4.6,3))
isrc(ax,(4.6,0),(4.6,3),None); label(ax,(5.1,1.5),"g$_m$v$_π$",ha="left",size=9)
node(ax,(6.4,3)); res(ax,(6.4,3),(6.4,0),"R$_C$",side=1,off=0.55)
node(ax,(7.8,3)); res(ax,(7.8,3),(7.8,0),"R$_L$",side=1,off=0.55)
wire(ax,[(8.6,3),(9.0,3)]); terminal(ax,(9.0,3)); terminal(ax,(9.0,0)); label(ax,(9.6,1.5),"v$_o$",size=9)
wire(ax,[(0,0),(9.0,0)]); node(ax,(1.2,0)); node(ax,(2.8,0)); node(ax,(4.6,0)); node(ax,(6.4,0)); node(ax,(7.8,0))
label(ax,(3.3,3.5),"v$_π$ across r$_π$",size=7,color=MUTED,ha="left")
```

**Input impedance.** R$_B$ = R$_1$ ∥ R$_2$ = 10 k ∥ 10 k = 5 kΩ, and the resistance looking into the base is r$_π$ = βr$_e$ = 200 × 20 = 4 kΩ.

$$\begin{gathered}Z_i=R_B\parallel r_\pi=\frac{5\times4}{5+4}\ \text{k}\Omega=2.22\ \text{k}\Omega \\
\text{(seen by the source: } R_s+Z_i=2.82\ \text{k}\Omega\text{)}
\end{gathered}$$

**Output impedance.** Looking back into the collector with v$_s$ = 0, i$_b$ = 0 and the dependent source is dead, so

$$Z_o=R_C\parallel r_o\approx R_C=2\ \text{k}\Omega$$

**Voltage gain.** The a.c. load is R$_C$ ∥ R$_L$ = 2 k ∥ 10 k = 1.667 kΩ. With v$_π$ = v$_i$ and v$_o$ = −g$_m$v$_π$(R$_C$ ∥ R$_L$), g$_m$ = 1/r$_e$ (taking α ≈ 1):

$$A_v=\frac{v_o}{v_i}=-\frac{R_C\parallel R_L}{r_e}=-\frac{1667}{20}=\boxed{-83.3}$$

(negative sign: 180° phase shift). Including the source resistance, the overall gain is

$$A_{vs}=\frac{v_o}{v_s}=A_v\,\frac{Z_i}{Z_i+R_s}=-83.3\times\frac{2222}{2822}=-65.6$$

and the current gain is A$_i$ = A$_v$Z$_i$/R$_L$ = −83.3 × 2.22 k/10 k = −18.5. *Remark:* the d.c. bias gives I$_E$ ≈ (5 − 0.7)/4.3 k = 1 mA, i.e. r$_e$ = 26 Ω; the value r$_e$ = 20 Ω given in the question has been used as instructed (with 26 Ω: Z$_i$ = 2.4 kΩ, A$_v$ = −64).

@s 5
**Construction.** The n-channel depletion-type MOSFET (D-MOSFET) is built on a lightly doped **p-type substrate**. Two heavily doped **n⁺ regions** form the source and the drain, and a thin **n-type channel is diffused between them during manufacture**, so a conducting channel already exists at V$_{GS}$ = 0. A very thin insulating layer of SiO$_2$ covers the channel and carries the **metal gate**, so the gate current is of the order of 10$^{-12}$ A (input resistance 10$^{10}$ to 10$^{15}$ Ω). The substrate is usually joined to the source.

```figure caption="n-channel depletion MOSFET: structure, transfer curve and drain characteristics."
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
fig=plt.figure(figsize=(7.4,2.8))
a=fig.add_axes([0.0,0.02,0.32,0.95]); a.set_xlim(0,12); a.set_ylim(0,9); a.axis('off')
a.add_patch(Rectangle((1,1.0),10,3.6,fc="#efe9dc",ec=INK,lw=1.2)); a.text(6,1.8,"p-type substrate",ha="center",fontsize=7.4)
a.add_patch(Rectangle((1.8,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1)); a.add_patch(Rectangle((8.0,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1))
a.text(2.9,4.0,"n+",ha="center",va="center",fontsize=8); a.text(9.1,4.0,"n+",ha="center",va="center",fontsize=8)
a.add_patch(Rectangle((4.0,3.4),4.0,1.2,fc="#9fc4ee",ec=INK,lw=0.6)); a.text(6,3.1,"built-in n channel",ha="center",va="center",fontsize=6.0)
a.add_patch(Rectangle((4.0,4.6),4.0,0.35,fc="#d9d9d9",ec=INK,lw=0.8)); a.text(8.3,4.78,"SiO$_2$",fontsize=6.2,va="center")
a.add_patch(Rectangle((4.2,4.95),3.6,0.7,fc="#b9b9b9",ec=INK,lw=1)); a.text(6,5.3,"metal gate",ha="center",va="center",fontsize=6.4)
for x,t in ((2.9,"S"),(9.1,"D"),(6,"G")):
    a.plot([x,x],[5.7 if t=="G" else 4.6,7.2],color=INK,lw=1.2); a.text(x,7.6,t,ha="center",fontsize=9)
b=fig.add_axes([0.40,0.18,0.25,0.72]); v=np.linspace(-5,2.0,200); b.plot(v,10*(1-v/(-4))**2*(v>=-4),color=INK,lw=1.4)
b.scatter([-4,0],[0,10],color=ACCENT,s=16,zorder=5); b.text(-3.9,0.8,"V$_P$",fontsize=7.4,color=ACCENT); b.text(0.1,8.6,"I$_{DSS}$",fontsize=7.4,color=ACCENT)
b.text(-4.6,12.6,"I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)$^2$",fontsize=6.8); b.axvline(0,color=MUTED,lw=0.6)
b.set_xlabel("V$_{GS}$ (V)",fontsize=8); b.set_ylabel("I$_D$ (mA)",fontsize=8); b.set_title("transfer curve",fontsize=8); b.set_ylim(0,15)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.74,0.18,0.25,0.72]); vds=np.linspace(0,12,300)
for vg,col in ((1,ACCENT),(0,INK),(-1,INK),(-2,INK),(-3,INK)):
    ids=10*(1+vg/4)**2; vk=vg+4
    c.plot(vds,np.where(vds<vk,ids*(2*vds/vk-(vds/vk)**2),ids),color=col,lw=1.0); c.text(12.1,ids,f"{vg} V",fontsize=6.4,va="center")
c.set_xlim(0,14); c.set_ylim(0,17); c.set_xlabel("V$_{DS}$ (V)",fontsize=8); c.set_ylabel("I$_D$ (mA)",fontsize=8); c.set_title("drain characteristics",fontsize=8)
c.text(5,15.6,"V$_{GS}$ > 0: enhancement mode",fontsize=6.0,color=ACCENT)
for s in ("top","right"): c.spines[s].set_visible(False)
```

**Operation.**

- **V$_{GS}$ = 0, V$_{DS}$ > 0:** electrons flow from source to drain through the built-in channel, giving I$_D$ = I$_{DSS}$.
- **V$_{GS}$ < 0 (depletion mode):** the negative gate repels electrons from the channel and attracts holes, so the channel is **depleted** of carriers, becomes narrower and I$_D$ decreases. At V$_{GS}$ = V$_P$ (the pinch-off voltage, a negative number) the channel is closed and I$_D$ ≈ 0.
- **V$_{GS}$ > 0 (enhancement mode):** the positive gate attracts more electrons into the channel, which widens it, and I$_D$ rises above I$_{DSS}$. (This is the feature that separates it from the JFET.)
- **Effect of V$_{DS}$:** for small V$_{DS}$ the device is an ohmic (triode) resistor controlled by V$_{GS}$; for V$_{DS}$ > V$_{GS}$ − V$_P$ the channel pinches off near the drain and I$_D$ saturates.

In saturation the transfer characteristic is the Shockley square law

$$\begin{gathered}I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2 \\ g_m=\frac{2I_{DSS}}{|V_P|}\left(1-\frac{V_{GS}}{V_P}\right)\end{gathered}$$

The symbol has a **solid** channel line (continuous channel) for the depletion type, against the broken line of the enhancement type.

@s 6
The gate current is zero, so the divider sets the gate voltage and the source resistor gives the feedback:

$$\begin{gathered}V_G=V_{DD}\frac{R_2}{R_1+R_2}=10\times\frac{10}{20}=5\ \text{V} \\
V_{GS}=V_G-I_DR_S=5-6I_D\qquad (I_D\text{ in mA, }R_S\text{ in k}\Omega)\\
I_D=K(V_{GS}-V_t)^2=0.5(5-6I_D-1)^2=0.5(4-6I_D)^2
\end{gathered}$$

Expand: I$_D$ = 0.5(16 − 48I$_D$ + 36I$_D^2$) gives

$$18I_D^2-25I_D+8=0\ \Rightarrow\ I_D=\frac{25\pm\sqrt{625-576}}{36}=\frac{25\pm7}{36}=0.889\ \text{mA or }0.5\ \text{mA}$$

For I$_D$ = 0.889 mA the gate-source voltage is V$_{GS}$ = 5 − 6(0.889) = −0.33 V, which is below V$_t$ (the device would be off), so this root is **rejected**. The valid root is

$$\begin{gathered}I_D=0.5\ \text{mA} \\
V_{GS}=5-6(0.5)=2\ \text{V}>V_t \\
V_{DS}=V_{DD}-I_D(R_D+R_S)=10-0.5(6+6)=4\ \text{V}
\end{gathered}$$

**Check of the region:** V$_{GS}$ − V$_t$ = 1 V < V$_{DS}$ = 4 V, so the MOSFET is in **saturation** and the square-law equation was applicable.

**Answer: I$_D$ = 0.5 mA, V$_{DS}$ = 4 V** (V$_{GS}$ = 2 V).

@s 7
**Properties of an ideal op-amp** (any four): (1) infinite open-loop voltage gain A$_{OL}$ = ∞; (2) infinite input impedance (zero input currents); (3) zero output impedance; (4) infinite bandwidth (flat gain from d.c. to any frequency); (5) infinite CMRR and PSRR; (6) zero input offset voltage and zero output when the inputs are equal (v$_1$ = v$_2$ gives v$_o$ = 0); (7) infinite slew rate and no noise or drift. Because A$_{OL}$ = ∞ with finite output, **v$_+$ = v$_−$** (virtual short) and i$_+$ = i$_−$ = 0.

**Design.** A single inverting summer gives only negative coefficients: v$_o$ = −R$_f$(V$_1$/R$_1$ + V$_2$/R$_2$ + V$_3$/R$_3$). Since V$_1$ and V$_3$ have positive weights and V$_2$ has a negative weight, use **two inverting stages**. Stage 1 sums V$_1$ and V$_3$ with inversion:

$$V_a=-R_f\left(\frac{V_1}{R_1}+\frac{V_3}{R_3}\right)=-(2V_1+5V_3)\ \Rightarrow\ \frac{R_f}{R_1}=2,\ \frac{R_f}{R_3}=5$$

Take R$_f$ = 10 kΩ, so R$_1$ = 5 kΩ and R$_3$ = 2 kΩ. Stage 2 sums V$_a$ (weight 1) and V$_2$ (weight 4) with inversion:

$$V_o=-R_f\left(\frac{V_a}{R_a}+\frac{V_2}{R_2}\right)=-(V_a+4V_2)=2V_1-4V_2+5V_3$$

with R$_a$ = 10 kΩ and R$_2$ = R$_f$/4 = 2.5 kΩ.

```figure caption="Summing amplifier for V$_o$ = 2V$_1$ − 4V$_2$ + 5V$_3$ (two inverting stages, R$_f$ = 10 kΩ)."
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
fig,ax=ckt_canvas(7.0,2.7,xlim=(-1.8,14.4),ylim=(0.6,6.4))
o1=opamp(ax,3.4,3.0,2.2,2.0,"A$_1$")
terminal(ax,(-0.5,4.6)); label(ax,(-0.8,4.6),"V$_1$",ha="right",size=8.4); wire(ax,[(-0.5,4.6),(0.4,4.6)]); res(ax,(0.4,4.6),(1.8,4.6),"5 kΩ",side=1,off=0.35)
terminal(ax,(-0.5,3.5)); label(ax,(-0.8,3.5),"V$_3$",ha="right",size=8.4); wire(ax,[(-0.5,3.5),(0.4,3.5)]); res(ax,(0.4,3.5),(1.8,3.5),"2 kΩ",side=-1,off=0.35)
wire(ax,[(1.8,4.6),(2.6,4.6),(2.6,3.5)]); wire(ax,[(1.8,3.5),(3.4,3.5)]); node(ax,(2.6,3.5))
wire(ax,[(2.6,4.6),(2.6,5.6),(3.2,5.6)]); res(ax,(3.2,5.6),(5.0,5.6),"10 kΩ",side=1,off=0.35); wire(ax,[(5.0,5.6),(6.2,5.6),(6.2,3.0)])
wire(ax,[(3.4,2.5),(3.0,2.5),(3.0,1.6)]); gnd(ax,(3.0,1.6))
wire(ax,[o1["out"],(6.2,3.0)]); node(ax,(6.2,3.0)); wire(ax,[(6.2,3.0),(6.8,3.0),(6.8,3.5)]); label(ax,(5.9,2.45),"V$_a$",size=8,ha="center")
res(ax,(6.8,3.5),(8.0,3.5),"10 kΩ",side=1,off=0.35,body=0.9); wire(ax,[(8.0,3.5),(9.4,3.5)]); node(ax,(8.6,3.5))
terminal(ax,(6.0,2.2)); label(ax,(5.7,2.2),"V$_2$",ha="right",size=8.4) if False else None
wire(ax,[(6.0,2.2),(6.8,2.2)]); res(ax,(6.8,2.2),(8.0,2.2),"2.5 kΩ",side=-1,off=0.35,body=0.9); wire(ax,[(8.0,2.2),(8.6,2.2),(8.6,3.5)])
label(ax,(6.0,1.8),"V$_2$",size=8.4)
wire(ax,[(8.6,3.5),(8.6,5.6),(9.2,5.6)]); res(ax,(9.2,5.6),(11.0,5.6),"10 kΩ",side=1,off=0.35); wire(ax,[(11.0,5.6),(12.2,5.6),(12.2,3.0)])
o2=opamp(ax,9.4,3.0,2.2,2.0,"A$_2$")
wire(ax,[(9.4,2.5),(9.0,2.5),(9.0,1.6)]); gnd(ax,(9.0,1.6))
wire(ax,[o2["out"],(12.2,3.0)]); node(ax,(12.2,3.0)); wire(ax,[(12.2,3.0),(13.2,3.0)]); terminal(ax,(13.2,3.0)); label(ax,(13.5,3.0),"V$_o$",ha="left",size=8.4)
```

**Check:** V$_1$ = V$_2$ = V$_3$ = 1 V gives V$_a$ = −7 V and V$_o$ = −(−7 + 4) = 3 V = 2 − 4 + 5. For bias-current balance a resistor equal to the parallel of the input resistors of that stage (5 k ∥ 2 k ∥ 10 k = 1.25 kΩ and 10 k ∥ 2.5 k ∥ 10 k = 1.25 kΩ) can be placed from each non-inverting input to ground.

@s 8
**Wien bridge oscillator.** An op-amp (non-inverting amplifier of gain A = 1 + R$_f$/R$_1$) is combined with a **lead-lag network**: a series R–C branch (Z$_s$) and a parallel R–C branch (Z$_p$). The lead-lag network is the positive-feedback path and the divider R$_f$, R$_1$ is the negative-feedback path that sets the gain. The two arms form a bridge, so the circuit is called a Wien bridge.

```figure caption="Wien bridge oscillator."
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
fig,ax=ckt_canvas(5.4,3.6,xlim=(-2.2,9.4),ylim=(0.3,6.2))
o=opamp(ax,4.0,3.6,2.4,2.4,"")
out=o["out"]; inv=o["inv"]; non=o["non"]
wire(ax,[out,(7.2,out[1])]); node(ax,(7.2,out[1])); wire(ax,[(7.2,out[1]),(8.2,out[1])]); terminal(ax,(8.2,out[1])); label(ax,(8.5,out[1]),"v$_o$",ha="left",size=8.4)
wire(ax,[inv,(2.8,inv[1])]); node(ax,(2.8,inv[1]))
wire(ax,[(7.2,out[1]),(7.2,5.4),(6.4,5.4)]); res(ax,(6.4,5.4),(4.2,5.4),"R$_f$",side=1,off=0.35,body=1.2); wire(ax,[(4.2,5.4),(2.8,5.4),(2.8,inv[1])])
wire(ax,[(2.8,inv[1]),(1.8,inv[1])]); res(ax,(1.8,inv[1]),(0.4,inv[1]),"R$_1$",side=1,off=0.35,body=0.9); gnd(ax,(0.4,inv[1]))
wire(ax,[non,(2.0,non[1])]); node(ax,(2.0,non[1]))
wire(ax,[(7.2,out[1]),(7.2,1.0),(6.4,1.0)]); res(ax,(6.4,1.0),(4.9,1.0),"R",side=1,off=0.35,body=1.0); wire(ax,[(4.9,1.0),(4.4,1.0)]); cap(ax,(4.4,1.0),(3.4,1.0),"C",side=1,off=0.5); wire(ax,[(3.4,1.0),(2.0,1.0),(2.0,non[1])])
wire(ax,[(2.0,non[1]),(0.6,non[1])]); node(ax,(0.6,non[1])); res(ax,(0.6,non[1]),(0.6,1.5),"R",side=-1,off=0.3,body=0.8); gnd(ax,(0.6,1.5))
wire(ax,[(0.6,non[1]),(-0.8,non[1])]); cap(ax,(-0.8,non[1]),(-0.8,1.5),"C",side=-1,off=0.5); gnd(ax,(-0.8,1.5))
label(ax,(5.6,0.55),"series R–C branch (Z$_s$)",size=7,color=MUTED); label(ax,(-0.1,0.9),"parallel R–C (Z$_p$)",size=7,color=MUTED,ha="center") if False else None
```

The feedback factor of the lead-lag network (output of the op-amp to the non-inverting input):

$$\begin{gathered}Z_s=R+\frac{1}{j\omega C},\qquad Z_p=\frac{R}{1+j\omega RC} \\
\beta=\frac{Z_p}{Z_s+Z_p}=\frac{1}{3+j\left(\omega RC-\dfrac{1}{\omega RC}\right)}
\end{gathered}$$

The Barkhausen condition requires the loop gain Aβ to be real and equal to 1. The loop phase is zero only if the imaginary part of the denominator vanishes:

$$\omega RC-\frac{1}{\omega RC}=0\ \Rightarrow\ \omega_o=\frac{1}{RC}\quad\Rightarrow\quad\boxed{\ f_o=\frac{1}{2\pi RC}\ }$$

At this frequency β = 1/3 with no phase shift, so oscillations are sustained when A = 3, i.e. **R$_f$ = 2R$_1$** (in practice a slightly larger gain, with a lamp or a diode network to stabilise the amplitude). If the two branches are different, f$_o$ = 1/(2π√(R$_1$R$_2$C$_1$C$_2$)). *Example:* R = 10 kΩ and C = 10 nF give f$_o$ = 1.59 kHz.

@s 9
**Circuit.** The series-fed class A amplifier has the load R$_L$ in series with the collector and the bias resistor R$_B$ from V$_{CC}$ to the base. All the d.c. collector current flows through the load, so the load is also the d.c. load. Q-point at the centre of the load line: V$_{CEQ}$ = V$_{CC}$/2 and I$_{CQ}$ = V$_{CC}$/(2R$_L$).

```figure caption="Series-fed class A amplifier and its load line."
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
fig=plt.figure(figsize=(7.2,2.9))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-1.2,6.2); ax.set_ylim(-0.4,7.8); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.6,7.0),(3.8,7.0)]); terminal(ax,(5.0,7.0)); wire(ax,[(3.8,7.0),(5.0,7.0)]); label(ax,(5.0,7.45),"+V$_{CC}$",size=8)
res(ax,(1.6,7.0),(1.6,4.6),"R$_B$",side=-1,off=0.2); wire(ax,[(1.6,4.6),(1.6,3.8)]); node(ax,(1.6,3.8))
bj=bjt(ax,3.2,3.8); wire(ax,[(1.6,3.8),bj["B"]])
res(ax,(3.8,7.0),(3.8,5.4),"R$_L$ (load)",side=1,off=0.2); wire(ax,[(3.8,5.4),bj["C"]])
wire(ax,[bj["E"],(3.8,1.6)]); gnd(ax,(3.8,1.6))
wire(ax,[(1.6,3.8),(0.9,3.8)]); cap(ax,(0.9,3.8),(0.1,3.8)); wire(ax,[(0.1,3.8),(-0.5,3.8)]); terminal(ax,(-0.5,3.8)); label(ax,(-0.5,4.3),"v$_i$",size=8.4)
b=fig.add_axes([0.56,0.22,0.41,0.70]); vcc=1.0
b.plot([0,2*vcc],[2*0.5*1.0*1.0,0],color=INK,lw=1.4) if False else None
b.plot([0,vcc],[1.0,0],color=INK,lw=1.6); b.scatter([vcc/2],[0.5],color=ACCENT,zorder=5,s=22)
b.text(vcc/2+0.04,0.56,"Q",color=ACCENT,fontsize=8); b.plot([vcc/2,vcc/2],[0,0.5],color=ACCENT,lw=0.8,ls=":"); b.plot([0,vcc/2],[0.5,0.5],color=ACCENT,lw=0.8,ls=":")
b.set_xticks([0,vcc/2,vcc]); b.set_xticklabels(["0","V$_{CC}$/2","V$_{CC}$"],fontsize=8); b.set_yticks([0,0.5,1.0]); b.set_yticklabels(["0","I$_{CQ}$ = V$_{CC}$/2R$_L$","V$_{CC}$/R$_L$"],fontsize=7)
b.set_xlabel("v$_{CE}$",fontsize=8); b.set_ylabel("i$_C$",fontsize=8); b.set_title("d.c. = a.c. load line, Q at the centre",fontsize=7.6); b.set_xlim(0,1.08); b.set_ylim(0,1.12)
for s in ("top","right"): b.spines[s].set_visible(False)
```

**Power drawn from the supply** (signal independent):

$$P_{dc}=V_{CC}I_{CQ}=\frac{V_{CC}^2}{2R_L}$$

**Maximum signal power.** The largest undistorted swing about Q is V$_{CE}$ from 0 to V$_{CC}$, so the peak output voltage is V$_p$ = V$_{CC}$/2 and the peak current is I$_p$ = I$_{CQ}$ = V$_{CC}$/(2R$_L$):

$$P_{ac(max)}=\frac{V_pI_p}{2}=\frac{1}{2}\cdot\frac{V_{CC}}{2}\cdot\frac{V_{CC}}{2R_L}=\frac{V_{CC}^2}{8R_L}$$

**Efficiency:**

$$\eta_{max}=\frac{P_{ac(max)}}{P_{dc}}=\frac{V_{CC}^2/8R_L}{V_{CC}^2/2R_L}=\frac14=\boxed{25\ \text{percent}}$$

For a smaller swing, η = 25 percent × (V$_p$/(V$_{CC}$/2))$^2$. At no signal the whole P$_{dc}$ is dissipated in the transistor (and load), which is the weakness of the class A series-fed stage. *Example:* V$_{CC}$ = 12 V, R$_L$ = 8 Ω: P$_{dc}$ = 9 W, P$_{ac(max)}$ = 2.25 W, of the 9 W drawn, 2.25 W is useful output and the other 6.75 W is lost as heat in the load and the transistor (at zero signal all 9 W is heat: 4.5 W in the transistor and 4.5 W in R$_L$).

@s 10
**Class A tuned amplifier (single tuned).** A CE amplifier has a parallel LC tank (L with its series resistance, C) as the collector load. At resonance the tank impedance is a pure and large resistance, so the gain is maximum; away from resonance the tank impedance falls, so the amplifier is selective (used in radio and IF amplifiers).


```figure caption="Class A tuned amplifier and its frequency response."
fig=plt.figure(figsize=(7.2,3.0))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-0.6,7.4); ax.set_ylim(-1.0,8.0); ax.set_aspect('equal'); ax.axis('off')
bj=bjt(ax,2.6,2.4)
wire(ax,[bj["C"],(3.2,4.6)]); node(ax,(3.2,4.6))
wire(ax,[(2.2,4.6),(4.2,4.6)]); wire(ax,[(2.2,6.2),(4.2,6.2)]); node(ax,(3.2,6.2))
ind(ax,(2.2,6.2),(2.2,4.6),"L",side=-1,body=1.1,off=0.45); cap(ax,(4.2,6.2),(4.2,4.6),"C",side=1,off=0.45)
wire(ax,[(3.2,6.2),(3.2,7.2)]); terminal(ax,(3.2,7.2)); label(ax,(3.2,7.6),"+V$_{CC}$",size=8)
wire(ax,[(4.2,4.6),(5.4,4.6)]); terminal(ax,(5.4,4.6)); label(ax,(5.9,4.6),"v$_o$",ha="left",size=8.6)
wire(ax,[bj["B"],(0.4,2.4)]); terminal(ax,(0.4,2.4)); label(ax,(0.0,2.4),"v$_i$",ha="right",size=8.4)
wire(ax,[bj["E"],(3.2,0.5)]); res(ax,(3.2,0.5),(3.2,-0.8),"R$_E$",side=1,off=0.5,body=0.5); gnd(ax,(3.2,-0.8))
b=fig.add_axes([0.56,0.2,0.42,0.7]); f=np.linspace(0.6,1.4,400); Q=8; A=1/np.sqrt(1+(Q*(f-1/f))**2)
b.plot(f,A,color=INK,lw=1.6); b.axhline(0.7071,color=ACCENT,lw=0.8,ls="--"); b.text(0.62,0.74,"A$_{max}$/√2 (−3 dB)",fontsize=7,color=ACCENT)
f1=(-1/(2*Q)+np.sqrt(1/(2*Q)**2+1)); f2=(1/(2*Q)+np.sqrt(1/(2*Q)**2+1))
b.plot([f1,f1],[0,0.7071],color=ACCENT,lw=0.8,ls=":"); b.plot([f2,f2],[0,0.7071],color=ACCENT,lw=0.8,ls=":")
b.annotate("",xy=(f1,0.3),xytext=(f2,0.3),arrowprops=dict(arrowstyle="<->",lw=0.9)); b.text(1.0,0.34,"BW = f$_2$ − f$_1$",ha="center",fontsize=7.4)
b.set_xticks([f1,1,f2]); b.set_xticklabels(["f$_1$","f$_o$","f$_2$"],fontsize=8); b.set_yticks([1]); b.set_yticklabels(["A$_{max}$"],fontsize=8); b.set_xlabel("frequency",fontsize=8); b.set_ylabel("voltage gain",fontsize=8)
for s in ("top","right"): b.spines[s].set_visible(False)
```


Resonance frequency f$_o$ = 1/(2π√(LC)). Near resonance the tank impedance is

$$\begin{gathered}Z(f)=\frac{R_p}{1+jQ\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)} \\ Q=\frac{R_p}{\omega_oL}=\omega_oCR_p\end{gathered}$$

where R$_p$ is the equivalent parallel resistance (the coil loss resistance in parallel with r$_o$ and the load). With a transconductance g$_m$ the voltage gain is A$_v$ = −g$_m$Z, so

$$\begin{gathered}|A_v|=\frac{A_{max}}{\sqrt{1+Q^2\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)^2}} \\ A_{max}=g_mR_p\end{gathered}$$

**3 dB bandwidth.** The gain drops to A$_{max}$/√2 when Q(f/f$_o$ − f$_o$/f) = ±1. Solving the two quadratics f² ∓ (f$_o$/Q)f − f$_o^2$ = 0 for the positive roots:

$$\begin{gathered}f_{1,2}=f_o\left[\sqrt{1+\frac{1}{4Q^2}}\mp\frac{1}{2Q}\right]\ \Rightarrow\ f_2-f_1=\frac{f_o}{Q} \\ f_1f_2=f_o^2\end{gathered}$$

$$\boxed{\ BW=f_2-f_1=\frac{f_o}{Q}\ }$$

so a higher Q gives a narrower bandwidth and a sharper response (for Q > 10, f$_{1,2}$ ≈ f$_o$ ∓ BW/2). *Example:* f$_o$ = 1 MHz, Q = 50 gives BW = 20 kHz; with a heavy load, R$_p$ and hence Q fall and the bandwidth rises.


@s 11
The Zener is assumed to conduct (breakdown). Check: if it were removed, the load voltage would be 18 × 1.2/(0.1 + 1.2) = 16.6 V, which is greater than V$_Z$ = 10 V, so the Zener **is in breakdown** and V$_o$ = V$_Z$ = 10 V.

$$\begin{gathered}I_S=\frac{V_S-V_Z}{R}=\frac{18-10}{100}=80\ \text{mA} \\
I_L=\frac{V_Z}{R_L}=\frac{10}{1.2\ \text{k}\Omega}=8.33\ \text{mA} \\
I_Z=I_S-I_L=80-8.33=\boxed{71.7\ \text{mA}}
\end{gathered}$$

The Zener dissipates P$_Z$ = V$_Z$I$_Z$ = 10 × 71.7 mA = 0.717 W, so a Zener of at least 1 W rating is needed.

@s 12
**Circuit.** The series regulator has a **pass transistor Q$_1$** (emitter follower) in series with the load, a **Zener reference D$_Z$** (biased by R from V$_{in}$) at its base, and a small **sensing resistor R$_{sc}$** in series with the output. A second transistor Q$_2$ with its base-emitter junction across R$_{sc}$ and its collector at the base of Q$_1$ provides the **current limit**.

```figure caption="Series voltage regulator with current-limiting transistor Q$_2$ and sense resistor R$_{sc}$."
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
fig,ax=ckt_canvas(5.6,3.7,xlim=(-1.0,9.8),ylim=(-0.4,7.2))
terminal(ax,(0.0,6.4)); label(ax,(-0.3,6.4),"V$_{in}$",ha="right",size=8.4)
wire(ax,[(0.0,6.4),(4.2,6.4),(4.2,5.3)]); node(ax,(1.6,6.4))
q1=bjt(ax,3.6,4.2); label(ax,(5.5,4.7),"Q$_1$ (pass)",ha="left",size=7.6)
res(ax,(1.6,6.4),(1.6,4.8),"R",side=-1,off=0.2,body=0.9); wire(ax,[(1.6,4.8),(1.6,4.2),q1["B"]]); node(ax,(1.6,4.2))
wire(ax,[(1.6,4.2),(1.6,3.9)]); diode(ax,(1.6,1.0),(1.6,3.9),"D$_Z$",side=-1,off=0.5,zener=True); gnd(ax,(1.6,1.0))
wire(ax,[q1["E"],(4.2,2.6),(4.8,2.6)]); node(ax,(4.8,2.6)); res(ax,(4.8,2.6),(7.2,2.6),"R$_{sc}$",side=-1,off=0.5,body=1.4)
q2=bjt(ax,6.6,3.7); label(ax,(8.0,4.9),"Q$_2$ (limiter)",ha="left",size=7.6)
wire(ax,[(4.8,2.6),(4.8,3.7),q2["B"]]); wire(ax,[q2["E"],(7.2,2.6)]); node(ax,(7.2,2.6))
wire(ax,[q2["C"],(7.2,5.9),(2.4,5.9),(2.4,4.2)]); node(ax,(2.4,4.2))
wire(ax,[(7.2,2.6),(8.2,2.6)]); node(ax,(8.2,2.6)); wire(ax,[(8.2,2.6),(9.2,2.6)]); terminal(ax,(9.2,2.6)); label(ax,(9.2,3.1),"V$_o$",size=8.4)
wire(ax,[(8.2,2.6),(8.2,2.2)]); res(ax,(8.2,2.2),(8.2,0.6),"R$_L$",side=-1,off=0.5,body=0.9); gnd(ax,(8.2,0.6))
```

**Regulation.** The Zener holds the base of Q$_1$ at V$_Z$, so V$_o$ = V$_Z$ − V$_{BE1}$ − I$_L$R$_{sc}$ ≈ V$_Z$ − 0.7 V. If V$_{in}$ rises, the extra voltage is dropped across Q$_1$ (V$_{CE1}$ increases) and V$_o$ stays constant. If the load current rises and V$_o$ tends to fall, V$_{BE1}$ increases, so Q$_1$ conducts harder and restores V$_o$ (negative feedback). The line and load regulation are good because the Zener current is nearly constant, and the base current of Q$_1$ is only I$_L$/(β+1).

**Current limiting.** The load current flows through R$_{sc}$ and produces V$_{sc}$ = I$_L$R$_{sc}$, which is the base-emitter voltage of Q$_2$. While V$_{sc}$ < 0.6 V, Q$_2$ is off and plays no part. When the load current reaches

$$I_{L(max)}=\frac{V_{BE2}}{R_{sc}}\approx\frac{0.65\ \text{V}}{R_{sc}}$$

Q$_2$ turns on and **diverts the base current of Q$_1$ to ground** through its collector, so Q$_1$ conducts less and the output current cannot rise further (short-circuit protection). *Example:* R$_{sc}$ = 0.65 Ω limits the output to about 1 A. The price paid is a voltage drop of about 0.65 V in R$_{sc}$ at full load and the power dissipated in Q$_1$ during a short circuit, (V$_{in}$ − 0)·I$_{L(max)}$, so a heat sink is needed.
