"""Dashain fusion score for the NEBians launch film: madal and bansuri over a modern beat.
Everything is synthesised; every sound effect comes from film.CUES."""
import os
import sys
import wave

import numpy as np

import importlib.util  # noqa: E402

import film  # noqa: E402  (this film; it also puts ../neby on the path for kit/characters)

_spec = importlib.util.spec_from_file_location(
    "neby_score", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "neby", "score.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
SR, bandsweep, bell, env, filt, hat = base.SR, base.bandsweep, base.bell, base.env, base.filt, base.hat
kick_full, note, pad, sine, snap, t_axis = base.kick_full, base.note, base.pad, base.sine, base.snap, base.t_axis

N = int(SR * film.DURATION)
BEAT = 60.0 / film.BPM
rng = np.random.default_rng(23)


class Mix:
    def __init__(self):
        self.L = np.zeros(N)
        self.R = np.zeros(N)

    def add(self, x, t, gain=1.0, pan=0.0):
        if x is None:
            return
        i = int(t * SR)
        if i >= N or i < 0:
            return
        x = x[: N - i] * gain
        l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        self.L[i:i + len(x)] += x * l * 1.41
        self.R[i:i + len(x)] += x * r * 1.41


# ------------------------------------------------------------- Nepali colour

def dhin(gain=1.0):
    d = 0.42
    x = sine(lambda t: 72 + 60 * np.exp(-t * 22), d) * env(d, 0.002, 7)
    x += 0.35 * sine(lambda t: 150 + 40 * np.exp(-t * 30), d) * env(d, 0.002, 14)
    x += filt(rng.standard_normal(int(SR * d)), "lowpass", 900) * env(d, 0.001, 40) * 0.3
    return x * gain


def ta(gain=1.0):
    d = 0.16
    x = sine(lambda t: 330 + 120 * np.exp(-t * 60), d) * env(d, 0.001, 32) * 0.6
    x += filt(rng.standard_normal(int(SR * d)), "bandpass", [1400, 4200]) * env(d, 0.001, 55) * 0.55
    return x * gain


def bansuri(m, d, glide_from=None, vib=1.0):
    """A breathy bamboo flute: sine body, a little 2nd/3rd harmonic, breath noise, delayed vibrato."""
    t = t_axis(d)
    f0 = note(m)
    if glide_from is not None:
        fg = note(glide_from)
        f = f0 + (fg - f0) * np.exp(-t * 28)
    else:
        f = np.full_like(t, f0)
    vibr = 1 + 0.007 * vib * np.sin(2 * np.pi * 5.4 * t) * np.clip((t - 0.18) / 0.25, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vibr) / SR
    x = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = filt(rng.standard_normal(len(t)), "bandpass", [max(200, f0 * 0.8), min(SR / 2 - 200, f0 * 3)]) * 0.10
    a = np.clip(t / 0.05, 0, 1) * np.clip((d - t) / 0.08, 0, 1)
    swell = 0.85 + 0.15 * np.clip(t / max(d, 1e-3), 0, 1)
    return (x + breath) * a * swell


def flute_phrase(mx, t0, notes, gain=0.22, pan=-0.15):
    t = t0
    prev = None
    for m, beats in notes:
        d = beats * BEAT
        if m is not None:
            g = prev + 2 if prev is not None and m < prev else None
            mx.add(bansuri(m, d * 1.04 + 0.05, glide_from=g, vib=1.0 if d > 0.4 else 0.4), t, gain, pan)
            prev = m
        t += d
    # a touch of room: two quiet echoes
    return t


def sub(m, d):
    x = sine(note(m), d) * env(d, 0.01, 2.5)
    return filt(x, "lowpass", 220)


# ------------------------------------------------------------- effects

def sfx(kind):
    if kind == "air":
        d = 2.6
        n = filt(rng.standard_normal(int(SR * d)), "bandpass", [600, 5000])
        return n * np.sin(np.pi * np.clip(t_axis(d) / d, 0, 1)) * 0.12
    if kind == "rise":
        d = 0.8
        return bandsweep(rng.standard_normal(int(SR * d)), 300, 4000) * np.sin(np.pi * t_axis(d) / d) * 0.5
    if kind == "shimmer":
        out = np.zeros(int(SR * 1.6))
        for i, m in enumerate([86, 90, 93, 98, 102]):
            b = bell(m, 1.2) * 0.07
            j = int(i * 0.05 * SR)
            out[j:j + len(b)] += b[: len(out) - j]
        return out
    if kind == "kite":
        d = 0.5
        n = rng.standard_normal(int(SR * d))
        flutter = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 34 * t_axis(d)))
        return bandsweep(n, 4000, 900) * flutter * np.sin(np.pi * t_axis(d) / d) * 0.35
    if kind == "land":
        return dhin(0.55)
    if kind == "chip":
        d = 0.12
        return sine(lambda t: 1200 * np.exp(-t * 10) + 500, d) * env(d, 0.001, 30) * 0.4
    if kind == "write":
        d = 0.7
        n = filt(rng.standard_normal(int(SR * d)), "bandpass", [2500, 7000])
        am = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 9 * t_axis(d)))
        return n * am * np.sin(np.pi * t_axis(d) / d) * 0.18
    if kind == "like":
        return bell(93, 0.4) * 0.16
    if kind == "tap":
        d = 0.1
        return sine(lambda t: 900 * np.exp(-t * 30) + 200, d) * env(d, 0.001, 50) * 0.5
    if kind == "sheet":
        return base.sfx("swish")
    if kind == "whoosh":
        return base.sfx("whoosh_up")
    if kind == "confetti":
        out = np.zeros(int(SR * 1.2))
        for i in range(18):
            b = sine(2000 + 1500 * rng.random(), 0.04) * env(0.04, 0.001, 90) * 0.12
            j = int(rng.random() * 1.0 * SR)
            out[j:j + len(b)] += b
        return out
    if kind == "bells":
        out = np.zeros(int(SR * 1.0))
        for i, m in enumerate([86, 93, 98]):
            b = bell(m, 0.9) * 0.10
            j = int(i * 0.08 * SR)
            out[j:j + len(b)] += b[: len(out) - j]
        return out
    if kind == "type":
        return base.sfx("type")
    if kind in ("word", "pop", "bubble", "tick", "page", "count", "riser", "boom", "facet", "wink"):
        return base.sfx(kind)
    return None


# ------------------------------------------------------------- arrangement

CHORDS = [(3.0, 38, [62, 66, 69, 74]), (5.0, 35, [59, 62, 66, 71]), (7.0, 31, [55, 59, 62, 67]),
          (9.0, 33, [57, 61, 64, 69]), (11.0, 38, [62, 66, 69, 74]), (13.0, 35, [59, 62, 66, 71]),
          (15.0, 31, [55, 59, 62, 67])]


def arrange():
    mx = Mix()
    mx.add(pad([50, 57, 62, 66, 69], 3.2, attack=1.4), 0.0, 0.10)
    flute_phrase(mx, 0.45, [(81, 1), (83, 0.5), (81, 0.5), (78, 1), (76, 0.5), (74, 1.5)], gain=0.20)
    mx.add(dhin(0.5), 1.0)
    mx.add(dhin(0.6), 2.0)
    mx.add(ta(0.5), 2.5)
    mx.add(ta(0.6), 2.75)
    groove_end = 15.5
    madal = [("D", 1.0), ("t", 0.45), ("t", 0.35), ("D", 0.8), ("t", 0.5), ("D", 0.7), ("t", 0.45), ("t", 0.6)]
    t = 3.0
    while t < groove_end - 1e-6:
        beat_in_bar = int(round((t - 3.0) / BEAT)) % 4
        if beat_in_bar in (0, 2):
            mx.add(kick_full(), t, 0.75)
        if beat_in_bar in (1, 3) and t >= 5.0:
            mx.add(snap(), t, 0.40, pan=0.12)
        for e in range(2):
            te = t + e * BEAT / 2
            kind, g = madal[(beat_in_bar * 2 + e) % 8]
            if te < groove_end:
                mx.add(dhin(g * 0.55) if kind == "D" else ta(g * 0.55), te, 1.0, pan=-0.2 if kind == "t" else 0.0)
            for q in range(2):
                tq = te + q * BEAT / 4
                if tq < groove_end and t >= 5.0:
                    mx.add(hat(0.03), tq, 0.10 if q else 0.06, pan=0.4)
        t += BEAT
    for t0, root, chord in CHORDS:
        d = min(2.0, groove_end - t0)
        if d <= 0:
            continue
        mx.add(pad(chord, d, attack=0.25), t0, 0.06)
        for b in range(4):
            tb = t0 + b * BEAT
            if tb < groove_end:
                mx.add(base.bass(root + (12 if b % 2 else 0), BEAT * 0.85), tb, 0.30)
        mx.add(sub(root, d), t0, 0.25)
    flute_phrase(mx, 5.0, [(78, 0.5), (81, 0.5), (83, 1), (81, 0.5), (78, 0.5), (76, 1), (74, 1), (76, 0.5), (78, 0.5), (81, 2)], gain=0.17)
    flute_phrase(mx, 9.0, [(83, 0.5), (86, 0.5), (83, 0.5), (81, 0.5), (78, 1), (81, 1), (83, 1), (81, 1), (78, 2)], gain=0.16)
    flute_phrase(mx, 13.0, [(81, 1), (78, 0.5), (76, 0.5), (74, 2)], gain=0.13)
    mx.add(pad([38, 50, 57, 62, 66, 69, 76], 4.0, attack=0.05), 16.0, 0.22)
    mx.add(sub(26, 3.5), 16.0, 0.45)
    mx.add(kick_full(), 16.0, 0.9)
    for i, (kind, tt) in enumerate([("D", 16.0), ("t", 16.25), ("t", 16.375), ("D", 16.5), ("t", 16.75), ("D", 17.0),
                                    ("t", 17.5), ("D", 18.0), ("D", 19.0)]):
        mx.add(dhin(0.5) if kind == "D" else ta(0.5), tt)
    tt = 17.0
    while tt < 19.4:
        b = int(round((tt - 17.0) / BEAT)) % 4
        if b == 0:
            mx.add(kick_full(), tt, 0.55)
        if b in (1, 3):
            mx.add(snap(), tt, 0.28, pan=0.12)
        for e in range(2):
            kind, g = madal[(b * 2 + e) % 8]
            mx.add(dhin(g * 0.45) if kind == "D" else ta(g * 0.45), tt + e * BEAT / 2, 1.0)
        tt += BEAT
    mx.add(pad([62, 66, 69, 74, 78], 3.0, attack=0.6), 17.0, 0.08)
    flute_phrase(mx, 16.15, [(86, 0.5), (83, 0.5), (81, 0.5), (78, 0.5), (81, 1), (86, 4)], gain=0.20)
    for i, m in enumerate([74, 78, 81, 86, 90]):
        mx.add(bell(m, 1.8), 17.15 + i * BEAT / 2, 0.07, pan=-0.4 + 0.2 * i)
    for tc, kind in film.CUES:
        mx.add(sfx(kind), tc, 1.0, pan={"kite": 0.35, "chip": 0.2, "pop": -0.2}.get(kind, 0.0))
    return mx


def write(path):
    mx = arrange()
    st = np.stack([mx.L, mx.R], axis=1)
    # small stereo room: short cross-delays
    for dl, g in ((0.031, 0.12), (0.047, 0.09)):
        k = int(dl * SR)
        st[k:, 0] += st[:-k, 1] * g
        st[k:, 1] += st[:-k, 0] * g
    fade = int(SR * 0.6)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st = st / np.max(np.abs(st)) * 0.89
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "score.wav")
