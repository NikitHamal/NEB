/* Pathways: schematic Nepal map. District centres as [lon, lat] and a rough outline; not a survey map.
   Same points as PwMap.kt on Android. PW.map(counts, selected, onPick) returns an SVG element. */
(function () {
  'use strict';
  var PW = window.PW;
  var P = {"Baglung": [83.60, 28.27], "Banke": [81.62, 28.05], "Bhaktapur": [85.43, 27.67], "Bhojpur": [87.05, 27.17], "Chitwan": [84.43, 27.53], "Dadeldhura": [80.58, 29.30], "Dang": [82.30, 28.10], "Dhankuta": [87.34, 26.98], "Dhanusha": [85.95, 26.85], "Dolakha": [86.07, 27.70], "Doti": [80.98, 29.25], "Gorkha": [84.63, 28.00], "Ilam": [87.93, 26.91], "Jhapa": [87.89, 26.62], "Jumla": [82.18, 29.27], "Kailali": [80.95, 28.75], "Kanchanpur": [80.35, 28.85], "Kaski": [84.00, 28.25], "Kathmandu": [85.32, 27.71], "Kavrepalanchok": [85.55, 27.55], "Lalitpur": [85.32, 27.55], "Lamjung": [84.38, 28.25], "Makwanpur": [85.05, 27.42], "Morang": [87.45, 26.65], "Nawalparasi East": [84.10, 27.55], "Palpa": [83.55, 27.87], "Parsa": [84.85, 27.10], "Rupandehi": [83.45, 27.55], "Saptari": [86.75, 26.62], "Siraha": [86.20, 26.65], "Sunsari": [87.20, 26.67], "Surkhet": [81.62, 28.60], "Tanahu": [84.25, 27.95], "Achham": [81.25, 29.05], "Arghakhanchi": [83.15, 27.95], "Baitadi": [80.45, 29.52], "Bajhang": [81.20, 29.55], "Bajura": [81.50, 29.45], "Bara": [85.05, 27.00], "Bardiya": [81.45, 28.35], "Dailekh": [81.70, 28.85], "Darchula": [80.55, 29.85], "Dhading": [84.90, 27.90], "Dolpa": [82.90, 29.00], "Gulmi": [83.30, 28.05], "Humla": [81.85, 29.97], "Jajarkot": [82.20, 28.70], "Kalikot": [81.85, 29.15], "Kapilvastu": [83.00, 27.55], "Khotang": [86.80, 27.20], "Mahottari": [85.80, 26.95], "Manang": [84.15, 28.65], "Mugu": [82.20, 29.55], "Mustang": [83.85, 28.95], "Myagdi": [83.40, 28.45], "Nawalparasi West": [83.65, 27.60], "Nuwakot": [85.15, 27.90], "Okhaldhunga": [86.50, 27.30], "Panchthar": [87.80, 27.15], "Parbat": [83.70, 28.20], "Pyuthan": [82.85, 28.10], "Ramechhap": [86.10, 27.35], "Rasuwa": [85.30, 28.20], "Rautahat": [85.30, 26.95], "Rolpa": [82.65, 28.35], "Rukum East": [82.65, 28.60], "Rukum West": [82.20, 28.60], "Salyan": [82.15, 28.35], "Sankhuwasabha": [87.25, 27.40], "Sarlahi": [85.55, 27.00], "Sindhuli": [85.95, 27.25], "Sindhupalchok": [85.70, 27.95], "Solukhumbu": [86.65, 27.70], "Syangja": [83.85, 28.00], "Taplejung": [87.65, 27.55], "Terhathum": [87.55, 27.12], "Udayapur": [86.55, 26.95]};
  var O = [[80.06, 28.83], [80.25, 29.15], [80.55, 29.30], [80.95, 29.70], [81.10, 30.15], [81.60, 30.35], [82.10, 30.35], [82.70, 29.95], [83.35, 29.45], [84.05, 29.25], [84.20, 28.90], [84.65, 28.65], [85.15, 28.30], [85.75, 28.25], [86.00, 27.95], [86.60, 28.10], [87.10, 27.85], [87.80, 27.95], [88.15, 27.90], [88.05, 27.45], [88.15, 26.45], [87.50, 26.40], [86.75, 26.45], [86.00, 26.65], [85.25, 26.75], [84.65, 27.05], [84.20, 27.40], [83.40, 27.45], [82.70, 27.70], [82.00, 28.00], [81.50, 28.30], [80.80, 28.65]];
  var L0 = 79.9, L1 = 88.3, A0 = 26.3, A1 = 30.5, W = 840, H = 420, PAD = 24;
  function x(lon) { return PAD + (lon - L0) / (L1 - L0) * (W - 2 * PAD); }
  function y(lat) { return PAD + (A1 - lat) / (A1 - A0) * (H - 2 * PAD); }
  var NS = 'http://www.w3.org/2000/svg';
  function s(tag, a) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); return e; }
  PW.map = function (counts, selected, onPick) {
    var svg = s('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'pw-map', role: 'img', 'aria-label': 'Map of Nepal with colleges by district' });
    svg.appendChild(s('path', { d: 'M' + O.map(function (p) { return x(p[0]).toFixed(1) + ' ' + y(p[1]).toFixed(1); }).join('L') + 'Z', class: 'pw-land' }));
    Object.keys(P).forEach(function (d) {
      var n = counts[d] || 0, on = d === selected;
      if (!n && !on) { svg.appendChild(s('circle', { cx: x(P[d][0]), cy: y(P[d][1]), r: 2.4, class: 'pw-dot off' })); return; }
      var g = s('g', { class: 'pw-pin' + (on ? ' on' : ''), tabindex: 0, role: 'button', 'aria-label': d + ', ' + n + ' listed' });
      g.appendChild(s('circle', { cx: x(P[d][0]), cy: y(P[d][1]), r: on ? 11 : Math.min(9, 4 + n * 0.7), class: 'pw-dot' }));
      g.addEventListener('click', function () { onPick(on ? '' : d); });
      g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onPick(on ? '' : d); } });
      var t = s('title', {}); t.textContent = d + ' (' + n + ')'; g.appendChild(t);
      svg.appendChild(g);
    });
    return svg;
  };
})();
