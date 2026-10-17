# soc10 progress (Grade 10 सामाजिक अध्ययन, SEE)

Lead helper: writes unit 1 itself, delegates units 2–10 to sub-agents (one unit each), verifies and logs.

| Unit | Status | check.py | Commit |
|---|---|---|---|
| 1 हामी र हाम्रो समाज | DONE | 7736 words, 11 figures (6 fig + 5 photo), 3 examples | 43a11f6798 |
| 2 विकास र विकासका आधार | DONE (sub-agent) | 8141 words, 14 figures (5 photos), 4 examples | 8da6f85ffa |
| 3 हाम्रा सामाजिक मूल्य र मान्यता | DONE (sub-agent) | 8529 words, 16 figures (8 photos), 1 example | 6eae6bb61c |
| 4 सामाजिक समस्या र समाधान | DONE (sub-agent) | 8987 words, 10 figures (3 photos), 2 examples | fb1935d569 |
| 5 नागरिक चेतना | DONE (sub-agent) | 8985 words, 17 figures (7 photos), 2 examples | ba76032c1e |
| 6 हाम्रो पृथ्वी | DONE (sub-agent) | 11176 words (12 lessons, ~60 questions), 18 figures (5 photos), 2 examples | 7114c2dddc |
| 7 हाम्रो विगत | DONE (sub-agent) | 11927 words (10 lessons, 44 questions), 17 figures (7 photos), 1 example | 394936ca54 |
| 8 आर्थिक क्रियाकलाप | DONE (sub-agent) | 11568 words (9 lessons, 43 questions), 14 figures (5 photos), 6 examples | d44e052cfe |
| 9 हाम्रो अन्तर्राष्ट्रिय सम्बन्ध र सहयोग | DONE (sub-agent) | 8783 words, 11 figures (4 photos), 1 example | 5cc797fa47 |
| 10 जनसङ्ख्या र यसको व्यवस्थापन | DONE (sub-agent) | 9146 words, 19 figures (4 photos), 6 examples | a20e64f14a |

Notes:
- Unit 1: 4 lessons (१.१ सामाजिकीकरण, १.२ हाम्रा पहिचान, १.३ विविधतामा एकता, १.४ हाम्रा राष्ट्रिय गौरव), one अभ्यास per lesson, all answered.
- Corrections noted in unit 1: hindu 81.2 → 81.19 (rounded, both fine), "शिख" → सिख, flag "त्रिकोण आकार" clarified as two stacked triangles / only non-quadrilateral flag; "अन्य" religions = 0.60 (old draft said 0.58).
- hours: all files have hours: 0 — kept.
- Unit 2 fixes: Stockholm conference 1978 → 1972 (textbook box contradicts its own text). Post-textbook updates (airports, Upper Tamakoshi 456 MW) in caution box.
- Unit 6 fixes: smallest N. American country is St Kitts & Nevis; Sonoran desert location; Germany not Mediterranean; Asian/African animals wrongly in Amazon list; emu is Australian; S. America 12 sovereign countries; Brazil leads coffee not cocoa; diamond leader outdated; temperate marine latitude. Unit 6 is long (11k words) — candidate for trimming.
- Sub-agents in parallel hit API 409 errors; running units 3,4,5,7,8,9,10 one at a time.
- Unit 3 fixes: CRC ratified (not signed) 14 Sep 1990; Malala's age/prize year; नुत्से → नुप्से.
- Unit 4 fixes: anti-corruption body names (राष्ट्रिय सतर्कता केन्द्र, महालेखा परीक्षकको कार्यालय, सम्पत्ति शुद्धीकरण अनुसन्धान विभाग); UNICEF is a UN fund, not a specialised agency; police trafficking table total 352 added.
- Unit 5 fixes: candidate ages (21 local only; 25/35/45); Eleanor Roosevelt role; 1962 Kennedy message (not a bill); duplicate UDHR point. National-party list is the post-2079 one (verified: 7 parties) with a note that it changes after each election (2082 election changed it).
- Unit 7 fixes: Tanka Prasad govt fell 2014 (not 2013); BP released 2025; NC seats 2056 = 111; Deuba dissolution 2059 Jestha 8; Bosnia 1878/1908; black day 8 Aug 1918; reparations ~£6.6 bn; Rhineland 50 km; Bulgaria WWI dead 87,500; 3 Sep 1939 Britain+France; Greece 1941; Japan surrender 2 Sep 1945; Marshall/Molotov order. Kept as textbook (doubtful): Maoists 73 members in interim legislature (likely 83), Piskar date. Unit 7 long (11.9k words).
- LEAD ATTENTION: photo id soc10/tribhuvan fails check — registry expects tribhuvan.jpg but asset is tribhuvan.png (outside soc10 content; not touched).
- Unit 8 fixes: अनवीकरणीय → नवीकरणीय misprint; textbook claim that direct taxes are the largest revenue share corrected (VAT largest; indirect > direct). Unit 8 long (11.6k).
- Unit 9 fixes: first veto USSR 1946 (not Britain); 2/3 majority only for important questions; ITU specialised agency 1947; विश्व जलवायु सङ्गठन → विश्व मौसम विज्ञान सङ्गठन; Oscar submission not nominee; moon-mission news updated (Chandrayaan-3 landed 2023 etc.).
- Unit 10 fixes: doubling time 2078 = 76 yr (table had 71.3 = life expectancy); 1.35% belongs to 2068; 2078 sex split 48.87/51.13; 2078 age shares 61.96/10.21 (table had 65.2/6.9); nine castes over 10 lakh, not six; Bagmati (6,116,866) narrowly ahead of Madhesh (6,114,600) — verified. Left as textbook: under-5 mortality listed in PQLI (original index uses infant mortality).

## STATUS: ALL 10 UNITS DONE AND PUSHED. Final re-check: check.py OK on all ten; check_nepali_only.py soc10 passes.
Possible follow-up for lead: units 6, 7, 8 are 11–12k words (above 8k target) because of 9–12 lessons each; tribhuvan photo registry mismatch.
