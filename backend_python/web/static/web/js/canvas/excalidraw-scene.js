window.NebScene = (function () {
  var CARD_W = 360;
  var FONT = 6;
  var FONT_PX = 18;
  var EDGE_COLOR = "#8fa0b8";
  var CARD_BG = "#ffffff";
  var CARD_INK = "#1e293b";

  var KIND_STROKE = {
    ai: "#1d4ed8", note: "#b45309", question: "#7c3aed", source: "#0f766e",
    comparison: "#be185d", practice: "#15803d", summary: "#475569", task: "#c2410c",
    decision: "#6d28d9", warning: "#dc2626",
  };

  var measureCtx = null;
  function measurer() {
    if (!measureCtx) {
      try { measureCtx = document.createElement("canvas").getContext("2d"); } catch (e) { measureCtx = null; }
    }
    return measureCtx;
  }

  function stripMd(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/(\*\*|__)(.*?)\1/g, "$2")
      .replace(/(^|\s)[*_]([^*_]+)[*_](\s|$)/g, "$1$2$3")
      .replace(/`([^`]+)`/g, "$1")
      .replace(/^#{1,6}\s+/gm, "")
      .replace(/^>\s?/gm, "")
      .replace(/^\s*[-*+]\s+/gm, "• ")
      .replace(/^\s*\d+[.)]\s+/gm, "")
      .replace(/\r/g, "")
      .replace(/[ \t]+/g, " ")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  function wrapLines(text, maxWidth) {
    var ctx = measurer();
    var out = [];
    String(text).split("\n").forEach(function (para) {
      if (!para.trim()) { out.push(""); return; }
      if (!ctx) {
        var approx = Math.max(12, Math.floor(maxWidth / (FONT_PX * 0.52)));
        for (var i = 0; i < para.length; i += approx) out.push(para.slice(i, i + approx));
        return;
      }
      ctx.font = FONT_PX + 'px Poppins, sans-serif';
      var words = para.split(/\s+/);
      var line = "";
      words.forEach(function (w) {
        var trial = line ? line + " " + w : w;
        if (ctx.measureText(trial).width > maxWidth && line) {
          out.push(line);
          line = w;
        } else {
          line = trial;
        }
      });
      if (line) out.push(line);
    });
    return out;
  }

  function cardText(node) {
    var title = stripMd(node.title || node.prompt || "Untitled").slice(0, 120);
    var content = node.content || {};
    var summary = stripMd(content.summary || node.prompt || "").slice(0, 500);
    if (summary === title) summary = "";
    return { title: title || "Untitled", summary: summary };
  }

  function layoutCard(title, summary) {
    var inner = CARD_W - 64;
    var titleLines = wrapLines(title, inner).slice(0, 2);
    var bodyLines = [];
    if (summary) {
      bodyLines = wrapLines(summary, inner).slice(0, 9);
      if (wrapLines(summary, inner).length > 9) bodyLines[bodyLines.length - 1] += " …";
    }
    var h = 30 + titleLines.length * 27 + (bodyLines.length ? 12 + bodyLines.length * 24 : 0) + 26;
    h = Math.min(520, Math.max(180, h));
    var text = titleLines.join("\n") + (bodyLines.length ? "\n\n" + bodyLines.join("\n") : "");
    return { h: h, text: text };
  }

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

  function nodeRect(node, idx) {
    var parts = cardText(node);
    var laid = layoutCard(parts.title, parts.summary);
    var x = Number(node.x) || 0;
    var y = Number(node.y) || 0;
    var rect = base(String(node.id), "rectangle", x, y, idx);
    rect.width = CARD_W;
    rect.height = laid.h;
    rect.strokeColor = KIND_STROKE[node.kind] || KIND_STROKE.ai;
    rect.backgroundColor = CARD_BG;
    rect.strokeWidth = 3;
    rect.customData = { neb: "node", id: String(node.id) };
    var label = base(String(node.id) + ":t", "text", x + 32, y + 30, idx + "t");
    label.width = CARD_W - 64;
    label.height = laid.h - 60;
    label.strokeColor = CARD_INK;
    label.backgroundColor = "transparent";
    label.fontSize = FONT_PX;
    label.fontFamily = FONT;
    label.textAlign = "left";
    label.verticalAlign = "top";
    label.text = laid.text;
    label.originalText = laid.text;
    label.autoResize = false;
    label.lineHeight = 1.3;
    label.containerId = rect.id;
    label.customData = { neb: "node", id: String(node.id) };
    rect.boundElements = [{ type: "text", id: label.id }];
    return { rect: rect, label: label, h: laid.h };
  }

  function nodeEdge(node, pos) {
    if (!node.parentId || !pos[node.parentId] || !pos[node.id]) return null;
    var p = pos[node.parentId];
    var c = pos[node.id];
    var x1, y1, x2, y2;
    if (c.y >= p.y + p.h - 60) {
      x1 = p.x + CARD_W / 2; y1 = p.y + p.h;
      x2 = c.x + CARD_W / 2; y2 = c.y;
    } else if (c.y + c.h <= p.y + 60) {
      x1 = p.x + CARD_W / 2; y1 = p.y;
      x2 = c.x + CARD_W / 2; y2 = c.y + c.h;
    } else if (c.x >= p.x + CARD_W - 60) {
      x1 = p.x + CARD_W; y1 = p.y + p.h / 2;
      x2 = c.x; y2 = c.y + c.h / 2;
    } else {
      x1 = p.x; y1 = p.y + p.h / 2;
      x2 = c.x + CARD_W; y2 = c.y + c.h / 2;
    }
    var edge = base("e" + String(node.id), "arrow", x1, y1, "e" + pos[node.id].idx);
    edge.width = Math.abs(x2 - x1) || 1;
    edge.height = Math.abs(y2 - y1) || 1;
    edge.points = [[0, 0], [x2 - x1, y2 - y1]];
    edge.strokeColor = EDGE_COLOR;
    edge.strokeWidth = 2;
    edge.startBinding = { elementId: String(node.parentId), focus: 0, gap: 10 };
    edge.endBinding = { elementId: String(node.id), focus: 0, gap: 10 };
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
    cardSize: function (text) { return { w: CARD_W, h: layoutCard("", text || "").h }; },
  };
})();
