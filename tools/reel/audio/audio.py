#!/usr/bin/env python3
"""Score and sound design for the NEBians v1.7 reel, synthesized from scratch with numpy/scipy.

    python tools/reel/audio/audio.py --cues tools/reel/out/cues.json --out tools/reel/out/audio.wav

120 BPM in D major (Bm, G, D, A): a ticking intro, a drop on the logo at 2.0 s, a break into the
"v1.7" slam at 8.0 s, the feature run, and a IV-V-I ending under the logo. Sound effects come from
the cue sheet the stage exports, so every whoosh, pop and tick sits on the motion that made it.
Loudness is normalised to -14 LUFS with a -1 dBTP ceiling by ffmpeg's two-pass loudnorm.
"""
import argparse, json, os, subprocess, tempfile

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
BEAT = 0.5
DUR = 32.0
N = int(DUR * SR) + SR
rng = np.random.default_rng(1707)


def secs(d):
    return int(round(d * SR))


def tt(n):
    return np.arange(n) / SR


def noise(d):
    return rng.uniform(-1, 1, secs(d))


def flt(x, kind, f, order=2):
    nyq = SR / 2
    if kind == "bp":
        b, a = signal.butter(order, [max(20, f[0]) / nyq, min(f[1], nyq * 0.95) / nyq], "band")
    else:
        b, a = signal.butter(order, min(f, nyq * 0.95) / nyq, kind)
    return signal.lfilter(b, a, x)


def sweep_lp(x, f0, f1, curve=1.0):
    """Lowpass whose cutoff glides from f0 to f1 (processed in 256-sample blocks)."""
    out = np.zeros_like(x)
    zi = None
    blocks = range(0, len(x), 256)
    nb = max(1, len(blocks) - 1)
    for k, s in enumerate(blocks):
        p = (k / nb) ** curve
        f = f0 * (f1 / f0) ** p
        b, a = signal.butter(2, min(f, SR * 0.45) / (SR / 2), "low")
        if zi is None:
            zi = signal.lfilter_zi(b, a) * 0
        out[s:s + 256], zi = signal.lfilter(b, a, x[s:s + 256], zi=zi)
    return out


def saw(f, d, phase=None):
    """Band-limited enough saw: 4x oversampled naive saw, then decimated."""
    n4 = secs(d) * 4
    ph = (np.arange(n4) * f / (SR * 4) + (rng.random() if phase is None else phase)) % 1.0
    return signal.resample_poly(2 * ph - 1, 1, 4)


def env(n, a=0.005, d=0.2, s=0.0, r=0.05, hold=None):
    e = np.ones(n)
    na = max(1, secs(a))
    e[:na] = np.linspace(0, 1, na)
    if hold is None:
        e[na:] = s + (1 - s) * np.exp(-np.arange(n - na) / SR / max(d, 1e-4))
    else:
        nh = secs(hold)
        e[na:nh] = s + (1 - s) * np.exp(-np.arange(max(0, nh - na)) / SR / max(d, 1e-4))
        if nh < n:
            last = e[nh - 1] if nh > 0 else 1
            e[nh:] = last * np.exp(-np.arange(n - nh) / SR / max(r, 1e-4))
    return e


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pan(x, p):
    p = np.clip(p, -1, 1)
    return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)])


def put(bus, x, t, g=1.0):
    s = secs(t)
    if s >= bus.shape[-1] or s < -x.shape[-1]:
        return
    if x.ndim == 1:
        x = np.stack([x, x])
    a = max(0, s)
    x = x[:, a - s:]
    m = min(x.shape[1], bus.shape[1] - a)
    bus[:, a:a + m] += g * x[:, :m]


def pluck(f, d, decay=0.996, bright=6000):
    """Karplus-Strong, computed one period-block at a time."""
    n = secs(d)
    p = max(2, int(round(SR / f)))
    y = np.zeros(n + p + 1)
    y[:p + 1] = flt(rng.uniform(-1, 1, p + 1), "low", bright)
    i = p + 1
    while i < n + p + 1:
        j = min(i + p, n + p + 1)
        y[i:j] = decay * 0.5 * (y[i - p:j - p] + y[i - p - 1:j - p - 1])
        i = j
    return y[p + 1:]


def reverb_ir(d=2.4, tone=0.55):
    n = secs(d)
    t = tt(n)
    ir = np.zeros((2, n))
    for c in range(2):
        x = rng.standard_normal(n) * np.exp(-t / (d / 6.9))
        x = sweep_lp(x, 9000, 1200 * tone + 300, 0.7)
        x[:secs(0.012)] *= np.linspace(0, 1, secs(0.012))
        ir[c] = x
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True)) * 0.9


def convolve(x, ir):
    return np.stack([signal.fftconvolve(x[0], ir[0])[:x.shape[1]], signal.fftconvolve(x[1], ir[1])[:x.shape[1]]])


# ------------------------------------------------------------------ drums
def kick(g=1.0, sub=46):
    n = secs(0.5)
    t = tt(n)
    f = sub + 120 * np.exp(-t / 0.032)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.3)
    click = flt(noise(0.008), "high", 2500) * np.exp(-tt(secs(0.008)) / 0.0018)
    body[:len(click)] += 0.4 * click
    return np.tanh(1.8 * body) * g


def clap(g=1.0):
    n = secs(0.4)
    out = np.zeros(n)
    for dl in (0.0, 0.010, 0.021):
        s, m = secs(dl), secs(0.012)
        out[s:s + m] += flt(noise(0.012), "bp", (900, 3200)) * np.exp(-tt(m) / 0.004)
    tail = flt(noise(0.4), "bp", (800, 2800)) * np.exp(-tt(n) / 0.11)
    s = secs(0.021)
    out[s:] += 0.7 * tail[:n - s]
    return out * g * 1.3


def hat(open_=False, g=1.0):
    d = 0.25 if open_ else 0.06
    x = flt(noise(d), "high", 7500, 3) * np.exp(-tt(secs(d)) / (0.075 if open_ else 0.013))
    return x * g * 0.5


def crash(g=1.0):
    d = 2.2
    x = flt(noise(d), "high", 4500, 2) * np.exp(-tt(secs(d)) / 0.6)
    x += 0.3 * flt(noise(d), "bp", (3000, 9000)) * np.exp(-tt(secs(d)) / 0.25)
    return x * g * 0.35


# ------------------------------------------------------------------ harmony
CHORDS = {"Bm": [59, 62, 66], "G": [55, 59, 62], "D": [62, 66, 69], "A": [57, 61, 64]}
ROOT = {"Bm": 35, "G": 31, "D": 38, "A": 33}
# Sections (seconds): intro, logo groove, break, "v1.7" drop and the feature run, break, ending, tail.
INTRO, DROP1, BREAK1, DROP2, BREAK2, ENDING, TAIL = 0.0, 2.0, 3.5, 4.0, 26.0, 26.5, 30.5
_RUN = ["Bm", "G", "D", "A"]
TIMELINE = ([(0, 2, "Bm"), (2, 3.5, "G"), (3.5, 4, "A")] +
            [(4 + 2 * k, 6 + 2 * k, _RUN[k % 4]) for k in range(11)] +
            [(26, 26.5, "A"), (26.5, 28.5, "G"), (28.5, 30.5, "A"), (30.5, 32, "D")])


def chord_at(t):
    for a, b, c in TIMELINE:
        if a <= t < b:
            return c
    return "D"


def supersaw(notes, d, voices=5, spread=0.11, cutoff=2400, a=0.004, dec=0.2, s=0.0, hold=None, r=0.1):
    n = secs(d)
    L = np.zeros(n)
    R = np.zeros(n)
    for m in notes:
        for v in range(voices):
            det = (v - (voices - 1) / 2) / ((voices - 1) / 2) * spread
            x = saw(midi(m + det), d)[:n]
            p = (v / (voices - 1)) * 1.6 - 0.8
            L += x * np.cos((p + 1) * np.pi / 4)
            R += x * np.sin((p + 1) * np.pi / 4)
    e = env(n, a, dec, s, r, hold)
    out = np.stack([flt(L, "low", cutoff), flt(R, "low", cutoff)]) * e
    return out / (len(notes) * voices) * 2.2


def bassnote(m, d, g=1.0):
    n = secs(d)
    f = midi(m)
    x = 0.55 * saw(f, d)[:n] + 0.45 * np.sin(2 * np.pi * f * tt(n))
    e = env(n, 0.003, 0.16, 0.35, 0.03, hold=d * 0.85)
    x = flt(x * e, "low", 520)
    sub = np.sin(2 * np.pi * f * tt(n)) * e
    return np.tanh(1.4 * (x * 0.8 + sub * 0.6)) * g


# ------------------------------------------------------------------ the score
def score():
    drums = np.zeros((2, N))
    music = np.zeros((2, N))
    send = np.zeros((2, N))
    kicks = []
    steps = int(DUR / 0.125)
    for st in range(steps):
        t = st * 0.125
        beat, sixteenth = divmod(st, 4)
        sec = ("intro" if t < DROP1 else "A" if t < BREAK1 else "break" if t < DROP2 else "B" if t < BREAK2 else
               "break2" if t < ENDING else "end" if t < TAIL else "tail")
        c = chord_at(t)
        if sec == "intro":
            if sixteenth in (0, 2):
                put(drums, pan(hat(False, 0.35 + 0.4 * t / 2), 0.25), t)
        if sec in ("A", "B", "end"):
            if sixteenth == 0:
                put(drums, kick(1.0), t)
                kicks.append(t)
            if sixteenth == 2:
                put(drums, pan(hat(True, 0.75), 0.15), t)
            if sec != "A" or t >= 2.5:
                if sixteenth in (1, 3):
                    put(drums, pan(hat(False, 0.35), -0.3), t)
            if beat % 2 == 1 and sixteenth == 0:
                cl = clap(0.85)
                put(drums, cl, t)
                put(send, np.stack([cl, cl]) * 0.25, t)
        if sec == "break":
            k = (t - BREAK1) / (DROP2 - BREAK1)
            put(drums, clap(0.25 + 0.6 * k), t)
            put(drums, clap(0.2 + 0.5 * k), t + 0.0625)
        if sec == "tail" and st % 8 == 0 and t < 31:
            put(drums, kick(0.6), t)
            kicks.append(t)
        # bass: eighths, octave on the offbeat 16th of beats 2 and 4
        if sec in ("A", "B", "end") and sixteenth in (0, 2):
            m = ROOT[c] + (12 if (sixteenth == 2 and beat % 2 == 1) else 0)
            put(music, bassnote(m + 12, 0.24, 0.75), t)
        # stabs on the "and"
        if sec in ("A", "B", "end") and sixteenth == 2:
            put(music, supersaw(CHORDS[c], 0.3, cutoff=2600 if sec == "B" else 1800, dec=0.12) * 0.75, t)
            put(send, supersaw(CHORDS[c], 0.3, cutoff=2000, dec=0.1) * 0.25, t)
        # arp: sixteenths up and down the chord, an octave up
        if sec in ("B", "end"):
            notes = CHORDS[c] + [CHORDS[c][0] + 12]
            seq = [0, 1, 2, 3, 2, 1, 2, 3]
            m = notes[seq[st % 8]] + 12
            x = pluck(midi(m), 0.32, 0.993, 5200) * 0.42
            p = 0.45 if st % 2 else -0.45
            put(music, pan(x, p), t)
            put(send, pan(x, -p) * 0.5, t + 0.375)
    # pads: per chord span
    for a, b, c in TIMELINE:
        lvl = 0.55 if a < 2 else 0.28 if a < 26.5 else 0.6
        cutoff = 900 if a < 2 else 1500 if a < 26.5 else 2600
        x = supersaw([m - 12 for m in CHORDS[c]] + [CHORDS[c][0]], b - a + 0.6, cutoff=cutoff, a=0.25 if a < 2 else 0.04,
                     dec=4, s=0.85, hold=b - a, r=0.35, spread=0.16) * lvl
        put(music, x, a)
        put(send, x * 0.6, a)
    # intro: sub drone and a filter opening under the clock
    n = secs(2.0)
    drone = np.sin(2 * np.pi * midi(23) * tt(n)) * np.linspace(0.0, 0.5, n)
    put(music, drone, 0)
    # final chord bloom
    put(music, supersaw(CHORDS["D"] + [74, 78], 3.0, cutoff=3200, a=0.01, dec=1.4, s=0.0) * 0.9, 30.5)
    put(send, supersaw(CHORDS["D"] + [74, 78], 3.0, cutoff=3200, a=0.01, dec=1.4, s=0.0) * 0.6, 30.5)
    put(music, bassnote(26, 1.5, 0.9), 30.5)
    for t in (26.5,):
        put(drums, crash(1.0), t)
        put(drums, kick(1.2, 40), t)
        kicks.append(t)
    put(drums, crash(0.7), DROP2)
    put(drums, crash(0.6), DROP1)
    return drums, music, send, kicks


def sidechain(kicks, depth=0.62, rel=0.16):
    g = np.ones(N)
    t = tt(N)
    for k in kicks:
        s = secs(k)
        m = min(N - s, secs(0.5))
        seg = 1 - depth * np.exp(-t[:m] / rel)
        seg[:secs(0.006)] = np.linspace(1, seg[secs(0.006)], secs(0.006))
        g[s:s + m] = np.minimum(g[s:s + m], seg)
    return g


# ------------------------------------------------------------------ sound effects
def fx_whoosh(o):
    d = o.get("dur", 0.4) + 0.25
    n = secs(d)
    x = noise(d)
    lo, hi = 250, 3600
    e = np.sin(np.pi * np.clip(tt(n) / d, 0, 1)) ** 1.6
    out = np.zeros(n)
    for k, s in enumerate(range(0, n, 512)):
        p = s / n
        fc = lo * (hi / lo) ** np.sin(np.pi * p)
        b, a = signal.butter(2, [fc * 0.6 / (SR / 2), min(fc * 1.6, SR * 0.45) / (SR / 2)], "band")
        out[s:s + 512] = signal.lfilter(b, a, x[s:s + 512])
    out *= e * 2.2
    ps = np.linspace(-0.7, 0.7, n)
    return np.stack([out * np.cos((ps + 1) * np.pi / 4), out * np.sin((ps + 1) * np.pi / 4)])


def fx_swish(o):
    o = dict(o)
    o["dur"] = 0.22
    x = fx_whoosh(o)
    return np.stack([flt(x[0], "high", 900), flt(x[1], "high", 900)]) * 0.9


def fx_riser(o):
    d = o.get("dur", 0.5)
    n = secs(d)
    t = tt(n)
    p = t / d
    f = 180 * (2400 / 180) ** (p ** 1.4)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 + saw(300, d)[:n] * 0.0
    nz = sweep_lp(noise(d), 400, 9000, 1.2) * 0.8
    x = (tone + nz) * (p ** 1.8)
    return np.stack([x, np.roll(x, 90)])


def fx_impact(o):
    n = secs(0.9)
    t = tt(n)
    f = 38 + 70 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.32)
    hitn = flt(noise(0.9), "low", 1800) * np.exp(-t / 0.06) * 0.6
    return np.tanh(2.2 * (body + hitn)) * 0.9


def fx_boom(o):
    n = secs(2.2)
    t = tt(n)
    f = 30 + 85 * np.exp(-t / 0.07)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.75)
    mid = flt(noise(2.2), "bp", (120, 900)) * np.exp(-t / 0.18) * 0.9
    metal = sum(np.sin(2 * np.pi * fr * t) * np.exp(-t / dc) for fr, dc in ((311, 0.5), (523, 0.35), (787, 0.25))) * 0.08
    x = np.tanh(1.8 * (sub + mid)) + metal
    return np.stack([x, np.roll(x, 240) * 0.96])


def fx_tick(o):
    n = secs(0.05)
    f = 2400 * o.get("pitch", 1)
    x = np.sin(2 * np.pi * f * tt(n)) * np.exp(-tt(n) / 0.008)
    x += flt(noise(0.05), "high", 5000) * np.exp(-tt(n) / 0.002) * 0.5
    return x * 0.5


def fx_click(o):
    return fx_tick({**o, "pitch": 0.55 * o.get("pitch", 1)}) * 0.9


def fx_flip(o):
    n = secs(0.07)
    x = flt(noise(0.07), "bp", (1200, 5200)) * np.exp(-tt(n) / 0.01)
    x[secs(0.018):] += flt(noise(0.07 - 0.018), "bp", (900, 3000)) * np.exp(-tt(n - secs(0.018)) / 0.008) * 0.6
    return x * 0.8


def fx_pop(o):
    n = secs(0.12)
    t = tt(n)
    k = o.get("pitch", 1)
    f = (300 + 650 * np.exp(-t / 0.018)) * k
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
    return x * 0.7


def fx_coin(o):
    out = []
    for f, d in ((988, 0.07), (1319, 0.32)):
        n = secs(d)
        sq = np.sign(np.sin(2 * np.pi * f * tt(n))) * 0.5 + np.sin(2 * np.pi * f * tt(n)) * 0.5
        out.append(flt(sq, "low", 6000) * (np.exp(-tt(n) / 0.12) if d > 0.1 else 1.0))
    return np.concatenate(out) * 0.22


def bell(f, d=1.4, bright=1.0):
    n = secs(d)
    t = tt(n)
    mod = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * bright * np.exp(-t / 0.3)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t / (d / 3.5))


def fx_chime(o):
    x = np.zeros(secs(1.8))
    for k, m in enumerate((74, 81, 86)):
        b = bell(midi(m), 1.6) * 0.3
        s = secs(k * 0.06)
        x[s:s + len(b)] += b[:len(x) - s]
    return np.stack([x, np.roll(x, 300)])


def fx_ding(o):
    return bell(midi(81) * o.get("pitch", 1), 1.0) * 0.35


def fx_counter(o):
    d = o.get("dur", 0.85)
    x = np.zeros(secs(d + 0.1))
    k, t = 0, 0.0
    while t < d:
        b = fx_tick({"pitch": 1.4 + 0.3 * (t / d)}) * 0.55
        s = secs(t)
        x[s:s + len(b)] += b[:len(x) - s]
        k += 1
        t = d * (1 - (1 - k / 26) ** 0.35) if k < 26 else d + 1
    return x


def fx_glitch(o):
    x = np.zeros(secs(0.18))
    for k in range(6):
        s, m = secs(k * 0.028), secs(0.018)
        seg = np.round(noise(0.018) * 3) / 3 * (0.8 if k % 2 else 0.4)
        x[s:s + m] += flt(seg, "bp", (600 + 400 * k, 6000))
    return x * 0.6


def fx_tap(o):
    n = secs(0.04)
    return flt(noise(0.04), "low", 2200) * np.exp(-tt(n) / 0.006) * 0.9


def fx_shimmer(o):
    d = o.get("dur", 0.5)
    x = np.zeros(secs(d + 0.6))
    for k in range(9):
        f = midi([86, 88, 90, 93, 95, 98][k % 6])
        b = bell(f, 0.5, 0.4) * 0.08
        s = secs(k * d / 9)
        x[s:s + len(b)] += b[:len(x) - s]
    return np.stack([x, np.roll(x, 220)])


def fx_flipcard(o):
    n = secs(0.06)
    return flt(noise(0.06), "bp", (1800 * o.get("pitch", 1), 6000)) * np.exp(-tt(n) / 0.012) * 0.7


def fx_hum(o):
    d = o.get("dur", 2.5)
    n = secs(d)
    t = tt(n)
    x = (np.sin(2 * np.pi * 73.4 * t) + 0.4 * np.sin(2 * np.pi * 146.8 * t) + 0.15 * np.sin(2 * np.pi * 220.2 * t))
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)) * env(n, 0.3, 4, 1, 0.4, hold=d - 0.4)
    return flt(x, "low", 900) * 0.18


def fx_type(o):
    n = secs(0.035)
    f = rng.uniform(1600, 2600)
    x = flt(noise(0.035), "bp", (f * 0.7, f * 1.4)) * np.exp(-tt(n) / 0.006)
    return x * 0.8


def fx_send(o):
    n = secs(0.16)
    t = tt(n)
    f = 420 * (1400 / 420) ** (t / 0.16)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.16) * 0.4


def fx_bubble(o):
    n = secs(0.09)
    t = tt(n)
    f = (600 + 900 * (t / 0.09) ** 0.6) * o.get("pitch", 1)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03) * 0.45


def fx_stream(o):
    return fx_tick({"pitch": rng.uniform(1.6, 2.1)}) * 0.6


def fx_sparkle(o):
    x = np.zeros(secs(0.9))
    for k in range(7):
        f = rng.uniform(2600, 6200)
        b = np.sin(2 * np.pi * f * tt(secs(0.35))) * np.exp(-tt(secs(0.35)) / 0.06) * 0.12
        s = secs(k * 0.045 + rng.uniform(0, 0.02))
        x[s:s + len(b)] += b[:len(x) - s]
    return np.stack([x, np.roll(x, 400)])


def fx_toggle(o):
    a = fx_tap(o)
    x = np.zeros(secs(0.09))
    x[:len(a)] += a
    x[secs(0.045):secs(0.045) + len(a)] += a * 0.7
    return x


def fx_ploink(o):
    return pluck(660, 0.45, 0.995, 3000) * 0.55


def fx_ping(o):
    n = secs(0.25)
    return np.sin(2 * np.pi * 1760 * o.get("pitch", 1) * tt(n)) * np.exp(-tt(n) / 0.05) * 0.28


def fx_pageflip(o):
    n = secs(0.32)
    t = tt(n)
    x = flt(noise(0.32), "bp", (700, 5000)) * np.sin(np.pi * t / 0.32) ** 2
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * 38 * t)
    return x * 0.6


def fx_draw(o):
    n = secs(0.3)
    return flt(noise(0.3), "bp", (2500, 7000)) * np.sin(np.pi * tt(n) / 0.3) * 0.25


def fx_card(o):
    w = fx_swish(o)
    th = fx_impact(o)[:secs(0.25)] * 0.35
    x = np.zeros((2, w.shape[1] + secs(0.1)))
    x[:, :w.shape[1]] += w * 0.7
    s = secs(0.12)
    x[:, s:s + len(th)] += np.stack([th, th])[:, :x.shape[1] - s]
    return x


def fx_like(o):
    return fx_pop({"pitch": 1.6 * o.get("pitch", 1)}) * 0.8


PENTA = [74, 76, 78, 81, 83, 86, 88, 90, 93, 95, 98, 100]


def fx_chip(o):
    m = PENTA[o.get("note", 0) % len(PENTA)]
    return pluck(midi(m), 0.5, 0.995, 7000) * 0.45


def fx_zoom(o):
    d = o.get("dur", 0.4)
    w = fx_whoosh({"dur": d})
    n = secs(d)
    t = tt(n)
    f = 200 * (1200 / 200) ** (t / d)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 2 * 0.22
    w[:, :n] += np.stack([tone, tone])
    return w


FX = {k[3:]: v for k, v in globals().items() if k.startswith("fx_")}
FX_GAIN = {"whoosh": 0.55, "swish": 0.5, "riser": 0.55, "impact": 0.9, "boom": 1.0, "tick": 0.55, "click": 0.6,
           "flip": 0.6, "pop": 0.55, "coin": 0.55, "chime": 0.6, "ding": 0.6, "counter": 0.45, "glitch": 0.45,
           "tap": 0.5, "shimmer": 0.6, "flipcard": 0.5, "hum": 0.5, "type": 0.45, "send": 0.5, "bubble": 0.55,
           "stream": 0.35, "sparkle": 0.6, "toggle": 0.6, "ploink": 0.6, "ping": 0.55, "pageflip": 0.6,
           "draw": 0.5, "card": 0.6, "like": 0.5, "chip": 0.45, "zoom": 0.6}
FX_SEND = {"chime": 0.5, "ding": 0.4, "coin": 0.25, "shimmer": 0.5, "sparkle": 0.45, "boom": 0.25, "ploink": 0.3,
           "chip": 0.3, "ping": 0.35, "pop": 0.15, "bubble": 0.2}


def sfx(cues):
    bus = np.zeros((2, N))
    send = np.zeros((2, N))
    missing = set()
    for c in cues:
        f = FX.get(c["type"])
        if f is None:
            missing.add(c["type"])
            continue
        x = f(c)
        if x.ndim == 1:
            x = pan(x, c.get("pan", 0.0))
        g = FX_GAIN.get(c["type"], 0.5) * c.get("gain", 1.0)
        put(bus, x, c["t"], g)
        if c["type"] in FX_SEND:
            put(send, x, c["t"], g * FX_SEND[c["type"]])
    if missing:
        print("no synth for:", sorted(missing))
    return bus, send


def master(path_wav, out_wav):
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path_wav, "-af",
                           "loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    af = ("loudnorm=I=-14:TP=-1.0:LRA=9:linear=true:"
          f"measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path_wav, "-af", af, "-ar", str(SR),
                    "-c:a", "pcm_s24le", out_wav], check=True)
    return js


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cues = json.load(open(a.cues))["cues"]
    drums, music, msend, kicks = score()
    music *= sidechain(kicks)
    fx, fsend = sfx(cues)
    ir = reverb_ir(2.4)
    wet = convolve(msend + fsend, ir)
    mix = drums * 0.62 + music * 0.5 + wet * 0.32 + fx * 0.95
    mix = np.stack([flt(mix[0], "high", 28), flt(mix[1], "high", 28)])
    fade = np.ones(N)
    s, e = secs(30.9), secs(DUR)
    fade[s:e] = np.linspace(1, 0, e - s) ** 1.5
    fade[e:] = 0
    mix = mix * fade
    mix = mix[:, :secs(DUR)]
    mix = np.tanh(mix / max(1e-9, np.abs(mix).max()) * 1.25) * 0.89
    with tempfile.TemporaryDirectory() as d:
        raw = os.path.join(d, "raw.wav")
        wavfile.write(raw, SR, (mix.T * 32767).astype(np.int16))
        js = master(raw, a.out)
    print(f"audio -> {a.out}  (input {js['input_i']} LUFS, normalised to -14 LUFS / -1 dBTP)")


if __name__ == "__main__":
    main()
