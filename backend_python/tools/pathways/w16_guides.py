"""Wave 16 guides: education loan from a Nepali bank and the police clearance certificate, with three FAQs. Plain sentences, no dashes.

Sources (read 16 November 2026): interestrateinnepal.com (May 2026 table of education loan rates by bank: Krishi Bikas 5.40 to 7.40 percent, RBB 5.56 to 6.56, Siddhartha 5.86 to 9.11 and so on, floating);
houseofadmissions.com (July 2026: RBB floating 5.97 percent, up to NPR 80 lakh, 12 month moratorium after the course, 15 year tenure, collateral above NPR 7.5 lakh, fixed rates near 10 percent);
saralbankingsewa.com (processing fee 0.75 percent and fixed rates near 10 percent, dated Baisakh 2082); thenext.edu.np (August 2026: land or fixed deposit collateral, document list, loan letter accepted as proof of funds by most destinations);
studyabroadfromnepal.com, nexusadvisory.com.np and pricenepal.com (police clearance: free at opcr.nepalpolice.gov.np or the Nagarik App, 2 to 3 working days, attestation about NPR 500).
Rates are bank by bank and change monthly, so every line says to read the bank's own page.
"""

GUIDES_ADD = [
    {'id': 'education-loan', 'name': 'Education loan from a Nepali bank (study abroad)', 'cat': 'Abroad',
     'steps': [
         ['Get the offer or admission letter and a written cost sheet from the university: tuition, living and travel', 0, 0, 'online'],
         ['Compare banks on the floating rate, fixed rate, processing fee and the moratorium. 2026 comparison pages show floating rates from about 5.4 to 11 percent and fixed rates near 10 percent; the bank\'s own page is the final word', 2, 0, 'online'],
         ['Prepare the collateral: land ownership certificate (Lalpurja) or a fixed deposit, a valuation report, tax clearance and the guarantor\'s income papers. One guide says loans above NPR 7.5 lakh need collateral', 14, 0, 'in person'],
         ['Submit the file with citizenship, passport, transcripts, the cost sheet and the NOC if you have one', 1, 0, 'in person'],
         ['Collect the sanction letter, which most destinations accept as proof of funds, and ask the bank to pay the university or a visa approved account (timing differs by bank)', 14, 0, 'in person'],
     ],
     'docs': ['Offer or admission letter', 'Citizenship (you and the collateral owner)', 'Passport', 'Transcripts from SEE onwards', 'Land ownership certificate or fixed deposit receipt', 'Valuation report and tax clearance', 'Guarantor income proof', 'NOC from the Ministry of Education if issued'],
     'link': 'guide:noc-study-abroad'},
    {'id': 'police-clearance', 'name': 'Police clearance certificate for a visa', 'cat': 'Documents',
     'steps': [
         ['Create an account at opcr.nepalpolice.gov.np, or open the Nagarik App and choose the police clearance service', 0, 0, 'online'],
         ['Fill in your details, pick the purpose (student visa), upload your citizenship and a photo, and submit; the application is free', 0, 0, 'online'],
         ['Wait for the digitally signed PDF with a QR code, quoted at 2 to 3 working days', 3, 0, 'online'],
         ['If the embassy asks for the Foreign Ministry stamp, attest it (NPR 500 is quoted by guides; check the portal)', 3, 500, 'online'],
     ],
     'docs': ['Citizenship certificate', 'Passport copy if you hold one', 'Passport size photo', 'Mobile number and email for the account'],
     'link': 'guide:mofa-attestation'},
]

FAQ_ADD = [
    {'id': 'fw16-16', 'topic': 'abroad', 'q': 'How much interest does an education loan cost in Nepal?', 'go': ['abroad-ms'],
     'a': 'A May 2026 comparison table lists floating education loan rates from about 5.4 to 7.4 percent at Agricultural Development Bank and 5.56 to 6.56 percent at Rastriya Banijya Bank, up to 9 to 11 percent at some commercial and development banks, and fixed rates near 10 percent. Another guide quotes Rastriya Banijya Bank at 5.97 percent floating, up to NPR 80 lakh, a 12 month moratorium after the course and a tenure up to 15 years. '
          'Processing fees of 0.75 percent are quoted in an older guide. One guide says collateral is needed above NPR 7.5 lakh. Banks reset rates monthly, so read the bank page and ask for the sanction letter in writing.'},
    {'id': 'fw16-17', 'topic': 'abroad', 'q': 'Can a bank loan count as proof of funds for my visa?', 'go': ['abroad-ms'],
     'a': 'A guide from August 2026 says a sanctioned education loan letter is accepted as proof of funds by most destinations, and Nepali A class banks usually ask for land or a fixed deposit as collateral. Each country has its own rule about how the loan, the bank and the holding period are shown (the UK, for example, asks for funds held for 28 days). Ask the embassy or the university, not an agent, and keep the sanction letter and the disbursement receipt together.'},
    {'id': 'fw16-18', 'topic': 'abroad', 'q': 'How do I get a police clearance certificate for a student visa?', 'go': ['abroad-ms'],
     'a': 'Apply online at opcr.nepalpolice.gov.np or through the Nagarik App. Guides say the application is free and you receive a digitally signed PDF with a QR code in 2 to 3 working days. If the embassy wants it attested, the Department of Consular Services charges about NPR 500 per document according to guides. There is no fixed validity: the embassy or employer usually sets how old it may be, often 3 to 6 months.'},
]
