"""Creator marketplace — every client value passes through here before storage.

Unknown block types are dropped, unknown keys inside a known block are dropped,
strings are trimmed and capped, and every URL must be http(s) or site-relative.
That is the whole reason a page can be "fully customizable" without becoming a
stored-XSS surface.
"""
import re
import uuid

from .creator_pages_schema import (
    ACCENT_RE, BLOCK_FIELDS, ITEM_FIELDS, LIST_FIELDS, MAX_BLOCKS,
    MAX_LIST_ITEMS, SOCIAL_KEYS, URL_FIELDS,
)
from .creator_themes import (
    BLOCK_ALIGNS, BLOCK_TONES, BLOCK_WIDTHS, CARD_STYLES, DEFAULT_PALETTE,
    DENSITIES, FONTS, HERO_STYLES, PALETTES, PATTERNS, RADII, SCHEMES, WIDTHS,
)


def _text(value, limit=400):
    if value is None:
        return ''
    if not isinstance(value, str):
        value = str(value)
    return value.strip()[:limit]


#: An in-page jump: `#courses`, `#pricing`. Templates lean on these heavily --
#: a hero button that scrolls to the fees is the single most useful link a
#: storefront has -- so the allowlist has to let them through, while still
#: refusing anything that could carry a scheme.
_FRAGMENT_RE = re.compile(r'^#[A-Za-z0-9_-]{1,60}$')


def _clean_url(value):
    if not isinstance(value, str):
        return ''
    value = value.strip()
    if not value:
        return ''
    if _FRAGMENT_RE.match(value):
        return value
    if value.startswith('/') and not value.startswith('//'):
        return value[:600]
    if re.match(r'^https?://', value, re.IGNORECASE):
        return value[:600]
    return ''


def _bool(value):
    return value in (True, 'true', 'True', 'on', '1', 1, 'yes')


def sanitize_accent(value):
    value = (value or '').strip()
    return value.upper() if ACCENT_RE.match(value) else '#004BD4'


def _pick(raw, key, allowed, default):
    value = raw.get(key)
    return value if value in allowed else default


def sanitize_style(raw):
    """The creator's whole look, reduced to values both renderers understand.

    Anything unrecognised becomes the default rather than an error: a page saved
    by an older app that has never heard of `pattern` should still round-trip,
    and a palette we retire should degrade to Indigo, not 500.
    """
    if not isinstance(raw, dict):
        raw = {}
    style = {
        'palette': _pick(raw, 'palette', PALETTES, DEFAULT_PALETTE),
        'scheme': _pick(raw, 'scheme', SCHEMES, 'light'),
        'hero': _pick(raw, 'hero', HERO_STYLES, 'art'),
        'font': _pick(raw, 'font', FONTS, 'sans'),
        'pattern': _pick(raw, 'pattern', PATTERNS, 'none'),
        'card': _pick(raw, 'card', CARD_STYLES, 'elevated'),
        'radius': _pick(raw, 'radius', RADII, 'round'),
        'density': _pick(raw, 'density', DENSITIES, 'comfortable'),
        'width': _pick(raw, 'width', WIDTHS, 'standard'),
        'show_stats': _bool(raw.get('show_stats')),
        'show_contact': _bool(raw.get('show_contact', True)),
        'show_verified': raw.get('show_verified') is not False,
    }
    columns = raw.get('gallery_columns')
    try:
        style['gallery_columns'] = min(4, max(2, int(columns))) if columns else 3
    except (TypeError, ValueError):
        style['gallery_columns'] = 3
    return style


def sanitize_block_settings(raw):
    """A section's own overrides: where it sits, how loud it is, how wide.

    Returned empty when the creator has not overridden anything, so a page that
    never touches these stays as small on the wire as it was before they existed.
    """
    if not isinstance(raw, dict):
        return {}
    settings = {}
    align = raw.get('align')
    if align in BLOCK_ALIGNS and align != 'start':
        settings['align'] = align
    tone = raw.get('tone')
    if tone in BLOCK_TONES and tone != 'plain':
        settings['tone'] = tone
    width = raw.get('width')
    if width in BLOCK_WIDTHS and width != 'standard':
        settings['width'] = width
    columns = raw.get('columns')
    try:
        columns = int(columns)
    except (TypeError, ValueError):
        columns = 0
    if 1 <= columns <= 4:
        settings['columns'] = columns
    return settings


def sanitize_socials(raw):
    if not isinstance(raw, dict):
        return {}
    socials = {}
    for key in SOCIAL_KEYS:
        value = raw.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        value = value.strip()
        if key in ('email', 'phone'):
            socials[key] = _text(value, 120)
            continue
        clean = _clean_url(value)
        if clean:
            socials[key] = clean
    return socials


def _sanitize_items(block_type, raw):
    key = LIST_FIELDS.get(block_type)
    if not key:
        return None
    if key == 'images':
        if not isinstance(raw, list):
            return []
        return [_clean_url(item) for item in raw if _clean_url(item)][:MAX_LIST_ITEMS]
    if not isinstance(raw, list):
        return []
    fields = ITEM_FIELDS.get(block_type, ())
    items = []
    for entry in raw[:MAX_LIST_ITEMS]:
        if not isinstance(entry, dict):
            continue
        item = {}
        for field in fields:
            value = entry.get(field)
            item[field] = _clean_url(value) if field in URL_FIELDS else _text(value, 800)
        if any(item.values()):
            items.append(item)
    return items


#: A block id becomes an `#anchor` in the page, so it has to survive being put
#: in an href. Anything else is replaced rather than escaped -- an id is
#: machine-made, and no creator ever typed one.
_ID_RE = re.compile(r'^[A-Za-z0-9_-]{1,40}$')


def _slug_id(value, block_type):
    value = _text(value, 40)
    if _ID_RE.match(value or ''):
        return value
    return f'{block_type}-{uuid.uuid4().hex[:6]}'


def sanitize_blocks(raw):
    if not isinstance(raw, list):
        return []
    blocks = []
    # Ids are anchors, and two anchors with the same name make the first one
    # unreachable. A creator who adds a second Courses shelf gets `courses-2`.
    seen = {}
    for entry in raw[:MAX_BLOCKS]:
        if not isinstance(entry, dict):
            continue
        block_type = _text(entry.get('type'), 20).lower()
        if block_type not in BLOCK_FIELDS:
            continue
        block_id = _slug_id(entry.get('id'), block_type)
        if block_id in seen:
            seen[block_id] += 1
            block_id = f'{block_id}-{seen[block_id]}'
        seen[block_id] = seen.get(block_id, 1)
        block = {'id': block_id, 'type': block_type,
                 'enabled': entry.get('enabled') is not False}
        settings = sanitize_block_settings(entry.get('settings'))
        if settings:
            block['settings'] = settings
        for field in BLOCK_FIELDS[block_type]:
            value = entry.get(field)
            block[field] = _clean_url(value) if field in URL_FIELDS else _text(value, 4000 if field == 'body' else 300)
        items = _sanitize_items(block_type, entry.get(LIST_FIELDS.get(block_type)) if LIST_FIELDS.get(block_type) else None)
        if items is not None:
            block[LIST_FIELDS[block_type]] = items
        blocks.append(block)
    return blocks


def sanitize_include_list(raw):
    if isinstance(raw, str):
        raw = [part for part in raw.split('\n')]
    if not isinstance(raw, list):
        return []
    return [_text(item, 160) for item in raw[:20] if _text(item, 160)]
