import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_JS = [
  '// JavaScript runs line by line, top to bottom.',
  '// console.log() prints to the console panel.',
  '',
  'console.log("Hello, JavaScript Quest!");',
  '',
  '// Goal 1: print your own name',
  '',
  '// Goal 2: make the computer calculate 7 * 8',
  '',
  '// Goal 3: store a number in a variable and print it',
  '// let score = 100;',
  '',
].join('\n');

function stripComments(js) {
  return (js || '').replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'js',
    tabs: ['js'],
    starter: { js: STARTER_JS },
    autoRun: false,
    goals: [
      {
        label: 'Print something with console.log()',
        test: ({ js, output }) => /console\.log\s*\(/.test(stripComments(js)) && output.length > 0,
      },
      {
        label: 'Make JS calculate 7 * 8 and print the answer',
        test: ({ js, output }) => /7\s*\*\s*8|8\s*\*\s*7/.test(stripComments(js)) && output.some((l) => l.includes('56')),
      },
      {
        label: 'Create a variable with let or const and print it',
        test: ({ js, output }) => {
          const clean = stripComments(js);
          const m = clean.match(/\b(?:let|const|var)\s+([A-Za-z_$][\w$]*)\s*=\s*[^;\n]+/);
          if (!m) return false;
          const name = m[1];
          const re = new RegExp('console\\.log\\s*\\([^)]*\\b' + name.replace(/\$/g, '\\$') + '\\b');
          return re.test(clean) && output.length > 0;
        },
      },
      {
        label: 'Do math with your variable (like score + 10)',
        test: ({ js }) => {
          const clean = stripComments(js);
          const m = clean.match(/\b(?:let|const|var)\s+([A-Za-z_$][\w$]*)\s*=/);
          if (!m) return false;
          const name = m[1].replace(/\$/g, '\\$');
          return new RegExp('\\b' + name + '\\b\\s*[-+*/]|[-+*/]\\s*\\b' + name + '\\b').test(clean);
        },
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Goal done — ' + n + ' of ' + total + '! Variables are labelled boxes: the computer remembers what you put inside.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 50);
      guide.say('All goals smashed! You can print, calculate and store values — the three superpowers every program is built from!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Welcome to JavaScript Quest! The console is your direct line to the computer. Press Run to see the starter message, then tackle the goals one by one!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
