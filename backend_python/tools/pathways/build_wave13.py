"""Builds api/data/pathways/wave13.json from w13_abroad.py, w13_study.py and w13_faq.py.

Wave 13 (adds to wave 12, no overlap): US rule correction (the fixed admission rule was blocked by a court on 14 September 2026),
UK and German funds, Thailand work rule, scholarship windows (Manaaki, Turkiye Burslari, Rhodes), two new scholarships (Humphrey, SAU),
guides for IOE, MEC and KU admission, KU fees for two more BE routes, the Pulchowk 2083/84 notice, two Baneshwor colleges, 13 FAQs.
Run: python3 backend_python/tools/pathways/build_wave13.py   (never hand edit wave13.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w13_abroad as A  # noqa: E402
import w13_faq as F  # noqa: E402
import w13_study as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

out = {
    'providers_add': S.PROVIDERS_ADD,
    'where_add': S.WHERE_ADD,
    'fees': S.FEES,
    'note_add': S.NOTE_ADD,
    'exam_sub': S.EXAM_SUB,
    'guides_add': S.GUIDES_ADD,
    'scholarship_extra': A.SCHOLARSHIP_EXTRA,
    'scholarships_add': A.SCHOLARSHIPS_ADD,
    'abroad_extra': A.ABROAD_EXTRA,
    'faq_add': F.FAQ_ADD,
    'faq_update': F.FAQ_UPDATE,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text
(DATA / 'wave13.json').write_text(text + '\n', encoding='utf-8')
print('wave13.json', len(text), 'bytes', len(F.FAQ_ADD), 'faq', len(S.GUIDES_ADD), 'guides')
