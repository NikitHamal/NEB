---
file: NEBians-IOE-Past-Paper-Logic-Circuit-ENEX203-2082-Kartik.pdf
subject: Logic Circuit
level: BE · Year II / Part I
code: ENEX 203
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electronics, Communication and Information (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is an ASCII code? Design 3-bit binary to Gray code converter with truth table. [[1+4]]

@q 2
Perform adding $(+18)_{10}$ with $(-27)_{10}$ using an 8-bit signed number with 1's complement method. [[2]]

@q 3
Perform the following code conversion: [[3×1]]

i) $(51.825)_{10}=(?)_2$

ii) $(E3A.9B)_{16}=(?)_8$

iii) $(11010)_2=(?)_{BCD}$

@q 4
Simplify the following Boolean function using K-map and draw the circuit of simplified expression using NAND-NAND logic functions only. [[3+2]]

$Y=\sum m(0,1,4,6,7,8,12,15)+d(2,3,9,11)$

@q 5
Draw the simplest logic circuit for "c" segment of the BCD-to-seven segment display decoder. [[3]]

@q 6
What is an encoder? Realize a full-subtractor circuit using a single 1:4 demultiplexer and use logic gates if necessary. [[1+3]]

@q 7
Define sequential logic circuit. Explain the operation of positive edge-triggered JK flip-flop with its excitation table, state diagram and find out its characteristic equation. [[1+5]]

@q 8
Convert SR flip-flop into D flip-flop with necessary logic expressions and logic circuit diagram. [[6]]

@q 9
Explain briefly about how 1011 data can be stored and retrieved in 4-bit parallel-in parallel-out (PIPO) shift register with neat diagram and its corresponding data transfer timing diagram. [[5]]

@q 10
Design the mod-6 synchronous counter using only T flip-flops with state diagram, logic circuit diagram and timing diagram. [[6]]

@q 11
Design a sequential machine which consists of a single input, X and the single output, Z. The machine is required to give output Z high when it contains serial message 1010. Use JK flip-flops only to realize the desired machine design. [[10]]

@q 12
What are the key advantages of using multiplexing in a display system? Explain multiplexing display with suitable diagram. [[5]]

<!-- SOLUTIONS -->

@s 1
**ASCII code.** ASCII (American Standard Code for Information Interchange) is a 7-bit alphanumeric code (128 characters; an 8th bit may be used for parity or for the extended set). It represents the digits 0-9 ($30_{16}$-$39_{16}$), the upper-case letters ($41_{16}$-$5A_{16}$), the lower-case letters ($61_{16}$-$7A_{16}$), punctuation and control characters (CR $=0D_{16}$, LF $=0A_{16}$, ESC $=1B_{16}$). Example: 'A' $=100\,0001_2=65_{10}$, '0' $=011\,0000_2=48_{10}$. It lets computers, keyboards and printers exchange text.

**3-bit binary to Gray converter.** Gray code: $G_2=B_2$ and each other bit is the XOR of two adjacent binary bits. Truth table:

| $B_2B_1B_0$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| $G_2G_1G_0$ | 000 | 001 | 011 | 010 | 110 | 111 | 101 | 100 |

K-maps ($G_1$: ones at 2, 3, 4, 5; $G_0$: ones at 1, 2, 5, 6):

$$\begin{gathered}G_2=B_2 \\ G_1=B_2'B_1+B_2B_1'=B_2\oplus B_1 \\ G_0=B_1'B_0+B_1B_0'=B_1\oplus B_0\end{gathered}$$

*Circuit:* $B_2$ goes straight to $G_2$; one XOR gate takes $B_2,B_1$ and gives $G_1$; another XOR gate takes $B_1,B_0$ and gives $G_0$ (two XOR gates in total). Consecutive Gray codes differ in one bit only (e.g. 011 to 010).

@s 2
8-bit signed numbers, 1's complement for negative numbers.

$$\begin{gathered}+18=0001\,0010 \\ +27=0001\,1011\ \Rightarrow\ -27=1110\,0100\ \text{(1's complement)}\end{gathered}$$

$$\begin{array}{r}0001\,0010\\+\ 1110\,0100\\\hline 1111\,0110\end{array}$$

No carry out of the MSB, so no end-around carry is needed. The sign bit is 1, so the result is negative; its magnitude is the 1's complement $0000\,1001=9$. Hence $18+(-27)=-9$ ✓.

@s 3
**i)** $(51.825)_{10}$. Integer part: $51=32+16+2+1=110011_2$. Fraction: $0.825\times2=1.65\to1$; $0.65\times2=1.3\to1$; $0.3\times2=0.6\to0$; $0.6\times2=1.2\to1$; $0.2\times2=0.4\to0$; $0.4\times2=0.8\to0$; $0.8\times2=1.6\to1$; $0.6\to1\ldots$ (the fraction $33/40$ does not terminate: $0.11010011\,0011\ldots$).

$$(51.825)_{10}=(110011.11010011\ldots)_2\approx(110011.1101001)_2$$

**ii)** $(E3A.9B)_{16}$: write each hex digit in 4 bits: $1110\ 0011\ 1010\ .\ 1001\ 1011$. Regroup in threes from the radix point: integer $111\ 000\ 111\ 010$, fraction $100\ 110\ 110$ (padded with a 0):

$$(E3A.9B)_{16}=(7072.466)_8$$

**iii)** $(11010)_2=26_{10}$; BCD takes each decimal digit separately: $2=0010$, $6=0110$:

$$(11010)_2=(0010\ 0110)_{BCD}$$

@s 4
**K-map** (rows $AB$, columns $CD$ in Gray order 00, 01, 11, 10; X = don't care):

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 1 | 1 | X | X |
| 01 | 1 | 0 | 1 | 1 |
| 11 | 1 | 0 | 1 | 0 |
| 10 | 1 | X | X | 0 |

Prime implicant groups (don't cares used where they help):

- $m(3,7,11,15)$ gives $CD$
- $m(0,2,4,6)$ gives $A'D'$
- $m(0,1,8,9)$ gives $B'C'$
- $m(0,4,8,12)$ gives $C'D'$ (needed for the 1 at $m_{12}$)

$$\boxed{Y=CD+A'D'+B'C'+C'D'}$$

Check: every minterm 0, 1, 4, 6, 7, 8, 12, 15 is covered and none of 5, 10, 13, 14 is.

**NAND-NAND realisation.** A SOP is converted by double inversion, $Y=\overline{\overline{CD}\cdot\overline{A'D'}\cdot\overline{B'C'}\cdot\overline{C'D'}}$:

| Level | Gate | Inputs | Output |
|---|---|---|---|
| inverters | NOT (NAND with tied inputs) | $A,B,C,D$ | $A',B',C',D'$ |
| 1 | NAND-1 | $C,D$ | $\overline{CD}$ |
| 1 | NAND-2 | $A',D'$ | $\overline{A'D'}$ |
| 1 | NAND-3 | $B',C'$ | $\overline{B'C'}$ |
| 1 | NAND-4 | $C',D'$ | $\overline{C'D'}$ |
| 2 | NAND-5 (4-input) | outputs of NAND-1 to 4 | $Y$ |

(4 + 1 two-input/four-input NANDs plus four NAND inverters for the complemented inputs.)

@s 5
Segment **c** of a seven-segment display is **off** only for the digit 2 (0010) and **on** for 0, 1, 3, 4, 5, 6, 7, 8, 9; the inputs 1010 to 1111 do not occur (don't care). K-map with $ABCD$: the single zero is $m_2$ and it can be grouped with $m_{10}$ (don't care) to give $c'=B'CD'$, so

$$c'=B'CD'\ \Rightarrow\ \boxed{c=B+C'+D}$$

Check for each digit: 0 ($C'=1$), 1 ($C'$), 2 (0010: $B=0,C'=0,D=0$, so $c=0$ ✓ off), 3 ($D$), 4-7 ($B$), 8-9 ($C'$) ✓.

*Circuit:* one inverter for $C$ and a single 3-input OR gate with inputs $B$, $C'$, $D$ (an equivalent NAND form is a 3-input NAND with inputs $B'$, $C$, $D'$).

@s 6
**Encoder.** An encoder is a combinational circuit that has $2^n$ (or fewer) input lines, of which only one is active at a time, and produces an $n$-bit binary code of the active input (e.g. a 4-to-2 encoder: $D_3D_2D_1D_0=1000\to Y_1Y_0=11$). Its inverse is the decoder. Examples: decimal-to-BCD, octal-to-binary, keyboard encoder; a *priority* encoder gives the code of the highest-priority active input.

**Full subtractor with a single 1:4 demultiplexer.** Difference and borrow of $A-B-B_{in}$:

$$\begin{gathered}D=\sum m(1,2,4,7) \\ B_{out}=\sum m(1,2,3,7)\end{gathered}$$

Use the demultiplexer with the data input tied to logic 1 and the select lines $S_1S_0=AB$: the four outputs are $P_0=A'B'$, $P_1=A'B$, $P_2=AB'$, $P_3=AB$ (one is 1 at a time). Then

$$\begin{gathered}D=B_{in}'(P_1+P_2)+B_{in}(P_0+P_3) \\ B_{out}=P_1+B_{in}(P_0+P_3)\end{gathered}$$

*Check:* $D$ equals 1 for $AB=01,10$ with $B_{in}=0$ (minterms $010=2$ and $100=4$ in the order $AB B_{in}$) and for $AB=00,11$ with $B_{in}=1$ (minterms 1 and 7) ✓. $B_{out}=A'B$ (minterms 2, 3) $+\,B_{in}A'B'$ (minterm 1) $+\,B_{in}AB$ (minterm 7) ✓.

*Gates required:* two OR gates ($P_1+P_2$ and $P_0+P_3$), two AND gates with $B_{in}'$ and $B_{in}$ ($B_{in}'$ from one NOT gate), one OR gate for $D$, one AND gate and one OR gate for $B_{out}$. (A 1:4 demultiplexer cannot alone realise a three-variable function, so a few gates are needed as the question allows.)

@s 7
**Sequential logic circuit.** A sequential circuit is a logic circuit whose output depends on the present inputs **and on the past history of the inputs (the stored state)**; it contains memory elements (flip-flops) in a feedback path, usually driven by a clock. Examples are registers, counters, sequence detectors. Types: synchronous (common clock) and asynchronous; Mealy and Moore machines.

**Positive-edge-triggered JK flip-flop.** The inputs are $J$, $K$ and the clock CLK; the outputs are $Q$ and $Q'$. On the rising edge of the clock the flip-flop samples $J,K$:

| $J$ | $K$ | $Q_{n+1}$ | Operation |
|---|---|---|---|
| 0 | 0 | $Q_n$ | no change (hold) |
| 0 | 1 | 0 | reset |
| 1 | 0 | 1 | set |
| 1 | 1 | $Q_n'$ | toggle |

*Excitation table* (what $J,K$ must be for a required change $Q_n\to Q_{n+1}$):

| $Q_n$ | $Q_{n+1}$ | $J$ | $K$ |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | X |
| 1 | 0 | X | 1 |
| 1 | 1 | X | 0 |

*State diagram:* two states 0 and 1. From 0: stay on $JK=0X$; go to 1 on $JK=1X$. From 1: stay on $JK=X0$; go to 0 on $JK=X1$.

```figure caption="Question 7: state diagram of the JK flip-flop (arrows are labelled with the inputs JK; X = don't care)."
fig,ax=plt.subplots(figsize=(4.6,2.3)); ax.axis("off")
import matplotlib.patches as mp
for x,t in ((0,"0"),(4,"1")): ax.add_patch(mp.Circle((x,0),0.7,fc="#e8ecf5",ec=INK,lw=1.8)); ax.text(x,0,t,ha="center",va="center",fontsize=14,fontweight="bold")
ax.annotate("",xy=(3.28,0.35),xytext=(0.72,0.35),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6,connectionstyle="arc3,rad=-0.25")); ax.text(2,1.1,"J K = 1 X",ha="center",fontsize=9)
ax.annotate("",xy=(0.72,-0.35),xytext=(3.28,-0.35),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6,connectionstyle="arc3,rad=-0.25")); ax.text(2,-1.1,"J K = X 1",ha="center",fontsize=9)
ax.annotate("",xy=(-0.4,0.6),xytext=(0.4,0.62),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6,connectionstyle="arc3,rad=1.6")); ax.text(-1.4,1.05,"J K = 0 X",fontsize=9)
ax.annotate("",xy=(3.6,0.62),xytext=(4.4,0.6),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6,connectionstyle="arc3,rad=1.6")); ax.text(4.6,1.05,"J K = X 0",fontsize=9)
ax.set_xlim(-2.4,6.4); ax.set_ylim(-1.6,1.7)
```

**Characteristic equation.** From the operation table, $Q_{n+1}=1$ for $JKQ_n=\,$001 ($J=K=0$, hold 1), 100 (set), 101 (set) and 110 (toggle $0\to1$); in the order $JKQ_n$ these are the minterms $m(1,4,5,6)$. The K-map of $Q_{n+1}$ has two groups, $m(4,6)\to JQ_n'$ and $m(1,5)\to K'Q_n$:

$$\boxed{Q_{n+1}=J\,Q_n'+K'\,Q_n}$$

Check: $J=K=1$ gives $Q_{n+1}=Q_n'$ (toggle); $J=K=0$ gives $Q_n$ (hold); $J=1,K=0$ gives $Q_n'+Q_n=1$ (set); $J=0,K=1$ gives $0$ (reset) ✓.

@s 8
**SR to D flip-flop.** A D flip-flop must follow $Q_{n+1}=D$. Write the SR excitation table and find $S,R$ in terms of $D$ and $Q_n$:

| $D$ | $Q_n$ | $Q_{n+1}$ | $S$ | $R$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | X |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | X | 0 |

K-map for $S$ ($D,Q_n$): ones at $DQ_n=10$, don't care at $11$, so $S=D$. K-map for $R$: one at $DQ_n=01$, don't care at $00$, so $R=D'$.

$$\boxed{S=D,\qquad R=D'}$$

*Circuit:* the input $D$ is applied directly to $S$ and, through one NOT gate, to $R$ of the SR flip-flop; the clock is common. Then $S=R=1$ can never occur (the forbidden state is avoided) and the output follows $D$ on each clock: $Q_{n+1}=S+R'Q_n=D+DQ_n=D$ ✓.

@s 9
**4-bit parallel-in parallel-out (PIPO) shift register.** Four D flip-flops $FF_3FF_2FF_1FF_0$ share one clock and one clear line. The parallel data inputs are $D_3D_2D_1D_0$, each connected to the D input of its own flip-flop, and the outputs are $Q_3Q_2Q_1Q_0$ (all four available at the same time).

*Storing the data 1011:* apply $D_3D_2D_1D_0=1\,0\,1\,1$ to the data inputs (the register initially cleared to 0000) and give **one** clock pulse. On the rising edge every flip-flop loads its input simultaneously, so $Q_3Q_2Q_1Q_0=1011$ immediately after the pulse. The data stay stored until the next clock edge (the inputs may then change without affecting the stored word).

*Retrieving the data:* the stored word is read at the same time from the four outputs $Q_3Q_2Q_1Q_0=1011$ (parallel out), no further clock pulses are needed; the word is available after one clock period. (If it is read serially, the register has to be used as a shift register with the $Q$ output of each stage fed to the next stage, taking four clock pulses.)

```figure caption="Question 9: timing diagram of the PIPO register loading the word 1011 (D3 D2 D1 D0) on the first rising clock edge; the outputs Q3 Q2 Q1 Q0 show the stored word during the rest of the period."
fig,ax=plt.subplots(figsize=(6.0,3.4))
t=np.arange(0,5.01,0.01)
def clk(t): return ((t%1)<0.5).astype(float)
rows=[("CLK",None),("D3",1),("D2",0),("D1",1),("D0",1),("Q3",1),("Q2",0),("Q1",1),("Q0",1)]
for i,(n,v) in enumerate(rows):
    y0=(len(rows)-1-i)*1.4
    if n=="CLK": y=clk(t)
    elif n.startswith("D"): y=np.where(t>=0.2,v,0.0)
    else: y=np.where(t>=1.0,v,0.0)
    ax.plot(t,y*0.9+y0,color=ACCENT if n!="CLK" else INK,lw=1.8); ax.text(-0.15,y0+0.4,n,ha="right",va="center",fontsize=9)
ax.axvline(1.0,color="#d9534f",ls="--",lw=1); ax.text(1.05,len(rows)*1.4-0.5,"first rising edge: load 1011",color="#d9534f",fontsize=8)
ax.axis("off"); ax.set_xlim(-0.8,5.1); ax.set_ylim(-0.3,len(rows)*1.4)
```

@s 10
**Mod-6 synchronous counter with T flip-flops.** Six states 000 to 101 (three flip-flops $Q_2Q_1Q_0$), then back to 000; states 110, 111 are unused (don't care). State diagram: $000\to001\to010\to011\to100\to101\to000$.

*Excitation table* ($T=Q_n\oplus Q_{n+1}$):

| Present $Q_2Q_1Q_0$ | Next | $T_2$ | $T_1$ | $T_0$ |
|---|---|---|---|---|
| 000 | 001 | 0 | 0 | 1 |
| 001 | 010 | 0 | 1 | 1 |
| 010 | 011 | 0 | 0 | 1 |
| 011 | 100 | 1 | 1 | 1 |
| 100 | 101 | 0 | 0 | 1 |
| 101 | 000 | 1 | 0 | 1 |
| 110, 111 | X | X | X | X |

K-maps (with the don't cares 110, 111):

$$\begin{gathered}T_0=1 \\ T_1=Q_2'Q_0 \\ T_2=Q_1Q_0+Q_2Q_0=Q_0(Q_1+Q_2)\end{gathered}$$

*Logic circuit:* three T flip-flops with a common clock; $T_0$ tied to logic 1; $T_1$ from a 2-input AND gate with inputs $Q_2'$ and $Q_0$; $T_2$ from an OR gate ($Q_1+Q_2$) followed by an AND gate with $Q_0$. (Self-start: from 110: $T_2=0$, $T_1=0$, $T_0=1$ gives 111; from 111: $T_2=1$, $T_1=0$, $T_0=1$ gives 000, so the unused states lead back to the sequence.)

```figure caption="Question 10: timing diagram of the mod-6 synchronous counter (T flip-flops, positive-edge clock). The count repeats every 6 clock pulses."
fig,ax=plt.subplots(figsize=(6.2,2.9))
n=13; t=np.arange(0,n,0.01)
seq=[0,1,2,3,4,5]
def val(t,bit):
    k=int(np.floor(t))%6; return (seq[k]>>bit)&1
names=[("CLK",None),("Q0",0),("Q1",1),("Q2",2)]
for i,(nm,b) in enumerate(names):
    y0=(3-i)*1.5
    y=np.array([((tt%1)<0.5)*1.0 if b is None else float(val(tt,b)) for tt in t])
    ax.plot(t,y*0.9+y0,color=INK if b is None else ACCENT,lw=1.8); ax.text(-0.2,y0+0.4,nm,ha="right",va="center",fontsize=9)
for k in range(n): ax.text(k+0.5,-0.55,str(seq[k%6]),ha="center",fontsize=8,color=MUTED)
ax.axis("off"); ax.set_xlim(-1,n+0.2); ax.set_ylim(-0.9,6)
```

@s 11
**Sequence detector for 1010** (Mealy machine, overlapping sequences allowed). $Z=1$ when the last four inputs are 1010.

*States:* $S_0$ (nothing useful yet), $S_1$ (last bit 1), $S_2$ (last bits 10), $S_3$ (last bits 101).

| Present state | $X=0$: next / $Z$ | $X=1$: next / $Z$ |
|---|---|---|
| $S_0$ | $S_0$ / 0 | $S_1$ / 0 |
| $S_1$ | $S_2$ / 0 | $S_1$ / 0 |
| $S_2$ | $S_0$ / 0 | $S_3$ / 0 |
| $S_3$ | $S_2$ / **1** | $S_1$ / 0 |

(In $S_3$ with $X=0$ the sequence 1010 is complete; the last 10 may start a new 1010, so the next state is $S_2$.)

```figure caption="Question 11: state diagram of the 1010 sequence detector (Mealy; labels are X/Z)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.8,3.2)); ax.axis("off")
P={"S0":(0,0),"S1":(3,0),"S2":(6,0),"S3":(3,-2.6)}
for k,(x,y) in P.items(): ax.add_patch(mp.Circle((x,y),0.55,fc="#e8ecf5",ec=INK,lw=1.7)); ax.text(x,y,k,ha="center",va="center",fontsize=10,fontweight="bold")
def arr(a,b,t,rad=0.0,off=(0,0.25)):
    (x1,y1),(x2,y2)=P[a],P[b]; d=np.array([x2-x1,y2-y1]); d=d/np.hypot(*d)
    ax.annotate("",xy=(x2-0.58*d[0],y2-0.58*d[1]),xytext=(x1+0.58*d[0],y1+0.58*d[1]),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.5,connectionstyle=f"arc3,rad={rad}"))
    ax.text((x1+x2)/2+off[0],(y1+y2)/2+off[1],t,ha="center",fontsize=8.5)
arr("S0","S1","1/0",off=(0,0.3)); arr("S1","S2","0/0",off=(0,0.3)); arr("S2","S3","1/0",rad=-0.2,off=(0.5,-0.2)); arr("S3","S2","0/1",rad=-0.2,off=(1.1,-0.7)); arr("S3","S1","1/0",off=(-0.4,0.0)); arr("S2","S0","0/0",rad=0.45,off=(0,1.8))
ax.text(0,0.9,"0/0",ha="center",fontsize=8.5); ax.text(3,0.9,"1/0",ha="center",fontsize=8.5)
ax.set_xlim(-1.2,7.2); ax.set_ylim(-3.6,2.9)
```

*State assignment:* $S_0=00,\ S_1=01,\ S_2=10,\ S_3=11$ ($Q_1Q_0$). *JK excitation table:* $0\to0$: $J=0,K=X$; $0\to1$: $J=1,K=X$; $1\to0$: $J=X,K=1$; $1\to1$: $J=X,K=0$.

| $Q_1Q_0$ | $X$ | Next $Q_1Q_0$ | $Z$ | $J_1$ | $K_1$ | $J_0$ | $K_0$ |
|---|---|---|---|---|---|---|---|
| 00 | 0 | 00 | 0 | 0 | X | 0 | X |
| 00 | 1 | 01 | 0 | 0 | X | 1 | X |
| 01 | 0 | 10 | 0 | 1 | X | X | 1 |
| 01 | 1 | 01 | 0 | 0 | X | X | 0 |
| 10 | 0 | 00 | 0 | X | 1 | 0 | X |
| 10 | 1 | 11 | 0 | X | 0 | 1 | X |
| 11 | 0 | 10 | **1** | X | 0 | X | 1 |
| 11 | 1 | 01 | 0 | X | 1 | X | 0 |

K-map simplification (variables $Q_1,Q_0,X$):

$$\begin{gathered}J_1=Q_0X' \\ K_1=Q_0X+Q_0'X'=(Q_0\oplus X)' \\ J_0=X \\ K_0=X' \\ Z=Q_1Q_0X'\end{gathered}$$

*Circuit:* two JK flip-flops on a common clock. $J_0$ is connected to $X$ and $K_0$ to $X'$ (one NOT gate), so $FF_0$ acts as a D flip-flop that stores the last input. $J_1=Q_0\cdot X'$ (AND gate), $K_1$ is an XNOR of $Q_0$ and $X$. The output $Z$ is a 3-input AND of $Q_1$, $Q_0$ and $X'$.

*Check with the input stream 1 0 1 0 (starting in $S_0$):* $S_0\xrightarrow{1}S_1\xrightarrow{0}S_2\xrightarrow{1}S_3\xrightarrow{0}S_2$ with $Z=1$ on the last bit; an overlapping stream 1 0 1 0 1 0 gives $Z=1$ twice ✓.

@s 12
**Advantages of multiplexing in a display system.** In multiplexed displays several digits share the same segment drivers and decoder, and the digits are switched on one at a time at a high rate.

1. **Fewer connections and driver circuits:** for an $N$-digit seven-segment display the segment lines are common ($7$ or $8$ lines plus $N$ digit-select lines instead of $7N$), so the number of pins, wires, decoders and current-limiting resistors is much smaller.
2. **Lower hardware cost and PCB area**, because only one BCD-to-seven-segment decoder (or one microcontroller port) is needed.
3. **Lower power consumption:** only one digit is on at any time (average current of the whole display is low, while the peak current of the active digit can be larger so the brightness is good).
4. Easy extension to more digits, and easy control by a microprocessor/counter.

**Multiplexed display operation.** A counter running from a clock of a few hundred hertz drives (i) a 1-of-$N$ decoder, which turns on the common cathode (or anode) of one digit at a time through a transistor, and (ii) a data multiplexer, which places the BCD data of that same digit on the input of the single BCD-to-seven-segment decoder. Each digit is lit in turn for a time $T/N$; if the refresh rate $1/T$ is above about 50 Hz (typically 100-1000 Hz) persistence of vision makes all digits appear continuously lit.

```figure caption="Question 12: block diagram of a 4-digit multiplexed seven-segment display: the clock and a mod-4 counter select one BCD digit (4:1 MUX) and the matching digit driver (2:4 decoder); one BCD-to-7-segment decoder drives the common segment lines a-g."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.4,3.0)); ax.axis("off")
def box(x,y,w,h,t,c="#e8ecf5"): ax.add_patch(mp.FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc=c,ec=INK,lw=1.4)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=8)
box(0,1.2,1.2,0.8,"Clock"); box(1.8,1.2,1.4,0.8,"Mod-4\ncounter")
box(4.0,2.3,1.6,0.9,"4:1 MUX\n(BCD digits D0-D3)"); box(4.0,0.0,1.6,0.9,"2:4 decoder\n+ drivers")
box(6.4,2.3,1.6,0.9,"BCD to\n7-segment"); box(6.4,0.0,1.6,0.9,"Digit select\n(common pins)")
box(8.7,1.0,1.5,1.5,"4 digits\nseg a-g common\n1 digit on at a time","#fff3d6")
for a,b in (((1.2,1.6),(1.8,1.6)),((3.2,1.6),(4.0,2.7)),((3.2,1.6),(4.0,0.45)),((5.6,2.75),(6.4,2.75)),((5.6,0.45),(6.4,0.45)),((8.0,2.75),(8.7,2.2)),((8.0,0.45),(8.7,1.3))): ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.4))
ax.set_xlim(-0.3,10.4); ax.set_ylim(-0.3,3.5)
```
