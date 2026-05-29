import json
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