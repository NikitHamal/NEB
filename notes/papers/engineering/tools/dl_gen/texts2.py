from texts1 import *

# ---------------- timing diagrams ----------------
def timing_fig(caption, states, names, ripple=False, d=0.07, neg=False, extra=""):
    nq = len(names); n = len(states) - 1
    ystep = 0.95
    clk_y = nq * ystep + 0.3
    off = 0.5 if neg else 0.0
    code = f"clock(ax,0,{clk_y},{n})\n"
    for k in range(n + 1):
        pass
    code += "guides(ax,%r,%s,-0.1)\n" % ([k + off for k in range(n)], clk_y + 0.7)
    for f in range(nq):
        bit = nq - 1 - f
        lv = (states[0] >> bit) & 1
        tr = [(0.0, lv)]
        for k in range(1, n + 1):
            nb = (states[k] >> bit) & 1
            if nb != lv:
                tr.append((round(k - 1 + off + 0.05 + (d * bit if ripple else 0), 3), nb)); lv = nb
        yy = (nq - 1 - f) * ystep + 0.1
        code += "wave(ax,%s,%r,%s,%r)\n" % (yy, tr, n, names[f])
    code += extra
    xh = 1.2 if extra else 0.0
    W = n + 2.6; H = clk_y + 1.1 + xh
    return figblock(caption, code, w=5.9, h=round(max(1.6, 5.9 * H / W), 2), xlim="(-1.9,%s)" % (n + 0.7), ylim="(-0.3,%s)" % round(clk_y + 0.9 + xh, 2))

def count_states(seq_fn, n, s0=0):
    s = [s0]
    for _ in range(n): s.append(seq_fn(s[-1]))
    return s

# ---------------- flip flops ----------------
def latch_vs_ff():
    return tbl(["Point", "Latch", "Flip-flop"], [
        ["Triggering", "Level sensitive: the output follows the input the whole time the enable is active", "Edge triggered: the output can change only at the rising (or falling) edge of the clock"],
        ["Clock", "Enable / gate signal (no clock edge)", "Clock with edge-detector (master-slave or edge circuit)"],
        ["Race / transparency", "Transparent while enabled, so a changing input appears at the output (race-around possible)", "Not transparent; samples the input only at the edge"],
        ["Circuit", "Built from cross-coupled gates (NOR or NAND) plus steering gates", "Built from two latches (master + slave) or latch + edge detector"],
        ["Synchronisation", "Asynchronous or gated, hard to synchronise", "Synchronous, used in counters, registers and state machines"],
        ["Example", "SR latch, gated D latch (7475)", "D, JK, T flip-flop (7474, 7476)"]])

def d_to_jk():
    code = r'''
fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.8,9.6),ylim=(-1.2,3.9))
P=ffb(ax,5.0,0.3,"D flip-flop","D",w=1.3,h=1.8,qn=True)
Dp=P["D"]; ck=P["CK"]
# gates: J.Q' and K'.Q then OR
ins1,o1=gn(ax,"AND",0.8,3.0,n=2,w=0.9,lead=0.3)
ins2,o2=gn(ax,"AND",0.8,1.4,n=2,w=0.9,lead=0.3)
ino,oo=gn(ax,"OR",3.1,2.2,n=2,w=0.9,lead=0.3)
L(ax,[o1,(2.7,o1[1]),(2.7,ino[0][1]),ino[0]]); L(ax,[o2,(2.7,o2[1]),(2.7,ino[1][1]),ino[1]])
L(ax,[oo,(4.2,oo[1]),(4.2,Dp[1]),Dp]) if False else L(ax,[oo,(4.4,oo[1]),(4.4,Dp[1]),Dp])
T(ax,ins1[0][0]-0.1,ins1[0][1],"J",ha="right"); T(ax,ins2[1][0]-0.1,ins2[1][1],"K",ha="right")
# K' into gate2 top input via inverter
iin,iout=inv(ax,-1.2,ins2[0][1],w=0.45,h=0.45,lead=0.1); L(ax,[iout,ins2[0]]); T(ax,iin[0]-0.1,iin[1],"K",ha="right")
L(ax,[(ins2[1][0],ins2[1][1]),(ins2[1][0]-0.3,ins2[1][1])]) 
T(ax,ins2[1][0]-0.1,ins2[1][1],"",ha="right")
# feedback Q' -> gate1 lower input, Q -> gate2 lower input
qn=P["QN"]; q=P["Q"]
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-0.9),(-0.2,-0.9),(-0.2,ins1[1][1]),ins1[1]])
L(ax,[q,(q[0]+0.8,q[1]),(q[0]+0.8,-0.6)]) if False else None
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q",ha="left"); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'$",ha="left")
L(ax,[(q[0]+0.5,q[1]),(q[0]+0.5,-0.55),(0.1,-0.55),(0.1,ins2[1][1]),ins2[1]]); dot(ax,q[0]+0.5,q[1])
T(ax,ck[0]-0.1,ck[1],"CLK",ha="right")
'''
    return ("**Latch vs flip-flop.**\n\n" + latch_vs_ff() +
            "\n**Modifying a D flip-flop into a JK flip-flop.** A JK flip-flop obeys the characteristic equation\n\n"
            "$$Q^{+} = J\\overline{Q} + \\overline{K}\\,Q$$\n\nA D flip-flop obeys $Q^{+} = D$. Hence if the D input is driven by the combinational logic\n\n"
            "$$\\boxed{D = J\\overline{Q} + \\overline{K}Q}$$\n\nthe D flip-flop behaves exactly like a JK flip-flop. Check with the excitation table:\n\n" +
            tbl(["J", "K", "Q", "D = J Q' + K' Q", "Q⁺", "Action"], [[0, 0, 0, 0, 0, "hold"], [0, 0, 1, 1, 1, "hold"], [0, 1, 0, 0, 0, "reset"], [0, 1, 1, 0, 0, "reset"], [1, 0, 0, 1, 1, "set"], [1, 0, 1, 1, 1, "set"], [1, 1, 0, 1, 1, "toggle"], [1, 1, 1, 0, 0, "toggle"]]) +
            "\nTwo AND gates, one OR gate and one inverter (the logic block below) are needed, with $Q$ and $\\overline{Q}$ fed back.\n\n" +
            figblock("JK flip-flop from a D flip-flop: D = J Q' + K' Q.", code, canvas=False))

def sr_to_jk():
    code = r'''
fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.6,9.6),ylim=(-0.6,4.2))
P=ffb(ax,4.6,0.5,"SR flip-flop","SR",w=1.4,h=2.4)
S=P["S"]; R=P["R"]; ck=P["CK"]; q=P["Q"]; qn=P["QN"]
i1,o1=gn(ax,"AND",1.8,S[1],n=2,w=0.9,lead=0.3)
i2,o2=gn(ax,"AND",1.8,R[1]-0.15,n=2,w=0.9,lead=0.3)
L(ax,[o1,S]); L(ax,[o2,(o2[0]+0.1,o2[1]),(o2[0]+0.1,R[1]),R]) if abs(o2[1]-R[1])>1e-6 else L(ax,[o2,R])
T(ax,i1[0][0]-0.1,i1[0][1],"J",ha="right"); T(ax,i2[1][0]-0.1,i2[1][1],"K",ha="right")
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-0.1),(0.9,-0.1),(0.9,i1[1][1]),i1[1]])
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q",ha="left"); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'$",ha="left")
L(ax,[(q[0]+0.6,q[1]),(q[0]+0.6,-0.45),(0.5,-0.45),(0.5,i2[0][1]),i2[0]]); dot(ax,q[0]+0.6,q[1])
T(ax,ck[0]-0.1,ck[1],"CLK",ha="right")
'''
    return ("**Converting an SR flip-flop into a JK flip-flop.**\n\n"
            "*Step 1 - excitation table of the SR flip-flop* (what $S,R$ must be for each $Q\\to Q^{+}$ change):\n\n" +
            tbl(["Q", "Q⁺", "S", "R"], [[0, 0, 0, "X"], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, "X", 0]]) +
            "\n*Step 2 - truth table of the required JK flip-flop with the S, R needed:*\n\n" +
            tbl(["J", "K", "Q", "Q⁺", "S", "R"], [[0, 0, 0, 0, 0, "X"], [0, 0, 1, 1, "X", 0], [0, 1, 0, 0, 0, "X"], [0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0], [1, 0, 1, 1, "X", 0], [1, 1, 0, 1, 1, 0], [1, 1, 1, 0, 0, 1]]) +
            "\n*Step 3 - K-maps* (rows $J$, columns $KQ$ in Gray order $00, 01, 11, 10$):\n\n"
            "| S | KQ=00 | 01 | 11 | 10 |\n|---|---|---|---|---|\n| J=0 | 0 | X | 0 | 0 |\n| J=1 | 1 | X | 0 | 1 |\n\n"
            "| R | KQ=00 | 01 | 11 | 10 |\n|---|---|---|---|---|\n| J=0 | X | 0 | 1 | X |\n| J=1 | 0 | 0 | 1 | 0 |\n\n"
            "Looping the 1s with the don't-cares: for S the cells $J\\overline{Q}$ (J = 1, Q = 0: columns 00 and 10, using the X for Q = 1 in the K = 0 column is not needed); for R the pair $KQ=11$ in both rows:\n\n"
            "$$\\boxed{S = J\\,\\overline{Q}} \\qquad \\boxed{R = K\\,Q}$$\n\n"
            "*Step 4 - circuit.* Two 2-input AND gates fed back from the outputs:\n\n" +
            figblock("JK flip-flop from an SR flip-flop: S = J Q', R = K Q.", code, canvas=False) +
            "\nThe forbidden state $S=R=1$ never occurs, because $S=J\\overline{Q}$ and $R=KQ$ cannot both be 1; with $J=K=1$ the flip-flop toggles. (It still needs a master-slave or edge-triggered SR to avoid race-around.)\n")

# ---------------- shift registers ----------------
def sipo(data="1010"):
    n = 4
    # chain A (first FF) .. D; serial in
    states = []
    reg = [0] * 4
    hist = [tuple(reg)]
    for b in data:
        reg = [int(b)] + reg[:-1]; hist.append(tuple(reg))
    # states as integer with QA as MSB bit index 3 ... use order QA,QB,QC,QD top to bottom
    st = [sum(v << (3 - i) for i, v in enumerate(h)) for h in hist]
    din = [int(c) for c in data]
    code = r'''
fig,ax=ckt_canvas(5.9,2.2,xlim=(-1.6,15),ylim=(-0.2,3.0))
Ps=[ffb(ax,0.2+3.6*i,0.6,"FF"+"ABCD"[i],"D",w=1.2,h=1.5,qn=False) for i in range(4)]
for i in range(3):
    L(ax,[Ps[i]["Q"],Ps[i+1]["D"]])
for i,P in enumerate(Ps):
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]) if i==3 else None
    L(ax,[(P["Q"][0]+0.55,P["Q"][1]),(P["Q"][0]+0.55,0.1)]) if False else None
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"ABCD"[i],size=8.2,ha="left")
    L(ax,[P["CK"],(P["CK"][0],0.25)]); dot(ax,P["CK"][0],0.25)
L(ax,[(Ps[0]["CK"][0],0.25),(Ps[3]["CK"][0],0.25)]); T(ax,Ps[0]["CK"][0]-0.1,0.25,"CLK",ha="right")
L(ax,[(Ps[0]["D"][0]-0.7,Ps[0]["D"][1]),Ps[0]["D"]]); T(ax,Ps[0]["D"][0]-0.75,Ps[0]["D"][1],"Serial in",ha="right")
L(ax,[Ps[3]["Q"],(Ps[3]["Q"][0]+0.5,Ps[3]["Q"][1])]); 
'''
    return states_wrap(st, data, code, din)

def states_wrap(st, data, code, din):
    # return (block text for sipo) assembled by caller
    return dict(st=st, code=code, din=din, data=data)

def sipo_text(data="1010"):
    r = sipo(data)
    st = r["st"]
    n = len(data)
    tm = timing_fig(f"Timing diagram of the 4-bit SIPO register for the serial input {data} (QA is the first stage, QD the last; the bits appear in QD..QA after four clock pulses).", st, ["QA", "QB", "QC", "QD"],
                    extra="wave(ax,%s,%r,%s,'Din')\n" % (4 * 0.95 + 1.5, [(0.0, int(data[0]))] + [(round(k + 0.5 - 0.5, 3), int(data[k])) for k in range(1, n) if data[k] != data[k - 1]], n))
    tm = tm.replace("ylim=(-0.3,", "ylim=(-0.3,").replace("clock(ax,0,%s,%d)" % (4 * 0.95 + 0.3, n), "clock(ax,0,%s,%d)" % (4 * 0.95 + 0.3, n))
    rows = []
    reg = ["0"] * 4
    rows.append(["initial", "-", *reg])
    for k, b in enumerate(data):
        reg = [b] + reg[:3]
        rows.append([k + 1, b, *reg])
    return ("**4-bit SIPO (serial-in, parallel-out) shift register.** It consists of four D flip-flops with a common clock; the output $Q$ of each stage drives the $D$ input of the next, and the serial data enter the first stage. At every rising clock edge each flip-flop copies the previous stage, so the data move one place to the right. After $n=4$ clock pulses the 4 serial bits are present together at $Q_A\\dots Q_D$ (parallel output); the parallel word can be read when the 4th pulse has ended.\n\n" +
            figblock("4-bit SIPO shift register built from four D flip-flops (clock common to all stages).", r["code"], canvas=False) +
            f"\n**Working for the serial input {data}** (the first bit applied is {data[0]}, the last {data[-1]}; the register is first cleared):\n\n" +
            tbl(["Clock pulse", "Serial in", "QA", "QB", "QC", "QD"], rows) +
            f"\nAfter the fourth pulse $Q_AQ_BQ_CQ_D = {''.join(reg)}$, i.e. $Q_DQ_CQ_BQ_A = {''.join(reversed(reg))} = {data}$, the word applied serially, now available in parallel.\n\n" + tm)

def piso(data="1101"):
    n = 4
    # after load, shift out Q_D first
    reg = [int(c) for c in data]  # QA..QD
    hist = [tuple(reg)]
    for _ in range(4):
        reg = [0] + reg[:3]; hist.append(tuple(reg))
    st = [sum(v << (3 - i) for i, v in enumerate(h)) for h in hist]
    code = r'''
fig,ax=ckt_canvas(5.9,3.2,xlim=(-2.2,15.6),ylim=(-1.2,4.4))
Ps=[ffb(ax,1.0+3.7*i,0.8,"FF"+"ABCD"[i],"D",w=1.2,h=1.5,qn=False) for i in range(4)]
for i in range(4):
    P=Ps[i]
    iy=3.4
    # 2:1 selection: AND(load.Pi) OR AND(shift.Q_prev)
    ins,o=gn(ax,"AND",P["D"][0]-1.45-1.0+0.2,2.95,n=2,w=0.7,lead=0.15) if False else (None,None)
    T(ax,P["D"][0]-0.25,P["D"][1]+0.27,"mux",size=7,color=MUTED) if False else None
    # data inputs
    T(ax,P["D"][0]-0.9,3.9,"P"+"ABCD"[i],size=8.4)
    L(ax,[(P["D"][0]-0.9,3.65),(P["D"][0]-0.9,3.15)])
    mux(ax,P["D"][0]-1.6,2.62,2,[None,None],[],out="",sp=0.55,w=0.9,name="2:1") if False else None
# draw tiny 2:1 selectors as boxes
for i,P in enumerate(Ps):
    bx=P["D"][0]-0.95
    box(ax,bx,P["D"][1]-0.35,0.6,0.7,"2:1",size=7.4)
    L(ax,[(bx+0.6,P["D"][1]),P["D"]])
    L(ax,[(bx-0.0,P["D"][1]+0.17),(bx-0.2,P["D"][1]+0.17),(bx-0.2,3.3)]) ; T(ax,bx-0.2,3.55,"P"+"ABCD"[i],size=8.2)
    if i==0:
        L(ax,[(bx,P["D"][1]-0.17),(bx-0.45,P["D"][1]-0.17)]); T(ax,bx-0.5,P["D"][1]-0.17,"0",ha="right",size=8.2)
    else:
        q=Ps[i-1]["Q"]; L(ax,[q,(q[0]+0.2,q[1]),(q[0]+0.2,0.35),(bx-0.35,0.35),(bx-0.35,P["D"][1]-0.17),(bx,P["D"][1]-0.17)])
    L(ax,[(bx+0.3,P["D"][1]-0.35),(bx+0.3,-0.35)]); dot(ax,bx+0.3,-0.35) if False else None
    L(ax,[P["CK"],(P["CK"][0],-0.8)]); dot(ax,P["CK"][0],-0.8)
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"ABCD"[i],size=8.2,ha="left") if i<3 else None
for i,P in enumerate(Ps):
    L(ax,[(P["D"][0]-0.95+0.3,P["D"][1]-0.35),(P["D"][0]-0.95+0.3,-0.35)])
L(ax,[(Ps[0]["D"][0]-0.65,-0.35),(Ps[3]["D"][0]-0.65,-0.35)]); T(ax,Ps[0]["D"][0]-0.75,-0.35,"SH/$\\overline{LD}$",ha="right",size=8.2)
for i,P in enumerate(Ps): dot(ax,P["D"][0]-0.65,-0.35)
L(ax,[(Ps[0]["CK"][0],-0.8),(Ps[3]["CK"][0],-0.8)]); T(ax,Ps[0]["CK"][0]-0.1,-0.8,"CLK",ha="right",size=8.2)
L(ax,[Ps[3]["Q"],(Ps[3]["Q"][0]+0.6,Ps[3]["Q"][1])]); T(ax,Ps[3]["Q"][0]+0.7,Ps[3]["Q"][1],"Serial out",ha="left",size=8.4)
'''
    return st, code

def piso_text(data="1101"):
    st, code = piso(data)
    reg = [int(c) for c in data]
    rows = [["load", *reg, "-"]]
    cur = reg[:]
    outs = []
    for k in range(4):
        out = cur[-1]; outs.append(out)
        cur = [0] + cur[:3]
        rows.append([k + 1, *cur, out])
    tm = timing_fig(f"Timing diagram of the 4-bit PISO register: parallel word {data} loaded (SH/LD = 0) then shifted out serially (SH/LD = 1), LSB side (QD) first.", st, ["QA", "QB", "QC", "QD"],
                    extra="wave(ax,%s,%r,%s,'SH/LD')\n" % (4 * 0.95 + 1.5, [(0.0, 0), (0.5, 1)], 4))
    return ("**4-bit PISO (parallel-in, serial-out) shift register.** Each D input is fed by a 2-to-1 selector (two AND gates and an OR gate) controlled by the line $SH/\\overline{LD}$. With $SH/\\overline{LD}=0$ the parallel inputs $P_A\\dots P_D$ are loaded into the four flip-flops at the next clock pulse; with $SH/\\overline{LD}=1$ each stage takes the output of the previous stage (the first stage takes 0) and the data move towards $Q_D$, from where they leave serially, one bit per clock pulse.\n\n" +
            figblock("4-bit PISO shift register: a 2:1 selector in front of each D input chooses between parallel load and shift.", code, canvas=False) +
            f"\n**Operation for the parallel word $P_AP_BP_CP_D = {data}$:**\n\n" +
            tbl(["Clock pulse", "QA", "QB", "QC", "QD", "Serial out (before the pulse)"], rows) +
            f"\nThe serial output sequence read at $Q_D$ is {', '.join(map(str, outs))}, that is the word {data} sent out last bit first (D, C, B, A). Four clock pulses empty the register; the next pulse can load a new word.\n\n" + tm)

def shift_types():
    return ("A **shift register** is a chain of flip-flops with a common clock in which the stored word moves one position per clock pulse. According to how the data enter and leave there are four types:\n\n" +
            tbl(["Type", "Data in", "Data out", "Use"], [["SISO", "Serial", "Serial", "Delay line (n clock pulses), serial memory"], ["SIPO", "Serial", "Parallel", "Serial-to-parallel conversion (UART receiver)"], ["PISO", "Parallel", "Serial", "Parallel-to-serial conversion (UART transmitter)"], ["PIPO", "Parallel", "Parallel", "Temporary storage, buffer register"]]) +
            "\nBesides these, a shift register can shift in either direction (**bidirectional**) or be a **universal** register (parallel load + left shift + right shift), and when its output is fed back to the input it becomes a **ring counter** or a **Johnson (twisted-ring) counter**.\n\n"
            "**Johnson counter.** The inverted output of the last flip-flop, $\\overline{Q_D}$, is connected back to the serial input of the first. An $n$-bit register then has $2n$ distinct states (mod-$2n$ counter): for $n=4$, 8 states, $0000\\to1000\\to1100\\to1110\\to1111\\to0111\\to0011\\to0001\\to0000$. Each state is decoded by a 2-input AND gate (no decoding glitches), and the output frequency of any stage is $f/2n$.\n")

def johnson(n=3):
    code = r'''
fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.4,12.6),ylim=(-1.9,3.0))
Ps=[ffb(ax,0.4+3.4*i,0.6,"FF"+"012"[i],"D",w=1.2,h=1.5,qn=True) for i in range(3)]
for i in range(2): L(ax,[Ps[i]["Q"],Ps[i+1]["D"]])
for i,P in enumerate(Ps):
    L(ax,[P["CK"],(P["CK"][0],-0.3)]); dot(ax,P["CK"][0],-0.3)
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"012"[i],size=8.2,ha="left") if i<2 else None
L(ax,[(Ps[0]["CK"][0],-0.3),(Ps[2]["CK"][0],-0.3)]); T(ax,Ps[0]["CK"][0]-0.1,-0.3,"CLK",ha="right")
q=Ps[2]["Q"]; qn=Ps[2]["QN"]; d0=Ps[0]["D"]
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-1.2),(d0[0]-0.6,-1.2),(d0[0]-0.6,d0[1]),d0]); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'_2$",ha="left",size=8.2)
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q$_2$",ha="left")
'''
    st = [0]; s = (0, 0, 0)
    seq = []
    cur = [0, 0, 0]
    for _ in range(8):
        cur = [1 - cur[2]] + cur[:2]; seq.append(cur[:])
    rows = [[k + 1, *seq[k]] for k in range(6)]
    states = [0] + [sum(v << (2 - i) for i, v in enumerate(s)) for s in seq]
    tm = timing_fig("Timing diagram of the 3-bit Johnson counter (6 states, each output is a square wave of frequency f/6, shifted by one clock period).", states[:8], ["Q0", "Q1", "Q2"])
    return ("**Johnson counter (3-bit example).** The shift register of three D flip-flops has $\\overline{Q_2}$ connected back to $D_0$.\n\n" +
            figblock("3-bit Johnson (twisted-ring) counter.", code, canvas=False) +
            "\nStarting from 000 the sequence is\n\n" + tbl(["Clock", "Q0", "Q1", "Q2"], [[0, 0, 0, 0]] + rows) +
            "\nafter which 000 recurs: $2n=6$ states, so the counter divides the clock by 6, and every output has a 50 % duty cycle.\n\n" + tm)

# ---------------- ripple counters ----------------
def ripple_up(nbits=3, neg=False):
    # positive-edge FFs, clock of FF(i+1) from Q'(i)
    names = ["Q%d" % i for i in range(nbits - 1, -1, -1)]
    code = f'''
fig,ax=ckt_canvas(5.9,2.2,xlim=(-1.6,{4*nbits+2.5}),ylim=(-0.4,3.0))
Ps=[ffb(ax,0.4+4.0*i,0.6,"FF%d"%i,"T",w=1.3,h=1.6,qn=True,neg={neg}) for i in range({nbits})]
for i,P in enumerate(Ps):
    T(ax,P["T"][0]-0.1,P["T"][1],"1",ha="right",size=8.4)
for i in range({nbits}-1):
    Pa,Pb=Ps[i],Ps[i+1]
    src=Pa["{ 'Q' if neg else 'QN' }"]
    L(ax,[src,(src[0]+0.5,src[1]),(src[0]+0.5,0.05),(Pb["CK"][0]-0.45,0.05),(Pb["CK"][0]-0.45,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
for i,P in enumerate(Ps):
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]); T(ax,P["Q"][0]+0.55,P["Q"][1],"Q%d"%i,ha="left",size=8.4)
'''
    return code

def async_up3():
    code = ripple_up(3)
    seq = count_states(lambda s: (s + 1) % 8, 8)
    tm = timing_fig("Timing diagram of the 3-bit ripple up counter (rising-edge clock). Each Q changes slightly after the one before it (propagation delay), and each stage halves the frequency.", seq, ["Q2", "Q1", "Q0"], ripple=True, d=0.08)
    rows = [[k, *format(k % 8, "03b")] for k in range(9)]
    return ("**3-bit asynchronous (ripple) up counter with positive-edge triggered clock.** Three T flip-flops (JK flip-flops with $J=K=1$) are cascaded. The external clock drives only the first stage. Since each flip-flop toggles on a *rising* edge, the clock of the next stage is taken from the **complemented output $\\overline{Q}$ of the previous stage**: $\\overline{Q}$ rises when $Q$ falls, so the next stage toggles when the previous bit goes from 1 to 0 (the carry).\n\n" +
            figblock("3-bit ripple up counter built from rising-edge toggle flip-flops (clock of each stage from Q' of the previous one).", code, canvas=False) +
            "\n**Operation.** $Q_0$ toggles on every clock pulse, so its frequency is $f/2$; $Q_1$ toggles whenever $Q_0$ falls, giving $f/4$; $Q_2$ toggles whenever $Q_1$ falls, giving $f/8$. The count is $Q_2Q_1Q_0$:\n\n" +
            tbl(["Clock pulse", "Q2", "Q1", "Q0"], rows) +
            "\nThe counter has $2^3 = 8$ states (mod-8) and returns to 000 on the 8th pulse.\n\n" + tm +
            "\nBecause the stages respond one after another, the total settling time is $n\\,t_{pd}$, which limits the clock frequency to $f_{max} \\le 1/(n\\,t_{pd}+t_{decode})$. This is the price of the simplicity of the asynchronous counter.\n")

def bcd_async():
    code = r'''
fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.6,19.6),ylim=(-2.4,3.0))
Ps=[ffb(ax,0.4+4.2*i,0.6,"FF%d"%i,"JK",w=1.3,h=1.7,qn=True) for i in range(4)]
for i,P in enumerate(Ps):
    T(ax,P["J"][0]-0.1,P["J"][1],"1",ha="right",size=8.2); T(ax,P["K"][0]-0.1,P["K"][1],"1",ha="right",size=8.2)
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]); T(ax,P["Q"][0]+0.55,P["Q"][1],"Q%d"%i,ha="left",size=8.4)
for i in range(3):
    Pa,Pb=Ps[i],Ps[i+1]
    src=Pa["QN"]; L(ax,[src,(src[0]+0.6,src[1]),(src[0]+0.6,0.05),(Pb["CK"][0]-0.5,0.05),(Pb["CK"][0]-0.5,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
# NAND of Q3 and Q1 -> clear (all flip-flops)
ins,o=gn(ax,"NAND",9.0,-1.3,n=2,w=0.9,lead=0.3)
q3=Ps[3]["Q"]; q1=Ps[1]["Q"]
L(ax,[(q1[0]+0.25,q1[1]),(q1[0]+0.25,ins[1][1]),ins[1]]) if False else None
L(ax,[(Ps[1]["Q"][0]+0.3,Ps[1]["Q"][1]),(Ps[1]["Q"][0]+0.3,ins[1][1]),ins[1]]); dot(ax,Ps[1]["Q"][0]+0.3,Ps[1]["Q"][1])
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.2),(8.3,-2.2),(8.3,ins[0][1]),ins[0]]) if False else None
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.0),(7.7,-2.0),(7.7,ins[0][1]),ins[0]]); dot(ax,Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1])
T(ax,o[0]+0.15,o[1],"to CLR of\nall four FFs",ha="left",size=7.8)
T(ax,13.2,2.55,"clear (active low) when Q3Q2Q1Q0 = 1010",size=7.8,color=MUTED)
'''
    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    tm = timing_fig("Timing diagram of the asynchronous BCD counter: counts 0 to 9 and returns to 0 at the tenth pulse (the 1010 state lasts only a few nanoseconds, so it is not seen as a valid count).", seq, ["Q3", "Q2", "Q1", "Q0"], ripple=True, d=0.07)
    rows = [[k, *format(k, "04b")] for k in range(10)] + [["10 (momentary)", *"1010"], ["10 -> 0", *"0000"]]
    return ("**Asynchronous BCD (decade, mod-10) counter.** A 4-bit ripple counter naturally counts 0 to 15. To make it count only 0 to 9, the counter is **cleared as soon as the count 10 (1010) is reached**: the outputs $Q_3$ and $Q_1$ (the first two 1s of 1010) are NANDed, and the active-low NAND output is applied to the asynchronous clear (CLR) inputs of all four flip-flops.\n\n" +
            figblock("Asynchronous BCD counter: 4-bit ripple counter (JK flip-flops with J = K = 1) with a NAND gate on Q3 and Q1 driving the clear inputs.", code, canvas=False) +
            "\n**Operation.**\n\n1. The clock drives $FF_0$; each following flip-flop is clocked by $\\overline{Q}$ of the previous stage, so the outputs count in binary 0000, 0001, ..., 1001.\n"
            "2. On the tenth pulse the counter tries to go to 1010; the moment $Q_3=Q_1=1$, the NAND output goes low, clears all flip-flops and the counter returns to 0000. The state 1010 exists only for about one propagation delay.\n"
            "3. $Q_3$ is high only for counts 8 and 9, so it gives one pulse for every ten clock pulses: **frequency division by 10**.\n\n" +
            tbl(["Clock pulse", "Q3", "Q2", "Q1", "Q0"], rows) + "\n" + tm)

def async_mod12(neg=False):
    # JK, positive edge, clear on 1100 -> Q3 and Q2 NAND
    code = bcd_async.__defaults__ if False else None
    code = r'''
fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.6,19.6),ylim=(-2.4,3.0))
Ps=[ffb(ax,0.4+4.2*i,0.6,"FF%d"%i,"JK",w=1.3,h=1.7,qn=True) for i in range(4)]
for i,P in enumerate(Ps):
    T(ax,P["J"][0]-0.1,P["J"][1],"1",ha="right",size=8.2); T(ax,P["K"][0]-0.1,P["K"][1],"1",ha="right",size=8.2)
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]); T(ax,P["Q"][0]+0.55,P["Q"][1],"Q%d"%i,ha="left",size=8.4)
for i in range(3):
    Pa,Pb=Ps[i],Ps[i+1]
    src=Pa["QN"]; L(ax,[src,(src[0]+0.6,src[1]),(src[0]+0.6,0.05),(Pb["CK"][0]-0.5,0.05),(Pb["CK"][0]-0.5,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
ins,o=gn(ax,"NAND",9.0,-1.3,n=2,w=0.9,lead=0.3)
L(ax,[(Ps[2]["Q"][0]+0.3,Ps[2]["Q"][1]),(Ps[2]["Q"][0]+0.3,ins[1][1]),ins[1]]); dot(ax,Ps[2]["Q"][0]+0.3,Ps[2]["Q"][1])
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.0),(7.7,-2.0),(7.7,ins[0][1]),ins[0]]); dot(ax,Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1])
T(ax,o[0]+0.15,o[1],"to CLR of\nall four FFs",ha="left",size=7.8)
T(ax,13.2,2.55,"clear (active low) when Q3Q2Q1Q0 = 1100",size=7.8,color=MUTED)
'''
    seq = list(range(12)) + [0, 1, 2]
    tm = timing_fig("Timing diagram of the mod-12 asynchronous counter (rising-edge clock): the state 1100 is momentary and clears the counter to 0000.", seq, ["Q3", "Q2", "Q1", "Q0"], ripple=True, d=0.07)
    rows = [[k, *format(k, "04b")] for k in range(12)] + [["12 (momentary)", *"1100"], ["12 -> 0", *"0000"]]
    return ("**Mod-12 asynchronous counter (JK flip-flops, positive-edge clock).** $2^4=16 > 12 > 2^3 = 8$, so four flip-flops are needed. The counter must skip the states 12 to 15, so it is reset when the count 12 ($1100$) is reached. The first state with $Q_3=Q_2=1$ is 1100, and no earlier count has both high, so a 2-input NAND of $Q_3$ and $Q_2$ detects it; the NAND output (active low) clears all the flip-flops.\n\n"
            "All JK inputs are tied to 1 (toggle mode). The clock goes to $FF_0$, and since the flip-flops are positive-edge triggered, each later stage is clocked from $\\overline{Q}$ of the previous one (so it toggles when the previous bit falls).\n\n" +
            figblock("Mod-12 ripple counter with JK flip-flops: NAND of Q3 and Q2 clears the counter.", code, canvas=False) +
            "\n**Count sequence.**\n\n" + tbl(["Clock pulse", "Q3", "Q2", "Q1", "Q0"], rows) + "\n" + tm +
            "\n$Q_3$ goes high for counts 8 to 11 only, so it is a square-ish wave at $f/12$ (high for 4 of 12 clock periods).\n")

def async_updown3_neg():
    # 3-bit up/down async, negative edge triggered
    code = r'''
fig,ax=ckt_canvas(5.9,3.0,xlim=(-1.6,15.4),ylim=(-1.6,4.4))
Ps=[ffb(ax,0.6+4.6*i,0.6,"FF%d"%i,"T",w=1.3,h=1.6,qn=True,neg=True) for i in range(3)]
for i,P in enumerate(Ps):
    T(ax,P["T"][0]-0.1,P["T"][1],"1",ha="right",size=8.4)
    L(ax,[P["Q"],(P["Q"][0]+0.4,P["Q"][1])]) if i==2 else None
    T(ax,P["Q"][0]+0.45,P["Q"][1],"Q%d"%i,ha="left",size=8.4) if i==2 else None
# clock of stage i+1 selected by mode M: M=0 up (clock from Q), M=1 down (clock from Q')
for i in range(2):
    Pa,Pb=Ps[i],Ps[i+1]
    ia,oa=gn(ax,"AND",Pa["Q"][0]+1.0,3.5,n=2,w=0.8,lead=0.2)
    ib,ob=gn(ax,"AND",Pa["Q"][0]+1.0,2.3,n=2,w=0.8,lead=0.2)
    io,oo=gn(ax,"OR",Pa["Q"][0]+2.7,2.9,n=2,w=0.8,lead=0.2) if False else (None,None)
    L(ax,[Pa["Q"],(Pa["Q"][0]+0.3,Pa["Q"][1]),(Pa["Q"][0]+0.3,ia[0][1]),ia[0]]); dot(ax,Pa["Q"][0]+0.3,Pa["Q"][1])
    L(ax,[Pa["QN"],(Pa["QN"][0]+0.55,Pa["QN"][1]),(Pa["QN"][0]+0.55,ib[0][1]),ib[0]]); dot(ax,Pa["QN"][0]+0.55,Pa["QN"][1])
    T(ax,ia[1][0]-0.05,ia[1][1],"$\\overline{M}$",ha="right",size=7.6); T(ax,ib[1][0]-0.05,ib[1][1],"M",ha="right",size=7.6)
    ig,og=gn(ax,"OR",Pa["Q"][0]+2.55,2.9,n=2,w=0.8,lead=0.2)
    L(ax,[oa,(og[0]-1.35,oa[1]),(og[0]-1.35,ig[0][1]),ig[0]]) if False else L(ax,[oa,(ig[0][0]-0.2,oa[1]),(ig[0][0]-0.2,ig[0][1]),ig[0]])
    L(ax,[ob,(ig[1][0]-0.2,ob[1]),(ig[1][0]-0.2,ig[1][1]),ig[1]])
    L(ax,[og,(og[0]+0.2,og[1]),(og[0]+0.2,0.0),(Pb["CK"][0]-0.5,0.0),(Pb["CK"][0]-0.5,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
T(ax,-1.4,4.2,"M = 0 : up counting     M = 1 : down counting",size=8,ha="left",color=MUTED)
'''
    up = count_states(lambda s: (s + 1) % 8, 8)
    dn = count_states(lambda s: (s - 1) % 8, 8, 7)
    tm1 = timing_fig("Up mode (M = 0): Q0 toggles on every falling clock edge and each higher bit toggles on the falling edge of the previous Q.", up, ["Q2", "Q1", "Q0"], ripple=True, d=0.08, neg=True)
    tm2 = timing_fig("Down mode (M = 1): the clock of the next stage is taken from Q' of the previous stage, so the count falls 7, 6, ..., 0.", dn, ["Q2", "Q1", "Q0"], ripple=True, d=0.08, neg=True)
    return code, tm1, tm2

# ---------------- gate-level building blocks ----------------
def comparator3():
    code = r'''
fig,ax=ckt_canvas(5.9,3.9,xlim=(-0.5,14.5),ylim=(-3.6,6.4))
names=["A2","B2","A1","B1","A0","B0"]
xs={}
for i,nm in enumerate(names):
    xs[nm]=0.4+0.55*i; T(ax,xs[nm],6.0,nm,size=8.2)
    L(ax,[(xs[nm],5.7),(xs[nm],-3.2)],lw=1.1,color="#4a5565")
# XNOR for each pair
xn={}
for k,(a,b) in enumerate([("A2","B2"),("A1","B1"),("A0","B0")]):
    y=-0.6 if False else 4.3-1.9*k
    ins,o=ckt_gate_xnor(ax,5.0,y) if False else gn(ax,"NAND",5.0,y,n=2,w=0.9,lead=0.3)
    L(ax,[(xs[a],ins[0][1]),ins[0]]); dot(ax,xs[a],ins[0][1]); L(ax,[(xs[b],ins[1][1]),ins[1]]); dot(ax,xs[b],ins[1][1])
    T(ax,o[0]+0.1,y+0.25,"x%d"%(2-k),size=7.6,ha="left")
'''
    return code

# ---------------- logic families ----------------
def logic_families():
    return ("A **logic family** is a group of digital ICs that use the same circuit technology (and hence the same voltage levels, speed and power) so that they can be connected to each other directly. The main families are **RTL, DTL, TTL (bipolar transistor-transistor logic), ECL (emitter-coupled logic)** and **MOS/CMOS**. Their performance is compared by the following characteristics:\n\n"
            "1. **Propagation delay** $t_{pd}$ - the time for a change at the input to appear at the output (average of $t_{pHL}$ and $t_{pLH}$, measured between the 50 % points); it sets the speed.\n"
            "2. **Power dissipation** $P_D$ - the supply power per gate ($V_{CC}\\times I_{CC}$). For CMOS it is mostly dynamic ($P = C V^2 f$) and tiny when static.\n"
            "3. **Speed-power product** - $t_{pd}\\times P_D$ in picojoules, the single figure of merit of a family.\n"
            "4. **Fan-out** - the number of similar gate inputs one output can drive without leaving the valid logic levels.\n"
            "5. **Fan-in** - the number of inputs a gate has.\n"
            "6. **Noise margin** - the largest noise voltage that does not change the logic level: $NM_H = V_{OH(min)} - V_{IH(min)}$, $NM_L = V_{IL(max)} - V_{OL(max)}$.\n"
            "7. **Logic levels** $V_{OH}, V_{OL}, V_{IH}, V_{IL}$, and the supply voltage range.\n"
            "8. **Current-sourcing / sinking capacity** $I_{OH}, I_{OL}, I_{IH}, I_{IL}$, and **cost/packing density** (CMOS has the highest integration density).\n\n" +
            tbl(["Parameter", "Standard TTL (74)", "CMOS (4000B / 74HC)", "ECL (10K)"], [
                ["Supply", "5 V ± 5 %", "3 to 15 V (4000B), 2 to 6 V (74HC)", "-5.2 V"],
                ["Propagation delay (gate)", "10 ns", "50 ns (4000B), 8 ns (74HC)", "2 ns"],
                ["Power per gate", "10 mW", "~ 0.01 mW static, rises with f", "25 mW"],
                ["Speed-power product", "100 pJ", "~ 1 pJ at low f", "50 pJ"],
                ["Fan-out", "10", "> 50", "25"],
                ["Noise margin", "0.4 V", "~ 45 % of VDD", "0.2 V"],
                ["$V_{OH}$ / $V_{OL}$", "3.4 V / 0.2 V", "≈ VDD / ≈ 0 V", "-0.9 V / -1.75 V"],
                ["Notes", "Very common, totem-pole output", "Lowest power, high density, slow in older series", "Fastest, non-saturating, high power"]]) )

def cmos_nand():
    code = r'''
fig,ax=ckt_canvas(5.9,4.2,xlim=(-2.2,9.0),ylim=(-5.0,6.0))
p1=mosfet(ax,0.8,3.0,kind="p"); p2=mosfet(ax,4.0,3.0,kind="p")
na=mosfet(ax,3.0,-1.0,kind="n"); nb=mosfet(ax,3.0,-3.2,kind="n")
# supply rail
L(ax,[(p1["D"][0],5.0),(p2["D"][0],5.0)]); L(ax,[p1["D"],(p1["D"][0],5.0)]); L(ax,[p2["D"],(p2["D"][0],5.0)]); T(ax,p2["D"][0]+0.15,5.35,"+V$_{DD}$",ha="left",size=8.6)
# output node
yo=1.0
L(ax,[(p1["S"][0],p1["S"][1]),(p1["S"][0],yo),(p2["S"][0],yo),(p2["S"][0],p2["S"][1])]); dot(ax,p2["S"][0],yo)
L(ax,[(p2["S"][0],yo),(8.0,yo)]); T(ax,8.1,yo,"Y",ha="left",size=9)
L(ax,[na["D"],(na["D"][0],yo)]); dot(ax,na["D"][0],yo)
L(ax,[nb["S"],(nb["S"][0],-4.5)]); L(ax,[(nb["S"][0]-0.4,-4.5),(nb["S"][0]+0.4,-4.5)]); L(ax,[(nb["S"][0]-0.25,-4.65),(nb["S"][0]+0.25,-4.65)]); L(ax,[(nb["S"][0]-0.1,-4.8),(nb["S"][0]+0.1,-4.8)])
# inputs
L(ax,[(-1.0,-1.0),(-1.0,3.0)]); dot(ax,-1.0,-1.0); L(ax,[(-1.0,3.0),p1["G"]]); L(ax,[(-1.0,-1.0),na["G"]]); T(ax,-1.1,-1.0,"A",ha="right",size=9)
L(ax,[(-1.8,-3.2),nb["G"]]); T(ax,-1.9,-3.2,"B",ha="right",size=9)
L(ax,[(2.0,-3.2),(2.0,3.0),p2["G"]]); dot(ax,2.0,-3.2)
T(ax,6.2,3.0,"PMOS pair\n(parallel pull-up)",size=7.8,color=MUTED,ha="left"); T(ax,5.4,-2.1,"NMOS pair\n(series pull-down)",size=7.8,color=MUTED,ha="left")
'''
    return code

def cmos_nand_text():
    return ("**Two-input CMOS NAND gate.** Two PMOS transistors in **parallel** form the pull-up network (between $+V_{DD}$ and the output) and two NMOS transistors in **series** form the pull-down network (between the output and ground). Both inputs $A$ and $B$ drive one PMOS and one NMOS gate.\n\n" +
            figblock("Circuit of a 2-input CMOS NAND gate (PMOS in parallel on top, NMOS in series below).", cmos_nand(), canvas=False) +
            "\n**Logic operation.**\n\n" +
            tbl(["A", "B", "PMOS A", "PMOS B", "NMOS A", "NMOS B", "Output Y"], [[0, 0, "on", "on", "off", "off", "1 (pulled to VDD)"], [0, 1, "on", "off", "off", "on", "1"], [1, 0, "off", "on", "on", "off", "1"], [1, 1, "off", "off", "on", "on", "0 (pulled to ground)"]]) +
            "\nIf either input is low, at least one PMOS conducts and at least one NMOS of the series chain is open: $Y=1$. Only when $A=B=1$ do both NMOS conduct (path to ground) and both PMOS turn off: $Y=0$. So $Y = \\overline{AB}$. In every steady state exactly one of the two networks is off, so there is no DC path from $V_{DD}$ to ground and the static power is almost zero.\n")

def ttl_char():
    return ("**Characteristics of the TTL logic family** (standard 74 series):\n\n"
            "- **Basic gate:** NAND, with a multi-emitter input transistor and a *totem-pole* output stage (two transistors, one pulls the output up, the other pulls it down); the supply is $V_{CC}= +5$ V ± 5 %.\n"
            "- **Logic levels:** $V_{IH(min)} = 2$ V, $V_{IL(max)} = 0.8$ V, $V_{OH(min)} = 2.4$ V (typ. 3.4 V), $V_{OL(max)} = 0.4$ V (typ. 0.2 V).\n"
            "- **Noise margin:** $NM_H = 2.4-2.0 = 0.4$ V, $NM_L = 0.8-0.4 = 0.4$ V.\n"
            "- **Propagation delay:** about 10 ns per gate.\n"
            "- **Power dissipation:** about 10 mW per gate (so the speed-power product is about 100 pJ).\n"
            "- **Fan-out:** 10 standard loads ($I_{OL} = 16$ mA, $I_{IL}=1.6$ mA).\n"
            "- **Unused inputs** float to logic 1 (high); they should still be tied to a defined level to avoid noise pick-up.\n"
            "- **Variants:** Schottky (74S), low-power Schottky (74LS), advanced versions (74AS, 74ALS, 74F), with different speed/power trade-offs; open-collector and tri-state outputs for bus connection.\n")

# ---------------- time / frequency measurement ----------------
def time_measure():
    code = r'''
fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.6,17.0),ylim=(-1.2,4.6))
box(ax,0.0,2.4,3.0,1.2,"Input pulse\n(start/stop)",size=7.8)
box(ax,4.4,2.4,2.6,1.2,"Control\nflip-flop",size=7.8)
box(ax,0.0,0.2,3.0,1.2,"Crystal\noscillator",size=7.8)
box(ax,4.4,0.2,2.6,1.2,"Divider /\npulse shaper",size=7.8)
ins,o=gn(ax,"AND",8.4,2.0,n=2,w=0.9,lead=0.4)
box(ax,10.8,1.4,2.6,1.2,"Decade\ncounter",size=7.8); box(ax,14.0,1.4,2.2,1.2,"Display",size=7.8)
arr(ax,(3.0,3.0),(4.4,3.0)); arr(ax,(3.0,0.8),(4.4,0.8))
L(ax,[(7.0,3.0),(7.7,3.0),(7.7,ins[0][1]),ins[0]]); L(ax,[(7.0,0.8),(7.7,0.8),(7.7,ins[1][1]),ins[1]])
arr(ax,o,(10.8,2.0)); arr(ax,(13.4,2.0),(14.0,2.0))
T(ax,5.7,4.0,"gate: open for the interval T",size=7.8,color=MUTED); T(ax,5.7,-0.4,"clock pulses of period T$_c$",size=7.8,color=MUTED)
'''
    return code

def time_measure_text():
    return ("**Time-interval (period) measurement.** A digital time-measuring instrument counts the number of pulses of a *known, accurate clock* that occur during the unknown interval.\n\n" +
            figblock("Functional diagram of a digital time-interval meter.", time_measure(), canvas=False) +
            "\n**Working.**\n\n1. A crystal oscillator and divider produce clock pulses of known period $T_c$ (e.g. 1 MHz gives $T_c = 1\\ \\mu s$).\n"
            "2. The start pulse (rising edge of the input) sets the control flip-flop, opening the AND gate; the stop pulse resets it and closes the gate. So the gate is open for exactly the unknown interval $T$.\n"
            "3. While the gate is open the clock pulses pass to the decade counter, which counts $N$ pulses.\n"
            "4. The display shows $T = N\\,T_c$. The resolution is $\\pm T_c$ (one count), so a faster clock gives better resolution, e.g. $N = 2347$ with $T_c = 1\\ \\mu s$ gives $T = 2.347$ ms.\n\n"
            "The same arrangement gives the **period of a periodic signal** (gate open for one period of the input; use several periods and divide for small errors).\n")

def freq_measure_text():
    code = r'''
fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.6,19.0),ylim=(-1.2,4.6))
box(ax,0.0,2.4,3.0,1.2,"Signal\nconditioner\n(Schmitt trigger)",size=7.4)
box(ax,0.0,0.0,3.0,1.2,"Crystal\noscillator",size=7.8)
box(ax,4.4,0.0,2.6,1.2,"Decade\ndivider",size=7.8)
box(ax,8.0,0.0,2.6,1.2,"Gate flip-flop\n(T = 1 s)",size=7.4)
ins,o=gn(ax,"AND",8.6,3.0,n=2,w=0.9,lead=0.4)
box(ax,11.8,2.4,2.6,1.2,"Decade\ncounter",size=7.8); box(ax,15.0,2.4,2.6,1.2,"Latch +\ndisplay",size=7.6)
arr(ax,(3.0,3.0),(ins[0][0],ins[0][1])); arr(ax,(3.0,0.6),(4.4,0.6)); arr(ax,(7.0,0.6),(8.0,0.6))
L(ax,[(9.3,1.2),(9.3,2.0),(7.6,2.0),(7.6,ins[1][1]),ins[1]]) if False else L(ax,[(9.3,1.2),(9.3,1.8),(6.6,1.8),(6.6,ins[1][1]),ins[1]])
arr(ax,o,(11.8,3.0)); arr(ax,(14.4,3.0),(15.0,3.0))
T(ax,7.0,4.2,"unknown frequency f$_x$",size=7.8,color=MUTED)
'''
    return ("**Frequency measurement (frequency counter).** Frequency is the number of cycles per second, so a digital frequency counter counts the cycles of the unknown signal during a **precise 1 s gate time** derived from a crystal oscillator.\n\n" +
            figblock("Functional diagram of a digital frequency counter.", code, canvas=False) +
            "\n**Working.**\n\n1. The unknown signal (sine, any shape) is squared by a **Schmitt-trigger signal conditioner**, giving clean pulses, one per cycle.\n"
            "2. A crystal oscillator (say 1 MHz) is divided by decade dividers to give very accurate gate pulses; the gate flip-flop output is high for exactly $T = 1$ s (or 0.1 s, 10 s for other ranges).\n"
            "3. The AND gate passes the input pulses to the decade counter only while the gate is high; the counter counts $N$ pulses.\n"
            "4. At the end of the gate the count is transferred to the latch/display and the counter is reset for the next measurement.\n\n"
            "$$f_x = \\frac{N}{T}$$\n\nFor $T=1$ s the display reads $f_x$ directly in hertz; with $T=0.1$ s a decimal point is shifted. The uncertainty is $\\pm 1$ count, i.e. $\\pm 1/T$ hertz, plus the crystal error. At *low* frequencies the **period-measuring mode** is used instead (count clock pulses during one input period), which gives a better resolution.\n")
