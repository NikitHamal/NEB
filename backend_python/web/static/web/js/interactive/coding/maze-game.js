const DIRS = [
  { dx: 0, dy: -1 },
  { dx: 1, dy: 0 },
  { dx: 0, dy: 1 },
  { dx: -1, dy: 0 },
];

const ROBOT_SVG = [
  '<svg viewBox="0 0 48 48" aria-hidden="true">',
  '<rect class="mz-robot-body" x="8" y="10" width="32" height="30" rx="10" fill="#3B82F6"/>',
  '<circle cx="24" cy="6.5" r="2.6" fill="#FCD34D"/>',
  '<rect x="22.9" y="7.5" width="2.2" height="4.5" rx="1.1" fill="#FCD34D"/>',
  '<path d="M20 13 L24 7.5 L28 13 Z" fill="#FCD34D" opacity="0.9"/>',
  '<rect x="12.5" y="16" width="23" height="14" rx="7" fill="#fff"/>',
  '<g class="mz-robot-eyes">',
  '<circle class="mz-eye" cx="19" cy="23" r="2.8" fill="#0F172A"/>',
  '<circle class="mz-eye" cx="29" cy="23" r="2.8" fill="#0F172A"/>',
  '<circle cx="19.9" cy="22.1" r="0.9" fill="#fff"/>',
  '<circle cx="29.9" cy="22.1" r="0.9" fill="#fff"/>',
  '</g>',
  '<path class="mz-robot-mouth" d="M19.5 33.5 Q24 36.5 28.5 33.5" stroke="#0F172A" stroke-width="1.8" fill="none" stroke-linecap="round"/>',
  '</svg>',
].join('');

const delay = (ms) => new Promise((r) => setTimeout(r, ms));

export function launchConfetti(container, count = 36) {
  const colors = ['#EC4899', '#F59E0B', '#3B82F6', '#10B981', '#8B5CF6', '#EF4444'];
  const layer = document.createElement('div');
  layer.className = 'mz-confetti-layer';
  for (let i = 0; i < count; i++) {
    const p = document.createElement('span');
    p.className = 'mz-confetti';
    p.style.left = (5 + Math.random() * 90) + '%';
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = (Math.random() * 0.5) + 's';
    p.style.animationDuration = (1 + Math.random() * 0.9) + 's';
    p.style.setProperty('--cf-drift', (Math.random() * 120 - 60) + 'px');
    p.style.setProperty('--cf-spin', (Math.random() * 720 - 360) + 'deg');
    if (Math.random() > 0.5) p.style.borderRadius = '50%';
    layer.appendChild(p);
  }
  container.appendChild(layer);
  setTimeout(() => layer.remove(), 2400);
}

export function createMaze(host, level) {
  const rows = level.grid.map((r) => r.split(''));
  const h = rows.length;
  const w = rows[0].length;
  let start = { x: 1, y: 1 };
  const collectibles = new Map();
  const cells = [];

  const board = document.createElement('div');
  board.className = 'mz-board';
  board.style.setProperty('--mz-cols', w);
  board.style.setProperty('--mz-rows', h);

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const ch = rows[y][x];
      const cell = document.createElement('div');
      cell.className = 'mz-cell ' + (ch === '#' ? 'mz-wall' : 'mz-path');
      if (ch === 'S') start = { x, y };
      if (ch === 'G') {
        cell.classList.add('mz-goal');
        cell.innerHTML = '<span class="mz-star">★</span>';
      }
      if (ch === 'o') {
        cell.classList.add('mz-gem-cell');
        cell.innerHTML = '<span class="mz-gem">◆</span>';
        collectibles.set(x + ',' + y, cell);
      }
      board.appendChild(cell);
      cells.push(cell);
    }
  }

  const robot = document.createElement('div');
  robot.className = 'mz-robot';
  robot.innerHTML = ROBOT_SVG;
  board.appendChild(robot);
  host.appendChild(board);

  const state = { x: start.x, y: start.y, dir: level.dir == null ? 1 : level.dir, angle: 0, collected: new Set(), crashed: false };
  state.angle = state.dir * 90;

  function isOpen(x, y) {
    return x >= 0 && y >= 0 && x < w && y < h && rows[y][x] !== '#';
  }

  function place(animate) {
    if (!animate) robot.classList.add('mz-no-anim');
    robot.style.transform =
      'translate(' + (state.x * 100) + '%, ' + (state.y * 100) + '%) rotate(' + state.angle + 'deg)';
    if (!animate) {
      void robot.offsetWidth;
      robot.classList.remove('mz-no-anim');
    }
  }
  place(false);

  function setFace(mood) {
    robot.classList.remove('mz-face-sad', 'mz-face-happy');
    if (mood === 'sad') robot.classList.add('mz-face-sad');
    if (mood === 'happy') robot.classList.add('mz-face-happy');
  }

  return {
    el: board,
    get crashed() { return state.crashed; },

    reset() {
      state.x = start.x;
      state.y = start.y;
      state.dir = level.dir == null ? 1 : level.dir;
      state.angle = state.dir * 90;
      state.crashed = false;
      state.collected.clear();
      collectibles.forEach((cell) => cell.classList.remove('mz-gem-taken'));
      robot.classList.remove('mz-crash');
      setFace(null);
      place(false);
    },

    async moveForward() {
      if (state.crashed) return false;
      const d = DIRS[state.dir];
      const nx = state.x + d.dx;
      const ny = state.y + d.dy;
      if (!isOpen(nx, ny)) {
        state.crashed = true;
        robot.classList.add('mz-crash');
        setFace('sad');
        await delay(450);
        return false;
      }
      state.x = nx;
      state.y = ny;
      place(true);
      await delay(300);
      const key = nx + ',' + ny;
      if (collectibles.has(key) && !state.collected.has(key)) {
        state.collected.add(key);
        collectibles.get(key).classList.add('mz-gem-taken');
      }
      return true;
    },

    async turnLeft() {
      state.dir = (state.dir + 3) % 4;
      state.angle -= 90;
      place(true);
      await delay(260);
    },

    async turnRight() {
      state.dir = (state.dir + 1) % 4;
      state.angle += 90;
      place(true);
      await delay(260);
    },

    isPathAhead() {
      const d = DIRS[state.dir];
      return isOpen(state.x + d.dx, state.y + d.dy);
    },

    isComplete() {
      if (state.crashed) return false;
      if (state.collected.size < collectibles.size) return false;
      return rows[state.y][state.x] === 'G';
    },

    celebrate() {
      setFace('happy');
      robot.classList.add('mz-win');
      launchConfetti(host);
      setTimeout(() => robot.classList.remove('mz-win'), 1400);
    },

    dispose() { board.remove(); },
  };
}
