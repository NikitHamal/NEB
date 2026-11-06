"""Keep TeX intact while a forum body goes through markdown.

Markdown reads x_1 + y_2 as emphasis and turns straight quotes curly, so a
formula has to be set aside before rendering and put back after sanitising.
Code spans and fences are left alone: a dollar sign in code is a dollar sign.
"""
import re
from django.utils.html import escape

_CODE = r'```.*?```|`[^`\n]+`'
_DISPLAY = r'\$\$.+?\$\$'
_INLINE = r'(?<![\\$\w])\$(?!\s)[^$\n]+?(?<!\s)\$(?![\w$])'
_PATTERN = re.compile('(%s)|(%s)|(%s)' % (_CODE, _DISPLAY, _INLINE), re.S)
_TOKEN = re.compile(r'zzmathzz(\d+)zz')


def protect_math(text):
    stash = []

    def repl(m):
        if m.group(1):
            return m.group(0)
        stash.append(m.group(0))
        return 'zzmathzz%dzz' % (len(stash) - 1)

    return _PATTERN.sub(repl, text), stash


def restore_math(html, stash):
    if not stash:
        return html
    return _TOKEN.sub(lambda m: escape(stash[int(m.group(1))]) if int(m.group(1)) < len(stash) else m.group(0), html)
