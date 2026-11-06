"""Cache-Control for WhiteNoise. No Django imports: settings.py loads this at start-up."""
ONE_YEAR = 31536000
VERSIONED_EXT = ('.js', '.mjs', '.css')
IMMUTABLE_EXT = ('.woff2', '.woff', '.ttf')


def static_cache_headers(headers, path, url):
    """WhiteNoise `add_headers_function`: long, immutable caching where the URL is versioned.

    * fonts: the file name never changes meaning -> one year, immutable
    * js/css: every template reference is versioned (see above) -> one year, immutable
    * vendor libraries: same
    * images, art, audio: referenced from CSS and JS by plain path -> 7 days, then
      revalidate in the background
    """
    p = (url or path or '').lower()
    if p.endswith(IMMUTABLE_EXT) or '/vendor/' in p or '/needle3/' in p:
        headers['Cache-Control'] = 'public, max-age=%d, immutable' % ONE_YEAR
    elif p.endswith(VERSIONED_EXT):
        headers['Cache-Control'] = 'public, max-age=%d, immutable' % ONE_YEAR
    else:
        headers['Cache-Control'] = 'public, max-age=604800, stale-while-revalidate=86400'
