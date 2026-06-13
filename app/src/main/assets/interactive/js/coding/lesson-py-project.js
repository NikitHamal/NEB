import { createPyLesson } from './py-console.js';

const STARTER = [
  '# FINAL QUEST: NEB Grade Calculator',
  '# Marks -> Letter grade, just like real NEB results!',
  '#',
  '#   90+ : A+      80-89 : A      70-79 : B+',
  '#   60-69 : B     50-59 : C+     40-49 : C',
  '#   below 40 : NG',
  '',
  'marks = [78, 92, 85, 64, 49]',
  '',
  '# Step 1: write grade(m) that returns the letter for a mark',
  'def grade(m):',
  '    if m >= 90:',
  '        return "A+"',
  '    # add elif lines for the other grades...',
  '    return "NG"',
  '',
  '# Step 2: write average(nums) -> sum of list / how many',
  '',
  '# Step 3: loop over marks and print each with its grade,',
  '#         like:  78 -> B+',
  '',
  '# Step 4: print the average at the end with an f-string',
].join('\n');

function noComments(src) {
  return src.replace(/#[^\n]*/g, '');
}

function lastLine(res) {
  return res && res.ok && res.output.length ? res.output[res.output.length - 1] : null;
}

export default function init(stage) {
  return createPyLesson(stage, {
    starter: STARTER,
    intro: 'The Final Quest! Build a real NEB grade calculator: a grade() function, an average() function, and a neat report. Follow the steps — I\'ll verify each one with secret tests!',
    allDoneLine: 'QUEST COMPLETE! You built a genuine, working grade calculator from scratch. From print() to full programs — you\'ve earned the title of Python Programmer!',
    errorLines: [
      'An error in the quest! Check the red line — every if/elif needs a colon and an indented body.',
      'Almost! Read the error message: Python always tells you which line confused it.',
    ],
    goals: [
      {
        label: 'grade(95) returns A+ and grade(85) returns A',
        test: ({ run }) => lastLine(run('print(grade(95))')) === 'A+' && lastLine(run('print(grade(85))')) === 'A',
      },
      {
        label: 'grade() knows all bands (72→B+, 65→B, 55→C+, 45→C)',
        test: ({ run }) =>
          lastLine(run('print(grade(72))')) === 'B+' &&
          lastLine(run('print(grade(65))')) === 'B' &&
          lastLine(run('print(grade(55))')) === 'C+' &&
          lastLine(run('print(grade(45))')) === 'C',
      },
      {
        label: 'grade(25) returns NG (below 40)',
        test: ({ run }) => lastLine(run('print(grade(25))')) === 'NG',
      },
      {
        label: 'average([80, 90, 100]) returns 90 (secret test)',
        test: ({ run }) => {
          const v = lastLine(run('print(average([80, 90, 100]))'));
          return v === '90' || v === '90.0';
        },
      },
      {
        label: 'Print a report line for every mark using a loop',
        test: ({ source, output }) => {
          const clean = noComments(source);
          return /\bfor\b[^\n]*\bmarks\b/.test(clean) && output.filter((l) => /\d+/.test(l) && /(A\+|A|B\+|B|C\+|C|NG)/.test(l)).length >= 5;
        },
      },
    ],
  });
}
