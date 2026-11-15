"""python3 gen_dc.py <content dir> -> ioe-enct253-2083-baishakh.md, ioe-enct253-2082-bhadra.md (from tplA/tplB.md)."""
import os, re, sys
import numpy as np
import dclib as D
out = sys.argv[1] if len(sys.argv) > 1 else '.'
here = os.path.dirname(os.path.abspath(__file__))
K = {}

def b(v): return ''.join(str(int(x)) for x in v)

# ---------- Shannon-Fano (paper A)
S1 = "Solve {(a+b)(a-b)}²."
syms, f, codes, steps = D.shannon_fano(S1)
tbl, H, L, eff, enc, bits, n = D.coding_md(S1, syms, f, codes)
K['SF_TABLE'] = tbl
K['SF_STEPS'] = '\n'.join('| %d | `%s` (total %d) | `%s` (total %d) |' % (d, ' '.join(D.name(c) for c in a_), sa, ' '.join(D.name(c) for c in b_), sb) for d, a_, b_, sa, sb in steps)
K['SF_STATS'] = (n, '%.4f' % H, '%.2f' % L, '%.2f' % (eff * 100), bits, 8 * n, '%.1f' % (100 * (1 - bits / (8 * n))))
K['SF_ENC'] = enc
K['SF_H'] = '%.4f' % H; K['SF_L'] = '%.2f' % L; K['SF_EFF'] = '%.2f' % (eff * 100); K['SF_BITS'] = str(bits); K['SF_N'] = str(n); K['SF_ASCII'] = str(8 * n)
# ---------- Huffman (paper B)
S2 = "I'm 100% OK."
order, f2, codes2, hsteps = D.huffman(S2)
syms2 = sorted(order, key=lambda c: (-f2[c], order.index(c)))
tbl2, H2, L2, eff2, enc2, bits2, n2 = D.coding_md(S2, syms2, f2, codes2)
names = {}
def lab(it):
    return D.name(it[2]) if isinstance(it[2], str) else names[it[1]]
rows = []
for k, (x, y, tot, node) in enumerate(hsteps, 1):
    names[node[1]] = 'N%d' % k
    rows.append('| %d | `%s` (%d) | `%s` (%d) | **N%d** = %d |' % (k, lab(x), x[0], lab(y), y[0], k, tot))
K['HUFF_TABLE'] = tbl2; K['HUFF_STEPS'] = '\n'.join(rows); K['HUFF_ENC'] = enc2
K['H_H'] = '%.4f' % H2; K['H_L'] = '%.3f' % L2; K['H_EFF'] = '%.2f' % (eff2 * 100); K['H_BITS'] = str(bits2); K['H_N'] = str(n2); K['H_ASCII'] = str(8 * n2)
# ---------- Hamming 1110011
(c1, c2, c4), syn, fixed = D.hamming74_check('1110011')
K['HAM'] = (c1, c2, c4, syn, fixed, fixed[2] + fixed[4] + fixed[5] + fixed[6])
# ---------- LBC (6,3)
words, dmin = D.lbc()
K['LBC_TABLE'] = '\n'.join('| %s | %s |' % (b(m), b(c)) for m, c in words.items())
K['LBC_DMIN'] = str(dmin)
msg = (1, 0, 1); cw = words[msg]; r = list(cw); r[3] ^= 1  # error in bit 4
s_ = (np.array(r) @ D.H.T) % 2
K['LBC_CW'] = b(cw); K['LBC_R'] = b(r); K['LBC_S'] = b(s_)
K['LBC_SYN'] = '\n'.join('| %d | %s | %s |' % (j + 1, b([1 if i == j else 0 for i in range(6)]), b(D.H[:, j])) for j in range(6))
assert b(D.H[:, 3]) == b(s_)
# ---------- CRC-4
crc, csteps = D.crc_div('1101011011', '10011')
K['CRC'] = crc
K['CRC_STEPS'] = '\n'.join('| %d | `%s` | `%s` |' % (i + 1, bf, af) for i, (pos, bf, af) in enumerate(csteps))
K['CRC_TX'] = '1101011011' + crc
chk, _ = D.crc_div(K['CRC_TX'], '10011'); assert chk == '0000'
bad = list(K['CRC_TX']); bad[4] = '1' if bad[4] == '0' else '0'
chk2, _ = D.crc_div(''.join(bad), '10011')
# remainder of the received word: compute properly
def rem(word, g):
    w = [int(c) for c in word]; gg = [int(c) for c in g]
    for i in range(len(w) - len(gg) + 1):
        if w[i]:
            for j in range(len(gg)): w[i + j] ^= gg[j]
    return ''.join(map(str, w[-(len(gg) - 1):]))
K['CRC_BAD'] = ''.join(bad); K['CRC_BAD_REM'] = rem(''.join(bad), '10011')
assert K['CRC_BAD_REM'] != '0000'
# ---------- checksum
words16 = [0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0x0000, 0xC0A8, 0x0001, 0xC0A8, 0x00C7]
ck, tot = D.internet_checksum(words16)
raw = sum(words16)
K['CK_RAW'] = '%X' % raw; K['CK_FOLD'] = '%X' % tot; K['CK'] = '%04X' % ck
assert D.internet_checksum(words16[:5] + [ck] + words16[6:])[1] == 0xFFFF
# ---------- CDMA
def cdma_md(bitsv):
    Hd, tx, rec = D.cdma(bitsv)
    sym = lambda v: '+' if v > 0 else '-'
    rows = ['| User | Walsh code (chips 1 to 8) | Data bit | $d_i$ |', '|---|---|---|---|']
    for i in range(8):
        dv = bitsv[i]; bt = '1' if dv > 0 else ('0' if dv < 0 else 'silent')
        rows.append('| %d | `%s` | %s | %+d |' % (i + 1, ' '.join(sym(v) for v in Hd[i]), bt, dv))
    t1 = '\n'.join(rows)
    rows = ['| User | $d_i \\times$ code (8 chips) |', '|---|---|']
    for i in range(8): rows.append('| %d | `%s` |' % (i + 1, ' '.join('%+d' % (bitsv[i] * v) for v in Hd[i])))
    rows.append('| **Sum (channel)** | **`%s`** |' % ' '.join('%+d' % v for v in tx))
    t2 = '\n'.join(rows)
    rows = ['| User | $\\sum \\text{chip}_k \\cdot c_{i,k}$ | $/8$ | Decision |', '|---|---|---|---|']
    for i in range(8):
        s = int((tx * Hd[i]).sum()); v = s / 8
        rows.append('| %d | %+d | %+.0f | %s |' % (i + 1, s, v, '1' if v > 0 else ('0' if v < 0 else 'silent')))
    return t1, t2, '\n'.join(rows)
K['CDMA_A'] = cdma_md([1, 1, 1, -1, -1, -1, 0, 0])
K['CDMA_B'] = cdma_md([1, 1, 1, 1, -1, -1, 0, 0])
# ---------- DSSS
barker = '10110111000'
K['DSSS'] = '\n'.join('| %s | `%s` | `%s` |' % (bt, barker, ''.join(str(int(c) ^ (1 if bt == '1' else 0) ^ 1) if False else str(int(c) ^ int(bt) ^ 1) for c in barker)) for bt in '10')
K['DSSS_NOTE'] = ''
# ---------- figures
K['FIG_full'] = D.duplex_fig('full'); K['FIG_both'] = D.duplex_fig('both')
K['FIG_lineA'] = D.line_fig('1000000101'); K['FIG_lineB'] = D.line_fig('1000000000101', True)
K['FIG_am'] = D.am_fig(); K['FIG_mod'] = D.digital_mod_fig(); K['FIG_hier'] = D.hierarchy_fig()
K['FIG_spec'] = D.spectrum_fig(); K['FIG_amfm'] = D.amfm_fig(); K['FIG_pcm'] = D.pcm_fig()

def sub(m):
    key = m.group(1)
    if key.startswith('CDMA'):
        base, idx = key.split('.'); return K[base][int(idx)]
    v = K[key]
    return v if isinstance(v, str) else str(v)
for src, dst in (('tplA.md', 'ioe-enct253-2083-baishakh.md'), ('tplB.md', 'ioe-enct253-2082-bhadra.md')):
    t = open(os.path.join(here, src)).read()
    t = re.sub(r'\{\{([\w.]+)\}\}', sub, t)
    # tuple values
    t = t.replace('@HAM@', '%d %d %d' % K['HAM'][:3])
    open(os.path.join(out, dst), 'w').write(t); print('wrote', dst, len(t))
print(K['HAM'], K['SF_STATS'], K['H_H'], K['H_L'], K['H_EFF'], K['H_BITS'], K['CRC'], K['CK'], K['CRC_BAD_REM'])
print(K['DSSS'])
