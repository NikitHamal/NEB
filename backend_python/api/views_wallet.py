"""Wallet, purchases, withdrawals, Nebians points & AI credits API for the
Android app. All endpoints are buyer-scoped (require a signed-in user)."""
from .view_helpers import *  # noqa: F401,F403
from .models import PaymentVerification, WithdrawalRequest
from .marketplace import (
    get_payment_config, convert_points_to_credits, ensure_monthly_free_credits,
    total_ai_credits,
)
from decimal import Decimal


def _balance_for(user):
    bal = getattr(user, 'seller_balance', None)
    if bal is None:
        from .models import SellerBalance
        bal, _ = SellerBalance.objects.get_or_create(
            user=user, defaults={'total_earned': 0, 'total_withdrawn': 0, 'current_balance': 0, 'updated_at': now_ms()}
        )
    return bal


def _rs(value):
    try:
        f = float(value or 0)
    except (TypeError, ValueError):
        f = 0.0
    return ('%g' % f) if f else '0'


@api_view(['GET'])
def wallet_overview(request):
    """Balance, lifetime totals, Nebians points and AI credits for the viewer."""
    user, err = _require_user(request)
    if err:
        return err
    cfg = get_payment_config()
    ensure_monthly_free_credits(user, cfg)
    bal = _balance_for(user)
    pending_withdrawals = WithdrawalRequest.objects.filter(user=user, status='pending').count()
    return Response({
        'currency': 'NPR',
        'current_balance': _rs(bal.current_balance),
        'total_earned': _rs(bal.total_earned),
        'total_withdrawn': _rs(bal.total_withdrawn),
        'pending_withdrawals': pending_withdrawals,
        'withdraw_min': _rs(cfg.withdraw_min),
        'total_spent': _rs(user.total_spent),
        'nebians_points': user.nebians_points or 0,
        'ai_credits_purchased': user.ai_credits or 0,
        'ai_credits_free': user.free_credits or 0,
        'ai_credits_total': total_ai_credits(user, cfg),
        'free_credits_per_month': cfg.free_credits_per_month,
        'points_to_credit': cfg.points_to_credit,
    })


@api_view(['GET'])
def wallet_purchases(request):
    """Purchase history for the viewer (resources they paid for) with status."""
    user, err = _require_user(request)
    if err:
        return err
    qs = (PaymentVerification.objects
          .filter(buyer=user)
          .select_related('resource', 'seller')
          .order_by('-created_at'))[:100]
    items = []
    for p in qs:
        items.append({
            'id': p.id,
            'resource_id': p.resource_id,
            'resource_title': p.resource.title if p.resource else '(removed)',
            'amount': _rs(p.amount),
            'status': p.status,
            'transaction_id': p.transaction_id or '',
            'payment_proof_url': p.payment_proof_url or '',
            'admin_notes': p.admin_notes or '',
            'created_at': p.created_at,
            'verified_at': p.verified_at,
        })
    return Response({'purchases': items, 'total_spent': _rs(user.total_spent)})


@api_view(['GET', 'POST'])
def wallet_withdrawals(request):
    """GET — withdrawal history. POST — request a new withdrawal (>= withdraw_min)."""
    user, err = _require_user(request)
    if err:
        return err
    cfg = get_payment_config()

    if request.method == 'GET':
        qs = WithdrawalRequest.objects.filter(user=user).order_by('-created_at')[:50]
        return Response({
            'withdrawals': [{
                'id': w.id,
                'amount': _rs(w.amount),
                'payout_method': w.payout_method,
                'payout_details': w.payout_details,
                'status': w.status,
                'admin_notes': w.admin_notes or '',
                'created_at': w.created_at,
                'processed_at': w.processed_at,
            } for w in qs],
            'withdraw_min': _rs(cfg.withdraw_min),
            'current_balance': _rs(_balance_for(user).current_balance),
        })

    # POST — create a withdrawal request
    data = request.data
    try:
        amount = Decimal(str(data.get('amount') or '0').strip())
    except Exception:
        return Response({'error': 'Enter a valid amount'}, status=400)
    if amount <= 0:
        return Response({'error': 'Enter a valid amount'}, status=400)
    if amount < (cfg.withdraw_min or Decimal('1000')):
        return Response({'error': f'Minimum withdrawal is Rs. {_rs(cfg.withdraw_min)}'}, status=400)

    payout_method = (data.get('payout_method') or 'esewa').strip()
    valid_methods = [c[0] for c in WithdrawalRequest.PAYOUT_METHODS]
    if payout_method not in valid_methods:
        payout_method = 'esewa'
    payout_details = (data.get('payout_details') or '').strip()
    if not payout_details:
        return Response({'error': 'Please provide your payout account details'}, status=400)

    bal = _balance_for(user)
    if amount > (bal.current_balance or 0):
        return Response({'error': 'Amount exceeds your available balance'}, status=400)

    w = WithdrawalRequest.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        amount=amount,
        payout_method=payout_method,
        payout_details=payout_details[:1000],
        status='pending',
        created_at=now_ms(),
    )
    # Reserve the funds immediately so the user can't double-request.
    bal.current_balance = (bal.current_balance or 0) - amount
    bal.updated_at = now_ms()
    bal.save()
    return Response({
        'id': w.id,
        'amount': _rs(w.amount),
        'payout_method': w.payout_method,
        'status': w.status,
        'created_at': w.created_at,
        'message': 'Withdrawal request submitted. Funds arrive within 7 days.',
    }, status=201)


@api_view(['GET'])
def payments_config(request):
    """Public marketplace config the app needs to render the checkout sheet:
    company QR, instructions, and the withdraw floor. Auth optional."""
    cfg = get_payment_config()
    return Response({
        'company_qr_url': cfg.company_qr_url or '',
        'company_qr_caption': cfg.company_qr_caption or 'NEBians — Company QR',
        'payment_instructions': cfg.payment_instructions or '',
        'upi_id': cfg.upi_id or '',
        'commission_percent': _rs(cfg.commission_percent),
        'withdraw_min': _rs(cfg.withdraw_min),
    })


@api_view(['GET', 'POST'])
def credits_overview(request):
    """GET — AI credits + Nebians points balance & rates.
    POST — convert Nebians points to AI credits (2 points = 1 credit by default)."""
    user, err = _require_user(request)
    if err:
        return err
    cfg = get_payment_config()
    ensure_monthly_free_credits(user, cfg)

    if request.method == 'GET':
        return Response({
            'nebians_points': user.nebians_points or 0,
            'ai_credits_purchased': user.ai_credits or 0,
            'ai_credits_free': user.free_credits or 0,
            'ai_credits_total': total_ai_credits(user, cfg),
            'free_credits_per_month': cfg.free_credits_per_month,
            'points_to_credit': cfg.points_to_credit,
            'month': ensure_monthly_free_credits(user, cfg)[1],
        })

    points = request.data.get('points')
    try:
        credits_gained, points_used = convert_points_to_credits(user, points, cfg)
    except ValueError as exc:
        return Response({'error': str(exc)}, status=400)
    return Response({
        'credits_gained': credits_gained,
        'points_used': points_used,
        'nebians_points': user.nebians_points or 0,
        'ai_credits_total': total_ai_credits(user, cfg),
        'message': f'Converted {points_used} points into {credits_gained} AI credits.',
    }, status=201)
