/* Sample people. Names and numbers are invented for the concept. */
(function () {
  function R(by, shape, tone, rows) {
    return rows.map(function (r, i) { return { title: r[0], subject: r[1], type: r[2], meta: r[3], views: r[4], when: r[5], seed: r[6] || (i + 3) * 7, by: by, shape: shape, tone: tone }; });
  }
  function P(cat, title, body, likes, comments, views, when, o) { o = o || {}; return { cat: cat, title: title, body: body, likes: likes, comments: comments, views: views, when: when, pin: o.pin, liked: o.liked }; }
  var D = window.PROFILES = {};

  D.student = {
    id: 'student', label: 'Student', name: 'Aarav Sharma', user: 'aarav.sharma', letter: 'A', shape: 'cookie', tone: 't1', verified: false,
    role: { icon: 'school', label: 'Student' }, headline: 'Grade 12 Science. Physics is the fun one, Chemistry is the long one.',
    meta: [{ i: 'location_on', t: 'Kathmandu' }, { i: 'apartment', t: 'Everest Valley Secondary', link: 1 }, { i: 'calendar_month', t: 'Joined Jan 2025' }],
    cover: { kind: 'cover', seed: 41, palette: 'azure', layout: 'graph' },
    nums: [['318', 'Followers'], ['142', 'Following'], ['64', 'Posts', 'posts'], ['27', 'Resources', 'resources']],
    tabs: [['overview', 'Overview', 'dashboard'], ['posts', 'Posts', 'forum', 64], ['resources', 'Resources', 'folder_open', 27], ['replies', 'Replies', 'reply', 212], ['portfolio', 'Portfolio', 'work', 5], ['progress', 'Progress', 'monitoring'], ['saved', 'Saved', 'bookmark', 38, 1]],
    openTo: [{ i: 'diversity_3', t: 'Study partner', d: 'Physics, evenings', c: 1 }, { i: 'swap_horiz', t: 'Swapping notes', d: 'Chemistry for Maths', c: 2 }, { i: 'psychology_alt', t: 'Doubt solving', d: 'Grade 11 and 12', c: 3 }, { i: 'quiz', t: 'Mock tests', d: 'Weekly, Sunday', c: 4 }],
    glance: [{ i: 'visibility', n: '12.4k', l: 'Reads on my notes', c: 1 }, { i: 'check_circle', n: '86', l: 'Answers', c: 2 }, { i: 'local_fire_department', n: '9', l: 'Day streak', c: 3 }],
    studying: { subject: 'Physics', title: 'Current electricity', ch: 7, total: 12, exam: 'Boards in 64 days', today: '42 min today', streak: 9, week: [3, 5, 2, 6, 4, 7, 5], res: 'Grade 12 Physics, Unit 7 notes', seed: 12 },
    pinned: P('Physics', 'How I finally understood Kirchhoff in one evening', 'Draw the loop first, label every current, and only then write equations. Three worked examples and the mistakes I kept making are in the attached notes.', 148, 23, '2.1k', '3d ago', { pin: 1, liked: 1 }),
    posts: [P('Chemistry', 'Is there a trick for remembering the reactivity series?', 'I keep mixing up zinc and aluminium. What do you all use?', 41, 17, '630', '1d ago'), P('Maths', 'Integration by parts, a checklist', 'LIATE helps, but it is not a law. Here is when it breaks and what to try instead.', 96, 12, '1.2k', '5d ago')],
    resources: R('Aarav Sharma', 'cookie', 't1', [['Grade 12 Physics, Unit 7 notes', 'Physics', 'Notes', 'Grade 12, PDF, 3.2 MB', '4.8k', '2d ago', 12], ['Organic chemistry reaction map', 'Chemistry', 'Cheat sheet', 'Grade 12, PDF, 1.1 MB', '2.9k', '1w ago', 55], ['Maths formula deck', 'Mathematics', 'Notes', 'Grade 12, PDF, 900 KB', '3.3k', '2w ago', 71], ['English essay bank', 'English', 'Notes', 'Grade 12, PDF, 2 MB', '1.4k', '3w ago', 90]]),
    replies: [['Why is the current the same in a series circuit?', 'Because charge cannot pile up anywhere, so what enters one point must leave it.', 'Answer'], ['What is the difference between emf and potential difference?', 'Emf is the energy given per charge by the source. Terminal voltage is what is left after the internal drop.', 'Helpful']],
    portfolio: [['science', 'Science fair, second place', 'Kathmandu district, 2025', 'c1'], ['code', 'Weather station with Arduino', 'Project, 2025', 'c4'], ['groups', 'Physics club, secretary', 'School, 2025 to now', 'c2']],
    skills: ['Problem solving', 'Note taking', 'Arduino', 'Python'],
    achievements: [['workspace_premium', 'First 100 reads'], ['verified', 'Top answer'], ['local_fire_department', '7 day streak'], ['auto_stories', 'Note author'], ['groups', 'Study group'], ['bolt', 'Physics 10']]
  };

  D.teacher = {
    id: 'teacher', label: 'Teacher', name: 'Sushmita Karki', user: 'sushmita.karki', letter: 'S', shape: 'sunny', tone: 't2', verified: true,
    role: { icon: 'cast_for_education', label: 'Teacher' }, headline: 'Physics teacher, 11 years. I write notes the way I explain them in class.',
    meta: [{ i: 'location_on', t: 'Lalitpur' }, { i: 'apartment', t: 'Lalitpur Science Academy', link: 1 }, { i: 'history_edu', t: '11 years teaching' }],
    cover: { kind: 'cover', seed: 17, palette: 'teal', layout: 'orbit' }, contact: { phone: '+977 98410 55218', hours: 'Sun to Fri, 4 pm to 7 pm' },
    nums: [['4.2k', 'Followers'], ['58', 'Following'], ['186', 'Answers', 'answers'], ['43', 'Resources', 'resources']],
    tabs: [['overview', 'Overview', 'dashboard'], ['teaches', 'Teaches', 'menu_book', 4], ['resources', 'Resources', 'folder_open', 43], ['posts', 'Posts', 'forum', 31], ['answers', 'Answers', 'verified', 186], ['schools', 'Schools', 'apartment', 3], ['earnings', 'Earnings', 'payments', null, 1]],
    openTo: [{ i: 'co_present', t: 'Guest lectures', d: 'Schools in Lalitpur', c: 4 }, { i: 'rate_review', t: 'Reviewing notes', d: 'Physics, free', c: 2 }, { i: 'support_agent', t: 'Doubt sessions', d: 'Saturdays', c: 1 }, { i: 'groups', t: 'Collaboration', d: 'Question banks', c: 3 }],
    glance: [{ i: 'visibility', n: '96k', l: 'Reads', c: 4 }, { i: 'verified', n: '186', l: 'Accepted answers', c: 2 }, { i: 'groups', n: '1.9k', l: 'Students helped', c: 3 }],
    teaches: [['bolt', 'Physics', 'Grade 11 and 12', 'c1', 'Physics'], ['functions', 'Mathematics', 'Grade 11', 'c3', 'Mathematics'], ['science', 'Science', 'Grade 9 and 10', 'c2', 'Chemistry'], ['rocket_launch', 'Astronomy club', 'All grades', 'c4', 'Space Science']],
    pinned: P('Physics', 'Numericals that appear every year in Grade 12 Physics', 'I went through nine years of NEB papers. These twelve numerical types cover almost half the marks. Notes and solutions are attached.', 612, 88, '14k', '1w ago', { pin: 1 }),
    posts: [P('Teaching', 'A 10 minute demo for electromagnetic induction', 'A magnet, a copper pipe and a phone timer. Students remember it for years.', 233, 31, '4k', '2d ago'), P('Exam', 'How to write a five mark answer', 'State, derive, conclude. Examiners reward structure before they reward length.', 188, 22, '3.2k', '1w ago')],
    resources: R('Sushmita Karki', 'sunny', 't2', [['Grade 12 Physics, complete notes', 'Physics', 'Notes', 'Grade 12, PDF, 14 MB', '38k', '1mo ago', 8], ['Optics numerical bank', 'Physics', 'Question bank', 'Grade 12, PDF, 4 MB', '19k', '2mo ago', 22], ['Grade 11 Maths, limits and derivatives', 'Mathematics', 'Notes', 'Grade 11, PDF, 6 MB', '9.8k', '3mo ago', 61], ['Model paper set 2082', 'Physics', 'Model paper', 'Grade 12, PDF, 2 MB', '12k', '4mo ago', 33]]),
    answers: [['Why does the sky appear blue but sunsets red?', 'Short wavelengths scatter far more, so overhead we see blue. At sunset the light travels through more air and the blue is scattered out.', 'Accepted'], ['Difference between speed and velocity in circular motion?', 'Speed stays constant, the direction of velocity keeps changing, so velocity is not constant.', 'Helpful']],
    schools: [['Lalitpur Science Academy', 'Physics teacher, 2019 to now', 'apartment', 'c1'], ['Patan Model College', 'Visiting faculty, 2016 to 2019', 'apartment', 'c6'], ['Bright Future School', 'Physics teacher, 2014 to 2016', 'apartment', 'c6']],
    achievements: [['workspace_premium', 'Top teacher 2025'], ['verified', 'Verified teacher'], ['auto_stories', '40 resources'], ['groups', '1k students'], ['bolt', 'Physics 10'], ['star', '4.9 rating']]
  };

  D.institution = {
    id: 'institution', label: 'Institution', name: 'Lalitpur Science Academy', user: 'lsa.edu.np', letter: 'L', shape: 'squircle', tone: 't3', verified: true,
    role: { icon: 'apartment', label: 'School' }, headline: 'Plus Two Science and Management. Admissions for 2083 are open.',
    meta: [{ i: 'location_on', t: 'Jawalakhel, Lalitpur' }, { i: 'language', t: 'lsa.edu.np', link: 1 }, { i: 'calendar_month', t: 'Since 2058' }],
    cover: { kind: 'school', seed: 8, palette: 'azure', layout: 'arches' }, contact: { phone: '+977 01 5521 340', hours: 'Sun to Fri, 9 am to 5 pm' },
    nums: [['1.2k', 'Followers'], ['64', 'Teachers', 'teachers'], ['18', 'Programs', 'programs'], ['212', 'Resources', 'resources']],
    tabs: [['overview', 'Overview', 'dashboard'], ['notices', 'Notices', 'campaign', 7], ['programs', 'Programs', 'school', 4], ['teachers', 'Teachers', 'groups', 64], ['gallery', 'Gallery', 'photo_library', 48], ['resources', 'Resources', 'folder_open', 212], ['posts', 'Posts', 'forum', 52]],
    openTo: [{ i: 'how_to_reg', t: 'Admissions 2083', d: 'Science and Management', c: 2 }, { i: 'badge', t: 'Hiring', d: '2 physics, 1 english', c: 1 }, { i: 'tour', t: 'Campus visits', d: 'Saturdays', c: 3 }, { i: 'redeem', t: 'Scholarships', d: 'Top 10 percent', c: 4 }],
    glance: [{ i: 'trending_up', n: '94%', l: 'Pass rate', c: 2 }, { i: 'emoji_events', n: '31', l: 'GPA 4.0 last year', c: 3 }, { i: 'groups', n: '820', l: 'Students', c: 1 }],
    notices: [['how_to_reg', 'Admission form for 2083 is open', 'Closes on 15 Baisakh', 'Admissions', 'g'], ['event', 'Pre-board exam routine', 'Starts 10 Chaitra, Grade 12', 'Exam', 'y'], ['celebration', 'Annual science fair', 'Open to all schools', 'Event', 't']],
    programs: [['Plus Two Science', 'Physics, Chemistry, Biology or Computer', '2 years, 120 seats', 'science', 'c1'], ['Plus Two Management', 'Accountancy, Economics, Business', '2 years, 80 seats', 'payments', 'c3'], ['Grade 11 bridge course', 'Maths and English for SEE graduates', '2 months', 'trending_up', 'c4'], ['NEB crash course', 'Revision for Grade 12', '6 weeks', 'bolt', 'c5']],
    teachers: [['Sushmita Karki', 'Physics', 'S', 'sunny', 't2'], ['Dipesh Rana', 'Mathematics', 'D', 'flower', 't1'], ['Anita Joshi', 'English', 'A', 'cookie', 't4'], ['Rajan Shrestha', 'Chemistry', 'R', 'squircle', 't5']],
    pinned: P('Admissions', 'Admission 2083 is open, with scholarships for the top 10 percent', 'Forms are available at the front desk and online. Entrance test every Saturday at 10 am. Call the office for a campus visit.', 204, 41, '9k', '2d ago', { pin: 1 }),
    posts: [P('Result', 'Our Grade 12 results, 31 students scored GPA 4.0', 'Congratulations to every student and teacher. Full list is in the notices tab.', 540, 62, '12k', '3w ago')],
    resources: R('Lalitpur Science Academy', 'squircle', 't3', [['Pre-board Physics paper 2082', 'Physics', 'Model paper', 'Grade 12, PDF, 1 MB', '8.4k', '1w ago', 2], ['Chemistry lab manual', 'Chemistry', 'Notes', 'Grade 12, PDF, 5 MB', '4.1k', '1mo ago', 14], ['Accountancy practice set', 'Accountancy', 'Question bank', 'Grade 12, PDF, 3 MB', '3.6k', '2mo ago', 44], ['English grammar workbook', 'English', 'Notes', 'Grade 11, PDF, 2 MB', '2.2k', '3mo ago', 77]]),
    facilities: [['science', 'Science labs'], ['local_library', 'Library'], ['computer', 'Computer lab'], ['sports_basketball', 'Sports ground'], ['directions_bus', 'School bus'], ['restaurant', 'Canteen']]
  };

  D.contributor = {
    id: 'contributor', label: 'Contributor', name: 'Prakash Neupane', user: 'prakash.neupane', letter: 'P', shape: 'flower', tone: 't4', verified: true,
    role: { icon: 'edit_note', label: 'Contributor' }, headline: 'I turn textbooks into clean notes and books. Management and Humanities first.',
    meta: [{ i: 'location_on', t: 'Pokhara' }, { i: 'link', t: 'prakash.np', link: 1 }, { i: 'calendar_month', t: 'Joined Aug 2024' }],
    cover: { kind: 'cover', seed: 29, palette: 'amber', layout: 'stack' },
    nums: [['8.9k', 'Followers'], ['34', 'Following'], ['96', 'Resources', 'resources'], ['7', 'Books', 'books']],
    tabs: [['overview', 'Overview', 'dashboard'], ['resources', 'Resources', 'folder_open', 96], ['books', 'Books', 'auto_stories', 7], ['collections', 'Collections', 'collections_bookmark', 9], ['posts', 'Posts', 'forum', 22], ['impact', 'Impact', 'monitoring'], ['studio', 'Studio', 'dashboard_customize', null, 1]],
    openTo: [{ i: 'edit_note', t: 'Requests', d: 'Notes on a topic', c: 3 }, { i: 'handshake', t: 'Collaboration', d: 'Co-author books', c: 1 }, { i: 'rate_review', t: 'Feedback', d: 'On drafts', c: 2 }, { i: 'translate', t: 'Translation', d: 'Nepali to English', c: 4 }],
    glance: [{ i: 'visibility', n: '212k', l: 'Total reads', c: 3 }, { i: 'download', n: '48k', l: 'Downloads', c: 1 }, { i: 'bookmark', n: '9.6k', l: 'Saves', c: 2 }],
    pinned: P('Notes', 'Accountancy in 30 pages, all journal entries in one place', 'Every entry type with the rule, a worked example and the common trap. Free, no sign up. Corrections are welcome in the comments.', 884, 120, '31k', '2w ago', { pin: 1 }),
    posts: [P('Books', 'New book out: Economics made simple', 'Twelve chapters, each with a one page summary. Print-friendly.', 322, 47, '8k', '4d ago')],
    resources: R('Prakash Neupane', 'flower', 't4', [['Accountancy in 30 pages', 'Accountancy', 'Notes', 'Grade 12, PDF, 4 MB', '31k', '2w ago', 5], ['Economics made simple', 'Economics', 'Book', 'Grade 11, PDF, 8 MB', '22k', '4d ago', 19], ['Business Studies case files', 'Business Studies', 'Question bank', 'Grade 12, PDF, 6 MB', '15k', '2mo ago', 37], ['Sociology short notes', 'Sociology', 'Notes', 'Grade 11, PDF, 2 MB', '7k', '3mo ago', 48]]),
    books: [['Accountancy in 30 pages', 'Accountancy', '12k reads'], ['Economics made simple', 'Economics', '22k reads'], ['Business case files', 'Business Studies', '15k reads'], ['Sociology short notes', 'Sociology', '7k reads'], ['Statistics for Grade 12', 'Statistics', '5k reads'], ['Law basics', 'Law', '3k reads']],
    collections: [['Management Grade 12', 'Accountancy', 14], ['Humanities Grade 11', 'Sociology', 11], ['Model papers', 'Economics', 18], ['Case studies', 'Business Studies', 9]],
    impact: [14, 22, 18, 30, 26, 41, 38, 52, 47, 63, 58, 72]
  };
})();
