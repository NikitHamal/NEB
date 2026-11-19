"""Wave 39 websites, found by tools/pathways/scrape_sites_w39.py (621 providers without a site, name based domain guesses; 11 passed the title and place test) and then opened by hand on 2026-11-19.
Kept (page shows the college name and place): apollocollege.edu.np (Apollo International College, Kathmandu, est. 2010), gpcar.edu.np (G.P. Koirala College of Agriculture and Research Centre, Purbanchal University),
dpsp.edu.np (Dhaulagiri Prabidhik Shikshya Pratisthan, Baglung Municipality 4), ynsra.edu.np (Yogi Naraharinath Study and Research Academy, Surkhet).
Rejected: birgunjcollege.com (title does not say Multiple or Model, matched two different providers), mahalaxmi-institute.com (NIOS counselling), rainas.org.np (launching soon page), gaurinstitute.com (a welfare institute with
another name), arun.com and gorkha.com (unrelated sites), rasuwa.com, medical.com and valley.com.np from the first test run (single word domains).
"""
PROVIDER_UPDATE = {
    'p-w24-pu-apollo': {'website': 'https://apollocollege.edu.np'},
    'p-w28-pu-g-p-koirala-college-of-agriculture-and-research-morang': {'website': 'https://gpcar.edu.np'},
    'p-ct37-176': {'website': 'https://dpsp.edu.np'},
    'p-ct37-1094': {'website': 'https://www.ynsra.edu.np'},
}
