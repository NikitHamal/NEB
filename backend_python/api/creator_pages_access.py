"""Creator marketplace — who gets a storefront, and who may open a course.

`check_user_course_access` is deliberately shaped like
`check_user_resource_access`: same return tuple, same reason strings, so a
client can drive one purchase state machine for both kinds of paid content.
"""
from decimal import Decimal

from .creator_pages_schema import ELIGIBLE_ROLES
from .models import PaymentVerification, User


def can_have_storefront(user):
    if user is None:
        return False
    if getattr(user, 'is_admin', False):
        return True
    if getattr(user, 'is_banned', False) or getattr(user, 'is_locked', False):
        return False
    return getattr(user, 'role', '') in ELIGIBLE_ROLES


def allowed_kinds(user):
    if user is None:
        return []
    if getattr(user, 'is_admin', False):
        return ['admin', 'institute', 'tutor']
    if getattr(user, 'role', '') == User.ROLE_INSTITUTION:
        return ['institute', 'tutor']
    return ['tutor']


def default_kind_for(user):
    kinds = allowed_kinds(user)
    return kinds[0] if kinds else 'tutor'


def check_user_course_access(user, course):
    """Mirror of check_user_resource_access() for paid courses.

    Returns (has_access, reason, purchase|None) with the same reasons so a
    client can render one purchase state machine for both kinds."""
    if course is None:
        return False, 'missing', None
    if course.is_free or not course.price or Decimal(course.price) <= 0:
        return True, 'free', None
    if user is None:
        return False, 'unpurchased', None
    if course.page_id and course.page.user_id == getattr(user, 'id', None):
        return True, 'owner', None
    if getattr(user, 'is_admin', False):
        return True, 'admin', None
    purchase = (PaymentVerification.objects
                .filter(buyer_id=user.id, course_id=course.id)
                .order_by('-created_at')
                .first())
    if purchase:
        if purchase.status == 'approved':
            return True, 'purchased', purchase
        if purchase.status == 'pending':
            return False, 'pending_verification', purchase
        if purchase.status == 'rejected':
            return False, 'rejected', purchase
    return False, 'unpurchased', None
