/* v3 resource thumbnails: the `thumb` kind of the art library (still-life objects on calm M3X backdrops), picked for a real resource.
   Same recipe in js/v3-thumb.js (web) and ui/components/v3art/V3Thumb.kt (app): change one, change both.
   Left out on purpose: scenes (sun, moon, hills, mountains, forests, trees, skylines) and the buildings and peaks among the objects. */
(function (g) {
  'use strict';
  var A = g.NebArtV3;
  /* subject -> [palette, study objects] (the same table as v3-catalog.js) */
  var SUB = {
    'Physics': ['brand', ['atom', 'magnet', 'telescope']],
    'Chemistry': ['aqua', ['flask', 'atom', 'leaf']],
    'Biology': ['emerald', ['dna', 'sprout', 'leaf']],
    'Mathematics': ['cobalt', ['compass', 'abacus', 'chart']],
    'Computer Science': ['sky', ['laptop', 'gear', 'bulb']],
    'English': ['coral', ['books', 'pencil', 'notebook']],
    'Nepali': ['rose', ['pencil', 'notebook', 'pagoda']],
    'Accountancy': ['teal', ['calculator', 'chart', 'abacus']],
    'Economics': ['amber', ['chart', 'scales', 'calculator']],
    'Business Studies': ['marigold', ['chart', 'backpack', 'bulb']],
    'Social Studies': ['sky', ['globe', 'books', 'pagoda']],
    'Geography': ['moss', ['globe', 'compass', 'summit']],
    'History': ['terracotta', ['stupa', 'pagoda', 'doc']],
    'Environment': ['mint', ['leaf', 'sprout', 'plant']],
    'Hotel Management': ['marigold', ['bell', 'notebook', 'plant']],
    'Law': ['slate', ['scales', 'shield', 'doc']],
    'Political Science': ['brand', ['scales', 'doc', 'globe']],
    'Sociology': ['sky', ['globe', 'backpack', 'books']],
    'Psychology': ['rose', ['bulb', 'pulse', 'notebook']],
    'Education': ['denim', ['cap', 'books', 'backpack']],
    'Music': ['coral', ['music', 'bell', 'palette']],
    'Health & Nursing': ['crimson', ['pulse', 'flask', 'shield']],
    'Statistics': ['teal', ['chart', 'calculator', 'compass']],
    'Engineering': ['terracotta', ['gear', 'compass', 'laptop']],
    'Agriculture': ['lime', ['sprout', 'plant', 'leaf']],
    'Space & Astronomy': ['cobalt', ['rocket', 'planet', 'telescope']],
    'BCA & Software': ['brand', ['laptop', 'gear', 'bulb']],
    'Medicine & Entrance': ['emerald', ['pulse', 'flask', 'dna']],
    'Architecture': ['amber', ['pagoda', 'compass', 'gear']],
    'Nepal Heritage': ['sand', ['stupa', 'pagoda', 'summit']],
    'Art & Design': ['coral', ['palette', 'pencil', 'plane']],
    'Career Pathways': ['pine', ['plane', 'summit', 'backpack']],
    'Study Skills': ['denim', ['clock', 'notebook', 'bulb']],
    'Exam Prep': ['marigold', ['trophy', 'clock', 'pencil']],
  };
  var NO_OBJ = { pagoda: 1, stupa: 1, summit: 1 };
  var FILL = ['books', 'notebook', 'bulb', 'pencil', 'clock', 'chart'];
  var STYLES = ['disc', 'plate', 'arch', 'pattern', 'disc', 'plate'];
  /* v3 subject <- words found in a resource's subject text. First match wins; an array value is a pool picked by the hash. */
  var KW = [
    ['Health & Nursing', ['health', 'nursing', 'physical education', 'phy. edu', 'hpe', 'nutrition', 'yoga', 'sport', 'fitness', 'medical', 'स्वास्थ्य']],
    ['Medicine & Entrance', ['medicine', 'mbbs', 'entrance', 'pharmac']],
    ['Physics', ['physics', 'भौतिक']], ['Chemistry', ['chemistry', 'chemical', 'रसायन']],
    ['Biology', ['biology', 'botany', 'zoology', 'microbio', 'anatomy', 'genetic', 'जीव']],
    ['Statistics', ['statistic']], ['Mathematics', ['math', 'algebra', 'geometry', 'trigonometry', 'calculus', 'गणित']],
    ['BCA & Software', ['bca', 'software']],
    ['Computer Science', ['computer', 'programming', 'informatics', 'information tech', 'digital', 'coding', 'algorithm', 'database', 'web dev']],
    ['Engineering', ['engineering']], ['Architecture', ['architect']], ['Agriculture', ['agricultur', 'farm']],
    ['Space & Astronomy', ['astronom', 'space']], ['Accountancy', ['account', 'book keeping', 'bookkeeping', 'audit']],
    ['Economics', ['economic', 'अर्थ']], ['Business Studies', ['business', 'finance', 'commerce', 'marketing', 'banking', 'management']],
    ['Hotel Management', ['hotel', 'hospitality', 'tourism']], ['Geography', ['geograph', 'population']], ['History', ['history']],
    ['Political Science', ['political']], ['Sociology', ['sociolog']], ['Psychology', ['psycholog']],
    ['Social Studies', ['social', 'civic', 'culture', 'सामाजिक', 'अध्ययन']], ['Environment', ['environment', 'ecolog']],
    ['Law', ['legal', 'constitution', 'jurisprudence']], ['Music', ['music']], ['Art & Design', ['design', 'drawing', 'painting']],
    ['Nepali', ['nepali', 'sanskrit', 'hindi', 'maithili', 'newari', 'नेपाली']], ['English', ['english', 'grammar', 'literature', 'writing', 'अंग्रेजी', 'साहित्य']],
    ['Education', ['education', 'teaching', 'pedagog']],
    [['Physics', 'Chemistry', 'Biology'], ['science', 'laboratory', 'विज्ञान']],
    ['Exam Prep', ['exam', 'model paper', 'model set', 'past paper', 'question bank', 'mock', 'revision', 'pyq']],
    ['Study Skills', ['study', 'skill', 'tips']]
  ];
  var GENERIC = ['Education', 'Study Skills', 'Exam Prep', 'English', 'Mathematics', 'Social Studies'];

  function pal(base, k) { var P = A.palettes; return k % 3 === 0 ? base : P[(P.indexOf(base) + (k % 3) * 7 + k) % P.length]; }

  A.thumbTables = { SUB: SUB, KW: KW, GENERIC: GENERIC, FILL: FILL, STYLES: STYLES, NO_OBJ: NO_OBJ };

  A.thumbPick = function (seed, subject) {
    var h = A.hash('v3thumb|' + seed + '|' + subject), s = (subject || '').toLowerCase(), name = null, i, j, pool;
    for (i = 0; i < KW.length && !name; i++) for (j = 0; j < KW[i][1].length; j++) if (s.indexOf(KW[i][1][j]) >= 0) { pool = KW[i][0]; name = typeof pool === 'string' ? pool : pool[(h >>> 12) % pool.length]; break; }
    if (!name) name = GENERIC[(h >>> 12) % GENERIC.length];
    var d = SUB[name], list = d[1].filter(function (o) { return !NO_OBJ[o]; });
    for (i = 0; list.length < 3; i++) if (list.indexOf(FILL[i]) < 0) list.push(FILL[i]);
    var rot = (h >>> 3) % 3, k = (h >>> 6) % 9;
    return { id: 'rt' + h, seed: 0, engine: 'still', subj: name, palette: pal(d[0], k), o: { objs: [list[rot], list[(rot + 1) % 3], list[(rot + 2) % 3]], style: STYLES[(h >>> 10) % 6] } };
  };

  /* aspect = box width / height (steps of 0.05, 0.6 to 4); the drawing is built for the box, so nothing is cropped */
  A.thumbFit = function (aspect) { return Math.max(0.6, Math.min(4, Math.round((aspect || 2.5) * 20) / 20)); };
  A.thumb = function (seed, subject, aspect, mode) {
    var s = A.thumbPick(seed, subject);
    s.h = 256; s.w = Math.round(256 * A.thumbFit(aspect)); s.mode = mode; s.kind = 'thumb';
    return A.make(s);
  };
})(typeof window !== 'undefined' ? window : globalThis);
