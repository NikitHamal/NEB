// The hand lens: a real second view. While the lens is in hand, a small camera looks straight
// down through it and its picture is drawn on the glass, magnified about three times, so the
// student sees the specimen enlarged under the lens the way a lens actually shows it. Low-tier
// devices render the lens view at quarter size and every other frame.
import { THREE } from '../engine.js';

export function createLens(ctx, opts = {}) {
  const { engine, scene, tools, camera } = ctx;
  const low = ctx.low;
  const size = low ? 256 : 512;
  const rt = new THREE.WebGLRenderTarget(size, size, { samples: low ? 0 : 2 });
  if (rt.texture.colorSpace !== undefined) rt.texture.colorSpace = THREE.SRGBColorSpace;
  const cam = new THREE.PerspectiveCamera(20, 1, 0.005, 20);
  const mag = opts.mag || 3;
  const back = new THREE.Vector3(); const tmp = new THREE.Vector3();
  void camera;
  let frame = 0;
  const lensMat = new THREE.MeshBasicMaterial({ map: rt.texture, toneMapped: false });
  return {
    get active() { return tools.id === 'lens' && tools.holder.visible; },
    update() {
      if (tools.id !== 'lens' || !tools.holder.visible || !tools.model) return;
      const glass = tools.model.userData.glass;
      if (glass.material !== lensMat) glass.material = lensMat;
      frame += 1; if (low && frame % 2) return;
      const tip = tools.holder.position;
      const height = opts.height || 0.25;
      const radius = 0.29 * tools.holder.scale.x;
      cam.position.set(tip.x, tip.y + height * 0.2, tip.z);
      back.set(camera.matrixWorld.elements[8], 0, camera.matrixWorld.elements[10]).normalize();
      cam.up.copy(back).negate();
      tmp.set(tip.x, tip.y - 1, tip.z);
      cam.lookAt(tmp);
      const dist = tip.y + height * 0.2 - (opts.groundY ?? 0.85);
      cam.fov = THREE.MathUtils.radToDeg(2 * Math.atan((radius / mag) / Math.max(0.02, dist)));
      cam.updateProjectionMatrix();
      const vis = tools.holder.visible; tools.holder.visible = false;
      const r = engine.renderer; const prev = r.getRenderTarget();
      r.setRenderTarget(rt); r.render(scene, cam); r.setRenderTarget(prev);
      tools.holder.visible = vis;
    },
    dispose() { rt.dispose(); lensMat.dispose(); },
  };
}
