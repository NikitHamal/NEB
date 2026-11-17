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
import os

from django.conf import settings
import whitenoise.compress as _whitenoise_compress
import whitenoise.storage as _whitenoise_storage
from whitenoise.storage import CompressedStaticFilesStorage

from nebians import minify
from nebians.static_headers import IMMUTABLE_EXT, static_cache_headers  # noqa: F401

# collectstatic's compression pass runs in a ThreadPoolExecutor, and whitenoise
# 6.12 sizes it with the ThreadPoolExecutor default: min(32, cpu_count + 4),
# which is 32 threads on the live box's 80 cores. That box is shared cPanel with
# a tight per-account LVE thread budget, and daphne alone holds ~64 threads, so
# the pool pushed the account over the cap:
#
#   RuntimeError: can't start new thread
#
# raised from inside post_process, after part of the static tree had already
# been rewritten (2026-11-16). Capping the pool keeps collectstatic inside the
# budget. Compression is a per-file, I/O-shaped job, so a handful of workers is
# no slower here in practice.
_MAX_POST_PROCESS_WORKERS = 4


def _bounded_executor(*args, **kwargs):
    """ThreadPoolExecutor with a pool small enough for the LVE thread budget."""
    kwargs.setdefault(
        'max_workers',
        getattr(settings, 'STATIC_POST_PROCESS_WORKERS', _MAX_POST_PROCESS_WORKERS),
    )
    from concurrent.futures import ThreadPoolExecutor

    return ThreadPoolExecutor(*args, **kwargs)


# whitenoise.storage looks the name up in its own module globals, so replacing
# the attribute here is enough to bound the pool it builds.
_whitenoise_storage.ThreadPoolExecutor = _bounded_executor

# Model weights are already-compressed binary blobs: needle3.cact (34 MB) and
# whistle.cact (17 MB) shrink about 6 percent (34 -> 32 MB) but cost minutes
# of gzip level 9 plus brotli quality 11 CPU on every collectstatic, because
# WhiteNoise re-compresses the whole tree each run. They also never change in
# place, and every visitor caches them forever, so compression buys nothing.
# Skip them here (merged with WhiteNoise's own defaults, never replacing, so
# a WhiteNoise upgrade that skips a new extension still works). The compressed
# copies already on disk keep being served until they go stale.
_SKIP_COMPRESS_EXTENSIONS = ("cact",)


class VersionedStaticFilesStorage(CompressedStaticFilesStorage):
    def create_compressor(self, **kwargs):
        extensions = set(_whitenoise_compress.Compressor.SKIP_COMPRESS_EXTENSIONS)
        extensions.update(getattr(settings, "WHITENOISE_SKIP_COMPRESS_EXTENSIONS", None) or ())
        extensions.update(_SKIP_COMPRESS_EXTENSIONS)
        kwargs["extensions"] = extensions
        return super().create_compressor(**kwargs)

    def _compressed_form_is_current(self, name):
        # A compressed copy is current when at least one compressed form exists
        # and no existing copy is older than the file. WhiteNoise copies the
        # source modification time onto the .gz/.br, so equality means the
        # file was already compressed from these bytes.
        full = self.path(name)
        try:
            source_mtime = os.path.getmtime(full)
        except OSError:
            return False
        found = False
        for suffix in (".br", ".gz"):
            try:
                compressed_mtime = os.path.getmtime(full + suffix)
            except OSError:
                continue
            found = True
            if compressed_mtime < source_mtime:
                return False
        return found

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return
            yield  # pragma: no cover (keeps this a generator)
        # Minify first so the .gz/.br copies WhiteNoise writes are of the small bytes.
        if minify.enabled():
            saved = 0
            for name in paths:
                saved += minify.minify_file(self.path(name), name)
            if saved:
                print('Minified static files: -%d KB' % (saved // 1024))
        # Collectstatic hands post_process every collected file, not only the
        # ones it copied, and WhiteNoise then re-compresses all of them (6745
        # post-processed on 2026-11-17 for a 156-file delta). Keep only the
        # files whose compressed forms are missing or stale. A file just copied
        # or minified is newer than its compressed forms, so it is kept.
        if isinstance(paths, dict):
            stale = {name: paths[name] for name in paths if not self._compressed_form_is_current(name)}
        else:
            stale = [name for name in paths if not self._compressed_form_is_current(name)]
        if stale:
            yield from super().post_process(stale, dry_run, **options)

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
