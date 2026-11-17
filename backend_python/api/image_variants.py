"""Small copies of stored images for lists (feeds, comments, cards).

A feed row draws an avatar at about 44 px but the stored photo is up to 640 px (20 to 100 KB).
Each stored file gets a small WebP next to it; list code asks ``variant_url`` and receives the
small file when it exists, otherwise the original URL. Originals are never touched or deleted,
so cached pages, older app builds and a rollback keep working.

    profile_photos/<stem>.<ext>        original
    profile_photos/<stem>_o.webp       resized copy (optimize_profile_photos)
    profile_photos/<stem>_s.webp       192 px list copy          <- this module
    resource_thumbnails/<stem>_c.webp  480 px card cover copy    <- this module
"""
import os
import time
from io import BytesIO

from django.conf import settings

AVATAR = ('/media/profile_photos/', '_s', 192, 80)
COVER = ('/media/resource_thumbnails/', '_c', 480, 78)
_KINDS = (AVATAR, COVER)

_HIT_TTL = 24 * 3600     # a copy that exists keeps existing
_MISS_TTL = 300          # a missing copy may be written by the next deploy or upload
_CACHE = {}              # url -> (result, expires)
_CACHE_MAX = 6000


def _split(url):
    """(kind, prefix, name) for a URL that points at a local stored image, else None."""
    if not url or not isinstance(url, str):
        return None
    for kind in _KINDS:
        marker = kind[0]
        if marker in url:
            prefix, _, name = url.partition(marker)
            name = name.split('?')[0]
            if name and '/' not in name:
                return kind, prefix + marker, name
    return None


def _stem(name, suffix):
    if name.endswith('_o.webp'):
        return name[:-len('_o.webp')]
    return os.path.splitext(name)[0]


def variant_name(name, kind):
    """The file name of the list copy for a stored file name (None if name is already a copy)."""
    suffix = kind[1]
    if name.endswith(suffix + '.webp'):
        return None
    return _stem(name, suffix) + suffix + '.webp'


def _dir(kind):
    return os.path.join(str(settings.MEDIA_ROOT), kind[0].strip('/').split('/', 1)[1])


def variant_url(url):
    """The small copy of a stored image if one exists on disk, else ``url`` unchanged."""
    parts = _split(url)
    if not parts:
        return url
    now = time.monotonic()
    hit = _CACHE.get(url)
    if hit and hit[1] > now:
        return hit[0]
    kind, prefix, name = parts
    out = url
    vname = variant_name(name, kind)
    if vname:
        try:
            if os.path.isfile(os.path.join(_dir(kind), vname)):
                out = prefix + vname
        except Exception:
            out = url
    if len(_CACHE) > _CACHE_MAX:
        _CACHE.clear()
    _CACHE[url] = (out, now + (_HIT_TTL if out != url else _MISS_TTL))
    return out


def variant_bytes(image, kind):
    """Encode a PIL image as the list copy for ``kind`` (long side capped, alpha kept)."""
    from PIL import Image, ImageOps
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass
    edge = kind[2]
    if max(image.size) > edge:
        image = image.copy()
        image.thumbnail((edge, edge), Image.Resampling.LANCZOS)
    has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    image = image.convert('RGBA' if has_alpha else 'RGB')
    out = BytesIO()
    image.save(out, format='WEBP', quality=kind[3], method=4)
    return out.getvalue()


def write_variant(src_path, kind, root=None):
    """Create the list copy for one stored file. Returns bytes saved, 0 if skipped, -1 on failure."""
    from PIL import Image
    folder = root or _dir(kind)
    vname = variant_name(os.path.basename(src_path), kind)
    if not vname:
        return 0
    dest = os.path.join(folder, vname)
    if os.path.isfile(dest):
        return 0
    try:
        with Image.open(src_path) as im:
            if getattr(im, 'is_animated', False):
                return 0
            im.load()
            data = variant_bytes(im, kind)
        old = os.path.getsize(src_path)
        if len(data) >= old:        # already tiny: the original is the better file
            return 0
        tmp = dest + '.tmp'
        with open(tmp, 'wb') as fh:
            fh.write(data)
        os.replace(tmp, dest)
        return old - len(data)
    except Exception:
        return -1
