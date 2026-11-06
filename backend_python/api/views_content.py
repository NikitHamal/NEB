"""HTTP surface of the content service. Public, read-only, throttled; see api/content_api.py for the rules."""
import os

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils.http import http_date
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.throttling import SimpleRateThrottle

from . import content_api as C
from . import content_search

CACHE = 'public, max-age=300, must-revalidate'


class ContentRateThrottle(SimpleRateThrottle):
    scope = 'content'
    rate = os.environ.get('DRF_CONTENT_THROTTLE', '1200/hour')

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}


class ContentSearchThrottle(ContentRateThrottle):
    scope = 'content_search'
    rate = os.environ.get('DRF_CONTENT_SEARCH_THROTTLE', '90/minute')


class BookThrottle(ContentRateThrottle):
    scope = 'content_books'
    rate = os.environ.get('DRF_CONTENT_BOOK_THROTTLE', '120/hour')


def _decorate(resp, etag=None, last_modified=None, cache=CACHE):
    resp['Cache-Control'] = cache
    resp['X-Content-Type-Options'] = 'nosniff'
    if etag:
        resp['ETag'] = etag
    if last_modified:
        resp['Last-Modified'] = http_date(last_modified)
    return resp


def _json_file(request, path):
    if path is None:
        return JsonResponse({'error': 'Not found.'}, status=404)
    etag = C.etag_for(path)
    if request.headers.get('If-None-Match') == etag:
        return _decorate(HttpResponse(status=304), etag)
    with open(path, 'rb') as fh:
        body = fh.read()
    resp = HttpResponse(body, content_type='application/json; charset=utf-8')
    return _decorate(resp, etag, path.stat().st_mtime)


def _public(fn):
    fn = throttle_classes([ContentRateThrottle])(fn)
    fn = permission_classes([AllowAny])(fn)
    fn = authentication_classes([])(fn)
    return api_view(['GET', 'HEAD'])(fn)


_warm = {'started': False}


def _warm_search():
    if _warm['started']:
        return
    _warm['started'] = True
    import threading
    threading.Thread(target=content_search._docs, daemon=True).start()


@_public
def content_manifest(request):
    _warm_search()
    return _decorate(JsonResponse(C.manifest()), cache='public, max-age=60, must-revalidate')


@_public
def content_index(request):
    return _json_file(request, C.syllabus_index_path())


@_public
def content_syllabus(request, key):
    return _json_file(request, C.syllabus_path(key))


@_public
def content_study(request, key, name):
    return _json_file(request, C.study_path(key, name))


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([ContentSearchThrottle])
def content_search_view(request):
    q = request.query_params.get('q', '')
    try:
        limit = max(1, min(int(request.query_params.get('limit', 40)), 100))
    except (TypeError, ValueError):
        limit = 40
    resp = JsonResponse({'query': q[:80], 'hits': content_search.search(q, limit)})
    return _decorate(resp, cache='private, max-age=30')


@_public
def content_books(request):
    return _decorate(JsonResponse({'books': C.list_books()}), cache='public, max-age=120, must-revalidate')


def _iter_file(fh, start, length, chunk=256 * 1024):
    try:
        fh.seek(start)
        left = length
        while left > 0:
            data = fh.read(min(chunk, left))
            if not data:
                break
            left -= len(data)
            yield data
    finally:
        fh.close()


@api_view(['GET', 'HEAD'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([BookThrottle])
def content_book_file(request, slug):
    path = C.book_path(slug)
    if path is None:
        return JsonResponse({'error': 'Not found.'}, status=404)
    size = path.stat().st_size
    etag = C.etag_for(path)
    rng = C.parse_range(request.headers.get('Range', ''), size)
    if rng is False:
        resp = HttpResponse(status=416)
        resp['Content-Range'] = 'bytes */%d' % size
        return resp
    start, end = rng if rng else (0, size - 1)
    length = end - start + 1
    if request.method == 'HEAD':
        resp = HttpResponse(status=200)
    else:
        resp = StreamingHttpResponse(_iter_file(open(path, 'rb'), start, length), status=206 if rng else 200)
    resp['Content-Type'] = 'application/pdf'
    resp['Content-Length'] = str(length)
    resp['Accept-Ranges'] = 'bytes'
    resp['Content-Disposition'] = 'attachment; filename="%s.pdf"' % slug
    if rng:
        resp['Content-Range'] = 'bytes %d-%d/%d' % (start, end, size)
    return _decorate(resp, etag, path.stat().st_mtime, cache='public, max-age=3600')
