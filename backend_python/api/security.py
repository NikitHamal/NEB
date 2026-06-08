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
POST_IMAGE_MAX_COUNT = 3
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
    '.txt', '.rtf', '.odt', '.ods', '.odp',
    '.zip', '.rar', '.7z',
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg',
    '.mp4', '.mkv', '.avi', '.mov', '.webm',
    '.mp3', '.wav', '.ogg', '.flac', '.aac',
    '.epub', '.mobi',
}
RESOURCE_ALLOWED_MIME_PREFIXES = (
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats', 'application/vnd.ms-',
    'application/vnd.oasis.opendocument',
    'text/', 'image/', 'video/', 'audio/',
    'application/zip', 'application/x-rar', 'application/x-7z',
    'application/epub', 'application/x-mobipocket',
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
