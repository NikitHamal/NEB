import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_a import *

def fa_text():
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                rows.append([a, b, c, a ^ b ^ c, int(a + b + c >= 2)])
    d_lab = ["C", "$\\overline{C}$", "$\\overline{C}$", "C"]
    c_lab = ["0", "C", "C", "1"]
    code = f'''
fig,ax=ckt_canvas(5.9,2.3,xlim=(-3.2,17.4),ylim=(-2.2,3.2))
m1=mux(ax,3.0,0.6,4,{d_lab!r},["A","B"],out="Sum",name="4:1 MUX (sum)")
m2=mux(ax,12.0,0.6,4,{c_lab!r},["A","B"],out="Cout",name="4:1 MUX (carry)")
T(ax,7.5,-2.0,"select lines A (S1) and B (S0) are common to both multiplexers",size=7.6,color=MUTED)
'''
    return ("**Full adder.** It adds three bits $A$, $B$ and the carry-in $C$ (written $C_{in}$) and gives Sum and Carry-out:\n\n" +
            tbl(["A", "B", "C", "Sum", "Cout"], rows) +
            "\n$$S = A\\oplus B\\oplus C, \\qquad C_{out} = AB + BC + CA$$\n\n"
            "**Multiplexer implementation.** Use two 4:1 multiplexers with $A$ and $B$ on the select lines ($S_1 = A$, $S_0 = B$). For each of the four select combinations read the output as a function of the third variable $C$ (implementation table):\n\n" +
            tbl(["AB (select)", "Sum (data input)", "Cout (data input)"], [["00", "C", "0"], ["01", "$\\overline{C}$", "C"], ["10", "$\\overline{C}$", "C"], ["11", "C", "1"]]) +
            "\nCheck: for $AB=01$ the truth table rows $010 \\to (S,C_{out}) = (1,0)$ and $011 \\to (0,1)$ give $S=\\overline{C}$ and $C_{out}=C$; for $AB=00$: $000\\to(0,0)$, $001\\to(1,0)$ give $S=C$, $C_{out}=0$; for $AB=11$: $110\\to(0,1)$, $111\\to(1,1)$ give $S=C$, $C_{out}=1$.\n\n" +
            figblock("Full adder from two 4:1 multiplexers (A = S1, B = S0; data inputs are 0, 1, C and its complement).", code, canvas=False) +
            "\nOne NOT gate (for $\\overline{C}$) and two 4:1 multiplexers are enough. (With 8:1 multiplexers the select lines would be $A,B,C$ and the data inputs simply the constants of the truth table.)\n")

def comparator_text():
    # verify
    for a in range(8):
        for b in range(8):
            a2, a1, a0 = (a >> 2) & 1, (a >> 1) & 1, a & 1
            b2, b1, b0 = (b >> 2) & 1, (b >> 1) & 1, b & 1
            x2, x1, x0 = int(a2 == b2), int(a1 == b1), int(a0 == b0)
            gt = (a2 & (1 - b2)) | (x2 & a1 & (1 - b1)) | (x2 & x1 & a0 & (1 - b0))
            lt = ((1 - a2) & b2) | (x2 & (1 - a1) & b1) | (x2 & x1 & (1 - a0) & b0)
            eq = x2 & x1 & x0
            assert gt == int(a > b) and lt == int(a < b) and eq == int(a == b)
    xn = r'''
fig,ax=ckt_canvas(5.9,2.0,xlim=(-1.2,10.6),ylim=(-0.4,3.6))
for k,(a,b) in enumerate([("A2","B2"),("A1","B1"),("A0","B0")]):
    x0=1.0+3.4*k
    ins,o=gn(ax,"NOR",x0,2.0,n=2,w=0.9,lead=0.3) if False else (None,None)
import numpy as _np2
'''
    code1 = r'''
fig,ax=ckt_canvas(5.9,1.9,xlim=(-1.2,11.2),ylim=(-0.2,3.0))
for k,(a,b) in enumerate([("A2","B2"),("A1","B1"),("A0","B0")]):
    x0=1.2+3.7*k
    ins,o=gate(ax,"XNOR",x0,1.4,w=1.2,h=0.9,lead=0.4)
    T(ax,ins[0][0]-0.1,ins[0][1],a,ha="right",size=8.4); T(ax,ins[1][0]-0.1,ins[1][1],b,ha="right",size=8.4)
    T(ax,o[0]+0.12,o[1],"x%d"%(2-k),ha="left",size=8.6)
'''
    code2 = r'''
def row(ax,y0,terms,out):
    m=len(terms); pitch=1.5; ys=[y0-k*pitch for k in range(m)]; outs=[]
    for k,t in enumerate(terms):
        ins,o=gn(ax,"AND",4.0,ys[k],n=len(t),w=0.9,lead=0.3)
        for (px,py),lab in zip(ins,t): T(ax,px-0.08,py,lab,ha="right",size=8.2)
        outs.append(o)
    if m==1:
        L(ax,[outs[0],(outs[0][0]+0.5,outs[0][1])]); T(ax,outs[0][0]+0.6,outs[0][1],out,ha="left",size=8.8); return
    yc=sum(ys)/m
    ins,o=gn(ax,"OR",7.0,yc,n=m,sp=pitch,w=1.0,lead=0.3)
    for (px,py),(ox,oy) in zip(ins,outs): L(ax,[(ox,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=8.8)
fig,ax=ckt_canvas(5.9,6.2,xlim=(0.5,10.5),ylim=(-12.6,2.0))
row(ax,1.0,[["A2","B2'"],["x2","A1","B1'"],["x2","x1","A0","B0'"]],"A>B")
row(ax,-5.2,[["x2","x1","x0"]],"A=B")
row(ax,-8.2,[["A2'","B2"],["x2","A1'","B1"],["x2","x1","A0'","B0"]],"A<B")
T(ax,0.9,1.9,"(an apostrophe means the complemented input, obtained with a NOT gate)",size=7.4,color=MUTED,ha="left")
'''
    return ("**Magnitude comparator.** A magnitude comparator is a combinational circuit that compares two binary numbers $A$ and $B$ and tells whether $A>B$, $A=B$ or $A<B$ (three outputs, only one of which is 1).\n\n"
            "**Design of a 3-bit comparator** ($A=A_2A_1A_0$, $B=B_2B_1B_0$). Compare from the MSB downwards. Two bits of equal weight are equal when $x_i = A_i \\odot B_i = \\overline{A_i\\oplus B_i}$ (XNOR).\n\n"
            "$$(A=B) = x_2x_1x_0$$\n\n"
            "$A>B$ if the MSBs differ with $A_2=1, B_2=0$, **or** the MSBs are equal and the next bits satisfy $A_1=1,B_1=0$, **or** the two upper bits are equal and $A_0=1, B_0 = 0$; $A<B$ is the mirror image:\n\n"
            "$$\\begin{gathered} (A>B) = A_2\\overline{B_2} + x_2A_1\\overline{B_1} + x_2x_1A_0\\overline{B_0} \\\\ (A<B) = \\overline{A_2}B_2 + x_2\\overline{A_1}B_1 + x_2x_1\\overline{A_0}B_0 \\\\ (A=B) = x_2x_1x_0 \\end{gathered}$$\n\n"
            "(All three expressions were checked against the 64 input combinations.) A few rows of the function table:\n\n" +
            tbl(["A", "B", "A>B", "A=B", "A<B"], [["101", "011", 1, 0, 0], ["010", "010", 0, 1, 0], ["011", "100", 0, 0, 1], ["110", "111", 0, 0, 1], ["111", "110", 1, 0, 0]]) +
            "\n**Logic diagram.** The three XNOR gates give $x_2,x_1,x_0$, which feed the AND-OR networks of the three outputs:\n\n" +
            figblock("The three XNOR gates producing x2 = A2 xnor B2, x1 and x0.", code1, canvas=False) +
            figblock("Output logic of the 3-bit magnitude comparator (inputs x2, x1, x0 come from the XNOR gates above).", code2, canvas=False) +
            "\nThe same design cascades: an IC such as the 7485 compares 4 bits and has cascading inputs $(A>B)_{in}, (A=B)_{in}, (A<B)_{in}$ so that two ICs make an 8-bit comparator.\n")

def comb_vs_seq():
    return tbl(["Point", "Combinational circuit", "Sequential circuit"], [
        ["Output depends on", "Present inputs only", "Present inputs **and** the past (stored state)"],
        ["Memory", "None", "Flip-flops / latches store the state"],
        ["Clock", "Not needed", "Usually clocked (synchronous) or event driven"],
        ["Feedback", "No feedback path", "Outputs fed back to the inputs through the memory"],
        ["Building blocks", "Gates, adders, MUX, decoders", "Flip-flops + gates: counters, registers"],
        ["Speed", "Faster, only gate delays", "Slower, limited by clock and flip-flop delays"],
        ["Design tools", "Truth table, K-map", "State table, state diagram, excitation table"],
        ["Example", "Half adder, encoder, comparator", "Counter, shift register, sequence detector"]])

def paper_b():
    Q = []
    Q.append((1, "Convert the following binary codes to gray codes. [[2+2]]\n\na) 101101\n\nb) 110001"))
    Q.append((2, "What is 2's complement representation? Perform BCD addition of 23 + 48. [[1+2]]"))
    Q.append((3, "State and explain De Morgan's Theorem with truth table and necessary diagrams. [[4]]"))
    Q.append((4, "Minimize the function $F(A,B,C,D) = \\sum m(0,1,2,4,7,8,9,10,12,15) + d(5,11,13)$ using K-Map and realize it with suitable logic gates. [[5]]"))
    Q.append((5, "What is magnitude comparator? Design a 3-bit magnitude comparator. [[1+5]]"))
    Q.append((6, "Implement a full adder circuit using Multiplexer. [[4]]"))
    Q.append((7, "Differentiate between combinational circuit and sequential circuit. With necessary steps and implementation, convert SR flip flop into JK flip flop. [[2+5]]"))
    Q.append((8, "Write briefly about different types of shift registers. With necessary circuit and timing diagram, explain the operation of how the shift register is used as a Johnson's Counter. [[2+3]]"))
    Q.append((9, "Describe the operation of 3-bit ripple up counter with positive edge triggered clock. [[5]]"))
    Q.append((10, "Design the synchronous mod-6 counter using S R flip-flop and draw its timing diagram also. [[7]]"))
    Q.append((11, "Design a synchronous sequential machine that has 1 bit serial input X and output Z which will be high when the input contains the message 110 (Use SR Flip Flop). [[7]]"))
    Q.append((12, "Write a short note on frequency counter. [[3]]"))
    S = []
    S.append((1, "**(a)** " + binary_to_gray("101101") + "\n**(b)** " + binary_to_gray("110001")))
    S.append((2, twos_complement_def() + "\n**BCD addition of 23 + 48.**\n\n" + bcd_add(23, 48)))
    S.append((3, demorgan()))
    ks, _ = kmap_solution([0, 1, 2, 4, 7, 8, 9, 10, 12, 15], [5, 11, 13], 4, "ABCD", "F")
    S.append((4, ks))
    S.append((5, comparator_text()))
    S.append((6, fa_text()))
    S.append((7, comb_vs_seq() + "\n" + sr_to_jk()))
    S.append((8, shift_types() + "\n" + johnson()))
    S.append((9, async_up3()))
    tr = {(s, 0): ((s + 1) % 6, None) for s in range(6)}
    ct, _ = counter_text("the synchronous mod-6 counter with SR flip-flops", 3, "SR", tr, unused="110 and 111",
                         seq_for_timing=count_states(lambda s: (s + 1) % 6, 8),
                         timing_cap="Timing diagram of the synchronous mod-6 counter (states 000 to 101): Q2 is high for counts 4 and 5, so the output at Q2 has frequency f/6 (high for 2 of 6 clock periods).")
    S.append((10, ct))
    dt, _ = detector_text("110", "SR")
    S.append((11, dt))
    S.append((12, freq_measure_text()))
    md = front("Digital-Logic-ENEX152-2082-Bhadra", "Digital Logic", "ENEX 152", "2082 Bhadra", 2025, "BEI, BCT", "Regular (new course)")
    md += qs(Q) + ss(S)
    return md

if __name__ == "__main__":
    md = paper_b()
    open(f"{OUT}/ioe-enex152-2082-bhadra.md", "w").write(md)
    print(len(md))
