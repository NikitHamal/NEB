"""Wave 38: every school on the NEB Class 12 exam centre notice of 2083 (Baishakh 14 to 27, 2083 BS = April 2026).

Source: National Examinations Board, Examination Control Office (Class 11 and 12), Sanothimi, "Class 12 exam centres 2083" (248 page PDF,
mirrored at https://media.edusanjal.com/c/Neb%20Class%2012%20Exam%20Center%20Notice%20..pdf). Each row lists the exam centre, the 5 digit
school code (first two digits are the district) and the school with its address. A school only appears when it had Class 12 candidates,
so this is the list of schools that run Grade 11 and 12 under NEB. The PDF is typeset in Preeti, decoded by preeti.py.

Run: python3 backend_python/tools/pathways/scrape_neb_plus2_w38.py   (downloads the PDF to /tmp/neb_ec.pdf when it is missing)
Writes api/data/pathways/neb_plus2.json (served by api.pathways.plus2_schools, not merged into the main payload to keep it small).
"""
import collections
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
from preeti import preeti_to_unicode, to_roman  # noqa: E402

URL = 'https://media.edusanjal.com/c/Neb%20Class%2012%20Exam%20Center%20Notice%20..pdf'
PDF = Path('/tmp/neb_ec.pdf')
OUT = HERE.parent.parent / 'api' / 'data' / 'pathways' / 'neb_plus2.json'
ROW = re.compile(r'^(?:\d{1,4}\s+)?(.*?)\s*(?<![\d-])(\d{5})(?!\d)\s*(.*)$')
TYPE = re.compile(r'(?:उ\.|नि\.)?मा\.वि\.?|आ\.वि\.?|प्रा\.वि\.?')
DISTRICT = {
    '01': 'Taplejung', '02': 'Panchthar', '03': 'Ilam', '04': 'Jhapa', '05': 'Morang', '06': 'Sunsari', '07': 'Dhankuta', '08': 'Terhathum',
    '09': 'Sankhuwasabha', '10': 'Bhojpur', '11': 'Solukhumbu', '12': 'Okhaldhunga', '13': 'Khotang', '14': 'Udayapur', '15': 'Saptari',
    '16': 'Siraha', '17': 'Dhanusha', '18': 'Mahottari', '19': 'Sarlahi', '20': 'Sindhuli', '21': 'Ramechhap', '22': 'Dolakha',
    '23': 'Sindhupalchok', '24': 'Kavrepalanchok', '25': 'Lalitpur', '26': 'Bhaktapur', '27': 'Kathmandu', '28': 'Nuwakot', '29': 'Rasuwa',
    '30': 'Dhading', '31': 'Makwanpur', '32': 'Rautahat', '33': 'Bara', '34': 'Parsa', '35': 'Chitwan', '36': 'Gorkha', '37': 'Lamjung',
    '38': 'Tanahu', '39': 'Syangja', '40': 'Kaski', '41': 'Manang', '42': 'Mustang', '43': 'Myagdi', '44': 'Parbat', '45': 'Baglung',
    '46': 'Gulmi', '47': 'Palpa', '48': 'Nawalparasi West', '49': 'Rupandehi', '50': 'Kapilvastu', '51': 'Arghakhanchi', '52': 'Pyuthan',
    '53': 'Rolpa', '54': 'Rukum East', '55': 'Salyan', '56': 'Dang', '57': 'Banke', '58': 'Bardiya', '59': 'Surkhet', '60': 'Dailekh',
    '61': 'Jajarkot', '62': 'Dolpa', '63': 'Jumla', '64': 'Kalikot', '65': 'Mugu', '66': 'Humla', '67': 'Bajura', '68': 'Bajhang',
    '69': 'Achham', '70': 'Doti', '71': 'Kailali', '72': 'Kanchanpur', '73': 'Dadeldhura', '74': 'Baitadi', '75': 'Darchula',
    '76': 'Nawalparasi East', '77': 'Rukum West',
}  # checked against the trailing district word of every row and the local level names of 48, 54, 76 and 77


def load_text():
    if not PDF.exists():
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 Chrome/120'})
        PDF.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    from pypdf import PdfReader
    return '\n'.join((p.extract_text() or '') for p in PdfReader(str(PDF)).pages).split('\n')


def parse(lines):
    rows = {}
    for line in lines:
        m = ROW.match(line)
        if not m:
            continue
        code = m.group(2)
        if not (1 <= int(code[:2]) <= 77):
            continue
        txt = preeti_to_unicode(m.group(3))
        txt = re.split(r'कक्षा\s*१२|र\.नं|नियमित|नियमीत|तपर्फ|तर्फ|वाँकी|बाँकी', txt)[0].strip()
        if len(txt) < 6 or code in rows:
            continue
        rows[code] = txt
    return rows


def main():
    rows = parse(load_text())
    last = collections.defaultdict(collections.Counter)
    for code, txt in rows.items():
        last[code[:2]][txt.split()[-1].strip(',')] += 1
    dist_ne = {k: v.most_common(1)[0][0] for k, v in last.items()}
    dist_en = {k: DISTRICT[k] for k in dist_ne}
    assert set(dist_en) == set(DISTRICT), set(DISTRICT) ^ set(dist_en)
    out = []
    for code in sorted(rows):
        txt, ne = rows[code], dist_ne[code[:2]]
        while txt.endswith(ne) or txt.endswith(ne + ','):
            txt = txt[: txt.rindex(ne)].rstrip(' ,')
        m = TYPE.search(txt)
        if m:
            name, addr = txt[: m.end()], txt[m.end():]
        elif ',' in txt:
            name, addr = txt.split(',', 1)
        else:
            name, addr = txt, ''
        name, addr = name.strip(' ,'), addr.strip(' ,')
        en, ad = (re.sub(r'[^\x00-\x7f]', '', to_roman(x)) for x in (name, addr))
        ad = re.sub(r'\b(?:Niyami\w*|Taparpha\w*|Dekhi|Sammaka?|Pariksha\w*)\b', '', ad)
        out.append([code, re.sub(r'\s+', ' ', en).strip(), name, re.sub(r'\s+', ' ', ad).strip(' ,-')])
    data = {
        'source': 'National Examinations Board, Class 12 exam centre notice 2083 (exams from Baishakh 14 to 27, 2083 BS)',
        'districts': {k: dist_en[k] for k in sorted(dist_en)},
        'fields': ['code', 'name', 'name_ne', 'address'],
        'schools': out,
    }
    text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    for bad in ('\u2014', '\u2013'):
        assert bad not in text
    OUT.write_text(text + '\n', encoding='utf-8')
    per = collections.Counter(c[:2] for c in rows)
    print(len(out), 'schools', len(dist_en), 'districts', len(text) // 1024, 'KB')
    print({dist_en[k]: n for k, n in sorted(per.items(), key=lambda x: -x[1])[:12]})
    print(sorted(dist_en.values()))


if __name__ == '__main__':
    main()
