"""Builds api/data/pathways/wave19.json from w19_health_eng.py, w19_health_eng_seats.py, w19_exams_guides.py, w19_exams_links.py, w19_abroad_websites.py and w19_faq.py.

Wave 19 (adds to waves 12 to 18, no overlap):
- 21 new providers (9 remaining MEC 2083/84 health colleges completing 100% of the MEC 30 Ashwin 2083 seat notice + 6 IOE affiliated engineering colleges + 6 Pokhara University engineering colleges)
- route_seats for all 28 MBBS colleges (2,695 seats), 15 BDS colleges (625 seats), 9 MEC health colleges, 5 IOE constituent campuses, 10 IOE affiliated colleges (2,304 seats), KU School of Engineering and 9 Pokhara University engineering colleges
- 9 new entrance and statutory licensing exams (TU BCA, TU BIT, KUCAT-CBT, Pokhara University Bachelor/Scholarship, MECEE-PG, IOE MSc, ICAN CA, NLEV Veterinary Council, NAMC Ayurveda Council) + 19 route exam_id links + 3 career licence links + 5 step-by-step guides
- 10 new country-specific scholarships (Denmark, Austria Ernst Mach, Norway BI Presidential, Australia RTP, Canada Vanier/CGRS-D, Thailand TIPP, Lithuania KTU/VMU + State eligibility rule, Estonia Harno/TalTech + Tartu 2026/27 rule, Spain UC3M/BSE/ICFO, Portugal FCT/Aveiro/Coimbra)
- 33 live-verified official college websites + 20 FAQs (fw19-1 to fw19-20).
Run: python3 backend_python/tools/pathways/build_wave19.py   (never hand edit wave19.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w19_abroad_websites as AW  # noqa: E402
import w19_exams_guides as EG  # noqa: E402
import w19_exams_links as EL  # noqa: E402
import w19_faq as F  # noqa: E402
import w19_health_eng as HE  # noqa: E402
import w19_health_eng_seats as HES  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'

where_add = {}
for pid, rs in sorted(HES.ROUTE_SEATS.items()):
    for rid in rs:
        where_add.setdefault(rid, []).append(pid)

out = {
    'providers_add': HE.PROVIDERS_ADD,
    'where_add': where_add,
    'route_seats': HES.ROUTE_SEATS,
    'provider_note_add': HES.PROVIDER_NOTE_ADD,
    'govt_add': EG.GOVT_ADD,
    'route_exam': EL.ROUTE_EXAM,
    'career_licence': EL.CAREER_LICENCE,
    'guides_add': EL.GUIDES_ADD,
    'scholarships_add': AW.SCHOLARSHIPS_ADD,
    'abroad_note_add': AW.ABROAD_NOTE_ADD,
    'provider_websites': AW.PROVIDER_WEBSITES,
    'faq_add': F.FAQ_ADD,
}
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave19.json').write_text(text + '\n', encoding='utf-8')
print(
    'wave19.json', len(text), 'bytes;',
    len(HE.PROVIDERS_ADD), 'new providers;',
    len(HES.ROUTE_SEATS), 'providers with route_seats;',
    len(EG.GOVT_ADD), 'exams;',
    len(EL.GUIDES_ADD), 'guides;',
    len(AW.SCHOLARSHIPS_ADD), 'scholarships;',
    len(AW.PROVIDER_WEBSITES), 'websites;',
    len(F.FAQ_ADD), 'faqs',
)
