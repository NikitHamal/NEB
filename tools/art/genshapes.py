#!/usr/bin/env python3
"""Generate the Material 3 Expressive shape set for the web.

The app waits on `LoadingIndicator`, which is not a spinning arc: it is a
sequence of MaterialShapes morphing into one another while the whole thing
turns. That reads as the same drawing as the rest of the app, which a circular
arc does not, and the web had nine different spinners and no answer at all.

There is no MaterialShapes on the web, so the shapes are rebuilt here from the
same descriptions -- a polar radius function per shape, sampled at a fixed
number of angles. Fixing the sample count is the whole trick: browsers
interpolate one clip-path: polygon() into another point by point, but only when
both have the same number of points. Every shape sampled at the same count
therefore morphs into every other one for free, in CSS, with no SVG and no
markup -- which matters because most of the spinners being replaced are bare
elements with nothing inside them. One file comes out:

  web/static/web/css/material3/08-shapes.css

It is checked in. Re-run this after changing anything here:

    tools/art/genshapes.py
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WEB = os.path.join(ROOT, "backend_python/web")

# Samples per shape. A clip-path polygon has no curves between its points, so
# the smoothing has to come from there being enough of them. 48 was not:
# cookie-9 has nine lobes, which is five samples each, and five straight
# segments per lobe reads as a spike rather than a scallop. 72 gives eight and
# the lobe comes back. Every shape uses this same count, which is what makes
# them interpolable.
CN = 72
# How long one pass through the whole sequence takes, matching the app.
CYCLE = '4.2s'


def _polygon(sides, rotate=0.0):
    """Radius function of a regular polygon inscribed in the unit circle."""
    step = 2 * math.pi / sides
    apothem = math.cos(step / 2)

    def r(t):
        a = (t + rotate) % step - step / 2
        return apothem / math.cos(a)
    return r


def _superellipse(a, b, n):
    def r(t):
        cx = abs(math.cos(t) / a) ** n
        cy = abs(math.sin(t) / b) ** n
        return (cx + cy) ** (-1.0 / n)
    return r


def _rotated(r, angle):
    """The same outline, turned. `slanted` is only a squircle off-axis."""
    def rr(t):
        return r(t - angle)
    return rr


def _gem():
    """A cut stone: a hexagon stood on a point, slightly narrowed. The facets
    have to be straight and the vertices sharp, which is what separates it from
    every cookie in the set."""
    hexagon = _polygon(6, rotate=math.pi / 2)

    def r(t):
        # Narrowing horizontally turns a regular hexagon into a stone rather
        # than a honeycomb cell.
        base = hexagon(t)
        return base * (1.0 - 0.10 * abs(math.cos(t)))
    return r


def _clover(count, depth, sharpness=2.0):
    """A clover: fat lobes separated by narrow notches.

    A cookie is a cosine, which spends as much of its circumference in the
    valley as on the peak -- at four lobes that reads as a four-pointed star,
    not as Expressive's Clover4Leaf. Raising the normalised valley to a power
    above one pulls the notch in tight and leaves the lobe broad, which is the
    difference between a sparkle and a clover.
    """
    def r(t):
        u = (1.0 - math.cos(count * t)) / 2.0
        return 1.0 - depth * (u ** sharpness)
    return r


def _lobed(count, depth, phase=0.0):
    """A cookie: a circle with `count` lobes pushed out of it."""
    def r(t):
        return 1.0 + depth * math.cos(count * t + phase)
    return r


# The morph sequence, in order. These are the Expressive shapes the app's
# loader cycles through; the names are theirs.
SHAPES = [
    # Lobe depth is the whole character of a cookie. Past about 12% the peaks
    # stop reading as scallops and start reading as a star, which is a different
    # drawing and not the one the app uses.
    ("soft-burst", _lobed(10, 0.085)),
    ("cookie-9", _lobed(9, 0.105)),
    ("pentagon", _polygon(5, rotate=math.pi / 2)),
    ("pill", _superellipse(1.0, 0.62, 4.0)),
    ("sunny", _lobed(8, 0.10)),
    ("cookie-4", _lobed(4, 0.17)),
    ("oval", _superellipse(1.0, 0.78, 2.0)),
]

# Shapes offered as clip-paths. A couple are not in the morph but are what the
# app puts avatars and badges in.
CLIPS = SHAPES + [
    ("clover", _clover(4, 0.26)),
    ("square", _superellipse(1.0, 1.0, 4.0)),
    ("circle", lambda t: 1.0),
    # The other two in the app's NebShapes.Option bank. A column of four
    # identical rounded squares is a form; four different silhouettes is a
    # choice, and the user can tell which one they picked from across the room.
    ("gem", _gem()),
    ("slanted", _rotated(_superellipse(1.0, 1.0, 3.4), math.radians(14))),
]


def sample(r, n=CN, scale=1.0):
    """n points around the outline, normalised so the widest point is `scale`."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        pts.append((r(t) * math.cos(t), r(t) * math.sin(t)))
    peak = max(math.hypot(x, y) for x, y in pts) or 1.0
    k = scale / peak
    return [(x * k, y * k) for x, y in pts]


def _num(v):
    s = '%.2f' % v
    s = s.rstrip('0').rstrip('.')
    return s or '0'


# Where the avatar shape is actually applied. NebShapes.Avatar is
# MaterialShapes.Cookie9Sided and every avatar in the app is clipped to it; the
# web drew circles everywhere, which is the parity gap that shows up on the most
# screens -- every feed row, every comment, every profile, the top bar.
#
# The clip goes on the picture and the initial, never on the container. A
# verified user's badge is a child of the container positioned past its
# bottom-right corner, and clip-path clips every descendant regardless of
# overflow, so clipping the container would cut the badge in half. Going through
# the children also leaves each container's own ring, size and fill alone.
#
# Bot and assistant avatars are deliberately not here: Neby and the agents are
# not people, and the app keeps them circular for exactly that reason.
# The containers. These get the shape directly, which is what makes an avatar
# showing only an initial the same silhouette as one showing a photo -- the
# initial has no background of its own, the container's fill is what you see.
#
# The exception is a container holding a verified badge. The badge is a child
# positioned past the bottom-right corner, and clip-path clips descendants
# whatever overflow says, so clipping that container would cut the badge in
# half. Those keep their box and let the picture inside carry the shape.




def build_css():
    lines = [
        "/* GENERATED by tools/art/genshapes.py -- do not edit.",
        "   Material 3 Expressive shapes, as clip-paths and as the loader. */",
        "",
        "/* ── Shapes ─────────────────────────────────────────────────────────",
        "   polygon() in percentages rather than path() in pixels, so one class",
        "   fits a 28px avatar and a 120px thumbnail without being redrawn. */",
    ]
    for name, r in CLIPS:
        lines.append('.md-shape-%s { clip-path: %s; }' % (name, _poly(r)))
    lines.append(_option_cycle_css())
    lines.append(LOADER_CSS.replace('$CYCLE', CYCLE))
    lines.append(_morph_keyframes())
    return '\n'.join(lines) + '\n'



# NebShapes.Option, in order. A column of four identical rounded squares is a
# form; four different silhouettes is a choice, and the user can tell which one
# they picked from across the room. The app spells this as
# NebShapes.option(index); on the web nth-child does the indexing.
OPTION_CYCLE = ["cookie-9", "clover", "gem", "slanted"]


def _option_cycle_css():
    """Auto-assign the Option bank's silhouettes down a list of options.

    Android calls NebGlyphTile(polygon = NebShapes.option(index)) and gets the
    rotation for free. Putting it in a container class means web markup does
    not have to hand-count .md-shape-* classes either -- and cannot get the
    order wrong, which is the whole point of generating this file.
    """
    out = ["", "/* \u2500\u2500 Option banks " + "\u2500" * 59,
           "   NebShapes.Option, cycled by position. Wrap a bank of .neb-option",
           "   or .neb-tile in .neb-opt-bank and their glyph tiles take one",
           "   silhouette each, in the app's order. */"]
    clips = dict(CLIPS)
    n = len(OPTION_CYCLE)
    for i, name in enumerate(OPTION_CYCLE):
        sel = ".neb-opt-bank > *:nth-child(%dn+%d) > .neb-glyph" % (n, i + 1)
        out.append("%s {\n  clip-path: %s;\n}" % (sel, _poly(clips[name])))
    return "\n".join(out) + "\n"

def _poly(r):
    pts = sample(r, scale=50.0)
    return 'polygon(%s)' % ', '.join(
        '%s%% %s%%' % (_num(50 + x), _num(50 + y)) for x, y in pts)


def _morph_keyframes():
    """The morph. One stop per shape, plus the first again so the loop closes."""
    seq = SHAPES + SHAPES[:1]
    out = ['@keyframes md-loader-morph {']
    for i, (name, r) in enumerate(seq):
        pct = _num(100.0 * i / (len(seq) - 1))
        out.append('  %s%% { clip-path: %s; } /* %s */' % (pct, _poly(r), name))
    out.append('}')
    return '\n'.join(out) + '\n'


LOADER_CSS = """/* ── The loader ─────────────────────────────────────────────
   One wait for the whole site, at the app's four sizes: inside a button,
   inside a row, inside a card, or holding a screen. It is a solid block of
   currentColor with a shape cut out of it -- the shape morphs, the block
   turns. An empty element is the entire markup, which is what lets the
   spinners that were already scattered about adopt it without being rewritten.

     <span class="md-loader md-loader-inline"></span> */
.md-loader {
  display: inline-block;
  width: 36px;
  height: 36px;
  flex: none;
  color: var(--md-primary);
  background: currentColor;
  vertical-align: middle;
  clip-path: polygon(50% 0, 100% 0, 100% 100%, 0 100%, 0 0);
  animation: md-loader-morph $CYCLE ease-in-out infinite,
             md-loader-turn $CYCLE linear infinite;
}
.md-loader-inline { width: 18px; height: 18px; }
.md-loader-small { width: 26px; height: 26px; }
.md-loader-screen { width: 48px; height: 48px; }
/* On a filled button or a coloured bar the loader has to invert. */
.md-loader-on-primary { color: var(--md-on-primary); }
.md-loader-plain { color: inherit; }

@keyframes md-loader-turn {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* A wait that holds a row, and a wait that holds a screen. */
.md-loading-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 18px 0;
  color: var(--md-on-surface-variant);
  font-size: 0.9375rem;
}
.md-loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  min-height: 240px;
  width: 100%;
  color: var(--md-on-surface-variant);
  font-size: 0.9375rem;
  text-align: center;
}

/* Motion off means motion off: it stops turning and stops morphing. It still
   has to look like something is happening, so it breathes instead. */
@media (prefers-reduced-motion: reduce) {
  .md-loader {
    animation: md-loader-pulse 1.6s ease-in-out infinite;
    clip-path: polygon(50% 0, 100% 0, 100% 100%, 0 100%, 0 0);
  }
  @keyframes md-loader-pulse {
    0%, 100% { opacity: 0.35; }
    50% { opacity: 1; }
  }
}
"""


def main():
    path = os.path.join(WEB, 'static/web/css/material3/08-shapes.css')
    text = build_css()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('%-56s %6d bytes' % (os.path.relpath(path, ROOT), len(text.encode('utf-8'))))


if __name__ == '__main__':
    main()
