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
    """Convert @username mentions in text to clickable profile links."""
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
    return mark_safe(s)


@register.filter
def split(value, key):
    if not value:
        return []
    return [s.strip() for s in str(value).split(key) if s.strip()]


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