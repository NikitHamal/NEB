import { THREE, createEngine, createOrbitControls, basicLights, makeLabelSprite } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SCALE = 0.04; // 1 cm = 0.04 world units

export default function init(stage, opts) {
  const engine = createEngine(stage, {});
  if (!engine) return null;
  const { scene, camera, quality } = engine;
  const seg = quality.segments;

  camera.position.set(0, 4, 12);
  const controls = createOrbitControls(camera, engine.canvas, {
    minDistance: 2, maxDistance: 30,
    target: new THREE.Vector3(0, 0, 0),
  });
  controls.setTarget(new THREE.Vector3(0, 0, 0));

  basicLights(scene, { ambient: 0.55, key: 1.4 });
  scene.background = new THREE.Color(0x0b1c30);

  // Optical bench (rod)
  const benchGeo = new THREE.CylinderGeometry(0.04, 0.04, 18, 12);
  const benchMat = new THREE.MeshStandardMaterial({ color: 0x5d779e, metalness: 0.5, roughness: 0.4 });
  const bench = new THREE.Mesh(benchGeo, benchMat);
  bench.rotation.z = Math.PI / 2;
  scene.add(bench);

  // Scale ticks on bench
  for (let x = -8; x <= 8; x += 1) {
    const tick = new THREE.Mesh(new THREE.BoxGeometry(0.02, x % 2 === 0 ? 0.25 : 0.15, 0.02), new THREE.MeshBasicMaterial({ color: 0x8aa3c8 }));
    tick.position.set(x, -0.15, 0);
    scene.add(tick);
  }
  const scaleLabel = makeLabelSprite('← 200 cm bench →', { scale: 1.0, fontSize: 28 });
  scaleLabel.position.set(0, -0.6, 0);
  scene.add(scaleLabel);

  // Lens / mirror element group (rebuilt on element change)
  const elementGroup = new THREE.Group();
  scene.add(elementGroup);

  // Object arrow group
  const objectGroup = new THREE.Group();
  scene.add(objectGroup);
  const objArrowBody = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1, 8), new THREE.MeshStandardMaterial({ color: 0xF59E0B, emissive: 0x7a4f00, emissiveIntensity: 0.2 }));
  objArrowBody.position.y = 0.5;
  objectGroup.add(objArrowBody);
  const objArrowTip = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.22, 8), new THREE.MeshStandardMaterial({ color: 0xF59E0B }));
  objArrowTip.position.y = 1.1;
  objectGroup.add(objArrowTip);
  const objLabel = makeLabelSprite('object', { scale: 0.9, fontSize: 30 });
  objLabel.position.set(0, 1.5, 0);
  objectGroup.add(objLabel);

  // Image arrow group
  const imageGroup = new THREE.Group();
  scene.add(imageGroup);
  const imgArrowBody = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1, 8), new THREE.MeshStandardMaterial({ color: 0x8be9a8, transparent: true, opacity: 0.9 }));
  imgArrowBody.position.y = 0.5;
  imageGroup.add(imgArrowBody);
  const imgArrowTip = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.22, 8), new THREE.MeshStandardMaterial({ color: 0x8be9a8, transparent: true, opacity: 0.9 }));
  imgArrowTip.position.y = 1.1;
  imageGroup.add(imgArrowTip);
  const imgLabel = makeLabelSprite('image', { scale: 0.9, fontSize: 30 });
  imgLabel.position.set(0, 1.5, 0);
  imageGroup.add(imgLabel);
  imageGroup.visible = false;

  // Ray lines (3 principal rays)
  const RAY_COLORS_HEX = [0x7dd3fc, 0xf472b6, 0xa3e635];
  const rayLines = [];
  const rayGeos = [];
  for (let i = 0; i < 3; i++) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(9), 3));
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: RAY_COLORS_HEX[i], transparent: true, opacity: 0.85 }));
    scene.add(line);
    rayLines.push(line);
    rayGeos.push(geo);
  }

  // Focal point markers
  const fDotMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0x7a5000, emissiveIntensity: 0.4 });
  const fDot1 = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), fDotMat);
  const fDot2 = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), fDotMat);
  scene.add(fDot1);
  scene.add(fDot2);
  const fLabel1 = makeLabelSprite('F', { scale: 0.7, fontSize: 28 });
  const fLabel2 = makeLabelSprite("F'", { scale: 0.7, fontSize: 28 });
  scene.add(fLabel1);
  scene.add(fLabel2);

  // State
  let element = 'convex-lens';
  let fMag = 40; // cm
  let objDist = 100; // cm
  const objH = 32; // cm (height of arrow)

  function isMirror() { return element.endsWith('mirror'); }
  function focal() { return element === 'convex-lens' || element === 'concave-mirror' ? fMag : -fMag; }
  function toWorld(cm) { return cm * SCALE; }

  function compute() {
    const f = focal();
    const denom = objDist - f;
    if (Math.abs(denom) < 2) return { atFocus: true, f };
    const di = (f * objDist) / denom;
    const hi = (-objH * di) / objDist;
    const m = -di / objDist;
    return { atFocus: false, f, di, hi, m, real: di > 0 };
  }

  function buildElement() {
    elementGroup.clear();
    const H = toWorld(120);
    if (element.includes('lens')) {
      const bulge = element === 'convex-lens' ? 0.18 : -0.15;
      // Create lens shape with a tube-like geometry
      const lensShape = new THREE.Shape();
      lensShape.moveTo(-H / 2, 0);
      lensShape.quadraticCurveTo(bulge, 0, H / 2, 0);
      // Simple flat disc for now
      const lensMat = new THREE.MeshStandardMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.35, side: THREE.DoubleSide });
      const lensGeo = new THREE.CylinderGeometry(H / 2, H / 2, Math.abs(bulge) * 0.6 + 0.05, seg, 1);
      const lensMesh = new THREE.Mesh(lensGeo, lensMat);
      lensMesh.rotation.z = Math.PI / 2;
      elementGroup.add(lensMesh);
      // Outline ring
      const ringGeo = new THREE.TorusGeometry(H / 2, 0.03, 8, 32);
      elementGroup.add(new THREE.Mesh(ringGeo, new THREE.MeshStandardMaterial({ color: 0xc7d4ea, roughness: 0.5 })));
    } else {
      // Mirror disc
      const mirrorMat = new THREE.MeshStandardMaterial({ color: 0x8aa3c8, metalness: 0.8, roughness: 0.2, side: THREE.DoubleSide });
      const mirrorGeo = new THREE.CircleGeometry(H / 2, 24);
      const mirrorMesh = new THREE.Mesh(mirrorGeo, mirrorMat);
      mirrorMesh.rotation.y = Math.PI / 2;
      elementGroup.add(mirrorMesh);
    }
    const elemLabel = makeLabelSprite(
      element === 'convex-lens' ? 'Converging lens' : element === 'concave-lens' ? 'Diverging lens' : element === 'concave-mirror' ? 'Concave mirror' : 'Convex mirror',
      { scale: 0.9, fontSize: 30 }
    );
    elemLabel.position.set(0, toWorld(140), 0);
    elementGroup.add(elemLabel);
  }
  buildElement();

  function updateScene() {
    const res = compute();
    const f = res.f;

    // Object position (to the left of lens)
    const objX = -toWorld(objDist);
    objectGroup.position.set(objX, 0, 0);
    objectGroup.scale.y = 1;

    // Focal dots
    const fW = toWorld(Math.abs(f));
    if (!isMirror()) {
      fDot1.position.set(-fW, 0, 0);
      fDot2.position.set(fW, 0, 0);
      fLabel1.position.set(-fW, 0.3, 0);
      fLabel2.position.set(fW, 0.3, 0);
      fDot2.visible = true;
      fLabel2.visible = true;
    } else {
      fDot1.position.set(-fW * (f > 0 ? 1 : -1), 0, 0);
      fDot2.visible = false;
      fLabel2.visible = false;
      fLabel1.position.copy(fDot1.position).add(new THREE.Vector3(0, 0.3, 0));
    }

    // Image
    if (!res.atFocus && res.hi !== undefined) {
      const imgX = isMirror() ? -toWorld(res.di) : toWorld(res.di);
      const imgH = toWorld(Math.abs(res.hi));
      const imgFlipped = res.hi < 0;

      imageGroup.position.set(imgX, 0, 0);
      imageGroup.scale.y = imgFlipped ? -1 : 1;
      // Scale height
      const bodyScale = imgH / toWorld(objH);
      imgArrowBody.scale.y = bodyScale;
      imgArrowBody.position.y = bodyScale / 2;
      imgArrowTip.position.y = bodyScale + 0.11;

      const isReal = res.real;
      const c = isReal ? 0x8be9a8 : 0xc4b5fd;
      imgArrowBody.material.color.setHex(c);
      imgArrowTip.material.color.setHex(c);
      imgArrowBody.material.opacity = isReal ? 0.9 : 0.75;
      imageGroup.visible = true;

      const natText = `${isReal ? 'Real' : 'Virtual'} · ${res.m > 0 ? 'upright' : 'inverted'} · ×${Math.abs(res.m).toFixed(2)}`;
      const imgLabelNew = makeLabelSprite(natText, { scale: 0.9, fontSize: 28, bg: isReal ? 'rgba(0,80,30,0.8)' : 'rgba(60,20,80,0.8)' });
      imgLabel.material.map.dispose();
      imgLabel.material = imgLabelNew.material;
      imgLabel.scale.copy(imgLabelNew.scale);
      imgLabel.position.set(0, bodyScale + 0.5, 0);
      scene.remove(imgLabelNew);
    } else {
      imageGroup.visible = false;
    }

    // Principal rays (simplified 3-ray construction)
    // Ray from tip of object, parallel → through focal point after lens
    const objTipY = toWorld(objH);
    const REACH = 9;
    const ob = { x: objX, y: objTipY };
    const cx = 0; // lens at x=0

    if (!res.atFocus && res.hi !== undefined) {
      const imgX = isMirror() ? -toWorld(res.di) : toWorld(res.di);
      const imgTipY = toWorld(res.hi);

      const rayDefs = [
        // Ray 1: parallel to axis → through front focal after element
        { from: ob, through: { x: cx, y: objTipY }, to: { x: imgX, y: imgTipY } },
        // Ray 2: through optical centre unchanged
        { from: ob, through: { x: cx, y: 0 }, to: { x: imgX, y: imgTipY } },
        // Ray 3: through focal to element → parallel after
        { from: ob, through: { x: cx, y: objTipY * 0.6 }, to: { x: imgX, y: imgTipY } },
      ];

      rayDefs.forEach(({ from, to, through }, i) => {
        const pos = rayGeos[i].attributes.position.array;
        // from → through
        pos[0] = from.x; pos[1] = from.y; pos[2] = 0;
        pos[3] = through.x; pos[4] = through.y; pos[5] = 0;
        // through → end (real image direction or extended)
        const ex = res.real ? to.x : to.x * 0.5;
        const ey = res.real ? to.y : to.y * 0.5;
        pos[6] = ex; pos[7] = ey; pos[8] = 0;
        rayGeos[i].attributes.position.needsUpdate = true;
        rayGeos[i].setDrawRange(0, 3);
        rayLines[i].visible = true;
      });
    } else {
      rayLines.forEach((l) => { l.visible = false; });
    }
  }

  // Panel
  const panel = createPanel(stage, { title: 'Optics 3D' });
  panel.select({
    label: 'Optical element',
    options: [
      { value: 'convex-lens', label: 'Converging (convex) lens' },
      { value: 'concave-lens', label: 'Diverging (concave) lens' },
      { value: 'concave-mirror', label: 'Concave mirror' },
      { value: 'convex-mirror', label: 'Convex mirror' },
    ],
    value: element,
    onChange: (v) => { element = v; buildElement(); },
  });
  panel.slider({
    label: 'Focal length |f|', min: 20, max: 90, step: 1, value: fMag,
    format: (v) => `${v} cm`, onChange: (v) => { fMag = v; },
  });
  const objSlider = panel.slider({
    label: 'Object distance u', min: 15, max: 190, step: 1, value: objDist,
    format: (v) => `${v} cm`, onChange: (v) => { objDist = v; },
  });
  panel.divider();
  const uOut = panel.readout({ label: 'u (object)', value: '—' });
  const vOut = panel.readout({ label: 'v (image)', value: '—' });
  const mOut = panel.readout({ label: 'Magnification m', value: '—' });
  const natOut = panel.readout({ label: 'Image is', value: '—' });
  panel.info('Drag the object distance slider to move the object along the 3D bench. Orbit to see 3D ray cones. 1/f = 1/v + 1/u (thin-lens equation).');

  const hud = createHud(stage);
  const natureBadge = hud.badge('Real · inverted', '#F59E0B');

  engine.setUpdate((dt) => {
    controls.update(dt);
    updateScene();

    const res = compute();
    uOut.set(`${objDist.toFixed(0)} cm`);
    if (res.atFocus) {
      vOut.set('∞');
      mOut.set('—');
      natOut.set('No image (object at focus)');
      natureBadge.set('No image — parallel rays');
    } else {
      vOut.set(`${Math.abs(res.di).toFixed(1)} cm ${res.real ? '(real)' : '(virtual)'}`);
      mOut.set(`${res.m.toFixed(2)}×`);
      const upright = res.m > 0;
      const size = Math.abs(res.m) > 1.02 ? 'magnified' : Math.abs(res.m) < 0.98 ? 'reduced' : 'same size';
      const nat = `${res.real ? 'Real' : 'Virtual'}, ${upright ? 'upright' : 'inverted'}, ${size}`;
      natOut.set(nat);
      natureBadge.set(`${res.real ? 'Real' : 'Virtual'} · ${upright ? 'upright' : 'inverted'}`);
    }
  });

  engine.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      controls.dispose();
      engine.dispose();
    },
  };
}
