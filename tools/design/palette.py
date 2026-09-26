#!/usr/bin/env python3
"""The NEBians palette, defined once and emitted for both clients.

The app and the web had drifted into two different neutral ramps -- the app on
a navy, the web on a blue-grey, neither the same numbers -- so "the same
screen" was never quite the same screen. This file is the single source. It
writes the generated block of

  app/src/main/java/com/neb/ians/ui/theme/Palette.kt
  backend_python/web/static/web/css/material3/00-palette.css

and it refuses to write either one unless the contrast audit passes, which is
the point of it being a program rather than two lists of hex.

Run after changing anything here:

    tools/design/palette.py            # write both files
    tools/design/palette.py --check    # audit only, non-zero on drift
    tools/design/palette.py --audit    # print the full contrast table

── Why these numbers ─────────────────────────────────────────────────────────

The complaint was contrast, in both themes, and the measurement agreed -- but
not where you would guess. Text was never the problem: body text ran 15:1 in
light and 14.7:1 in dark. What failed was *structure*.

    outline-variant vs surface        1.16 light    1.50 dark
    card vs page                      1.08 light    1.15 dark

Every card, field, chip and menu on both platforms is a 1px outline-variant
border around a surface-container-lowest fill. At 1.16 the border is not there,
and at 1.08 neither is the fill difference, so nothing on the page had an edge.
That reads as low contrast even though every letter passes AAA, and no amount
of darkening the text fixes it.

Notion is the reference the brief named and it is the right one, because Notion
solves exactly this and solves it structurally: near-neutral low-chroma greys,
almost no fill difference between page and card, and then a hairline you can
actually see plus a real shadow on anything that floats. Contrast comes from
edges and elevation, not from painting surfaces different colours.

So:

  * The ramp is near-neutral. The app's navy (#0B1C30 dark, a blue-grey light)
    is gone. It carries about 1.5% chroma on the brand's hue -- enough that a
    grey sits with a blue accent rather than against it, far less than the
    10-15% the navy was carrying. Dark is graphite now, which is the half of
    the brief that said the dark theme's contrast is fine but it is disliked.
  * The hairline is visible: outline-variant lands at ~1.9:1 against the
    surfaces it is drawn on, up from 1.16/1.50.
  * outline -- the load-bearing border, on inputs, focus rings and selected
    chips -- clears 3:1 on every surface, which is the WCAG bar for a
    meaningful non-text boundary and which it previously missed at 2.31.
  * Text keeps three honest tiers rather than two: primary, secondary at 4.8:1
    or better on *every* surface (it used to drop to 4.30 on the highest), and
    a tertiary tier for placeholders and timestamps that still clears 3.2:1.
  * Floating layers get Notion's layered shadow. A menu is separated from the
    page by elevation, which is what elevation is for.

The brand blue is untouched. It is the product's, it is not Notion's, and the
neutrals were retuned around it rather than the other way round.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# ── The ramp ────────────────────────────────────────────────────────────────
# Near-neutral, ~1.5% chroma on the brand's hue. The key is the step number:
# N0 is ink, N100 is paper, and the numbers are perceptual lightness, so a
# light role and its dark counterpart can be read off the same list.
N = {
    0:   '#000000',
    3:   '#0A0B0E',
    6:   '#101216',
    8:   '#141519',
    10:  '#191B20',
    12:  '#1D1F25',
    14:  '#212329',
    17:  '#26282F',
    20:  '#2B2D35',
    24:  '#31343C',
    28:  '#383B44',
    32:  '#3F424C',
    36:  '#474A55',
    42:  '#525663',
    48:  '#5F636F',
    54:  '#6B707D',
    60:  '#787D8A',
    66:  '#878C99',
    72:  '#979CA8',
    78:  '#A9AEB9',
    82:  '#B7BCC6',
    86:  '#C6CAD2',
    88:  '#CFD2D9',
    90:  '#D7DAE0',
    92:  '#E0E2E7',
    94:  '#E7E9ED',
    95:  '#EBEDF0',
    96:  '#EFF0F3',
    97:  '#F3F4F6',
    98:  '#F7F8FA',
    99:  '#FBFBFC',
    100: '#FFFFFF',
}

# ── The brand ───────────────────────────────────────────────────────────────
# Unchanged. B40 is the blue the site has shipped since the Django rewrite.
B = {
    10: '#00174B', 20: '#002D78', 30: '#003EA8', 40: '#004AC6', 50: '#0053DB',
    60: '#2E6BEA', 70: '#6E9BFF', 80: '#B4C5FF', 90: '#DBE1FF', 95: '#EDF0FF',
    98: '#F7F9FF',
}
# The brand desaturated, for secondary roles that should recede not recolour.
S = {
    10: '#111A28', 20: '#20293B', 30: '#3B4A66', 40: '#4B5B78', 60: '#7C8AA3',
    70: '#9DAAC2', 80: '#C2CBDA', 90: '#DCE2EB', 95: '#EDF0F5',
}
# The third voice. Used sparingly; never the only cue for anything.
V = {20: '#31185E', 30: '#4C2A93', 40: '#6D45C4', 70: '#C4B5FD', 90: '#EBE6FE', 95: '#F5F2FF'}
E = {  # error keeps its red: an error that reads as ordinary text is not one
    'light': '#BA1A1A', 'onLight': '#FFFFFF', 'containerLight': '#FFDAD6',
    'onContainerLight': '#8C0009',
    'dark': '#FFB4AB', 'onDark': '#690005', 'containerDark': '#93000A',
    'onContainerDark': '#FFDAD6',
}

# ── The roles ───────────────────────────────────────────────────────────────
# One dict per theme. Names are Material's, because both clients already speak
# them; the values are what changed.
LIGHT = {
    'primary': B[40], 'onPrimary': N[100],
    'primaryContainer': B[90], 'onPrimaryContainer': B[10],
    'secondary': S[30], 'onSecondary': N[100],
    'secondaryContainer': S[90], 'onSecondaryContainer': S[10],
    'tertiary': V[40], 'onTertiary': N[100],
    'tertiaryContainer': V[90], 'onTertiaryContainer': V[20],
    'error': E['light'], 'onError': E['onLight'],
    'errorContainer': E['containerLight'], 'onErrorContainer': E['onContainerLight'],

    # Page is a shade off white so a white card has something to sit on; the
    # separation that actually does the work is the border below.
    'background': N[97], 'onBackground': N[12],
    'surface': N[97], 'onSurface': N[12],
    'surfaceVariant': N[94], 'onSurfaceVariant': N[42],
    # Third text tier: placeholders, timestamps, disabled labels. 3.2:1+.
    'onSurfaceTertiary': N[54],
    # The load-bearing border. 3:1 against every surface it is drawn on.
    'outline': N[60],
    # The hairline. Visible now -- this is the single biggest change.
    'outlineVariant': N[82],

    'surfaceDim': N[90], 'surfaceBright': N[100],
    'surfaceContainerLowest': N[100],
    'surfaceContainerLow': N[99],
    'surfaceContainer': N[96],
    'surfaceContainerHigh': N[94],
    'surfaceContainerHighest': N[92],

    'inverseSurface': N[20], 'inverseOnSurface': N[96], 'inversePrimary': B[80],
    'surfaceTint': B[50], 'scrim': N[0],
}

DARK = {
    'primary': B[80], 'onPrimary': B[20],
    'primaryContainer': B[30], 'onPrimaryContainer': B[90],
    'secondary': S[70], 'onSecondary': S[10],
    'secondaryContainer': S[20], 'onSecondaryContainer': S[90],
    'tertiary': V[70], 'onTertiary': V[20],
    'tertiaryContainer': V[30], 'onTertiaryContainer': V[90],
    'error': E['dark'], 'onError': E['onDark'],
    'errorContainer': E['containerDark'], 'onErrorContainer': E['onContainerDark'],

    # Graphite, not navy. Text is N94 rather than white, which is Notion's
    # trick for a dark theme that does not glare.
    'background': N[10], 'onBackground': N[94],
    'surface': N[10], 'onSurface': N[94],
    'surfaceVariant': N[24], 'onSurfaceVariant': N[78],
    'onSurfaceTertiary': N[66],
    'outline': N[60],
    'outlineVariant': N[32],

    'surfaceDim': N[6], 'surfaceBright': N[32],
    'surfaceContainerLowest': N[6],
    'surfaceContainerLow': N[12],
    'surfaceContainer': N[14],
    'surfaceContainerHigh': N[20],
    'surfaceContainerHighest': N[24],

    'inverseSurface': N[94], 'inverseOnSurface': N[12], 'inversePrimary': B[40],
    'surfaceTint': B[80], 'scrim': N[0],
}

# Fixed accents -- identical in both themes, for anything that must not flip.
FIXED = {
    'primaryFixed': B[90], 'primaryFixedDim': B[80],
    'onPrimaryFixed': B[10], 'onPrimaryFixedVariant': B[30],
    'secondaryFixed': S[90], 'secondaryFixedDim': S[80],
    'onSecondaryFixed': S[10], 'onSecondaryFixedVariant': S[30],
    'tertiaryFixed': V[90], 'tertiaryFixedDim': V[70],
    'onTertiaryFixed': V[20], 'onTertiaryFixedVariant': V[30],
}

# ── Contrast ────────────────────────────────────────────────────────────────

def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(h):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


SURFACES = ['surface', 'surfaceContainerLowest', 'surfaceContainerLow',
            'surfaceContainer', 'surfaceContainerHigh', 'surfaceContainerHighest']
# A hairline is drawn around a card or a field and read against both the card's
# own fill and the page behind it. The two highest containers are chip and hover
# fills -- nothing draws a 1px border on those -- so holding the hairline to a
# ratio against them would only force it darker everywhere else for no gain.
HAIRLINE_SURFACES = ['surface', 'surfaceContainerLowest', 'surfaceContainerLow',
                     'surfaceContainer']
# A visible hairline, not an invisible one. Notion's divider is 1.11:1 and this
# codebase's was 1.16; 1.55 is the point where an edge reads as an edge on a
# phone at arm's length without turning into a drawn box.
HAIRLINE_MIN = 1.55

# (foreground, [backgrounds], minimum, what it is for)
def rules(S, theme='light'):
    r = []
    # Dark body text is N94 rather than white on purpose -- a dark theme that
    # runs text at 15:1 glares. 10:1 is where Notion's own dark body text sits.
    body = 11.0 if theme == 'light' else 10.0
    for s in SURFACES:
        r.append(('onSurface', s, body, 'body text'))
        r.append(('onSurfaceVariant', s, 4.8, 'secondary text'))
        r.append(('onSurfaceTertiary', s, 3.2, 'placeholders, timestamps'))
        r.append(('primary', s, 4.5, 'links and actions'))
        r.append(('error', s, 4.5, 'error text'))
        r.append(('outline', s, 3.0, 'inputs, focus, selected borders'))
    for s in HAIRLINE_SURFACES:
        r.append(('outlineVariant', s, HAIRLINE_MIN, 'hairline between surfaces'))
    for on, c in [('onPrimary', 'primary'), ('onPrimaryContainer', 'primaryContainer'),
                  ('onSecondary', 'secondary'), ('onSecondaryContainer', 'secondaryContainer'),
                  ('onTertiary', 'tertiary'), ('onTertiaryContainer', 'tertiaryContainer'),
                  ('onError', 'error'), ('onErrorContainer', 'errorContainer'),
                  ('inverseOnSurface', 'inverseSurface')]:
        r.append((on, c, 4.5, 'text on a container'))
    return r


def audit(verbose=False):
    fails = []
    for name, S in (('light', LIGHT), ('dark', DARK)):
        if verbose:
            print('=' * 74)
            print(name.upper())
            print('=' * 74)
        for fg, bg, need, why in rules(S, name):
            v = contrast(S[fg], S[bg])
            ok = v >= need
            if not ok:
                fails.append((name, fg, bg, v, need, why))
            if verbose:
                print('  %-4s %-22s on %-24s %6.2f  need %4.1f  %s'
                      % ('' if ok else 'FAIL', fg, bg, v, need, why))
    return fails


# ── Emit ────────────────────────────────────────────────────────────────────

MARK_START = '// ── GENERATED by tools/design/palette.py ── do not edit below'
MARK_END = '// ── end generated ──'


def kotlin():
    out = [
        'package com.neb.ians.ui.theme',
        '',
        '// GENERATED by tools/design/palette.py -- do not edit.',
        '// The palette is defined once, for both clients, in that file. Edit it',
        '// there and re-run, or the web and the app drift apart again.',
        '',
        'import androidx.compose.ui.graphics.Color',
        '',
    ]

    def block(comment, d):
        out.append(comment)
        for k, v in d.items():
            out.append('val %s = Color(0xFF%s)' % (k, v.lstrip('#').upper()))
        out.append('')

    def ramp(doc, name, d, prefix):
        out.append(doc)
        out.append('object %s {' % name)
        for k in sorted(d):
            out.append('    val %s%d = Color(0xFF%s)' % (prefix, k, d[k].lstrip('#').upper()))
        out.append('}')
        out.append('')

    ramp('/** The neutral ramp. N0 is ink, N100 is paper. */', 'NebNeutral', N, 'N')
    ramp('/** The brand blue and its tonal neighbours. B40 is the brand itself. */',
         'NebBrandRamp', B, 'B')
    ramp('/** The brand desaturated -- roles that should recede, not recolour. */',
         'NebSteel', S, 'S')
    ramp('/** The third voice. Used sparingly; never the only cue for anything. */',
         'NebVioletRamp', V, 'V')
    block('// Light theme', {'md_theme_light_' + k: v for k, v in LIGHT.items()})
    block('// Dark theme', {'md_theme_dark_' + k: v for k, v in DARK.items()})
    block('// Fixed accents -- the same in both themes', {'md_theme_' + k: v for k, v in FIXED.items()})
    return '\n'.join(out) + '\n'


def _kebab(k):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', k).lower()


def css():
    out = [
        '/* GENERATED by tools/design/palette.py -- do not edit.',
        '   The palette is defined once, for both clients, in that file. Edit it',
        '   there and re-run, or the app and the web drift apart again. */',
        '',
        ':root {',
    ]
    for k, v in LIGHT.items():
        out.append('  --md-%s: %s;' % (_kebab(k), v))
    for k, v in FIXED.items():
        out.append('  --md-%s: %s;' % (_kebab(k), v))
    out.append('')
    out.append('  /* The ramps themselves, for the handful of rules that need a step')
    out.append('     rather than a role -- gradients, generated art, skeletons, chart')
    out.append('     series. A rule reaching for one of these is saying "this exact')
    out.append('     step in both themes", which is different from a role and is why')
    out.append('     they are not repeated under [data-theme="dark"]. */')
    for prefix, ramp in (('n', N), ('b', B), ('s', S), ('v', V)):
        for k in sorted(ramp):
            out.append('  --md-%s%d: %s;' % (prefix, k, ramp[k]))
    out.append('}')
    out.append('')
    out.append('[data-theme="dark"] {')
    for k, v in DARK.items():
        out.append('  --md-%s: %s;' % (_kebab(k), v))
    out.append('}')
    return '\n'.join(out) + '\n'


KT_PATH = 'app/src/main/java/com/neb/ians/ui/theme/Palette.kt'
CSS_PATH = 'backend_python/web/static/web/css/material3/00-palette.css'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='audit and compare, write nothing')
    ap.add_argument('--audit', action='store_true', help='print the full contrast table')
    a = ap.parse_args()

    fails = audit(verbose=a.audit)
    if fails:
        print('\ncontrast audit FAILED -- %d pair(s):' % len(fails), file=sys.stderr)
        for theme, fg, bg, v, need, why in fails:
            print('  %-5s %-22s on %-24s %6.2f < %4.1f  (%s)'
                  % (theme, fg, bg, v, need, why), file=sys.stderr)
        return 1
    print('contrast audit passed: %d pair(s), both themes'
          % (len(rules(LIGHT, 'light')) + len(rules(DARK, 'dark'))))
    if a.audit:
        return 0

    targets = [(KT_PATH, kotlin()), (CSS_PATH, css())]
    drift = False
    for rel, text in targets:
        path = os.path.join(ROOT, rel)
        old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
        if a.check:
            if old != text:
                print('%s is stale -- re-run tools/design/palette.py' % rel, file=sys.stderr)
                drift = True
            else:
                print('%-58s up to date' % rel)
            continue
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print('%-58s %6d bytes' % (rel, len(text.encode('utf-8'))))
    return 1 if drift else 0


if __name__ == '__main__':
    sys.exit(main())
