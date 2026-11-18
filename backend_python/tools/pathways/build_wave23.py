"""Builds api/data/pathways/wave23.json from w23_links_verified.json (made by verify_urls.py), w23_abroad.py and w23_faq.py.

Wave 23 (adds to waves 12 to 22, no overlap):
- 35 scholarship `link` values, each opened live (HTTP 200 with a page title) by verify_urls.py; scholarships whose sites could
  not be opened from the build sandbox (s-rtp-au, s-mtcp-taylors-my, s-silk-road-uz) are left without a link on purpose
- Europe student work hours and post-study stay read on the official EC EU Immigration Portal: 10 `abroad_update` entries
  (work text, work_hours for Lithuania and Cyprus, stay_back for 8 countries; corrects the Lithuania 40 hour claim)
- 9 master level routes get PhD / MPhil `next` steps
- 14 FAQs (`fw23-1` to `fw23-14`)
Run: python3 backend_python/tools/pathways/build_wave23.py   (never hand edit wave23.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w23_abroad as A  # noqa: E402
import w23_faq as F  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
links = {k: v['url'] for k, v in json.loads((HERE / 'w23_links_verified.json').read_text(encoding='utf-8')).items()}
assert len(links) == 35, len(links)
assert all(u.startswith('https://') for u in links.values())
assert len(F.FAQ_ADD) == 14
out = {
    'scholarship_links': links,
    'abroad_update': A.ABROAD_UPDATE,
    'route_next': A.ROUTE_NEXT,
    'faq_add': F.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave23.json').write_text(text + '\n', encoding='utf-8')
print('wave23.json', len(text), 'bytes;', len(links), 'links;', len(A.ABROAD_UPDATE), 'abroad updates;', len(A.ROUTE_NEXT), 'route next;', len(F.FAQ_ADD), 'faqs')
