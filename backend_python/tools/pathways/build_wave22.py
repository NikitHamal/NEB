"""Builds api/data/pathways/wave22.json from w22_exams_a.py, w22_exams_b.py, w22_guides_links.py, w22_nepal.py, w22_scholarships.py and w22_faq.py.

Wave 22 (adds to waves 12 to 21, no overlap):
- 12 new verified exams (SEE `e-see`, NEB +2 `e-neb-plus2`, Cambridge A Level / IB `e-cambridge-ib`, TU FoM BBS `e-tu-fom-bbs`,
  TU FoE BEd/MEd `e-tu-foe-bed`, NSTB Skill Test `e-nstb-skill`, Sainik/Police/Budhanilkantha School `e-sainik-police-school`,
  Nepal Airlines `g-nac`, Nepal Insurance Authority & SEBON `g-beema-sebon`, Lok Sewa Foreign Service `g-foreign-service`,
  Lok Sewa Revenue Service `g-revenue-service`, CFA `l-cfa`)
- 52 existing exams enriched via `govt_update` so 100% of all 86 exams have verified `fee`, `apply` window and `exam_month`
- 17 route `exam_id` links (bringing route `exam_id` coverage to 123/124), 2 career `licence` links (`electrician`, `investment-analyst`),
  and 6 step-by-step guides (`nstb-skill-test`, `cfa-nepal-register`, `camb-alevel-nepal`, `sainik-school-apply`, `nea-ntc-apply`, `foreign-revenue-psc`)
- 12 new verified Nepal institutions (`p-mrc-tahachal`, `p-sanothimi-campus`, `p-cde-tu`, `p-dhawalagiri-mc`, `p-dadeldhura-mc`,
  `p-jumla-mc`, `p-myagdi-mc`, `p-dhaulagiri-pi`, `p-mahuregadhi-pi`, `p-rolpa-pi`, `p-bharatpur-pi`, `p-annapurna-pi`),
  28 thin-route expansions, seat quotas, fees, and 24 live-verified official HTTPS websites
- 12 new international scholarships (closing all 8 single-scholarship countries so 100% of all 46 destinations have >= 2 scholarships)
  and 28 scholarships enriched with numerical `awards` counts
- 30 verified FAQs (`fw22-1` to `fw22-30`).
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
import w22_nepal as N  # noqa: E402
import w22_scholarships as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

assert len(E.GOVT_ADD) == 12, len(E.GOVT_ADD)
assert len(G.GUIDES_ADD) == 6, len(G.GUIDES_ADD)
assert len(N.PROVIDERS_ADD) == 12, len(N.PROVIDERS_ADD)
assert len(S.SCHOLARSHIPS_ADD) == 12, len(S.SCHOLARSHIPS_ADD)
assert len(F.FAQ_ADD) == 30, len(F.FAQ_ADD)

out = {
    'govt_add': E.GOVT_ADD,
    'govt_update': E.GOVT_UPDATE,
    'route_exam': G.ROUTE_EXAM,
    'career_licence': G.CAREER_LICENCE,
    'guides_add': G.GUIDES_ADD,
    'providers_add': N.PROVIDERS_ADD,
    'where_add': N.WHERE_ADD,
    'route_seats': N.ROUTE_SEATS,
    'fees': N.FEES,
    'provider_websites': N.PROVIDER_WEBSITES,
    'scholarships_add': S.SCHOLARSHIPS_ADD,
    'scholarship_extra': S.SCHOLARSHIP_EXTRA,
    'faq_add': F.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave22.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave22.json', len(text), 'bytes;',
    len(E.GOVT_ADD), 'new exams;',
    len(E.GOVT_UPDATE), 'exams updated;',
    len(G.GUIDES_ADD), 'guides;',
    len(N.PROVIDERS_ADD), 'new providers;',
    len(N.PROVIDER_WEBSITES), 'websites;',
    len(S.SCHOLARSHIPS_ADD), 'new scholarships;',
    len(S.SCHOLARSHIP_EXTRA), 'scholarships enriched;',
    len(F.FAQ_ADD), 'faqs',
)
