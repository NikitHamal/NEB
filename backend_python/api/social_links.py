"""Social links CRUD service functions used by web views."""
import json
from django.db import transaction
from django.core.exceptions import ValidationError
from api.models import SocialLink, SOCIAL_PLATFORMS
from api.security import validate_external_https_url
from api.utils import now_ms, uuid_str

MAX_LINKS_PER_USER = 15


def _validate_social_url(url, platform):
    url = (url or '').strip()
    if not url:
        raise ValidationError('URL or username is required')
    
    if not (url.startswith('http://') or url.startswith('https://')):
        # Automatically convert username/handle to direct platform link
        if platform == 'instagram':
            url = f'https://instagram.com/{url}'
        elif platform == 'facebook':
            url = f'https://facebook.com/{url}'
        elif platform == 'twitter':
            url = f'https://x.com/{url}'
        elif platform == 'youtube':
            username = url if url.startswith('@') else f'@{url}'
            url = f'https://youtube.com/{username}'
        elif platform == 'tiktok':
            username = url if url.startswith('@') else f'@{url}'
            url = f'https://tiktok.com/{username}'
        elif platform == 'linkedin':
            url = f'https://linkedin.com/in/{url}'
        elif platform == 'github':
            url = f'https://github.com/{url}'
        elif platform == 'telegram':
            url = f'https://t.me/{url}'
        elif platform == 'whatsapp':
            phone = ''.join(c for c in url if c.isdigit())
            url = f'https://wa.me/{phone}'
        elif platform == 'snapchat':
            url = f'https://snapchat.com/add/{url}'
        elif platform == 'pinterest':
            url = f'https://pinterest.com/{url}'
        elif platform == 'reddit':
            url = f'https://reddit.com/user/{url}'
        elif platform == 'website':
            url = f'https://{url}'

    if len(url) > 500:
        raise ValidationError('URL is too long')
    try:
        url = validate_external_https_url(url, allow_http=False)
    except ValidationError:
        raise ValidationError('Only HTTPS URLs are allowed')
    return url


def get_user_links(user_id):
    links = SocialLink.objects.filter(user_id=user_id, is_visible=True).order_by('sort_order', 'created_at')
    return [_serialize_link(l) for l in links]


def get_all_user_links(user_id):
    links = SocialLink.objects.filter(user_id=user_id).order_by('sort_order', 'created_at')
    return [_serialize_link(l) for l in links]


def _serialize_link(link):
    platform_info = SOCIAL_PLATFORMS.get(link.platform, SOCIAL_PLATFORMS['website'])
    domain = ''
    if link.platform == 'website':
        from urllib.parse import urlparse
        try:
            domain = urlparse(link.url).netloc
            if not domain:
                domain = urlparse('https://' + link.url).netloc
            # Remove www.
            if domain.lower().startswith('www.'):
                domain = domain[4:]
        except Exception:
            domain = ''
    return {
        'id': link.id,
        'platform': link.platform,
        'platform_label': platform_info['label'],
        'icon': platform_info['icon'],
        'color': platform_info['color'],
        'url': link.url,
        'label': link.label or '',
        'sort_order': link.sort_order,
        'is_visible': link.is_visible,
        'website_domain': domain,
    }


def create_link(user_id, platform, url, label=''):
    if SocialLink.objects.filter(user_id=user_id).count() >= MAX_LINKS_PER_USER:
        raise ValidationError(f'Maximum {MAX_LINKS_PER_USER} social links allowed')
    if platform not in SOCIAL_PLATFORMS:
        platform = 'website'
    url = _validate_social_url(url, platform)
    label = (label or '').strip()[:100]
    current_max = SocialLink.objects.filter(user_id=user_id).count()
    link = SocialLink.objects.create(
        id=uuid_str(),
        user_id=user_id,
        platform=platform,
        url=url,
        label=label,
        sort_order=current_max,
        created_at=now_ms(),
    )
    return _serialize_link(link)


def update_link(user_id, link_id, platform=None, url=None, label=None):
    try:
        link = SocialLink.objects.get(id=link_id, user_id=user_id)
    except SocialLink.DoesNotExist:
        raise ValidationError('Link not found')
    if platform is not None:
        if platform not in SOCIAL_PLATFORMS:
            platform = 'website'
        link.platform = platform
    if url is not None:
        link.url = _validate_social_url(url, link.platform)
    if label is not None:
        link.label = (label or '').strip()[:100]
    link.save()
    return _serialize_link(link)


def delete_link(user_id, link_id):
    deleted, _ = SocialLink.objects.filter(id=link_id, user_id=user_id).delete()
    if not deleted:
        raise ValidationError('Link not found')
    return True


def reorder_links(user_id, ordered_ids):
    with transaction.atomic():
        for idx, link_id in enumerate(ordered_ids):
            SocialLink.objects.filter(id=link_id, user_id=user_id).update(sort_order=idx)
    return get_all_user_links(user_id)
