"""Creator marketplace — every client value passes through here before storage.

Unknown block types are dropped, unknown keys inside a known block are dropped,
strings are trimmed and capped, and every URL must be http(s) or site-relative.
That is the whole reason a page can be "fully customizable" without becoming a
stored-XSS surface.
"""
import re
import uuid

from .creator_pages_schema import (
    ACCENT_RE, BLOCK_FIELDS, DENSITIES, HERO_STYLES, ITEM_FIELDS, LIST_FIELDS,
    MAX_BLOCKS, MAX_LIST_ITEMS, RADII, SOCIAL_KEYS, URL_FIELDS,
)


def _text(value, limit=400):
    if value is None:
        return ''
    if not isinstance(value, str):
        value = str(value)
    return value.strip()[:limit]


def _clean_url(value):
    if not isinstance(value, str):
        return ''
    value = value.strip()
    if not value:
        return ''
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


def sanitize_style(raw):
    if not isinstance(raw, dict):
        return {}
    style = {
        'hero': raw.get('hero') if raw.get('hero') in HERO_STYLES else 'art',
        'radius': raw.get('radius') if raw.get('radius') in RADII else 'round',
        'density': raw.get('density') if raw.get('density') in DENSITIES else 'comfortable',
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


def sanitize_blocks(raw):
    if not isinstance(raw, list):
        return []
    blocks = []
    for entry in raw[:MAX_BLOCKS]:
        if not isinstance(entry, dict):
            continue
        block_type = _text(entry.get('type'), 20).lower()
        if block_type not in BLOCK_FIELDS:
            continue
        block = {'id': _text(entry.get('id'), 40) or uuid.uuid4().hex[:10], 'type': block_type,
                 'enabled': entry.get('enabled') is not False}
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
