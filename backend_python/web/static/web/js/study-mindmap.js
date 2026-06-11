(function () {
  'use strict';

  var ESC_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (c) { return ESC_MAP[c]; });
  }
  function clamp(value, min, max) { return Math.max(min, Math.min(max, value)); }

  var LATEX_MAP = {'Delta':'Δ','alpha':'α','beta':'β','gamma':'γ','delta':'δ','epsilon':'ε','theta':'θ','lambda':'λ','sigma':'σ','omega':'ω','mu':'μ','nu':'ν','pi':'π','rho':'ρ','tau':'τ','phi':'φ','psi':'ψ','chi':'χ','kappa':'κ','xi':'ξ','zeta':'ζ','eta':'η','upsilon':'υ','varphi':'φ','varepsilon':'ε','vartheta':'ϑ','rightarrow':'→','leftarrow':'←','leftrightarrow':'↔','Rightarrow':'⇒','Leftarrow':'⇐','Leftrightarrow':'⇔','approx':'≈','neq':'≠','leq':'≤','geq':'≥','leqslant':'≤','geqslant':'≥','pm':'±','mp':'∓','times':'×','div':'÷','cdot':'·','partial':'∂','nabla':'∇','infty':'∞','sum':'∑','prod':'∏','int':'∫','circ':'∘','bullet':'•','oplus':'⊕','otimes':'⊗','perp':'⊥','parallel':'∥','angle':'∠','cong':'≅','sim':'∼','propto':'∝','equiv':'≡','subset':'⊂','supset':'⊃','subseteq':'⊆','supseteq':'⊇','cup':'∪','cap':'∩','in':'∈','notin':'∉','forall':'∀','exists':'∃','neg':'¬','land':'∧','lor':'∨','prime':'′','ell':'ℓ','Re':'ℜ','Im':'ℑ','aleph':'ℵ','hbar':'ℏ','top':'⊤','bot':'⊥','rightarrow':'→','leftarrow':'←','Rightarrow':'⇒','Leftarrow':'⇐','ldots':'…','cdots':'⋯','vdots':'⋮','ddots':'⋱'};
  function latexToText(s){
    if(!s) return s;
    s = s.replace(/\$+\$(.*?)\$\$+/g, '$1');
    s = s.replace(/\$([^$]+)\$/g, '$1');
    s = s.replace(/\\ce\{([^}]*)\}/g, function(m, inner){
      return inner.replace(/(\d+)/g, function(m,n){ return n; }).replace(/([A-Z][a-z]?)(\d*)/g, function(m, el, num){ return el + (num || ''); }).replace(/\^(\{[^}]*\}|.)/g, function(m, p){ return p.replace(/[{}]/g,''); }).replace(/_(\{[^}]*\}|.)/g, function(m, p){ return '₋' + p.replace(/[{}]/g,''); }).replace(/->/g,'→').replace(/\+/g,' + ').replace(/->/g,' → ');
    });
    s = s.replace(/\\([A-Za-z]+)(\{[^}]*\})?/g, function(m, cmd, arg){
      if(LATEX_MAP[cmd]) return LATEX_MAP[cmd];
      if(cmd==='mathrm'||cmd==='text'||cmd==='operatorname') return arg ? arg.replace(/[{}]/g,'') : cmd;
      return (arg || '').replace(/[{}]/g,'');
    });
    s = s.replace(/([A-Za-z])_([\d]+|[{}][^{}]*[{}])/g, function(m, base, sub){
      var s2 = sub.replace(/[{}]/g,'');
      var subMap = {'0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','eg':'ₑg','n':'ₙ','i':'ᵢ','j':'ⱼ','max':'ₘₐₓ'};
      return base + (subMap[s2] || '₍'+s2+'₎');
    });
    s = s.replace(/([A-Za-z])\^([\d]+|[{}][^{}]*[{}])/g, function(m, base, sup){
      var s2 = sup.replace(/[{}]/g,'');
      var supMap = {'2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','-':'⁻','+':'⁺','n':'ⁿ','i':'ⁱ'};
      return base + (supMap[s2] || '⁽'+s2+'⁾');
    });
    return s;
  }

  var TITLE_CHAR_W = 8.6;
  var NOTE_CHAR_W = 6.35;
  var MIN_NODE_W = 142;
  var MAX_NODE_W = 340;
  var PAD_X = 20;
  var PAD_Y = 13;
  var TITLE_LH = 20;
  var NOTE_LH = 15;
  var NOTE_GAP = 5;
  var INDICATOR_R = 12;
  var INDICATOR_GAP = 12;
  var COLUMN_GAP = 96;
  var ROW_GAP = 24;
  var ANIMATE_MS = 220;

  // Measure text with a canvas context for accurate widths (incl. Devanagari);
  // falls back to a per-character estimate if canvas is unavailable.
  var _measureCtx = null;
  function textWidth(text, charW) {
    var str = String(text || '');
    try {
      if (!_measureCtx) _measureCtx = document.createElement('canvas').getContext('2d');
      _measureCtx.font = (charW > 7 ? '600 14px ' : '400 11.5px ') + "'Poppins', 'Segoe UI', sans-serif";
      return _measureCtx.measureText(str).width;
    } catch (e) {
      return str.length * charW;
    }
  }

  function closestWithClass(target, className, stopAt) {
    var node = target;
    while (node && node !== stopAt) {
      if (node.classList && node.classList.contains(className)) return node;
      node = node.parentNode;
    }
    return node && node.classList && node.classList.contains(className) ? node : null;
  }

  function splitLongWord(word, maxChars) {
    var parts = [];
    var size = Math.max(4, maxChars - 1);
    for (var i = 0; i < word.length; i += size) parts.push(word.slice(i, i + size));
    return parts;
  }

  function trimLine(line, maxChars) {
    if (line.length <= maxChars) return line;
    return line.slice(0, Math.max(0, maxChars - 1)).replace(/[\s,;:.]+$/g, '') + '…';
  }

  function wrapText(text, maxChars, maxLines) {
    var raw = String(text || '').replace(/\s+/g, ' ').trim();
    if (!raw) return [];
    var words = [];
    raw.split(' ').forEach(function (word) {
      if (word.length > maxChars) words = words.concat(splitLongWord(word, maxChars));
      else words.push(word);
    });

    var lines = [];
    var current = '';
    var usedAll = true;
    for (var i = 0; i < words.length; i++) {
      var next = current ? current + ' ' + words[i] : words[i];
      if (next.length <= maxChars) {
        current = next;
      } else {
        if (current) lines.push(current);
        current = words[i];
        if (lines.length === maxLines) { usedAll = false; break; }
      }
    }
    if (usedAll && current) lines.push(current);
    if (lines.length > maxLines) {
      lines = lines.slice(0, maxLines);
      usedAll = false;
    }
    if (!usedAll || (current && words.length && lines.length === maxLines && words.indexOf(current) < words.length - 1)) {
      lines[lines.length - 1] = trimLine(lines[lines.length - 1], maxChars);
    }
    return lines.length ? lines : [trimLine(raw, maxChars)];
  }

  function flatten(map, collapsed) {
    var nodes = [];
    var edges = [];
    function walk(raw, parentId, depth, path) {
      var children = Array.isArray(raw.children) ? raw.children : [];
      var hidden = collapsed.has(path);
      nodes.push({
        id: path,
        pid: parentId,
        depth: depth,
        title: raw.title || raw.name || 'Topic',
        note: raw.note || raw.subtitle || raw.description || '',
        hasKids: children.length > 0,
        hidden: hidden
      });
      if (parentId) edges.push({ from: parentId, to: path });
      if (!hidden) children.forEach(function (child, index) { walk(child || {}, path, depth + 1, path + '-' + index); });
    }
    walk({ title: map.title || 'Mindmap', children: map.nodes || [] }, null, 0, 'root');
    return { nodes: nodes, edges: edges };
  }

  function byId(data) {
    var map = {};
    data.nodes.forEach(function (node) { map[node.id] = node; });
    return map;
  }

  function byParent(data) {
    var map = {};
    data.nodes.forEach(function (node) {
      var key = node.pid || '_root';
      if (!map[key]) map[key] = [];
      map[key].push(node);
    });
    return map;
  }

  function measureNode(node) {
    if (node._mmBox) return node._mmBox;
    var titleChars = Math.floor((MAX_NODE_W - PAD_X * 2) / TITLE_CHAR_W);
    var noteChars = Math.floor((MAX_NODE_W - PAD_X * 2) / NOTE_CHAR_W);
    var titleLines = wrapText(latexToText(node.title), titleChars, 2);
    var noteLines = node.note ? wrapText(latexToText(node.note), noteChars, 2) : [];
    var titleW = titleLines.reduce(function (max, line) { return Math.max(max, textWidth(line, TITLE_CHAR_W)); }, 0);
    var noteW = noteLines.reduce(function (max, line) { return Math.max(max, textWidth(line, NOTE_CHAR_W)); }, 0);
    var contentW = Math.max(titleW, noteW);
    var width = clamp(Math.ceil(contentW + PAD_X * 2), MIN_NODE_W, MAX_NODE_W);
    var contentH = titleLines.length * TITLE_LH + (noteLines.length ? NOTE_GAP + noteLines.length * NOTE_LH : 0);
    var height = Math.max(node.note ? 66 : 50, Math.ceil(contentH + PAD_Y * 2));
    node._mmBox = {
      w: width,
      h: height,
      totalW: width + (node.hasKids ? INDICATOR_GAP + INDICATOR_R * 2 : 0),
      titleLines: titleLines,
      noteLines: noteLines,
      contentH: contentH
    };
    return node._mmBox;
  }

  function treeLayout(data) {
    var bp = byParent(data);
    var maxDepth = 0;
    var maxWidthByDepth = [];
    data.nodes.forEach(function (node) {
      maxDepth = Math.max(maxDepth, node.depth);
      var box = measureNode(node);
      maxWidthByDepth[node.depth] = Math.max(maxWidthByDepth[node.depth] || 0, box.totalW);
    });

    var depthX = [64];
    for (var d = 1; d <= maxDepth; d++) depthX[d] = depthX[d - 1] + (maxWidthByDepth[d - 1] || MIN_NODE_W) + COLUMN_GAP;

    var y = 64;
    var pos = {};
    function place(node) {
      var children = bp[node.id] || [];
      var box = measureNode(node);
      if (!children.length) {
        pos[node.id] = { x: depthX[node.depth], y: y };
        y += box.h + ROW_GAP;
        return;
      }
      children.forEach(place);
      var first = pos[children[0].id];
      var last = pos[children[children.length - 1].id];
      pos[node.id] = { x: depthX[node.depth], y: (first.y + last.y) / 2 };
    }
    place(data.nodes[0]);
    return pos;
  }

  function fitCanvas(data, pos) {
    var pad = 72;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    data.nodes.forEach(function (node) {
      var point = pos[node.id];
      if (!point) return;
      var box = measureNode(node);
      minX = Math.min(minX, point.x);
      maxX = Math.max(maxX, point.x + box.totalW);
      minY = Math.min(minY, point.y - box.h / 2);
      maxY = Math.max(maxY, point.y + box.h / 2);
    });
    if (!isFinite(minX)) return { w: 900, h: 560 };
    var dx = pad - minX;
    var dy = pad - minY;
    Object.keys(pos).forEach(function (id) { pos[id].x += dx; pos[id].y += dy; });
    return {
      w: Math.max(760, Math.ceil(maxX - minX + pad * 2)),
      h: Math.max(520, Math.ceil(maxY - minY + pad * 2))
    };
  }

  function textElements(lines, cssClass, x, startY, lineHeight) {
    return lines.map(function (line, index) {
      var y = startY + index * lineHeight;
      return '<text class="' + cssClass + '" x="' + x + '" y="' + y + '" text-anchor="start" dominant-baseline="middle">' + esc(line) + '</text>';
    }).join('');
  }

  function drawNode(node, point) {
    var box = measureNode(node);
    var depth = Math.min(node.depth, 4);
    var cls = 'sl-mm-n sl-mm-d' + depth + (node.depth === 0 ? ' sl-mm-root' : '') + (node.hasKids ? ' sl-mm-clickable' : '');
    var aria = node.hasKids ? ' tabindex="0" role="button" aria-expanded="' + (!node.hidden) + '" aria-label="Toggle ' + esc(node.title) + '"' : '';
    var html = '<g class="' + esc(cls) + '" data-nid="' + esc(node.id) + '" transform="translate(' + point.x + ',' + point.y + ')"' + aria + '>';
    html += '<rect class="sl-mm-nr" x="0" y="' + (-box.h / 2) + '" width="' + box.w + '" height="' + box.h + '" rx="12" ry="12"></rect>';

    var titleStart = -box.contentH / 2 + TITLE_LH / 2;
    html += textElements(box.titleLines, 'sl-mm-t', PAD_X, titleStart, TITLE_LH);
    if (box.noteLines.length) {
      var noteStart = titleStart + box.titleLines.length * TITLE_LH - TITLE_LH / 2 + NOTE_GAP + NOTE_LH / 2;
      html += textElements(box.noteLines, 'sl-mm-nt', PAD_X, noteStart, NOTE_LH);
    }

    if (node.hasKids) {
      var cx = box.w + INDICATOR_GAP + INDICATOR_R;
      var symbol = node.hidden ? '&gt;' : '&lt;';
      html += '<circle class="sl-mm-indicator sl-mm-indicator-d' + depth + ' sl-mm-toggle" cx="' + cx + '" cy="0" r="' + INDICATOR_R + '"></circle>';
      html += '<text class="sl-mm-indicator-text" x="' + cx + '" y="1" text-anchor="middle" dominant-baseline="middle">' + symbol + '</text>';
      html += '<circle class="sl-mm-toggle sl-mm-toggle-hit" cx="' + cx + '" cy="0" r="' + (INDICATOR_R + 8) + '"></circle>';
    }
    html += '</g>';
    return html;
  }

  function outputPoint(node, point) {
    var box = measureNode(node);
    if (!node.hasKids) return { x: point.x + box.w, y: point.y };
    return { x: point.x + box.w + INDICATOR_GAP + INDICATOR_R, y: point.y };
  }

  function inputPoint(node, point) {
    return { x: point.x - 8, y: point.y };
  }

  function edgePath(fromNode, toNode, fromPoint, toPoint) {
    var start = outputPoint(fromNode, fromPoint);
    var end = inputPoint(toNode, toPoint);
    var distance = Math.max(80, end.x - start.x);
    var curve = Math.min(150, Math.max(72, distance * 0.54));
    return 'M' + start.x + ',' + start.y + ' C' + (start.x + curve) + ',' + start.y + ' ' + (end.x - curve) + ',' + end.y + ' ' + end.x + ',' + end.y;
  }

  function getState(el, opts) {
    var state = el.__mm || { collapsed: new Set(), zoom: 1, query: '', centered: false, scroll: { x: 0, y: 0 } };
    if (opts) {
      if (opts.query != null) state.query = opts.query;
      if (typeof opts.zoom === 'number') state.zoom = clamp(opts.zoom, 0.25, 2.8);
    }
    el.__mm = state;
    return state;
  }

  function bindPanAndZoom(wrapEl, hostEl) {
    var drag = null;
    function isInteractiveTarget(event) {
      return closestWithClass(event.target, 'sl-mm-clickable', null) || closestWithClass(event.target, 'sl-mm-toggle', null);
    }
    function finishDrag() {
      if (!drag) return;
      wrapEl.__mmMoved = drag.moved;
      drag = null;
      wrapEl.classList.remove('sl-mm-grabbing');
      setTimeout(function () { wrapEl.__mmMoved = false; }, 0);
    }
    wrapEl.addEventListener('pointerdown', function (event) {
      if (event.button !== 0 || isInteractiveTarget(event)) return;
      drag = { x: event.clientX, y: event.clientY, left: wrapEl.scrollLeft, top: wrapEl.scrollTop, moved: false };
      if (wrapEl.setPointerCapture) wrapEl.setPointerCapture(event.pointerId);
      wrapEl.classList.add('sl-mm-grabbing');
    });
    wrapEl.addEventListener('pointermove', function (event) {
      if (!drag) return;
      var dx = event.clientX - drag.x;
      var dy = event.clientY - drag.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
      wrapEl.scrollLeft = drag.left - dx;
      wrapEl.scrollTop = drag.top - dy;
    });
    wrapEl.addEventListener('pointerup', finishDrag);
    wrapEl.addEventListener('pointercancel', finishDrag);
    wrapEl.addEventListener('lostpointercapture', finishDrag);
    wrapEl.addEventListener('wheel', function (event) {
      event.preventDefault();
      var state = getState(hostEl, {});
      var oldZoom = state.zoom || 1;
      var rect = wrapEl.getBoundingClientRect();
      var mx = event.clientX - rect.left;
      var my = event.clientY - rect.top;
      var nextZoom = clamp(oldZoom + (event.deltaY < 0 ? 0.1 : -0.1), 0.25, 2.8);
      state.zoom = nextZoom;
      state.pendingScroll = {
        x: (wrapEl.scrollLeft + mx) * (nextZoom / oldZoom) - mx,
        y: (wrapEl.scrollTop + my) * (nextZoom / oldZoom) - my
      };
      if (!applyZoomOnly(hostEl, state)) render(hostEl, hostEl.__mmMap || {}, state);
    }, { passive: false });
    wrapEl.addEventListener('dblclick', function () { resetView(hostEl, hostEl.__mmMap || {}); });
  }

  function applyInitialScroll(state, wrapEl, canvasEl, canvas, pos) {
    requestAnimationFrame(function () {
      if (state.fitRequested) {
        state.zoom = clamp(Math.min((wrapEl.clientWidth - 56) / canvas.w, (wrapEl.clientHeight - 56) / canvas.h), 0.25, 2.1);
        canvasEl.style.transform = 'scale(' + state.zoom + ')';
        var sizerEl = wrapEl.querySelector('.sl-mm-sizer');
        if (sizerEl) {
          sizerEl.style.width = (canvas.w * state.zoom) + 'px';
          sizerEl.style.height = (canvas.h * state.zoom) + 'px';
        }
        state.forceCenter = true;
        state.fitRequested = false;
      }
      if (state.pendingScroll) {
        wrapEl.scrollLeft = Math.max(0, state.pendingScroll.x);
        wrapEl.scrollTop = Math.max(0, state.pendingScroll.y);
        state.pendingScroll = null;
      } else if (state.forceCenter || !state.centered) {
        var root = pos.root || { x: canvas.w / 2, y: canvas.h / 2 };
        wrapEl.scrollLeft = Math.max(0, root.x * state.zoom - wrapEl.clientWidth / 2);
        wrapEl.scrollTop = Math.max(0, root.y * state.zoom - wrapEl.clientHeight / 2);
        state.centered = true;
        state.forceCenter = false;
      } else {
        wrapEl.scrollLeft = state.scroll.x || 0;
        wrapEl.scrollTop = state.scroll.y || 0;
      }
      state.scroll = { x: wrapEl.scrollLeft, y: wrapEl.scrollTop };
    });
  }

  function toggleNode(el, map, state, id, wrapEl) {
    if (!id) return;
    if (wrapEl) state.scroll = { x: wrapEl.scrollLeft, y: wrapEl.scrollTop };
    if (state.collapsed.has(id)) state.collapsed.delete(id);
    else state.collapsed.add(id);
    state.animate = true;
    render(el, map || el.__mmMap || {}, state);
  }

  function render(el, map, opts) {
    if (!el) return;
    var oldWrap = el.querySelector('.sl-mm-wrap');
    var state = getState(el, opts);
    if (oldWrap) state.scroll = { x: oldWrap.scrollLeft, y: oldWrap.scrollTop };
    el.__mmMap = map || {};

    var data = flatten(map || {}, state.collapsed);
    var positions = treeLayout(data);
    var canvas = fitCanvas(data, positions);
    var nodeMap = byId(data);
    var query = String(state.query || '').trim().toLowerCase();

    var edges = data.edges.map(function (edge) {
      var fromNode = nodeMap[edge.from];
      var toNode = nodeMap[edge.to];
      if (!fromNode || !toNode || !positions[edge.from] || !positions[edge.to]) return '';
      return '<path class="sl-mm-e sl-mm-e-d' + Math.min(toNode.depth, 4) + '" pathLength="1" d="' + edgePath(fromNode, toNode, positions[edge.from], positions[edge.to]) + '"></path>';
    }).join('');

    var nodes = data.nodes.map(function (node) {
      var html = drawNode(node, positions[node.id]);
      if (query && (node.title + ' ' + node.note).toLowerCase().indexOf(query) >= 0) html = html.replace('sl-mm-n ', 'sl-mm-n sl-mm-match ');
      return html;
    }).join('');

    var zoom = state.zoom || 1;
    state.canvasSize = canvas;
    var animateClass = state.animate ? ' sl-mm-animate' : '';
    el.innerHTML = '<div class="sl-mm-wrap' + animateClass + '"><div class="sl-mm-sizer" style="width:' + (canvas.w * zoom) + 'px;height:' + (canvas.h * zoom) + 'px;"><div class="sl-mm-canvas" style="transform:scale(' + zoom + ');width:' + canvas.w + 'px;height:' + canvas.h + 'px;"><svg class="sl-mm-svg" viewBox="0 0 ' + canvas.w + ' ' + canvas.h + '" width="' + canvas.w + '" height="' + canvas.h + '" style="width:' + canvas.w + 'px;height:' + canvas.h + 'px">' + edges + nodes + '</svg></div></div></div>';

    var wrapEl = el.querySelector('.sl-mm-wrap');
    var canvasEl = el.querySelector('.sl-mm-canvas');
    bindPanAndZoom(wrapEl, el);
    wrapEl.addEventListener('click', function (event) {
      if (wrapEl.__mmMoved) return;
      var nodeEl = closestWithClass(event.target, 'sl-mm-clickable', wrapEl);
      if (!nodeEl || !wrapEl.contains(nodeEl)) return;
      event.preventDefault();
      event.stopPropagation();
      toggleNode(el, map, state, nodeEl.getAttribute('data-nid'), wrapEl);
    });
    wrapEl.querySelectorAll('.sl-mm-clickable').forEach(function (nodeEl) {
      nodeEl.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          toggleNode(el, map, state, nodeEl.getAttribute('data-nid'), wrapEl);
        }
      });
    });
    if (state.animate) {
      setTimeout(function () {
        var currentWrap = el.querySelector('.sl-mm-wrap');
        if (currentWrap) currentWrap.classList.remove('sl-mm-animate');
        state.animate = false;
      }, ANIMATE_MS);
    }
    applyInitialScroll(state, wrapEl, canvasEl, canvas, positions);
  }

  // Apply a zoom change to the existing DOM without a full layout +
  // innerHTML rebuild (cheap path used by wheel zoom and the zoom buttons).
  function applyZoomOnly(el, state) {
    var wrapEl = el.querySelector('.sl-mm-wrap');
    var canvasEl = el.querySelector('.sl-mm-canvas');
    var sizerEl = el.querySelector('.sl-mm-sizer');
    var c = state.canvasSize;
    if (!wrapEl || !canvasEl || !c) return false;
    canvasEl.style.transform = 'scale(' + state.zoom + ')';
    if (sizerEl) {
      sizerEl.style.width = (c.w * state.zoom) + 'px';
      sizerEl.style.height = (c.h * state.zoom) + 'px';
    }
    if (state.pendingScroll) {
      wrapEl.scrollLeft = Math.max(0, state.pendingScroll.x);
      wrapEl.scrollTop = Math.max(0, state.pendingScroll.y);
      state.pendingScroll = null;
    }
    state.scroll = { x: wrapEl.scrollLeft, y: wrapEl.scrollTop };
    return true;
  }

  function setZoom(el, delta, map) {
    if (!el) return;
    var state = getState(el, {});
    var wrapEl = el.querySelector('.sl-mm-wrap');
    var oldZoom = state.zoom || 1;
    state.zoom = clamp(oldZoom + delta, 0.25, 2.8);
    if (wrapEl) {
      state.pendingScroll = {
        x: (wrapEl.scrollLeft + wrapEl.clientWidth / 2) * (state.zoom / oldZoom) - wrapEl.clientWidth / 2,
        y: (wrapEl.scrollTop + wrapEl.clientHeight / 2) * (state.zoom / oldZoom) - wrapEl.clientHeight / 2
      };
    }
    if (applyZoomOnly(el, state)) return;
    render(el, map || el.__mmMap || {}, state);
  }

  function expandAll(el, map) {
    if (!el) return;
    var state = getState(el, {});
    state.collapsed = new Set();
    render(el, map || el.__mmMap || {}, state);
  }

  function collapseAll(el, map) {
    if (!el) return;
    var state = getState(el, {});
    state.collapsed = new Set();
    function walk(nodes, path) {
      (nodes || []).forEach(function (node, index) {
        var id = (path || 'root') + '-' + index;
        if (node.children && node.children.length) state.collapsed.add(id);
        walk(node.children || [], id);
      });
    }
    walk((map || el.__mmMap || {}).nodes || [], 'root');
    render(el, map || el.__mmMap || {}, state);
  }

  function fitView(el, map) {
    if (!el) return;
    var state = getState(el, {});
    state.fitRequested = true;
    render(el, map || el.__mmMap || {}, state);
  }

  function resetView(el, map) {
    if (!el) return;
    var state = getState(el, {});
    state.zoom = 1;
    state.forceCenter = true;
    render(el, map || el.__mmMap || {}, state);
  }

  function exportStyles(theme) {
    var dark = theme === 'dark';
    if (dark) {
      return '.sl-mm-svg{background:#0f1724}.sl-mm-e{fill:none;stroke:#818cf8;stroke-width:2.45;stroke-linecap:round;opacity:.86}.sl-mm-e-d2,.sl-mm-e-d4{stroke:#2dd4bf}.sl-mm-e-d3{stroke:#60a5fa}.sl-mm-nr{stroke-width:1.2}.sl-mm-root .sl-mm-nr{fill:#4a4bb6;stroke:#6670e8}.sl-mm-d1 .sl-mm-nr{fill:#335a9a;stroke:#4f78ba}.sl-mm-d2 .sl-mm-nr,.sl-mm-d3 .sl-mm-nr,.sl-mm-d4 .sl-mm-nr{fill:#1f7b73;stroke:#34b7aa}.sl-mm-t{fill:#ecfeff;font-family:Poppins,system-ui,sans-serif;font-size:15.5px;font-weight:500;letter-spacing:-0.015em}.sl-mm-nt{fill:#99f6e4;font-family:Poppins,system-ui,sans-serif;font-size:11.5px;font-weight:500}.sl-mm-d1 .sl-mm-nt{fill:#bfdbfe}.sl-mm-root .sl-mm-t{fill:#eef2ff}.sl-mm-root .sl-mm-nt{fill:#c7d2fe}.sl-mm-indicator{fill:#2563eb;stroke:#0b1120;stroke-width:2.5}.sl-mm-indicator-d2,.sl-mm-indicator-d3,.sl-mm-indicator-d4{fill:#0d9488}.sl-mm-indicator-text{fill:#ecfeff;font-family:system-ui,sans-serif;font-size:17px;font-weight:800}.sl-mm-toggle-hit{fill:transparent;stroke:none}';
    }
    return '.sl-mm-svg{background:#f7f8fc}.sl-mm-e{fill:none;stroke:#7284ff;stroke-width:2.45;stroke-linecap:round;opacity:.92}.sl-mm-e-d2,.sl-mm-e-d4{stroke:#5acfc3}.sl-mm-e-d3{stroke:#5aa8ff}.sl-mm-nr{stroke-width:1.2}.sl-mm-root .sl-mm-nr{fill:#cfd6ff;stroke:#b3befd}.sl-mm-d1 .sl-mm-nr{fill:#c4d8f3;stroke:#c4d8f3}.sl-mm-d2 .sl-mm-nr,.sl-mm-d3 .sl-mm-nr,.sl-mm-d4 .sl-mm-nr{fill:#9fd8cf;stroke:#9fd8cf}.sl-mm-t{fill:#0f172a;font-family:Poppins,system-ui,sans-serif;font-size:15.5px;font-weight:500;letter-spacing:-0.015em}.sl-mm-nt{fill:#047d73;font-family:Poppins,system-ui,sans-serif;font-size:11.5px;font-weight:500}.sl-mm-d1 .sl-mm-nt{fill:#2563eb}.sl-mm-root .sl-mm-t{fill:#111827}.sl-mm-root .sl-mm-nt{fill:#4f46e5}.sl-mm-indicator{fill:#d7e6ff;stroke:#ffffff;stroke-width:2.5}.sl-mm-indicator-d2,.sl-mm-indicator-d3,.sl-mm-indicator-d4{fill:#c1ebe6}.sl-mm-indicator-text{fill:#253069;font-family:system-ui,sans-serif;font-size:17px;font-weight:800}.sl-mm-toggle-hit{fill:transparent;stroke:none}';
  }

  function svgMetrics(svg) {
    var viewBox = svg.viewBox && svg.viewBox.baseVal;
    var w = viewBox && viewBox.width ? viewBox.width : parseFloat(svg.getAttribute('width'));
    var h = viewBox && viewBox.height ? viewBox.height : parseFloat(svg.getAttribute('height'));
    if (!w || !h) {
      var box = svg.getBoundingClientRect();
      w = w || box.width || 1200;
      h = h || box.height || 800;
    }
    return { w: Math.ceil(w), h: Math.ceil(h) };
  }

  function buildExportSvg(svg, theme) {
    var size = svgMetrics(svg);
    var clone = svg.cloneNode(true);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('width', size.w);
    clone.setAttribute('height', size.h);
    clone.setAttribute('viewBox', '0 0 ' + size.w + ' ' + size.h);
    clone.setAttribute('style', 'background:' + (theme === 'dark' ? '#0f1724' : '#f7f8fc'));
    clone.querySelectorAll('[tabindex],[role],[aria-label],[aria-expanded]').forEach(function (node) {
      node.removeAttribute('tabindex');
      node.removeAttribute('role');
      node.removeAttribute('aria-label');
      node.removeAttribute('aria-expanded');
    });

    var ns = 'http://www.w3.org/2000/svg';
    var style = document.createElementNS(ns, 'style');
    style.textContent = exportStyles(theme);
    var bg = document.createElementNS(ns, 'rect');
    bg.setAttribute('x', 0);
    bg.setAttribute('y', 0);
    bg.setAttribute('width', size.w);
    bg.setAttribute('height', size.h);
    bg.setAttribute('fill', theme === 'dark' ? '#0f1724' : '#f7f8fc');
    clone.insertBefore(bg, clone.firstChild);
    clone.insertBefore(style, clone.firstChild);
    return { svg: clone, w: size.w, h: size.h };
  }

  function downloadPng(el) {
    var svg = el && el.querySelector('.sl-mm-svg');
    if (!svg) return;
    var theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var exportSvg = buildExportSvg(svg, theme);
    var data = '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(exportSvg.svg);
    var blob = new Blob([data], { type: 'image/svg+xml;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var image = new Image();
    image.onload = function () {
      var maxDimension = Math.max(exportSvg.w, exportSvg.h);
      var scale = maxDimension > 8192 ? 8192 / maxDimension : 2;
      var canvas = document.createElement('canvas');
      canvas.width = Math.ceil(exportSvg.w * scale);
      canvas.height = Math.ceil(exportSvg.h * scale);
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = theme === 'dark' ? '#0f1724' : '#f7f8fc';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      ctx.drawImage(image, 0, 0, exportSvg.w, exportSvg.h);
      URL.revokeObjectURL(url);
      var link = document.createElement('a');
      link.href = canvas.toDataURL('image/png');
      link.download = 'nebians-mindmap.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };
    image.onerror = function () {
      URL.revokeObjectURL(url);
      window.alert('Could not export this mindmap image. Please try again after the map finishes rendering.');
    };
    image.src = url;
  }

  window.NEBiansMindmap = {
    render: render,
    setZoom: setZoom,
    expandAll: expandAll,
    collapseAll: collapseAll,
    fitView: fitView,
    resetView: resetView,
    downloadPng: downloadPng
  };
})();