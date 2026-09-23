window.NebCards = (function () {
  var B = null;
  function bridge() {
    if (!B) B = window.NebCanvas;
    return B;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function md(s) {
    if (!s) return "";
    var str = String(s);
    var codeBlocks = [];
    str = str.replace(/```([a-zA-Z0-9_#+-]*)\r?\n?([\s\S]*?)```/g, function (_, lang, code) {
      var idx = codeBlocks.length;
      var l = (lang || "code").trim().toUpperCase();
      var cleanCode = code.replace(/^\r?\n+|\r?\n+$/g, "");
      var blockHtml = '<div class="code-block"><div class="code-block-head"><span class="code-lang">' +
        esc(l) + '</span><button class="code-copy" title="Copy code" aria-label="Copy code"><span class="material-symbols-outlined">content_copy</span></button></div><pre class="code-pre">' +
        esc(cleanCode) + "</pre></div>";
      codeBlocks.push(blockHtml);
      return "___CV_CODE_BLOCK_" + idx + "___";
    });
    str = esc(str);
    str = str.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    str = str.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\*(?!\s)([^*]+?)\*/g, "<em>$1</em>").replace(/\r?\n/g, "<br>");
    for (var i = 0; i < codeBlocks.length; i++) {
      str = str.replace("___CV_CODE_BLOCK_" + i + "___", codeBlocks[i]);
    }
    return str;
  }

  function hostOf(u) {
    try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return ""; }
  }

  function copyText(t) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(t);
    return new Promise(function (res, rej) {
      try {
        var ta = document.createElement("textarea");
        ta.value = t;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        ta.remove();
        res();
      } catch (e) { rej(e); }
    });
  }

  var TONES = ["blue", "green", "amber", "rose", "slate"];
  function rFlow(sec) {
    var h = '<div class="flow-wrap"><div class="flow-title">' + esc(sec.title || "Flow") + '</div><div class="flow-col">';
    var links = sec.links || [];
    var nodes = sec.nodes || sec.steps || [];
    nodes.forEach(function (nd, i) {
      var label = typeof nd === "string" ? nd : nd.label || nd.title || nd.name || "";
      var desc = typeof nd === "object" && nd ? nd.desc || nd.description || "" : "";
      var tone = nd.tone && TONES.indexOf(nd.tone) > -1 ? nd.tone : TONES[i % TONES.length];
      h += '<div class="flow-node t-' + tone + '"' + (desc ? ' title="' + esc(desc) + '"' : "") + ">" + esc(label) + (desc ? '<span class="fn-desc">' + esc(desc) + "</span>" : "") + "</div>";
      if (i < nodes.length - 1) {
        h += '<div class="flow-arrow">' + (links[i] ? '<span class="fa-label">' + esc(links[i]) + "</span>" : "") + '<span class="fa-head"></span></div>';
      }
    });
    return h + "</div></div>";
  }

  function rTimeline(sec) {
    var h = '<div class="tl-wrap"><div class="tl-title">' + esc(sec.title || "Timeline") + '</div><div class="tl-row">';
    var steps = sec.steps || sec.items || [];
    steps.forEach(function (st, i) {
      var title = typeof st === "string" ? st : st.title || st.name || st.label || "";
      var sub = typeof st === "object" && st ? st.sub || st.subtitle || st.desc || "" : "";
      h += '<div class="tl-item"><span class="tl-dot">' + (i + 1) + '</span><span class="tl-label">' + esc(title) + "</span>" + (sub ? '<span class="tl-sub">' + esc(sub) + "</span>" : "") + "</div>";
    });
    return h + "</div></div>";
  }

  function rStats(sec) {
    var h = '<div class="stats-grid">';
    (sec.items || []).forEach(function (it) {
      var k = it.k || it.key || it.label || it.name || "";
      var v = it.v || it.val || it.value || it.stat || "";
      h += '<div class="stat-chip"><div class="stat-k">' + esc(k) + '</div><div class="stat-v">' + esc(v) + "</div></div>";
    });
    return h + "</div>";
  }

  function rQuote(sec) {
    var txt = sec.text || sec.quote || sec.content || "";
    var cite = sec.cite || sec.author || sec.source || "";
    return '<div class="quote-block"><div class="quote-text">' + esc(txt) + "</div>" + (cite ? '<div class="quote-cite">' + esc(cite) + "</div>" : "") + "</div>";
  }

  function rCode(sec) {
    var txt = sec.text || sec.code || sec.content || sec.snippet || "";
    var lang = sec.lang || sec.language || "code";
    return '<div class="code-block"><div class="code-block-head"><span class="code-lang">' + esc(lang.toUpperCase()) + '</span><button class="code-copy" title="Copy code" aria-label="Copy code"><span class="material-symbols-outlined">content_copy</span></button></div><pre class="code-pre">' + esc(txt) + "</pre></div>";
  }

  function rProsCons(sec) {
    function li(t) { return "<li>" + esc(t) + "</li>"; }
    return '<div class="pc-wrap">' +
      '<div class="pc-col pc-pros"><div class="pc-head"><span class="material-symbols-outlined">thumb_up</span> Pros</div><ul>' + (sec.pros || []).map(li).join("") + "</ul></div>" +
      '<div class="pc-col pc-cons"><div class="pc-head"><span class="material-symbols-outlined">thumb_down</span> Cons</div><ul>' + (sec.cons || []).map(li).join("") + "</ul></div>" +
      "</div>";
  }

  function rAskUser(sec, nodeId) {
    var opts = (sec.options || []).slice(0, 4);
    var h = '<div class="ask-wrap" data-ask-node="' + esc(nodeId) + '"><div class="ask-q"><span class="material-symbols-outlined">help</span> ' + esc(sec.question || "Could you clarify?") + "</div>";
    if (opts.length) {
      h += '<div class="ask-opts">';
      opts.forEach(function (o) { h += '<button class="ask-opt" data-opt="' + esc(o) + '">' + esc(o) + "</button>"; });
      h += "</div>";
    }
    h += '<div class="ask-input-row"><input class="ask-input" placeholder="' + esc(sec.placeholder || "Type your context…") + '" /><button class="ask-send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
    h += '<div class="ask-hint">Pick an option or type above — I’ll tailor the next card precisely and truthfully.</div></div>';
    return h;
  }

  function renderSection(sec, idx, nodeId) {
    if (!sec) return "";
    var t = String(sec.type || "").toLowerCase().trim();
    if ((t === "text" || t === "summary" || t === "paragraph" || t === "note") && (sec.content || sec.text || sec.body)) {
      var c = sec.content || sec.text || sec.body || "";
      return '<div class="text-block">' + (sec.title ? '<strong class="sec-subtitle">' + esc(sec.title) + "</strong><br>" : "") + md(c) + "</div>";
    }
    if ((t === "flow" || t === "pipeline" || t === "process" || t === "workflow") && (sec.nodes || sec.steps)) return rFlow(sec);
    if ((t === "timeline" || t === "steps" || t === "history") && (sec.steps || sec.items)) return rTimeline(sec);
    if ((t === "stats" || t === "metrics" || t === "numbers") && sec.items) return rStats(sec);
    if ((t === "quote" || t === "callout" || t === "definition") && (sec.text || sec.quote || sec.content)) return rQuote(sec);
    if ((t === "code" || t === "snippet" || t === "script" || t === "program") && (sec.text || sec.code || sec.content || sec.snippet)) return rCode(sec);
    if ((t === "proscons" || t === "tradeoffs") && (sec.pros || sec.cons)) return rProsCons(sec);
    if ((t === "diagram" || t === "chart" || t === "graph") && sec.nodes) {
      var h = '<div class="diagram-wrap"><div class="diagram-title">' + esc(sec.title || "Diagram") + '</div><div class="diagram-grid">';
      sec.nodes.forEach(function (dn) { h += '<div class="diagram-node" data-diag="' + idx + '" data-nid="' + esc(dn.id || dn.label || "") + '"><div class="diagram-node-label">' + esc(dn.label || dn.title || "") + '</div><div class="diagram-node-desc">' + esc(dn.desc || dn.description || "") + "</div></div>"; });
      return h + '</div><div class="diagram-detail" id="diag_' + nodeId + "_" + idx + '"></div></div>';
    }
    if ((t === "comparison" || t === "table") && (sec.rows || sec.items)) {
      var h2 = '<div class="comp-wrap"><div class="comp-title">' + esc(sec.title || "Comparison") + '</div><div class="comp-table-wrap"><table class="comp-table"><thead><tr>';
      (sec.headers || ["Aspect", "A", "B"]).forEach(function (hh) { h2 += "<th>" + esc(hh) + "</th>"; });
      h2 += "</tr></thead><tbody>";
      (sec.rows || sec.items || []).forEach(function (row) {
        h2 += "<tr>";
        if (Array.isArray(row)) row.forEach(function (v) { h2 += "<td>" + esc(v) + "</td>"; });
        else if (typeof row === "object" && row) Object.values(row).forEach(function (v) { h2 += "<td>" + esc(v) + "</td>"; });
        h2 += "</tr>";
      });
      return h2 + "</tbody></table></div></div>";
    }
    if ((t === "cards" || t === "references" || t === "sources") && sec.items) {
      if (t === "references" || t === "sources" || (sec.items[0] && (sec.items[0].url || sec.items[0].source))) {
        var h5 = '<div class="refs-wrap"><div class="refs-title"><span class="material-symbols-outlined">travel_explore</span> ' + esc(sec.title || "Sources") + "</div>";
        sec.items.forEach(function (rf) {
          var title = esc(rf.title || rf.url || "Source"), u = String(rf.url || "");
          if (u && /^https?:\/\//i.test(u)) h5 += '<a class="ref-item" href="' + esc(u) + '" target="_blank" rel="noopener noreferrer nofollow"><span class="ref-fav" aria-hidden="true">' + esc((rf.source || hostOf(u)).charAt(0).toUpperCase()) + '</span><span class="ref-main"><span class="ref-t">' + title + '</span><span class="ref-s">' + esc(hostOf(u) || rf.source || "") + '</span></span><span class="material-symbols-outlined ref-arrow">north_east</span></a>';
          else h5 += '<span class="ref-item static"><span class="ref-fav">' + esc((rf.source || "S").charAt(0).toUpperCase()) + '</span><span class="ref-main"><span class="ref-t">' + title + "</span>" + (rf.source ? '<span class="ref-s">' + esc(rf.source) + "</span>" : "") + "</span></span>";
        });
        return h5 + "</div>";
      }
      var h3 = '<div class="comp-wrap"><div class="comp-title">' + esc(sec.title || "References") + '</div><div class="cards-grid">';
      sec.items.forEach(function (it) {
        h3 += '<div class="card-ref"><div class="card-ref-title">' + esc(it.title || "") + '</div><div class="card-ref-sub">' + esc(it.subtitle || "") + "</div>";
        if (it.bullets) { h3 += '<ul class="card-ref-bullets">'; it.bullets.forEach(function (b) { h3 += "<li>" + esc(b) + "</li>"; }); h3 += "</ul>"; }
        if (it.desc || it.description) h3 += '<div class="card-ref-desc">' + esc(it.desc || it.description) + "</div>";
        h3 += "</div>";
      });
      return h3 + "</div></div>";
    }
    if ((t === "bullets" || t === "list" || t === "points" || t === "key_points") && sec.items) {
      var h4 = "<div><div class='bullets-title'>" + esc(sec.title || "") + '</div><ul class="bullets-list">';
      sec.items.forEach(function (v) { h4 += "<li>" + (typeof v === "string" ? md(v) : v.text ? md(v.text) : esc(JSON.stringify(v))) + "</li>"; });
      return h4 + "</ul></div>";
    }
    if (t === "ask_user" && (sec.question || sec.prompt)) return rAskUser(sec, nodeId);
    if (sec.code || sec.snippet) return rCode(sec);
    if (sec.content || sec.text || sec.body || sec.desc || sec.description) {
      var txt = sec.content || sec.text || sec.body || sec.desc || sec.description || "";
      return '<div class="text-block">' + (sec.title ? '<strong class="sec-subtitle">' + esc(sec.title) + "</strong><br>" : "") + md(txt) + "</div>";
    }
    return "";
  }

  function layer() { return document.getElementById("nebCards"); }

  function renderCard(n) {
    var old = document.getElementById("node_" + n.id);
    if (old) old.remove();
    var host = layer();
    if (!host) return null;
    var card = document.createElement("div");
    card.className = "canvas-card";
    card.id = "node_" + n.id;
    card.dataset.nodeId = n.id;
    card.style.left = n.x + "px";
    card.style.top = n.y + "px";
    card.tabIndex = 0;
    var c = n.content || {};
    var isEmpty = n.status === "empty";
    var gen = n.status === "generating";
    if (isEmpty) card.classList.add("is-empty");
    else if (gen) card.classList.add("is-generating");
    var title = isEmpty ? "New thread" : c.title || n.title || String(n.prompt || "").slice(0, 48);
    var head;
    if (isEmpty) {
      head = '<div class="card-head"><div class="card-title">New thread</div><div class="card-actions"><button class="card-icon-btn" data-action="delete" title="Delete"><span class="material-symbols-outlined">close</span></button></div></div>';
    } else {
      head = '<div class="card-head"><div class="card-title">' + esc(title) + '</div><div class="card-actions"><button class="card-icon-btn" data-action="focus" title="Center (F)"><span class="material-symbols-outlined">center_focus_strong</span></button><button class="card-icon-btn" data-action="copy" title="Copy prompt"><span class="material-symbols-outlined">content_copy</span></button><button class="card-icon-btn" data-action="delete" title="Delete (Del)"><span class="material-symbols-outlined">delete</span></button></div></div>';
    }
    var body = "";
    if (isEmpty) {
      body = '<div class="card-body empty-thread"><div class="empty-thread-hint">What should this thread explore?</div></div><div class="card-followup"><input class="draft-input" placeholder="Ask anything to start this thread…" aria-label="Thread prompt"><button class="cf-send" aria-label="Send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
    } else if (gen) {
      body = '<div class="card-body"><div class="card-status"><span class="card-dots"><i></i><i></i><i></i></span> <em>Creating a visual…</em></div></div>';
    } else {
      body = '<div class="card-body">';
      if (c.summary) body += '<div class="text-block">' + md(c.summary) + "</div>";
      (c.sections || []).forEach(function (sec, idx) {
        try { body += renderSection(sec, idx, n.id); } catch (err) { /* skip bad section */ }
      });
      body += '</div><div class="card-followup"><input placeholder="Ask a follow-up…" aria-label="Ask follow-up"><button class="cf-send" aria-label="Send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
    }
    card.innerHTML = head + body;
    host.appendChild(card);
    wireCard(card, n);
    return card;
  }

  function wireCard(card, n) {
    var readOnly = bridge().config().readOnly;
    card.querySelectorAll(".code-copy").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var block = btn.closest(".code-block");
        var preEl = block ? block.querySelector(".code-pre") : null;
        var txt = preEl ? preEl.textContent : "";
        copyText(txt.trim()).then(function () {
          btn.classList.add("copied");
          btn.innerHTML = '<span class="material-symbols-outlined">check</span>';
          bridge().toast("Code copied");
          setTimeout(function () { btn.classList.remove("copied"); btn.innerHTML = '<span class="material-symbols-outlined">content_copy</span>'; }, 1400);
        }, function () { bridge().toast("Copy failed"); });
      });
    });
    if (readOnly) return;
    var del = card.querySelector('[data-action="delete"]');
    if (del) del.addEventListener("click", function (e) { e.stopPropagation(); bridge().deleteNode(n.id); });
    if (n.status === "empty") {
      var dInp = card.querySelector(".draft-input"), dBtn = card.querySelector(".cf-send");
      if (dInp && dBtn) {
        var dGo = function () {
          var v = dInp.value.trim();
          if (!v) return;
          if (n.parentId) bridge().followupNode(n.parentId, v, { x: n.x, y: n.y });
          else bridge().runAgent(v);
          bridge().dropLocal(n.id);
        };
        dInp.addEventListener("input", function () { dBtn.disabled = !this.value.trim(); });
        dInp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); dGo(); } });
        dBtn.addEventListener("click", dGo);
      }
      return;
    }
    if (n.status === "generating") return;
    var inp = card.querySelector(".card-followup input"), btn = card.querySelector(".cf-send");
    if (inp && btn) {
      inp.addEventListener("input", function () { btn.disabled = !this.value.trim(); });
      inp.addEventListener("keydown", function (e) {
        if (e.key === "Enter") { e.preventDefault(); var v = inp.value.trim(); if (!v) return; inp.value = ""; btn.disabled = true; bridge().followupNode(n.id, v, {}); }
      });
      btn.addEventListener("click", function () { var v = inp.value.trim(); if (!v) return; inp.value = ""; btn.disabled = true; bridge().followupNode(n.id, v, {}); });
    }
    card.querySelectorAll(".diagram-node").forEach(function (el) {
      el.addEventListener("click", function () {
        var idx = el.dataset.diag, detail = document.getElementById("diag_" + n.id + "_" + idx);
        if (!detail) return;
        var was = el.classList.contains("active");
        card.querySelectorAll(".diagram-node").forEach(function (x) { x.classList.remove("active"); });
        if (!was) {
          el.classList.add("active");
          detail.textContent = el.querySelector(".diagram-node-desc").textContent + " — tap again to dismiss.";
          detail.classList.add("show");
        } else detail.classList.remove("show");
      });
    });
    var askWrap = card.querySelector(".ask-wrap");
    if (askWrap) {
      var askInput = askWrap.querySelector(".ask-input");
      var askSend = askWrap.querySelector(".ask-send");
      if (askInput && askSend) {
        var askGo = function () {
          var v = askInput.value.trim();
          if (!v) return;
          askInput.value = "";
          askSend.disabled = true;
          askWrap.querySelectorAll(".ask-opt").forEach(function (b) { b.disabled = true; });
          bridge().followupNode(n.id, "Context: " + v + " — please tailor the next card for this context.", {});
          bridge().toast("Context received — generating tailored card");
        };
        askInput.addEventListener("input", function () { askSend.disabled = !this.value.trim(); });
        askInput.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); askGo(); } });
        askSend.addEventListener("click", askGo);
      }
      askWrap.querySelectorAll(".ask-opt").forEach(function (btnOpt) {
        btnOpt.addEventListener("click", function () {
          var opt = btnOpt.dataset.opt;
          if (!opt) return;
          askWrap.querySelectorAll(".ask-opt").forEach(function (b) { b.disabled = true; b.style.opacity = ".5"; });
          btnOpt.disabled = false;
          btnOpt.style.opacity = "1";
          btnOpt.style.background = "var(--cv-primary)";
          btnOpt.style.color = "#fff";
          bridge().followupNode(n.id, "Selected context: '" + opt + "' — please tailor the next card for this context and be truthful. If still ambiguous, ask again.", {});
          bridge().toast("Context selected");
        });
      });
    }
    var focusBtn = card.querySelector('[data-action="focus"]');
    if (focusBtn) focusBtn.addEventListener("click", function (e) { e.stopPropagation(); bridge().focusNode(n.id); });
    var copyBtn = card.querySelector('[data-action="copy"]');
    if (copyBtn) copyBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      copyText(n.prompt).then(function () { bridge().toast("Prompt copied"); }, function () { bridge().toast("Copy failed"); });
    });
    card.addEventListener("pointerdown", function (e) {
      select(n.id);
      if (e.target.closest("button") || e.target.closest("input") || e.target.closest("a")) return;
      if (!e.target.closest(".card-head")) return;
      e.preventDefault();
      try { window.getSelection().removeAllRanges(); } catch (err) {}
      bridge().startDrag(n.id, card, e.clientX, e.clientY);
      try { card.setPointerCapture(e.pointerId); } catch (err) {}
    });
  }

  function select(id) {
    document.querySelectorAll("#nebCards .canvas-card.selected").forEach(function (el) { el.classList.remove("selected"); });
    if (!id) return;
    var el = document.getElementById("node_" + id);
    if (el) el.classList.add("selected");
  }

  function syncView(scrollX, scrollY, zoom) {
    var host = layer();
    if (!host) return;
    host.style.transform = "translate(" + scrollX * zoom + "px," + scrollY * zoom + "px) scale(" + zoom + ")";
  }

  function renderAll(list) {
    var host = layer();
    if (!host) return {};
    host.innerHTML = "";
    var sizes = {};
    (list || []).forEach(function (n) {
      var card = renderCard(n);
      if (card) sizes[String(n.id)] = { w: card.offsetWidth || 480, h: card.offsetHeight || 420 };
    });
    return sizes;
  }

  function upsert(n) {
    var card = renderCard(n);
    if (!card) return null;
    return { w: card.offsetWidth || 480, h: card.offsetHeight || 420 };
  }

  function remove(id) {
    var el = document.getElementById("node_" + id);
    if (el) el.remove();
  }

  function moveEl(id, x, y) {
    var el = document.getElementById("node_" + id);
    if (el) { el.style.left = x + "px"; el.style.top = y + "px"; }
  }

  return {
    renderAll: renderAll, upsert: upsert, remove: remove, moveEl: moveEl,
    select: select, syncView: syncView, esc: esc, md: md,
  };
})();
