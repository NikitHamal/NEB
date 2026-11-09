"""Block-diagram / Nyquist / Bode helpers for the Control System papers (used inside ```figure blocks)."""
import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as mp
INK = "#14181f"; ACC = "#1d6fb8"; RED = "#d9534f"; MUT = "#5b6472"


def canvas(w, h, xl, yl):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*xl); ax.set_ylim(*yl); return fig, ax


def box(ax, x, y, t, w=1.3, h=0.8, fc="white", fs=7.8):
    ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                   fc=fc, ec=INK, lw=1.2, zorder=3))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, zorder=4)


def line(ax, pts, c=INK, lw=1.3, ls="-"):
    p = np.array(pts, float); ax.plot(p[:, 0], p[:, 1], color=c, lw=lw, ls=ls, zorder=2, solid_capstyle="butt")


def arr(ax, pts, c=INK, lw=1.3):
    if len(pts) > 2: line(ax, pts[:-1], c, lw)
    ax.annotate("", xy=pts[-1], xytext=pts[-2], arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, shrinkA=0, shrinkB=0), zorder=2)


def dot(ax, x, y): ax.plot(x, y, "o", color=INK, ms=3.2, zorder=5)


def txt(ax, x, y, s, fs=8, **kw):
    kw.setdefault("ha", "center"); kw.setdefault("va", "center"); ax.text(x, y, s, fontsize=fs, **kw)


def sj(ax, x, y, r=0.24, top=None, left="+", bottom="-", right=None):
    ax.add_patch(mp.Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=3))
    d = r * 0.7071
    ax.plot([x - d, x + d], [y - d, y + d], color=INK, lw=1, zorder=4); ax.plot([x - d, x + d], [y + d, y - d], color=INK, lw=1, zorder=4)
    for s, dx, dy in ((top, 0.18, 0.5), (left, -0.48, 0.2), (bottom, 0.2, -0.5), (right, 0.5, 0.2)):
        if s: ax.text(x + dx, y + dy, "+" if s == "+" else "\u2212", fontsize=8, ha="center", va="center", color=RED)


def nyq_a(ax):
    w = np.logspace(-3, 3, 2000); s = 1j * w; g = (s + 5) / ((s - 2) * (s + 2))
    ax.plot(g.real, g.imag, color=ACC, lw=1.8); ax.plot(g.real, -g.imag, color=ACC, lw=1.4, ls="--")
    for ww in (0.7, 3.0):
        gg = (1j * ww + 5) / ((1j * ww - 2) * (1j * ww + 2))
        ax.annotate("", xy=(gg.real - 0.01, gg.imag + 0.002 * 0), xytext=(gg.real + 0.04, gg.imag - 0.05), arrowprops=dict(arrowstyle="-|>", color=ACC)) if False else None
    ax.annotate("", xy=(-0.6, -0.285), xytext=(-0.8, -0.25), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.4))
    ax.annotate("", xy=(-0.8, 0.25), xytext=(-0.6, 0.285), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.4))
    ax.plot(-1, 0, "x", color=RED, ms=9, mew=2); ax.text(-1.0, 0.11, "-1", color=RED, ha="center", fontsize=9)
    ax.plot(-1.25, 0, "o", color=INK, ms=4); ax.text(-1.25, -0.12, "-1.25", ha="center", fontsize=8)
    ax.plot(0, 0, "o", color=INK, ms=3); ax.axhline(0, color="#aab0ba", lw=0.8); ax.axvline(0, color="#aab0ba", lw=0.8)
    ax.set_xlim(-1.6, 0.4); ax.set_ylim(-0.6, 0.6); ax.set_xlabel("Re G(j\u03c9)H(j\u03c9)"); ax.set_ylabel("Im G(j\u03c9)H(j\u03c9)"); ax.grid(True)
    ax.text(-0.55, -0.43, "\u03c9: 0 \u2192 \u221e (solid)", fontsize=7.5, color=ACC); ax.text(-0.55, 0.40, "\u03c9: \u2212\u221e \u2192 0 (dashed)", fontsize=7.5, color=ACC)


def bode_pm(G, Gc, wmin, wmax, labels=("G(s)", "Gc(s)G(s)")):
    w = np.logspace(np.log10(wmin), np.log10(wmax), 3000)
    fig, (a, b) = plt.subplots(2, 1, figsize=(6.0, 4.4), sharex=True)
    out = []
    for f, lab, col in ((G, labels[0], MUT), (lambda ww: G(ww) * Gc(ww), labels[1], ACC)):
        v = f(w); m = 20 * np.log10(abs(v)); p = np.degrees(np.unwrap(np.angle(v)))
        i = np.argmin(abs(m)); pm = 180 + p[i]; out.append((w[i], pm))
        a.semilogx(w, m, color=col, lw=1.6, label=lab); b.semilogx(w, p, color=col, lw=1.6)
        b.plot([w[i]], [p[i]], "o", color=col, ms=4); b.text(w[i] * 1.1, p[i] - 9, "PM = %.1f\u00b0" % pm, color=col, fontsize=8)
    a.axhline(0, color="#aab0ba", lw=0.8); b.axhline(-180, color="#aab0ba", lw=0.8)
    a.set_ylabel("|G| (dB)"); b.set_ylabel("phase (deg)"); b.set_xlabel("\u03c9 (rad/s)"); a.legend(); a.grid(True, which="both"); b.grid(True, which="both")
    fig.tight_layout(); return out
