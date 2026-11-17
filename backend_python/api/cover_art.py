"""Profile covers from the M3X art library (concepts/art-v7, tools/art/export_m3x_assets.js).

The list of ids that ship as images is covers.json next to the images, so the API accepts exactly
what the web and the app can draw and nothing else."""
import json
import os
from functools import lru_cache

_MANIFEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         'web', 'static', 'web', 'img', 'm3x', 'covers.json')


@lru_cache(maxsize=1)
def cover_rows():
    """[(id, layout, palette)] in the order the images were exported (append only)."""
    try:
        with open(_MANIFEST, encoding='utf-8') as fh:
            return tuple(tuple(row) for row in json.load(fh).get('covers', []))
    except (OSError, ValueError):
        return ()


def cover_ids():
    return frozenset(row[0] for row in cover_rows())


def _fnv1a(text):
    h = 2166136261
    for b in text.encode('utf-8'):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def default_cover(username):
    """The cover a member who never chose one gets: a stable pick from the username.
    The Android app (M3xArt.defaultCover) runs the same hash over the same list."""
    rows = cover_rows()
    if not rows:
        return 'cover-001'
    return rows[_fnv1a('cover|' + (username or '')) % len(rows)][0]


def is_valid_cover(cover_id):
    return cover_id == '' or cover_id in cover_ids()
