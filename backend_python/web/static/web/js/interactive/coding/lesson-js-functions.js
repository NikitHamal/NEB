import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_JS = [
  '// A function is a reusable recipe.',
  '// Define it once, use it as many times as you like!',
  '',
  'function shout(word) {',
  '  return word + "!!!";',
  '}',
  '',
  'console.log(shout("hello"));',
  '',
  '// Goal 1: write a function double(n) that returns n * 2',
  '',
  '// Goal 2: write a function greet(name) that returns',
  '//         a greeting containing the name, like "Hello, Mina!"',
  '',
  '// Try them yourself:',
  '// console.log(double(21));',
  '// console.log(greet("Mina"));',
].join('\n');

const HARNESS = [
  ';(function(){',
  'try{console.log("__T_D4:"+double(4));}catch(e){}',
  'try{console.log("__T_D9:"+double(9.5));}catch(e){}',
  'try{console.log("__T_G:"+greet("Mina"));}catch(e){}',
  'try{console.log("__T_G2:"+greet("Ramesh"));}catch(e){}',
  '})();',
].join('\n');

function lineValue(output, prefix) {
  const line = output.find((l) => l.startsWith(prefix));
  return line ? line.slice(prefix.length) : null;
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'js',
    tabs: ['js'],
    starter: { js: STARTER_JS },
    autoRun: false,
    harness: (js) => js + '\n' + HARNESS,
    consoleFilter: (payload) => !payload.text.startsWith('__T_'),
    goals: [
      {
        label: 'double(4) returns 8',
        test: ({ output }) => lineValue(output, '__T_D4:') === '8',
      },
      {
        label: 'double works for any number (9.5 → 19)',
        test: ({ output }) => lineValue(output, '__T_D9:') === '19',
      },
      {
        label: 'greet("Mina") returns a greeting with Mina in it',
        test: ({ output }) => {
          const v = lineValue(output, '__T_G:');
          return !!v && v.includes('Mina') && v.length > 4 && !v.includes('undefined');
        },
      },
      {
        label: 'greet works for any name, not just one',
        test: ({ output }) => {
          const v = lineValue(output, '__T_G2:');
          return !!v && v.includes('Ramesh') && !v.includes('undefined');
        },
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Test passed — ' + n + ' of ' + total + '! I secretly call your functions with my own values to check them. Sneaky, right?', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 50);
      guide.say('All my secret tests passed! Your functions take input, transform it, and return output — that\'s the heart of all programming!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Functions are recipes: ingredients go in (parameters), something tasty comes out (return). Write double(n) and greet(name), press Run, and I\'ll test them with my own secret values!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
