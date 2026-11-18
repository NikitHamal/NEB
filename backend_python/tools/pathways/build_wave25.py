"""Builds api/data/pathways/wave25.json from w25_campus.py, w25_abroad.py and w25_faq.py.

Wave 25 (adds to waves 12 to 24, no overlap):
- 8 constituent campuses: 6 Far-Western University (Tikapur, Triveni, Ghanteshwar Seti Mahakali, Sitaram, Patan Baitadi, Durgalaxmi)
  from the FWU Faculty of Education campus table and the campus sites, 2 Mid-West University (Bageshwari, Vidhyapur Janata)
- B.Ed., M.Ed., BBS, BBA, BA and MBS links for those campuses and for 9 existing FWU providers; Manilek record corrected
- stay back / work rules for Spain, Portugal, Estonia, Hungary, Romania, Cyprus and Norway from the EC portal and UDI
- 8 FAQs (`fw25-1` to `fw25-8`)
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

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
ids = [p['id'] for p in C.PROVIDERS_ADD]
assert len(ids) == len(set(ids)), 'duplicate provider id'
assert len(F.FAQ_ADD) == 8
where_add = {r: list(dict.fromkeys(v)) for r, v in C.WHERE_ADD.items()}
out = {'providers_add': C.PROVIDERS_ADD, 'where_add': where_add, 'provider_update': C.PROVIDER_UPDATE,
       'abroad_update': A.ABROAD_UPDATE, 'faq_add': F.FAQ_ADD}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave25.json').write_text(text + '\n', encoding='utf-8')
print('wave25.json', len(text), 'bytes;', len(C.PROVIDERS_ADD), 'providers;', sum(len(v) for v in where_add.values()), 'route links;',
      len(A.ABROAD_UPDATE), 'abroad updates;', len(F.FAQ_ADD), 'faqs')
