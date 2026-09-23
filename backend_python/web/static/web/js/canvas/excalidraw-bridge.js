window.NebCanvas = (function () {
  var cfg = window.CANVAS_CONFIG || {};
  var boardId = cfg.boardId || "";
  var nodes = {};
  var saveTimer = null;
  var lastMoves = "";
  var lastInk = "";
  var busyAgent = false;
  var selectedId = null;

  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function toast(msg) {
    var t = $("toastPill");
    if (!t) return;
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.hidden = true; }, 2600);
  }

  function api(path, opts) {
    opts = opts || {};
    return fetch(path, {
      method: opts.method || "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cfg.csrfToken || "",
      },
      credentials: "same-origin",
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    }).then(function (r) {
      if (!r.ok) throw new Error("http-" + r.status);
      return r.json();
    });
  }

  function theme() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function currentElements() {
    return (window.NebExcali && window.NebExcali.getSceneElements()) || [];
  }

  function refreshScene() {
    if (!window.NebExcali) return;
    var scene = window.NebScene.boardToScene(
      Object.keys(nodes).map(function (k) { return nodes[k]; }),
      window.NebCanvasInk || []
    );
    window.NebExcali.updateScene({ elements: scene.elements, files: scene.files });
  }

  function addNodes(list, focusLast) {
    (list || []).forEach(function (n) { nodes[String(n.id)] = n; });
    refreshScene();
    if (focusLast && list && list.length && window.NebExcali) {
      try { window.NebExcali.scrollToContent(); } catch (e) {}
    }
  }

  function scheduleSave() {
    if (!boardId || cfg.readOnly) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(persistScene, 900);
  }

  function persistScene() {
    if (!boardId || cfg.readOnly || !cfg.isAuthenticated) return;
    var parts = window.NebScene.sceneToPersist(currentElements());
    var movesKey = JSON.stringify(parts.moves);
    var jobs = [];
    if (movesKey !== lastMoves && parts.moves.length) {
      lastMoves = movesKey;
      jobs.push(api("/ajax/canvas/boards/" + boardId + "/batch-move/", {
        method: "POST", body: { nodes: parts.moves },
      }).catch(function () {}));
    }
    var inkKey = JSON.stringify(parts.ink);
    if (inkKey !== lastInk) {
      lastInk = inkKey;
      jobs.push(api("/ajax/canvas/boards/" + boardId + "/objects/", {
        method: "POST",
        body: { objects: [{ id: "neb-scene-ink", type: "excalidraw-ink", x: 0, y: 0, z: 0, elements: parts.ink.slice(0, 1500) }] },
      }).catch(function () {}));
    }
    return Promise.all(jobs);
  }

  function onSceneChange(elements, appState) {
    var ids = (appState && appState.selectedElementIds) || {};
    var keys = Object.keys(ids).filter(function (k) { return ids[k]; });
    var found = null;
    for (var i = 0; i < keys.length; i++) {
      var el = null;
      for (var j = 0; j < elements.length; j++) {
        if (elements[j].id === keys[i]) { el = elements[j]; break; }
      }
      if (el && el.customData && el.customData.neb === "node") { found = el.customData.id; break; }
      if (el && el.customData && el.customData.widget) { found = "@widget:" + el.id; break; }
    }
    if (found !== selectedId) {
      selectedId = found;
      if (window.NebPanel) {
        if (found) window.NebPanel.inspect(found);
        else window.NebPanel.close();
      }
    }
    scheduleSave();
  }

  function loadBoard() {
    if (!boardId && !cfg.sharedToken) return Promise.resolve();
    var detailUrl = (cfg.readOnly && cfg.sharedToken)
      ? "/ajax/canvas/shared/" + cfg.sharedToken + "/detail/"
      : "/ajax/canvas/boards/" + boardId + "/";
    var detail = api(detailUrl).catch(function () { return null; });
    var ink = (!cfg.readOnly && boardId)
      ? api("/ajax/canvas/boards/" + boardId + "/objects/list/").catch(function () { return { objects: [] }; })
      : Promise.resolve({ objects: [] });
    return Promise.all([detail, ink]).then(function (res) {
      var d = res[0];
      if (d && d.nodes) {
        nodes = {};
        d.nodes.forEach(function (n) { nodes[String(n.id)] = n; });
      }
      var objs = (res[1] && res[1].objects) || [];
      var sceneInk = objs.filter(function (o) { return o.type === "excalidraw-ink"; });
      window.NebCanvasInk = sceneInk.length ? sceneInk : objs;
      lastMoves = JSON.stringify(Object.keys(nodes).map(function (k) {
        return { id: k, x: Math.round(Number(nodes[k].x) || 0), y: Math.round(Number(nodes[k].y) || 0) };
      }));
      refreshScene();
      lastInk = JSON.stringify(window.NebScene.sceneToPersist(currentElements()).ink);
    });
  }

  function ensureBoard(title) {
    if (boardId) return Promise.resolve(boardId);
    return api("/ajax/canvas/boards/create/", { method: "POST", body: { title: title || "Untitled canvas" } })
      .then(function (b) {
        var nb = b.board || b;
        boardId = nb.id;
        cfg.boardId = boardId;
        document.body.setAttribute("data-board-id", boardId);
        history.replaceState(null, "", "/canvas/?board=" + boardId);
        return boardId;
      });
  }

  function runAgent(prompt) {
    if (busyAgent || !prompt) return Promise.resolve();
    busyAgent = true;
    return ensureBoard(prompt.slice(0, 60)).then(function () {
      return api("/ajax/canvas/boards/" + boardId + "/agent-prompt/", {
        method: "POST", body: { prompt: prompt },
      });
    }).then(function (res) {
      if (res && res.nodes) addNodes(res.nodes, true);
      var steps = (res && res.steps) || [];
      var widgets = steps.filter(function (s) { return s.tool === "add_widget"; }).slice(0, 3);
      var chain = Promise.resolve();
      widgets.forEach(function (w) {
        chain = chain.then(function () {
          return api("/ajax/canvas/boards/" + boardId + "/widget-content/", {
            method: "POST", body: { kind: (w.topic && w.topic.kind) || w.kind || "flash", topic: (w.topic && w.topic.topic) || w.topic || prompt },
          }).then(function (wc) {
            if (window.NebPanel) window.NebPanel.addWidget(w, wc, prompt);
          }).catch(function () {});
        });
      });
      return chain.then(function () {
        toast((res && res.summary) || "Canvas updated");
        refreshCredits(res && res.credits);
      });
    }).catch(function (e) {
      toast("Neby is busy. Try again.");
    }).then(function () { busyAgent = false; });
  }

  function refreshCredits(c) {
    if (!c) return;
    var v = document.querySelector(".cs-credits-val");
    if (v && !c.unlimited) v.textContent = c.remaining + " left";
  }

  function wirePrompt() {
    var bar = $("canvasBottomBar");
    if (cfg.readOnly && bar) { bar.style.display = "none"; return; }
    var box = $("globalPrompt");
    var btn = $("globalSendBtn");
    if (!box || !btn || box._neb) return;
    box._neb = true;
    var sync = function () {
      btn.disabled = !box.value.trim() || busyAgent;
      box.style.height = "auto";
      box.style.height = Math.min(120, box.scrollHeight) + "px";
    };
    box.addEventListener("input", sync);
    var send = function () {
      var v = box.value.trim();
      if (!v || busyAgent) return;
      box.value = "";
      sync();
      runAgent(v).then(sync);
    };
    btn.addEventListener("click", send);
    box.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
    });
    var fab = $("cvNebyFab");
    if (fab && !fab._neb) {
      fab._neb = true;
      fab.addEventListener("click", function () { box.focus(); });
    }
    sync();
  }

  function mount() {
    var host = $("excalidrawMount");
    if (!host || !window.NebExcali) return;
    window.NebExcali.mount(host, { theme: theme(), viewMode: !!cfg.readOnly });
    window.NebExcali.onChange(onSceneChange);
    loadBoard().then(function () {
      if (window.NebPanel) window.NebPanel.wireRail();
    });
    wirePrompt();
    wireSidebar();
  }

  function wireSidebar() {
    var nb = $("csNewBoardBtn");
    if (nb && !nb._neb) {
      nb._neb = true;
      nb.addEventListener("click", function () {
        var t = window.prompt("Name your canvas:", "");
        if (t === null) return;
        api("/ajax/canvas/boards/create/", { method: "POST", body: { title: t || "Untitled canvas" } })
          .then(function (b) {
            var board = b.board || b;
            location.href = "/canvas/?board=" + board.id;
          }).catch(function () { toast("Could not create canvas."); });
      });
    }
    var list = $("csBoards");
    if (list && !list._neb) {
      list._neb = true;
      list.addEventListener("click", function (e) {
        var item = e.target.closest("[data-board-id]");
        if (item) location.href = "/canvas/?board=" + item.getAttribute("data-board-id");
      });
    }
    var col = $("csCollapseBtn");
    if (col) col.addEventListener("click", function () { $("canvasSidebar").classList.toggle("collapsed"); });
    var mob = $("csMobileToggle");
    if (mob) mob.addEventListener("click", function () { $("canvasSidebar").classList.toggle("open"); });
  }

  return {
    mount: mount,
    esc: esc,
    api: api,
    toast: toast,
    addNodes: addNodes,
    runAgent: runAgent,
    refreshScene: refreshScene,
    persistScene: persistScene,
    getNode: function (id) { return nodes[String(id)] || null; },
    setNode: function (n) { nodes[String(n.id)] = n; refreshScene(); },
    dropNode: function (id) { delete nodes[String(id)]; refreshScene(); },
    boardId: function () { return boardId; },
    config: function () { return cfg; },
  };
})();
