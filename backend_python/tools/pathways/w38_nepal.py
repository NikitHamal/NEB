"""Wave 38 Nepal notes: the NEB Class 12 exam centre notice of 2083 (5,335 schools with Class 12 candidates, see scrape_neb_plus2_w38.py).

Counts are computed from api/data/pathways/neb_plus2.json, so rerun scrape_neb_plus2_w38.py first.
"""
import collections
import json
from pathlib import Path

_J = json.loads((Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'neb_plus2.json').read_text(encoding='utf-8'))
TOTAL = len(_J['schools'])
PER = collections.Counter(_J['districts'][s[0][:2]] for s in _J['schools'])
TOP = PER.most_common(5)
_TOP_TXT = ', '.join(f'{d} {n}' for d, n in TOP)
_SMALL = ', '.join(f'{d} {n}' for d, n in sorted(PER.items(), key=lambda x: x[1])[:3])
_NOTE = (f"NEB's Class 12 exam centre notice for 2083 (exams 14 to 27 Baishakh, April 2026) lists {TOTAL:,} schools with Class 12 candidates in all 77 "
         f"districts ({_TOP_TXT}). The list gives school, address and district but not the streams, so ask the school which of Science, Management, "
         "Humanities, Education or Law it runs before you apply.")
ROUTE_NOTE_ADD = {rid: _NOTE for rid in ('plus2-science', 'plus2-management', 'plus2-humanities', 'plus2-education', 'plus2-law')}
