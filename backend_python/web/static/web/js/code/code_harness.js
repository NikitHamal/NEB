/* ──────────────────────────────────────────────────────────
 * Neby Code — Ice Cream UI Harness for Coding Agent
 * ────────────────────────────────────────────────────────── */

(function(window) {
  "use strict";

  var I = window.LazyIcons || {};
  var P = window.LazyPrimitives || {};
  var AI = window.AIWidgets || {};
  var CFG = window.CODE_BOOT || {};

  function sanitizeMojibake(s) {
    if (!s || typeof s !== "string") return s || "";
    try {
      if (/[\u00C2-\u00F4][\u0080-\u00BF]/.test(s)) {
        return decodeURIComponent(escape(s));
      }
    } catch (e) {}
    return s
      .replace(/ð\x9f\x91\x8b/g, "👋")
      .replace(/ð[\x90-\xBF][\x80-\xBF][\x80-\xBF]/g, "🤖")
      .replace(/â\x80\x94/g, "—")
      .replace(/â\x80\x93/g, "–")
      .replace(/â\x80\x98/g, "‘")
      .replace(/â\x80\x99/g, "’")
      .replace(/â\x80\x9c/g, "“")
      .replace(/â\x80\x9d/g, "”")
      .replace(/â\x80\xa6/g, "…")
      .replace(/â\x9c\x93/g, "✓")
      .replace(/â/g, "");
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function(c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderInline(s) {
    return s
      .replace(/`([^`]+)`/g, '<code class="font-mono bg-field px-1 rounded">$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\s][^*]*)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer nofollow" class="text-accent underline">$1</a>');
  }

  function parseMarkdown(src) {
    src = sanitizeMojibake(String(src || "")).replace(/\r\n/g, "\n");
    var blocks = [];
    src = src.replace(/```([a-zA-Z0-9_#+.-]*)\n?([\s\S]*?)```/g, function(_, lang, code) {
      var i = blocks.length;
      blocks.push(
        '<div class="code-block" style="margin:10px 0;background:var(--inset,#1e2026);border-radius:8px;border:1px solid var(--line);overflow:hidden;">' +
        '<div class="code-head" style="display:flex;justify-content:space-between;padding:6px 12px;background:rgba(0,0,0,0.12);font-size:11.5px;color:var(--ink-2);font-family:var(--font-mono);">' +
        '<span>' + esc((lang || "code").trim() || "code") + '</span>' +
        '<button type="button" class="code-copy-btn" data-code-idx="' + i + '" style="background:none;border:none;cursor:pointer;color:inherit;font-size:11.5px;display:inline-flex;align-items:center;gap:4px;">Copy</button></div>' +
        '<pre style="padding:10px 12px;margin:0;overflow-x:auto;font-family:var(--font-mono);font-size:12.5px;line-height:1.5;color:var(--ink);">' + esc(code.replace(/\n$/, "")) + '</pre></div>'
      );
      return "\n@@CODEBLOCK" + i + "@@\n";
    });

    var lines = esc(src).split("\n"), out = [], inUl = false, inOl = false, listBuf = [];
    function flushList() {
      if (listBuf.length) {
        out.push("<" + (inOl ? "ol" : "ul") + " style='padding-left:20px;margin-bottom:8px;'>" + listBuf.map(function(x){ return "<li style='margin-bottom:3px;'>" + renderInline(x) + "</li>"; }).join("") + "</" + (inOl ? "ol" : "ul") + ">");
        listBuf = []; inUl = false; inOl = false;
      }
    }
    var para = [];
    function flushPara() {
      if (para.length) {
        out.push("<p style='margin-bottom:8px;line-height:1.6;'>" + renderInline(para.join("<br>")) + "</p>");
        para = [];
      }
    }

    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i], t = ln.trim();
      var cm = t.match(/^@@CODEBLOCK(\d+)@@$/);
      if (cm) { flushPara(); flushList(); out.push(blocks[+cm[1]]); continue; }
      if (!t) { flushPara(); flushList(); continue; }
      var h = t.match(/^(#{1,6})\s+(.*)$/);
      if (h) { flushPara(); flushList(); out.push("<h4 style='margin:12px 0 6px;font-weight:600;color:var(--ink);'>" + renderInline(h[2]) + "</h4>"); continue; }
      if (/^(---+|\*\*\*+)$/.test(t)) { flushPara(); flushList(); out.push("<hr style='border:none;border-top:1px solid var(--line);margin:10px 0;'>"); continue; }
      if (/^&gt;\s?/.test(t)) { flushPara(); flushList(); out.push("<blockquote style='border-left:3px solid var(--accent);padding-left:10px;margin:8px 0;color:var(--ink-2);'>" + renderInline(t.replace(/^&gt;\s?/, "")) + "</blockquote>"); continue; }
      if (/^[-*]\s+/.test(t)) { if (inOl) flushList(); inUl = true; listBuf.push(renderInline(t.replace(/^[-*]\s+/, ""))); continue; }
      if (/^\d+[.)]\s+(.*)$/.test(t)) { if (inUl) flushList(); inOl = true; listBuf.push(t.replace(/^\d+[.)]\s+/, "")); continue; }
      para.push(t);
    }
    flushPara(); flushList();
    return out.join("");
  }

  function bindCopyButtons(container) {
    var btns = container.querySelectorAll('.code-copy-btn');
    btns.forEach(function(b) {
      if (b.dataset.bound) return;
      b.dataset.bound = 'true';
      b.addEventListener('click', function() {
        var pre = b.closest('.code-block').querySelector('pre');
        if (pre) {
          navigator.clipboard.writeText(pre.textContent || '').then(function() {
            b.textContent = 'Copied!';
            setTimeout(function() { b.textContent = 'Copy'; }, 1800);
          });
        }
      });
    });
  }

  function toast(msg, isErr) {
    var t = document.createElement("div");
    t.className = "lz-toast" + (isErr ? " error" : "");
    t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(function() { t.classList.add("show"); });
    setTimeout(function() {
      t.classList.remove("show");
      setTimeout(function() { t.remove(); }, 250);
    }, 2800);
  }

  function CodeHarness(root) {
    this.root = root;
    this.api = new window.NebyCodeAPI(CFG);
    this.sessions = new Map();
    this.tabs = [];
    this.activeSessionId = "";
    this.activePanel = "changes"; // changes | files | term | connect
    this.daemonOnline = !!CFG.daemonOnline;
    this.daemonInfo = CFG.daemonInfo || {};
    this.models = CFG.models || {};
    this.allModels = [];
    var self = this;

    (this.models.groups || []).forEach(function(g) {
      (g.models || []).forEach(function(m) { self.allModels.push(m); });
    });

    this.selectedModel = this.chooseDefaultModel();
    this.selectedEffort = "balanced";
    this.selectedMode = "agent"; // agent | plan | ask

    this.changes = [];
    this.activeDiffFile = "";
    this.fileTree = [];
    this.activeFilePath = "";

    this.init();
  }

  CodeHarness.prototype.chooseDefaultModel = function() {
    var wanted = this.models.default || {};
    var match = this.allModels.find(function(m) {
      return m.provider === wanted.provider && m.model === wanted.model && (m.provider_id || '') === (wanted.provider_id || '');
    });
    return match || this.allModels.find(function(m) { return m.available; }) || this.allModels[0] || {
      provider: 'tryingopen', provider_id: '', model: 'qwen/qwen3.8-27b', label: 'Qwen 3.8 27B', available: true
    };
  };

  CodeHarness.prototype.init = function() {
    var self = this;
    this.root.innerHTML = "";
    this.root.className = "lz-harness-root";

    // 1. Sidebar
    this.sidebar = document.createElement("aside");
    this.sidebar.className = "lz-sidebar-nav";
    this.sidebar.dataset.collapsed = "false";
    this.buildSidebar();
    this.root.appendChild(this.sidebar);

    // 2. Stage
    this.stage = document.createElement("div");
    this.stage.className = "lz-stage";

    this.panelsRow = document.createElement("div");
    this.panelsRow.className = "lz-panels-row";

    // 3. Main Pane
    this.mainPane = document.createElement("section");
    this.mainPane.className = "lz-main-pane";
    this.buildMainPane();
    this.panelsRow.appendChild(this.mainPane);

    // 4. Artifact Pane
    this.artifactPane = document.createElement("aside");
    this.artifactPane.className = "lz-artifact-pane";
    this.artifactPane.dataset.open = "true";
    this.buildWorkspacePane();
    this.panelsRow.appendChild(this.artifactPane);

    this.stage.appendChild(this.panelsRow);
    this.root.appendChild(this.stage);

    // Mobile Scrim
    this.scrim = document.createElement("div");
    this.scrim.className = "lz-scrim";
    this.scrim.addEventListener("click", function() {
      self.closeMobileSidebar();
    });
    this.root.appendChild(this.scrim);

    // Popover click-outside dismissal
    document.addEventListener("click", function(e) {
      if (self.activePopover && !self.activePopover.contains(e.target) && !e.target.closest(".code-popover-trigger")) {
        self.closeActivePopover();
      }
    });

    // Seed Sessions
    (CFG.sessions || []).forEach(function(s) {
      self.sessions.set(s.id, s);
    });

    this.renderSidebarSessions();

    // Check Initial URL
    var pathMatch = window.location.pathname.match(/\/code\/([a-zA-Z0-9_-]+)/);
    var targetSid = (pathMatch && pathMatch[1] !== "session") ? pathMatch[1] : (CFG.initial_session_id || "");

    if (targetSid && (self.sessions.has(targetSid) || targetSid.length > 8)) {
      this.openSession(targetSid, true);
    } else if (CFG.sessions && CFG.sessions.length > 0) {
      this.openSession(CFG.sessions[0].id, true);
    } else {
      this.newSession(true);
    }

    // Popstate Listener
    window.addEventListener("popstate", function(e) {
      var m = window.location.pathname.match(/\/code\/([a-zA-Z0-9_-]+)/);
      var popSid = (m && m[1] !== "session") ? m[1] : (e.state && e.state.sessionId);
      if (popSid && popSid !== self.activeSessionId) {
        self.openSession(popSid, true);
      } else if (!popSid && self.activeSessionId) {
        self.newSession(true);
      }
    });

    // Realtime channel subscriptions with wildcard event support
    if (window.WS && typeof window.WS.on === "function") {
      window.WS.on("*:user_enqueued", function(d, ch) { self.onRealtimeEvent("user_enqueued", d, ch); });
      window.WS.on("*:agent_delta", function(d, ch) { self.onRealtimeEvent("agent_delta", d, ch); });
      window.WS.on("*:agent_thought", function(d, ch) { self.onRealtimeEvent("agent_thought", d, ch); });
      window.WS.on("*:agent_tool_call", function(d, ch) { self.onRealtimeEvent("agent_tool_call", d, ch); });
      window.WS.on("*:agent_tool_result", function(d, ch) { self.onRealtimeEvent("agent_tool_result", d, ch); });
      window.WS.on("*:agent_done", function(d, ch) { self.onRealtimeEvent("agent_done", d, ch); });
      window.WS.on("*:agent_error", function(d, ch) { self.onRealtimeEvent("agent_error", d, ch); });
      window.WS.on("*:daemon_status", function(d) { self.updateDaemonStatus(d); });
    }

    setInterval(function() { self.checkDaemonStatus(); }, 15000);
  };

  CodeHarness.prototype.startPolling = function() {
    var self = this;
    this.stopPolling();
    this.pollTimer = setInterval(function() {
      if (!self.activeSessionId) return;
      self.api.session(self.activeSessionId).then(function(res) {
        if (!res || !res.session) return;
        var s = res.session;
        if (s.status === "idle" || s.status === "error") {
          self.stopPolling();
          self.sendBtn.disabled = false;
          if (res.messages && res.messages.length) {
            self.threadWrap.innerHTML = "";
            res.messages.forEach(function(m) {
              if (m.role === "user") self.appendUserBubble(m.content, (m.meta && m.meta.attachments) || []);
              else self.appendAssistantResponse(m);
            });
            self.scrollToBottom();
          }
        }
      }).catch(function(){});
    }, 1500);
  };

  CodeHarness.prototype.stopPolling = function() {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  };

  CodeHarness.prototype.closeActivePopover = function() {
    if (this.activePopover) {
      this.activePopover.remove();
      this.activePopover = null;
    }
  };

  CodeHarness.prototype.buildSidebar = function() {
    var self = this;
    this.sidebar.innerHTML = "";

    // Header
    var head = document.createElement("div");
    head.className = "lz-sb-header";

    var wsBtn = document.createElement("button");
    wsBtn.type = "button";
    wsBtn.className = "lz-sb-workspace-btn";
    wsBtn.innerHTML = '<img src="/static/web/img/n-logo-48.png" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="Neby Code">' +
      '<span class="lz-sb-workspace-name">' + esc(this.daemonInfo.workspace_label || "Neby Code") + '</span>';
    wsBtn.addEventListener("click", function() {
      if (self.sidebar.dataset.collapsed === "true") {
        self.sidebar.dataset.collapsed = "false";
      }
    });
    head.appendChild(wsBtn);

    var colBtn = document.createElement("button");
    colBtn.type = "button";
    colBtn.className = "lz-sb-collapse-btn";
    colBtn.title = "Toggle sidebar";
    colBtn.innerHTML = I.sidebarToggle({ size: 16 });
    colBtn.addEventListener("click", function() {
      self.sidebar.dataset.collapsed = self.sidebar.dataset.collapsed === "true" ? "false" : "true";
    });
    head.appendChild(colBtn);
    this.sidebar.appendChild(head);

    // Body
    var body = document.createElement("div");
    body.className = "lz-sb-body";

    // New Session
    var newBtn = document.createElement("button");
    newBtn.type = "button";
    newBtn.className = "lz-sb-action-btn";
    newBtn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>' +
      '<span class="lz-sb-copy">New Session</span><kbd class="lz-sb-kbd">⌘N</kbd>';
    newBtn.addEventListener("click", function() { self.newSession(); });
    body.appendChild(newBtn);

    // Search
    var searchWrap = document.createElement("div");
    searchWrap.className = "lz-sb-search-wrap";
    searchWrap.innerHTML = '<input type="search" placeholder="Search sessions…" class="lz-sb-search-input">' +
      '<span class="lz-sb-search-icon"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></span>';
    var searchInput = searchWrap.querySelector("input");
    searchInput.addEventListener("input", function() {
      self.filterSidebarSessions(searchInput.value.trim().toLowerCase());
    });
    body.appendChild(searchWrap);

    // Sessions List
    var recentHead = document.createElement("div");
    recentHead.className = "lz-sb-label-row";
    recentHead.textContent = "Recent Sessions";
    body.appendChild(recentHead);

    this.sessionListEl = document.createElement("div");
    this.sessionListEl.className = "lz-sb-recents-list";
    body.appendChild(this.sessionListEl);

    this.sidebar.appendChild(body);

    // Footer
    var foot = document.createElement("div");
    foot.className = "lz-sb-footer";

    // Daemon Runtime Card
    var machineCard = document.createElement("button");
    machineCard.type = "button";
    machineCard.className = "lz-sb-action-btn";
    machineCard.style.justifyContent = "space-between";
    machineCard.innerHTML = '<div style="display:flex;align-items:center;gap:8px;"><span class="code-status-dot ' + (this.daemonOnline ? "online" : "") + '"></span>' +
      '<span class="lz-sb-copy" style="font-size:12px;">' + (this.daemonOnline ? "Runtime: Online" : "Runtime: Offline") + '</span></div>' +
      '<span class="code-machine-chevron"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></span>';
    machineCard.addEventListener("click", function() {
      self.openWorkspacePane("connect");
    });
    foot.appendChild(machineCard);

    // Theme Switcher
    var themeToggle = document.createElement("div");
    themeToggle.className = "lz-theme-toggle";
    var isDark = document.documentElement.getAttribute("data-theme") === "dark";
    var sunBtn = document.createElement("button");
    sunBtn.type = "button";
    sunBtn.className = "lz-theme-toggle-btn" + (!isDark ? " active" : "");
    sunBtn.title = "Light theme";
    sunBtn.innerHTML = I.sun({ size: 13 });
    var moonBtn = document.createElement("button");
    moonBtn.type = "button";
    moonBtn.className = "lz-theme-toggle-btn" + (isDark ? " active" : "");
    moonBtn.title = "Dark theme";
    moonBtn.innerHTML = I.moon({ size: 13 });

    sunBtn.addEventListener("click", function() {
      document.documentElement.removeAttribute("data-theme");
      sunBtn.classList.add("active");
      moonBtn.classList.remove("active");
      try { localStorage.setItem("lz-theme", "light"); } catch(e){}
    });
    moonBtn.addEventListener("click", function() {
      document.documentElement.setAttribute("data-theme", "dark");
      moonBtn.classList.add("active");
      sunBtn.classList.remove("active");
      try { localStorage.setItem("lz-theme", "dark"); } catch(e){}
    });
    themeToggle.appendChild(sunBtn);
    themeToggle.appendChild(moonBtn);
    foot.appendChild(themeToggle);

    // User Profile
    if (CFG.username) {
      var userCard = document.createElement("div");
      userCard.className = "lz-sb-user-card";
      userCard.innerHTML = I.user({ size: 14 }) + '<span class="lz-sb-user-name lz-sb-copy">' + esc(CFG.username) + '</span>';
      foot.appendChild(userCard);
    }
    this.sidebar.appendChild(foot);
  };

  CodeHarness.prototype.renderSidebarSessions = function() {
    var self = this;
    if (!this.sessionListEl) return;
    this.sessionListEl.innerHTML = "";
    var list = Array.from(this.sessions.values()).sort(function(a, b) {
      return (b.updated_at || b.updatedAt || 0) - (a.updated_at || a.updatedAt || 0);
    });

    list.forEach(function(ses) {
      var item = document.createElement("button");
      item.type = "button";
      item.className = "lz-sb-recent-item" + (ses.id === self.activeSessionId ? " active" : "");
      item.innerHTML = '<span class="lz-sb-recent-title">' + esc(ses.name || ses.title || "New session") + '</span>' +
        '<span class="lz-sb-recent-del" title="Delete session">' + I.trash({ size: 12 }) + '</span>';

      item.addEventListener("click", function(e) {
        if (e.target.closest(".lz-sb-recent-del")) {
          e.stopPropagation();
          self.deleteSession(ses.id);
          return;
        }
        self.openSession(ses.id);
      });
      self.sessionListEl.appendChild(item);
    });
  };

  CodeHarness.prototype.filterSidebarSessions = function(q) {
    var items = this.sessionListEl.querySelectorAll(".lz-sb-recent-item");
    items.forEach(function(it) {
      var t = it.querySelector(".lz-sb-recent-title").textContent.toLowerCase();
      it.style.display = (!q || t.indexOf(q) !== -1) ? "flex" : "none";
    });
  };

  CodeHarness.prototype.buildMainPane = function() {
    var self = this;
    this.mainPane.innerHTML = "";

    // Tab Bar
    this.tabBar = document.createElement("div");
    this.tabBar.className = "lz-tab-bar";

    var leftSection = document.createElement("div");
    leftSection.style.display = "flex";
    leftSection.style.alignItems = "center";
    leftSection.style.gap = "8px";
    leftSection.style.flex = "1";
    leftSection.style.minWidth = "0";

    var mobileBtn = document.createElement("button");
    mobileBtn.type = "button";
    mobileBtn.className = "lz-btn-pane-toggle lz-mobile-menu-btn";
    mobileBtn.title = "Open navigation";
    mobileBtn.innerHTML = I.menu({ size: 15 });
    mobileBtn.addEventListener("click", function() {
      self.toggleMobileSidebar();
    });
    leftSection.appendChild(mobileBtn);

    this.tabListEl = document.createElement("div");
    this.tabListEl.className = "lz-tab-list";
    leftSection.appendChild(this.tabListEl);

    // New Tab Button
    var newTabBtn = document.createElement("button");
    newTabBtn.type = "button";
    newTabBtn.className = "lz-tab-new";
    newTabBtn.title = "New Tab";
    newTabBtn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>';
    newTabBtn.addEventListener("click", function() {
      self.newSession();
    });
    leftSection.appendChild(newTabBtn);

    this.tabBar.appendChild(leftSection);

    // Right Actions
    var rightSection = document.createElement("div");
    rightSection.className = "lz-tab-bar-actions";
    rightSection.style.position = "relative";

    // Branch Selector Pill
    this.branchPill = document.createElement("button");
    this.branchPill.type = "button";
    this.branchPill.className = "code-branch-pill code-popover-trigger";
    this.branchPill.title = "Git Branch";
    this.branchPill.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 3v12M18 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18 9a9 9 0 0 1-9 9"/></svg>' +
      '<span class="code-branch-label">' + esc(this.daemonInfo.git_branch || "main") + '</span>' +
      '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>';
    this.branchPill.addEventListener("click", function(e) {
      e.stopPropagation();
      self.toggleBranchPopover(rightSection);
    });
    rightSection.appendChild(this.branchPill);

    // Toggle Workspace Pane
    var togglePaneBtn = document.createElement("button");
    togglePaneBtn.type = "button";
    togglePaneBtn.className = "lz-btn-pane-toggle";
    togglePaneBtn.title = "Toggle Workspace Pane";
    togglePaneBtn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18"/></svg>';
    togglePaneBtn.addEventListener("click", function() {
      var cur = self.artifactPane.style.display !== "none";
      self.artifactPane.style.display = cur ? "none" : "flex";
    });
    rightSection.appendChild(togglePaneBtn);

    this.tabBar.appendChild(rightSection);
    this.mainPane.appendChild(this.tabBar);

    // Thread Scroll Area
    this.threadScroll = document.createElement("div");
    this.threadScroll.className = "lz-thread-scroll";
    this.threadWrap = document.createElement("div");
    this.threadWrap.className = "lz-thread-wrap";
    this.threadScroll.appendChild(this.threadWrap);
    this.mainPane.appendChild(this.threadScroll);

    // Floating Composer Container
    this.promptContainer = document.createElement("div");
    this.promptContainer.className = "lz-promptbar-shell";
    this.buildComposer();
    this.mainPane.appendChild(this.promptContainer);
  };

  CodeHarness.prototype.renderTabs = function() {
    var self = this;
    if (!this.tabListEl) return;
    this.tabListEl.innerHTML = "";
    this.tabs.forEach(function(tab) {
      var item = document.createElement("button");
      item.type = "button";
      item.className = "lz-tab" + (tab.id === self.activeSessionId ? " active" : "");
      item.innerHTML = '<span class="lz-tab-title">' + esc(tab.name || tab.title || "Session") + '</span>' +
        '<span class="lz-tab-close" title="Close tab">' + I.close({ size: 11 }) + '</span>';

      item.addEventListener("click", function(e) {
        if (e.target.closest(".lz-tab-close")) {
          e.stopPropagation();
          self.closeTab(tab.id);
          return;
        }
        self.openSession(tab.id);
      });
      self.tabListEl.appendChild(item);
    });
  };

  CodeHarness.prototype.closeTab = function(id) {
    this.tabs = this.tabs.filter(function(t) { return t.id !== id; });
    if (this.activeSessionId === id) {
      if (this.tabs.length) this.openSession(this.tabs[this.tabs.length - 1].id);
      else this.newSession();
    } else {
      this.renderTabs();
    }
  };

  CodeHarness.prototype.toggleMobileSidebar = function() {
    var cur = this.sidebar.dataset.mobileOpen === "true";
    this.sidebar.dataset.mobileOpen = cur ? "false" : "true";
    if (this.scrim) this.scrim.classList.toggle("show", !cur);
  };

  CodeHarness.prototype.closeMobileSidebar = function() {
    this.sidebar.dataset.mobileOpen = "false";
    if (this.scrim) this.scrim.classList.remove("show");
  };

  CodeHarness.prototype.toggleBranchPopover = function(anchor) {
    if (this.activePopover && this.activePopover.dataset.popType === "branch") {
      this.closeActivePopover();
      return;
    }
    this.closeActivePopover();

    var self = this;
    var pop = document.createElement("div");
    pop.className = "code-popover pop-down";
    pop.dataset.popType = "branch";
    pop.style.right = "0";
    pop.style.left = "auto";

    pop.innerHTML = '<div class="code-popover-head"><span>Git Workspace</span><button type="button" class="lz-btn-icon sm" id="popClose">' + I.close({ size: 12 }) + '</button></div>' +
      '<div class="code-popover-body"><div style="display:flex;align-items:center;justify-content:center;padding:20px;"><span class="lz-think-step-spin"></span></div></div>';

    pop.querySelector("#popClose").addEventListener("click", function(){ self.closeActivePopover(); });
    anchor.appendChild(pop);
    this.activePopover = pop;

    this.api.git("status").then(function(res) {
      var body = pop.querySelector(".code-popover-body");
      if (!body) return;
      var curBranch = (res && res.branch) || self.daemonInfo.git_branch || "main";
      var branches = (res && res.branches) || [curBranch];

      var html = '<div class="code-popover-group-title">Active Branch</div>' +
        '<div class="code-popover-item active"><span>✓ ' + esc(curBranch) + '</span><span class="code-model-tag">' + ((res && res.clean) ? "Clean" : "Modified") + '</span></div>';

      if (branches.length > 1) {
        html += '<div class="code-popover-group-title">Other Branches</div>';
        branches.forEach(function(b) {
          if (b !== curBranch) {
            html += '<button type="button" class="code-popover-item branch-switch-btn" data-branch="' + esc(b) + '"><span>' + esc(b) + '</span></button>';
          }
        });
      }

      body.innerHTML = html;

      body.querySelectorAll(".branch-switch-btn").forEach(function(btn) {
        btn.addEventListener("click", function() {
          var targetBranch = btn.dataset.branch;
          self.api.term(self.activeSessionId, "git checkout " + targetBranch).then(function() {
            toast("Switched to " + targetBranch);
            self.daemonInfo.git_branch = targetBranch;
            var lbl = self.branchPill.querySelector(".code-branch-label");
            if (lbl) lbl.textContent = targetBranch;
            self.closeActivePopover();
            self.refreshGitChanges();
          });
        });
      });
    }).catch(function() {
      var body = pop.querySelector(".code-popover-body");
      if (body) body.innerHTML = '<div style="padding:10px 8px;font-size:12px;color:var(--ink-3);">Daemon offline or not a Git repo</div>';
    });
  };

  CodeHarness.prototype.newSession = function(skipPushState) {
    var self = this;
    this.activeSessionId = "";
    this.closeMobileSidebar();
    document.title = "Neby Code — Local AI IDE";

    this.api.createSession({
      name: "New coding session",
      provider: this.selectedModel.provider || "tryingopen",
      provider_id: this.selectedModel.provider_id || "",
      model: this.selectedModel.model || "",
      effort: this.selectedEffort,
      mode: this.selectedMode
    }).then(function(d) {
      var ses = d.session;
      self.sessions.set(ses.id, ses);
      self.tabs.push(ses);
      self.activeSessionId = ses.id;
      if (!skipPushState && window.location.pathname !== "/code/" + ses.id + "/") {
        history.pushState({ sessionId: ses.id }, "", "/code/" + ses.id + "/");
      }
      self.renderTabs();
      self.renderSidebarSessions();
      self.renderEmptyState();
    }).catch(function() {
      self.renderEmptyState();
    });
  };

  CodeHarness.prototype.openSession = function(id, skipPushState) {
    var self = this;
    if (!id) return;
    this.activeSessionId = id;
    this.closeMobileSidebar();

    if (!skipPushState && window.location.pathname !== "/code/" + id + "/") {
      history.pushState({ sessionId: id }, "", "/code/" + id + "/");
    }

    var existingTab = this.tabs.find(function(t) { return t.id === id; });
    if (!existingTab) {
      var sesObj = this.sessions.get(id) || { id: id, name: "Coding Session" };
      this.tabs.push(sesObj);
    }
    this.renderTabs();
    this.renderSidebarSessions();

    if (window.WS && typeof window.WS.subscribe === "function") {
      window.WS.subscribe("code.ui." + id);
    }

    this.threadWrap.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;padding:40px;"><span class="lz-think-step-spin"></span></div>';

    this.api.session(id).then(function(d) {
      self.sessions.set(id, d.session);
      if (d.session && d.session.name) {
        document.title = d.session.name + " — Neby Code";
        var t = self.tabs.find(function(tab){ return tab.id === id; });
        if (t) t.name = d.session.name;
      }
      self.renderTabs();
      self.renderSidebarSessions();
      self.threadWrap.innerHTML = "";

      if (!d.messages || !d.messages.length) {
        self.renderEmptyState();
        return;
      }

      d.messages.forEach(function(m) {
        if (m.role === "user") {
          self.appendUserBubble(m.content, (m.meta && m.meta.attachments) || []);
        } else {
          self.appendAssistantResponse(m);
        }
      });
      self.scrollToBottom();
    }).catch(function(err) {
      toast((err && err.message) || "Could not load session", true);
    });

    this.refreshGitChanges();
  };

  CodeHarness.prototype.deleteSession = function(id) {
    var self = this;
    if (!confirm("Delete this coding session?")) return;
    this.sessions.delete(id);
    this.tabs = this.tabs.filter(function(t){ return t.id !== id; });
    if (this.activeSessionId === id) {
      if (this.tabs.length) this.openSession(this.tabs[this.tabs.length - 1].id);
      else this.newSession();
    } else {
      this.renderTabs();
      this.renderSidebarSessions();
    }
    this.api.deleteSession(id).then(function() {
      toast("Session deleted");
    }).catch(function(){});
  };

  CodeHarness.prototype.renderEmptyState = function() {
    var self = this;
    this.threadWrap.innerHTML = "";

    var empty = document.createElement("div");
    empty.className = "code-empty-state";

    var icon = document.createElement("div");
    icon.className = "code-empty-icon";
    icon.innerHTML = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 16 4-4-4-4M6 8l-4 4 4 4M14.5 4l-5 16"/></svg>';
    empty.appendChild(icon);

    var title = document.createElement("h2");
    title.className = "code-empty-title";
    title.textContent = "What code are we building today?";
    empty.appendChild(title);

    var sub = document.createElement("p");
    sub.className = "code-empty-sub";
    sub.textContent = "Neby Code connects to your local codebase to read files, run terminal commands, and implement changes with real-time Git diffs.";
    empty.appendChild(sub);

    var grid = document.createElement("div");
    grid.className = "code-suggestions-grid";

    var suggestions = [
      { icon: "⚡", head: "Inspect Project Architecture", desc: "Scan workspace structure, dependencies, and entrypoints." },
      { icon: "🐛", head: "Debug & Fix Errors", desc: "Analyze failing tests, runtime logs, or type errors." },
      { icon: "🛠️", head: "Refactor & Modernize", desc: "Clean up codebase, extract modular helpers, and optimize." },
      { icon: "🚀", head: "Review Git Changes & Diffs", desc: "Inspect changed files, staged hunks, and prepare commits." }
    ];

    suggestions.forEach(function(s) {
      var card = document.createElement("button");
      card.type = "button";
      card.className = "code-sugg-card";
      card.innerHTML = '<div class="code-sugg-head"><span class="code-sugg-icon">' + s.icon + '</span><span>' + esc(s.head) + '</span></div>' +
        '<div class="code-sugg-desc">' + esc(s.desc) + '</div>';
      card.addEventListener("click", function() {
        if (self.promptInput) {
          self.promptInput.value = s.head + " in this workspace";
          self.promptInput.focus();
        }
      });
      grid.appendChild(card);
    });

    empty.appendChild(grid);
    this.threadWrap.appendChild(empty);
  };

  CodeHarness.prototype.appendUserBubble = function(content, attachments) {
    var row = document.createElement("div");
    row.className = "lz-user-bubble-row";

    var bubble = document.createElement("div");
    bubble.className = "lz-user-bubble";
    bubble.textContent = content;

    if (attachments && attachments.length) {
      var attWrap = document.createElement("div");
      attWrap.className = "lz-user-meta";
      attWrap.textContent = "📎 " + attachments.map(function(a){ return a.name || a; }).join(", ");
      bubble.appendChild(attWrap);
    }

    row.appendChild(bubble);
    this.threadWrap.appendChild(row);
    this.scrollToBottom();
  };

  CodeHarness.prototype.appendAssistantResponse = function(msg) {
    var self = this;
    var msgWrap = document.createElement("div");
    msgWrap.className = "lz-assistant-msg";

    var meta = msg.meta || {};

    if (meta.thinking || meta.thought || (meta.tools && meta.tools.length)) {
      var variant = (meta.tools && meta.tools.length) ? "Coding" : "Reasoning";
      var rows = [];
      if (meta.tools && meta.tools.length) {
        meta.tools.forEach(function(t) {
          rows.push({
            primary: t.name || t.tool || "Action",
            secondary: t.summary || t.args_preview || "",
            add: t.add,
            del: t.del
          });
        });
      } else if (meta.thinking || meta.thought) {
        rows.push({ primary: meta.thinking || meta.thought });
      }

      if (P.createThinkingState) {
        var tState = P.createThinkingState({
          variant: variant,
          isDone: true,
          doneTitle: variant === "Coding" ? "Inspected & executed actions" : "Thought for a moment",
          rows: rows
        });
        msgWrap.appendChild(tState.el);
      }
    }

    if (msg.content) {
      var textHolder = document.createElement("div");
      textHolder.className = "lz-markdown-body";
      textHolder.innerHTML = parseMarkdown(msg.content || "");
      bindCopyButtons(textHolder);
      msgWrap.appendChild(textHolder);
    }

    var actionRow = document.createElement("div");
    actionRow.className = "lz-turn-actions";
    actionRow.innerHTML = '<button type="button" class="lz-turn-btn lz-turn-copy" title="Copy response">' + I.copy({ size: 13 }) + '<span>Copy</span></button>' +
      '<button type="button" class="lz-turn-btn lz-turn-retry" title="Retry prompt">' + I.refresh({ size: 13 }) + '<span>Retry</span></button>';

    var copyBtn = actionRow.querySelector(".lz-turn-copy");
    copyBtn.addEventListener("click", function() {
      navigator.clipboard.writeText(msg.content || "").then(function() {
        copyBtn.innerHTML = I.check({ size: 13 }) + '<span>Copied</span>';
        setTimeout(function() { copyBtn.innerHTML = I.copy({ size: 13 }) + '<span>Copy</span>'; }, 1800);
      });
    });

    var retryBtn = actionRow.querySelector(".lz-turn-retry");
    retryBtn.addEventListener("click", function() {
      if (self.promptInput) {
        self.promptInput.value = "Please retry the previous request";
        self.submitUserPrompt();
      }
    });

    msgWrap.appendChild(actionRow);
    this.threadWrap.appendChild(msgWrap);
    this.scrollToBottom();
  };

  CodeHarness.prototype.scrollToBottom = function() {
    var self = this;
    requestAnimationFrame(function() {
      self.threadScroll.scrollTop = self.threadScroll.scrollHeight;
    });
  };

  CodeHarness.prototype.buildWorkspacePane = function() {
    var self = this;
    this.artifactPane.innerHTML = "";

    var head = document.createElement("div");
    head.className = "lz-pane-header";

    var tabs = document.createElement("div");
    tabs.className = "code-pane-tabs";

    var tabChanges = document.createElement("button");
    tabChanges.type = "button";
    tabChanges.className = "code-pane-tab-btn" + (this.activePanel === "changes" ? " active" : "");
    tabChanges.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/></svg><span>Changes</span><span class="code-badge-count" id="codeDiffCount">0</span>';
    tabChanges.addEventListener("click", function() { self.openWorkspacePane("changes"); });
    tabs.appendChild(tabChanges);

    var tabFiles = document.createElement("button");
    tabFiles.type = "button";
    tabFiles.className = "code-pane-tab-btn" + (this.activePanel === "files" ? " active" : "");
    tabFiles.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/></svg><span>Files</span>';
    tabFiles.addEventListener("click", function() { self.openWorkspacePane("files"); });
    tabs.appendChild(tabFiles);

    var tabTerm = document.createElement("button");
    tabTerm.type = "button";
    tabTerm.className = "code-pane-tab-btn" + (this.activePanel === "term" ? " active" : "");
    tabTerm.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m4 17 6-6-6-6M12 19h8"/></svg><span>Terminal</span>';
    tabTerm.addEventListener("click", function() { self.openWorkspacePane("term"); });
    tabs.appendChild(tabTerm);

    head.appendChild(tabs);

    var actions = document.createElement("div");
    actions.className = "lz-pane-actions";

    var refreshBtn = document.createElement("button");
    refreshBtn.type = "button";
    refreshBtn.className = "lz-btn-icon";
    refreshBtn.title = "Refresh Workspace";
    refreshBtn.innerHTML = I.refresh({ size: 14 });
    refreshBtn.addEventListener("click", function() { self.refreshCurrentWorkspacePanel(); });
    actions.appendChild(refreshBtn);

    var closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "lz-btn-icon";
    closeBtn.title = "Close Pane";
    closeBtn.innerHTML = I.close({ size: 14 });
    closeBtn.addEventListener("click", function() { self.artifactPane.style.display = "none"; });
    actions.appendChild(closeBtn);

    head.appendChild(actions);
    this.artifactPane.appendChild(head);

    this.paneBody = document.createElement("div");
    this.paneBody.className = "lz-pane-body";
    this.artifactPane.appendChild(this.paneBody);

    this.renderCurrentWorkspacePanel();
  };

  CodeHarness.prototype.openWorkspacePane = function(tabName) {
    this.activePanel = tabName;
    this.artifactPane.style.display = "flex";
    var btns = this.artifactPane.querySelectorAll(".code-pane-tab-btn");
    btns.forEach(function(b) {
      var isCur = b.textContent.toLowerCase().indexOf(tabName) !== -1;
      b.classList.toggle("active", isCur);
    });
    this.renderCurrentWorkspacePanel();
  };

  CodeHarness.prototype.renderCurrentWorkspacePanel = function() {
    if (!this.paneBody) return;
    this.paneBody.innerHTML = "";

    if (this.activePanel === "changes") {
      this.renderChangesView();
    } else if (this.activePanel === "files") {
      this.renderFilesView();
    } else if (this.activePanel === "term") {
      this.renderTerminalView();
    } else if (this.activePanel === "connect") {
      this.renderConnectView();
    }
  };

  CodeHarness.prototype.renderChangesView = function() {
    var self = this;
    var container = document.createElement("div");
    container.className = "code-changes-container";

    var fileBar = document.createElement("div");
    fileBar.className = "code-changes-files-bar";

    if (!this.changes.length) {
      fileBar.innerHTML = '<span style="font-size:12px;color:var(--ink-3);">No pending changes</span>';
    } else {
      this.changes.forEach(function(ch) {
        var chip = document.createElement("button");
        chip.type = "button";
        chip.className = "code-file-chip-btn" + (ch.file === self.activeDiffFile ? " active" : "");
        chip.innerHTML = '<span>' + esc(ch.file) + '</span>' +
          '<span class="text-green">+' + (ch.add || 0) + '</span><span class="text-red">−' + (ch.del || 0) + '</span>';
        chip.addEventListener("click", function() {
          self.activeDiffFile = ch.file;
          self.renderChangesView();
        });
        fileBar.appendChild(chip);
      });
    }
    container.appendChild(fileBar);

    var diffScroll = document.createElement("div");
    diffScroll.className = "code-diff-scroll";

    var activeChange = this.changes.find(function(c){ return c.file === self.activeDiffFile; }) || this.changes[0];
    if (activeChange && activeChange.diff) {
      var lines = activeChange.diff.split("\n");
      lines.forEach(function(l, i) {
        var row = document.createElement("div");
        row.className = "code-diff-line" + (l.startsWith("+") ? " added" : (l.startsWith("-") ? " deleted" : (l.startsWith("@") ? " info" : "")));
        row.innerHTML = '<span class="code-diff-num">' + (i + 1) + '</span><span>' + esc(l) + '</span>';
        diffScroll.appendChild(row);
      });
    } else {
      diffScroll.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:var(--ink-3);gap:8px;">' +
        '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/></svg>' +
        '<span>Clean working directory — no diffs</span></div>';
    }
    container.appendChild(diffScroll);
    this.paneBody.appendChild(container);
  };

  CodeHarness.prototype.renderFilesView = function() {
    var self = this;
    var layout = document.createElement("div");
    layout.className = "code-files-layout";

    var treeSidebar = document.createElement("div");
    treeSidebar.className = "code-tree-sidebar";

    // Toolbar
    var treeToolbar = document.createElement("div");
    treeToolbar.className = "code-tree-toolbar";
    treeToolbar.innerHTML = '<span style="font-size:11.5px;font-weight:600;color:var(--ink-3);text-transform:uppercase;">Workspace Files</span>' +
      '<button type="button" class="lz-btn-icon sm" id="treeRefreshBtn" title="Refresh Tree">' + I.refresh({ size: 12 }) + '</button>';
    treeSidebar.appendChild(treeToolbar);

    // Search
    var treeSearch = document.createElement("div");
    treeSearch.className = "code-tree-search";
    treeSearch.innerHTML = '<input type="search" placeholder="Filter files…" class="code-tree-search-input">';
    treeSidebar.appendChild(treeSearch);

    var treeScroll = document.createElement("div");
    treeScroll.className = "code-tree-scroll";
    treeSidebar.appendChild(treeScroll);

    function loadTreeData() {
      treeScroll.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;padding:20px;"><span class="lz-think-step-spin"></span></div>';
      self.api.fsTree(4).then(function(res) {
        var nodes = (res && (res.tree || res.nodes)) || [];
        self.fileTree = nodes;
        renderTreeNodes(nodes);
      }).catch(function() {
        treeScroll.innerHTML = '<div style="padding:10px 8px;font-size:12px;color:var(--ink-3);">Daemon offline</div>';
      });
    }

    function renderTreeNodes(nodes, filter) {
      treeScroll.innerHTML = "";
      if (!nodes.length) {
        treeScroll.innerHTML = '<div style="padding:10px 8px;font-size:12px;color:var(--ink-3);">No files found</div>';
        return;
      }
      nodes.forEach(function(node) {
        var p = node.path || node.name || "";
        if (filter && p.toLowerCase().indexOf(filter) === -1) return;
        var it = document.createElement("div");
        it.className = "code-tree-item" + (node.is_dir ? " is-dir" : "") + (p === self.activeFilePath ? " active" : "");
        it.innerHTML = (node.is_dir
          ? '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/></svg>'
          : '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>') +
          '<span>' + esc(p) + '</span>';
        if (!node.is_dir) {
          it.addEventListener("click", function() {
            treeScroll.querySelectorAll(".code-tree-item").forEach(function(el){ el.classList.remove("active"); });
            it.classList.add("active");
            self.loadFileInEditor(p);
          });
        }
        treeScroll.appendChild(it);
      });
    }

    var searchInput = treeSearch.querySelector(".code-tree-search-input");
    searchInput.addEventListener("input", function() {
      renderTreeNodes(self.fileTree, searchInput.value.trim().toLowerCase());
    });

    treeToolbar.querySelector("#treeRefreshBtn").addEventListener("click", function() {
      loadTreeData();
    });

    loadTreeData();
    layout.appendChild(treeSidebar);

    // Editor Area
    var editorArea = document.createElement("div");
    editorArea.className = "code-editor-area";

    var editorHead = document.createElement("div");
    editorHead.className = "code-editor-head";
    editorHead.innerHTML = '<div style="display:flex;align-items:center;gap:8px;"><span id="codeEditorFilename" style="font-weight:600;">' + esc(this.activeFilePath || "Select a file to inspect") + '</span><span class="code-model-tag" id="codeEditorLines">0 lines</span></div>' +
      '<div style="display:flex;align-items:center;gap:6px;"><button type="button" class="lz-btn-icon sm" id="codeCopyFileBtn" title="Copy code">' + I.copy({ size: 13 }) + '</button>' +
      '<button type="button" class="code-mode-chip" id="codeSaveBtn" style="padding:3px 8px;font-size:11.5px;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/></svg><span>Save</span></button></div>';
    editorArea.appendChild(editorHead);

    var editorWrap = document.createElement("div");
    editorWrap.className = "code-editor-wrap";

    this.editorGutter = document.createElement("div");
    this.editorGutter.className = "code-editor-gutter";
    this.editorGutter.innerHTML = "1";
    editorWrap.appendChild(this.editorGutter);

    this.editorTextarea = document.createElement("textarea");
    this.editorTextarea.className = "code-editor-textarea";
    this.editorTextarea.placeholder = "Select a file from the tree to view and edit...";
    this.editorTextarea.spellcheck = false;

    this.editorTextarea.addEventListener("scroll", function() {
      self.editorGutter.scrollTop = self.editorTextarea.scrollTop;
    });

    this.editorTextarea.addEventListener("input", function() {
      self.updateEditorGutter();
    });

    editorWrap.appendChild(this.editorTextarea);
    editorArea.appendChild(editorWrap);

    var copyBtn = editorHead.querySelector("#codeCopyFileBtn");
    copyBtn.addEventListener("click", function() {
      if (!self.editorTextarea.value) return;
      navigator.clipboard.writeText(self.editorTextarea.value).then(function() {
        toast("Code copied to clipboard");
      });
    });

    var saveBtn = editorHead.querySelector("#codeSaveBtn");
    saveBtn.addEventListener("click", function() {
      if (!self.activeFilePath) return;
      self.api.fsWrite(self.activeFilePath, self.editorTextarea.value).then(function() {
        toast("File saved");
        self.refreshGitChanges();
      }).catch(function(err) {
        toast((err && err.message) || "Failed to save", true);
      });
    });

    layout.appendChild(editorArea);
    this.paneBody.appendChild(layout);

    if (this.activeFilePath) {
      this.loadFileInEditor(this.activeFilePath);
    }
  };

  CodeHarness.prototype.updateEditorGutter = function() {
    if (!this.editorTextarea || !this.editorGutter) return;
    var lines = this.editorTextarea.value.split("\n").length;
    var nums = [];
    for (var i = 1; i <= lines; i++) nums.push(i);
    this.editorGutter.innerHTML = nums.join("<br>");
    var linesEl = document.getElementById("codeEditorLines");
    if (linesEl) linesEl.textContent = lines + " lines";
  };

  CodeHarness.prototype.loadFileInEditor = function(path) {
    var self = this;
    this.activeFilePath = path;
    var filenameEl = document.getElementById("codeEditorFilename");
    if (filenameEl) filenameEl.textContent = path;
    if (this.editorTextarea) this.editorTextarea.value = "Loading " + path + "...";

    this.api.fsRead(path).then(function(res) {
      if (self.editorTextarea) {
        var content = (res && (res.content != null ? res.content : res)) || "";
        self.editorTextarea.value = content;
        self.updateEditorGutter();
      }
    }).catch(function(err) {
      if (self.editorTextarea) {
        self.editorTextarea.value = "Failed to load file: " + ((err && err.message) || "Error");
        self.updateEditorGutter();
      }
    });
  };

  CodeHarness.prototype.renderTerminalView = function() {
    var self = this;
    var wrap = document.createElement("div");
    wrap.className = "code-term-wrap";

    var head = document.createElement("div");
    head.className = "code-term-head";
    head.innerHTML = '<span>Integrated Workspace Terminal</span>' +
      '<button type="button" class="lz-btn-icon" style="color:inherit;" id="codeTermClear">Clear</button>';
    wrap.appendChild(head);

    this.termOutput = document.createElement("div");
    this.termOutput.className = "code-term-output";
    this.termOutput.innerHTML = '<span style="color:#6b7280;">Neby Code Terminal Ready\nType any shell command to execute directly on the local workspace.\n\n</span>';
    wrap.appendChild(this.termOutput);

    var promptRow = document.createElement("div");
    promptRow.className = "code-term-prompt-row";
    promptRow.innerHTML = '<span class="code-term-symbol">neby-code $</span>' +
      '<input type="text" class="code-term-input" placeholder="e.g. pytest, git status, npm test...">';
    wrap.appendChild(promptRow);

    var input = promptRow.querySelector(".code-term-input");
    input.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        var cmd = input.value.trim();
        if (!cmd) return;
        input.value = "";
        self.termOutput.innerHTML += '\n<span style="color:#10b981;">neby-code $ ' + esc(cmd) + '</span>\n';
        self.api.term(self.activeSessionId, cmd).then(function(res) {
          var out = (res && res.data && res.data.output) || (res && res.output) || "Command completed";
          self.termOutput.innerHTML += '<span style="color:#d1d5db;">' + esc(out) + '</span>\n';
          self.termOutput.scrollTop = self.termOutput.scrollHeight;
          self.refreshGitChanges();
        }).catch(function(err) {
          self.termOutput.innerHTML += '<span style="color:#ef4444;">Error: ' + esc((err && err.message) || "Failed") + '</span>\n';
          self.termOutput.scrollTop = self.termOutput.scrollHeight;
        });
      }
    });

    var clearBtn = head.querySelector("#codeTermClear");
    clearBtn.addEventListener("click", function() {
      self.termOutput.innerHTML = "";
    });

    this.paneBody.appendChild(wrap);
  };

  CodeHarness.prototype.renderConnectView = function() {
    var self = this;
    var wrap = document.createElement("div");
    wrap.className = "code-connect-modal";
    wrap.innerHTML = '<h3 style="margin:0 0 8px;font-size:16px;font-weight:600;color:var(--ink);">Connect Local Workspace</h3>' +
      '<p style="margin:0 0 16px;font-size:13px;color:var(--ink-2);line-height:1.5;">Run this command in your project directory to link your local files, Git repository, and terminal to Neby Code:</p>';

    this.api.connection().then(function(res) {
      var cmd = res.command || 'python -m neby_code --workspace . --ws-url "' + (res.ws_url || "") + '" --ticket "' + (res.ticket || "") + '"';
      var box = document.createElement("div");
      box.className = "code-cli-box";
      box.innerHTML = '<span>' + esc(cmd) + '</span>' +
        '<button type="button" class="code-cli-copy-btn">Copy</button>';
      var cBtn = box.querySelector(".code-cli-copy-btn");
      cBtn.addEventListener("click", function() {
        navigator.clipboard.writeText(cmd).then(function() {
          cBtn.textContent = "Copied!";
          setTimeout(function(){ cBtn.textContent = "Copy"; }, 1800);
        });
      });
      wrap.appendChild(box);
    }).catch(function() {
      wrap.innerHTML += '<p style="color:var(--red);">Could not generate connection token. Please log in again.</p>';
    });

    this.paneBody.appendChild(wrap);
  };

  CodeHarness.prototype.refreshCurrentWorkspacePanel = function() {
    if (this.activePanel === "changes") this.refreshGitChanges();
    else this.renderCurrentWorkspacePanel();
  };

  CodeHarness.prototype.refreshGitChanges = function() {
    var self = this;
    this.api.git("diff").then(function(res) {
      self.changes = (res && res.files) || [];
      var countEl = document.getElementById("codeDiffCount");
      if (countEl) countEl.textContent = self.changes.length;
      if (self.activePanel === "changes") self.renderChangesView();
    }).catch(function() {});
  };

  CodeHarness.prototype.checkDaemonStatus = function() {
    var self = this;
    this.api.status().then(function(res) {
      self.daemonOnline = !!res.daemon_online;
      self.daemonInfo = res.info || {};
      self.updateDaemonUI();
    }).catch(function() {});
  };

  CodeHarness.prototype.updateDaemonStatus = function(d) {
    this.daemonOnline = !!(d && d.online);
    this.daemonInfo = (d && d.info) || {};
    this.updateDaemonUI();
  };

  CodeHarness.prototype.updateDaemonUI = function() {
    var self = this;
    var dots = document.querySelectorAll(".code-status-dot");
    dots.forEach(function(dot) {
      dot.classList.toggle("online", self.daemonOnline);
    });
  };

  CodeHarness.prototype.buildComposer = function() {
    var self = this;
    this.promptContainer.innerHTML = "";

    var wrap = document.createElement("div");
    wrap.className = "lz-promptbar-wrap";

    var bar = document.createElement("div");
    bar.className = "lz-promptbar";

    // Textarea
    this.promptInput = document.createElement("textarea");
    this.promptInput.className = "lz-promptbar-input";
    this.promptInput.placeholder = "Describe what code to write, refactor, or test…";
    this.promptInput.rows = 1;

    this.promptInput.addEventListener("input", function() {
      self.promptInput.style.height = "auto";
      self.promptInput.style.height = Math.min(self.promptInput.scrollHeight, 180) + "px";
    });

    this.promptInput.addEventListener("keydown", function(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        self.submitUserPrompt();
      }
    });
    bar.appendChild(this.promptInput);

    // Controls Row
    var ctrl = document.createElement("div");
    ctrl.className = "lz-promptbar-controls";

    var left = document.createElement("div");
    left.className = "lz-promptbar-left";
    left.style.position = "relative";

    // Mode Selector Chip
    this.modeBtn = document.createElement("button");
    this.modeBtn.type = "button";
    this.modeBtn.className = "code-mode-chip code-popover-trigger";
    this.modeBtn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/></svg>' +
      '<span id="codeModeLabel">' + (this.selectedMode.toUpperCase()) + '</span>';
    this.modeBtn.addEventListener("click", function(e) {
      e.stopPropagation();
      self.toggleModePopover(left);
    });
    left.appendChild(this.modeBtn);

    // Model Selector Chip
    this.modelBtn = document.createElement("button");
    this.modelBtn.type = "button";
    this.modelBtn.className = "lz-model-picker-btn code-popover-trigger";
    this.modelBtn.innerHTML = I.sparkle({ size: 13, className: "text-accent" }) +
      '<span class="lz-model-name" id="codeModelLabel">' + esc(this.selectedModel.label || this.selectedModel.model || "Model") + '</span>' +
      I.chevronDown({ size: 12 });
    this.modelBtn.addEventListener("click", function(e) {
      e.stopPropagation();
      self.toggleModelPopover(left);
    });
    left.appendChild(this.modelBtn);

    ctrl.appendChild(left);

    var right = document.createElement("div");
    right.className = "lz-promptbar-right";

    this.sendBtn = document.createElement("button");
    this.sendBtn.type = "button";
    this.sendBtn.className = "lz-promptbar-send";
    this.sendBtn.title = "Send message";
    this.sendBtn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
    this.sendBtn.addEventListener("click", function() { self.submitUserPrompt(); });
    right.appendChild(this.sendBtn);

    ctrl.appendChild(right);
    bar.appendChild(ctrl);
    wrap.appendChild(bar);
    this.promptContainer.appendChild(wrap);
  };

  CodeHarness.prototype.toggleModePopover = function(anchor) {
    if (this.activePopover && this.activePopover.dataset.popType === "mode") {
      this.closeActivePopover();
      return;
    }
    this.closeActivePopover();

    var self = this;
    var pop = document.createElement("div");
    pop.className = "code-popover";
    pop.dataset.popType = "mode";

    pop.innerHTML = '<div class="code-popover-head"><span>Agent Execution Mode</span><button type="button" class="lz-btn-icon sm" id="popClose">' + I.close({ size: 12 }) + '</button></div>' +
      '<div class="code-popover-body">' +
        '<div class="code-mode-item ' + (this.selectedMode === "agent" ? "active" : "") + '" data-mode="agent">' +
          '<div class="code-mode-icon-box"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/></svg></div>' +
          '<div class="code-mode-copy"><div class="code-mode-name">Agent Mode</div><div class="code-mode-desc">Autonomous loop with tools, file edits, and commands</div></div>' +
        '</div>' +
        '<div class="code-mode-item ' + (this.selectedMode === "plan" ? "active" : "") + '" data-mode="plan">' +
          '<div class="code-mode-icon-box"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/></svg></div>' +
          '<div class="code-mode-copy"><div class="code-mode-name">Plan Mode</div><div class="code-mode-desc">High-level architecture design and step-by-step roadmap</div></div>' +
        '</div>' +
        '<div class="code-mode-item ' + (this.selectedMode === "ask" ? "active" : "") + '" data-mode="ask">' +
          '<div class="code-mode-icon-box"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>' +
          '<div class="code-mode-copy"><div class="code-mode-name">Ask Mode</div><div class="code-mode-desc">Direct explanation, answering questions, syntax advice</div></div>' +
        '</div>' +
      '</div>';

    pop.querySelector("#popClose").addEventListener("click", function(){ self.closeActivePopover(); });

    pop.querySelectorAll(".code-mode-item").forEach(function(item) {
      item.addEventListener("click", function() {
        self.selectedMode = item.dataset.mode;
        var lbl = document.getElementById("codeModeLabel");
        if (lbl) lbl.textContent = self.selectedMode.toUpperCase();
        toast("Mode: " + self.selectedMode);
        self.closeActivePopover();
      });
    });

    anchor.appendChild(pop);
    this.activePopover = pop;
  };

  CodeHarness.prototype.toggleModelPopover = function(anchor) {
    if (this.activePopover && this.activePopover.dataset.popType === "model") {
      this.closeActivePopover();
      return;
    }
    this.closeActivePopover();

    var self = this;
    var pop = document.createElement("div");
    pop.className = "code-popover";
    pop.dataset.popType = "model";

    var head = '<div class="code-popover-head"><span>Select LLM Model</span><button type="button" class="lz-btn-icon sm" id="popClose">' + I.close({ size: 12 }) + '</button></div>';

    var effortRow = "";
    if (this.selectedModel.effort_levels && this.selectedModel.effort_levels.length > 0) {
      effortRow = '<div class="code-effort-row">' +
        '<button type="button" class="code-effort-btn ' + (this.selectedEffort === "quick" ? "active" : "") + '" data-effort="quick">⚡ Quick</button>' +
        '<button type="button" class="code-effort-btn ' + (this.selectedEffort === "balanced" ? "active" : "") + '" data-effort="balanced">⚖️ Balanced</button>' +
        '<button type="button" class="code-effort-btn ' + (this.selectedEffort === "deep" ? "active" : "") + '" data-effort="deep">🧠 Deep</button>' +
      '</div>';
    }

    var search = '<div class="code-popover-search"><input type="search" placeholder="Search models…" class="code-popover-input"></div>';

    var body = '<div class="code-popover-body">';
    (this.models.groups || []).forEach(function(g) {
      if (g.models && g.models.length) {
        body += '<div class="code-popover-group-title">' + esc(g.title || g.provider) + '</div>';
        g.models.forEach(function(m) {
          var isCur = m.provider === self.selectedModel.provider && m.model === self.selectedModel.model && (m.provider_id || "") === (self.selectedModel.provider_id || "");
          body += '<button type="button" class="code-popover-item ' + (isCur ? "active" : "") + '" data-val="' + esc(m.value || m.model) + '">' +
            '<span>' + esc(m.label || m.model) + '</span>' +
            '<span class="code-model-tag">' + (m.context_window ? Math.round(m.context_window / 1000) + 'k' : '') + '</span>' +
          '</button>';
        });
      }
    });
    body += '</div>';

    pop.innerHTML = head + effortRow + search + body;
    pop.querySelector("#popClose").addEventListener("click", function(){ self.closeActivePopover(); });

    // Effort buttons
    pop.querySelectorAll(".code-effort-btn").forEach(function(btn) {
      btn.addEventListener("click", function() {
        pop.querySelectorAll(".code-effort-btn").forEach(function(b){ b.classList.remove("active"); });
        btn.classList.add("active");
        self.selectedEffort = btn.dataset.effort;
        toast("Reasoning effort: " + self.selectedEffort);
      });
    });

    // Search filter
    var sInput = pop.querySelector(".code-popover-input");
    sInput.addEventListener("input", function() {
      var q = sInput.value.trim().toLowerCase();
      pop.querySelectorAll(".code-popover-item").forEach(function(it) {
        var t = it.textContent.toLowerCase();
        it.style.display = (!q || t.indexOf(q) !== -1) ? "flex" : "none";
      });
    });

    // Model selection
    pop.querySelectorAll(".code-popover-item").forEach(function(item) {
      item.addEventListener("click", function() {
        var val = item.dataset.val;
        var chosen = self.allModels.find(function(m){ return (m.value || m.model) === val; });
        if (chosen) {
          self.selectedModel = chosen;
          var lbl = document.getElementById("codeModelLabel");
          if (lbl) lbl.textContent = chosen.label || chosen.model;
          toast("Model: " + (chosen.label || chosen.model));
        }
        self.closeActivePopover();
      });
    });

    anchor.appendChild(pop);
    this.activePopover = pop;
  };

  CodeHarness.prototype.submitUserPrompt = function() {
    var self = this;
    var text = (this.promptInput && this.promptInput.value.trim()) || "";
    if (!text) return;

    this.promptInput.value = "";
    this.promptInput.style.height = "auto";

    var emptyEl = this.threadWrap.querySelector(".code-empty-state");
    if (emptyEl) emptyEl.remove();

    this.appendUserBubble(text);

    var msgWrap = document.createElement("div");
    msgWrap.className = "lz-assistant-msg";

    var tState = null;
    if (P.createThinkingState) {
      tState = P.createThinkingState({
        variant: "Coding",
        active: "Executing coding tools…",
        isDone: false,
        expanded: true
      });
      msgWrap.appendChild(tState.el);
    }

    var mdBody = document.createElement("div");
    mdBody.className = "lz-markdown-body";
    msgWrap.appendChild(mdBody);

    this.threadWrap.appendChild(msgWrap);
    this.scrollToBottom();

    this.sendBtn.disabled = true;
    this.startPolling();

    this.api.send(this.activeSessionId, {
      content: text,
      provider: this.selectedModel.provider || "tryingopen",
      provider_id: this.selectedModel.provider_id || "",
      model: this.selectedModel.model || "",
      effort: this.selectedEffort,
      mode: this.selectedMode
    }).then(function(res) {
      if (res.session && res.session.name) {
        var ses = self.sessions.get(self.activeSessionId);
        if (ses) {
          ses.name = res.session.name;
          self.sessions.set(self.activeSessionId, ses);
          self.renderSidebarSessions();
          self.renderTabs();
        }
      }
    }).catch(function(err) {
      self.sendBtn.disabled = false;
      self.stopPolling();
      if (tState) tState.setDone("Failed");
      mdBody.innerHTML = '<span style="color:var(--red);">' + esc((err && err.message) || "Error sending prompt") + '</span>';
      toast((err && err.message) || "Error", true);
    });
  };

  CodeHarness.prototype.onRealtimeEvent = function(event, data, ch) {
    if (!data) return;
    var sid = String(data.session_id || data.sessionId || (ch && ch.replace(/^code\.ui\./, "")) || "");
    if (sid && sid !== String(this.activeSessionId)) return;

    var lastMsg = this.threadWrap.querySelector(".lz-assistant-msg:last-child");
    if (!lastMsg) return;

    var mdBody = lastMsg.querySelector(".lz-markdown-body");
    var tStateEl = lastMsg.querySelector(".lz-thinking-state");

    if (event === "agent_delta") {
      if (mdBody) {
        var prev = mdBody.dataset.rawContent || "";
        prev += (data.content || "");
        mdBody.dataset.rawContent = prev;
        mdBody.innerHTML = parseMarkdown(prev);
        bindCopyButtons(mdBody);
        this.scrollToBottom();
      }
    } else if (event === "agent_done" || event === "agent_error") {
      this.stopPolling();
      this.sendBtn.disabled = false;
      if (tStateEl && P.createThinkingState) {
        // finalize trace
      }
      this.refreshGitChanges();
      this.scrollToBottom();
    }
  };

  window.CodeHarness = CodeHarness;
})(window);
