window.NebPanel = (function () {
  var B = null;
  function bridge() {
    if (!B) B = window.NebCanvas;
    return B;
  }
  function $(id) { return document.getElementById(id); }

  function open(kicker, title, html) {
    var p = $("cvPanel");
    if (!p) return;
    $("cvPanelKicker").textContent = kicker;
    $("cvPanelTitle").textContent = title;
    $("cvPanelBody").innerHTML = html;
    p.hidden = false;
    var bd = $("cvPanelBackdrop");
    if (bd) bd.hidden = false;
    wireBody();
  }

  function close() {
    var p = $("cvPanel");
    if (p) p.hidden = true;
    var bd = $("cvPanelBackdrop");
    if (bd) bd.hidden = true;
  }

  function sectionHtml(content) {
    if (!content) return "";
    var out = "";
    if (content.summary) out += '<p class="np-sum">' + bridge().esc(content.summary) + "</p>";
    var secs = Array.isArray(content.sections) ? content.sections.slice(0, 4) : [];
    secs.forEach(function (s) {
      out += '<div class="np-sec"><div class="np-sec-t">' + bridge().esc(s.title || s.type || "") + "</div>";
      if (s.type === "bullets" && Array.isArray(s.items)) {
        out += "<ul>" + s.items.slice(0, 6).map(function (i) { return "<li>" + bridge().esc(typeof i === "string" ? i : (i.text || i.label || "")) + "</li>"; }).join("") + "</ul>";
      } else if (s.type === "cards" && Array.isArray(s.items)) {
        out += "<ul>" + s.items.slice(0, 6).map(function (i) { return "<li><b>" + bridge().esc(i.title || "") + "</b> — " + bridge().esc(i.body || i.text || "") + "</li>"; }).join("") + "</ul>";
      } else if ((s.type === "flow" || s.type === "diagram") && Array.isArray(s.nodes)) {
        out += "<ol>" + s.nodes.slice(0, 8).map(function (n) { return "<li><b>" + bridge().esc(n.label || "") + "</b> " + bridge().esc(n.desc || "") + "</li>"; }).join("") + "</ol>";
      } else if (s.type === "text" && s.body) {
        out += "<p>" + bridge().esc(String(s.body).slice(0, 600)) + "</p>";
      } else if (s.type === "quote" && s.quote) {
        out += "<blockquote>" + bridge().esc(s.quote) + "</blockquote>";
      } else if (s.type === "code" && s.code) {
        out += "<pre>" + bridge().esc(String(s.code).slice(0, 600)) + "</pre>";
      }
      out += "</div>";
    });
    return out;
  }

  function inspect(id) {
    if (String(id).indexOf("@widget:") === 0) return inspectWidget(String(id).slice(8));
    var n = bridge().getNode(id);
    if (!n) return;
    var meta = n.meta || {};
    var html = '<div class="np-kind">' + bridge().esc(n.kind || "ai") + (n.status === "generating" ? " · working…" : "") + "</div>";
    html += '<h3 class="np-title">' + bridge().esc(n.title || n.prompt || "") + "</h3>";
    html += sectionHtml(n.content);
    if (n.error) html += '<p class="np-err">' + bridge().esc(n.error) + "</p>";
    html += '<div class="np-follow"><input id="npFollowInput" placeholder="Ask a follow-up…" autocomplete="off">';
    html += '<button class="md-btn-f" data-action="followup" data-id="' + bridge().esc(n.id) + '">Send</button></div>';
    html += '<div class="np-row">';
    html += '<button data-action="retry" data-id="' + bridge().esc(n.id) + '">Retry</button>';
    html += '<button data-action="dig" data-id="' + bridge().esc(n.id) + '">Dig deeper</button>';
    html += '<button data-action="del" data-id="' + bridge().esc(n.id) + '" class="danger">Delete</button>';
    html += "</div>";
    open("Card", n.title || "Card", html);
  }

  function inspectWidget(elId) {
    var found = null;
    var els = (window.NebExcali && window.NebExcali.getSceneElements()) || [];
    for (var i = 0; i < els.length; i++) {
      if (els[i].id === elId && els[i].customData && els[i].customData.widget) { found = els[i].customData.widget; break; }
    }
    if (!found) { close(); return; }
    var html = '<div class="np-kind">' + bridge().esc(found.kind || "widget") + "</div>";
    html += '<h3 class="np-title">' + bridge().esc(found.topic || "") + "</h3>";
    html += widgetHtml(found.kind, found.content);
    open("Widget", found.kind || "Widget", html);
  }

  function widgetHtml(kind, content) {
    if (!content) return "<p>Empty.</p>";
    var items = content.items || content.questions || content.cards || content.events || content.nodes || [];
    if (!Array.isArray(items)) return "<pre>" + bridge().esc(JSON.stringify(content).slice(0, 1500)) + "</pre>";
    var out = "<ol class='np-list'>";
    items.slice(0, 20).forEach(function (it) {
      if (typeof it === "string") { out += "<li>" + bridge().esc(it) + "</li>"; return; }
      var q = it.question || it.front || it.label || it.title || "";
      var a = it.answer || it.back || it.desc || "";
      if (Array.isArray(it.options)) {
        out += "<li>" + bridge().esc(q) + "<ul>" + it.options.map(function (o) { return "<li>" + bridge().esc(o) + "</li>"; }).join("") + "</ul></li>";
      } else {
        out += "<li><b>" + bridge().esc(q) + "</b>" + (a ? " — " + bridge().esc(a) : "") + "</li>";
      }
    });
    return out + "</ol>";
  }

  function addWidget(step, wc, prompt) {
    var kind = (step.topic && step.topic.kind) || step.kind || "flash";
    var topic = (step.topic && step.topic.topic) || step.topic || prompt;
    var els = (window.NebExcali && window.NebExcali.getSceneElements()) || [];
    var ox = 120 + (els.length % 5) * 60;
    var oy = 120 + (els.length % 5) * 40;
    var id = "w" + Date.now().toString(36);
    var rect = {
      id: id, type: "rectangle", x: ox, y: oy, width: 300, height: 150, angle: 0,
      strokeColor: "#7c3aed", backgroundColor: "#ede9fe", fillStyle: "solid",
      strokeWidth: 2, strokeStyle: "dashed", roughness: 1, opacity: 100,
      groupIds: [], frameId: null, roundness: { type: 3 }, boundElements: [{ type: "text", id: id + ":t" }],
      link: null, locked: false, seed: (Math.random() * 2147483647) | 0, version: 1,
      versionNonce: (Math.random() * 2147483647) | 0, isDeleted: false, index: "w" + els.length,
      customData: { neb: "ink", widget: { kind: kind, topic: topic, content: (wc && wc.content) || null } },
    };
    var label = {
      id: id + ":t", type: "text", x: ox, y: oy, width: 252, height: 102, angle: 0,
      strokeColor: "#1e1e1e", backgroundColor: "transparent", fillStyle: "solid",
      strokeWidth: 1, strokeStyle: "solid", roughness: 1, opacity: 100,
      groupIds: [], frameId: null, roundness: null, boundElements: [],
      link: null, locked: false, seed: (Math.random() * 2147483647) | 0, version: 1,
      versionNonce: (Math.random() * 2147483647) | 0, isDeleted: false, index: "w" + els.length + "t",
      fontSize: 16, fontFamily: 6, textAlign: "left", verticalAlign: "top",
      text: kind.toUpperCase() + "\n" + topic.slice(0, 90), originalText: kind.toUpperCase() + "\n" + topic.slice(0, 90),
      autoResize: false, lineHeight: 1.25, containerId: id,
      customData: { neb: "ink", widget: { kind: kind, topic: topic, content: (wc && wc.content) || null } },
    };
    window.NebExcali.updateScene({ elements: els.concat([rect, label]) });
    bridge().persistScene();
  }

  function showTemplates() {
    bridge().api("/ajax/canvas/templates/").then(function (res) {
      var html = "<div class='np-list-wrap'>";
      (res.templates || []).forEach(function (t) {
        html += "<button class='np-item' data-action='tpl' data-id='" + bridge().esc(t.key) + "'><b>" + bridge().esc(t.name) + "</b><span>" + bridge().esc(t.description || "") + "</span></button>";
      });
      open("Templates", "Start from a template", html + "</div>");
    }).catch(function () { bridge().toast("Could not load templates."); });
  }

  function showHistory() {
    var bid = bridge().boardId();
    if (!bid) { bridge().toast("Open a canvas first."); return; }
    bridge().api("/ajax/canvas/boards/" + bid + "/snapshots/").then(function (res) {
      var html = "<button class='np-item' data-action='snap-new'><b>Save checkpoint</b><span>Snapshot the current board</span></button>";
      (res.snapshots || []).forEach(function (s) {
        html += "<div class='np-item-row'><button class='np-item' data-action='snap-restore' data-id='" + bridge().esc(s.id) + "'><b>" + bridge().esc(s.label || "Checkpoint") + "</b><span>" + (s.nodeCount || 0) + " cards</span></button></div>";
      });
      open("History", "Checkpoints", html);
    }).catch(function () { bridge().toast("Could not load history."); });
  }

  function showNote() {
    open("Note", "New note",
      "<input id='npNoteTitle' class='np-input' placeholder='Title' maxlength='120'>" +
      "<textarea id='npNoteBody' class='np-input' rows='5' placeholder='Write the note…'></textarea>" +
      "<button class='md-btn-f' data-action='note-save'>Add note</button>");
  }

  function showExport() {
    var bid = bridge().boardId();
    if (!bid) { bridge().toast("Open a canvas first."); return; }
    open("Export", "Export canvas",
      "<a class='np-item' href='/ajax/canvas/boards/" + bid + "/export/?format=json'><b>Export JSON</b><span>Full board backup</span></a>" +
      "<a class='np-item' href='/ajax/canvas/boards/" + bid + "/export/?format=md'><b>Export Markdown</b><span>Readable notes</span></a>" +
      "<button class='np-item' data-action='import'><b>Import canvas</b><span>Restore from a .canvas.json file</span></button>");
  }

  function wireBody() {
    var body = $("cvPanelBody");
    if (!body || body._neb) return;
    body._neb = true;
    body.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-action]");
      if (!btn) return;
      var a = btn.getAttribute("data-action");
      var id = btn.getAttribute("data-id");
      if (a === "followup") {
        var v = ($("npFollowInput") || {}).value || "";
        if (!v.trim()) return;
        bridge().api("/ajax/canvas/nodes/" + id + "/followup/", { method: "POST", body: { prompt: v } })
          .then(function (n) { bridge().addNodes([n.node || n], true); close(); })
          .catch(function () { bridge().toast("Follow-up failed."); });
      } else if (a === "retry") {
        bridge().api("/ajax/canvas/nodes/" + id + "/retry/", { method: "POST", body: {} })
          .then(function (n) { bridge().setNode(n.node || n); close(); })
          .catch(function () { bridge().toast("Retry failed."); });
      } else if (a === "dig") {
        var n0 = bridge().getNode(id);
        var seed = n0 && n0.content && n0.content.summary ? n0.content.summary.slice(0, 500) : "";
        bridge().api("/ajax/canvas/nodes/" + id + "/dig-deeper/", { method: "POST", body: { selected_text: seed } })
          .then(function (n) { bridge().addNodes([n.node || n], true); close(); })
          .catch(function () { bridge().toast("Dig deeper failed."); });
      } else if (a === "del") {
        bridge().api("/ajax/canvas/nodes/" + id + "/delete/", { method: "POST", body: {} })
          .then(function () { bridge().dropNode(id); close(); })
          .catch(function () { bridge().toast("Delete failed."); });
      } else if (a === "tpl") {
        bridge().api("/ajax/canvas/templates/create/", { method: "POST", body: { template: id } })
          .then(function (res) {
            if (res && res.board) location.href = "/canvas/?board=" + res.board.id;
          }).catch(function () { bridge().toast("Template failed."); });
      } else if (a === "snap-new") {
        bridge().api("/ajax/canvas/boards/" + bridge().boardId() + "/snapshots/create/", { method: "POST", body: {} })
          .then(function () { bridge().toast("Checkpoint saved."); showHistory(); })
          .catch(function () { bridge().toast("Checkpoint failed."); });
      } else if (a === "snap-restore") {
        bridge().api("/ajax/canvas/boards/" + bridge().boardId() + "/snapshots/" + id + "/restore/", { method: "POST", body: {} })
          .then(function (res) { if (res) location.reload(); })
          .catch(function () { bridge().toast("Restore failed."); });
      } else if (a === "note-save") {
        var t = ($("npNoteTitle") || {}).value || "";
        var b2 = ($("npNoteBody") || {}).value || "";
        bridge().api("/ajax/canvas/boards/" + bridge().boardId() + "/notes/", { method: "POST", body: { title: t, body: b2, kind: "note" } })
          .then(function (n) { bridge().addNodes([n.node || n], true); close(); })
          .catch(function () { bridge().toast("Note failed."); });
      } else if (a === "import") {
        var fi = $("cvImportInput");
        if (fi) fi.click();
      }
    });
  }

  function wireRail() {
    if ($("nebRail") || bridge().config().readOnly) return;
    var rail = document.createElement("div");
    rail.id = "nebRail";
    rail.className = "neb-rail";
    rail.innerHTML =
      "<button data-rail='note' title='Add note'><span class='material-symbols-outlined'>note_add</span></button>" +
      "<button data-rail='tpl' title='Templates'><span class='material-symbols-outlined'>dashboard_customize</span></button>" +
      "<button data-rail='hist' title='History'><span class='material-symbols-outlined'>history</span></button>" +
      "<button data-rail='exp' title='Export / import'><span class='material-symbols-outlined'>ios_share</span></button>";
    document.body.appendChild(rail);
    rail.addEventListener("click", function (e) {
      var b = e.target.closest("[data-rail]");
      if (!b) return;
      var k = b.getAttribute("data-rail");
      if (k === "note") showNote();
      else if (k === "tpl") showTemplates();
      else if (k === "hist") showHistory();
      else if (k === "exp") showExport();
    });
    var fi = $("cvImportInput");
    if (fi && !fi._neb) {
      fi._neb = true;
      fi.addEventListener("change", function () {
        var f = fi.files && fi.files[0];
        if (!f) return;
        var r = new FileReader();
        r.onload = function () {
          try {
            bridge().api("/ajax/canvas/boards/" + bridge().boardId() + "/import/", { method: "POST", body: { canvas: JSON.parse(r.result) } })
              .then(function () { location.reload(); })
              .catch(function () { bridge().toast("Import failed."); });
          } catch (err) { bridge().toast("Bad file."); }
        };
        r.readAsText(f);
        fi.value = "";
      });
    }
    var c = $("cvPanelClose");
    if (c) c.addEventListener("click", close);
    var bd = $("cvPanelBackdrop");
    if (bd) bd.addEventListener("click", close);
  }

  return {
    open: open, close: close, inspect: inspect,
    wireRail: wireRail, addWidget: addWidget,
  };
})();
