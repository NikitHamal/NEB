"""Builds api/data/pathways/wave15.json from w15_abroad.py, w15_nepal.py and w15_sites.py.

Wave 15 (adds to waves 12 to 14, no overlap): Romania, Estonia, Switzerland and Cyprus, the Romanian government scholarship, ACCA partners, flying schools, two Health Service Lok Sewa
exams, 2083/84 Lok Sewa dates, NEB and SEE calendar answers, fourteen FAQs and verified websites for 80 colleges that had none.
Run: python3 backend_python/tools/pathways/build_wave15.py   (never hand edit wave15.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w15_abroad as A  # noqa: E402
import w15_more as M  # noqa: E402
import w15_nepal as N  # noqa: E402
import w15_sites as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

out = {
    'abroad_add': A.ABROAD_ADD,
    'abroad_update': A.ABROAD_UPDATE,
    'scholarships_add': A.SCHOLARSHIPS_ADD,
    'scholarship_extra': {**A.SCHOLARSHIP_EXTRA, **M.SCHOLARSHIP_EXTRA},
    'providers_add': M.PROVIDERS_ADD,
    'where_add': M.WHERE_ADD,
    'route_about_add': M.NOTE_ROUTE,
    'govt_add': N.GOVT_ADD,
    'govt_note_add': N.GOVT_NOTE_ADD,
    'faq_add': N.FAQ_ADD + M.FAQ_ADD,
    'provider_update': {pid: {'website': url} for pid, url in S.WEBSITES.items()},
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text
(DATA / 'wave15.json').write_text(text + '\n', encoding='utf-8')
print('wave15.json', len(text), 'bytes', len(N.FAQ_ADD) + len(M.FAQ_ADD), 'faq', len(A.ABROAD_ADD), 'abroad', len(S.WEBSITES), 'websites')
