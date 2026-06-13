import { createPyLesson } from './py-console.js';

const STARTER = [
  '# DATA DETECTIVE: investigate this exam data!',
  '# Pass mark is 40. Print a report like:',
  '#',
  '#   === Exam Report ===',
  '#   Students: 10',
  '#   Average: ...',
  '#   Highest: ...',
  '#   Lowest: ...',
  '#   Pass rate: ...%',
  '',
  'scores = [78, 45, 92, 33, 60, 85, 25, 70, 52, 100]',
  'PASS_MARK = 40',
  '',
  '# Step 1: count the students with len()',
  '',
  '# Step 2: loop over scores to total them up',
  '#         and count how many are >= PASS_MARK',
  '',
  '# Step 3: average = total / count',
  '#         highest and lowest: max() and min() help!',
  '',
  '# Step 4: pass_rate = passed / count * 100',
  '',
  '# Step 5: print the report with f-strings',
  'print("=== Exam Report ===")',
].join('\n');

function noComments(src) {
  return src.replace(/#[^\n]*/g, '');
}

function hasLine(output, word, value) {
  const re = new RegExp(word, 'i');
  const val = new RegExp('\\b' + value + '(\\.0)?\\b');
  return output.some((l) => re.test(l) && val.test(l));
}

export default function init(stage) {
  return createPyLesson(stage, {
    starter: STARTER,
    intro: 'Detective, the exam data is in! Loop through the scores, total them with an accumulator, and let max(), min() and len() do the heavy lifting. Print the full report!',
    allDoneLine: 'CASE CLOSED! You turned a raw list of numbers into insight: count, average, extremes and a pass rate. That is real data analysis — the exact skill behind every dashboard!',
    errorLines: [
      'A clue gone wrong! Check the red line — every if and for needs a colon and an indented body.',
      'Hmm, an error. Read it carefully: Python names the exact line that confused it.',
    ],
    goals: [
      {
        label: 'Report the number of students (10)',
        test: ({ output }) => hasLine(output, 'student', '10'),
      },
      {
        label: 'Compute and print the average (64)',
        test: ({ output }) => hasLine(output, 'average', '64'),
      },
      {
        label: 'Find the highest (100) and lowest (25) scores',
        test: ({ output }) => hasLine(output, 'highest', '100') && hasLine(output, 'lowest', '25'),
      },
      {
        label: 'Print the pass rate with a % sign (80%)',
        test: ({ output }) => output.some((l) => /pass/i.test(l) && /\b80(\.0)?\s*%/.test(l)),
      },
      {
        label: 'Process the list with a loop (no hardcoding the totals!)',
        test: ({ source }) => {
          const clean = noComments(source);
          return /\bfor\b[^\n]*\bscores\b/.test(clean) && /\blen\s*\(/.test(clean);
        },
      },
    ],
  });
}
