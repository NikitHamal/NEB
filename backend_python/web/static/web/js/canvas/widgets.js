(function () {
  "use strict";

  var CATALOG = [
    { id: "w-filter", kind: "filter-table", title: "Filter table", w: 440, h: 276 },
    { id: "w-records", kind: "records", title: "Records", w: 680, h: 340 },
    { id: "w-flow", kind: "flow", title: "Flow", w: 440, h: 320 },
    { id: "w-insights", kind: "insights", title: "Insights", w: 344, h: 420 },
    { id: "w-tune", kind: "tune", title: "Fine-tune", w: 248, h: 292 },
    { id: "w-selbar", kind: "selbar", title: "Selection AI", w: 460, h: 156 },
    { id: "w-quiz", kind: "quiz", title: "Quiz", w: 320, h: 268 },
    { id: "w-flash", kind: "flash", title: "Flashcards", w: 292, h: 228 },
    { id: "w-timeline", kind: "timeline", title: "Timeline", w: 340, h: 248 },
    { id: "w-poll", kind: "poll", title: "Poll", w: 300, h: 248 }
  ];

  var HTML_TYPES = { widget: 1, card: 1, sticky: 1, file: 1 };
  var BOX_TYPES = { widget: 1, card: 1, sticky: 1, file: 1, image: 1, rect: 1, ellipse: 1, text: 1 };

  var TAG = {
    Gelato: "#9a5cff", Seasonal: "#d69e2e", B2C: "#68d391", Cafe: "#f56565",
    Vegan: "#68d391", Local: "#38a169", B2B: "#dd6b20", Wholesale: "#dd6b20",
    Sorbet: "#ed64a6", "Dairy-free": "#0bc5ea", Catering: "#d53f8c", Imports: "#dd6b20"
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      if (c === "&") return "&" + "amp;";
      if (c === "<") return "&" + "lt;";
      if (c === ">") return "&" + "gt;";
      if (c === '"') return "&" + "quot;";
      return "&#39;";
    });
  }

  function defFor(idOrKind) {
    for (var i = 0; i < CATALOG.length; i++) {
      if (CATALOG[i].kind === idOrKind || CATALOG[i].id === idOrKind) return CATALOG[i];
    }
    return CATALOG[0];
  }

  function camOf(board) {
    var c = board.camera || board.view || { x: 0, y: 0, zoom: 1 };
    return { x: c.x || 0, y: c.y || 0, zoom: c.zoom != null ? c.zoom : (c.scale != null ? c.scale : 1) };
  }
  function xyOf(board, e) {
    if (typeof board.xy === "function") return board.xy(e);
    if (typeof board._getCanvasXY === "function") return board._getCanvasXY(e);
    var host = board.root || board.container;
    var r = host.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }
  function s2wOf(board, x, y) {
    if (typeof board.s2w === "function") return board.s2w(x, y);
    if (typeof board._screenToWorld === "function") return board._screenToWorld(x, y);
    var cam = camOf(board);
    return { x: (x - cam.x) / cam.zoom, y: (y - cam.y) / cam.zoom };
  }
  function persistOf(board) {
    if (typeof board.persist === "function") board.persist();
    else if (typeof board._save === "function") board._save();
    else if (typeof board._updateElement === "function" && selIndex(board) >= 0) board._updateElement(selIndex(board), board.elements[selIndex(board)]);
  }

  function selIndex(board) {
    if (typeof board.selectedIdx === "number") return board.selectedIdx;
    if (typeof board.selected === "number") return board.selected;
    return -1;
  }

  function setSel(board, idx) {
    if ("selectedIdx" in board) {
      board.selectedIdx = idx;
      board.selected = idx >= 0 ? board.elements[idx] : null;
    } else {
      board.selected = idx;
    }
  }

  function mark(board) {
    board.dirty = true;
    if (typeof board.markDirty === "function") board.markDirty();
  }

  function spark(values, color) {
    var w = 300, h = 96, min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    var d = values.map(function (v, i) {
      var x = (i / (values.length - 1)) * w;
      var y = 10 + (h - 20) - ((v - min) / ((max - min) || 1)) * (h - 20);
      return x + "," + y;
    }).join(" ");
    return '<svg viewBox="0 0 ' + w + " " + h + '" width="100%" height="100%" preserveAspectRatio="none"><polyline fill="none" stroke="' + color + '" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" points="' + d + '"/></svg>';
  }

  function dualSpark(a, b, ca, cb) {
    return spark(a, ca).replace("</svg>", spark(b, cb).replace(/<svg[^>]*>/, "").replace("</svg>", "") + "</svg>");
  }

  /* ── builders ── */
  function htmlFilter(el) {
    var filter = (el.state && el.state.filter) || "all";
    var filters = [
      { key: "all", label: "All", count: 5 },
      { key: "todo", label: "To do", dot: "#f09a2f", count: 2 },
      { key: "progress", label: "In Progress", dot: "#16a6c7", count: 2 },
      { key: "done", label: "Completed", dot: "#25a878", count: 1 }
    ];
    var rows = [
      { task: "Restock mango sorbet", date: "Dec 03", status: "todo", owner: "Mango Moon Gelato" },
      { task: "Churn black sesame", date: "Sep 22", status: "progress", owner: "Kumo Creamery" },
      { task: "Print summer menu", date: "Jan 02", status: "todo", owner: "Coral Coast Sorbet" },
      { task: "Taste-test batch 42", date: "Nov 08", status: "progress", owner: "Maple Orbit" },
      { task: "Order waffle cones", date: "Apr 14", status: "done", owner: "Aurora Scoops" }
    ];
    var pills = { todo: "To do", progress: "In Progress", done: "Completed" };
    var chips = filters.map(function (f) {
      return '<button type="button" class="w-chip' + (filter === f.key ? " is-on" : "") + '" data-ui data-filter="' + f.key + '" aria-pressed="' + (filter === f.key) + '">' +
        (f.dot ? '<span class="w-dot" style="background:' + f.dot + '"></span>' : "") +
        esc(f.label) + '<span class="w-count">' + f.count + "</span></button>";
    }).join("");
    var body = rows.map(function (r) {
      var shown = filter === "all" || r.status === filter;
      return '<div class="w-fwrap' + (shown ? "" : " is-hide") + '"><div class="w-frow body"><span><span class="trunc">' + esc(r.task) + "</span></span><span>" + esc(r.date) + '</span><span><span class="w-pill ' + r.status + '">' + pills[r.status] + '</span></span><span class="trunc">' + esc(r.owner) + "</span></div></div>";
    }).join("");
    return '<div class="w-card w-filter"><div class="w-filter-chips">' + chips + '</div><div class="w-filter-table"><div class="w-frow head"><span>Task name</span><span>Date</span><span>Status</span><span>Advisor</span></div>' + body + "</div></div>";
  }

  function htmlRecords() {
    var rows = [
      { name: "Aurora Scoops — Reykjavík", tags: ["Gelato", "Seasonal"], last: "9 days ago", str: "Very strong", col: "#25a878", link: true },
      { name: "Kumo Creamery — Tokyo", tags: ["B2C", "Cafe", "Vegan"], last: "3 weeks ago", str: "Very strong", col: "#25a878", link: true },
      { name: "Sol y Nieve — Buenos Aires", tags: ["Gelato", "Local"], last: "2 months ago", str: "Weak", col: "#f09a2f", link: true },
      { name: "Maple Orbit — Montréal", tags: ["B2B", "Wholesale"], last: "15 days ago", str: "Weak", col: "#f09a2f", link: true },
      { name: "Blue Fig Gelato — Florence", tags: ["Gelato", "Cafe"], last: "over 1 year", str: "Very weak", col: "#e53e3e", link: true },
      { name: "Cloudberry Cone — Helsinki", tags: ["Dairy-free", "Seasonal"], last: "No contact", str: "None", col: "#78849c", link: false },
      { name: "Coral Coast Sorbet — Honolulu", tags: ["Sorbet", "Local"], last: "9 days ago", str: "Very strong", col: "#25a878", link: true },
      { name: "Alpine Churn — Zürich", tags: ["B2B", "Gelato"], last: "4 days ago", str: "Very strong", col: "#25a878", link: true }
    ];
    var body = rows.map(function (r) {
      var tags = r.tags.map(function (t) {
        return '<span class="w-tag" style="--tag-base:' + (TAG[t] || "#78849c") + '">' + esc(t) + "</span>";
      }).join("");
      return '<div class="w-rrow"><span class="w-check"></span><span class="trunc" style="font-weight:500">' + esc(r.name) + '</span><span class="w-tags">' + tags + '</span><span>' + esc(r.last) + '</span><span class="w-str"><span class="w-dot" style="background:' + r.col + '"></span>' + r.str + '</span><span class="w-muted">' + (r.link ? "↗" : "—") + "</span></div>";
    }).join("");
    return '<div class="w-card w-records"><div class="w-rhead"><b>Companies</b><span class="w-muted">' + rows.length + ' rows</span></div><div class="w-rtable"><div class="w-rrow head"><span></span><span>Company</span><span>Categories</span><span>Last</span><span>Strength</span><span>Links</span></div>' + body + '</div><div class="w-foot"><span><b>8</b> count</span><span>67% average</span><span>6 links</span></div></div>';
  }

  function htmlFlow(el) {
    var st = el.state || {};
    var flavor = st.flavor || "Rocky Road";
    var prop = st.prop || "flavor";
    var open = st.open || "";
    function chip(id, value, opts) {
      opts = opts || [];
      var menu = "";
      if (open === id) {
        menu = '<div class="w-menu" data-ui>' + opts.map(function (n) {
          return '<button type="button" data-ui data-pick="' + id + '" data-val="' + esc(n) + '">' + esc(n) + "</button>";
        }).join("") + "</div>";
      }
      return '<span class="w-selchip" data-ui><button type="button" data-ui data-open="' + id + '">' + esc(value) + ' <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="m6 9 6 6 6-6"/></svg></button>' + menu + "</span>";
    }
    return '<div class="w-flow">' +
      '<svg class="w-flow-svg" viewBox="0 0 440 320" preserveAspectRatio="none"><path d="M 220 108 C 220 148, 220 156, 220 176" fill="none" stroke="#c5cdd8" stroke-width="1.25"/></svg>' +
      '<div class="w-flow-node" style="left:70px;top:16px;width:300px"><span class="w-kind k-purple">Trigger</span>' +
      '<div class="w-step"><span class="w-ico i-purple"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m7 11 4.08 10.35a1 1 0 0 0 1.84 0L17 11"/><path d="M17 7A5 5 0 0 0 7 7"/><path d="M17 7a2 2 0 0 1 0 4H7a2 2 0 0 1 0-4"/></svg></span><span><b>New order created</b><span class="w-muted">Trigger when a new order is created</span></span></div></div>' +
      '<div class="w-flow-node" style="left:42px;top:176px;width:356px"><span class="w-kind k-amber">If / Else</span>' +
      '<div class="w-cond" data-ui><div class="w-cline">If <span class="w-src" data-ui>order</span> ' + chip("prop", prop, ["flavor", "topping", "size", "scoops"]) + " is " + chip("val", flavor, ["Rocky Road", "Mint Chip", "Pistachio", "Bubblegum"]) + "</div>" +
      '<div class="w-cline">and <span class="w-src" data-ui>order</span> topping is Brown butter bourbon</div></div></div></div>';
  }

  function htmlInsights(el) {
    var page = (el.state && el.state.page) || 0;
    var metric = (el.state && el.state.metric) || "spend";
    var pages = [
      {
        prose: 'The worst performer in your <span class="w-ent"><i style="background:#f09a2f"></i>Creamery</span> is Rocky Road — down <code class="bad">-6%</code>.',
        pill: "Should I rebalance flavors?",
        inner: '<div class="w-ins-card"><div class="w-pair"><div><span class="w-muted"><i class="w-dot" style="background:#f68f3c"></i> Mint Chip</span><b class="bad">-4.41%</b><code class="bad">-$2,377.66</code></div><div><span class="w-muted"><i class="w-dot" style="background:#3d9aff"></i> Pistachio</span><b class="good">+1.15%</b><code class="good">+$617.22</code></div></div><div class="w-spark">' + dualSpark([-2.9, -3.4, -3.05, -3.86, -3.52, -4.1, -3.82, -4.41], [0.22, 0.58, 0.42, 0.91, 0.76, 1.08, 0.96, 1.15], "#f68f3c", "#3d9aff") + "</div></div>"
      },
      {
        prose: 'Unusually high freezer bill on <b>Dec 13</b> — <code class="bad">+$1,834.66</code> above average.',
        pill: "Get tips on cutting freezer costs",
        inner: '<div class="w-ins-card"><div class="w-ins-row"><span class="w-muted">High freezer spend</span><span class="w-seg-mini"><button type="button" data-ui data-metric="spend" class="' + (metric === "spend" ? "is-on" : "") + '">Spend</button><button type="button" data-ui data-metric="usage" class="' + (metric === "usage" ? "is-on" : "") + '">Usage</button></span></div><div class="w-spark">' + spark(metric === "usage" ? [18, 19, 17, 21, 22, 58, 81, 96] : [274, 289, 264, 307, 331, 1210, 1718, 2112], "#ee5c61") + '</div><div class="w-metric-line"><b>$2,112 spent</b> <code class="bad">+$1,834.66</code> <span class="w-muted">vs 3 months</span></div></div>'
      },
      {
        prose: 'You’re heavily invested in <span class="w-ent"><i style="background:#f09a2f"></i>Vanilla</span> — it’s <b>72.5%</b> of your case.',
        pill: "If we look at seasonals, what changes?",
        inner: '<div class="w-ins-card"><div class="w-muted">Vanilla allocation</div><b class="w-hero">$51,785</b><div class="w-alloc"><i style="width:72.5%;background:#f09a2f"></i><i style="width:22.8%;background:#c5cdd8"></i><i style="width:4.7%;background:#e2e6f0"></i></div><div class="w-legend"><span><i class="w-dot" style="background:#f09a2f"></i>VAN 72.5%</span><span><i class="w-dot" style="background:#c5cdd8"></i>CHOC 22.8%</span><span><i class="w-dot" style="background:#e2e6f0"></i>MINT 4.7%</span></div></div>'
      }
    ];
    var p = pages[page % 3];
    return '<div class="w-card w-ins"><div class="w-ins-top"><span><b>Insights</b> <span class="w-muted">3</span></span><span class="w-ins-nav">' +
      '<button type="button" data-ui data-ins="-1" aria-label="Previous">‹</button><button type="button" data-ui data-ins="1" aria-label="Next">›</button></span></div>' +
      "<p>" + p.prose + "</p>" + p.inner +
      '<button type="button" class="w-ask" data-ui>' + esc(p.pill) + "</button></div>";
  }

  function htmlTune(el) {
    var s = el.state || {};
    var w = s.w != null ? s.w : 324;
    var h = s.h != null ? s.h : 96;
    var r = s.r != null ? s.r : 28;
    var o = s.o != null ? s.o : 100;
    var seg = s.seg || 0;
    var type = s.type || "Select type";
    var done = seg !== 0 || w !== 324 || h !== 96 || r !== 28 || o !== 100 || type !== "Select type";
    function scrub(key, label, val, suf, def) {
      return '<div class="w-scrub' + (val !== def ? " is-on" : "") + '"><label data-ui data-scrub="' + key + '">' + label + '</label><input data-ui data-field="' + key + '" value="' + val + '">' + (suf ? '<span class="w-muted">' + suf + "</span>" : "") + "</div>";
    }
    return '<div class="w-card w-tune"><div class="w-tune-bar"><span>Flavor card</span>' +
      (done ? '<span class="good" style="font-size:12px">Edited</span>' : '<span class="w-shimmer">Adjust</span>') + "</div>" +
      '<div class="w-tune-body"><p>Layout</p><div class="w-seg3"><i style="transform:translateX(' + seg * 100 + '%)"></i>' +
      '<button type="button" data-ui data-seg="0" class="' + (seg === 0 ? "is-on" : "") + '" aria-label="row">▭</button>' +
      '<button type="button" data-ui data-seg="1" class="' + (seg === 1 ? "is-on" : "") + '" aria-label="col">▯</button>' +
      '<button type="button" data-ui data-seg="2" class="' + (seg === 2 ? "is-on" : "") + '" aria-label="grid">▦</button></div>' +
      '<div class="w-scrub-grid">' + scrub("w", "W", w, "", 324) + scrub("h", "H", h, "", 96) + scrub("r", "Radius", r, "", 28) + scrub("o", "Opacity", o, "%", 100) + "</div></div>" +
      '<div class="w-tune-foot"><span>Type</span><select class="w-type" data-ui data-type="1"><option' + (type === "Select type" ? " selected" : "") + ">Select type</option><option" + (type === "Seasonal" ? " selected" : "") + ">Seasonal</option><option" + (type === "Classic" ? " selected" : "") + ">Classic</option><option" + (type === "Limited" ? " selected" : "") + ">Limited</option></select></div></div>";
  }

  function htmlSelbar(el) {
    var mode = (el.state && el.state.mode) || "idle";
    var picked = "Churn it first thing Saturday so the batch has time to firm up before the afternoon rush.";
    var rewrite = "Churn pistachio first thing Saturday so the batch has time to fully firm before the afternoon rush.";
    var text = mode === "idle" || mode === "thinking" ? picked : rewrite;
    var bar;
    if (mode === "result") {
      bar = '<button type="button" class="primary" data-ui data-keep="1">Keep</button><button type="button" data-ui data-keep="1">Discard</button>';
    } else if (mode === "thinking") {
      bar = '<span class="w-spin"></span><span class="w-muted" style="padding:0 8px">Improving…</span>';
    } else {
      bar = '<input data-ui placeholder="Describe edits"><span class="sep"></span><button type="button" data-ui data-act="Explain">Explain</button><button type="button" data-ui data-act="Improve">Improve</button>';
    }
    return '<div class="w-card w-selbar"><p>Pistachio holds the top slot all weekend. <mark>' + esc(text) + '</mark></p><div class="w-ai">' + bar + "</div></div>";
  }

  function htmlQuiz(el) {
    var pick = el.state && el.state.pick;
    var opts = ["Next token prediction", "An inner simulator of the world", "A larger vocabulary", "A search index"];
    var answer = 1;
    var buttons = opts.map(function (o, i) {
      var cls = pick == null ? "" : i === answer ? " ok" : i === pick ? " no" : "";
      return '<button type="button" class="w-opt' + cls + '" data-ui data-quiz="' + i + '">' + esc(o) + "</button>";
    }).join("");
    var foot = pick == null ? "" : (pick === answer ? '<div class="w-ok-msg">Correct — a world model predicts the next state.</div>' : '<div class="w-no-msg">Not quite. Think simulation, not autocomplete.</div>');
    return '<div class="w-card w-quiz"><div class="q">What is a world model?</div>' + buttons + foot + "</div>";
  }

  function htmlFlash(el) {
    var i = (el.state && el.state.i) || 0;
    var flip = !!(el.state && el.state.flip);
    var cards = [
      { q: "World model", a: "A compact inner simulator that predicts the next state — not the next token." },
      { q: "Failure mode", a: "When the inner map drifts, actions look confident and land wrong." },
      { q: "Retrieval", a: "Draw the loop from memory. Name the signal that proves the model is wrong." }
    ];
    var c = cards[i % cards.length];
    return '<div class="w-card w-flash"><div class="w-face' + (flip ? " is-back" : "") + '" data-ui data-flip="1">' + esc(flip ? c.a : c.q) + '</div><div class="w-flash-nav"><button type="button" data-ui data-flash="-1">Prev</button><span>' + ((i % 3) + 1) + ' / 3</span><button type="button" data-ui data-flash="1">Next</button></div></div>';
  }

  function htmlTimeline() {
    var items = [
      { t: "Sense", d: "Read the board and name the current state." },
      { t: "Predict", d: "The inner model forecasts the next move." },
      { t: "Act", d: "Place a card, a trap, or a practice prompt." },
      { t: "Update", d: "Tighten the map from what actually happened." }
    ];
    return '<div class="w-card w-time"><h4>Action loop</h4>' + items.map(function (it) {
      return '<div class="w-titem"><i></i><div><b>' + esc(it.t) + '</b><div class="w-muted">' + esc(it.d) + "</div></div></div>";
    }).join("") + "</div>";
  }

  function htmlPoll(el) {
    var votes = (el.state && el.state.votes) || [12, 7, 4];
    var opts = ["Draw the loop from memory", "Name one failure mode", "Teach it to a peer"];
    var total = votes[0] + votes[1] + votes[2] || 1;
    var rows = opts.map(function (o, i) {
      var pct = Math.round((votes[i] / total) * 100);
      return '<button type="button" class="w-opt w-poll-row" data-ui data-poll="' + i + '"><span class="w-poll-lab"><span>' + esc(o) + '</span><span class="w-muted">' + pct + '%</span></span><span class="w-bar"><span style="width:' + pct + '%"></span></span></button>';
    }).join("");
    return '<div class="w-card w-poll"><b>Best next practice?</b>' + rows + "</div>";
  }

  function htmlCard(el) {
    return '<div class="w-card w-note"><i class="w-accent"></i><div class="w-k">' + esc((el.kind || "Card").toUpperCase()) + '</div><div class="w-t" data-edit="title">' + esc(el.title || "") + '</div><div class="w-b" data-edit="body">' + esc(el.body || "") + "</div></div>";
  }

  function htmlSticky(el) {
    return '<div class="w-sticky" style="background:' + esc(el.bg || el.bgColor || "#fff9c4") + '"><div data-edit="text">' + esc(el.text || "") + "</div></div>";
  }

  function htmlFile(el) {
    return '<div class="w-card w-filechip"><b>' + esc(el.title || "File") + '</b><span class="w-muted">' + esc(el.kind || "PDF") + "</span></div>";
  }

  var BUILD = {
    "filter-table": htmlFilter,
    records: htmlRecords,
    flow: htmlFlow,
    insights: htmlInsights,
    tune: htmlTune,
    selbar: htmlSelbar,
    quiz: htmlQuiz,
    flash: htmlFlash,
    timeline: htmlTimeline,
    poll: htmlPoll
  };

  function renderEl(el) {
    if (el.type === "widget") {
      var fn = BUILD[el.kind];
      return fn ? fn(el) : '<div class="w-card">Unknown</div>';
    }
    if (el.type === "card") return htmlCard(el);
    if (el.type === "sticky") return htmlSticky(el);
    if (el.type === "file") return htmlFile(el);
    return "";
  }

  /* ── overlay controller ── */
  function CanvasWidgets(board) {
    this.board = board;
    this.el = document.createElement("div");
    this.el.className = "cw-world is-interact";
    (board.root || board.container).appendChild(this.el);
    this.sel = document.createElement("div");
    this.sel.className = "cw-sel";
    this.sel.hidden = true;
    this.sel.innerHTML = '<i class="cw-handle h-nw" data-h="nw"></i><i class="cw-handle h-n" data-h="n"></i><i class="cw-handle h-ne" data-h="ne"></i><i class="cw-handle h-e" data-h="e"></i><i class="cw-handle h-se" data-h="se"></i><i class="cw-handle h-s" data-h="s"></i><i class="cw-handle h-sw" data-h="sw"></i><i class="cw-handle h-w" data-h="w"></i>';
    this.el.appendChild(this.sel);
    this.nodes = {};
    this._bind();
  }

  CanvasWidgets.prototype._item = function () {
    var i = selIndex(this.board);
    if (i < 0) return null;
    return this.board.elements[i] || null;
  };

  CanvasWidgets.prototype._find = function (id) {
    var list = this.board.elements;
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return { el: list[i], i: i };
    return null;
  };

  CanvasWidgets.prototype._bind = function () {
    var self = this, board = this.board;
    this.el.addEventListener("pointerdown", function (e) {
      var handle = e.target.closest("[data-h]");
      var node = e.target.closest(".cw-node");
      var ui = e.target.closest("[data-ui]");
      var edit = e.target.closest("[data-edit]");
      if (handle) {
        var item = self._item();
        if (!item || item.w == null) return;
        var xy = xyOf(board, e);
        board.resizeDrag = { h: handle.getAttribute("data-h"), start: s2wOf(board, xy.x, xy.y), orig: { x: item.x, y: item.y, w: item.w, h: item.h } };
        try { handle.setPointerCapture(e.pointerId); } catch (err) {}
        e.stopPropagation(); e.preventDefault(); return;
      }
      if (edit && e.detail === 2) {
        e.stopPropagation();
        self._startEdit(edit);
        return;
      }
      if (ui) {
        var host = ui.closest(".cw-node");
        if (host) {
          var hitUi = self._find(host.getAttribute("data-id"));
          if (hitUi) setSel(board, hitUi.i);
        }
        e.stopPropagation();
        self._onUi(ui, e);
        return;
      }
      if (node) {
        var hit = self._find(node.getAttribute("data-id"));
        if (!hit) return;
        setSel(board, hit.i);
        if (board.tool === "select" || !board.tool) {
          var w = s2wOf(board, xyOf(board, e).x, xyOf(board, e).y);
          board.drag = { start: w, orig: JSON.parse(JSON.stringify(hit.el)), moved: false };
        }
        mark(board);
        e.stopPropagation();
      }
    });
    this.el.addEventListener("dblclick", function (e) {
      var edit = e.target.closest("[data-edit]");
      if (!edit) return;
      e.stopPropagation();
      self._startEdit(edit);
    });
    window.addEventListener("pointermove", function (e) {
      if (self._scrub) {
        var d = self._scrub;
        var n = Math.round(d.v + (e.clientX - d.x) / 2);
        n = Math.max(d.min, Math.min(d.max, n));
        d.el.state[d.key] = n;
        mark(board);
        return;
      }
      if (board.resizeDrag) {
        var item = self._item(); if (!item) return;
        var w = s2wOf(board, xyOf(board, e).x, xyOf(board, e).y);
        var o = board.resizeDrag.orig, h = board.resizeDrag.h;
        var x = o.x, y = o.y, ww = o.w, hh = o.h;
        var dx = w.x - board.resizeDrag.start.x, dy = w.y - board.resizeDrag.start.y;
        var minW = item.type === "widget" ? 180 : 80;
        var minH = item.type === "widget" ? 90 : 48;
        if (h.indexOf("e") >= 0) ww = Math.max(minW, o.w + dx);
        if (h.indexOf("s") >= 0) hh = Math.max(minH, o.h + dy);
        if (h.indexOf("w") >= 0) { ww = Math.max(minW, o.w - dx); x = o.x + (o.w - ww); }
        if (h.indexOf("n") >= 0) { hh = Math.max(minH, o.h - dy); y = o.y + (o.h - hh); }
        item.x = x; item.y = y; item.w = ww; item.h = hh;
        mark(board); e.preventDefault();
        return;
      }
      if (board.drag && board.drag.orig && selIndex(board) >= 0) {
        var el = board.elements[selIndex(board)];
        if (!el || !HTML_TYPES[el.type]) return;
        var ww2 = s2wOf(board, xyOf(board, e).x, xyOf(board, e).y);
        var ddx = ww2.x - board.drag.start.x, ddy = ww2.y - board.drag.start.y;
        if (!board.drag.moved && Math.hypot(ddx, ddy) < 3) return;
        board.drag.moved = true;
        var orig = board.drag.orig;
        el.x = orig.x + ddx; el.y = orig.y + ddy;
        mark(board);
      }
    });
    window.addEventListener("pointerup", function () {
      self._scrub = null;
      if (board.resizeDrag) { board.resizeDrag = null; persistOf(board); }
      if (board.drag && board.drag.orig && HTML_TYPES[(board.elements[selIndex(board)] || {}).type]) {
        board.drag = null; persistOf(board);
      }
    });
  };

  CanvasWidgets.prototype._startEdit = function (node) {
    var field = node.getAttribute("data-edit");
    var wrap = node.closest(".cw-node");
    if (!wrap || !field) return;
    var hit = this._find(wrap.getAttribute("data-id"));
    if (!hit) return;
    node.contentEditable = "true";
    node.focus();
    wrap._editing = true;
    var self = this;
    function done() {
      node.contentEditable = "false";
      wrap._editing = false;
      hit.el[field] = node.textContent;
      persistOf(self.board);
      mark(self.board);
      node.removeEventListener("blur", done);
    }
    node.addEventListener("blur", done);
    node.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); node.blur(); }
      e.stopPropagation();
    });
  };

  CanvasWidgets.prototype._onUi = function (ui, e) {
    var node = ui.closest(".cw-node");
    if (!node) return;
    var hit = this._find(node.getAttribute("data-id"));
    if (!hit) return;
    var el = hit.el;
    el.state = el.state || {};
    var f = ui.getAttribute("data-filter");
    if (f) el.state.filter = f;
    var ins = ui.getAttribute("data-ins");
    if (ins) el.state.page = (((el.state.page || 0) + parseInt(ins, 10)) + 3) % 3;
    var metric = ui.getAttribute("data-metric");
    if (metric) el.state.metric = metric;
    var quiz = ui.getAttribute("data-quiz");
    if (quiz != null) el.state.pick = parseInt(quiz, 10);
    var flip = ui.getAttribute("data-flip");
    if (flip) el.state.flip = !el.state.flip;
    var fl = ui.getAttribute("data-flash");
    if (fl) { el.state.i = ((el.state.i || 0) + parseInt(fl, 10) + 3) % 3; el.state.flip = false; }
    var poll = ui.getAttribute("data-poll");
    if (poll != null) {
      el.state.votes = el.state.votes || [12, 7, 4];
      el.state.votes[parseInt(poll, 10)]++;
    }
    var act = ui.getAttribute("data-act");
    if (act) {
      el.state.mode = "thinking";
      var self = this;
      setTimeout(function () { el.state.mode = "result"; mark(self.board); persistOf(self.board); }, 700);
    }
    if (ui.getAttribute("data-keep")) el.state.mode = "idle";
    var seg = ui.getAttribute("data-seg");
    if (seg != null) el.state.seg = parseInt(seg, 10);
    var type = ui.getAttribute("data-type");
    if (type && ui.tagName === "SELECT") el.state.type = ui.value;
    var field = ui.getAttribute("data-field");
    if (field && ui.tagName === "INPUT") el.state[field] = parseInt(ui.value, 10) || 0;
    var scrub = ui.getAttribute("data-scrub");
    if (scrub) {
      this._scrub = { key: scrub, x: e.clientX, v: el.state[scrub] != null ? el.state[scrub] : 0, el: el, min: 0, max: scrub === "o" ? 100 : 999 };
      try { ui.setPointerCapture(e.pointerId); } catch (err) {}
    }
    var open = ui.getAttribute("data-open");
    if (open) el.state.open = el.state.open === open ? "" : open;
    var pick = ui.getAttribute("data-pick");
    if (pick) { el.state[pick === "prop" ? "prop" : "flavor"] = ui.getAttribute("data-val"); el.state.open = ""; }
    mark(this.board);
    persistOf(this.board);
    e.preventDefault();
  };

  CanvasWidgets.prototype.sync = function () {
    var board = this.board, cam = camOf(board);
    this.el.style.transform = "translate(" + cam.x + "px," + cam.y + "px) scale(" + cam.zoom + ")";
    var tool = board.tool || "select";
    var interact = tool === "select" || tool === "pan" || (tool && tool.indexOf("w-") === 0);
    this.el.classList.toggle("is-interact", interact);

    var live = {};
    for (var i = 0; i < board.elements.length; i++) {
      var el = board.elements[i];
      if (!HTML_TYPES[el.type]) continue;
      live[el.id] = true;
      var node = this.nodes[el.id];
      var sig = (el.type || "") + (el.kind || "") + JSON.stringify(el.state || {}) + (el.title || "") + (el.body || "") + (el.text || "") + el.w + "x" + el.h + (el.bg || "");
      if (!node) {
        node = document.createElement("div");
        node.className = "cw-node";
        node.setAttribute("data-id", el.id);
        this.el.appendChild(node);
        this.nodes[el.id] = node;
        node._sig = "";
      }
      node.style.transform = "translate(" + el.x + "px," + el.y + "px)";
      node.style.width = (el.w || 280) + "px";
      node.style.height = (el.h || 180) + "px";
      if (node._sig !== sig && !node._editing) {
        node.innerHTML = renderEl(el);
        node._sig = sig;
      }
    }
    Object.keys(this.nodes).forEach(function (id) {
      if (!live[id]) { this.nodes[id].remove(); delete this.nodes[id]; }
    }, this);

    var item = this._item();
    if (item && item.w != null && BOX_TYPES[item.type]) {
      this.sel.hidden = false;
      this.sel.style.transform = "translate(" + (item.x - 6) + "px," + (item.y - 6) + "px)";
      this.sel.style.width = (item.w + 12) + "px";
      this.sel.style.height = (item.h + 12) + "px";
    } else {
      this.sel.hidden = true;
    }
  };

  CanvasWidgets.create = function (kind, x, y) {
    var def = defFor(kind);
    return { id: Math.random().toString(36).slice(2, 10), type: "widget", kind: def.kind, x: x, y: y, w: def.w, h: def.h, state: {} };
  };

  CanvasWidgets.isHtml = function (el) { return !!(el && HTML_TYPES[el.type]); };
  CanvasWidgets.CATALOG = CATALOG;
  CanvasWidgets.toolIds = CATALOG.map(function (c) { return c.id; });
  window.CanvasWidgets = CanvasWidgets;
})();
