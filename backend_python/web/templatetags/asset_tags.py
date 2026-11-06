import hashlib
from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()
_cache = {}


def _digest(path):
    hit = _cache.get(path)
    if hit is not None:
        return hit
    found = finders.find(path)
    token = ''
    if isinstance(found, str):
        try:
            with open(found, 'rb') as fh:
                token = hashlib.md5(fh.read()).hexdigest()[:10]
        except OSError:
            token = ''
    _cache[path] = token
    return token


@register.simple_tag
def asset(path):
    url = static(path)
    if '?' in url:  # the storage already versioned it
        return url
    token = _digest(path)
    return f'{url}?v={token}' if token else url
