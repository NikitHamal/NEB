#!/usr/bin/env python3
"""Build the NEBians SVG art library.

    python3 tools/svgart/build.py            riso and flat SVGs + manifest
    python3 tools/svgart/pixel.py            the pixel versions (needs Playwright's Chromium)

Writes backend_python/web/static/web/art/<set>/<name>-<look>.svg and art/manifest.json, which
the admin gallery (/admin/art/) reads. Every scene is seeded, so a rebuild is byte-identical.
"""
import json
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "backend_python", "web", "static", "web", "art")

from painter import LOOKS  # noqa: E402
import scenes  # noqa: E402

LOOK_INFO = {
    "riso": "Grain: risograph stipple, soft glows, paper texture",
    "flat": "Flat: warm editorial vector, two tones and hairline detail",
    "pixel": "Pixel: the same scene as crisp, dithered pixel art",
}


def seed(name):
    return zlib.crc32(name.encode())


def main():
    manifest = {"looks": LOOK_INFO, "sets": []}
    sets = dict(scenes.SETS)
    sets["backgrounds"] = ({k: v[0] for k, v in scenes.BACKGROUNDS.items()}, None, None, "Backgrounds", "Auth hero, landscapes, glows")
    for key, (table, w, h, title, blurb) in sets.items():
        os.makedirs(os.path.join(OUT, key), exist_ok=True)
        items = []
        for name, fn in table.items():
            ww, hh = (w, h) if w else scenes.BACKGROUNDS[name][1:]
            files = {}
            for look, cls in LOOKS.items():
                p = cls(ww, hh, "%s %s (%s)" % (title, name, look), seed("%s/%s" % (key, name)))
                fn(p)
                rel = "%s/%s-%s.svg" % (key, name, look)
                with open(os.path.join(OUT, rel), "w", encoding="utf-8") as fh:
                    fh.write(p.svg())
                files[look] = rel
            pix = "%s/%s-pixel.svg" % (key, name)
            if os.path.exists(os.path.join(OUT, pix)):
                files["pixel"] = pix
            items.append({"name": name, "w": ww, "h": hh, "files": files})
            print("%-12s %-16s %s" % (key, name, " ".join(sorted(files))))
        manifest["sets"].append({"key": key, "title": title, "blurb": blurb, "items": items})
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)


if __name__ == "__main__":
    main()
