"""Static scan: rules whose background and text colour come from different 'worlds'.
In dark mode the m3x roles flip (primary becomes light), so a hard-coded white label on
var(--md-primary), or var(--md-on-primary) on a hard-coded fill, silently loses contrast.
   python3 tools/design/pairs.py backend_python/web/static/web/css"""
import re, sys, pathlib
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
rule = re.compile(r'([^{}]+)\{([^{}]*)\}')
WHITE = re.compile(r'(?<![\w-])color\s*:\s*(#fff(?:fff)?|white)\b', re.I)
DARK = re.compile(r'(?<![\w-])color\s*:\s*(#000(?:000)?|black)\b', re.I)
for f in sorted(root.rglob('*.css')):
    if f.name.endswith('.min.css') or 'vendor' in f.parts: continue
    txt = re.sub(r'/\*.*?\*/', '', f.read_text(errors='ignore'), flags=re.S)
    for m in rule.finditer(txt):
        sel, body = m.group(1).strip(), m.group(2)
        bg = re.search(r'background(?:-color)?\s*:\s*([^;]+)', body)
        if not bg: continue
        b = bg.group(1)
        role = re.search(r'var\(--(?:md-)?(primary|secondary|tertiary|inverse-primary|pri)(?:-container)?\b', b)
        onrole = re.search(r'(?<![\w-])color\s*:\s*var\(--md-on-(primary|secondary|tertiary)', body)
        hard = re.search(r'^\s*(#[0-9a-f]{3,8}|rgb)', b.strip(), re.I)
        if role and (WHITE.search(body) or DARK.search(body)):
            print(f'{f.name}: [hardcoded text on role fill] {sel[:80]} -> {b.strip()[:40]}')
        elif onrole and hard:
            print(f'{f.name}: [role text on hardcoded fill] {sel[:80]} -> {b.strip()[:40]}')
