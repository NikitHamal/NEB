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


def _settled(user, course):
    """The part of the decision that needs no query, or None if a purchase
    lookup is the only thing left to check."""
    if course.is_free or not course.price or Decimal(course.price) <= 0:
        return True, 'free', None
    if user is None:
        return False, 'unpurchased', None
    if course.page_id and course.page.user_id == getattr(user, 'id', None):
        return True, 'owner', None
    if getattr(user, 'is_admin', False):
        return True, 'admin', None
    return None


def _from_purchase(purchase):
    if purchase:
        if purchase.status == 'approved':
            return True, 'purchased', purchase
        if purchase.status == 'pending':
            return False, 'pending_verification', purchase
        if purchase.status == 'rejected':
            return False, 'rejected', purchase
    return False, 'unpurchased', None


def check_user_course_access(user, course):
    """Mirror of check_user_resource_access() for paid courses.

    Returns (has_access, reason, purchase|None) with the same reasons so a
    client can render one purchase state machine for both kinds."""
    if course is None:
        return False, 'missing', None
    settled = _settled(user, course)
    if settled is not None:
        return settled
    # Approved first, newest second. Access a buyer has paid for is permanent:
    # deciding on the newest row alone meant a stray later submission (a retried
    # POST, a duplicate an admin then rejected) took the course away from
    # someone who had already paid for it.
    purchase = (PaymentVerification.objects
                .filter(buyer_id=user.id, course_id=course.id)
                .order_by('-created_at')
                .first())
    if purchase is not None and purchase.status != 'approved':
        approved = (PaymentVerification.objects
                    .filter(buyer_id=user.id, course_id=course.id, status='approved')
                    .order_by('-created_at')
                    .first())
        purchase = approved or purchase
    return _from_purchase(purchase)


def course_access_map(user, courses):
    """The same decision for a whole list, in one query instead of one each.

    A marketplace shelf of 48 offerings used to cost 48 PaymentVerification
    lookups for any signed-in visitor. Ordering newest-first and keeping the
    first row per course reproduces the single-course `.first()` exactly.
    """
    courses = list(courses)
    decided = {}
    pending = []
    for course in courses:
        settled = _settled(user, course)
        if settled is not None:
            decided[course.id] = settled
        else:
            pending.append(course)
    if pending:
        best = {}
        rows = (PaymentVerification.objects
                .filter(buyer_id=user.id, course_id__in=[c.id for c in pending])
                .order_by('-created_at'))
        for row in rows:
            # same precedence as the single-course check: an approved row wins
            # over a newer one of any other status
            current = best.get(row.course_id)
            if current is None or (current.status != 'approved' and row.status == 'approved'):
                best[row.course_id] = row
        for course in pending:
            decided[course.id] = _from_purchase(best.get(course.id))
    return decided


def sold_course_delete_error(course):
    """Why this course may not be deleted, or None.

    `PaymentVerification.course` is SET_NULL, so deleting an offering someone
    paid for would quietly detach the receipt: the buyer loses the access the
    row granted and the seller loses the sale from their ledger. Archiving takes
    it off the shelf without touching anybody's purchase.
    """
    if course is None:
        return None
    sold = PaymentVerification.objects.filter(course_id=course.id, status='approved').count()
    if not sold:
        return None
    return (f'{sold} student{"s" if sold != 1 else ""} already bought this course, so it cannot be '
            'deleted. Archive it instead to take it off your page.')
