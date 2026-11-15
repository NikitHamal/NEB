"""python3 gen_mpu.py <content dir>  -> writes ioe-enex251-2083-baishakh.md and ioe-enex251-2082-bhadra.md"""
import os, re, sys
import mpulib as L
out = sys.argv[1] if len(sys.argv) > 1 else '.'
here = os.path.dirname(os.path.abspath(__file__))
coa = open(os.path.join(out, 'ioe-enex253-2082-bhadra.md')).read()
m = re.search(r'```figure caption="Left: hardwired control unit.*?\n```\n', coa, re.S)
FIGS = dict(
    hwmp=m.group(0),
    biueu=L.biu_eu(),
    decodeA=L.decode_fig(("ROM", "4", "4000H - 4FFFH", 4, "A0-A11, D0-D7, RD", 0), ("RAM", "2", "5000H - 57FFH", 5, "A0-A10, D0-D7, RD, WR", 1),
                         "+5V", "A15", "IO/M", "Address decoding for 4 KB ROM at 4000H and 2 KB RAM at 5000H with a 74LS138 (Y4 selects the ROM; Y5 OR A11 selects the RAM)."),
    decodeB=L.decode_fig(("RAM", "4", "A000H - AFFFH", 2, "A0-A11, D0-D7, RD, WR", 0), ("ROM", "2", "B000H - B7FFH", 3, "A0-A10, D0-D7, RD", 1),
                         "A15", "IO/M", "GND", "Address decoding for 4 KB RAM at A000H and 2 KB ROM at B000H with a 74LS138 (Y2 selects the RAM; Y3 OR A11 selects the ROM)."),
    inA=L.cycles_fig("IN", 4, "Machine cycles and timing of IN 80H: opcode fetch (4 T), memory read of the port address (3 T) and I/O read (3 T)."),
    outB=L.cycles_fig("OUT", 2, "Machine cycles and timing of OUT 80H: opcode fetch (4 T), memory read of the port address (3 T) and I/O write (3 T)."),
    arch51=L.arch8051(), ram51=L.ram8051(), flags=L.flags86(), harvard=L.harvard(), pipeline=L.pipeline(), asmflow=L.asmflow())
for src, dst in (('p1.tpl.md', 'ioe-enex251-2083-baishakh.md'), ('p2.tpl.md', 'ioe-enex251-2082-bhadra.md')):
    t = open(os.path.join(here, src)).read()
    t = re.sub(r'\{\{FIG:(\w+)\}\}', lambda mm: FIGS[mm.group(1)], t)
    open(os.path.join(out, dst), 'w').write(t)
    print('wrote', dst, len(t))
