"""Builds api/data/pathways/wave37.json from the w37_*.py tables (never hand edit wave37.json).

Run: python3 backend_python/tools/pathways/build_wave37.py
Each w37_* module may define any of the upper case keys listed in KEYS.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave37.json').exists():
    (DATA / 'wave37.json').unlink()
KEYS = ('providers_add', 'where_add', 'route_seats', 'note_add', 'provider_update', 'faq_add', 'abroad_add', 'abroad_update',
        'abroad_note_add', 'abroad_text_swap', 'faq_text_swap', 'scholarships_add', 'scholarship_extra', 'scholarship_note_add', 'careers_new',
        'career_links', 'govt_add', 'govt_note_add', 'guides_add', 'scholarship_text_swap', 'route_note_add', 'abroad_exams_add')
out = {}
for name in ('w37_ctevt', 'w37_nepal', 'w37_abroad', 'w37_exams', 'w37_faq'):
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
import re
_flat = re.sub(r'[a-z0-9]--[a-z0-9]', '', text)  # an old provider id (p-w12-ce-n-p-i--college...) holds a double hyphen
for _bad in ('--', '\u2014', '\u2013'):
    if _bad in _flat:
        _i = _flat.index(_bad)
        print('BAD', repr(_flat[_i - 80:_i + 40]))
assert '\u2014' not in _flat and '\u2013' not in _flat and '--' not in _flat
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave37.json').write_text(text + '\n', encoding='utf-8')
print('wave37.json', len(text), 'bytes;', {k: len(v) for k, v in out.items()})
