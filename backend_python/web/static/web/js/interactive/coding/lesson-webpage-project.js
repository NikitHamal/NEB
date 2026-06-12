import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<h1>About Me</h1>',
  '<p>Hi, I am ... and this is my very own webpage.</p>',
  '',
  '<h2>Three things I love</h2>',
  '<ul>',
  '  <li>...</li>',
  '</ul>',
].join('\n');

const STARTER_CSS = [
  'body {',
  '  font-family: sans-serif;',
  '}',
].join('\n');

function stripComments(css) {
  return (css || '').replace(/\/\*[\s\S]*?\*\//g, '');
}

function countRules(css) {
  const clean = stripComments(css);
  const matches = clean.match(/[^{}]+\{[^}]*:[^}]+\}/g);
  return matches ? matches.length : 0;
}

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'web',
    tabs: ['html', 'css'],
    starter: { html: STARTER_HTML, css: STARTER_CSS },
    goals: [
      {
        label: 'A heading that says who you are',
        test: ({ doc }) => {
          const h = doc && doc.querySelector('h1, h2');
          return h && h.textContent.trim().length >= 3;
        },
      },
      {
        label: 'A paragraph about you (20+ characters)',
        test: ({ doc }) => {
          if (!doc) return false;
          return [...doc.querySelectorAll('p')].some((p) => p.textContent.trim().length >= 20 && !p.textContent.includes('...'));
        },
      },
      {
        label: 'A list of things you love (3+ items)',
        test: ({ doc }) => {
          if (!doc) return false;
          const items = [...doc.querySelectorAll('ul li, ol li')];
          return items.filter((li) => li.textContent.trim().length > 0 && !li.textContent.includes('...')).length >= 3;
        },
      },
      {
        label: 'At least 3 CSS rules with styles inside',
        test: ({ css }) => countRules(css) >= 3,
      },
      {
        label: 'Use at least one color or background',
        test: ({ css }) => /(^|[^-])(color|background(-color)?)\s*:\s*[^;}]+/i.test(stripComments(css)),
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Looking great — ' + n + ' of ' + total + ' goals! Make it yours: your hobbies, your favourite colors, your style.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 60);
      guide.say('YOU BUILT A WEBPAGE! A real one, about the most interesting topic ever: you. Keep decorating it — there\'s no limit!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Project time! Build an About Me page. Replace the ... placeholders with real things about you, then style it with at least 3 CSS rules. Press Run anytime to see it!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
