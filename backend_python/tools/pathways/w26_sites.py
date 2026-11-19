"""Wave 26: website audit of the provider list (tools/pathways/audit_sites.py, 488 sites opened on 2026-11-18).

Findings:
- 38 provider websites had no DNS record (NXDOMAIN or SERVFAIL on the system resolver and on Google DoH): guessed domains that
  never existed. 10 more TU campuses pointed at the tu.edu.np home page, which is not the campus own site.
- Replacement sources, in order: (1) the official TU campus list https://tu.edu.np/campuses (8 pages, 64 campuses, each with its
  official subdomain, all 64 answered HTTP 200), (2) the NPCA member page of the campus (npca.edu.np/campus_details/<id>) with the
  site opened, (3) the campus own page found by web search and opened.
- With no verified site the website is dropped (value None) instead of keeping a dead or generic link.
- Parent university links for constituent campuses (fwu.edu.np, mwu.edu.np, nsu.edu.np, ctevt.org.np) are real pages and stay.
"""

# provider id -> official subdomain on https://tu.edu.np/campuses (Mahendra Multiple Campus Ghorahi/Dang is mamc,
# Nepalgunj is mahemc, addresses read on both sites)
TU_OFFICIAL = {
    'p-mmamc': 'mmamc', 'p-patan': 'pmc', 'p-cct': 'cct', 'p-dhankuta': 'dhmc', 'p-iof-hetauda': 'hc', 'p-cec-rampur': 'cec',
    'p-bhaktapur-mc': 'bkmc', 'p-pulchowk': 'puc', 'p-amrit': 'ac', 'p-janaprasashan': 'pac', 'p-rr': 'rrlc',
    'p-mmc-dharan': 'mahmc', 'p-padmakanya': 'pkmc', 'p-terhathum-mc': 'temc', 'p-prithvi': 'prnc', 'p-shankerdev': 'sdc',
    'p-ssmy-siraha': 'ssmc', 'p-purc': 'purc', 'p-iof': 'pc', 'p-tribhuvan-palpa': 'tmc', 'p-birendra': 'bimc',
    'p-mmc-dang': 'mamc', 'p-mmc-nepalgunj': 'mahemc', 'p-ilam': 'mrmc', 'p-ayurved': 'ayc', 'p-lamjung-iaas': 'lac',
    'p-trichandra': 'trc', 'p-gorkha': 'gc', 'p-thapathali': 'thc', 'p-wrc': 'pasc', 'p-mechi': 'memc',
    'p-saraswati-mc': 'smc', 'p-dhaulagiri': 'dmc', 'p-mahendra-ratna': 'mrc',
}

# provider id -> NPCA campus id (website taken from tools/pathways/npca_campuses.json, opened HTTP 200)
NPCA_IDS = {
    'p-w24-iost-aishwarya': 91, 'p-salyan': 226, 'p-parbat-mc': 299, 'p-nuwakot-adarsha': 317, 'p-palhi-nawalparasi': 202,
    'p-simara-bara': 296, 'p-panchthar': 429, 'p-w24-iost-sahid-smriti-chitwan': 485,
}

# found by web search and opened or confirmed on a second page
OWN_SITES = {
    'p-damak-mc': 'https://damakcampus.edu.np',       # NPCA page 102 lists it; Cloudflare answers 403 to scripts
    'p-pathibhara': 'https://pathivaracampus.edu.np',  # spelled pathivara on the site, HTTP 200
    'p-manipal-pokhara': 'https://manipal-pokhara.com',  # HTTP 200, title Manipal Pokhara College of Medical Science
}

# dead or generic with no verified replacement: the website is removed
DROP = [
    'p-kailali', 'p-terhathum-poly', 'p-sunkoshi-sindhu', 'p-gupteshwor-parbat', 'p-swargadwari-pyuthan', 'p-sdcuhs',
    'p-bpkmch-nursing', 'p-himalaya-eye', 'p-valley-tech', 'p-aryan-eng', 'p-birat-multiple', 'p-lumbini-city',
    'p-ambikeshwori', 'p-model-multiple-janakpur', 'p-w12-lahan-ti', 'p-npi-narayani', 'p-shree-medical',
    'p-solukhumbu', 'p-trishuli-nuwakot', 'p-rasuwa', 'p-sisne-rukum-east', 'p-dolpa', 'p-manasarowar-humla',
    'p-harikhetan', 'p-dudh-koshi-solu', 'p-melamchi-sindhu', 'p-gaumukhi-pyuthan',
]
