"""Security helpers for NEBians.

Centralizes authentication-adjacent helpers so API and web views follow the
same validation and production safety rules.
"""
import hmac
import ipaddress
import os
import re
import secrets
import socket
from io import BytesIO
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
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
ADMIN_API_SALT = 'nebians.admin-api.v1'
LEGACY_SHA256_RE = re.compile(r'^[a-f0-9]{64}$')


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


def make_internal_admin_signature() -> str:
    return TimestampSigner(salt=ADMIN_API_SALT).sign('admin-api')


def verify_internal_admin_signature(value: str, max_age: int = 60) -> bool:
    if not value:
        return False
    try:
        return TimestampSigner(salt=ADMIN_API_SALT).unsign(value, max_age=max_age) == 'admin-api'
    except (BadSignature, SignatureExpired):
        return False
