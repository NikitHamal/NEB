"""Figure-block strings for the Microprocessors and Microcontrollers (ENEX 251) papers.
Each function returns a ```figure ...``` block (code runs inside the paper pipeline: plt, INK, ACCENT are provided)."""

PRE = '''import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
'''


def fig(caption, body):
    return '```figure caption="%s"\n%s%s\n```\n' % (caption, PRE, body.strip('\n'))


def biu_eu():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.2)
ax.add_patch(mp.Rectangle((0.2,0.3),6.4,8.6,fc="#f6f9ff",ec=INK,lw=1.2,ls="--",zorder=1)); ax.text(3.4,8.6,"Bus Interface Unit (BIU)",ha="center",fontsize=9,weight="bold")
ax.add_patch(mp.Rectangle((8.2,0.3),6.4,8.6,fc="#fffaf0",ec=INK,lw=1.2,ls="--",zorder=1)); ax.text(11.4,8.6,"Execution Unit (EU)",ha="center",fontsize=9,weight="bold")
# BIU
for i,(n) in enumerate(["ES","CS","SS","DS"]): box(ax,1.0+i*1.1,7.5,1.0,0.6,n,fs=7.5,fc=BLUE)
box(ax,3.4,6.5,5.8,0.6,"Instruction pointer (IP)",fs=7.5,fc=BLUE)
box(ax,3.4,5.4,5.8,0.8,"Address adder\\n(segment x 16 + offset = 20-bit address)",fs=6.3,fc=YEL)
box(ax,3.4,3.9,5.8,1.0,"Instruction queue\\n6 bytes (FIFO): 1 | 2 | 3 | 4 | 5 | 6",fs=7,fc=GRN)
box(ax,3.4,2.2,5.8,0.9,"Bus control logic\\n(address, data, control signals)",fs=7)
box(ax,3.4,0.8,5.8,0.0001,"",fs=1,ec="white")
# EU
box(ax,9.7,7.5,2.6,0.7,"Control circuitry",fs=7,fc=YEL); box(ax,12.9,7.5,2.6,0.7,"Instr. decoder",fs=7,fc=YEL)
for i,n in enumerate(["AX (AH AL)","BX (BH BL)","CX (CH CL)","DX (DH DL)"]): box(ax,9.7+(i%2)*3.2,6.0-(i//2)*0.85,3.0,0.65,n,fs=7,fc=BLUE)
for i,n in enumerate(["SP","BP","SI","DI"]): box(ax,9.0+i*1.35,3.9,1.2,0.6,n,fs=7.5,fc=BLUE)
box(ax,9.7,2.7,2.6,0.8,"ALU",fs=9,fc=YEL); box(ax,12.9,2.7,2.6,0.8,"Flag register",fs=7.5,fc=BLUE)
box(ax,11.4,1.2,5.8,0.6,"Temporary operand registers",fs=7,fc=GRN)
# connections
arr(ax,(6.6,5.4),(8.2,5.4),c=INK,style="<|-|>"); ax.text(7.4,5.7,"internal\\nbus",fontsize=6.3,ha="center")
arr(ax,(3.4,3.4),(3.4,2.65),c=ACCENT,style="<|-|>"); arr(ax,(3.4,4.4+0.5),(3.4,5.05),c=ACCENT); arr(ax,(3.4,6.2),(3.4,5.75),c=ACCENT)
arr(ax,(6.3,3.9),(7.5,3.9),c=INK); ax.text(7.45,4.2,"to decoder",fontsize=6.3,ha="center")
arr(ax,(3.4,1.75),(3.4,0.62),c=INK,style="<|-|>"); ax.text(3.4,0.45,"system bus (A0-A19, D0-D15)",fontsize=7,ha="center")
arr(ax,(11.6,7.5),(11.0,7.5),c=INK,sa=0)
'''
    return fig("Internal block diagram of the 8086: the Bus Interface Unit (left) fetches instructions into the 6-byte queue and forms 20-bit addresses; the Execution Unit (right) decodes and executes them.", body)


def decode_fig(c1, c2, g1, g2a, g2b, cap):
    """c1/c2 = (name, size, range, Y index, addr lines text, via_or)"""
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,8.9)
C1=%r; C2=%r; G1=%r; G2A=%r; G2B=%r
# address bus labels
ax.text(0.1,8.5,"8085 address bus",fontsize=8,weight="bold")
for n,y in [("A15",7.6),("A14",6.7),("A13",5.8),("A12",4.9)]:
    ax.text(0.2,y,n,fontsize=7.5,va="center"); ax.plot([1.0,2.5],[y,y],color=INK,lw=1)
box(ax,3.9,5.35,2.8,5.1,"74LS138\\n3:8 decoder",fs=8,fc=YEL)
for lab,y in [("A",4.9),("B",5.8),("C",6.7)]: ax.text(2.6,y,lab,fontsize=7,va="center")
ax.text(3.9,8.15,"G1=%%s   G2A=%%s   G2B=%%s"%%(G1,G2A,G2B),fontsize=6.8,ha="center")
for k in range(8):
    y=7.55-0.62*k; ax.plot([5.3,6.0],[y,y],color=INK,lw=1); ax.text(5.05,y,"Y%%d"%%k,fontsize=6.2,ha="right",va="center")
def ypos(k): return 7.55-0.62*k
y1=ypos(C1[3]); box(ax,11.9,6.6,3.6,1.9,"%%s\\n%%s KB\\n%%s"%%(C1[0],C1[1],C1[2]),fs=7.5,fc=BLUE)
ax.plot([6.0,8.0,8.0,10.1],[y1,y1,6.1,6.1],color=ACCENT,lw=1.3); ax.text(10.15,6.1,"CS",fontsize=6.5,va="center",ha="left",color="#b00020",bbox=dict(fc="white",ec="none",pad=0.3))
ax.text(11.9,5.3,C1[4],fontsize=6.5,ha="center")
y2=ypos(C2[3]); box(ax,11.9,2.6,3.6,1.9,"%%s\\n%%s KB\\n%%s"%%(C2[0],C2[1],C2[2]),fs=7.5,fc=GRN)
ax.add_patch(mp.Polygon([(7.2,3.4),(7.2,2.0),(8.4,2.7)],fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(7.55,2.7,"OR",fontsize=6.5,ha="center",va="center",zorder=4)
ax.plot([6.0,6.3,6.3,7.2],[y2,y2,3.1,3.1],color=ACCENT,lw=1.3)
ax.text(0.2,1.8,"A11",fontsize=7.5,va="center"); ax.plot([1.0,6.7,6.7,7.2],[1.8,1.8,2.3,2.3],color=INK,lw=1.2)
ax.text(5.2,1.95,"A11",fontsize=6.5)
ax.plot([8.4,9.0,9.0,10.1],[2.7,2.7,2.6,2.6],color=ACCENT,lw=1.3); ax.text(10.15,2.6,"CS",fontsize=6.5,va="center",color="#b00020",bbox=dict(fc="white",ec="none",pad=0.3))
ax.text(11.9,1.3,C2[4],fontsize=6.5,ha="center")
ax.text(7.4,0.35,"Low address lines (A0-A11 / A0-A10) go straight to the chips; the data bus D0-D7 connects every chip",fontsize=6.3,ha="center")
''' % (c1, c2, g1, g2a, g2b)
    return fig(cap, body)


def cycles_fig(instr, clk, cap):
    third = "IO read" if instr == "IN" else "IO write"
    opc = "DBH" if instr == "IN" else "D3H"
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10.9); ax.set_ylim(-0.4,8.6); ax.axis("off")
INSTR=%r; OPC=%r; THIRD=%r
ctrl="RD" if INSTR=="IN" else "WR"
# bands
for i,(n,l,c) in enumerate([("Opcode fetch (M1)",4,YEL),("Memory read (M2)",3,BLUE),(THIRD+" (M3)",3,GRN)]):
    x0=[0,4,7][i]; ax.add_patch(mp.Rectangle((x0+0.9,7.6),l,0.6,fc=c,ec=INK,lw=1,zorder=2)); ax.text(x0+0.9+l/2,7.9,n,ha="center",va="center",fontsize=7)
for t in range(10):
    ax.text(0.9+t+0.5,7.3,"T%%d"%%(t%%4+1 if t<4 else (t-4+1 if t<7 else t-7+1)),fontsize=6.3,ha="center")
    ax.plot([0.9+t,0.9+t],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
ax.plot([10.9,10.9],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
rows={"CLK":6.4,"ALE":5.4,"IO/M":4.4,ctrl:3.4,"A15-A8":2.3,"AD7-AD0":1.0}
for n,y in rows.items(): ax.text(0.8,y+0.1,n if n not in("RD","WR") else n,fontsize=7.3,ha="right",va="center")
# clock
for t in range(10):
    ax.plot([0.9+t,0.9+t,0.9+t+0.5,0.9+t+0.5,0.9+t+1],[6.1,6.7,6.7,6.1,6.1],color=INK,lw=1)
# ALE high in T1 of each cycle
def pulse(y,spans,hi_low=True,base=0.0):
    pass
for s in (0,4,7):
    ax.plot([0.9+s,0.9+s,0.9+s+0.5,0.9+s+0.5],[5.1,5.7,5.7,5.1],color=INK,lw=1.3)
ax.plot([0.9,0.9],[5.1,5.1],color=INK); ax.plot([0.9+0.5,0.9+4],[5.1,5.1],color=INK,lw=1.3); ax.plot([0.9+4.5,0.9+7],[5.1,5.1],color=INK,lw=1.3); ax.plot([0.9+7.5,10.9],[5.1,5.1],color=INK,lw=1.3)
# IO/M: low for M1,M2 (0..7), high for M3
ax.plot([0.9,7.9],[4.1,4.1],color=INK,lw=1.3); ax.plot([7.9,7.9],[4.1,4.7],color=INK,lw=1.3); ax.plot([7.9,10.9],[4.7,4.7],color=INK,lw=1.3)
ax.text(5.4,4.2,"low (memory)",fontsize=6.3,ha="center",va="bottom",color="#555"); ax.text(9.4,4.8,"high (I/O)",fontsize=6.3,ha="center",va="bottom",color="#555")
# RD / WR active low in T2-T3 of each cycle (OF, MR); only M3 for OUT uses WR instead of RD
hi,lo=3.7,3.1
segs=[(1,3),(5,7),(8,10)]
if INSTR=="OUT": segs_rd=[(1,3),(5,7)]; segs_wr=[(8,10)]
else: segs_rd=segs; segs_wr=[]
ax.plot([0.9,10.9],[hi,hi],color="#bbbbbb",lw=0.5)
x=0.9; pts=[]
def lowpulses(spans,y0=hi,y1=lo):
    x=0.9; X=[x]; Y=[y0]
    for a,b in spans:
        X+= [0.9+a,0.9+a,0.9+b,0.9+b]; Y+=[y0,y1,y1,y0]
    X.append(10.9); Y.append(y0); return X,Y
if INSTR=="IN":
    X,Y=lowpulses(segs); ax.plot(X,Y,color=INK,lw=1.3)
else:
    X,Y=lowpulses(segs_wr); ax.plot(X,Y,color=INK,lw=1.3)
    ax.text(10.8,3.15,"WR low",fontsize=6.3,ha="right",va="top",color="#555")
    ax.text(3.0,3.2,"RD (low in T2-T3 of M1, M2)",fontsize=6.0,color="#999")
    X2,Y2=lowpulses(segs_rd,y0=hi,y1=lo); ax.plot(X2,Y2,color="#aaaaaa",lw=1.0,ls="--")
# buses
def bus(y,spans,h=0.55):
    for (a,b,t,c) in spans:
        ax.add_patch(mp.Rectangle((0.9+a,y),b-a,h,fc=c,ec=INK,lw=1,zorder=2)); ax.text(0.9+(a+b)/2,y+h/2,t,ha="center",va="center",fontsize=6.3,zorder=3)
bus(2.0,[(0,4,"PCH (PC high)",BLUE),(4,7,"PCH (PC+1 high)",BLUE),(7,10,"80H (port address)",GRN)])
bus(0.7,[(0,0.5,"PCL",YEL),(0.5,4,"opcode "+OPC,BLUE),(4,4.5,"PCL+1",YEL),(4.5,7,"data 80H (port no.)",BLUE),(7,7.5,"80H",GRN),(7.5,10,"data " + ("in from port to A" if INSTR=="IN" else "A out to port"),GRN)])
ax.text(5.9,-0.2,"10 T-states in 3 machine cycles",fontsize=8,ha="center",weight="bold")
''' % (instr, opc, third)
    return fig(cap, body)


def arch8051():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,5.0)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(0,10)
box(ax,1.5,9.2,2.4,0.7,"On-chip\\noscillator",fs=6.8,fc=YEL); box(ax,4.3,9.2,2.4,0.7,"External\\ninterrupts",fs=6.5,fc=YEL)
box(ax,2.3,7.9,2.8,0.8,"Interrupt control",fs=7.2,fc=YEL); box(ax,5.4,7.9,2.8,0.8,"Timer 0 / Timer 1\\n(T0, T1 pins)",fs=6.8,fc=GRN)
box(ax,2.0,6.5,2.4,1.0,"On-chip ROM\\n4 KB program\\nmemory",fs=6.5,fc=BLUE); box(ax,4.8,6.5,2.4,0.9,"On-chip RAM\\n128 bytes",fs=6.8,fc=BLUE)
box(ax,7.6,6.5,2.4,0.9,"SFR block",fs=7,fc=BLUE)
box(ax,12.5,8.5,4.0,2.0,"CPU\\nALU  Accumulator A  B reg\\nPSW  SP  DPTR (DPH DPL)\\nPC  instruction register\\nTiming and control",fs=6.8,fc=YEL)
ax.plot([0.5,10.3],[5.1,5.1],color=INK,lw=3,solid_capstyle="butt"); ax.text(5.4,5.35,"8-bit internal data bus",fontsize=7,ha="center")
for x in (2.0,4.8,7.6): arr(ax,(x,6.05),(x,5.15),c=INK,style="<|-|>")
arr(ax,(2.3,7.5),(2.3,5.15),c=INK,style="<|-|>"); arr(ax,(5.4,7.5),(5.4,5.15),c=INK,style="<|-|>")
arr(ax,(10.5,8.0),(10.5,5.15),c=INK,style="<|-|>"); ax.plot([10.5,10.5,10.9],[8.0,8.0,8.0],color=INK,lw=1.2); ax.plot([10.5,11.4],[7.9,7.9],color=INK,lw=1.2)
for i,(n,x) in enumerate([("P0\\nAD0-AD7",1.3),("P1",3.9),("P2\\nA8-A15",6.2),("P3\\nRD WR T0 T1\\nINT0 INT1 TxD RxD",9.0)]):
    box(ax,x,3.6,2.0 if i<3 else 3.0,0.9,"I/O port "+n,fs=6.3,fc=GRN); arr(ax,(x,4.1),(x,5.1),c=INK,style="<|-|>"); arr(ax,(x,3.1),(x,2.2),c=ACCENT,style="<|-|>")
    ax.text(x,1.9,["8 pins","8 pins","8 pins","8 pins"][i],fontsize=6.5,ha="center")
box(ax,12.5,3.6,3.0,0.9,"Serial port\\n(SBUF, SCON, TxD, RxD)",fs=6.5,fc=GRN); arr(ax,(11.0,3.6),(11.0,5.1),c=INK,style="<|-|>")
ax.plot([10.3,10.3,13.0,13.0],[5.1,5.1,5.1,5.1],color=INK,lw=3)
arr(ax,(12.5,7.4),(12.5,5.15),c=INK,style="<|-|>"); ax.plot([10.3,12.5],[5.1,5.1],color=INK,lw=3,solid_capstyle="butt")
ax.text(12.5,1.9,"TxD / RxD",fontsize=6.5,ha="center"); arr(ax,(12.5,3.1),(12.5,2.2),c=ACCENT,style="<|-|>")
ax.text(7.4,0.7,"40-pin DIP: Vcc, GND, RST, XTAL1, XTAL2, EA, PSEN, ALE",fontsize=6.8,ha="center")
'''
    return fig("Internal architecture of the 8051 microcontroller: CPU, 4 KB ROM, 128-byte RAM, SFRs, two timers, interrupt control, serial port and four 8-bit I/O ports on one chip.", body)


def ram8051():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.4); ax.set_ylim(0,9.4)
def blk(x,y,w,h,t,fc,fs=7.2): ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1.2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
ax.text(3.0,9.1,"Internal data memory (direct addresses)",ha="center",fontsize=8.2,weight="bold")
blk(2.0,7.2,4.0,1.5,"SFR (direct addressing only)\\nP0 80H, SP 81H, DPL 82H, DPH 83H,\\nTCON 88H, P1 90H, SCON 98H, P2 A0H,\\nIE A8H, P3 B0H, IP B8H, PSW D0H, A E0H, B F0H",BLUE,6.2)
blk(2.0,3.7,4.0,3.5,"General purpose RAM\\n(scratch pad, stack)\\n30H - 7FH  (80 bytes)\\nDirect or indirect",YEL)
blk(2.0,2.5,4.0,1.2,"Bit-addressable RAM\\n20H - 2FH (128 bits, bit addr 00H-7FH)",GRN,6.8)
for i,(n,fc) in enumerate([("Bank 3: 18H-1FH (R0-R7)",RED),("Bank 2: 10H-17H",RED),("Bank 1: 08H-0FH",RED),("Bank 0: 00H-07H (default)",RED)]):
    blk(2.0,2.5-(i+1)*0.6,4.0,0.6,n,fc,6.5)
for y,t in [(8.7,"FFH"),(7.2,"80H"),(3.7,"30H"),(2.5,"20H"),(0.1,"00H")]: ax.text(1.8,y,t,ha="right",va="center",fontsize=7)
ax.text(1.8,6.9,"7FH",ha="right",va="center",fontsize=7); ax.text(1.8,3.4,"2FH",ha="right",va="center",fontsize=7)
ax.text(1.8,2.2,"1FH",ha="right",va="center",fontsize=7)
ax.text(9.9,8.6,"Register banks and PSW",ha="center",fontsize=8.2,weight="bold")
for i in range(8):
    ax.add_patch(mp.Rectangle((7.6+i*0.55,7.4),0.55,0.6,fc=BLUE if i<4 else YEL,ec=INK,lw=1)); ax.text(7.6+i*0.55+0.275,7.7,"R%d"%i,ha="center",va="center",fontsize=6.5)
ax.text(9.9,7.05,"bank select by PSW.4 (RS1) and PSW.3 (RS0)",ha="center",fontsize=6.8)
ax.text(9.9,6.4,"RS1 RS0  bank  address range",ha="center",fontsize=6.8,weight="bold")
for i,(a,b,c) in enumerate([("0 0","0","00H-07H"),("0 1","1","08H-0FH"),("1 0","2","10H-17H"),("1 1","3","18H-1FH")]): ax.text(9.9,5.9-i*0.5,"%s     %s     %s"%(a,b,c),ha="center",fontsize=6.8)
ax.text(9.9,3.5,"PSW:  CY AC F0 RS1 RS0 OV - P",ha="center",fontsize=7.2,family="monospace")
ax.text(9.9,2.8,"bit:    7  6  5   4   3  2 1 0",ha="center",fontsize=7.2,family="monospace")
'''
    return fig("Organisation of the 8051 internal memory: four register banks (00H-1FH), 16 bytes of bit-addressable RAM (20H-2FH), 80 bytes of scratch pad (30H-7FH) and the special function registers (80H-FFH).", body)


def flags86():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,2.6)); ax.axis("off"); ax.set_xlim(-0.3,16.6); ax.set_ylim(-1.2,3.4)
names={11:"OF",10:"DF",9:"IF",8:"TF",7:"SF",6:"ZF",4:"AF",2:"PF",0:"CF"}
for b in range(16):
    x=15-b; k=b
    fc=YEL if k in (11,7,6,4,2,0) else (BLUE if k in (10,9,8) else "#eeeeee")
    ax.add_patch(mp.Rectangle((x,1.0),1,0.9,fc=fc,ec=INK,lw=1.2)); ax.text(x+0.5,1.45,names.get(k,"-"),ha="center",va="center",fontsize=8,weight="bold" if k in names else "normal")
    ax.text(x+0.5,2.15,str(k),ha="center",fontsize=6.8)
ax.text(8.0,-0.8,"yellow = status flags (CF PF AF ZF SF OF), blue = control flags (TF IF DF), grey = undefined",ha="center",fontsize=6.8)
ax.text(8.0,2.85,"8086 flag register (16 bits)",ha="center",fontsize=8.2,weight="bold")
'''
    return fig("The 8086 flag register: six status flags set by the ALU and three control flags set by the programmer; seven bits are unused.", body)


def harvard():
    body = '''
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,3.2))
for z in (a,b): z.axis("off"); z.set_xlim(0,7); z.set_ylim(0,6)
a.set_title("Von Neumann architecture",fontsize=8.5)
box(a,3.5,4.9,3.0,0.9,"CPU\\n(control unit + ALU)",fs=7.5,fc=YEL); box(a,3.5,1.3,3.4,1.1,"Single memory\\ninstructions + data",fs=7.5,fc=BLUE)
arr(a,(3.0,4.4),(3.0,1.9),c=ACCENT,style="<|-|>"); arr(a,(4.0,4.4),(4.0,1.9),c=ACCENT,style="<|-|>"); a.text(3.5,3.15,"one shared\\naddress + data bus",ha="center",fontsize=6.5,bbox=dict(fc="white",ec="none",pad=0.5))
box(a,3.5,0.15,0.01,0.01,"",ec="white")
b.set_title("Harvard architecture",fontsize=8.5)
box(b,3.5,4.9,3.0,0.9,"CPU\\n(control unit + ALU)",fs=7.5,fc=YEL); box(b,1.4,1.3,2.5,1.1,"Program\\nmemory\\n(instructions)",fs=7.2,fc=BLUE); box(b,5.6,1.3,2.5,1.1,"Data\\nmemory",fs=7.5,fc=GRN)
arr(b,(2.5,4.45),(1.4,1.9),c=ACCENT,style="<|-|>"); arr(b,(4.5,4.45),(5.6,1.9),c=ACCENT,style="<|-|>"); b.text(1.2,3.3,"program bus",fontsize=6.5,rotation=55,ha="center"); b.text(5.9,3.3,"data bus",fontsize=6.5,rotation=-55,ha="center")
'''
    return fig("Block diagrams of the Von Neumann architecture (one memory and one bus) and the Harvard architecture (separate program and data memories with separate buses).", body)


def pipeline():
    body = '''
fig,(a,b)=plt.subplots(2,1,figsize=(7.4,3.6),sharex=True)
cols=[BLUE,YEL,GRN]
a.set_title("Without pipelining (fetch, then execute)",fontsize=8,loc="left")
for i in range(3):
    a.add_patch(mp.Rectangle((i*4,2-i),2,0.8,fc=BLUE,ec=INK)); a.text(i*4+1,2-i+0.4,"F%d"%(i+1),ha="center",va="center",fontsize=7)
    a.add_patch(mp.Rectangle((i*4+2,2-i),2,0.8,fc=YEL,ec=INK)); a.text(i*4+3,2-i+0.4,"E%d"%(i+1),ha="center",va="center",fontsize=7)
a.set_ylim(-0.3,3.2); a.set_yticks([]); a.text(12.2,0.4,"12 time units",fontsize=7,va="center")
b.set_title("With pipelining (fetch of the next instruction overlaps execution)",fontsize=8,loc="left")
for i in range(3):
    b.add_patch(mp.Rectangle((i*2,2-i),2,0.8,fc=BLUE,ec=INK)); b.text(i*2+1,2-i+0.4,"F%d"%(i+1),ha="center",va="center",fontsize=7)
    b.add_patch(mp.Rectangle((i*2+2,2-i),2,0.8,fc=YEL,ec=INK)); b.text(i*2+3,2-i+0.4,"E%d"%(i+1),ha="center",va="center",fontsize=7)
b.set_ylim(-0.3,3.2); b.set_yticks([]); b.set_xlim(0,14); b.text(8.2,0.4,"8 time units",fontsize=7,va="center"); b.set_xlabel("time (each box = 2 units)",fontsize=7)
for z in (a,b):
    for s in ("top","right","left"): z.spines[s].set_visible(False)
    z.tick_params(labelsize=6.5)
fig.tight_layout()
'''
    return fig("Instruction pipelining: overlapping the fetch of instruction n+1 with the execution of instruction n (the 8086 does this with its BIU and EU).", body)


def asmflow():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,2.6)); ax.axis("off"); ax.set_xlim(0,15.6); ax.set_ylim(0,5)
items=[(1.4,3.4,"Editor\\n(source\\nprogram)",BLUE),(4.3,3.4,"Assembler\\nMASM / TASM",YEL),(7.2,3.4,"Linker\\nLINK / TLINK",YEL),(10.1,3.4,"Loader\\n(DOS / OS)",YEL),(13.0,3.4,"Run /\\nDEBUG",GRN)]
for x,y,t,c in items: box(ax,x,y,2.2,1.4,t,fs=7,fc=c)
for x in (1.4,4.3,7.2,10.1): arr(ax,(x+1.1,3.4),(x+1.8,3.4),c=ACCENT)
for x,t in [(2.85,"prog.ASM"),(5.75,"prog.OBJ"),(8.65,"prog.EXE"),(11.55,"in memory")]: ax.text(x,4.35,t,ha="center",fontsize=6.8,color="#b00020")
box(ax,4.3,1.3,2.3,0.8,"prog.LST (listing)\\nprog.CRF",fs=6.3,fc="white"); arr(ax,(4.3,2.7),(4.3,1.7),c=INK)
box(ax,7.2,1.3,2.3,0.8,"Library files\\n+ other .OBJ",fs=6.3,fc="white"); arr(ax,(7.2,1.7),(7.2,2.7),c=INK)
box(ax,10.1,1.3,2.3,0.8,"PSP + segments\\nCS:IP, SS:SP set",fs=6.3,fc="white"); arr(ax,(10.1,1.7),(10.1,2.7),c=INK)
box(ax,7.2,0.0,0.01,0.01,"",ec="white")
'''
    return fig("Assembling, linking and execution of an 8086 program: source file (.ASM) to object file (.OBJ) to executable (.EXE) to a running process.", body)
