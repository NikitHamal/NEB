"""Creator marketplace -- the design vocabulary a storefront may speak.

A creator page is not styled by the app's theme. It carries its own: palette,
colour scheme, type, texture, card treatment, hero shape. That is what makes
one page look like a physics tutor's notebook and the next like an institute's
prospectus, without either of them writing a line of CSS.

Everything here is data on purpose. `css/pages/marketplace/theme.css` turns a
palette into custom properties and `CreatorPageTheme.kt` turns the same palette
into a Compose colour set, both keyed by the ids below. Add a palette here and
it exists on both surfaces; there is no third place to edit.

The light and dark ramps are written out rather than derived. Deriving them
twice -- once in Python for the stylesheet, once in Kotlin -- is how two
surfaces quietly drift apart, and a creator who picks "Midnight" on their phone
has to see that same page on a laptop.
"""

# --- palettes ---------------------------------------------------------------
#
# `accent` carries the brand; `soft` is the accent at tint strength, used for
# chips and the hero wash; `line` is the hairline between sections; `ink` and
# `muted` are the two text weights. Every ink/surface pair below clears WCAG AA
# for body text, in both ramps.

PALETTES = {
    'indigo': {
        'label': 'Indigo', 'accent': '#004BD4', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F4F6FC', 'surface': '#FFFFFF', 'ink': '#0B1020',
                  'muted': '#535E78', 'line': '#E2E7F2', 'soft': '#E8EEFF'},
        'dark': {'bg': '#080B14', 'surface': '#121826', 'ink': '#EEF2FB',
                 'muted': '#9AA6C0', 'line': '#232B3D', 'soft': '#17203A'},
    },
    'teal': {
        'label': 'Teal', 'accent': '#0F766E', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F2F8F7', 'surface': '#FFFFFF', 'ink': '#06201D',
                  'muted': '#4A6360', 'line': '#DCEAE7', 'soft': '#DBF0EC'},
        'dark': {'bg': '#04110F', 'surface': '#0E1D1B', 'ink': '#E6F5F2',
                 'muted': '#93B3AE', 'line': '#1C312E', 'soft': '#123330'},
    },
    'amber': {
        'label': 'Amber', 'accent': '#B45309', 'on_accent': '#FFFFFF',
        'light': {'bg': '#FBF6EF', 'surface': '#FFFFFF', 'ink': '#241503',
                  'muted': '#6B5539', 'line': '#EDE2D2', 'soft': '#FAECD8'},
        'dark': {'bg': '#120C04', 'surface': '#1F160B', 'ink': '#F8EFE2',
                 'muted': '#BFA684', 'line': '#342716', 'soft': '#35270F'},
    },
    'rose': {
        'label': 'Rose', 'accent': '#9D174D', 'on_accent': '#FFFFFF',
        'light': {'bg': '#FCF4F7', 'surface': '#FFFFFF', 'ink': '#25060F',
                  'muted': '#6E4A57', 'line': '#EFDCE3', 'soft': '#FBE2EC'},
        'dark': {'bg': '#130509', 'surface': '#200B13', 'ink': '#F9E9EF',
                 'muted': '#C396A6', 'line': '#36141F', 'soft': '#3A0F1F'},
    },
    'violet': {
        'label': 'Violet', 'accent': '#5B21B6', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F7F4FD', 'surface': '#FFFFFF', 'ink': '#150929',
                  'muted': '#5A4C74', 'line': '#E6DFF5', 'soft': '#EDE6FD'},
        'dark': {'bg': '#0C0718', 'surface': '#171027', 'ink': '#EFEAFB',
                 'muted': '#A99CC4', 'line': '#2A2040', 'soft': '#241640'},
    },
    'forest': {
        'label': 'Forest', 'accent': '#166534', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F3F8F3', 'surface': '#FFFFFF', 'ink': '#0A1B0F',
                  'muted': '#4C6353', 'line': '#DEEADF', 'soft': '#DCF0E1'},
        'dark': {'bg': '#050F08', 'surface': '#101E14', 'ink': '#E9F5EC',
                 'muted': '#9BB6A3', 'line': '#1D3122', 'soft': '#123320'},
    },
    'slate': {
        'label': 'Slate', 'accent': '#334155', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F5F6F8', 'surface': '#FFFFFF', 'ink': '#0F1520',
                  'muted': '#55606F', 'line': '#E3E6EB', 'soft': '#E7EAF0'},
        'dark': {'bg': '#080A0E', 'surface': '#141821', 'ink': '#EDEFF3',
                 'muted': '#9BA4B4', 'line': '#242A35', 'soft': '#1D232F'},
    },
    'ink': {
        'label': 'Ink', 'accent': '#111111', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F6F6F5', 'surface': '#FFFFFF', 'ink': '#0A0A0A',
                  'muted': '#585856', 'line': '#E4E4E1', 'soft': '#EDEDEA'},
        # Ink inverts to the editorial black page: the accent has to lift off it,
        # so in the dark ramp the "accent" is paper white, not the same near-black.
        'dark': {'bg': '#000000', 'surface': '#0D0D0D', 'ink': '#F7F7F5',
                 'muted': '#A1A1A0', 'line': '#242422', 'soft': '#1A1A18'},
        'dark_accent': '#FFFFFF', 'dark_on_accent': '#111111',
    },
    'sky': {
        'label': 'Sky', 'accent': '#0369A1', 'on_accent': '#FFFFFF',
        'light': {'bg': '#F2F8FC', 'surface': '#FFFFFF', 'ink': '#061A26',
                  'muted': '#496173', 'line': '#DBE9F2', 'soft': '#DDEDF9'},
        'dark': {'bg': '#030F17', 'surface': '#0D1C26', 'ink': '#E7F3FA',
                 'muted': '#93AEC0', 'line': '#1A2E3B', 'soft': '#0F2C3E'},
    },
    'crimson': {
        'label': 'Crimson', 'accent': '#B91C1C', 'on_accent': '#FFFFFF',
        'light': {'bg': '#FCF5F4', 'surface': '#FFFFFF', 'ink': '#250807',
                  'muted': '#6D4C49', 'line': '#EFDDDB', 'soft': '#FBE3E1'},
        'dark': {'bg': '#120605', 'surface': '#1F0D0C', 'ink': '#F9EAE9',
                 'muted': '#C39B98', 'line': '#361817', 'soft': '#3A1210'},
    },
}

DEFAULT_PALETTE = 'indigo'

# --- the rest of the vocabulary ---------------------------------------------

SCHEMES = ('light', 'dark')

#: How the top of the page is shaped. `art` and `cover` predate the theme work
#: and keep their meaning; the rest are new arrangements of the same material.
HERO_STYLES = ('art', 'cover', 'plain', 'split', 'center', 'gradient', 'banner')

#: Type personality. The web side maps these to font stacks and the app to the
#: nearest `FontFamily`; what has to survive the trip is the *character*.
FONTS = ('sans', 'serif', 'display', 'mono', 'rounded')

#: A texture behind the page. Drawn, not downloaded -- CSS gradients on web, a
#: Canvas on Android -- so a page never waits on an image to look finished.
PATTERNS = ('none', 'dots', 'grid', 'rays', 'waves', 'glow', 'mesh')

#: How a section reads as an object: raised, drawn, plain, or frosted.
CARD_STYLES = ('elevated', 'outlined', 'flat', 'glass')

RADII = ('soft', 'round', 'sharp', 'pill')
DENSITIES = ('comfortable', 'compact', 'airy')
WIDTHS = ('standard', 'wide', 'narrow')

#: Per-section overrides. These are what make a page's rhythm its own: a
#: centred quote between two left-aligned sections, one shelf on the accent
#: colour, a gallery that goes full-bleed.
BLOCK_ALIGNS = ('start', 'center')
BLOCK_TONES = ('plain', 'soft', 'accent', 'contrast')
BLOCK_WIDTHS = ('standard', 'wide', 'full')

PALETTE_LABELS = [{'id': key, 'label': value['label'], 'accent': value['accent'],
                   'soft': value['light']['soft'], 'ink': value['light']['ink']}
                  for key, value in PALETTES.items()]

HERO_LABELS = {
    'art': 'Banner art', 'cover': 'Cover photo', 'plain': 'Plain',
    'split': 'Side by side', 'center': 'Centred', 'gradient': 'Gradient',
    'banner': 'Wide banner',
}
FONT_LABELS = {'sans': 'Clean sans', 'serif': 'Editorial serif', 'display': 'Big display',
               'mono': 'Technical mono', 'rounded': 'Friendly rounded'}
PATTERN_LABELS = {'none': 'None', 'dots': 'Dots', 'grid': 'Grid', 'rays': 'Rays',
                  'waves': 'Waves', 'glow': 'Glow', 'mesh': 'Mesh'}
CARD_LABELS = {'elevated': 'Raised', 'outlined': 'Outlined', 'flat': 'Flat', 'glass': 'Frosted'}
TONE_LABELS = {'plain': 'Plain', 'soft': 'Tinted', 'accent': 'Accent', 'contrast': 'Contrast'}


def palette(palette_id, scheme='light'):
    """The resolved colour set for one palette in one scheme.

    Returns a flat dict -- `accent`, `on_accent`, `bg`, `surface`, `ink`,
    `muted`, `line`, `soft` -- because that is exactly the set both renderers
    need and neither should have to know about the light/dark nesting.
    """
    entry = PALETTES.get(palette_id) or PALETTES[DEFAULT_PALETTE]
    ramp = entry['dark'] if scheme == 'dark' else entry['light']
    resolved = dict(ramp)
    if scheme == 'dark':
        resolved['accent'] = entry.get('dark_accent', entry['accent'])
        resolved['on_accent'] = entry.get('dark_on_accent', entry['on_accent'])
    else:
        resolved['accent'] = entry['accent']
        resolved['on_accent'] = entry['on_accent']
    return resolved


def theme_vocabulary():
    """Everything an editor needs to draw its Look tab, in one payload.

    Both studios build their controls from this rather than hardcoding option
    lists, so a palette added above shows up in the app without an app release.
    """
    return {
        'palettes': PALETTE_LABELS,
        'schemes': [{'id': s, 'label': s.title()} for s in SCHEMES],
        'heroes': [{'id': h, 'label': HERO_LABELS[h]} for h in HERO_STYLES],
        'fonts': [{'id': f, 'label': FONT_LABELS[f]} for f in FONTS],
        'patterns': [{'id': p, 'label': PATTERN_LABELS[p]} for p in PATTERNS],
        'cards': [{'id': c, 'label': CARD_LABELS[c]} for c in CARD_STYLES],
        'radii': [{'id': r, 'label': r.title()} for r in RADII],
        'densities': [{'id': d, 'label': d.title()} for d in DENSITIES],
        'widths': [{'id': w, 'label': w.title()} for w in WIDTHS],
        'block_tones': [{'id': t, 'label': TONE_LABELS[t]} for t in BLOCK_TONES],
        'block_aligns': [{'id': a, 'label': a.title()} for a in BLOCK_ALIGNS],
        'block_widths': [{'id': w, 'label': w.title()} for w in BLOCK_WIDTHS],
    }
