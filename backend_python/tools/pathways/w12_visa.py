"""Wave 12, part 6: 2026 student visa facts for Australia, Canada, the UK and the USA.

Keys owned in wave12.json: abroad_update, faq_visa.
Sources (read July to October 2026): Australia Home Affairs fee change from 1 July 2026 (subclass 500 AUD 2,500, ELICOS and non award AUD 2,050,
regulation F2026L00874) and the AUD 29,710 living funds figure; IRCC 2026 levels (408,000 study permits: 155,000 new, 253,000 extensions), Student Direct
Stream closed, GIC about CAD 22,895; GOV.UK Student visa fee GBP 558 from 8 April 2026 and the Graduate Route cut to 18 months for applications from
1 January 2027 (PhD stays 3 years); DHS final rule ending duration of status for F-1 from 15 September 2026 (admission up to 4 years, extension through USCIS).
Run: python3 backend_python/tools/pathways/w12_visa.py
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}

w['abroad_update'] = {
    'au': {'note': ('Student visa (subclass 500) charge is AUD 2,500 from 1 July 2026 (AUD 2,050 for English courses and non award study), non refundable. '
                    'You must show AUD 29,710 a year for living on top of tuition, travel and OSHC health cover, and write a Genuine Student statement '
                    '(it replaced the Genuine Temporary Entrant test). The post study visa (485) fee also rose on 1 July 2026. Check homeaffairs.gov.au before paying any agent.')},
    'ca': {'note': ('Canada plans up to 408,000 study permits for 2026 (155,000 for new students, 253,000 for extensions and returning students). '
                    'The fast track Student Direct Stream is closed, so every file takes the standard route (about 7 to 12 weeks). Show a GIC of about CAD 22,895 plus first-year tuition. '
                    'Most undergraduate applicants need a provincial attestation letter; master and doctoral students at public universities are exempt. Verify on canada.ca.')},
    'uk': {'note': ('The Student visa fee is GBP 558 from 8 April 2026. The Graduate Route falls from 2 years to 18 months for applications made from 1 January 2027 '
                    '(PhD graduates keep 3 years), so plan on the rule in force when you graduate. One year master degrees save time and money.')},
    'us': {'note': ('From 15 September 2026 F-1 students are admitted for the length of the programme up to 4 years instead of "duration of status" and must file for an '
                    'extension of stay with USCIS to stay longer. OPT (1 year, 3 for STEM) still applies. Assistantships can cover tuition for master and PhD students in science and engineering.')},
}

w['faq_visa'] = [{
    'id': 'fw12-v1', 'topic': 'abroad', 'q': 'What changed in student visa rules for 2026?', 'go': ['abroad-ms'],
    'a': ('Australia: visa charge AUD 2,500 from 1 July 2026 and AUD 29,710 living funds, with a Genuine Student statement. Canada: 408,000 study permits in 2026, no Student Direct '
          'Stream, GIC about CAD 22,895. UK: Student visa fee GBP 558 from 8 April 2026 and a Graduate Route of 18 months for applications from 1 January 2027 '
          '(2 years before that, 3 for PhD). USA: from 15 September 2026 a fixed admission period of up to 4 years replaces duration of status. '
          'These rules change several times a year, so read the official immigration page of the country on the day you apply.')}]

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(w['abroad_update']), len(w['faq_visa']))
