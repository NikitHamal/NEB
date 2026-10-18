// A working Bunsen burner: a bench gas tap and rubber tubing, a cast base, a chrome barrel and a
// rotating brass collar over the air holes. With the collar shut the gas burns as a lazy yellow
// luminous flame (soot glowing); opened, premixed air gives the roaring blue cone with a pale
// inner cone, the hottest point just above its tip. setGas/setAir drive it; update(t) animates.
import { THREE } from '../engine.js';
import { MAT, mesh } from '../bio-handson/kit.js';
import { flameMaterial, flameGeometry } from './flame.js';

export function bunsen(quality) {
  const g = new THREE.Group();
  g.add(mesh(new THREE.CylinderGeometry(0.3, 0.34, 0.07, 36), MAT.matte(0x22272e), [0, 0.035, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.11, 0.16, 0.08, 24), MAT.matte(0x22272e), [0, 0.1, 0]));
  const barrel = mesh(new THREE.CylinderGeometry(0.055, 0.058, 1.15, 28), MAT.steel(), [0, 0.7, 0]); g.add(barrel);
  g.add(mesh(new THREE.TorusGeometry(0.055, 0.008, 6, 24), MAT.steel(), [0, 1.275, 0]).rotateX(Math.PI / 2));
  const collar = new THREE.Group(); collar.position.y = 0.3;
  const brass = new THREE.MeshStandardMaterial({ color: 0xd4a94a, metalness: 1, roughness: 0.3 });
  collar.add(mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.16, 28, 1, true), brass));
  for (let i = 0; i < 2; i++) { const hole = mesh(new THREE.CircleGeometry(0.03, 16), MAT.matte(0x0b0b0b), [Math.cos(i * Math.PI) * 0.0765, 0, Math.sin(i * Math.PI) * 0.0765]); hole.lookAt(Math.cos(i * Math.PI), 0, Math.sin(i * Math.PI)); collar.add(hole); }
  const knurl = mesh(new THREE.TorusGeometry(0.077, 0.007, 6, 28), brass, [0, 0.07, 0]); knurl.rotation.x = Math.PI / 2; collar.add(knurl);
  g.add(collar);
  const inlet = mesh(new THREE.CylinderGeometry(0.022, 0.026, 0.32, 12), brass, [0.19, 0.13, 0]); inlet.rotation.z = Math.PI / 2; g.add(inlet);
  const tubePts = [new THREE.Vector3(0.34, 0.13, 0), new THREE.Vector3(0.7, 0.05, 0.05), new THREE.Vector3(1.1, 0.04, -0.2), new THREE.Vector3(1.35, 0.05, -0.55), new THREE.Vector3(1.4, 0.2, -0.8)];
  g.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(tubePts), 40, 0.035, 10), MAT.gloss(0xc2410c)));
  const tap = new THREE.Group(); tap.position.set(1.4, 0, -0.85);
  tap.add(mesh(new THREE.CylinderGeometry(0.07, 0.09, 0.32, 16), brass, [0, 0.16, 0]));
  const lever = new THREE.Group(); lever.position.y = 0.36;
  lever.add(mesh(new THREE.BoxGeometry(0.36, 0.035, 0.06), MAT.gloss(0x111827), [0.12, 0, 0]));
  tap.add(lever); g.add(tap);

  const top = 1.28;
  const outer = new THREE.Mesh(flameGeometry(0.11, 0.85), flameMaterial({ color: 0x3f6fe0, tip: 0x7c3aed, alpha: 0.32, height: 0.85, wobble: 0.012, seed: 1 }));
  const inner = new THREE.Mesh(flameGeometry(0.055, 0.3), flameMaterial({ color: 0x9ccaff, tip: 0x60a5fa, alpha: 0.75, height: 0.3, wobble: 0.003, seed: 2 }));
  const lumi = new THREE.Mesh(flameGeometry(0.15, 1.5), flameMaterial({ color: 0xffb02e, tip: 0xffe08a, alpha: 0.85, height: 1.5, wobble: 0.06, seed: 3 }));
  const tint = new THREE.Mesh(flameGeometry(0.15, 1.1), flameMaterial({ color: 0xffffff, alpha: 0, height: 1.1, wobble: 0.035, seed: 4 }));
  [outer, inner, lumi, tint].forEach((m, i) => { m.position.y = top; m.renderOrder = 8 + i; m.userData.noPick = true; m.visible = false; g.add(m); });
  inner.renderOrder = 12;
  const light = quality && quality.tier !== 'low' ? new THREE.PointLight(0xffa040, 0, 3.5, 2) : null;
  if (light) { light.position.y = top + 0.5; g.add(light); }

  let gas = 0; let air = 0; let lit = false; let emis = 0;
  const emisCol = new THREE.Color();
  const api = {
    group: g, collar, tap, lever, barrel, top,
    get lit() { return lit; }, get gas() { return gas; }, get air() { return air; },
    setGas(v) { gas = v; lever.rotation.y = -v * Math.PI / 2; if (gas <= 0) lit = false; },
    setAir(v) { air = Math.max(0, Math.min(1, v)); collar.rotation.y = air * Math.PI * 0.5; },
    light() { if (gas > 0) lit = true; return lit; },
    /** Colour and strength (0..1) of what is burning in the flame. */
    setEmission(col, k) { emisCol.copy(col); emis = k; },
    /** Hottest point of the flame, just above the inner cone, in the burner's frame. */
    hotY() { return top + (air > 0.5 ? 0.38 : 0.6); },
    update(dt, t) {
      const on = lit && gas > 0; const blue = on ? Math.min(1, air * 1.6) : 0;
      outer.visible = inner.visible = on && blue > 0.05; lumi.visible = on && blue < 0.95; tint.visible = on && emis > 0.01;
      for (const m of [outer, inner, lumi, tint]) { if (m.visible) m.material.uniforms.uTime.value = t; }
      outer.material.uniforms.uAlpha.value = 0.34 * blue; inner.material.uniforms.uAlpha.value = 0.75 * blue;
      lumi.material.uniforms.uAlpha.value = 0.85 * (1 - blue);
      lumi.scale.set(1, 1 - 0.3 * blue, 1);
      if (tint.visible) { tint.material.uniforms.uColor.value.copy(emisCol); tint.material.uniforms.uTip.value.copy(emisCol); tint.material.uniforms.uAlpha.value = Math.min(0.9, emis * 0.95); tint.scale.set(1 + emis * 0.25, 0.8 + emis * 0.5, 1 + emis * 0.25); }
      if (light) {
        if (!on) light.intensity = 0;
        else if (emis > 0.02) { light.color.copy(emisCol); light.intensity = 0.6 + emis * 2.6 + Math.sin(t * 31) * 0.1; }
        else { light.color.setHex(blue > 0.5 ? 0x7aa2ff : 0xffa040); light.intensity = (blue > 0.5 ? 0.25 : 1.1) + Math.sin(t * 27) * 0.06; }
      }
    },
  };
  return api;
}
