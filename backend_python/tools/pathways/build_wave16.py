"""Builds api/data/pathways/wave16.json from w16_abroad.py, w16_nepal.py and w16_faq.py.

Wave 16 (adds to waves 12 to 15, no overlap): Malta and Latvia, scholarships for Finland (Aalto, Helsinki), Malaysia, Kazakhstan, the UAE and Uzbekistan, the COMPEX 2026 window,
six A Level and IB schools with fee ranges, ICAN official fees, the MEC MBBS fee text fix, MECEE-BL 2027 dates, the SEE 2083 calendar and fifteen FAQs.
Run: python3 backend_python/tools/pathways/build_wave16.py   (never hand edit wave16.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w16_abroad as A  # noqa: E402
import w16_faq as F  # noqa: E402
import w16_guides as G  # noqa: E402
import w16_more as M  # noqa: E402
import w16_nepal as N  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

out = {
    'abroad_add': A.ABROAD_ADD,
    'abroad_update': {**A.ABROAD_UPDATE, **M.ABROAD_UPDATE},
    'abroad_note_add': M.ABROAD_NOTE_ADD,
    'guides_add': G.GUIDES_ADD,
    'scholarships_add': A.SCHOLARSHIPS_ADD,
    'scholarship_extra': A.SCHOLARSHIP_EXTRA,
    'providers_add': N.PROVIDERS_ADD,
    'where_add': N.WHERE_ADD,
    'fees': N.FEES,
    'provider_note_add': N.PROVIDER_NOTE_ADD,
    'route_about_add': N.ROUTE_ABOUT_ADD,
    'text_swap': N.TEXT_SWAP,
    'faq_add': F.FAQ_ADD + G.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text
(DATA / 'wave16.json').write_text(text + '\n', encoding='utf-8')
print('wave16.json', len(text), 'bytes', len(F.FAQ_ADD) + len(G.FAQ_ADD), 'faq', len(A.ABROAD_ADD), 'abroad', len(A.SCHOLARSHIPS_ADD), 'scholarships', len(N.PROVIDERS_ADD), 'providers')
