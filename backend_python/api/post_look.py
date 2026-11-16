"""The look of a dynamic post: page colour, cover (pattern or photo), icon, paper and type.

A look is a handful of small numbers and one icon key, the same vocabulary the
Android notes page uses (tone, cover, icon, paper). Nothing user-written is ever
stored here except the icon key, which is held to a short a-z slug, so the value
is safe to put into a page as data and never as markup.

Stored as a JSON string on `Post.look`. An empty string means the plain post,
so every old post keeps looking exactly as it did.
"""
import json
import re

MAX_TONE = 40
MAX_COVER = 60
MAX_PAPER = 5
MAX_FONT = 2
MAX_PHOTO = 2_000_000_000
_ICON = re.compile(r'^[a-z_]{1,24}$')


def _int(value, low, high):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return number if low <= number <= high else 0


def clean(raw):
    """Return (json_string, error). '' clears the look. Unknown keys are dropped."""
    if raw is None or raw == '' or raw == {} or raw == 'null':
        return '', None
    if isinstance(raw, str):
        if len(raw) > 400:
            return '', 'Look is too large'
        try:
            raw = json.loads(raw)
        except ValueError:
            return '', 'Look is not valid'
    if not isinstance(raw, dict):
        return '', 'Look is not valid'
    icon = str(raw.get('icon') or '')
    look = {
        'tone': _int(raw.get('tone'), 0, MAX_TONE),
        'cover': _int(raw.get('cover'), 0, MAX_COVER),
        'icon': icon if _ICON.match(icon) else '',
        'paper': _int(raw.get('paper'), 0, MAX_PAPER),
        'font': _int(raw.get('font'), 0, MAX_FONT),
        'photo': _int(raw.get('photo'), 0, MAX_PHOTO),
        'bg': _int(raw.get('bg'), 0, MAX_PHOTO),
    }
    look = {k: v for k, v in look.items() if v}
    if not look:
        return '', None
    return json.dumps(look, separators=(',', ':'), sort_keys=True), None


def parse(stored):
    """The look as a dict for the API, or None for a plain post."""
    if not stored:
        return None
    try:
        value = json.loads(stored)
    except ValueError:
        return None
    return value if isinstance(value, dict) and value else None


def finalize(stored):
    """Before saving: keep a cover or page picture only if that picture exists, and keep it from being cleaned up."""
    look = parse(stored)
    if not look or not (look.get('photo') or look.get('bg')):
        return stored or ''
    from .models import ContentImage
    from .content_images import mark_used
    keep = []
    for key in ('photo', 'bg'):
        value = look.get(key)
        if not value:
            continue
        if ContentImage.objects.filter(pk=value).exists():
            keep.append(value)
        else:
            look.pop(key, None)
    if keep:
        mark_used(keep)
    return json.dumps(look, separators=(',', ':'), sort_keys=True) if look else ''
