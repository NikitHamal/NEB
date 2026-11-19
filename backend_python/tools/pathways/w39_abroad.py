"""Wave 39 Germany Ausbildung (dual vocational training), the +2 route that had no row before. Read on 2026-11-19 from pages that cite Make it in Germany and the Residence Act:
studyu.org (10 Nov 2026: s.16a training visa needs a place and German B1, no age limit, allowance of EUR 1,048 gross or 822 net a month or a blocked account, 20 hours of side work, 18 months to look for work after
qualifying, s.17 search visa under 35 with EUR 1,091 a month), goausbildung.com (10 Oct 2026: legal minimum allowance EUR 724, 854, 977 in years 1 to 3, B2 for nursing, blocked account EUR 11,904 a year, visa fee EUR 75, apply
at the German Embassy in Kathmandu), acaluna.com (24 Sept 2026: no upper age limit, B1 certificate from Goethe, telc or OSD), sprachschule.org (26 Mar 2026: says under 35 and 10 hours a week of other work, which the other
three do not, so both are stated). The Make it in Germany portal itself is behind a bot wall from this server, so confirm each figure there and with the German Embassy before you pay for anything.
"""
ABROAD_NOTE_ADD = {
    'de': 'Ausbildung (paid dual vocational training, 2 to 3.5 years) is the cheapest way into Germany after +2. You need a signed training contract or school place, German at B1 (B2 for nursing and care, and many firms ask for it) and a national visa under section 16a of the Residence Act from the German Embassy in Kathmandu (fee EUR 75). Pages cited for 2026 show a legal minimum training allowance of EUR 724 in year 1, 854 in year 2 and 977 in year 3, and a living funds test of EUR 1,048 gross (822 net) a month from the allowance or else a blocked account of about EUR 11,904 a year. Three pages say there is no upper age limit for the training visa and one says under 35; the visa to search for a place (section 17) needs under 35. Side work is 20 hours a week on most pages and 10 on one. After qualifying you may stay up to 18 months to look for work.',
}
GUIDES_ADD = [
    {'id': 'ausbildung-germany', 'name': 'Ausbildung in Germany after +2', 'cat': 'Applications',
     'steps': [['Pick a trade that has a shortage (nursing and care, mechatronics, hospitality, logistics, retail) and read the allowance for it on the IHK or the Federal Employment Agency site', 7, 0, 'online'],
               ['Study German to B1 at Goethe-Institut Kathmandu or another centre, and pass an exam with all four skills (B2 for nursing and care)', 270, 0, 'in person'],
               ['Authenticate your SEE, +2 and other certificates in Nepal and have them translated for the visa file', 30, 0, 'in person'],
               ['Apply to companies and vocational schools directly, interview in German, and sign the training contract (the company usually arranges the Federal Employment Agency approval)', 90, 0, 'online'],
               ['Apply for the national visa (section 16a) at the German Embassy in Kathmandu; the fee is EUR 75, so no NPR amount is shown here, and the contract pay must reach EUR 1,048 gross a month or you need a blocked account', 30, 0, 'in person'],
               ['Fly out, register your address, take statutory health insurance through the employer and start work and vocational school; after qualifying you may stay up to 18 months to find a job', 1, 0, 'in person']],
     'docs': ['Passport', 'Signed training contract', 'German B1 certificate', 'SEE and +2 certificates with translations', 'CV in tabular form', 'Health insurance for the days before training', 'Proof of funds if the pay is below the limit', 'Biometric photos'],
     'link': 'route:foreign-lang-work'},
]
FAQ_ADD = [
    {'id': 'fw39-9', 'topic': 'abroad', 'q': 'Can I go to Germany for an Ausbildung (paid vocational training) after +2?',
     'a': 'Yes. A company or vocational school gives you a training contract, you hold German at B1 (B2 for nursing and care) and you get a section 16a national visa from the German Embassy in Kathmandu. The legal minimum training pay in 2026 is EUR 724 a month in year 1, EUR 854 in year 2 and EUR 977 in year 3, and employers often pay more. The funds test is training pay of at least EUR 1,048 gross a month, or else a blocked account of about EUR 11,904 a year. Three sources say there is no upper age limit for this visa, one says under 35, and the separate search visa needs under 35. Plan about 18 months for German, certificates, interviews and the visa, and never pay anyone for a contract.',
     'go': ['foreign-lang-work']},
    {'id': 'fw39-10', 'topic': 'abroad', 'q': 'How many hours can I work during an Ausbildung in Germany, and what happens after it?',
     'a': 'The training itself is paid work at your company plus vocational school. Most 2026 pages say you may work 20 hours a week outside the training, and one says 10, so check the visa conditions on your permit. After you qualify you may stay up to 18 months to look for a skilled job, and can then switch to a skilled worker residence permit.',
     'go': ['foreign-lang-work']},
]
