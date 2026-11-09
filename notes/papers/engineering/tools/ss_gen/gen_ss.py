"""python3 gen_ss.py <content dir> -> ioe-enex255-2083-baishakh.md, ioe-enex255-2082-bhadra.md (from tplA.md / tplB.md)."""
import os, re, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mpu_gen'))
from mpulib import fig
out = sys.argv[1] if len(sys.argv) > 1 else '.'
here = os.path.dirname(os.path.abspath(__file__))
K = {}

# ------------------------------------------------ numerics (all asserted)
def fmt(v):
    v = float(v)
    return str(int(round(v))) if abs(v - round(v)) < 1e-9 else ('%g' % round(v, 6))

xa, ha = [1, 2, 3, 4], [1, 2, -3]
ya = np.convolve(xa, ha); assert list(ya) == [1, 4, 4, 4, -1, -12]
xb, hb = [1, -0.25, 0, -1, 0.5, -0.5], [-2, -1, 0, 1, 2]
yb = np.convolve(xb, hb)
def shift_table(x, h, y):
    n = len(y); hdr = '| $x[k]$ | ' + ' | '.join('n=%d' % i for i in range(n)) + ' |'
    rows = [hdr, '|---|' + '---|' * n]
    for k, xv in enumerate(x):
        cells = [''] * n
        for j, hv in enumerate(h): cells[k + j] = fmt(xv * hv)
        rows.append('| %s ($k = %d$) | ' % (fmt(xv), k) + ' | '.join(cells) + ' |')
    rows.append('| **y[n]** | ' + ' | '.join('**%s**' % fmt(v) for v in y) + ' |')
    return '\n'.join(rows)
K['TAB_A'] = shift_table(xa, ha, ya); K['Y_A'] = ', '.join(fmt(v) for v in ya)
K['TAB_B'] = shift_table(xb, hb, yb); K['Y_B'] = ', '.join(fmt(v) for v in yb)
# Fourier series check, paper A, N = 8
N = 8; n = np.arange(N)
x = 1 + np.sin(2 * np.pi / N * n) + 3 * np.cos(2 * np.pi / N * n) + np.cos(4 * np.pi / N * n + np.pi / 2)
c = np.fft.fft(x) / N
assert abs(c[0] - 1) < 1e-12 and abs(c[1] - (1.5 - 0.5j)) < 1e-12 and abs(c[2] - 0.5j) < 1e-12 and abs(c[7] - (1.5 + 0.5j)) < 1e-12 and abs(c[6] + 0.5j) < 1e-12
assert abs((abs(c) ** 2).sum() - 6.5) < 1e-12 and abs((x ** 2).mean() - 6.5) < 1e-12
n6 = np.arange(6); c6 = np.fft.fft(np.sin(np.pi / 3 * n6)) / 6
assert abs(c6[1] + 0.5j) < 1e-12 and abs(c6[5] - 0.5j) < 1e-12 and abs((abs(c6) ** 2).sum() - 0.5) < 1e-12
EB = 4 * np.exp(-10) / 10; K['EB'] = '%.3e' % EB
# differencer
W = np.linspace(-np.pi, np.pi, 9); Hd = 0.5 * (1 - np.exp(-1j * W)); assert np.allclose(abs(Hd), abs(np.sin(W / 2)))
# 5cos(3000 pi t) sin(1000 pi t) = 2.5 [sin 4000 pi t - sin 2000 pi t]
tt = np.linspace(0, 0.01, 777)
assert np.allclose(5 * np.cos(3000 * np.pi * tt) * np.sin(1000 * np.pi * tt), 2.5 * (np.sin(4000 * np.pi * tt) - np.sin(2000 * np.pi * tt)))

# ------------------------------------------------ figures
def stem_fig(cap, body): return fig(cap, body)

K['FIG_fsA'] = fig("Spectra of x[n] = 1 + sin(2 pi n/N) + 3 cos(2 pi n/N) + cos(4 pi n/N + pi/2) (N >= 5): magnitude |c_k| (left) and phase of c_k (right); both repeat with period N.", '''
import numpy as np
k=np.arange(-4,5); c={0:1,1:1.5-0.5j,-1:1.5+0.5j,2:0.5j,-2:-0.5j}
mag=[abs(c.get(i,0)) for i in k]; ph=[np.degrees(np.angle(c[i])) if i in c else 0 for i in k]
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.9))
a.stem(k,mag,linefmt=ACCENT,markerfmt="o",basefmt="k-"); a.set_xlabel("k",fontsize=7); a.set_title("|c_k|",fontsize=8); a.set_ylim(0,1.9); a.tick_params(labelsize=6)
for i,m in zip(k,mag):
    if m>0: a.text(i,m+0.08,"%.3g"%m,ha="center",fontsize=6.5)
b.stem(k,ph,linefmt="#b00020",markerfmt="o",basefmt="k-"); b.set_xlabel("k",fontsize=7); b.set_title("angle of c_k (degrees)",fontsize=8); b.set_ylim(-130,130); b.tick_params(labelsize=6)
for i,p in zip(k,ph):
    if i in c: b.text(i,p+(12 if p>=0 else -22),"%.1f"%p,ha="center",fontsize=6.5)
fig.tight_layout()
''')
K['FIG_rc'] = fig("RC low-pass filter: circuit, magnitude response |H| (dB) and phase response against w/wc (log scale); wc = 1/RC, |H| = -3 dB and phase = -45 degrees at wc.", '''
import numpy as np
fig=plt.figure(figsize=(7.4,3.4))
c=fig.add_axes([0.0,0.05,0.34,0.9]); c.axis("off"); c.set_xlim(0,6); c.set_ylim(0,6)
L=dict(color=INK,lw=1.4)
c.plot([0.8,1.5],[4.5,4.5],**L)
zx=[1.5,1.7,1.9,2.1,2.3,2.5,2.7,2.9,3.1]; zy=[4.5,4.9,4.1,4.9,4.1,4.9,4.1,4.9,4.5]
c.plot(zx,zy,**L); c.plot([3.1,4.4],[4.5,4.5],**L)
c.plot([4.4,4.4],[4.5,3.5],**L); c.plot([3.9,4.9],[3.5,3.5],color=INK,lw=2.4); c.plot([3.9,4.9],[3.0,3.0],color=INK,lw=2.4); c.plot([4.4,4.4],[3.0,1.5],**L)
c.plot([0.8,4.4],[1.5,1.5],**L); c.plot([0.8,0.8],[1.5,4.5],**L,alpha=0); c.plot([4.4,5.2],[4.5,4.5],**L); c.plot([4.4,5.2],[1.5,1.5],**L)
c.plot([0.8,0.8],[1.5,2.4],**L); c.plot([0.8,0.8],[3.6,4.5],**L); c.add_patch(mp.Circle((0.8,3.0),0.6,fc="white",ec=INK,lw=1.4)); c.text(0.8,3.0,"~",ha="center",va="center",fontsize=11)
c.plot([5.2,5.2],[1.5,4.5],color=ACCENT,lw=1.2,ls="--"); c.plot([5.2],[4.5],"o",color=ACCENT,ms=4); c.plot([5.2],[1.5],"o",color=ACCENT,ms=4)
c.text(2.3,5.35,"R",fontsize=9,ha="center"); c.text(5.15,3.25,"C",fontsize=9); c.text(0.15,3.0,"x(t)",fontsize=8,ha="right"); c.text(5.4,3.0,"y(t)",fontsize=8,va="center")
w=np.logspace(-2,2,400); H=1/(1+1j*w)
a=fig.add_axes([0.46,0.57,0.52,0.38]); a.semilogx(w,20*np.log10(abs(H)),color=ACCENT,lw=1.6); a.axhline(-3,color="#999",lw=0.6,ls=":"); a.axvline(1,color="#999",lw=0.6,ls=":")
a.set_ylabel("|H| (dB)",fontsize=7); a.tick_params(labelsize=6); a.set_xticklabels([]); a.set_ylim(-42,3); a.plot([1],[-3.01],"o",color="#b00020",ms=3)
b=fig.add_axes([0.46,0.14,0.52,0.38]); b.semilogx(w,np.degrees(np.angle(H)),color="#b00020",lw=1.6); b.axhline(-45,color="#999",lw=0.6,ls=":"); b.axvline(1,color="#999",lw=0.6,ls=":")
b.set_ylabel("phase (deg)",fontsize=7); b.set_xlabel("w / wc",fontsize=7); b.tick_params(labelsize=6); b.set_ylim(-95,5); b.plot([1],[-45],"o",color="#b00020",ms=3)
''')
def conv_fig(x, h, y, nx0, cap):
    body = '''
import numpy as np
x=@X@; h=@H@; y=@Y@
fig,axs=plt.subplots(1,3,figsize=(7.4,2.5))
for ax,v,t in zip(axs,(x,h,y),("x[n]","h[n]","y[n] = x[n] * h[n]")):
    n=np.arange(len(v)); ax.stem(n,v,linefmt=ACCENT,markerfmt="o",basefmt="k-"); ax.set_title(t,fontsize=8); ax.set_xlabel("n",fontsize=7); ax.tick_params(labelsize=6)
    ax.set_ylim(min(0,min(v))-0.15*(max(v)-min(v)+1),max(0,max(v))+0.2*(max(v)-min(v)+1)); ax.set_xticks(n)
    for i,vv in zip(n,v): ax.text(i,vv+(0.04*(max(v)-min(v)+1) if vv>=0 else -0.1*(max(v)-min(v)+1)),("%.4g"%vv),ha="center",fontsize=5.5)
fig.tight_layout()
'''.replace('@X@', repr([float(v) for v in x])).replace('@H@', repr([float(v) for v in h])).replace('@Y@', repr([float(v) for v in y]))
    return fig(cap, body)
K['FIG_convA'] = conv_fig(xa, ha, ya, 0, "Convolution of x[n] = {1, 2, 3, 4} and h[n] = {1, 2, -3} with the first sample of each at n = 0: y[n] has 4 + 3 - 1 = 6 samples.")
K['FIG_convB'] = conv_fig(xb, hb, yb, 0, "Output of the DT LTI system: y[n] = x[n] * h[n], 6 + 5 - 1 = 10 samples (first samples at n = 0).")
K['FIG_samp'] = fig("Sampling in the frequency domain: for fs > 2B the replicas of the spectrum at multiples of fs do not overlap (left); for fs < 2B they overlap, which is aliasing (right).", '''
import numpy as np
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.6))
def tri(f,B): return np.clip(1-abs(f)/B,0,None)
f=np.linspace(-16,16,2000); B=3
for ax,fs,t in ((a,8,"fs = 8 B/3 > 2B: no overlap"),(b,4,"fs = 4 B/3 < 2B: overlap (aliasing)")):
    tot=0
    for m in range(-3,4):
        y=tri(f-m*fs,B); ax.plot(f,y,color=ACCENT if m==0 else "#b00020",lw=1.3 if m==0 else 0.9,ls="-" if m==0 else "--"); tot=tot+y
    if fs<2*B: ax.fill_between(f,0,tot,where=tot>1.0001*np.maximum(tri(f,B),0),color="#b00020",alpha=0.15)
    ax.set_title(t,fontsize=7.5); ax.set_xlim(-14,14); ax.set_ylim(0,1.5); ax.set_xlabel("f",fontsize=7); ax.tick_params(labelsize=6)
    ax.set_xticks([-fs,0,fs]); ax.set_xticklabels(["-fs","0","fs"])
fig.tight_layout()
''')
K['FIG_diff'] = fig("Frequency response of y[n] = 0.5 x[n] - 0.5 x[n-1]: |H(W)| = |sin(W/2)| (a high-pass / differencing filter) and its phase.", '''
import numpy as np
W=np.linspace(-np.pi,np.pi,801); H=0.5*(1-np.exp(-1j*W))
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.7))
a.plot(W,abs(H),color=ACCENT,lw=1.6); a.set_title("|H(W)| = |sin(W/2)|",fontsize=8); a.set_xlabel("W (rad)",fontsize=7); a.tick_params(labelsize=6); a.set_xticks([-np.pi,0,np.pi]); a.set_xticklabels(["-pi","0","pi"])
b.plot(W,np.degrees(np.angle(H)),color="#b00020",lw=1.6); b.set_title("angle H(W) (degrees)",fontsize=8); b.set_xlabel("W (rad)",fontsize=7); b.tick_params(labelsize=6); b.set_xticks([-np.pi,0,np.pi]); b.set_xticklabels(["-pi","0","pi"]); b.set_ylim(-100,100)
fig.tight_layout()
''')
K['FIG_basic'] = fig("Discrete-time unit impulse delta[n], unit step u[n] and unit ramp r[n] = n u[n].", '''
import numpy as np
n=np.arange(-4,7)
fig,axs=plt.subplots(1,3,figsize=(7.4,2.3))
for ax,y,t in zip(axs,(n==0,(n>=0),np.where(n>=0,n,0)),("delta[n]","u[n]","r[n] = n u[n]")):
    ax.stem(n,y.astype(float),linefmt=ACCENT,markerfmt="o",basefmt="k-"); ax.set_title(t,fontsize=8); ax.set_xticks(n[::2]); ax.tick_params(labelsize=6); ax.set_xlabel("n",fontsize=7)
fig.tight_layout()
''')
K['FIG_sinB'] = fig("Spectra of x[n] = sin(pi n/3) (N = 6): the only non-zero coefficients are c_1 = -j/2 and c_-1 = c_5 = +j/2; magnitude (left) and phase (right).", '''
import numpy as np
k=np.arange(-3,4); c={1:-0.5j,-1:0.5j}
mag=[abs(c.get(i,0)) for i in k]; ph=[np.degrees(np.angle(c[i])) if i in c else 0 for i in k]
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.6))
a.stem(k,mag,linefmt=ACCENT,markerfmt="o",basefmt="k-"); a.set_title("|c_k|",fontsize=8); a.set_xlabel("k",fontsize=7); a.set_ylim(0,0.75); a.tick_params(labelsize=6)
for i,m in zip(k,mag):
    if m: a.text(i,m+0.04,"0.5",ha="center",fontsize=7)
b.stem(k,ph,linefmt="#b00020",markerfmt="o",basefmt="k-"); b.set_title("angle of c_k (degrees)",fontsize=8); b.set_xlabel("k",fontsize=7); b.set_ylim(-130,130); b.tick_params(labelsize=6)
for i,p in zip(k,ph):
    if i in c: b.text(i,p+(12 if p>0 else -22),"%d"%p,ha="center",fontsize=7)
fig.tight_layout()
''')
K['FIG_ideal'] = fig("Ideal low-pass and high-pass filters: frequency responses (top) and impulse responses (bottom), h_LP(t) = sin(wc t)/(pi t) and h_HP(t) = delta(t) - h_LP(t).", '''
import numpy as np
fig,axs=plt.subplots(2,2,figsize=(7.4,4.2)); wc=2*np.pi
w=np.linspace(-3*wc,3*wc,1200)
lp=(abs(w)<=wc).astype(float); hp=1-lp
for ax,y,t in ((axs[0,0],lp,"Ideal LPF: H(w)"),(axs[0,1],hp,"Ideal HPF: H(w)")):
    ax.plot(w,y,color=ACCENT,lw=1.8); ax.set_ylim(-0.2,1.3); ax.set_title(t,fontsize=8); ax.set_xticks([-wc,0,wc]); ax.set_xticklabels(["-wc","0","wc"]); ax.tick_params(labelsize=6); ax.set_xlabel("w",fontsize=7)
t=np.linspace(-3,3,1201); h=np.where(abs(t)<1e-9,wc/np.pi,np.sin(wc*t)/(np.pi*np.where(abs(t)<1e-9,1,t)))
axs[1,0].plot(t,h,color="#b00020",lw=1.4); axs[1,0].set_title("h_LP(t) = sin(wc t)/(pi t); peak wc/pi",fontsize=8)
axs[1,1].plot(t,-h,color="#b00020",lw=1.4); axs[1,1].annotate("",xy=(0,1.35),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#b00020",lw=1.6)); axs[1,1].text(0.1,1.2,"delta(t)",fontsize=7); axs[1,1].set_ylim(-0.4,1.6); axs[1,1].set_title("h_HP(t) = delta(t) - h_LP(t)",fontsize=8)
for ax in axs[1]:
    ax.axhline(0,color="#999",lw=0.5); ax.set_xlabel("t (s), wc = 2 pi rad/s",fontsize=7); ax.tick_params(labelsize=6)
fig.tight_layout()
''')

def sub(m): return str(K[m.group(1)])
for src, dst in (('tplA.md', 'ioe-enex255-2083-baishakh.md'), ('tplB.md', 'ioe-enex255-2082-bhadra.md')):
    t = open(os.path.join(here, src)).read()
    t = re.sub(r'\{\{([\w.]+)\}\}', sub, t)
    open(os.path.join(out, dst), 'w').write(t); print('wrote', dst, len(t))
print(K['Y_A'], '|', K['Y_B'], '|', K['EB'])
