"""Builds api/data/pathways/wave20.json from w20_exams.py, w20_nepal.py, w20_scholarships.py, w20_faq.py and w20_more.py.

Wave 20 (adds to waves 12 to 19, no overlap):
- 8 new public enterprise, banking, university entrance and overseas work exams (NEA Lok Sewa `g-nea`, Nepal Telecom Lok Sewa `g-ntc`,
  Rastriya Banijya Bank `g-rbb`, Agricultural Development Bank `g-adbl`, Nepal Bank Limited `g-nbl`, TU SMSTU Actuarial/Data Science `e-smstu`,
  EPS-TOPIK Korea `l-eps`, JFT-Basic and Japan SSW `l-ssw`) + 5 route exam links (`foreign-lang-work`, `abroad-ms`, `msc-cs`, `bmath-actuarial`, `mds-data-science`)
- 4 step-by-step guides (`eps-korea-apply`, `ssw-japan-apply`, `somat-mba-apply`, `caan-cpl-licence`)
- 9 new verified providers (`p-cafodat`, `p-sirjana-arts`, `p-ncfst`, `p-lvc`, `p-nilgiri`, `p-hicast`, `p-kafcol`, `p-ncft`, `p-iec-art`),
  seat quotas & fees for BTech Food, BVSc & AH, BSc Ag, BSc Forestry, BFDM Fashion Design and SMSTU Actuarial/Data Science,
  provider links for 13 thin routes, and 13 live-verified official websites on existing providers
- 17 scholarship open windows and award counts (bringing open-window coverage to 78/80, with only the 2 closed-to-Nepal scholarships omitted)
- 25 verified FAQs (`fw20-1` to `fw20-25`).
Run: python3 backend_python/tools/pathways/build_wave20.py   (never hand edit wave20.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w20_exams as E  # noqa: E402
import w20_faq as F  # noqa: E402
import w20_more as M  # noqa: E402
import w20_nepal as N  # noqa: E402
import w20_scholarships as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

govt_all = E.GOVT_ADD + M.GOVT_MORE
providers_all = N.PROVIDERS_ADD + M.PROVIDERS_MORE
where_all = {**N.WHERE_ADD, **M.WHERE_MORE}
route_seats_all = {**N.ROUTE_SEATS, **M.ROUTE_SEATS_MORE}
route_exam_all = {**E.ROUTE_EXAM, **M.ROUTE_EXAM_MORE}
sch_extra_all = {**S.SCHOLARSHIP_EXTRA, **M.SCHOLARSHIP_EXTRA_MORE}
faq_all = F.FAQ_ADD + M.FAQ_MORE

assert len(govt_all) == 8, len(govt_all)
assert len(providers_all) == 9, len(providers_all)
assert len(faq_all) == 25, len(faq_all)

out = {
    'govt_add': govt_all,
    'route_exam': route_exam_all,
    'guides_add': E.GUIDES_ADD,
    'providers_add': providers_all,
    'where_add': where_all,
    'route_seats': route_seats_all,
    'fees': M.FEES_MORE,
    'provider_note_add': M.PROVIDER_NOTE_MORE,
    'provider_websites': N.PROVIDER_WEBSITES,
    'scholarship_extra': sch_extra_all,
    'faq_add': faq_all,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave20.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave20.json', len(text), 'bytes;',
    len(govt_all), 'exams;',
    len(E.GUIDES_ADD), 'guides;',
    len(providers_all), 'new providers;',
    len(N.PROVIDER_WEBSITES), 'websites;',
    len(sch_extra_all), 'scholarships enriched;',
    len(faq_all), 'faqs',
)
