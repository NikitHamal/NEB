"""Builds api/data/pathways/wave18.json from w18_abroad.py, w18_exams.py, w18_nepal.py, w18_routes_a.py, w18_routes_b.py and w18_faq.py.

Wave 18 (adds to waves 12 to 17, no overlap): seven scholarships closing all remaining zero-scholarship destinations (Latvia, Bangladesh SAARC quota,
Kyrgyzstan OSCE Academy, Georgia, Philippines ADB-JSP, Cyprus, Malta), 2026 visa/funds/work notes for 15 thin destinations, six statutory Nepal professional
council licensing exams (NEC, NMCLE, NLEN, NPC, Bar Council, NHPC) + 20 career licence links + 4 guides, Lincoln School + 34 verified college websites,
100 route journey plans (bringing route plan coverage to 124/124 = 100%), and 20 FAQs.
Run: python3 backend_python/tools/pathways/build_wave18.py   (never hand edit wave18.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w18_abroad as A  # noqa: E402
import w18_exams as E  # noqa: E402
import w18_faq as F  # noqa: E402
import w18_more as M  # noqa: E402
import w18_nepal as N  # noqa: E402
import w18_routes_a as RA  # noqa: E402
import w18_routes_b as RB  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

route_plan = {**RA.ROUTE_PLAN_A, **RB.ROUTE_PLAN_B}
assert len(route_plan) == 100, len(route_plan)
govt_all = E.GOVT_ADD + M.GOVT_MORE
faq_all = F.FAQ_ADD + M.FAQ_MORE

out = {
    'scholarships_add': A.SCHOLARSHIPS_ADD,
    'abroad_update': A.ABROAD_UPDATE,
    'abroad_note_add': A.ABROAD_NOTE_ADD,
    'govt_tracks_add': E.GOVT_TRACKS_ADD,
    'govt_add': govt_all,
    'career_licence': E.CAREER_LICENCE,
    'route_exam': {**E.ROUTE_EXAM, **M.ROUTE_EXAM_MORE},
    'guides_add': E.GUIDES_ADD,
    'providers_add': N.PROVIDERS_ADD,
    'where_add': N.WHERE_ADD,
    'provider_websites': N.PROVIDER_WEBSITES,
    'route_plan': route_plan,
    'faq_add': faq_all,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave18.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave18.json', len(text), 'bytes',
    len(A.SCHOLARSHIPS_ADD), 'scholarships',
    len(govt_all), 'exams',
    len(E.GUIDES_ADD), 'guides',
    len(N.PROVIDER_WEBSITES) + len(N.PROVIDERS_ADD), 'websites',
    len(route_plan), 'route plans',
    len(faq_all), 'faqs',
)
