"""Builds api/data/pathways/wave22.json from w22_exams_a.py, w22_exams_b.py, w22_guides_links.py, w22_nepal.py, w22_scholarships.py,
w22_faq.py, w22_more_a.py, w22_more_b.py and w22_more_faq.py.

Wave 22 (adds to waves 12 to 21, no overlap):
- 17 new verified exams (SEE `e-see`, NEB +2 `e-neb-plus2`, Cambridge A Level / IB `e-cambridge-ib`, TU FoM BBS `e-tu-fom-bbs`,
  TU FoE BEd/MEd `e-tu-foe-bed`, NSTB Skill Test `e-nstb-skill`, Sainik/Police/Budhanilkantha School `e-sainik-police-school`,
  Nepal Airlines `g-nac`, Nepal Insurance Authority & SEBON `g-beema-sebon`, Lok Sewa Foreign Service `g-foreign-service`,
  Lok Sewa Revenue Service `g-revenue-service`, CFA `l-cfa`, Lok Sewa Sub-Engineer `g-sub-engineer`, Lok Sewa JT/JTA `g-jt-jta`,
  Lok Sewa Ranger & Ban Rakshak `g-forest-ranger`, Provincial Universities `e-provincial-uni`, Japanese NAT-TEST `l-nat`)
- 52 existing exams enriched via `govt_update` so 100% of all 91 exams have verified `fee`, `apply` window and `exam_month`
- 17 route `exam_id` links (bringing route `exam_id` coverage to 123/124), 2 career `licence` links (`electrician`, `bank-officer`),
  and 6 step-by-step guides (`nstb-skill-test`, `cfa-nepal-register`, `camb-alevel-nepal`, `sainik-school-apply`, `nea-ntc-apply`, `foreign-revenue-psc`)
- 47 new verified Nepal institutions (expanding all 27 single-provider districts so 100% of all 77 districts have >= 2 providers,
  plus TU FoE constituent campuses, CTEVT polytechnics and provincial universities LTU Banke & MAU Saptari),
  route expansions, seat quotas, fees, and 30 live-verified official HTTPS websites
- 12 new international scholarships (closing all 8 single-scholarship countries so 100% of all 46 destinations have >= 2 scholarships)
  and 30 scholarships enriched with numerical `awards` counts (100% coverage across all 108 scholarships)
- 40 verified FAQs (`fw22-1` to `fw22-40`).
Run: python3 backend_python/tools/pathways/build_wave22.py   (never hand edit wave22.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w22_exams_b as E  # noqa: E402
import w22_faq as F  # noqa: E402
import w22_guides_links as G  # noqa: E402
import w22_more_a as MA  # noqa: E402
import w22_more_b as MB  # noqa: E402
import w22_more_faq as MF  # noqa: E402
import w22_nepal as N  # noqa: E402
import w22_scholarships as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

govt_add = E.GOVT_ADD + MB.GOVT_MORE
providers_add = N.PROVIDERS_ADD + MA.PROVIDERS_MORE
where_add = dict(N.WHERE_ADD)
for rid, more in MB.WHERE_MORE.items():
    where_add[rid] = list(dict.fromkeys(where_add.get(rid, []) + more))
route_seats = {**N.ROUTE_SEATS, **MB.ROUTE_SEATS_MORE}
provider_websites = {**N.PROVIDER_WEBSITES, **MB.WEBSITES_MORE}
faq_add = F.FAQ_ADD + MF.FAQ_MORE

assert len(govt_add) == 17, len(govt_add)
assert len(G.GUIDES_ADD) == 6, len(G.GUIDES_ADD)
assert len(providers_add) == 47, len(providers_add)
assert len(S.SCHOLARSHIPS_ADD) == 12, len(S.SCHOLARSHIPS_ADD)
assert len(faq_add) == 40, len(faq_add)

out = {
    'govt_add': govt_add,
    'govt_update': E.GOVT_UPDATE,
    'route_exam': G.ROUTE_EXAM,
    'career_licence': G.CAREER_LICENCE,
    'guides_add': G.GUIDES_ADD,
    'providers_add': providers_add,
    'where_add': where_add,
    'route_seats': route_seats,
    'fees': N.FEES,
    'provider_websites': provider_websites,
    'websites_replace': MB.WEBSITES_REPLACE,
    'scholarships_add': S.SCHOLARSHIPS_ADD,
    'scholarship_extra': S.SCHOLARSHIP_EXTRA,
    'faq_add': faq_add,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave22.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave22.json', len(text), 'bytes;',
    len(govt_add), 'new exams;',
    len(E.GOVT_UPDATE), 'exams updated;',
    len(G.GUIDES_ADD), 'guides;',
    len(providers_add), 'new providers;',
    len(provider_websites) + len(MB.WEBSITES_REPLACE), 'websites;',
    len(S.SCHOLARSHIPS_ADD), 'new scholarships;',
    len(S.SCHOLARSHIP_EXTRA), 'scholarships enriched;',
    len(faq_add), 'faqs',
)
