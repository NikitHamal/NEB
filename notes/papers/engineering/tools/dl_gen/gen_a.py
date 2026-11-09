import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from texts3 import *

OUT = "/app/notes/papers/engineering/content"

def front(file, subject, code, yr, yad, stream, kind, note=""):
    return f"""---
file: NEBians-IOE-Past-Paper-{file}.pdf
subject: {subject}
level: BE · Year I / Part II
code: {code}
year_bs: {yr}
cal: BS
year_ad: {yad}
stream: {stream}
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. {kind}. Pass marks 24.{note}
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

"""

def qs(items):
    return "".join(f"@q {i}\n{t}\n\n" for i, t in items)

def ss(items):
    return "<!-- SOLUTIONS -->\n\n" + "".join(f"@s {i}\n{t}\n\n" for i, t in items)

def fs_mux():
    d_lab = ["B$_{in}$", "$\\overline{B_{in}}$", "$\\overline{B_{in}}$", "B$_{in}$"]
    b_lab = ["B$_{in}$", "1", "0", "B$_{in}$"]
    code = f'''
fig,ax=ckt_canvas(5.9,2.3,xlim=(-3.2,17.4),ylim=(-2.2,3.2))
m1=mux(ax,3.0,0.6,4,{d_lab!r},["A","B"],out="Diff",name="4:1 MUX (difference)")
m2=mux(ax,12.0,0.6,4,{b_lab!r},["A","B"],out="Bout",name="4:1 MUX (borrow)")
T(ax,7.5,-2.0,"select lines A (S1) and B (S0) are common to both multiplexers",size=7.6,color=MUTED)
'''
    return figblock("Full subtractor with two 4:1 multiplexers (A = S1, B = S0; the data inputs are Bin, its complement, 0 or 1).", code, canvas=False)

def fs_text():
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                dd = a ^ b ^ c; bo = int((not a and b) or (not a and c) or (b and c))
                rows.append([a, b, c, dd, bo])
    return ("**Full subtractor.** It subtracts $A - B - B_{in}$ and gives the difference $D$ and borrow-out $B_{out}$.\n\n" +
            tbl(["A", "B", "Bin", "Diff", "Bout"], rows) +
            "\n$$D = A\\oplus B\\oplus B_{in}, \\qquad B_{out} = \\overline{A}B + \\overline{A}B_{in} + B\\,B_{in}$$\n\n"
            "**Multiplexer implementation.** Take $A$ and $B$ as the select inputs of a 4:1 multiplexer ($S_1=A$, $S_0=B$) and express each output as a function of the remaining variable $B_{in}$ for each select combination (implementation table):\n\n" +
            tbl(["AB (select)", "Diff (data input)", "Bout (data input)"], [["00", "Bin", "Bin"], ["01", "$\\overline{B_{in}}$", "1"], ["10", "$\\overline{B_{in}}$", "0"], ["11", "Bin", "Bin"]]) +
            "\nCheck: for $AB=00$ the rows give $D=B_{in}$ and $B_{out}=B_{in}$; for $AB=01$, $D=\\overline{B_{in}}$ and $B_{out}=1$; for $AB=10$, $D=\\overline{B_{in}}$ and $B_{out}=0$; for $AB=11$, $D=B_{in}$, $B_{out}=B_{in}$. These agree with the 8 rows of the truth table.\n\n" +
            fs_mux() +
            "\nTwo 4:1 multiplexers and one NOT gate realise the full subtractor.\n")

def paper_a():
    Q = []
    Q.append((1, "Convert the following gray codes to binary codes. [[2+2]]\n\na) 10011\n\nb) 110001"))
    Q.append((2, "Differentiate between analog and digital signal. Convert 159 to excess-3 code. [[1+2]]"))
    Q.append((3, "Show that NAND and NOR gates are universal gates. [[3]]"))
    Q.append((4, "Minimize the function $F(A,B,C,D) = \\sum m(1, 2, 4, 5, 6, 8, 10, 11, 13, 15)$ using K-Map and realize it with suitable logic gates. [[5]]"))
    Q.append((5, "Differentiate between encoder and decoder. Design octal to binary encoder with necessary diagrams. [[2+4]]"))
    Q.append((6, "Implement a full subtractor circuit using multiplexer. [[4]]"))
    Q.append((7, "Differentiate between latch and flipflop. Modify a D flip-flop such that it functions as a JK flip-flop. [[2+5]]"))
    Q.append((8, "Explain the working of 4-bit SIPO register with timing diagram of 1010 data input. [[5]]"))
    Q.append((9, "Describe the operation of asynchronous BCD (decade) counter with necessary diagrams. [[5]]"))
    Q.append((10, "Design the synchronous mod-10 up counter using T flip-flop and draw its timing diagram also. [[7]]"))
    Q.append((11, "Design a synchronous sequential machine that has 1 bit serial input X and output Z which will be high when the input contains the message 011 (Use T Flip Flop). [[7]]"))
    Q.append((12, "Explain about the main characteristics of digital logic families. [[4]]"))
    S = []
    S.append((1, "**(a)** " + gray_to_binary("10011") + "\n**(b)** " + gray_to_binary("110001") + "\n*Check by conversion back:* $11101 \\to$ Gray: $1,\\ 1\\oplus1=0,\\ 1\\oplus1=0,\\ 1\\oplus0=1,\\ 0\\oplus1 = 1$ gives 10011 ✓; $100001\\to 110001$ ✓.\n"))
    S.append((2, analog_vs_digital() + "\n**Excess-3 code of 159.**\n\n" + excess3(159) + "\nThe codeword has 12 bits, each decimal digit using its own 4-bit group, so $159 \\to 0100\\ 1000\\ 1100$.\n"))
    S.append((3, universal_text()))
    ks, _ = kmap_solution([1, 2, 4, 5, 6, 8, 10, 11, 13, 15], [], 4, "ABCD", "F")
    S.append((4, ks))
    S.append((5, encoder_decoder_diff() + "\n" + octal_encoder()))
    S.append((6, fs_text()))
    S.append((7, d_to_jk()))
    S.append((8, sipo_text("1010")))
    S.append((9, bcd_async()))
    tr = {(s, 0): ((s + 1) % 10, None) for s in range(10)}
    ct, _ = counter_text("the synchronous mod-10 up counter with T flip-flops", 4, "T", tr, unused="1010 to 1111",
                         seq_for_timing=count_states(lambda s: (s + 1) % 10, 12),
                         kmcs=0.7, timing_cap="Timing diagram of the synchronous mod-10 up counter: all outputs change together just after the rising clock edge; Q3 is high for counts 8 and 9 and the counter returns to 0000 on the tenth pulse (f/10 at Q3).", per_row=2)
    ct += "\nAll four flip-flops are clocked by the same pulse, so the outputs change together (no ripple delay) and the maximum clock frequency is limited only by one flip-flop delay plus the AND-gate delay.\n"
    S.append((10, ct))
    dt, _ = detector_text("011", "T")
    S.append((11, dt))
    S.append((12, logic_families()))
    md = front("Digital-Logic-ENEX152-2083-Baishakh", "Digital Logic", "ENEX 152", "2083 Baishakh", 2026, "BEI, BCT", "Back paper (new course)")
    md += qs(Q) + ss(S)
    return md

if __name__ == "__main__":
    md = paper_a()
    open(f"{OUT}/ioe-enex152-2083-baishakh.md", "w").write(md)
    print(len(md))
