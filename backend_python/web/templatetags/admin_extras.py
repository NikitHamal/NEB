"""Admin-panel-only template tags (never used by the public site)."""
from django import template
from django.core.cache import cache
from django.urls import reverse

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


NAV_GROUPS = (
    ('Overview', (
        ('dashboard', 'admin_dashboard', 'dashboard', 'Dashboard', None),
        ('analytics', 'admin_analytics', 'insights', 'Analytics', None),
    )),
    ('People', (
        ('users', 'admin_users', 'people', 'Users', None),
        ('push_notifications', 'admin_push_notifications', 'notifications_active', 'Push notifications', None),
        ('deletions', 'admin_deletions', 'person_remove', 'Account deletions', 'pending_deletions'),
    )),
    ('Library', (
        ('resources', 'admin_resources', 'auto_stories', 'Resources', None),
        ('syllabus', 'admin_syllabus_list', 'menu_book', 'Syllabus and chapters', None),
        ('resource_requests', 'admin_resource_requests', 'contact_support', 'Requests', 'open_requests'),
    )),
    ('Review', (
        ('pending_resources', 'admin_pending_resources', 'pending_actions', 'Pending review', 'pending_resources'),
        ('payments', 'admin_pending_payments', 'payments', 'Payments', 'pending_payments'),
        ('withdrawals', 'admin_withdrawals', 'account_balance_wallet', 'Withdrawals', 'pending_withdrawals'),
        ('reports', 'admin_reports', 'flag', 'Reports', 'open_reports'),
    )),
    ('Community', (
        ('posts', 'admin_posts', 'forum', 'Forum posts', None),
        ('announcements', 'admin_announcements', 'newspaper', 'Blog and updates', None),
        ('study_spaces', 'admin_study_spaces', 'science', 'Study spaces', None),
    )),
    ('Design', (
        ('site_themes', 'admin_site_themes', 'palette', 'Site themes', None),
        ('neby_studio', 'admin_neby_studio', 'mood', 'Neby studio', None),
        ('art_library', 'admin_art_library', 'brush', 'Art library', None),
        ('dither_art', 'admin_dither_art', 'blur_on', 'Dither arts', None),
    )),
    ('Automation', (
        ('bot', 'admin_bots', 'smart_toy', 'AI bots', None),
        ('neby', 'admin_neby_manager', 'psychology', 'Neby manager', None),
        ('agent_activity', 'admin_agent_activity', 'monitor_heart', 'Agent heartbeat', None),
        ('chat', 'admin_chat', 'chat', 'AI chat test', None),
        ('media_test', 'admin_media_test', 'perm_media', 'Media test', None),
    )),
)


@register.simple_tag
def admin_nav(active_page=''):
    """Sidebar groups (label, items). One source for the drawer and the Ctrl+K palette."""
    badges = admin_nav_badges()
    return [
        {
            'label': label,
            'items': [
                {
                    'key': key,
                    'url': reverse('web:' + url_name),
                    'icon': icon,
                    'label': text,
                    'badge': badges.get(badge_key) if badge_key else 0,
                    'active': key == active_page,
                }
                for key, url_name, icon, text, badge_key in items
            ],
        }
        for label, items in NAV_GROUPS
    ]
