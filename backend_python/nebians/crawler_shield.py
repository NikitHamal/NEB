"""Keep greedy crawlers from starving real visitors.

Why: the access log (Nov 2026) showed one AI crawler (`meta-externalagent`, ~100
rotating IPs) walking all 25k school pages plus /login/ and the OAuth entry
points: 35% of every dynamic request in a 4 h window, while the account only has
6 LSAPI workers (+2 extra). When all 8 were busy real people got 503.

What: a global per-minute budget for each known heavy crawler family, counted in
the shared cache. Inside the budget the crawler is served normally (search
engines and AI search can still index, just slowly). Over it, a cheap 429 with
Retry-After is returned before sessions, CSRF, the database or templates run.

Never limited: Googlebot, Bingbot, DuckDuckBot, Yandex, social link previews
(facebookexternalhit, Twitterbot, WhatsApp, Telegram, LinkedIn, Slack, Discord),
browsers and the Android app. robots.txt, sitemaps, static files and media are
always answered. If the cache is down the middleware fails open.
"""
from __future__ import annotations

import os
import re

from django.http import HttpResponse

# Families that crawl for training / bulk SEO data, not for sending visitors.
_HEAVY = re.compile(
    r'(meta-externalagent|meta-webindexer|gptbot|claudebot|anthropic-ai|ccbot|bytespider|amazonbot|'
    r'petalbot|ahrefsbot|semrushbot|mj12bot|dotbot|dataforseobot|imagesiftbot|barkrowler|blexbot|'
    r'serpstatbot|seekportbot|omgilibot|diffbot|timpibot|friendlycrawler|zoominfobot|perplexitybot)',
    re.I,
)
_ALWAYS = ('/robots.txt', '/sitemap', '/static/', '/media/', '/favicon', '/.well-known/')

try:
    _BUDGET = max(1, int(os.environ.get('CRAWLER_BUDGET_PER_MIN', '6')))
except ValueError:
    _BUDGET = 6
_RETRY_AFTER = '300'


class CrawlerShieldMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        if ua and len(ua) > 12:
            m = _HEAVY.search(ua)
            if m and not request.path.startswith(_ALWAYS) and self._over_budget(m.group(1).lower()):
                resp = HttpResponse('Too many requests. Please slow down.', status=429, content_type='text/plain')
                resp['Retry-After'] = _RETRY_AFTER
                resp['Cache-Control'] = 'no-store'
                return resp
        return self.get_response(request)

    @staticmethod
    def _over_budget(family: str) -> bool:
        try:
            from django.core.cache import cache
            key = 'crawler-shield:' + family
            if cache.add(key, 1, 60):
                return False
            try:
                return cache.incr(key) > _BUDGET
            except ValueError:  # window ended between add and incr
                cache.add(key, 1, 60)
                return False
        except Exception:
            return False  # fail open
