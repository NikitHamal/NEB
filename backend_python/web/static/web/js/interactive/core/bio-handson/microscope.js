// A school compound microscope at true size (about 32 cm tall; 1 unit = 10 cm): horseshoe base,
// pillar and curved arm, a square stage with two spring clips over a central aperture, an Abbe
// condenser with an iris diaphragm lever, a plane/concave mirror, a monocular body tube with a
// 10x eyepiece, a revolving nosepiece carrying 4x (red band), 10x (yellow) and 40x (blue)
// objectives, and coaxial coarse and fine focusing knobs. The nosepiece turns to the selected
// objective, the knobs turn as the stage is focused, and a slide can be laid under the clips.
import { THREE } from '../engine.js';
import { MAT, mesh, roundedSlab } from './kit.js';

const BLACK = () => MAT.gloss(0x1b1f24);
const OBJ = [{ mag: 4, color: 0xdc2626, len: 0.22 }, { mag: 10, color: 0xeab308, len: 0.3 }, { mag: 40, color: 0x2563eb, len: 0.38 }];

function horseshoe() {
  const s = new THREE.Shape();
  s.moveTo(-0.62, -0.5); s.lineTo(0.62, -0.5); s.quadraticCurveTo(0.74, -0.5, 0.74, -0.36);
  s.lineTo(0.62, 0.42); s.quadraticCurveTo(0.6, 0.58, 0.44, 0.58); s.lineTo(0.3, 0.58); s.lineTo(0.22, 0.05); s.lineTo(-0.22, 0.05); s.lineTo(-0.3, 0.58);
  s.lineTo(-0.44, 0.58); s.quadraticCurveTo(-0.6, 0.58, -0.62, 0.42); s.lineTo(-0.74, -0.36); s.quadraticCurveTo(-0.74, -0.5, -0.62, -0.5);
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.12, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 2, curveSegments: 8 });
  g.rotateX(-Math.PI / 2);
  return g;
}
function armGeometry() {
  // the C-shaped limb seen from the side: from the pillar top, back and up, over to the tube
  const s = new THREE.Shape();
  s.moveTo(-0.08, 0); s.lineTo(0.1, 0); s.bezierCurveTo(0.22, 0.4, 0.26, 0.9, 0.12, 1.42); s.lineTo(-0.02, 1.62);
  s.lineTo(-0.2, 1.54); s.bezierCurveTo(-0.02, 1.2, 0.02, 0.6, -0.08, 0);
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.16, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.015, bevelSegments: 2, curveSegments: 16 });
  g.translate(0, 0, -0.08);
  g.rotateY(-Math.PI / 2);
  return g;
}
function stageGeometry() {
  const s = new THREE.Shape();
  s.moveTo(-0.55, -0.55); s.lineTo(0.55, -0.55); s.lineTo(0.55, 0.55); s.lineTo(-0.55, 0.55); s.lineTo(-0.55, -0.55);
  const hole = new THREE.Path(); hole.absarc(0, 0, 0.09, 0, Math.PI * 2, true); s.holes.push(hole);
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.05, bevelEnabled: true, bevelThickness: 0.01, bevelSize: 0.01, bevelSegments: 1, curveSegments: 20 });
  g.rotateX(-Math.PI / 2);
  return g;
}
function knob(r, w, mat) {
  const g = new THREE.Group();
  const body = mesh(new THREE.CylinderGeometry(r, r, w, 28), mat); body.rotation.z = Math.PI / 2; g.add(body);
  for (let i = 0; i < 18; i++) {
    const a = (i / 18) * Math.PI * 2;
    const rib = mesh(new THREE.BoxGeometry(w * 0.9, r * 0.12, r * 0.08), mat, [0, Math.cos(a) * r, Math.sin(a) * r]);
    rib.rotation.x = a; g.add(rib);
  }
  return g;
}

export function buildMicroscope() {
  const root = new THREE.Group(); root.name = 'microscope';
  const black = BLACK(); const chrome = MAT.steel();
  root.add(mesh(horseshoe(), black, [0, 0.02, 0]));
  root.add(mesh(new THREE.CylinderGeometry(0.1, 0.13, 0.5, 20), black, [0, 0.36, 0.42]));
  const arm = mesh(armGeometry(), black, [0, 0.58, 0.42]); root.add(arm);
  // the stage and its focusing carriage (the stage moves; the tube is fixed)
  const stage = new THREE.Group(); stage.position.set(0, 1.18, -0.02); root.add(stage);
  stage.add(mesh(stageGeometry(), black));
  const clipMat = chrome;
  [-1, 1].forEach((side) => {
    const clip = new THREE.Group(); clip.position.set(side * 0.3, 0.065, 0.22);
    clip.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.05, 12), chrome));
    const strip = mesh(new THREE.BoxGeometry(0.05, 0.008, 0.36), clipMat, [0, 0.02, -0.16]); strip.rotation.x = -0.06; clip.add(strip);
    stage.add(clip);
  });
  const condenser = mesh(new THREE.CylinderGeometry(0.09, 0.07, 0.16, 24), black, [0, -0.1, 0]); stage.add(condenser);
  const lens = mesh(new THREE.CircleGeometry(0.06, 24), new THREE.MeshBasicMaterial({ color: 0xfff7e0 }), [0, 0.052, 0]); lens.rotation.x = -Math.PI / 2; stage.add(lens);
  const lever = mesh(new THREE.BoxGeometry(0.16, 0.012, 0.02), chrome, [0.12, -0.16, 0.05]); stage.add(lever);
  stage.add(mesh(new THREE.BoxGeometry(0.2, 0.3, 0.12), black, [0, -0.08, 0.44]));
  // mirror in its fork
  const mirror = new THREE.Group(); mirror.position.set(0, 0.62, -0.02); root.add(mirror);
  const fork = mesh(new THREE.TorusGeometry(0.17, 0.014, 6, 20, Math.PI), chrome); fork.rotation.z = Math.PI; mirror.add(fork);
  const disc = new THREE.Group(); disc.rotation.x = -0.75; mirror.add(disc);
  disc.add(mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.03, 32), black));
  disc.add(mesh(new THREE.CylinderGeometry(0.135, 0.135, 0.032, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0.04 })));
  // focusing knobs, coaxial: coarse (large) and fine (small) on both sides
  const knobs = new THREE.Group(); knobs.position.set(0, 1.05, 0.48); root.add(knobs);
  const coarse = []; const fine = [];
  [-1, 1].forEach((side) => {
    const c = knob(0.13, 0.06, black); c.position.x = side * 0.15; knobs.add(c); coarse.push(c);
    const f = knob(0.07, 0.05, chrome); f.position.x = side * 0.22; knobs.add(f); fine.push(f);
  });
  // body tube, eyepiece, nosepiece
  const head = new THREE.Group(); head.position.set(0, 2.05, 0.05); root.add(head);
  head.add(mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.62, 28), black, [0, 0.36, -0.02]));
  head.add(mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.2, 24), chrome, [0, 0.76, -0.02]));
  const eyepiece = new THREE.Group(); eyepiece.position.set(0, 0.86, -0.02); head.add(eyepiece); eyepiece.name = 'eyepiece';
  eyepiece.add(mesh(new THREE.CylinderGeometry(0.085, 0.08, 0.16, 24), MAT.matte(0x111111), [0, 0.08, 0]));
  const eyeGlass = mesh(new THREE.CircleGeometry(0.05, 20), new THREE.MeshStandardMaterial({ color: 0x1e3a5f, metalness: 0.4, roughness: 0.05 }), [0, 0.162, 0]); eyeGlass.rotation.x = -Math.PI / 2; eyepiece.add(eyeGlass);
  head.add(mesh(new THREE.BoxGeometry(0.24, 0.16, 0.26), black, [0, 0.0, 0.26]));
  const turret = new THREE.Group(); turret.position.set(0, -0.06, -0.12); turret.rotation.x = 0.12; head.add(turret);
  turret.add(mesh(new THREE.CylinderGeometry(0.19, 0.16, 0.08, 32), chrome));
  const objectives = OBJ.map((o, i) => {
    const g = new THREE.Group();
    const a = (i / OBJ.length) * Math.PI * 2;
    g.position.set(Math.sin(a) * 0.1, -0.04, Math.cos(a) * 0.1);
    g.rotation.x = -0.12;
    const barrel = mesh(new THREE.CylinderGeometry(0.05, 0.035, o.len, 20), chrome, [0, -o.len / 2, 0]); g.add(barrel);
    g.add(mesh(new THREE.CylinderGeometry(0.051, 0.051, 0.025, 20), MAT.plastic(o.color), [0, -o.len * 0.35, 0]));
    g.add(mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.01, 12), MAT.matte(0x0b0b0b), [0, -o.len, 0]));
    g.userData.mag = o.mag; g.userData.angle = a;
    turret.add(g);
    return g;
  });
  root.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  let current = 1; let turretAngle = -objectives[1].userData.angle; turret.rotation.y = turretAngle;
  let knobAngle = 0;
  const stageY0 = stage.position.y;
  return {
    root, stage, eyepiece, objectives, turret, mirror, mirrorDisc: disc,
    /** World-space top of the stage, where a slide rests. */
    stageTop: 0.06,
    stageY0,
    get objective() { return OBJ[current].mag; },
    pickObjective(obj) { return objectives.indexOf(obj); },
    /** Turns the nosepiece toward objective index i (returns the angle goal; the caller animates). */
    turretGoal(i) { current = i; let goal = -objectives[i].userData.angle; while (goal - turretAngle > Math.PI) goal -= Math.PI * 2; while (goal - turretAngle < -Math.PI) goal += Math.PI * 2; return goal; },
    setTurret(a) { turretAngle = a; turret.rotation.y = a; },
    get turretAngle() { return turretAngle; },
    /** Stage height offset (units) for a focus position, and knob rotation. */
    setFocus(stageOffset, knobDelta) {
      stage.position.y = stageY0 + stageOffset;
      knobAngle += knobDelta;
      coarse.forEach((c) => { c.rotation.x = knobAngle; }); fine.forEach((f) => { f.rotation.x = knobAngle * 4; });
    },
    pickables: objectives.concat([eyepiece]),
  };
}

/** The white glazed tile the slide work is done on. */
export function tile(w = 1.6, d = 1.2) {
  return mesh(roundedSlab(w, d, 0.03, 0.04, 0.005), MAT.gloss(0xf8fafc));
}
