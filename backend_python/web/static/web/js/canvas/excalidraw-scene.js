window.NebScene = (function () {
  var CARD_W = 340;
  var FONT = 6;
  var EDGE_COLOR = "#9aa7bd";

  var KIND_STYLE = {
    ai: { stroke: "#1d4ed8", bg: "#dbeafe" },
    note: { stroke: "#b45309", bg: "#fef3c7" },
    question: { stroke: "#7c3aed", bg: "#ede9fe" },
    source: { stroke: "#0f766e", bg: "#ccfbf1" },
    comparison: { stroke: "#be185d", bg: "#fce7f3" },
    practice: { stroke: "#15803d", bg: "#dcfce7" },
    summary: { stroke: "#334155", bg: "#f1f5f9" },
    task: { stroke: "#c2410c", bg: "#ffedd5" },
    decision: { stroke: "#6d28d9", bg: "#ede9fe" },
    warning: { stroke: "#dc2626", bg: "#fee2e2" },
  };

  var META_BG = {
    blue: "#dbeafe", green: "#dcfce7", amber: "#fef3c7",
    rose: "#ffe4e6", purple: "#ede9fe", slate: "#f1f5f9", default: "",
  };

  function hashSeed(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return Math.abs(h) % 2147483647;
  }

  function base(id, type, x, y, idx) {
    return {
      id: id, type: type, x: x, y: y, angle: 0,
      strokeColor: "#1e1e1e", backgroundColor: "transparent",
      fillStyle: "solid", strokeWidth: 2, strokeStyle: "solid",
      roughness: 1, opacity: 100, groupIds: [], frameId: null,
      roundness: type === "arrow" || type === "line" ? { type: 2 } : { type: 3 },
      boundElements: [], link: null, locked: false,
      seed: hashSeed(id), version: 1, versionNonce: (Math.random() * 2147483647) | 0,
      isDeleted: false, index: "a" + idx, customData: undefined,
    };
  }

  function styleFor(node) {
    var meta = node.meta || {};
    var st = KIND_STYLE[node.kind] || KIND_STYLE.ai;
    var bg = META_BG[meta.color] || st.bg;
    return { stroke: st.stroke, bg: bg };
  }

  function cardText(node) {
    var title = String(node.title || node.prompt || "Untitled").slice(0, 140);
    var content = node.content || {};
    var summary = String(content.summary || "").slice(0, 420);
    if (!summary && typeof node.prompt === "string") summary = node.prompt.slice(0, 420);
    return summary ? title + "\n\n" + summary : title;
  }

  function estimateHeight(text) {
    var lines = String(text).split("\n");
    var rows = 0;
    lines.forEach(function (ln, i) {
      rows += Math.max(1, Math.ceil(ln.length / (i === 0 ? 26 : 34)));
    });
    return Math.min(460, Math.max(170, 56 + rows * 24));
  }

  function nodeRect(node, idx) {
    var st = styleFor(node);
    var text = cardText(node);
    var h = estimateHeight(text);
    var x = Number(node.x) || 0;
    var y = Number(node.y) || 0;
    var rect = base(String(node.id), "rectangle", x, y, idx);
    rect.width = CARD_W;
    rect.height = h;
    rect.strokeColor = st.stroke;
    rect.backgroundColor = st.bg;
    rect.strokeWidth = 2.5;
    rect.customData = { neb: "node", id: String(node.id) };
    var label = base(String(node.id) + ":t", "text", x, y, idx + "t");
    label.width = CARD_W - 48;
    label.height = h - 48;
    label.strokeColor = "#1e1e1e";
    label.backgroundColor = "transparent";
    label.fontSize = 18;
    label.fontFamily = FONT;
    label.textAlign = "left";
    label.verticalAlign = "top";
    label.text = text;
    label.originalText = text;
    label.autoResize = false;
    label.lineHeight = 1.25;
    label.containerId = rect.id;
    label.customData = { neb: "node", id: String(node.id) };
    rect.boundElements = [{ type: "text", id: label.id }];
    return { rect: rect, label: label, h: h };
  }

  function nodeEdge(node, pos) {
    if (!node.parentId || !pos[node.parentId] || !pos[node.id]) return null;
    var p = pos[node.parentId];
    var c = pos[node.id];
    var x1 = p.x + CARD_W / 2;
    var y1 = p.y + p.h;
    var x2 = c.x + CARD_W / 2;
    var y2 = c.y;
    if (c.y < p.y) { y1 = p.y; y2 = c.y + c.h; }
    var edge = base("e" + String(node.id), "arrow", x1, y1, "e" + pos[node.id].idx);
    edge.width = Math.abs(x2 - x1) || 1;
    edge.height = Math.abs(y2 - y1) || 1;
    edge.points = [[0, 0], [x2 - x1, y2 - y1]];
    edge.strokeColor = EDGE_COLOR;
    edge.strokeWidth = 2;
    edge.startBinding = { elementId: String(node.parentId), focus: 0, gap: 8 };
    edge.endBinding = { elementId: String(node.id), focus: 0, gap: 8 };
    edge.startArrowhead = null;
    edge.endArrowhead = "arrow";
    edge.elbowed = false;
    edge.customData = { neb: "edge", child: String(node.id) };
    return edge;
  }

  function boardToScene(nodes, objects) {
    var elements = [];
    var files = {};
    var pos = {};
    var idx = 0;
    (nodes || []).forEach(function (n) {
      var built = nodeRect(n, idx++);
      pos[String(n.id)] = { x: built.rect.x, y: built.rect.y, h: built.h, idx: idx };
      elements.push(built.rect, built.label);
    });
    (nodes || []).forEach(function (n) {
      var edge = nodeEdge(n, pos);
      if (edge) elements.push(edge);
    });
    var ink = objectsToElements(objects || [], files, idx);
    ink.forEach(function (el) { elements.push(el); });
    return { elements: elements, files: files };
  }

  function objectsToElements(objects, files, startIdx) {
    var out = [];
    var idx = startIdx || 0;
    objects.forEach(function (o) {
      if (!o || typeof o !== "object") return;
      if (o.type === "excalidraw-ink" && Array.isArray(o.elements)) {
        o.elements.forEach(function (el) {
          if (el && el.id && !el.isDeleted) out.push(el);
        });
        return;
      }
      var conv = convertLegacy(o, "k" + (idx++));
      if (conv) {
        if (Array.isArray(conv)) conv.forEach(function (e) { out.push(e); });
        else out.push(conv);
      }
    });
    return out;
  }

  function inkBase(o, type, x, y, idx) {
    var el = base("k-" + String(o.id || idx), type, Number(o.x) || x || 0, Number(o.y) || y || 0, "k" + idx);
    el.strokeColor = o.stroke || o.color || "#1e1e1e";
    el.customData = { neb: "ink" };
    return el;
  }

  function convertLegacy(o, idx) {
    var t = o.type;
    if (t === "pen" || t === "highlighter" || t === "marker") {
      var pts = Array.isArray(o.points) ? o.points : [];
      if (pts.length < 2) return null;
      var xs = pts.map(function (p) { return p[0]; });
      var ys = pts.map(function (p) { return p[1]; });
      var minX = Math.min.apply(null, xs);
      var minY = Math.min.apply(null, ys);
      var el = inkBase(o, "freedraw", minX, minY, idx);
      el.points = pts.map(function (p) { return [p[0] - minX, p[1] - minY]; });
      el.pressures = pts.map(function () { return 0.5; });
      el.strokeWidth = Number(o.lineWidth) || (t === "highlighter" ? 18 : 3);
      el.opacity = t === "highlighter" ? 40 : 100;
      el.width = Math.max.apply(null, xs) - minX || 1;
      el.height = Math.max.apply(null, ys) - minY || 1;
      return el;
    }
    if (t === "rect" || t === "ellipse") {
      var sh = inkBase(o, t === "rect" ? "rectangle" : "ellipse", 0, 0, idx);
      sh.width = Math.max(4, Number(o.w) || 80);
      sh.height = Math.max(4, Number(o.h) || 60);
      sh.strokeWidth = Number(o.lineWidth) || 2;
      return sh;
    }
    if (t === "line" || t === "arrow") {
      var x1 = Number(o.x1) || 0, y1 = Number(o.y1) || 0;
      var x2 = (o.x2 !== undefined ? Number(o.x2) : x1 + 80);
      var y2 = (o.y2 !== undefined ? Number(o.y2) : y1);
      var ln = inkBase(o, t, x1, y1, idx);
      ln.points = [[0, 0], [x2 - x1, y2 - y1]];
      ln.width = Math.abs(x2 - x1) || 1;
      ln.height = Math.abs(y2 - y1) || 1;
      ln.strokeWidth = Number(o.lineWidth) || 2;
      if (t === "arrow") ln.endArrowhead = "arrow";
      return ln;
    }
    if (t === "text") {
      var tx = inkBase(o, "text", 0, 0, idx);
      tx.width = 240; tx.height = 60;
      tx.text = String(o.text || "");
      tx.originalText = tx.text;
      tx.fontSize = Number(o.fontSize) || 18;
      tx.fontFamily = FONT;
      tx.textAlign = "left";
      tx.verticalAlign = "top";
      tx.autoResize = true;
      return tx;
    }
    if (t === "sticky") {
      var st = inkBase(o, "rectangle", 0, 0, idx);
      st.width = Number(o.w) || 160;
      st.height = Number(o.h) || 120;
      st.backgroundColor = o.bg || "#fef9c3";
      return st;
    }
    if (t === "image" && typeof o.src === "string" && o.src.indexOf("data:") === 0) {
      var fid = "f-" + String(o.id || idx);
      var im = inkBase(o, "image", 0, 0, idx);
      im.width = Number(o.w) || 220;
      im.height = Number(o.h) || 160;
      im.fileId = fid;
      im.scale = [1, 1];
      im._nebFile = { id: fid, mimeType: "image/png", dataURL: o.src };
      return im;
    }
    var label = String(o.title || o.type || "file");
    var ph = inkBase(o, "rectangle", 0, 0, idx);
    ph.width = Number(o.w) || 220;
    ph.height = Number(o.h) || 64;
    ph.strokeStyle = "dashed";
    ph.customData = { neb: "ink", legacy: t, label: label };
    var pt = inkBase(o, "text", (Number(o.x) || 0) + 12, (Number(o.y) || 0) + 18, idx + "t");
    pt.width = ph.width - 24; pt.height = 30;
    pt.text = label.slice(0, 60);
    pt.originalText = pt.text;
    pt.fontSize = 15;
    pt.fontFamily = FONT;
    pt.textAlign = "left";
    pt.verticalAlign = "top";
    pt.containerId = ph.id;
    ph.boundElements = [{ type: "text", id: pt.id }];
    return [ph, pt];
  }

  function sceneToPersist(elements) {
    var moves = [];
    var ink = [];
    (elements || []).forEach(function (el) {
      if (!el || el.isDeleted) return;
      var neb = el.customData && el.customData.neb;
      if (neb === "node") {
        if (el.type === "rectangle") moves.push({ id: el.customData.id, x: Math.round(el.x), y: Math.round(el.y) });
        return;
      }
      if (neb === "edge") return;
      var copy = {};
      for (var k in el) copy[k] = el[k];
      delete copy._nebFile;
      ink.push(copy);
    });
    return { moves: moves, ink: ink };
  }

  return {
    boardToScene: boardToScene,
    nodeToElements: function (node, idx) {
      var built = nodeRect(node, idx || 0);
      return [built.rect, built.label];
    },
    sceneToPersist: sceneToPersist,
    cardSize: function (text) { return { w: CARD_W, h: estimateHeight(text) }; },
  };
})();
