---
file: NEBians-IOE-Past-Paper-Data-Communication-ENCT253-2083-Baishakh.pdf
subject: Data Communication
level: BE · Year II / Part II
code: ENCT 253
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define any six performance/impairment parameters common in digital data communication. [[3]]

b) Using a suitable generic real-world example of a digital communication system, explain its functioning in full-duplex mode. [[4]]

@q 2
a) With suitable examples, explain how linearity of a system is checked. [[5]]

b) Mention the conditions and properties of Fourier transformation. [[4]]

@q 3
a) Compare coaxial cable, twisted pair, and optical fiber based on bandwidth, cost, and use case. [[2]]

b) Encode "Solve {(a+b)(a-b)}²." using Shannon-Fano Encoder, and find the transmission efficiency. [[5+2]]

c) Using any example of a 3×3 generation matrix, demonstrate how LBC corrects a single bit error. [[5]]

@q 4
a) Draw the waveform for the bit sequence 1000000101 using each one suitable unipolar, polar and bipolar encoders. [[6]]

b) Compare single tone-AM with that of double-tone with basic mathematical formulations and performance parameters. [[5]]

c) Describe ASK, PSK and FSK with signal diagrams. [[3]]

@q 5
a) Compare digital and analog hierarchies with detailed block diagram showing number of channels and data-rate. [[4]]

b) Demonstrate the operation of CDMA for 8 users among whom three users are sending bit 1, three users are sending bit 0 and remaining two are silent. [[4]]

@q 6
Write short notes on (Any Two): [[2×4]]

a) Evolution of mobile communication technologies from 1G to 5G

b) Checksum

c) LAN vs MAN

d) Packet switching vs circuit switching

<!-- SOLUTIONS -->

@s 1
**(a) Performance and impairment parameters.**

| Parameter | Definition | Measure / formula |
|---|---|---|
| **Bandwidth** | the range of frequencies the channel passes (or the signal occupies); it limits the data rate | $B = f_{max} - f_{min}$ in Hz |
| **Data rate (throughput)** | bits per second actually delivered; limited by bandwidth and SNR | Nyquist: $C = 2B\log_2 M$; Shannon: $C = B\log_2(1 + \mathrm{SNR})$ |
| **Attenuation** | loss of signal strength with distance in the medium; high frequencies lose more | $\mathrm{dB} = 10\log_{10}(P_1/P_2)$; repeaters or amplifiers restore it |
| **Distortion** | change of the signal shape because frequency components travel at different speeds (delay distortion) or are attenuated unequally | equalizers correct it |
| **Noise** | unwanted signals added in transit: thermal, crosstalk, impulse, intermodulation | $\mathrm{SNR_{dB}} = 10\log_{10}(P_{signal}/P_{noise})$ |
| **Bit error rate (BER)** | fraction of received bits that are wrong | $\mathrm{BER} = N_{error}/N_{total}$ |
| **Latency (delay)** | time for a bit to cross the link: propagation, transmission, queueing, processing | $d/v + L/R$ |
| **Jitter** | variation of the delay between packets (matters for voice and video) | std. deviation of the delay |

(Any six of these are enough; they are the impairments that decide how reliably and how fast data are carried.)

**(b) Full-duplex example: a digital mobile / VoIP voice call.** Both users speak and listen at the same time.

```figure caption="Full-duplex digital voice link: the transmit chain and the receive chain of a station work simultaneously on two separate channels."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.2)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(0,8.6)
ax.text(7.5,8.2,"Digital voice call (mobile phone / VoIP): full duplex, both directions at the same time",ha="center",fontsize=8,weight="bold")
names=["Microphone\n(analog voice)","ADC + speech\nencoder (codec)","Channel\nencoder","Modulator\n+ transmitter"]
for i,n in enumerate(names): box(ax,1.2+i*2.35,6.4,2.0,1.2,n,fs=6.3,fc=BLUE)
for i in range(3): arr(ax,(2.25+i*2.35,6.4),(2.55+i*2.35,6.4),c=ACCENT)
box(ax,12.0,6.4,2.2,1.2,"Radio channel 1\n(uplink, f1)",fs=6.8,fc=YEL); arr(ax,(9.3,6.4),(10.85,6.4),c=ACCENT)
box(ax,12.0,4.0,2.2,1.2,"Radio channel 2\n(downlink, f2)",fs=6.8,fc=YEL)
names2=["Speaker\n(analog voice)","DAC + speech\ndecoder","Channel\ndecoder","Demodulator\n+ receiver"]
for i,n in enumerate(names2): box(ax,1.2+i*2.35,4.0,2.0,1.2,n,fs=6.3,fc=GRN)
for i in range(3): arr(ax,(2.55+i*2.35,4.0),(2.25+i*2.35,4.0),c="#2e7d32")
arr(ax,(10.85,4.0),(9.3,4.0),c="#2e7d32")
arr(ax,(12.0,5.8),(12.0,4.6),c=INK,style="<|-|>",lw=0.0)
ax.text(5.0,2.7,"Station A (left half) talks to station B through channel 1 and, at the same time,",ha="center",fontsize=7)
ax.text(5.0,2.2,"listens to station B through channel 2 (the same two chains exist in B in mirror image).",ha="center",fontsize=7)
ax.text(5.0,1.5,"Separation of the two directions: FDD (different frequencies f1, f2) or two wire pairs / echo cancellation.",ha="center",fontsize=7)
ax.text(5.0,0.8,"Top chain = transmit path of A, bottom chain = receive path of A.",ha="center",fontsize=7,color="#555")
```


*Operation (station A to station B):* the microphone gives an analog voice signal → the ADC samples it (8 kHz) and the codec compresses it into a digital bit stream (source coding) → the channel encoder adds error-control bits → the modulator and radio transmitter send it on the **uplink** frequency f1 → the channel adds attenuation, noise and distortion → the receiver of B demodulates, the channel decoder corrects errors, the codec decodes and the DAC and loudspeaker reproduce the voice.

*At the same time* B's transmit chain uses the **downlink** frequency f2 (frequency-division duplex, FDD) so A hears B. Because the two directions use different channels (or different wire pairs, or echo cancellation as in a telephone hybrid), the two flows never collide; each station has its own transmitter **and** receiver active together. Half duplex (a walkie-talkie) would use a single channel and a push-to-talk switch.

@s 2
**(a) Checking linearity.** A system $y = T[x]$ is **linear** if it obeys **superposition**, which combines two properties for all inputs $x_1, x_2$ and constants $a, b$:

- additivity: $T[x_1 + x_2] = T[x_1] + T[x_2]$;
- homogeneity (scaling): $T[a\,x] = a\,T[x]$;

that is, $T[a x_1 + b x_2] = a\,T[x_1] + b\,T[x_2]$.

*Procedure:* (1) apply $x_1$ and $x_2$ separately and note $y_1, y_2$; (2) apply $a x_1 + b x_2$ and find the output; (3) compare with $a y_1 + b y_2$. Equal for all inputs means linear; one counter-example is enough to prove non-linear. (Quick check: a linear system gives zero output for zero input.)

| System | $T[ax_1 + bx_2]$ | $aT[x_1] + bT[x_2]$ | Result |
|---|---|---|---|
| $y = 3x$ | $3(ax_1 + bx_2)$ | $3a x_1 + 3b x_2$ | equal: **linear** |
| $y = \dfrac{dx}{dt}$ | $a x_1' + b x_2'$ | $a x_1' + b x_2'$ | equal: **linear** |
| $y = x^2$ | $a^2x_1^2 + 2ab\,x_1x_2 + b^2x_2^2$ | $a x_1^2 + b x_2^2$ | different: **non-linear** |
| $y = 2x + 5$ | $2ax_1 + 2bx_2 + 5$ | $2ax_1 + 2bx_2 + 5(a+b)$ | different (output $5 \ne 0$ for $x = 0$): **non-linear** |
| $y = \lvert x \rvert$ | | | $x_1 = 1,\ x_2 = -1,\ a = b = 1$: $\lvert 0 \rvert = 0$ but $1 + 1 = 2$: **non-linear** |

*Numerical check for $y = x^2 + x$:* take $x_1 = 1,\ x_2 = 2,\ a = b = 1$. $y_1 = 2,\ y_2 = 6$ so $y_1 + y_2 = 8$; but $T[x_1 + x_2] = T[3] = 9 + 3 = 12 \ne 8$: not linear.

**(b) Fourier transform: conditions and properties.** The Fourier transform of $x(t)$ is $X(f) = \displaystyle\int_{-\infty}^{\infty} x(t)\,e^{-j2\pi ft}\,dt$, and the inverse is $x(t) = \displaystyle\int_{-\infty}^{\infty} X(f)\,e^{j2\pi ft}\,df$.

*Conditions (Dirichlet, sufficient):* (1) $x(t)$ is absolutely integrable, $\int |x(t)|\,dt < \infty$; (2) it has a finite number of maxima and minima in any finite interval; (3) it has a finite number of finite discontinuities in any finite interval. (Power signals such as the sinusoid and the unit step have transforms only in the generalized sense, with impulses.)

| Property | Time domain | Frequency domain |
|---|---|---|
| Linearity | $a x_1(t) + b x_2(t)$ | $a X_1(f) + b X_2(f)$ |
| Time shift | $x(t - t_0)$ | $X(f)\,e^{-j2\pi f t_0}$ |
| Frequency shift (modulation) | $x(t)\,e^{j2\pi f_0 t}$ | $X(f - f_0)$ |
| Scaling | $x(at)$ | $\dfrac{1}{\lvert a \rvert}X\!\left(\dfrac{f}{a}\right)$ |
| Time reversal | $x(-t)$ | $X(-f)$ |
| Duality | $X(t)$ | $x(-f)$ |
| Convolution | $x_1(t) * x_2(t)$ | $X_1(f)\,X_2(f)$ |
| Multiplication | $x_1(t)\,x_2(t)$ | $X_1(f) * X_2(f)$ |
| Differentiation | $\dfrac{dx}{dt}$ | $j2\pi f\,X(f)$ |
| Integration | $\int_{-\infty}^{t} x\,d\tau$ | $\dfrac{X(f)}{j2\pi f} + \tfrac{1}{2}X(0)\delta(f)$ |
| Conjugate symmetry (real $x$) | $x(t)$ real | $X(-f) = X^*(f)$: $\lvert X \rvert$ even, phase odd |
| Parseval (energy) | $\int \lvert x \rvert^2 dt$ | $\int \lvert X(f) \rvert^2 df$ |

Useful pairs: $\delta(t) \leftrightarrow 1$; $1 \leftrightarrow \delta(f)$; $\mathrm{rect}(t/T) \leftrightarrow T\,\mathrm{sinc}(fT)$; $\cos 2\pi f_0 t \leftrightarrow \tfrac12[\delta(f - f_0) + \delta(f + f_0)]$.

@s 3
**(a) Transmission media.**

| Basis | Twisted pair (UTP, Cat 5e/6) | Coaxial cable | Optical fiber |
|---|---|---|---|
| Bandwidth / data rate | low: about 100 Mbit/s to 10 Gbit/s over 100 m (up to about 250 MHz) | medium: up to about 1 GHz (hundreds of Mbit/s to Gbit/s) | very high: tens of THz, 10 Gbit/s to Tbit/s |
| Cost | cheapest | medium | highest (cable, connectors, optical equipment), falling |
| Immunity / loss | sensitive to noise and crosstalk, short range | shielded, better immunity, medium loss | immune to EMI, lowest attenuation (0.2 dB/km), no tapping |
| Use case | telephone lines, LAN (Ethernet) to desks | cable TV, broadband (DOCSIS), antenna feeders | backbone, long haul, FTTH, undersea links |

**(b) Shannon-Fano coding of "Solve {(a+b)(a-b)}²."** The message has $N = 20$ symbols (every character, including the space, the braces and the superscript 2 counted as one symbol).

*Step 1.* Count the symbols and sort them in decreasing order of probability. *Step 2.* Divide the list into two groups with total probabilities as nearly equal as possible, give 0 to the upper and 1 to the lower group; repeat inside every group until each group has one symbol.

| Level | Upper group (bit 0) | Lower group (bit 1) |
|---|---|---|
| 1 | `( a b ) S o` (total 10) | `l v e ␣ { + - } ² .` (total 10) |
| 2 | `( a` (total 4) | `b ) S o` (total 6) |
| 3 | `(` (total 2) | `a` (total 2) |
| 3 | `b` (total 2) | `) S o` (total 4) |
| 4 | `)` (total 2) | `S o` (total 2) |
| 5 | `S` (total 1) | `o` (total 1) |
| 2 | `l v e ␣ {` (total 5) | `+ - } ² .` (total 5) |
| 3 | `l v` (total 2) | `e ␣ {` (total 3) |
| 4 | `l` (total 1) | `v` (total 1) |
| 4 | `e` (total 1) | `␣ {` (total 2) |
| 5 | `␣` (total 1) | `{` (total 1) |
| 3 | `+ -` (total 2) | `} ² .` (total 3) |
| 4 | `+` (total 1) | `-` (total 1) |
| 4 | `}` (total 1) | `² .` (total 2) |
| 5 | `²` (total 1) | `.` (total 1) |

(`␣` is the space; where several symbols have the same count they are kept in order of their appearance.)

| Symbol | Count $n_i$ | $p_i$ | $-\log_2 p_i$ | Code | Length $l_i$ | $p_i l_i$ |
|---|---|---|---|---|---|---|
| `(` | 2 | 2/20 = 0.1000 | 3.322 | `000` | 3 | 0.3000 |
| `a` | 2 | 2/20 = 0.1000 | 3.322 | `001` | 3 | 0.3000 |
| `b` | 2 | 2/20 = 0.1000 | 3.322 | `010` | 3 | 0.3000 |
| `)` | 2 | 2/20 = 0.1000 | 3.322 | `0110` | 4 | 0.4000 |
| `S` | 1 | 1/20 = 0.0500 | 4.322 | `01110` | 5 | 0.2500 |
| `o` | 1 | 1/20 = 0.0500 | 4.322 | `01111` | 5 | 0.2500 |
| `l` | 1 | 1/20 = 0.0500 | 4.322 | `1000` | 4 | 0.2000 |
| `v` | 1 | 1/20 = 0.0500 | 4.322 | `1001` | 4 | 0.2000 |
| `e` | 1 | 1/20 = 0.0500 | 4.322 | `1010` | 4 | 0.2000 |
| `␣` | 1 | 1/20 = 0.0500 | 4.322 | `10110` | 5 | 0.2500 |
| `{` | 1 | 1/20 = 0.0500 | 4.322 | `10111` | 5 | 0.2500 |
| `+` | 1 | 1/20 = 0.0500 | 4.322 | `1100` | 4 | 0.2000 |
| `-` | 1 | 1/20 = 0.0500 | 4.322 | `1101` | 4 | 0.2000 |
| `}` | 1 | 1/20 = 0.0500 | 4.322 | `1110` | 4 | 0.2000 |
| `²` | 1 | 1/20 = 0.0500 | 4.322 | `11110` | 5 | 0.2500 |
| `.` | 1 | 1/20 = 0.0500 | 4.322 | `11111` | 5 | 0.2500 |
| **Total** | 20 | 1 | | | | **4.0000** |

*Encoded message* (spaces separate the symbols):

`01110 01111 1000 1001 1010 10110 10111 000 001 1100 010 0110 000 001 1101 010 0110 1110 11110 11111`

Total bits = 80 (fixed 8-bit ASCII would need 160 bits).

*Entropy:* $H = -\sum p_i\log_2 p_i$, so $H$ is 3.9219 bit/symbol. *Average length:* $\bar L = \sum p_i l_i$ is 4.00 bit/symbol (80/20).

$$\text{Transmission efficiency } \eta = \frac{H}{\bar L} \times 100\% = \frac{3.9219}{4.00} \times 100\% = 98.05\%$$

(redundancy $= 100 - \eta$). The result is correct to the table above, which was generated and checked by program (the lengths satisfy Kraft's inequality).

**(c) Linear block code (6, 3) and single-error correction.** Take the generator matrix of the systematic form $G = [\,I_3 \mid P\,]$ with

$$G = \begin{bmatrix} 1&0&0&1&1&0\\ 0&1&0&0&1&1\\ 0&0&1&1&0&1 \end{bmatrix}, \qquad H = [\,P^T \mid I_3\,] = \begin{bmatrix} 1&0&1&1&0&0\\ 1&1&0&0&1&0\\ 0&1&1&0&0&1 \end{bmatrix}$$

and $c = mG$ (modulo 2), so a codeword is the message followed by three parity bits $p_1 = m_1 \oplus m_3$, $p_2 = m_1 \oplus m_2$, $p_3 = m_2 \oplus m_3$. The eight codewords:

| Message | Codeword |
|---|---|
| 000 | 000000 |
| 001 | 001101 |
| 010 | 010011 |
| 011 | 011110 |
| 100 | 100110 |
| 101 | 101011 |
| 110 | 110101 |
| 111 | 111000 |

The minimum distance is $d_{min} = 3$, so the code detects $d_{min} - 1 = 2$ errors and corrects $t = \lfloor (d_{min}-1)/2 \rfloor = 1$ error. The syndrome is $s = rH^T$ ($r$ = received word); $s = 0$ means no error, and for a single error in bit $j$ the syndrome equals column $j$ of $H$:

| Error in bit | Error pattern $e$ | Syndrome $s$ (= column of $H$) |
|---|---|---|
| 1 | 100000 | 110 |
| 2 | 010000 | 011 |
| 3 | 001000 | 101 |
| 4 | 000100 | 100 |
| 5 | 000010 | 010 |
| 6 | 000001 | 001 |

All six syndromes are non-zero and different, so each single error is located.

*Example.* Message $m = 101$ → transmitted codeword $c = 101011$. Suppose bit 4 is flipped in the channel: $r = 101111$. The syndrome is

$$s = rH^T = 100$$

(bits $s_1 s_2 s_3$ as the three rows of $H$ give them), which is the fourth column of $H$ (the entries 100 read downwards), so the error is in **bit 4**. The decoder flips bit 4 and recovers $101011$; the message is the first three bits, $101$.

@s 4
**(a) Line codes for 1000000101.** Suitable encoders: **unipolar NRZ** (1 = +V, 0 = 0 V), **polar NRZ-L** (1 = +V, 0 = −V; Manchester is also drawn: a transition in the middle of every bit, here 1 = high-to-low and 0 = low-to-high) and **bipolar AMI** (0 = zero level; the 1s are alternately +V and −V; here the first 1 is +V, so the three 1s are +, −, +).

```figure caption="Line codes for the bit sequence 1000000101: unipolar NRZ, polar NRZ-L and Manchester, bipolar AMI."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
bits=[int(c) for c in "1000000101"]; n=len(bits); B8=False
def steps(levels): 
    x=[];y=[]
    for i,l in enumerate(levels): x+=[i,i+1]; y+=[l,l]
    return x,y
def half(levels2):
    x=[];y=[]
    for i,(a,b) in enumerate(levels2): x+=[i,i+0.5,i+0.5,i+1]; y+=[a,a,b,b]
    return x,y
unip=[b for b in bits]; polar=[1 if b else -1 for b in bits]
manch=[(1,-1) if b else (-1,1) for b in bits]   # 1: high-to-low, 0: low-to-high (IEEE 802.3 uses the opposite)
last=-1; ami=[]
for b in bits:
    if b: last=-last; ami.append(last)
    else: ami.append(0)
rows=[("Unipolar NRZ",steps(unip),(-0.3,1.3)),("Polar NRZ-L",steps(polar),(-1.4,1.4)),("Polar Manchester",half(manch),(-1.4,1.4)),("Bipolar AMI",steps(ami),(-1.4,1.4))]
if B8:
    b8=[];last=-1;i=0;sq=[]
    # B8ZS: eight consecutive zeros -> 0 0 0 V B 0 V B
    zeros=0;out=[];last=-1
    k=0
    while k<n:
        if bits[k]==1: last=-last; out.append(last); k+=1
        else:
            if k+8<=n and all(v==0 for v in bits[k:k+8]):
                V=last; Bp=-last; out+=[0,0,0,V,Bp,0,Bp,V]; last=V; k+=8
            else: out.append(0); k+=1
    rows.append(("Bipolar B8ZS",steps(out),(-1.4,1.4)))
fig,axs=plt.subplots(len(rows),1,figsize=(7.4,0.95*len(rows)+0.5),sharex=True)
for ax,(t,(x,y),yl) in zip(axs,rows):
    ax.plot(x,y,color=ACCENT,lw=1.8); ax.axhline(0,color="#999999",lw=0.6)
    for i in range(n+1): ax.axvline(i,color="#cccccc",lw=0.5,ls=":")
    ax.set_ylim(*yl); ax.set_yticks([]); ax.set_ylabel(t,rotation=0,ha="right",va="center",fontsize=7)
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6)
for i,b in enumerate(bits): axs[0].text(i+0.5,1.55,str(b),ha="center",fontsize=8,weight="bold")
axs[-1].set_xticks(range(n+1)); axs[-1].set_xlabel("bit interval",fontsize=7)
fig.subplots_adjust(left=0.2,right=0.98,top=0.9,bottom=0.12,hspace=0.25)
```


| Bit | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Unipolar NRZ | +V | 0 | 0 | 0 | 0 | 0 | 0 | +V | 0 | +V |
| Polar NRZ-L | +V | −V | −V | −V | −V | −V | −V | +V | −V | +V |
| Bipolar AMI | +V | 0 | 0 | 0 | 0 | 0 | 0 | −V | 0 | +V |

Unipolar has a DC component and no clocking; polar needs no DC removal but loses synchronisation in long strings (the string of six 0s); Manchester has a transition in every bit; AMI has no DC component and the alternation is a built-in error check.

**(b) Single-tone and double-tone AM.** The AM wave is $s(t) = A_c\,[1 + m(t)/A_c]\cos 2\pi f_c t$ (the carrier amplitude varies with the message).

| Basis | Single-tone AM | Double-tone AM |
|---|---|---|
| Message | $m(t) = A_m\cos 2\pi f_m t$ | $m(t) = A_1\cos 2\pi f_1 t + A_2\cos 2\pi f_2 t$ |
| AM wave | $A_c[1 + \mu\cos 2\pi f_m t]\cos 2\pi f_c t$ | $A_c[1 + \mu_1\cos 2\pi f_1 t + \mu_2\cos 2\pi f_2 t]\cos 2\pi f_c t$ |
| Modulation index | $\mu = A_m/A_c$ ($\le 1$) | $\mu_1 = A_1/A_c$, $\mu_2 = A_2/A_c$; total $\mu_t = \sqrt{\mu_1^2 + \mu_2^2}$ ($\le 1$) |
| Spectrum | carrier at $f_c$ and two sidebands $f_c \pm f_m$, amplitude $A_c\mu/2$ | carrier and four sidebands $f_c \pm f_1$ (amplitude $A_c\mu_1/2$), $f_c \pm f_2$ ($A_c\mu_2/2$) |
| Bandwidth | $2f_m$ | $2\max(f_1, f_2)$ |
| Total power | $P_t = P_c\left(1 + \dfrac{\mu^2}{2}\right)$ | $P_t = P_c\left(1 + \dfrac{\mu_1^2 + \mu_2^2}{2}\right) = P_c\left(1 + \dfrac{\mu_t^2}{2}\right)$ |
| Sideband power | $P_{SB} = P_c\mu^2/2$ | $P_{SB} = P_c\mu_t^2/2$ |
| Efficiency | $\eta = \dfrac{\mu^2}{2 + \mu^2}$, maximum 33.3 % at $\mu = 1$ | $\eta = \dfrac{\mu_t^2}{2 + \mu_t^2}$, maximum 33.3 % at $\mu_t = 1$ |

```figure caption="Single-tone and double-tone AM: waveforms with the envelope 1+m(t) (top) and line spectra (bottom)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
t=np.linspace(0,2.0,4000); fc=12.0
fig,axs=plt.subplots(2,2,figsize=(7.4,4.4))
m1=0.6*np.cos(2*np.pi*1*t); s1=(1+m1)*np.cos(2*np.pi*fc*t)
m2=0.4*np.cos(2*np.pi*1*t)+0.3*np.cos(2*np.pi*2.5*t); s2=(1+m2)*np.cos(2*np.pi*fc*t)
for ax,m,s,tt in ((axs[0,0],m1,s1,"Single-tone AM, mu = 0.6"),(axs[0,1],m2,s2,"Double-tone AM, mu1 = 0.4, mu2 = 0.3")):
    ax.plot(t,s,color=ACCENT,lw=0.5); ax.plot(t,1+m,color="#b00020",lw=1.0); ax.plot(t,-(1+m),color="#b00020",lw=1.0)
    ax.set_title(tt,fontsize=7.5); ax.set_xlabel("t",fontsize=6.5); ax.tick_params(labelsize=6); ax.set_ylim(-2.2,2.2)
def stems(ax,fr,am,lab):
    ax.vlines(fr,0,am,color=ACCENT,lw=2.2)
    for f,a,l in zip(fr,am,lab): ax.text(f,a+0.04,l,ha="center",fontsize=6.3)
    ax.set_xlim(7,17); ax.set_ylim(0,1.35); ax.set_xlabel("f",fontsize=6.5); ax.tick_params(labelsize=6)
stems(axs[1,0],[11,12,13],[0.3,1.0,0.3],["Ac*mu/2","Ac","Ac*mu/2"]); axs[1,0].set_title("Spectrum: BW = 2 fm",fontsize=7.5)
stems(axs[1,1],[9.5,10,12,14,14.5],[0.15,0.2,1.0,0.2,0.15],["","Ac*mu1/2","Ac","","Ac*mu2/2"]); axs[1,1].set_title("Spectrum: BW = 2 max(f1, f2)",fontsize=7.5)
axs[1,1].set_xticks([9.5,10,11,12,13,14,14.5])
fig.tight_layout()
```


*Numerical example.* $\mu = 0.6$: $\eta = 0.36/2.36 = 15.3\%$, $P_t = 1.18\,P_c$. Double tone with $\mu_1 = 0.4,\ \mu_2 = 0.3$: $\mu_t = \sqrt{0.16 + 0.09} = 0.5$, $\eta = 0.25/2.25 = 11.1\%$, $P_t = 1.125\,P_c$. Over-modulation occurs when $\mu$ (or $\mu_t$ for peaks adding in phase, i.e. $\mu_1 + \mu_2$) exceeds 1, and the envelope no longer follows the message. The carrier carries no information but most of the power in both cases.

**(c) ASK, PSK and FSK.** Digital modulation changes a parameter of a sinusoidal carrier $A\cos(2\pi f t + \phi)$ with the data bits.

```figure caption="Binary ASK, PSK and FSK waveforms for the data 1011001."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
bits=[1,0,1,1,0,0,1]; n=len(bits); fs=200
t=np.arange(n*fs)/fs; d=np.repeat(bits,fs)
fig,axs=plt.subplots(4,1,figsize=(7.4,4.6),sharex=True)
axs[0].plot(t,d,color=INK,lw=1.6); axs[0].set_ylim(-0.3,1.3); axs[0].set_yticks([]); axs[0].set_ylabel("data",rotation=0,ha="right",va="center",fontsize=7)
ask=d*np.sin(2*np.pi*4*t); psk=np.sin(2*np.pi*4*t+np.pi*(1-d)); fsk=np.sin(2*np.pi*(2.5+3.0*d)*t)
for ax,y,tt in ((axs[1],ask,"ASK"),(axs[2],psk,"PSK"),(axs[3],fsk,"FSK")):
    ax.plot(t,y,color=ACCENT,lw=1.0); ax.set_yticks([]); ax.set_ylabel(tt,rotation=0,ha="right",va="center",fontsize=7); ax.set_ylim(-1.4,1.4)
for ax in axs:
    for i in range(n+1): ax.axvline(i,color="#cccccc",lw=0.5,ls=":")
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
for i,b in enumerate(bits): axs[0].text(i+0.5,1.4,str(b),ha="center",fontsize=8,weight="bold")
axs[1].text(7.05,0,"amplitude: carrier on / off",fontsize=6.3,va="center"); axs[2].text(7.05,0,"phase: 0 / 180 deg",fontsize=6.3,va="center"); axs[3].text(7.05,0,"frequency: f0 / f1",fontsize=6.3,va="center")
axs[0].set_xlim(0,9.6); axs[-1].tick_params(labelsize=6); axs[-1].set_xlabel("bit interval",fontsize=7)
fig.subplots_adjust(left=0.1,right=0.98,top=0.93,bottom=0.1,hspace=0.2)
```


- **ASK (amplitude shift keying):** the amplitude is switched, $s(t) = A\cos 2\pi f_c t$ for 1 and $0$ for 0 (on-off keying). Simple, but sensitive to noise and fading; bandwidth $\approx 2R_b$.
- **PSK (phase shift keying):** the phase is switched, $s(t) = A\cos 2\pi f_c t$ for 1 and $A\cos(2\pi f_c t + \pi)$ for 0 (BPSK). Constant amplitude, good noise performance, needs a coherent receiver; QPSK sends 2 bits per symbol with four phases.
- **FSK (frequency shift keying):** the frequency is switched, $f_1$ for 1 and $f_0$ for 0. Constant amplitude, robust against amplitude noise, wider bandwidth ($\approx 2R_b + |f_1 - f_0|$); used in modems and low-rate radio.

@s 5
**(a) Digital and analog multiplexing hierarchies.**

```figure caption="Digital (T-carrier) and analog (FDM) multiplexing hierarchies with the number of channels and the data rate or bandwidth at each level."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,4.4))
for z in (a,b): z.axis("off"); z.set_xlim(0,10); z.set_ylim(0,13)
a.set_title("Digital hierarchy (North American T-carrier)",fontsize=8)
rows=[("24 x DS0 (64 kbit/s)\n24 voice channels",None),("DS1 (T1)\n24 ch, 1.544 Mbit/s","24 : 1"),("DS2 (T2)\n96 ch, 6.312 Mbit/s","4 x DS1"),("DS3 (T3)\n672 ch, 44.736 Mbit/s","7 x DS2"),("DS4 (T4)\n4032 ch, 274.176 Mbit/s","6 x DS3")]
for i,(t,m) in enumerate(rows):
    y=11.6-i*2.6; box(a,6.0,y,5.4,1.5,t,fs=6.5,fc=[BLUE,YEL,YEL,GRN,GRN][i])
    if m:
        ax_=a; ax_.add_patch(mp.Polygon([(0.6,y+1.35),(2.8,y+0.9),(2.8,y-0.9),(0.6,y-1.35)],fc="white",ec=INK,lw=1.1,zorder=3)); ax_.text(1.7,y,"MUX\n"+m,fontsize=5.8,ha="center",va="center",zorder=4)
        arr(ax_,(2.8,y),(3.3,y),c=ACCENT); arr(ax_,(6.0,y+1.85),(6.0,y+0.8),c=INK,lw=0.0)
    if i: arr(a,(0.1,y+2.6-0.0),(0.1,y+2.6),c=INK,lw=0)
b.set_title("Analog hierarchy (FDM, AT&T)",fontsize=8)
rows=[("12 voice channels\n4 kHz each",None),("Group\n12 ch, 48 kHz\n(60-108 kHz)","12 x 4 kHz"),("Supergroup\n60 ch, 240 kHz\n(312-552 kHz)","5 groups"),("Mastergroup\n600 ch, 2.52 MHz\n(564-3084 kHz)","10 supergroups"),("Jumbogroup\n3600 ch, 16.984 MHz","6 mastergroups")]
for i,(t,m) in enumerate(rows):
    y=11.6-i*2.6; box(b,6.0,y,5.4,1.7,t,fs=6.3,fc=[BLUE,YEL,YEL,GRN,GRN][i])
    if m:
        b.add_patch(mp.Polygon([(0.2,y+1.35),(2.9,y+0.9),(2.9,y-0.9),(0.2,y-1.35)],fc="white",ec=INK,lw=1.1,zorder=3)); b.text(1.55,y,"FDM\n"+m,fontsize=5.4,ha="center",va="center",zorder=4)
        arr(b,(2.9,y),(3.3,y),c=ACCENT)
for z in (a,b):
    for i in range(4):
        y=11.6-i*2.6; arr(z,(6.0,y-0.9),(6.0,y-2.6+0.9),c=INK)
fig.tight_layout()
```


*Digital hierarchy (TDM).* Each voice channel is sampled at 8 kHz with 8 bits: 64 kbit/s (DS0). The higher levels time-multiplex the lower ones and add framing and bit-stuffing overhead:

| Level | Made of | Channels | Data rate | Calculation |
|---|---|---|---|---|
| DS1 (T1) | 24 DS0 | 24 | 1.544 Mbit/s | $24 \times 64 = 1.536$ + 8 kbit/s framing |
| DS2 (T2) | 4 DS1 | 96 | 6.312 Mbit/s | $4 \times 1.544 = 6.176$ + stuffing and framing |
| DS3 (T3) | 7 DS2 | 672 | 44.736 Mbit/s | $7 \times 6.312 = 44.184$ + overhead |
| DS4 (T4) | 6 DS3 | 4032 | 274.176 Mbit/s | $6 \times 44.736 = 268.416$ + overhead |

The European (ITU-T E-carrier) hierarchy is 30 channels in E1 (2.048 Mbit/s, 32 slots), then ×4 each: E2 120 channels, 8.448 Mbit/s; E3 480, 34.368 Mbit/s; E4 1920, 139.264 Mbit/s; E5 7680, 565.148 Mbit/s.

*Analog hierarchy (FDM).* Voice channels of 4 kHz are single-sideband modulated onto different carriers:

| Level | Made of | Channels | Bandwidth | Band |
|---|---|---|---|---|
| Group | 12 voice channels | 12 | 48 kHz | 60 to 108 kHz |
| Supergroup | 5 groups | 60 | 240 kHz | 312 to 552 kHz |
| Mastergroup | 10 supergroups | 600 | 2.52 MHz | 564 to 3084 kHz |
| Jumbogroup | 6 mastergroups | 3600 | 16.984 MHz | |

| Digital (TDM) | Analog (FDM) |
|---|---|
| channels share the link in **time** slots | channels share the link in **frequency** bands |
| signals digital, regenerated at repeaters | signals analog, noise accumulates in amplifiers |
| rate given in bit/s | bandwidth given in Hz |
| needs synchronisation | needs guard bands and carrier generators |

**(b) CDMA for 8 users.** In CDMA every user has a unique orthogonal chip code and all users transmit at once in the same band. Here **Walsh codes** of length 8 (rows of the Hadamard matrix) are used. A bit 1 is sent as $+1$ times the code, a bit 0 as $-1$ times the code and a silent user sends 0. Users 1, 2, 3 send bit 1; users 4, 5, 6 send bit 0; users 7, 8 are silent.

| User | Walsh code (chips 1 to 8) | Data bit | $d_i$ |
|---|---|---|---|
| 1 | `+ + + + + + + +` | 1 | +1 |
| 2 | `+ - + - + - + -` | 1 | +1 |
| 3 | `+ + - - + + - -` | 1 | +1 |
| 4 | `+ - - + + - - +` | 0 | -1 |
| 5 | `+ + + + - - - -` | 0 | -1 |
| 6 | `+ - + - - + - +` | 0 | -1 |
| 7 | `+ + - - - - + +` | silent | +0 |
| 8 | `+ - - + - + + -` | silent | +0 |

*Transmission.* Each user multiplies its data by its code; the channel adds the eight signals chip by chip:

| User | $d_i \times$ code (8 chips) |
|---|---|
| 1 | `+1 +1 +1 +1 +1 +1 +1 +1` |
| 2 | `+1 -1 +1 -1 +1 -1 +1 -1` |
| 3 | `+1 +1 -1 -1 +1 +1 -1 -1` |
| 4 | `-1 +1 +1 -1 -1 +1 +1 -1` |
| 5 | `-1 -1 -1 -1 +1 +1 +1 +1` |
| 6 | `-1 +1 -1 +1 +1 -1 +1 -1` |
| 7 | `+0 +0 +0 +0 +0 +0 +0 +0` |
| 8 | `+0 +0 +0 +0 +0 +0 +0 +0` |
| **Sum (channel)** | **`+0 +2 +0 -2 +4 +2 +4 -2`** |

*Reception.* The receiver of user $i$ multiplies the channel chips by the code of user $i$ and sums over the 8 chips (the inner product); because the codes are orthogonal ($c_i\cdot c_j = 0$ for $i \ne j$ and $c_i\cdot c_i = 8$) the other users cancel, and the result divided by 8 is the user's bit:

| User | $\sum \text{chip}_k \cdot c_{i,k}$ | $/8$ | Decision |
|---|---|---|---|
| 1 | +8 | +1 | 1 |
| 2 | +8 | +1 | 1 |
| 3 | +8 | +1 | 1 |
| 4 | -8 | -1 | 0 |
| 5 | -8 | -1 | 0 |
| 6 | -8 | -1 | 0 |
| 7 | +0 | +0 | silent |
| 8 | +0 | +0 | silent |

So users 1, 2, 3 receive 1, users 4, 5, 6 receive 0, and users 7, 8 receive nothing (0, silent): the operation recovers every user's data exactly.

@s 6
**(a) Evolution of mobile communication, 1G to 5G.**

| Generation | Period | Technology | Data rate | Features |
|---|---|---|---|---|
| 1G | 1980s | analog, FDMA (AMPS, NMT) | 2.4 kbit/s | voice only, poor security and capacity, large phones |
| 2G | 1990s | digital, TDMA / CDMA (GSM, IS-95) | 9.6 to 64 kbit/s (GPRS 114, EDGE 384) | digital voice, SMS, encryption, roaming |
| 3G | 2000s | WCDMA, CDMA2000 (UMTS, HSPA) | 384 kbit/s to 42 Mbit/s | mobile internet, video calls, packet data |
| 4G | 2010s | OFDMA / SC-FDMA, MIMO, all-IP (LTE, LTE-A) | 100 Mbit/s to 1 Gbit/s | HD video, VoLTE, low latency (about 50 ms) |
| 5G | 2020s | OFDM with flexible numerology, massive MIMO, mmWave (NR) | up to 10 to 20 Gbit/s | latency about 1 ms, 1 million devices per km², eMBB, URLLC, mMTC, network slicing, IoT |

**(b) Checksum.** A checksum is an error-detecting code: the sender divides the data into $n$-bit words, adds them in one's complement arithmetic, complements the sum and sends the result with the data; the receiver adds everything including the checksum, and an all-ones result means no error is detected.

*Example (the 16-bit words of a 20-byte header):* `4500 0073 0000 4000 4011 [0000] C0A8 0001 C0A8 00C7`. The ordinary sum is 2479CH; the carry is wrapped around (added back to the low 16 bits) giving 479EH; its one's complement is the checksum **B861H**. The receiver adds all ten words including B861H and gets FFFFH, so the data pass. A single flipped bit changes the sum and the result is not FFFFH, so it is detected. Weakness: swapping two words or two compensating errors give the same sum, so CRC is stronger; the checksum is used for IP, TCP, UDP headers.

**(c) LAN vs MAN.**

| Basis | LAN (local area network) | MAN (metropolitan area network) |
|---|---|---|
| Area | a room, building or campus (up to a few km) | a city or town (up to about 50 km) |
| Data rate | 100 Mbit/s to 10 Gbit/s | 10 Mbit/s to 1 Gbit/s and more over fibre rings |
| Ownership | a single organisation (private) | private or a public carrier / ISP |
| Technology | Ethernet (IEEE 802.3), Wi-Fi (802.11), switches | FDDI, DQDB (802.6), metro Ethernet, WiMAX (802.16), SONET rings |
| Delay and errors | very low delay, low error rate | higher delay, more errors |
| Cost | cheap to set up and maintain | more expensive |
| Example | a college computer lab | a cable TV network or a city-wide bank network |

**(d) Packet switching vs circuit switching.**

| Basis | Circuit switching | Packet switching |
|---|---|---|
| Path | a dedicated physical path is set up before the data are sent (setup, transfer, release) | no dedicated path; each packet is routed independently |
| Resource use | bandwidth reserved for the whole call even if idle: poor efficiency | bandwidth shared (statistical multiplexing): efficient |
| Delay | setup delay, then constant low delay | variable delay (queueing), jitter |
| Order | data arrive in order | packets may arrive out of order (datagram) and are reordered |
| Failure | call dropped if a link fails | packets re-routed around the failure |
| Congestion | a call may be blocked at set-up | packets are queued or dropped |
| Billing | by time | by data volume |
| Example | traditional telephone network (PSTN) | the Internet (IP), X.25 |
