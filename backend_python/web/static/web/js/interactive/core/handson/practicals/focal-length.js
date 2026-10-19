// Focal length of a convex lens on an optical bench: a candle, the lens in its holder and a white
// screen ride on a metre-long bench. The student sets the candle at some distance u from the lens
// and slides the screen until the inverted image of the flame is sharpest. The picture on the
// screen is drawn from the optics: the image forms at v = uf/(u - f) with magnification v/u, and
// a screen away from v shows the blur circle of the lens aperture, d·|s - v|/v wide. Several
// (u, v) pairs give f = uv/(u + v), and the 1/u + 1/v graph cuts both axes at 1/f.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { createGraph, fitLine } from '../stopwatch.js';
import { flameMaterial, flameGeometry } from '../flame.js';

const BY = 0.8; const LENS_X = 0; const APERTURE = 4.0;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function benchTex() {
  return canvasTexture('ho-optbench', 8192, 128, (g, w, h) => {
    g.fillStyle = '#e8dcc0'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    for (let mm = 0; mm <= 1500; mm += 5) { const x = 20 + (w - 40) * mm / 1500; const cm = mm % 10 === 0; const ten = mm % 100 === 0; g.fillRect(Math.round(x), 0, cm ? 3 : 1.5, ten ? 60 : cm ? 36 : 20); if (ten) { g.font = '700 40px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(mm / 10 - 75), x, 104); } }
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: '1/v against 1/u', xLabel: '1/u (cm⁻¹ × 100)', yLabel: '1/v (cm⁻¹ × 100)' });
  const f = Math.round(10 + Math.random() * 8);
  const st = { u: 30, s: 20, readings: [] };
  const X = (cm) => LENS_X + cm / 10;

  world.add(mesh(new THREE.BoxGeometry(15.4, 0.12, 0.5), MAT.matte(0x2b3138), [0, 0.06, 0]));
  const scale = new THREE.Mesh(new THREE.PlaneGeometry(15.2, 0.16), new THREE.MeshStandardMaterial({ map: benchTex(), roughness: 0.6 })); scale.rotation.x = -Math.PI / 2; scale.position.set(0, 0.122, 0.17); world.add(scale);
  const upright = (x, h) => { const g = new THREE.Group(); g.position.x = x; g.add(mesh(new THREE.BoxGeometry(0.3, 0.06, 0.42), MAT.matte(0x111827), [0, 0.15, 0])); g.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, h, 10), MAT.steel(), [0, 0.18 + h / 2, 0])); world.add(g); return g; };
  const lens = upright(X(0), 0.9);
  const glass = mesh(new THREE.SphereGeometry(0.4, 40, 20), new THREE.MeshPhysicalMaterial({ color: 0xeef8ff, transmission: 0, roughness: 0.02, transparent: true, opacity: 0.35, clearcoat: 1, depthWrite: false }), [0, 1.35, 0], { cast: false });
  glass.scale.set(0.08, 1, 1); glass.renderOrder = 5; lens.add(glass);
  lens.add(mesh(new THREE.TorusGeometry(0.4, 0.025, 8, 40), MAT.matte(0x1f2937), [0, 1.35, 0]).rotateY(Math.PI / 2));
  const candle = upright(X(-30), 0.5);
  candle.add(mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.75, 18), MAT.matte(0xf5f0e1), [0, 1.05, 0]));
  const flame = new THREE.Mesh(flameGeometry(0.05, 0.22), flameMaterial({ color: 0xffa630, tip: 0xffe7a1, alpha: 0.95, height: 0.22, wobble: 0.01 })); flame.position.y = 1.44; flame.renderOrder = 8; candle.add(flame);
  const screenU = upright(X(20), 0.6);
  const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 256;
  const tex = new THREE.CanvasTexture(canvas); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const screenFace = mesh(new THREE.PlaneGeometry(0.9, 0.9), new THREE.MeshBasicMaterial({ map: tex }), [0, 1.35, 0]); screenFace.rotation.y = -Math.PI / 2; screenU.add(screenFace);
  screenU.add(mesh(new THREE.BoxGeometry(0.04, 0.96, 0.96), MAT.matte(0x111827), [0.025, 1.35, 0]));

  function image() {
    const u = st.u; const v = u > f + 0.01 ? (u * f) / (u - f) : Infinity; const m = v / u;
    const blur = Number.isFinite(v) ? APERTURE * Math.abs(st.s - v) / v : 3;
    return { v, m, blur };
  }
  let lastKey = '';
  function drawScreen(t) {
    const { v, m, blur } = image();
    const key = `${st.s.toFixed(2)}|${st.u.toFixed(2)}|${Math.floor(t * 8)}`; if (key === lastKey) return; lastKey = key;
    const g = canvas.getContext('2d'); const W = 256;
    g.fillStyle = '#f7f5ef'; g.fillRect(0, 0, W, W);
    const pxPerCm = W / 9; const H = 1.4 * (Number.isFinite(m) ? m : 0) * pxPerCm * 2.2;
    const blurPx = Math.min(40, blur * pxPerCm * 0.9);
    if (H > 2 && Number.isFinite(v)) {
      g.save(); g.filter = `blur(${blurPx.toFixed(1)}px)`;
      // the image is inverted: the candle hangs from the top, its flame points down
      const cx = W / 2; const flick = 1 + 0.05 * Math.sin(t * 13); const y0 = W / 2 - H * 0.55;
      g.fillStyle = 'rgba(232,226,210,.95)'; g.fillRect(cx - H * 0.09, y0 - H * 0.6, H * 0.18, H * 0.6);
      g.fillStyle = 'rgba(40,30,20,.9)'; g.fillRect(cx - H * 0.012, y0, H * 0.024, H * 0.08);
      const fy = y0 + H * 0.08; const fh = H * 0.42 * flick;
      const grd = g.createLinearGradient(0, fy, 0, fy + fh); grd.addColorStop(0, 'rgba(120,170,255,.9)'); grd.addColorStop(0.18, 'rgba(255,245,200,1)'); grd.addColorStop(0.7, 'rgba(255,170,60,.95)'); grd.addColorStop(1, 'rgba(255,120,30,0)');
      g.fillStyle = grd; g.beginPath(); g.moveTo(cx, fy + fh); g.quadraticCurveTo(cx + H * 0.13, fy + fh * 0.35, cx, fy); g.quadraticCurveTo(cx - H * 0.13, fy + fh * 0.35, cx, fy + fh); g.fill();
      g.restore();
      const a = clamp(1 - blurPx / 40, 0.15, 1); g.globalAlpha = 1;
      const lum = g.createRadialGradient(W / 2, W / 2, 0, W / 2, W / 2, W * 0.7); lum.addColorStop(0, `rgba(255,210,140,${0.18 * (1 - a) + 0.05})`); lum.addColorStop(1, 'rgba(255,210,140,0)');
      g.fillStyle = lum; g.fillRect(0, 0, W, W);
    }
    tex.needsUpdate = true;
  }
  function place() { candle.position.x = X(-st.u); screenU.position.x = X(st.s); }

  const SHOT = shot({ pos: [0.4, 3.0, 9.6], target: [0.4, 1.0, 0], fit: 12.5 });
  const SCREEN = () => shot({ pos: [X(st.s) - 2.6, 1.6, 0.9], target: [X(st.s), 1.35, 0], fov: 30, limits: { yaw: 0.5, pitch: 0.3, zMin: 0.6, zMax: 2.2 } });
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -(BY + 0.15)); const hit = new THREE.Vector3();
  const dragHandler = {
    down(p) {
      if (hits(ctx, screenU, p, 70, 1.0)) { this.d = 's'; return true; }
      if (hits(ctx, candle, p, 70, 1.0)) { this.d = 'u'; return true; }
      return false;
    },
    move() {
      if (!this.d || !ctx.input.ptr.ray.intersectPlane(plane, hit)) return;
      const cm = (hit.x - LENS_X) * 10;
      if (this.d === 's') st.s = clamp(Math.round(cm * 2) / 2, 5, 72); else st.u = clamp(Math.round(-cm * 2) / 2, 8, 70);
      place(); sfx.play('knob');
    },
    up() { this.d = null; },
  };

  function record() {
    const { v, blur } = image();
    if (!Number.isFinite(v) || v > 72) { ctx.say('No image on the screen: the candle is at or inside the focal point, or the image falls off the bench. Move the candle further away.', 'hint', 3600); return; }
    if (blur > 0.35) { ctx.mistake(`The image is still blurred. Slide the screen until the flame is sharpest (it is sharp ${v < st.s ? 'nearer the lens' : 'further away'}).`, 2); return; }
    if (st.readings.some((r) => Math.abs(r.u - st.u) < 4)) { ctx.say('Use a clearly different object distance for each reading.', 'hint', 2400); return; }
    st.readings.push({ u: st.u, v: st.s }); sfx.play('ok');
    ui.observe(`u = ${st.u.toFixed(1)} cm`, `v = ${st.s.toFixed(1)} cm · f = ${(st.u * st.s / (st.u + st.s)).toFixed(1)} cm`);
    hud.relabel('rec', `Record (${st.readings.length})`); hud.enable('done', st.readings.length >= 4);
  }
  const steps = [
    {
      title: 'Focus a distant view (rough f)', text: 'Point the lens at the window and catch the image on the screen: for a far object the image forms at the focal point. Slide the <b>screen</b> (drag it) until the window is sharp — the lens-to-screen distance is roughly f.', hideBelt: true, shot: SHOT,
      enter() { hud.actions([{ id: 'ok', label: 'About f', primary: true, onClick: () => { ui.observe('Rough f', `${f} cm (distant object)`); hud.actions([]); ctx.next(`Roughly ${f} cm. Now place the candle beyond 2f for a real image.`); } }]); },
      exit() { hud.actions([]); },
    },
    {
      title: 'Find sharp images', text: 'Drag the <b>candle</b> to set u (beyond f), then drag the <b>screen</b> until the inverted flame is <b>sharpest</b>, and record. Do at least <b>four</b> different u.', hint: 'Sweep the screen through the sharp point both ways and stop where the flame has crisp edges.', hideBelt: true, shot: SHOT,
      enter() { hud.actions([{ id: 'rec', label: 'Record (0)', primary: true, onClick: record }, { id: 'look', label: 'Look at the screen', onClick: () => ctx.rig.go(SCREEN(), 1.0) }, { id: 'done', label: 'Calculate', disabled: true, onClick: () => { hud.actions([]); ctx.next(); } }]); },
      exit() { hud.actions([]); },
      skip() { [24, 30, 40, 55].forEach((u) => { const v = u * f / (u - f); st.readings.push({ u, v }); }); },
      handler: dragHandler,
    },
    {
      title: 'f from the readings', text: 'f = uv/(u + v) for each pair; the 1/u–1/v graph is a straight line cutting both axes at 1/f.', hideBelt: true, shot: SHOT,
      enter() {
        const fs = st.readings.map((r) => r.u * r.v / (r.u + r.v)); const mean = fs.reduce((a, b) => a + b, 0) / fs.length; st.f = mean;
        const pts = st.readings.map((r) => [100 / r.u, 100 / r.v]); graph.draw(pts, fitLine(pts), { xMax: 100 / Math.min(...st.readings.map((r) => r.u)) * 1.15 + 1, yMax: 12 }); graph.show(true);
        const opts = [[mean, 'uv/(u + v)'], [st.readings.reduce((a, r) => a + (r.u + r.v) / 2, 0) / fs.length / 2, '(u + v)/4'], [st.readings.reduce((a, r) => a + r.u * r.v / Math.abs(r.u - r.v), 0) / fs.length, 'uv/(u − v)']].map(([v, w]) => ({ label: `${v.toFixed(1)} cm  (${w})`, value: v })).sort(() => Math.random() - 0.5);
        anim.wait(1.0, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Mean focal length from your pairs =', opts, (v) => {
          if (Math.abs(v - mean) > 1e-6) ctx.mistake('From 1/f = 1/u + 1/v (real-is-positive): f = uv/(u + v).', 3);
          ui.observe('f', `<b>${mean.toFixed(1)} cm</b>`); ctx.next(`f = ${mean.toFixed(1)} cm; power ${(100 / mean).toFixed(1)} D.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); graph.show(false); },
    },
  ];
  place();
  ctx.debug = { st, f, image };
  return {
    tools: [], steps,
    update(dt, t) { drawScreen(t); flame.material.uniforms.uTime.value = t; hud.update(); },
    result() {
      const err = ((st.f || 0) - f) / f * 100;
      return { title: 'Focal length of a convex lens', rows: st.readings.map((r) => [`u = ${r.u.toFixed(1)} cm`, `v = ${r.v.toFixed(1)} cm`]).concat([['Your f', `${(st.f || 0).toFixed(1)} cm`], ['Lens', `${f} cm`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]]),
        conclusion: 'A real, inverted image forms only beyond the focal point; the nearer the object comes to F, the further and larger the image. Every sharp pair obeys 1/u + 1/v = 1/f.' };
    },
    dispose() { hud.dispose(); graph.dispose(); tex.dispose(); },
  };
}
