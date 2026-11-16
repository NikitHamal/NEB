"""BSc CSIT seat quota 2083/84 per college (TU IoST entrance result, 3,108 seats, 61 colleges, 80/20 open and Samabesi split).

Sources: TU IoST entrance result notice of Shrawan 2083 as republished by edusanjal.com and hamrocsit.com; place names
from the same notice. Totals are checked in build_wave10.py (16 constituent campuses 1,224; 45 private colleges 1,884).
"""
# existing provider id (or new key), seats
CONSTITUENT = [
    ('p-patan', 144), ('p-amrit', 144), ('bhairahawa-mc', 108), ('bhaktapur-mc', 72), ('p-padmakanya', 72),
    ('p-siddhanath', 72), ('p-rrmc', 72), ('p-mechi', 72), ('p-mmamc', 72), ('p-birendra', 72), ('p-prithvi', 72),
    ('p-butwal', 72), ('p-mmc-nepalgunj', 72), ('p-mmc-dang', 36), ('p-cct', 36), ('p-tribhuvan-palpa', 36),
]
# new constituent campuses: key, name, district, place
NEW_CONSTITUENT = [
    ('bhairahawa-mc', 'Bhairahawa Multiple Campus (Tribhuvan University)', 'Rupandehi', 'Bhairahawa'),
    ('bhaktapur-mc', 'Bhaktapur Multiple Campus (Tribhuvan University)', 'Bhaktapur', 'Doodhpati'),
]
# key or existing id, name, district, place, seats
PRIVATE = [
    ('p-sxc', "St. Xavier's College", 'Kathmandu', 'Maitighar', 48),
    ('p-kathford', 'Kathford International College of Engineering and Management', 'Lalitpur', 'Balkumari', 48),
    ('new-summit', 'New Summit College', 'Kathmandu', 'Old Baneshwor', 48),
    ('prime', 'Prime College', 'Kathmandu', 'Nayabazar', 48),
    ('st-lawrence', 'St. Lawrence College', 'Kathmandu', 'Chabahil', 36),
    ('cab', 'College of Applied Business', 'Kathmandu', 'Chabahil', 36),
    ('kbc', 'Kathmandu BernHardt College', 'Kathmandu', 'Bafal', 48),
    ('dwit', 'Deerwalk Institute of Technology', 'Kathmandu', 'Sifal', 48),
    ('vedas', 'Vedas College', 'Lalitpur', 'Jawalakhel', 48),
    ('texas', 'Texas International College', 'Kathmandu', 'Chabahil', 48),
    ('p-ncc', 'National College of Computer Studies (NCCS)', 'Kathmandu', 'Paknajol', 48),
    ('orchid', 'Orchid International College', 'Kathmandu', 'Gaushala', 48),
    ('ambition', 'Ambition College', 'Kathmandu', 'New Baneshwor', 36),
    ('sagarmatha-cst', 'Sagarmatha College of Science and Technology', 'Lalitpur', 'Sanepa', 48),
    ('nagarjuna-cit', 'Nagarjuna College of Information Technology', 'Lalitpur', 'Shankhamul', 36),
    ('academia', 'Academia International College', 'Lalitpur', 'Gwarko', 48),
    ('hce', 'Himalaya College of Engineering', 'Lalitpur', 'Chyasal', 48),
    ('asmt', 'Asian School of Management and Technology', 'Kathmandu', 'Gongabu', 48),
    ('mbmc', 'Madan Bhandari Memorial College', 'Kathmandu', 'New Baneshwor', 48),
    ('nepalaya', 'Nepalaya College', 'Kathmandu', 'Kalanki', 36),
    ('achs', 'Asian College of Higher Studies', 'Lalitpur', 'Jawalakhel', 48),
    ('trinity', 'Trinity International College', 'Kathmandu', 'Dillibazar', 48),
    ('samriddhi', 'Samriddhi College', 'Bhaktapur', 'Lokanthali', 48),
    ('swastik', 'Swastik College', 'Bhaktapur', 'Thimi', 36),
    ('kct', 'Kathmandu College of Technology', 'Bhaktapur', 'Lokanthali', 36),
    ('nist-banepa', 'NIST College', 'Kavrepalanchok', 'Banepa', 36),
    ('shreeyantra', 'Shreeyantra College', 'Jhapa', 'Damak', 48),
    ('birendra-memorial', 'Birendra Memorial College', 'Sunsari', 'Dharan', 48),
    ('godawari-itahari', 'Godawari College', 'Sunsari', 'Itahari', 36),
    ('birat-kshitiz', 'Birat Kshitiz College', 'Morang', 'Biratnagar', 36),
    ('nihareeka', 'Nihareeka College', 'Morang', 'Biratnagar', 36),
    ('birat-multiple', 'Birat Multiple College', 'Morang', 'Biratnagar', 36),
    ('aims-biratnagar', 'AIMS College', 'Morang', 'Biratnagar', 36),
    ('himalaya-darshan', 'Himalaya Darshan College', 'Morang', 'Biratnagar', 36),
    ('national-infotech', 'National Infotech College', 'Parsa', 'Birgunj', 48),
    ('hetauda-city', 'Hetauda City College', 'Makwanpur', 'Hetauda', 36),
    ('chitwan-cot', 'Chitwan College of Technology', 'Chitwan', 'Bharatpur', 36),
    ('lumbini-ict', 'Lumbini ICT Campus', 'Nawalparasi East', 'Gaindakot', 48),
    ('mount-annapurna', 'Mount Annapurna Campus', 'Kaski', 'Pokhara', 36),
    ('soch', 'Soch College of IT', 'Kaski', 'Pokhara', 36),
    ('lumbini-city', 'Lumbini City College', 'Rupandehi', 'Tilottama', 36),
    ('nepathya', 'Nepathya College', 'Rupandehi', 'Tilottama', 36),
    ('banke-bageshwori', 'Banke Bageshwori Campus', 'Banke', 'Nepalgunj', 36),
    ('nepalgunj-campus', 'Nepalgunj Campus', 'Banke', 'Nepalgunj', 36),
    ('ambikeshwori', 'Ambikeshwari Campus', 'Dang', 'Ghorahi', 36),
]
