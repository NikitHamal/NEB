import json
import time
from datetime import datetime, timezone
from django import template
from django.utils.safestring import mark_safe

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
    return colors.get((subject or '').lower().strip(), '#5F6368')


@register.filter
def subject_slug(subject):
    import re
    s = (subject or '').lower().strip()
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
    return icons.get((subject or '').lower().strip(), 'category')


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
    import re
    s = str(value)
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
    if usernames:
        known = set(u.lower() for u in usernames)
        def replacer(m):
            nm = m.group(1)
            if nm.lower() in known:
                return '<a href="/profile/' + nm + '/" class="fp-mention">@' + nm + '</a>'
            return m.group(0)
        s = re.sub(r'@(\w+)', replacer, s)
    else:
        s = re.sub(r'@(\w+)', r'<a href="/profile/\1/" class="fp-mention">@\1</a>', s)
    # Basic markdown: bold, italic, line breaks
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)__(.+?)__(?!\w)', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<em>\1</em>', s)
    s = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', s)
    s = s.replace('\n', '<br>')
    return mark_safe(s)


@register.filter
def render_content(value):
    """Render markdown formatting and @mention links for post card previews. Truncates to ~50 words."""
    if not value:
        return mark_safe('')
    import re
    s = str(value)
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
    s = re.sub(r'@(\w+)', r'<a href="/profile/\1/" class="fp-mention">@\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)__(.+?)__(?!\w)', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<em>\1</em>', s)
    s = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', s)
    s = s.replace('\n', '<br>')
    plain = re.sub(r'<[^>]+>', '', s).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#x27;', "'").replace('&hellip;', '...')
    words = plain.split()
    if len(words) > 50:
        truncated_plain = ' '.join(words[:50])
        t = truncated_plain.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
        t = re.sub(r'@(\w+)', r'<a href="/profile/\1/" class="fp-mention">@\1</a>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'(?<!\w)__(.+?)__(?!\w)', r'<strong>\1</strong>', t)
        t = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<em>\1</em>', t)
        t = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', t)
        t = t.replace('\n', '<br>')
        return mark_safe(t + '&hellip;')
    return mark_safe(s)


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