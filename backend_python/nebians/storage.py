"""Static files: compressed, and every URL carries its own content version.

`CompressedStaticFilesStorage` (not the manifest one, see settings.py) keeps plain
file names, so a deploy cannot 404 on a worker that holds an old index. The cost
was that nothing could be cached for long: the same URL meant different bytes
after a deploy, so WhiteNoise sent `max-age=60` and every visit re-validated
every font, script and stylesheet. The font swap people saw on each page load
was that revalidation round trip.

`url()` here appends `?v=<digest of the file>` (computed once per process from
the file on disk, no manifest and no index to go stale). The query string is
ignored by WhiteNoise when it serves the file, but it changes the cache key, so
a changed file is a new URL. That is what makes `Cache-Control: immutable`
safe in `nebians.static_headers.static_cache_headers`.
"""
from django.conf import settings
from whitenoise.storage import CompressedStaticFilesStorage

from nebians import minify
from nebians.static_headers import IMMUTABLE_EXT, static_cache_headers  # noqa: F401


class VersionedStaticFilesStorage(CompressedStaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        # Minify first so the .gz/.br copies WhiteNoise writes are of the small bytes.
        if not dry_run and minify.enabled():
            saved = 0
            for name in paths:
                saved += minify.minify_file(self.path(name), name)
            if saved:
                print('Minified static files: -%d KB' % (saved // 1024))
        yield from super().post_process(paths, dry_run, **options)

    def url(self, name):
        url = super().url(name)
        if '?' in url or '#' in url or settings.DEBUG:
            return url
        # Fonts are referenced twice, by <link rel=preload> and by url() inside
        # fonts.css, and a preload only counts when both URLs are byte-identical.
        # Fonts are therefore never versioned here; to change one, rename it
        # (or bump the ?v= that fonts.css already carries on the icon font).
        if name.lower().endswith(IMMUTABLE_EXT):
            return url
        from web.templatetags.asset_tags import _digest
        token = _digest(name)
        return '%s?v=%s' % (url, token) if token else url
