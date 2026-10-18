// Camera rig and pointer input. The camera flies between authored shots (a slow arc about the
// subject, eased), and the student can lean the view a little with a drag, a pinch or the wheel.
// Pointer presses go first to the current step (cutting, picking, pinning); a press the step
// does not want becomes a camera drag. Mouse, pen and touch share one code path.
import { THREE } from '../engine.js';
import { clamp, ease } from './kit.js';

export function createRig(camera) {
  const target = new THREE.Vector3(0, 1, 0);
  const sph = new THREE.Spherical(6, 1, 0);
  const from = { t: new THREE.Vector3(), s: new THREE.Spherical() };
  const to = { t: new THREE.Vector3(), s: new THREE.Spherical() };
  const tmp = new THREE.Vector3();
  let k = 1; let dur = 1; let fovFrom = camera.fov; let fovTo = camera.fov;
  let yaw = 0; let pitch = 0; let zoom = 1;
  let yawGoal = 0; let pitchGoal = 0; let zoomGoal = 1;
  const lim = { yaw: 0.7, pitch: 0.38, zMin: 0.55, zMax: 1.6 };
  return {
    target,
    go(shot, seconds = 1.3) {
      from.t.copy(target);
      tmp.copy(camera.position).sub(target); from.s.setFromVector3(tmp);
      to.t.set(shot.target[0], shot.target[1], shot.target[2]);
      tmp.set(shot.pos[0], shot.pos[1], shot.pos[2]).sub(to.t); to.s.setFromVector3(tmp);
      if (shot.fit) {
        const vf = THREE.MathUtils.degToRad(shot.fov || camera.fov);
        const hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
        const need = Math.max(shot.fit / 2 / Math.tan(hf / 2), (shot.fitH || 0) / 2 / Math.tan(vf / 2));
        to.s.radius = Math.max(to.s.radius, need * 1.08);
      }
      let dth = to.s.theta - from.s.theta; if (dth > Math.PI) dth -= Math.PI * 2; if (dth < -Math.PI) dth += Math.PI * 2;
      to.s.theta = from.s.theta + dth;
      fovFrom = camera.fov; fovTo = shot.fov || fovFrom;
      if (shot.limits) Object.assign(lim, shot.limits); else Object.assign(lim, { yaw: 0.7, pitch: 0.38, zMin: 0.55, zMax: 1.6 });
      yaw = yawGoal = pitch = pitchGoal = 0; zoom = zoomGoal = 1;
      dur = seconds; k = seconds <= 0 ? 1 : 0;
      if (k === 1) { target.copy(to.t); sph.copy(to.s); camera.fov = fovTo; camera.updateProjectionMatrix(); }
    },
    orbit(dx, dy) { yawGoal = clamp(yawGoal - dx * 0.006, -lim.yaw, lim.yaw); pitchGoal = clamp(pitchGoal - dy * 0.005, -lim.pitch, lim.pitch); },
    zoomBy(f) { zoomGoal = clamp(zoomGoal * f, lim.zMin, lim.zMax); },
    resetLean() { yawGoal = 0; pitchGoal = 0; zoomGoal = 1; },
    get moving() { return k < 1; },
    get lean() { return [yaw, pitch, zoom, sph.theta, sph.phi, sph.radius]; },
    update(dt) {
      if (k < 1) {
        k = Math.min(1, k + dt / dur);
        const e = ease.inOut(k);
        target.lerpVectors(from.t, to.t, e);
        sph.radius = from.s.radius + (to.s.radius - from.s.radius) * e;
        sph.phi = from.s.phi + (to.s.phi - from.s.phi) * e;
        sph.theta = from.s.theta + (to.s.theta - from.s.theta) * e;
        if (fovTo !== fovFrom) { camera.fov = fovFrom + (fovTo - fovFrom) * e; camera.updateProjectionMatrix(); }
      }
      const a = 1 - Math.pow(0.0015, dt);
      yaw += (yawGoal - yaw) * a; pitch += (pitchGoal - pitch) * a; zoom += (zoomGoal - zoom) * a;
      tmp.setFromSphericalCoords(sph.radius * zoom, clamp(sph.phi + pitch, 0.05, Math.PI - 0.05), sph.theta + yaw);
      camera.position.copy(target).add(tmp);
      camera.lookAt(target);
    },
  };
}

export function createInput(dom, camera, rig) {
  const raycaster = new THREE.Raycaster();
  const hits = [];
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const ptr = {
    x: 0, y: 0, ndc: new THREE.Vector2(), down: false, touch: false, inside: false, sx: 0, sy: 0, moved: 0, id: -1,
    ray: raycaster.ray, time: 0,
  };
  let handler = null;
  let captured = false;
  let orbiting = false;
  const pointers = new Map();
  let pinch = 0;

  function setFrom(e) {
    const r = dom.getBoundingClientRect();
    ptr.x = e.clientX - r.left; ptr.y = e.clientY - r.top;
    ptr.ndc.set((ptr.x / r.width) * 2 - 1, -(ptr.y / r.height) * 2 + 1);
    raycaster.setFromCamera(ptr.ndc, camera);
    ptr.touch = e.pointerType === 'touch';
  }
  function down(e) {
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 2) {
      if (captured && handler && handler.cancel) handler.cancel(ptr);
      captured = false; orbiting = true;
      const p = [...pointers.values()]; pinch = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      return;
    }
    if (pointers.size > 2) return;
    setFrom(e);
    dom.setPointerCapture && dom.setPointerCapture(e.pointerId);
    ptr.down = true; ptr.inside = true; ptr.id = e.pointerId; ptr.sx = ptr.x; ptr.sy = ptr.y; ptr.moved = 0; ptr.time = performance.now();
    captured = !!(handler && handler.down && handler.down(ptr, e.button));
    orbiting = !captured;
    e.preventDefault();
  }
  function move(e) {
    if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 2) {
      const p = [...pointers.values()]; const d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
      if (pinch > 0 && d > 0) rig.zoomBy(pinch / d);
      pinch = d; return;
    }
    const px = ptr.x; const py = ptr.y;
    setFrom(e); ptr.inside = true;
    if (ptr.down && e.pointerId === ptr.id) {
      ptr.moved += Math.hypot(ptr.x - px, ptr.y - py);
      if (captured) { if (handler && handler.move) handler.move(ptr); }
      else if (orbiting) rig.orbit(ptr.x - px, ptr.y - py);
    } else if (!ptr.down && handler && handler.hover) handler.hover(ptr);
  }
  function up(e) {
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinch = 0;
    if (e.pointerId !== ptr.id) return;
    setFrom(e);
    ptr.down = false;
    if (captured && handler && handler.up) handler.up(ptr);
    else if (!captured && ptr.moved < 8 && handler && handler.tap) handler.tap(ptr);
    captured = false; orbiting = false;
    if (ptr.touch) ptr.inside = false;
  }
  function leave(e) { if (e.pointerType !== 'touch' && !ptr.down) { ptr.inside = false; if (handler && handler.hover) handler.hover(ptr); } }
  function wheel(e) { e.preventDefault(); rig.zoomBy(e.deltaY > 0 ? 1.08 : 0.92); }
  function ctxmenu(e) { e.preventDefault(); }
  dom.style.touchAction = 'none';
  dom.addEventListener('pointerdown', down);
  dom.addEventListener('pointermove', move);
  dom.addEventListener('pointerup', up);
  dom.addEventListener('pointercancel', up);
  dom.addEventListener('pointerleave', leave);
  dom.addEventListener('wheel', wheel, { passive: false });
  dom.addEventListener('contextmenu', ctxmenu);

  return {
    ptr,
    setHandler(h) { if (captured && handler && handler.cancel) handler.cancel(ptr); handler = h; captured = false; },
    /** First hit among objects (recursive), or null. Reuses one array. */
    pick(objects, recursive = true) {
      hits.length = 0;
      raycaster.intersectObjects(objects, recursive, hits);
      for (let i = 0; i < hits.length; i++) if (hits[i].object.visible !== false && !hits[i].object.userData.noPick) return hits[i];
      return null;
    },
    planePoint(y, out) { plane.constant = -y; return raycaster.ray.intersectPlane(plane, out); },
    /** Projects a world point to stage pixels (out.x, out.y). */
    project(v, out, w, h) { out.copy(v).project(camera); out.x = (out.x + 1) / 2 * w; out.y = (1 - out.y) / 2 * h; return out; },
    dispose() {
      dom.removeEventListener('pointerdown', down); dom.removeEventListener('pointermove', move); dom.removeEventListener('pointerup', up);
      dom.removeEventListener('pointercancel', up); dom.removeEventListener('pointerleave', leave); dom.removeEventListener('wheel', wheel); dom.removeEventListener('contextmenu', ctxmenu);
    },
  };
}
