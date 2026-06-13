import { createPlayground } from './playground.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

const STARTER_HTML = [
  '<!-- Welcome! Write your HTML below. -->',
  '<!-- Goal 1: add a big heading with <h1>...</h1> -->',
  '',
  '<!-- Goal 2: add a paragraph with <p>...</p> -->',
  '',
  '<!-- Goal 3: add a picture: <img src="..." alt="..."> -->',
  '<!-- Tip: try src="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 10 10\'><circle cx=\'5\' cy=\'5\' r=\'4\' fill=\'gold\'/><circle cx=\'3.5\' cy=\'4\' r=\'.6\'/><circle cx=\'6.5\' cy=\'4\' r=\'.6\'/><path d=\'M3 6 Q5 8 7 6\' stroke=\'black\' fill=\'none\' stroke-width=\'.4\'/></svg>" -->',
  '',
  '<!-- Goal 4: add a list: <ul> with three <li> items -->',
  '',
].join('\n');

export default function init(stage) {
  let guide = null;
  const pg = createPlayground(stage, {
    mode: 'web',
    tabs: ['html'],
    starter: { html: STARTER_HTML },
    goals: [
      {
        label: 'Add a big heading with <h1>',
        test: ({ doc }) => {
          const h = doc && doc.querySelector('h1');
          return h && h.textContent.trim().length > 0;
        },
      },
      {
        label: 'Add a paragraph with <p>',
        test: ({ doc }) => {
          const p = doc && doc.querySelector('p');
          return p && p.textContent.trim().length > 0;
        },
      },
      {
        label: 'Add a picture with <img>',
        test: ({ doc }) => {
          const img = doc && doc.querySelector('img');
          return img && (img.getAttribute('src') || '').length > 0;
        },
      },
      {
        label: 'Add a <ul> list with 3 <li> items',
        test: ({ doc }) => doc && doc.querySelectorAll('ul li').length >= 3,
      },
    ],
    onGoalMet: (n, total) => {
      if (n < total) guide.say('Goal complete — ' + n + ' of ' + total + '! Tags are like labelled boxes, and you\'re stacking them perfectly.', { mood: 'celebrate' });
    },
    onAllGoals: () => {
      launchConfetti(stage, 50);
      guide.say('ALL goals done! You just built a real webpage with headings, text, pictures and lists. You\'re officially a Web Wizard apprentice!', { mood: 'celebrate' });
    },
  });
  guide = createGuide(stage, { name: 'Neby' });
  guide.say('Hi! HTML tags are like containers: <h1> holds a big title, <p> holds text. Open a tag, put something inside, close it. Type in the editor and press Run!', { mood: 'happy' });
  return {
    dispose() {
      guide.dispose();
      pg.dispose();
    },
  };
}
