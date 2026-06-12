import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<h1>My Stopwatch</h1>',
  '<div id="display">0.0</div>',
  '',
  '<!-- Goal: add three buttons with these exact ids: -->',
  '<!--   start-btn   stop-btn   reset-btn -->',
  '',
].join('\n');

const STARTER_JS = [
  '// Build a real stopwatch!',
  '//',
  '// Plan:',
  '//  1. let elapsed = 0; and let timer = null; to hold state',
  '//  2. grab #display with document.getElementById',
  '//  3. start-btn: setInterval that adds 0.1 to elapsed',
  '//     every 100ms and writes it into the display',
  '//  4. stop-btn: clearInterval(timer)',
  '//  5. reset-btn: elapsed = 0 and update the display',
  '',
  'let elapsed = 0;',
  'let timer = null;',
  '',
].join('\n');

function noComments(js) {
  return (js || '').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'web',
    tabs: ['html', 'js'],
    starter: { html: STARTER_HTML, js: STARTER_JS },
    goals: [
      {
        label: 'Buttons with ids start-btn, stop-btn and reset-btn',
        test: ({ doc }) => !!(doc && doc.querySelector('button#start-btn') && doc.querySelector('button#stop-btn') && doc.querySelector('button#reset-btn')),
      },
      {
        label: 'Tick with setInterval(...)',
        test: ({ js }) => /setInterval\s*\(/.test(noComments(js)),
      },
      {
        label: 'Write the time into #display with textContent',
        test: ({ js }) => {
          const clean = noComments(js);
          return /(getElementById\s*\(\s*['"]display['"]\s*\)|querySelector\s*\(\s*['"]#display['"]\s*\))/.test(clean) && /\.textContent\s*=/.test(clean);
        },
      },
      {
        label: 'Stop the timer with clearInterval(...)',
        test: ({ js }) => /clearInterval\s*\(/.test(noComments(js)),
      },
      {
        label: 'Reset puts the time back to 0 (three click listeners)',
        test: ({ js }) => {
          const clean = noComments(js);
          const listeners = clean.match(/addEventListener\s*\(\s*['"]click['"]/g) || [];
          return listeners.length >= 3 && /=\s*0\b/.test(clean);
        },
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Tick tock — ' + n + ' of ' + total + ' goals! Press your buttons in the preview to test the stopwatch for real.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 60);
      guide.say('A WORKING STOPWATCH! setInterval fires your code again and again, and your state variables remember the time between ticks. That\'s real app architecture!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Advanced challenge! Build a stopwatch: setInterval(fn, 100) runs fn every 100 milliseconds. Add the three buttons in HTML, wire them up in JS, then click them in the preview!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
