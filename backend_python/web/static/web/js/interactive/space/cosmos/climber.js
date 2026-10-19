import { THREE } from '../../core/engine.js';

function lathe(profile, seg = 20) {
  return new THREE.LatheGeometry(profile.map(([r, y]) => new THREE.Vector2(r, y)), seg);
}

function puffy(r0, r1, h, rings, seg) {
  const pts = [];
  const n = rings * 6;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const bulge = 1 + 0.06 * Math.pow(Math.sin(t * rings * Math.PI), 2);
    const cap = Math.sin(Math.min(1, Math.min(t, 1 - t) * 6) * Math.PI / 2);
    pts.push([Math.max(0.001, (r0 + (r1 - r0) * t) * bulge * (0.25 + 0.75 * cap)), t * h]);
  }
  return lathe(pts, seg);
}

function limb(a, b, r0, r1, mat, parent) {
  const va = new THREE.Vector3(...a); const vb = new THREE.Vector3(...b);
  const len = va.distanceTo(vb);
  const geo = puffy(r0, r1, len, 4, 14);
  const m = new THREE.Mesh(geo, mat);
  m.position.copy(va);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vb.clone().sub(va).normalize());
  parent.add(m);
  const j = new THREE.Mesh(new THREE.SphereGeometry(r1 * 1.02, 14, 10), mat);
  j.position.copy(vb);
  parent.add(j);
  return m;
}

function flagTexture() {
  const c = document.createElement('canvas');
  c.width = 64; c.height = 64;
  const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, 64, 64);
  g.globalAlpha = 0.35; g.fillStyle = '#222';
  for (let i = 0; i < 7; i++) g.fillRect(10, 12 + i * 6, 44 - (i % 3) * 6, 2);
  g.beginPath(); g.arc(32, 30, 9, 0, Math.PI * 2); g.lineWidth = 2; g.strokeStyle = '#222'; g.stroke();
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function prayerFlags(from, to, count, sag, uniforms) {
  const colors = [0x1f5fbf, 0xf4f1e6, 0xc3262b, 0x2f8a3c, 0xf2c230];
  const group = new THREE.Group();
  const a = new THREE.Vector3(...from); const b = new THREE.Vector3(...to);
  const pts = [];
  for (let i = 0; i <= 24; i++) {
    const t = i / 24;
    const p = a.clone().lerp(b, t);
    p.y -= Math.sin(t * Math.PI) * sag;
    pts.push(p);
  }
  const curve = new THREE.CatmullRomCurve3(pts);
  const cord = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, 0.004, 4, false), new THREE.MeshStandardMaterial({ color: 0x8a7d6a, roughness: 1 }));
  group.add(cord);
  const tex = flagTexture();
  const geo = new THREE.PlaneGeometry(0.2, 0.24, 6, 6);
  geo.translate(0, -0.12, 0);
  for (let i = 0; i < count; i++) {
    const t = (i + 0.5) / count;
    const mat = new THREE.MeshStandardMaterial({ color: colors[i % 5], map: tex, roughness: 0.9, side: THREE.DoubleSide });
    mat.onBeforeCompile = (sh) => {
      sh.uniforms.uTime = uniforms.uTime;
      sh.uniforms.uPhase = { value: i * 0.7 };
      sh.vertexShader = 'uniform float uTime; uniform float uPhase;\n' + sh.vertexShader.replace('#include <begin_vertex>', `
        vec3 transformed = vec3(position);
        float hang = clamp(-position.y / 0.24, 0.0, 1.0);
        float w = sin(uTime * 7.0 + uPhase + position.x * 18.0 + position.y * 9.0) * 0.5 + sin(uTime * 11.3 + uPhase * 2.0 + position.y * 22.0) * 0.25;
        transformed.z += w * 0.05 * hang;
        transformed.x += hang * 0.03 * sin(uTime * 3.0 + uPhase);
        transformed.y += hang * 0.02;`);
    };
    const flag = new THREE.Mesh(geo, mat);
    const p = curve.getPoint(t);
    flag.position.copy(p);
    const tan = curve.getTangent(t);
    flag.rotation.y = Math.atan2(-tan.z, tan.x);
    group.add(flag);
  }
  return { group, tex, geo };
}

export function createClimber(ground = () => -0.4) {
  const root = new THREE.Group();
  const uniforms = { uTime: { value: 0 } };
  const suit = new THREE.MeshPhysicalMaterial({ color: 0xe8541c, roughness: 0.55, sheen: 0.6, sheenColor: new THREE.Color(0xffb38a), sheenRoughness: 0.5 });
  const pants = new THREE.MeshPhysicalMaterial({ color: 0x1b2230, roughness: 0.6, sheen: 0.4, sheenColor: new THREE.Color(0x6f7d99) });
  const boot = new THREE.MeshStandardMaterial({ color: 0xf2c94c, roughness: 0.5 });
  const sole = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.8 });
  const glove = new THREE.MeshStandardMaterial({ color: 0x15171c, roughness: 0.75 });
  const metal = new THREE.MeshStandardMaterial({ color: 0xc7ccd4, metalness: 1, roughness: 0.3 });
  const goggle = new THREE.MeshPhysicalMaterial({ color: 0x0f0f12, metalness: 0.2, roughness: 0.05, clearcoat: 1, iridescence: 0.8, iridescenceIOR: 1.6 });
  const pack = new THREE.MeshStandardMaterial({ color: 0x24406b, roughness: 0.8 });
  const bottle = new THREE.MeshStandardMaterial({ color: 0xd8a62a, metalness: 0.6, roughness: 0.35 });
  const fur = new THREE.MeshStandardMaterial({ color: 0x6e5a44, roughness: 1 });

  const body = new THREE.Group();
  root.add(body);
  [-1, 1].forEach((s) => {
    const b = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.13, 0.3, 2, 2, 2), boot);
    b.position.set(0.12 * s, 0.075, 0.03);
    body.add(b);
    const so = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.03, 0.32), sole);
    so.position.set(0.12 * s, 0.015, 0.03);
    body.add(so);
    const cr = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.02, 0.28), metal);
    cr.position.set(0.12 * s, 0.002, 0.03);
    body.add(cr);
    limb([0.12 * s, 0.13, 0], [0.11 * s, 0.5, 0.02], 0.085, 0.08, pants, body);
    limb([0.11 * s, 0.5, 0.02], [0.1 * s, 0.9, 0], 0.08, 0.1, pants, body);
  });
  const torso = new THREE.Mesh(puffy(0.21, 0.24, 0.62, 6, 24), suit);
  torso.position.y = 0.86; torso.scale.z = 0.78;
  body.add(torso);
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.05, 10, 20), suit);
  collar.rotation.x = Math.PI / 2; collar.position.y = 1.47;
  body.add(collar);
  const head = new THREE.Group();
  head.position.set(0, 1.6, 0.01);
  body.add(head);
  const hood = new THREE.Mesh(new THREE.SphereGeometry(0.13, 24, 18), suit);
  hood.scale.set(1, 1.12, 1.05);
  head.add(hood);
  const face = new THREE.Mesh(new THREE.CircleGeometry(0.075, 24), new THREE.MeshStandardMaterial({ color: 0x2a1d17, roughness: 0.9 }));
  face.scale.set(1, 1.15, 1); face.position.set(0, -0.005, 0.128);
  head.add(face);
  const ruff = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.024, 10, 28), fur);
  ruff.scale.set(1, 1.18, 0.8); ruff.position.set(0, -0.005, 0.122);
  head.add(ruff);
  const gog = new THREE.Mesh(new THREE.SphereGeometry(0.105, 24, 12, -0.9, 1.8, 1.1, 0.45), goggle);
  gog.position.set(0, 0.03, 0.05);
  head.add(gog);
  const mask = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), glove);
  mask.scale.set(1, 0.85, 0.75); mask.position.set(0, -0.045, 0.125);
  head.add(mask);
  const hose = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([
    new THREE.Vector3(0.03, -0.08, 0.12), new THREE.Vector3(0.12, -0.2, 0.08), new THREE.Vector3(0.16, -0.3, -0.12), new THREE.Vector3(0.1, -0.4, -0.22)]), 20, 0.012, 6), glove);
  head.add(hose);
  const bag = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.46, 0.18, 3, 3, 2), pack);
  bag.position.set(0, 1.13, -0.24);
  body.add(bag);
  const cyl = new THREE.Mesh(new THREE.CapsuleGeometry(0.055, 0.36, 6, 14), bottle);
  cyl.position.set(0.05, 1.2, -0.36);
  body.add(cyl);
  limb([-0.25, 1.38, 0], [-0.33, 1.08, 0.05], 0.075, 0.065, suit, body);
  limb([-0.33, 1.08, 0.05], [-0.3, 0.86, 0.16], 0.065, 0.055, suit, body);
  const gl = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), glove);
  gl.position.set(-0.3, 0.82, 0.18);
  body.add(gl);
  const axe = new THREE.Group();
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.7, 10), metal);
  shaft.position.y = -0.35;
  axe.add(shaft);
  const headA = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.03, 0.02), metal);
  headA.position.y = 0.01;
  axe.add(headA);
  axe.position.set(-0.3, 0.82, 0.18);
  axe.rotation.z = 0.1;
  body.add(axe);
  const arm = new THREE.Group();
  arm.position.set(0.25, 1.38, 0);
  body.add(arm);
  limb([0, 0, 0], [0.12, 0.26, 0.04], 0.075, 0.065, suit, arm);
  limb([0.12, 0.26, 0.04], [0.16, 0.52, 0.08], 0.065, 0.055, suit, arm);
  const g2 = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), glove);
  g2.position.set(0.17, 0.57, 0.09);
  arm.add(g2);
  root.traverse((o) => { if (o.isMesh) { o.castShadow = true; } });

  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.025, 1.3, 8), new THREE.MeshStandardMaterial({ color: 0x6b5a45, roughness: 0.9 }));
  pole.position.set(-0.9, 0.55, -0.6);
  root.add(pole);
  const end = (x, z) => [x, ground(x, z) + 0.06, z];
  pole.position.y = ground(-0.9, -0.6) + 0.6;
  const top = pole.position.y + 0.6;
  const f1 = prayerFlags([-0.9, top, -0.6], end(2.1, -1.7), 14, 0.25, uniforms);
  const f2 = prayerFlags([-0.9, top - 0.06, -0.6], end(-2.6, 1.3), 12, 0.2, uniforms);
  const f3 = prayerFlags([-0.9, top - 0.03, -0.6], end(0.5, 2.3), 12, 0.22, uniforms);
  [[2.1, -1.7], [-2.6, 1.3], [0.5, 2.3]].forEach(([x, z]) => {
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.3, 6), metal);
    st.position.set(x, ground(x, z) + 0.12, z);
    root.add(st);
  });
  root.add(f1.group, f2.group, f3.group);
  const lean = arm.rotation;
  return {
    group: root,
    update(t) {
      uniforms.uTime.value = t;
      lean.z = -0.12 + Math.sin(t * 1.3) * 0.06;
      head.rotation.y = Math.sin(t * 0.35) * 0.35;
      body.rotation.z = Math.sin(t * 0.9) * 0.01;
    },
    dispose() {
      [f1, f2, f3].forEach((f) => { f.tex.dispose(); f.geo.dispose(); });
    },
  };
}
