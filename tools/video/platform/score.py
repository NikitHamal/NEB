"""Score for the NEBians platform film: bright modern groove with a Nepali accent.
Reuses the instruments of ../neby/score.py and ../nebians-launch/score.py; effects come from film.CUES."""
import importlib.util
import os
import sys
import wave

import numpy as np

import film

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


base = _load("neby_score", os.path.join(HERE, "..", "neby", "score.py"))
das = _load("dashain_score", os.path.join(HERE, "..", "nebians-launch", "score.py"))
SR = base.SR
N = int(SR * film.DURATION)
BEAT = 60.0 / film.BPM
rng = np.random.default_rng(5)


class Mix(das.Mix):
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


def slam():
    d = 0.6
    x = base.sine(lambda t: 45 + 110 * np.exp(-t * 30), d) * base.env(d, 0.001, 6) * 1.0
    x += base.filt(rng.standard_normal(int(SR * d)), "lowpass", 3000) * base.env(d, 0.001, 18) * 0.5
    s = base.snap()
    x[: len(s)] += s * 0.6
    return x


def implode():
    d = 0.32
    n = rng.standard_normal(int(SR * d))
    x = base.bandsweep(n, 6000, 300) * np.linspace(1, 0.2, len(n)) * 0.6
    return x


def sfx(kind):
    if kind == "slam":
        return slam()
    if kind == "implode":
        return implode()
    if kind == "drop":
        return base.sfx("whoosh_down")[: int(SR * 0.35)] * 0.6
    if kind == "upload":
        d = 0.55
        return base.sine(lambda t: 500 + 900 * t / d, d) * base.env(d, 0.01, 2) * 0.12
    if kind == "badge":
        x = base.bell(88, 1.2) * 0.25
        x[: int(SR * 0.6)] += base.bell(95, 0.6) * 0.15
        return x
    if kind == "swap":
        return base.sfx("swish") * 0.6
    if kind == "sparkle":
        return base.sfx("sparkle")
    return das.sfx(kind)


CHORDS = [(48, [60, 64, 67, 72]), (43, [55, 59, 62, 67]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69])]


def arrange():
    mx = Mix()
    for t0 in (0.0, 0.5, 1.0, 1.5):
        mx.add(base.pad([48 + (t0 * 2) * 2, 55, 60, 64], 0.5, attack=0.01), t0, 0.12)
    mx.add(base.pad([60, 64, 67, 71, 74], 2.6, attack=1.0), 2.2, 0.08)
    for i, m in enumerate([72, 76, 79, 84]):
        mx.add(base.bell(m, 1.0), 2.3 + i * 0.09, 0.08)
    start, end = 2.5, 17.5
    t = start
    b = 0
    while t < end - 1e-6:
        root, chord = CHORDS[b % 4]
        for beat in range(4):
            tb = t + beat * BEAT
            if tb >= end:
                break
            mx.add(base.kick_full(), tb, 0.8)
            if beat in (1, 3) and tb >= 5.0:
                mx.add(base.snap(), tb, 0.42, pan=0.1)
            mx.add(base.hat(), tb + BEAT / 2, 0.20, pan=0.35)
            if tb >= 5.0:
                mx.add(base.hat(0.03), tb + BEAT / 4, 0.08, pan=-0.35)
                mx.add(base.hat(0.03), tb + 3 * BEAT / 4, 0.08, pan=-0.35)
            mx.add(base.bass(root - 12 + (12 if beat % 2 else 0), BEAT * 0.85), tb, 0.34)
            if beat == 3 and tb >= 9.0:
                mx.add(das.ta(0.4), tb + BEAT / 2, 1.0, pan=-0.25)
                mx.add(das.dhin(0.4), tb + 3 * BEAT / 4, 1.0)
        pattern = [0, 2, 1, 3, 2, 1, 3, 2]
        for s in range(8):
            ts = t + s * BEAT / 2
            if ts < end:
                mx.add(base.marimba(chord[pattern[s]] + 12, 0.45), ts, 0.15, pan=-0.3 + 0.6 * (s % 2))
        mx.add(base.pad(chord, 4 * BEAT, attack=0.3), t, 0.05)
        t += 4 * BEAT
        b += 1
    mx.add(base.pad([36, 48, 55, 60, 64, 67, 71, 74], 4.0, attack=0.05), 18.0, 0.22)
    mx.add(das.sub(24, 3.5), 18.0, 0.45)
    mx.add(base.kick_full(), 18.0, 0.95)
    tt = 19.0
    while tt < 21.5:
        bb = int(round((tt - 19.0) / BEAT)) % 4
        if bb == 0:
            mx.add(base.kick_full(), tt, 0.5)
        if bb in (1, 3):
            mx.add(base.snap(), tt, 0.25)
        mx.add(das.dhin(0.35) if bb % 2 == 0 else das.ta(0.35), tt, 1.0)
        tt += BEAT
    das.flute_phrase(mx, 18.15, [(84, 0.5), (79, 0.5), (76, 0.5), (79, 0.5), (84, 1), (88, 3)], gain=0.17)
    for i, m in enumerate([72, 76, 79, 84, 88]):
        mx.add(base.bell(m, 1.8), 19.1 + i * BEAT / 2, 0.07, pan=-0.4 + 0.2 * i)
    for tc, kind in film.CUES:
        mx.add(sfx(kind), tc, 1.0, pan={"pop": -0.2, "tick": 0.2, "swap": 0.3}.get(kind, 0.0))
    return mx


def write(path):
    mx = arrange()
    st = np.stack([mx.L, mx.R], axis=1)
    for dl, g in ((0.029, 0.12), (0.043, 0.09)):
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
