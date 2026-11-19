"""Builds api/data/pathways/wave40.json from the w40_*.py tables (never hand edit wave40.json).

Run: python3 backend_python/tools/pathways/build_wave40.py
Each w40_* module may define any of the upper case keys listed in KEYS.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave40.json').exists():
    (DATA / 'wave40.json').unlink()
KEYS = ('providers_add', 'where_add', 'route_seats', 'note_add', 'provider_update', 'faq_add', 'abroad_add', 'abroad_update',
        'abroad_note_add', 'abroad_text_swap', 'faq_text_swap', 'scholarships_add', 'scholarship_extra', 'scholarship_note_add', 'careers_new',
        'career_links', 'govt_add', 'govt_note_add', 'guides_add', 'scholarship_text_swap', 'route_note_add')
out = {}
for name in ('w40_nepal', 'w40_exams', 'w40_faq'):
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
(DATA / 'wave40.json').write_text(text + '\n', encoding='utf-8')
print('wave40.json', len(text), 'bytes;', {k: len(v) for k, v in out.items()})
