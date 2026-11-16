"""Builds api/data/pathways/wave14.json from w14_abroad.py and w14_guides.py.

Wave 14 (adds to waves 12 and 13, no overlap): Uzbekistan, Portugal, Lithuania and Hong Kong, work rules for Czechia, Georgia, Bangladesh,
Kyrgyzstan, Kazakhstan and the Philippines, HKPFS and Pearson scholarships, 2026-27 windows for MGSS, GJSS, Homi Bhabha, Stipendium Hungaricum and
Pokhara University, guides for attestation, TU equivalence and foreign MBBS, 14 FAQs.
Run: python3 backend_python/tools/pathways/build_wave14.py   (never hand edit wave14.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w14_abroad as A  # noqa: E402
import w14_guides as G  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

out = {
    'abroad_add': A.ABROAD_ADD,
    'abroad_update': A.ABROAD_UPDATE,
    'scholarships_add': A.SCHOLARSHIPS_ADD,
    'scholarship_extra': A.SCHOLARSHIP_EXTRA,
    'guides_add': G.GUIDES_ADD,
    'faq_add': G.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text
(DATA / 'wave14.json').write_text(text + '\n', encoding='utf-8')
print('wave14.json', len(text), 'bytes', len(G.FAQ_ADD), 'faq', len(G.GUIDES_ADD), 'guides', len(A.ABROAD_ADD), 'abroad')
