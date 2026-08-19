"""Port of blobatar/src/traits.ts — deterministic keyed trait reader (v2)."""

from .hash import seed_state, stream


class Traits:
    __slots__ = ("_state", "_overrides")

    def __init__(self, seed, normalize=True, overrides=None):
        self._state = seed_state(seed, normalize)
        self._overrides = overrides or {}

    def __call__(self, key):
        v = self._overrides.get(key)
        if isinstance(v, list):
            o = v[int(stream(self._state, key) * len(v))] if v else None
        else:
            o = v
        if o is None:
            return stream(self._state, key)
        if o > 0:
            return o if o < 1 else 0.999999
        return 0.0

    def num(self, key, minimum, maximum):
        return minimum + self(key) * (maximum - minimum)

    def int(self, key, minimum, maximum):
        return minimum + int(self(key) * (maximum - minimum + 1))

    def pick(self, key, options):
        return options[int(self(key) * len(options))]

    def bool(self, key, p=0.5):
        return self(key) < p

    def jitter(self, key, amount):
        return (self(key) * 2 - 1) * amount


def traits(seed, normalize=True, overrides=None):
    return Traits(seed, normalize, overrides)