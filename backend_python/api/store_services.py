"""
Service functions for the cosmetics store — claiming, purchasing, and
equipping items with the spendable points balance.
Spendable balance = max(0, contribution_score - points_spent).
"""
import logging
import time

from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import F

from .models import User
from .models_store import UserCosmetic, PointsLedger
from . import store_catalog

logger = logging.getLogger(__name__)

_KIND_FIELD = {
    'theme': 'equipped_theme',
    'banner': 'equipped_banner',
    'border': 'equipped_border',
    'badge': 'equipped_badge',
}


def _now_ms():
    return int(time.time() * 1000)


def get_spendable_balance(user):
    return max(0, (user.contribution_score or 0) - (user.points_spent or 0))


def get_owned_keys(user_id):
    return set(UserCosmetic.objects.filter(user_id=user_id).values_list('item_key', flat=True))


def claim_or_purchase(user, key):
    item = store_catalog.get_item(key)
    if not item:
        raise ValueError('Item not found')
    if user.is_locked:
        raise ValueError('Account is locked')
    if UserCosmetic.objects.filter(user_id=user.id, item_key=key).exists():
        return {
            'ok': True, 'key': key, 'kind': item['kind'], 'owned': True,
            'alreadyOwned': True, 'balance': get_spendable_balance(user),
        }
    price = item['price']
    now = _now_ms()
    if price > 0:
        with transaction.atomic():
            locked_user = User.objects.select_for_update().get(pk=user.id)
            balance = get_spendable_balance(locked_user)
            if balance < price:
                raise ValueError('Not enough points')
            User.objects.filter(pk=user.id).update(points_spent=F('points_spent') + price)
            new_balance = balance - price
            try:
                UserCosmetic.objects.create(
                    user_id=user.id, item_key=key, kind=item['kind'],
                    price_paid=price, acquired_at=now,
                )
            except IntegrityError:
                return {
                    'ok': True, 'key': key, 'kind': item['kind'], 'owned': True,
                    'alreadyOwned': True, 'balance': balance,
                }
            PointsLedger.objects.create(
                user_id=user.id, delta=-price, reason='store_purchase',
                item_key=key, balance_after=new_balance, created_at=now,
            )
    else:
        balance = get_spendable_balance(user)
        new_balance = balance
        try:
            UserCosmetic.objects.create(
                user_id=user.id, item_key=key, kind=item['kind'],
                price_paid=0, acquired_at=now,
            )
        except IntegrityError:
            return {
                'ok': True, 'key': key, 'kind': item['kind'], 'owned': True,
                'alreadyOwned': True, 'balance': balance,
            }
        PointsLedger.objects.create(
            user_id=user.id, delta=0, reason='store_claim',
            item_key=key, balance_after=new_balance, created_at=now,
        )
    return {'ok': True, 'key': key, 'kind': item['kind'], 'owned': True, 'balance': new_balance}


def equip_item(user, key):
    item = store_catalog.get_item(key)
    if not item:
        raise ValueError('Item not found')
    if user.is_locked:
        raise ValueError('Account is locked')
    owned = UserCosmetic.objects.filter(user_id=user.id, item_key=key).exists()
    if not owned:
        if item['price'] > 0:
            raise ValueError('You do not own this item')
        claim_or_purchase(user, key)
    field = _KIND_FIELD[item['kind']]
    User.objects.filter(pk=user.id).update(**{field: key})
    cache.delete(f'store_equips:{user.id}')
    refreshed = User.objects.filter(pk=user.id).only('contribution_score', 'points_spent').first()
    balance = get_spendable_balance(refreshed) if refreshed else 0
    return {'ok': True, 'key': key, 'kind': item['kind'], 'equipped': True, 'balance': balance}


def unequip_item(user, kind):
    if kind not in store_catalog.KINDS:
        raise ValueError('Invalid item kind')
    field = _KIND_FIELD[kind]
    User.objects.filter(pk=user.id).update(**{field: ''})
    cache.delete(f'store_equips:{user.id}')
    return {'ok': True, 'kind': kind, 'equipped': False}


def get_equipped(user_id):
    def _load():
        row = (User.objects.filter(pk=user_id)
               .values('equipped_theme', 'equipped_banner', 'equipped_border', 'equipped_badge')
               .first())
        if not row:
            return {'theme': '', 'banner': '', 'border': '', 'badge': ''}
        return {
            'theme': row['equipped_theme'] or '',
            'banner': row['equipped_banner'] or '',
            'border': row['equipped_border'] or '',
            'badge': row['equipped_badge'] or '',
        }
    return cache.get_or_set(f'store_equips:{user_id}', _load, 300)


def _serialize_item(item, owned_keys, equipped):
    data = {k: v for k, v in item.items() if k not in ('card_rgb1', 'card_rgb2')}
    data['owned'] = item['key'] in owned_keys
    data['equipped'] = equipped.get(item['kind'], '') == item['key']
    return data


def serialize_store(user_or_none):
    if user_or_none:
        balance = get_spendable_balance(user_or_none)
        score = user_or_none.contribution_score or 0
        owned_keys = get_owned_keys(user_or_none.id)
        equipped = get_equipped(user_or_none.id)
    else:
        balance = 0
        score = 0
        owned_keys = set()
        equipped = {}
    return {
        'balance': balance,
        'score': score,
        'kinds': {
            kind: [_serialize_item(item, owned_keys, equipped)
                   for item in store_catalog.items_of_kind(kind)]
            for kind in store_catalog.KINDS
        },
    }
