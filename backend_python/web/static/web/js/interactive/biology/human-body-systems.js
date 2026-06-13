import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Human body systems — 2D interactive diagram, click organs for function
// Systems: digestive, circulatory, respiratory, skeletal

const SYSTEMS = {
  digestive: {
    label: 'Digestive System',
    color: '#f59e0b',
    organs: [
      {
        name: 'Mouth',
        x: 0.5, y: 0.12,
        r: 18,
        info: 'Food enters here! Teeth chew food into smaller pieces (mechanical digestion) and saliva starts breaking down starch with amylase enzyme. Chewing mixes food with saliva to make swallowing easier.',
      },
      {
        name: 'Stomach',
        x: 0.44, y: 0.42,
        r: 26,
        info: 'A muscular bag that churns food and mixes it with strong acid (HCl, pH ~2) and pepsin enzyme to digest proteins. Food stays here 2-4 hours turning into a soupy liquid called chyme.',
      },
      {
        name: 'Small Intestine',
        x: 0.5, y: 0.6,
        r: 22,
        info: 'About 6 metres long and coiled up! Most digestion and ALL absorption happens here. Tiny finger-like villi absorb nutrients (glucose, amino acids, fatty acids) into the blood.',
      },
      {
        name: 'Large Intestine',
        x: 0.5, y: 0.77,
        r: 18,
        info: 'Absorbs water from undigested food, turning it from liquid to solid. Friendly bacteria here make vitamins K and B12. Whatever cannot be absorbed becomes faeces and leaves the body.',
      },
    ],
  },
  circulatory: {
    label: 'Circulatory System',
    color: '#ef4444',
    organs: [
      {
        name: 'Heart',
        x: 0.5, y: 0.32,
        r: 26,
        info: 'Your amazing pump! It beats about 70 times a minute — 2.5 billion times in a lifetime. The right side pumps blood to the lungs to pick up oxygen. The left side pumps oxygen-rich blood to the whole body.',
      },
      {
        name: 'Arteries',
        x: 0.38, y: 0.5,
        r: 14,
        info: 'Strong, thick-walled blood vessels that carry blood AWAY from the heart. Arteries carry oxygen-rich (oxygenated) blood to body organs. You can feel your pulse where arteries run close to the skin.',
      },
      {
        name: 'Veins',
        x: 0.62, y: 0.5,
        r: 14,
        info: 'Blood vessels that carry blood BACK to the heart. They carry deoxygenated blood (used up oxygen). Veins have valves to stop blood flowing backwards — important because blood flows against gravity in your legs.',
      },
    ],
  },
  respiratory: {
    label: 'Respiratory System',
    color: '#7dd3fc',
    organs: [
      {
        name: 'Lungs',
        x: 0.5, y: 0.34,
        r: 32,
        info: 'Two spongy organs that fill most of your chest. Each breath brings oxygen in and takes carbon dioxide out. Inside are millions of tiny air sacs (alveoli) — if spread flat they would cover a tennis court!',
      },
      {
        name: 'Trachea (windpipe)',
        x: 0.5, y: 0.18,
        r: 14,
        info: 'The airway from your throat to your lungs. C-shaped cartilage rings keep it open so you can breathe even when you swallow. It splits into two bronchi, one going to each lung.',
      },
      {
        name: 'Diaphragm',
        x: 0.5, y: 0.52,
        r: 18,
        info: 'A dome-shaped muscle below the lungs. When it contracts and flattens, it increases the chest space, pulling air in (inhaling). When it relaxes and curves upward, it pushes air out (exhaling). Your diaphragm never stops working!',
      },
    ],
  },
  skeletal: {
    label: 'Skeletal System',
    color: '#d4d4d4',
    organs: [
      {
        name: 'Skull',
        x: 0.5, y: 0.10,
        r: 24,
        info: 'A helmet of 22 bones fused together to protect your brain — the most important organ. The skull also gives shape to your face. The only moving bone in the skull is the mandible (jaw), for chewing and talking.',
      },
      {
        name: 'Spine',
        x: 0.54, y: 0.46,
        r: 16,
        info: '33 vertebrae (small bones) stacked like building blocks with soft discs between them as shock absorbers. The spine protects your spinal cord (nerve highway) and lets you bend and twist. It also holds your whole skeleton together.',
      },
      {
        name: 'Femur (thigh bone)',
        x: 0.44, y: 0.71,
        r: 16,
        info: 'The longest and strongest bone in your body. It connects your hip to your knee. Inside all large bones is red bone marrow — the factory where your blood cells are made (about 2 million new red blood cells every second!).',
      },
    ],
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const systemBadge = hud.badge('Digestive System', '#f59e0b');
  const tipBadge = hud.badge('Click an organ!', '#84CC16');

  let activeSystem = 'digestive';
  let hoveredOrgan = null;
  let clickedOrgan = null;

  const panel = createPanel(stage, { title: 'Body Systems' });
  panel.buttonRow([
    { label: 'Digestive', onClick: () => { activeSystem = 'digestive'; clickedOrgan = null; systemBadge.set('Digestive System'); } },
    { label: 'Circulatory', onClick: () => { activeSystem = 'circulatory'; clickedOrgan = null; systemBadge.set('Circulatory System'); } },
  ]);
  panel.buttonRow([
    { label: 'Respiratory', onClick: () => { activeSystem = 'respiratory'; clickedOrgan = null; systemBadge.set('Respiratory System'); } },
    { label: 'Skeletal', onClick: () => { activeSystem = 'skeletal'; clickedOrgan = null; systemBadge.set('Skeletal System'); } },
  ]);
  panel.info('Choose a body system, then click any highlighted organ to learn what it does!');

  function getOrgansWithPx(w, h) {
    const sys = SYSTEMS[activeSystem];
    return sys.organs.map((o) => ({ ...o, px: o.x * w, py: o.y * h }));
  }

  function onPointerMove(e) {
    const rect = sim.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const organs = getOrgansWithPx(sim.width, sim.height);
    hoveredOrgan = organs.find((o) => Math.hypot(mx - o.px, my - o.py) < o.r + 10) || null;
    sim.canvas.style.cursor = hoveredOrgan ? 'pointer' : 'default';
  }

  function onClick(e) {
    const rect = sim.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const organs = getOrgansWithPx(sim.width, sim.height);
    const clicked = organs.find((o) => Math.hypot(mx - o.px, my - o.py) < o.r + 10);
    if (clicked) {
      clickedOrgan = clicked;
    }
  }

  sim.canvas.addEventListener('pointermove', onPointerMove);
  sim.canvas.addEventListener('click', onClick);

  let pulse = 0;

  sim.setUpdate((ctx, dt, w, h) => {
    pulse += dt * 3;

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0a1628');
    bg.addColorStop(1, '#060e1a');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    const sys = SYSTEMS[activeSystem];

    // Draw body outline (simple silhouette)
    const bodyX = w * 0.5;
    const bodyTop = h * 0.08;
    const bodyH = h * 0.82;
    const bodyW = w * 0.35;

    ctx.strokeStyle = `rgba(${parseInt(sys.color.slice(1, 3), 16)},${parseInt(sys.color.slice(3, 5), 16)},${parseInt(sys.color.slice(5, 7), 16)},0.25)`;
    ctx.lineWidth = 2;
    // Head
    ctx.beginPath();
    ctx.arc(bodyX, bodyTop + bodyW * 0.28, bodyW * 0.24, 0, Math.PI * 2);
    ctx.stroke();
    // Torso
    ctx.beginPath();
    ctx.roundRect
      ? ctx.roundRect(bodyX - bodyW * 0.32, bodyTop + bodyW * 0.56, bodyW * 0.64, bodyH * 0.45, 12)
      : ctx.rect(bodyX - bodyW * 0.32, bodyTop + bodyW * 0.56, bodyW * 0.64, bodyH * 0.45);
    ctx.stroke();
    // Legs
    ctx.beginPath();
    ctx.rect(bodyX - bodyW * 0.28, bodyTop + bodyW * 0.56 + bodyH * 0.45, bodyW * 0.22, bodyH * 0.28);
    ctx.stroke();
    ctx.beginPath();
    ctx.rect(bodyX + bodyW * 0.06, bodyTop + bodyW * 0.56 + bodyH * 0.45, bodyW * 0.22, bodyH * 0.28);
    ctx.stroke();

    // Draw organs
    const organs = getOrgansWithPx(w, h);
    organs.forEach((organ) => {
      const isHovered = organ === hoveredOrgan;
      const isClicked = organ === clickedOrgan;
      const glowScale = isHovered ? 1 + 0.15 * Math.sin(pulse * 2) : 1;

      // Glow ring for hover
      if (isHovered || isClicked) {
        ctx.strokeStyle = sys.color;
        ctx.lineWidth = 2.5;
        ctx.globalAlpha = 0.5 + 0.3 * Math.sin(pulse * 2);
        ctx.beginPath();
        ctx.arc(organ.px, organ.py, organ.r * 1.35, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
      }

      // Main organ circle
      ctx.fillStyle = isClicked ? sys.color : `${sys.color}88`;
      ctx.beginPath();
      ctx.arc(organ.px, organ.py, organ.r * glowScale, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = sys.color;
      ctx.lineWidth = 2;
      ctx.stroke();

      // Label
      ctx.fillStyle = isClicked ? '#ffffff' : 'rgba(220,235,255,0.8)';
      ctx.font = `${isClicked ? '700' : '600'} ${Math.max(8, organ.r * 0.45)}px Poppins, sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(organ.name, organ.px, organ.py);
      ctx.textBaseline = 'alphabetic';
    });

    // Info card at bottom
    if (clickedOrgan) {
      const infoY = h * 0.82;
      const infoH = h * 0.16;
      ctx.fillStyle = 'rgba(8,16,30,0.88)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(8, infoY, w - 16, infoH, 8);
      else ctx.rect(8, infoY, w - 16, infoH);
      ctx.fill();
      ctx.strokeStyle = sys.color;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = sys.color;
      ctx.font = '700 11px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(clickedOrgan.name, 16, infoY + 14);

      ctx.fillStyle = 'rgba(200,220,255,0.9)';
      ctx.font = '600 9px Poppins, sans-serif';
      const words = clickedOrgan.info.split(' ');
      let line = '';
      let ly2 = infoY + 28;
      for (const word of words) {
        const test = line + word + ' ';
        if (ctx.measureText(test).width > w - 28 && line) {
          ctx.fillText(line.trim(), 16, ly2);
          line = word + ' ';
          ly2 += 12;
          if (ly2 > infoY + infoH - 4) break;
        } else {
          line = test;
        }
      }
      if (ly2 <= infoY + infoH - 4) ctx.fillText(line.trim(), 16, ly2);
    }

    // Title
    ctx.fillStyle = sys.color;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(sys.label, 10, 18);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointermove', onPointerMove);
      sim.canvas.removeEventListener('click', onClick);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
