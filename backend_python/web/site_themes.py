"""The NEBians site themes.

A theme is a small, closed set of choices: a palette (CSS custom properties), one decor
motif drawn by ``templates/themes/_decor.html`` + ``static/web/css/themes.css``, and an
optional greeting. Admins do not author themes; they choose one of these and say when it
runs (``api.models.SiteTheme``). Keeping the library in code means every theme is
designed, reviewed and tested once, and a festival can never ship half-styled.

The decor layers only ever animate ``transform`` and ``opacity``, pause off-screen, and
switch off under ``prefers-reduced-motion``.
"""
from __future__ import annotations

import datetime as _dt

from django.core.cache import cache

CACHE_KEY = 'site_theme_resolved_v2'
DEFAULT_KEY = 'everyday'

THEMES = {
    'everyday': {
        'name': 'Everyday',
        'about': 'The house style. Calm blue, plenty of white, nothing seasonal.',
        'decor': 'none',
        'tokens': {
            '--st-accent': '#0b57d0', '--st-accent-2': '#6246d7', '--st-accent-ink': '#ffffff',
            '--st-warm': '#f59e0b', '--st-tint': '#eef3ff', '--st-glow-1': '#cfe0ff', '--st-glow-2': '#e9e2ff',
        },
        'greeting': None,
    },
    'dashain': {
        'name': 'Dashain',
        'about': 'Marigold garlands, kites on the wind, a tika-red accent.',
        'decor': 'dashain',
        'tokens': {
            '--st-accent': '#c8102e', '--st-accent-2': '#e8890c', '--st-accent-ink': '#ffffff',
            '--st-warm': '#f6a623', '--st-tint': '#fff4e2', '--st-glow-1': '#ffd9a3', '--st-glow-2': '#ffe3e3',
        },
        'greeting': {'ne': 'विजया दशमीको शुभकामना', 'en': 'Happy Dashain'},
    },
    'tihar': {
        'name': 'Tihar',
        'about': 'Strings of diyo light, rangoli colours, a warm evening glow.',
        'decor': 'tihar',
        'tokens': {
            '--st-accent': '#b4232c', '--st-accent-2': '#7c3aed', '--st-accent-ink': '#ffffff',
            '--st-warm': '#ffb020', '--st-tint': '#fff6e8', '--st-glow-1': '#ffd27a', '--st-glow-2': '#f3d9ff',
        },
        'greeting': {'ne': 'शुभ दीपावली', 'en': 'Happy Tihar'},
    },
    'holi': {
        'name': 'Holi',
        'about': 'Soft clouds of gulal drifting across the page.',
        'decor': 'holi',
        'tokens': {
            '--st-accent': '#d6246e', '--st-accent-2': '#0f9d8a', '--st-accent-ink': '#ffffff',
            '--st-warm': '#ffb300', '--st-tint': '#fff0f6', '--st-glow-1': '#ffc6e0', '--st-glow-2': '#c9f3ea',
        },
        'greeting': {'ne': 'फागु पूर्णिमाको शुभकामना', 'en': 'Happy Holi'},
    },
    'new-year': {
        'name': 'Nepali New Year',
        'about': 'Lali gurans red for Baisakh 1, petals falling slowly.',
        'decor': 'gurans',
        'tokens': {
            '--st-accent': '#c2185b', '--st-accent-2': '#1b5e20', '--st-accent-ink': '#ffffff',
            '--st-warm': '#ff7043', '--st-tint': '#fff1f3', '--st-glow-1': '#ffc1cc', '--st-glow-2': '#dcefd9',
        },
        'greeting': {'ne': 'नयाँ वर्षको शुभकामना', 'en': 'Happy New Year'},
    },
    'monsoon': {
        'name': 'Monsoon',
        'about': 'Asar rain over green paddy terraces. Cool, fresh, quiet.',
        'decor': 'rain',
        'tokens': {
            '--st-accent': '#00796b', '--st-accent-2': '#1565c0', '--st-accent-ink': '#ffffff',
            '--st-warm': '#c0ca33', '--st-tint': '#ecf8f4', '--st-glow-1': '#bfe8dc', '--st-glow-2': '#cfe3fb',
        },
        'greeting': {'ne': 'असार १५, दही चिउरा', 'en': 'Rice planting day'},
    },
    'winter': {
        'name': 'Winter',
        'about': 'A Himalayan ridge on the horizon and a little snow.',
        'decor': 'snow',
        'tokens': {
            '--st-accent': '#1e4fa8', '--st-accent-2': '#5b6bd6', '--st-accent-ink': '#ffffff',
            '--st-warm': '#90caf9', '--st-tint': '#f1f6fc', '--st-glow-1': '#d6e6fb', '--st-glow-2': '#e4e1fb',
        },
        'greeting': None,
    },
    'exams': {
        'name': 'Exam season',
        'about': 'Quiet and focused for board exams. A small good-luck note.',
        'decor': 'none',
        'tokens': {
            '--st-accent': '#173a8f', '--st-accent-2': '#0b7a5c', '--st-accent-ink': '#ffffff',
            '--st-warm': '#f4b400', '--st-tint': '#f2f5fb', '--st-glow-1': '#dbe4f7', '--st-glow-2': '#d9efe6',
        },
        'greeting': {'ne': 'परीक्षाको शुभकामना', 'en': 'Good luck in your exams'},
    },
}

# How each festive theme dresses the app itself (the web app and the Android app): the primary
# colour family in light and dark (Material roles: primary, on-primary, container, on-container),
# a small motif beside the logo, and the season card at the top of the home feed. Colours are
# chosen for contrast, not just mood: primary on surface and on-container on container both
# clear 4.5:1 in each mode.
APP = {
    'dashain': {
        'light': ('#B3261E', '#FFFFFF', '#FFDAD5', '#410002'), 'dark': ('#FFB4AB', '#690005', '#93000A', '#FFDAD6'),
        'motif': 'kite', 'message': 'Every book works offline in the app, so the library comes home with you.',
        'cta': ('Get the app', 'https://play.google.com/store/apps/details?id=com.neb.ians'),
    },
    'tihar': {
        'light': ('#9A4600', '#FFFFFF', '#FFDBC8', '#321200'), 'dark': ('#FFB68B', '#532200', '#753400', '#FFDBC8'),
        'motif': 'diyo', 'message': 'Light a diyo, then read one chapter. The library is open all five days.',
        'cta': ('Open the library', '/app/library/'),
    },
    'holi': {
        'light': ('#A8336B', '#FFFFFF', '#FFD9E5', '#3E001F'), 'dark': ('#FFB0CB', '#5E1137', '#7C2A4E', '#FFD9E5'),
        'motif': 'gulal', 'message': 'Colours today, questions tomorrow. Someone in the forum is stuck on yours.',
        'cta': ('Visit the forum', '/app/forum/'),
    },
    'new-year': {
        'light': ('#BA1A3A', '#FFFFFF', '#FFDADC', '#40000E'), 'dark': ('#FFB2B8', '#67001B', '#91102B', '#FFDADC'),
        'motif': 'gurans', 'message': 'A new year, a new class. Start with the notes for it.',
        'cta': ('Find your class', '/app/library/'),
    },
    'monsoon': {
        'light': ('#006A60', '#FFFFFF', '#9EF2E4', '#00201C'), 'dark': ('#82D5C8', '#003731', '#005048', '#9EF2E4'),
        'motif': 'drop', 'message': 'Rainy days are reading days. Save books now and read them offline.',
        'cta': ('Open the library', '/app/library/'),
    },
    'winter': {
        'light': ('#2E5AAC', '#FFFFFF', '#D8E2FF', '#001A41'), 'dark': ('#ADC6FF', '#002E69', '#1F4592', '#D8E2FF'),
        'motif': 'snow', 'message': 'Short days, long nights. The forum is open late.',
        'cta': ('Visit the forum', '/app/forum/'),
    },
    'exams': {
        'light': ('#26418F', '#FFFFFF', '#DBE1FF', '#00174B'), 'dark': ('#B4C5FF', '#002A77', '#1B3A88', '#DBE1FF'),
        'motif': 'pencil', 'message': 'Past papers, model questions and fully solved books, all free.',
        'cta': ('Practise past papers', '/app/past-papers/'),
    },
}

ROLES = ('--md-primary', '--md-on-primary', '--md-primary-container', '--md-on-primary-container')


def app_css(key: str) -> str:
    """The CSS that recolours the app for a festive theme, light and dark."""
    a = APP.get(key)
    if not a:
        return ''
    light = ';'.join(f'{r}:{c}' for r, c in zip(ROLES, a['light']))
    dark = ';'.join(f'{r}:{c}' for r, c in zip(ROLES, a['dark']))
    return (f'html[data-site-theme="{key}"]{{{light}}}'
            f'html[data-theme="dark"][data-site-theme="{key}"]{{{dark}}}')


CHOICES = [(k, v['name']) for k, v in THEMES.items()]


GARLANDS = {'dashain': (24, 4, 32), 'tihar': (28, 3, 28)}


def decor_data(key: str) -> dict:
    """Points on the garland string for the decor partial. The string is a chain of
    quadratic curves; a point at parameter f across a swag sits at top + sag*4f(1-f),
    which is exactly where the curve passes, so flowers and lights sit on the thread."""
    decor = THEMES.get(key, THEMES[DEFAULT_KEY])['decor']
    spec = GARLANDS.get(decor)
    if not spec:
        return {'decor': decor, 'dots': [], 'path': ''}
    n, swags, sag = spec
    w, top = 1200 / swags, 6
    path = f'M0 {top}' + ''.join(f' Q{w * k + w / 2:.0f} {top + 2 * sag} {w * (k + 1):.0f} {top}' for k in range(swags))
    dots = []
    for i in range(n):
        u = (i + 0.5) / n * swags
        f = u - int(u)
        dots.append({'x': round((i + 0.5) / n * 100, 2), 'y': round(top + sag * 4 * f * (1 - f), 1)})
    return {'decor': decor, 'dots': dots, 'path': path}


def kathmandu_today() -> _dt.date:
    """Festival dates are Nepal dates, whatever the server's clock says."""
    return (_dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(hours=5, minutes=45)).date()


def _payload(key: str, why: str, show_in_app: bool = True, show_greeting: bool = True) -> dict:
    t = THEMES.get(key) or THEMES[DEFAULT_KEY]
    css = ';'.join(f'{k}:{v}' for k, v in t['tokens'].items())
    return {
        'key': key if key in THEMES else DEFAULT_KEY,
        'name': t['name'],
        **decor_data(key),
        'css': css,
        'greeting': t['greeting'] if show_greeting else None,
        'show_in_app': show_in_app,
        'why': why,
        'festive': key != DEFAULT_KEY,
        'app_css': app_css(key),
        'app': APP.get(key),
    }


def resolve(today: _dt.date | None = None) -> dict:
    """Which theme is live: one switched on now beats a scheduled window; else everyday."""
    from api.models import SiteTheme
    today = today or kathmandu_today()
    row = SiteTheme.objects.filter(is_forced=True).order_by('-updated_at').first()
    if row:
        return _payload(row.key, 'Turned on by an admin', row.show_in_app, row.show_greeting)
    row = (SiteTheme.objects.filter(is_forced=False, starts_on__lte=today, ends_on__gte=today)
           .order_by('-starts_on', '-updated_at').first())
    if row:
        return _payload(row.key, f'Scheduled {row.starts_on:%d %b} to {row.ends_on:%d %b}',
                        row.show_in_app, row.show_greeting)
    return _payload(DEFAULT_KEY, 'Nothing scheduled today')


def current() -> dict:
    data = cache.get(CACHE_KEY)
    if data is None:
        try:
            data = resolve()
        except Exception:
            data = _payload(DEFAULT_KEY, 'Theme table unavailable')
        from . import neby_looks
        data = {**data, 'neby': neby_looks.resolve(data['key'])}
        cache.set(CACHE_KEY, data, 300)
    return data


def invalidate():
    cache.delete(CACHE_KEY)


def context(request):
    """Template context processor: ``site_theme`` on every page."""
    return {'site_theme': current()}
