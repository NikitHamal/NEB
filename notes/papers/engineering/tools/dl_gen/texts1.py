from lib_logic import *

def tbl(h, rows):
    s = "| " + " | ".join(h) + " |\n|" + "---|" * len(h) + "\n"
    for r in rows: s += "| " + " | ".join(str(c) for c in r) + " |\n"
    return s

# ---------------- number systems / codes ----------------
def g2b_steps(g):
    b = [int(g[0])]
    for c in g[1:]: b.append(b[-1] ^ int(c))
    return "".join(map(str, b))

def b2g(b):
    return b[0] + "".join(str(int(b[i - 1]) ^ int(b[i])) for i in range(1, len(b)))

def gray_to_binary(g):
    b = g2b_steps(g)
    steps = [f"$b_1 = g_1 = {g[0]}$"]
    for i in range(1, len(g)):
        steps.append(f"$b_{i+1} = b_{i} \\oplus g_{i+1} = {b[i-1]} \\oplus {g[i]} = {b[i]}$")
    return (f"Rule: the MSB of the binary code equals the MSB of the Gray code; every other binary bit is $b_i = b_{{i-1}} \\oplus g_i$.\n\n- " + "\n- ".join(steps) +
            f"\n\n$$({g})_{{Gray}} = ({b})_2$$\n")

def binary_to_gray(b):
    g = b2g(b)
    steps = [f"$g_1 = b_1 = {b[0]}$"]
    for i in range(1, len(b)):
        steps.append(f"$g_{i+1} = b_{i} \\oplus b_{i+1} = {b[i-1]} \\oplus {b[i]} = {g[i]}$")
    return (f"Rule: the MSB of the Gray code equals the MSB of the binary code; every other Gray bit is $g_i = b_{{i-1}} \\oplus b_i$.\n\n- " + "\n- ".join(steps) +
            f"\n\n$$({b})_2 = ({g})_{{Gray}}$$\n")

def excess3(n):
    digs = [int(c) for c in str(n)]
    rows = [(d, d + 3, format(d + 3, "04b")) for d in digs]
    code = " ".join(format(d + 3, "04b") for d in digs)
    return ("Excess-3 code = BCD code of the digit + 3 (0011), taken digit by digit.\n\n" +
            tbl(["Digit", "Digit + 3", "Excess-3"], rows) + f"\n$$({n})_{{10}} = ({code})_{{XS-3}}$$\n")

def analog_vs_digital():
    return tbl(["Point", "Analog signal", "Digital signal"], [
        ["Values", "Continuous in amplitude and time", "Discrete levels (two for binary: 0 and 1)"],
        ["Representation", "Continuously varying voltage/current (sine wave)", "Sequence of bits, square pulses"],
        ["Noise immunity", "Poor, noise adds to the signal and cannot be removed", "Good, a threshold decides 0 or 1, so noise is rejected"],
        ["Storage and processing", "Difficult; processing by analog circuits", "Easy; memories, microprocessors, error correction"],
        ["Accuracy", "Limited by component tolerance and drift", "Set by the number of bits, can be made as high as required"],
        ["Examples", "Microphone output, temperature sensor, AM/FM radio", "Computer data, CD/DVD, digital TV"]])

def merits_demerits():
    return ("**Merits of digital signals over analog signals**\n\n"
            "- Better noise immunity: only two levels, so small noise never changes a bit; regenerative repeaters restore the signal exactly.\n"
            "- Easy storage in memory, easy processing/transmission by computers.\n"
            "- Error detection and correction by coding (parity, CRC, Hamming).\n"
            "- Easy encryption and compression, so secure and efficient communication is possible.\n"
            "- Circuits are IC-friendly, cheap, small and low power; precision is fixed by the number of bits.\n"
            "- Many signals (voice, data, video) can be time-multiplexed on a single channel.\n\n"
            "**Demerits**\n\n"
            "- Needs a larger bandwidth than analog for the same information (e.g. a voice channel needs 64 kb/s instead of 4 kHz).\n"
            "- Needs A/D and D/A converters for real-world (analog) signals, adding cost and quantisation error.\n"
            "- Needs accurate synchronisation between transmitter and receiver.\n"
            "- Sampling below the Nyquist rate produces aliasing; quantisation always leaves some error.\n"
            "- Digital circuits are slower to react than a simple analog circuit for tiny sub-problems and dissipate power when switching at high speed.\n")

def ascii_def():
    return ("**ASCII** (American Standard Code for Information Interchange) is a 7-bit alphanumeric code that represents $2^7 = 128$ characters: 10 digits, 26 upper-case and 26 lower-case letters, punctuation, and 33 control characters. An 8th bit (parity or extended set) makes it a byte.\n\n" +
            tbl(["Character", "Decimal", "7-bit ASCII", "Hex"], [["0", 48, "011 0000", "30"], ["9", 57, "011 1001", "39"], ["A", 65, "100 0001", "41"], ["Z", 90, "101 1010", "5A"], ["a", 97, "110 0001", "61"], ["Space", 32, "010 0000", "20"], ["CR (carriage return)", 13, "000 1101", "0D"]]))

def twos_complement_def():
    return ("**2's complement representation.** In an $n$-bit signed number the MSB is the sign bit (0 for positive, 1 for negative). A positive number is written in ordinary binary. A negative number $-N$ is stored as $2^n - N$, i.e. the **2's complement** of $N$:\n\n"
            "1. write $N$ in $n$-bit binary, 2. invert every bit (1's complement), 3. add 1.\n\n"
            "Range of an $n$-bit number: $-2^{n-1}$ to $+(2^{n-1}-1)$, and 0 has only one representation. Subtraction becomes addition, so one adder serves for both, which is why every computer uses it. Example (4 bits): $-5$: $0101 \\to 1010 \\to 1011$.\n")

def twos_add():
    return ("$+12 = 0000\\,1100$. $28 = 0001\\,1100$, so $-28$: invert $\\to 1110\\,0011$, add 1 $\\to 1110\\,0100$.\n\n"
            "$$\\begin{array}{r@{\\;}l} & 1110\\,0100 \\quad(-28) \\\\ + & 0000\\,1100 \\quad(+12) \\\\ \\hline & 1111\\,0000 \\end{array}$$\n\n"
            "No carry out of the MSB position and the sign bit is 1, so the result is negative and is in 2's complement form. Magnitude: invert $1111\\,0000 \\to 0000\\,1111$, add 1 $\\to 0001\\,0000 = 16$.\n\n"
            "$$(-28) + 12 = -16 \\quad\\Rightarrow\\quad \\boxed{1111\\,0000}_2 \\ (\\text{no overflow, since the operands have different signs})$$\n")

def bcd_add(a, b):
    sa, sb = str(a), str(b)
    da = [int(c) for c in sa]; db = [int(c) for c in sb]
    out = f"BCD addition: add the two BCD numbers as ordinary binary; any 4-bit group greater than 9 (or with a carry out) is corrected by adding $0110_2$ ($6$).\n\n"
    fa = " ".join(format(d, "04b") for d in da); fb = " ".join(format(d, "04b") for d in db)
    s = a + b
    # units
    u1 = da[-1] + db[-1]; t1 = da[0] + db[0]
    out += f"$$({a})_{{BCD}} = {fa}, \\qquad ({b})_{{BCD}} = {fb}$$\n\n"
    ulow = u1
    out += f"- Units: ${format(da[-1],'04b')} + {format(db[-1],'04b')} = {format(u1,'05b')}$ ({u1}). "
    carry = 0
    if u1 > 9:
        fixed = u1 + 6
        out += f"Since {u1} > 9, add 0110: ${format(u1,'04b')} + 0110 = {format(fixed,'05b')}$, giving the digit ${format(fixed & 15,'04b')}$ and a carry 1 into the tens.\n"
        carry = 1; ud = fixed & 15
    else:
        out += "Valid BCD digit, no correction.\n"; ud = u1
    t2 = t1 + carry
    out += f"- Tens: ${format(da[0],'04b')} + {format(db[0],'04b')} + {carry} = {format(t2,'04b')}$ ({t2}); "
    if t2 > 9:
        out += "needs correction (not needed here).\n"
    else:
        out += "a valid digit, no correction.\n"
    out += f"\n$$\\begin{{array}}{{r@{{\\;}}l}} & {fa} \\\\ + & {fb} \\\\ \\hline & {format(t1,'04b')}\\ {format(u1,'04b')} \\\\ + & 0000\\ 0110 \\quad(\\text{{units corrected}}) \\\\ \\hline & {format(t2,'04b')}\\ {format(ud,'04b')} \\end{{array}}$$\n\n"
    out += f"$$23 + 48 = {s} \\quad\\Rightarrow\\quad \\boxed{{{format(t2,'04b')}\\ {format(ud,'04b')}}}_{{BCD}} = ({s})_{{10}}$$\n" if (a, b) == (23, 48) else ""
    return out

# ---------------- Boolean algebra ----------------
def demorgan():
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            rows.append([a, b, int(not (a or b)), int((not a) and (not b)), int(not (a and b)), int((not a) or (not b))])
    code = r'''
fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.2,13.0),ylim=(-0.4,4.9))
# law 1: NOR = bubbled AND
ins,o=gn(ax,"NOR",1.0,3.8,n=2,w=1.0,lead=0.4); T(ax,0.2,4.05,"A",ha="right"); T(ax,0.2,3.55,"B",ha="right"); T(ax,o[0]+0.15,3.8,"$\\overline{A+B}$",ha="left"); T(ax,3.3,3.8,"=",size=11)
ins2,o2=gn(ax,"AND",6.0,3.8,n=2,w=1.0,lead=0.3)
for (px,py),nm in zip(ins2,"AB"):
    iin,iout=inv(ax,px-0.95,py,w=0.5,h=0.5,lead=0.15); L(ax,[iout,(px,py)]); T(ax,iin[0]-0.1,py,nm,ha="right")
T(ax,o2[0]+0.15,3.8,"$\\overline{A}\\,\\overline{B}$",ha="left"); T(ax,9.9,3.8,"NOR = bubbled AND",size=8,ha="left",color=MUTED)
# law 2: NAND = bubbled OR
ins,o=gn(ax,"NAND",1.0,1.5,n=2,w=1.0,lead=0.4); T(ax,0.2,1.75,"A",ha="right"); T(ax,0.2,1.25,"B",ha="right"); T(ax,o[0]+0.15,1.5,"$\\overline{AB}$",ha="left"); T(ax,3.3,1.5,"=",size=11)
ins2,o2=gn(ax,"OR",6.0,1.5,n=2,w=1.0,lead=0.3)
for (px,py),nm in zip(ins2,"AB"):
    iin,iout=inv(ax,px-0.95,py,w=0.5,h=0.5,lead=0.15); L(ax,[iout,(px,py)]); T(ax,iin[0]-0.1,py,nm,ha="right")
T(ax,o2[0]+0.15,1.5,"$\\overline{A}+\\overline{B}$",ha="left"); T(ax,9.9,1.5,"NAND = bubbled OR",size=8,ha="left",color=MUTED)
'''
    return ("**De Morgan's theorems.**\n\n1. The complement of a sum equals the product of the complements: $\\overline{A+B} = \\overline{A}\\cdot\\overline{B}$.\n"
            "2. The complement of a product equals the sum of the complements: $\\overline{A\\cdot B} = \\overline{A}+\\overline{B}$.\n\n"
            "They extend to any number of variables: $\\overline{A+B+C+\\dots} = \\overline{A}\\,\\overline{B}\\,\\overline{C}\\dots$ and $\\overline{ABC\\dots} = \\overline{A}+\\overline{B}+\\overline{C}+\\dots$\n\n"
            "**Proof by truth table** (columns 3 and 4 are identical, and so are columns 5 and 6):\n\n" +
            tbl(["A", "B", "$\\overline{A+B}$", "$\\overline{A}\\,\\overline{B}$", "$\\overline{AB}$", "$\\overline{A}+\\overline{B}$"], rows) +
            "\nThe first case is 1 only when both inputs are 0 (a NOR gate), which is exactly when both $\\overline{A}$ and $\\overline{B}$ are 1 (an AND of the inverted inputs). The second is 0 only when both inputs are 1, which is when $\\overline{A}$ or $\\overline{B}$ is 1 fails to hold, matching an OR of inverted inputs.\n\n" +
            figblock("De Morgan's theorems as gates: a NOR gate equals an AND gate with inverted inputs; a NAND gate equals an OR gate with inverted inputs.", code, canvas=False) +
            "\n**Use.** De Morgan's laws convert AND-OR forms into NAND-NAND or NOR-NOR forms, which is how circuits are built with a single gate type.\n")

def universal():
    nand = r'''
def nt(ax,x,y,lbl=None):
    ins,o=gn(ax,"NAND",x,y,n=2,w=0.9,lead=0.25)
    L(ax,[ins[0],(ins[0][0]-0.15,ins[0][1]),(ins[0][0]-0.15,ins[1][1]),ins[1]]); dot(ax,ins[0][0]-0.15,y)
    L(ax,[(ins[0][0]-0.15,y),(ins[0][0]-0.5,y)])
    return (ins[0][0]-0.5,y),o
fig,ax=ckt_canvas(5.9,3.6,xlim=(-1.5,15),ylim=(-0.3,6.2))
# NOT
i,o=nt(ax,1.0,5.3); T(ax,i[0]-0.1,5.3,"A",ha="right"); T(ax,o[0]+0.1,5.3,"$\\overline{A}$",ha="left"); T(ax,1.2,6.0,"NOT",size=8.2,color=MUTED)
# AND
ins,o=gn(ax,"NAND",6.2,5.3,n=2,w=0.9,lead=0.3); T(ax,ins[0][0]-0.1,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.1,ins[1][1],"B",ha="right")
i2,o2=nt(ax,o[0]+1.0,5.3); L(ax,[o,i2]); T(ax,o2[0]+0.1,5.3,"AB",ha="left"); T(ax,7.0,6.0,"AND",size=8.2,color=MUTED)
# OR
a,b=(10.2,1.9),(10.2,0.9)
i3,o3=nt(ax,12.0,2.9)
ins,o4=gn(ax,"NAND",12.4,1.4,n=2,w=0.9,lead=0.3)
i5,o5=nt(ax,10.0,2.0)
i6,o6=nt(ax,10.0,0.8)
L(ax,[o5,(ins[0][0],o5[1]),ins[0]]) if False else None
L(ax,[o5,(11.7,o5[1]),(11.7,ins[0][1]),ins[0]]); L(ax,[o6,(11.7,o6[1]),(11.7,ins[1][1]),ins[1]]) if False else L(ax,[o6,ins[1]]) if False else None
L(ax,[o6,(11.9,o6[1]),(11.9,ins[1][1]),ins[1]]) if False else None
T(ax,i5[0]-0.1,2.0,"A",ha="right"); T(ax,i6[0]-0.1,0.8,"B",ha="right"); T(ax,o4[0]+0.1,1.4,"A+B",ha="left"); T(ax,10.5,3.2,"OR",size=8.2,color=MUTED)
'''
    # simpler, cleaner figure code for NAND and NOR as separate generated figures
    def build(kind):
        k = kind
        tied = lambda: ""
        code = f'''
def nt(ax,x,y):
    ins,o=gn(ax,"{k}",x,y,n=2,w=0.9,lead=0.25)
    xl=ins[0][0]-0.15
    L(ax,[ins[0],(xl,ins[0][1]),(xl,ins[1][1]),ins[1]]); dot(ax,xl,y); L(ax,[(xl,y),(xl-0.35,y)])
    return (xl-0.35,y),o
fig,ax=ckt_canvas(5.9,3.7,xlim=(-1.6,15.2),ylim=(-0.4,6.6))
T(ax,0.4,6.2,"NOT",size=8.2,color=MUTED); T(ax,5.2,6.2,"%s",size=8.2,color=MUTED); T(ax,5.0,3.0,"%s",size=8.2,color=MUTED)
i,o=nt(ax,1.0,5.2); T(ax,i[0]-0.1,5.2,"A",ha="right"); T(ax,o[0]+0.1,5.2,"$\\\\overline{{A}}$",ha="left")
'''
        return code
    # AND / OR panels depend on the family
    def panel(kind):
        if kind == "NAND":
            top = ('"AND"', '"OR"')
            a = r'''
ins,o=gn(ax,"NAND",5.2,5.2,n=2,w=0.9,lead=0.3); T(ax,ins[0][0]-0.1,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.1,ins[1][1],"B",ha="right")
i2,o2=nt(ax,o[0]+1.0,5.2); L(ax,[o,i2]); T(ax,o2[0]+0.1,5.2,"$AB$",ha="left")
'''
            b = r'''
ia,oa=nt(ax,3.2,2.4); ib,ob=nt(ax,3.2,0.8); T(ax,ia[0]-0.1,2.4,"A",ha="right"); T(ax,ib[0]-0.1,0.8,"B",ha="right")
ins,o=gn(ax,"NAND",7.6,1.6,n=2,w=0.9,lead=0.3)
L(ax,[oa,(ins[0][0]-0.3,2.4),(ins[0][0]-0.3,ins[0][1]),ins[0]]) if False else L(ax,[oa,(6.4,oa[1]),(6.4,ins[0][1]),ins[0]])
L(ax,[ob,(6.4,ob[1]),(6.4,ins[1][1]),ins[1]]) if False else L(ax,[ob,(6.2,ob[1]),(6.2,ins[1][1]),ins[1]])
T(ax,o[0]+0.1,1.6,"$A+B$",ha="left")
'''
        else:
            a = r'''
ia,oa=nt(ax,3.2,5.6); ib,ob=nt(ax,3.2,4.4); T(ax,ia[0]-0.1,5.6,"A",ha="right"); T(ax,ib[0]-0.1,4.4,"B",ha="right")
ins,o=gn(ax,"NOR",7.6,5.0,n=2,w=0.9,lead=0.3)
L(ax,[oa,(6.4,oa[1]),(6.4,ins[0][1]),ins[0]]); L(ax,[ob,(6.2,ob[1]),(6.2,ins[1][1]),ins[1]])
T(ax,o[0]+0.1,5.0,"$AB$",ha="left")
'''
            b = r'''
ins,o=gn(ax,"NOR",5.2,1.6,n=2,w=0.9,lead=0.3); T(ax,ins[0][0]-0.1,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.1,ins[1][1],"B",ha="right")
i2,o2=nt(ax,o[0]+1.0,1.6); L(ax,[o,i2]); T(ax,o2[0]+0.1,1.6,"$A+B$",ha="left")
'''
        return a + b
    figs = ""
    for k in ("NAND", "NOR"):
        lab = ("AND", "OR") if k == "NAND" else ("AND", "OR")
        code = f'''
def nt(ax,x,y):
    ins,o=gn(ax,"{k}",x,y,n=2,w=0.9,lead=0.25)
    xl=ins[0][0]-0.15
    L(ax,[ins[0],(xl,ins[0][1]),(xl,ins[1][1]),ins[1]]); dot(ax,xl,y); L(ax,[(xl,y),(xl-0.35,y)])
    return (xl-0.35,y),o
fig,ax=ckt_canvas(5.9,3.7,xlim=(-1.6,15.2),ylim=(-0.4,6.8))
T(ax,0.2,6.4,"NOT",size=8.2,color=MUTED); T(ax,5.0,6.4,"AND",size=8.2,color=MUTED); T(ax,5.0,3.1,"OR",size=8.2,color=MUTED)
i,o=nt(ax,1.0,5.2); T(ax,i[0]-0.1,5.2,"A",ha="right"); T(ax,o[0]+0.1,5.2,"$\\\\overline{{A}}$",ha="left")
{panel(k)}
'''
        figs += figblock(f"Basic gates built only from {k} gates (NOT, AND, OR).", code, canvas=False)
    return figs

def universal_text():
    f = universal().split("```figure")
    nandfig = "```figure" + f[1]; norfig = "```figure" + f[2]
    return ("A gate type is **universal** if every Boolean function (that is, NOT, AND and OR) can be built from it alone.\n\n"
            "**(a) NAND is universal.** With $\\overline{AA} = \\overline{A}$ and De Morgan:\n\n"
            "$$\\text{NOT: } \\overline{A\\cdot A} = \\overline{A} \\qquad \\text{AND: } \\overline{\\overline{A\\cdot B}} = AB \\qquad \\text{OR: } \\overline{\\overline{A}\\cdot\\overline{B}} = A + B$$\n\n"
            "NOT: tie both inputs together. AND: a NAND followed by a NAND used as inverter. OR: invert each input with a NAND-inverter, then NAND the results.\n\n" + nandfig +
            "\n**(b) NOR is universal.**\n\n"
            "$$\\text{NOT: } \\overline{A+A} = \\overline{A} \\qquad \\text{OR: } \\overline{\\overline{A+B}} = A + B \\qquad \\text{AND: } \\overline{\\overline{A}+\\overline{B}} = AB$$\n\n"
            "NOT: tie the inputs. OR: NOR followed by a NOR-inverter. AND: invert each input with a NOR-inverter, then NOR the results.\n\n" + norfig +
            "\nSince NOT, AND and OR are available from either gate, any logic function can be realised with NAND gates alone or with NOR gates alone; hence both are universal gates (they are also cheaper in IC form).\n")

# ---------------- K-map ----------------
def kmap_solution(ones, dcs, nv=4, names="ABCD", out="F", title=None, extra=""):
    terms = minimize(ones, dcs, nv)
    check_cover(terms, ones, dcs, nv)
    mt = sorted(ones); dc = sorted(dcs)
    nm = list(names[:nv])
    expr = tex_sop(terms, nm)
    s = "**Step 1 - K-map.** Enter 1 in each minterm cell" + (" and X (don't care) in each don't-care cell" if dcs else "") + ", Gray-code ordered rows and columns so neighbouring cells differ in one variable.\n\n"
    s += kmap_figure(f"{nv}-variable K-map of {out} with the prime-implicant loops (cell numbers are minterm numbers).", [(out, nv, ones, dcs, terms)], names, per_row=1, cs=0.72)
    s += "\n**Step 2 - groups (largest possible, power of two).**\n\n"
    for gi, t in enumerate(terms):
        cells = term_minterms(t, nv)
        cl = [c for c in cells if c in ones or c in dcs]
        s += f"- Group {gi+1} (loop colour {['red','blue','green','gold','violet','teal'][gi%6]}), cells {', '.join(str(c) for c in cells)}: variables that do not change survive, giving ${tex_term(t, nm)}$.\n"
    s += f"\n**Step 3 - minimised expression.**\n\n$$\\boxed{{{out}({','.join(nm)}) = {expr}}}$$\n\n"
    # circuit
    m = len(terms)
    sp = max(1.15, max(len(t) for t in terms) * 0.42 + 0.3)
    W = nv * 0.95 + 5.0; H = 2.2 + (m - 1) * sp + 1.2
    code = "sopc(ax,%r,%r,out=%r)\n" % (term_lits_py(terms) and [[(i, p) for i, p in t] for t in terms], list(nm), out)
    s += "**Step 4 - realisation with logic gates (AND-OR, two-level).** The complemented inputs come from NOT gates.\n\n"
    s += figblock(f"AND-OR realisation of {out} = {''.join(' ' for _ in '')}" + "".join(tex_term(t, nm).replace('\\overline{', '').replace('}', "'") + (' + ' if i < m - 1 else '') for i, t in enumerate(terms)).replace('\\', ''), code, w=5.9, h=round(5.9 * H / W, 2), xlim="(-0.5,%s)" % round(W, 2), ylim="(%s,1.8)" % round(-0.9 - (m - 1) * sp - 1.0, 2))
    s += f"\n*Equivalent NAND-only form.* Replacing every AND and the OR by NAND gates (double inversion, De Morgan) gives the same function with {m + (1 if m > 1 else 0)} NAND gates (plus the input inverters).\n"
    s += extra
    return s, terms

# ---------------- decoders / encoders ----------------
def encoder_decoder_diff():
    return tbl(["Point", "Encoder", "Decoder"], [
        ["Function", "Converts $2^n$ (or fewer) input lines into an $n$-bit binary code", "Converts an $n$-bit binary code into one of $2^n$ output lines"],
        ["Inputs / outputs", "$2^n$ inputs, $n$ outputs", "$n$ inputs, $2^n$ outputs"],
        ["Active lines", "Only one input is active at a time", "Only one output is active for a given code"],
        ["Built from", "OR gates", "AND (or NAND) gates"],
        ["Example", "Octal-to-binary (8:3), keyboard encoder", "3-to-8, BCD-to-7-segment decoder"],
        ["Use", "Keyboards, interrupt priority, data compression", "Address decoding, memory chip select, display drivers"]])

def octal_encoder():
    rows = []
    for i in range(8):
        rows.append([("1" if j == i else "0") for j in range(7, -1, -1)] + [(i >> 2) & 1, (i >> 1) & 1, i & 1])
    code = r'''
fig,ax=ckt_canvas(5.9,3.4,xlim=(-1,11),ylim=(-0.6,7.4))
ys=[7.0-0.75*k for k in range(8)]   # D0..D7 top to bottom? place D7 at top
ys=[6.8-0.75*(7-i) for i in range(8)]
xs={}
for i,y in enumerate(ys):
    T(ax,0.0,y,"D%d"%i,ha="right",size=8.2)
    L(ax,[(0.1,y),(0.6+0.22*i,y)],lw=1.1,color="#4a5565")
for i,y in enumerate(ys): xs[i]=0.6+0.22*i
for i in range(8): L(ax,[(xs[i],ys[i]),(xs[i],-0.2)],lw=1.1,color="#4a5565")
outs=[("A2",[4,5,6,7],6.0),("A1",[2,3,6,7],3.3),("A0",[1,3,5,7],0.6)]
for nm,inp,yc in outs:
    ins,o=gn(ax,"OR",5.4,yc,n=4,w=1.1,lead=0.3)
    for (px,py),i in zip(ins,inp):
        L(ax,[(xs[i],py),(px,py)],lw=1.1); dot(ax,xs[i],py)
    L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],nm,ha="left",size=9)
T(ax,8.0,7.1,"D0 has no gate: all outputs 0",size=7.6,color=MUTED)
'''
    return ("**Octal-to-binary encoder (8-line to 3-line).** Eight inputs $D_0\\dots D_7$ (only one high at a time) produce a 3-bit code $A_2A_1A_0$ equal to the number of the active input.\n\n" +
            tbl(["D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0", "A2", "A1", "A0"], rows) +
            "\nFrom the table each output is the OR of the inputs whose code has a 1 in that position:\n\n"
            "$$A_2 = D_4 + D_5 + D_6 + D_7, \\qquad A_1 = D_2 + D_3 + D_6 + D_7, \\qquad A_0 = D_1 + D_3 + D_5 + D_7$$\n\n"
            "$D_0$ needs no gate (the code is 000 when $D_0$ is active or when no input is active). Three 4-input OR gates give the encoder.\n\n" +
            figblock("Octal-to-binary encoder: three 4-input OR gates.", code, canvas=False).replace("fig,ax=ckt_canvas", "fig,ax=ckt_canvas") +
            "\n*Limitation.* If two inputs are high together, the output is the OR of the two codes (wrong); a **priority encoder** removes this ambiguity.\n")

def priority_encoder():
    # inputs D7..D1 (D0 not needed), outputs A2 A1 A0 and V (valid)
    names = ["D7", "D6", "D5", "D4", "D3", "D2", "D1"]
    nv = 7
    res = {}
    hi = lambda m: next((7 - i for i in range(nv) if (m >> (nv - 1 - i)) & 1), 0)  # highest active index (1..7); 0 if none
    for b, nm in ((2, "A2"), (1, "A1"), (0, "A0")):
        ones = [m for m in range(2 ** nv) if (hi(m) >> b) & 1]
        res[nm] = minimize(ones, [], nv)
        check_cover(res[nm], ones, [], nv)
    tx = {k: tex_sop(v, names).replace("D7", "D_7").replace("D6", "D_6").replace("D5", "D_5").replace("D4", "D_4").replace("D3", "D_3").replace("D2", "D_2").replace("D1", "D_1") for k, v in res.items()}
    # reorder indices: variable i in terms refers to names[i]
    rows = []
    rows.append(["0"] * 8 + ["0", "0", "0", "0"])
    for i in range(8):
        r = []
        for j in range(7, -1, -1):
            r.append("1" if j == i else ("X" if j < i else "0"))
        rows.append(r + [(i >> 2) & 1, (i >> 1) & 1, i & 1, 1])
    rows = rows[1:] + [rows[0]]
    rows = [rows[-1]] + rows[:-1]
    # circuit with sopc on 7 variables
    ac = "".join(f"sopc_xy({k})" for k in [])
    codes = ""
    for nm in ("A2", "A1", "A0"):
        terms = res[nm]
        m = len(terms); sp = max(1.15, max(len(t) for t in terms) * 0.42 + 0.3)
        W = 7 * 0.95 + 5.0; H = 2.2 + (m - 1) * sp + 1.2
        code = "sopc(ax,%r,%r,out=%r)\n" % ([[(i, p) for i, p in t] for t in terms], names, nm)
        codes += figblock(f"Priority encoder output {nm} (inputs D7 ... D1).", code, w=5.9, h=round(5.9 * H / W, 2), xlim="(-0.5,%s)" % round(W, 2), ylim="(%s,1.8)" % round(-0.9 - (m - 1) * sp - 1.0, 2))
    return res, tx, rows, codes

def mux_fa_fs(kind):
    """Full adder (kind='add') or full subtractor ('sub') using two 4:1 MUX, select A,B, data from C / Bin."""
    c = "C" if kind == "add" else "B$_{in}$"
    cn = "$\\overline{C}$" if kind == "add" else "$\\overline{B_{in}}$"
    top = "Sum" if kind == "add" else "Diff"
    bot = "Cout" if kind == "add" else "Bout"
    if kind == "add":
        bl = [c, "1", "1", "0"][:0]
        d_lab = [c, cn, cn, c]; c_lab = ["0", c, c, "1"]
    else:
        d_lab = [c, cn, cn, c]; c_lab = [c, "1", "0", c]
    code = f'''
fig,ax=ckt_canvas(5.9,3.6,xlim=(-2.6,10.5),ylim=(-1.9,8.0))
m1=mux(ax,3.0,5.6,4,{d_lab!r},["B","A"],out={top!r},name="4:1 MUX")
m2=mux(ax,3.0,1.4,4,{c_lab!r},["B","A"],out={bot!r},name="4:1 MUX")
# select lines shared: A (left select) and B -- in this drawing the first select is the less significant S0=B? keep S1=A,S0=B
'''
    return code

PAIR = None
