"""Wave 33 Nepal side. Websites opened on 2026-11-21: janapriya.edu.np (title Janapriya Multiple Campus, HTTP 200) and
birathealthcollege.edu.np (title Birat Health College, HTTP 200), found as the OpenStreetMap website tag of the same named institution
(Overpass query of Nepal education objects with a website tag) and then opened. The OSM match was kept only when the page title equals the row name.
Rejected: indrenicollege.edu.np (does not answer from our VM), godawari.edu.np and nationalcollege.edu.np (different institutions with similar words).
"""
PROVIDER_UPDATE = {
    'p-w24-iost-janapriya-mc': {'website': 'https://janapriya.edu.np'},
    'p-w28-pu-birat-health-college-morang': {'website': 'https://birathealthcollege.edu.np'},
}
