"""Builds api/data/pathways/wave33.json from the w33_*.py tables (never hand edit wave33.json).

Run: python3 backend_python/tools/pathways/build_wave33.py
Each w33_* module may define any of the upper case keys listed in KEYS.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave33.json').exists():
    (DATA / 'wave33.json').unlink()
KEYS = ('providers_add', 'where_add', 'route_seats', 'note_add', 'provider_update', 'faq_add', 'abroad_add', 'abroad_update',
        'abroad_note_add', 'abroad_text_swap', 'faq_text_swap', 'scholarships_add', 'scholarship_extra', 'scholarship_note_add', 'careers_new',
        'career_links', 'govt_add', 'govt_note_add', 'guides_add')
out = {}
for name in ('w33_abroad', 'w33_more', 'w33_nepal', 'w33_exams', 'w33_careers', 'w33_faq'):
    try:
        mod = __import__(name)
    except ImportError:
        continue
    for key in KEYS:
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
(DATA / 'wave33.json').write_text(text + '\n', encoding='utf-8')
print('wave33.json', len(text), 'bytes;', {k: len(v) for k, v in out.items()})
