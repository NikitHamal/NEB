import { createPyLesson } from './py-console.js';

const STARTER = [
  '# Loops repeat work so you don\'t have to!',
  '',
  '# for counts through a range:',
  'for i in range(1, 4):',
  '    print(f"round {i}")',
  '',
  '# Goal 1: print the numbers 1 to 10 with a loop',
  '',
  '# Goal 2: inside a loop, use if/else to say if each number',
  '#         is "even" or "odd"  (hint: n % 2 == 0)',
  '',
  '# Goal 3: use a while loop to count DOWN from 5 to 1',
  '',
  '# Goal 4 (boss level): for numbers 1 to 15, print "Fizz"',
  '#         when the number divides by 3, otherwise the number',
].join('\n');

function noComments(src) {
  return src.replace(/#[^\n]*/g, '');
}

export default function init(stage) {
  return createPyLesson(stage, {
    starter: STARTER,
    intro: 'Loops are a programmer\'s best friend: write the work once, let the computer repeat it. range(1, 11) counts 1 to 10 — the end number is never included!',
    allDoneLine: 'Boss level cleared! Loops plus if/else means your programs can repeat AND decide — that combo runs the whole digital world!',
    errorLines: [
      'Red alert! Check the line number. Common loop bugs: missing the colon : or forgetting to indent the body.',
      'Hmm, an error. Did you indent the lines inside your loop with spaces?',
    ],
    goals: [
      {
        label: 'Print the numbers 1 to 10 using a loop',
        test: ({ source, output }) => {
          if (!/\b(for|while)\b/.test(noComments(source))) return false;
          let idx = -1;
          for (let n = 1; n <= 10; n++) {
            idx = output.indexOf(String(n), idx + 1);
            if (idx < 0) return false;
          }
          return true;
        },
      },
      {
        label: 'Use if/else inside a loop (even or odd?)',
        test: ({ source, output }) => {
          const clean = noComments(source);
          return /\bif\b/.test(clean) && /\belse\b/.test(clean) && /%\s*2/.test(clean) &&
            output.some((l) => l.toLowerCase().includes('even')) && output.some((l) => l.toLowerCase().includes('odd'));
        },
      },
      {
        label: 'Count down 5 to 1 with a while loop',
        test: ({ source, output }) => {
          if (!/\bwhile\b/.test(noComments(source))) return false;
          let idx = -1;
          for (const n of ['5', '4', '3', '2', '1']) {
            idx = output.findIndex((l, i) => i > idx && l.trim().endsWith(n));
            if (idx < 0) return false;
          }
          return true;
        },
      },
      {
        label: 'Fizz challenge: 1 to 15, say "Fizz" on multiples of 3',
        test: ({ output }) => {
          const fizzes = output.filter((l) => l.trim() === 'Fizz').length;
          return fizzes >= 5 && output.some((l) => l.trim() === '14') && output.some((l) => l.trim() === '4');
        },
      },
    ],
  });
}
