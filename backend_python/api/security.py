"""Security helpers for NEBians.

Centralizes authentication-adjacent helpers so API and web views follow the
same validation and production safety rules.
"""
import hmac
import hashlib
import ipaddress
import os
import re
import secrets
import socket
import time
import uuid
from io import BytesIO
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils.text import get_valid_filename
from PIL import Image, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 20_000_000

PROFILE_PHOTO_MAX_BYTES = getattr(settings, 'PROFILE_PHOTO_MAX_BYTES', 5 * 1024 * 1024)
PROFILE_PHOTO_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
PROFILE_PHOTO_ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}
PROFILE_PHOTO_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
EXTERNAL_URL_MAX_LENGTH = 2048
ADMIN_API_SALT = getattr(settings, 'ADMIN_API_SALT', None) or os.environ.get('ADMIN_API_SALT')
LEGACY_SHA256_RE = re.compile(r'^[a-f0-9]{64}$')

if not ADMIN_API_SALT:
    raise RuntimeError('ADMIN_API_SALT must be configured in environment or settings.')


def hash_password(raw_password: str) -> str:
    """Return a Django-managed password hash with salt and work factor."""
    return make_password(raw_password)


def verify_password(raw_password: str, stored_hash: str) -> tuple[bool, bool]:
    """Verify a password.

    Returns (is_valid, needs_rehash). The second value is True for legacy raw
    SHA-256 hashes so callers can transparently migrate users at successful
    login/change-password time.
    """
    if not raw_password or not stored_hash:
        return False, False
    if LEGACY_SHA256_RE.match(stored_hash):
        digest = __import__('hashlib').sha256(raw_password.encode('utf-8')).hexdigest()
        return hmac.compare_digest(stored_hash, digest), True
    return check_password(raw_password, stored_hash), False


def generate_numeric_code(length: int = 6) -> str:
    """Generate a cryptographically strong numeric code."""
    if length < 6:
        raise ValueError('verification code length must be at least 6')
    upper = 10 ** length
    return f"{secrets.randbelow(upper):0{length}d}"


def hash_auth_token(raw_token: str) -> str:
    """Return a deterministic database-safe hash for a bearer auth token."""
    if not raw_token:
        return ''
    return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()


def issue_auth_token(user, *, save: bool = True) -> str:
    """Create a new bearer token, store only its SHA-256 hash, and return the raw token once.

    Always creates a UserAuthToken row for the new session. When save=True,
    also persists the user.auth_token field immediately. When save=False, the
    caller is responsible for saving user.auth_token later (e.g. as part of a
    larger update_fields batch).
    """
    raw_token = user.generate_token()
    token_hash = hash_auth_token(raw_token)
    now = int(time.time() * 1000)
    from .models import UserAuthToken
    UserAuthToken.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        token_hash=token_hash,
        created_at=now,
        last_used_at=now,
        revoked_at=0,
    )
    user.auth_token = token_hash
    if save:
        user.save(update_fields=['auth_token'])
    return raw_token


def get_user_by_auth_token(raw_token: str, *, migrate_legacy: bool = True):
    """Resolve a bearer token against hashed storage, accepting legacy plain tokens during rollout."""
    if not raw_token:
        raise ValueError('auth token is required')

    from .models import User, UserAuthToken

    token_hash = hash_auth_token(raw_token)
    try:
        token_row = UserAuthToken.objects.select_related('user').get(token_hash=token_hash, revoked_at=0)
        return token_row.user
    except UserAuthToken.DoesNotExist:
        pass

    try:
        return User.objects.get(auth_token=token_hash)
    except User.DoesNotExist:
        pass

    # Backward compatibility for rows created before auth_token hashing. Once a
    # legacy token is used successfully, replace it with its hash and add it to
    # the per-session token table.
    user = User.objects.get(auth_token=raw_token)
    if migrate_legacy:
        now = int(time.time() * 1000)
        user.auth_token = token_hash
        user.save(update_fields=['auth_token'])
        UserAuthToken.objects.get_or_create(
            token_hash=token_hash,
            defaults={
                'id': str(uuid.uuid4()),
                'user': user,
                'created_at': now,
                'last_used_at': now,
                'revoked_at': 0,
            },
        )
    return user


def revoke_auth_token(raw_token: str) -> None:
    """Revoke one bearer token and clear auth caches for immediate logout."""
    if not raw_token:
        return
    from .models import UserAuthToken
    token_hash = hash_auth_token(raw_token)
    now = int(time.time() * 1000)
    UserAuthToken.objects.filter(token_hash=token_hash, revoked_at=0).update(revoked_at=now)
    cache.delete_many([
        f'auth_user:{token_hash}',
        f'valid_token:{token_hash}',
        f'user_id_{token_hash}',
    ])


def hash_verification_code(code: str) -> str:
    """Hash a short verification code with Django's password hasher."""
    return make_password(code)


def verify_verification_code(code: str, stored_hash: str) -> bool:
    """Verify a short code against the stored hash.

    Backward compatibility: if an old database row still contains a six-digit
    plain code, validate it once and let the caller clear/rotate it.
    """
    if not code or not stored_hash:
        return False
    if re.fullmatch(r'\d{6}', stored_hash):
        return hmac.compare_digest(code, stored_hash)
    return check_password(code, stored_hash)


def _is_private_or_local_host(hostname: str) -> bool:
    if not hostname:
        return True
    host = hostname.strip().rstrip('.').lower()
    if host in {'localhost', 'localhost.localdomain'}:
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast
    except ValueError:
        pass
    try:
        addresses = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return True
    return False


def validate_external_https_url(url: str, *, allow_http: bool = False) -> str:
    """Validate an external URL used in user/admin-controlled content."""
    if not url:
        raise ValidationError('URL is required')
    url = url.strip()
    if len(url) > EXTERNAL_URL_MAX_LENGTH:
        raise ValidationError('URL is too long')
    parsed = urlparse(url)
    allowed_schemes = {'https'} | ({'http'} if allow_http else set())
    if parsed.scheme not in allowed_schemes:
        raise ValidationError('Only HTTPS URLs are allowed')
    if not parsed.netloc or parsed.username or parsed.password:
        raise ValidationError('Invalid URL host')
    if _is_private_or_local_host(parsed.hostname or ''):
        raise ValidationError('Private, local, or reserved hosts are not allowed')
    return url


def validate_profile_photo_url(url: str) -> str:
    return validate_external_https_url(url, allow_http=False)


def validate_resource_file_url(url: str) -> str:
    # Resource files are iframe-rendered, so force HTTPS and block local/private hosts.
    return validate_external_https_url(url, allow_http=False)


def save_profile_image_upload(request, user, file_obj) -> str:
    """Validate and save an uploaded profile image, returning an absolute URL."""
    if not file_obj:
        raise ValidationError('Image file is required')
    if getattr(file_obj, 'size', 0) > PROFILE_PHOTO_MAX_BYTES:
        raise ValidationError('Image is too large. Maximum size is 5 MB.')

    original_name = get_valid_filename(getattr(file_obj, 'name', 'profile-photo'))
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in PROFILE_PHOTO_ALLOWED_EXTENSIONS:
        raise ValidationError('Invalid image format. Only JPG, PNG, and WEBP are allowed.')
    content_type = getattr(file_obj, 'content_type', '')
    if content_type and content_type not in PROFILE_PHOTO_CONTENT_TYPES:
        raise ValidationError('Invalid image MIME type.')

    data = file_obj.read(PROFILE_PHOTO_MAX_BYTES + 1)
    if len(data) > PROFILE_PHOTO_MAX_BYTES:
        raise ValidationError('Image is too large. Maximum size is 5 MB.')

    try:
        image = Image.open(BytesIO(data))
        image.verify()
    except (UnidentifiedImageError, OSError):
        raise ValidationError('Uploaded file is not a valid image.')

    image = Image.open(BytesIO(data))
    image_format = image.format
    if image_format not in PROFILE_PHOTO_ALLOWED_FORMATS:
        raise ValidationError('Invalid image format. Only JPG, PNG, and WEBP are allowed.')

    # Strip metadata and normalize the image into a safe format.
    output = BytesIO()
    if image_format == 'PNG':
        safe_ext = '.png'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='PNG', optimize=True)
    elif image_format == 'WEBP':
        safe_ext = '.webp'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='WEBP', quality=90, method=6)
    else:
        safe_ext = '.jpg'
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output, format='JPEG', quality=88, optimize=True)

    filename = f"{user.id}_{secrets.token_urlsafe(16)}{safe_ext}"
    path = default_storage.save(os.path.join('profile_photos', filename), ContentFile(output.getvalue()))
    return request.build_absolute_uri(settings.MEDIA_URL + path)


def save_banner_image_upload(request, user, file_obj) -> str:
    """Validate and save an uploaded banner image, returning an absolute URL.

    Banners are wider than profile photos (typically 11:2.8 aspect) and have a
    larger size allowance. Reuses the same image validation as profile photos
    but stores under a separate subdir and tolerates wider aspect ratios.
    """
    if not file_obj:
        raise ValidationError('Banner file is required')
    if getattr(file_obj, 'size', 0) > PROFILE_PHOTO_MAX_BYTES * 2:
        raise ValidationError('Banner is too large. Maximum size is 10 MB.')

    original_name = get_valid_filename(getattr(file_obj, 'name', 'banner'))
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in PROFILE_PHOTO_ALLOWED_EXTENSIONS:
        raise ValidationError('Invalid image format. Only JPG, PNG, and WEBP are allowed.')
    content_type = getattr(file_obj, 'content_type', '')
    if content_type and content_type not in PROFILE_PHOTO_CONTENT_TYPES:
        raise ValidationError('Invalid image MIME type.')

    data = file_obj.read((PROFILE_PHOTO_MAX_BYTES * 2) + 1)
    if len(data) > PROFILE_PHOTO_MAX_BYTES * 2:
        raise ValidationError('Banner is too large. Maximum size is 10 MB.')

    try:
        image = Image.open(BytesIO(data))
        image.verify()
    except (UnidentifiedImageError, OSError):
        raise ValidationError('Uploaded file is not a valid image.')

    image = Image.open(BytesIO(data))
    image_format = image.format
    if image_format not in PROFILE_PHOTO_ALLOWED_FORMATS:
        raise ValidationError('Invalid image format. Only JPG, PNG, and WEBP are allowed.')

    # Banners keep their original color profile (no alpha) and stay as PNG/JPG/WEBP.
    output = BytesIO()
    if image_format == 'PNG':
        safe_ext = '.png'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='PNG', optimize=True)
    elif image_format == 'WEBP':
        safe_ext = '.webp'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='WEBP', quality=88, method=6)
    else:
        safe_ext = '.jpg'
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output, format='JPEG', quality=85, optimize=True)

    filename = f"{user.id}_banner_{secrets.token_urlsafe(16)}{safe_ext}"
    path = default_storage.save(os.path.join('banner_photos', filename), ContentFile(output.getvalue()))
    return request.build_absolute_uri(settings.MEDIA_URL + path)


POST_IMAGE_MAX_BYTES = 10 * 1024 * 1024  # 10 MB per image
POST_IMAGE_MAX_COUNT = 10
POST_IMAGE_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
POST_IMAGE_ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP', 'GIF'}
POST_IMAGE_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}


def save_post_image_upload(request, file_obj, order=0) -> str:
    """Validate and save an uploaded post image, returning an absolute URL.

    Max 10 MB per image, JPG/PNG/WEBP/GIF only. Images are stored under
    post_images/ with a random filename. Returns the absolute URL.
    """
    if not file_obj:
        raise ValidationError('Image file is required')
    if getattr(file_obj, 'size', 0) > POST_IMAGE_MAX_BYTES:
        raise ValidationError('Image is too large. Maximum size is 10 MB.')

    original_name = get_valid_filename(getattr(file_obj, 'name', 'post-image'))
    ext = os.path.splitext(original_name)[1].lower()
    content_type = getattr(file_obj, 'content_type', '')

    data = file_obj.read(POST_IMAGE_MAX_BYTES + 1)
    if len(data) > POST_IMAGE_MAX_BYTES:
        raise ValidationError('Image is too large. Maximum size is 10 MB.')

    try:
        image = Image.open(BytesIO(data))
        image_format = image.format
        if not image_format:
            image.load()
            image_format = image.format
        else:
            image.load()
    except (UnidentifiedImageError, OSError):
        raise ValidationError('Uploaded file is not a valid image.')

    if image_format not in POST_IMAGE_ALLOWED_FORMATS:
        raise ValidationError('Invalid image format. Only JPG, PNG, WEBP, and GIF are allowed.')

    format_to_ext = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'GIF': '.gif'}
    if ext not in POST_IMAGE_ALLOWED_EXTENSIONS:
        ext = format_to_ext.get(image_format, '')
        if not ext:
            raise ValidationError('Invalid image format. Only JPG, PNG, WEBP, and GIF are allowed.')

    if content_type and content_type not in POST_IMAGE_CONTENT_TYPES:
        content_type_map = {'JPEG': 'image/jpeg', 'PNG': 'image/png', 'WEBP': 'image/webp', 'GIF': 'image/gif'}
        content_type = content_type_map.get(image_format, content_type)

    max_dim = 2000
    if image.width > max_dim or image.height > max_dim:
        image.thumbnail((max_dim, max_dim), Image.LANCZOS)

    output = BytesIO()
    if image_format == 'PNG':
        safe_ext = '.png'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='PNG', optimize=True)
    elif image_format == 'WEBP':
        safe_ext = '.webp'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='WEBP', quality=88, method=6)
    elif image_format == 'GIF':
        safe_ext = '.gif'
        image.save(output, format='GIF', optimize=True)
    else:
        safe_ext = '.jpg'
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output, format='JPEG', quality=88, optimize=True)

    filename = f"post_{secrets.token_urlsafe(12)}_{order}{safe_ext}"
    path = default_storage.save(os.path.join('post_images', filename), ContentFile(output.getvalue()))
    return request.build_absolute_uri(settings.MEDIA_URL + path)


RESOURCE_ALLOWED_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
    '.txt', '.rtf', '.odt', '.ods', '.odp', '.csv',
    '.zip', '.rar', '.7z',
    # NOTE: .svg intentionally excluded — SVG can carry scripts (stored XSS).
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.heic', '.heif',
    '.mp4', '.mkv', '.avi', '.mov', '.webm', '.wmv', '.flv', '.3gp',
    '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma',
    '.epub', '.mobi',
}
RESOURCE_ALLOWED_MIME_PREFIXES = (
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats', 'application/vnd.ms-',
    'application/vnd.oasis.opendocument',
    'text/', 'image/', 'video/', 'audio/',
    'application/zip', 'application/x-rar', 'application/x-7z',
    'application/epub', 'application/x-mobipocket',
    'application/octet-stream',
)
RESOURCE_MAX_BYTES = 50 * 1024 * 1024  # 50 MB


def validate_and_save_resource_file(request, file_obj) -> tuple:
    """Validate an uploaded resource file, compress if possible, and save it.

    Returns (path, file_size, error_response) tuple.
    On success, path is the storage path and file_size is the byte count.
    On failure, path is None and error_response is a dict suitable for Response().
    """
    if not file_obj:
        return None, 0, None

    if getattr(file_obj, 'size', 0) > RESOURCE_MAX_BYTES:
        return None, 0, {'error': f'File is too large. Maximum size is {RESOURCE_MAX_BYTES // (1024*1024)} MB.'}

    original_name = get_valid_filename(getattr(file_obj, 'name', 'resource'))
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in RESOURCE_ALLOWED_EXTENSIONS:
        return None, 0, {'error': f'File type "{ext}" is not allowed. Allowed types: {", ".join(sorted(RESOURCE_ALLOWED_EXTENSIONS))}'}

    content_type = getattr(file_obj, 'content_type', '')
    if content_type and not content_type.startswith(RESOURCE_ALLOWED_MIME_PREFIXES):
        return None, 0, {'error': f'MIME type "{content_type}" is not allowed.'}

    import time as _time
    import uuid as _uuid
    from .compression import compress_resource_file

    try:
        result = compress_resource_file(file_obj, ext)
        if result is not None:
            compressed_content, final_ext = result
            compressed_size = compressed_content.size
            final_name = f"{_uuid.uuid4().hex[:12]}_{int(_time.time())}{final_ext}"
            path = default_storage.save(os.path.join('resources', final_name), compressed_content)
            return path, compressed_size, None
    except Exception:
        pass

    if hasattr(file_obj, 'seek'):
        file_obj.seek(0)

    file_size = getattr(file_obj, 'size', 0)
    filename = f"{_uuid.uuid4().hex[:12]}_{int(_time.time())}{ext}"
    path = default_storage.save(os.path.join('resources', filename), file_obj)

    return path, file_size, None


def make_internal_admin_signature() -> str:
    return TimestampSigner(salt=ADMIN_API_SALT).sign('admin-api')


def verify_internal_admin_signature(value: str, max_age: int = 60) -> bool:
    if not value:
        return False
    try:
        return TimestampSigner(salt=ADMIN_API_SALT).unsign(value, max_age=max_age) == 'admin-api'
    except (BadSignature, SignatureExpired):
        return False

# ---------------------------------------------------------------------------
# Forum media uploads (videos / audio / generic attachments on posts+replies)
# ---------------------------------------------------------------------------

FORUM_MEDIA_MAX_VIDEO_BYTES = 150 * 1024 * 1024  # 150 MB
FORUM_MEDIA_MAX_AUDIO_BYTES = 40 * 1024 * 1024   # 40 MB
FORUM_MEDIA_MAX_FILE_BYTES = 30 * 1024 * 1024    # 30 MB
FORUM_MEDIA_MAX_ABS_BYTES = FORUM_MEDIA_MAX_VIDEO_BYTES

# ext -> (kind, mime). Executable/scriptable types (svg, html, js…) are
# intentionally absent — attachments are never inline-executed markup.
FORUM_MEDIA_TYPES = {
    '.mp4': ('video', 'video/mp4'), '.m4v': ('video', 'video/mp4'),
    '.webm': ('video', 'video/webm'), '.mov': ('video', 'video/quicktime'),
    '.mp3': ('audio', 'audio/mpeg'), '.m4a': ('audio', 'audio/mp4'),
    '.aac': ('audio', 'audio/aac'), '.ogg': ('audio', 'audio/ogg'),
    '.opus': ('audio', 'audio/ogg'), '.wav': ('audio', 'audio/wav'),
    '.flac': ('audio', 'audio/flac'),
    '.pdf': ('file', 'application/pdf'), '.txt': ('file', 'text/plain'),
    '.md': ('file', 'text/markdown'), '.csv': ('file', 'text/csv'),
    '.json': ('file', 'application/json'),
    '.doc': ('file', 'application/msword'),
    '.docx': ('file', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
    '.ppt': ('file', 'application/vnd.ms-powerpoint'),
    '.pptx': ('file', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
    '.xls': ('file', 'application/vnd.ms-excel'),
    '.xlsx': ('file', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    '.zip': ('file', 'application/zip'),
}

_FORUM_MEDIA_MAGIC = (
    (b'%PDF', ('file', 'application/pdf')),
    (b'PK\x03\x04', ('file', 'application/zip')),
    (b'OggS', ('audio', 'audio/ogg')),
    (b'fLaC', ('audio', 'audio/flac')),
    (b'RIFF', ('audio', 'audio/wav')),
    (b'ID3', ('audio', 'audio/mpeg')),
    (b'\xff\xfb', ('audio', 'audio/mpeg')),
    (b'\xff\xf3', ('audio', 'audio/mpeg')),
    (b'\xff\xf2', ('audio', 'audio/mpeg')),
    (b'\x1a\x45\xdf\xa3', ('video', 'video/webm')),
)


def _sniff_forum_media_kind(data: bytes):
    """Light magic-byte validation; returns (kind, mime) or None."""
    head = data[:16]
    if b'ftyp' in data[4:12]:
        return ('video', 'video/mp4')
    for magic, hit in _FORUM_MEDIA_MAGIC:
        if head.startswith(magic):
            return hit
    return None


def save_forum_media_upload(request, file_obj) -> dict:
    """Validate + store one forum attachment. Returns a descriptor dict the
    client echoes back inside the post/reply `attachments` payload:
    {url, kind, name, size, mime}. Raises ValidationError on bad input."""
    if not file_obj:
        raise ValidationError('File is required')

    size = int(getattr(file_obj, 'size', 0) or 0)
    if size <= 0:
        raise ValidationError('File is empty')
    if size > FORUM_MEDIA_MAX_ABS_BYTES:
        raise ValidationError('File is too large. Maximum size is 150 MB.')

    original_name = get_valid_filename(getattr(file_obj, 'name', 'attachment'))[:120] or 'attachment'
    ext = os.path.splitext(original_name)[1].lower()
    kind_mime = FORUM_MEDIA_TYPES.get(ext)

    # Voice-note hint: browser/app recorders produce audio-only webm/mp4
    # containers that extension-based mapping would class as video. An explicit
    # kind_hint=audio field reclasses them (sniff check below still validates).
    kind_hint = ''
    try:
        kind_hint = str(request.data.get('kind_hint', '') or '').strip().lower()
    except Exception:
        kind_hint = ''

    if kind_mime is None and kind_hint == 'audio' and ext == '':
        # Extensionless multipart filename (a recording staged under a display
        # name like "Voice note (0:07)"): class purely by magic bytes. Only
        # reached with an explicit audio hint — everything else still 400s.
        file_obj.seek(0)
        sniffed0 = _sniff_forum_media_kind(file_obj.read(64))
        file_obj.seek(0)
        if sniffed0 is not None:
            s0_kind, s0_mime = sniffed0
            if s0_kind == 'audio':
                kind_mime = ('audio', s0_mime)
            elif s0_mime == 'video/webm':
                kind_mime, ext = ('audio', 'audio/webm'), '.webm'
            elif s0_mime == 'video/mp4':
                kind_mime, ext = ('audio', 'audio/mp4'), '.m4a'
    if kind_mime is None:
        raise ValidationError(
            'Unsupported file type. Videos (mp4/webm/mov), audio (mp3/m4a/ogg/wav/flac) '
            'or documents (pdf/office/txt/zip) only.'
        )
    kind, mime = kind_mime
    if kind_hint == 'audio' and ext in ('.webm', '.mp4', '.m4v'):
        kind = 'audio'
        mime = 'audio/webm' if ext == '.webm' else 'audio/mp4'

    per_kind_limit = {
        'video': FORUM_MEDIA_MAX_VIDEO_BYTES,
        'audio': FORUM_MEDIA_MAX_AUDIO_BYTES,
        'file': FORUM_MEDIA_MAX_FILE_BYTES,
    }[kind]
    if size > per_kind_limit:
        raise ValidationError(
            {'video': 'Videos are limited to 150 MB.',
             'audio': 'Audio files are limited to 40 MB.',
             'file': 'Attachments are limited to 30 MB.'}[kind]
        )

    file_obj.seek(0)
    data = file_obj.read(per_kind_limit + 1)
    if len(data) > per_kind_limit:
        raise ValidationError('File is too large.')

    # Magic-byte check for binary formats; text formats pass through.
    if ext in ('.mp4', '.m4v', '.webm', '.mov', '.mp3', '.m4a', '.aac', '.ogg', '.opus',
               '.wav', '.flac', '.pdf', '.zip', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'):
        sniffed = _sniff_forum_media_kind(data)
        if sniffed is None:
            raise ValidationError('File content does not match its extension.')
        sniffed_kind, sniffed_mime = sniffed
        # Office files are zips; allow zip detection for office extensions.
        office_exts = ('.docx', '.pptx', '.xlsx')
        hinted_audio = kind_hint == 'audio' and kind == 'audio'
        if not (sniffed_kind == kind or (ext in office_exts and sniffed_mime == 'application/zip')
                or (ext == '.m4a' and sniffed_kind == 'video')
                or (hinted_audio and sniffed_mime in ('video/webm', 'video/mp4'))):
            raise ValidationError('File content does not match its extension.')
        if ext not in office_exts and not hinted_audio:
            mime = sniffed_mime

    import secrets as _secrets
    subdir = {'video': 'videos', 'audio': 'audios', 'file': 'files'}[kind]
    filename = f"forum_{_secrets.token_urlsafe(12)}{ext}"
    path = default_storage.save(os.path.join('forum_media', subdir, filename), ContentFile(data))
    return {
        'url': request.build_absolute_uri(settings.MEDIA_URL + path),
        'kind': kind,
        'name': original_name,
        'size': len(data),
        'mime': mime,
    }


FORUM_ATTACHMENTS_MAX_COUNT = 4
FORUM_ATTACHMENTS_MAX_VIDEO = 1


def validate_forum_attachments(raw) -> list:
    """Validate client-supplied attachment descriptors. Urls must point at
    this site's own MEDIA_URL (uploaded via /api/forum/uploads/). Raises
    ValidationError; returns a cleaned list of dicts."""
    if raw in (None, ''):
        return []
    if not isinstance(raw, list):
        raise ValidationError('attachments must be a list')
    cleaned = []
    for item in raw[:FORUM_ATTACHMENTS_MAX_COUNT + 1]:  # +1 so we can error precisely
        if not isinstance(item, dict):
            raise ValidationError('Each attachment must be an object')
        url = str(item.get('url') or '').strip()
        kind = str(item.get('kind') or '').strip().lower()
        if kind not in ('video', 'audio', 'file'):
            raise ValidationError('Invalid attachment kind')
        parsed = urlparse(url)
        media_prefix = settings.MEDIA_URL or '/media/'
        path = parsed.path or url
        if parsed.scheme and parsed.scheme not in ('http', 'https'):
            raise ValidationError('Invalid attachment url')
        if media_prefix not in path:
            raise ValidationError('Attachments must be uploaded through the forum upload endpoint first')
        name = str(item.get('name') or '')[:255]
        mime_type = str(item.get('mime') or item.get('mime_type') or '')[:120]
        try:
            size_bytes = max(0, int(item.get('size') or item.get('size_bytes') or 0))
        except (TypeError, ValueError):
            size_bytes = 0
        cleaned.append({'url': url, 'kind': kind, 'name': name, 'mime_type': mime_type, 'size_bytes': size_bytes})
    if len(cleaned) > FORUM_ATTACHMENTS_MAX_COUNT:
        raise ValidationError(f'Maximum {FORUM_ATTACHMENTS_MAX_COUNT} attachments')
    if sum(1 for a in cleaned if a['kind'] == 'video') > FORUM_ATTACHMENTS_MAX_VIDEO:
        raise ValidationError('Maximum 1 video per post or reply')
    return cleaned


# ---------------------------------------------------------------------------
# Resource thumbnails: explicit cover upload + automatic video frame capture
# ---------------------------------------------------------------------------

RESOURCE_THUMBNAIL_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
RESOURCE_THUMBNAIL_ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP', 'GIF'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.wmv', '.flv', '.3gp', '.m4v'}


def save_resource_thumbnail_upload(request, file_obj):
    """Validate, re-encode and store an uploaded resource cover image.

    Returns the absolute thumbnail URL. Raises ValidationError on bad input.
    """
    if not file_obj:
        raise ValidationError('Thumbnail image is required')
    if getattr(file_obj, 'size', 0) > RESOURCE_THUMBNAIL_MAX_BYTES:
        raise ValidationError('Thumbnail is too large. Maximum size is 10 MB.')
    data = file_obj.read(RESOURCE_THUMBNAIL_MAX_BYTES + 1)
    if len(data) > RESOURCE_THUMBNAIL_MAX_BYTES:
        raise ValidationError('Thumbnail is too large. Maximum size is 10 MB.')
    try:
        image = Image.open(BytesIO(data))
        image.verify()
        image = Image.open(BytesIO(data))
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError('Thumbnail must be a JPG, PNG, WEBP, or GIF image.')

    image_format = (image.format or '').upper()
    if image_format not in RESOURCE_THUMBNAIL_ALLOWED_FORMATS:
        raise ValidationError('Thumbnail must be a JPG, PNG, WEBP, or GIF image.')

    max_dim = 1280
    if image.width > max_dim or image.height > max_dim:
        image.thumbnail((max_dim, max_dim), Image.LANCZOS)

    output = BytesIO()
    if image_format == 'PNG':
        safe_ext = '.png'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='PNG', optimize=True)
    elif image_format == 'WEBP':
        safe_ext = '.webp'
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        image.save(output, format='WEBP', quality=88, method=6)
    elif image_format == 'GIF':
        safe_ext = '.gif'
        image.save(output, format='GIF', optimize=True)
    else:
        safe_ext = '.jpg'
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output, format='JPEG', quality=88, optimize=True)

    filename = f"res_{secrets.token_urlsafe(12)}{safe_ext}"
    path = default_storage.save(os.path.join('resource_thumbnails', filename), ContentFile(output.getvalue()))
    return request.build_absolute_uri(settings.MEDIA_URL + path)


def is_video_file_path(path) -> bool:
    return os.path.splitext(str(path or ''))[1].lower() in VIDEO_EXTENSIONS


def extract_video_thumbnail_frame(video_storage_path):
    """Extract a cover frame from a stored video with ffmpeg.

    Returns the storage-relative thumbnail path, or None on any failure
    (missing ffmpeg, non-local storage, unreadable/short video). Purely
    best-effort; never raises.
    """
    import shutil
    import subprocess
    import tempfile

    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg or not video_storage_path:
        return None
    try:
        video_abs = default_storage.path(str(video_storage_path))
    except Exception:
        return None
    if not os.path.exists(video_abs):
        return None

    tmp_fd, tmp_out = tempfile.mkstemp(suffix='.jpg')
    os.close(tmp_fd)

    def _run(seek_seconds):
        cmd = [
            ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
            '-ss', str(seek_seconds), '-i', video_abs,
            '-frames:v', '1', '-vf', "scale='min(640,iw)':-2",
            '-q:v', '4', tmp_out,
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=30, check=False)
        except Exception:
            return False
        return os.path.exists(tmp_out) and os.path.getsize(tmp_out) > 0

    try:
        if not _run(1) and not _run(0):
            return None
        with open(tmp_out, 'rb') as fh:
            data = fh.read()
        filename = f"video_{secrets.token_urlsafe(12)}.jpg"
        return default_storage.save(os.path.join('resource_thumbnails', filename), ContentFile(data))
    except Exception:
        return None
    finally:
        try:
            os.unlink(tmp_out)
        except OSError:
            pass


def maybe_autoset_video_thumbnail(resource, request=None):
    """Auto-assign a cover frame for a stored video that has no thumbnail.

    Sets ``resource.thumbnail_url`` (absolute URL) and saves when extraction
    succeeds. Returns the URL that was set, or '' when nothing changed.
    Never raises — upload flows must not fail because of ffmpeg.
    """
    try:
        if getattr(resource, 'thumbnail_url', ''):
            return ''
        file_path = str(getattr(resource, 'file', '') or '')
        if not is_video_file_path(file_path):
            return ''
        thumb_rel = extract_video_thumbnail_frame(file_path)
        if not thumb_rel:
            return ''
        if request is not None:
            url = request.build_absolute_uri(settings.MEDIA_URL + thumb_rel)
        else:
            base = getattr(settings, 'SITE_URL', 'https://nebians.consica.com.np').rstrip('/')
            url = base + settings.MEDIA_URL + thumb_rel
        resource.thumbnail_url = url
        resource.save(update_fields=['thumbnail_url'])
        return url
    except Exception:
        return ''
