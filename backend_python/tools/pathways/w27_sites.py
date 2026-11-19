"""Wave 27: official websites for providers that lost a dead guessed domain in wave 26 (audit of 2026-11-19).

Each domain below was found on a page that names the institution (its own search result page, a FWU campus table, or the
college listing with the same e-mail domain), resolved through Google DoH, and opened with a browser User-Agent.
- kailali.fwu.edu.np: FWU Faculty of Humanities campus table; page title "FWU | Kailali Multiple Campus" (HTTP 200).
- dcuhs.edu.np: "Martyr Dasharath Chand University of Health Science (MDCUHS)", Godawari-05, Geta, Kailali (HTTP 200).
- heh.org.np: Himalaya Eye Hospital home page (HTTP 200); the Himalaya Eye Institute is its education wing.
- thearyanschool.edu.np: e-mail domain info@thearyanschool.edu.np on its listing; the page shows an "under maintenance" notice today.
- biratmultiplecollege.edu.np, lcc.edu.np: resolve to Cloudflare / Vercel; the bot check blocks scripts but the sites are the
  ones in the college's own search result (biratmultiplecollege.edu.np) and the lcc.edu.np address on its Facebook page.
- amc.edu.np: "Ambikeshwari Campus", Ghorahi, Dang (HTTP 200).
- npihospital.com: "Narayani Samudayik Hospital, Chitwan" (HTTP 200); the nursing college is a part of the hospital.
- shreemedical.edu.np: page text names Shree Medical and Technical College (title shows the newer name Shree College of Technology).
- gmckusma.edu.np: "Gupteshwor Multiple Campus", Kushma (HTTP 200).
Not added (domain does not resolve today on the system resolver and Google DoH, or answers HTTP 500): valleycollege.edu.np,
mmcjnk.edu.np, lts.edu.np, bpkmch.org.np, sunkoshicampus.edu.np, smcpyuthan.edu.np (TLS error 526). No site found for Terhathum
Polytechnic Institute.
"""
PROVIDER_UPDATE = {
    'p-kailali': {'website': 'https://kailali.fwu.edu.np'},
    'p-sdcuhs': {'website': 'https://www.dcuhs.edu.np'},
    'p-himalaya-eye': {'website': 'https://heh.org.np'},
    'p-aryan-eng': {'website': 'https://thearyanschool.edu.np'},
    'p-birat-multiple': {'website': 'https://biratmultiplecollege.edu.np'},
    'p-lumbini-city': {'website': 'https://lcc.edu.np'},
    'p-ambikeshwori': {'website': 'https://amc.edu.np'},
    'p-npi-narayani': {'website': 'https://www.npihospital.com'},
    'p-shree-medical': {'website': 'https://shreemedical.edu.np'},
    'p-gupteshwor-parbat': {'website': 'https://gmckusma.edu.np'},
}
WEBSITE_DROP = []
