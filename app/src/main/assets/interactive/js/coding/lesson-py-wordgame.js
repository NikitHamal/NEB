import { createPyLesson } from './py-console.js';

const STARTER = [
  '# WORD GAME: a hangman-style guessing engine!',
  '# The player already made these guesses — your code',
  '# checks them against the secret word.',
  '',
  'secret = "planet"',
  'guesses = ["a", "o", "t", "p", "z"]',
  '',
  'found = []',
  'wrong = []',
  '',
  '# Step 1: loop over guesses. If a guess is in secret,',
  '#         append it to found and print f"Hit: {g}" --',
  '#         otherwise append to wrong and print f"Miss: {g}"',
  '',
  '# Step 2: build the masked word: loop over the letters',
  '#         of secret, add the letter if it is in found,',
  '#         otherwise add "_". Print f"Word: {masked}"',
  '',
  '# Step 3: print how many wrong guesses (len helps)',
  '',
  '# Step 4: if masked == secret print "YOU WIN!"',
  '#         else print "Keep guessing!"',
].join('\n');

function noComments(src) {
  return src.replace(/#[^\n]*/g, '');
}

export default function init(stage) {
  return createPyLesson(stage, {
    starter: STARTER,
    intro: 'Game developer mode! The "in" operator is your engine: "a" in "planet" is True. Check every guess, build the masked word letter by letter, and judge the round!',
    allDoneLine: 'GAME COMPLETE! You built the entire logic core of hangman: membership tests, accumulator lists and a masked-word builder. Wrap a real UI around this and you have shipped a game!',
    errorLines: [
      'Bug in the game engine! Check the red line — strings and lists both work with "in", but watch your indentation.',
      'Error! Read the message: Python points at the exact line. Is every if/else followed by a colon?',
    ],
    goals: [
      {
        label: 'Announce every guess as a Hit or a Miss (5 lines)',
        test: ({ output }) => output.filter((l) => /\b(hit|miss)\b/i.test(l)).length >= 5,
      },
      {
        label: 'Build and print the masked word: p_a__t',
        test: ({ output }) => output.some((l) => l.includes('p_a__t')),
      },
      {
        label: 'Count the wrong guesses (2) using your wrong list',
        test: ({ output, source }) => {
          const clean = noComments(source);
          return /wrong\s*\.\s*append\s*\(/.test(clean) && output.some((l) => /wrong/i.test(l) && /\b2\b/.test(l));
        },
      },
      {
        label: 'Judge the round with if/else (win or keep guessing)',
        test: ({ output, source }) => {
          const clean = noComments(source);
          return /\bif\b[^\n]*==/.test(clean) && output.some((l) => /(win|keep guessing)/i.test(l));
        },
      },
      {
        label: 'Use "in" to test letters against the secret word',
        test: ({ source }) => /\bif\b[^\n]*\bin\s+(secret|found)\b/.test(noComments(source)),
      },
    ],
  });
}
