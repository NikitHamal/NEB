"""Mid-West University (Surkhet) 2083/84 bachelor admission notice, as printed by collegenp.com (read 19 Nov 2026) and the
official Examinations Management Office lists (muexam.edu.np/colleges/consituent and /affiliated, read through a fetch
tool because the site answers 403 to scripts). mu.edu.np answers 403 to scripts as well."""

CK = 'MU Registrar notice for 2083/84 bachelor admission as printed on collegenp.com, read 19 Nov 2026'

# Central schools of the university: text only, they all sit in the one university row p-mu.
MU_NOTE = (
    f'Bachelor programmes open for admission in 2083/84 ({CK}): Graduate School of Humanities and Social Sciences, Birendranagar: '
    'BA in English, International Relations, Journalism and Mass Communication, Mathematics, Nepali, Sociology, Social Work, '
    'Economics and Rural Development. Graduate School of Management: BBS. Graduate School of Education: B.Ed. in Nepali, English, '
    'Health, Population, Mathematics, Educational Planning and Management and Special Needs Education. Graduate School of Science '
    'and Technology: BSc CSIT, BIT, BSc Environment, BSc Biology group and BSc Physical group. Graduate School of Engineering at '
    'Sano Surkhet: BE Computer, BE Civil and BE Hydropower. Graduate School of Agriculture and Forestry Science at Ramghat: BSc '
    'Agriculture. School of Law: BA LL.B. The same notice lists ten constituent campuses and one affiliated college. The '
    'Examinations Management Office also lists the Central Departments of Physical and Mathematical Sciences, Biological and '
    'Chemical Sciences, Computer and Information Technology, Civil Engineering, Computer Engineering, Hydropower Engineering and '
    'Management. The university site mwu.edu.np answers, while mu.edu.np and muexam.edu.np answer 403 to scripts. Seats and fees are '
    'not printed in the notice, so confirm them with the school.'
)
MU_ROUTES = ['bsc-csit', 'bit', 'bsc-environment', 'bsc-science', 'bbs', 'bsw', 'bjmc', 'be-computer', 'be-civil', 'ba-llb', 'bsc-agri', 'bed', 'ba']

# existing constituent rows: id -> (programmes text, routes to add, phones)
CAMPUS_NOTES = {
    'p-babai-bardiya': ('BBS; B.Ed. in Nepali, English, Population, Science Education, Mathematics and Health; BA in Nepali, English, Rural Development, Social Work and Sociology', ['bbs', 'bed', 'ba', 'bsw'], '9858031710, 9858024651, 9848026088', 'Gulariya, Bardiya'),
    'p-w25-bageshwari': ('BSc; BBS; BBA; B.Ed. in Nepali, English, Population and Health; BA in Nepali, English, Rural Development and Sociology', ['bsc-science', 'bbs', 'bba', 'bed', 'ba'], '9858033488', 'Kohalpur, Banke'),
    'p-bheri-jajarkot': ('BBS; B.Ed. in Nepali, English, Health, Mathematics and Population; BA in International Relations and Economics', ['bbs', 'bed', 'ba'], '9748008777, 9868019440', 'Khalanga, Jajarkot'),
    'p-jaljala-rolpa': ('BBS; B.Ed. in Nepali, English and Population; BA in Sociology', ['bbs', 'bed', 'ba'], '9860819020', 'Liwang, Rolpa'),
    'p-musikot-rukum-west': ('BBS; B.Ed. in Nepali, English, Health, Population and Mathematics; BA in Sociology', ['bbs', 'bed', 'ba'], '984345179, 9815152071', 'Musikot, Rukum'),
    'p-narayan-dailekh': ('BBS; B.Ed. in Nepali, English, Health, Population and Mathematics; BA in Rural Development and Sociology', ['bbs', 'bed', 'ba'], '9848064474', 'Dailekh Bazar, Dailekh'),
    'p-rara-mugu': ('B.Ed. in Nepali, English, Health and Population (the notice lists no BBS or BA here)', ['bed'], '9858087988', 'Gamgadhi, Mugu'),
    'p-tila-kalikot': ('B.Ed. in Nepali, English, Health and Population (the notice lists no BBS or BA here)', ['bed'], '9848169453', 'Manma, Kalikot'),
    'p-w25-vidhyapur': ('BBS; B.Ed. in Nepali, English and Health', ['bbs', 'bed'], '9848278390', 'Vidhyapur, Surkhet'),
}

# new rows: id, name, kind, sector, district, place, website, programmes, routes, extra
NEW = [
    ('p-w30-bheri-gumi', 'Bheri Multiple Campus (Mid-West University)', 'Campus', 'Community', 'Surkhet', 'Gumi',
     None, 'BBS; B.Ed. in Nepali, English, Mathematics and Population', ['bbs', 'bed'],
     'Phone 9868296547. Collegenp lists it as a community campus with the 4 year BBS and B.Ed. under Mid-West University. Bheri Gyanodaya (Jajarkot) is a different campus.'),
    ('p-w30-gci', 'Global College International', 'College', 'Private', 'Kathmandu', 'Mid-Baneshwor',
     None, 'BBA; BHM; BTTM', ['bba', 'bhm', 'bttm'],
     'Phones 01-5970319, 9801258882. It is the only college on the official Mid-West University affiliated list (college code 1010, muexam.edu.np/colleges/affiliated). Global College of Management is a different college.'),
]
