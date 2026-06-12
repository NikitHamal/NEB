import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<h1>Generative Art</h1>',
  '<canvas id="art" width="360" height="240" style="border:1px solid #ccc"></canvas>',
].join('\n');

const STARTER_JS = [
  '// Paint with code!',
  '//',
  '// Plan:',
  '//  1. const ctx = canvas.getContext("2d");',
  '//  2. a for loop that runs 20+ times',
  '//  3. inside the loop, set a CHANGING colour:',
  '//     ctx.fillStyle = "hsl(" + i * 15 + ", 80%, 60%)";',
  '//  4. draw a shape that moves with i:',
  '//     circles:  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();',
  '//     squares:  ctx.fillRect(x, y, w, h);',
  '',
  'const canvas = document.getElementById("art");',
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
        label: 'Keep a <canvas> on the page',
        test: ({ doc }) => !!(doc && doc.querySelector('canvas')),
      },
      {
        label: 'Get the drawing context with getContext("2d")',
        test: ({ js }) => /getContext\s*\(\s*['"]2d['"]\s*\)/.test(noComments(js)),
      },
      {
        label: 'Use a loop to repeat your drawing',
        test: ({ js }) => /\b(for|while)\s*\(/.test(noComments(js)),
      },
      {
        label: 'Draw shapes with arc(...) or fillRect(...)',
        test: ({ js }) => /\.(arc|fillRect)\s*\(/.test(noComments(js)),
      },
      {
        label: 'Colours that change: fillStyle with hsl(...) using your loop variable',
        test: ({ js }) => {
          const clean = noComments(js);
          return /fillStyle\s*=/.test(clean) && /hsl\s*\(/i.test(clean);
        },
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Beautiful — ' + n + ' of ' + total + ' goals! Tweak the numbers in your loop and re-run: tiny changes make wildly different art.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 60);
      guide.say('GENERATIVE ART! One loop, a changing colour, a moving shape — and the canvas becomes your gallery. Try Math.sin(i), random sizes, hundreds of shapes!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Time to paint with pure code! A canvas is a grid of pixels you command with JavaScript. Get the 2d context, loop, and let hsl(i * 15, ...) walk through the rainbow!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
