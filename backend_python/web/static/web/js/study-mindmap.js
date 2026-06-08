(function () {
  'use strict';

  function escapeHtml(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (ch) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch];
    });
  }

  function flatten(map, collapsed) {
    var nodes = [];
    var edges = [];
    var id = 0;
    function walk(raw, parentId, depth, path) {
      var nodeId = path || ('n' + (id++));
      var children = Array.isArray(raw.children) ? raw.children : [];
      var hidden = collapsed.has(nodeId);
      var node = {
        id: nodeId,
        parentId: parentId,
        depth: depth,
        title: raw.title || raw.name || 'Topic',
        note: raw.note || raw.description || '',
        hasChildren: children.length > 0,
        hidden: hidden,
        childCount: children.length
      };
      nodes.push(node);
      if (parentId) edges.push({from: parentId, to: nodeId});
      if (!hidden) {
        children.forEach(function (child, i) { walk(child || {}, nodeId, depth + 1, nodeId + '-' + i); });
      }
      return node;
    }
    walk({title: map.title || 'Mindmap', note: '', children: map.nodes || []}, null, 0, 'root');
    return {nodes: nodes, edges: edges};
  }

  function splitText(text, maxChars, maxLines) {
    var words = String(text || '').split(/\s+/).filter(Boolean);
    var lines = [];
    var line = '';
    words.forEach(function (word) {
      while (word.length > maxChars) {
        var chunk = word.slice(0, maxChars - 1) + '…';
        if (line) {
          lines.push(line);
          line = '';
        }
        lines.push(chunk);
        word = word.slice(maxChars - 1);
      }
      if ((line + ' ' + word).trim().length > maxChars && line) {
        lines.push(line);
        line = word;
      } else {
        line = (line + ' ' + word).trim();
      }
    });
    if (line) lines.push(line);
    if (!lines.length) lines = ['Topic'];
    if (lines.length > maxLines) {
      lines = lines.slice(0, maxLines);
      lines[lines.length - 1] = lines[lines.length - 1].replace(/\.*$/, '') + '…';
    }
    return lines;
  }

  function radialLayout(data) {
    var byParent = {};
    data.nodes.forEach(function (n) { (byParent[n.parentId || 'none'] = byParent[n.parentId || 'none'] || []).push(n); });
    var pos = {root: {x: 520, y: 360}};
    var mains = byParent.root || [];
    var total = Math.max(mains.length, 1);
    mains.forEach(function (n, i) {
      var angle = -Math.PI / 2 + (2 * Math.PI * i / total);
      pos[n.id] = {x: 520 + Math.cos(angle) * 245, y: 360 + Math.sin(angle) * 210, angle: angle};
      placeChildren(n, angle, 1);
    });
    function placeChildren(parent, baseAngle, level) {
      var kids = byParent[parent.id] || [];
      var fan = Math.min(Math.PI * 0.9, Math.PI * (0.36 + kids.length * 0.055));
      kids.forEach(function (kid, idx) {
        var offset = kids.length === 1 ? 0 : -fan / 2 + fan * idx / (kids.length - 1);
        var angle = baseAngle + offset;
        var radius = 145 + Math.min(level, 3) * 34;
        pos[kid.id] = {x: pos[parent.id].x + Math.cos(angle) * radius, y: pos[parent.id].y + Math.sin(angle) * radius, angle: angle};
        placeChildren(kid, angle, level + 1);
      });
    }
    return pos;
  }

  function treeLayout(data) {
    var byParent = {};
    data.nodes.forEach(function (n) { (byParent[n.parentId || 'none'] = byParent[n.parentId || 'none'] || []).push(n); });
    var y = 92;
    var pos = {};
    function layout(node, depth) {
      var kids = byParent[node.id] || [];
      if (!kids.length) {
        pos[node.id] = {x: 96 + depth * 235, y: y};
        y += 108;
      } else {
        kids.forEach(function (k) { layout(k, depth + 1); });
        var first = pos[kids[0].id].y;
        var last = pos[kids[kids.length - 1].id].y;
        pos[node.id] = {x: 96 + depth * 235, y: (first + last) / 2};
      }
    }
    layout(data.nodes[0], 0);
    return pos;
  }

  function nodeSize(node, settings) {
    var root = node.depth === 0;
    return {
      width: root ? 210 : (settings.density === 'compact' ? 168 : 192),
      height: root ? 72 : (node.note ? 72 : 56)
    };
  }

  function fitCanvas(data, pos, settings) {
    var pad = settings.layout === 'tree' ? 56 : 72;
    var minX = Infinity;
    var minY = Infinity;
    var maxX = -Infinity;
    var maxY = -Infinity;

    data.nodes.forEach(function (node) {
      var p = pos[node.id];
      if (!p) return;
      var size = nodeSize(node, settings);
      minX = Math.min(minX, p.x - size.width / 2);
      maxX = Math.max(maxX, p.x + size.width / 2);
      minY = Math.min(minY, p.y - size.height / 2);
      maxY = Math.max(maxY, p.y + size.height / 2);
    });

    if (!isFinite(minX) || !isFinite(minY)) {
      return {width: 1040, height: 720};
    }

    var dx = pad - minX;
    var dy = pad - minY;
    Object.keys(pos).forEach(function (id) {
      pos[id].x += dx;
      pos[id].y += dy;
    });

    return {
      width: Math.max(760, Math.ceil((maxX - minX) + pad * 2)),
      height: Math.max(520, Math.ceil((maxY - minY) + pad * 2))
    };
  }

  function drawNode(node, p, settings) {
    var root = node.depth === 0;
    var size = nodeSize(node, settings);
    var width = size.width;
    var height = size.height;
    var x = p.x - width / 2;
    var y = p.y - height / 2;
    var lines = splitText(node.title, root ? 18 : 20, root ? 2 : 2);
    var note = node.note ? splitText(node.note, 28, 1)[0] : '';
    var cls = 'sl-mm-node sl-mm-depth-' + Math.min(node.depth, 4) + (root ? ' sl-mm-root-node' : '') + (node.hasChildren ? ' sl-mm-has-children' : '');
    var html = '<g class="' + cls + '" tabindex="0" role="button" data-node-id="' + escapeHtml(node.id) + '">' +
      '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + width + '" height="' + height + '" rx="18"></rect>' +
      '<text x="' + p.x.toFixed(1) + '" y="' + (y + (note ? 25 : 32)).toFixed(1) + '" text-anchor="middle">';
    lines.forEach(function (line, i) {
      html += '<tspan x="' + p.x.toFixed(1) + '" dy="' + (i ? 17 : 0) + '">' + escapeHtml(line) + '</tspan>';
    });
    if (note) html += '<tspan class="sl-mm-note" x="' + p.x.toFixed(1) + '" dy="18">' + escapeHtml(note) + '</tspan>';
    html += '</text>';
    if (node.hasChildren) {
      html += '<circle cx="' + (x + width - 18).toFixed(1) + '" cy="' + (y + 18).toFixed(1) + '" r="10"></circle>' +
        '<text class="sl-mm-count" x="' + (x + width - 18).toFixed(1) + '" y="' + (y + 22).toFixed(1) + '" text-anchor="middle">' + node.childCount + '</text>';
    }
    html += '</g>';
    return html;
  }

  function render(container, map, options) {
    if (!container) return;
    options = options || {};
    var state = container.__mindmapState || {collapsed: new Set(), zoom: 1, layout: 'radial', theme: 'clean', density: 'comfortable', query: ''};
    state.layout = options.layout || state.layout;
    state.theme = options.theme || state.theme;
    state.density = options.density || state.density;
    state.query = options.query != null ? options.query : state.query;
    container.__mindmapState = state;

    var data = flatten(map || {}, state.collapsed);
    var pos = state.layout === 'tree' ? treeLayout(data) : radialLayout(data);
    var canvas = fitCanvas(data, pos, state);
    var width = Math.max(state.layout === 'tree' ? 1000 : 1040, canvas.width);
    var height = Math.max(state.layout === 'tree' ? 620 : 720, canvas.height);
    var q = String(state.query || '').trim().toLowerCase();
    var edges = data.edges.map(function (e) {
      var a = pos[e.from]; var b = pos[e.to];
      if (!a || !b) return '';
      var midx = state.layout === 'tree' ? (a.x + b.x) / 2 : null;
      var d = state.layout === 'tree'
        ? 'M' + a.x.toFixed(1) + ',' + a.y.toFixed(1) + ' C' + midx.toFixed(1) + ',' + a.y.toFixed(1) + ' ' + midx.toFixed(1) + ',' + b.y.toFixed(1) + ' ' + b.x.toFixed(1) + ',' + b.y.toFixed(1)
        : 'M' + a.x.toFixed(1) + ',' + a.y.toFixed(1) + ' L' + b.x.toFixed(1) + ',' + b.y.toFixed(1);
      return '<path class="sl-mm-edge" d="' + d + '"></path>';
    }).join('');
    var nodes = data.nodes.map(function (n) {
      var html = drawNode(n, pos[n.id], state);
      if (q && (n.title + ' ' + n.note).toLowerCase().indexOf(q) >= 0) html = html.replace('sl-mm-node', 'sl-mm-node sl-mm-match');
      return html;
    }).join('');

    container.className = 'sl-mindmap-stage sl-mm-theme-' + state.theme + ' sl-mm-density-' + state.density;
    container.innerHTML = '<div class="sl-mm-scroll"><svg class="sl-mm-svg" viewBox="0 0 ' + width + ' ' + height + '" style="width:' + (width * state.zoom) + 'px;height:' + (height * state.zoom) + 'px" aria-label="Interactive study mindmap"><g class="sl-mm-edges">' + edges + '</g><g class="sl-mm-nodes">' + nodes + '</g></svg></div><div class="sl-mm-hint">Tap a branch to collapse or expand it.</div>';

    container.querySelectorAll('.sl-mm-node').forEach(function (el) {
      el.addEventListener('click', function () {
        var id = el.getAttribute('data-node-id');
        var node = data.nodes.find(function (n) { return n.id === id; });
        if (!node || !node.hasChildren) return;
        if (state.collapsed.has(id)) state.collapsed.delete(id); else state.collapsed.add(id);
        render(container, map, state);
      });
    });
  }

  function setZoom(container, delta, map) {
    var state = container.__mindmapState || {collapsed: new Set(), zoom: 1};
    state.zoom = Math.max(0.65, Math.min(1.75, (state.zoom || 1) + delta));
    render(container, map, state);
  }

  function expandAll(container, map) {
    var state = container.__mindmapState || {collapsed: new Set()};
    state.collapsed = new Set();
    render(container, map, state);
  }

  function collapseAll(container, map) {
    var state = container.__mindmapState || {collapsed: new Set()};
    state.collapsed = new Set();
    function walk(nodes, path) {
      (nodes || []).forEach(function (n, i) {
        var id = (path || 'root') + '-' + i;
        if (n.children && n.children.length) state.collapsed.add(id);
        walk(n.children || [], id);
      });
    }
    walk(map.nodes || [], 'root');
    render(container, map, state);
  }

  window.NEBiansMindmap = { render: render, setZoom: setZoom, expandAll: expandAll, collapseAll: collapseAll };
})();
