from __future__ import annotations

import hashlib
import re

from django.conf import settings
from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware, get_token


_TTL = int(getattr(settings, 'PAGE_CACHE_TTL', 45))
_MAX_BYTES = 512 * 1024
_PATHS = ('/', '/app/faq/', '/app/library/', '/app/forum/', '/app/news/')
_NONCE_PH = b'\x00nebnonce\x00'
_TOKEN_PH = b'\x00nebcsrf\x00'
_TOKEN_CTX = re.compile(
    rb'''(?:csrf-token"\s+content="|CSRF_TOKEN\s*=\s*['"]|'''
    rb'''X-CSRFToken['"]?\s*:\s*\(?\s*['"]|name="csrfmiddlewaretoken"\s+value=")'''
    rb'''([A-Za-z0-9]{64})'''
)
_MOBILE_UA = re.compile(r'android|iphone|ipad|ipod|mobile|phone', re.I)


def _whitelisted(path):
    if path == '/':
        return True
    return path.startswith(('/app/faq/', '/app/library/', '/app/forum/', '/app/news/'))


def _device(request):
    ua = request.META.get('HTTP_USER_AGENT', '') or ''
    if _MOBILE_UA.search(ua):
        return 'm'
    return 'd'


def _key(request):
    host = request.get_host().split(':')[0].lower()
    raw = '|'.join((host, request.get_full_path(), _device(request)))
    digest = hashlib.sha1(raw.encode()).hexdigest()
    return 'anonpage:v1:' + digest


def _mask(body, nonce):
    if nonce:
        body = body.replace(nonce.encode(), _NONCE_PH)
    body = _TOKEN_CTX.sub(
        lambda m: m.group(0)[:len(m.group(0)) - 64] + _TOKEN_PH, body)
    return body


def _unmask(body, request):
    nonce = getattr(request, 'csp_nonce', '') or ''
    if nonce:
        body = body.replace(_NONCE_PH, nonce.encode())
    if _TOKEN_PH in body:
        body = body.replace(_TOKEN_PH, get_token(request).encode())
    return body


class AnonPageCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._servable(request):
            return self.get_response(request)
        from django.core.cache import cache
        key = _key(request)
        hit = cache.get(key)
        if hit is not None:
            return self._serve(request, hit)
        response = self.get_response(request)
        self._store(request, key, response)
        return response

    def _servable(self, request):
        if request.method != 'GET':
            return False
        if not _whitelisted(request.path):
            return False
        if request.META.get('HTTP_AUTHORIZATION'):
            return False
        if getattr(request, 'htmx', False):
            return False
        cookies = request.COOKIES
        if settings.SESSION_COOKIE_NAME in cookies:
            return False
        if getattr(settings, 'MESSAGE_COOKIE_NAME', 'messages') in cookies:
            return False
        try:
            user = getattr(request, 'user', None)
            if user is not None and getattr(user, 'is_authenticated', False):
                return False
        except Exception:
            return False
        return True

    def _store(self, request, key, response):
        try:
            if response.status_code != 200 or response.streaming:
                return
            ctype = response.get('Content-Type', '')
            if 'text/html' not in ctype:
                return
            if 'Set-Cookie' in response:
                return
            try:
                session = request.session
            except Exception:
                session = None
            if session is not None:
                try:
                    if session.modified or getattr(settings, 'SESSION_SAVE_EVERY_REQUEST', False):
                        return
                except Exception:
                    return
            cc = response.get('Cache-Control', '').lower()
            if 'no-store' in cc or 'no-cache' in cc:
                return
            body = response.content
            if len(body) > _MAX_BYTES:
                return
            nonce = getattr(request, 'csp_nonce', '') or ''
            masked = _mask(body, nonce)
            from django.core.cache import cache
            cache.set(key, bytes(masked), _TTL)
        except Exception:
            pass

    def _serve(self, request, body):
        try:
            body = _unmask(bytes(body), request)
        except Exception:
            pass
        response = HttpResponse(body, content_type='text/html; charset=utf-8')
        response['Cache-Control'] = 'private, max-age=30'
        response['Vary'] = 'Cookie'
        response['X-Page-Cache'] = 'hit'
        try:
            response = CsrfViewMiddleware(lambda req: response)(request)
        except Exception:
            pass
        return response
