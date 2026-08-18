"""Port of blobatar/src/render.ts + src/blobatar.ts — options resolution and SVG assembly."""

import re

from .blob import background as default_background
from .blob import layout as default_layout
from .blob import render as default_render
from .color import palette as build_palette
from .shape import superellipse
from .traits import traits

_ESCAPE_RE = re.compile(r"[&<>]")


def _escape(s):
    def _sub(m):
        c = m.group(0)
        if c == "&":
            return "&amp;"
        if c == "<":
            return "&lt;"
        return "&gt;"

    return _ESCAPE_RE.sub(_sub, s)


def resolve(seed, opts=None):
    opts = opts or {}
    t = traits(seed, opts.get("normalize", True), opts.get("traits"))
    merged = build_palette(
        opts.get("hue", t.num("hue", 0, 360)),
        opts.get("contrast", True),
        opts.get("tone", t("tone")),
    )
    merged.update(opts.get("palette", {}) or {})
    return {"t": t, "palette": merged}


def _backdrop(opts, p):
    bg = opts.get("background") if "background" in opts else default_background
    if bg is False:
        return None
    if bg == "square":
        d = "M0 0H100V100H0Z"
    else:
        d = superellipse(50, 50, 50, 50, 2 if bg == "circle" else 6)
    return {'d': d, 'fill': p['bg']}


def _anim_element(anim):
    if anim == "bob":
        return ('<animateTransform attributeName="transform" type="translate" '
                'values="0 0; 0 -7; 0 0" keyTimes="0; 0.5; 1" '
                'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
                'dur="3s" repeatCount="indefinite"/>')
    if anim == "wave":
        return ('<animateTransform attributeName="transform" type="rotate" '
                'values="0 50 50; 5 50 50; 0 50 50; -5 50 50; 0 50 50" '
                'keyTimes="0; 0.25; 0.5; 0.75; 1" '
                'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1" '
                'dur="4s" repeatCount="indefinite"/>')
    if anim == "spin":
        return ('<animateTransform attributeName="transform" type="rotate" '
                'from="0 50 50" to="360 50 50" dur="6s" repeatCount="indefinite"/>')
    if anim == "pulse":
        return ('<animateTransform attributeName="transform" '
                'values="translate(50 50) scale(1) translate(-50 -50); '
                'translate(50 50) scale(1.06) translate(-50 -50); '
                'translate(50 50) scale(1) translate(-50 -50)" '
                'keyTimes="0; 0.5; 1" calcMode="spline" '
                'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
                'dur="3s" repeatCount="indefinite"/>')
    return None


def blobatar(name, opts=None):
    opts = opts or {}
    resolved = resolve(name, opts)
    palette = resolved["palette"]
    dim = ' width="%s" height="%s"' % (opts["size"], opts["size"]) if opts.get("size") else ""
    title = "<title>%s</title>" % _escape(opts["title"]) if opts.get("title") else ""
    plate = _backdrop(opts, palette)
    plate_svg = '<path d="%s" fill="%s"/>' % (plate['d'], plate['fill']) if plate else ""
    inner = default_render(default_layout(resolved["t"]), palette)
    anim = _anim_element(opts.get("anim"))
    if anim:
        inner = '<g>%s%s</g>' % (anim, inner)
    body = title + plate_svg + inner
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%s>%s</svg>' % (dim, body)
