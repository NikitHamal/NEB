// Reading a scale the way a student does: a red hairline the student drags to where they judge
// the bottom of the meniscus to be, with a magnified readout of the value it stands on. The
// student's value is recorded as read, right or wrong, and compared with the truth.
import { THREE } from '../engine.js';
import { BURETTE } from './glass.js';

export function createReadingTool(ctx, hud, bur, burY) {
  const line = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.0016, 0.002), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false, transparent: true }));
  line.renderOrder = 20; line.visible = false; line.userData.noPick = true;
  ctx.world.add(line);
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
  const hit = new THREE.Vector3();
  let chip = null; let cb = null; let localY = 0; let active = false;
  const valueAt = (y) => Math.round(bur.readingAtY(y) * 20) / 20;
  function place(y) {
    localY = Math.max(BURETTE.zeroY - BURETTE.len - 0.05, Math.min(BURETTE.zeroY + 0.05, y));
    line.position.set(0, burY + localY, BURETTE.r + 0.03);
    const v = valueAt(localY);
    chip.at.set(0.12, ctx.BENCH_Y + burY + localY, 0); chip.set(`<b>${v.toFixed(2)}</b> mL`);
  }
  function fromPointer() {
    if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return;
    place(hit.y - ctx.BENCH_Y - burY);
  }
  return {
    start(onRecord) {
      cb = onRecord; active = true;
      chip = hud.chip('ho-chip-read').show(true); chip.dx = 14; chip.dy = -14;
      line.visible = true;
      place(bur.yOf(bur.reading) + (Math.random() < 0.5 ? -1 : 1) * (0.03 + Math.random() * 0.04));
      hud.actions([{ id: 'rec', label: 'Record reading', primary: true, onClick: () => { if (!active) return; const v = valueAt(localY); active = false; hud.actions([]); cb(v, bur.reading); } }]);
    },
    stop() { active = false; line.visible = false; if (chip) { chip.remove(); chip = null; } hud.actions([]); },
    handler: {
      down() { if (!active) return false; fromPointer(); return true; },
      move() { if (active) fromPointer(); },
      up() {},
      cancel() {},
    },
    dispose() { ctx.world.remove(line); line.geometry.dispose(); line.material.dispose(); },
  };
}
