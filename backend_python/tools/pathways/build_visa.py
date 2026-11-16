#!/usr/bin/env python3
"""Writes api/data/pathways/visa.json: the student visa steps shown under every country in Study > Abroad.

A step is [name, days, cost, mode, note]: days is the usual wait or effort, cost is text in the currency the
embassy charges (empty when free or unknown), mode is "online", "in person" or "" and note is one short line.
Fees move every year, so the screen says "check the embassy page". Countries without their own list use DEFAULT.
Run: python3 tools/pathways/build_visa.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'api' / 'data' / 'pathways' / 'visa.json'

NOC = ['Get the NOC', 5, 'NPR 2,000', 'online', 'MoEST No Objection Certificate, needed to study abroad on a visa']

DEFAULT = {
    'name': 'Student visa',
    'steps': [
        ['Accept the offer', 7, '', 'online', 'Pay the deposit if the university asks'],
        NOC,
        ['Show your funds', 21, '', 'in person', 'Bank letter and statement for the amount the embassy states'],
        ['Medical check', 3, '', 'in person', 'Only where the embassy asks, at an approved clinic'],
        ['Lodge the visa', 1, '', 'online', 'Form, passport, offer, funds and the NOC'],
        ['Biometrics or interview', 2, '', 'in person', 'Fingerprints and photo, sometimes a short interview'],
        ['Decision', 30, '', '', 'Track the application; do not book flights before the visa is stamped'],
    ],
}

VISA = {
    'au': ('Student visa (subclass 500)', [
        ['Accept the offer and pay the deposit', 7, '', 'online', 'You receive the Confirmation of Enrolment (CoE)'],
        ['Buy overseas student health cover', 1, '', 'online', 'OSHC for the whole visa'],
        NOC,
        ['Write the Genuine Student statement', 5, '', 'online', 'Your study plan and why this course, in your own words'],
        ['Lodge in ImmiAccount', 1, 'AUD 2,000', 'online', 'Upload passport, CoE, funds and test score'],
        ['Health exam and biometrics', 7, '', 'in person', 'Panel doctor and the visa application centre in Kathmandu'],
        ['Decision', 35, '', '', 'Usually four to six weeks'],
    ]),
    'us': ('F-1 student visa', [
        ['Receive the I-20', 14, '', 'online', 'The school issues it after admission and a funds check'],
        ['Pay the SEVIS fee', 1, 'USD 350', 'online', 'I-901, keep the receipt'],
        ['Fill in the DS-160', 1, '', 'online', 'Print the confirmation page'],
        ['Pay the visa fee', 1, 'USD 185', 'online', 'Then book the interview slot'],
        ['Interview at the embassy', 1, '', 'in person', 'US Embassy, Kathmandu. Bring I-20, funds, transcripts and test scores'],
        ['Decision and passport', 7, '', '', 'Some cases go to extra checks, which can take weeks'],
    ]),
    'uk': ('Student visa', [
        ['Receive the CAS', 10, '', 'online', 'Confirmation of Acceptance for Studies from the university'],
        ['Arrange funds for 28 days', 28, '', 'in person', 'Keep the money in your account for a full month'],
        ['TB test', 3, '', 'in person', 'Required for Nepal, at an approved clinic in Kathmandu'],
        ['Apply online and pay', 1, 'GBP 524 + health surcharge', 'online', 'Surcharge is paid per year of stay'],
        ['Biometrics', 2, '', 'in person', 'Visa application centre, or the app where offered'],
        ['Decision', 21, '', '', 'About three weeks from biometrics'],
    ]),
    'ca': ('Study permit', [
        ['Get the acceptance letter', 14, '', 'online', 'From a designated learning institution'],
        ['Get the provincial attestation letter', 14, '', 'online', 'Needed for most programmes; the school helps'],
        ['Buy the GIC and pay tuition', 7, 'CAD 22,895 funds', 'online', 'Proof of funds for living, plus the first year tuition'],
        NOC,
        ['Medical exam', 5, '', 'in person', 'IRCC panel physician'],
        ['Apply online and pay', 1, 'CAD 150', 'online', 'Include your study plan'],
        ['Biometrics', 5, 'CAD 85', 'in person', 'Visa application centre, Kathmandu'],
        ['Decision', 45, '', '', 'Processing time changes often, check the IRCC page'],
    ]),
    'de': ('National student visa', [
        ['Get the admission letter', 30, '', 'online', 'Through uni-assist or the university'],
        ['Open a blocked account', 7, 'EUR 11,904 a year', 'online', 'The monthly amount is released after arrival'],
        ['Buy health insurance', 2, '', 'online', 'German cover for the visa'],
        ['Verify your documents', 10, '', 'in person', 'Degree and transcripts as the embassy asks'],
        ['Book the embassy slot', 14, '', 'online', 'German Embassy, Kathmandu. Book early, slots fill'],
        ['Submit and interview', 1, 'EUR 75', 'in person', 'Bring the originals and copies'],
        ['Decision', 60, '', '', 'Six to twelve weeks is normal'],
    ]),
    'jp': ('Student visa', [
        ['Get the offer from the school', 30, '', 'online', 'Language school or university'],
        ['School applies for your COE', 60, '', '', 'Certificate of Eligibility from Japan Immigration'],
        ['Receive the COE', 2, '', 'online', 'Scan or original, as the school says'],
        NOC,
        ['Apply at the embassy', 1, '', 'in person', 'Embassy of Japan, Kathmandu. Passport, COE, photo, form'],
        ['Decision', 7, '', '', 'Usually about five working days after a valid COE'],
    ]),
    'kr': ('D-2 or D-4 student visa', [
        ['Get the admission letter', 30, '', 'online', 'Apply through the university'],
        ['Receive the visa issuance number', 14, '', 'online', 'The university requests it from Korean immigration'],
        ['Show your funds', 14, '', 'in person', 'Bank statement for the amount the university states'],
        NOC,
        ['Apply at the embassy', 1, '', 'in person', 'Embassy of Korea, Kathmandu'],
        ['Decision', 14, '', '', 'Then register as a foreign resident within 90 days'],
    ]),
    'cn': ('X1 student visa', [
        ['Get the admission notice', 30, '', 'online', 'With the JW201 or JW202 form'],
        ['Physical examination form', 3, '', 'in person', 'Foreigner Physical Examination Form at an approved hospital'],
        ['Apply at the visa centre', 1, '', 'in person', 'Chinese visa application centre, Kathmandu'],
        ['Collect the passport', 7, '', 'in person', 'Check the entry deadline printed on the visa'],
        ['Residence permit after arrival', 30, '', 'in person', 'Apply within 30 days of landing'],
    ]),
    'in': ('No visa for Nepali citizens', [
        ['Apply to the university or take the test', 30, '', 'online', 'JEE, NEET or the university test'],
        ['Check equivalence of your +2', 7, '', 'online', 'Needed for some universities'],
        ['Pay the seat fee', 3, '', 'online', 'Keep the receipt and allotment letter'],
        ['Travel with your citizenship or passport', 1, '', 'in person', 'The open border means no student visa'],
        ['Register at the university', 3, '', 'in person', 'Bring the original certificates'],
    ]),
    'nz': ('Student visa', [
        ['Accept the offer of place', 7, '', 'online', 'Pay the first fee if asked'],
        ['Show funds for the year', 21, 'NZD 20,000 a year', 'in person', 'Bank statement or a sponsor'],
        NOC,
        ['Medical and police certificates', 14, '', 'in person', 'Only when the course is long enough to ask'],
        ['Apply online and pay', 1, 'NZD 375', 'online', 'Immigration New Zealand account'],
        ['Decision', 30, '', '', 'Usually four to eight weeks'],
    ]),
    'nl': ('Residence permit for study', [
        ['Get the admission letter', 30, '', 'online', 'Through Studielink'],
        ['Pay the tuition deposit and show funds', 14, '', 'in person', 'The monthly amount is set each year by DUO'],
        ['University applies for your permit', 30, '', '', 'The school files with the IND for you'],
        ['Collect the MVV entry visa', 5, '', 'in person', 'At the Dutch representation named in the letter'],
        ['Collect the residence card after arrival', 14, '', 'in person', 'Biometrics at the IND desk'],
    ]),
    'fi': ('Residence permit for studies', [
        ['Get the study place', 30, '', 'online', 'Through Studyinfo'],
        ['Show your funds', 14, 'EUR 800 a month', 'in person', 'Bank statement for the whole year'],
        ['Apply in Enter Finland', 1, 'EUR 350 online', 'online', 'Upload passport, offer and funds'],
        ['Visit the embassy to confirm identity', 7, '', 'in person', 'Embassy of Finland, Kathmandu'],
        ['Decision', 45, '', '', 'Then collect the card in Finland'],
    ]),
    'ie': ('Study visa', [
        ['Accept the offer and pay the fee', 7, '', 'online', 'Get the acceptance letter'],
        ['Show funds', 21, '', 'in person', 'Bank statement for the year plus fees'],
        ['Apply on the AVATS portal', 1, '', 'online', 'Upload documents and the offer'],
        ['Biometrics', 3, '', 'in person', 'Visa application centre'],
        ['Decision', 30, '', '', 'Register for the residence permit after arrival'],
    ]),
    'sg': ('Student pass', [
        ['Get the offer from the institution', 30, '', 'online', 'Approved private or public institution'],
        ['Institution applies on SOLAR', 14, '', '', 'You complete the form online'],
        ['In-principle approval letter', 7, '', 'online', 'Needed to enter Singapore'],
        ['Medical check', 3, '', 'in person', 'Done after arrival at a listed clinic'],
        ['Collect the pass', 7, '', 'in person', 'Within the days stated in the letter'],
    ]),
    'my': ('Student pass', [
        ['Get the offer letter', 14, '', 'online', 'Through a registered institution'],
        ['University applies for the visa approval letter', 21, '', '', 'EMGS processes it'],
        ['Medical check', 3, '', 'in person', 'At an approved clinic in Nepal'],
        ['Collect the visa reference letter', 2, '', 'online', 'Needed to board the flight'],
        ['Stamp the visa at the airport', 1, '', 'in person', 'Then complete the pass formalities at the university'],
    ]),
    'fr': ('Long stay student visa', [
        ['Apply on Etudes en France', 30, '', 'online', 'Interview with Campus France, Kathmandu'],
        ['Get the admission letter', 30, '', 'online', 'Through the French university'],
        ['Show funds', 14, 'EUR 615 a month', 'in person', 'Bank proof or scholarship letter'],
        ['Apply for the visa', 1, '', 'in person', 'Visa centre or embassy named by the Campus France account'],
        ['Decision', 30, '', '', 'Then validate the visa online after arrival'],
    ]),
    'pl': ('National student visa', [
        ['Get the admission letter', 30, '', 'online', 'From the Polish university'],
        ['Buy health insurance', 2, '', 'online', 'Valid for the first year'],
        ['Show funds', 14, '', 'in person', 'Bank statement for the amount stated by the embassy'],
        ['Book and attend the embassy appointment', 30, '', 'in person', 'Embassy or visa centre, with all originals'],
        ['Decision', 30, '', '', 'Then apply for the residence card in Poland'],
    ]),
}


def main():
    data = {'default': {'name': DEFAULT['name'], 'steps': DEFAULT['steps']},
            'visa': {k: {'name': n, 'steps': s} for k, (n, s) in VISA.items()}}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(OUT, len(VISA), 'countries')


if __name__ == '__main__':
    main()
