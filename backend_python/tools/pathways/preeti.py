"""Preeti (legacy Nepali font) to Unicode Devanagari, and Devanagari to a readable Roman spelling.

Used by scrape_neb_plus2_w38.py: the NEB Class 12 exam centre notice is typeset in Preeti, so pypdf returns Latin looking text.
Glyph meanings were checked against the notice itself (for example `/fli6«o` is Rashtriya, `jÍ6]Zj/` is Venkateshwar).
"""
import re

_MAP = {
    'a': 'ब', 'b': 'द', 'c': 'अ', 'd': 'म', 'e': 'भ', 'f': 'ा', 'g': 'न', 'h': 'ज', 'i': 'ष्', 'j': 'व', 'k': 'प', 'l': 'ि',
    'm': 'फ', 'n': 'ल', 'o': 'य', 'p': 'उ', 'q': 'त्र', 'r': 'च', 's': 'क', 't': 'त', 'u': 'ग', 'v': 'ख', 'w': 'ध', 'x': 'ह',
    'y': 'थ', 'z': 'श', 'A': 'ब्', 'B': 'द्', 'C': 'ऋ', 'D': 'म्', 'E': 'भ्', 'F': 'ँ', 'G': 'न्', 'H': 'ज्', 'I': 'क्ष्',
    'J': 'व्', 'K': 'प्', 'L': 'ी', 'M': 'ः', 'N': 'ल्', 'O': 'इ', 'P': 'ए', 'Q': 'त्त', 'R': 'च्', 'S': 'क्', 'T': 'त्',
    'U': 'ग्', 'V': 'ख्', 'W': 'ध्', 'X': 'ह्', 'Y': 'थ्', 'Z': 'श्', '0': 'ण्', '1': 'ज्ञ', '2': 'द्द', '3': 'घ', '4': 'द्ध',
    '5': 'छ', '6': 'ट', '7': 'ठ', '8': 'ड', '9': 'ढ', '!': '१', '@': '२', '#': '३', '$': '४', '%': '५', '^': '६', '&': '७',
    '*': '८', '(': '९', ')': '०', '`': 'ञ', '~': 'ञ्', '-': '-', '_': ')', '=': '.', '+': 'ं', '[': 'ृ', ']': 'े', '{': 'र्',
    '}': 'ै', '\\': '्', '|': '्र', '<': '?', '>': 'श्र', ';': 'स', ':': 'स्', '"': 'ू', "'": 'ु', ',': ',', '.': '।', '/': 'र',
    '?': 'रु', 'ª': 'ङ', 'Ë': 'ङ्ग', '«': '्र', '¿': 'रू', '§': 'ट्ट', 'å': 'द्व', 'ˆ': 'फ्', 'Í': 'ङ्क', '£': 'क्', '´': 'झ',
    'ß': 'द्य', '¢': 'द्ध', '÷': '/', '—': '-', '–': '-', '›': 'द्र', '…': '"', 'Î': 'ङ्ख', '•': 'ङ्क', 'ç': 'ह', '¥': '',
    '¦': '', '‰': '', '‘': "'", '’': "'", '“': '"', '”': '"', '¡': 'ः',
}
_CONS = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ'
_MATRA = 'ािीुूृेैोौंँः'
_REPH = '\u0001'


def preeti_to_unicode(s):
    out = []
    for ch in s:
        if '\u0900' <= ch <= '\u097f':
            out.append(ch)  # real Unicode that the PDF already carries
        elif ch == '{':
            out.append(_REPH)
        else:
            out.append(_MAP.get(ch, ch))
    t = ''.join(out)
    t = t.replace('ाे', 'ो').replace('ाै', 'ौ').replace('ाो', 'ो')
    for a, b in (('अाे', 'ओ'), ('अाै', 'औ'), ('अो', 'ओ'), ('अौ', 'औ'), ('अा', 'आ'), ('अै', 'ऐ'), ('इी', 'ई'), ('उू', 'ऊ'), ('एै', 'ऐ'), ('एे', 'ए'), ('इ' + _REPH, 'ई')):
        t = t.replace(a, b)
    t = re.sub('(ण|ष|क्ष|ञ)्ा', lambda m: m.group(1), t)  # half forms with no full key: half form plus the aa stem is the bare letter
    t = re.sub('्([ािीुूृेैोौ])', lambda m: m.group(1), t)  # a half form followed by a vowel sign is a typing slip (0f is णा)
    # short i matra (typed before the consonant) goes after the whole conjunct
    t = re.sub(r'ि((?:[क-ह]्)*[क-ह])', r'\1ि', t)
    # reph typed after the syllable goes before its conjunct
    def _reph(m):
        return 'र्' + m.group(1) + m.group(2)
    t = re.sub('((?:[क-ह]्)*[क-ह])([' + _MATRA + ']*)' + _REPH, _reph, t)
    t = t.replace(_REPH, 'र्')
    t = re.sub('([िी])ा', lambda m: m.group(1), t)  # stray aa stem after an i sign
    t = re.sub('([ािीुूृेैोौ])(्र)', lambda m: m.group(2) + m.group(1), t)  # rakar goes before the vowel sign
    t = re.sub('([ािीुूृेैोौ])[ािीुूृेैोौ]+', lambda m: m.group(1), t)  # doubled vowel signs are typing slips
    t = re.sub(r'\s+', ' ', t).strip()
    return t


_V = {'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'}
_M = {'ा': 'A', 'ि': 'i', 'ी': 'i', 'ु': 'u', 'ू': 'u', 'ृ': 'ri', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au'}
_C = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng', 'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'n', 'ट': 't',
      'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n', 'प': 'p', 'फ': 'ph',
      'ब': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h'}
_DIG = dict(zip('०१२३४५६७८९', '0123456789'))
_LONG = ('aa', 'A', 'e', 'o', 'ai', 'au')


def _word_to_roman(w):
    # tokens: (roman consonant or vowel, kind)
    toks = []
    i = 0
    while i < len(w):
        ch = w[i]
        if ch in _C or ch == 'क' or ch == 'त' or ch == 'ज':
            if ch == 'क' and i + 2 < len(w) and w[i + 1] == '्' and w[i + 2] == 'ष':
                base, step = 'ksh', 3
            elif ch == 'त' and i + 2 < len(w) and w[i + 1] == '्' and w[i + 2] == 'र':
                base, step = 'tr', 3
            elif ch == 'ज' and i + 2 < len(w) and w[i + 1] == '्' and w[i + 2] == 'ञ':
                base, step = 'gy', 3
            else:
                base, step = _C[ch], 1
            j = i + step
            if j < len(w) and w[j] == '्':
                toks.append([base, 'h'])  # halant, no vowel
                i = j + 1
            elif j < len(w) and w[j] in _M:
                toks.append([base, 'c'])
                toks.append([_M[w[j]], 'v'])
                i = j + 1
            else:
                toks.append([base, 'ca'])  # consonant with inherent a
                i = j
        elif ch in _V:
            toks.append([_V[ch], 'v'])
            i += 1
        elif ch in 'ंँ':
            toks.append(['n', 'h'])
            i += 1
        elif ch == 'ः':
            toks.append(['h', 'h'])
            i += 1
        elif ch in _DIG:
            toks.append([_DIG[ch], 'd'])
            i += 1
        else:
            toks.append([ch, 'o'])
            i += 1
    # schwa deletion: word final, and after a long vowel before another consonant + vowel (Rampur, not Ramapur)
    for k, t in enumerate(toks):
        if t[1] != 'ca':
            continue
        last = all(x[1] in ('o', 'd') for x in toks[k + 1:]) and not (k > 0 and toks[k - 1][1] == 'h') and t[0] != 'y'
        prev_long = k > 0 and toks[k - 1][1] == 'v' and toks[k - 1][0] in _LONG
        nxt = toks[k + 1] if k + 1 < len(toks) else None
        nxt2 = toks[k + 2] if k + 2 < len(toks) else None
        syl = sum(1 for x in toks[:k] if x[1] in ('v', 'cv', 'cx'))
        mid = syl == 1 and prev_long and nxt is not None and nxt[1] in ('c', 'ca') and (nxt2 is not None and nxt2[1] in ('v', 'ca', 'c', 'h'))
        t[1] = 'cx' if (last or mid) else 'cv'
    out = []
    for t in toks:
        if t[1] == 'cv':
            out.append(t[0] + 'a')
        else:
            out.append(t[0])
    s = ''.join(out)
    return s.replace('A', 'a').replace('aaa', 'aa')


_FIX = [('विदा', 'विद्या'), ('विदालय', 'विद्यालय'), ('राष्टिय', 'राष्ट्रिय'), ('आर्दश', 'आदर्श'), ('गणोश', 'गणेश'), ('ई.बो.मा.वि', ' English Boarding Secondary School '),
        ('इ.बो.मा.वि', ' English Boarding Secondary School '), ('ई.वो.मा.वि', ' English Boarding Secondary School '),
        ('बो.मा.वि', ' Boarding Secondary School '), ('वो.मा.वि', ' Boarding Secondary School '), ('आ.मा.वि', ' Secondary School '),
        ('ने.रा.मा.वि', ' Nepal Rastriya Secondary School ')]
_WORDS = {
    'स्कुल': 'School', 'स्कूल': 'School', 'एकेडेमी': 'Academy', 'एकाडेमी': 'Academy', 'एकेडमी': 'Academy', 'क्याम्पस': 'Campus', 'कलेज': 'College',
    'पब्लिक': 'Public', 'बोर्डिङ': 'Boarding', 'बोर्डिङ्ग': 'Boarding', 'बोडिङ्ग': 'Boarding', 'वोर्डिङ': 'Boarding', 'बोडिङ': 'Boarding',
    'इन्टरनेशनल': 'International', 'न्यू': 'New', 'मेमोरियल': 'Memorial', 'इङ्गलिस': 'English', 'इङलिस': 'English', 'ईङ्गलिस': 'English',
    'इङ्लिस': 'English', 'इङ्लिश': 'English', 'सेकेण्डरी': 'Secondary', 'सेकेन्डरी': 'Secondary', 'मोडेल': 'Model', 'मोर्डन': 'Modern',
    'नेशनल': 'National', 'स्टार': 'Star', 'लिटिल': 'Little', 'एजुकेशन': 'Education', 'एजुकेशनल': 'Educational', 'साइन्स': 'Science',
    'माउण्ट': 'Mount', 'माउन्ट': 'Mount', 'एण्ड': 'and', 'ग्लोबल': 'Global', 'ग्यालेक्सी': 'Galaxy', 'भिजन': 'Vision', 'सनराइज': 'Sunrise',
    'होराइजन': 'Horizon', 'ब्राइट': 'Bright', 'युनाइटेड': 'United', 'गोल्डेन': 'Golden', 'चिल्ड्रेन': 'Children', 'गार्डेन': 'Garden',
    'मेरीगोल्ड': 'Marigold', 'वर्ल्ड': 'World', 'नोवेल': 'Novel', 'प्वाइन्ट': 'Point', 'लाइट': 'Light', 'एभरेष्ट': 'Everest',
    'हिमालयन': 'Himalayan', 'सेन्ट': 'Saint', 'अंग्रेजी': 'English', 'अङ्ग्रेजी': 'English', 'आवासीय': 'Residential', 'आवासिय': 'Residential',
    'माध्यमिक': 'Secondary', 'सामुदायिक': 'Community', 'बहुमुखी': 'Multiple', 'संस्कृत': 'Sanskrit', 'कन्या': 'Kanya', 'श्री': 'Shree',
    'क्याम्पस,': 'Campus,', 'नमूना': 'Namuna', 'नमुना': 'Namuna', 'सैनिक': 'Sainik', 'गुरुकुल': 'Gurukul', 'विद्यालय': 'Vidyalaya',
    'ब.क्याम्पस': 'Campus', 'पोखरा': 'Pokhara', 'काठमाडौं': 'Kathmandu', 'काठमाण्डौ': 'Kathmandu', 'चितवन': 'Chitwan',
}

_ABBR = [
    ('उ.मा.वि', 'Higher Secondary School'), ('नि.मा.वि', 'Lower Secondary School'), ('मा.वि', 'Secondary School'),
    ('आ.वि', 'Basic School'), ('प्रा.वि', 'Primary School'), ('उ.मा.वि.', 'Higher Secondary School'),
]


def to_roman(text):
    """Roman spelling of a Devanagari school name or address. School type abbreviations become English words."""
    t = text
    for a, b in _FIX:
        t = t.replace(a + '.', b).replace(a, b)
    for a, b in sorted(_ABBR, key=lambda x: -len(x[0])):
        t = t.replace(a + '.', ' ' + b + ' ').replace(a, ' ' + b + ' ')
    parts = []
    for w in re.split(r'(\s+|[,()\-/])', t):
        if not w or w.isspace() or w in ',()-/':
            parts.append(w)
        elif re.fullmatch(r'[A-Za-z .]+', w):
            parts.append(w)
        elif w in _WORDS:
            parts.append(_WORDS[w])
        else:
            parts.append(_word_to_roman(w))
    s = ''.join(parts)
    s = re.sub(r'\s+', ' ', s).strip(' ,-')
    s = re.sub(r'\s*,\s*', ', ', s)
    return ' '.join(x if x[:1].isupper() else x.capitalize() for x in s.split(' '))
