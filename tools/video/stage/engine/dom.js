import { round } from './math.js';

const SVG_NS = 'http://www.w3.org/2000/svg';

function decorate(node, props, children) {
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === 'class') node.setAttribute('class', value);
    else if (key === 'style') {
      if (typeof value === 'string') node.style.cssText = value;
      else {
        for (const [name, v] of Object.entries(value)) {
          if (name.startsWith('--')) node.style.setProperty(name, v);
          else node.style[name] = v;
        }
      }
    } else if (key === 'text') node.textContent = value;
    else if (key === 'html') node.innerHTML = value;
    else node.setAttribute(key, value === true ? '' : value);
  }
  for (const child of [children].flat()) {
    if (child === undefined || child === null || child === false) continue;
    node.append(typeof child === 'string' || typeof child === 'number' ? document.createTextNode(String(child)) : child);
  }
  return node;
}

export const el = (tag, props = {}, children = []) => decorate(document.createElement(tag), props, children);
export const svg = (tag, props = {}, children = []) => decorate(document.createElementNS(SVG_NS, tag), props, children);
export const icon = (name, props = {}) => el('span', { ...props, class: `icon ${props.class ?? ''}`.trim(), text: name });

export function place(node, p) {
  const { x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s = 1, sx = s, sy = s, o, cx = false, skx = 0 } = p;
  let tf = cx ? 'translate(-50%,-50%) ' : '';
  if (z || rx || ry) tf += `translate3d(${round(x)}px,${round(y)}px,${round(z)}px)`;
  else tf += `translate(${round(x)}px,${round(y)}px)`;
  if (rx) tf += ` rotateX(${round(rx)}deg)`;
  if (ry) tf += ` rotateY(${round(ry)}deg)`;
  if (rz) tf += ` rotate(${round(rz)}deg)`;
  if (skx) tf += ` skewX(${round(skx)}deg)`;
  if (sx !== 1 || sy !== 1) tf += ` scale(${round(sx, 4)},${round(sy, 4)})`;
  if (node._tf !== tf) {
    node.style.transform = tf;
    node._tf = tf;
  }
  if (o !== undefined) {
    const v = round(o, 3);
    if (node._o !== v) {
      node.style.opacity = v;
      node._o = v;
    }
  }
}

export function show(node, on) {
  const v = on ? '' : 'none';
  if (node._d !== v) {
    node.style.display = v;
    node._d = v;
  }
}

export function setStyle(node, name, value) {
  const key = `_s_${name}`;
  if (node[key] !== value) {
    node.style[name] = value;
    node[key] = value;
  }
}
