"""Port of blobatar/src/hash.ts — murmur3-style seed hashing."""

import unicodedata

SEP = 0xFF
MASK32 = 0xFFFFFFFF


def _imul(a, b):
    return (a * b) & MASK32


def feed(h, data):
    for byte in data:
        h = _imul(h ^ byte, 3432918353)
        h = ((h << 13) | (h >> 19)) & MASK32
    return h


def finalize(h):
    h = _imul(h ^ (h >> 16), 2246822507)
    h = _imul(h ^ (h >> 13), 3266489909)
    return (h ^ (h >> 16)) & MASK32


def normalize_seed(seed):
    return unicodedata.normalize("NFC", seed).strip().lower()


def seed_state(seed, normalize=True):
    s = normalize_seed(seed) if normalize else seed
    return feed(1779033703 ^ (len(s.encode("utf-16-le")) // 2), s.encode("utf-8"))


def stream(state, key):
    return finalize(feed(feed(state, bytes([SEP])), key.encode("utf-8"))) / 4294967296.0
