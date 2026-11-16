"""Wave 12, part 3: KU engineering fees, two guides (NOC for study abroad, CTEVT apply) and 14 FAQs into wave12.json.

Sources: MoEST NOC portal descriptions (noc.moest.gov.np, fee NPR 2,000, 1 to 5 working days; read on four agency and portal pages),
KU fee structure 2082/83 (EC decision 2082/02/07) and the School of Engineering admission notice of 4 Aug 2026, IOE BE/B.Arch notice 2083/84,
CTEVT notices of 2083 (classified scholarship, special scholarship, full fee selection), MBBS abroad cost guides and the NMC licensing rule.
Run: python3 backend_python/tools/pathways/w12_faq.py
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}

w['provider_fees'] = {'p-ku-eng': {'be-computer': [960000, 960000], 'be-civil': [960000, 960000], 'be-electrical': [960000, 960000],
                                   'be-mechanical': [960000, 960000], 'be-geomatics': [960000, 960000], 'barch': [1097000, 1097000]}}
w['provider_notes'] = {}
w['provider_notes']['p-ku-eng'] = (
    'BE fee for 2082/83 is NPR 9,60,000 for the four years and B.Arch NPR 10,97,000 for five, with NPR 2,21,000 (B.Arch 2,23,000) due on admission day '
    'after document verification. Entry is through KUCAT-CBT; in 2026 the offers were the School of Engineering notices of 4, 11 and 14 August, '
    'a reservation list on 18 August and an expression of interest list on 19 August (the rank list alone is not an offer).')

w['guides_add'] = [
    {'id': 'noc-study-abroad', 'name': 'No Objection Certificate (NOC) for study abroad', 'cat': 'Abroad',
     'steps': [['Get the offer or admission letter that shows programme, level and length', 0, 0, 'online'],
               ['Register on noc.moest.gov.np with your mobile number and email', 1, 0, 'online'],
               ['Fill the form and upload passport, citizenship, transcripts, offer letter and proof of funds', 1, 0, 'online'],
               ['Pay the NOC fee online', 0, 2000, 'online'],
               ['Wait for checking (1 to 5 working days, longer in peak months) and download the QR coded NOC', 5, 0, 'online']],
     'docs': ['Passport', 'Citizenship certificate', 'Offer or admission letter', 'Transcripts and certificates',
              'Bank statement or sponsor letter', 'Ward office name letter if names differ'], 'link': 'route:abroad-ms'},
    {'id': 'ctevt-apply', 'name': 'Apply for a CTEVT diploma or PCL seat', 'cat': 'Colleges',
     'steps': [['Read this year notice: full fee, classified scholarship and special scholarship are separate forms', 0, 0, 'online'],
               ['Open the ITMS online form at ctevtexam.org.np and choose one programme (scholarship forms: one programme in one province)', 1, 0, 'online'],
               ['Upload citizenship or birth registration, SEE marksheet, character certificate and a 35 by 45 mm photo', 1, 0, 'online'],
               ['Submit before the last date (2083/84 full fee and classified forms closed on Jestha 13)', 0, 0, 'online'],
               ['Sit the entrance, check your merit list, then take the recommendation to the institute', 30, 0, 'in person']],
     'docs': ['Citizenship or birth registration', 'SEE marksheet', 'Character certificate', 'Photo 35 x 45 mm',
              'Community certificate for quota seats', 'Local level letter for remote area seats'], 'link': 'route:dip-civil-eng'},
]

F = [
    ('after10', 'What is the NOC for study abroad and how do I get it?', ['abroad-ms'],
     'The No Objection Certificate (the Foreign Study Approval Letter) comes from the Ministry of Education (MoEST). Banks will not send tuition abroad and embassies often will not take your visa file without it. Apply online at noc.moest.gov.np once you hold an offer letter: upload passport, citizenship, transcripts, offer letter and proof of funds, pay NPR 2,000 and download the QR coded certificate. Checking usually takes 1 to 5 working days; allow more time in the peak months before September and January intakes. Sources differ on whether you must also visit the Sanothimi office, so read what the portal asks.'),
    ('abroad', 'Why do NOC applications get rejected?', [],
     'The usual reasons are a name that differs between citizenship, passport and offer letter (a ward office letter fixes this), blurry scans, an offer letter without programme, level and length, a duplicate application for the same intake, and an institution that is not recognised. A change of university, course or intake needs a new NOC. Check the current status for your country on the portal; South Korea D-2 and D-4 NOCs were paused in May 2025.'),
    ('after10', 'How many free CTEVT seats are there in 2083/84 and who gets them?', ['dip-civil-eng', 'dip-computer-eng'],
     'CTEVT opened 3,417 classified (free) seats in 34 programmes, split equally between a general group and target groups (women, Dalit, Janajati, Khas Arya, Madhesi, Tharu, Muslim, remote area and disability). Civil is the largest at 640, then General Medicine 446, Pharmacy 341, Agriculture Plant 261, Medical Laboratory 250, Nursing 189, Computer Engineering 187 and Animal Science 186. You need SEE from a government or community school with GPA 2.0 for health programmes or 1.6 for others, and you may apply for one programme in one province only.'),
    ('after10', 'What is the CTEVT special scholarship with NPR 3,500 a month?', [],
     'It is a separate programme of 480 free seats (457 diploma and 23 pre-diploma) for Dalit, Muslim, poor and marginalized students and for 78 local levels with no technical education nearby (17 in Koshi, 17 in Madhesh, 9 in Bagmati, 10 in Gandaki, 5 in Lumbini, 7 in Karnali, 13 in Sudurpashchim). Students get NPR 3,500 a month, NPR 1,500 a year for travel and NPR 2,500 a year for a uniform. The 2083 form was free and ran from Ashadh 4 to 18 on ctevtexam.org.np. Merit is by SEE GPA, with one extra mark for government or community school students and institutional school marks counted at 0.85.'),
    ('after10', 'Do CTEVT scholarship students pay anything, and is there a catch?', [],
     'Institutes may not charge scholarship students tuition, lab, registration, exam form, library or practical travel fees. The catch is a service promise: recipients agree to work where the government posts them for a set period. Fake documents mean cancelled registration, legal action and a 5 year ban from CTEVT exams, and a student who already got a CTEVT scholarship cannot apply again.'),
    ('after10', 'Where can I study Diploma in Computer Engineering in 2083/84?', ['dip-computer-eng'],
     'The CTEVT full fee notice lists 45 institutes, each with an approved quota of 48: Madhesh 16, Koshi 10, Lumbini 6, Karnali 5, Bagmati 4, Gandaki 3 and Sudurpashchim 1 (Sharada Secondary School, Dhangadhi). Most are school based (TECS) or private; a few are partnership or constituent. Diploma in Information Technology is listed separately, so do not treat them as one course. The form allowed one programme at one institute and closed on Jestha 13, 2083.'),
    ('after10', 'Which CTEVT institute near me has free seats for civil, pharmacy or agriculture?', ['dip-civil-eng', 'dip-pharmacy', 'dip-agriculture'],
     'Open the course in Pathways and pick your district: 48 constituent and partnership polytechnics are now listed with the free seats they hold in the special programme, for example Karnali Technical Institute in Jumla (civil 5, plant 4, animal 4, pharmacy 4, forestry 4), Seti Technical Institute in Doti, Bheri Technical Institute in Banke and Korea-Nepal Polytechnic Institute in Rupandehi. Seats can shrink if a full fee programme does not run, so confirm with the CTEVT provincial office.'),
    ('after12', 'When was the IOE entrance for 2083/84 and how big is it?', ['be-civil', 'be-computer'],
     'IOE took forms from Ashadh 23 to Shrawan 1, 2083 (7 to 17 July 2026) at entrance.ioe.edu.np with a fee of NPR 2,500 (one page says 2,000, so check the notice). The test is computer based: 2 hours, 100 objective questions, from Shrawan 11 (26 July 2026). In 2025 the five constituent campuses had 2,040 BE and B.Arch seats and ten affiliated colleges 2,304, 4,344 in all.'),
    ('after12', 'How much does a BE at Kathmandu University cost?', ['be-computer', 'barch'],
     'KU fixed NPR 9,60,000 for the whole four year BE and NPR 10,97,000 for five year B.Arch for 2082/83. On admission day, after your documents are verified, you pay NPR 2,21,000 (B.Arch 2,23,000). Entry is through KUCAT-CBT; in 2026 the rank list was not an offer, the School of Engineering notices of 4, 11 and 14 August were, followed by a reservation list on 18 August and an expression of interest list on 19 August.'),
    ('abroad', 'Is studying in the Czech Republic really free?', [],
     'Only if you study in Czech at a public university: that is free for every nationality, usually after a one year language course. English taught programmes cost CZK 100,000 to 400,000 a year (about NPR 6 to 24 lakh) and medicine about EUR 12,000 to 15,000. Living costs CZK 15,000 to 25,000 a month. The visa fee is CZK 2,500, you must show funds of about CZK 124,500 for the year, and Nepali applicants book at the Czech Embassy in New Delhi.'),
    ('abroad', 'Can Nepali students use the Czech Government scholarship?', [],
     'Not in the 2027-28 call as far as the lists read show. The scholarship (CZK 16,000 a month for a master, CZK 24,960 for a PhD) is limited to named countries such as Bangladesh, Georgia, Ukraine and Cambodia, and the call ran from 21 August to 30 September 2026. Nepal can be added in later years, so check the call each August before you prepare.'),
    ('abroad', 'What do MBBS in Georgia and Bangladesh cost for Nepali students?', ['mbbs'],
     'Georgia: about USD 4,000 to 8,000 tuition a year (NPR 5.5 to 11 lakh) for a six year MD, plus hostel and living of roughly NPR 3.5 to 6.5 lakh a year. Bangladesh: about NPR 40 to 70 lakh in all for a private MBBS (five years plus an internship), with fewer, cheaper government seats under the SAARC quota. Both ranges are approximate. In either country the college must be recognised by the Nepal Medical Council, and you must pass the NMC licensing examination (NMCLE) to practise at home, so get recognition in writing first.'),
    ('general', 'Which free diploma route leads to a bachelor degree?', ['dip-civil-eng', 'be-civil'],
     'A CTEVT diploma in civil or computer engineering takes 3 years after SEE and can lead to a BE through lateral entry, to a BIT or BCA, or straight to a sub-engineer or technician job. Because 3,417 seats are free in 2083/84, check the scholarship forms first and keep the full fee form as a back up.'),
]
w['faq_add'] = [{'id': f'fw12-{i}', 'topic': t, 'q': q, 'go': g, 'a': a} for i, (t, q, g, a) in enumerate(F, 1)]

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(w['faq_add']), 'faqs', len(w['guides_add']), 'guides')
