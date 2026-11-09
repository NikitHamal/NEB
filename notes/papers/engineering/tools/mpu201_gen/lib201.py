"""Figures + a small 8085 simulator for the Microprocessor (ENEX 201, 3rd sem) papers.
Figure functions return ```figure ...``` blocks (plt, INK, ACCENT provided by the paper pipeline)."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mpu_gen'))
from mpulib import PRE, fig  # noqa


# ----------------------------------------------------------------- 8085 simulator
def _n(s):
    s = s.strip().upper()
    return int(s[:-1], 16) if s.endswith('H') else int(s)


def sim85(src, mem=None, steps=200000):
    prog, labels = [], {}
    for line in src.splitlines():
        line = line.split(';')[0].strip()
        if not line:
            continue
        m = re.match(r'(\w+):\s*(.*)', line)
        if m:
            labels[m.group(1).upper()] = len(prog)
            line = m.group(2).strip()
        if not line:
            continue
        p = line.split(None, 1)
        prog.append((p[0].upper(), [a.strip() for a in p[1].split(',')] if len(p) > 1 else []))
    R = dict(A=0, B=0, C=0, D=0, E=0, H=0, L=0)
    F = dict(Z=0, CY=0, S=0)
    mem = dict(mem or {})
    P = {'B': 'C', 'D': 'E', 'H': 'L'}
    pair = lambda p: (R[p] << 8) | R[P[p]]

    def setp(p, v):
        R[p] = (v >> 8) & 255
        R[P[p]] = v & 255

    getr = lambda r: mem.get(pair('H'), 0) if r == 'M' else R[r]

    def setr(r, v):
        if r == 'M':
            mem[pair('H')] = v & 255
        else:
            R[r] = v & 255

    def zs(v):
        F['Z'] = int((v & 255) == 0)
        F['S'] = (v >> 7) & 1
    pc = 0
    n = 0
    while pc < len(prog) and n < steps:
        n += 1
        op, a = prog[pc]
        pc += 1
        if op == 'HLT':
            break
        elif op == 'LDA': R['A'] = mem.get(_n(a[0]), 0)
        elif op == 'STA': mem[_n(a[0])] = R['A']
        elif op == 'SHLD':
            ad = _n(a[0]); mem[ad] = R['L']; mem[ad + 1] = R['H']
        elif op == 'LHLD':
            ad = _n(a[0]); R['L'] = mem.get(ad, 0); R['H'] = mem.get(ad + 1, 0)
        elif op == 'MOV': setr(a[0], getr(a[1]))
        elif op == 'MVI': setr(a[0], _n(a[1]))
        elif op == 'LXI': setp(a[0], _n(a[1]))
        elif op == 'LDAX': R['A'] = mem.get(pair(a[0]), 0)
        elif op == 'STAX': mem[pair(a[0])] = R['A']
        elif op == 'ADD':
            t = R['A'] + getr(a[0]); F['CY'] = int(t > 255); R['A'] = t & 255; zs(R['A'])
        elif op == 'ANI': R['A'] &= _n(a[0]); F['CY'] = 0; zs(R['A'])
        elif op == 'ORI': R['A'] |= _n(a[0]); F['CY'] = 0; zs(R['A'])
        elif op == 'XRI': R['A'] ^= _n(a[0]); F['CY'] = 0; zs(R['A'])
        elif op == 'ORA': R['A'] |= getr(a[0]); F['CY'] = 0; zs(R['A'])
        elif op == 'CMA': R['A'] ^= 255
        elif op == 'DCR': v = (getr(a[0]) - 1) & 255; setr(a[0], v); zs(v)
        elif op == 'INR': v = (getr(a[0]) + 1) & 255; setr(a[0], v); zs(v)
        elif op == 'INX': setp(a[0], (pair(a[0]) + 1) & 0xFFFF)
        elif op == 'DCX': setp(a[0], (pair(a[0]) - 1) & 0xFFFF)
        elif op == 'DAD':
            t = pair('H') + pair(a[0]); F['CY'] = int(t > 0xFFFF); setp('H', t & 0xFFFF)
        elif op == 'CPI':
            v = _n(a[0]); F['CY'] = int(R['A'] < v); F['Z'] = int(R['A'] == v)
        elif op in ('JNZ', 'JZ', 'JC', 'JNC', 'JMP'):
            c = dict(JNZ=not F['Z'], JZ=F['Z'], JC=F['CY'], JNC=not F['CY'], JMP=True)[op]
            if c:
                pc = labels[a[0].upper()]
        else:
            raise ValueError(op)
    return R, mem, n


# ----------------------------------------------------------------- figures
def arch8085():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,5.0)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,10)
ax.add_patch(mp.Rectangle((0.1,0.2),14.6,9.6,fc="#fafcff",ec=INK,lw=1.3,ls="--",zorder=1)); ax.text(7.4,9.45,"8085 microprocessor",ha="center",fontsize=9,weight="bold")
BX=7.3
ax.plot([BX,BX],[0.7,8.9],color=INK,lw=2.4,zorder=2); ax.text(BX,9.05,"internal 8-bit data bus",fontsize=6.5,ha="center")
def tie(x,y,fr=True): ax.plot([x,BX],[y,y],color="#777",lw=1.0,zorder=2)
box(ax,1.6,8.2,2.6,0.8,"Accumulator (8)",fs=7.2,fc=BLUE); tie(2.9,8.2)
box(ax,1.6,7.0,2.6,0.8,"Temporary register (8)",fs=7.0,fc=BLUE)
box(ax,1.6,5.8,2.6,0.8,"Flag register\\nS Z AC P CY",fs=6.8,fc=BLUE)
box(ax,4.9,6.9,2.2,2.6,"ALU",fs=10,fc=YEL); ax.plot([4.9,4.9],[8.2,8.2]); tie(6.0,6.9)
ax.plot([2.9,3.8],[8.2,8.2],color="#777",lw=1); ax.plot([2.9,3.8],[7.0,7.0],color="#777",lw=1); ax.plot([2.9,3.8],[5.8,5.8],color="#777",lw=1)
for i,(a,b) in enumerate([("B","C"),("D","E"),("H","L"),("W","Z")]):
    y=4.5-i*0.85; box(ax,1.2,y,1.6,0.65,a,fs=8,fc=GRN); box(ax,2.9,y,1.6,0.65,b,fs=8,fc=GRN); tie(3.7,y)
box(ax,2.1,0.95,3.4,0.65,"Stack pointer SP (16)",fs=7,fc=GRN); tie(3.8,0.95)
box(ax,2.1,0.1+0.0001,0.0001,0.0001,"",fs=1,ec="white")
box(ax,9.4,8.3,2.4,0.8,"Instruction register (8)",fs=6.8,fc=RED); tie(8.2,8.3); ax.plot([8.2,BX],[8.3,8.3],color="#777",lw=1)
box(ax,9.4,7.2,2.4,0.8,"Instruction decoder\\nand machine cycle\\nencoder",fs=6.2,fc=RED)
box(ax,9.4,5.6,2.4,1.3,"Timing and control\\nCLK  ALE  RD  WR\\nIO/M  S0  S1  READY\\nRESET IN / OUT",fs=6.2,fc=RED)
box(ax,9.4,3.9,2.4,1.3,"Interrupt control\\nINTR  INTA  TRAP\\nRST7.5  RST6.5\\nRST5.5",fs=6.2,fc=RED)
box(ax,9.4,2.4,2.4,0.9,"Serial I/O control\\nSID  SOD",fs=6.6,fc=RED)
box(ax,13.1,7.9,3.0,0.8,"Program counter (16)",fs=6.8,fc=GRN)
box(ax,13.1,6.6,3.0,0.8,"Incrementer / decrementer\\naddress latch (16)",fs=6.2,fc=GRN)
box(ax,13.1,4.9,3.0,0.8,"Address buffer\\nA15 - A8 (output)",fs=6.5,fc=BLUE)
box(ax,13.1,3.6,3.0,0.8,"Address / data buffer\\nAD7 - AD0 (bidirectional)",fs=6.2,fc=BLUE)
for y in (7.9,6.6,4.9,3.6): ax.plot([BX,11.6],[y,y],color="#777",lw=1.0,zorder=1)
ax.plot([8.2,8.2],[8.3,7.2],color="#999",lw=0.8); ax.plot([9.4,9.4],[6.8,6.3],color="#999",lw=0.8)
ax.text(9.4,0.95,"8085 internal architecture",fontsize=6.6,ha="center",color="#555",style="italic")
'''
    return fig("Internal architecture of the 8085: registers (blue/green) on one internal data bus, the ALU, and the control section (red) that decodes instructions and produces timing, interrupt and serial I/O signals.", body)


def timing_mvim():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10.9); ax.set_ylim(-0.4,8.6); ax.axis("off")
bands=[("Opcode fetch (M1)",0,4,YEL),("Memory read (M2)",4,3,BLUE),("Memory write (M3)",7,3,GRN)]
for n,x0,l,c in bands:
    ax.add_patch(mp.Rectangle((x0+0.9,7.6),l,0.6,fc=c,ec=INK,lw=1,zorder=2)); ax.text(x0+0.9+l/2,7.9,n,ha="center",va="center",fontsize=7)
lab=["T1","T2","T3","T4","T1","T2","T3","T1","T2","T3"]
for t in range(10):
    ax.text(0.9+t+0.5,7.3,lab[t],fontsize=6.3,ha="center"); ax.plot([0.9+t,0.9+t],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
ax.plot([10.9,10.9],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
for n,y in {"CLK":6.4,"ALE":5.4,"IO/M":4.4,"RD":3.4,"WR":2.6,"A15-A8":1.6,"AD7-AD0":0.4}.items(): ax.text(0.8,y+0.1,n,fontsize=7.3,ha="right",va="center")
for t in range(10): ax.plot([0.9+t,0.9+t,0.9+t+0.5,0.9+t+0.5,0.9+t+1],[6.1,6.7,6.7,6.1,6.1],color=INK,lw=1)
for s in (0,4,7): ax.plot([0.9+s,0.9+s,0.9+s+1,0.9+s+1],[5.1,5.7,5.7,5.1],color=INK,lw=1.3)
ax.plot([0.9,0.9+10],[5.1,5.1],color=INK,lw=1.0)
ax.plot([0.9,10.9],[4.1,4.1],color=INK,lw=1.3); ax.text(5.9,4.2,"IO/M = 0 (memory cycles)",fontsize=6.3,ha="center",va="bottom",color="#555")
def low(y,spans,hi=0.6):
    X=[0.9]; Y=[y+hi]
    for a,b in spans: X+=[0.9+a,0.9+a,0.9+b,0.9+b]; Y+=[y+hi,y,y,y+hi]
    X.append(10.9); Y.append(y+hi); ax.plot(X,Y,color=INK,lw=1.3)
low(3.0,[(1,3),(5,7)]); low(2.2,[(8,10)])
ax.text(8.4,3.45,"RD high",fontsize=6.3,ha="center",color="#555")
def bus(y,spans,h=0.55):
    for a,b,t,c in spans: ax.add_patch(mp.Rectangle((0.9+a,y),b-a,h,fc=c,ec=INK,lw=1,zorder=2)); ax.text(0.9+(a+b)/2,y+h/2,t,ha="center",va="center",fontsize=6.2,zorder=3)
bus(1.3,[(0,4,"PCH",BLUE),(4,7,"PCH (PC+1)",BLUE),(7,10,"H (address of M)",GRN)])
bus(0.1,[(0,0.5,"PCL",YEL),(0.5,4,"opcode 36H",BLUE),(4,4.5,"PCL+1",YEL),(4.5,7,"data byte",BLUE),(7,7.5,"L",GRN),(7.5,10,"data out",GRN)])
ax.text(5.9,-0.35,"10 T-states in 3 machine cycles",fontsize=8,ha="center",weight="bold")
'''
    return fig("Timing diagram of MVI M, data (opcode 36H): opcode fetch (4 T), memory read of the data byte (3 T) and memory write to the location addressed by HL (3 T) = 10 T-states.", body)


def dec_fig(title, sel, enab, chips, cap):
    """sel = [(pin,label)] for C,B,A ; enab = text ; chips = [(name,size,range,[Y indices],lines)]"""
    body = '''
TITLE=%r; SEL=%r; ENAB=%r; CHIPS=%r
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.0)
ax.text(0.1,8.7,TITLE,fontsize=8,weight="bold")
for k,(pin,lab) in enumerate(SEL):
    y=6.9-k*0.9; ax.text(0.2,y,lab,fontsize=7.5,va="center"); ax.plot([1.1,2.7],[y,y],color=INK,lw=1); ax.text(2.8,y,pin,fontsize=7,va="center")
box(ax,4.2,5.3,2.8,5.2,"74LS138\\n3:8 decoder",fs=8,fc=YEL)
ax.text(4.2,8.25,ENAB,fontsize=6.0,ha="center",va="center")
def yp(k): return 7.4-0.62*k
for k in range(8):
    ax.plot([5.6,6.4],[yp(k),yp(k)],color=INK,lw=1); ax.text(5.5,yp(k),"Y%%d"%%k,fontsize=6,ha="right",va="center")
cy=[7.0,4.3,1.6][:len(CHIPS)] if len(CHIPS)<=3 else [7.0,4.8,2.6,0.6]
for (nm,sz,rg,ys,ln),y in zip(CHIPS,cy):
    box(ax,12.2,y,4.2,1.5,nm+" "+sz+"\\n"+rg+"\\n"+ln,fs=6.3,fc=GRN)
    if len(ys)==1:
        yy=yp(ys[0]); ax.plot([6.4,9.0,9.0,10.1],[yy,yy,y,y],color=ACCENT,lw=1.2)
    else:
        gx=8.3; ax.add_patch(mp.Rectangle((gx,y-0.35),0.9,0.7,fc="white",ec=INK,lw=1.1,zorder=3)); ax.text(gx+0.45,y,"AND",fontsize=6.5,ha="center",va="center",zorder=4)
        for j,k in enumerate(ys):
            yy=yp(k); ax.plot([6.4,7.7,7.7,gx],[yy,yy,y+0.18-0.36*j,y+0.18-0.36*j],color=ACCENT,lw=1.2)
        ax.plot([gx+0.9,10.1],[y,y],color=ACCENT,lw=1.2)
    ax.text(10.15,y+0.15,"CS",fontsize=6.5,color=ACCENT)
ax.text(7.4,0.15,"CS is active low; A0-A(n-1) of each chip are connected to the same address lines, D0-D7 to the data bus",fontsize=6.0,ha="center",color="#555")
''' % (title, sel, enab, chips)
    return fig(cap, body)


def ppi8255():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.4)
ax.add_patch(mp.Rectangle((3.0,0.5),8.2,8.4,fc="#fafcff",ec=INK,lw=1.4)); ax.text(7.1,8.55,"Intel 8255A PPI",ha="center",fontsize=9,weight="bold")
box(ax,4.9,7.2,3.0,1.0,"Data bus\\nbuffer",fs=7.5,fc=BLUE); box(ax,4.9,5.4,3.0,1.2,"Read / Write\\ncontrol logic",fs=7.5,fc=RED); box(ax,4.9,3.2,3.0,1.3,"Group A control\\nGroup B control",fs=7.2,fc=YEL)
box(ax,9.2,7.4,2.6,0.8,"Group A\\nPort A (8)",fs=7,fc=GRN); box(ax,9.2,6.0,2.6,0.8,"Group A\\nPort C upper (PC7-4)",fs=6.3,fc=GRN)
box(ax,9.2,4.3,2.6,0.8,"Group B\\nPort C lower (PC3-0)",fs=6.3,fc=GRN); box(ax,9.2,2.9,2.6,0.8,"Group B\\nPort B (8)",fs=7,fc=GRN)
ax.text(0.2,7.2,"D7 - D0",fontsize=8,va="center"); arr(ax,(1.4,7.2),(3.3,7.2),c=INK,style="<|-|>")
for y,t in [(5.9,"RD"),(5.4,"WR"),(4.9,"A0, A1"),(4.4,"RESET"),(3.9,"CS")]:
    ax.text(0.2,y,t,fontsize=7.5,va="center"); arr(ax,(1.4,y),(3.3,y),c=INK)
for y,t in [(7.4,"PA7 - PA0"),(6.0,"PC7 - PC4"),(4.3,"PC3 - PC0"),(2.9,"PB7 - PB0")]:
    arr(ax,(10.5,y),(12.0,y),c=INK,style="<|-|>"); ax.text(12.1,y,t,fontsize=7.5,va="center")
ax.plot([6.4,7.9],[7.2,7.2],color="#777"); ax.plot([6.4,7.9],[3.2,3.2],color="#777"); ax.plot([7.9,7.9],[3.2,7.4],color="#777",lw=1.5)
ax.text(7.1,0.9,"Vcc  GND  (40-pin DIP, 24 programmable I/O lines)",fontsize=6.5,ha="center",color="#555")
'''
    return fig("Block diagram of the 8255A programmable peripheral interface: data bus buffer, read/write control, group A and group B control and the three 8-bit ports (port C is split into two 4-bit halves).", body)


def dma8257():
    body = '''
fig,ax=plt.subplots(figsize=(7.4,4.8)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.8)
ax.add_patch(mp.Rectangle((3.4,0.4),8.0,9.0,fc="#fafcff",ec=INK,lw=1.4)); ax.text(7.4,9.05,"Intel 8257 DMA controller",ha="center",fontsize=9,weight="bold")
box(ax,5.1,7.9,3.0,0.9,"Data bus buffer",fs=7.5,fc=BLUE); box(ax,5.1,6.4,3.0,1.0,"Read / write logic",fs=7.5,fc=RED); box(ax,5.1,4.5,3.0,1.6,"Control logic\\n(mode set register,\\nstatus register)",fs=7,fc=YEL)
box(ax,5.1,2.2,3.0,1.2,"Priority resolver",fs=7.5,fc=RED)
for i in range(4): box(ax,9.4,8.0-i*1.35,3.2,1.0,"Channel %d\\nDMA address reg. (16)\\nterminal count reg. (16)"%i,fs=5.9,fc=GRN)
for y,t in [(7.9,"D0 - D7"),(6.9,"IOR, IOW"),(6.0,"A0 - A3, CS"),(5.1,"RESET, CLK"),(4.2,"HRQ / HLDA"),(3.3,"READY"),(2.0,"DRQ0-3 in"),(1.2,"DACK0-3 out")]:
    ax.text(0.1,y,t,fontsize=7,va="center"); arr(ax,(1.9,y),(3.6,y),c=INK,style="<|-|>" if t.startswith("D0") else "-|>")
for y,t in [(8.0,"A0 - A7, A8 - A15"),(6.5,"MEMR, MEMW"),(5.0,"AEN, ADSTB"),(3.5,"TC, MARK")]:
    ax.text(14.7,y,t,fontsize=7,va="center",ha="right"); arr(ax,(11.5,y),(12.0,y),c=INK) if False else None
ax.text(7.4,0.7,"4 channels: 16-bit address + 14-bit count with 2 mode bits each",fontsize=6.5,ha="center",color="#555")
'''
    return fig("Block diagram of the 8257 DMA controller: four channels with address and terminal-count registers, a priority resolver, read/write and control logic, and the data bus buffer. DRQ/DACK pins serve the I/O devices, HRQ/HLDA the CPU.", body)


def flynn():
    body = '''
fig,ax=plt.subplots(1,4,figsize=(7.4,2.6))
def panel(a,title,ncu,npu,nds,desc):
    a.set_xlim(0,6); a.set_ylim(0,6); a.axis("off"); a.set_title(title,fontsize=8)
    for i in range(ncu):
        y=5.0-i*(3.3/max(ncu,1)) if ncu>1 else 4.6
        a.add_patch(mp.Rectangle((0.2,y-0.35),1.1,0.7,fc="#fde8e8",ec=INK,lw=1)); a.text(0.75,y,"CU",ha="center",va="center",fontsize=6.5)
    for i in range(npu):
        y=5.0-i*(3.3/max(npu,1)) if npu>1 else 4.6
        a.add_patch(mp.Rectangle((2.3,y-0.35),1.1,0.7,fc="#fff4d6",ec=INK,lw=1)); a.text(2.85,y,"PU",ha="center",va="center",fontsize=6.5)
    if ncu==1 and npu>1:
        for i in range(npu):
            y=5.0-i*(3.3/npu); a.plot([1.3,2.3],[4.6,y],color=ACCENT,lw=0.9)
    elif ncu==npu:
        for i in range(ncu):
            y=5.0-i*(3.3/max(ncu,1)) if ncu>1 else 4.6; a.plot([1.3,2.3],[y,y],color=ACCENT,lw=0.9)
    else:
        for i in range(ncu):
            y=5.0-i*(3.3/ncu); a.plot([1.3,2.3],[y,4.6],color=ACCENT,lw=0.9)
    a.add_patch(mp.Rectangle((4.4,0.9),1.3,3.9,fc="#e6f4ea",ec=INK,lw=1)); a.text(5.05,2.85,"Memory\\n(data)",ha="center",va="center",fontsize=6.3)
    for i in range(npu):
        y=5.0-i*(3.3/max(npu,1)) if npu>1 else 4.6; a.plot([3.4,4.4],[y,min(max(y,1.2),4.5)],color="#555",lw=0.9)
    a.text(3.0,0.3,desc,ha="center",fontsize=6.2)
panel(ax[0],"SISD",1,1,1,"1 instr. stream\\n1 data stream")
panel(ax[1],"SIMD",1,3,3,"1 instr. stream\\nmany data streams")
panel(ax[2],"MISD",3,1,1,"many instr. streams\\n1 data stream")
panel(ax[3],"MIMD",3,3,3,"many instr. streams\\nmany data streams")
plt.tight_layout()
'''
    return fig("Flynn's classification: CU = control unit (instruction stream), PU = processing unit, with one or many data streams from memory.", body)
