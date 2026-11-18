"""Builds api/data/pathways/wave24.json from w24_pu.py, w24_iost.py and w24_faq.py.

Wave 24 (adds to waves 12 to 23, no overlap):
- 36 Pokhara University affiliated colleges read from the official pu.edu.np college lists (all 58 affiliated colleges and the four
  faculty lists checked against the dataset; the 22 already present were left alone), each with its PU faculty and address; 12 live
  verified college websites and the programmes those sites name
- 23 new TU IoST affiliated campuses (2 with live verified websites) and 23 existing providers linked to B.Sc. general, Microbiology, Environmental Science and
  B.Tech Food from the official iost.tu.edu.np table
- 6 new +2 schools and Caribbean College linked to +2 Science and Management, each read on its own website
- 11 FAQs (`fw24-1` to `fw24-11`)
Run: python3 backend_python/tools/pathways/build_wave24.py   (never hand edit wave24.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w24_faq as F  # noqa: E402
import w24_iost as I  # noqa: E402
import w24_plus2 as Q  # noqa: E402
import w24_pu as P  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
providers_add = P.PROVIDERS_ADD + I.PROVIDERS_ADD + Q.PROVIDERS_ADD
where_add = {}
for src in (P.WHERE_ADD, P.WHERE_EXISTING, I.WHERE_ADD, Q.WHERE_ADD):
    for rid, ids in src.items():
        where_add[rid] = list(dict.fromkeys(where_add.get(rid, []) + ids))
ids = [p['id'] for p in providers_add]
assert len(ids) == len(set(ids)), 'duplicate provider id'
assert len(F.FAQ_ADD) == 11
out = {'providers_add': providers_add, 'where_add': where_add, 'faq_add': F.FAQ_ADD}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave24.json').write_text(text + '\n', encoding='utf-8')
print('wave24.json', len(text), 'bytes;', len(providers_add), 'providers;', sum(len(v) for v in where_add.values()), 'route links;', len(F.FAQ_ADD), 'faqs')
