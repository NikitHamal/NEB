"""Admin page for site themes: switch one on now, or schedule it for a festival window."""
import datetime as dt

from django.contrib import messages
from django.shortcuts import redirect, render

from api.models import SiteTheme

from . import site_themes
from .view_helpers import _ctx, _require_staff_admin


def _date(value):
    try:
        return dt.date.fromisoformat((value or '').strip())
    except ValueError:
        return None


def admin_site_themes(request):
    blocked = _require_staff_admin(request)
    if blocked:
        return blocked

    if request.method == 'POST':
        action = request.POST.get('action')
        key = request.POST.get('key', '')
        show_in_app = request.POST.get('show_in_app') == 'on'
        show_greeting = request.POST.get('show_greeting') == 'on'
        if action in ('force', 'schedule') and key not in site_themes.THEMES:
            messages.error(request, 'That theme does not exist.')
        elif action == 'force':
            SiteTheme.objects.filter(is_forced=True).update(is_forced=False)
            SiteTheme.objects.filter(is_forced=False, starts_on__isnull=True).delete()
            if key != site_themes.DEFAULT_KEY:
                SiteTheme.objects.create(key=key, is_forced=True, show_in_app=show_in_app,
                                         show_greeting=show_greeting)
            messages.success(request, f"{site_themes.THEMES[key]['name']} is live now.")
        elif action == 'schedule':
            start, end = _date(request.POST.get('starts_on')), _date(request.POST.get('ends_on'))
            if not start or not end or end < start:
                messages.error(request, 'Pick a start date and an end date on or after it.')
            else:
                SiteTheme.objects.create(key=key, starts_on=start, ends_on=end, show_in_app=show_in_app,
                                         show_greeting=show_greeting,
                                         note=request.POST.get('note', '')[:120])
                messages.success(request, f"{site_themes.THEMES[key]['name']} scheduled for "
                                          f"{start:%d %b %Y} to {end:%d %b %Y}.")
        elif action == 'release':
            SiteTheme.objects.filter(is_forced=True).delete()
            messages.success(request, 'Back to the calendar.')
        elif action == 'delete':
            SiteTheme.objects.filter(id=request.POST.get('id')).delete()
            messages.success(request, 'Removed from the schedule.')
        site_themes.invalidate()
        return redirect('web:admin_site_themes')

    today = site_themes.kathmandu_today()
    live = site_themes.resolve(today)
    themes = [{'key': k, **v, **site_themes.decor_data(k), 'app': site_themes.APP.get(k), 'css': ';'.join(f'{a}:{b}' for a, b in v['tokens'].items()),
               'live': k == live['key']} for k, v in site_themes.THEMES.items()]
    schedule = list(SiteTheme.objects.filter(is_forced=False, ends_on__gte=today).order_by('starts_on'))
    for row in schedule:
        row.theme_name = site_themes.THEMES.get(row.key, {}).get('name', row.key)
    past = SiteTheme.objects.filter(is_forced=False, ends_on__lt=today).order_by('-ends_on')[:6]
    forced = SiteTheme.objects.filter(is_forced=True).first()
    ctx = _ctx(request, active_page='site_themes', themes=themes, live=live, schedule=schedule,
               past=past, forced=forced, today=today, names=dict(site_themes.CHOICES))
    return render(request, 'admin_panel/site_themes.html', ctx)
