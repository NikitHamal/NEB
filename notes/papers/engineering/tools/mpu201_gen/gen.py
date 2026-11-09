"""python3 gen.py <content dir>  -> writes the three Microprocessor (ENEX 201) papers from t*.md + blocks.txt"""
import os, re, sys
import lib201 as L
import mpulib as M

out = sys.argv[1] if len(sys.argv) > 1 else '.'
here = os.path.dirname(os.path.abspath(__file__))

BLK = {}
cur = None
for line in open(os.path.join(here, 'blocks.txt')).read().split('\n'):
    if line.startswith('=== '):
        cur = line[4:].strip(); BLK[cur] = []
    else:
        BLK[cur].append(line)
BLK = {k: '\n'.join(v).strip() for k, v in BLK.items()}
BLK['directives'] = BLK['directives'].replace("| `LABEL`, `EVEN`, `NAME`, `TITLE`, `DS`-type `DW ?` | type a label, align on an even address, name the module | `EVEN` |",
                                              "| `LABEL`, `EVEN`, `NAME`, `TITLE` | type a label, align on an even address, name the module, title of the listing | `EVEN` |")

mpsys = '''
fig,ax=plt.subplots(figsize=(7.4,3.8)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,7.6)
box(ax,2.0,5.2,3.2,1.8,"CPU\\n(microprocessor)\\nALU, registers,\\ncontrol unit",fs=7.5,fc=YEL)
box(ax,7.4,6.4,3.0,1.0,"ROM / EPROM",fs=8,fc=GRN); box(ax,7.4,4.8,3.0,1.0,"RAM",fs=8,fc=GRN)
box(ax,12.6,6.4,3.4,1.0,"Input device\\n(keyboard, switches)",fs=7,fc=BLUE); box(ax,12.6,4.8,3.4,1.0,"Output device\\n(display, LEDs)",fs=7,fc=BLUE)
for y,t,c in [(2.9,"Address bus  (A15 - A0, unidirectional)","#c62828"),(2.0,"Data bus  (D7 - D0, bidirectional)","#1565c0"),(1.1,"Control bus  (RD, WR, IO/M, ALE, READY, INTR ...)","#2e7d32")]:
    ax.plot([0.4,14.4],[y,y],color=c,lw=2.4); ax.text(7.4,y+0.2,t,fontsize=7,ha="center",color=c)
for x in (2.0,7.4,12.6):
    for y in (2.9,2.0,1.1): ax.plot([x],[y],"o",color=INK,ms=3)
ax.plot([2.0,2.0],[4.3,1.1],color="#777",lw=1); ax.plot([7.4,7.4],[4.3,1.1],color="#777",lw=1); ax.plot([12.6,12.6],[4.3,1.1],color="#777",lw=1)
ax.text(7.4,7.2,"Memory",fontsize=8,ha="center",weight="bold"); ax.text(12.6,7.2,"I/O devices (via interface, e.g. 8255)",fontsize=7.5,ha="center",weight="bold")
'''
FIG = dict(
    mpsys=M.fig("Organization of a microprocessor-based system: the CPU, memory and I/O devices are connected by the address, data and control buses.", mpsys),
    arch85=L.arch8085(), biueu=M.biu_eu(), flags86=M.flags86(), harvard=M.harvard(),
    ppi=L.ppi8255(), dma=L.dma8257(), flynn=L.flynn(), mvim=L.timing_mvim(),
    decC=L.dec_fig("Address decoding: 2 x 1 KB EPROM and 1 x 2 KB RAM from 1000H",
                   [("C", "A12"), ("B", "A11"), ("A", "A10")], "G1 = NOR(A15, A14, A13)   G2A = IO/M   G2B = GND",
                   [("EPROM 1", "1K x 8", "1000H - 13FFH", [4], "A0-A9, D0-D7, RD"), ("EPROM 2", "1K x 8", "1400H - 17FFH", [5], "A0-A9, D0-D7, RD"),
                    ("RAM", "2K x 8", "1800H - 1FFFH", [6, 7], "A0-A10, D0-D7, RD, WR")],
                   "Address decoding with a 74LS138: Y4 selects EPROM 1 (1000H-13FFH), Y5 selects EPROM 2 (1400H-17FFH) and the AND of Y6 and Y7 selects the 2 KB RAM (1800H-1FFFH)."),
    decK=L.dec_fig("Address decoding: 4K x 8 EPROM and 2 x 2K x 8 RAM (start 0000H)",
                   [("C", "A13"), ("B", "A12"), ("A", "A11")], "G1 = NOR(A15, A14)   G2A = IO/M   G2B = GND",
                   [("EPROM", "4K x 8", "0000H - 0FFFH", [0, 1], "A0-A11, D0-D7, RD"), ("RAM 1", "2K x 8", "1000H - 17FFH", [2], "A0-A10, D0-D7, RD, WR"),
                    ("RAM 2", "2K x 8", "1800H - 1FFFH", [3], "A0-A10, D0-D7, RD, WR")],
                   "Address decoding with a 74LS138: the AND of Y0 and Y1 selects the 4 KB EPROM (0000H-0FFFH), Y2 selects RAM 1 (1000H-17FFH) and Y3 selects RAM 2 (1800H-1FFFH)."),
    decH=L.dec_fig("Address decoding: 2K ROM, 2K RAM, 4K EPROM consecutively from A000H",
                   [("C", "A13"), ("B", "A12"), ("A", "A11")], "G1 = A15   G2A = A14   G2B = IO/M",
                   [("ROM", "2K x 8", "A000H - A7FFH", [4], "A0-A10, D0-D7, RD"), ("RAM", "2K x 8", "A800H - AFFFH", [5], "A0-A10, D0-D7, RD, WR"),
                    ("EPROM", "4K x 8", "B000H - BFFFH", [6, 7], "A0-A11, D0-D7, RD")],
                   "Address decoding with a 74LS138: Y4 selects the 2 KB ROM (A000H-A7FFH), Y5 the 2 KB RAM (A800H-AFFFH) and the AND of Y6 and Y7 the 4 KB EPROM (B000H-BFFFH)."),
)


def expand(t):
    t = re.sub(r'\{\{B:(\w+)\}\}', lambda m: BLK[m.group(1)], t)
    t = re.sub(r'\{\{FIG:(\w+)\}\}', lambda m: FIG[m.group(1)], t)
    return t


for src, dst in (('tC.md', 'ioe-enex201-2082-chaitra.md'), ('tK.md', 'ioe-enex201-2082-kartik.md'), ('tH.md', 'ioe-enex201-2081-chaitra.md')):
    t = open(os.path.join(here, src)).read()
    for _ in range(2):
        t = expand(t)
    open(os.path.join(out, dst), 'w').write(t)
    print('wrote', dst, len(t))
