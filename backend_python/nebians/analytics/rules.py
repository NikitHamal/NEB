"""Pure analytics rules: no database, no request objects, no network.

Everything that decides *what a hit means* lives here so the tracker (write
side), the backfill command and the report (read side) cannot drift apart.

The old implementation matched referrers with substring tests, which is why
`com.google.android.gm` (the Gmail app) was reported as a search engine,
`classroom.google.com` as search, and `box.com` as X. Matching here is on whole
host labels only.
"""
from __future__ import annotations

import hashlib
import re
from collections import namedtuple
from urllib.parse import urlparse

# --------------------------------------------------------------------------
# Time
# --------------------------------------------------------------------------

MS_DAY = 86_400_000
MS_HOUR = 3_600_000
SESSION_GAP_MS = 30 * 60 * 1000


# --------------------------------------------------------------------------
# Bots
# --------------------------------------------------------------------------

_BOT_RE = re.compile(
    r'bot\b|bot/|crawl|spider|slurp|scrap|fetch|preview|monitor|uptime|headless'
    r'|lighthouse|pagespeed|pingdom|facebookexternalhit|whatsapp|discord'
    r'|embedly|curl/|wget/|python-|requests|httpx|aiohttp|go-http-client|java/'
    r'|libwww|axios|node-fetch|postman|insomnia|selenium|puppeteer|playwright'
    r'|phantomjs|gptbot|claudebot|ccbot|bytespider|petalbot|semrush|ahrefs|mj12'
    r'|dotbot|baiduspider|duckduckbot|applebot|inspectiontool|googleother'
    r'|feedfetcher|mediapartners|adsbot|apis-google|validator|check_http',
    re.I,
)


def is_bot(user_agent: str, *, is_app: bool = False) -> bool:
    """True for crawlers, link-preview fetchers and scripts.

    Real browsers always send a User-Agent, so an empty one is a script. The
    Android app is allowed through even though its HTTP stack looks scripted.
    """
    ua = (user_agent or '').strip()
    if is_app:
        return False
    if not ua:
        return True
    return bool(_BOT_RE.search(ua))


# --------------------------------------------------------------------------
# Device / OS / browser
# --------------------------------------------------------------------------

def device_class(user_agent: str) -> str:
    u = (user_agent or '').lower()
    if not u:
        return 'other'
    if 'ipad' in u or 'tablet' in u or ('android' in u and 'mobile' not in u):
        return 'tablet'
    if 'mobi' in u or 'iphone' in u or 'ipod' in u or 'android' in u:
        return 'mobile'
    if any(k in u for k in ('windows', 'macintosh', 'x11', 'linux', 'cros')):
        return 'desktop'
    return 'other'


def detect_platform(user_agent: str) -> str:
    """Operating system family, lowercase. Android is tested before Linux and
    iOS before macOS because those UAs contain both words."""
    ua = (user_agent or '').lower()
    if not ua:
        return ''
    if 'android' in ua:
        return 'android'
    if 'iphone' in ua or 'ipad' in ua or 'ipod' in ua or 'ios' in ua:
        return 'ios'
    if 'windows' in ua:
        return 'windows'
    if 'cros' in ua:
        return 'chromeos'
    if 'macintosh' in ua or 'mac os x' in ua:
        return 'mac'
    if 'linux' in ua or 'x11' in ua:
        return 'linux'
    return ''


_BROWSERS = (
    ('fban', 'Facebook app'), ('fbav', 'Facebook app'), ('fb_iab', 'Facebook app'),
    ('instagram', 'Instagram app'),
    ('edg/', 'Edge'), ('edga/', 'Edge'), ('edgios/', 'Edge'),
    ('opr/', 'Opera'), ('opera', 'Opera'),
    ('samsungbrowser', 'Samsung Internet'),
    ('ucbrowser', 'UC Browser'),
    ('firefox', 'Firefox'), ('fxios', 'Firefox'),
    ('; wv)', 'Android WebView'),
    ('chrome', 'Chrome'), ('crios', 'Chrome'),
    ('safari', 'Safari'),
)


def browser_name(user_agent: str) -> str:
    ua = (user_agent or '').lower()
    if not ua:
        return ''
    for token, name in _BROWSERS:
        if token in ua:
            return name
    return 'Other'


# --------------------------------------------------------------------------
# Referrers -> channel + friendly source name
# --------------------------------------------------------------------------

CHANNELS = ('direct', 'search', 'social', 'email', 'ai', 'referral', 'campaign')
INTERNAL = 'internal'

_HOST_PREFIX_RE = re.compile(r'^(www|m|mobile|l|lm|lnk|out|away|amp)\.')

Referrer = namedtuple('Referrer', 'host channel name')


def normalize_host(host: str) -> str:
    h = (host or '').lower().strip().rstrip('.')
    prev = None
    while h != prev:
        prev = h
        h = _HOST_PREFIX_RE.sub('', h)
    return h


# (regex on the normalised host, friendly name, channel). First match wins, so
# the specific hosts (Gmail, Classroom, Gemini) sit above the broad ones.
_RULES = tuple(
    (re.compile(rx), name, channel) for rx, name, channel in (
        # OAuth / login round trips: someone who signed in, not someone we won.
        (r'^accounts\.(google|youtube)\.', 'Sign-in redirect', INTERNAL),
        (r'^login\.facebook\.com$', 'Sign-in redirect', INTERNAL),
        # Email
        (r'^(mail|inbox)\.google\.', 'Gmail', 'email'),
        (r'^com\.google\.android\.gm$', 'Gmail', 'email'),
        (r'^(outlook\.(live|office|office365)\.com|com\.microsoft\.office\.outlook)$', 'Outlook', 'email'),
        (r'^mail\.(yahoo|proton|zoho)\.', 'Webmail', 'email'),
        # AI assistants
        (r'^gemini\.google\.', 'Gemini', 'ai'),
        (r'^(chatgpt\.com|chat\.openai\.com|openai\.com|com\.openai\.chatgpt)$', 'ChatGPT', 'ai'),
        (r'^claude\.ai$', 'Claude', 'ai'),
        (r'^perplexity\.ai$', 'Perplexity', 'ai'),
        (r'^copilot\.microsoft\.com$', 'Copilot', 'ai'),
        (r'^(deepseek\.com|chat\.deepseek\.com|grok\.com|poe\.com|you\.com)$', 'AI assistant', 'ai'),
        # Education surfaces that are referrals, not search
        (r'^classroom\.google\.', 'Google Classroom', 'referral'),
        # Search
        (r'^com\.google\.android\.googlequicksearchbox$', 'Google', 'search'),
        (r'^google\.[a-z.]+$', 'Google', 'search'),
        (r'^(bing\.com|cn\.bing\.com)$', 'Bing', 'search'),
        (r'^([a-z]+\.)?yahoo\.', 'Yahoo', 'search'),
        (r'^duckduckgo\.com$', 'DuckDuckGo', 'search'),
        (r'^(search\.brave\.com|brave\.com)$', 'Brave Search', 'search'),
        (r'^(baidu|yandex|ecosia|qwant|startpage|naver|kagi)\.', 'Other search', 'search'),
        (r'^ask\.com$', 'Other search', 'search'),
        # Social / messaging
        (r'^(facebook\.com|fb\.com|fb\.me|m\.me|messenger\.com|com\.facebook\.(katana|lite|orca))$', 'Facebook', 'social'),
        (r'^(instagram\.com|com\.instagram\.android)$', 'Instagram', 'social'),
        (r'^(twitter\.com|x\.com|t\.co)$', 'X', 'social'),
        (r'^(linkedin\.com|lnkd\.in)$', 'LinkedIn', 'social'),
        (r'^reddit\.com$', 'Reddit', 'social'),
        (r'^(tiktok\.com|vm\.tiktok\.com)$', 'TikTok', 'social'),
        (r'^pinterest\.', 'Pinterest', 'social'),
        (r'^(youtube\.com|youtu\.be|com\.google\.android\.youtube)$', 'YouTube', 'social'),
        (r'^(whatsapp\.com|wa\.me|com\.whatsapp)$', 'WhatsApp', 'social'),
        (r'^(telegram\.org|t\.me|telegram\.me|org\.telegram\.[a-z.]+)$', 'Telegram', 'social'),
        (r'^(discord\.com|discord\.gg|com\.discord)$', 'Discord', 'social'),
        (r'^(snapchat\.com|com\.snapchat\.android)$', 'Snapchat', 'social'),
        (r'^(threads\.net|com\.viber\.voip)$', 'Social', 'social'),
    )
)

_UTM_MEDIUM_CHANNEL = {
    'email': 'email', 'e-mail': 'email', 'newsletter': 'email',
    'social': 'social', 'social-media': 'social', 'sm': 'social',
    'organic': 'search', 'search': 'search',
}


_UTM_SOURCE_ALIASES = {
    'chatgpt': 'chatgpt.com', 'openai': 'chatgpt.com', 'gemini': 'gemini.google.com',
    'claude': 'claude.ai', 'perplexity': 'perplexity.ai', 'copilot': 'copilot.microsoft.com',
    'deepseek': 'deepseek.com', 'grok': 'grok.com', 'google': 'google.com', 'bing': 'bing.com',
    'duckduckgo': 'duckduckgo.com', 'yahoo': 'yahoo.com', 'facebook': 'facebook.com',
    'fb': 'facebook.com', 'ig': 'instagram.com', 'instagram': 'instagram.com',
    'whatsapp': 'whatsapp.com', 'telegram': 'telegram.org', 'twitter': 'x.com', 'x': 'x.com',
    'linkedin': 'linkedin.com', 'reddit': 'reddit.com', 'youtube': 'youtube.com',
    'tiktok': 'tiktok.com', 'gmail': 'mail.google.com',
}


def classify_utm_source(utm_source: str):
    """Map a utm_source like `chatgpt.com` or `ig` onto the known referrer rules.

    Returns a Referrer or None. Only well-known sources match, so a custom
    campaign name stays a campaign.
    """
    raw = (utm_source or '').strip().lower()
    if not raw or len(raw) > 80:
        return None
    host = normalize_host(_UTM_SOURCE_ALIASES.get(raw, raw))
    if '.' not in host:
        return None
    for rx, name, channel in _RULES:
        if rx.match(host):
            return None if channel == INTERNAL else Referrer(host, channel, name)
    return None


def classify_referrer(referrer_url: str, own_hosts, utm_source: str = '', utm_medium: str = '') -> Referrer:
    """Return (host, channel, name) for a hit.

    `channel` is one of CHANNELS or 'internal'. `own_hosts` is an iterable of
    host names that count as this site. Internal navigation is never an
    acquisition channel: the report ignores it for sources and channels.
    """
    ref = (referrer_url or '').strip()
    host = ''
    path = ''
    if ref:
        try:
            parsed = urlparse(ref)
            host = normalize_host(parsed.hostname or '')
            path = parsed.path or ''
        except ValueError:
            host = ''

    own = {normalize_host(h) for h in own_hosts if h}
    if host:
        if host in own or any(host.endswith('.' + o) for o in own):
            return Referrer(host, INTERNAL, host)
        if host in ('localhost', '127.0.0.1', '::1') or host.endswith('.localhost'):
            return Referrer(host, INTERNAL, host)
        if host == 'github.com' and path.startswith('/login'):
            return Referrer(host, INTERNAL, 'Sign-in redirect')
        for rx, name, channel in _RULES:
            if rx.match(host):
                return Referrer(host, channel, name)

    utm_source = (utm_source or '').strip()[:80]
    utm_medium = (utm_medium or '').strip().lower()
    if host:
        # Unknown external site. A utm_medium can still say what kind it is.
        channel = _UTM_MEDIUM_CHANNEL.get(utm_medium, 'referral')
        return Referrer(host, channel, host)
    known = classify_utm_source(utm_source)
    if known:
        # ChatGPT, Gemini and friends strip the Referer header but tag the link
        # with utm_source=chatgpt.com: that is an AI assistant, not a campaign.
        return known
    if utm_source or utm_medium:
        channel = _UTM_MEDIUM_CHANNEL.get(utm_medium, 'campaign')
        return Referrer('', channel, utm_source or 'Campaign')
    return Referrer('', 'direct', 'Direct')


def referrer_label(url: str) -> str:
    """What we keep of a referrer URL: host and path, never the query string."""
    try:
        p = urlparse(url or '')
    except ValueError:
        return ''
    if not p.hostname:
        return ''
    return (p.hostname + (p.path or ''))[:255]


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

Page = namedtuple('Page', 'key label section')

_SEGMENT_SECTION = {
    'forum': 'Forum', 'library': 'Library', 'resource': 'Library', 'reader': 'Library',
    'upload': 'Library', 'past-papers': 'Library', 'model-questions': 'Library',
    'requests': 'Library', 'syllabus': 'Syllabus', 'subject': 'Syllabus',
    'interactive': 'Interactive', 'news': 'News',
    'results': 'Results', 'tools': 'Tools', 'search': 'Search',
    'profile': 'Profiles', 'settings': 'Account', 'credits': 'Account',
    'bookmarks': 'Account', 'notifications': 'Account',
    'analytics': 'Account', 'study-space': 'Study', 'study-lab': 'Study', 'canvas': 'Study',
    'online-learning': 'Study', 'faq': 'Info',
}

# (regex, key, label, section) for routes with dynamic segments.
_PAGE_RULES = tuple(
    (re.compile(rx), key, label, section) for rx, key, label, section in (
        (r'^/app/forum/post/[^/]+/$', '/app/forum/post/*/', 'Forum thread', 'Forum'),
        (r'^/app/forum/reply/[^/]+/$', '/app/forum/reply/*/', 'Forum reply', 'Forum'),
        (r'^/app/resource/[^/]+/(edit|submit-payment)/$', '/app/resource/*/manage/', 'Resource (manage)', 'Library'),
        (r'^/app/resource/[^/]+/$', '/app/resource/*/', 'Resource', 'Library'),
        (r'^/app/reader/[^/]+/$', '/app/reader/*/', 'Reader', 'Library'),
        (r'^/app/syllabus/[^/]+/[^/]+/.+$', '/app/syllabus/*/*/chapter/', 'Syllabus chapter', 'Syllabus'),
        (r'^/app/syllabus/[^/]+/[^/]+/$', '/app/syllabus/*/*/', 'Syllabus subject', 'Syllabus'),
        (r'^/app/syllabus/[^/]+/$', '/app/syllabus/*/', 'Syllabus class', 'Syllabus'),
        (r'^/app/subject/[^/]+/[^/]+/$', '/app/subject/*/*/', 'Subject', 'Syllabus'),
        (r'^/app/news/[^/]+/$', '/app/news/*/', 'News article', 'News'),
        (r'^/app/interactive/[^/]+/[^/]+/$', '/app/interactive/*/*/', 'Interactive lesson', 'Interactive'),
        (r'^/app/interactive/[^/]+/$', '/app/interactive/*/', 'Interactive course', 'Interactive'),
        (r'^/app/profile/[^/]+/(achievements/)?$', '/app/profile/*/', 'Profile', 'Profiles'),
        (r'^/avatar/[^/]+/$', '/avatar/*/', 'Public avatar profile', 'Profiles'),
        (r'^/auth/', '/auth/*', 'Sign-in flow', 'Account'),
    )
)

_STATIC_LABELS = {
    '/': ('Landing page', 'Landing'),
    '/login/': ('Sign in', 'Account'),
    '/app/': ('Home feed', 'Home'),
    '/avatar/': ('Avatar studio', 'Profiles'),
    '/privacy/': ('Privacy', 'Info'),
    '/terms/': ('Terms', 'Info'),
}


def _prettify(path: str) -> str:
    parts = [p for p in path.strip('/').split('/') if p and p != 'app']
    if not parts:
        return path
    return ' / '.join(p.replace('-', ' ').replace('_', ' ').capitalize() for p in parts[:3])


def classify_page(path: str) -> Page:
    """Collapse a concrete URL path to a route pattern with a readable label.

    /avatar/prashantchataut/ and /avatar/bAdhikarii/ are one page, not two
    hundred rows in a top-pages table.
    """
    p = (path or '/').split('?', 1)[0].split('#', 1)[0]
    if not p.startswith('/'):
        p = '/' + p
    if not p.endswith('/') and '.' not in p.rsplit('/', 1)[-1]:
        p += '/'
    if p in _STATIC_LABELS:
        label, section = _STATIC_LABELS[p]
        return Page(p, label, section)
    for rx, key, label, section in _PAGE_RULES:
        if rx.match(p):
            return Page(key, label, section)
    segs = [s for s in p.strip('/').split('/') if s]
    section = 'Other'
    if segs and segs[0] == 'app' and len(segs) > 1:
        section = _SEGMENT_SECTION.get(segs[1], 'Other')
    key = p[:200]
    return Page(key, _prettify(p), section)


# --------------------------------------------------------------------------
# Visitors (no cookies, no raw IPs stored)
# --------------------------------------------------------------------------

def anon_visitor_id(secret: str, day: str, ip: str, user_agent: str) -> str:
    """Daily-rotating pseudonym for a logged-out visitor.

    The salt includes the local date, so the same person cannot be followed
    from one day to the next, and nothing here can be turned back into an IP.
    """
    raw = f'{secret}|anon|{day}|{ip}|{user_agent}'.encode('utf-8', 'ignore')
    return 'a' + hashlib.sha256(raw).hexdigest()[:19]


def user_visitor_id(secret: str, user_id: str) -> str:
    """Stable pseudonym for a signed-in visitor, so one account counts once
    over any range and across devices."""
    raw = f'{secret}|user|{user_id}'.encode('utf-8', 'ignore')
    return 'u' + hashlib.sha256(raw).hexdigest()[:19]


# --------------------------------------------------------------------------
# Geography from edge headers (no third party sees visitor IPs)
# --------------------------------------------------------------------------

_COUNTRIES = (
    'AF Afghanistan|AL Albania|DZ Algeria|AD Andorra|AO Angola|AR Argentina|AM Armenia|AU Australia|'
    'AT Austria|AZ Azerbaijan|BS Bahamas|BH Bahrain|BD Bangladesh|BY Belarus|BE Belgium|BZ Belize|'
    'BJ Benin|BT Bhutan|BO Bolivia|BA Bosnia and Herzegovina|BW Botswana|BR Brazil|BN Brunei|'
    'BG Bulgaria|BF Burkina Faso|BI Burundi|KH Cambodia|CM Cameroon|CA Canada|CL Chile|CN China|'
    'CO Colombia|CR Costa Rica|HR Croatia|CU Cuba|CY Cyprus|CZ Czechia|DK Denmark|DO Dominican Republic|'
    'EC Ecuador|EG Egypt|SV El Salvador|EE Estonia|ET Ethiopia|FI Finland|FR France|GE Georgia|'
    'DE Germany|GH Ghana|GR Greece|GT Guatemala|HK Hong Kong|HU Hungary|IS Iceland|IN India|'
    'ID Indonesia|IR Iran|IQ Iraq|IE Ireland|IL Israel|IT Italy|JM Jamaica|JP Japan|JO Jordan|'
    'KZ Kazakhstan|KE Kenya|KW Kuwait|KG Kyrgyzstan|LA Laos|LV Latvia|LB Lebanon|LY Libya|LT Lithuania|'
    'LU Luxembourg|MO Macao|MG Madagascar|MW Malawi|MY Malaysia|MV Maldives|ML Mali|MT Malta|MU Mauritius|'
    'MX Mexico|MD Moldova|MN Mongolia|ME Montenegro|MA Morocco|MZ Mozambique|MM Myanmar|NA Namibia|'
    'NP Nepal|NL Netherlands|NZ New Zealand|NI Nicaragua|NE Niger|NG Nigeria|MK North Macedonia|NO Norway|'
    'OM Oman|PK Pakistan|PS Palestine|PA Panama|PY Paraguay|PE Peru|PH Philippines|PL Poland|PT Portugal|'
    'PR Puerto Rico|QA Qatar|RO Romania|RU Russia|RW Rwanda|SA Saudi Arabia|SN Senegal|RS Serbia|SG Singapore|'
    'SK Slovakia|SI Slovenia|SO Somalia|ZA South Africa|KR South Korea|SS South Sudan|ES Spain|LK Sri Lanka|'
    'SD Sudan|SE Sweden|CH Switzerland|SY Syria|TW Taiwan|TJ Tajikistan|TZ Tanzania|TH Thailand|TN Tunisia|'
    'TR Turkey|TM Turkmenistan|UG Uganda|UA Ukraine|AE United Arab Emirates|GB United Kingdom|'
    'US United States|UY Uruguay|UZ Uzbekistan|VE Venezuela|VN Vietnam|YE Yemen|ZM Zambia|ZW Zimbabwe'
)
COUNTRY_NAMES = dict(item.split(' ', 1) for item in _COUNTRIES.split('|'))


def country_from_code(code: str) -> str:
    """Country name for a 2-letter code; '' for unknown, Tor (T1) and XX."""
    c = (code or '').strip().upper()
    if len(c) != 2 or c in ('XX', 'T1', 'ZZ'):
        return ''
    return COUNTRY_NAMES.get(c, '')
