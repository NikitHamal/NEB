"""Palettes and the scene registry."""
from engine import Pal

# Ramps run darkest to lightest. Warm, mineral and phosphor tones; no blue or purple ramps.
P = {p.name: p for p in (
    Pal('bone', '#0f0e0d', '#f2ecdc'),
    Pal('newsprint', '#1b1a18', '#e9e5d9'),
    Pal('ember', '#120907', '#7c1d10', '#e8602a', '#f8e9c4'),
    Pal('lava', '#0b0605', '#a31515', '#ff6a1f', '#ffd36b', '#fff6dc'),
    Pal('acid', '#050e07', '#17692f', '#7bd84a', '#e4ffb0'),
    Pal('phosphor', '#040a05', '#b9ff7a'),
    Pal('amber', '#130b02', '#7d4306', '#f0a321', '#ffe9ad'),
    Pal('rose', '#1a0d12', '#c93f5b', '#f9e7df'),
    Pal('jade', '#07130e', '#1d5b47', '#6db38c', '#eaf3da'),
    Pal('sand', '#25190f', '#a96e34', '#e9c98a', '#fbf1d6'),
    Pal('gold', '#0d0b09', '#6a4710', '#dfa82c', '#fcf2d0'),
    Pal('terracotta', '#1a0e09', '#ad4528', '#f2dcb8'),
    Pal('signal', '#0b0b0b', '#ff3a2d'),
    Pal('lime', '#0b0c08', '#d8ff3c'),
    Pal('tangerine', '#0c0a08', '#ff7a1c'),
    Pal('ice', '#0b1517', '#4f9d99', '#e4f4ee'),
    Pal('moss', '#0c120a', '#4d6b2a', '#c4c98a', '#f4f1dd'),
    Pal('clay', '#201512', '#8c5a45', '#e2cdb4'),
    Pal('ink-red', '#15110f', '#d03a28', '#f3ecdd'),
)}

REG = []


def scene(slug, title, era, w, h, variants, scale=4):
    """variants: list of (palette, method, kwargs)."""
    def deco(fn):
        REG.append(dict(slug=slug, title=title, era=era, w=w, h=h, scale=scale, variants=variants, fn=fn))
        return fn
    return deco
