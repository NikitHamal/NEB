from django.conf import settings
from django.core.exceptions import ValidationError

from api.security import validate_resource_file_url

from .view_helpers import _file_ext

PLAY_STORE_URL = 'https://play.google.com/store/apps/details?id=com.neb.ians'

KIND_META = {
    'pdf': {'icon': 'picture_as_pdf', 'label': 'PDF', 'verb': 'Read', 'sprite': 'bookLoader'},
    'image': {'icon': 'image', 'label': 'Image', 'verb': 'View', 'sprite': 'magnifier'},
    'video': {'icon': 'play_circle', 'label': 'Video', 'verb': 'Watch', 'sprite': 'nebyHop'},
    'audio': {'icon': 'headphones', 'label': 'Audio', 'verb': 'Listen', 'sprite': 'sleepyBell'},
    'embed': {'icon': 'play_circle', 'label': 'Video', 'verb': 'Watch', 'sprite': 'nebyHop'},
    'link': {'icon': 'link', 'label': 'Link', 'verb': 'Open', 'sprite': 'pushPin'},
    'document': {'icon': 'description', 'label': 'Document', 'verb': 'Read', 'sprite': 'newspaper'},
    'locked': {'icon': 'lock', 'label': 'Paid', 'verb': 'Unlock', 'sprite': 'padlock'},
    'error': {'icon': 'cloud_off', 'label': 'Unavailable', 'verb': 'Read', 'sprite': 'rainCloud'},
    'none': {'icon': 'draft', 'label': 'Empty', 'verb': 'Read', 'sprite': 'nebyIdle'},
}


def safe_file_url(request, raw):
    if not raw:
        return '', ''
    media_prefix = settings.MEDIA_URL
    if raw.startswith(media_prefix) or (request and raw.startswith(request.build_absolute_uri(media_prefix))):
        return raw, ''
    try:
        return validate_resource_file_url(raw), ''
    except ValidationError as exc:
        return '', ' '.join(exc.messages)


def classify_kind(res, src, embed_url, has_access, error):
    if not has_access:
        return 'locked'
    if embed_url:
        return 'embed'
    if error:
        return 'error'
    if not src:
        return 'none'
    media_type = res.get('media_type') or 'document'
    if media_type in ('pdf', 'image', 'video', 'audio'):
        return media_type
    rtype = (res.get('type') or '').lower().strip()
    if rtype == 'link' or (not _file_ext(src) and src.startswith(('http://', 'https://'))):
        return 'link'
    return 'document'


def build_part(request, res, has_access, current_id):
    src, error = safe_file_url(request, res.get('file_url') or '') if has_access else ('', '')
    embed_url = res.get('embed_url') or '' if has_access else ''
    kind = classify_kind(res, src, embed_url, has_access, error)
    meta = KIND_META[kind]
    ext = _file_ext(src).lstrip('.').upper() if src else ''
    host = ''
    if kind == 'link':
        host = src.split('//', 1)[-1].split('/', 1)[0]
    shown_kind = meta['label']
    if kind == 'document' and ext:
        shown_kind = ext
    return {
        'id': res['id'], 'title': res['title'], 'subject': res.get('subject', ''),
        'type': res.get('type', ''), 'kind': kind, 'media_type': kind if kind in ('video', 'audio') else res.get('media_type', ''),
        'icon': meta['icon'], 'label': shown_kind, 'verb': meta['verb'], 'sprite': meta['sprite'],
        'src': src, 'safe_file_url': src, 'embed_url': embed_url, 'mime_type': res.get('mime_type', ''),
        'thumbnail_url': res.get('thumbnail_url') or '', 'file_size': res.get('file_size') or 0,
        'author_name': res.get('author_name') or '', 'ext': ext, 'host': host, 'error': error,
        'is_current': res['id'] == current_id,
        'readable': kind in ('pdf', 'image', 'video', 'audio', 'embed', 'link'),
    }


def build_parts(request, resources, has_access, current_id):
    return [build_part(request, r, has_access, current_id) for r in resources]
