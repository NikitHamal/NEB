"""Builds api/data/pathways/wave9.json from the MEC 2083/84 seat notice (tools/pathways/mec2083_seats.json).

The seat file is the college by college table of the Medical Education Commission notice of 30 Ashwin 2083
(16 Oct 2026): 9,691 seats, 84 institutions. The program totals add up to the notice (BSc Nursing 2,640, BNS 1,160,
BPharm 905, BPH 610, BSc MLT 437, BPT 150, BSc MIT 147, BOptom 110, BAMS 80). MBBS and BDS were loaded in wave 8.
A college is only listed when its district is known for sure; the rest stay out until a source names the town.
Run: python3 backend_python/tools/pathways/build_wave9.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / 'api' / 'data' / 'pathways' / 'wave9.json'
ROUTE = {'BSc Nursing': 'bsc-nursing', 'BNS': 'bns', 'BPharm': 'bpharm', 'BPH': 'bph', 'BSc MLT': 'bmlt', 'BPT': 'bpt',
         'BSc MIT': 'bsc-mit', 'BOptom': 'boptom', 'BAMS': 'bams', 'BSc Midwifery': 'bmid', 'BASLP': 'baslp',
         'B Perfusion Technology': 'bperfusion-anesthesia'}
LABEL = {'bsc-nursing': 'BSc Nursing', 'bns': 'BNS', 'bpharm': 'BPharm', 'bph': 'BPH', 'bmlt': 'BSc MLT', 'bpt': 'BPT',
         'bsc-mit': 'BSc MIT', 'boptom': 'BOptom', 'bams': 'BAMS', 'bmid': 'BSc Midwifery', 'baslp': 'BASLP',
         'bperfusion-anesthesia': 'B.Perfusion'}
# MEC fee ceiling for a paying seat at a private college (wave 7 notice figures): nursing, allied health and BPharm, BAMS
CEILING = {'bsc-nursing': 1036000, 'bpharm': 777000, 'bmlt': 777000, 'bpt': 777000, 'boptom': 777000, 'bams': 1131930}
EXISTING = {
    'National Academy of Medical Sciences (NAMS)': 'p-nams', 'B. P. Koirala Institute of Health Sciences': 'p-bpkihs',
    'Birat Medical College': 'p-birat-med', 'Chitwan Medical College': 'p-cmc',
    'College of Medical Sciences Teaching Hospital': 'p-coms-chitwan', 'Kathmandu University School of Medical Sciences': 'p-kusms',
    'Lalitpur Nursing Campus (PAHS)': 'p-pahs', 'Lumbini Medical College & Teaching Hospital Ltd': 'p-lumbini-med',
    'Maharajgunj Nursing Campus': 'p-iom', 'Maharajgunj Medical Campus': 'p-iom', 'Central Department of Public Health': 'p-iom',
    'Manipal College of Medical Sciences': 'p-manipal-pokhara', 'Nobel Medical College Teaching Hospital Public Ltd.': 'p-nobel-med',
    'Devdaha Medical College & Research Institute': 'p-devdaha-med', 'Gandaki Medical College': 'p-gandaki-med',
    'Kathmandu Medical College P. Ltd.': 'p-kmc', 'Nepal Medical College Pvt. Ltd.': 'p-nmc-jorpati',
    'Nepalese Army Institute of Health Sciences': 'p-naihs', 'Nepalgunj Medical College': 'p-nepalgunj-med',
    'Universal College of Medical Sciences and Teaching Hospital': 'p-ucms', 'B & C Medical College Teaching Hospital & Research Center Pvt. Ltd.': 'p-bc-med',
    'National Medical College': 'p-national-med', 'Janaki Medical College': 'p-janaki-med', 'Madan Bhandari Academy of Health Sciences': 'p-mbahs',
    'Rapti Academy of Health Sciences': 'p-rahs', 'Karnali Academy of Health Sciences': 'p-kahs', 'Madhesh Institute of Health Sciences': 'p-mihs',
    'Martyr Dasharath Chand University of Health Sciences': 'p-sdcuhs', 'Pokhara Academy of Health Sciences': 'p-pokhara-ahs',
    'KIST Medical College': 'p-kist-med', 'Kantipur Dental College': 'p-kantipur-dental', "People's Dental College & Hospital Pvt. Ltd": 'p-peoples-dental',
    'Gandaki University': 'p-gu-pokhara', 'Kathmandu University School of Sciences': 'p-ku-eng', 'Ayurveda Campus Kirtipur': 'p-ayurved',
    'University Campus (RJU)': 'p-rju', 'Manmohan Technical University School of Medicine & Allied Health Sciences': 'p-mtu-morang',
}
# name: (id, display name, kind, sector, district, place)
NEW = {
    'Biratnagar Nursing Campus': ('p-biratnagar-nursing', 'Biratnagar Nursing Campus (Tribhuvan University)', 'Campus', 'Public', 'Morang', 'Biratnagar'),
    'Birgunj Nursing Campus': ('p-birgunj-nursing', 'Birgunj Nursing Campus (Tribhuvan University)', 'Campus', 'Public', 'Parsa', 'Birgunj'),
    'Pokhara Nursing Campus': ('p-pokhara-nursing', 'Pokhara Nursing Campus (Tribhuvan University)', 'Campus', 'Public', 'Kaski', 'Pokhara'),
    'Nepalgunj Nursing Campus': ('p-nepalgunj-nursing', 'Nepalgunj Nursing Campus (Tribhuvan University)', 'Campus', 'Public', 'Banke', 'Nepalgunj'),
    'School of Health And Allied Sciences (SHAS)': ('p-shas-pu', 'School of Health and Allied Sciences (Pokhara University)', 'Campus', 'Public', 'Kaski', 'Lekhnath'),
    'Himalaya Eye Institute (SHAS)': ('p-himalaya-eye', 'Himalaya Eye Institute (Pokhara University SHAS)', 'Institute', 'Private', 'Kaski', 'Pokhara'),
    'Purbanchal University School of Health Sciences': ('p-pu-shs', 'Purbanchal University School of Health Sciences', 'Campus', 'Public', 'Morang', 'Gothgaun'),
    'B.P. Koirala Memorial Cancer Hospital Nursing College': ('p-bpkmch-nursing', 'B. P. Koirala Memorial Cancer Hospital Nursing College', 'College', 'Public', 'Chitwan', 'Bharatpur'),
    'Scheer Memorial Adventist Hospital Medical Institute, College of Nursing': ('p-scheer-nursing', 'Scheer Memorial Adventist Hospital College of Nursing', 'College', 'Private', 'Kavrepalanchok', 'Banepa'),
    'Crimson College of Technology': ('p-crimson', 'Crimson College of Technology', 'College', 'Private', 'Rupandehi', 'Devinagar'),
    'Kathmandu Model Hospital School of Nursing': ('p-kmh-nursing', 'Kathmandu Model Hospital School of Nursing', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'Everest College of Nursing': ('p-everest-nursing', 'Everest College of Nursing', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'Little Buddha College of Health Science': ('p-little-buddha', 'Little Buddha College of Health Science', 'College', 'Private', 'Kathmandu', 'Minbhawan'),
    'Nobel College': ('p-nobel-college', 'Nobel College (Pokhara University)', 'College', 'Private', 'Kathmandu', 'Sinamangal'),
    'Yeti Health Science Academy': ('p-yeti-health', 'Yeti Health Science Academy', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'B & B Medical Institute': ('p-bb-medical', 'B and B Medical Institute', 'Institute', 'Private', 'Lalitpur', 'Gwarko'),
    'Hope International College & Hospital Pvt. Ltd.': ('p-hope-intl', 'Hope International College and Hospital', 'College', 'Private', 'Lalitpur', 'Lalitpur'),
    'Manmohan Memorial Institute of Health Sciences': ('p-mmihs', 'Manmohan Memorial Institute of Health Sciences', 'Institute', 'Private', 'Kathmandu', 'Soalteemode'),
    'Modern Technical College Ltd.': ('p-modern-tech', 'Modern Technical College', 'College', 'Private', 'Lalitpur', 'Lalitpur'),
    'Valley College of Technical Sciences': ('p-valley-tech', 'Valley College of Technical Sciences', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'Nagarik College of Health Sciences': ('p-nagarik-health', 'Nagarik College of Health Sciences', 'College', 'Private', 'Bhaktapur', 'Bhaktapur'),
    'Koshi Health & Science Campus': ('p-koshi-health', 'Koshi Health and Science Campus', 'Campus', 'Private', 'Morang', 'Biratnagar'),
    'Om Health Campus (P.) Ltd.': ('p-om-health', 'Om Health Campus', 'Campus', 'Private', 'Kathmandu', 'Chabahil'),
    'Oasis Medical College Teaching Hospital & Research Centre Pvt. Ltd.': ('p-oasis-med', 'Oasis Medical College', 'Medical college', 'Private', 'Chitwan', 'Bharatpur'),
    'Sanjeevani College of Medical Sciences': ('p-sanjeevani', 'Sanjeevani College of Medical Sciences', 'Medical college', 'Private', 'Rupandehi', 'Butwal'),
    'Charak Academy, Pokhara': ('p-charak', 'Charak Academy', 'College', 'Private', 'Kaski', 'Pokhara'),
    'Novel Academy, Pokhara': ('p-novel', 'Novel Academy', 'College', 'Private', 'Kaski', 'Pokhara'),
    'Norvic College of Health Sciences and Technologies Pvt. Ltd.': ('p-norvic', 'Norvic College of Health Sciences and Technologies', 'College', 'Private', 'Kathmandu', 'Thapathali'),
    'Asian College for Advance Studies': ('p-asian-adv', 'Asian College for Advance Studies', 'College', 'Private', 'Lalitpur', 'Satdobato'),
    'National Model College for Advance Learning (NIST)': ('p-nist', 'National Model College for Advance Learning (NIST)', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'Chakrabarti Habi Education Academy, College of Nursing Science': ('p-chakrabarti', 'Chakrabarti Habi Education Academy, College of Nursing Science', 'College', 'Private', 'Kathmandu', 'Kathmandu'),
    'Kendriya Ayurveda Bidhyapeeth Dang': ('p-kendriya-ayurveda', 'Kendriya Ayurveda Bidhyapeeth', 'Campus', 'Public', 'Dang', 'Dang'),
}


def main():
    data = json.loads((HERE / 'mec2083_seats.json').read_text(encoding='utf-8'))
    per = {}
    for prog, rows in data.items():
        rid = ROUTE.get(prog)
        if not rid:
            continue
        for name, seats in rows:
            pid = EXISTING.get(name) or (NEW[name][0] if name in NEW else None)
            if pid and seats > 0:
                per.setdefault(pid, {})
                per[pid][rid] = per[pid].get(rid, 0) + seats
    new_by_id = {v[0]: v for v in NEW.values()}
    out = {'providers_add': [], 'where_add': {}, 'route_seats': {}, 'note_add': {}, 'fees': {}, 'seats_if_empty': {}}
    for pid, rs in sorted(per.items()):
        text = ', '.join(f'{LABEL[r]} {n}' for r, n in sorted(rs.items(), key=lambda kv: -kv[1]))
        out['route_seats'][pid] = rs
        primary = max(rs.values())
        if pid in new_by_id:
            _, name, kind, sector, district, place = new_by_id[pid]
            out['providers_add'].append({
                'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': district, 'place': place, 'website': '',
                'note': f'MEC seats for 2083/84: {text}.' + (' Fee is the MEC ceiling for a paying seat; confirm the college notice for the year.' if sector == 'Private' else ''),
                'seats': rs.get('bsc-nursing', primary),
            })
        else:
            out['note_add'][pid] = f'More MEC seats for 2083/84: {text}.'
            if pid not in ('p-ku-eng', 'p-gu-pokhara', 'p-mtu-morang', 'p-rju'):
                out['seats_if_empty'][pid] = primary
        for r in rs:
            out['where_add'].setdefault(r, []).append(pid)
        sector = new_by_id[pid][3] if pid in new_by_id else None
        if sector == 'Private':
            fees = {r: [CEILING[r], CEILING[r]] for r in rs if r in CEILING}
            if fees:
                out['fees'][pid] = fees
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(out['providers_add']), 'new providers;', len(out['note_add']), 'existing;', {r: len(v) for r, v in out['where_add'].items()})


if __name__ == '__main__':
    main()
