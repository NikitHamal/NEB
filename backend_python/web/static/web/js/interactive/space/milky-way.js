import { THREE, createEngine, createOrbitControls, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { starfield } from '../core/space-kit.js';

const GALAXY_RADIUS = 50;
const SUN_RADIUS = 26;

function makeStarTexture() {
  const c = document.createElement('canvas');
  c.width = 64;
  c.height = 64;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(32, 32, 1, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.25, 'rgba(255,255,255,0.5)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

export default function init(stage) {
  const engine = createEngine(stage, { far: 2000 });
  if (!engine) return null;
  const { scene, camera, quality } = engine;

  camera.position.set(0, 52, 78);
  const controls = createOrbitControls(camera, engine.canvas, { minDistance: 10, maxDistance: 300, autoRotate: 0.02 });

  // A barred spiral, as the Milky Way is: an elongated central bar inside a bulge of old,
  // yellow stars; two major arms (Scutum-Centaurus, Perseus) and two minor ones of young blue
  // stars; pink star-forming nebulae strung along the arms; dark dust lanes on their inner
  // edges; and a soft diffuse glow of unresolved stars under it all.
  const count = quality.tier === 'low' ? 6000 : quality.tier === 'medium' ? 16000 : 30000;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const PITCH = 0.22; // spiral pitch, in the log-spiral's exponent
  const armAngle = (r, arm) => Math.log(Math.max(r, 6) / 6) / PITCH + arm * Math.PI / 2 + (arm % 2 ? 0 : 0);
  const old = new THREE.Color(0xffd9a0), mid = new THREE.Color(0xfff2dc), young = new THREE.Color(0xa8c4ff), hot = new THREE.Color(0xd2e0ff);
  const c = new THREE.Color();
  const gauss = () => (Math.random() + Math.random() + Math.random() - 1.5) / 1.5;
  for (let i = 0; i < count; i++) {
    let x; let y; let z; let col; let size;
    const kind = Math.random();
    if (kind < 0.18) {
      // bulge and bar: a triaxial cloud of old stars, the bar tilted 27 degrees
      const r = Math.pow(Math.random(), 1.6) * 11;
      const th = Math.random() * Math.PI * 2;
      x = Math.cos(th) * r * 1.9; z = Math.sin(th) * r * 0.7; y = gauss() * (3.2 - r * 0.18);
      const bx = x * Math.cos(0.47) - z * Math.sin(0.47); z = x * Math.sin(0.47) + z * Math.cos(0.47); x = bx;
      col = c.copy(old).lerp(mid, Math.random() * 0.4); size = 1.2 + Math.random() * 1.4;
    } else {
      const t = Math.pow(Math.random(), 0.7);
      const r = 7 + t * (GALAXY_RADIUS - 7);
      const arm = Math.floor(Math.random() * 4);
      const major = arm === 0 || arm === 2;
      const inArm = Math.random() < (major ? 0.82 : 0.6);
      const spread = inArm ? gauss() * (0.16 + r * 0.004) * (major ? 1 : 1.4) : (Math.random() - 0.5) * Math.PI * 2;
      const ang = armAngle(r, arm) + spread;
      x = Math.cos(ang) * r; z = Math.sin(ang) * r;
      y = gauss() * (1.1 - (r / GALAXY_RADIUS) * 0.6);
      const youth = inArm ? Math.max(0, 1 - Math.abs(spread) * 6) : 0;
      col = c.copy(mid).lerp(young, youth * 0.9 + (r / GALAXY_RADIUS) * 0.15);
      if (Math.random() < youth * 0.12) col.copy(hot);
      size = 0.8 + Math.random() * 1.0 + youth * 1.4;
    }
    positions[i * 3] = x; positions[i * 3 + 1] = y; positions[i * 3 + 2] = z;
    const b = 0.6 + Math.random() * 0.4;
    colors[i * 3] = col.r * b; colors[i * 3 + 1] = col.g * b; colors[i * 3 + 2] = col.b * b;
    sizes[i] = size;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { scale: { value: 1 } },
    vertexShader: 'attribute float size; varying vec3 vC; uniform float scale; void main(){ vC = color; vec4 mv = modelViewMatrix*vec4(position,1.0); gl_PointSize = size * scale * (300.0 / -mv.z); gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'varying vec3 vC; void main(){ vec2 d = gl_PointCoord-0.5; float r = length(d); float a = exp(-r*r*18.0); gl_FragColor = vec4(vC*1.25, a); }',
    vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  engine.onResize((w, h) => { mat.uniforms.scale.value = Math.max(0.6, h / 900) * Math.min(window.devicePixelRatio || 1, 2); });
  const galaxy = new THREE.Points(geo, mat);
  scene.add(galaxy);

  // the diffuse disc: unresolved starlight, painted once from the same arms
  const glowTex = (() => {
    const W = quality.tier === 'low' ? 512 : 1024;
    const cv = document.createElement('canvas'); cv.width = cv.height = W; const g = cv.getContext('2d');
    // a transparent canvas: black would still write alpha and darken the page behind the stage
    g.globalCompositeOperation = 'lighter';
    const k = W / (GALAXY_RADIUS * 2.3);
    const blob = (x, y, r, col, a) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(${col},${a})`); gr.addColorStop(1, `rgba(${col},0)`); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); };
    blob(W / 2, W / 2, W * 0.16, '255,214,150', 0.9);
    blob(W / 2, W / 2, W * 0.32, '255,226,180', 0.25);
    for (let arm = 0; arm < 4; arm++) for (let r = 7; r < GALAXY_RADIUS; r += 0.45) {
      const ang = armAngle(r, arm);
      const x = W / 2 + Math.cos(ang) * r * k, y = W / 2 + Math.sin(ang) * r * k;
      blob(x, y, (2.2 + r * 0.09) * k, arm % 2 ? '170,190,255' : '190,205,255', arm % 2 ? 0.05 : 0.08);
    }
    // dust lanes trail the arms on their inner edge
    for (let arm = 0; arm < 4; arm += 2) for (let r = 9; r < GALAXY_RADIUS * 0.85; r += 0.5) {
      const ang = armAngle(r, arm) - 0.12;
      const x = W / 2 + Math.cos(ang) * r * k, y = W / 2 + Math.sin(ang) * r * k;
      g.globalCompositeOperation = 'destination-out'; blob(x, y, (0.9 + r * 0.03) * k, '0,0,0', 0.35);
    }
    const t = new THREE.CanvasTexture(cv); if (t.colorSpace !== undefined) t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const disc = new THREE.Mesh(new THREE.PlaneGeometry(GALAXY_RADIUS * 2.3, GALAXY_RADIUS * 2.3), new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
  disc.rotation.x = -Math.PI / 2;
  galaxy.add(disc);
  // star-forming nebulae, pink with hydrogen, along the major arms
  if (quality.tier !== 'low') {
    const neb = new THREE.SpriteMaterial({ map: makeStarTexture(), color: 0xff7aa8, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false });
    for (let i = 0; i < 46; i++) {
      const arm = (i % 2) * 2; const r = 12 + Math.random() * 34;
      const ang = armAngle(r, arm) + (Math.random() - 0.5) * 0.08;
      const sp = new THREE.Sprite(neb); sp.position.set(Math.cos(ang) * r, 0.2, Math.sin(ang) * r); sp.scale.setScalar(1.2 + Math.random() * 1.8); galaxy.add(sp);
    }
  }
  const coreGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: makeStarTexture(), color: 0xffe0a8, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.9 }));
  coreGlow.scale.set(30, 16, 1);
  galaxy.add(coreGlow);

  scene.add(starfield(quality, 900));

  const sunMarker = new THREE.Group();
  // the Sun sits in the Orion Spur, between the Perseus and Sagittarius arms
  const sunAngle = Math.log(SUN_RADIUS / 6) / 0.22 + Math.PI / 2 + Math.PI / 4;
  sunMarker.position.set(Math.cos(sunAngle) * SUN_RADIUS, 0.6, Math.sin(sunAngle) * SUN_RADIUS);
  const sunDot = new THREE.Mesh(new THREE.SphereGeometry(0.55, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffd24d }));
  sunMarker.add(sunDot);
  const ringGeo = new THREE.RingGeometry(1.1, 1.35, 32);
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: 0xffd24d, side: THREE.DoubleSide, transparent: true, opacity: 0.85 }));
  ring.rotation.x = Math.PI / 2;
  sunMarker.add(ring);
  const hereLabel = makeLabelSprite('\u2605 You are here \u2014 the Sun', { scale: 5, fontSize: 42, color: '#ffe3a3' });
  hereLabel.position.y = 4.2;
  sunMarker.add(hereLabel);
  galaxy.add(sunMarker);

  const coreLabel = makeLabelSprite('Galactic core \u00b7 Sagittarius A*', { scale: 4.4, fontSize: 40 });
  coreLabel.position.set(0, 7.5, 0);
  galaxy.add(coreLabel);
  const distLabel = makeLabelSprite('26,000 light-years from the core', { scale: 3.6, fontSize: 36, bg: 'rgba(11,28,48,0.55)' });
  distLabel.position.set(Math.cos(sunAngle) * SUN_RADIUS * 0.55, 2.6, Math.sin(sunAngle) * SUN_RADIUS * 0.55);
  galaxy.add(distLabel);

  const hud = createHud(stage);
  hud.badge('The Milky Way \u2014 100,000 light-years across', '#c4b5fd');
  hud.badge(`${count.toLocaleString()} of ~200,000,000,000 stars shown`, '#9ec1ff');

  let rotSpeed = 0.02;
  const panel = createPanel(stage, { title: 'Galaxy Controls' });
  panel.slider({
    label: 'Rotation speed',
    min: 0, max: 100, step: 5, value: 20,
    format: (v) => (v === 0 ? 'Paused' : `${v}%`),
    onChange: (v) => { rotSpeed = v / 1000; },
  });
  panel.toggle({
    label: 'Show labels',
    value: true,
    onChange: (v) => { hereLabel.visible = v; coreLabel.visible = v; distLabel.visible = v; },
  });
  panel.info('Each dot here stands in for millions of real stars \u2014 the actual galaxy holds about 200 billion. Our whole night sky \u2014 every star you have ever seen \u2014 sits inside a tiny bubble around the yellow marker.');

  let pulse = 0;
  engine.setUpdate((dt) => {
    galaxy.rotation.y += rotSpeed * dt * 10;
    pulse += dt * 2.4;
    const s = 1 + Math.sin(pulse) * 0.18;
    ring.scale.set(s, s, 1);
    controls.update(dt);
  });

  engine.start();

  return {
    dispose() {
      controls.dispose();
      panel.dispose();
      hud.dispose();
      engine.dispose();
    },
  };
}
