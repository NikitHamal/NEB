// Every product string and number in the film, in one place, with asserts so the story stays true
// in every frame: the post is the question the hook asked, the answer comes from the teacher, the
// GPA is the mean of the grades shown, the read count only climbs.
export const QUESTION = { subject: 'Chemistry', klass: 'Class 11', text: 'Why is the 2nd ionisation energy higher?', author: 'Asha', initial: 'A' };

export const REPLIES = [
  { name: 'Rohan', initial: 'R', role: 'Class 11', text: 'The electrons left feel the nucleus more.' },
  { name: 'Sita', initial: 'S', role: 'Class 12', text: 'Same in our book, chapter 3.' },
  { name: 'Ms. Pandey', initial: 'P', role: 'Teacher', text: 'Once one leaves, the rest are held tighter.' },
];
export const ANSWER_INDEX = 2;

export const RESOURCES = [
  { kind: 'Notes', title: 'Ionisation energy', meta: 'Chemistry · Class 11' },
  { kind: 'Past paper', title: 'NEB 2080', meta: 'Chemistry · Class 11' },
  { kind: 'Solved book', title: 'Physical chemistry', meta: 'Every exercise solved' },
];

export const LEVELS = ['School', 'Plus two', 'Diploma', "Bachelor's", "Master's", 'Entrance'];

export const READER = { book: 'Chemistry 11', page: 84, pages: 275, heading: '3.2 Ionisation energy', answer: ['Fewer electrons,', 'held more tightly.'] };

export const GRADES = [
  { subject: 'English', grade: 'A', gp: 3.6 },
  { subject: 'Nepali', grade: 'B+', gp: 3.2 },
  { subject: 'Maths', grade: 'A', gp: 3.6 },
  { subject: 'Physics', grade: 'A', gp: 3.6 },
  { subject: 'Chemistry', grade: 'A+', gp: 4.0 },
  { subject: 'Biology', grade: 'A', gp: 3.6 },
];
export const HERO_GRADE = 4; // Chemistry: the subject the whole film was stuck on
export const GPA = Math.round((GRADES.reduce((s, g) => s + g.gp, 0) / GRADES.length) * 100) / 100;

export const UPLOAD = { file: 'Ionisation notes.pdf', by: 'Asha', steps: ['Uploaded', 'Checked by a moderator', 'Published'], readers: 1240 };

export const URL = 'nebians.consica.com.np';

// --- asserts: the film refuses to render a story that contradicts itself
const fail = (m: string) => { throw new Error(`data: ${m}`); };
if (REPLIES[ANSWER_INDEX].role !== 'Teacher') fail('the marked answer must be the teacher’s');
if (GRADES[HERO_GRADE].subject !== QUESTION.subject) fail('the hero bar must be the subject of the question');
if (GRADES[HERO_GRADE].gp !== Math.max(...GRADES.map((g) => g.gp))) fail('the hero bar must be the tallest');
if (Math.abs(GPA - 3.6) > 0.001) fail(`GPA is ${GPA}, the film says 3.60`);
if (UPLOAD.by !== QUESTION.author) fail('the student who asked is the one who passes it on');
if (RESOURCES[0].meta !== `${QUESTION.subject} · ${QUESTION.klass}`) fail('the first resource is for the question’s subject');
