# M3X Design System (NEBians Material 3 Expressive)

One file, complete. Paste the whole thing (or just the section "THE PROMPT" plus the tokens in section 3) into any AI coding agent before it builds a new app or site, and the result has the NEBians look: brand blue, tonal surfaces, springy expressive shapes, no shadows, no emojis, no slop.

Source of truth in this repo: `backend_python/web/static/web/css/m3x/tokens.css` (colour, shape, motion), `m3x/shapes.css` (generated shapes and springs), `m3x/app-*.css` (components), `backend_python/scripts/gen_m3x_shapes.py` (shape generator), `tools/design/sync_android_palette.py` (web to Android palette). When this doc and those files disagree, the files win; fix the doc.

Contents: 1 How to use, 2 THE PROMPT, 3 Tokens, 4 Type, 5 Shape, 6 Motion, 7 Components, 8 Layout, 9 Content rules, 10 Bans, 11 Android, 12 Review checklist.

---

## 1. How to use

1. New project: paste section 2 as the first message, then paste section 3 (tokens) and 6 (springs) as files (`tokens.css`, `shapes.css`).
2. Existing project: paste section 2 and section 12, ask the agent to restyle one screen at a time and to run the checklist before it says done.
3. Never let the agent invent a colour, radius or easing. Every value comes from section 3, 5 or 6. If it needs something new, it adds a role to `tokens.css` first.

---

## 2. THE PROMPT (copy from here)

```text
You are building UI in the "M3X" design system: Material 3 Expressive in the NEBians brand blue. Follow every rule. If a rule conflicts with your habits, the rule wins.

LOOK
- Calm, tonal, confident. Separation comes from tone, a 1px hairline and shape. Never from shadow.
- One brand blue (#0058df) and its tonal family. The page is blue-tinted off-white (#f6f8ff) in light and neutral graphite (#121318) in dark. Cards are white (light) or graphite #1b1b21 (dark) with a 1px outline-variant hairline.
- Everything is rounded with a FINITE radius: 12, 16, 20, 24, 28, 32, 44. A pill is 28px radius on anything up to 56px tall. Never 9999px, never 50% on a rectangle that will animate, never 0 on a button.
- Expressive means shape and motion: cookie, sunny, flower, clover, burst, squircle, pebble silhouettes (clip-path polygons with identical point counts so they morph) for avatars, glyph tiles, hero art and the loader; springy overshoot on press, hover and enter.
- Typography: Poppins inside the app (weights 400, 500, 600, 700; headings 600 with -0.02em tracking). Marketing pages may use Bricolage Grotesque (display) + Figtree (body). Never Inter, Roboto, system-only, or a second family in the same screen.
- Icons: Material Symbols Outlined only (FILL 0, wght 400; FILL 1 for a selected or verified state). No emoji, no icon packs mixed in.

TOKENS (never hard-code a colour; a fill and its label are always a role pair)
- Use CSS variables --md-primary / --md-on-primary, --md-primary-container / --md-on-primary-container, --md-secondary-container / --md-on-secondary-container, --md-tertiary-container / --md-on-tertiary-container, --md-error-container / --md-on-error-container, --md-surface, --md-surface-container-lowest|low|(none)|high|highest, --md-on-surface, --md-on-surface-variant, --md-outline, --md-outline-variant. Both themes must be complete from day one; test dark before shipping.
- Contrast: body text on its surface at least 7:1 where possible, never under 4.5:1. Secondary text uses --md-on-surface-variant, never a faded opacity of the primary text. Never put coloured text on a coloured tonal fill unless it is that fill's on-role.

SURFACES AND FIELDS
- Page: --md-surface. Card: --md-surface-container-lowest + 1px --md-outline-variant + radius 24 to 28. Inset tile inside a card: --md-surface-container-low + radius 20, no border.
- Floating things (menu, dialog, bottom sheet, popover): --x-float (white in light, #25262c in dark) + 1px --x-float-line. No shadow, no blur backdrop.
- Text fields, selects, option cards: white (--x-field) with ONE 1.5px stroke (--x-field-line). Hover, focus and selected change only the stroke colour (to primary). Never an outline stacked on a border, never fill a field with a surface-container tone, never a floating-label animation.

BUTTONS
- Filled (primary), Tonal (secondary container), Outlined (1px outline), Text. Heights 40 for page and dialog actions, 52 for the single main call to action on a form, 32 compact, 28 for Follow. Radius = pill (28). Label 14px / 600. Optional 18px leading icon.
- Press: scale(.95) with spring. Hover: 8% state layer or a tonal warm-up and a gentle radius morph between two ROUNDED values (for example 28px to 20px). A button must never become a sharp rectangle or a square on hover.
- Disabled: opacity .5, no pointer events. Loading: swap the icon for the morphing loader, keep the label.

CHIPS, SEGMENTS, TABS
- Chip: 40px tall, 20px radius, white with 1px outline-variant; selected = secondary-container fill, on-secondary-container text, no border; a leading check appears on select.
- Segmented switch: surface-container track, 4px padding, 24 to 28px radius, ONE sliding indicator (primary-container, on-primary-container text) that moves on --spring.
- Filter pills, category tags, status labels (Solved, Answer, Correct, Helpful) keep tonal container fills. Those are chips and keep their background.

USER AND ROLE BADGES
- Verified, Admin, Teacher, Moderator and similar are an icon plus text in a role colour with NO background fill and no border. Verified is the Material Symbol "verified" (FILL 1) in --md-primary placed beside the name. On an avatar rim the only badge is a small filled disc with a 2px ring cut from the surface colour.

AVATARS AND PICTURES
- Profile pictures are clipped to an expressive shape chosen by a stable hash of the username (so a person has one shape everywhere). Three tonal fills (primary, secondary, tertiary containers). NEVER draw a circular stroke, ring, outline or border around a profile picture. Hover tips the shape into its neighbour shape with a clip-path transition.
- NO generated avatars: no pixel art, blobs, dicebear, 2D characters, avatar studio or avatar pickers, on web or Android. A member with no photo shows their Google account photo when they signed in with Google, else the first letter in a neutral disc (`Avatar`, `.neb-letter`). Neby the AI bot keeps its own mascot; that is a bot identity, not a user avatar.

MOTION
- Springs, not tweens, for anything spatial: --spring (.55s), --spring-fast (.35s), --spring-soft (.8s). Colour and opacity changes use .2s ease. Use --ease-io (cubic-bezier(.65,0,.35,1)) for progress.
- Enter: opacity + translateY(14px) to 0 on --spring. Press: scale(.95-.97). Lists stagger at most 40ms per item and never more than 6 items.
- Respect prefers-reduced-motion: no springs, no morphs, no entrance animation.

LAYOUT
- 4px grid. Page gutters 16 (phone) and 24 (desktop). Content columns 640 (forms and tools), 760 (detail), 1040 (directories), 1280 (shell). Section gap 26, card gap 14, field gap 14 to 18.
- Mobile first. Below 600px dialogs become bottom sheets and menus become sheets. Touch targets at least 44x44.
- The same drawing on phone and desktop. Do not hide features on mobile.

COPY
- Short. Sentence case. No taglines, no helper paragraphs, no "Welcome to", no "Powered by" fillers, no exclamation marks. If a screen needs explanatory text to make sense, fix the layout instead. Placeholders show the format ("2065/03/15"); labels are nouns.

HARD BANS
- No box-shadow, drop-shadow, text-shadow, elevation tokens (set them to none).
- No emojis in markup, scripts, strings, notifications, or commit messages for UI.
- No gradients (no blue, purple or any hero wash; scrims over photos are the only exception).
- No rings or strokes around profile pictures.
- No background fill on user, role or verification badges.
- No hover that morphs a rounded control into border-radius 0 (finite radii only).
- No tinted colour wash as a screen background (splash, intro, hero): the page colour only. The blue-tinted container the old splash filled the screen with is banned for good.
- No glassmorphism except the floating bottom navigation (a real blur of the page behind it on Android 12+, solid tint elsewhere), no neon glows, bento-for-the-sake-of-bento, floating blobs, decorative orbs, "LIVE" dots.
- No purple. The accent family is azure, sky, aqua, periwinkle, all derived from the brand blue.
- No lorem ipsum, no stock avatars, no fake testimonials, no fake numbers.

PRESS, SPACING, SCROLL (hard rules, details in section 13)
- Press feedback (ripple, state layer, tap flash) is clipped to the control's own shape. Clip first, then make it clickable; never the other way round.
- Tonal tiles that sit side by side keep a gap of at least 4px (6 for 38 to 44px tiles). A selected, hovered or pressed tile may never touch its neighbour.
- Icons and glyphs drawn on a themed surface must reach 3:1 against it (text 4.5:1). Never a fixed low alpha for a disabled icon.
- Never nest two scrollers of the same axis. A parent that scrolls horizontally must not contain a child that scrolls horizontally.
- Text with pictures inside keeps its own line height; only the line that holds a picture grows, and the caret stays as tall as the text.

Before you answer, run the checklist: tokens only, both themes, finite radii, no shadows, no gradients, no emojis, no picture rings, no filled role badges, springs plus reduced motion, touch targets 44px, copy short.
```

---

## 3. Tokens (`tokens.css`)

Brand colour comes from the NEBians N: front face `#0058df`, dark faces `#052566` and `#07337f`, light facet `#a8c5ff`. Everything is a tonal ramp of that blue so a surface is never a neutral grey.

```css
:root {
  color-scheme: light;
  --md-primary: #0058df;                --md-on-primary: #ffffff;
  --md-primary-container: #dbe4ff;      --md-on-primary-container: #001a52;
  --md-secondary: #485a80;              --md-on-secondary: #ffffff;
  --md-secondary-container: #dfe7fa;    --md-on-secondary-container: #0f1c3b;
  --md-tertiary: #006782;               --md-on-tertiary: #ffffff;
  --md-tertiary-container: #c6ecff;     --md-on-tertiary-container: #001f2a;
  --md-error: #ba1a1a;                  --md-on-error: #ffffff;
  --md-error-container: #ffdad6;        --md-on-error-container: #8c0009;
  --md-background: #f6f8ff;             --md-on-background: #0b1530;
  --md-surface: #f6f8ff;                --md-on-surface: #0b1530;
  --md-surface-variant: #e1e8f8;        --md-on-surface-variant: #414b66;
  --md-on-surface-tertiary: #4f5976;    /* placeholders */
  --md-outline: #707a96;                --md-outline-variant: #c6d0ea;
  --md-surface-dim: #d5dcee;            --md-surface-bright: #fbfcff;
  --md-surface-container-lowest: #ffffff;   /* cards, fields */
  --md-surface-container-low: #f0f4fe;      /* inset tiles */
  --md-surface-container: #e9eefb;
  --md-surface-container-high: #e2e8f7;
  --md-surface-container-highest: #dae1f3;
  --x-float: #ffffff;  --x-float-line: #d3dbef;       /* menus, dialogs, sheets */
  --x-field: var(--md-surface-container-lowest);
  --x-field-line: color-mix(in srgb, var(--md-outline) 58%, var(--md-surface));
  --x-line-w: 1.5px;
  --md-inverse-surface: #1f2840;  --md-inverse-on-surface: #edf1fc;  --md-inverse-primary: #b2c5ff;

  /* tonal accents: X = vivid fill (dark text), X-c = soft container, X-d = deep fill (white text) */
  --azure: #7aa2ff;  --azure-c: #d7e3ff;  --azure-d: #0047b8;
  --sky:   #5cc8ff;  --sky-c:   #cdeeff;  --sky-d:   #00598a;
  --aqua:  #55d9c6;  --aqua-c:  #c6f3eb;  --aqua-d:  #0a6a62;
  --peri:  #a9b9ff;  --peri-c:  #e3e9ff;  --peri-d:  #2a47a3;
  --ink: #06235f;    --on-ink:  #e6eeff;

  /* shape */
  --md-shape-xs: 8px;  --md-shape-sm: 12px;  --md-shape-md: 16px;
  --md-shape-lg: 24px; --md-shape-xl: 32px;  --md-shape-xxl: 44px;
  --md-shape-full: 28px;   /* a pill is FINITE: perfect up to 56px tall */

  /* no elevation: tone, hairline and shape do the separating */
  --md-elevation-1: none; --md-elevation-2: none; --md-elevation-3: none;
  --md-shadow: transparent; --md-shadow-lg: transparent;

  --ease-io: cubic-bezier(.65, 0, .35, 1);
  --display: Poppins, ui-sans-serif, system-ui, sans-serif;
  --body:    Poppins, ui-sans-serif, system-ui, sans-serif;
}

[data-theme="dark"] {
  color-scheme: dark;
  --md-primary: #b6c4ff;                --md-on-primary: #002780;
  --md-primary-container: #00389f;      --md-on-primary-container: #dce1ff;
  --md-secondary: #c0c6dc;              --md-on-secondary: #2a3042;
  --md-secondary-container: #404659;    --md-on-secondary-container: #dce1f9;
  --md-tertiary: #e2bbdb;               --md-on-tertiary: #422740;
  --md-tertiary-container: #5b3d57;     --md-on-tertiary-container: #ffd7f5;
  --md-error: #ffb4ab;                  --md-on-error: #690005;
  --md-error-container: #93000a;        --md-on-error-container: #ffdad6;
  --md-background: #121318;             --md-on-background: #e4e1e9;
  --md-surface: #121318;                --md-on-surface: #e4e1e9;
  --md-surface-variant: #45464f;        --md-on-surface-variant: #c6c6d0;
  --md-on-surface-tertiary: #909099;
  --md-outline: #8f909a;                --md-outline-variant: #45464f;
  --md-surface-dim: #121318;            --md-surface-bright: #38393f;
  --md-surface-container-lowest: #0d0e13;
  --md-surface-container-low: #1b1b21;
  --md-surface-container: #1f1f25;
  --md-surface-container-high: #292a2f;
  --md-surface-container-highest: #2e2f36;
  --x-float: #25262c;  --x-float-line: #45464f;
  --md-inverse-surface: #e4e1e9;  --md-inverse-on-surface: #303036;  --md-inverse-primary: #004bd4;
  --azure-c: #1c3470;  --azure-d: #9db8ff;
  --sky-c: #0b3a52;    --sky-d: #8fdcff;
  --aqua-c: #0b3b37;   --aqua-d: #8ae9da;
  --peri-c: #25306a;   --peri-d: #c1ccff;
  --ink: #16397f;
}
```

Pairing rules

| Use | Fill | Label |
| --- | --- | --- |
| Main action, selected nav, positive grade | `--md-primary` | `--md-on-primary` |
| Selected segment, tile glyph, step number | `--md-primary-container` | `--md-on-primary-container` |
| Tonal button, chip selected, count pill | `--md-secondary-container` | `--md-on-secondary-container` |
| Neutral status, mid grade | `--md-tertiary` or its container | its on-role |
| Error, failing grade | `--md-error` or its container | its on-role |
| Card | `--md-surface-container-lowest` + 1px `--md-outline-variant` | `--md-on-surface` |
| Inset tile | `--md-surface-container-low` | `--md-on-surface` |
| Secondary text | none | `--md-on-surface-variant` |

Semantic colour: success, warning and failure map to primary, tertiary and error roles. Do not import green and amber hexes.

---

## 4. Type

- Family: Poppins (self-host 400, 500, 600, 700; `font-display: swap`). Devanagari falls through to Poppins too. Landing and marketing may use Bricolage Grotesque (display, wght 500 to 800) and Figtree (body).
- Scale (rem, line-height): display 2.5 / 1.1 (600, -0.02em), page title 2 / 1.15 (600, -0.02em; 1.625 on phones), section title 1.125 to 1.5 (600), body 0.9375 / 1.5 (400 to 500), secondary 0.875 / 1.45, caption and labels 0.8125 / 1.35, micro 0.75.
- Numbers that change (counts, timers, GPA) use `font-variant-numeric: tabular-nums`.
- No ALL CAPS labels with wide tracking except one-letter chips. Sentence case everywhere. No letter-spaced uppercase "eyebrow" above every heading.
- Text colours: `--md-on-surface` for content, `--md-on-surface-variant` for support. No third grey.

---

## 5. Shape

Radii (finite): 8 chip-inner, 12 tag, 16 small card, 20 field and inset tile, 24 card, 28 pill and large card, 32 hero card, 44 hero panel. Pills are 28.

Expressive silhouettes are generated, not drawn. Every shape is sampled at the same number of points (120) so `clip-path` can transition between any two of them. Save as `scripts/gen_m3x_shapes.py`, run it, commit the CSS it writes.

```python
import math, pathlib
N = 120
OUT = pathlib.Path('shapes.css')
def lobed(k, a, phase=0.0): return lambda t: 1 + a * math.cos(k * t + phase)
def superellipse(n): return lambda t: (abs(math.cos(t)) ** n + abs(math.sin(t)) ** n) ** (-1 / n)
SHAPES = {
  'circle': lambda t: 1.0, 'cookie': lobed(9, 0.065), 'sunny': lobed(8, 0.11),
  'flower': lobed(5, 0.17), 'clover': lobed(4, 0.2), 'burst': lobed(12, 0.12),
  'squircle': superellipse(4), 'gem': superellipse(1.55),
  'pebble': lambda t: 1 + 0.1 * math.cos(2 * t - 0.6) + 0.05 * math.cos(3 * t + 0.4),
}
def polygon(fn):
  rs = [fn(2 * math.pi * i / N - math.pi / 2) for i in range(N)]; top = max(rs); pts = []
  for i, r in enumerate(rs):
    t = 2 * math.pi * i / N - math.pi / 2
    pts.append(f'{50 + 50 * r / top * math.cos(t):.2f}% {50 + 50 * r / top * math.sin(t):.2f}%')
  return 'polygon(' + ','.join(pts) + ')'
def spring(zeta, omega, steps=48, duration=1.0):
  wd = omega * math.sqrt(1 - zeta ** 2); out = []
  for i in range(steps + 1):
    t = duration * i / steps
    v = 1 - math.exp(-zeta * omega * t) * (math.cos(wd * t) + zeta * omega / wd * math.sin(wd * t))
    out.append(f'{v:.3f}'.rstrip('0').rstrip('.') or '0')
  out[-1] = '1'; return 'linear(' + ','.join(out) + ')'
lines = [':root{'] + [f'--shape-{n}:{polygon(f)};' for n, f in SHAPES.items()]
lines += ['--spring-fast:cubic-bezier(.3,1.3,.5,1);--spring:cubic-bezier(.3,1.5,.5,1);--spring-soft:cubic-bezier(.25,1.2,.4,1);', '}',
  '@supports (transition-timing-function:linear(0,1)){:root{',
  f'--spring-fast:{spring(0.62, 24)};', f'--spring:{spring(0.5, 15)};', f'--spring-soft:{spring(0.72, 11)};', '}}']
OUT.write_text('\n'.join(lines) + '\n')
```

Using a shape:

```css
.shape { clip-path: var(--shape, var(--shape-cookie)); transition: clip-path .8s var(--spring); }
@media (hover: hover) { a:hover > .shape { clip-path: var(--alt); } }   /* neighbour shape */
[data-shape="cookie"] { --shape: var(--shape-cookie); --alt: var(--shape-flower); }
[data-shape="sunny"]  { --shape: var(--shape-sunny);  --alt: var(--shape-burst); }
[data-shape="flower"] { --shape: var(--shape-flower); --alt: var(--shape-clover); }
[data-shape="clover"] { --shape: var(--shape-clover); --alt: var(--shape-cookie); }
[data-shape="burst"]  { --shape: var(--shape-burst);  --alt: var(--shape-sunny); }
[data-shape="pebble"] { --shape: var(--shape-pebble); --alt: var(--shape-squircle); }
[data-shape="squircle"] { --shape: var(--shape-squircle); --alt: var(--shape-circle); }
[data-tone="0"] { --av-fill: var(--md-secondary-container); --av-ink: var(--md-on-secondary-container); }
[data-tone="1"] { --av-fill: var(--md-primary-container);   --av-ink: var(--md-on-primary-container); }
[data-tone="2"] { --av-fill: var(--md-tertiary-container);  --av-ink: var(--md-on-tertiary-container); }
```

Hash the username (FNV-1a) once: `shape = names[h % 7]`, `tone = (h >> 3) % 3`. Same input, same shape on every screen and every platform.

Where shapes are used: avatars, glyph tiles (the icon tile standing in for a logo), the GPA or score medallion, empty-state art, the loader (`md-loader` morphs cookie, sunny, flower, clover while it turns), splash screens.

Clip-path clips borders, so a shaped element has no stroke by construction. If a container must keep its box (for a badge on the rim), clip the picture inside it instead.

---

## 6. Motion

- Springs: `--spring-fast` .35s (small controls), `--spring` .55s (default), `--spring-soft` .8s (large morphs, indicators). They overshoot slightly; that is the personality.
- Colour, background, border-colour, opacity: .2s ease.
- Progress and determinate bars: .3s `--ease-io`.
- Press: `transform: scale(.95)` (buttons, chips) or `.985` (large cards), `transition-duration: .12s` on press.
- Hover (pointer devices only, inside `@media (hover: hover)`): border-colour to primary, or an 8% state layer, or a radius morph between two rounded values (card 24 to 32, row 20 to 24, pill 28 to 20). Never to 0.
- Enter: `@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }` at .6s `--spring`.
- Sliding indicator: one absolutely positioned element moved with `transform: translateX(...)`, `.55s var(--spring)`.
- `@media (prefers-reduced-motion: reduce)`: remove springs, clip-path transitions, entrance animation.
- No parallax, no scroll-jacking, no looping decoration except the loader.

---

## 7. Components

### Button

```css
.md-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 40px; padding: 0 20px;
  border: 0; border-radius: 28px; font: 600 .875rem/1 var(--body); cursor: pointer; text-decoration: none;
  transition: border-radius .5s var(--spring), transform .4s var(--spring), background-color .2s, color .2s; }
.md-btn .material-symbols-outlined { font-size: 18px; }
.md-btn-filled   { background: var(--md-primary); color: var(--md-on-primary); }
.md-btn-tonal    { background: var(--md-secondary-container); color: var(--md-on-secondary-container); }
.md-btn-outlined { background: transparent; color: var(--md-primary); border: 1px solid var(--md-outline); }
.md-btn-text     { background: transparent; color: var(--md-primary); }
.md-btn-small    { min-height: 32px; padding: 0 14px; font-size: .8125rem; }
.md-btn:active   { transform: scale(.95); transition-duration: .12s; }
.md-btn:disabled { opacity: .5; pointer-events: none; }
@media (hover: hover) { .md-btn:hover { border-radius: 20px; } }   /* rounded to rounded, never 0 */
```

Icon button: 42px, round, hover fills `--md-surface-container-high`, press `scale(.9)`.

### Field

```css
.md-input, .md-select, .md-textarea { min-height: 52px; padding: 0 16px; border-radius: 20px; font: 500 .9375rem var(--body);
  background: var(--x-field); color: var(--md-on-surface); border: var(--x-line-w) solid var(--x-field-line); outline: none;
  transition: border-color .2s; }
.md-input:hover, .md-select:hover { border-color: var(--md-outline); }
.md-input:focus, .md-select:focus, .md-textarea:focus { border-color: var(--md-primary); }
.md-input::placeholder { color: var(--md-on-surface-tertiary); opacity: 1; }
.md-input[aria-invalid="true"] { border-color: var(--md-error); }
label { display: block; padding: 0 4px 6px; font: 600 .8125rem var(--body); color: var(--md-on-surface-variant); }   /* sentence case, above the field */
select.md-select { appearance: none; padding-right: 42px; /* one chevron as a background svg in --md-outline */ }
```

Error text: `.8125rem`, `--md-error`, directly under the field. Required marker: none; mark optional ones instead.

### Chip

```css
.md-chip { display: inline-flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 16px; border-radius: 20px;
  background: var(--md-surface-container-lowest); color: var(--md-on-surface); border: 1px solid var(--md-outline-variant);
  font: 600 .875rem/1 var(--body); cursor: pointer; transition: border-radius .45s var(--spring), background-color .2s, border-color .2s, transform .4s var(--spring); }
.md-chip:hover { border-color: var(--md-primary); }
.md-chip:active { transform: scale(.95); }
.md-chip-active, .md-chip[aria-pressed="true"] { background: var(--md-secondary-container); color: var(--md-on-secondary-container); border-color: transparent; }
```

### Segmented switch

Track `--md-surface-container`, padding 4, radius 28; buttons 48px tall transparent; one `span.ind` with `--md-primary-container`, radius 24, `width: calc(50% - 4px)` moved by `transform: translateX(100%)` when the second option is on. Label colour of the active button is `--md-on-primary-container`.

### Card

```css
.card { background: var(--md-surface-container-lowest); border: 1px solid var(--md-outline-variant); border-radius: 28px; padding: 22px; }
.tile { background: var(--md-surface-container-low); border-radius: 20px; padding: 12px 16px; }
@media (hover: hover) { a.card:hover { border-color: var(--md-primary); border-radius: 32px; } }
```

Interactive cards press with `scale(.985)`. No shadow ever. Nested radius rule: inner radius = outer radius minus padding, never smaller than 12.

### Glyph tile (stands in for a logo or icon)

48px (row), 56px (feature), 84px (hero); radius 16, 20, 28; `--md-primary-container` fill, `--md-on-primary-container` glyph. Or clip it to an expressive shape.

### Lists and rows

Row: 10px 14px padding, 20px radius, transparent; hover `--md-surface-container-low` and radius 24; 14px gap between glyph, body, trailing count pill. Name 600 .9375rem, meta .8125rem `--md-on-surface-variant`, both one line with ellipsis. Count pill: secondary-container, 14px radius, 600 .8125rem.

### Tables

Wrap in a `--md-surface-container-low` panel, radius 24, padding 4 8, horizontal scroll if needed. Header .75rem 600 `--md-on-surface-variant`, 1px `--md-outline-variant` row separators, no zebra, no heavy header fill. Numbers centred or right aligned and tabular.

### Status and grade labels (these keep a tonal fill)

Radius 12, padding 4 10, 600 .8125rem. Best: primary-container. Neutral: secondary-container. Caution: tertiary-container. Failing: error-container. Each with its on-role colour.

### Dialog, sheet, menu

Floating surface `--x-float` + 1px `--x-float-line`, radius 28 (dialog), 28 28 0 0 (bottom sheet), 20 (menu). Scrim is `color-mix(in srgb, var(--md-on-surface) 40%, transparent)`. Header: title 600 1.125rem and a 40px round close button; actions row right-aligned, primary action filled. Below 600px every dialog is a bottom sheet and every menu is a sheet. Escape closes, focus is trapped, scroll is locked, focus returns to the trigger. Dialog body scrolls; header and actions stay put.

### Alert and empty state

Alert: error-container fill, on-error-container text, 20px radius, 22px icon, one sentence. Empty state: 28px radius `--md-surface-container-low`, 40px icon in `--md-on-surface-variant`, one sentence in `--md-on-surface`, one tonal button.

### Progress

Track 8px tall, `--md-surface-container-high`, bar `--md-primary`, both radius 8. The count sits at the right as "12 of 40" in tabular numbers. The indeterminate wait is the morphing shape loader, never a spinner ring.

### Navigation

Top bar on desktop: brand tile (42px), nav pills, actions. Bottom nav on phones: five destinations max, selected item gets a primary-container pill behind the icon and a 600 label. Back affordance is one round 44px button with `arrow_back`, never a text link. Tabs are the segmented switch or chips, never underlined tabs.

### Verified and role badges (no fill)

```html
<span class="name">Asha Gurung <span class="material-symbols-outlined verified" aria-label="Verified">verified</span></span>
```

```css
.verified { font-size: 20px; color: var(--md-primary); font-variation-settings: 'FILL' 1; background: none; border: 0; }
```

Teacher, Admin, Moderator: text or icon in a role ink colour, no pill, no tint. The one exception is the 16px disc on an avatar rim, ringed with the colour of whatever it sits on.

---

## 8. Layout

- 4px grid. Gutters 16 phone, 24 tablet and up. Top padding 20, bottom padding 96 (clears the bottom nav).
- Column widths: forms and tools 640, detail pages 760, directories 1040, shell 1280. Centre with `margin: 0 auto`.
- Gaps: card to card 14, section to section 26, field to field 14 to 18, chip to chip 8, icon to label 8.
- Page head: back button, title (600, 2rem, -0.02em), at most one tonal action on the right. No subtitle.
- Order on a page: head, search or primary form, filters as chips, content. The most important thing is above the fold at 360x640.
- Breakpoints: 480 (single column forms), 600 (sheets), 768 (nav swap), 1024.
- Phone and desktop render the same design. Only the column count changes.

---

## 9. Content rules

- Sentence case. Verbs for buttons ("Check result", "Get verified"), nouns for labels ("Symbol number").
- No helper paragraph under a title. No placeholder that repeats the label. If the label and placeholder both need to exist, the placeholder is the example value.
- Counts are numbers with a unit once ("120 students"), never "Total number of students: 120".
- Errors say what to do ("Enter your date of birth"), not what went wrong in the system.
- Empty states are one sentence and one action.
- No emojis anywhere, including toasts, push text, seeds and test data. Use a Material Symbol or nothing.
- No exclamation marks, no "Oops", no "Awesome".

---

## 10. Bans (with the reason, so an agent can generalise)

| Ban | Why / what to do instead |
| --- | --- |
| `box-shadow`, `drop-shadow`, `text-shadow`, elevation | Separation is tone plus a 1px hairline. Set elevation tokens to `none`. |
| Gradients (blue, purple, any hero wash, gradient text, gradient buttons) | Flat role colours. Scrims over photos are the one exception. Logos are drawn with flat fills. |
| Emojis in UI, JS, Python, Kotlin, notifications | Material Symbols or no icon. |
| "LIVE" badges, pulsing dots | Say nothing, or show a count. |
| Ring, stroke or border around a profile picture | Expressive shape clip only. |
| Filled background on Verified, Admin, Teacher, role badges | Icon and text in a role ink colour. Filled tonal backgrounds stay on chips, filter pills, category tags and status labels (Solved, Answer, Correct, Helpful). |
| Hover that changes a rounded control to `border-radius: 0`, or 9999px that passes through 0 mid-spring | Finite radii; morph between two rounded values. |
| Hard-coded hex in components | Use roles. A fill and its label are a pair. |
| Stacked outline plus border on fields | One 1.5px stroke whose colour changes. |
| Fields filled with surface-container tones | Fields are white (`--x-field`). |
| Underlined tabs, floating-label inputs, ripple rectangles | Segmented switch, labels above, state layers. |
| Taglines, helper copy, secondary labels that exist to explain a confusing layout | Fix the layout. |
| Purple, neon, glass blur, decorative blobs and orbs | Azure, sky, aqua, periwinkle tonal tiles and expressive shapes. |
| Inter, Roboto, system-only type, mixed families | Poppins in app. |
| Native `alert`, `confirm`, `prompt` | The dialog component. |
| Placeholder or fake data (lorem, stock faces, invented stats) | Real data or an empty state. |

---

## 11. Android (Jetpack Compose)

The app is the same system, with three deliberate differences from the web page: the light page is pure white, every
surface role is a neutral grey (no blue in a card, popup or background), and shapes are drawn with `MaterialShapes`.

- **Palette:** generate `Palette.kt` from `tokens.css` with `tools/design/sync_android_palette.py` (copies every `--md-*` role, light and dark; `--check` fails on drift). `ANDROID_LIGHT_OVERRIDES` in that script pins the light surface ramp to neutral greys and `onSurface` to near-black. Brand blue stays in `primary`, the tonal containers (chips, tags, selected rows) and links.
- **Floating surfaces** (menu, popover, dialog, bottom sheet): `nebFloatColor()` (white in light, a raised tone in dark), hairline `nebFloatLine()`, no elevation. Components: `NebDropdownMenu`, `NebModalSheet`, `NebDialog`. A raw Material `DropdownMenu`, `ModalBottomSheet` or `AlertDialog` must pass `containerColor = nebFloatColor()` and no shadow.
- **Cards and fields:** card = `surface` + 1dp `outlineVariant` hairline + 24 to 28dp radius. Field = white + one 1dp stroke, primary on focus. Tonal fills are for chips, tags, selected rows and quiet panels only.
- **Composer:** one outlined container (24dp), avatar with chevron identity menu, field, ghost tool buttons (38dp, tonal rounded square while on), round send button (tonal when empty, primary when ready). The A tool reveals the markdown row, tools row and expand. Reply type is a sheet, never chips above the field. No mic.
- **Type:** Poppins via `FontFamily`; same scale as section 4. Reading mode may use a serif body, headings stay Poppins.
- **Shapes:** `RoundedCornerShape` with the section 5 radii for containers; expressive silhouettes (cookie, sunny, flower, clover, gem, burst) for profile pictures and tiles through `nebShape(polygon)`; morph with `NebMorphBlob`. Never a circle tile where the web has a shape, never a stroke on a profile picture.
- **Motion:** springs only (`nebSpatialSpec`, `nebEffectsSpec`, `nebAnimationsReduced()` collapses to a snap); press scale .95 through `nebPressable`; entrances through `Reveal(index)` (rise and settle, staggered 80 ms). Pointer-driven change (pinch, drag) follows the finger with no easing.
- **No** `.shadow()`, no non-zero `shadowElevation` or `tonalElevation` on a floating surface, no gradient other than a photo scrim, no emoji in strings or Kotlin, no `RoundedCornerShape(0.dp)` on press.
- **Icons:** the web's own glyphs through `NebIcon(NebIcons.X)` where one exists (`tools/design/svg_to_vector.py`), otherwise Material Symbols Outlined.
- **Parity method:** run the site locally, screenshot the same screen at 390 px, compare before you build. Whatever the web does not have, the app does not have.

---

## 12. Review checklist (agent must pass every line before it says done)

1. Every colour is a `--md-*` role (or a tonal accent); grep for `#` in component CSS finds nothing but the token files.
2. Light and dark both rendered and read; text is legible on every surface.
3. `grep -E "box-shadow|drop-shadow|text-shadow"` finds only `none`. `grep -E "gradient"` finds nothing except photo scrims.
4. No emoji characters in any file touched (`[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]`).
5. No ring, border or outline on profile pictures. Verified and role badges have no background.
6. Every radius is finite; no hover state sets a radius to 0; pills are 28px.
7. Springs on press, hover and enter; `prefers-reduced-motion` handled.
8. Touch targets at least 44px; screens checked at 360x640 and 1280x800; no horizontal scroll.
9. Copy: sentence case, no taglines, no helper text that a better layout would remove.
10. Fields are white with a single 1.5px stroke; focus changes the stroke colour only.
11. Dialogs trap focus, close on Escape, become bottom sheets under 600px.
12. Screenshots of light and dark are looked at, not assumed.
13. Android only: light surfaces are neutral grey (grep `0xFF[EF][0-9A-F]FE`-style blue-white values in Kotlin finds nothing), every menu, dialog and sheet uses `nebFloatColor()`, the comment bar matches the web composer, and a screen compared with its web twin at 390 px shows the same structure.


## Android additions (session 11)

- **System bars:** the app is edge to edge. Every screen whose top or bottom is not the app surface calls `NebSystemBars(darkIcons)` with what is behind the bars (reader page, video, photo, splash). The root keeps horizontal touch targets clear of a landscape navigation bar and the camera cut-out with `Modifier.nebSafeSides()`. Never hide and re-show the status bar to make room: the next screen jumps by its height.
- **Toast:** one component, `NebToast` through `NebToastHost`. Inverse surface card, 24 dp corners, a 38 dp tonal tile (tertiary for done, error for a problem, primary for information), a medium weight message, an optional action pill in `inversePrimary`. NO progress bar or timer line, on web or Android: the toast leaves by time alone. Spring in from below, swipe sideways away. No shadow, no emoji.
- **Plus menu:** where a field can take more than text there is one plus tool, not a row of icons. It opens a compact popup of tonal tiles with a word each (image, PDF, audio, video, poll), and the plus turns into a cross while it is open. Web `neb-plus`, Android `ComposerAttachMenu`.
- **Slider:** thick 14 dp rail, strong fill to a 30 dp round thumb, haptic tick on every step, `setProgress` semantics. Values are in real units (sp), never percentages, where the unit is something the reader can feel.
- **Bento sheet:** a settings sheet is one scrolling column of tonal cards, each with its own hue (blue, amber, green, violet, indigo, rose; each with a dark mode partner), a bold value, and the control inside. A selected choice becomes the strong colour and rounds further (24 dp, never to a square).
- **Toast bus (session 12):** a message from anywhere (a click handler, a download callback) goes through `Context.nebToast(text)`, which sends it to the one `NebToastBusHost` mounted over the navigation host in `MainActivity`. Nobody calls `Toast.makeText` (only the crash screen, which has no host, and the bus's own fallback do). The host sits above the navigation bar.
- **Minimal composer (news):** a comment bar that takes text only carries the identity avatar menu (you or anonymous) in the leading slot and a send button. No tools, no plus.
- **Splash:** the page colour (white in light, the deep navy in dark, following the theme chosen in settings; `values-night/colors.xml` keeps the system window and the API 31 splash on the same colour), the N settling in on a spring, NEBians cut in letter by letter, then the stack lifts away. No tinted wash, no big shape behind the logo, nothing orbits, pulses or rings it. Springs only, values read in the draw phase.
- **About:** it fills the screen like a poster: big shape and name, version tiles (version, build, channel; this is the only place version info lives, Settings has one About row and no version card), team, then credits for open source libraries and the on-device models (Whistle, Phonon, Needle). No scroll-driven animation anywhere in the Android app: no parallax, no collapsing-on-scroll effects, no items that animate in as they scroll into view. Motion answers a touch or a state change only.
- **Upload (Android):** a three pill stepper (the open pill carries its name, done steps are ticks and tap back), steps slide in the direction of travel, a full width Scan tile plus Gallery and Files tiles in their own tones, and publishing covers the screen with a morphing shape, the percentage and a flat bar. No bar pinned to the bottom of the screen.

---

## 13. Press, spacing, contrast, scroll (written after these flaws came back again and again)

These are the flaws that keep appearing in dialogs, popups, sheets, toolbars and composers. Every agent checks them before it says done, on web and Android.

### 13.1 Press feedback follows the shape
- A ripple, state layer, pressed tint or tap flash is drawn inside the control's own rounded box. A rounded or circular control with a rectangular flash is a bug.
- Android: `Modifier.clip(shape)` comes BEFORE `.clickable(...)` / `.combinedClickable(...)` / `.selectable(...)`, with the same `shape` as the background. A `background(color, shape)` alone does not clip the ripple. Material components (`IconButton`, `Button`, `Card(onClick)`, `FilterChip`) already clip; a custom `Box` or `Row` does not. Custom expressive shapes (the clover create button) are clipped with the same `nebShape(...)`.
- Android safety net: the app provides `NebIndication` (`ui/theme/NebIndication.kt`) as `LocalIndication` inside `NEBiansTheme`. It is a state layer in the content colour drawn inside a rounded shape (circle on small square controls, 16dp otherwise), so a control that forgot to clip still never flashes a rectangle. Never remove it, never provide the square platform ripple again, and never call `ripple()` without a clip of the control's shape before it. It does not replace the clip rule: the clip is still required so the pressed area matches the exact radius.
- Web: `-webkit-tap-highlight-color: transparent` on every interactive element (`m3x/app-press.css`), and the pressed or hover tone is a background on the element itself, which already has its radius. Never an overlay without `border-radius: inherit`.
- Press may change the radius only between two rounded values, never to 0.

### 13.2 Neighbours never touch
- Icon buttons, tonal tiles, toggles and chips in a row are separated by a gap: 4px minimum, 6px for 38 to 44px tiles. In Compose use `Arrangement.spacedBy(...)`; never rely on tile padding for the gap.
- Reason: a tile at rest is transparent, so zero gap looks fine until one is selected or pressed and its tonal fill meets the next tile's fill. The two fills then read as one slab.
- Applies to toolbars, composer tool rows, dialog action rows, segmented groups that are not a real segmented control, and sheet icon grids.

### 13.3 Contrast on themed surfaces
- Notes, cards and sheets that take a theme colour compute their ink with `readableOn(ink, background, min)` (`screens/notes/NoteContrast.kt`): 4.5 for text, 3 for icons and glyphs. If the themed ink fails, it falls back to black or white.
- A disabled or secondary icon uses `softReadable(...)`, which keeps 3:1. Do not write `tint = fg.copy(alpha = 0.35f)`.
- The brand blue is never used as an icon colour on a coloured note tone without `readableOn(c.primary, tone.container, 3f)`.

### 13.4 Scroll
- Never put a `horizontalScroll` / `LazyRow` inside another horizontal scroller. The child gets an infinite maximum width and Compose throws `Horizontally scrollable component was measured with an infinity maximum width constraints`. A helper that is placed inside a scrolling row emits its items directly and does not scroll itself (`ImageTools`).
- The same goes for vertical: no `verticalScroll` or `LazyColumn` inside a vertical scroller without a bounded `heightIn(max = ...)`.
- The floating bottom bar hides while the user scrolls down and returns on scroll up (`NavBarScroll.kt`): it follows the finger and a spring settles it. Only the layer transform changes, nothing recomposes per frame. The create menu pins the bar.

- **Always `nebHorizontalScroll`, never `horizontalScroll`** (`ui/components/SafeScroll.kt`). It puts a width guard (`boundedWidth`) in front of the scroller, so an ancestor that hands down an infinite width (an intrinsic probe, a wrap-content parent, a scroller above) degrades to a layout that scrolls instead of a crash. A grep for the bare name must return only `SafeScroll.kt`. Do not "fix" a crash by removing the guard.

- **`LazyRow`, `HorizontalPager` and every other lazy horizontal list carry `Modifier.boundedWidth()`** in their `modifier`. They check their constraints too and throw the same infinity error; `nebHorizontalScroll` alone did not cover them (session 13). `python3 tools/android/check_scrollers.py` fails on a bare `horizontalScroll(` or an unguarded `LazyRow(` / `HorizontalPager(`, and runs first in the Android release workflow. Run it before every push that touches a scroller.

### 13.5 Text with pictures inside (post, reply and note composers)
- The text keeps its normal line height everywhere. Only the paragraph (line) that holds a picture grows (`ParagraphStyle`), so an ordinary line never gets taller because a picture exists elsewhere.
- The caret is as tall as the text and centred in its line, also on a line that holds a picture. On Android the field draws its own caret when pictures exist (`RichTextField`); on the web the drop bar is capped to the text's line height.
- While a picture is dragged, the writing caret itself (the keyboard's cursor, never a bar, line or ghost shape) walks to the exact drop place under the fingertip; the picture rides above the finger so it never hides the caret. A drop never lands inside another picture. On Android `RichState.moveCaret` moves the real selection during the drag and `restoreSelection` gives it back on cancel.
- A Compose paragraph that ends in a real line break gets one more empty line from the platform layout. A picture line is therefore its own paragraph that ends in a zero width mark (U+200B) instead of `\n` (and so does the line before it); an empty last line after a picture line gets a mark of its own. Never close a `ParagraphStyle` range on a `\n`. The default picture is 32dp and its line is the picture plus 4dp.
- Never put a `Box` with a fixed size straight inside a parent that has `propagateMinConstraints = true`: the parent's minimum width is forced on it (this was the full width blue bar).

### 13.5b Selection menu
- Selected text opens the app's own menu (`NebTextToolbar.kt`, provided once in `NEBiansTheme`): a floating pill in the float colour with a hairline, no shadow, Cut, Copy, Paste, Select all, plus Bold, Italic and Underline icons in the writing fields. It sits above the selection and drops below it near the top edge, never takes focus (the keyboard stays) and springs in. Dialog and sheet windows keep the system menu.

### 13.6 Covers and cards
- A cover is as tall as its width asks, not a fixed strip: the editor cover is `aspectRatio(1.9)` between 168 and 264dp. Cover art scales with the banner's proportions, so a short wide banner keeps its shapes bold.
- Change and Remove appear only after a tap on the cover and fold away after a few seconds.
- A list card shows a short preview: a title, two to four lines, and one small preview of what the note holds (pictures as a 1, 2 or 3-up mosaic with +N, a recording as a waveform tile, a drawing redrawn from its strokes, a table as a mini grid, code as a mono tile), then one footer line. Media is read from the note's blocks off the main thread and cached (`NoteMediaCache`). Lists of notes use a staggered grid (adaptive columns) and a header that is one 56dp row followed directly by the filters.
- The drop caret reads the fingertip from the screen (`localPositionOf` the field's overlay), never from accumulated drag deltas, so a page that scrolls while a picture is dragged cannot make the caret drift away from the finger. A picture's line is the picture plus 6dp; the caret is 1.2 em tall (Meta's), not the line's height. One scroll-follow job at a time (cancel the previous).

### 13.7 Bottom sheets: padded content, never under the status bar (session 18, third time)

Why it kept happening: `NebModalSheet` padded only its title row. Whatever a caller put in the body started at x = 0, so every new sheet (Sign in, Pathways route detail) shipped with text and buttons glued to the screen edge, and a tall sheet ran up under the status bar. Each agent copied the nearest sheet and nobody owned the padding.

The rule now lives in the component, not in the caller:
- `NebModalSheet` pads its body by `horizontalPadding` (22dp) by default. A new sheet writes content and gets correct margins for free. Do not add your own horizontal padding on top.
- `fullBleed = true` is for menu style rows that draw edge to edge, lazy lists, or content that already pads itself. It needs a `// bleed: why` comment on the call.
- The body is capped to the window height minus the status bar minus a 24dp scrim band, so a full height sheet never touches or passes the status bar. Keep long content in a `verticalScroll` or lazy list inside the sheet.
- Never call `ModalBottomSheet(` directly in a new file. `tools/android/check_sheets.py` (first CI step) fails on it, and on `fullBleed = true` without the comment. The legacy raw sheets are in the script's list; migrate them, do not extend it.
- Same check by eye before saying done: open the sheet at 390 px wide, the text must have 22dp from both edges and the buttons must not touch the screen sides.



## 14. Dark mode, status bar, post and comment rows (session 44; written after these flaws came back again)

**Dark is neutral graphite, never navy.** Page `#121318`, cards `#1b1b21` / `#1f1f25`, raised `#292a2f` / `#2e2f36`, hairline `#45464f`, text `#e4e1e9` / `#c6c6d0`, primary `#b6c4ff`. It is the dark of `NEBians-Pathways.html` and is the same on web (`tokens.css`), Android (`Palette.kt`, generated), the splash (`values-night`), the auth screens and desktop. A new dark colour is taken from this ramp; no hex with a blue cast (`#0b1020`, `#172036` and friends) is written by hand. Brand blue lives in primary and the tonal containers only.

**Status bar (Android).** The app is edge to edge. Every full screen starts with `NebTopBar(...)`, which applies `statusBarsPadding()`. Never write a bare `Row { IconButton(ArrowBack) Text(title) }` at the top of a screen. `tools/android/check_insets.py` runs in CI and fails on it (opt out with `// inset-ok: reason` only when a host already pads, such as a tab body).

**Post and comment rows (web and Android).**
1. Layout is one grid: avatar column, then a content column. Header line (name, badge, dot, time, chips), body 2dp under it, media, then the action row. The body starts at the same x as the name. No extra gap between header and body: header height 20dp, gap 2dp.
2. The first icon of the action row sits exactly under the left edge of the body text, not inset by the pill padding. Ghost pills keep 12dp (10px web) of inner padding for the touch target; the row is shifted left by the same amount with `Modifier.nebGhostRowStart()` (Android) or `--act-inset` on `.post-card-actions` (web). The last action sits on the right edge of the content, not past it.
3. Actions are ghost (no fill) with icon 18dp, count `labelLarge`, 6dp icon to label gap, 2dp between pills. Liked turns primary. Filled tonal pills are for the post detail bar, which starts at the page margin, so no shift there.
4. Reply, like and mark all use the same pill metrics; never hand-pick `padding(horizontal = 8.dp, vertical = 5.dp)` for one of them.

**Segmented controls (LOCKED, session 47).** The original Pathways connected button group is the real one and is final. Separate tonal blocks with a 3dp gap (`surfaceContainerHigh`); outer corners of the group are full pills, inner corners 8dp; the selected block is a full pill in `onSurface` with `surface` text and the corner morph animates on the spring. Session 46 replaced it with a single pill track and the owner rejected that. Do not change it again without an explicit ask. Android: `PwSeg`; concepts and web: `.seg` in `NEBians-*.html` and `pages/pathways.css`.

**Dark flag (Android).** Use `MaterialTheme.colorScheme.surface.luminance() < 0.5f`. `isSystemInDarkTheme()` is allowed only in `ui/theme` (the guard `tools/android/check_insets.py` fails the CI otherwise), because the app theme can be forced Dark or Light in Settings.
