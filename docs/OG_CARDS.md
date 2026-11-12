# Share cards

Every public page of NEBians has a drawn Open Graph card of its own: a
1200×630 PNG served from `/og/<kind>/<key>.png`, referenced by `og:image` and
`twitter:image`. This is the picture that appears when a student pastes a link
into Facebook, WhatsApp, Viber, Discord or a Google result.

## Why they look like this

M3 Expressive, light. A card is one flat tonal surface (the subject colour at 3.5 %),
one big expressive shape on the right (a cookie, in the 12 % container tone), a solid
accent squircle inside it, and a white glyph that says what the page is about
(`og_m3x.glyph`: books, paper, bubbles, flask, graph, question, cards, spark, mark).
Four shape variants are chosen from the card seed. On the left: the logo lockup, a tonal
kicker pill, the title in ink, tonal meta pills, the address.

Rules: flat colour only (no gradient, glow, grain or shadow), no stroke on a portrait
(a profile photo is clipped to a cookie shape), no dash punctuation in any card text.
The subject colour still comes from `web/templatetags/subject_tokens.py`; `og_m3x.roles`
darkens it until white text on it passes contrast and derives container and on-container.

## Where it lives

| file | what it is |
| --- | --- |
| `web/og_cards.py` | composition: ground, title fitting, kicker, meta, lockup, address. **No Django at import time.** |
| `web/og_m3x.py` | the M3E shapes, glyphs, role colours and the cookie-clipped portrait used by the current design |
| `web/og_art.py` | legacy isometric geometry and palette maths (kept for the old sculptures and tests) |
| `web/og_heroes.py` | the ten sculptures: books, paper, bubbles, flask, graph, question, cards, spark, avatar, mark |
| `web/og_logo.py` | the real mark, loaded from pre-rasterised PNGs |
| `web/views_og.py` | Django side: what each card says, the cache, the rate limit, the context processor |
| `tools/og/build_logo.py` | regenerates the logo PNGs when the SVG changes |
| `tools/og/preview.py` | renders the whole set plus a contact sheet, without Django |
| `web/test_og_cards.py` | 22 tests, most of them without a database |

## The grid

```
┌──────────────────────────────────────────────────────────────┐
│  ▬ KICKER                                                     │
│                                                               │
│  The title, set as large as it              ╱▔▔╲              │
│  will fit in three lines                 ╱  the   ╲           │
│                                          ╲ sculpture ╱        │
│  meta · meta · meta                       ╲__╱               │
│                                                               │
│  [N] NEBians  nebians.consica.com.np                          │
└──────────────────────────────────────────────────────────────┘
```

The title gets a **vertical budget**, not just a width: one word may be set at
148px, a sentence lands around 56px. Without that budget every title hits the
same ceiling and a card for "Physics" looks as timid as a card for a headline.

The wrap is **balanced** — it steals a word from the line above rather than
leaving one orphan word alone on the last line.

## Adding a card

**A static page.** Add an entry to `PAGES` in `views_og.py` and map the route
name to it in `_ROUTE_PAGES`:

```python
'my-page': {
    'kicker': 'Kicker', 'title': 'The sentence the card says',
    'meta': ('one', 'two'), 'hero': 'books',
},
...
'my_route_name': 'my-page',
```

**A page about a database row.** Write a builder returning the same dict shape
and add it to `KINDS` and `_ROUTE_OBJECTS`. The builder gets the URL key and
must raise `Http404` for anything that should not have a card — unapproved
resources, archived threads, unpublished courses, private study spaces.

**A new sculpture.** Write `hero_x(accent, rng, stage)` in `og_heroes.py`,
register it in `HEROES`, and add a placement to `HERO_TUNING` in `og_cards.py`
if the default doesn't suit its silhouette.

## Rules that are not obvious

- **Bump `CARD_VERSION` in `views_og.py` whenever the drawing changes.**
  The cache is keyed on what a card *says*, which is right for a title edit and
  wrong for a redesign. Without a bump, a new renderer keeps serving the old
  picture for a day — this actually happened, and it is why the card URL
  carries `?v=` as well: a crawler treats a new URL as a new thing.
- **`og:image` must never 404.** A missing card is a blank preview that a
  scraper caches. Builders catch anything that isn't an explicit `Http404`.
- **Never trust the URL key.** `_SAFE_KEY` allows ids, slugs and usernames and
  nothing else; anything that would need escaping falls through to the default
  card.
- **The card must be readable at 300px wide.** That is the size most people see
  it at. One idea per card, one sculpture, one sentence.
- **The logo is not redrawn.** `og_logo.mark()` loads the committed PNG from
  `n-logo-tight.svg`. If the SVG changes, run `tools/og/build_logo.py`
  (`pip install cairosvg` — a build-time tool, not a backend dependency).

## Working on them

```bash
python3 tools/og/preview.py /tmp/og-preview   # every card + contact sheet
python3 -m unittest web.test_og_cards         # the tests
```

`preview.py` needs only Pillow: the drawing module has no Django in it, so a
design change is a one-second loop rather than a deploy.

## Checking a live card

```bash
curl -s https://nebians.consica.com.np/og/page/home.png?v=2 -o /tmp/c.png
```

Then re-scrape the page in the Facebook Sharing Debugger. Two caches sit in
front of you: ours (`CARD_VERSION` in the cache key, 24 h TTL) and the
scraper's own (only cleared by a new URL or a manual re-scrape).
