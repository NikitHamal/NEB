"""Marketplace economy: company payment config, commission, Nebians points and
AI credits.

Business rules (per the platform model):
  * Buyers pay the COMPANY QR (not the seller). An admin verifies the payment
    screenshot/transaction, then the system credits the seller's wallet.
  * Commission: ``commission_percent`` of the sale amount (default 2.5%).
  * On approval the seller earns (amount − commission) into their wallet; the
    buyer's total_spent increases; both earn Nebians points.
  * Sellers withdraw once their wallet reaches ``withdraw_min`` (Rs. 1,000).
  * Nebians points convert to AI credits at ``points_to_credit`` (2 points = 1).
  * Each month every user gets ``free_credits_per_month`` (10) free AI credits;
    unused free credits are lost at month rollover. Purchased/earned credits
    (``ai_credits``) persist across months. Spending consumes free credits first.
"""
import time
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import F

from .models import User, SellerBalance, PaymentConfig
from .utils import now_ms


def get_payment_config():
    """Return the singleton PaymentConfig row, creating a sane default."""
    cfg, _ = PaymentConfig.objects.get_or_create(
        pk=1,
        defaults={
            'company_qr_url': '',
            'payment_instructions': (
                'Pay the exact amount to the NEBians company QR using eSewa, '
                'Khalti, mobile banking or ConnectIPS, then submit your '
                'transaction reference or a payment screenshot. Your access '
                'unlocks after our team verifies the payment.'
            ),
            'updated_at': now_ms(),
        },
    )
    return cfg


def _q2(value):
    return (value or Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def compute_commission(amount, cfg=None):
    """Platform commission on a sale amount."""
    cfg = cfg or get_payment_config()
    amount = Decimal(amount or 0)
    return _q2(amount * (cfg.commission_percent or 0) / Decimal(100))


def seller_earnings_for(amount, cfg=None):
    cfg = cfg or get_payment_config()
    return _q2(Decimal(amount or 0) - compute_commission(amount, cfg))


def _points_for(amount, per_rupee):
    """Integer Nebians points for a rupee amount given a per-rupee rate."""
    raw = Decimal(amount or 0) * Decimal(per_rupee or 0)
    return int(raw.to_integral_value(rounding=ROUND_HALF_UP))


@transaction.atomic
def grant_purchase_rewards(payment, cfg=None):
    """Credit seller wallet + Nebians points (buyer & seller) + buyer spend.

    Called once, at admin approval. Idempotent-ish: it does not re-grant if the
    payment is already approved (callers gate on status == 'approved').
    """
    cfg = cfg or get_payment_config()
    buyer_pts = _points_for(payment.amount, cfg.points_per_rupee_buyer)
    seller_pts = _points_for(payment.seller_earnings, cfg.points_per_rupee_seller)

    if payment.buyer_id:
        User.objects.filter(pk=payment.buyer_id).update(
            nebians_points=F('nebians_points') + buyer_pts,
            total_spent=F('total_spent') + Decimal(payment.amount or 0),
        )
    if payment.seller_id:
        User.objects.filter(pk=payment.seller_id).update(
            nebians_points=F('nebians_points') + seller_pts,
        )
        bal, _ = SellerBalance.objects.get_or_create(user_id=payment.seller_id, defaults={
            'total_earned': 0, 'total_withdrawn': 0, 'current_balance': 0, 'updated_at': now_ms(),
        })
        bal.total_earned = _q2(bal.total_earned) + _q2(payment.seller_earnings)
        bal.current_balance = _q2(bal.current_balance) + _q2(payment.seller_earnings)
        bal.updated_at = now_ms()
        bal.save()
    return buyer_pts, seller_pts


def current_month():
    return time.strftime('%Y-%m')


def ensure_monthly_free_credits(user, cfg=None):
    """Grant the month's free AI credits on first activity in a new month.
    Unused free credits are dropped (reset semantics). Returns the refreshed
    (free_credits, month) tuple."""
    cfg = cfg or get_payment_config()
    month = current_month()
    if not user or user.free_credits_month == month:
        return user.free_credits if user else 0, month
    updated = User.objects.filter(pk=user.pk).exclude(free_credits_month=month).update(
        free_credits=cfg.free_credits_per_month,
        free_credits_month=month,
    )
    if updated:
        user.free_credits = cfg.free_credits_per_month
        user.free_credits_month = month
    return user.free_credits, month


def total_ai_credits(user, cfg=None):
    cfg = cfg or get_payment_config()
    ensure_monthly_free_credits(user, cfg)
    return (user.ai_credits or 0) + (user.free_credits or 0)


@transaction.atomic
def consume_ai_credit(user, cfg=None):
    """Spend one AI credit for a generation. Free credits are spent first.
    Returns True if a credit was available & consumed, False otherwise."""
    cfg = cfg or get_payment_config()
    if user is None:
        return False
    ensure_monthly_free_credits(user, cfg)
    if user.free_credits and user.free_credits > 0:
        rows = User.objects.filter(pk=user.pk, free_credits__gt=0).update(free_credits=F('free_credits') - 1)
        if rows:
            user.free_credits = max(0, (user.free_credits or 0) - 1)
            return True
    if user.ai_credits and user.ai_credits > 0:
        rows = User.objects.filter(pk=user.pk, ai_credits__gt=0).update(ai_credits=F('ai_credits') - 1)
        if rows:
            user.ai_credits = max(0, (user.ai_credits or 0) - 1)
            return True
    return False


@transaction.atomic
def convert_points_to_credits(user, points, cfg=None):
    """Convert whole Nebians points into AI credits at points_to_credit rate.
    Returns (credits_gained, points_used) or raises ValueError on bad input."""
    cfg = cfg or get_payment_config()
    try:
        points = int(points)
    except (TypeError, ValueError):
        raise ValueError('Invalid points amount')
    rate = cfg.points_to_credit or 1
    if points < rate:
        raise ValueError(f'Minimum {rate} points are required for a conversion')
    if points > (user.nebians_points or 0):
        raise ValueError('You do not have that many Nebians points')
    credits = points // rate
    used = credits * rate
    User.objects.filter(pk=user.pk).update(
        nebians_points=F('nebians_points') - used,
        ai_credits=F('ai_credits') + credits,
    )
    user.nebians_points = max(0, (user.nebians_points or 0) - used)
    user.ai_credits = (user.ai_credits or 0) + credits
    return credits, used
