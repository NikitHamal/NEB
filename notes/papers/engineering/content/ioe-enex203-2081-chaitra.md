---
file: NEBians-IOE-Past-Paper-Logic-Circuit-ENEX203-2081-Chaitra.pdf
subject: Logic Circuit
level: BE · Year II / Part I
code: ENEX 203
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course, 2080 batch), BE Electronics, Communication and Information (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
List the advantages of digital system over analog system with necessary diagrams. [[3]]

@q 2
Perform adding $(+28)_{10}$ with $(-37)_{10}$ using an 8-bit signed number with 2's complement method. [[2]]

@q 3
Convert the number as indicated [[1+1]]

(a) $(11011.1001)_2$ (into decimal)  (b) $(101101)_2$ (into gray code)

@q 4
Simplify the following Boolean function using K-map and draw the circuit of simplified expression using NOR-NOR logic function only. [[3+2]]

$Y=\sum m(0,1,4,6,7,8,12,14)+d(2,3,9,10)$

@q 5
Design a logic circuit which can be realized for the both full-adder and full-subtractor. [[6]]

@q 6
Define demultiplexer. Realize a full-adder circuit using a single 4:1 multiplexer and necessary logic gates. [[1+3]]

@q 7
Design an octal priority encoder with corresponding truth table, logic expressions and neat circuit diagram. [[6]]

@q 8
Convert SR flip-flop into JK flip-flop with necessary logic expressions and logic circuit diagram. [[6]]

@q 9
Explain briefly about how 1101 data can be stored and retrieve in 4-bit parallel-in serial-out (PISO) shift register with neat diagram and its corresponding data transfer timing diagram. [[6]]

@q 10
Describe the operation of mod-12 asynchronous counter using negative-edge triggered T flip-flops with neat logic circuit diagram and timing diagram. [[6]]

@q 11
Design a sequential machine which consist of a single input, X and the single output, Z. The machine is required to give output Z high when it contains serial message 010. Use RS flip-flops only to realize in the desired machine design. [[10]]

@q 12
Explain briefly about how counter can be used in the measurement of frequency with neat diagram. [[4]]

<!-- SOLUTIONS -->

@s 1
**Advantages of a digital system over an analog system.** A digital system represents information by two levels (0 and 1) instead of a continuously varying quantity.

1. **Noise immunity:** a noisy digital signal is restored to clean levels by a threshold (regenerated at every stage), whereas noise added to an analog signal can never be removed.
2. **Accuracy and precision** are fixed by the number of bits; component tolerance and drift do not change the result.
3. **Easy storage** of data (memory, flip-flops, disks) without degradation and with error detection/correction.
4. **Easy design and programmability:** logic gates and ICs are standard, and the function can be changed by software (microprocessors, FPGAs).
5. **Easy integration and low cost** (VLSI), low power per function, small size.
6. **Reliable transmission and multiplexing** (time-division, coding, encryption, compression).

```figure caption="Question 1: noise on an analog signal (left) stays in the signal; a digital signal with the same noise (right) is restored exactly by a threshold circuit."
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.2,2.1))
t=np.linspace(0,4,400); rng=np.random.default_rng(3); n=0.18*rng.standard_normal(400)
sig=np.sin(2*np.pi*t*0.75)
a1.plot(t,sig,color=MUTED,lw=1.2,ls="--",label="original"); a1.plot(t,sig+n,color=ACCENT,lw=1.2,label="received"); a1.set_title("Analog: noise stays",fontsize=9); a1.legend(fontsize=7,loc="lower left")
bits=np.repeat([1,0,1,1,0,1,0,0],50)[:400]
a2.plot(t,bits+n,color=ACCENT,lw=1.0,label="received (noisy)"); a2.plot(t,bits,color=INK,lw=1.6,label="restored by threshold 0.5"); a2.axhline(0.5,color="#d9534f",lw=0.8,ls=":"); a2.set_title("Digital: noise removed",fontsize=9); a2.legend(fontsize=7,loc="center right")
for a in (a1,a2): a.set_yticks([]); a.set_xticks([])
```

@s 2
8-bit signed numbers, negative numbers in 2's complement.

$$\begin{gathered}+28=0001\,1100 \\ +37=0010\,0101\ \Rightarrow\ -37=1101\,1010+1=1101\,1011\end{gathered}$$

$$\begin{array}{r}0001\,1100\\+\ 1101\,1011\\\hline 1111\,0111\end{array}$$

There is no carry out of the MSB and no overflow (the operands have opposite signs). The sign bit is 1, so the answer is negative; its magnitude is the 2's complement of $1111\,0111$: $0000\,1000+1=0000\,1001=9$. Hence $28+(-37)=-9$ ✓.

@s 3
**(a)** $(11011.1001)_2=1\cdot16+1\cdot8+0\cdot4+1\cdot2+1\cdot1+1\cdot2^{-1}+0+0+1\cdot2^{-4}=27+0.5+0.0625$:

$$(11011.1001)_2=(27.5625)_{10}$$

**(b)** Binary to Gray: $g_5=b_5$ and $g_i=b_{i+1}\oplus b_i$. For $101101$: $g=1,\ 1\oplus0=1,\ 0\oplus1=1,\ 1\oplus1=0,\ 1\oplus0=1,\ 0\oplus1=1$:

$$(101101)_2=(111011)_{Gray}$$

@s 4
**K-map** (rows $AB$, columns $CD$; X = don't care):

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 1 | 1 | X | X |
| 01 | 1 | 0 | 1 | 1 |
| 11 | 1 | 0 | 0 | 1 |
| 10 | 1 | X | 0 | X |

*SOP:* groups $m(0,2,4,6,8,10,12,14)\to D'$, $m(2,3,6,7)\to A'C$, $m(0,1,8,9)\to B'C'$, so $Y=D'+A'C+B'C'$.

*POS (needed for NOR-NOR):* group the zeros $m_5,m_{11},m_{13},m_{15}$: the group $m(9,11,13,15)$ (using the don't care 9) gives $AD$ and the pair $m(5,13)$ gives $BC'D$, so $Y'=AD+BC'D$ and

$$\boxed{Y=(A'+D')(B'+C+D')}$$

Check: zeros of $Y$ are $m_5,m_{11},m_{13},m_{15}$; for $m_5=0101$: $B'+C+D'=0$ ✓; $m_{11},m_{13},m_{15}$: $A'+D'=0$ ✓; $m_{14}=1110$: both factors 1 ✓.

**NOR-NOR circuit.** $Y=\overline{\overline{(A'+D')}+\overline{(B'+C+D')}}$:

| Level | Gate | Inputs | Output |
|---|---|---|---|
| inverters | NOR with tied inputs | $A,B,D$ | $A',B',D'$ |
| 1 | NOR-1 (2-input) | $A',D'$ | $\overline{A'+D'}$ |
| 1 | NOR-2 (3-input) | $B',C,D'$ | $\overline{B'+C+D'}$ |
| 2 | NOR-3 (2-input) | outputs of NOR-1 and NOR-2 | $Y$ |

@s 5
**Combined full adder / full subtractor (adder-subtractor).** Use a mode input $M$: $M=0$ gives addition $A+B+C_{in}$, $M=1$ gives subtraction $A-B-B_{in}$ (the third input is the carry-in or borrow-in). Let $X=A\oplus M$:

$$\text{Sum/Difference}=X\oplus B\oplus C_{in}=A\oplus M\oplus B\oplus C_{in}$$

$$\text{Carry/Borrow}=XB+C_{in}(X\oplus B)$$

*Check for $M=0$:* $X=A$, $S=A\oplus B\oplus C_{in}$, $C_{out}=AB+C_{in}(A\oplus B)$ — full adder ✓.

*Check for $M=1$:* $X=A'$, $D=A'\oplus B\oplus B_{in}=A\oplus B\oplus B_{in}$ (full-subtractor difference) and $B_{out}=A'B+B_{in}(A'\oplus B)=A'B+B_{in}(A\oplus B)'$ — exactly the full-subtractor borrow ✓.

*Truth table of the borrow ($M=1$):*

| $A$ | $B$ | $B_{in}$ | $D$ | $B_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |

*Circuit:* XOR-1 $(A,M)\to X$; XOR-2 $(X,B)\to P$; XOR-3 $(P,C_{in})\to$ Sum/Difference; AND-1 $(X,B)$; AND-2 $(P,C_{in})$; OR $(\text{AND-1},\text{AND-2})\to$ Carry/Borrow. Three XOR gates, two AND gates and one OR gate in total.

@s 6
**Demultiplexer.** A demultiplexer (data distributor) is a combinational circuit with one data input, $n$ select lines and $2^n$ outputs; it routes the data input to the output selected by the binary code on the select lines (the opposite of a multiplexer). For example, a 1:4 DEMUX with data $D$ and select $S_1S_0$ gives $Y_0=D\,S_1'S_0'$, $Y_1=D\,S_1'S_0$, $Y_2=D\,S_1S_0'$, $Y_3=D\,S_1S_0$. Applications: serial-to-parallel conversion, routing, decoder (with $D=1$).

**Full adder with a 4:1 multiplexer.** Use the select lines $S_1S_0=AB$ and put the proper function of $C_{in}$ on the data inputs. With $\text{Sum}=\sum m(1,2,4,7)$ and $\text{Carry}=\sum m(3,5,6,7)$ (minterms of $A,B,C_{in}$):

| $S_1S_0=AB$ | $I_0$ (00) | $I_1$ (01) | $I_2$ (10) | $I_3$ (11) |
|---|---|---|---|---|
| Sum | $C_{in}$ | $C_{in}'$ | $C_{in}'$ | $C_{in}$ |
| Carry | 0 | $C_{in}$ | $C_{in}$ | 1 |

For $AB=00$: Sum $=C_{in}$, Carry $=0$; for $AB=01$ or $10$: Sum $=C_{in}'$, Carry $=C_{in}$; for $AB=11$: Sum $=C_{in}$, Carry $=1$ ✓ (this is the full-adder truth table).

*Circuit:* one 4:1 multiplexer has a single output, so one multiplexer realises one output; the Sum multiplexer has data inputs $C_{in},C_{in}',C_{in}',C_{in}$ (one NOT gate), the Carry multiplexer (a second 4:1 MUX, or the same MUX reused with the other data pattern) has data inputs $0,C_{in},C_{in},1$. $A$ and $B$ drive $S_1,S_0$ of both. Alternatively, with a single multiplexer for the sum, the carry can be formed by one AND-OR network $AB+C_{in}(A\oplus B)$.

@s 7
**Octal priority encoder (8-to-3).** Inputs $D_7\ldots D_0$ ($D_7$ has the highest priority), outputs $A_2A_1A_0$ and a valid bit $V$ (1 when at least one input is active). The output is the binary code of the highest-priority active input.

| $D_7$ | $D_6$ | $D_5$ | $D_4$ | $D_3$ | $D_2$ | $D_1$ | $D_0$ | $A_2$ | $A_1$ | $A_0$ | $V$ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | X | X | X | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | X | 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 | 0 | 1 | X | X | 0 | 1 | 0 | 1 |
| 0 | 0 | 0 | 0 | 1 | X | X | X | 0 | 1 | 1 | 1 |
| 0 | 0 | 0 | 1 | X | X | X | X | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | X | X | X | X | X | 1 | 0 | 1 | 1 |
| 0 | 1 | X | X | X | X | X | X | 1 | 1 | 0 | 1 |
| 1 | X | X | X | X | X | X | X | 1 | 1 | 1 | 1 |

*Logic expressions* (K-map with the don't cares of the lower-priority inputs):

$$\begin{gathered}A_2=D_4+D_5+D_6+D_7\\A_1=D_7+D_6+D_5'D_4'D_3+D_5'D_4'D_2\\A_0=D_7+D_6'D_5+D_6'D_4'D_3+D_6'D_4'D_2'D_1\\V=D_0+D_1+D_2+D_3+D_4+D_5+D_6+D_7\end{gathered}$$

*Check, e.g. $D_6=D_3=1$:* $A_2=1$, $A_1=1$, $A_0=D_6'\ldots=0$ gives $110$, the code of the higher input $D_6$ ✓.

*Circuit:* $A_2$: one 4-input OR gate; $A_1$: two AND gates (3-input, with $D_5',D_4'$ from NOT gates) and a 4-input OR gate with $D_7$, $D_6$; $A_0$: AND gates $D_6'D_5$, $D_6'D_4'D_3$, $D_6'D_4'D_2'D_1$ and a 4-input OR with $D_7$; $V$: an 8-input OR gate. (Practical IC: 74148 or 74LS148.)

@s 8
**SR to JK flip-flop.** The JK flip-flop has inputs $J,K$ and present state $Q_n$; $S$ and $R$ must be generated so that the SR flip-flop goes to the state that a JK flip-flop would take. Using the SR excitation table ($0\to0$: $S=0,R=X$; $0\to1$: $S=1,R=0$; $1\to0$: $S=0,R=1$; $1\to1$: $S=X,R=0$):

| $J$ | $K$ | $Q_n$ | $Q_{n+1}$ | $S$ | $R$ |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | X |
| 0 | 0 | 1 | 1 | X | 0 |
| 0 | 1 | 0 | 0 | 0 | X |
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | X | 0 |
| 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 |

K-maps over $J,K,Q_n$: $S$ has ones at $JKQ_n=100,110$ and don't cares at $001,101$, giving $S=JQ_n'$. $R$ has ones at $011,111$ and don't cares at $000,010$, giving $R=KQ_n$.

$$\boxed{S=J\,Q_n',\qquad R=K\,Q_n}$$

*Circuit:* two 2-input AND gates; AND-1 takes $J$ and $\overline Q$ and drives $S$, AND-2 takes $K$ and $Q$ and drives $R$ of the SR flip-flop; the clock is common. Because $\overline Q$ and $Q$ are never 1 together, $S=R=1$ cannot occur, and $J=K=1$ toggles the output (the feedback removes the forbidden state): $Q_{n+1}=S+R'Q_n=JQ_n'+(K'+Q_n')Q_n=JQ_n'+K'Q_n$ ✓.

@s 9
**4-bit parallel-in serial-out (PISO) shift register.** Four D flip-flops are connected in a chain. In front of the D input of each flip-flop except the first there is a 2:1 multiplexer (AND-OR gates) controlled by a **SHIFT/LOAD** line: when SHIFT/LOAD $=0$ (load) the parallel input $D_i$ enters the flip-flop; when SHIFT/LOAD $=1$ (shift) the output $Q$ of the previous stage enters. The serial output is $Q_0$ (the last flip-flop).

*Storing 1101:* apply the parallel word $D_3D_2D_1D_0=1\,1\,0\,1$ and set SHIFT/LOAD $=0$; one clock pulse loads $Q_3Q_2Q_1Q_0=1101$ at the same time.

*Retrieving the data serially:* set SHIFT/LOAD $=1$; at each following clock pulse the word moves one place towards $Q_0$ and a new 0 enters at the serial input, so the bits appear one after another at the serial output $Q_0$ (LSB first): the values at $Q_0$ after pulses 1, 2, 3, 4 are **1, 0, 1, 1**; after the 5th pulse the register is empty (0000).

| After pulse | $Q_3$ | $Q_2$ | $Q_1$ | $Q_0$ (serial out) |
|---|---|---|---|---|
| 1 (load) | 1 | 1 | 0 | 1 |
| 2 (shift) | 0 | 1 | 1 | 0 |
| 3 | 0 | 0 | 1 | 1 |
| 4 | 0 | 0 | 0 | 1 |
| 5 | 0 | 0 | 0 | 0 |


```figure caption="Question 9: timing diagram of the PISO register: load 1101 on pulse 1 (SHIFT/LOAD = 0), then shift right on the following pulses; the serial output Q0 delivers 1 0 1 1."
fig,ax=plt.subplots(figsize=(6.2,3.2))
n=6; t=np.arange(0,n,0.01)
q=[[1,1,0,1],[0,1,1,0],[0,0,1,1],[0,0,0,1],[0,0,0,0]]  # Q3,Q2,Q1,Q0 after pulses 1..5
def Q(bit):
    return np.array([ (0 if tt<0.5 else q[min(int(np.floor(tt-0.5)),4)][bit]) for tt in t])
rows=[("CLK",None),("SH/LD",None),("Q3",0),("Q2",1),("Q1",2),("Q0 (serial out)",3)]
for i,(nm,b) in enumerate(rows):
    y0=(5-i)*1.5
    if nm=="CLK": y=np.array([float((tt%1)<0.5) for tt in t])
    elif nm=="SH/LD": y=np.array([0.0 if tt<1.5 else 1.0 for tt in t])
    else: y=Q(b).astype(float)
    ax.plot(t,y*0.9+y0,color=INK if b is None else ACCENT,lw=1.8); ax.text(-0.15,y0+0.4,nm,ha="right",va="center",fontsize=8.5)
ax.axvline(1.0,color="#d9534f",ls="--",lw=0.9); ax.text(1.05,7.1,"load 1101",color="#d9534f",fontsize=8)
ax.axis("off"); ax.set_xlim(-1.6,n); ax.set_ylim(-0.3,7.8)
```

@s 10
**Mod-12 asynchronous (ripple) counter with negative-edge triggered T flip-flops.** $2^4=16>12$, so four flip-flops $FF_0\ldots FF_3$ ($Q_0$ is the LSB) are used, all with $T=1$ (toggle mode). The external clock drives $FF_0$; the output $Q_0$ clocks $FF_1$, $Q_1$ clocks $FF_2$ and $Q_2$ clocks $FF_3$. A negative-edge triggered flip-flop toggles when its clock input goes from 1 to 0, i.e. when the previous stage output falls from 1 to 0, so the chain counts up in binary $0000\to0001\to\ldots\to1011$.

*Resetting at 12:* the counter must skip the states 1100 to 1111. The first time the count reaches **12 $=1100$** ($Q_3=Q_2=1$), a 2-input NAND gate with inputs $Q_3$ and $Q_2$ produces a 0 that is applied to the asynchronous clear input (active low) of all four flip-flops, which clears the counter to 0000 immediately (1100 exists only for a few nanoseconds, a glitch). So the sequence is $0,1,2,\ldots,11,0,1,\ldots$ (12 states, modulus 12; frequency of $Q_3$ is $f_{clk}/12$ approximately, with a duty cycle that is not 50 %).

*Operation summary:* $Q_0$ toggles on every falling clock edge ($f/2$), $Q_1$ on every falling edge of $Q_0$ ($f/4$), $Q_2$ ($f/8$), $Q_3$ ($f/16$ for a free-running counter; with the reset the repetition rate of the whole count is $f/12$).

```figure caption="Question 10: timing diagram of the mod-12 ripple counter (negative-edge T flip-flops); the count 0 to 11 repeats; the state 1100 only exists momentarily and clears the counter."
fig,ax=plt.subplots(figsize=(6.4,3.2))
n=13; t=np.arange(0,n,0.005)
def val(tt,bit):
    k=int(np.floor(tt))%12; return (k>>bit)&1
rows=[("CLK",None),("Q0",0),("Q1",1),("Q2",2),("Q3",3)]
for i,(nm,b) in enumerate(rows):
    y0=(4-i)*1.5
    y=np.array([float((tt%1)<0.5) if b is None else float(val(tt-0.5,b) if tt>=0.5 else 0) for tt in t])
    ax.plot(t,y*0.9+y0,color=INK if b is None else ACCENT,lw=1.6); ax.text(-0.2,y0+0.4,nm,ha="right",va="center",fontsize=9)
for k in range(n): ax.text(k+1.0,-0.6,str(k%12),ha="center",fontsize=7.5,color=MUTED)
ax.text(0,-1.1,"count after each falling edge",fontsize=7.5,color=MUTED)
ax.axis("off"); ax.set_xlim(-1,n+0.5); ax.set_ylim(-1.4,6.9)
```

@s 11
**Sequence detector for 010** (Mealy machine, overlapping allowed: in 01010 the output goes high twice). $Z=1$ when the last three inputs are 010.

*States:* $S_0$ (no useful bit), $S_1$ (last bit 0), $S_2$ (last bits 01).

| Present state | $X=0$: next / $Z$ | $X=1$: next / $Z$ |
|---|---|---|
| $S_0$ | $S_1$ / 0 | $S_0$ / 0 |
| $S_1$ | $S_1$ / 0 | $S_2$ / 0 |
| $S_2$ | $S_1$ / **1** | $S_0$ / 0 |

(From $S_2$ with $X=0$ the pattern 010 is complete and the final 0 can start the next pattern, so the next state is $S_1$.)

```figure caption="Question 11: state diagram of the 010 sequence detector (Mealy; labels are X/Z)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,2.6)); ax.axis("off")
P={"S0":(0,0),"S1":(3,0),"S2":(6,0)}
for k,(x,y) in P.items(): ax.add_patch(mp.Circle((x,y),0.55,fc="#e8ecf5",ec=INK,lw=1.7)); ax.text(x,y,k,ha="center",va="center",fontsize=10,fontweight="bold")
def arr(a,b,t,rad,ty):
    (x1,y1),(x2,y2)=P[a],P[b]; d=np.array([x2-x1,y2-y1]); d=d/np.hypot(*d)
    ax.annotate("",xy=(x2-0.58*d[0],y2-0.58*d[1]),xytext=(x1+0.58*d[0],y1+0.58*d[1]),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.5,connectionstyle=f"arc3,rad={rad}"))
    ax.text((x1+x2)/2,ty,t,ha="center",fontsize=8.5)
arr("S0","S1","0/0",-0.25,0.7); arr("S1","S2","1/0",-0.25,0.7); arr("S2","S1","0/1",-0.25,-0.9); arr("S2","S0","1/0",0.55,-1.9)
ax.text(0,0.95,"1/0",ha="center",fontsize=8.5); ax.text(3,0.95,"0/0",ha="center",fontsize=8.5)
ax.set_xlim(-1.2,7.2); ax.set_ylim(-2.4,1.8)
```

*State assignment:* $S_0=00,\ S_1=01,\ S_2=10$ ($Q_1Q_0$); $11$ is unused (don't care). *RS excitation table:* $0\to0$: $S=0,R=X$; $0\to1$: $S=1,R=0$; $1\to0$: $S=0,R=1$; $1\to1$: $S=X,R=0$.

| $Q_1Q_0$ | $X$ | Next | $Z$ | $S_1$ | $R_1$ | $S_0$ | $R_0$ |
|---|---|---|---|---|---|---|---|
| 00 | 0 | 01 | 0 | 0 | X | 1 | 0 |
| 00 | 1 | 00 | 0 | 0 | X | 0 | X |
| 01 | 0 | 01 | 0 | 0 | X | X | 0 |
| 01 | 1 | 10 | 0 | 1 | 0 | 0 | 1 |
| 10 | 0 | 01 | **1** | 0 | 1 | 1 | 0 |
| 10 | 1 | 00 | 0 | 0 | 1 | 0 | X |
| 11 | 0, 1 | X | X | X | X | X | X |

K-map simplification ($Q_1,Q_0,X$; the unused state 11 gives don't cares):

$$\begin{gathered}S_1=Q_0X \\ R_1=Q_0' \\ S_0=X' \\ R_0=X \\ Z=Q_1X'\end{gathered}$$

($S_0R_0=X'X=0$ and $S_1R_1=Q_0X\,Q_0'=0$, so the forbidden input $S=R=1$ never occurs.)

*Circuit:* two RS flip-flops with a common clock; one NOT gate gives $X'$ (used as $S_0$ and in $Z$); $R_0=X$ directly; $S_1$ is an AND gate with inputs $Q_0$ and $X$; $R_1$ is $Q_0'$ (the $\overline Q$ output of $FF_0$); $Z$ is an AND gate with inputs $Q_1$ and $X'$.

*Check with the input 0 1 0 (from $S_0$):* $S_0\xrightarrow{0}S_1\xrightarrow{1}S_2\xrightarrow{0}S_1$ and $Z=1$ on the last bit; with the input 0 1 0 1 0 the output is 1 on the third and the fifth bit ✓.

@s 12
**Frequency measurement with a counter.** The frequency is the number of cycles per second, so the unknown signal is counted for a precisely known time (gate time).

*Block diagram:* the input signal $f_x$ is conditioned by a Schmitt trigger (squared up to TTL levels) and applied to one input of an AND gate. A crystal oscillator followed by a frequency divider chain (decade dividers) produces an accurate time base, for example a 1 s or 0.1 s pulse; a gate-control flip-flop (the time-base pulse toggles it) generates the gate signal, which is the second input of the AND gate. A decade counter (BCD counters) counts the number of pulses that pass through the AND gate during the gate time; at the end of the gate a latch stores the count, the display shows it (BCD to seven-segment decoders) and a reset pulse clears the counter for the next measurement.

$$f_x=\frac{N}{T_{gate}}$$

With $T_{gate}=1$ s the count $N$ is directly the frequency in Hz; with 0.1 s the decimal point is shifted by one digit. The resolution is $1/T_{gate}$ ($\pm1$ count error), so a longer gate gives a more accurate reading of low frequencies; the accuracy of the time base (crystal) determines the accuracy of the instrument.

```figure caption="Question 12: digital frequency counter: input conditioning, time-base gate, AND gate, counter, latch and display."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.6,2.6)); ax.axis("off")
def box(x,y,w,h,t,c="#e8ecf5"): ax.add_patch(mp.FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc=c,ec=INK,lw=1.4)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=7.8)
box(0,1.5,1.5,0.9,"Schmitt\ntrigger"); box(2.1,1.5,1.0,0.9,"AND\ngate"); box(3.7,1.5,1.6,0.9,"BCD\ncounter"); box(5.9,1.5,1.3,0.9,"Latch"); box(7.8,1.5,1.5,0.9,"Decoder +\n7-seg display","#fff3d6")
box(0,0,1.5,0.9,"Crystal\noscillator"); box(2.1,0,1.5,0.9,"Divider\nchain"); box(4.2,0,1.9,0.9,"Gate control\n(T = 1 s)")
ax.text(-0.2,2.8,"input f_x",fontsize=8)
for a,b in (((1.5,1.95),(2.1,1.95)),((3.1,1.95),(3.7,1.95)),((5.3,1.95),(5.9,1.95)),((7.2,1.95),(7.8,1.95)),((1.5,0.45),(2.1,0.45)),((3.6,0.45),(4.2,0.45)),((5.15,0.9),(2.6,1.5)),((6.1,0.45),(6.5,1.5)),((5.15,0.9),(4.5,1.5))): ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.3))
ax.text(6.9,0.8,"latch / reset pulses",fontsize=7.5,color=MUTED)
ax.set_xlim(-0.8,9.6); ax.set_ylim(-0.3,3.1)
```
