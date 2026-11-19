"""Wave 34 websites found by tools/pathways/scrape_sites_w34.py on 2026-11-19: for each of the 369 providers without a website the script tried name derived
.edu.np, .com.np and .org.np domains and kept a hit only when the page answered HTTP 200 and its title held every distinctive word of the college name.
41 hits came back; 12 were kept after a manual look (same name, same kind of institution, same area where the page says it).
Rejected look alikes (do not retry): khwopa.edu.np (Khwopa College of Engineering, not Khwopa College), nationalcollege.edu.np, annapurna.edu.np (a different Annapurna School),
sagarmatha.edu.np (Sagarmatha Engineering College), siddhartha.edu.np (Banepa, not Butwal), amarjyoti.edu.np, everest.edu.np, narayani.edu.np (schools), mega.com.np (a computer distributor),
ambitionguru.edu.np (e-learning), nepathya.com.np, glaciercollege.edu.np (title does not name the college or Banepa), brihaspati.com.np (a hotel) and the .org.np foundations.
"""
PROVIDER_UPDATE = {
    'p-kmc-health': {'website': 'https://kathmandumultiplecollege.edu.np'},
    'p-w24-pu-camad': {'website': 'https://camadcollege.edu.np'},
    'p-w24-pu-citizen': {'website': 'https://citizencollege.edu.np'},
    'p-w24-pu-valley-state': {'website': 'https://valleystatecollege.edu.np'},
    'p-w24-iost-gyandeep': {'website': 'https://gyandeepcollege.edu.np'},
    'p-w24-iost-nagarik-nawalparasi': {'website': 'https://nagarikcollege.edu.np'},
    'p-w26-npca-292': {'website': 'https://udayashreemultiplecampus.edu.np'},
    'p-w27-npca-491': {'website': 'https://janajyoticampus.edu.np'},
    'p-w28-pu-d-a-v-business-school-kathmandu': {'website': 'https://davbusinessschool.edu.np'},
    'p-w28-pu-sann-international-college-for-higher-studies-kathmandu': {'website': 'https://sann.edu.np'},
    'p-w28-pu-lumbini-adarsha-degree-college-nawalparasieast': {'website': 'https://lumbiniadarsha.edu.np'},
    'p-w28-rju-nepalaya-education-foundation-kathmandu': {'website': 'https://nepalayaeducationfoundation.edu.np'},
}
