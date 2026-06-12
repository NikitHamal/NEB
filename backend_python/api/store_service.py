"""Cosmetics store business logic — purchase, equip, and store state."""
import time
import uuid

from django.db import transaction
from django.db.models import F

from .models import User, UserCosmetic
from .store_catalog import all_categories, get_item

EQUIP_FIELDS = {
    'theme': 'equipped_theme',
    'banner': 'equipped_banner',
    'border': 'equipped_border',
    'badge': 'equipped_badge',
}


def _equipped_dict(user):
    return {
        'theme': user.equipped_theme or '',
        'banner': user.equipped_banner or '',
        'border': user.equipped_border or '',
        'badge': user.equipped_badge or '',
    }


def _create_cosmetic(user, item, price_paid):
    return UserCosmetic.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        item_id=item['id'],
        item_type=item['type'],
        price_paid=price_paid,
        acquired_at=int(time.time() * 1000),
    )


def get_store_state(user):
    owned_ids = []
    equipped = {'theme': '', 'banner': '', 'border': '', 'badge': ''}
    points_balance = None
    if user is not None:
        owned_ids = list(
            UserCosmetic.objects.filter(user_id=user.pk).values_list('item_id', flat=True)
        )
        equipped = _equipped_dict(user)
        points_balance = user.points_balance
    return {
        'categories': all_categories(),
        'owned_ids': owned_ids,
        'equipped': equipped,
        'points_balance': points_balance,
    }


def purchase_item(user, item_id):
    item = get_item(item_id)
    if not item:
        return False, 'Unknown item'
    if UserCosmetic.objects.filter(user_id=user.pk, item_id=item_id).exists():
        return False, 'Already owned'
    price = int(item['price'])
    if price <= 0:
        _create_cosmetic(user, item, 0)
        user.refresh_from_db(fields=['points_balance'])
        return True, {'points_balance': user.points_balance}
    with transaction.atomic():
        updated = User.objects.filter(pk=user.pk, points_balance__gte=price).update(
            points_balance=F('points_balance') - price,
        )
        if not updated:
            return False, 'Not enough points'
        _create_cosmetic(user, item, price)
    user.refresh_from_db(fields=['points_balance'])
    return True, {'points_balance': user.points_balance}


def equip_item(user, item_id):
    item = get_item(item_id)
    if not item:
        return False, 'Unknown item'
    if not UserCosmetic.objects.filter(user_id=user.pk, item_id=item_id).exists():
        return False, 'Item not owned'
    field = EQUIP_FIELDS[item['type']]
    setattr(user, field, item_id)
    user.save(update_fields=[field])
    return True, _equipped_dict(user)


def unequip_item(user, item_type):
    field = EQUIP_FIELDS.get(item_type)
    if not field:
        return False, 'Unknown item type'
    setattr(user, field, '')
    user.save(update_fields=[field])
    return True, _equipped_dict(user)
