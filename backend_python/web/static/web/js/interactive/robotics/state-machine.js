import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const STATES = ['SEARCH', 'BACKUP', 'TURN', 'DOCK'];
const STATE_COLORS = { SEARCH: '#35d07f', BACKUP: '#f5b942', TURN: '#7fc7ff', DOCK: '#ff8a5c' };

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const panel = createPanel(stage, { title: 'State Machine' });
  const hud = createHud(stage);
  const stateBadge = hud.badge('SEARCH', STATE_COLORS.SEARCH);
  const battBadge = hud.badge('Battery 100%', '#35d07f');

  let simSpeed = 1;
  let dockEnabled = true;
  let running = true;
  let viewMode = '2d';

  const bot = { x: 0.3, y: 0.55, heading: 0.7, state: 'SEARCH', timer: 0, turnGoal: 0 };
  let battery = 100;
  const dock = { x: 0.12, y: 0.14 };
  let placed = false;

  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  panel.toggle({ label: 'Running', value: true, onChange: (v) => { running = v; } });
  panel.slider({
    label: 'Sim speed', min: 0.5, max: 3, step: 0.25, value: 1,
    format: (v) => v.toFixed(2) + '×',
    onChange: (v) => { simSpeed = v; },
  });
  panel.toggle({
    label: 'Enable DOCK state', value: true,
    onChange: (v) => { dockEnabled = v; },
  });
  panel.button({
    label: 'Drain battery to 20%', icon: 'battery_alert',
    onClick: () => { battery = Math.min(battery, 20); },
  });
  panel.button({
    label: 'Recharge & reset', icon: 'restart_alt', variant: 'ghost',
    onClick: () => {
      battery = 100;
      bot.x = 0.3; bot.y = 0.55; bot.heading = 0.7;
      setState('SEARCH');
    },
  });
  panel.info('Watch the diagram: the glowing node is the active state. Bumping a wall fires SEARCH→BACKUP→TURN→SEARCH. Battery below 15% sends every state to DOCK.');

  function setState(s) {
    bot.state = s;
    bot.timer = 0;
    stateBadge.set(s);
    stateBadge.el.style.setProperty('--ix-hud-color', STATE_COLORS[s]);
    if (s === 'TURN') bot.turnGoal = bot.heading + (Math.random() * 2 - 1) * 2.2 + Math.PI * 0.5 * (Math.random() < 0.5 ? -1 : 1);
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const roomW = w * 0.62;
    const roomH = h * 0.84;
    const roomX = w * 0.04;
    const roomY = h * 0.08;
    const r = Math.min(roomW, roomH) * 0.05;

    if (!placed && w > 10) placed = true;

    if (running && placed) {
      const sdt = dt * simSpeed;
      battery = Math.max(0, battery - sdt * (bot.state === 'DOCK' ? 0.4 : 1.4));
      const speed = 0.13;

      if (dockEnabled && battery < 15 && bot.state !== 'DOCK') setState('DOCK');

      if (bot.state === 'SEARCH') {
        bot.x += Math.cos(bot.heading) * speed * sdt;
        bot.y += Math.sin(bot.heading) * speed * sdt;
        if (bot.x < 0.05 || bot.x > 0.95 || bot.y < 0.05 || bot.y > 0.95) {
          bot.x = Math.max(0.05, Math.min(0.95, bot.x));
          bot.y = Math.max(0.05, Math.min(0.95, bot.y));
          setState('BACKUP');
        }
      } else if (bot.state === 'BACKUP') {
        bot.timer += sdt;
        bot.x -= Math.cos(bot.heading) * speed * 0.7 * sdt;
        bot.y -= Math.sin(bot.heading) * speed * 0.7 * sdt;
        bot.x = Math.max(0.05, Math.min(0.95, bot.x));
        bot.y = Math.max(0.05, Math.min(0.95, bot.y));
        if (bot.timer > 0.8) setState('TURN');
      } else if (bot.state === 'TURN') {
        const diff = bot.turnGoal - bot.heading;
        bot.heading += Math.sign(diff) * Math.min(Math.abs(diff), 2.4 * sdt);
        if (Math.abs(diff) < 0.05) setState('SEARCH');
      } else if (bot.state === 'DOCK') {
        const dx = dock.x - bot.x;
        const dy = dock.y - bot.y;
        const dist = Math.hypot(dx, dy);
        if (dist > 0.03) {
          const goal = Math.atan2(dy, dx);
          let diff = goal - bot.heading;
          while (diff > Math.PI) diff -= Math.PI * 2;
          while (diff < -Math.PI) diff += Math.PI * 2;
          bot.heading += Math.sign(diff) * Math.min(Math.abs(diff), 3 * sdt);
          bot.x += Math.cos(bot.heading) * speed * sdt;
          bot.y += Math.sin(bot.heading) * speed * sdt;
        } else {
          battery = Math.min(100, battery + sdt * 14);
          if (battery >= 99) setState('SEARCH');
        }
      }
    }

    battBadge.set('Battery ' + Math.round(battery) + '%');
    battBadge.el.style.setProperty('--ix-hud-color', battery < 15 ? '#e2484d' : battery < 40 ? '#f5b942' : '#35d07f');

    ctx.clearRect(0, 0, w, h);

    if (viewMode === '3d') {
      const room = [
        projectRoom(0, 0, roomX, roomY, roomW, roomH),
        projectRoom(1, 0, roomX, roomY, roomW, roomH),
        projectRoom(1, 1, roomX, roomY, roomW, roomH),
        projectRoom(0, 1, roomX, roomY, roomW, roomH),
      ];
      ctx.fillStyle = '#22344f';
      ctx.beginPath();
      ctx.moveTo(room[0].x, room[0].y - 8);
      ctx.lineTo(room[1].x, room[1].y - 8);
      ctx.lineTo(room[2].x, room[2].y + 8);
      ctx.lineTo(room[3].x, room[3].y + 8);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = '#d9e2ee';
      ctx.beginPath();
      ctx.moveTo(room[0].x, room[0].y);
      for (let i = 1; i < room.length; i++) ctx.lineTo(room[i].x, room[i].y);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = 'rgba(16,21,31,0.25)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      const dockP = projectRoom(dock.x, dock.y, roomX, roomY, roomW, roomH, r * 0.35);
      ctx.fillStyle = 'rgba(0,0,0,0.2)';
      ctx.beginPath();
      ctx.ellipse(dockP.x, dockP.y + r * 0.45, r * 1.1, r * 0.38, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ff8a5c';
      ctx.beginPath();
      ctx.moveTo(dockP.x, dockP.y - r);
      ctx.lineTo(dockP.x + r, dockP.y);
      ctx.lineTo(dockP.x, dockP.y + r);
      ctx.lineTo(dockP.x - r, dockP.y);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = '#5c2a10';
      ctx.font = '700 ' + Math.round(r * 0.8) + 'px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('⚡', dockP.x, dockP.y + r * 0.28);

      const bp = projectRoom(bot.x, bot.y, roomX, roomY, roomW, roomH, r * 0.5);
      const hp = projectRoom(bot.x + Math.cos(bot.heading) * 0.08, bot.y + Math.sin(bot.heading) * 0.08, roomX, roomY, roomW, roomH, r * 0.5);
      ctx.fillStyle = 'rgba(0,0,0,0.22)';
      ctx.beginPath();
      ctx.ellipse(bp.x, bp.y + r * 0.7, r * 1.1, r * 0.42, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.save();
      ctx.translate(bp.x, bp.y);
      ctx.rotate(Math.atan2(hp.y - bp.y, hp.x - bp.x));
      ctx.scale(1, 0.74);
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.fillStyle = STATE_COLORS[bot.state];
      ctx.fill();
      ctx.strokeStyle = '#10151f';
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(r * 1.1, 0);
      ctx.lineTo(r * 0.4, -r * 0.5);
      ctx.lineTo(r * 0.4, r * 0.5);
      ctx.closePath();
      ctx.fillStyle = '#10151f';
      ctx.fill();
      ctx.restore();
    } else {
      ctx.fillStyle = '#22344f';
      roundRect(ctx, roomX - 6, roomY - 6, roomW + 12, roomH + 12, 12);
      ctx.fill();
      ctx.fillStyle = '#d9e2ee';
      roundRect(ctx, roomX, roomY, roomW, roomH, 8);
      ctx.fill();

      const dockPx = roomX + dock.x * roomW;
      const dockPy = roomY + dock.y * roomH;
      ctx.fillStyle = '#ff8a5c';
      roundRect(ctx, dockPx - r * 0.9, dockPy - r * 0.9, r * 1.8, r * 1.8, 5);
      ctx.fill();
      ctx.fillStyle = '#5c2a10';
      ctx.font = '700 ' + Math.round(r * 0.8) + 'px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('⚡', dockPx, dockPy + r * 0.3);

      const bx = roomX + bot.x * roomW;
      const by = roomY + bot.y * roomH;
      ctx.save();
      ctx.translate(bx, by);
      ctx.rotate(bot.heading);
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.fillStyle = STATE_COLORS[bot.state];
      ctx.fill();
      ctx.strokeStyle = '#10151f';
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(r * 1.1, 0);
      ctx.lineTo(r * 0.4, -r * 0.5);
      ctx.lineTo(r * 0.4, r * 0.5);
      ctx.closePath();
      ctx.fillStyle = '#10151f';
      ctx.fill();
      ctx.restore();
    }

    const dgX = w * 0.70;
    const dgW = w * 0.27;
    const nodeH = Math.min(40, h * 0.075);
    const gap = (h * 0.8 - nodeH * 4) / 3.4;
    ctx.font = '700 ' + Math.round(nodeH * 0.36) + 'px Poppins, sans-serif';

    const nodes = {};
    STATES.forEach((s, i) => {
      const ny = h * 0.10 + i * (nodeH + gap);
      nodes[s] = { x: dgX, y: ny, w: dgW, h: nodeH };
    });

    ctx.strokeStyle = 'rgba(199,212,234,0.5)';
    ctx.lineWidth = 1.6;
    arrow(ctx, dgX + dgW * 0.5, nodes.SEARCH.y + nodeH, dgX + dgW * 0.5, nodes.BACKUP.y);
    arrow(ctx, dgX + dgW * 0.5, nodes.BACKUP.y + nodeH, dgX + dgW * 0.5, nodes.TURN.y);
    ctx.beginPath();
    ctx.moveTo(dgX, nodes.TURN.y + nodeH / 2);
    ctx.lineTo(dgX - 14, nodes.TURN.y + nodeH / 2);
    ctx.lineTo(dgX - 14, nodes.SEARCH.y + nodeH / 2);
    ctx.lineTo(dgX, nodes.SEARCH.y + nodeH / 2);
    ctx.stroke();
    arrowHead(ctx, dgX, nodes.SEARCH.y + nodeH / 2, 0);
    if (dockEnabled) {
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(dgX + dgW * 0.5, nodes.TURN.y + nodeH);
      ctx.lineTo(dgX + dgW * 0.5, nodes.DOCK.y);
      ctx.stroke();
      ctx.setLineDash([]);
      arrowHead(ctx, dgX + dgW * 0.5, nodes.DOCK.y, Math.PI / 2);
    }

    STATES.forEach((s) => {
      const n = nodes[s];
      const active = bot.state === s;
      const enabled = s !== 'DOCK' || dockEnabled;
      ctx.fillStyle = active ? STATE_COLORS[s] : 'rgba(28,44,68,0.9)';
      ctx.globalAlpha = enabled ? 1 : 0.35;
      roundRect(ctx, n.x, n.y, n.w, n.h, 9);
      ctx.fill();
      ctx.strokeStyle = active ? '#ffffff' : 'rgba(199,212,234,0.35)';
      ctx.lineWidth = active ? 2.5 : 1.2;
      ctx.stroke();
      ctx.fillStyle = active ? '#0c1626' : '#c7d4ea';
      ctx.textAlign = 'center';
      ctx.fillText(s, n.x + n.w / 2, n.y + n.h / 2 + nodeH * 0.13);
      ctx.globalAlpha = 1;
    });

    ctx.fillStyle = 'rgba(199,212,234,0.6)';
    ctx.font = '500 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('bump', dgX + dgW * 0.5 + 22, (nodes.SEARCH.y + nodeH + nodes.BACKUP.y) / 2 + 3);
    ctx.fillText('done', dgX + dgW * 0.5 + 22, (nodes.BACKUP.y + nodeH + nodes.TURN.y) / 2 + 3);
    if (dockEnabled) {
      const midGap = (nodes.TURN.y + nodeH + nodes.DOCK.y) / 2;
      ctx.fillText('any state', dgX + dgW * 0.5, midGap - 3);
      ctx.fillText('battery low', dgX + dgW * 0.5, midGap + 9);
    }
  });

  function projectRoom(nx, ny, roomX, roomY, roomW, roomH, z = 0) {
    const cx = roomX + roomW * 0.5;
    const cy = roomY + roomH * 0.5;
    const x = roomX + nx * roomW;
    const y = roomY + ny * roomH;
    return { x: cx + (x - cx) * 0.92, y: cy + (y - cy) * 0.55 - z };
  }

  function arrow(ctx, x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    arrowHead(ctx, x2, y2, Math.atan2(y2 - y1, x2 - x1));
  }

  function arrowHead(ctx, x, y, ang) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x - 7 * Math.cos(ang - 0.45), y - 7 * Math.sin(ang - 0.45));
    ctx.moveTo(x, y);
    ctx.lineTo(x - 7 * Math.cos(ang + 0.45), y - 7 * Math.sin(ang + 0.45));
    ctx.stroke();
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
    else ctx.rect(x, y, w, h);
  }

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
