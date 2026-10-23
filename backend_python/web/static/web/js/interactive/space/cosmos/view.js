import { THREE } from '../../core/engine.js';
import { smooth } from './astro.js';

export const MIN_LOG = -0.3;
export const MAX_LOG = 27.35;

export function viewQuaternion(up, front) {
  const u = up.clone().normalize();
  const f = front.clone().addScaledVector(u, -u.dot(front)).normalize();
  const r = new THREE.Vector3().crossVectors(u, f).normalize();
  const m = new THREE.Matrix4().makeBasis(r, u, f);
  return new THREE.Quaternion().setFromRotationMatrix(m).invert();
}

export function keyframed(keys, logW, mix) {
  if (logW <= keys[0].log) return keys[0].value;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i]; const b = keys[i + 1];
    if (logW <= b.log) return mix(a.value, b.value, smooth(a.log, b.log, logW));
  }
  return keys[keys.length - 1].value;
}

export function createRig(dom, opts = {}) {
  let logW = opts.start ?? 0.2;
  let target = logW;
  let yaw = 0; let pitch = 0;
  let yawGoal = 0; let pitchGoal = 0;
  const pointers = new Map();
  let pinch = 0;
  let interacted = () => {};
  let autoYaw = opts.autoYaw ?? 0.02;

  function clampT() { target = Math.min(MAX_LOG, Math.max(MIN_LOG, target)); }
  function down(e) {
    dom.setPointerCapture && dom.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 2) { const p = [...pointers.values()]; pinch = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y); }
    interacted('drag');
  }
  function move(e) {
    const prev = pointers.get(e.pointerId);
    if (!prev) return;
    const dx = e.clientX - prev.x; const dy = e.clientY - prev.y;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 1) {
      yawGoal -= dx * 0.006;
      pitchGoal = Math.min(1.35, Math.max(-1.35, pitchGoal + dy * 0.005));
    } else if (pointers.size === 2) {
      const p = [...pointers.values()];
      const d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      if (pinch > 0) { target -= Math.log10(d / pinch) * 1.6; clampT(); interacted('zoom'); }
      pinch = d;
    }
  }
  function up(e) { pointers.delete(e.pointerId); pinch = 0; }
  function wheel(e) {
    e.preventDefault();
    const dy = e.deltaMode === 1 ? e.deltaY * 30 : e.deltaY;
    target += Math.max(-0.6, Math.min(0.6, dy * 0.0028));
    clampT();
    interacted('zoom');
  }
  function key(e) {
    if (e.key === '+' || e.key === '=') { target -= 0.5; clampT(); interacted('zoom'); }
    if (e.key === '-' || e.key === '_') { target += 0.5; clampT(); interacted('zoom'); }
  }
  dom.style.touchAction = 'none';
  dom.tabIndex = 0;
  dom.addEventListener('pointerdown', down);
  dom.addEventListener('pointermove', move);
  dom.addEventListener('pointerup', up);
  dom.addEventListener('pointercancel', up);
  dom.addEventListener('wheel', wheel, { passive: false });
  dom.addEventListener('keydown', key);

  return {
    get logW() { return logW; },
    get target() { return target; },
    set target(v) { target = v; clampT(); },
    jump(v) { target = v; clampT(); },
    snap(v) { target = v; logW = v; clampT(); },
    onInteract(fn) { interacted = fn; },
    setAutoYaw(v) { autoYaw = v; },
    resetOrbit() { yawGoal = 0; pitchGoal = 0; },
    update(dt) {
      const gap = target - logW;
      const rate = Math.abs(gap) > 4 ? 2.2 : 3.4;
      logW += gap * (1 - Math.exp(-dt * rate));
      if (Math.abs(gap) < 1e-4) logW = target;
      yawGoal += autoYaw * dt;
      const k = 1 - Math.exp(-dt * 8);
      yaw += (yawGoal - yaw) * k;
      pitch += (pitchGoal - pitch) * k;
      return logW;
    },
    orbit() { return { yaw, pitch }; },
    dispose() {
      dom.removeEventListener('pointerdown', down);
      dom.removeEventListener('pointermove', move);
      dom.removeEventListener('pointerup', up);
      dom.removeEventListener('pointercancel', up);
      dom.removeEventListener('wheel', wheel);
      dom.removeEventListener('keydown', key);
    },
  };
}
