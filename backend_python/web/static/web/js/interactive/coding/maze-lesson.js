import { createBlocksEngine, executeProgram, countBlocks } from './blocks-engine.js';
import { createMaze, launchConfetti } from './maze-game.js';
import { createGuide } from './guide.js';

export function setupMazeLesson(stage, config) {
  stage.classList.add('ix-coding', 'ix-coding-maze');

  const root = document.createElement('div');
  root.className = 'ix-coding-root';
  root.innerHTML =
    '<div class="ix-level-bar">' +
    '<span class="ix-level-title"></span>' +
    '<div class="ix-level-dots"></div>' +
    '<span class="ix-level-challenge" hidden></span>' +
    '</div>' +
    '<div class="ix-maze-layout">' +
    '<div class="ix-maze-left">' +
    '<div class="ix-maze-board-host"></div>' +
    '<div class="ix-run-controls">' +
    '<button type="button" class="ix-run-btn ix-btn-run"><span class="material-symbols-outlined">play_arrow</span>Run</button>' +
    '<button type="button" class="ix-run-btn ix-btn-step"><span class="material-symbols-outlined">skip_next</span>Step</button>' +
    '<button type="button" class="ix-run-btn ix-btn-reset"><span class="material-symbols-outlined">replay</span>Reset</button>' +
    '</div>' +
    '</div>' +
    '<div class="ix-maze-right"></div>' +
    '</div>';
  stage.appendChild(root);

  const titleEl = root.querySelector('.ix-level-title');
  const dotsEl = root.querySelector('.ix-level-dots');
  const challengeEl = root.querySelector('.ix-level-challenge');
  const boardHost = root.querySelector('.ix-maze-board-host');
  const engineHost = root.querySelector('.ix-maze-right');
  const runBtn = root.querySelector('.ix-btn-run');
  const stepBtn = root.querySelector('.ix-btn-step');
  const resetBtn = root.querySelector('.ix-btn-reset');

  const guide = createGuide(stage, { name: 'Neby' });
  const engine = createBlocksEngine(engineHost, {
    palette: config.palette,
    onChange: () => updateChallenge(),
  });

  let levelIndex = 0;
  let maze = null;
  let running = false;
  let control = { stopped: false };
  let releaseStep = null;
  let mode = 'run';
  let advanceTimer = null;
  const done = new Array(config.levels.length).fill(false);

  function level() { return config.levels[levelIndex]; }

  function updateChallenge() {
    const max = level().maxBlocks;
    if (!max) { challengeEl.hidden = true; return; }
    challengeEl.hidden = false;
    const n = engine.blockCount();
    challengeEl.textContent = 'Challenge: solve with ≤ ' + max + ' blocks (you: ' + n + ')';
    challengeEl.classList.toggle('ix-challenge-over', n > max);
  }

  function renderDots() {
    dotsEl.innerHTML = '';
    config.levels.forEach((lv, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'ix-level-dot' + (i === levelIndex ? ' ix-dot-current' : '') + (done[i] ? ' ix-dot-done' : '');
      dot.setAttribute('aria-label', 'Level ' + (i + 1));
      dot.textContent = done[i] ? '✓' : String(i + 1);
      dot.addEventListener('click', () => { if (!running) loadLevel(i); });
      dotsEl.appendChild(dot);
    });
  }

  function loadLevel(i, keepProgram) {
    if (advanceTimer) { clearTimeout(advanceTimer); advanceTimer = null; }
    levelIndex = i;
    if (maze) maze.dispose();
    boardHost.innerHTML = '';
    maze = createMaze(boardHost, level());
    titleEl.textContent = 'Level ' + (i + 1) + ' of ' + config.levels.length;
    if (!keepProgram) engine.clear();
    renderDots();
    updateChallenge();
    if (level().hint) guide.say(level().hint, { mood: 'happy' });
  }

  function stopRun() {
    control.stopped = true;
    if (releaseStep) { releaseStep(); releaseStep = null; }
    running = false;
    engine.setLocked(false);
    engine.clearHighlight();
    runBtn.disabled = false;
    stepBtn.disabled = false;
  }

  function gate() {
    return new Promise((resolve) => {
      if (mode === 'run') setTimeout(resolve, level().stepDelay || 360);
      else releaseStep = resolve;
    });
  }

  async function start(startMode) {
    if (running) {
      if (startMode === 'step' && releaseStep) {
        const r = releaseStep;
        releaseStep = null;
        r();
      }
      return;
    }
    if (!engine.getProgram().length) {
      guide.say('Your program is empty! Add some blocks first.', { mood: 'thinking' });
      return;
    }
    mode = startMode;
    running = true;
    control = { stopped: false };
    engine.setLocked(true);
    runBtn.disabled = startMode === 'step';
    maze.reset();
    let finished = false;
    try {
      finished = await executeProgram(engine.getProgram(), maze, {
        gate,
        control,
        onBlock: (node) => engine.highlight(node),
      });
    } catch (err) {
      guide.say('Whoa, that program ran too many steps! Try fewer repeats.', { mood: 'thinking' });
    }
    if (control.stopped) return;
    engine.clearHighlight();
    running = false;
    engine.setLocked(false);
    runBtn.disabled = false;
    if (maze.crashed) {
      guide.say(pick(config.crashLines || ['Bonk! The robot hit a wall. Check your steps and try again!']), { mood: 'sad' });
      return;
    }
    if (finished && maze.isComplete()) {
      onWin();
    } else {
      guide.say(pick(config.missLines || ['The robot stopped before reaching the star. Tweak your blocks and run again!']), { mood: 'thinking' });
    }
  }

  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function onWin() {
    maze.celebrate();
    done[levelIndex] = true;
    renderDots();
    const max = level().maxBlocks;
    const used = countBlocks(engine.getProgram());
    let praise = pick(config.winLines || ['You did it!']);
    if (max && used <= max) praise += ' And you beat the ' + max + '-block challenge with ' + used + ' blocks!';
    if (done.every(Boolean)) {
      guide.say(praise + ' ' + (config.allDoneLine || 'That was the last level — you finished the whole lesson! Amazing work!'), { mood: 'celebrate' });
      launchConfetti(stage, 60);
    } else if (levelIndex < config.levels.length - 1) {
      guide.say(praise + ' Ready for the next level?', { mood: 'celebrate' });
      advanceTimer = setTimeout(() => {
        advanceTimer = null;
        if (!running) loadLevel(levelIndex + 1);
      }, 2200);
    } else {
      guide.say(praise, { mood: 'celebrate' });
    }
  }

  runBtn.addEventListener('click', () => start('run'));
  stepBtn.addEventListener('click', () => start('step'));
  resetBtn.addEventListener('click', () => {
    stopRun();
    maze.reset();
    guide.say('Fresh start! The robot is back at the beginning.', { mood: 'happy', duration: 3000 });
  });

  loadLevel(0);
  if (config.intro) guide.say(config.intro, { mood: 'happy' });

  return {
    dispose() {
      if (advanceTimer) { clearTimeout(advanceTimer); advanceTimer = null; }
      stopRun();
      guide.dispose();
      engine.dispose();
      if (maze) maze.dispose();
      root.remove();
      stage.classList.remove('ix-coding', 'ix-coding-maze');
    },
  };
}
