import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Lesson 8 – AI That Learns by Playing (Q-Learning)
// Grid world: agent navigates from start to goal, avoiding pits.
// Full Q-table update: Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') − Q(s,a)]

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Q-Learning', '#6366F1');

  const GRID_W = 6, GRID_H = 6;
  const ACTIONS = 4; // 0=up 1=right 2=down 3=left
  const ACTION_DX = [0, 1, 0, -1];
  const ACTION_DY = [-1, 0, 1, 0];
  const ACTION_LABEL = ['↑', '→', '↓', '←'];

  // World layout (0=empty, 1=wall, 2=pit, 3=goal)
  const WORLD = [
    [0,0,0,0,0,0],
    [0,1,1,0,2,0],
    [0,0,0,0,0,0],
    [0,2,0,1,0,0],
    [0,0,0,0,1,0],
    [0,0,2,0,0,3],
  ];
  const START = { x: 0, y: 0 };
  const GOAL  = { x: 5, y: 5 };

  let alpha = 0.3;    // learning rate
  let gamma = 0.9;    // discount factor
  let epsilon = 0.8;  // exploration rate
  let epsilonDecay = 0.995;

  // Q-table: Q[y][x][action]
  let Q = Array.from({ length: GRID_H }, () =>
    Array.from({ length: GRID_W }, () => new Float32Array(ACTIONS))
  );

  let agentX = START.x, agentY = START.y;
  let episode = 0, step = 0, totalReward = 0;
  let episodeReward = 0;
  let running = false;
  let rewardHistory = [];
  let stepHistory = [];
  let lastReward = 0;
  let animAccum = 0;
  let stepsPerEp = 0;

  function resetAgent() { agentX = START.x; agentY = START.y; stepsPerEp = 0; episodeReward = 0; }

  function getReward(x, y) {
    const cell = WORLD[y] ? WORLD[y][x] : -1;
    if (cell === 3) return 10;    // goal
    if (cell === 2) return -5;    // pit
    if (cell === 1) return -1;    // wall collision
    return -0.1;                  // step cost
  }

  function isTerminal(x, y) {
    const cell = WORLD[y] && WORLD[y][x];
    return cell === 3 || cell === 2;
  }

  function chooseAction(x, y) {
    if (Math.random() < epsilon) return Math.floor(Math.random() * ACTIONS);
    const qs = Q[y][x];
    let best = 0;
    for (let a = 1; a < ACTIONS; a++) if (qs[a] > qs[best]) best = a;
    return best;
  }

  function step2(x, y, action) {
    let nx = x + ACTION_DX[action];
    let ny = y + ACTION_DY[action];
    // Clamp & wall check
    if (nx < 0 || nx >= GRID_W || ny < 0 || ny >= GRID_H || (WORLD[ny] && WORLD[ny][nx] === 1)) {
      nx = x; ny = y;
    }
    const r = getReward(nx, ny);
    return { nx, ny, r };
  }

  function qUpdate() {
    const a = chooseAction(agentX, agentY);
    const { nx, ny, r } = step2(agentX, agentY, a);

    // Q update
    const maxQNext = Math.max(...Q[ny][nx]);
    Q[agentY][agentX][a] += alpha * (r + gamma * maxQNext - Q[agentY][agentX][a]);

    agentX = nx; agentY = ny;
    episodeReward += r;
    stepsPerEp++;
    step++;

    if (isTerminal(agentX, agentY) || stepsPerEp > 100) {
      rewardHistory.push(episodeReward);
      stepHistory.push(stepsPerEp);
      if (rewardHistory.length > 150) rewardHistory.shift();
      if (stepHistory.length > 150) stepHistory.shift();
      lastReward = episodeReward;
      episode++;
      epsilon = Math.max(0.05, epsilon * epsilonDecay);
      resetAgent();
    }
  }

  function initQ() {
    Q = Array.from({ length: GRID_H }, () =>
      Array.from({ length: GRID_W }, () => new Float32Array(ACTIONS))
    );
    episode = 0; step = 0; epsilon = 0.8;
    rewardHistory = []; stepHistory = [];
    resetAgent();
    running = false;
    runBtn.setLabel('Train');
    badge.set('Reset');
  }

  const panel = createPanel(stage, { title: 'Q-Learning' });
  panel.slider({ label: 'Learning rate α', min: 0.05, max: 0.9, step: 0.05, value: alpha,
    format: (v) => v.toFixed(2), onChange: (v) => { alpha = v; } });
  panel.slider({ label: 'Discount γ', min: 0.5, max: 0.99, step: 0.01, value: gamma,
    format: (v) => v.toFixed(2), onChange: (v) => { gamma = v; } });
  panel.slider({ label: 'ε decay /ep', min: 0.98, max: 0.9999, step: 0.0001, value: epsilonDecay,
    format: (v) => v.toFixed(4), onChange: (v) => { epsilonDecay = v; } });
  panel.divider();
  const epOut = panel.readout({ label: 'Episode', value: '0' });
  const epsOut = panel.readout({ label: 'Epsilon ε', value: epsilon.toFixed(3) });
  const rewOut = panel.readout({ label: 'Last reward', value: '—' });
  panel.divider();
  const [runBtn, resetBtn] = panel.buttonRow([
    { label: 'Train', icon: 'play_arrow', onClick: () => { running = !running; runBtn.setLabel(running ? 'Pause' : 'Train'); badge.set(running ? 'Training…' : 'Paused'); } },
    { label: 'Reset', icon: 'replay', onClick: initQ },
  ]);
  panel.info('Watch the value map (heat = Q-value) light up as the agent learns. Yellow = high value, dark = unknown/bad.');

  function maxQ(x, y) { return Math.max(...Q[y][x]); }
  function bestAction(x, y) {
    const qs = Q[y][x];
    let best = 0;
    for (let a = 1; a < ACTIONS; a++) if (qs[a] > qs[best]) best = a;
    return best;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (running) {
      animAccum += dt;
      const rate = episode < 200 ? 2 : episode < 500 ? 5 : 15;
      while (animAccum > 0) { animAccum -= 0.016; for (let r = 0; r < rate; r++) qUpdate(); }
    }

    ctx.clearRect(0, 0, w, h);
    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, '#0f1729'); bg.addColorStop(1, '#1a1040');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h);

    const gridSize = Math.min(w * 0.58, h - 70);
    const cellPx = gridSize / Math.max(GRID_W, GRID_H);
    const gx0 = 10, gy0 = 30;

    // Compute Q-value range for colouring
    let qMin = 0, qMax = 1;
    for (let gy = 0; gy < GRID_H; gy++) for (let gx = 0; gx < GRID_W; gx++) {
      const v = maxQ(gx, gy);
      if (v < qMin) qMin = v; if (v > qMax) qMax = v;
    }

    for (let gy = 0; gy < GRID_H; gy++) {
      for (let gx = 0; gx < GRID_W; gx++) {
        const cell = WORLD[gy][gx];
        const px = gx0 + gx * cellPx, py = gy0 + gy * cellPx;

        if (cell === 1) {
          ctx.fillStyle = '#374151';
        } else if (cell === 2) {
          ctx.fillStyle = '#7f1d1d';
        } else if (cell === 3) {
          ctx.fillStyle = '#14532d';
        } else {
          const t = Math.max(0, Math.min(1, (maxQ(gx, gy) - qMin) / (qMax - qMin + 0.01)));
          const r = Math.round(t * 245 + (1 - t) * 30);
          const g2 = Math.round(t * 200 + (1 - t) * 40);
          const b2 = Math.round((1 - t) * 80);
          ctx.fillStyle = `rgb(${r},${g2},${b2})`;
        }
        ctx.fillRect(px, py, cellPx - 1, cellPx - 1);

        // Cell labels
        ctx.font = `bold ${Math.round(cellPx * 0.35)}px Poppins,sans-serif`;
        ctx.textAlign = 'center';
        if (cell === 2) { ctx.fillStyle = '#fca5a5'; ctx.fillText('✗', px + cellPx / 2, py + cellPx * 0.65); }
        else if (cell === 3) { ctx.fillStyle = '#6ee7b7'; ctx.fillText('★', px + cellPx / 2, py + cellPx * 0.65); }
        else if (cell === 0 && episode > 5) {
          // Draw best action arrow
          const ba = bestAction(gx, gy);
          ctx.fillStyle = 'rgba(255,255,255,0.5)';
          ctx.font = `${Math.round(cellPx * 0.5)}px sans-serif`;
          ctx.fillText(ACTION_LABEL[ba], px + cellPx / 2, py + cellPx * 0.65);
        }
      }
    }

    // Grid lines
    ctx.strokeStyle = 'rgba(165,180,252,0.2)'; ctx.lineWidth = 1;
    for (let i = 0; i <= GRID_W; i++) {
      ctx.beginPath(); ctx.moveTo(gx0 + i * cellPx, gy0); ctx.lineTo(gx0 + i * cellPx, gy0 + GRID_H * cellPx); ctx.stroke();
    }
    for (let i = 0; i <= GRID_H; i++) {
      ctx.beginPath(); ctx.moveTo(gx0, gy0 + i * cellPx); ctx.lineTo(gx0 + GRID_W * cellPx, gy0 + i * cellPx); ctx.stroke();
    }

    // Agent
    const ax = gx0 + agentX * cellPx + cellPx / 2;
    const ay = gy0 + agentY * cellPx + cellPx / 2;
    const ag = ctx.createRadialGradient(ax - 3, ay - 3, 2, ax, ay, cellPx * 0.38);
    ag.addColorStop(0, '#a5f3fc'); ag.addColorStop(1, '#0891b2');
    ctx.beginPath(); ctx.arc(ax, ay, cellPx * 0.38, 0, Math.PI * 2);
    ctx.fillStyle = ag; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = `bold ${Math.round(cellPx * 0.35)}px Poppins,sans-serif`;
    ctx.textAlign = 'center'; ctx.fillText('🤖', ax, ay + cellPx * 0.13);

    // Reward history chart
    const chartX = gx0 + GRID_W * cellPx + 20;
    const chartW = w - chartX - 10;
    const chartH = Math.min(80, h * 0.25);
    const chartY = gy0;
    if (chartW > 60) {
      ctx.fillStyle = 'rgba(8,16,30,0.6)';
      if (ctx.roundRect) ctx.roundRect(chartX, chartY, chartW, chartH, 6);
      else ctx.rect(chartX, chartY, chartW, chartH);
      ctx.fill();
      ctx.strokeStyle = 'rgba(165,180,252,0.2)'; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = 'rgba(199,212,234,0.6)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Reward / episode', chartX + 4, chartY + 11);

      if (rewardHistory.length > 1) {
        const rMin = Math.min(...rewardHistory), rMax = Math.max(...rewardHistory);
        ctx.strokeStyle = '#10b981'; ctx.lineWidth = 1.5; ctx.beginPath();
        rewardHistory.forEach((r, i) => {
          const rx = chartX + (i / (rewardHistory.length - 1)) * chartW;
          const ry = chartY + chartH - 6 - ((r - rMin) / (rMax - rMin + 0.01)) * (chartH - 20);
          if (i === 0) ctx.moveTo(rx, ry); else ctx.lineTo(rx, ry);
        });
        ctx.stroke();
      }

      // Legend / info
      const infoY = chartY + chartH + 16;
      const legendItems = [
        { col: '#14532d', sym: '★', label: 'Goal (+10)' },
        { col: '#7f1d1d', sym: '✗', label: 'Pit (−5)' },
        { col: '#374151', sym: '■', label: 'Wall' },
      ];
      legendItems.forEach(({ col, sym, label }, i) => {
        ctx.fillStyle = col; ctx.fillRect(chartX + 4, infoY + i * 18, 12, 12);
        ctx.fillStyle = '#e8eefb'; ctx.font = '11px Poppins,sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(label, chartX + 20, infoY + i * 18 + 11);
      });

      // Q-value color scale
      const scaleY = infoY + 62;
      ctx.fillStyle = 'rgba(199,212,234,0.6)'; ctx.font = '10px Poppins,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText('Q-value:', chartX + 4, scaleY);
      const grad = ctx.createLinearGradient(chartX + 4, 0, chartX + chartW - 8, 0);
      grad.addColorStop(0, 'rgb(30,40,80)'); grad.addColorStop(1, 'rgb(245,200,11)');
      ctx.fillStyle = grad; ctx.fillRect(chartX + 4, scaleY + 6, chartW - 8, 8);
      ctx.fillStyle = 'rgba(199,212,234,0.5)'; ctx.font = '9px monospace';
      ctx.textAlign = 'left'; ctx.fillText('low', chartX + 4, scaleY + 24);
      ctx.textAlign = 'right'; ctx.fillText('high', chartX + chartW - 4, scaleY + 24);
    }

    epOut.set(String(episode));
    epsOut.set(epsilon.toFixed(3));
    rewOut.set(episode > 0 ? lastReward.toFixed(1) : '—');
    badge.set(running ? `Episode ${episode} | ε=${epsilon.toFixed(2)}` : episode === 0 ? 'Press Train to start' : `Trained ${episode} episodes`);
  });

  sim.start();

  return {
    dispose() { panel.dispose(); hud.dispose(); sim.dispose(); },
  };
}
