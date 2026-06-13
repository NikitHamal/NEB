import { createPyLesson } from './py-console.js';

const STARTER = [
  '# Welcome to Python! Lines starting with # are notes.',
  '# print() shows things on the screen:',
  '',
  'print("Namaste, Python!")',
  '',
  '# Goal 2: store your name in a variable:',
  '# name = "Mina"',
  '',
  '# Goal 3: print a sentence using an f-string:',
  '# print(f"My name is {name}")',
  '',
].join('\n');

export default function init(stage) {
  return createPyLesson(stage, {
    starter: STARTER,
    intro: 'Namaste! This is Python — the language scientists, game studios and AI labs all use. print() is your voice. Press Run, then work through the goals!',
    allDoneLine: 'All goals done! You can print, store values and weave them into sentences — the foundations of every Python program!',
    errorLines: [
      'A red error! Don\'t worry — read it carefully. It tells you the line number where Python got confused.',
      'Errors are friends in disguise: they point exactly at what to fix. Check the line number!',
    ],
    goals: [
      {
        label: 'Print a message with print()',
        test: ({ source, output }) => /print\s*\(/.test(source) && output.length > 0,
      },
      {
        label: 'Create a variable holding text (like name = "Mina")',
        test: ({ source }) => /^\s*\w+\s*=\s*["'][^"']+["']/m.test(source.replace(/#[^\n]*/g, '')),
      },
      {
        label: 'Create a number variable (like age = 16)',
        test: ({ source }) => /^\s*\w+\s*=\s*\d+/m.test(source.replace(/#[^\n]*/g, '')),
      },
      {
        label: 'Use an f-string to mix a variable into a sentence',
        test: ({ source, output }) => /f["'][^"']*\{\s*\w+[^}]*\}/.test(source.replace(/#[^\n]*/g, '')) && output.length > 0,
      },
    ],
  });
}
