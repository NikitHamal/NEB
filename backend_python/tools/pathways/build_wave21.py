"""Builds api/data/pathways/wave21.json from w21_exams_more.py, w21_guides_links.py, w21_nepal.py, w21_scholarships.py and w21_faq.py.

Wave 21 (adds to waves 12 to 20, no overlap):
- 12 new verified exams (CIT `g-cit`, SSF `g-ssf`, EPF `g-epf`, CAAN `g-caan`, Judicial Service `g-judicial`,
  Audit/Parliament `g-parliament-audit`, TU IOST BSc/BTech Food `e-tu-bachelor-sci`, TU IOST MSc `e-tu-msc-iost`,
  TU FoHSS Bachelor `e-fohss-bachelor`, TU Master/Postgraduate `e-fohss-master`, Purbanchal University `e-purbanchal`, ACCA `e-acca`)
- 24 route exam_id links, 1 career licence link (`actuary-risk-analyst`), and 6 step by step guides (`adbl-nbl-bank-apply`,
  `judicial-service-apply`, `acca-nepal-register`, `nhpc-licence-apply`, `npc-pharmacy-licence`, `nvc-vet-licence`)
- 9 new verified Nepal institutions (`p-ist-college`, `p-gate-college`, `p-silver-mountain`, `p-mid-valley`, `p-sasthm`,
  `p-cobeas`, `p-valmiki`, `p-samv-bhaktapur`, `p-nps-sanga`), 26 thin-route expansions, seat quotas, and 15 live-verified official websites
- 8 new country-specific international scholarships (`s-nl-maastricht-delft`, `s-polimi-unibo-it`, `s-taiwan-icdf`, `s-eth-esop-ch`,
  `s-auckland-otago-nz`, `s-ucd-tcd-ie`, `s-hk-belt-road`, `s-kaist-ust-kr`) and 20 scholarships enriched with award counts
- 22 verified FAQs (`fw21-1` to `fw21-22`).
Run: python3 backend_python/tools/pathways/build_wave21.py   (never hand edit wave21.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w21_exams_more as E  # noqa: E402
import w21_faq as F  # noqa: E402
import w21_guides_links as G  # noqa: E402
import w21_more as M  # noqa: E402
import w21_nepal as N  # noqa: E402
import w21_scholarships as S  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

govt_add = E.GOVT_ADD + M.GOVT_MORE
scholarships_add = S.SCHOLARSHIPS_ADD + M.SCHOLARSHIPS_MORE
scholarship_extra = {**S.SCHOLARSHIP_EXTRA, **M.SCHOLARSHIP_EXTRA_MORE}
route_seats = {**N.ROUTE_SEATS, **M.ROUTE_SEATS_MORE}
faq_add = F.FAQ_ADD + M.FAQ_MORE

assert len(govt_add) == 15, len(govt_add)
assert len(G.GUIDES_ADD) == 6, len(G.GUIDES_ADD)
assert len(N.PROVIDERS_ADD) == 9, len(N.PROVIDERS_ADD)
assert len(scholarships_add) == 16, len(scholarships_add)
assert len(faq_add) == 30, len(faq_add)

out = {
    'govt_add': govt_add,
    'route_exam': G.ROUTE_EXAM,
    'career_licence': G.CAREER_LICENCE,
    'guides_add': G.GUIDES_ADD,
    'providers_add': N.PROVIDERS_ADD,
    'where_add': N.WHERE_ADD,
    'route_seats': route_seats,
    'fees': M.FEES_MORE,
    'provider_note_add': M.PROVIDER_NOTE_MORE,
    'provider_websites': N.PROVIDER_WEBSITES,
    'scholarships_add': scholarships_add,
    'scholarship_extra': scholarship_extra,
    'faq_add': faq_add,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave21.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave21.json', len(text), 'bytes;',
    len(govt_add), 'exams;',
    len(G.GUIDES_ADD), 'guides;',
    len(N.PROVIDERS_ADD), 'new providers;',
    len(N.PROVIDER_WEBSITES), 'websites;',
    len(scholarships_add), 'new scholarships;',
    len(scholarship_extra), 'scholarships enriched;',
    len(faq_add), 'faqs',
)
