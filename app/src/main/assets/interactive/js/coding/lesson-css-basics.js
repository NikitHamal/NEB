import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<h1>My Colourful Page</h1>',
  '<p>CSS gives plain HTML its style!</p>',
  '<div class="card">',
  '  <p>I am a card. Make me pretty!</p>',
  '</div>',
].join('\n');

const STARTER_CSS = [
  '/* CSS rules look like this:',
  '   selector {',
  '     property: value;',
  '   }',
  '*/',
  '',
  'h1 {',
  '  ',
  '}',
  '',
  'body {',
  '  ',
  '}',
  '',
  '.card {',
  '  border: 2px solid #EC4899;',
  '  padding: 16px;',
  '}',
].join('\n');

function stripComments(css) {
  return (css || '').replace(/\/\*[\s\S]*?\*\//g, '');
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'web',
    tabs: ['html', 'css'],
    starter: { html: STARTER_HTML, css: STARTER_CSS },
    goals: [
      {
        label: 'Give the <h1> heading a color',
        test: ({ css }) => /h1[^{}]*\{[^}]*[^-]color\s*:\s*[^;}]+/i.test(' ' + stripComments(css)),
      },
      {
        label: 'Set a background on the page or card',
        test: ({ css }) => /background(-color)?\s*:\s*[^;}]+/i.test(stripComments(css)),
      },
      {
        label: 'Round some corners with border-radius',
        test: ({ css }) => /border-radius\s*:\s*[^;}]+/i.test(stripComments(css)),
      },
      {
        label: 'Center text with text-align',
        test: ({ css }) => /text-align\s*:\s*center/i.test(stripComments(css)),
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Styled! ' + n + ' of ' + total + ' goals done. Selectors are like name tags — they pick which element gets the style.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 50);
      guide.say('Magnificent! Colors, backgrounds, round corners and centered text — your CSS magic is strong!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Time for CSS magic! A selector like h1 is a name tag: it points at every <h1> and applies styles. Try color: hotpink; inside the h1 rule, then press Run!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
