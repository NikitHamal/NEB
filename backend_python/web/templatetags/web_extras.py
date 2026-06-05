import json
import re
import time
from datetime import datetime, timezone
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import quote
import markdown as md_lib

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def timestamp_to_iso(value):
    """Convert millisecond timestamp to ISO 8601 format for JSON-LD."""
    try:
        ts = int(value) / 1000
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.isoformat()
    except (ValueError, TypeError):
        return ''

@register.filter
def time_ago(value):
    try:
        ts = int(value) / 1000
    except (ValueError, TypeError):
        return ''
    import time
    now = time.time()
    diff = now - ts
    if diff < 60:
        return 'just now'
    if diff < 3600:
        return f'{int(diff / 60)}m ago'
    if diff < 86400:
        return f'{int(diff / 3600)}h ago'
    if diff < 2592000:
        return f'{int(diff / 86400)}d ago'
    return f'{int(diff / 2592000)}mo ago'


@register.filter
def join_date(value):
    """Format a millisecond Unix timestamp as 'Month YYYY' (e.g. 'January 2025').
    Returns empty string when value is 0/None/invalid."""
    try:
        ts = int(value)
        if ts <= 0:
            return ''
        dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
        return dt.strftime('%B %Y')
    except (ValueError, TypeError, OSError):
        return ''


def _normalize_subject(subject):
    s = (subject or '').lower().strip()
    if not s:
        return 'general'
    if 'physics' in s:
        return 'physics'
    if 'chemistry' in s:
        return 'chemistry'
    if 'math' in s:
        return 'mathematics'
    if 'biology' in s:
        return 'biology'
    if 'english' in s:
        return 'english'
    if 'nepali' in s:
        return 'nepali'
    if 'computer' in s or 'network' in s:
        return 'computer science'
    if 'economics' in s:
        return 'economics'
    if 'account' in s:
        return 'accountancy'
    if 'exam' in s or 'prep' in s:
        return 'exam tips'
    return s


@register.filter
def subject_color(subject):
    colors = {
        'physics': '#1B6EF3',
        'chemistry': '#006E1C',
        'mathematics': '#E8710A',
        'math': '#E8710A',
        'biology': '#9334E6',
        'english': '#D93025',
        'nepali': '#1967D2',
        'computer science': '#185ABC',
        'economics': '#E37400',
        'accountancy': '#0D652D',
        'general': '#5F6368',
        'exam tips': '#C5221F',
    }
    return colors.get(_normalize_subject(subject), '#5F6368')


@register.filter
def subject_slug(subject):
    import re
    s = _normalize_subject(subject)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


@register.filter
def subject_icon(subject):
    icons = {
        'physics': 'science',
        'chemistry': 'biotech',
        'mathematics': 'calculate',
        'math': 'calculate',
        'biology': 'eco',
        'english': 'menu_book',
        'nepali': 'translate',
        'computer science': 'computer',
        'economics': 'trending_up',
        'accountancy': 'account_balance',
        'general': 'category',
        'exam tips': 'quiz',
    }
    return icons.get(_normalize_subject(subject), 'category')


@register.filter
def resource_type_icon(rtype):
    """Return a Material Symbol icon name for a resource type."""
    icons = {
        'pdf': 'picture_as_pdf',
        'note': 'description',
        'notes': 'description',
        'video': 'play_circle',
        'audio': 'headphones',
        'image': 'image',
        'link': 'link',
        'textbook': 'menu_book',
        'paper': 'article',
        'past paper': 'article',
        'model paper': 'article',
        'presentation': 'slideshow',
        'slides': 'slideshow',
        'document': 'description',
    }
    return icons.get((rtype or '').lower().strip(), 'description')


@register.filter
def resource_media_type(rtype):
    """Classify resource type into media category for rendering."""
    t = (rtype or '').lower().strip()
    if t in ('pdf',):
        return 'pdf'
    if t in ('video',):
        return 'video'
    if t in ('audio',):
        return 'audio'
    if t in ('image',):
        return 'image'
    return 'document'


@register.filter
def file_size_human(bytes_val):
    try:
        b = int(bytes_val)
    except (ValueError, TypeError):
        return ''
    if b < 1024:
        return f'{b} B'
    if b < 1048576:
        return f'{b / 1024:.1f} KB'
    return f'{b / 1048576:.1f} MB'


@register.filter
def short_number(value):
    try:
        n = int(value)
    except (ValueError, TypeError):
        return value if value else '0'
    if n < 1000:
        return str(n)
    if n < 1_000_000:
        v = n / 1000
        return f'{v:.1f}K' if v != int(v) else f'{int(v)}K'
    v = n / 1_000_000
    return f'{v:.1f}M' if v != int(v) else f'{int(v)}M'


@register.filter
def truncate_chars(value, max_length):
    if not value:
        return ''
    s = str(value)
    if len(s) <= max_length:
        return s
    if max_length <= 3:
        return s[:max_length]
    return s[:max_length - 3] + '...'


@register.filter
def format_count(value):
    try:
        n = int(value)
    except (ValueError, TypeError):
        return value
    if n >= 1000000:
        return f'{n / 1000000:.1f}M'
    if n >= 1000:
        return f'{n / 1000:.1f}K'
    return str(n)


@register.filter
def to_json(value):
    if value is None:
        return mark_safe('null')
    json_str = json.dumps(value, ensure_ascii=True)
    json_str = json_str.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return mark_safe(json_str)


@register.filter
def mention_links(value, usernames=None):
    """Convert @username mentions in text to clickable profile links, then render basic markdown."""
    if not value:
        return mark_safe('')
    return _render_user_content(str(value))


@register.filter
def render_content(value):
    """Render markdown formatting and @mention links for post card previews. Truncates to ~50 words."""
    if not value:
        return mark_safe('')
    plain = str(value)
    words = plain.split()
    if len(words) > 50:
        truncated = ' '.join(words[:50])
        html = _render_user_content(truncated)
        return mark_safe(str(html) + '&hellip;')
    return _render_user_content(plain)


_STRIP_BLOCK_RE = re.compile(r'</?(?:h[1-6]|pre|blockquote|ul|ol|li|table|thead|tbody|tr|th|td|hr|div|p)\b[^>]*>', re.IGNORECASE)


@register.filter
def render_content_inline(value):
    """Render content for card previews — strips block-level tags, keeps inline formatting only."""
    if not value:
        return mark_safe('')
    html = _render_user_content(str(value))
    inline = _STRIP_BLOCK_RE.sub('', str(html))
    return mark_safe(inline)


def _render_user_content(value):
    """Render markdown formatting and @mention links."""
    text = str(value)
    mention_re = re.compile(r'@([A-Za-z0-9_]+)')

    def replace_mentions(text):
        parts = []
        last = 0
        for m in mention_re.finditer(text):
            if m.start() > last:
                parts.append(text[last:m.start()])
            parts.append('[@' + m.group(1) + '](/profile/' + quote(m.group(1)) + '/)')
            last = m.end()
        if last < len(text):
            parts.append(text[last:])
        return ''.join(parts)

    md_text = replace_mentions(text)
    html = md_lib.markdown(md_text, extensions=['nl2br', 'tables', 'sane_lists', 'smarty'], output_format='html5')

    html = re.sub(
        r'<a href="/profile/([^"]+)/">',
        r'<a href="/profile/\1/" class="fp-mention">',
        html,
    )
    html = re.sub(
        r'<a href="(?!/profile/|/)(https?://[^"]+)"(?![^>]*target=)',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html,
    )

    return mark_safe(html)


@register.filter
def comma_space(value):
    """Add a space after commas if missing. e.g. 'a,b,c' -> 'a, b, c'"""
    if not value:
        return ''
    s = str(value)
    import re
    return re.sub(r'\s*,\s*', ', ', s).strip()


@register.filter
def split(value, key):
    if not value:
        return []
    return [s.strip() for s in str(value).split(key) if s.strip()]


@register.filter
def dict_get(d, key):
    """Get an item from a dict by key. Usage: {{ mydict|dict_get:key }}"""
    if not isinstance(d, dict):
        return None
    return d.get(key)


@register.filter
def clean_province(value):
    if not value:
        return ''
    s = str(value).strip()
    mapping = {
        '1': 'Koshi',
        '2': 'Madhesh',
        '3': 'Bagmati',
        '4': 'Gandaki',
        '5': 'Lumbini',
        '6': 'Karnali',
        '7': 'Sudurpashchim',
    }
    if s in mapping:
        return mapping[s]
    
    import re
    s_lower = s.lower()
    if 'province 1' in s_lower or 'koshi' in s_lower:
        return 'Koshi'
    if 'province 2' in s_lower or 'madhesh' in s_lower:
        return 'Madhesh'
    if 'province 3' in s_lower or 'bagmati' in s_lower:
        return 'Bagmati'
    if 'province 4' in s_lower or 'gandaki' in s_lower:
        return 'Gandaki'
    if 'province 5' in s_lower or 'lumbini' in s_lower:
        return 'Lumbini'
    if 'province 6' in s_lower or 'karnali' in s_lower:
        return 'Karnali'
    if 'province 7' in s_lower or 'sudurpashchim' in s_lower:
        return 'Sudurpashchim'
    
    s_clean = re.sub(r'(?i)\bprovience\b|\bprovince\b', '', s)
    s_clean = re.sub(r'\s+', ' ', s_clean).strip(' ,')
    return s_clean


@register.simple_tag
def role_badge(verification_level, moderator_level, is_admin):
    """Render role badge HTML (admin crown, mod shield, or verified tick)."""
    if is_admin:
        return mark_safe('<span class="role-badge role-badge-admin" title="Admin"><span class="material-symbols-outlined">crown</span></span>')
    if moderator_level and int(moderator_level) > 0:
        ml = int(moderator_level)
        if ml == 3:
            return mark_safe('<span class="role-badge role-badge-mod-3" title="Community Lead"><span class="material-symbols-outlined">shield_with_heart</span></span>')
        elif ml == 2:
            return mark_safe('<span class="role-badge role-badge-mod-2" title="Senior Mod"><span class="material-symbols-outlined">shield</span></span>')
        else:
            return mark_safe('<span class="role-badge role-badge-mod-1" title="Community Mod"><span class="material-symbols-outlined">local_police</span></span>')
    if verification_level and int(verification_level) > 0:
        vl = int(verification_level)
        if vl == 4:
            return mark_safe('<span class="role-badge role-badge-verified-4" title="Elite Verified"><span class="material-symbols-outlined">verified</span></span>')
        elif vl == 3:
            return mark_safe('<span class="role-badge role-badge-verified-3" title="Premium Verified"><span class="material-symbols-outlined">verified</span></span>')
        elif vl == 2:
            return mark_safe('<span class="role-badge role-badge-verified-2" title="Expert Verified"><span class="material-symbols-outlined">verified</span></span>')
        else:
            return mark_safe('<span class="role-badge role-badge-verified-1" title="Verified"><span class="material-symbols-outlined">verified</span></span>')
    return mark_safe('')


ACHIEVEMENT_MAP = {
    'top_contributor': {'icon': 'emoji_events', 'label': 'Top Contributor'},
    'helpful': {'icon': 'volunteer_activism', 'label': 'Helpful'},
    'scholar': {'icon': 'school', 'label': 'Scholar'},
    'streak': {'icon': 'local_fire_department', 'label': 'Streak'},
    'first_post': {'icon': 'rocket_launch', 'label': 'First Post'},
    '100_likes': {'icon': 'favorite', 'label': '100 Likes'},
    'bookworm': {'icon': 'auto_stories', 'label': 'Bookworm'},
    'problem_solver': {'icon': 'lightbulb', 'label': 'Problem Solver'},
}


@register.filter
def achievement_badges(badges_str):
    """Render achievement badges HTML from comma-separated keys."""
    if not badges_str:
        return mark_safe('')
    parts = [s.strip() for s in str(badges_str).split(',') if s.strip()]
    html_parts = []
    for key in parts:
        info = ACHIEVEMENT_MAP.get(key)
        if info:
            html_parts.append(
                f'<span class="achievement-badge {key}" title="{info["label"]}">'
                f'<span class="material-symbols-outlined">{info["icon"]}</span>'
                f'{info["label"]}</span>'
            )
    return mark_safe(' '.join(html_parts))


@register.filter
def markdown_format(value):
    """Render markdown formatting safely without mention replacement."""
    if not value:
        return mark_safe('')
    html = md_lib.markdown(str(value), extensions=['nl2br', 'tables', 'sane_lists', 'smarty'], output_format='html5')
    html = re.sub(
        r'<a href="(?!/)(https?://[^"]+)"(?![^>]*target=)',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html,
    )
    return mark_safe(html)


@register.filter
def markdown(value):
    """Alias for markdown_format for template brevity."""
    return markdown_format(value)


@register.filter
def parse_qa(value):
    """Parse Q&A text format into list of {question, answer} dicts for template rendering."""
    if not value:
        return []
    blocks = str(value).split('\n\n')
    result = []
    for block in blocks:
        lines = block.strip().split('\n')
        question = ''
        answer = ''
        current = 'q'
        for line in lines:
            stripped = line.strip()
            if stripped.lower().startswith('q:') or stripped.lower().startswith('q：'):
                question = stripped[2:].strip()
                current = 'a'
            elif stripped.lower().startswith('a:') or stripped.lower().startswith('a：'):
                answer = stripped[2:].strip()
                current = 'a'
            elif current == 'q':
                question = (question + ' ' + stripped).strip() if question else stripped
            else:
                answer = (answer + ' ' + stripped).strip() if answer else stripped
        if question or answer:
            result.append({'question': question, 'answer': answer})
    return result
