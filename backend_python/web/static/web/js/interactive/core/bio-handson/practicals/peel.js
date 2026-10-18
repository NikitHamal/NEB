// Epidermal peel practicals. Plasmolysis: peel the purple lower epidermis of a Rhoeo leaf, mount
// it in water (turgid cells), draw 5% salt solution under the coverslip with blotting paper and
// watch the protoplasts shrink from the walls, then restore them with water (deplasmolysis).
// Stomata: peel the lower and the upper epidermis of a dicot leaf, mount both, count stomata in
// a high-power field of each and work out the stomatal frequency per mm².
import { THREE } from '../../engine.js';
import { watchGlass, reagentBottle } from '../props.js';
import { buildStation, stepDrop, stepCoverslip, stepToStage, createScopeView } from '../slideprep.js';
import { createEpidermisField } from '../fields/epidermis.js';
import { canvasTexture, ease, clamp, rng } from '../kit.js';

function leafTexture(purple) {
  return canvasTexture(`leaf:${purple}`, 512, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    if (purple) { gr.addColorStop(0, '#5b2a6e'); gr.addColorStop(0.5, '#7b3a8e'); gr.addColorStop(1, '#5b2a6e'); }
    else { gr.addColorStop(0, '#5e8f3e'); gr.addColorStop(0.5, '#79a957'); gr.addColorStop(1, '#5e8f3e'); }
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.strokeStyle = purple ? 'rgba(220,180,230,0.25)' : 'rgba(230,245,210,0.35)'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();
    g.lineWidth = 1;
    if (purple) { for (let y = 12; y < h; y += 14) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y + 2); g.stroke(); } }
    else { for (let x = 20; x < w; x += 34) { g.beginPath(); g.moveTo(x, h / 2); g.quadraticCurveTo(x + 30, h * 0.25, x + 60, 4); g.moveTo(x, h / 2); g.quadraticCurveTo(x + 30, h * 0.75, x + 60, h - 4); g.stroke(); } }
    const R = rng(4); g.fillStyle = 'rgba(255,255,255,0.05)'; for (let i = 0; i < 400; i++) g.fillRect(R() * w, R() * h, 2, 2);
  });
}
function leafMesh(purple, len = 1.5, wid = 0.45) {
  const s = new THREE.Shape();
  s.moveTo(-len / 2, 0); s.quadraticCurveTo(-len * 0.2, wid * 0.62, len * 0.1, wid / 2); s.quadraticCurveTo(len * 0.38, wid * 0.4, len / 2, 0);
  s.quadraticCurveTo(len * 0.38, -wid * 0.4, len * 0.1, -wid / 2); s.quadraticCurveTo(-len * 0.2, -wid * 0.62, -len / 2, 0);
  const geo = new THREE.ShapeGeometry(s, 24); geo.rotateX(-Math.PI / 2);
  const uv = geo.attributes.uv; const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) uv.setXY(i, (p.getX(i) + len / 2) / len, (p.getZ(i) + wid / 2) / wid);
  const m = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ map: leafTexture(purple), roughness: 0.45, clearcoat: 0.5, clearcoatRoughness: 0.3, side: THREE.DoubleSide }));
  m.receiveShadow = true; m.castShadow = true;
  return m;
}

export function create(ctx) {
  const plasmo = ctx.config.slug.startsWith('plasmolysis');
  const { world, input, tools, fx, anim, sfx, ui } = ctx;
  const st = buildStation(ctx, { tileX: 0.1, tileZ: 0.35, slideDX: 0.42 });
  const leaves = []; const peels = [];
  const surfaces = plasmo ? [{ key: 'lower', label: 'lower epidermis', purple: true }] : [{ key: 'lower', label: 'lower epidermis', purple: false }, { key: 'upper', label: 'upper epidermis', purple: false }];
  surfaces.forEach((sf, i) => {
    const leaf = leafMesh(sf.purple); leaf.position.set(-0.32, 0.036 + i * 0.004, 0.28 + (surfaces.length > 1 ? (i - 0.5) * 0.48 : 0)); world.add(leaf);
    if (!plasmo) leaf.material.color.setHex(sf.key === 'lower' ? 0xc8dcb0 : 0xffffff);
    leaves.push(leaf);
  });
  const wg = watchGlass(0xcfe8f5, 0.55); wg.scale.setScalar(0.7); wg.position.set(0.55, 0.03, -0.12); world.add(wg);
  if (plasmo) { const b = reagentBottle('5% NaCl', 0xe0f2fe, 'salt solution'); b.position.set(0.95, 0, -0.55); world.add(b); }
  ctx.surfaces.push(st.tile, ...leaves);
  const tmp = new THREE.Vector3(); const tmp2 = new THREE.Vector3();
  const projectFn = (v, out) => input.project(v, out, ctx.stage.clientWidth, ctx.stage.clientHeight);
  let field = null; let view = null; const counts = {};
  const SHOT_LEAF = { pos: [-0.25, 1.75, 1.25], target: [-0.28, 0.84, 0.3], fit: 1.6 };
  const SHOT_SLIDE = { pos: [0.52, 1.32, 1.02], target: [0.52, 0.84, 0.52], fit: 0.55 };

  // ---- peeling --------------------------------------------------------------------------------
  function peelStep(i) {
    const sf = surfaces[i]; const leaf = leaves[i];
    let mark = null; let pulling = null; let strip = null;
    const s = {
      title: plasmo ? 'Peel the lower epidermis' : `Peel the ${sf.label}`,
      text: plasmo ? 'Tear the leaf obliquely, then with <b>forceps</b> catch the thin purple skin at the torn edge and pull it back slowly along the leaf.' : `Fold and tear the leaf, then catch the thin, colourless ${sf.label} at the torn edge with <b>forceps</b> and pull it off slowly.`,
      hint: 'Press on the glowing ring and drag slowly along the leaf. Pull too fast and green mesophyll comes away with it.',
      tool: 'forceps', shot: SHOT_LEAF,
      enter() { tmp.set(leaf.position.x + 0.42, leaf.position.y, leaf.position.z); world.localToWorld(tmp); mark = fx.mark(tmp, 0.04, 0xfacc15); },
      exit() { if (mark) fx.unmark(mark); mark = null; },
      skip() { makeStrip(0.3); finish(true); },
      handler: {
        down(p) {
          projectFn(mark.position, tmp2); if (Math.hypot(tmp2.x - p.x, tmp2.y - p.y) > 44) return false;
          if (!ctx.requireTool('forceps')) return true;
          pulling = { x: p.x, y: p.y, t: performance.now(), len: 0, fast: 0 }; tools.press(1); tools.action(1); sfx.play('pick');
          makeStrip(0.001); return true;
        },
        move(p) {
          if (!pulling) return;
          const now = performance.now(); const d = Math.hypot(p.x - pulling.x, p.y - pulling.y);
          const speed = (d - pulling.len * 600) / Math.max(1, now - pulling.t);
          pulling.t = now;
          const len = clamp(d / 600, 0, 0.32);
          if (speed > 1.6 && len > 0.05) pulling.fast += 1;
          pulling.len = len; makeStrip(len);
          ctx.progress(len / 0.3);
          if (len >= 0.3) { tools.press(0); tools.action(0); const bad = pulling.fast > 2; pulling = null; if (bad) tornThick(); else finish(false); }
        },
        up() { if (!pulling) return; pulling = null; tools.press(0); tools.action(0); if (strip) { leaf.parent.remove(strip); strip = null; } ctx.say('The peel snapped back. Pull it the whole way, slowly.', 'hint', 2400); },
      },
    };
    function makeStrip(len) {
      if (!strip) {
        strip = new THREE.Mesh(new THREE.PlaneGeometry(1, 0.09, 12, 1), new THREE.MeshPhysicalMaterial({ color: sf.purple ? 0x9a4fb0 : 0xe8f2dc, roughness: 0.3, transparent: true, opacity: 0.8, side: THREE.DoubleSide, clearcoat: 1 }));
        strip.geometry.translate(0.5, 0, 0); strip.geometry.rotateX(-Math.PI / 2); world.add(strip);
      }
      strip.position.set(leaf.position.x + 0.42 - len, leaf.position.y + 0.004 + len * 0.25, leaf.position.z);
      strip.scale.set(Math.max(0.001, len), 1, 1); strip.rotation.z = -len * 1.2;
    }
    function tornThick() {
      ctx.mistake('Too fast — the peel tore thick and green: mesophyll cells came with it, so it will not be one cell thick. Try again, slowly.', 3);
      strip.material.color.setHex(0x5f8f3e); const sm = strip; strip = null;
      anim.add(0.5, (k) => { sm.material.opacity = 0.8 * (1 - k); }, { done: () => { world.remove(sm); sm.geometry.dispose(); sm.material.dispose(); } });
    }
    function finish(instant) {
      sfx.play('tear'); const sm = strip; strip = null; peels.push(sm);
      const from = sm.position.clone(); const to = new THREE.Vector3(wg.position.x - 0.08 + i * 0.1, 0.075, wg.position.z);
      if (instant) { sm.position.copy(to); sm.rotation.z = 0; sm.scale.x = 0.2; return; }
      anim.add(0.8, (k) => { sm.position.lerpVectors(from, to, k); sm.position.y += Math.sin(Math.PI * k) * 0.25; sm.rotation.z = (1 - k) * -0.4; sm.scale.x = 0.3 - k * 0.1; }, { ease: ease.inOut, done: () => { sfx.play('drop'); ctx.next(sf.purple ? 'A thin, transparent purple peel — one cell thick. It floats in water so it does not dry.' : 'A thin colourless peel, one cell thick, now in water.'); } });
    }
    return s;
  }

  const stepWater = stepDrop(ctx, st, { title: 'A drop of water on the slide', text: 'With the <b>dropper</b>, put one drop of water in the middle of a clean slide.', color: 0xcfe8f5, shot: SHOT_SLIDE });
  const stepTransfer = {
    title: plasmo ? 'Mount the peel' : 'Mount both peels',
    text: plasmo ? 'With the <b>forceps</b>, lift the peel from the watch glass and spread it flat in the drop.' : 'Lift each peel with the <b>forceps</b> and lay them side by side in the drop: lower epidermis on the left, upper on the right.',
    hint: 'Tap a peel in the watch glass.', tool: 'forceps', shot: { pos: [0.42, 1.6, 1.15], target: [0.5, 0.86, 0.25], fit: 0.95 },
    skip() { peels.forEach((p, i) => place(p, i, true)); },
    handler: {
      down() {
        let best = null; let bd = 50; let bi = -1;
        peels.forEach((p, i) => { if (p.userData.mounted) return; p.getWorldPosition(tmp); projectFn(tmp, tmp2); const d = Math.hypot(tmp2.x - input.ptr.x, tmp2.y - input.ptr.y); if (d < bd) { bd = d; best = p; bi = i; } });
        if (!best) return false;
        if (!ctx.requireTool('forceps')) return true;
        sfx.play('pick'); place(best, bi, false); return true;
      },
    },
  };
  function place(p, i, instant) {
    p.userData.mounted = true;
    const to = new THREE.Vector3(st.slide.position.x + (peels.length > 1 ? (i - 0.5) * 0.11 : 0) - 0.045, st.slideTopY + 0.002, st.slide.position.z);
    const from = p.position.clone();
    if (!st.specimen) st.specimen = p; else st.specimen2 = p;
    if (instant) { p.position.copy(to); p.scale.x = 0.09; return; }
    anim.add(0.7, (k) => { p.position.lerpVectors(from, to, k); p.position.y += Math.sin(Math.PI * k) * 0.15; p.scale.x = 0.2 - 0.11 * k; }, { ease: ease.inOut, done: () => { sfx.play('place'); if (peels.every((q) => q.userData.mounted)) ctx.next(); } });
  }
  const stepCover = stepCoverslip(ctx, st, { shot: SHOT_SLIDE });
  const stepStage = stepToStage(ctx, st, { shotStart: SHOT_SLIDE });
  // the second peel rides with the slide too
  const origStageSkip = stepStage.skip;
  stepStage.skip = () => { if (st.specimen2 && st.slideParts) st.slideParts.push({ m: st.specimen2, off: st.specimen2.position.clone().sub(st.slide.position), q: st.specimen2.quaternion.clone() }); origStageSkip(); };
  const origStageDown = stepStage.handler.down;
  stepStage.handler.down = (p) => { if (st.specimen2 && !st.slideParts) { st.slideParts = [st.coverslip, st.drop, st.specimen, st.specimen2].filter(Boolean).map((m) => ({ m, off: m.position.clone().sub(st.slide.position), q: m.quaternion.clone() })); } return origStageDown(p); };

  function makeView() {
    if (view) return view;
    field = plasmo ? createEpidermisField({ bubbles: st.bubbles }) : createDual(st.bubbles);
    view = createScopeView(ctx, st, field, { objective: 10, focus: -650, onTap: (c, e) => { if (ctx.step && ctx.step.onCell) ctx.step.onCell(c, e); } });
    ctx.debug = { field, view };
    return view;
  }
  const eyeHandler = { down() { const h = input.pick(st.scope.pickables); if (h) { makeView().open(); return true; } return false; } };
  let sharpT = 0;
  const stepFocus = {
    title: 'Focus the peel',
    text: 'Look into the eyepiece and focus with the <b>coarse</b>, then the <b>fine</b> knob.',
    hint: 'Drag the coarse knob up slowly until cells appear, then sharpen with fine.',
    tool: null, hideBelt: true, handler: eyeHandler,
    enter() { makeView().open(); sharpT = 0; },
    skip() { makeView(); },
    update(dt) {
      const e = view && view.eye; if (!e) return;
      const s = e.state; ctx.progress(clamp(1 - s.blur / 12));
      if (s.sharp) { sharpT += dt; if (sharpT > 0.6 && !this.done) { this.done = true; ctx.next(plasmo ? 'Rows of long epidermal cells, most filled with purple sap, and stomata with green guard cells.' : 'Epidermal cells and stomata, each a pair of bean-shaped guard cells round a pore.'); } } else sharpT = 0;
    },
  };
  function ask(title, opts, right, okMsg, badMsg, after) {
    const go = () => ui.choose(ctx.stage.clientWidth / 2, 70, title, opts.map((o) => ({ label: o[1], value: o[0] })), (v) => {
      if (v === right) { sfx.play('ok'); after ? after() : ctx.next(okMsg); if (after) ctx.say(okMsg, 'good', 5000); }
      else { ctx.mistake(badMsg, 3); anim.wait(0.4, go); }
    });
    anim.wait(0.7, go);
  }

  // ---- plasmolysis -------------------------------------------------------------------------------
  const stepTurgid = {
    title: 'Cells in water', text: 'The peel is mounted in water. Look at a purple cell: where is its coloured protoplast?', tool: null, hideBelt: true, handler: eyeHandler,
    enter() { if (!view || !view.eye) makeView().open(); ask('These cells are…', [['turgid', 'Turgid — protoplast pressed against the wall'], ['plas', 'Plasmolysed'], ['flaccid', 'Dead']], 'turgid', 'Turgid: water entered by osmosis until the wall pushed back; the purple vacuole fills the cell.', 'Look again: the purple fills each cell right up to the wall.'); },
    exit() { ui.clearChooser(); },
  };
  function irrigateStep(kind) {
    const salt = kind === 'salt';
    let dropped = false; let blotted = false;
    const s = {
      title: salt ? 'Draw salt solution under the coverslip' : 'Bring back water',
      text: salt ? 'Without moving the slide, add a drop of <b>5% NaCl</b> at one edge of the coverslip, then touch <b>blotting paper</b> to the opposite edge to draw it through. Watch the cells.' : 'Now irrigate with <b>water</b> the same way: a drop at one edge, blotting paper at the other.',
      hint: 'Use the two buttons beside the eyepiece view: first the dropper, then the blotting paper.',
      tool: null, hideBelt: true, handler: eyeHandler,
      enter() {
        if (!view || !view.eye) makeView().open();
        const e = view.eye; e.clearActions();
        const bDrop = e.action(salt ? 'Drop of 5% NaCl' : 'Drop of water', () => { dropped = true; bDrop.disabled = true; bBlot.classList.add('glow'); sfx.play('drop'); ctx.say('The drop sits at the coverslip edge. Now draw it through with blotting paper.', 'info', 2600); }, 'glow');
        const bBlot = e.action('Blotting paper', () => {
          if (!dropped) { ctx.mistake('Add the drop first — the paper only draws liquid that is already at the far edge.', 2); return; }
          if (blotted) return; blotted = true; bBlot.disabled = true; bBlot.classList.remove('glow'); sfx.play('squish');
          field.state.target = salt ? 1 : 0; field.state.speed = salt ? 0.09 : 0.11;
        });
      },
      skip() { field.state.target = salt ? 1 : 0; field.state.p = field.state.target; },
      update(dt) {
        if (!field) return;
        if (field.step(dt)) { view.eye.redraw(); ctx.progress(salt ? field.state.p : 1 - field.state.p); }
        if (blotted && field.state.p === field.state.target && !this.asked) {
          this.asked = true; view.eye.clearActions();
          if (salt) ask('What happened?', [['plas', 'The protoplasts shrank away from the walls'], ['burst', 'The cells burst'], ['grow', 'The cells swelled']], 'plas', 'Plasmolysis: the salt solution is hypertonic, so water left the vacuoles by exosmosis; the protoplasts shrank from the walls — first at the corners (incipient), then into rounded masses. The purple deepened as the sap concentrated.', 'Look closely: the walls stay put; the purple contents have pulled away from them.', () => ask('What fills the space between wall and protoplast?', [['salt', 'The salt solution'], ['air', 'Air'], ['nothing', 'A vacuum']], 'salt', 'The cell wall is freely permeable, so the outside salt solution fills the space; the cell membrane is selectively permeable.', 'The cell wall lets the solution straight through — what was the cell bathed in?'));
          else ask('And now?', [['deplas', 'The protoplasts swelled back to the walls'], ['same', 'No change'], ['burst', 'The cells burst']], 'deplas', 'Deplasmolysis: in water (hypotonic) the vacuoles took up water by endosmosis and the protoplasts pressed against the walls again. The cells were alive; the wall stopped them bursting.', 'Look again at the purple contents and the walls.');
        }
      },
      exit() { ui.clearChooser(); if (view && view.eye) view.eye.clearActions(); },
    };
    return s;
  }

  // ---- stomata --------------------------------------------------------------------------------------
  function createDual(bubbles) {
    const lower = createEpidermisField({ seed: 31, purple: 0, stomaRate: 0.12, cellLen: 46, rowH: 28, bubbles });
    const upper = createEpidermisField({ seed: 57, purple: 0, stomaRate: 0.028, cellLen: 46, rowH: 28 });
    const gap = 300;
    lower.cells.forEach((c) => { c.side = 'lower'; c.ox = 0; });
    upper.cells.forEach((c) => { c.side = 'upper'; c.ox = lower.width + gap; });
    return {
      width: lower.width * 2 + gap, height: lower.height, start: { x: lower.width * 0.5, y: lower.height / 2 }, background: '#eef0e6', mount: { thick: 0 }, animated: false,
      draw(g, v) {
        lower.draw(g, v);
        g.save(); g.translate(lower.width + gap, 0); upper.draw(g, Object.assign({}, v, { cx: v.cx - lower.width - gap })); g.restore();
        g.fillStyle = '#e8ebe0'; g.fillRect(lower.width, 0, gap, lower.height);
      },
      hit(x, y) { return x < lower.width ? lower.hit(x, y) : upper.hit(x - lower.width - gap, y); },
      inField(cx, cy, r, side) { return (side === 'lower' ? lower : upper).stomata.filter((c) => Math.hypot(c.cx + c.ox - cx, c.cy - cy) < r); },
      lowerW: lower.width, gap,
    };
  }
  function countStep(side) {
    const tapped = new Set();
    const s = {
      title: `Count stomata: ${side} epidermis`,
      text: `Switch to <b>40×</b>, bring the <b>${side === 'lower' ? 'left (lower)' : 'right (upper)'}</b> peel into view, focus, and tap every stoma inside the circle.`,
      hint: 'A stoma is a pair of green, bean-shaped guard cells around a slit. Drag the field to the right peel for the upper epidermis.',
      tool: null, hideBelt: true, handler: eyeHandler,
      enter() { if (!view || !view.eye) makeView().open(); if (side === 'upper') view.eye.clearMarks(); },
      skip() { counts[side] = side === 'lower' ? 9 : 2; },
      onCell(c, e) {
        const eye = view.eye; const stt = eye.state;
        if (stt.objective !== 40) { ctx.say('Count at high power: switch to 40×.', 'hint', 2200); return; }
        if (e.blur > 2.5) { ctx.say('Focus first.', 'hint', 1500); return; }
        const onSide = side === 'lower' ? stt.cx < field.lowerW : stt.cx > field.lowerW + field.gap;
        if (!onSide) { ctx.say(`Move to the ${side === 'lower' ? 'left' : 'right'} peel first.`, 'hint', 2200); return; }
        if (!c || !c.stoma) { ctx.mistake('That is an ordinary epidermal cell — look for the pair of green guard cells.', 1); return; }
        if (c.side !== side) { ctx.say(`That stoma is on the other peel — count the ${side} epidermis now.`, 'hint', 2200); return; }
        if (tapped.has(c)) return;
        tapped.add(c); sfx.play('click'); eye.mark(c.cx + c.ox, c.cy, String(tapped.size), 'count');
        const remaining = field.inField(stt.cx, stt.cy, 13000 / 40 / 2 * 0.92, side).filter((q) => !tapped.has(q)).length;
        ctx.progress(tapped.size / Math.max(1, tapped.size + remaining));
        if (remaining === 0 && !this.done) { this.done = true; counts[side] = tapped.size; ui.observe(`Stomata, ${side} (per field)`, String(tapped.size)); anim.wait(0.8, () => ctx.next(`${tapped.size} stomata in this field of the ${side} epidermis.`)); }
      },
    };
    return s;
  }
  const stepFrequency = {
    title: 'Stomatal frequency', text: 'The high-power field is 0.325 mm across. Its area is π r² ≈ 0.083 mm².', tool: null, hideBelt: true, handler: eyeHandler,
    enter() {
      const a = Math.PI * Math.pow(0.325 / 2, 2);
      const lo = Math.round((counts.lower || 0) / a); const up = Math.round((counts.upper || 0) / a);
      ui.observe('Field area', `${a.toFixed(3)} mm²`); ui.observe('Lower surface', `${lo} per mm²`); ui.observe('Upper surface', `${up} per mm²`);
      ask('Which surface has more stomata?', [['lower', 'Lower surface'], ['upper', 'Upper surface'], ['same', 'About the same']], 'lower', `Lower ≈ ${lo}/mm², upper ≈ ${up}/mm². Dicot leaves have most stomata on the shaded lower surface, which cuts water loss by transpiration.`, 'Compare the two counts you made.');
    },
    exit() { ui.clearChooser(); },
  };

  const steps = plasmo
    ? [peelStep(0), stepWater, stepTransfer, stepCover, stepStage, stepFocus, stepTurgid, irrigateStep('salt'), irrigateStep('water')]
    : [peelStep(0), peelStep(1), stepWater, stepTransfer, stepCover, stepStage, stepFocus, countStep('lower'), countStep('upper'), stepFrequency];
  return {
    tools: ['hand', 'forceps', 'dropper', 'needle'],
    steps,
    update(dt, t) { if (view) view.update(t); },
    result() {
      if (plasmo) return { title: 'Plasmolysis observed', rows: [['Mounted in water', 'turgid'], ['In 5% NaCl', 'plasmolysed'], ['Back in water', 'deplasmolysed'], ['Air bubbles', String(st.bubbles)]], conclusion: 'In a hypertonic salt solution the cells of Rhoeo lost water from their vacuoles by exosmosis and the protoplasts shrank away from the cell walls (plasmolysis). Returned to water, they took water back by endosmosis and became turgid again (deplasmolysis). This shows the cell membrane is selectively permeable and the cell wall freely permeable.' };
      const a = Math.PI * Math.pow(0.325 / 2, 2);
      return { title: 'Stomatal distribution', rows: [['Lower, per field', String(counts.lower || 0)], ['Upper, per field', String(counts.upper || 0)], ['Lower, per mm²', String(Math.round((counts.lower || 0) / a))], ['Upper, per mm²', String(Math.round((counts.upper || 0) / a))]], conclusion: 'The lower epidermis of a dicot leaf bears many more stomata than the upper. With fewer pores facing the sun, the leaf loses less water by transpiration while still taking in carbon dioxide.' };
    },
    dispose() { if (view) view.dispose(); },
  };
}
