import { THREE, createEngine } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createUniverse } from './cosmos/universe.js';
import { createRig, MIN_LOG, MAX_LOG } from './cosmos/view.js';
import { createLabels, hudElement } from './cosmos/labels.js';
import { AU, LY } from './cosmos/astro.js';

const BANDS = [
  [-9, 1.0, 'You', 'A person is about 1.7 m tall: 10⁰ metres. Light crosses you in about 6 billionths of a second.'],
  [1.0, 2.6, 'The summit of Everest', 'You are standing 8 849 m above sea level, on real elevation data. Up here the air holds only a third of the oxygen it has at sea level.'],
  [2.6, 4.1, 'Mount Everest (Sagarmatha)', 'The highest point on Earth, with Lhotse and Nuptse beside it. Its summit rock was once the floor of an ancient sea: it holds marine fossils.'],
  [4.1, 5.4, 'The Himalaya', 'India is still pushing into Asia at about 5 cm a year, and the Himalaya are rising by a few millimetres every year.'],
  [5.4, 6.6, 'Nepal and Tibet', 'The whole of Nepal fits in a strip about 885 km long. Notice how thin the snowy mountains look from here.'],
  [6.6, 7.9, 'Planet Earth', '12 742 km across. All the air you breathe is a layer thinner, compared to Earth, than the skin on an apple.'],
  [7.9, 9.4, 'Earth and the Moon', 'The Moon is 384 400 km away. You could fit every other planet in the Solar System into that gap.'],
  [9.4, 10.6, 'Earth’s neighbourhood', 'Sunlight takes 8 minutes and 20 seconds to reach Earth. Everything here is drawn at its true size and true position for today.'],
  [10.6, 12.6, 'The inner Solar System', 'Mercury, Venus, Earth and Mars, in the places they really are today. One astronomical unit (AU) is the Earth–Sun distance, 150 million km.'],
  [12.6, 14.2, 'The Solar System', 'Neptune orbits 30 AU from the Sun. Planets are dots even at this scale; the Solar System is almost entirely empty space.'],
  [14.2, 15.6, 'The heliosphere', 'The solar wind blows a bubble about 120 AU across. Voyager 1, launched in 1977, has crossed it and is now in interstellar space.'],
  [15.6, 16.8, 'The Oort cloud', 'A shell of perhaps a trillion icy comets reaching out more than a light-year. A light-year is 9.46 trillion km.'],
  [16.8, 18.2, 'The nearest stars', 'Proxima Centauri is 4.24 light-years away, about 270 000 AU. At the speed of the fastest spacecraft the trip would take thousands of years.'],
  [18.2, 19.6, 'Our stellar neighbourhood', 'Bright stars like Betelgeuse, Rigel and Deneb are hundreds to thousands of light-years away; you see them as they were when their light left.'],
  [19.6, 21.4, 'The Orion Spur', 'The Sun sits in a small arm between the Sagittarius and Perseus arms, 26 700 light-years from the galaxy’s centre.'],
  [21.4, 22.7, 'The Milky Way', 'A barred spiral of 100–400 billion stars, about 100 000 light-years across. The Sun takes 230 million years to go round once.'],
  [22.7, 23.8, 'The Local Group', 'About 80 galaxies. Andromeda, 2.5 million light-years away, is heading towards us and will merge with the Milky Way in about 4.5 billion years.'],
  [23.8, 24.8, 'The Virgo Supercluster', 'Groups and clusters of galaxies, with the huge Virgo Cluster of over 1 000 galaxies at its heart.'],
  [24.8, 25.8, 'Laniakea Supercluster', '“Immeasurable heaven” in Hawaiian: 100 000 galaxies whose motions flow towards the Great Attractor. The glowing streams show that flow.'],
  [25.8, 26.6, 'The cosmic web', 'Galaxies gather along filaments around enormous empty voids, like foam. It is the largest pattern in the universe.'],
  [26.6, 99, 'The observable universe', '93 billion light-years across, holding about 2 trillion galaxies. Its edge is the cosmic microwave background, the oldest light there is.'],
];

const JUMPS = [
  { id: 'you', label: 'You', log: 0.6 },
  { id: 'everest', label: 'Everest', log: 3.95 },
  { id: 'himalaya', label: 'Himalaya', log: 5.25 },
  { id: 'earth', label: 'Earth', log: 7.35 },
  { id: 'moon', label: 'Moon', log: 6.9, focus: 'moon', name: 'The Moon', text: 'The Moon is 3 474 km across, a quarter the width of Earth. Its craters are records of impacts over 4 billion years; there is no weather to erase them.' },
  { id: 'earthmoon', label: 'Earth & Moon', log: 9.05 },
  { id: 'sun', label: 'The Sun', log: 9.65, focus: 'sun', name: 'The Sun', text: 'The Sun is 1.39 million km across: 109 Earths would fit across its face. Its boiling granules are each about the size of Nepal, and dark sunspots are cooler, magnetic regions.' },
  { id: 'jupiter', label: 'Jupiter', log: 8.4, focus: 'jupiter', name: 'Jupiter', text: 'The biggest planet, 143 000 km across, made mostly of hydrogen and helium. The Great Red Spot is a storm wider than Earth that has raged for centuries.' },
  { id: 'saturn', label: 'Saturn', log: 8.75, focus: 'saturn', name: 'Saturn', text: 'Saturn’s rings are 280 000 km wide but mostly only about 10 metres thick: billions of pieces of ice, from dust grains to house-sized blocks.' },
  { id: 'inner', label: 'Inner planets', log: 11.7 },
  { id: 'solar', label: 'Solar System', log: 13.25 },
  { id: 'oort', label: 'Oort cloud', log: 16.3 },
  { id: 'stars', label: 'Nearest stars', log: 17.35 },
  { id: 'milkyway', label: 'Milky Way', log: 21.1 },
  { id: 'andromeda', label: 'Andromeda', log: 21.55, focus: 'm31', name: 'Andromeda Galaxy', text: 'Our nearest big neighbour: a spiral of about a trillion stars, 2.5 million light-years away. On a dark night in Nepal you can see it with your naked eye as a faint smudge.' },
  { id: 'local', label: 'Local Group', log: 22.85 },
  { id: 'laniakea', label: 'Laniakea', log: 25.15 },
  { id: 'universe', label: 'Observable universe', log: 26.98 },
];

const TOUR = ['you', 'everest', 'himalaya', 'earth', 'earthmoon', 'inner', 'solar', 'oort', 'stars', 'milkyway', 'local', 'laniakea', 'universe'];

function fmtNum(x, d = 0) { return x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: 0 }).replace(/,/g, ' '); }

function human(m) {
  if (m < 1) return `${fmtNum(m * 100, 0)} cm`;
  if (m < 1e3) return `${fmtNum(m, m < 10 ? 1 : 0)} m`;
  if (m < 1e9) return `${fmtNum(m / 1e3, m < 1e4 ? 1 : 0)} km`;
  if (m < 0.05 * LY) return `${fmtNum(m / AU, m < 10 * AU ? 2 : 0)} AU`;
  const ly = m / LY;
  if (ly < 1e3) return `${fmtNum(ly, ly < 10 ? 2 : 0)} light-years`;
  if (ly < 1e6) return `${fmtNum(ly / 1e3, 0)} thousand light-years`;
  if (ly < 1e9) return `${fmtNum(ly / 1e6, 0)} million light-years`;
  return `${fmtNum(ly / 1e9, 1)} billion light-years`;
}

function lightTime(m) {
  const s = m / 2.998e8;
  if (s < 1e-6) return `${fmtNum(s * 1e9, 1)} ns`;
  if (s < 1e-3) return `${fmtNum(s * 1e6, 1)} µs`;
  if (s < 1) return `${fmtNum(s * 1e3, 1)} ms`;
  if (s < 120) return `${fmtNum(s, 1)} s`;
  if (s < 7200) return `${fmtNum(s / 60, 1)} min`;
  if (s < 86400 * 3) return `${fmtNum(s / 3600, 1)} hours`;
  if (s < 86400 * 365.25 * 2) return `${fmtNum(s / 86400, 0)} days`;
  const y = s / (86400 * 365.25);
  if (y < 1e6) return `${fmtNum(y, 0)} years`;
  if (y < 1e9) return `${fmtNum(y / 1e6, 0)} million years`;
  return `${fmtNum(y / 1e9, 1)} billion years`;
}

const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
const pow10 = (n) => `10${String(n).split('').map((c) => SUP[c]).join('')}`;

export default function init(stage) {
  stage.classList.add('ix-cosmos-stage');
  const engine = createEngine(stage, { logDepth: true, alpha: false, environment: false, fov: 45, near: 1e-3, far: 1e9, exposure: 1.0 });
  if (!engine) return null;
  const { scene, camera, renderer } = engine;
  scene.background = new THREE.Color(0x000000);
  renderer.setClearColor(0x000000, 1);

  const labels = createLabels(stage);
  const powEl = hudElement(stage, 'cz-hud-pow', '<b></b><small></small>');
  const barEl = hudElement(stage, 'cz-scalebar', '<span></span><em></em>');
  const capEl = hudElement(stage, 'cz-caption');
  const loadEl = hudElement(stage, 'cz-loading', 'Building Everest from real elevation data…');
  const hud = createHud(stage);
  const badge = hud.badge('You', '#60a5fa');

  const rig = createRig(engine.canvas, { start: 0.6, autoYaw: 0 });
  const added = new Set();
  const universe = createUniverse(engine, {
    onProgress: () => {
      universe.labelDefs.forEach((d) => {
        if (added.has(d.def)) return;
        added.add(d.def);
        labels.add(d.layer, d.def);
      });
    },
  });
  universe.ready().then(() => { loadEl.style.opacity = '0'; setTimeout(() => loadEl.remove(), 500); });

  let touring = false;
  let tourIdx = 0;
  let hold = 0;
  let captionUntil = 0;
  let lastBand = '';

  const panel = createPanel(stage, { title: 'Scale of the Universe' });
  panel.info('One continuous zoom through 27 powers of ten. Scroll, pinch or use the slider to zoom; drag to look around. Everything is at its true size and true position.');
  const zoom = panel.slider({
    label: 'View width', min: MIN_LOG, max: MAX_LOG, step: 0.01, value: 0.6,
    format: (v) => `${pow10(Math.round(v))} m`,
    onChange: (v) => { stopTour(); rig.jump(v); },
  });
  panel.chips({
    label: 'Fly to', options: JUMPS.map((j) => ({ value: j.id, label: j.label })), value: '',
    onChange: (id) => { stopTour(); flyTo(id); },
  });
  const [tourBtn] = panel.buttonRow([{ label: 'Take the tour', icon: 'rocket_launch', onClick: () => (touring ? stopTour() : startTour()) }]);
  panel.toggle({ label: 'Labels', value: true, onChange: (v) => { labels.enabled = v; } });
  const stats = panel.stats([
    { key: 'w', label: 'View width' }, { key: 'p', label: 'Power of ten' },
    { key: 'obj', label: 'In view' }, { key: 'light', label: 'Light takes' },
  ]);
  const about = panel.info(BANDS[0][3]);

  let activeJump = null;
  let pending = null;
  function apply(j) {
    activeJump = j;
    universe.setOverride(j.focus ? { log: j.log, get: (v) => v.copy(universe.targets[j.focus]()) } : null);
    rig.jump(j.log);
    rig.resetOrbit();
  }
  function flyTo(id) {
    const j = JUMPS.find((x) => x.id === id);
    if (!j) return;
    const to = j.focus ? universe.targets[j.focus]() : universe.pathFocus(j.log, new THREE.Vector3());
    const d = universe.focusNow().distanceTo(to);
    const peak = Math.log10(Math.max(1, d) * 2.2);
    if (peak > Math.max(rig.logW, j.log) + 0.4) {
      pending = { j, peak };
      rig.jump(peak);
    } else {
      pending = null;
      apply(j);
    }
  }
  function startTour() {
    touring = true; tourIdx = 0; hold = 0;
    tourBtn.setLabel && tourBtn.setLabel('Stop the tour');
    universe.setOverride(null);
    rig.resetOrbit();
    rig.jump(JUMPS.find((x) => x.id === TOUR[0]).log);
  }
  function stopTour() {
    if (!touring) return;
    touring = false;
    tourBtn.setLabel && tourBtn.setLabel('Take the tour');
  }
  rig.onInteract((kind) => { if (kind === 'zoom') stopTour(); });

  const BAR_STEPS = [1, 2, 5];
  let elapsed = 0;
  engine.setUpdate((dt, t) => {
    elapsed = t;
    if (touring) {
      const goal = JUMPS.find((x) => x.id === TOUR[tourIdx]).log;
      if (Math.abs(rig.logW - goal) < 0.04) {
        hold += dt;
        if (hold > 5.5) {
          hold = 0;
          tourIdx += 1;
          if (tourIdx >= TOUR.length) stopTour();
          else rig.jump(JUMPS.find((x) => x.id === TOUR[tourIdx]).log);
        }
      }
    }
    if (pending && Math.abs(rig.logW - pending.peak) < 0.2) { const j = pending.j; pending = null; apply(j); }
    const lw = rig.update(dt);
    const w = stage.clientWidth || 1; const h = stage.clientHeight || 1;
    const aspect = w / h;
    const vf = camera.fov * Math.PI / 180;
    const hf = 2 * Math.atan(Math.tan(vf / 2) * aspect);
    const D = 5 / Math.tan(Math.min(vf, hf) / 2);
    camera.near = D * 1e-4; camera.far = D * 1e7; camera.updateProjectionMatrix();
    const { W } = universe.frame(lw, t, dt, rig.orbit(), D);
    labels.update(camera, lw, w, h);

    const p = Math.round(lw);
    powEl.firstChild.textContent = `${pow10(p)} m`;
    powEl.lastChild.textContent = human(W);
    const pxPerM = Math.min(w, h) / W;
    const target = Math.min(w, h) * 0.22 / pxPerM;
    const e = Math.floor(Math.log10(target));
    let len = Math.pow(10, e);
    for (const s of BAR_STEPS) if (s * Math.pow(10, e) <= target) len = s * Math.pow(10, e);
    barEl.firstChild.style.width = `${(len * pxPerM).toFixed(1)}px`;
    barEl.lastChild.textContent = human(len);
    let band = BANDS.find((b) => lw >= b[0] && lw < b[1]) || BANDS[BANDS.length - 1];
    if (activeJump && activeJump.focus && Math.abs(lw - activeJump.log) < 0.8) band = [0, 0, activeJump.name, activeJump.text];
    if (band[2] !== lastBand) {
      lastBand = band[2];
      badge.set(band[2]);
      about.set(band[3]);
      if (touring) { capEl.textContent = band[3]; captionUntil = t + 7; }
    }
    capEl.classList.toggle('on', touring && t < captionUntil);
    if (Math.abs(zoom.input ? +zoom.input.value - lw : 1) > 0.02 && zoom.set) zoom.set(+lw.toFixed(2));
    stats.w.set(human(W));
    stats.p.set(`${pow10(p)} m`);
    stats.obj.set(band[2]);
    stats.light.set(lightTime(W));
  });
  engine.start();

  stage.__cosmos = { rig, universe, flyTo, apply: (id) => apply(JUMPS.find((x) => x.id === id)), get t() { return elapsed; } };
  return {
    dispose() {
      rig.dispose(); labels.dispose(); panel.dispose(); hud.dispose();
      universe.dispose(); engine.dispose();
      [powEl, barEl, capEl, loadEl].forEach((el) => el.remove());
    },
  };
}
