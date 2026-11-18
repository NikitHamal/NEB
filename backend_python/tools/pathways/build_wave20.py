"""Builds api/data/pathways/wave20.json from w20_exams.py, w20_nepal.py, w20_scholarships.py and w20_faq.py.

Wave 20 (adds to waves 12 to 19, no overlap):
- 5 new public enterprise, banking and overseas work exams (NEA Lok Sewa `g-nea`, Nepal Telecom Lok Sewa `g-ntc`, Rastriya Banijya Bank `g-rbb`,
  EPS-TOPIK Korea `l-eps`, JFT-Basic and Japan SSW `l-ssw`) + 3 route exam links (`foreign-lang-work`, `abroad-ms`, `msc-cs`)
- 4 step-by-step guides (`eps-korea-apply`, `ssw-japan-apply`, `somat-mba-apply`, `caan-cpl-licence`)
- 5 new verified providers (`p-cafodat`, `p-sirjana-arts`, `p-ncfst`, `p-lvc`, `p-nilgiri`), BTech Food seat quotas across 9 colleges,
  provider links for 8 thin routes (`btech-food`, `bfa`, `mpharm`, `msw`, `mca`, `ca-route`, `plus2-education`, `bjmc`), and 13 live-verified official websites
- 16 scholarship open windows and award counts (`s-singa`, `s-sisgp`, `s-vliruos`, `s-jds-japan`, `s-ugc`, `s-ugc-qaa-need`, `s-iccr`, `s-italy`,
  `s-rhodes`, `s-clarendon`, `s-adb-jsp`, `s-koica`, `s-ioe-regular`, `s-pu-scholarship`, `s-ku-scholarship`, `s-new-uz`)
- 18 verified FAQs (`fw20-1` to `fw20-18`).
Run: python3 backend_python/tools/pathways/build_wave20.py   (never hand edit wave20.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w20_exams as E  # noqa: E402
import w20_faq as F  # noqa: E402
import w20_nepal as N  # noqa: E402
import w20_scholarships as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

assert len(E.GOVT_ADD) == 5, len(E.GOVT_ADD)
assert len(F.FAQ_ADD) == 18, len(F.FAQ_ADD)

out = {
    'govt_add': E.GOVT_ADD,
    'route_exam': E.ROUTE_EXAM,
    'guides_add': E.GUIDES_ADD,
    'providers_add': N.PROVIDERS_ADD,
    'where_add': N.WHERE_ADD,
    'route_seats': N.ROUTE_SEATS,
    'provider_websites': N.PROVIDER_WEBSITES,
    'scholarship_extra': S.SCHOLARSHIP_EXTRA,
    'faq_add': F.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave20.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave20.json', len(text), 'bytes;',
    len(E.GOVT_ADD), 'exams;',
    len(E.GUIDES_ADD), 'guides;',
    len(N.PROVIDERS_ADD), 'new providers;',
    len(N.PROVIDER_WEBSITES), 'websites;',
    len(S.SCHOLARSHIP_EXTRA), 'scholarships enriched;',
    len(F.FAQ_ADD), 'faqs',
)
