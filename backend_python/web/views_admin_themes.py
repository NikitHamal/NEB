"""Admin page for site themes: switch one on now, or schedule it for a festival window."""
import datetime as dt

from django.contrib import messages
from django.shortcuts import redirect, render

from api.models import NebyConfig, SiteTheme

from . import neby_looks, site_themes
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


def admin_neby_studio(request):
    """Every pixel Neby look and animation in one place, and the switch for which look is live."""
    blocked = _require_staff_admin(request)
    if blocked:
        return blocked

    if request.method == 'POST':
        look = request.POST.get('look', neby_looks.AUTO)
        if look != neby_looks.AUTO and look not in neby_looks.LOOK_KEYS:
            messages.error(request, 'That look does not exist.')
        else:
            row = NebyConfig.objects.order_by('-updated_at').first() or NebyConfig()
            row.look = look
            row.ambient = request.POST.get('ambient') == 'on'
            row.reactions = request.POST.get('reactions') == 'on'
            row.save()
            site_themes.invalidate()
            label = dict((k, l) for k, l, _ in neby_looks.LOOKS).get(look, 'Festival auto')
            messages.success(request, f'Neby now wears: {label}. The apps pick it up within five minutes.')
        return redirect('web:admin_neby_studio')

    theme = site_themes.resolve(site_themes.kathmandu_today())
    live = neby_looks.resolve(theme['key'])
    groups = {}
    for key, label, group in neby_looks.LOOKS:
        groups.setdefault(group, []).append({'key': key, 'label': label, 'live': key == live['look']})
    states = {}
    for key, (frames, ms, group) in neby_looks.STATES.items():
        states.setdefault(group, []).append({'key': key, 'label': key.replace('-', ' ').capitalize(), 'frames': frames, 'ms': ms})
    ctx = _ctx(request, active_page='neby_studio', look_groups=groups, state_groups=states, live=live, theme=theme,
               looks=neby_looks.LOOKS, state_count=len(neby_looks.STATES), look_count=len(neby_looks.LOOKS),
               auto_look=neby_looks.for_theme(theme['key']))
    return render(request, 'admin_panel/neby_studio.html', ctx)


def admin_art_library(request):
    """The SVG art library (tools/svgart): every scene in its grain, flat and pixel looks.
    For review only; nothing in the site or the app uses these yet."""
    blocked = _require_staff_admin(request)
    if blocked:
        return blocked
    import json
    import os
    from django.conf import settings
    path = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'art', 'manifest.json')
    try:
        with open(path, encoding='utf-8') as fh:
            manifest = json.load(fh)
    except (OSError, ValueError):
        manifest = {'looks': {}, 'sets': []}
    total = sum(len(it['files']) for st in manifest['sets'] for it in st['items'])
    ctx = _ctx(request, active_page='art_library', art=manifest, art_total=total)
    return render(request, 'admin_panel/art_library.html', ctx)
