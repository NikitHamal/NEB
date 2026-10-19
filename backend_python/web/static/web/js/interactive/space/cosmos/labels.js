import { THREE } from '../../core/engine.js';

const CSS = `
.cz-labels{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:2;font-family:Poppins,system-ui,sans-serif}
.cz-label{position:absolute;left:0;top:0;display:flex;align-items:flex-start;gap:7px;white-space:nowrap;will-change:transform,opacity;transition:none}
.cz-label>span{background:rgba(6,10,22,.42);padding:2px 8px 3px;border-radius:9px;backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px)}
.cz-label i{width:7px;height:7px;border-radius:50%;margin-top:5px;flex:none;border:1.5px solid rgba(255,255,255,.9);box-shadow:0 0 8px rgba(160,200,255,.8)}
.cz-label b{display:block;font-weight:600;font-size:12.5px;color:#f4f7ff;text-shadow:0 1px 3px rgba(0,0,0,.9),0 0 10px rgba(0,0,0,.6);letter-spacing:.01em}
.cz-label small{display:block;font-size:10.5px;color:rgba(214,226,255,.78);text-shadow:0 1px 3px rgba(0,0,0,.9)}
.cz-label.flip{flex-direction:row-reverse;text-align:right}
.cz-label.here i{background:#ffd27a;border-color:#ffe7b0;box-shadow:0 0 10px #ffc04a}
.cz-label.here b{color:#ffe2a3}
.cz-label.minor b{font-weight:500;font-size:11px;color:rgba(230,238,255,.85)}
.cz-label.minor small{display:none}
.cz-hud-pow{position:absolute;right:16px;top:12px;z-index:3;pointer-events:none;text-align:right;font-family:Poppins,system-ui,sans-serif;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.7)}
.cz-hud-pow b{display:block;font-size:34px;font-weight:700;letter-spacing:-.02em;line-height:1}
.cz-hud-pow small{display:block;font-size:12px;opacity:.82;margin-top:4px}
.cz-scalebar{position:absolute;left:16px;bottom:14px;z-index:3;pointer-events:none;font:600 11px Poppins,system-ui,sans-serif;color:#e8eeff;text-shadow:0 1px 3px #000}
.cz-scalebar span{display:block;height:6px;border:1.5px solid rgba(255,255,255,.9);border-top:0;margin-bottom:4px}
.cz-caption{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);z-index:3;max-width:min(560px,86%);pointer-events:none;text-align:center;font:500 13px/1.45 Poppins,system-ui,sans-serif;color:#f1f5ff;background:rgba(8,12,24,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:9px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.12);opacity:0;transition:opacity .5s}
.cz-caption.on{opacity:1}
.cz-loading{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:4;font:500 13px Poppins,system-ui,sans-serif;color:#dbe6ff;background:rgba(8,12,24,.6);padding:8px 14px;border-radius:999px;pointer-events:none;transition:opacity .4s}
@media (max-width:640px){.cz-hud-pow b{font-size:24px}.cz-label b{font-size:11.5px}.cz-label small{font-size:9.5px}.cz-caption{font-size:12px;bottom:40px}}
`;

let styled = false;

export function createLabels(stage) {
  if (!styled) {
    const s = document.createElement('style');
    s.textContent = CSS;
    document.head.appendChild(s);
    styled = true;
  }
  const root = document.createElement('div');
  root.className = 'cz-labels';
  stage.appendChild(root);
  const items = [];
  const v = new THREE.Vector3();
  let enabled = true;

  function add(layer, def) {
    const el = document.createElement('div');
    el.className = `cz-label ${def.cls || ''} ${def.minor ? 'minor' : ''}`;
    el.innerHTML = `<i></i><span><b></b>${def.sub ? '<small></small>' : ''}</span>`;
    el.querySelector('b').textContent = def.text;
    if (def.sub) el.querySelector('small').textContent = def.sub;
    el.style.opacity = '0';
    root.appendChild(el);
    items.push({ layer, def, el, shown: false, w: Math.max(def.text.length, def.minor ? 0 : (def.sub || '').length * 0.82) * 7 + 22 });
  }

  function update(camera, logW, width, height) {
    const placed = [];
    const phone = width < 640;
    const order = items.slice().sort((a, b) => (a.def.minor ? 1 : 0) - (b.def.minor ? 1 : 0) || (a.def.cls === 'here' ? -1 : 0));
    for (const it of order) {
      const { def } = it;
      let a = enabled && it.layer.group.visible && it.layer.alpha > 0.05 ? 1 : 0;
      if (a) a = Math.min(1, (logW - def.min) / 0.35, (def.max - logW) / 0.35);
      if (a > 0 && phone && def.minor) a = 0;
      if (a > 0.02) {
        def.get(v);
        it.layer.group.localToWorld(v);
        v.project(camera);
        if (v.z > 1 || v.z < -1) a = 0;
        const x = (v.x * 0.5 + 0.5) * width;
        const y = (-v.y * 0.5 + 0.5) * height;
        if (x < -20 || y < -20 || x > width + 20 || y > height + 20) a = 0;
        if (a > 0.02) {
          const flip = x + it.w > width - 8;
          const left = flip ? x - it.w + 4 : x - 4;
          const box = [left, y - 8, left + it.w, y + 26];
          if (placed.some((p) => box[0] < p[2] && box[2] > p[0] && box[1] < p[3] && box[3] > p[1])) a = 0;
          else {
            placed.push(box);
            if (flip !== it.flip) { it.flip = flip; it.el.classList.toggle('flip', flip); }
            it.el.style.transform = `translate(${left.toFixed(1)}px,${(y - 9).toFixed(1)}px)`;
          }
        }
      }
      a = Math.max(0, a) * it.layer.alpha;
      if (a > 0.02 || it.shown) {
        it.el.style.opacity = a.toFixed(2);
        it.shown = a > 0.02;
        it.el.style.visibility = it.shown ? 'visible' : 'hidden';
      }
    }
  }

  return {
    root,
    add,
    update,
    set enabled(b) { enabled = b; },
    get enabled() { return enabled; },
    dispose() { root.remove(); },
  };
}

export function hudElement(stage, cls, html = '') {
  const el = document.createElement('div');
  el.className = cls;
  el.innerHTML = html;
  stage.appendChild(el);
  return el;
}
