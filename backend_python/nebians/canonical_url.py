"""One address per page.

Search Console listed 500+ "Alternate page with proper canonical tag" URLs:
the www host, tracking parameters (?from=AppAgg.com&utm_*), and sort or filter
variants. The canonical tag was right, but every variant still got crawled.
This middleware answers the two avoidable families with a 301 to the one
address, so they collapse into the canonical page instead of being reported:

* ``www.`` host to the bare host;
* advertising and referral parameters (utm_*, fbclid, gclid, ``from=<domain>``).

Sort and filter variants are handled with rel="nofollow" in the templates.
Only GET and HEAD are touched. API, admin, auth, ajax and asset paths are left
alone, so no client and no form is affected.
"""
from urllib.parse import parse_qsl, urlencode

from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = 'nebians.consica.com.np'
SKIP_PREFIXES = ('/api/', '/admin', '/auth/', '/ajax/', '/og/', '/static/', '/media/', '/login', '/logout')
TRACKING_EXACT = frozenset({'fbclid', 'gclid', 'msclkid', 'dclid', 'mc_cid', 'mc_eid', 'igshid', 'ref_src'})


def _is_tracking(key: str, value: str) -> bool:
    k = key.lower()
    if k.startswith('utm_') or k in TRACKING_EXACT:
        return True
    # "from" is a real filter on a few internal pages, but a referral tag when
    # it is a domain name (?from=AppAgg.com).
    return k in ('from', 'ref', 'source') and '.' in (value or '')


def clean_query(query_string: str):
    """Return (cleaned_query, changed)."""
    if not query_string:
        return '', False
    pairs = parse_qsl(query_string, keep_blank_values=True)
    kept = [(k, v) for k, v in pairs if not _is_tracking(k, v)]
    return urlencode(kept), len(kept) != len(pairs)


class CanonicalUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('GET', 'HEAD'):
            path = request.path
            if not path.startswith(SKIP_PREFIXES):
                host = (request.META.get('HTTP_HOST') or '').split(':')[0].lower()
                query, changed = clean_query(request.META.get('QUERY_STRING', ''))
                if host == 'www.' + CANONICAL_HOST or changed:
                    target = f'https://{CANONICAL_HOST}{path}'
                    if query:
                        target += '?' + query
                    return HttpResponsePermanentRedirect(target)
        return self.get_response(request)
