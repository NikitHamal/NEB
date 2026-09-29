import { el } from './dom.js';

const NAMES = { darkGrad: 'dark', innerGrad: 'inner', lightGrad: 'light', frontGrad: 'front', frontShadowGrad: 'shadow' };
let instance = 0;

export function buildLogo(S, svgText, height) {
  instance += 1;
  const doc = new DOMParser().parseFromString(svgText, 'image/svg+xml');
  const source = doc.documentElement;
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('xmlns', ns);
  svg.style.cssText = 'position:absolute;left:0;top:0;overflow:visible';
  const defs = source.querySelector('defs');
  const renamed = new Map();
  if (defs) {
    const copy = document.importNode(defs, true);
    copy.querySelectorAll('[id]').forEach((node) => {
      const next = `${node.id}-${instance}`;
      renamed.set(node.id, next);
      node.id = next;
    });
    svg.append(copy);
  }

  const filled = [...source.querySelectorAll('path')].filter((p) => (p.getAttribute('fill') ?? '').startsWith('url('));
  const holder = document.createElementNS(ns, 'g');
  svg.append(holder);
  const facets = {};
  const pieces = filled.length ? filled : [...source.querySelectorAll('path')];
  pieces.forEach((path, i) => {
    const id = (path.getAttribute('fill') ?? '').match(/#(\w+)/)?.[1];
    const name = NAMES[id] ?? `piece${i}`;
    const g = document.createElementNS(ns, 'g');
    g.style.transformBox = 'fill-box';
    g.style.transformOrigin = '50% 50%';
    const copy = document.importNode(path, true);
    for (const attr of ['fill', 'stroke']) {
      const value = copy.getAttribute(attr) ?? '';
      if (value.startsWith('url(')) copy.setAttribute(attr, value.replace(/#([\w-]+)/, (m, ref) => `#${renamed.get(ref) ?? ref}`));
    }
    g.append(copy);
    holder.append(g);
    facets[name] = g;
  });

  const probe = el('div', { style: 'position:absolute;left:-9999px;top:0;width:10px;height:10px' });
  probe.append(svg);
  document.body.append(probe);
  const box = holder.getBBox();
  const pad = 6;
  svg.setAttribute('viewBox', `${box.x - pad} ${box.y - pad} ${box.width + pad * 2} ${box.height + pad * 2}`);
  const ratio = (box.width + pad * 2) / (box.height + pad * 2);
  svg.setAttribute('width', height * ratio);
  svg.setAttribute('height', height);
  probe.remove();

  return { svg, facets, width: height * ratio, height, unit: (box.height + pad * 2) / height, box };
}
