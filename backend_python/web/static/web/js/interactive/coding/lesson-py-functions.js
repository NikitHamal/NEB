import { createPyLesson } from './py-console.js';

const STARTER = [
  '# Lists hold many values, functions package reusable logic.',
  '',
  'scores = [72, 95, 88]',
  'print(f"{len(scores)} scores: {scores}")',
  '',
  '# Goal 1: append a new score to the list with scores.append(...)',
  '',
  '# Goal 2: write a function that returns a doubled number:',
  '# def double(n):',
  '#     return n * 2',
  '',
  '# Goal 3 (boss): write a function biggest(numbers) that',
  '#         returns the biggest number in any list.',
  '#         Hint: start with best = numbers[0], then loop!',
  '',
  '# Test your work:',
  '# print(double(21))',
  '# print(biggest(scores))',
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
    intro: 'Lists are backpacks for data, and functions are machines you build once and reuse forever. Today you\'ll combine both — and I\'ll secretly test your functions with my own lists!',
    allDoneLine: 'Every secret test passed! Lists + loops + functions — you just used the exact toolkit behind real apps. Final quest awaits!',
    errorLines: [
      'Error spotted! Remember: def line ends with a colon, and the body must be indented.',
      'Check the red line number — maybe a missing return or a typo in a name?',
    ],
    goals: [
      {
        label: 'Grow the list with .append()',
        test: ({ source, output }) => /\.append\s*\(/.test(noComments(source)) && output.length > 0,
      },
      {
        label: 'Define a function with def and return',
        test: ({ source }) => {
          const clean = noComments(source);
          return /\bdef\s+\w+\s*\([^)]*\)\s*:/.test(clean) && /\breturn\b/.test(clean);
        },
      },
      {
        label: 'double(21) returns 42 (secret test)',
        test: ({ run }) => lastLine(run('print(double(21))')) === '42',
      },
      {
        label: 'biggest() finds the max of [3, 41, 7] (secret test)',
        test: ({ run }) => lastLine(run('print(biggest([3, 41, 7]))')) === '41',
      },
      {
        label: 'biggest() even works with negatives [-9, -2, -7]',
        test: ({ run }) => lastLine(run('print(biggest([-9, -2, -7]))')) === '-2',
      },
    ],
  });
}
