"""Every sound in the lessons is synthesised here, so nothing carries a licence or an attribution."""
import os
import wave

import numpy as np
from scipy.signal import butter, lfilter, sosfilt

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", ".cache", "sfx")
RNG = np.random.default_rng(7)


def _t(d):
    return np.arange(int(SR * d)) / SR


def _env(n, a=0.005, r=0.2, curve=4.0):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    dec = np.exp(-curve * np.clip(t - a, 0, None) / max(r, 1e-4))
    return att * dec


def _bp(x, lo, hi, order=2):
    sos = butter(order, [lo / (SR / 2), hi / (SR / 2)], btype="band", output="sos")
    return sosfilt(sos, x)


def _lp(x, f, order=2):
    sos = butter(order, f / (SR / 2), btype="low", output="sos")
    return sosfilt(sos, x)


def _norm(x, peak=0.8):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def whoosh(d=0.55, up=True):
    n = int(SR * d)
    noise = RNG.standard_normal(n)
    t = np.linspace(0, 1, n)
    out = np.zeros(n)
    bands = np.linspace(300, 3200, 18) if up else np.linspace(3200, 300, 18)
    seg = n // len(bands)
    for i, f in enumerate(bands):
        s = slice(i * seg, min(n, (i + 3) * seg))
        out[s] += _bp(noise[s], f * 0.7, f * 1.3) * np.hanning(s.stop - s.start)
    shape = np.sin(np.pi * t) ** 1.6
    return _norm(out * shape, 0.5)


def pop(f0=520, f1=900, d=0.12):
    t = _t(d)
    f = f0 + (f1 - f0) * (1 - np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return _norm(np.sin(ph) * _env(len(t), 0.002, d * 0.5), 0.55)


def click(d=0.03, f=2400):
    t = _t(d)
    x = np.sin(2 * np.pi * f * t) * _env(len(t), 0.0005, 0.01, 6) + 0.3 * RNG.standard_normal(len(t)) * _env(len(t), 0.0003, 0.004, 6)
    return _norm(x, 0.35)


def tick():
    return click(0.04, 3200) * 0.8


def bell(freq=880, d=1.6, amp=0.5):
    t = _t(d)
    parts = [(1, 1.0, 1.0), (2.0, 0.45, 1.6), (2.76, 0.3, 2.2), (5.4, 0.12, 3.5), (8.93, 0.06, 5)]
    x = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t * k * 2.2) for m, a, k in parts)
    return _norm(x * _env(len(t), 0.002, d, 0.5), amp)


def chime_correct():
    a = bell(1046.5, 1.4, 0.4)
    b = bell(1568.0, 1.6, 0.4)
    out = np.zeros(int(SR * 1.9))
    out[: len(a)] += a
    o = int(SR * 0.13)
    out[o: o + len(b)] += b
    return _norm(out, 0.5)


def soft_wrong():
    t = _t(0.35)
    x = np.sin(2 * np.pi * 220 * t) + 0.5 * np.sin(2 * np.pi * 233 * t)
    return _norm(_lp(x, 1200) * _env(len(t), 0.01, 0.25), 0.35)


def thud(f=70, d=0.45):
    t = _t(d)
    f_ = f * (1 + 1.5 * np.exp(-t * 30))
    x = np.sin(2 * np.pi * np.cumsum(f_) / SR) * _env(len(t), 0.002, d * 0.6, 3)
    x += 0.15 * _lp(RNG.standard_normal(len(t)), 900) * _env(len(t), 0.001, 0.05)
    return _norm(x, 0.7)


def riser(d=1.6):
    t = _t(d)
    f = 180 * (2 ** (np.linspace(0, 2.2, len(t))))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4
    x += _bp(RNG.standard_normal(len(t)), 900, 6000) * np.linspace(0, 1, len(t)) ** 2 * 0.6
    return _norm(x * np.linspace(0.05, 1, len(t)) ** 1.5 * np.minimum(1, (d - t) * 30), 0.45)


def shimmer(d=1.2):
    t = _t(d)
    x = np.zeros(len(t))
    for i, f in enumerate([1318.5, 1567.98, 1975.5, 2637.0, 3135.9]):
        o = int(SR * i * 0.06)
        b = bell(f, d - i * 0.06, 0.2)
        x[o: o + len(b)] += b[: len(x) - o]
    return _norm(x, 0.35)


def swoosh_down():
    return whoosh(0.5, up=False)


def typekey():
    return click(0.025, 1800 + RNG.integers(0, 900)) * 0.6


def impact():
    a = thud(55, 0.9)
    b = _norm(_bp(RNG.standard_normal(len(a)), 200, 3000) * _env(len(a), 0.001, 0.15, 5), 0.3)
    return _norm(a + b, 0.75)


def countdown_tick():
    return bell(1760, 0.18, 0.25)


SOUNDS = {
    "whoosh": lambda: whoosh(),
    "whoosh_down": swoosh_down,
    "pop": lambda: pop(),
    "pop_low": lambda: pop(300, 520, 0.14),
    "click": lambda: click(),
    "tick": tick,
    "bell": lambda: bell(),
    "correct": chime_correct,
    "wrong": soft_wrong,
    "thud": lambda: thud(),
    "riser": lambda: riser(),
    "shimmer": lambda: shimmer(),
    "type": typekey,
    "impact": impact,
    "count": countdown_tick,
}


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    st = np.stack([pcm, pcm], axis=1).reshape(-1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())


def get(name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name + ".wav")
    if not os.path.exists(path):
        write_wav(path, SOUNDS[name]())
    return path


def _pad_voice(freqs, d, bright=0.25):
    t = _t(d)
    x = np.zeros(len(t))
    for f in freqs:
        for det in (-0.12, 0.0, 0.13):
            ff = f * 2 ** (det / 12)
            ph = RNG.uniform(0, 2 * np.pi)
            x += np.sin(2 * np.pi * ff * t + ph) + bright * np.sin(4 * np.pi * ff * t + ph)
    a = np.minimum(1, t / 1.6) * np.minimum(1, (d - t) / 1.6)
    return x * a


def music_bed(seconds, seed=3, mood="calm"):
    """A quiet, slowly evolving pad with a soft pluck arpeggio, long enough for `seconds`."""
    rng = np.random.default_rng(seed)
    progs = {
        "calm": [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 66]],
        "bright": [[48, 52, 55, 59], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]],
        "warm": [[50, 53, 57, 60], [55, 58, 62, 65], [48, 52, 55, 58], [53, 57, 60, 64]],
    }[mood]
    bar = 8.0
    n = int(SR * (seconds + 2))
    out = np.zeros(n)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    i = 0
    pos = 0
    while pos < n:
        chord = progs[i % len(progs)]
        d = bar + 1.6
        pad = _pad_voice([hz(m) for m in chord], d)
        seg = out[pos: pos + len(pad)]
        seg += pad[: len(seg)] * 0.07
        step = bar / 8
        for k in range(8):
            note = chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12
            if rng.random() < 0.25:
                continue
            pl = _t(1.2)
            f = hz(note)
            pluck = (np.sin(2 * np.pi * f * pl) + 0.3 * np.sin(4 * np.pi * f * pl)) * np.exp(-pl * 3.5)
            o = pos + int(SR * k * step)
            s2 = out[o: o + len(pluck)]
            s2 += pluck[: len(s2)] * 0.045
        bass_t = _t(bar)
        bass = np.sin(2 * np.pi * hz(chord[0] - 12) * bass_t) * np.minimum(1, bass_t / 0.3) * np.exp(-bass_t * 0.25)
        s3 = out[pos: pos + len(bass)]
        s3 += bass[: len(s3)] * 0.06
        pos += int(SR * bar)
        i += 1
    out = _lp(out, 4200)
    rev = np.zeros_like(out)
    for dl, g in ((0.031, 0.5), (0.047, 0.4), (0.071, 0.3), (0.113, 0.22), (0.173, 0.15)):
        k = int(SR * dl)
        rev[k:] += out[:-k] * g
    out = out + rev * 0.5
    fade = int(SR * 3)
    out[-fade:] *= np.linspace(1, 0, fade)
    return _norm(out, 0.6)
