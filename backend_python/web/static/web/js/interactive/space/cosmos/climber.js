import { THREE } from '../../core/engine.js';
import { buildClimber } from './climber-model.js';

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

function sculpt(tier) {
  return new Promise((resolve) => {
    let w;
    try { w = new Worker(new URL('./climber-worker.js', import.meta.url), { type: 'module' }); } catch (e) { resolve(buildClimber(tier)); return; }
    w.onmessage = (e) => { w.terminate(); resolve(e.data); };
    w.onerror = (e) => { e.preventDefault && e.preventDefault(); w.terminate(); resolve(buildClimber(tier)); };
    w.postMessage({ tier });
  });
}

function partMesh(part, mat) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(part.mesh.position, 3));
  g.setAttribute('normal', new THREE.BufferAttribute(part.mesh.normal, 3));
  g.setAttribute('color', new THREE.BufferAttribute(part.color, 3));
  g.setIndex(new THREE.BufferAttribute(part.mesh.index, 1));
  g.computeBoundingSphere();
  return new THREE.Mesh(g, mat);
}

export async function createClimber(ground = () => -0.4, tier = 'medium') {
  const root = new THREE.Group();
  const uniforms = { uTime: { value: 0 } };
  const parts = await sculpt(tier);
  // nylon down: a soft sheen at grazing angles, a little gloss on the shell fabric
  const fabric = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, metalness: 0 });
  fabric.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <opaque_fragment>', `
      { float r = pow(1.0 - clamp(dot(normal, normalize(vViewPosition)), 0.0, 1.0), 3.0);
        outgoingLight += diffuseColor.rgb * r * 0.45 + vec3(0.03) * r; }
      #include <opaque_fragment>`);
  };
  const metal = new THREE.MeshStandardMaterial({ color: 0xc7ccd4, metalness: 1, roughness: 0.28 });
  const goggle = new THREE.MeshPhysicalMaterial({ color: 0x0b0c10, metalness: 0.3, roughness: 0.06, clearcoat: 1, iridescence: 0.9, iridescenceIOR: 1.7 });
  const strap = new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: 0.8 });
  const bottle = new THREE.MeshStandardMaterial({ color: 0xd9541e, metalness: 0.5, roughness: 0.35 });

  const body = new THREE.Group();
  root.add(body);
  body.add(partMesh(parts.body, fabric));
  const head = new THREE.Group();
  head.position.set(0, 1.55, 0.01);
  body.add(head);
  head.add(partMesh(parts.head, fabric));
  const gog = new THREE.Mesh(new THREE.SphereGeometry(0.112, 32, 12, -0.95, 1.9, 1.08, 0.42), goggle);
  gog.position.set(0, 0.075, 0.035);
  head.add(gog);
  const band = new THREE.Mesh(new THREE.TorusGeometry(0.133, 0.01, 6, 40), strap);
  band.rotation.x = Math.PI / 2 - 0.12; band.position.set(0, 0.1, -0.005); band.scale.set(1, 1.04, 1);
  head.add(band);
  const hose = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([
    new THREE.Vector3(0.04, -0.03, 0.17), new THREE.Vector3(0.12, -0.12, 0.12), new THREE.Vector3(0.17, -0.25, -0.05), new THREE.Vector3(0.12, -0.36, -0.2)]), 24, 0.011, 8), strap);
  head.add(hose);
  const cyl = new THREE.Mesh(new THREE.CapsuleGeometry(0.052, 0.38, 8, 16), bottle);
  cyl.position.set(0.06, 1.23, -0.36);
  const valve = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.022, 0.06, 10), metal);
  valve.position.set(0.06, 1.47, -0.36);
  body.add(cyl, valve);

  // the ice axe planted beside the left boot, mitten on its head
  const axe = new THREE.Group();
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.013, 0.016, 0.66, 12), new THREE.MeshStandardMaterial({ color: 0x2d6cdf, metalness: 0.6, roughness: 0.35 }));
  shaft.position.y = -0.36;
  const spike = new THREE.Mesh(new THREE.ConeGeometry(0.016, 0.06, 10), metal);
  spike.position.y = -0.72; spike.rotation.x = Math.PI;
  const pick = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.024, 0.014), metal);
  pick.position.set(0.07, 0, 0); pick.rotation.z = -0.18;
  const adze = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.02, 0.04), metal);
  adze.position.set(-0.06, 0.004, 0);
  axe.add(shaft, spike, pick, adze);
  axe.position.set(-0.3, 0.8, 0.2);
  axe.rotation.z = 0.08;
  body.add(axe);

  const arm = new THREE.Group();
  arm.position.set(0.235, 1.43, 0);
  body.add(arm);
  arm.add(partMesh(parts.arm, fabric));
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
      lean.z = -0.1 + Math.sin(t * 1.3) * 0.07;
      lean.x = Math.sin(t * 0.65) * 0.04;
      head.rotation.y = Math.sin(t * 0.35) * 0.35;
      body.rotation.z = Math.sin(t * 0.9) * 0.01;
    },
    dispose() {
      [f1, f2, f3].forEach((f) => { f.tex.dispose(); f.geo.dispose(); });
      root.traverse((o) => { if (o.isMesh) { o.geometry.dispose(); } });
      [fabric, metal, goggle, strap, bottle].forEach((m) => m.dispose());
    },
  };
}
