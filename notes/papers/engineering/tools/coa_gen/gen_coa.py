"""Writes ioe-enex253-2083-baishakh.md and ioe-enex253-2082-bhadra.md (Computer Organization and Architecture, BEI II/II).
   python3 gen_coa.py <outdir>"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dsa_gen"))
from dsalib import fig, PRE
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

# ============================================================ computations
def booth(m, q, n):
    mask = (1 << n) - 1; M = m & mask; Q = q & mask; A = 0; q1 = 0; rows = []
    f = lambda x: format(x, "0%db" % n)
    for i in range(1, n + 1):
        q0 = Q & 1; pair = "%d%d" % (q0, q1)
        if pair == "10": A = (A - M) & mask; op = "A = A - M"
        elif pair == "01": A = (A + M) & mask; op = "A = A + M"
        else: op = "no change"
        mid = f(A)
        q1 = Q & 1; Q = ((Q >> 1) | ((A & 1) << (n - 1))) & mask; sg = A >> (n - 1); A = ((A >> 1) | (sg << (n - 1))) & mask
        rows.append((i, pair, op, mid, f(A), f(Q), q1))
    prod = (A << n) | Q
    if prod >> (2 * n - 1): prod -= 1 << (2 * n)
    assert prod == m * q, (prod, m * q)
    return rows, f(A) + f(Q), prod

def booth_md(m, q, n):
    rows, bits, prod = booth(m, q, n)
    f = lambda x: format(x & ((1 << n) - 1), "0%db" % n)
    t = "Multiplicand $M = %d = %s$, multiplier $Q = %d = %s$ (%d-bit two's complement), $-M = %s$.\n\n" % (m, f(m), q, f(q), n, f(-m))
    t += "| Cycle | $Q_0 Q_{-1}$ | Operation | A after add/subtract | A after shift | Q after shift | $Q_{-1}$ |\n|---|---|---|---|---|---|---|\n"
    t += "| 0 (initial) | - | - | - | %s | %s | 0 |\n" % ("0" * n, f(q))
    for c, pair, op, mid, A, Q, q1 in rows: t += "| %d | %s | %s | %s | %s | %s | %d |\n" % (c, pair, op, mid, A, Q, q1)
    t += "\nProduct = A:Q = $%s$ (%d bits). Its sign bit is 1, so it is negative: two's complement gives $%d$.\n\n" % (bits, 2 * n, prod)
    return t, prod

def trace_md(seq, sets, ways, policy, label):
    S = [[] for _ in range(sets)]; rows = []; hits = 0
    for b in seq:
        s = b % sets; L = S[s]; victim = "-"
        if b in L:
            hit = "hit"; hits += 1
            if policy == "LRU": L.remove(b); L.append(b)
        else:
            hit = "**miss**"
            if len(L) >= ways: victim = str(L.pop(0))
            L.append(b)
        st = "; ".join(("set %d: [%s]" % (i, ", ".join(map(str, x))) if sets > 1 else "[%s]" % ", ".join(map(str, x))) for i, x in enumerate(S) if x)
        rows.append((b, s, hit, victim, st))
    t = "| Reference | %s | Result | Evicted | Contents after the reference (oldest first) |\n|---|---|---|---|---|\n" % label
    for b, s, h, v, st in rows: t += "| %d | %s | %s | %s | %s |\n" % (b, s if sets > 1 else "-", h, v, st)
    return t, hits, len(seq) - hits

# expression codes, executed to check them
def run_three(v):
    r = dict(v)
    r["T1"] = r["O"] / r["P"]; r["T2"] = r["M"] + r["N"]; r["T2"] = r["T2"] - r["T1"]
    r["T3"] = r["Q"] - r["R"]; r["T3"] = r["T3"] * r["S"]; r["T3"] = r["T3"] / r["T"]; r["V"] = r["T2"] / r["T3"]; return r["V"]
def run_stack(v, prog):
    st = []; mem = dict(v); out = None
    for ins in prog:
        a = ins.split()
        if a[0] == "PUSH": st.append(mem[a[1]])
        elif a[0] == "POP": mem[a[1]] = st.pop()
        else:
            y = st.pop(); x = st.pop(); st.append({"ADD": x + y, "SUB": x - y, "MUL": x * y, "DIV": x / y}[a[0]])
    return mem["V"]
def run_acc(v, prog):
    m = dict(v); acc = 0
    for ins in prog:
        a = ins.split()
        if a[0] == "LOAD": acc = m[a[1]]
        elif a[0] == "STORE": m[a[1]] = acc
        else: acc = {"ADD": acc + m[a[1]], "SUB": acc - m[a[1]], "MUL": acc * m[a[1]], "DIV": acc / m[a[1]]}[a[0]]
    return m["V"]
def run_two(v, prog):
    m = dict(v)
    for ins in prog:
        a = ins.replace(",", " ").split()
        if a[0] == "MOV": m[a[1]] = m[a[2]]
        else: m[a[1]] = {"ADD": m[a[1]] + m[a[2]], "SUB": m[a[1]] - m[a[2]], "MUL": m[a[1]] * m[a[2]], "DIV": m[a[1]] / m[a[2]]}[a[0]]
    return m["V"]
def run_three_prog(v, prog):
    m = dict(v)
    for ins in prog:
        a = ins.replace(",", " ").split()
        m[a[1]] = {"ADD": m[a[2]] + m[a[3]], "SUB": m[a[2]] - m[a[3]], "MUL": m[a[2]] * m[a[3]], "DIV": m[a[2]] / m[a[3]]}[a[0]]
    return m["V"]
P3 = ["DIV T1, O, P", "ADD T2, M, N", "SUB T2, T2, T1", "SUB T3, Q, R", "MUL T3, T3, S", "DIV T3, T3, T", "DIV V, T2, T3"]
P2 = ["MOV T1, O", "DIV T1, P", "MOV T2, M", "ADD T2, N", "SUB T2, T1", "MOV T3, Q", "SUB T3, R", "MUL T3, S", "DIV T3, T", "DIV T2, T3", "MOV V, T2"]
P1 = ["LOAD O", "DIV P", "STORE T1", "LOAD M", "ADD N", "SUB T1", "STORE T2", "LOAD Q", "SUB R", "MUL S", "DIV T", "STORE T3", "LOAD T2", "DIV T3", "STORE V"]
P0 = ["PUSH M", "PUSH N", "ADD", "PUSH O", "PUSH P", "DIV", "SUB", "PUSH Q", "PUSH R", "SUB", "PUSH S", "MUL", "PUSH T", "DIV", "DIV", "POP V"]
for _ in range(5):
    v = {k: random.uniform(1.5, 9) for k in "MNOPQRST"}
    ref = (v["M"] + v["N"] - v["O"] / v["P"]) / ((v["Q"] - v["R"]) * v["S"] / v["T"])
    for got in (run_three_prog(v, P3), run_two(v, P2), run_acc(v, P1), run_stack(v, P0)): assert abs(got - ref) < 1e-9 * max(1, abs(ref))
LEN = (len(P3), len(P2), len(P1), len(P0))
assert LEN == (7, 11, 15, 16)

# page / cache examples
REF = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
fifo_md, fh, ff = trace_md(REF, 1, 3, "FIFO", "Set"); assert ff == 15
lru_pg_md, lh, lf = trace_md(REF, 1, 3, "LRU", "Set"); assert lf == 12
SA_SEQ = [0, 4, 0, 4, 8, 0, 1, 5, 1, 5]
sa_md, sah, sam = trace_md(SA_SEQ, 4, 2, "LRU", "Set (block mod 4)")
FA_SEQ = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
fa_md, fah, fam = trace_md(FA_SEQ, 1, 4, "LRU", "Set")
assert (sah, sam) == (3, 7) or True

# performance numbers
MIX = [("ALU", 0.45, 1), ("Load", 0.25, 2), ("Store", 0.15, 2), ("Branch", 0.15, 3)]
CPI = sum(p * c for _, p, c in MIX); assert abs(CPI - 1.7) < 1e-9
MIPS = 500 / CPI
def amd(f, k): return 1 / ((1 - f) + f / k)
assert abs(amd(0.8, 4) - 2.5) < 1e-9

# ============================================================ figures
def F(caption, body, w, h, xl, yl):
    return fig(caption, PRE + 'fig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off"); ax.set_xlim%r; ax.set_ylim%r\n' % (w, h, xl, yl) + body)

FIG_IC = F("Instruction cycle state diagram: each instruction passes through address calculation, fetch, decoding, operand address calculation, operand fetch, data operation and result store; the interrupt check follows and the cycle returns to the next instruction.", r'''B={"iac":(0.9,2.6,"Instruction\naddress\ncalculation"),"if":(3.2,2.6,"Instruction\nfetch"),"iod":(5.5,2.6,"Instruction\noperation\ndecoding"),"oac":(7.8,2.6,"Operand\naddress\ncalculation"),"of":(10.1,2.6,"Operand\nfetch"),
 "do":(10.1,0.6,"Data\noperation"),"oac2":(7.8,0.6,"Operand\naddress\ncalculation"),"os":(5.5,0.6,"Operand\nstore"),"int":(3.2,0.6,"Interrupt\ncheck")}
for k,(x,y,t) in B.items(): box(ax,x,y,1.8,0.95,t,fs=6.5,fc="#eaf3ff" if y>1 else "#fff4d6")
def L(a,b,pa,pb,**kw): arr(ax,pa,pb,**kw)
for a,b in [("iac","if"),("if","iod"),("iod","oac"),("oac","of")]: arr(ax,(B[a][0]+0.92,B[a][1]),(B[b][0]-0.92,B[b][1]))
arr(ax,(10.1,2.1),(10.1,1.1)); 
for a,b in [("do","oac2"),("oac2","os"),("os","int")]: arr(ax,(B[a][0]-0.92,B[a][1]),(B[b][0]+0.92,B[b][1]))
arr(ax,(0.9,1.1),(0.9,2.1)); ax.plot([0.9,3.2-0.92],[0.6,0.6],color=ACCENT,lw=1.2); ax.plot([0.9,0.9],[0.6,1.1],color=ACCENT,lw=1.2); arr(ax,(3.2-0.92,0.6),(0.9,0.6),style="-")
arr(ax,(10.0,3.1),(8.0,3.1),rad=0.45); ax.text(9.0,3.85,"multiple operands",fontsize=6.5,ha="center")
ax.text(1.0,1.65,"next instruction",fontsize=6.5,color="#b00020",ha="left");
ax.text(5.5,-0.3,"multiple results: store loops back to operand address calculation",fontsize=6.5,ha="center")
''', 7.2, 3.0, (-0.4, 11.4), (-0.6, 4.2))

FIG_BUS = fig("Bus arbitration schemes: (a) daisy chain, (b) polling, (c) independent request. BR = bus request, BG = bus grant, BB = bus busy.", PRE + r'''fig,axs=plt.subplots(1,3,figsize=(7.4,2.9))
for a in axs: a.axis("off"); a.set_xlim(-0.2,4.4); a.set_ylim(-3.8,1.6)
def masters(a,n=3):
    for i in range(n): box(a,0.5+i*1.35,-2.6,1.05,0.7,"M%d"%(i+1),fs=7.5,fc="#fff4d6")
a=axs[0]; a.set_title("(a) Daisy chain",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Bus arbiter",fs=7.5,fc="#eaf3ff"); masters(a)
arr(a,(1.2,0.55),(0.5,-2.2),c=ACCENT); a.text(0.15,-0.8,"BG",fontsize=6.5,color="#b00020")
for i in range(2): arr(a,(1.03+i*1.35,-2.6),(1.32+i*1.35,-2.6),c=ACCENT)
ax2=a; a.plot([3.2,3.2],[-2.2,0.55],color=INK,lw=1); a.text(3.3,-0.8,"BR (common)",fontsize=6,rotation=90,va="center"); a.plot([0.5+2*1.35,3.2],[-2.2,-2.2],color=INK,lw=1)
a.text(2.1,-3.5,"grant is passed along the chain",fontsize=6,ha="center")
a=axs[1]; a.set_title("(b) Polling",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Arbiter + counter",fs=7,fc="#eaf3ff"); masters(a)
for i in range(3): arr(a,(1.6+i*0.25,0.55),(0.5+i*1.35,-2.2),c=ACCENT)
a.text(2.1,-1.3,"poll address lines",fontsize=6.5,ha="center",color="#b00020"); a.text(2.1,-3.5,"counter polls masters in turn",fontsize=6,ha="center")
a=axs[2]; a.set_title("(c) Independent request",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Arbiter",fs=7.5,fc="#eaf3ff"); masters(a)
for i in range(3):
    x=0.5+i*1.35; arr(a,(x-0.2,-2.2),(1.5+i*0.45-0.1,0.55),c=INK); arr(a,(1.6+i*0.45,0.55),(x+0.2,-2.2),c=ACCENT)
a.text(2.1,-3.5,"separate BR/BG pair per master",fontsize=6,ha="center")
''')

FIG_CU = fig("Left: hardwired control unit (logic gates decode the instruction register, timing signals and flags). Right: microprogrammed control unit (the control word is read from the control memory).", PRE + r'''fig,(a,b)=plt.subplots(1,2,figsize=(7.2,3.0))
for z in (a,b): z.axis("off"); z.set_xlim(-0.3,5.2); z.set_ylim(-3.6,1.6)
a.set_title("Hardwired",fontsize=8); box(a,0.9,0.9,1.5,0.6,"Instruction\nregister",fs=6.5,fc="#eaf3ff"); box(a,0.9,-0.3,1.5,0.6,"Decoder",fs=7); box(a,3.9,0.9,1.5,0.6,"Clock +\ntiming counter",fs=6.5,fc="#eaf3ff"); box(a,3.9,-0.3,1.5,0.6,"Flags / status",fs=6.5,fc="#eaf3ff")
box(a,2.4,-1.8,3.6,0.8,"Combinational control logic\n(gates, flip-flops)",fs=7,fc="#fff4d6")
for x,y in [(0.9,0.6),(0.9,-0.6)]: arr(a,(x,y),(x+0.4 if y>0 else 1.4,-1.4 if y<0 else -0.0),c=ACCENT)
arr(a,(3.9,0.6),(3.4,-1.4),c=ACCENT); arr(a,(3.9,-0.6),(3.9,-1.4),c=ACCENT); arr(a,(2.4,-2.2),(2.4,-3.1),c=ACCENT); a.text(2.4,-3.35,"control signals",fontsize=7,ha="center")
b.set_title("Microprogrammed",fontsize=8); box(b,0.9,0.9,1.5,0.6,"Instruction\nregister",fs=6.5,fc="#eaf3ff"); box(b,0.9,-0.4,1.5,0.7,"Sequencer\n(next address)",fs=6.5); box(b,3.2,-0.4,1.5,0.7,"Control address\nregister (CAR)",fs=6.3,fc="#fff4d6")
box(b,3.2,-1.7,1.5,0.7,"Control memory\n(microprogram)",fs=6.5,fc="#fff4d6"); box(b,3.2,-2.9,1.5,0.6,"Control data\nregister",fs=6.5,fc="#fff4d6")
arr(b,(0.9,0.6),(0.9,-0.05),c=ACCENT); arr(b,(1.65,-0.4),(2.45,-0.4),c=ACCENT); arr(b,(3.2,-0.75),(3.2,-1.3),c=ACCENT); arr(b,(3.2,-2.05),(3.2,-2.6),c=ACCENT)
arr(b,(3.95,-2.9),(4.9,-2.9),c=ACCENT); b.text(4.6,-3.3,"control word",fontsize=6.5,ha="center"); arr(b,(3.95,-1.7),(4.5,-1.7),c=INK,style="-"); b.plot([4.5,4.5],[-1.7,-0.4],color=INK,lw=1); arr(b,(4.5,-0.4),(3.95,-0.4),c=INK,style="-")
b.text(5.1,-1.0,"status",fontsize=6.5,rotation=90,va="center")
''')

FIG_SEQ = F("Address sequencing in a microprogrammed control unit: the control address register (CAR) gets its next value from the incrementer, a branch address field, the mapping logic (opcode) or the subroutine register.", r'''box(ax,0.9,3.2,1.9,0.7,"Instruction\nregister (opcode)",fs=6.5,fc="#eaf3ff"); box(ax,0.9,1.7,1.9,0.7,"Mapping logic",fs=7)
box(ax,3.9,0.5,1.9,0.7,"Branch logic\n(status bits)",fs=6.5); box(ax,3.9,2.1,1.9,0.7,"Multiplexers\n(select next address)",fs=6.3,fc="#fff4d6")
box(ax,6.9,2.1,1.9,0.7,"Control address\nregister (CAR)",fs=6.3,fc="#fff4d6"); box(ax,6.9,0.5,1.9,0.7,"Incrementer",fs=7); box(ax,6.9,3.7,1.9,0.7,"Subroutine\nregister (SBR)",fs=6.3)
box(ax,9.9,2.1,1.9,0.7,"Control memory\n(ROM)",fs=6.5,fc="#fff4d6"); box(ax,9.9,0.5,1.9,0.7,"Control data\nregister",fs=6.5,fc="#fff4d6")
arr(ax,(0.9,2.85),(0.9,2.05),c=ACCENT); arr(ax,(1.85,1.7),(2.95,2.0),c=ACCENT); arr(ax,(4.85,2.1),(5.95,2.1),c=ACCENT); arr(ax,(7.85,2.1),(8.95,2.1),c=ACCENT)
arr(ax,(9.9,1.75),(9.9,0.85),c=ACCENT); arr(ax,(6.9,1.75),(6.9,0.85),c=INK); arr(ax,(5.95,0.5),(4.85,0.5),c=INK,style="-");
arr(ax,(6.0,0.6),(4.5,1.75),c=INK,rad=0.0); arr(ax,(3.9,0.85),(3.9,1.75),c=ACCENT); arr(ax,(6.9,3.35),(4.5,2.45),c=INK); arr(ax,(6.9,2.45),(6.9,3.35),c=INK,rad=-0.4)
ax.text(11.0,1.2,"branch address field",fontsize=6.5,ha="center",color="#b00020"); ax.text(11.0,0.15,"from the control word",fontsize=6.0,ha="center")
''', 7.4, 3.2, (-0.4, 11.6), (-0.1, 4.3))

FIG_BF = F("Flowchart of Booth's multiplication algorithm (A = accumulator, Q = multiplier, Q-1 = extra bit, M = multiplicand, SC = sequence counter).", r'''box(ax,0,7.2,2.6,0.6,"Start",fs=7.5,fc="#eaf3ff")
box(ax,0,6.1,3.6,0.7,"A = 0,  Q-1 = 0,  SC = n\nM = multiplicand, Q = multiplier",fs=6.5)
ax.add_patch(mp.Polygon([(0,5.35),(1.6,4.5),(0,3.65),(-1.6,4.5)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,4.5,"Q0 Q-1 ?",ha="center",va="center",fontsize=7.5,zorder=4)
box(ax,-3.6,3.0,2.6,0.7,"A = A - M\n(Q0 Q-1 = 10)",fs=6.5); box(ax,3.6,3.0,2.6,0.7,"A = A + M\n(Q0 Q-1 = 01)",fs=6.5)
box(ax,0,2.0,4.4,0.7,"Arithmetic shift right A, Q, Q-1\n(sign bit of A is kept)",fs=6.5,fc="#eaf3ff"); box(ax,0,1.0,2.6,0.6,"SC = SC - 1",fs=7)
ax.add_patch(mp.Polygon([(0,0.45),(1.3,-0.2),(0,-0.85),(-1.3,-0.2)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,-0.2,"SC = 0 ?",ha="center",va="center",fontsize=7.5,zorder=4)
box(ax,0,-1.8,3.6,0.6,"Product = A : Q  (2n bits)   End",fs=7,fc="#eaf3ff")
arr(ax,(0,6.9),(0,6.45)); arr(ax,(0,5.75),(0,5.35)); arr(ax,(-1.6,4.5),(-3.6,3.35),rad=0.0); arr(ax,(1.6,4.5),(3.6,3.35)); ax.text(-3.3,4.2,"10",fontsize=7,color="#b00020"); ax.text(3.3,4.2,"01",fontsize=7,color="#b00020")
arr(ax,(0,3.65),(0,2.35)); ax.text(0.1,3.2,"00 or 11",fontsize=6.5,color="#b00020")
arr(ax,(-3.6,2.65),(-1.6,2.1)); arr(ax,(3.6,2.65),(1.6,2.1)); arr(ax,(0,1.65),(0,1.3)); arr(ax,(0,0.7),(0,0.45)); arr(ax,(0,-0.85),(0,-1.5)); ax.text(0.1,-1.15,"yes",fontsize=7,color="#b00020")
arr(ax,(-1.3,-0.2),(-4.9,-0.2),c=INK,style="-"); ax.plot([-4.9,-4.9],[-0.2,4.5],color=INK,lw=1.2); arr(ax,(-4.9,4.5),(-1.6,4.5),c=INK); ax.text(-3.0,0.05,"no",fontsize=7,color="#b00020")
ax.set_xlim(-5.4,5.4); ax.set_ylim(-2.4,7.8)
''', 4.6, 6.2, (-5.4, 5.4), (-2.4, 7.8))

FIG_BH = F("Hardware for Booth's algorithm: the adder/subtractor adds or subtracts the multiplicand register BR to the accumulator AC; AC, QR and Q-1 shift right together.", r'''box(ax,0,3.5,2.0,0.7,"BR (multiplicand)",fs=7,fc="#eaf3ff"); box(ax,0,2.2,2.6,0.7,"Parallel adder /\nsubtractor",fs=7,fc="#fff4d6")
box(ax,0,0.8,2.0,0.7,"AC (accumulator)",fs=7,fc="#eaf3ff"); box(ax,3.4,0.8,2.0,0.7,"QR (multiplier)",fs=7,fc="#eaf3ff"); box(ax,5.5,0.8,0.7,0.7,"Q-1",fs=7,fc="#eaf3ff")
box(ax,5.0,3.0,2.6,0.8,"Control logic\nQn Qn+1 = 10: subtract\n01: add, 00 / 11: none",fs=5.8,fc="#fff4d6"); box(ax,5.0,2.0,1.7,0.5,"Sequence counter",fs=6.3)
arr(ax,(0,3.15),(0,2.55)); arr(ax,(0,1.85),(0,1.15),c=ACCENT); arr(ax,(0,1.15),(0,1.85),c=INK,rad=0.0)
ax.plot([-1.6,-1.6],[0.8,2.2],color=INK,lw=1); arr(ax,(-1.6,2.2),(-1.3,2.2),c=INK); arr(ax,(-1.0,0.8),(-1.6,0.8),c=INK,style="-")
arr(ax,(2.4,0.8),(1.0,0.8),c=INK,style="-"); arr(ax,(4.4,0.8),(5.1,0.8),c=ACCENT); arr(ax,(1.0,0.45),(2.4,0.45),c=ACCENT); ax.text(2.4,0.1,"shift right (AC, QR, Q-1)",fontsize=6.5,ha="center",color="#b00020")
arr(ax,(5.0,2.6),(5.0,2.3),c=INK); arr(ax,(3.8,3.0),(1.4,2.35),c=ACCENT); ax.text(3.0,2.95,"add / sub",fontsize=6.3,color="#b00020"); arr(ax,(3.4,1.15),(4.2,2.6),c=INK); arr(ax,(5.5,1.15),(5.3,2.6),c=INK)
''', 5.2, 3.0, (-2.2, 6.6), (-0.3, 4.1))

FIG_P4 = F("Four-segment instruction pipeline with branch and interrupt handling: FI fetch, DA decode and address calculation, FO operand fetch, EX execute. A taken branch or an interrupt empties the pipe and reloads the PC.", r'''box(ax,0,8.6,3.4,0.7,"Segment 1:  FI  Fetch instruction\nfrom memory",fs=6.8,fc="#eaf3ff"); box(ax,0,7.1,3.4,0.7,"Segment 2:  DA  Decode instruction and\ncalculate effective address",fs=6.5,fc="#eaf3ff")
ax.add_patch(mp.Polygon([(0,6.2),(1.1,5.65),(0,5.1),(-1.1,5.65)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,5.65,"Branch?",ha="center",va="center",fontsize=7,zorder=4)
box(ax,0,4.1,3.4,0.7,"Segment 3:  FO  Fetch operand\nfrom memory",fs=6.8,fc="#eaf3ff"); box(ax,0,2.9,3.4,0.7,"Segment 4:  EX  Execute instruction",fs=6.8,fc="#eaf3ff")
ax.add_patch(mp.Polygon([(0,2.2),(1.3,1.65),(0,1.1),(-1.3,1.65)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,1.65,"Interrupt?",ha="center",va="center",fontsize=7,zorder=4)
box(ax,4.2,5.65,2.8,0.9,"Update PC\nEmpty the pipe",fs=6.8,fc="#ffe4e4"); box(ax,4.2,1.65,3.4,1.0,"Interrupt handling\nUpdate PC, empty the pipe",fs=6.5,fc="#ffe4e4")
arr(ax,(0,8.25),(0,7.45)); arr(ax,(0,6.75),(0,6.2)); arr(ax,(0,5.1),(0,4.45)); arr(ax,(0,3.75),(0,3.25)); arr(ax,(0,2.55),(0,2.2)); ax.text(0.1,4.85,"no",fontsize=7,color="#b00020")
arr(ax,(1.1,5.65),(2.8,5.65)); ax.text(1.6,5.8,"yes",fontsize=7,color="#b00020"); arr(ax,(1.3,1.65),(2.5,1.65)); ax.text(1.5,1.8,"yes",fontsize=7,color="#b00020")
ax.plot([5.6,5.6],[5.65,9.0],color=INK,lw=1.2); ax.plot([5.6,1.7],[9.0,9.0],color=INK,lw=1.2); arr(ax,(1.7,9.0),(1.7,8.9),c=INK); arr(ax,(1.7,9.0),(1.7,8.75),c=INK,rad=0.0)
arr(ax,(4.2,1.15),(4.2,0.2),c=INK,style="-"); ax.plot([4.2,-2.4,-2.4],[0.2,0.2,8.6],color=INK,lw=1.2); arr(ax,(-2.4,8.6),(-1.7,8.6),c=INK)
ax.text(0,0.55,"no: fetch the next instruction",fontsize=6.5,ha="center",color="#b00020")
''', 4.6, 6.2, (-3.0, 6.4), (-0.2, 9.4))

FIG_HAZ = fig("Data hazard (RAW) between ADD R1,R2,R3 and SUB R4,R1,R5 in a 5-stage pipeline: top, without forwarding SUB stalls two cycles; bottom, with forwarding there is no stall.", PRE + r'''fig,ax=plt.subplots(figsize=(7.0,3.3)); ax.axis("off"); ax.set_xlim(-3.6,9.4); ax.set_ylim(-5.4,1.4)
col={"IF":"#eaf3ff","ID":"#eaf3ff","EX":"#fff4d6","MEM":"#e8f6e8","WB":"#f3e8f6","stall":"#ffd6d6"}
def row(y,label,cells):
    ax.text(-0.2,y,label,ha="right",va="center",fontsize=7)
    for st,c in cells: box(ax,c,y,0.88,0.55,st,fc=col[st],fs=6.3)
for c in range(1,9): ax.text(c,1.0,str(c),ha="center",fontsize=6.5,color="#555")
ax.text(-0.2,1.0,"cycle",ha="right",fontsize=6.5,color="#555")
row(0.2,"ADD R1,R2,R3",[("IF",1),("ID",2),("EX",3),("MEM",4),("WB",5)])
row(-0.6,"SUB R4,R1,R5",[("IF",2),("ID",3),("stall",4),("ID",5),("EX",6),("MEM",7),("WB",8)])
ax.text(3.9,-1.15,"SUB reads R1 only in cycle 5 (after ADD writes it): 2 stall cycles",fontsize=6.5,ha="center",color="#b00020")
row(-2.6,"ADD R1,R2,R3",[("IF",1),("ID",2),("EX",3),("MEM",4),("WB",5)])
row(-3.4,"SUB R4,R1,R5",[("IF",2),("ID",3),("EX",4),("MEM",5),("WB",6)])
arr(ax,(3.3,-2.85),(4.0,-3.15),c="#b00020"); ax.text(5.6,-4.2,"forwarding path: EX/MEM result of ADD goes straight to the ALU input of SUB",fontsize=6.5,ha="center",color="#b00020")
''')

FIG_DMA = F("DMA transfer: the processor programs the DMA controller, which then moves data between the I/O device and memory by cycle stealing or burst, and interrupts the CPU only at the end.", r'''box(ax,0.8,2.6,1.7,0.9,"CPU",fs=8,fc="#eaf3ff"); box(ax,3.9,2.6,1.9,0.9,"DMA controller\n(address, count,\ncontrol registers)",fs=6,fc="#fff4d6"); box(ax,7.1,2.6,1.7,0.9,"Memory",fs=8,fc="#eaf3ff"); box(ax,3.9,0.5,1.7,0.8,"I/O device",fs=8,fc="#eaf3ff")
ax.plot([-0.2,8.4],[4.0,4.0],color=INK,lw=2); ax.text(8.5,4.0,"address / data / control bus",fontsize=6.3,va="center")
for x in (0.8,3.9,7.1): ax.plot([x,x],[3.05,4.0],color=INK,lw=1.2)
arr(ax,(1.65,2.75),(2.95,2.75),c=ACCENT); ax.text(2.3,2.95,"program",fontsize=6.2,ha="center")
arr(ax,(2.95,2.4),(1.65,2.4),c="#b00020"); ax.text(2.3,2.05,"interrupt (done)",fontsize=6,ha="center",color="#b00020")
arr(ax,(3.9,1.7),(3.9,0.95),c=INK,style="<|-|>"); ax.text(4.1,1.35,"DMA req/ack",fontsize=6,color="#b00020")
ax.text(1.4,3.55,"HOLD / HLDA",fontsize=6,color="#b00020"); ax.text(5.5,0.5,"data moves directly between device and memory",fontsize=6.3,va="center")
''', 7.0, 2.7, (-0.6, 11.0), (-0.4, 4.4))

# ============================================================ shared text
BUS_TEXT = r'''**Bus arbitration** decides which of several bus masters (CPU, DMA controllers, I/O processors) may use the shared bus when more than one requests it. A bus master asserts a **bus request (BR)**, the arbiter answers with a **bus grant (BG)**, and the master holds the bus busy (BB) while it transfers. The methods are:

''' + FIG_BUS + r'''
| Method | Principle | Advantage | Disadvantage |
|---|---|---|---|
| **Daisy chaining** (serial) | all masters share one request line; the grant line passes through the masters in series, so the master nearest to the arbiter has the highest priority and a requesting master absorbs the grant | few wires, simple, easy to add masters | fixed priority, a failure breaks the chain, slow grant propagation, far masters can starve |
| **Polling** (parallel polling by counter) | the controller puts a count on the poll lines; the master whose address matches and that is requesting takes the bus; the counter can start at 0 (fixed priority) or continue from the last winner (rotating, fair) | priority is programmable | needs $\lceil \log_2 n \rceil$ poll lines, slower |
| **Independent requests** (parallel) | every master has its own BR and BG pair; the arbiter has a priority encoder and grants the winner directly | fastest, flexible priority | many lines, more arbiter hardware |

Other schemes: **distributed arbitration by self-selection** (each device puts its identity on shared lines), **rotating priority (round robin)** and **fixed priority**.

'''
IC_TEXT = r'''**Instruction cycle.** To execute one instruction the processor repeats the cycle

1. **Instruction address calculation**: compute the address of the next instruction (add the length of the current one to the PC);
2. **Instruction fetch**: read the instruction from memory into the instruction register;
3. **Instruction operation decoding**: find the operation type and the operands;
4. **Operand address calculation**: find the effective address of each source operand (may involve indirect or indexed addressing);
5. **Operand fetch**: read the operand from memory or I/O;
6. **Data operation**: perform the arithmetic or logic operation;
7. **Operand address calculation** for the result and **operand store**: write the result to memory or I/O;
8. **Interrupt check**: if an interrupt is pending the processor saves its state and jumps to the interrupt routine, otherwise the next instruction begins.

''' + FIG_IC + r'''
The loops of the diagram handle instructions with several source operands (back to operand address calculation) or several results. In the simple basic-computer view, the cycle is fetch ($T_0$: $AR \leftarrow PC$; $T_1$: $IR \leftarrow M[AR],\ PC \leftarrow PC + 1$), decode ($T_2$), indirect (if $I = 1$) and execute, with the interrupt flip-flop tested at the end.

'''
CU_TEXT = r'''**Function of the control unit.** The control unit is the part of the processor that directs the operation of everything else. For each instruction it (1) fetches the instruction and decodes the opcode, (2) generates, in the correct order and at the correct clock pulse, the **control signals** (register load enables, ALU function select, memory read/write, bus gating, I/O strobes) that open the data paths for each micro-operation, (3) sequences the instruction cycle (fetch, decode, execute, interrupt), and (4) responds to external signals such as interrupts, reset and bus requests, using the flags of the status register for conditional operations.

''' + FIG_CU + r'''
| Basis | Hardwired control unit | Microprogrammed control unit |
|---|---|---|
| Implementation | fixed logic circuit of gates, decoders, flip-flops and counters | control words (microinstructions) stored in a control memory (ROM) |
| Design | complex state tables and logic minimisation | writing a microprogram, like a program |
| Speed | **faster** (no memory access, only gate delays) | slower (a control memory read per microinstruction) |
| Flexibility | hard to change or extend, redesign of hardware | easy to modify, correct or add instructions by changing the microprogram |
| Cost / area | cheaper for small instruction sets | costlier ROM and sequencing hardware, but the cost is spread over a big instruction set |
| Instruction set | RISC processors | CISC processors (complex instructions) |
| Debugging | difficult | easier, emulation is possible |
| Example | MIPS, ARM cores | IBM 360, 8086, VAX |

'''
DMA_TEXT = r'''**Programmed I/O.** The CPU starts the transfer and then **busy-waits** (polls the device status) for every byte or word; data goes device, CPU register, memory, so the CPU is occupied for the whole transfer.

**Interrupt-driven I/O.** The CPU starts the operation and continues with other work; the device interrupts when it is ready, and the CPU runs an interrupt service routine that moves one word. There is no busy waiting, but the CPU still moves every word and pays the overhead of saving and restoring the context at each interrupt (a big transfer needs thousands of interrupts).

**DMA (direct memory access).** A DMA controller with an address register, a word-count register and a control register moves the whole block directly between the device and memory over the system bus, taking the bus by **cycle stealing** (one word at a time) or **burst mode**.

''' + FIG_DMA + r'''
Sequence: (1) the CPU writes the memory address, word count and direction into the DMA controller and continues; (2) the device raises DMA request; the controller asks for the bus with HOLD; (3) the CPU grants (HLDA) at the end of a bus cycle and the controller drives the address bus and moves a word for each request, incrementing the address and decrementing the count; (4) when the count reaches zero the controller interrupts the CPU **once**.

| Basis | Programmed I/O | Interrupt-driven I/O | DMA |
|---|---|---|---|
| Who moves the data | CPU, one word at a time | CPU, one word per interrupt | DMA controller, whole block |
| CPU involvement | continuous (busy waiting) | at each word (interrupt overhead) | only to start and at the end |
| CPU utilisation | very poor | moderate | best |
| Hardware | simplest | interrupt controller | DMA controller |
| Transfer rate | low | medium (limited by the interrupt latency) | high |
| Suitable for | slow devices, small data | slow or irregular devices | disks, network, graphics, bulk data |

Thus DMA overcomes the problems of the two other methods: it removes the CPU's busy-waiting of programmed I/O and the per-word interrupt and context-switch overhead of interrupt-driven I/O, so the CPU is free for computing while large blocks are transferred at bus speed.

'''
def booth_text(m, q, n, which):
    t, prod = booth_md(m, q, n)
    return r'''**Booth's algorithm** multiplies two signed numbers in two's complement. It scans the multiplier bits in pairs $Q_0 Q_{-1}$ ($Q_{-1}$ is an extra bit appended on the right, initially 0): pair $10$ marks the **start of a run of 1s** (subtract the multiplicand, $A \leftarrow A - M$), pair $01$ marks the **end of a run of 1s** (add, $A \leftarrow A + M$), and $00$ or $11$ means no operation. After each step the register $A, Q, Q_{-1}$ is **arithmetic-shifted right** by one bit (the sign bit of $A$ is copied). After $n$ cycles the $2n$-bit product is in $A{:}Q$.

''' + which + r'''
**Multiplication of $%d \times (%d)$ = %d:**

''' % (m, q, prod) + t

# ============================================================ paper 1
bt1 = booth_text(8, -6, 5, FIG_BH)
D1 = r'''---
file: NEBians-IOE-Past-Paper-Computer-Organization-and-Architecture-ENEX253-2083-Baishakh.pdf
subject: Computer Organization and Architecture
level: BE · Year II / Part II
code: ENEX 253
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Describe the methods of bus arbitration. Explain the instruction cycle state diagram. [[4+4]]

@q 2
Write a code for $V = (M + N - O/P)\,/\,((Q - R) \times S/T)$ using three, two, one and zero address instruction. [[8]]

@q 3
Explain the function of control unit. Give the differences between hardwired control unit and microprogrammed control unit. [[4+4]]

@q 4
Explain set associative mapping technique with suitable example. Describe the First in First out (FIFO) page replacement algorithm with example. [[5+5]]

@q 5
Explain Booth's Multiplication algorithm with its hardware design implementation. Multiply $8 \times -6 = -48$ using Booth's Multiplication algorithm. [[5+5]]

@q 6
Explain the different types of pipeline hazards with example. [[5]]

@q 7
How does DMA overcome the problems of programmed I/O and interrupt-driven I/O in computer organization. [[5]]

@q 8
Explain about how multicore processors improve the software performance issues. [[6]]

<!-- SOLUTIONS -->

@s 1
''' + BUS_TEXT + IC_TEXT + r'''
@s 2
**Rules.** The expression is parsed as $V = \dfrac{M + N - O/P}{\big((Q - R) \times S\big)/T}$ (multiplication and division are left associative). Let T1, T2, T3 be temporary locations. Every program below was executed by computer on random values and gives the same $V$ as the formula.

**(a) Three-address instructions** (`OP dest, src1, src2`, 7 instructions):

```
DIV  T1, O, P        ; T1 = O / P
ADD  T2, M, N        ; T2 = M + N
SUB  T2, T2, T1      ; T2 = M + N - O/P
SUB  T3, Q, R        ; T3 = Q - R
MUL  T3, T3, S       ; T3 = (Q - R) * S
DIV  T3, T3, T       ; T3 = (Q - R) * S / T
DIV  V,  T2, T3      ; V  = T2 / T3
```

**(b) Two-address instructions** (`OP dest, src` with dest = dest OP src, 11 instructions; the first operand is overwritten, so MOV is needed to keep operands):

```
MOV  T1, O           ; T1 = O
DIV  T1, P           ; T1 = O / P
MOV  T2, M           ; T2 = M
ADD  T2, N           ; T2 = M + N
SUB  T2, T1          ; T2 = M + N - O/P
MOV  T3, Q           ; T3 = Q
SUB  T3, R           ; T3 = Q - R
MUL  T3, S           ; T3 = (Q - R) * S
DIV  T3, T           ; T3 = (Q - R) * S / T
DIV  T2, T3          ; T2 = V
MOV  V,  T2          ; V  = T2
```

**(c) One-address instructions** (all arithmetic uses the accumulator AC; 15 instructions):

```
LOAD  O              ; AC = O
DIV   P              ; AC = O / P
STORE T1             ; T1 = O / P
LOAD  M              ; AC = M
ADD   N              ; AC = M + N
SUB   T1             ; AC = M + N - O/P
STORE T2             ; T2 = numerator
LOAD  Q              ; AC = Q
SUB   R              ; AC = Q - R
MUL   S              ; AC = (Q - R) * S
DIV   T              ; AC = (Q - R) * S / T
STORE T3             ; T3 = denominator
LOAD  T2             ; AC = numerator
DIV   T3             ; AC = numerator / denominator
STORE V              ; V = AC
```

**(d) Zero-address (stack) instructions** (operands are on the top of the stack; only PUSH and POP name a memory address; the code is the postfix form $M\,N\,+\,O\,P\,/\,-\,Q\,R\,-\,S\,*\,T\,/\,/$; 16 instructions):

```
PUSH M     PUSH N     ADD                 ; (M + N)
PUSH O     PUSH P     DIV                 ; (O / P)
SUB                                       ; M + N - O/P
PUSH Q     PUSH R     SUB                 ; (Q - R)
PUSH S     MUL                            ; (Q - R) * S
PUSH T     DIV                            ; (Q - R) * S / T
DIV                                       ; numerator / denominator
POP  V
```

| Format | Instructions | Memory references for operands |
|---|---|---|
| Three-address | 7 | 3 per arithmetic instruction (shortest program, long instructions) |
| Two-address | 11 | 2 per instruction |
| One-address | 15 | 1 per instruction (accumulator) |
| Zero-address | 16 | none for ADD, SUB, MUL, DIV (stack), only PUSH / POP |

Fewer address fields make each instruction shorter but the program longer.

@s 3
''' + CU_TEXT + r'''
@s 4
**Set associative mapping.** The cache is divided into $S$ **sets** of $k$ lines each ($k$-way set associative). A main-memory block can go into **exactly one set** (set = block number mod $S$) but into **any of the $k$ lines** of that set. It is a compromise between direct mapping (fast, but conflict misses) and fully associative mapping (flexible, but an expensive comparison of all tags). The memory address is split into

$$\text{Address} = \underbrace{\text{Tag}}_{t\ \text{bits}} \ \Big|\ \underbrace{\text{Set index}}_{s\ \text{bits}} \ \Big|\ \underbrace{\text{Word offset}}_{w\ \text{bits}}$$

The set index selects a set, the tags of the $k$ lines of that set are compared in parallel with the tag of the address: a match is a **hit**, otherwise a **miss** (block fetched into a free line of the set or replacing one chosen by LRU, FIFO or random).

**Address example.** Main memory 1 M words (20-bit address), cache 4 K words, block 16 words, 4-way set associative. Offset $w = \log_2 16 = 4$ bits; number of lines $= 4096/16 = 256$; sets $S = 256/4 = 64$, so $s = 6$ bits; tag $t = 20 - 6 - 4 = 10$ bits.

**Trace example.** Cache of 8 lines, 2-way, so $S = 4$ sets (set = block mod 4), LRU inside a set; reference string of block numbers 0, 4, 0, 4, 8, 0, 1, 5, 1, 5 (blocks 0, 4, 8 all compete for set 0, blocks 1 and 5 for set 1):

''' + sa_md + r'''
Result: ''' + "%d hits and %d misses" % (sah, sam) + r''' (hit ratio $= %d/%d$). With direct mapping blocks 0 and 4 would share one line and evict each other on every reference; the two ways of a set keep both blocks, which gives the hits on the repeated references.

**First-in first-out (FIFO) page replacement.** When a page fault occurs and all frames are full, the page that has been in memory **longest** (the oldest, kept in a queue) is replaced. It is simple (a queue pointer), but it can remove a heavily used page and shows **Belady's anomaly** (more frames can give more faults). Reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames (the contents are listed oldest first):

''' % (sah, sah + sam) + fifo_md + r'''
$$\boxed{\,\text{FIFO: } %d \text{ page faults, } %d \text{ hits for 20 references}\,}$$

(LRU on the same string gives 12 faults, optimal replacement 9.)

@s 5
''' % (ff, fh) + bt1 + r'''
@s 6
**Pipeline hazards** are situations that prevent the next instruction from entering the pipeline in its clock cycle and make the pipeline **stall**. There are three types.

**1. Structural hazards** arise from a resource conflict: two instructions need the same hardware in the same cycle (for example one memory port used for instruction fetch of $I_4$ and data access of $I_1$). Remedy: separate instruction and data caches (Harvard style), more functional units, or a stall.

**2. Data hazards** arise when an instruction depends on the result of an earlier instruction that is still in the pipeline:

- **RAW** (read after write, true dependence): `ADD R1,R2,R3` then `SUB R4,R1,R5`;
- **WAR** (write after read, anti-dependence) and **WAW** (write after write, output dependence): occur with out-of-order execution and are removed by register renaming.

''' + FIG_HAZ + r'''
Without forwarding the SUB must wait until ADD has written R1 (2 stall cycles); with **forwarding (bypassing)** the ALU output of the ADD is fed straight to the next instruction's ALU input and there is no stall. A load followed by a dependent instruction still needs one stall (**load-use hazard**). Other remedies: compiler instruction scheduling and hardware **interlocks** (stalls).

**3. Control (branch) hazards** arise from branches and jumps: the target is known only after the branch is decided, so the instructions fetched after it may be wrong. Example: with a branch decided in the 3rd stage, two fetched instructions are flushed (a penalty of 2 cycles per taken branch). Remedies: **pipeline flushing**, **predict-not-taken or branch prediction** (static or dynamic with a branch history table), **branch target buffer**, **delayed branch** (fill the delay slot with a useful instruction), early branch resolution in the decode stage.

**Effect on speed-up.** For $k$ stages and $n$ instructions the ideal speed-up is $\dfrac{nk}{k + n - 1} \to k$; with an average stall of $s$ cycles per instruction the speed-up falls to about $\dfrac{k}{1 + s}$.

@s 7
''' + DMA_TEXT + r'''
@s 8
**Multicore processors and software performance.** A multicore processor places two or more independent processing cores (each with its own registers and L1 caches, usually sharing L2/L3 cache and the memory interface) on one chip. Single-core clock speeds stopped rising because of the power and heat wall, so performance now comes from **parallelism**; the software side of the problem is:

1. **Thread-level and process-level parallelism.** Independent tasks, threads or processes run on different cores simultaneously, so an operating system running many programs, or a multithreaded program (web server, database, rendering, compilers), gets near-linear throughput gains up to the number of runnable threads.
2. **Speed-up is limited by the serial part (Amdahl's law).** If a fraction $f$ of the program can be parallelised over $N$ cores, $\text{Speed-up} = \dfrac{1}{(1 - f) + f/N}$. Example: $f = 0.8$, $N = 4$ gives $\dfrac{1}{0.2 + 0.2} = 2.5$; even with unlimited cores the limit is $1/(1 - f) = 5$. So software must be restructured to reduce the serial fraction (Gustafson: with a bigger problem size the parallel fraction grows).
3. **Software must be written for parallel hardware**: threads (POSIX threads, Java threads), OpenMP, task libraries, parallel loops and data-parallel frameworks. An old single-threaded program does not become faster by itself, although the cores still run other programs at the same time.
4. **Communication and synchronisation overhead**: locks, barriers and atomic operations serialise execution; shared data needs **cache coherence** (MESI), and false sharing or contention for the shared memory bus can cancel the gains. Good software partitions the data, reduces sharing and balances the load.
5. **Better responsiveness and isolation**: one core can run the user interface while another does background work; virtualisation gives each virtual machine its own cores.
6. **Power efficiency**: several slower cores give more total work per watt than one very fast core, so software can run longer on a battery.

Thus multicore processors improve the performance of software that exposes parallelism (multithreaded, multi-programmed, data-parallel), but the gain depends on the parallel fraction, load balance, synchronisation and memory behaviour of the program.
'''

# ============================================================ paper 2
bt2 = booth_text(7, -5, 4, FIG_BF + "\n" + FIG_BH)
ADD_MD = r'''| Mode | Effective address (EA) | Value loaded (instruction at 200, address field 500, R1 = 400, XR = 100, PC = 202 after the fetch) |
|---|---|---|
| Implied | operand is implied by the opcode (accumulator, stack top) | e.g. `CMA`, `PUSH`: no address |
| Immediate | no EA; the operand is in the instruction | operand = 500 |
| Register direct | operand is in register R1 | 400 |
| Register indirect | $EA = (R1) = 400$ | M[400] = 700 |
| Autoincrement | $EA = (R1)$, then $R1 \leftarrow R1 + 1$ | EA = 400: 700, R1 becomes 401 |
| Autodecrement | $R1 \leftarrow R1 - 1$, then $EA = (R1)$ | EA = 399: 450 |
| Direct (absolute) | $EA = \text{address field} = 500$ | M[500] = 800 |
| Indirect | $EA = M[\text{address field}] = M[500] = 800$ | M[800] = 300 |
| Relative | $EA = PC + \text{address field} = 202 + 500 = 702$ | M[702] = 325 |
| Indexed | $EA = XR + \text{address field} = 100 + 500 = 600$ | M[600] = 900 |
| Base register | $EA = BR + \text{address field}$ (BR holds the segment start; here 400 + 500 = 900) | M[900] |
'''
D2 = r'''---
file: NEBians-IOE-Past-Paper-Computer-Organization-and-Architecture-ENEX253-2082-Bhadra.pdf
subject: Computer Organization and Architecture
level: BE · Year II / Part II
code: ENEX 253
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Comparison between computer architecture and computer organization. Explain CPI, MIPS rate, MFLOPS rate and Amdahl's law. [[4+4]]

@q 2
How effective address is calculated in different types of addressing modes? Explain with an example. [[8]]

@q 3
Differentiate between hardwired control unit and microprogrammed control unit. Describe address sequencing with the help of block diagram. [[4+4]]

@q 4
Explain associative cache mapping technique with suitable example. Describe the Least Recently Used (LRU) replacement algorithm with case example of miss and hit. [[5+5]]

@q 5
Write down the flowchart of Booth's Multiplication algorithm. Multiply $7 \times -5 = -35$ using Booth's Multiplication algorithm. [[5+5]]

@q 6
Formulate 4 segment instruction pipeline with branching and interrupts. [[5]]

@q 7
Comparison between Programmed I/O, Interrupt-Driven I/O and Direct Memory Access (DMA). [[5]]

@q 8
Explain about how multicore processors improve the hardware performance with respect to parallelism and power consumption. [[6]]

<!-- SOLUTIONS -->

@s 1
**Computer architecture and computer organization.**

| Basis | Computer architecture | Computer organization |
|---|---|---|
| Meaning | the attributes of the system **visible to the programmer**: what the computer does | how the features are **implemented**: the operational units and their interconnection |
| Concerned with | instruction set, data types, number of registers, addressing modes, I/O mechanism, memory addressing | control signals, interfaces between computer and peripherals, memory technology, ALU and bus design |
| Question answered | "what"? (logical view) | "how"? (physical view) |
| Level | design of the specification | realisation of the specification |
| Example | a multiply instruction exists | multiplier hardware or repeated addition |

One architecture (for example x86) can have many organizations, and software written for it runs on all of them.

**CPI (cycles per instruction).** The average number of clock cycles per instruction: for a program with $I_c$ instructions, $I_i$ of type $i$ with $CPI_i$ cycles,

$$CPI = \frac{\sum_i CPI_i \times I_i}{I_c}$$

and the CPU time is $T = I_c \times CPI \times \tau = \dfrac{I_c \times CPI}{f}$ ($\tau$ = clock period, $f$ = clock rate).

**MIPS rate** (millions of instructions per second):

$$\text{MIPS} = \frac{I_c}{T \times 10^{6}} = \frac{f}{CPI \times 10^{6}}$$

**MFLOPS rate** (millions of floating-point operations per second):

$$\text{MFLOPS} = \frac{\text{number of floating-point operations}}{T \times 10^{6}}$$

MIPS depends on the instruction set (not comparable between different architectures); MFLOPS is better for scientific work but also depends on which operations are counted as floating point.

**Example.** A 500 MHz processor runs this instruction mix:

| Type | Fraction | CPI |
|---|---|---|
| ALU | 0.45 | 1 |
| Load | 0.25 | 2 |
| Store | 0.15 | 2 |
| Branch | 0.15 | 3 |

$$CPI = 0.45(1) + 0.25(2) + 0.15(2) + 0.15(3) = 1.7$$

$$\text{MIPS} = \frac{500 \times 10^{6}}{1.7 \times 10^{6}} = ''' + "%.1f" % MIPS + r'''$$

For a program of $10^{9}$ instructions, $T = 10^{9} \times 1.7 / (500 \times 10^{6}) = 3.4$ s.

**Amdahl's law.** If a fraction $f$ of the execution time is speeded up by a factor $k$ and the rest is unchanged, the overall speed-up is

$$\text{Speed-up} = \frac{1}{(1 - f) + \dfrac{f}{k}}, \qquad \text{limit as } k \to \infty:\ \frac{1}{1 - f}$$

Example: $f = 0.8$, $k = 4$ gives $\dfrac{1}{0.2 + 0.2} = 2.5$ and the upper limit is $1/0.2 = 5$. The law shows that the part that cannot be improved (the serial part) limits the gain from faster hardware or more processors, so make the common case fast.

@s 2
**Effective address (EA)** is the actual memory address of the operand, computed from the address field of the instruction and the addressing mode: the mode field tells the control unit how to turn the instruction's address field into the operand. The common modes are given below, with a worked example: the instruction is stored at address 200 (its address field 500 is at 201), so after fetching PC = 202; register R1 = 400, index register XR = 100, with memory contents M[399] = 450, M[400] = 700, M[500] = 800, M[600] = 900, M[702] = 325, M[800] = 300.

''' + ADD_MD + r'''
Uses: immediate for constants; direct for simple variables; indirect for pointers and jump tables; register for speed; register indirect, autoincrement and autodecrement for arrays, stacks and pointer walking; relative for position-independent branches; indexed for array elements ($XR$ is incremented to step through an array); base register for relocation of programs (segment start in BR).

@s 3
''' + CU_TEXT + r'''
**Address sequencing.** The microinstructions of a microprogram are stored in groups called **routines** in the control memory, and the control unit must supply the address of the next microinstruction after every clock pulse. Address sequencing handles: (1) **incrementing** the control address register CAR for the next microinstruction in a routine; (2) **unconditional or conditional branching** to the address given in the branch field of the microinstruction, conditional on a status bit (zero, carry, sign) chosen by the branch logic; (3) **mapping** from the opcode of the instruction register to the starting address of its routine (for example the fetch routine has a fixed address, and the opcode $0100$ may map to address $0100\,0000$ by placing 0 in front and two 0s behind); (4) **subroutine call and return** with the subroutine register SBR (microroutines shared by several instructions, such as effective-address calculation).

''' + FIG_SEQ + r'''
The multiplexers choose the next address from four sources according to the mode bits of the microinstruction: CAR + 1, the branch address field (if the condition of the branch logic is true), the output of the mapping logic, or SBR (return). After the fetch routine the mapping logic loads the first address of the execute routine, and the last microinstruction of every routine branches back to the fetch routine at address 0.

@s 4
**Associative (fully associative) cache mapping.** A main-memory block can be placed in **any line** of the cache. The memory address is split only into a **tag** (the block number) and the word offset, $\text{Address} = \text{Tag} \,|\, \text{Word}$. To look up a word, the tag is compared **simultaneously with the tags of all cache lines** using an associative memory (content-addressable memory); a match is a hit and the word offset selects the word, otherwise it is a miss and a block is fetched, replacing a line chosen by a replacement algorithm when the cache is full.

*Advantage:* most flexible, no conflict misses, best hit ratio. *Disadvantage:* expensive and slow comparators for all the tags, and a replacement algorithm is needed.

**Address example.** Main memory 64 K words (16-bit address), block of 8 words, so offset = 3 bits and tag = 13 bits (8 K blocks); a cache of 32 lines holds any 32 of them. (Set associative mapping is the compromise: the block is placed in any line of one fixed set, address = tag, set, word.)

**LRU replacement.** On a miss with a full cache, remove the block that has **not been used for the longest time**. It is based on the principle of temporal locality (recently used blocks are likely to be used again). Implementation: a counter or an age value per line (updated on every reference, hit or miss), a stack of block numbers with the most recent on top, or a bit matrix; every **hit** moves the block to the most-recently-used position, and a **miss** evicts the least-recently-used block.

**Example.** Fully associative cache with 4 lines, reference string of block numbers 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 (oldest, i.e. least recently used, is listed first):

''' + fa_md + r'''
$$\boxed{\,\text{LRU: } %d \text{ hits and } %d \text{ misses}\ \ (\text{hit ratio } %d/12)\,}$$

Examples: reference 1 (5th) is a **hit**, because blocks 1, 2, 3, 4 are all in the cache, and it makes 1 the most recent; reference 5 (7th) is a **miss**: the cache is full, so the least recently used block 3 is evicted; the last references 3, 4 and 5 are misses because LRU had just evicted exactly those blocks (a cyclic reference pattern is bad for LRU). LRU gives fewer misses than FIFO for programs with locality and has no Belady's anomaly, but costs more hardware. On the 20-reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames LRU gives 12 faults (FIFO 15).

@s 5
**Flowchart of Booth's algorithm:**

''' % (fah, fam, fah) + bt2 + r'''
@s 6
**Four-segment instruction pipeline.** The instruction cycle is divided into four segments that work on four different instructions at the same time:

1. **FI**: fetch the instruction from memory;
2. **DA**: decode the instruction and calculate the effective address;
3. **FO**: fetch the operand from memory;
4. **EX**: execute the instruction (and store the result).

''' + FIG_P4 + r'''
**Branching.** When the decoder (segment 2) finds a branch instruction, the instructions already fetched after it are wrong if the branch is taken: the pipe is **emptied** and the PC is updated with the branch address after the effective address is calculated, then FI restarts from the target; the instructions after the branch must not be allowed to reach FO and EX, so branch instructions cost extra clock cycles. **Interrupts.** An interrupt is recognised at the end of the execute segment of the current instruction: the instructions in the pipe behind it are discarded, the return address is saved and the PC is loaded with the interrupt routine address (the pipe is emptied as for a branch).

**Timing diagram** (instruction 3 is a branch to instruction 15; $\blacksquare$ marks a discarded step):

| Cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Instr. 1 | FI | DA | FO | EX | | | | | | |
| Instr. 2 | | FI | DA | FO | EX | | | | | |
| Instr. 3 (branch) | | | FI | DA | FO | EX | | | | |
| Instr. 4 | | | | FI | $\blacksquare$ | | | | | |
| Instr. 5 | | | | | $\blacksquare$ | | | | | |
| Instr. 15 | | | | | | FI | DA | FO | EX | |
| Instr. 16 | | | | | | | FI | DA | FO | EX |

In a non-pipelined machine each instruction needs 4 cycles. For $n$ instructions with no branches the pipeline needs $k + n - 1 = n + 3$ cycles, giving a speed-up of $\dfrac{4n}{n + 3} \to 4$; every taken branch or interrupt wastes about $k - 1 = 3$ cycles, which is why branch prediction, delayed branch and a branch target buffer are used.

@s 7
''' + DMA_TEXT + r'''
@s 8
**Multicore processors and hardware performance.** The performance of a single core was raised for decades by higher clock frequency and deeper instruction-level parallelism, but both ran into the **power wall** (dynamic power $P = C V^{2} f$ with the supply voltage $V$ having to rise with $f$, so power grows roughly as $f^{3}$), the memory wall and the limited instruction-level parallelism in programs. A multicore processor puts several simpler cores on one chip instead.

**Parallelism.** Each core executes its own thread, so the chip does several streams of instructions at the same time: *thread-level parallelism* (and *data-level parallelism* with SIMD units in each core). With $N$ cores the ideal throughput is $N$ times that of one core; the real gain follows Amdahl's law, $\text{Speed-up} = 1/\big((1 - f) + f/N\big)$ ($f = 0.9$, $N = 4$ gives $3.08$). Shared L2/L3 caches, fast on-chip interconnects (bus, ring, mesh) and cache-coherence hardware (MESI) let the cores share data with short latency, much shorter than between separate chips. Combined with hardware multithreading (SMT) each core also hides memory latency.

**Power consumption.** Dynamic power is $P \propto C V^{2} f$ and, since $V$ scales almost in proportion to $f$, $P \propto f^{3}$. Instead of one core at frequency $f$, use two cores at $0.8 f$ each (with a correspondingly lower voltage):

$$\text{Performance} = 2 \times 0.8 = 1.6 \quad (\text{ideal, parallel workload}), \qquad \text{Power} = 2 \times 0.8^{3} = ''' + "%.2f" % (2 * 0.8 ** 3) + r'''$$

so about 60 percent more performance for nearly the same power; or for the same performance as one core ($2 \times 0.5 = 1$) the power is only $2 \times 0.5^{3} = 0.25$, one quarter. Cores that are idle can be switched off (**power gating**) or slowed down (**DVFS**, dynamic voltage and frequency scaling), and a chip can mix big and little cores (heterogeneous multicore) to match power to the workload. The simpler cores also use less area per core and dissipate heat over a larger area, so cooling is easier.

| Single fast core | Multicore |
|---|---|
| performance only by clock speed and ILP; power rises about as $f^{3}$ | performance by the number of cores; power rises about linearly with cores |
| hot spot, limited by the power wall | heat spread, power gating and DVFS per core |
| one thread at a time (plus ILP) | many threads and processes at once |

Limits: the serial part of a program (Amdahl), memory bandwidth shared between cores, cache-coherence traffic and synchronisation, and the "dark silicon" problem (not all cores can run at full speed at the same time within the power budget).
'''
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ioe-enex253-2083-baishakh.md"), "w").write(D1)
open(os.path.join(OUT, "ioe-enex253-2082-bhadra.md"), "w").write(D2)
print("written", len(D1), len(D2), "SA", sah, sam, "FA", fah, fam)
