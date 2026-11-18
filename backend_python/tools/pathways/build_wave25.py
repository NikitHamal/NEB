"""Builds api/data/pathways/wave25.json from w25_campus.py, w25_abroad.py and w25_faq.py.

Wave 25 (adds to waves 12 to 24, no overlap):
- 8 constituent campuses: 6 Far-Western University (Tikapur, Triveni, Ghanteshwar Seti Mahakali, Sitaram, Patan Baitadi, Durgalaxmi)
  from the FWU Faculty of Education campus table and the campus sites, 2 Mid-West University (Bageshwari, Vidhyapur Janata)
- B.Ed., M.Ed., BBS, BBA, BA and MBS links for those campuses and for 9 existing FWU providers; Manilek record corrected
- stay back / work rules for Spain, Portugal, Estonia, Hungary, Romania, Cyprus and Norway from the EC portal and UDI
- 20 Kathmandu University affiliated institutions missing from the dataset (official KU table), BIT / hospitality / BBA / BSW links
- 14 FAQs (`fw25-1` to `fw25-14`)
Run: python3 backend_python/tools/pathways/build_wave25.py   (never hand edit wave25.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w25_abroad as A  # noqa: E402
import w25_campus as C  # noqa: E402
import w25_faq as F  # noqa: E402
import w25_faq2 as F2  # noqa: E402
import w25_ku as K  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
PROV = C.PROVIDERS_ADD + K.PROVIDERS_ADD
FAQS = F.FAQ_ADD + F2.FAQ_ADD
ids = [p['id'] for p in PROV]
assert len(ids) == len(set(ids)), 'duplicate provider id'
assert len(FAQS) == 14 and len(PROV) == 28
where_add = {}
for src in (C.WHERE_ADD, K.WHERE_ADD):
    for r, v in src.items():
        where_add[r] = list(dict.fromkeys(where_add.get(r, []) + v))
out = {'providers_add': PROV, 'where_add': where_add, 'provider_update': {**C.PROVIDER_UPDATE, **K.PROVIDER_UPDATE},
       'abroad_update': A.ABROAD_UPDATE, 'faq_add': FAQS}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave25.json').write_text(text + '\n', encoding='utf-8')
print('wave25.json', len(text), 'bytes;', len(PROV), 'providers;', sum(len(v) for v in where_add.values()), 'route links;',
      len(A.ABROAD_UPDATE), 'abroad updates;', len(FAQS), 'faqs')
