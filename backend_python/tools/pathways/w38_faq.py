"""Wave 38 FAQs fw38-*. Figures come from the NEB Class 12 exam centre notice 2083 via neb_plus2.json (see scrape_neb_plus2_w38.py)."""
from w38_nepal import PER, TOTAL, TOP

_TOP = ', '.join(f'{d} ({n})' for d, n in TOP)
FAQ_ADD = [
    {'id': 'fw38-1', 'topic': 'after10', 'q': 'How many schools in Nepal run Class 11 and 12 under NEB?',
     'a': f"NEB's exam centre notice for the Class 12 exams of Baishakh 2083 lists {TOTAL:,} schools that had Class 12 candidates, in all 77 districts. "
          f"The most are in {_TOP}. A school that runs Class 11 but had no Class 12 candidate that year would not appear, so the real number can be a little higher.",
     'go': ['plus2-science', 'plus2-management', 'plus2-humanities']},
    {'id': 'fw38-2', 'topic': 'after10', 'q': 'How can I check that a +2 school is really NEB approved?',
     'a': "Every NEB school has a 5 digit school code and its Class 12 students sit at a named exam centre. The notice lists code, school name, address and district, "
          "and the first two digits of the code are the district (for example 27 is Kathmandu, 40 is Kaski, 56 is Dang). Ask the school for its NEB school code and compare it "
          "with the NEB notice on neb.gov.np before you pay any admission fee. A school with no NEB code cannot register you for the Class 12 exam.",
     'go': ['plus2-science', 'plus2-management']},
    {'id': 'fw38-3', 'topic': 'after10', 'q': 'Does the NEB school list show which streams a school runs?',
     'a': "No. The exam centre notice only gives the school name, address, district and which centre its students sit at. Streams (Science, Management, Humanities, Education, Law) "
          "and seats come from the school itself, its admission notice or the NEB streams registered for the school, so confirm them before you apply.",
     'go': ['plus2-science', 'plus2-management', 'plus2-humanities', 'plus2-education', 'plus2-law']},
]
