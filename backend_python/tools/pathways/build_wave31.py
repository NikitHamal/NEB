"""Builds api/data/pathways/wave31.json from w31_abroad.py (6 destinations, 3 scholarships) and the other w31_*.py tables.

Run: python3 backend_python/tools/pathways/build_wave31.py   (never hand edit wave31.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave31.json').exists():
    (DATA / 'wave31.json').unlink()
from api import pathways as P  # noqa: E402
import w31_abroad as A  # noqa: E402

base = P.payload()
out = {'abroad_add': A.ABROAD_ADD, 'scholarships_add': A.SCHOLARSHIPS_ADD, 'scholarship_extra': A.SCHOLARSHIP_EXTRA}
for name in ('w31_faq', 'w31_nepal', 'w31_careers'):
    try:
        mod = __import__(name)
    except ImportError:
        continue
    for key in ('providers_add', 'where_add', 'route_seats', 'note_add', 'provider_update', 'faq_add', 'abroad_update', 'scholarships_add', 'scholarship_extra', 'careers_new', 'career_links'):
        val = getattr(mod, key.upper(), None)
        if val:
            if isinstance(val, list):
                out[key] = out.get(key, []) + val
            else:
                out[key] = {**out.get(key, {}), **val}
text = json.dumps(out, ensure_ascii=False, indent=1)
for _bad in ('--', '\u2014', '\u2013'):
    if _bad in text:
        _i = text.index(_bad)
        print('BAD', repr(text[_i - 80:_i + 40]))
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave31.json').write_text(text + '\n', encoding='utf-8')
print('wave31.json', len(text), 'bytes;', {k: len(v) for k, v in out.items()})
