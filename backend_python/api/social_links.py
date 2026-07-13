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
        raise ValidationError('URL is required')
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
