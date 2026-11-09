"""Computations + figure blocks for the Data Communication (ENCT 253) papers."""
import sys, os, heapq, math, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mpu_gen'))
from mpulib import PRE, fig
import numpy as np


# ---------------------------------------------------------------- source coding
def freq_table(s):
    order, f = [], {}
    for ch in s:
        if ch not in f: order.append(ch); f[ch] = 0
        f[ch] += 1
    return order, f


def name(ch):
    return {' ': '␣', }.get(ch, ch)


def shannon_fano(s):
    order, f = freq_table(s)
    syms = sorted(order, key=lambda c: (-f[c], order.index(c)))
    codes = {c: '' for c in syms}
    steps = []

    def split(group, depth):
        if len(group) == 1: return
        tot = sum(f[c] for c in group); best = None; acc = 0
        for i in range(1, len(group)):
            acc += f[group[i - 1]]
            d = abs(tot - 2 * acc)
            if best is None or d < best[0]: best = (d, i)
        i = best[1]; a, b = group[:i], group[i:]
        steps.append((depth, a, b, sum(f[c] for c in a), sum(f[c] for c in b)))
        for c in a: codes[c] += '0'
        for c in b: codes[c] += '1'
        split(a, depth + 1); split(b, depth + 1)
    split(syms, 1)
    return syms, f, codes, steps


def huffman(s):
    order, f = freq_table(s)
    cnt = itertools.count(); h = [(f[c], next(cnt), c) for c in sorted(order, key=lambda c: (f[c], order.index(c)))]
    heapq.heapify(h); steps = []; tree = {}
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h)
        node = (a[0] + b[0], next(cnt), (a, b)); steps.append((a, b, a[0] + b[0], node)); heapq.heappush(h, node)
    codes = {}

    def walk(n, pre):
        if isinstance(n[2], str): codes[n[2]] = pre or '0'
        else: walk(n[2][0], pre + '0'); walk(n[2][1], pre + '1')
    walk(h[0], '')
    return order, f, codes, steps


def label(item):
    return item[2] if isinstance(item[2], str) else 'node(' + str(item[0]) + ')'


def code_stats(s, f, codes):
    n = len(s); H = -sum(f[c] / n * math.log2(f[c] / n) for c in f); L = sum(f[c] / n * len(codes[c]) for c in f)
    return n, H, L, H / L


def coding_md(s, syms, f, codes, nm=name):
    n, H, L, eff = code_stats(s, f, codes)
    rows = ['| Symbol | Count $n_i$ | $p_i$ | $-\\log_2 p_i$ | Code | Length $l_i$ | $p_i l_i$ |', '|---|---|---|---|---|---|---|']
    for c in syms:
        p = f[c] / n
        rows.append('| `%s` | %d | %d/%d = %.4f | %.3f | `%s` | %d | %.4f |' % (nm(c), f[c], f[c], n, p, -math.log2(p), codes[c], len(codes[c]), p * len(codes[c])))
    rows.append('| **Total** | %d | 1 | | | | **%.4f** |' % (n, L))
    enc = ' '.join(codes[c] for c in s); bits = sum(len(codes[c]) for c in s)
    return '\n'.join(rows), H, L, eff, enc, bits, n


# ---------------------------------------------------------------- error control
def hamming74_check(word):
    bits = [int(c) for c in word]
    pos = {i + 1: b for i, b in enumerate(bits)}
    c1 = sum(pos[i] for i in (1, 3, 5, 7)) % 2; c2 = sum(pos[i] for i in (2, 3, 6, 7)) % 2; c4 = sum(pos[i] for i in (4, 5, 6, 7)) % 2
    syn = c4 * 4 + c2 * 2 + c1
    fixed = bits[:]
    if syn: fixed[syn - 1] ^= 1
    return (c1, c2, c4), syn, ''.join(map(str, fixed))


G = np.array([[1, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1]])
H = np.array([[1, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 0], [0, 1, 1, 0, 0, 1]])
assert ((G @ H.T) % 2 == 0).all()


def lbc():
    words = {}
    for m in itertools.product([0, 1], repeat=3):
        c = tuple((np.array(m) @ G) % 2); words[m] = c
    dmin = min(sum(a != b for a, b in zip(x, y)) for x, y in itertools.combinations(words.values(), 2))
    return words, dmin


def crc_div(data, gen):
    r = len(gen) - 1; buf = [int(c) for c in data + '0' * r]; g = [int(c) for c in gen]; steps = []
    for i in range(len(data)):
        if buf[i]:
            before = ''.join(map(str, buf[i:i + len(g)]))
            for j in range(len(g)): buf[i + j] ^= g[j]
            steps.append((i, before, ''.join(map(str, buf[i:i + len(g)]))))
    return ''.join(map(str, buf[-r:])), steps


def internet_checksum(words):
    s = 0
    for w in words:
        s += w
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF, s


def cdma(bits):
    Hd = np.array([[1]])
    for _ in range(3): Hd = np.block([[Hd, Hd], [Hd, -Hd]])
    d = np.array(bits); tx = (d[:, None] * Hd).sum(axis=0)
    rec = [(tx * Hd[i]).sum() / 8 for i in range(8)]
    return Hd, tx, rec


# ---------------------------------------------------------------- figures
def duplex_fig(kind):
    if kind == 'full':
        body = '''
fig,ax=plt.subplots(figsize=(7.4,4.2)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(0,8.6)
ax.text(7.5,8.2,"Digital voice call (mobile phone / VoIP): full duplex, both directions at the same time",ha="center",fontsize=8,weight="bold")
names=["Microphone\\n(analog voice)","ADC + speech\\nencoder (codec)","Channel\\nencoder","Modulator\\n+ transmitter"]
for i,n in enumerate(names): box(ax,1.2+i*2.35,6.4,2.0,1.2,n,fs=6.3,fc=BLUE)
for i in range(3): arr(ax,(2.25+i*2.35,6.4),(2.55+i*2.35,6.4),c=ACCENT)
box(ax,12.0,6.4,2.2,1.2,"Radio channel 1\\n(uplink, f1)",fs=6.8,fc=YEL); arr(ax,(9.3,6.4),(10.85,6.4),c=ACCENT)
box(ax,12.0,4.0,2.2,1.2,"Radio channel 2\\n(downlink, f2)",fs=6.8,fc=YEL)
names2=["Speaker\\n(analog voice)","DAC + speech\\ndecoder","Channel\\ndecoder","Demodulator\\n+ receiver"]
for i,n in enumerate(names2): box(ax,1.2+i*2.35,4.0,2.0,1.2,n,fs=6.3,fc=GRN)
for i in range(3): arr(ax,(2.55+i*2.35,4.0),(2.25+i*2.35,4.0),c="#2e7d32")
arr(ax,(10.85,4.0),(9.3,4.0),c="#2e7d32")
arr(ax,(12.0,5.8),(12.0,4.6),c=INK,style="<|-|>",lw=0.0)
ax.text(5.0,2.7,"Station A (left half) talks to station B through channel 1 and, at the same time,",ha="center",fontsize=7)
ax.text(5.0,2.2,"listens to station B through channel 2 (the same two chains exist in B in mirror image).",ha="center",fontsize=7)
ax.text(5.0,1.5,"Separation of the two directions: FDD (different frequencies f1, f2) or two wire pairs / echo cancellation.",ha="center",fontsize=7)
ax.text(5.0,0.8,"Top chain = transmit path of A, bottom chain = receive path of A.",ha="center",fontsize=7,color="#555")
'''
        cap = "Full-duplex digital voice link: the transmit chain and the receive chain of a station work simultaneously on two separate channels."
    else:
        body = '''
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,3.0))
for z in (a,b): z.axis("off"); z.set_xlim(0,8); z.set_ylim(0,6)
a.set_title("Half duplex (walkie-talkie, push to talk)",fontsize=8)
box(a,1.2,3.5,1.8,1.2,"Station A\\nTx / Rx",fs=7.5,fc=BLUE); box(a,6.8,3.5,1.8,1.2,"Station B\\nRx / Tx",fs=7.5,fc=GRN)
arr(a,(2.15,3.8),(5.85,3.8),c=ACCENT); arr(a,(5.85,3.2),(2.15,3.2),c="#2e7d32"); a.text(4.0,4.35,"A speaks, B listens",fontsize=6.8,ha="center"); a.text(4.0,2.5,"then B speaks, A listens (turns)",fontsize=6.8,ha="center",color="#2e7d32")
a.text(4.0,1.2,"one channel, one direction at a time",fontsize=7.2,ha="center",weight="bold")
b.set_title("Full duplex (telephone, mobile call)",fontsize=8)
box(b,1.2,3.5,1.8,1.2,"Station A\\nTx + Rx",fs=7.5,fc=BLUE); box(b,6.8,3.5,1.8,1.2,"Station B\\nTx + Rx",fs=7.5,fc=GRN)
arr(b,(2.15,4.0),(5.85,4.0),c=ACCENT); arr(b,(5.85,3.0),(2.15,3.0),c="#2e7d32"); b.text(4.0,4.5,"channel 1: A to B",fontsize=6.8,ha="center"); b.text(4.0,2.45,"channel 2: B to A (simultaneous)",fontsize=6.8,ha="center",color="#2e7d32")
b.text(4.0,1.2,"two channels, both directions at once",fontsize=7.2,ha="center",weight="bold")
'''
        cap = "Half-duplex (one direction at a time over one channel) and full-duplex (both directions simultaneously over two channels) communication."
    return fig(cap, body)


def line_fig(bits, b8zs=False):
    body = '''
import numpy as np
bits=[int(c) for c in "@BITS@"]; n=len(bits); B8=@B8@
def steps(levels): 
    x=[];y=[]
    for i,l in enumerate(levels): x+=[i,i+1]; y+=[l,l]
    return x,y
def half(levels2):
    x=[];y=[]
    for i,(a,b) in enumerate(levels2): x+=[i,i+0.5,i+0.5,i+1]; y+=[a,a,b,b]
    return x,y
unip=[b for b in bits]; polar=[1 if b else -1 for b in bits]
manch=[(1,-1) if b else (-1,1) for b in bits]   # 1: high-to-low, 0: low-to-high (IEEE 802.3 uses the opposite)
last=-1; ami=[]
for b in bits:
    if b: last=-last; ami.append(last)
    else: ami.append(0)
rows=[("Unipolar NRZ",steps(unip),(-0.3,1.3)),("Polar NRZ-L",steps(polar),(-1.4,1.4)),("Polar Manchester",half(manch),(-1.4,1.4)),("Bipolar AMI",steps(ami),(-1.4,1.4))]
if B8:
    b8=[];last=-1;i=0;sq=[]
    # B8ZS: eight consecutive zeros -> 0 0 0 V B 0 V B
    zeros=0;out=[];last=-1
    k=0
    while k<n:
        if bits[k]==1: last=-last; out.append(last); k+=1
        else:
            if k+8<=n and all(v==0 for v in bits[k:k+8]):
                V=last; Bp=-last; out+=[0,0,0,V,Bp,0,Bp,V]; last=V; k+=8
            else: out.append(0); k+=1
    rows.append(("Bipolar B8ZS",steps(out),(-1.4,1.4)))
fig,axs=plt.subplots(len(rows),1,figsize=(7.4,0.95*len(rows)+0.5),sharex=True)
for ax,(t,(x,y),yl) in zip(axs,rows):
    ax.plot(x,y,color=ACCENT,lw=1.8); ax.axhline(0,color="#999999",lw=0.6)
    for i in range(n+1): ax.axvline(i,color="#cccccc",lw=0.5,ls=":")
    ax.set_ylim(*yl); ax.set_yticks([]); ax.set_ylabel(t,rotation=0,ha="right",va="center",fontsize=7)
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6)
for i,b in enumerate(bits): axs[0].text(i+0.5,1.55,str(b),ha="center",fontsize=8,weight="bold")
axs[-1].set_xticks(range(n+1)); axs[-1].set_xlabel("bit interval",fontsize=7)
fig.subplots_adjust(left=0.2,right=0.98,top=0.9,bottom=0.12,hspace=0.25)
'''.replace('@BITS@', bits).replace('@B8@', 'True' if b8zs else 'False')
    cap = "Line codes for the bit sequence %s: unipolar NRZ, polar NRZ-L and Manchester, bipolar AMI%s." % (bits, " and B8ZS (the eight zeros are replaced by 000VB0VB)" if b8zs else "")
    return fig(cap, body)


def am_fig():
    body = '''
import numpy as np
t=np.linspace(0,2.0,4000); fc=12.0
fig,axs=plt.subplots(2,2,figsize=(7.4,4.4))
m1=0.6*np.cos(2*np.pi*1*t); s1=(1+m1)*np.cos(2*np.pi*fc*t)
m2=0.4*np.cos(2*np.pi*1*t)+0.3*np.cos(2*np.pi*2.5*t); s2=(1+m2)*np.cos(2*np.pi*fc*t)
for ax,m,s,tt in ((axs[0,0],m1,s1,"Single-tone AM, mu = 0.6"),(axs[0,1],m2,s2,"Double-tone AM, mu1 = 0.4, mu2 = 0.3")):
    ax.plot(t,s,color=ACCENT,lw=0.5); ax.plot(t,1+m,color="#b00020",lw=1.0); ax.plot(t,-(1+m),color="#b00020",lw=1.0)
    ax.set_title(tt,fontsize=7.5); ax.set_xlabel("t",fontsize=6.5); ax.tick_params(labelsize=6); ax.set_ylim(-2.2,2.2)
def stems(ax,fr,am,lab):
    ax.vlines(fr,0,am,color=ACCENT,lw=2.2)
    for f,a,l in zip(fr,am,lab): ax.text(f,a+0.04,l,ha="center",fontsize=6.3)
    ax.set_xlim(7,17); ax.set_ylim(0,1.35); ax.set_xlabel("f",fontsize=6.5); ax.tick_params(labelsize=6)
stems(axs[1,0],[11,12,13],[0.3,1.0,0.3],["Ac*mu/2","Ac","Ac*mu/2"]); axs[1,0].set_title("Spectrum: BW = 2 fm",fontsize=7.5)
stems(axs[1,1],[9.5,10,12,14,14.5],[0.15,0.2,1.0,0.2,0.15],["","Ac*mu1/2","Ac","","Ac*mu2/2"]); axs[1,1].set_title("Spectrum: BW = 2 max(f1, f2)",fontsize=7.5)
axs[1,1].set_xticks([9.5,10,11,12,13,14,14.5])
fig.tight_layout()
'''
    return fig("Single-tone and double-tone AM: waveforms with the envelope 1+m(t) (top) and line spectra (bottom).", body)


def digital_mod_fig():
    body = '''
import numpy as np
bits=[1,0,1,1,0,0,1]; n=len(bits); fs=200
t=np.arange(n*fs)/fs; d=np.repeat(bits,fs)
fig,axs=plt.subplots(4,1,figsize=(7.4,4.6),sharex=True)
axs[0].plot(t,d,color=INK,lw=1.6); axs[0].set_ylim(-0.3,1.3); axs[0].set_yticks([]); axs[0].set_ylabel("data",rotation=0,ha="right",va="center",fontsize=7)
ask=d*np.sin(2*np.pi*4*t); psk=np.sin(2*np.pi*4*t+np.pi*(1-d)); fsk=np.sin(2*np.pi*(2.5+3.0*d)*t)
for ax,y,tt in ((axs[1],ask,"ASK"),(axs[2],psk,"PSK"),(axs[3],fsk,"FSK")):
    ax.plot(t,y,color=ACCENT,lw=1.0); ax.set_yticks([]); ax.set_ylabel(tt,rotation=0,ha="right",va="center",fontsize=7); ax.set_ylim(-1.4,1.4)
for ax in axs:
    for i in range(n+1): ax.axvline(i,color="#cccccc",lw=0.5,ls=":")
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
for i,b in enumerate(bits): axs[0].text(i+0.5,1.4,str(b),ha="center",fontsize=8,weight="bold")
axs[1].text(7.05,0,"amplitude: carrier on / off",fontsize=6.3,va="center"); axs[2].text(7.05,0,"phase: 0 / 180 deg",fontsize=6.3,va="center"); axs[3].text(7.05,0,"frequency: f0 / f1",fontsize=6.3,va="center")
axs[0].set_xlim(0,9.6); axs[-1].tick_params(labelsize=6); axs[-1].set_xlabel("bit interval",fontsize=7)
fig.subplots_adjust(left=0.1,right=0.98,top=0.93,bottom=0.1,hspace=0.2)
'''
    return fig("Binary ASK, PSK and FSK waveforms for the data 1011001.", body)


def hierarchy_fig():
    body = '''
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,4.4))
for z in (a,b): z.axis("off"); z.set_xlim(0,10); z.set_ylim(0,13)
a.set_title("Digital hierarchy (North American T-carrier)",fontsize=8)
rows=[("24 x DS0 (64 kbit/s)\\n24 voice channels",None),("DS1 (T1)\\n24 ch, 1.544 Mbit/s","24 : 1"),("DS2 (T2)\\n96 ch, 6.312 Mbit/s","4 x DS1"),("DS3 (T3)\\n672 ch, 44.736 Mbit/s","7 x DS2"),("DS4 (T4)\\n4032 ch, 274.176 Mbit/s","6 x DS3")]
for i,(t,m) in enumerate(rows):
    y=11.6-i*2.6; box(a,6.0,y,5.4,1.5,t,fs=6.5,fc=[BLUE,YEL,YEL,GRN,GRN][i])
    if m:
        ax_=a; ax_.add_patch(mp.Polygon([(0.6,y+1.35),(2.8,y+0.9),(2.8,y-0.9),(0.6,y-1.35)],fc="white",ec=INK,lw=1.1,zorder=3)); ax_.text(1.7,y,"MUX\\n"+m,fontsize=5.8,ha="center",va="center",zorder=4)
        arr(ax_,(2.8,y),(3.3,y),c=ACCENT); arr(ax_,(6.0,y+1.85),(6.0,y+0.8),c=INK,lw=0.0)
    if i: arr(a,(0.1,y+2.6-0.0),(0.1,y+2.6),c=INK,lw=0)
b.set_title("Analog hierarchy (FDM, AT&T)",fontsize=8)
rows=[("12 voice channels\\n4 kHz each",None),("Group\\n12 ch, 48 kHz\\n(60-108 kHz)","12 x 4 kHz"),("Supergroup\\n60 ch, 240 kHz\\n(312-552 kHz)","5 groups"),("Mastergroup\\n600 ch, 2.52 MHz\\n(564-3084 kHz)","10 supergroups"),("Jumbogroup\\n3600 ch, 16.984 MHz","6 mastergroups")]
for i,(t,m) in enumerate(rows):
    y=11.6-i*2.6; box(b,6.0,y,5.4,1.7,t,fs=6.3,fc=[BLUE,YEL,YEL,GRN,GRN][i])
    if m:
        b.add_patch(mp.Polygon([(0.2,y+1.35),(2.9,y+0.9),(2.9,y-0.9),(0.2,y-1.35)],fc="white",ec=INK,lw=1.1,zorder=3)); b.text(1.55,y,"FDM\\n"+m,fontsize=5.4,ha="center",va="center",zorder=4)
        arr(b,(2.9,y),(3.3,y),c=ACCENT)
for z in (a,b):
    for i in range(4):
        y=11.6-i*2.6; arr(z,(6.0,y-0.9),(6.0,y-2.6+0.9),c=INK)
fig.tight_layout()
'''
    return fig("Digital (T-carrier) and analog (FDM) multiplexing hierarchies with the number of channels and the data rate or bandwidth at each level.", body)


def spectrum_fig():
    body = '''
import numpy as np
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,3.0))
f=[0,80,150,160]; A=[6,3,1,4]
a.vlines([0,80,150,160],0,[6,6,2,8],color=ACCENT,lw=2.5)
for x,y,l in zip(f,[6,6,2,8],["6","6","2","8"]): a.text(x,y+0.25,l,ha="center",fontsize=7)
a.set_xlim(-20,200); a.set_ylim(0,9.5); a.set_xlabel("f (Hz)",fontsize=7); a.set_ylabel("single-sided amplitude",fontsize=7); a.set_title("Magnitude spectrum",fontsize=8); a.set_xticks([0,80,150,160]); a.tick_params(labelsize=6)
fr=[-160,-150,-80,0,80,150,160]; ph=[-120,-30,-130,0,130,30,120]
b.vlines(fr,0,ph,color="#b00020",lw=2.5); b.axhline(0,color="#999",lw=0.6)
for x,y in zip(fr,ph): b.text(x,y+(12 if y>=0 else -22),"%d"%y,ha="center",fontsize=6.5)
b.set_xlim(-200,200); b.set_ylim(-170,170); b.set_xlabel("f (Hz)",fontsize=7); b.set_ylabel("phase (degrees)",fontsize=7); b.set_title("Phase spectrum (cosine form)",fontsize=8); b.set_xticks([-160,-80,0,80,160]); b.tick_params(labelsize=6)
fig.tight_layout()
'''
    return fig("Line spectra of x(t) = 6 - 8 sin(2 pi 160 t + 30 deg) - 6 cos(160 pi t - 50 deg) + 2 sin(300 pi t + 120 deg): single-sided amplitude (left) and phase (right, cosine reference, two-sided).", body)


def amfm_fig():
    body = '''
import numpy as np
t=np.linspace(0,2,6000); m=np.cos(2*np.pi*t); fc=14
am=(1+0.7*m)*np.cos(2*np.pi*fc*t)
fm=np.cos(2*np.pi*fc*t+6*np.sin(2*np.pi*t))
fig,axs=plt.subplots(3,1,figsize=(7.4,4.4),sharex=True)
axs[0].plot(t,m,color=INK,lw=1.4); axs[0].set_ylabel("m(t)",fontsize=7)
axs[1].plot(t,am,color=ACCENT,lw=0.5); axs[1].plot(t,1+0.7*m,color="#b00020",lw=0.9); axs[1].plot(t,-(1+0.7*m),color="#b00020",lw=0.9); axs[1].set_ylabel("AM (mu = 0.7)\\namplitude varies",fontsize=7)
axs[2].plot(t,fm,color=ACCENT,lw=0.5); axs[2].set_ylabel("FM (beta = 6)\\nfrequency varies,\\namplitude constant",fontsize=7)
for ax in axs:
    ax.tick_params(labelsize=6)
    for s in ("top","right"): ax.spines[s].set_visible(False)
axs[2].set_xlabel("t",fontsize=7); fig.tight_layout()
'''
    return fig("Message signal, amplitude-modulated carrier (envelope follows m(t)) and frequency-modulated carrier (constant envelope, crowded where m(t) is high).", body)


def pcm_fig():
    body = '''
import numpy as np
fig=plt.figure(figsize=(7.4,4.6)); ax=fig.add_axes([0,0.62,1,0.38]); ax.axis("off"); ax.set_xlim(0,15.6); ax.set_ylim(0,3)
names=[("m(t)",None),("Low-pass\\nfilter",YEL),("Sampler\\nfs >= 2 fm",YEL),("Quantizer\\n2^n levels",YEL),("Encoder\\nn bits/sample",YEL),("PCM bit\\nstream",GRN)]
xs=[0.9,3.3,6.0,8.9,11.7,14.4]
for x,(t,c) in zip(xs,names):
    if c: box(ax,x,1.5,2.0 if x<14 else 1.8,1.2,t,fs=6.5,fc=c)
    else: ax.text(x,1.5,t,fontsize=8,ha="center",va="center")
for a_,b_ in zip([1.5,4.35,7.05,10.0,12.75],[2.25,5.0,7.85,10.75,13.5]): arr(ax,(a_,1.5),(b_,1.5),c=ACCENT)
ax.text(7.8,0.35,"transmitter: analog -> sampled (PAM) -> quantized -> binary code words",fontsize=6.8,ha="center",color="#555")
b=fig.add_axes([0.08,0.08,0.88,0.46])
t=np.linspace(0,1,400); x=3.5+3.4*np.sin(2*np.pi*t)
b.plot(t,x,color=INK,lw=1.2)
ts=np.arange(0,1.0001,1/8); xs_=3.5+3.4*np.sin(2*np.pi*ts); q=np.clip(np.round(xs_),0,7)
for L in range(8): b.axhline(L,color="#dddddd",lw=0.6); b.text(1.015,L,format(L,"03b"),fontsize=6,va="center")
b.stem(ts,q,linefmt=ACCENT,markerfmt="o",basefmt=" ")
for tt,qq in zip(ts,q): b.text(tt,qq+0.35,format(int(qq),"03b"),fontsize=6,ha="center",color="#b00020")
b.set_xlim(0,1.08); b.set_ylim(-0.5,8); b.set_yticks(range(8)); b.set_xlabel("t (one period, 8 samples, 3-bit quantizer, 8 levels)",fontsize=7); b.tick_params(labelsize=6)
b.set_ylabel("quantization level",fontsize=7)
'''
    return fig("Block diagram of PCM and an example: a sine wave sampled 8 times per period and quantized to 3 bits (levels 0 to 7, shown with their code words).", body)
