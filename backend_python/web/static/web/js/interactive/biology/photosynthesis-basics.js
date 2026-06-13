import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Kid-friendly photosynthesis — tune sunlight & water, watch plant grow & produce O₂
// Shows the equation: CO₂ + H₂O + light → glucose + O₂

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const growthBadge = hud.badge('Plant: growing!', '#22c55e');

  let sunlight = 70;    // 0-100
  let water = 60;       // 0-100
  let co2 = 80;         // fixed at atmosphere, show as info
  let plantHeight = 0.3; // 0..1
  let oxygenCount = 0;
  const oxygenBubbles = [];
  let glucoseStored = 0;
  let elapsed = 0;

  const panel = createPanel(stage, { title: 'Photosynthesis' });
  panel.slider({
    label: '☀️ Sunlight',
    min: 0, max: 100, step: 1, value: sunlight,
    format: (v) => `${v}%`,
    onChange: (v) => { sunlight = v; },
  });
  panel.slider({
    label: '💧 Water',
    min: 0, max: 100, step: 1, value: water,
    format: (v) => `${v}%`,
    onChange: (v) => { water = v; },
  });
  panel.divider();
  const heightOut = panel.readout({ label: 'Plant height', value: '30%' });
  const o2Out = panel.readout({ label: 'O₂ produced', value: '0' });
  const glucoseOut = panel.readout({ label: 'Glucose stored', value: '0' });
  panel.button({
    label: 'Reset plant',
    icon: 'replay',
    onClick: () => { plantHeight = 0.3; oxygenCount = 0; glucoseStored = 0; oxygenBubbles.length = 0; },
  });
  panel.info('Photosynthesis equation: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ (glucose) + 6O₂. Give the plant plenty of sunlight and water to watch it grow and release oxygen bubbles!');

  function computeRate() {
    const s = sunlight / 100;
    const w2 = water / 100;
    // Limiting factor: minimum of sunlight and water determines rate
    const rate = Math.min(s, w2) * 0.8 + (s + w2) / 2 * 0.2;
    return rate;
  }

  let bubbleTimer = 0;

  sim.setUpdate((ctx, dt, w, h) => {
    elapsed += dt;
    const rate = computeRate();

    // Grow plant
    if (plantHeight < 1.0) {
      plantHeight = Math.min(1.0, plantHeight + rate * dt * 0.008);
    }

    // O₂ bubbles
    bubbleTimer += dt;
    const bubbleInterval = rate > 0.05 ? 1 / (rate * 4) : 999;
    if (bubbleTimer > bubbleInterval) {
      bubbleTimer = 0;
      oxygenCount++;
      oxygenBubbles.push({
        x: w * 0.52 + (Math.random() - 0.5) * 60,
        y: h * (0.55 - plantHeight * 0.35),
        age: 0,
        vx: (Math.random() - 0.5) * 12,
        r: 5 + Math.random() * 6,
      });
      glucoseStored += 0.1;
    }

    for (const b of oxygenBubbles) {
      b.age += dt;
      b.y -= 20 * dt;
      b.x += b.vx * dt;
    }
    for (let i = oxygenBubbles.length - 1; i >= 0; i--) {
      if (oxygenBubbles[i].age > 3.5 || oxygenBubbles[i].y < 0) oxygenBubbles.splice(i, 1);
    }

    heightOut.set(`${Math.round(plantHeight * 100)}%`);
    o2Out.set(`${oxygenCount}`);
    glucoseOut.set(`${glucoseStored.toFixed(0)} units`);
    growthBadge.set(rate > 0.5 ? 'Growing fast!' : rate > 0.1 ? 'Growing slowly…' : 'Needs more light/water!');

    ctx.clearRect(0, 0, w, h);

    // Sky gradient (darker with less sunlight)
    const skyBright = sunlight / 100;
    const skyGrad = ctx.createLinearGradient(0, 0, 0, h * 0.7);
    skyGrad.addColorStop(0, `rgba(${Math.round(20 + skyBright * 100)},${Math.round(50 + skyBright * 130)},${Math.round(100 + skyBright * 80)},1)`);
    skyGrad.addColorStop(1, `rgba(${Math.round(30 + skyBright * 80)},${Math.round(70 + skyBright * 80)},${Math.round(50 + skyBright * 40)},1)`);
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, w, h * 0.7);

    // Ground
    ctx.fillStyle = '#5a3a1a';
    ctx.fillRect(0, h * 0.7, w, h * 0.3);
    ctx.fillStyle = '#6b4a2a';
    ctx.fillRect(0, h * 0.7, w, h * 0.04);

    // Sun
    if (sunlight > 5) {
      const sunX = w * 0.85;
      const sunY = h * 0.12;
      const sunR = 36 * (0.5 + skyBright * 0.5);
      const sunGrad = ctx.createRadialGradient(sunX, sunY, 4, sunX, sunY, sunR);
      sunGrad.addColorStop(0, `rgba(255,240,100,${skyBright})`);
      sunGrad.addColorStop(0.5, `rgba(255,200,50,${skyBright * 0.7})`);
      sunGrad.addColorStop(1, 'rgba(255,150,0,0)');
      ctx.fillStyle = sunGrad;
      ctx.beginPath();
      ctx.arc(sunX, sunY, sunR, 0, Math.PI * 2);
      ctx.fill();

      // Sunbeams
      ctx.strokeStyle = `rgba(255,220,80,${skyBright * 0.4})`;
      ctx.lineWidth = 1.5;
      for (let i = 0; i < 8; i++) {
        const a = (i / 8) * Math.PI * 2 + elapsed * 0.15;
        ctx.beginPath();
        ctx.moveTo(sunX + Math.cos(a) * sunR * 1.1, sunY + Math.sin(a) * sunR * 1.1);
        ctx.lineTo(sunX + Math.cos(a) * sunR * 1.7, sunY + Math.sin(a) * sunR * 1.7);
        ctx.stroke();
      }
    }

    // Rain drops if water > 70
    if (water > 70 && Math.random() < 0.3) {
      for (let i = 0; i < 3; i++) {
        const rx = Math.random() * w;
        const ry = h * 0.1 + Math.random() * h * 0.5;
        ctx.strokeStyle = 'rgba(100,160,220,0.5)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(rx, ry);
        ctx.lineTo(rx - 2, ry + 12);
        ctx.stroke();
      }
    }

    // Plant
    const plantX = w * 0.45;
    const groundLevel = h * 0.7;
    const maxStemH = h * 0.5;
    const stemH = plantHeight * maxStemH;

    // Stem
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = Math.max(3, plantHeight * 8);
    ctx.beginPath();
    ctx.moveTo(plantX, groundLevel);
    // Slight sway
    const sway = Math.sin(elapsed * 0.8) * 8 * plantHeight;
    ctx.quadraticCurveTo(plantX + sway * 0.5, groundLevel - stemH * 0.5, plantX + sway, groundLevel - stemH);
    ctx.stroke();

    const topX = plantX + sway;
    const topY = groundLevel - stemH;

    // Leaves
    const numLeaves = Math.floor(plantHeight * 5) + 1;
    ctx.fillStyle = '#16a34a';
    for (let i = 0; i < numLeaves; i++) {
      const ly = groundLevel - stemH * ((i + 1) / (numLeaves + 1));
      const side = i % 2 === 0 ? 1 : -1;
      const leafSize = 18 + plantHeight * 18;
      ctx.save();
      ctx.translate(plantX + sway * ((i + 1) / (numLeaves + 1)), ly);
      ctx.rotate(side * 0.5);
      ctx.beginPath();
      ctx.ellipse(side * leafSize * 0.6, 0, leafSize, leafSize * 0.35, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Flower at top if fully grown
    if (plantHeight > 0.85) {
      ctx.fillStyle = '#fde68a';
      ctx.beginPath();
      ctx.arc(topX, topY, 14, 0, Math.PI * 2);
      ctx.fill();
      for (let i = 0; i < 6; i++) {
        const fa = (i / 6) * Math.PI * 2;
        ctx.fillStyle = '#f9a8d4';
        ctx.beginPath();
        ctx.ellipse(topX + Math.cos(fa) * 18, topY + Math.sin(fa) * 18, 8, 12, fa, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Roots
    const waterSaturation = water / 100;
    ctx.strokeStyle = '#a16207';
    ctx.lineWidth = 2;
    for (let i = 0; i < 4; i++) {
      const ra = (i / 3 - 0.5) * Math.PI * 0.6;
      ctx.beginPath();
      ctx.moveTo(plantX, groundLevel);
      ctx.lineTo(plantX + Math.cos(ra + Math.PI / 2) * 35, groundLevel + 25 + i * 4);
      ctx.stroke();
    }
    // Water droplets in soil
    for (let i = 0; i < Math.floor(waterSaturation * 8); i++) {
      ctx.fillStyle = 'rgba(100,160,220,0.6)';
      ctx.beginPath();
      ctx.arc(plantX - 50 + i * 15 + (Math.random() - 0.5) * 10, groundLevel + 15 + Math.random() * 20, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // CO₂ arrows coming in
    ctx.fillStyle = 'rgba(180,200,180,0.55)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText('CO₂ →', topX - 35, topY + 8);
    ctx.fillText('H₂O ↑', plantX - 30, groundLevel - 20);

    // O₂ bubbles
    oxygenBubbles.forEach((b) => {
      const alpha = Math.max(0, 1 - b.age / 3.5);
      ctx.strokeStyle = `rgba(100,220,255,${alpha * 0.8})`;
      ctx.fillStyle = `rgba(180,240,255,${alpha * 0.3})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = `rgba(100,220,255,${alpha * 0.9})`;
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('O₂', b.x, b.y + 3);
    });

    // Equation banner
    const eqY = h - 32;
    ctx.fillStyle = 'rgba(8,14,8,0.8)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(6, eqY, w - 12, 24, 6);
    else ctx.rect(6, eqY, w - 12, 24);
    ctx.fill();
    ctx.fillStyle = '#86efac';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('6CO₂ + 6H₂O + ☀️ light → C₆H₁₂O₆ (glucose) + 6O₂', w / 2, eqY + 16);
  });

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
