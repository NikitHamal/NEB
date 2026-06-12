import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<h2 id="message">Click the button!</h2>',
  '<button id="magic-btn">Press me</button>',
  '<p>Clicks so far: <span id="count">0</span></p>',
].join('\n');

const STARTER_JS = [
  '// document.getElementById finds an element on the page.',
  'const btn = document.getElementById("magic-btn");',
  'const msg = document.getElementById("message");',
  '',
  '// Goal 1: listen for clicks:',
  '// btn.addEventListener("click", function () {',
  '//   ...your code here...',
  '// });',
  '',
  '// Goal 2: inside the click, change msg.textContent',
  '// Goal 3: change a color with msg.style.color',
  '// Goal 4: count clicks with a variable that goes up by 1',
].join('\n');

function stripComments(js) {
  return (js || '').replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'web',
    tabs: ['html', 'js'],
    showConsole: true,
    starter: { html: STARTER_HTML, js: STARTER_JS },
    goals: [
      {
        label: 'Listen for clicks with addEventListener',
        test: ({ js }) => /\.addEventListener\s*\(\s*["']click["']/.test(stripComments(js)),
      },
      {
        label: 'Change some text with textContent or innerText',
        test: ({ js }) => /\.(textContent|innerText)\s*=/.test(stripComments(js)),
      },
      {
        label: 'Change a style, like .style.color or .style.background',
        test: ({ js }) => /\.style\.[A-Za-z]+\s*=/.test(stripComments(js)),
      },
      {
        label: 'Count the clicks (a variable that goes up by 1)',
        test: ({ js }) => {
          const clean = stripComments(js);
          return /(\+\+|\+=\s*1)/.test(clean) && /\b(let|var)\s+\w+\s*=\s*0/.test(clean);
        },
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Goal ' + n + ' of ' + total + ' done! Press your button in the preview to feel the magic working.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 50);
      guide.say('Interactive! Your page now listens, reacts and remembers. That\'s exactly how every app, game and website works underneath!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Time to make pages come ALIVE! addEventListener is like giving your button ears — when it hears a click, your code runs. Follow the comments and press Run, then try clicking your button!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
