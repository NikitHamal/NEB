"""Admin-panel-only template tags (never used by the public site)."""
from django import template
from django.core.cache import cache

register = template.Library()


def _safe_count(key, resolver):
    try:
        return cache.get_or_set(key, resolver, 60)
    except Exception:
        try:
            return resolver()
        except Exception:
            return 0


@register.simple_tag
def admin_nav_badges():
    """Cached moderation-queue counts for the admin sidebar badges."""
    from api.models import (
        AccountDeletionRequest,
        PaymentVerification,
        Report,
        Resource,
        ResourceRequest,
        WithdrawalRequest,
    )

    return {
        'pending_resources': _safe_count(
            'admin_nav:pending_resources',
            lambda: Resource.objects.filter(approval_status='pending').count(),
        ),
        'open_reports': _safe_count(
            'admin_nav:open_reports',
            lambda: Report.objects.filter(status='open').count(),
        ),
        'pending_deletions': _safe_count(
            'admin_nav:pending_deletions',
            lambda: AccountDeletionRequest.objects.filter(status='pending').count(),
        ),
        'pending_payments': _safe_count(
            'admin_nav:pending_payments',
            lambda: PaymentVerification.objects.filter(status='pending').count(),
        ),
        'pending_withdrawals': _safe_count(
            'admin_nav:pending_withdrawals',
            lambda: WithdrawalRequest.objects.filter(status='pending').count(),
        ),
        'open_requests': _safe_count(
            'admin_nav:open_requests',
            lambda: ResourceRequest.objects.filter(status='open').count(),
        ),
    }
