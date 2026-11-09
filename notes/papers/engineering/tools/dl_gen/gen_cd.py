import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_b import *

def proofs():
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                l1 = (a & b) | ((1 - a) & c) | (b & c); r1 = (a & b) | ((1 - a) & c)
                xo = a ^ b
                l2 = (a & b) | (c & xo); r2 = (b & c) | (a & (b | c))
                assert l1 == r1 and l2 == r2
                rows.append([a, b, c, l1, r1, l2, r2])
    return ("**(a) $AB + \\overline{A}C + BC = AB + \\overline{A}C$ (consensus theorem).**\n\n"
            "Multiply the redundant term by $(A+\\overline{A}) = 1$:\n\n"
            "$$\\begin{aligned} \\text{LHS} &= AB + \\overline{A}C + BC(A+\\overline{A}) \\\\ &= AB + \\overline{A}C + ABC + \\overline{A}BC \\\\ &= AB(1 + C) + \\overline{A}C(1 + B) \\\\ &= AB + \\overline{A}C = \\text{RHS} \\end{aligned}$$\n\n"
            "**(b) $AB + C(A\\oplus B) = BC + A(B+C)$.**\n\n"
            "Left side, using $A\\oplus B = \\overline{A}B + A\\overline{B}$:\n\n"
            "$$\\begin{aligned} \\text{LHS} &= AB + \\overline{A}BC + A\\overline{B}C \\\\ &= B(A + \\overline{A}C) + A\\overline{B}C \\\\ &= B(A + C) + A\\overline{B}C \\qquad (x + \\overline{x}y = x + y) \\\\ &= AB + BC + A\\overline{B}C \\\\ &= BC + A(B + \\overline{B}C) = BC + A(B + C) = \\text{RHS} \\end{aligned}$$\n\n"
            "Both sides equal $AB + BC + CA$ (the majority function, which is the carry of a full adder). **Truth-table check:**\n\n" +
            tbl(["A", "B", "C", "AB+A'C+BC", "AB+A'C", "AB+C(A⊕B)", "BC+A(B+C)"], rows) + "\nIn every row the two columns of each pair are identical, so both identities hold.\n")

def priority_text():
    res, tx, _, codes = priority_encoder()
    rows = []
    for i in range(7, 0, -1):
        r = [("1" if j == i else ("X" if j < i else "0")) for j in range(7, -1, -1)]
        rows.append(r + [(i >> 2) & 1, (i >> 1) & 1, i & 1, 1])
    rows.append(["0"] * 7 + ["X"] + [0, 0, 0, 1])
    rows.append(["0"] * 8 + [0, 0, 0, 0])
    nm = ["D_7", "D_6", "D_5", "D_4", "D_3", "D_2", "D_1"]
    eq = {}
    for k, v in res.items():
        eq[k] = " + ".join("".join((nm[i] if p else "\\overline{%s}" % nm[i]) for i, p in t) for t in v)
    return ("**Decoder.** A decoder is a combinational circuit that converts an $n$-bit binary input code into a 1-of-$2^n$ output: exactly one output line is active for each input combination (for a 3-to-8 decoder each output is a minterm of the inputs, built with AND/NAND gates, and an enable input switches the decoder on or off). Applications: address decoding, memory chip-select, demultiplexing, BCD-to-seven-segment driving.\n\n"
            "**Octal priority encoder.** An ordinary encoder gives a wrong code if two inputs are active together. A priority encoder gives the code of the **highest-numbered active input** and ignores the lower ones (X = don't care). A valid output $V$ shows that at least one input is active.\n\n" +
            tbl(["D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0", "A2", "A1", "A0", "V"], rows) +
            "\nFrom this table (the minimisation was done on a 7-variable K-map/Quine-McCluskey over $D_7\\dots D_1$ and verified for all 128 input combinations; $D_0$ never changes the code):\n\n"
            f"$$\\begin{{aligned}} A_2 &= {eq['A2']} \\\\ A_1 &= {eq['A1']} \\\\ A_0 &= {eq['A0']} \\\\ V &= D_7 + D_6 + D_5 + D_4 + D_3 + D_2 + D_1 + D_0 \\end{{aligned}}$$\n\n"
            "**Logic diagram** (the three outputs; each product term is an AND gate and each output an OR gate; the complemented inputs come from NOT gates):\n\n" + codes + "\nThe valid output is a single 8-input OR gate on $D_0\\dots D_7$.\n")

def decoder_realisation():
    ones = [0, 2, 3, 7, 8, 10, 11, 14, 15]
    # verify decoder form
    for m in range(16):
        abc, d = m >> 1, m & 1
        f = ((abc == 0) and d == 0) or abc == 1 or ((abc == 3) and d == 1) or ((abc == 4) and d == 0) or abc == 5 or abc == 7
        assert bool(f) == (m in ones), m
    code = r'''
fig,ax=ckt_canvas(5.9,4.2,xlim=(-1.4,15.4),ylim=(-1.2,7.2))
box(ax,1.4,0.0,2.6,6.0,"3 × 8\nDECODER",size=8.4)
for k,(nm) in enumerate(["A","B","C"]):
    yy=4.6-1.5*k; L(ax,[(0.6,yy),(1.4,yy)]); T(ax,0.5,yy,nm,ha="right",size=8.6); T(ax,1.55,yy,["I2","I1","I0"][k],ha="left",size=7.4,color=MUTED)
ys=[5.5-0.75*i for i in range(8)]
for i,y in enumerate(ys):
    L(ax,[(4.0,y),(4.6,y)]); T(ax,3.9,y,"y%d"%i,ha="right",size=7.6)
# AND gates for y0.D', y3.D, y4.D'
outs={}
gy={0:5.5,3:3.55,4:2.55}
for i,lab in ((0,"D'"),(3,"D"),(4,"D'")):
    ins,o=gn(ax,"AND",6.2,gy[i],n=2,w=0.9,lead=0.3)
    L(ax,[(4.6,ys[i]),(ins[0][0],ys[i]) if abs(ins[0][1]-ys[i])<1e-6 else (4.6,ys[i]),(5.5,ys[i]),(5.5,ins[0][1]),ins[0]])
    T(ax,ins[1][0]-0.08,ins[1][1],lab,ha="right",size=8.0); outs[i]=o
# OR gate: inputs from y1,y5,y7 directly and the three ANDs
src=[("y",ys[1]),("a",outs[0]),("a",outs[3]),("a",outs[4]),("y",ys[5]),("y",ys[7])]
ins,o=gn(ax,"OR",11.0,3.0,n=6,sp=0.62,w=1.1,lead=0.4)
order=[("y",1),("a",0),("a",3),("a",4),("y",5),("y",7)]
for (kind,i),(px,py) in zip(order,ins):
    if kind=="y":
        xm=8.6+0.2*i%1.0
        L(ax,[(4.6,ys[i]),(7.3+0.18*(i%3),ys[i]),(7.3+0.18*(i%3),py),(px,py)]) if False else L(ax,[(4.6,ys[i]),(5.0+0.0,ys[i]),(5.0,ys[i]),(5.0,ys[i])]) if False else None
        xa=9.2+0.15*(i%3)
        L(ax,[(4.6,ys[i]),(4.6,ys[i])]) if False else None
        L(ax,[(4.6,ys[i]),(xa,ys[i]) if False else (4.6,ys[i])]) if False else None
    else:
        pass
for (kind,i),(px,py) in zip(order,ins):
    if kind=="a":
        ox,oy=outs[i]; xa=ox+0.4
        L(ax,[(ox,oy),(xa,oy),(xa,py),(px,py)])
    else:
        # route above/below the gates
        yy=ys[i]; xa=9.3+0.25*[1,5,7].index(i)
        ytr=yy
        L(ax,[(4.6,yy),(4.6+0.0,yy)])
        L(ax,[(4.6,yy),(5.0,yy),(5.0,yy+(0.0)),(xa,yy)]) if False else None
        L(ax,[(4.6,yy),(xa,yy),(xa,py),(px,py)])
L(ax,[o,(o[0]+0.5,o[1])]); T(ax,o[0]+0.6,o[1],"X",ha="left",size=9)
T(ax,6.2,6.6,"D' from a NOT gate",size=7.6,color=MUTED,ha="left")
'''
    return code

def decoder_text():
    ones = [0, 2, 3, 7, 8, 10, 11, 14, 15]
    rows = []
    for abc in range(8):
        pair = [int(2 * abc + d in ones) for d in (0, 1)]
        f = {(0, 0): "0", (1, 1): "1", (1, 0): "$\\overline{D}$", (0, 1): "$D$"}[(pair[0], pair[1])]
        rows.append([format(abc, "03b"), pair[0], pair[1], f])
    ks, terms = kmap_solution(ones, [], 4, "ABCD", "X")
    return ("**Realisation with a single 3×8 decoder.** The function has four variables but the decoder has only three inputs. Apply $A, B, C$ to the decoder (outputs $y_0\\dots y_7$ are the minterms of $ABC$, $y_k = 1$ when $ABC = k$) and handle $D$ with a few gates. For each value of $ABC$ look at the pair of minterms $m_{2k}$ ($D=0$) and $m_{2k+1}$ ($D=1$):\n\n" +
            tbl(["ABC", "D = 0 (m2k)", "D = 1 (m2k+1)", "X contains"], rows) +
            "\nSo (using the decoder outputs $y_k$ and $D$):\n\n$$X = y_0\\overline{D} + y_1 + y_3 D + y_4\\overline{D} + y_5 + y_7$$\n\n"
            "(checked against all 16 input combinations). Three AND gates, one NOT gate and a 6-input OR gate, together with the 3×8 decoder, give the function.\n\n" +
            figblock("X(A,B,C,D) = Σm(0,2,3,7,8,10,11,14,15) with one 3×8 decoder (A,B,C), three AND gates, an inverter for D and a 6-input OR gate.", decoder_realisation(), canvas=False) +
            "\n**Simplification by K-map.**\n\n" + ks)

def ttl_nor():
    code = r'''
fig,ax=ckt_canvas(5.9,3.9,xlim=(-2.0,17.0),ylim=(-1.8,8.6))
T(ax,7.5,8.2,"+V$_{CC}$ (5 V)",size=8.6)
L(ax,[(0,7.8),(15,7.8)],lw=1.6)
# input stages
for k,(nm,x) in enumerate((("A",1.0),("B",5.0))):
    res(ax,(x,7.8),(x,5.8),"4 kΩ",side=1,body=0.9,off=1.0)
    box(ax,x-0.7,3.8,1.4,1.4,"Q1%s\n(input)"%nm,size=7.6)
    L(ax,[(x,5.8),(x,5.2)])
    L(ax,[(x-0.7,4.5),(x-1.3,4.5)]); T(ax,x-1.4,4.5,nm,ha="right",size=9)
    # collector to phase splitter
    L(ax,[(x,3.8),(x,3.2)]); box(ax,x-0.7,1.8,1.4,1.4,"Q2%s\n(splitter)"%nm,size=7.6)
    L(ax,[(x,1.8),(x,1.2)])
# common emitter node of splitters
L(ax,[(1.0,1.2),(5.0,1.2)]); dot(ax,3.0,1.2); res(ax,(3.0,1.2),(3.0,-0.6),"1 kΩ",side=1,body=0.8,off=1.0); gnd(ax,(3.0,-0.6))
# common collectors (tied via 1.6 k to Vcc) go to the totem-pole
L(ax,[(0.3,3.5),(0.3,6.6),(8.0,6.6)]) if False else None
res(ax,(8.0,7.8),(8.0,6.4),"1.6 kΩ",side=1,body=0.8,off=1.1)
L(ax,[(8.0,6.4),(8.0,5.6),(5.8,5.6),(5.8,2.5),(5.7,2.5)]) if False else None
L(ax,[(8.0,6.4),(8.0,2.5)]); L(ax,[(1.7,2.5),(8.0,2.5)]); dot(ax,8.0,2.5)
L(ax,[(1.7,2.5),(1.7,2.5)])
L(ax,[(5.7,2.5),(5.7,2.5)])
# totem pole
box(ax,9.4,5.4,1.6,1.0,"Q3",size=8.2); box(ax,9.4,1.8,1.6,1.0,"Q4",size=8.2)
res(ax,(10.2,7.8),(10.2,6.4),"130 Ω",side=1,body=0.7,off=1.0)
L(ax,[(10.2,5.4),(10.2,4.8)]); diode(ax,(10.2,4.8),(10.2,3.6),None,side=1) if True else None
L(ax,[(10.2,3.6),(10.2,2.8)]); dot(ax,10.2,4.2)
L(ax,[(8.0,5.9),(9.4,5.9)]) ; dot(ax,8.0,5.9)
L(ax,[(8.0,2.3),(9.4,2.3)]); 
L(ax,[(10.2,1.8),(10.2,-0.6)]); gnd(ax,(10.2,-0.6))
L(ax,[(11.0,3.6),(13.0,3.6)]) if False else None
L(ax,[(10.2,4.2),(13.0,4.2)]); T(ax,13.1,4.2,"Y = $\\overline{A+B}$",ha="left",size=8.8)
T(ax,13.2,1.0,"Q2A, Q2B in parallel:\nY = 0 if A or B is high",size=7.6,color=MUTED,ha="left")
'''
    return code

def ttl_nor_text():
    return ("**Two-input TTL NOR gate.** The circuit has three parts: (i) two **input transistors** $Q_{1A}$, $Q_{1B}$ with their own base resistors (4 kΩ), one for each input, (ii) two **phase-splitter transistors** $Q_{2A}$, $Q_{2B}$ connected **in parallel** (collectors tied, emitters tied) and (iii) the **totem-pole output stage** $Q_3$ (pull-up) and $Q_4$ (pull-down) with a diode and 130 Ω resistor.\n\n" +
            figblock("Simplified circuit of a 2-input TTL NOR gate (each input has its own input transistor and phase splitter; the splitters are in parallel, then the totem-pole output).", ttl_nor(), canvas=False) +
            "\n**Logic operation.**\n\n"
            "- **A = B = 0 (low):** both input transistors conduct through their emitters, which steals the base current of the splitters, so $Q_{2A}$ and $Q_{2B}$ are both OFF. The common collector node goes high: $Q_3$ conducts and $Q_4$ is off, so the output is high, $Y\\approx 3.4$ V (logic 1).\n"
            "- **A = 1, B = 0 (or A = 0, B = 1):** the input transistor of the high input is reverse biased and its collector current drives the base of its splitter; that splitter $Q_2$ saturates. Because the splitters are in parallel, one conducting transistor is enough to pull the collector node low and to drive $Q_4$ into saturation while $Q_3$ is off: $Y\\approx0.2$ V (logic 0).\n"
            "- **A = B = 1:** both splitters conduct, $Q_4$ saturates, $Y = 0$.\n\n" +
            tbl(["A", "B", "Q2A", "Q2B", "Q3", "Q4", "Y = (A+B)'"], [[0, 0, "off", "off", "on", "off", 1], [0, 1, "off", "on", "off", "on", 0], [1, 0, "on", "off", "off", "on", 0], [1, 1, "on", "on", "off", "on", 0]]) +
            "\nThe output is low whenever *any* input is high, i.e. $Y = \\overline{A+B}$ (NOR).\n")

def cmos_char():
    return ("**Characteristics of the CMOS logic family.**\n\n"
            "- **Basic structure:** complementary pair of enhancement MOSFETs (PMOS pull-up network, NMOS pull-down network) with the same inputs; only one network conducts in a steady state.\n"
            "- **Supply voltage:** wide range, 3 to 15 V for the 4000B series (2 to 6 V for 74HC), so it can run from a battery.\n"
            "- **Logic levels:** $V_{OH}\\approx V_{DD}$ and $V_{OL}\\approx 0$ V (full rail-to-rail swing); $V_{IL}\\approx 0.3\\,V_{DD}$, $V_{IH}\\approx 0.7\\,V_{DD}$.\n"
            "- **Noise margin:** very high, about 45 % of $V_{DD}$ (≈ 2.25 V at 5 V, ≈ 4.5 V at 10 V).\n"
            "- **Power dissipation:** extremely low static power (≈ 10 nW per gate); dynamic power $P = C_L V_{DD}^2 f$ grows with frequency.\n"
            "- **Propagation delay:** about 50 ns for 4000B at 5 V (higher than TTL), 8 ns for 74HC.\n"
            "- **Fan-out:** very high (> 50) because the MOS input draws almost no DC current (input resistance ≈ $10^{12}$ Ω); the limit is the capacitive load.\n"
            "- **Packing density:** high, since the gates need no resistors, so CMOS is used for LSI/VLSI (microprocessors, memories).\n"
            "- **Unused inputs** must never be left floating (static charge can damage the thin gate oxide and cause excess power): tie to $V_{DD}$ or ground; handle with anti-static care.\n"
            "- **Speed-power product:** about 1 pJ at low frequency, the best of all families.\n")

def hex_oct():
    return ("**(a) $(6E.2C)_{16} = (?)_8$.** Convert each hex digit to 4 bits, regroup the bits in threes **from the radix point outwards**:\n\n"
            "$$6E.2C = 0110\\ 1110.\\ 0010\\ 1100 = 001\\ 101\\ 110.\\ 001\\ 011\\ 000$$\n\n"
            "Integer part: $001\\,101\\,110 = 1,5,6$; fractional part: $001\\,011\\,000 = 1,3,0$ (the last 0 is only padding). So\n\n"
            "$$\\boxed{(6E.2C)_{16} = (156.13)_8}$$\n\n"
            "Check in decimal: $6E_{16} = 110$, $156_8 = 64+40+6 = 110$ ✓; $0.2C_{16} = 2/16 + 12/256 = 0.171875$ and $0.13_8 = 1/8 + 3/64 = 0.171875$ ✓.\n\n"
            "**(b) $(10110110)_{Gray} = (?)_2$.** " + gray_to_binary("10110110"))

def seg_f():
    ones = [0, 4, 5, 6, 8, 9]; dcs = list(range(10, 16))
    tb = []
    for n in range(10):
        tb.append([n, *format(n, "04b"), 1 if n in ones else 0])
    tb += [[f"{n} - 15", "X", "X", "X", "X", "X"] for n in (10,)]
    ks, terms = kmap_solution(ones, dcs, 4, "ABCD", "f")
    return ("**BCD-to-seven-segment decoder, segment f.** The seven segments are labelled a (top), b, c, d (bottom), e, f (upper left), g (middle). The BCD inputs are $A$ (MSB) $B\\,C\\,D$ (LSB); segment f must be lit for the digits whose shape has the upper-left vertical bar: **0, 4, 5, 6, 8, 9** (digit 7 is drawn without it; the codes 10 to 15 never occur, so they are don't cares).\n\n" +
            tbl(["Digit", "A", "B", "C", "D", "f"], tb) + "\n" + ks)

def mux_y():
    ones = [0, 2, 3, 5, 7]
    data = ["$\\overline{C}$", "1", "C", "C"]
    code = f'''
fig,ax=ckt_canvas(5.9,2.8,xlim=(-3.0,9.0),ylim=(-1.8,3.6))
m=mux(ax,3.0,1.0,4,{data!r},["A","B"],out="Y",name="4:1 MUX")
'''
    code2 = r'''
fig,ax=ckt_canvas(5.9,3.0,xlim=(-1.8,13.0),ylim=(-0.6,6.2))
# S/D = A xor B ; C/Bo = (A xor M).B
ins,o=gate(ax,"XOR",3.0,5.0,w=1.2,h=0.9,lead=0.4)
T(ax,ins[0][0]-0.15,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.15,ins[1][1],"B",ha="right")
T(ax,o[0]+0.15,o[1],"Sum / Difference",ha="left",size=8.4)
L(ax,[(ins[0][0]-0.15,ins[0][1]),(ins[0][0]-0.15,ins[0][1])])
ins2,o2=gate(ax,"XOR",3.0,2.8,w=1.2,h=0.9,lead=0.4)
T(ax,ins2[0][0]-0.15,ins2[0][1],"A",ha="right"); T(ax,ins2[1][0]-0.15,ins2[1][1],"M",ha="right")
ins3,o3=gn(ax,"AND",6.8,2.1,n=2,w=0.9,lead=0.4)
L(ax,[o2,(6.0,o2[1]),(6.0,ins3[0][1]),ins3[0]])
T(ax,ins3[1][0]-0.1,ins3[1][1],"B",ha="right")
T(ax,o3[0]+0.15,o3[1],"Carry / Borrow",ha="left",size=8.4)
T(ax,1.0,0.2,"M = 0: half adder     M = 1: half subtractor",size=8,color=MUTED,ha="left")
'''
    return code, code2

def y_text():
    code, code2 = mux_y()
    return ("**(a) Implementation of $Y(A,B,C) = \\sum m(0,2,3,5,7)$ with one 4:1 MUX.** Use $A$ and $B$ as select lines ($S_1=A$, $S_0=B$) and $C$ as data. For each $AB$ the pair of minterms $(C=0, C=1)$ gives the data input (implementation table):\n\n" +
            tbl(["Select AB", "Minterms (C = 0, C = 1)", "Y for C = 0 / 1", "Data input"], [["00", "m0, m1", "1 / 0", "$\\overline{C}$ (I0)"], ["01", "m2, m3", "1 / 1", "1 (I1)"], ["10", "m4, m5", "0 / 1", "C (I2)"], ["11", "m6, m7", "0 / 1", "C (I3)"]]) +
            "\n$$Y = \\overline{A}\\,\\overline{B}\\,\\overline{C} + \\overline{A}B + AC$$\n\n" +
            figblock("Y(A,B,C) = Σm(0,2,3,5,7) with a single 4:1 multiplexer (data inputs C', 1, C, C).", code, canvas=False) +
            "\n**(b) One circuit for both the half adder and the half subtractor.**\n\n"
            "Half adder: $S = A\\oplus B$, $C = AB$. Half subtractor: $D = A\\oplus B$, $B_o = \\overline{A}B$. The sum and the difference are the same, only the second output differs; with a control input $M$ (0 = add, 1 = subtract):\n\n"
            "$$\\text{Sum/Difference} = A\\oplus B, \\qquad \\text{Carry/Borrow} = (A\\oplus M)\\cdot B$$\n\n" +
            tbl(["M", "A", "B", "Sum / Diff", "Carry / Borrow = (A⊕M)B"], [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 1], [1, 0, 0, 0, 0], [1, 0, 1, 1, 1], [1, 1, 0, 1, 0], [1, 1, 1, 0, 0]]) +
            "\nFor $M=0$: $(A\\oplus0)B = AB$ (carry); for $M=1$: $(A\\oplus1)B = \\overline{A}B$ (borrow). Two XOR gates and one AND gate are enough:\n\n" +
            figblock("Combined half adder / half subtractor with control input M (two XOR gates and an AND gate).", code2, canvas=False))

def updown_async():
    code, tm1, tm2 = async_updown3_neg()
    return ("**3-bit asynchronous up/down counter with negative-edge triggering.** Three T flip-flops (JK with $J=K=1$) that toggle on the **falling** edge of their clock input are cascaded. The first flip-flop gets the external clock. For the others the clock source depends on the mode input $M$:\n\n"
            "- **Up counting ($M=0$):** the clock of $FF_{i+1}$ is $Q_i$. A falling edge of $Q_i$ means a 1→0 change, i.e. a carry, so the next bit toggles - exactly the ripple up counter.\n"
            "- **Down counting ($M=1$):** the clock of $FF_{i+1}$ is $\\overline{Q_i}$. $\\overline{Q_i}$ falls when $Q_i$ rises (0→1), i.e. when the lower bit borrows from the higher one.\n\n"
            "The selection is made by two AND gates and an OR gate per stage: $CLK_{i+1} = \\overline{M}\\,Q_i + M\\,\\overline{Q_i}$.\n\n" +
            figblock("3-bit asynchronous up/down counter with falling-edge triggered T flip-flops; M selects Q (up) or Q' (down) as the clock of the next stage.", code, canvas=False) +
            "\n**Count sequences.**\n\n" + tbl(["Pulse", "Up: Q2 Q1 Q0", "Down: Q2 Q1 Q0"], [[k, format(k % 8, "03b"), format((7 - k) % 8, "03b")] for k in range(9)]) +
            "\nIn the up mode the counter counts $000, 001, \\dots, 111, 000$; in the down mode it counts $111, 110, \\dots, 000, 111$.\n\n" + tm1 + tm2 +
            "\nEach stage adds a propagation delay, so the outputs ripple; the maximum clock frequency is $1/(3\\,t_{pd}+t_{gate\\ delays})$.\n")

def paper_c():
    Q = []
    Q.append((1, "Define an ASCII code. Use 2's complement method to perform the following addition $(-28 + 12)_{10}$ in 8-bit signed number representation. [[1+3]]"))
    Q.append((2, "Prove the following: [[2×2]]\n\na) $AB + \\overline{A}C + BC = AB + \\overline{A}C$\n\nb) $AB + C(A\\oplus B) = BC + A(B+C)$"))
    Q.append((3, "What is a decoder? Design an octal priority encoder with neat circuit diagram. [[2+6]]"))
    Q.append((4, "Realize the following Boolean function using a single 3×8 decoder. Also simplify the logic function implementing K-map method. [[3+3]]\n\n$X(A,B,C,D) = \\sum m(0,2,3,7,8,10,11,14,15)$"))
    Q.append((5, "Design a synchronous 2-bit up/down counter using T flip-flops. [[7]]"))
    Q.append((6, "Explain the operation of 4-bit parallel-in serial-out (PISO) shift register with necessary circuit and timing diagram for 1101 input data. [[3+2]]"))
    Q.append((7, "Sketch the circuit diagram of mod-12 asynchronous counter having positive-edge triggering clock system implementing JK flip-flops with neat timing diagram. [[3+3]]"))
    Q.append((8, "Design a sequential machine that consists of one input, X and one output, Z. The machine is required to give output high (Y=1), whenever it detects the serial sequence of 010 from its input data stream X. Implement only D flip-flops for the designed circuit realization. [[10]]"))
    Q.append((9, "Draw the circuit diagram of two-input CMOS NAND gate and explain its logic operation briefly and list the characteristics of TTL logic family. [[4+2]]"))
    Q.append((10, "With the help of functional diagram explain the operation of time measuring circuit. [[4]]"))
    S = []
    S.append((1, ascii_def() + "\n**Addition of $(-28)+12$ in 8-bit 2's complement.**\n\n" + twos_add()))
    S.append((2, proofs()))
    S.append((3, priority_text()))
    S.append((4, decoder_text()))
    tr = {(s, m): (((s + 1) % 4) if m == 0 else ((s - 1) % 4), None) for s in range(4) for m in (0, 1)}
    ct, _ = counter_text("the synchronous 2-bit up/down counter with T flip-flops", 2, "T", tr, extra=1, extra_names=("M",),
                         seq_for_timing=count_states(lambda s: (s + 1) % 4, 8),
                         timing_cap="Timing diagram of the 2-bit up/down counter in the up mode (M = 0): 00, 01, 10, 11, 00, ... ; in the down mode (M = 1) the sequence is reversed: 00, 11, 10, 01, 00.")
    ct += "\nHere $M = 0$ selects up counting and $M = 1$ selects down counting. Check: for $M=0$, $T_0 = 1$ and $T_1 = Q_0$ (the usual up counter); for $M=1$, $T_1 = \\overline{Q_0}$ (down counter).\n"
    S.append((5, ct))
    S.append((6, piso_text("1101")))
    S.append((7, async_mod12()))
    dt, _ = detector_text("010", "D")
    S.append((8, dt))
    S.append((9, cmos_nand_text() + "\n" + ttl_char()))
    S.append((10, time_measure_text()))
    md = front("Digital-Logic-EX152-2082-Baishakh", "Digital Logic", "EX 152", "2082 Baishakh", 2025, "BCT, BEI", "Back paper (new course)")
    return md + qs(Q) + ss(S)

def paper_d():
    Q = []
    Q.append((1, "Mention merits and demerits of digital signal over analog signal. [[2]]"))
    Q.append((2, "Perform the following as indicated: [[2×1.5]]\n\na) $(6E.2C)_{16} = (?)_8$\n\nb) $(10110110)_{Gray} = (?)_2$"))
    Q.append((3, "Design the simplest logic circuit for 'f' segment for the BCD-to-seven segment display decoder. [[4]]"))
    Q.append((4, "Implement $Y(A,B,C) = \\sum m(0,2,3,5,7)$ using only a single 1:4 MUX. Design a circuit which can realize both the half-adder and the half-subtractor in a single circuit. [[3+7]]"))
    Q.append((5, "Design a mod-6 synchronous down counter using JK flip-flops. [[7]]"))
    Q.append((6, "Explain the operation of 4-bit serial-in parallel-out (SIPO) shift register with necessary circuit and timing diagram for input data of 1011. [[3+3]]"))
    Q.append((7, "Describe briefly the operation of 3 bit up/down asynchronous counter having negative edge triggering clock system with neat circuit diagram and timing diagram. [[4+3]]"))
    Q.append((8, "Design a sequential machine that consists of one input, X and one output, Z. The machine is required to give output high (Y=1), whenever it detects the serial sequence of 101 from its input data stream X. Implement only SR flip-flops for the designed circuit realization. [[10]]"))
    Q.append((9, "Draw the circuit diagram of two-input TTL NOR gate and explain its logic operation briefly and list the characteristics of CMOS logic family. [[5+2]]"))
    Q.append((10, "With the help of functional diagram explain the operation of frequency measurement. [[4]]"))
    S = []
    S.append((1, merits_demerits()))
    S.append((2, hex_oct()))
    S.append((3, seg_f()))
    S.append((4, y_text()))
    tr = {(s, 0): ((s - 1) % 6, None) for s in range(6)}
    ct, _ = counter_text("the synchronous mod-6 down counter with JK flip-flops", 3, "JK", tr, unused="110 and 111",
                         seq_for_timing=count_states(lambda s: (s - 1) % 6, 8, 5),
                         timing_cap="Timing diagram of the mod-6 down counter: 101, 100, 011, 010, 001, 000, 101, ... Each output changes just after the rising clock edge.")
    S.append((5, ct))
    S.append((6, sipo_text("1011")))
    S.append((7, updown_async()))
    dt, _ = detector_text("101", "SR")
    S.append((8, dt))
    S.append((9, ttl_nor_text() + "\n" + cmos_char()))
    S.append((10, freq_measure_text()))
    md = front("Digital-Logic-EX152-2081-Ashwin", "Digital Logic", "EX 152", "2081 Ashwin", 2024, "BEI, BCT", "Regular (new course, 2080 batch)")
    return md + qs(Q) + ss(S)

if __name__ == "__main__":
    for nm, fn in (("ioe-ex152-2082-baishakh", paper_c), ("ioe-ex152-2081-ashwin", paper_d), ("ioe-enex152-2083-baishakh", paper_a), ("ioe-enex152-2082-bhadra", paper_b)):
        md = fn()
        open(f"{OUT}/{nm}.md", "w").write(md); print(nm, len(md))
