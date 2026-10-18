"""Synthesised score and sound design for the Neby film. Same cue list as the picture."""
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

import film

SR = 48000
N = int(SR * film.DURATION)
rng = np.random.default_rng(11)
BEAT = 60.0 / film.BPM


def t_axis(d):
    return np.arange(int(SR * d)) / SR


def env(d, a=0.003, decay=6.0):
    t = t_axis(d)
    e = np.exp(-t * decay)
    na = max(1, int(SR * a))
    e[:na] *= np.linspace(0, 1, na)
    return e


def filt(x, kind, f):
    sos = butter(2, f, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x)


def bandsweep(x, f0, f1, steps=24):
    out = np.zeros_like(x)
    n = len(x)
    edges = np.linspace(0, n, steps + 1).astype(int)
    win = np.hanning(2 * (edges[1] - edges[0]) + 2)
    for i in range(steps):
        f = f0 * (f1 / f0) ** (i / (steps - 1))
        a, b = edges[i], edges[i + 1]
        lo, hi = max(0, a - (b - a) // 2), min(n, b + (b - a) // 2)
        seg = filt(x[lo:hi], "bandpass", [max(40, f * 0.6), min(SR / 2 - 100, f * 1.6)])
        w = np.hanning(hi - lo)
        out[lo:hi] += seg * w
    return out


def sine(f, d, phase=0.0):
    t = t_axis(d)
    if callable(f):
        ph = 2 * np.pi * np.cumsum(f(t)) / SR
    else:
        ph = 2 * np.pi * f * t
    return np.sin(ph + phase)


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


class Mix:
    def __init__(self):
        self.L = np.zeros(N)
        self.R = np.zeros(N)

    def add(self, x, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N or i + len(x) <= 0:
            return
        x = x[: N - i] * gain
        l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        self.L[i:i + len(x)] += x * l * 1.41
        self.R[i:i + len(x)] += x * r * 1.41


# ------------------------------------------------------------- instruments

def kick(d=0.45):
    f = lambda t: 48 + 120 * np.exp(-t * 38)
    return sine(f, d) * env(d, 0.001, 9)


def kick_full():
    x = kick()
    click = filt(rng.standard_normal(int(SR * 0.008)), "highpass", 2500) * 0.35
    x[: len(click)] += click
    return x


def hat(d=0.06, open_=False):
    n = rng.standard_normal(int(SR * d))
    return filt(n, "highpass", 7500) * env(d, 0.001, 70 if not open_ else 25)


def snap():
    d = 0.18
    n = filt(rng.standard_normal(int(SR * d)), "bandpass", [1200, 5200])
    e = env(d, 0.001, 30)
    e2 = np.zeros_like(e)
    for k in (0.0, 0.008, 0.016):
        i = int(k * SR)
        e2[i:] += np.exp(-np.arange(len(e) - i) / SR * 90) * 0.6
    return n * (e + e2) * 0.6


def marimba(m, d=0.5):
    f = note(m)
    x = sine(f, d) + 0.35 * sine(f * 4.0, d) * env(d, 0.001, 30) + 0.12 * sine(f * 9.2, d) * env(d, 0.001, 60)
    return x * env(d, 0.002, 7)


def bass(m, d=0.45):
    f = note(m)
    x = sine(f, d) + 0.3 * sine(2 * f, d) + 0.12 * np.sign(sine(f, d)) * 0.4
    return filt(x, "lowpass", 900) * env(d, 0.004, 5)


def pad(ms, d, attack=0.6):
    t = t_axis(d)
    x = np.zeros(len(t))
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            f = note(m + det)
            x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) + 0.25 * np.sin(4 * np.pi * f * t)
    x = filt(x, "lowpass", 2600) / (len(ms) * 3)
    e = np.minimum(1, t / attack) * np.minimum(1, (d - t) / 0.8)
    return x * np.clip(e, 0, 1)


def bell(m, d=1.2):
    f = note(m)
    x = sine(f, d) + 0.5 * sine(f * 2.76, d) * env(d, 0.001, 9) + 0.25 * sine(f * 5.4, d) * env(d, 0.001, 16)
    return x * env(d, 0.001, 3.2)


# ------------------------------------------------------------- sound effects

def sfx(kind):
    if kind in ("whoosh_down", "whoosh_up", "swish", "page"):
        d = {"whoosh_down": 0.62, "whoosh_up": 0.45, "swish": 0.28, "page": 0.4}[kind]
        n = rng.standard_normal(int(SR * d))
        f0, f1 = {"whoosh_down": (3500, 400), "whoosh_up": (500, 5000), "swish": (900, 4500), "page": (2500, 900)}[kind]
        x = bandsweep(n, f0, f1)
        t = t_axis(d)
        e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
        return x * e * {"whoosh_down": 0.9, "whoosh_up": 0.7, "swish": 0.55, "page": 0.5}[kind]
    if kind in ("thud", "land"):
        d = 0.5
        x = sine(lambda t: 55 + 90 * np.exp(-t * 25), d) * env(d, 0.001, 8)
        x += filt(rng.standard_normal(int(SR * d)), "lowpass", 500) * env(d, 0.001, 30) * 0.5
        return x * (1.0 if kind == "thud" else 0.6)
    if kind == "boing":
        d = 0.7
        f = lambda t: 220 * (1 + 0.5 * np.exp(-t * 3) * np.sin(2 * np.pi * 9 * t)) * (1 + 0.6 * np.exp(-t * 8))
        return sine(f, d) * env(d, 0.005, 4.5) * 0.45
    if kind in ("pop", "bubble"):
        d = 0.16
        f0 = 900 if kind == "pop" else 600
        x = sine(lambda t: f0 * np.exp(-t * 14) + 280, d) * env(d, 0.001, 22)
        return x * (0.6 if kind == "pop" else 0.7)
    if kind in ("tock", "facet"):
        d = 0.18
        f = 1250 if kind == "tock" else 2200
        x = sine(f, d) * env(d, 0.001, 45) + 0.4 * sine(f * 2.3, d) * env(d, 0.001, 70)
        return x * (0.5 if kind == "tock" else 0.35)
    if kind == "type":
        d = 0.6
        x = np.zeros(int(SR * d))
        for i in range(7):
            c = hat(0.03) * 0.8
            j = int(i * 0.075 * SR)
            x[j:j + len(c)] += c
        return x * 0.5
    if kind == "count":
        d = 1.25
        x = np.zeros(int(SR * d))
        i, k = 0.0, 0
        while i < d - 0.05:
            b = sine(2400 + 40 * k, 0.03) * env(0.03, 0.001, 120) * 0.3
            j = int(i * SR)
            x[j:j + len(b)] += b
            i += 0.03 + 0.07 * (i / d) ** 2
            k += 1
        return x
    if kind == "hop":
        d = 0.32
        return sine(lambda t: 300 + 1300 * t / d, d) * env(d, 0.004, 8) * 0.35
    if kind == "cap":
        x = sfx("pop")
        b = bell(91, 0.8) * 0.25
        out = np.zeros(max(len(x), len(b)))
        out[:len(x)] += x
        out[:len(b)] += b
        return out
    if kind in ("sparkle", "wink"):
        notes = [96, 100, 103, 108] if kind == "sparkle" else [91, 98]
        out = np.zeros(int(SR * 1.3))
        for i, m in enumerate(notes):
            b = bell(m, 1.0) * 0.16
            j = int(i * 0.06 * SR)
            out[j:j + len(b)] += b[: len(out) - j]
        return out
    if kind == "word":
        d = 0.3
        x = sine(lambda t: 140 * np.exp(-t * 10) + 70, d) * env(d, 0.001, 14) * 0.55
        x[: int(SR * 0.006)] += filt(rng.standard_normal(int(SR * 0.006)), "highpass", 3000) * 0.3
        return x
    if kind == "tick":
        return bell(98, 0.5) * 0.22
    if kind == "riser":
        d = 0.6
        n = rng.standard_normal(int(SR * d))
        x = bandsweep(n, 400, 9000) * np.linspace(0, 1, len(n)) ** 2 * 0.7
        x += sine(lambda t: 200 + 1400 * (t / d) ** 2, d) * np.linspace(0, 1, len(n)) ** 2 * 0.15
        return x
    if kind == "boom":
        d = 2.2
        x = sine(lambda t: 38 + 60 * np.exp(-t * 6), d) * env(d, 0.002, 2.2)
        x += filt(rng.standard_normal(int(SR * d)), "lowpass", 1200) * env(d, 0.001, 5) * 0.6
        return x * 1.1
    return None


# ------------------------------------------------------------- arrangement

def arrange():
    mx = Mix()
    mx.add(pad([60, 64, 67, 71], 2.2, attack=1.2), 0.0, 0.10)
    prog = [(48, [60, 64, 67, 72]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69]), (43, [55, 59, 62, 67])]
    groove_start, groove_end = 2.0, 14.0
    bar = 4 * BEAT
    b = 0
    t = groove_start
    while t < groove_end - 1e-6:
        root, chord = prog[b % 4]
        for beat in range(4):
            tb = t + beat * BEAT
            if tb >= groove_end:
                break
            mx.add(kick_full(), tb, 0.85)
            if beat in (1, 3) and tb >= 5.0:
                mx.add(snap(), tb, 0.45, pan=0.1)
            for h in range(2):
                th = tb + h * BEAT / 2
                if h == 1:
                    mx.add(hat(), th, 0.22, pan=0.35)
            mx.add(bass(root - 12 + (0 if beat % 2 == 0 else 12), BEAT * 0.9), tb, 0.38)
        pattern = [0, 1, 2, 3, 2, 1, 2, 3]
        for s in range(8):
            ts = t + s * BEAT / 2
            if ts < groove_end:
                mx.add(marimba(chord[pattern[s]] + 12, 0.45), ts, 0.16, pan=-0.3 + 0.6 * (s % 2))
        mx.add(pad(chord, bar, attack=0.3), t, 0.05)
        t += bar
        b += 1
    mx.add(pad([48, 55, 60, 64, 67, 71, 74], 3.0, attack=0.05), 15.0, 0.20)
    mx.add(kick_full(), 15.0, 0.9)
    mx.add(bass(36, 2.5), 15.0, 0.4)
    for i, m in enumerate([72, 76, 79, 83, 86, 88]):
        mx.add(bell(m, 1.6), 15.05 + i * BEAT / 2, 0.10, pan=-0.4 + 0.16 * i)
    for tc, kind in film.CUES:
        x = sfx(kind)
        if x is not None:
            mx.add(x, tc, 1.0, pan={"swish": 0.3, "tock": 0.2}.get(kind, 0.0))
    return mx


def write(path):
    mx = arrange()
    st = np.stack([mx.L, mx.R], axis=1)
    fade = int(SR * 0.4)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    peak = np.max(np.abs(st))
    st = st / peak * 0.89
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "score.wav")
