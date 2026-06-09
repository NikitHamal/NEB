(function () {
  'use strict';

  var ESC_MAP = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'};
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return ESC_MAP[c]; }); }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  /* ── Approximate text width for auto-sizing ── */
  var CHAR_W = 8.2;
  function textWidth(text) { return (text || '').length * CHAR_W; }

  /* ── Flatten tree ── */
  function flatten(map, collapsed) {
    var nodes = [], edges = [];
    function walk(raw, pid, depth, path) {
      var id = path;
      var kids = Array.isArray(raw.children) ? raw.children : [];
      var hidden = collapsed.has(id);
      nodes.push({ id: id, pid: pid, depth: depth, title: raw.title || raw.name || 'Topic', note: raw.note || raw.description || '', hasKids: kids.length > 0, hidden: hidden });
      if (pid) edges.push({ from: pid, to: id });
      if (!hidden) kids.forEach(function(k,i){ walk(k || {}, id, depth+1, id+'-'+i); });
    }
    walk({ title: map.title || 'Mindmap', children: map.nodes || [] }, null, 0, 'root');
    return { nodes: nodes, edges: edges };
  }

  /* ── Index children by parent ── */
  function byParent(data) {
    var m = {};
    data.nodes.forEach(function(n){ (m[n.pid||'_'] = m[n.pid||'_']||[]).push(n); });
    return m;
  }

  /* ── Horizontal tree layout ── */
  function treeLayout(data) {
    var bp = byParent(data);
    var y = 60;
    var pos = {};
    var xStep = 280, yStep = 78;
    function lay(node, depth) {
      var kids = bp[node.id] || [];
      if (!kids.length) {
        pos[node.id] = { x: 60 + depth * xStep, y: y };
        y += yStep + (node.note ? 18 : 0);
      } else {
        kids.forEach(function(k){ lay(k, depth + 1); });
        pos[node.id] = { x: 60 + depth * xStep, y: (pos[kids[0].id].y + pos[kids[kids.length-1].id].y) / 2 };
      }
    }
    lay(data.nodes[0], 0);
    return pos;
  }

  /* ── Node dimensions (NotebookLM style) ── */
  var PAD_L = 18, PAD_R = 18, H_TITLE = 44, H_WITH_NOTE = 62;
  var FONT_PX = 14, NOTE_FONT_PX = 11, INDICATOR_R = 10, INDICATOR_GAP = 8;

  function nodeW(node) {
    var tw = textWidth(node.title);
    var nw = node.note ? textWidth(node.note) * (NOTE_FONT_PX / FONT_PX) : 0;
    var contentW = Math.max(tw, nw);
    if (node.hasKids) contentW += INDICATOR_R * 2 + INDICATOR_GAP;
    return Math.max(80, contentW + PAD_L + PAD_R);
  }
  function nodeH(node) { return node.note ? H_WITH_NOTE : H_TITLE; }

  /* ── Fit canvas ── */
  function fitCanvas(data, pos) {
    var pad = 50;
    var minX=Infinity, minY=Infinity, maxX=-Infinity, maxY=-Infinity;
    data.nodes.forEach(function(n){
      var p = pos[n.id]; if (!p) return;
      var w = nodeW(n), h = nodeH(n);
      minX = Math.min(minX, p.x - PAD_L); maxX = Math.max(maxX, p.x - PAD_L + w);
      minY = Math.min(minY, p.y - h/2); maxY = Math.max(maxY, p.y + h/2);
    });
    if (!isFinite(minX)) return { w: 800, h: 500 };
    var dx = pad - minX, dy = pad - minY;
    Object.keys(pos).forEach(function(id){ pos[id].x += dx; pos[id].y += dy; });
    return { w: Math.max(600, Math.ceil(maxX - minX + pad*2)), h: Math.max(400, Math.ceil(maxY - minY + pad*2)) };
  }

  /* ── Draw a node (NotebookLM style: g transform, rect x=-18, text start, circle indicator) ── */
  function drawNode(node, p) {
    var w = nodeW(node), h = nodeH(node);
    var depth = Math.min(node.depth, 4);
    var cls = 'sl-mm-n sl-mm-d' + depth + (node.depth===0?' sl-mm-root':'') + (node.hasKids?' sl-mm-clickable':'');

    var rectX = -PAD_L;
    var rectY = -h / 2;

    var s = '<g class="'+esc(cls)+'" tabindex="0" role="button" data-nid="'+esc(node.id)+'" transform="translate('+p.x+','+p.y+')">';
    s += '<rect class="sl-mm-nr" x="'+rectX+'" y="'+rectY+'" width="'+w+'" height="'+h+'" rx="8" ry="8"></rect>';

    if (node.note) {
      /* Title + note: title top-aligned, note below */
      var titleY = -h/2 + 18;
      s += '<text class="sl-mm-t" x="0" y="'+titleY+'" text-anchor="start" dominant-baseline="middle">'+esc(node.title)+'</text>';
      var noteY = titleY + 15;
      s += '<text class="sl-mm-nt" x="0" y="'+noteY+'" text-anchor="start" dominant-baseline="middle">'+esc(node.note)+'</text>';
    } else {
      /* Title only: vertically centered */
      s += '<text class="sl-mm-t" x="0" y="0" text-anchor="start" dominant-baseline="middle">'+esc(node.title)+'</text>';
    }

    /* Expand/collapse circle at right edge */
    if (node.hasKids) {
      var cx = w - PAD_L - PAD_R + INDICATOR_R + 4;
      var symbol = node.hidden ? '&gt;' : '&lt;';
      s += '<circle class="sl-mm-indicator sl-mm-indicator-d'+depth+'" cx="'+cx+'" cy="0" r="'+INDICATOR_R+'"></circle>';
      s += '<text class="sl-mm-indicator-text" x="'+cx+'" y="1" text-anchor="middle" dominant-baseline="middle">'+symbol+'</text>';
    }

    s += '</g>';
    return s;
  }

  /* ── Smooth cubic bezier edge ── */
  function edgePath(a, b) {
    var dx = (b.x - a.x) * 0.45;
    return 'M'+a.x+','+a.y+' C'+(a.x+dx)+','+a.y+' '+(b.x-dx)+','+b.y+' '+b.x+','+b.y;
  }

  /* ── State ── */
  function getState(el, opts) {
    var st = el.__mm || { collapsed: new Set(), zoom: 1, query: '', centered: false, scroll: {x:0,y:0} };
    if (opts) {
      if (opts.query != null) st.query = opts.query;
      if (typeof opts.zoom === 'number') st.zoom = clamp(opts.zoom, 0.2, 3);
    }
    el.__mm = st;
    return st;
  }

  /* ── Bind pan + wheel zoom ── */
  function bindEvents(el) {
    if (el.__mmBound) return;
    el.__mmBound = true;
    var drag = null, moved = false;

    el.addEventListener('mousedown', function(e) {
      if (e.button !== 0) return;
      drag = { sx: e.clientX, sy: e.clientY, sl: el.scrollLeft, st: el.scrollTop };
      moved = false;
      el.classList.add('sl-mm-grabbing');
      e.preventDefault();
    });
    window.addEventListener('mousemove', function(e) {
      if (!drag) return;
      var dx = e.clientX - drag.sx, dy = e.clientY - drag.sy;
      if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
      el.scrollLeft = drag.sl - dx;
      el.scrollTop = drag.st - dy;
    });
    window.addEventListener('mouseup', function() {
      if (!drag) return;
      drag = null;
      el.classList.remove('sl-mm-grabbing');
      setTimeout(function(){ el.__moved = moved; moved = false; }, 0);
    });

    el.addEventListener('wheel', function(e) {
      e.preventDefault();
      var treeEl = el.closest('[id="slMindmapTree"]') || el.parentElement;
      var st = getState(treeEl, {});
      var oldZoom = st.zoom || 1;
      var rect = el.getBoundingClientRect();
      var mx = e.clientX - rect.left, my = e.clientY - rect.top;
      var delta = e.deltaY < 0 ? 0.1 : -0.1;
      var newZoom = clamp(oldZoom + delta, 0.2, 3);
      st.zoom = newZoom;
      st.pendingScroll = { x: (el.scrollLeft + mx) * (newZoom / oldZoom) - mx, y: (el.scrollTop + my) * (newZoom / oldZoom) - my };
      render(treeEl, window.__mmMap, st);
    }, { passive: false });

    el.addEventListener('dblclick', function() {
      var treeEl = el.closest('[id="slMindmapTree"]') || el.parentElement;
      var st = getState(treeEl, {});
      st.zoom = 1; st.forceCenter = true;
      render(treeEl, window.__mmMap, st);
    });
  }

  /* ── Main render ── */
  function render(el, map, opts) {
    if (!el) return;
    window.__mmMap = map;
    var st = getState(el, opts);
    var data = flatten(map || {}, st.collapsed);
    var pos = treeLayout(data);
    var canvas = fitCanvas(data, pos);

    var q = String(st.query || '').trim().toLowerCase();
    var edgesSvg = data.edges.map(function(e){
      var a = pos[e.from], b = pos[e.to];
      if (!a || !b) return '';
      var depth = 0;
      data.nodes.forEach(function(n){ if (n.id === e.to) depth = n.depth; });
      return '<path class="sl-mm-e sl-mm-e-d'+Math.min(depth, 4)+'" d="'+edgePath(a,b)+'"></path>';
    }).join('');

    var nodesSvg = data.nodes.map(function(n){
      var s = drawNode(n, pos[n.id]);
      if (q && n.title.toLowerCase().indexOf(q) >= 0) s = s.replace('sl-mm-n ', 'sl-mm-n sl-mm-match ');
      return s;
    }).join('');

    var zoom = st.zoom || 1;
    el.innerHTML = '<div class="sl-mm-wrap" style="height:520px;"><div class="sl-mm-canvas" style="transform:scale('+zoom+');transform-origin:0 0;width:'+canvas.w+'px;height:'+canvas.h+'px;"><svg class="sl-mm-svg" viewBox="0 0 '+canvas.w+' '+canvas.h+'" style="width:'+canvas.w+'px;height:'+canvas.h+'px">'+edgesSvg+nodesSvg+'</svg></div></div>';

    var wrapEl = el.querySelector('.sl-mm-wrap');
    bindEvents(wrapEl);

    requestAnimationFrame(function(){
      if (st.pendingScroll) {
        wrapEl.scrollLeft = Math.max(0, st.pendingScroll.x);
        wrapEl.scrollTop = Math.max(0, st.pendingScroll.y);
        st.pendingScroll = null;
      } else if (st.forceCenter || !st.centered) {
        var rootP = pos.root || { x: canvas.w/2, y: canvas.h/2 };
        wrapEl.scrollLeft = Math.max(0, rootP.x * st.zoom - wrapEl.clientWidth / 2);
        wrapEl.scrollTop = Math.max(0, rootP.y * st.zoom - wrapEl.clientHeight / 2);
        st.centered = true; st.forceCenter = false;
      } else {
        wrapEl.scrollLeft = st.scroll.x || 0;
        wrapEl.scrollTop = st.scroll.y || 0;
      }
      st.scroll = { x: wrapEl.scrollLeft, y: wrapEl.scrollTop };
    });

    wrapEl.querySelectorAll('.sl-mm-clickable').forEach(function(g){
      g.addEventListener('click', function(e) {
        if (wrapEl.__moved) return;
        var id = g.getAttribute('data-nid');
        if (st.collapsed.has(id)) st.collapsed.delete(id); else st.collapsed.add(id);
        render(el, map, st);
      });
      g.addEventListener('keydown', function(e) { if (e.key==='Enter'||e.key===' '){ e.preventDefault(); g.click(); }});
    });
  }

  /* ── Public API ── */
  function setZoom(el, delta, map) {
    var st = getState(el, {});
    var wrapEl = el.querySelector('.sl-mm-wrap');
    var old = st.zoom || 1;
    st.zoom = clamp(old + delta, 0.2, 3);
    if (wrapEl) {
      st.pendingScroll = { x: (wrapEl.scrollLeft + wrapEl.clientWidth/2) * (st.zoom/old) - wrapEl.clientWidth/2, y: (wrapEl.scrollTop + wrapEl.clientHeight/2) * (st.zoom/old) - wrapEl.clientHeight/2 };
    }
    render(el, map, st);
  }
  function expandAll(el, map) { var st = getState(el, {}); st.collapsed = new Set(); render(el, map, st); }
  function collapseAll(el, map) {
    var st = getState(el, {}); st.collapsed = new Set();
    function walk(nodes, path) { (nodes||[]).forEach(function(n,i){ var id=(path||'root')+'-'+i; if (n.children&&n.children.length) st.collapsed.add(id); walk(n.children||[], id); }); }
    walk((map||{}).nodes||[], 'root');
    render(el, map, st);
  }
  function fitView(el, map) {
    var st = getState(el, {});
    var wrapEl = el.querySelector('.sl-mm-wrap');
    if (wrapEl) {
      var svgEl = el.querySelector('.sl-mm-svg');
      if (svgEl) {
        var vb = svgEl.getAttribute('viewBox').split(' ');
        var svgW = parseFloat(vb[2]) || 800, svgH = parseFloat(vb[3]) || 500;
        st.zoom = clamp(Math.min((wrapEl.clientWidth - 40) / svgW, (wrapEl.clientHeight - 40) / svgH), 0.2, 2);
      }
    }
    st.forceCenter = true; render(el, map, st);
  }
  function resetView(el, map) { var st = getState(el, {}); st.zoom = 1; st.forceCenter = true; render(el, map, st); }

  function downloadPng(el) {
    var svg = el && el.querySelector('.sl-mm-svg'); if (!svg) return;
    var clone = svg.cloneNode(true);
    var bg = document.querySelector('[data-theme="dark"]') ? '#0f172a' : '#ffffff';
    var style = document.createElement('style');
    style.textContent = '.sl-mm-nr{fill:#fff;stroke:#e2e8f0;stroke-width:1;rx:8;ry:8}.sl-mm-root .sl-mm-nr{fill:#4f46e5;stroke:#4338ca;stroke-width:1.5}.sl-mm-d0 .sl-mm-nr{fill:#eef2ff;stroke:#c7d2fe}.sl-mm-d1 .sl-mm-nr{fill:#ecfdf5;stroke:#6ee7b7}.sl-mm-d2 .sl-mm-nr{fill:#fffbeb;stroke:#fcd34d}.sl-mm-d3 .sl-mm-nr{fill:#eff6ff;stroke:#93c5fd}.sl-mm-d4 .sl-mm-nr{fill:#faf5ff;stroke:#d8b4fe}.sl-mm-t{fill:#334155;font-family:Poppins,system-ui,sans-serif;font-size:14px;font-weight:600}.sl-mm-root .sl-mm-t{fill:#fff;font-weight:700}.sl-mm-e{fill:none;stroke:#cbd5e1;stroke-width:2;stroke-linecap:round}.sl-mm-e-d1{stroke:#6ee7b7}.sl-mm-e-d2{stroke:#fcd34d}.sl-mm-e-d3{stroke:#93c5fd}.sl-mm-e-d4{stroke:#d8b4fe}.sl-mm-indicator{stroke:#e2e8f0;stroke-width:1}.sl-mm-indicator-text{fill:#64748b;font-size:14px;font-weight:700;font-family:system-ui,sans-serif}';
    clone.insertBefore(style, clone.firstChild);
    var data = new XMLSerializer().serializeToString(clone);
    var blob = new Blob([data], {type:'image/svg+xml;charset=utf-8'});
    var url = URL.createObjectURL(blob), img = new Image();
    img.onload = function(){
      var c = document.createElement('canvas'); c.width = img.width * 2; c.height = img.height * 2;
      var ctx = c.getContext('2d'); ctx.scale(2,2); ctx.fillStyle = bg; ctx.fillRect(0,0,img.width,img.height); ctx.drawImage(img,0,0); URL.revokeObjectURL(url);
      var a = document.createElement('a'); a.href = c.toDataURL('image/png'); a.download = 'nebians-mindmap.png'; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    };
    img.src = url;
  }

  window.NEBiansMindmap = { render: render, setZoom: setZoom, expandAll: expandAll, collapseAll: collapseAll, fitView: fitView, resetView: resetView, downloadPng: downloadPng };
})();