(function(window){
"use strict";

var I = window.LazyIcons;
var P = window.LazyPrimitives;

var CFG = window.LAZY_CONFIG || {};

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function(c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function getCsrf() {
  var v = document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
  if (v) return decodeURIComponent(v[2]);
  var inp = document.querySelector('input[name=csrfmiddlewaretoken]');
  return inp ? inp.value : (CFG.csrfToken || "");
}

function api(path, opts) {
  opts = opts || {};
  opts.headers = opts.headers || {};
  var t = getCsrf();
  if (t) opts.headers["X-CSRFToken"] = t;
  if (!(opts.body instanceof FormData)) opts.headers["Content-Type"] = "application/json";
  opts.credentials = "same-origin";
  return fetch(path, opts).then(function(r) {
    return r.json().catch(function() { return { error: "HTTP " + r.status }; }).then(function(j) {
      if (!r.ok) throw j;
      return j;
    });
  });
}

function toast(msg, err) {
  var el = document.createElement("div");
  el.className = "lz-toast" + (err ? " err" : "");
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(function() {
    el.style.opacity = "0";
    el.style.transform = "scale(0.95)";
    el.style.transition = "all 200ms ease";
    setTimeout(function() { el.remove(); }, 220);
  }, 2600);
}

/* Markdown parsing with code blocks and tables */
function renderInline(s) {
  return s
    .replace(/`([^`]+)`/g, '<code class="inline">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*\s][^*]*)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer nofollow">$1</a>');
}

function parseMarkdown(src) {
  src = String(src || "").replace(/\r\n/g, "\n");
  var blocks = [];
  src = src.replace(/```([a-zA-Z0-9_#+.-]*)\n?([\s\S]*?)```/g, function(_, lang, code) {
    var i = blocks.length;
    blocks.push(
      '<div class="code-block">' +
      '<div class="code-head"><span>' + esc((lang || "code").trim() || "code") + '</span>' +
      '<button type="button" class="code-copy" data-code="' + i + '">' + I.copy({ size: 12 }) + '<span>Copy</span></button></div>' +
      '<pre>' + esc(code.replace(/\n$/, "")) + '</pre></div>'
    );
    return "\n@@LZCODE" + i + "@@\n";
  });

  var lines = esc(src).split("\n"), out = [], inUl = false, inOl = false, listBuf = [];
  function flushList() {
    if (listBuf.length) {
      out.push("<" + (inOl ? "ol" : "ul") + ">" + listBuf.map(function(x){ return "<li>" + renderInline(x) + "</li>"; }).join("") + "</" + (inOl ? "ol" : "ul") + ">");
      listBuf = []; inUl = false; inOl = false;
    }
  }
  var para = [];
  function flushPara() {
    if (para.length) {
      out.push("<p>" + renderInline(para.join("<br>")) + "</p>");
      para = [];
    }
  }

  for (var i = 0; i < lines.length; i++) {
    var ln = lines[i], t = ln.trim();
    var cm = t.match(/^@@LZCODE(\d+)@@$/);
    if (cm) { flushPara(); flushList(); out.push(blocks[+cm[1]]); continue; }
    if (!t) { flushPara(); flushList(); continue; }
    var h = t.match(/^(#{1,6})\s+(.*)$/);
    if (h) { flushPara(); flushList(); out.push("<h3>" + renderInline(h[2]) + "</h3>"); continue; }
    if (/^(---+|\*\*\*+)$/.test(t)) { flushPara(); flushList(); out.push("<hr>"); continue; }
    if (/^&gt;\s?/.test(t)) { flushPara(); flushList(); out.push("<blockquote>" + renderInline(t.replace(/^&gt;\s?/, "")) + "</blockquote>"); continue; }
    if (/^[-*]\s+/.test(t)) { if (inOl) flushList(); inUl = true; listBuf.push(renderInline(t.replace(/^[-*]\s+/, ""))); continue; }
    if (/^\d+[.)]\s+(.*)$/.test(t)) { if (inUl) flushList(); inOl = true; listBuf.push(t.replace(/^\d+[.)]\s+/, "")); continue; }
    para.push(t);
  }
  flushPara(); flushList();
  return out.join("");
}

var SUGGESTION_POOL = [
  { id: "assign", label: "Write a high-scoring Grade 12 Physics assignment", prompt: "Write a comprehensive Grade 12 Physics assignment on Electromagnetic Induction with numerical problems.", icon: "doc" },
  { id: "report", label: "Draft a formal Chemistry laboratory report", prompt: "Draft a complete lab report for preparation of oxalic acid standard solution and titration.", icon: "sparkle" },
  { id: "notes", label: "Prepare quick revision notes for NEB Board Exams", prompt: "Summarize Grade 12 Computer Science DBMS concepts into concise revision notes.", icon: "tasks" },
  { id: "resume", label: "Create a modern student resume for internship", prompt: "Create a sleek, one-page resume for a high school graduate applying for IT internships.", icon: "user" },
  { id: "workspace", label: "Open interactive Study Records & Syllabus Grid", prompt: "/table Show NEB grade 12 subject tracker", icon: "table", workspace: true }
];

function IceCreamHarness(rootEl) {
  this.root = rootEl;
  this.sessions = new Map();
  this.activeSessionId = "";
  this.tabs = [];
  this.workspaceMode = false;
  this.artifactPaneOpen = false;
  this.currentDocHtml = "";
  this.currentDocTitle = "";
  this.streaming = false;
  this.abortController = null;
  this.suggestionOffset = 0;
  this.credits = CFG.credits || { unlimited: false, remaining: 10 };

  this.init();
}

IceCreamHarness.prototype.init = function() {
  var self = this;
  this.root.innerHTML = "";
  this.root.className = "lz-harness-root";

  // 1. Sidebar Nav
  this.sidebar = document.createElement("aside");
  this.sidebar.className = "lz-sidebar-nav";
  this.sidebar.dataset.collapsed = "false";
  this.buildSidebar();
  this.root.appendChild(this.sidebar);

  // 2. Main Stage
  this.stage = document.createElement("div");
  this.stage.className = "lz-stage";

  this.panelsRow = document.createElement("div");
  this.panelsRow.className = "lz-panels-row";

  // Main Pane
  this.mainPane = document.createElement("section");
  this.mainPane.className = "lz-main-pane";

  // Tab Bar
  this.tabBar = document.createElement("div");
  this.tabBar.className = "lz-tab-bar";

  this.mobileMenuBtn = document.createElement("button");
  this.mobileMenuBtn.type = "button";
  this.mobileMenuBtn.className = "lz-btn-pane-toggle lz-mobile-menu-btn";
  this.mobileMenuBtn.title = "Open navigation";
  this.mobileMenuBtn.innerHTML = I.menu({ size: 15 });
  this.mobileMenuBtn.addEventListener("click", function() {
    self.toggleMobileSidebar();
  });
  this.tabBar.appendChild(this.mobileMenuBtn);

  this.tabList = document.createElement("div");
  this.tabList.className = "lz-tab-list";
  this.tabBar.appendChild(this.tabList);

  this.tabActions = document.createElement("div");
  this.tabActions.className = "lz-tab-bar-actions";

  this.paneToggleBtn = document.createElement("button");
  this.paneToggleBtn.type = "button";
  this.paneToggleBtn.className = "lz-btn-pane-toggle";
  this.paneToggleBtn.title = "Toggle document panel";
  this.paneToggleBtn.innerHTML = I.doc({ size: 15 });
  this.paneToggleBtn.addEventListener("click", function() {
    self.toggleArtifactPane();
  });
  this.tabActions.appendChild(this.paneToggleBtn);
  this.tabBar.appendChild(this.tabActions);

  this.mainPane.appendChild(this.tabBar);

  // Thread scroll area
  this.threadScroll = document.createElement("div");
  this.threadScroll.className = "lz-thread-scroll";
  this.threadWrap = document.createElement("div");
  this.threadWrap.className = "lz-thread-wrap";
  this.threadScroll.appendChild(this.threadWrap);
  this.mainPane.appendChild(this.threadScroll);

  // Prompt Bar container
  this.promptContainer = document.createElement("div");
  this.mainPane.appendChild(this.promptContainer);

  this.panelsRow.appendChild(this.mainPane);

  // Artifact Pane (Right Inspector)
  this.artifactPane = document.createElement("aside");
  this.artifactPane.className = "lz-artifact-pane";
  this.artifactPane.style.display = "none";
  this.buildArtifactPane();
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

  // Initialize PromptBar
  this.promptBar = new window.LazyPromptBar(this.promptContainer, {
    onSend: function(payload) { self.handleUserPrompt(payload); },
    onStop: function() { self.stopStreaming(); },
    onUpload: function(file, cb) { self.uploadFile(file, cb); }
  });

  // Seed sessions from config
  (CFG.sessions || []).forEach(function(s) {
    self.sessions.set(s.id, s);
  });

  this.renderSidebarSessions();

  if (CFG.sessions && CFG.sessions.length > 0) {
    this.openSession(CFG.sessions[0].id);
  } else {
    this.newChat();
  }
};

IceCreamHarness.prototype.buildSidebar = function() {
  var self = this;
  this.sidebar.innerHTML = "";

  // Header
  var head = document.createElement("div");
  head.className = "lz-sb-header";

  var wsBtn = document.createElement("button");
  wsBtn.type = "button";
  wsBtn.className = "lz-sb-workspace-btn";
  wsBtn.innerHTML = '<img src="/static/web/img/n-logo-48.png" style="width:22px;height:22px;border-radius:5px;object-fit:contain;" alt="Lazy"><span class="lz-sb-workspace-name">Lazy</span>';
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
    var isCol = self.sidebar.dataset.collapsed === "true";
    self.sidebar.dataset.collapsed = isCol ? "false" : "true";
  });
  head.appendChild(colBtn);
  this.sidebar.appendChild(head);

  // Body
  var body = document.createElement("div");
  body.className = "lz-sb-body";

  // New Chat
  var newBtn = document.createElement("button");
  newBtn.type = "button";
  newBtn.className = "lz-sb-action-btn";
  newBtn.innerHTML = I.plus({ size: 16 }) + '<span class="lz-sb-copy">New Chat</span>';
  newBtn.addEventListener("click", function() { self.newChat(); });
  body.appendChild(newBtn);

  // Live Records Workspace
  var recBtn = document.createElement("button");
  recBtn.type = "button";
  recBtn.className = "lz-sb-action-btn";
  recBtn.innerHTML = I.table({ size: 16 }) + '<span class="lz-sb-copy">Study Records</span>';
  recBtn.addEventListener("click", function() { self.toggleWorkspaceMode(); });
  body.appendChild(recBtn);

  // Label & Search
  var lblRow = document.createElement("div");
  lblRow.className = "lz-sb-label-row";
  lblRow.innerHTML = '<span>Recent Chats</span>';
  body.appendChild(lblRow);

  var searchWrap = document.createElement("div");
  searchWrap.className = "lz-sb-search-wrap lz-sb-copy";
  searchWrap.innerHTML = '<input type="text" class="lz-sb-search-input" placeholder="Search chats…">' +
    '<span class="lz-sb-search-icon">' + I.search({ size: 14 }) + '</span>';
  searchWrap.querySelector("input").addEventListener("input", function(e) {
    self.filterSidebarSessions(e.target.value.toLowerCase());
  });
  body.appendChild(searchWrap);

  this.sessionListEl = document.createElement("div");
  body.appendChild(this.sessionListEl);
  this.sidebar.appendChild(body);

  // Footer
  var foot = document.createElement("div");
  foot.className = "lz-sb-footer";

  // Theme toggle
  var isDark = document.documentElement.getAttribute("data-theme") === "dark";
  var themeToggle = document.createElement("div");
  themeToggle.className = "lz-theme-toggle";
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

  // Credits Badge
  var cred = document.createElement("div");
  cred.className = "lz-sb-credits-badge";
  cred.innerHTML = I.sparkle({ size: 13, className: "text-accent" }) +
    '<span>' + (this.credits.unlimited ? "∞ credits" : (this.credits.remaining + " credits")) + '</span>';
  foot.appendChild(cred);

  // User Profile non-link badge
  if (CFG.username) {
    var userCard = document.createElement("div");
    userCard.className = "lz-sb-user-card";
    userCard.innerHTML = I.user({ size: 14 }) + '<span class="lz-sb-user-name lz-sb-copy">' + esc(CFG.username) + '</span>';
    foot.appendChild(userCard);
  }
  this.sidebar.appendChild(foot);
};

IceCreamHarness.prototype.renderSidebarSessions = function() {
  var self = this;
  if (!this.sessionListEl) return;
  this.sessionListEl.innerHTML = "";
  var list = Array.from(this.sessions.values()).sort(function(a, b) {
    return (b.updatedAt || 0) - (a.updatedAt || 0);
  });

  list.forEach(function(ses) {
    var item = document.createElement("button");
    item.type = "button";
    item.className = "lz-sb-recent-item" + (ses.id === self.activeSessionId ? " active" : "");
    item.innerHTML = '<span class="lz-sb-recent-title">' + esc(ses.title || "New chat") + '</span>' +
      '<span class="lz-sb-recent-del" title="Delete chat">' + I.trash({ size: 12 }) + '</span>';

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

IceCreamHarness.prototype.filterSidebarSessions = function(q) {
  var items = this.sessionListEl.querySelectorAll(".lz-sb-recent-item");
  items.forEach(function(it) {
    var t = it.querySelector(".lz-sb-recent-title").textContent.toLowerCase();
    it.style.display = (!q || t.indexOf(q) !== -1) ? "flex" : "none";
  });
};

IceCreamHarness.prototype.buildArtifactPane = function() {
  var self = this;
  this.artifactPane.innerHTML = "";

  var head = document.createElement("div");
  head.className = "lz-pane-header";
  this.paneTitle = document.createElement("span");
  this.paneTitle.className = "lz-pane-title";
  this.paneTitle.textContent = "Working Document";
  head.appendChild(this.paneTitle);

  var actions = document.createElement("div");
  actions.className = "lz-pane-actions";

  var expDocx = document.createElement("button");
  expDocx.className = "lz-btn-icon";
  expDocx.title = "Export DOCX";
  expDocx.innerHTML = I.doc({ size: 15 });
  expDocx.addEventListener("click", function() { self.exportDoc("docx"); });
  actions.appendChild(expDocx);

  var expPdf = document.createElement("button");
  expPdf.className = "lz-btn-icon";
  expPdf.title = "Export PDF";
  expPdf.innerHTML = I.download({ size: 15 });
  expPdf.addEventListener("click", function() { self.exportDoc("pdf"); });
  actions.appendChild(expPdf);

  var closeBtn = document.createElement("button");
  closeBtn.className = "lz-btn-icon";
  closeBtn.title = "Close Pane";
  closeBtn.innerHTML = I.close({ size: 15 });
  closeBtn.addEventListener("click", function() { self.closeArtifactPane(); });
  actions.appendChild(closeBtn);

  head.appendChild(actions);
  this.artifactPane.appendChild(head);

  this.paneBody = document.createElement("div");
  this.paneBody.className = "lz-pane-body";

  this.docTitleInput = document.createElement("input");
  this.docTitleInput.className = "lz-doc-title-bar";
  this.docTitleInput.placeholder = "Untitled document";
  this.docTitleInput.addEventListener("input", function() {
    self.currentDocTitle = self.docTitleInput.value;
    self.saveDocDebounced();
  });
  this.paneBody.appendChild(this.docTitleInput);

  this.docPaper = document.createElement("div");
  this.docPaper.className = "lz-doc-paper";
  this.docPaper.contentEditable = "true";
  this.docPaper.addEventListener("input", function() {
    self.currentDocHtml = self.docPaper.innerHTML;
    self.saveDocDebounced();
  });
  this.paneBody.appendChild(this.docPaper);

  this.artifactPane.appendChild(this.paneBody);
};

IceCreamHarness.prototype.openArtifactPane = function(html, title) {
  this.artifactPaneOpen = true;
  this.artifactPane.style.display = "flex";
  if (this.paneToggleBtn) this.paneToggleBtn.classList.add("active");
  if (html != null) {
    this.currentDocHtml = html;
    this.docPaper.innerHTML = html;
  }
  if (title != null) {
    this.currentDocTitle = title;
    this.docTitleInput.value = title;
  }
};

IceCreamHarness.prototype.closeArtifactPane = function() {
  this.artifactPaneOpen = false;
  this.artifactPane.style.display = "none";
  if (this.paneToggleBtn) this.paneToggleBtn.classList.remove("active");
};

IceCreamHarness.prototype.toggleArtifactPane = function() {
  if (this.artifactPane.style.display === "none") {
    this.openArtifactPane(this.currentDocHtml, this.currentDocTitle);
  } else {
    this.closeArtifactPane();
  }
};

IceCreamHarness.prototype.toggleMobileSidebar = function() {
  var isOpen = this.sidebar.classList.contains("open");
  if (isOpen) {
    this.closeMobileSidebar();
  } else {
    this.sidebar.classList.add("open");
    this.scrim.classList.add("open");
  }
};

IceCreamHarness.prototype.closeMobileSidebar = function() {
  this.sidebar.classList.remove("open");
  this.scrim.classList.remove("open");
};

IceCreamHarness.prototype.saveDocDebounced = function() {
  var self = this;
  clearTimeout(this._saveT);
  this._saveT = setTimeout(function() {
    if (!self.activeSessionId) return;
    api("/ajax/lazy/sessions/" + self.activeSessionId + "/doc/save/", {
      method: "POST",
      body: JSON.stringify({ html: self.currentDocHtml, title: self.currentDocTitle })
    }).catch(function(err) {
      console.warn("Doc save error", err);
    });
  }, 900);
};

IceCreamHarness.prototype.exportDoc = function(format) {
  if (!this.activeSessionId) return;
  window.open("/ajax/lazy/sessions/" + this.activeSessionId + "/export/?format=" + format, "_blank");
};

IceCreamHarness.prototype.renderTabs = function() {
  var self = this;
  this.tabList.innerHTML = "";

  this.tabs.forEach(function(tab) {
    var el = document.createElement("div");
    el.className = "lz-tab" + (tab.id === self.activeSessionId ? " active" : "");
    el.innerHTML = '<span class="lz-tab-title">' + esc(tab.title || "New chat") + '</span>' +
      '<button type="button" class="lz-tab-close" aria-label="Close tab">' + I.close({ size: 11 }) + '</button>';

    el.querySelector(".lz-tab-title").addEventListener("click", function() {
      self.openSession(tab.id);
    });
    el.querySelector(".lz-tab-close").addEventListener("click", function(e) {
      e.stopPropagation();
      self.closeTab(tab.id);
    });
    self.tabList.appendChild(el);
  });

  var newTabBtn = document.createElement("button");
  newTabBtn.type = "button";
  newTabBtn.className = "lz-tab-new";
  newTabBtn.title = "New Tab";
  newTabBtn.innerHTML = I.plus({ size: 14 });
  newTabBtn.addEventListener("click", function() { self.newChat(); });
  this.tabList.appendChild(newTabBtn);
};

IceCreamHarness.prototype.closeTab = function(id) {
  this.tabs = this.tabs.filter(function(t){ return t.id !== id; });
  if (this.activeSessionId === id) {
    if (this.tabs.length) this.openSession(this.tabs[this.tabs.length - 1].id);
    else this.newChat();
  } else {
    this.renderTabs();
  }
};

IceCreamHarness.prototype.newChat = function() {
  var self = this;
  this.activeSessionId = "";
  this.workspaceMode = false;
  this.closeArtifactPane();
  this.closeMobileSidebar();

  api("/ajax/lazy/sessions/create/", { method: "POST", body: "{}" }).then(function(d) {
    var ses = d.session;
    self.sessions.set(ses.id, ses);
    self.tabs.push(ses);
    self.activeSessionId = ses.id;
    self.renderTabs();
    self.renderSidebarSessions();
    self.renderEmptyState();
  }).catch(function() {
    self.renderEmptyState();
  });
};

IceCreamHarness.prototype.openSession = function(id) {
  var self = this;
  this.activeSessionId = id;
  this.workspaceMode = false;
  this.closeMobileSidebar();

  var existingTab = this.tabs.find(function(t){ return t.id === id; });
  if (!existingTab) {
    var sesObj = this.sessions.get(id) || { id: id, title: "Chat" };
    this.tabs.push(sesObj);
  }
  this.renderTabs();
  this.renderSidebarSessions();

  this.threadWrap.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;padding:40px;"><span class="lz-tool-spin"></span></div>';

  api("/ajax/lazy/sessions/" + id + "/", { method: "GET" }).then(function(d) {
    self.sessions.set(id, d);
    self.renderTabs();
    self.threadWrap.innerHTML = "";
    if (d.docHtml) {
      self.openArtifactPane(d.docHtml, d.docTitle);
    } else {
      self.closeArtifactPane();
    }

    if (!d.messages || !d.messages.length) {
      self.renderEmptyState();
      return;
    }

    d.messages.forEach(function(m) {
      if (m.role === "user") {
        self.appendUserBubble(m.content, m.attachments);
      } else {
        self.appendAssistantResponse(m);
      }
    });
    self.scrollToBottom();
  }).catch(function(err) {
    toast((err && err.error) || "Could not load session", true);
  });
};

IceCreamHarness.prototype.deleteSession = function(id) {
  var self = this;
  if (!confirm("Delete this chat?")) return;
  self.sessions.delete(id);
  self.tabs = self.tabs.filter(function(t){ return t.id !== id; });
  if (self.activeSessionId === id) {
    if (self.tabs.length) self.openSession(self.tabs[self.tabs.length - 1].id);
    else self.newChat();
  } else {
    self.renderTabs();
    self.renderSidebarSessions();
  }
  api("/ajax/lazy/sessions/" + id + "/delete/", { method: "POST", body: "{}" }).then(function() {
    toast("Chat deleted");
  }).catch(function() {
    // Already removed from local UI
  });
};

IceCreamHarness.prototype.renderEmptyState = function() {
  var self = this;
  this.threadWrap.innerHTML = "";

  var empty = document.createElement("div");
  empty.className = "lz-empty-state";

  var greeting = document.createElement("h1");
  greeting.className = "lz-empty-greeting";
  greeting.innerHTML = '<span class="lz-empty-sub" style="display:block;">Hello ' + esc(CFG.username || "Student") + '</span>' +
    '<span>What can I help you write today?</span>';
  empty.appendChild(greeting);

  var pool = document.createElement("div");
  pool.className = "lz-empty-suggestions";

  var items = [0, 1, 2].map(function(i) {
    return SUGGESTION_POOL[(self.suggestionOffset + i) % SUGGESTION_POOL.length];
  });

  items.forEach(function(item) {
    var card = document.createElement("button");
    card.type = "button";
    card.className = "lz-suggestion-card";
    card.innerHTML = '<span class="lz-suggestion-icon">' + I[item.icon]({ size: 16 }) + '</span>' +
      '<span style="font-weight:500;">' + esc(item.label) + '</span>';
    card.addEventListener("click", function() {
      if (item.workspace) {
        self.toggleWorkspaceMode();
      } else {
        self.handleUserPrompt({ text: item.prompt });
      }
    });
    pool.appendChild(card);
  });

  var links = document.createElement("div");
  links.className = "lz-suggestion-links";
  var shufBtn = document.createElement("button");
  shufBtn.type = "button";
  shufBtn.innerHTML = I.shuffle({ size: 13 }) + "<span>Shuffle suggestions</span>";
  shufBtn.addEventListener("click", function() {
    self.suggestionOffset = (self.suggestionOffset + 3) % SUGGESTION_POOL.length;
    self.renderEmptyState();
  });
  links.appendChild(shufBtn);
  pool.appendChild(links);

  empty.appendChild(pool);
  this.threadWrap.appendChild(empty);
};

IceCreamHarness.prototype.toggleWorkspaceMode = function() {
  this.workspaceMode = !this.workspaceMode;
  this.threadWrap.innerHTML = "";
  if (this.workspaceMode) {
    new window.LazyRecordsTable(this.threadWrap);
  } else {
    this.renderEmptyState();
  }
};

IceCreamHarness.prototype.scrollToBottom = function() {
  var el = this.threadScroll;
  el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
};

IceCreamHarness.prototype.appendUserBubble = function(text, atts) {
  var row = document.createElement("div");
  row.className = "lz-user-bubble-row";
  var bubble = document.createElement("div");
  bubble.className = "lz-user-bubble";
  bubble.textContent = text;
  if (atts && atts.length) {
    var meta = document.createElement("div");
    meta.className = "lz-user-meta";
    meta.textContent = "📎 " + atts.map(function(a){ return a.name || a; }).join(", ");
    bubble.appendChild(meta);
  }
  row.appendChild(bubble);
  this.threadWrap.appendChild(row);
  this.scrollToBottom();
};

function formatToolLabel(raw) {
  var map = {
    "ask_clarification": "Clarify preferences",
    "generate_doc": "Draft document",
    "edit_doc": "Revise document",
    "append_section": "Add section",
    "breakdown": "Task checklist",
    "parallel_subagents": "Parallel subagents",
    "subagent": "Subagent task",
    "synthesis": "Document synthesis",
    "pdf_to_docx": "Convert PDF to Word",
    "pdf_merge": "Merge PDFs",
    "pdf_split": "Split PDF",
    "pdf_extract_pages": "Extract pages",
    "pdf_rotate": "Rotate PDF",
    "pdf_compress": "Compress PDF",
    "pdf_extract_images": "Extract images",
    "images_to_pdf": "Convert images to PDF",
    "word_count": "Count words",
    "pdf_info": "Inspect PDF metadata"
  };
  if (map[raw]) return map[raw];
  var s = String(raw || "Action").replace(/_/g, " ").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function buildChipRows(msg) {
  var rows = [];

  // 1. Thinking row (first row in ToolChips if think exists)
  if (msg.think) {
    var rawLines = String(msg.think).split(/\n+/).map(function(s){ return s.trim(); }).filter(Boolean);
    var firstLine = rawLines[0] || "Planning the document…";
    var chipText = firstLine;
    if (chipText.length > 42) chipText = chipText.slice(0, 40) + "…";
    var detailLines = rawLines.slice(1);
    if (!detailLines.length) detailLines = [firstLine];

    rows.push({
      icon: "think",
      label: "Thinking",
      chip: chipText,
      mono: false,
      detailMono: false,
      detail: detailLines.map(function(l) { return { text: l }; })
    });
  }

  // 2. Tool rows
  (msg.tools || []).forEach(function(t) {
    var name = t.name || t.tool || "tool";
    var actionLabel = t.action || formatToolLabel(name);
    var chipVal = t.arg || t.param || t.summary || "";
    var icon = "run";
    var detail = [];

    if (name === "generate_doc" || name === "write" || actionLabel.toLowerCase().indexOf("draft") !== -1 || actionLabel.toLowerCase().indexOf("write") !== -1) {
      icon = "write";
      actionLabel = "Draft document";
      if (t.summary) detail.push({ text: t.summary, tone: "add" });
    } else if (name === "edit_doc" || actionLabel.toLowerCase().indexOf("revis") !== -1) {
      icon = "write";
      actionLabel = "Revise document";
      if (t.summary) detail.push({ text: t.summary });
    } else if (name === "run_tool" || name === "run_command" || name === "rebuild") {
      icon = "run";
      if (!t.action) actionLabel = "Run " + (t.id || "tool");
      if (t.summary) detail.push({ text: "✓ " + t.summary });
    } else if (name.indexOf("pdf") !== -1 || name === "read_file" || name === "read_image") {
      icon = "read";
      if (!t.action) actionLabel = "Read document";
      if (t.summary) detail.push({ text: t.summary });
    } else if (name === "ask_clarification") {
      icon = "run";
      actionLabel = "Clarify preferences";
      if (t.summary) detail.push({ text: t.summary });
    } else if (name === "parallel_subagents" || name === "subagent") {
      icon = "run";
      if (t.items) {
        t.items.forEach(function(it) {
          detail.push({ text: "✓ " + (it.name || "Subagent") + ": " + (it.summary || "Done") });
        });
      } else if (t.summary) {
        detail.push({ text: "✓ " + t.summary });
      }
    } else {
      if (t.summary) detail.push({ text: t.summary });
    }

    rows.push({
      icon: icon,
      label: actionLabel,
      chip: chipVal,
      mono: icon === "write" || icon === "read",
      detail: detail
    });
  });

  return rows;
}

function buildDiffsForMsg(msg) {
  var diffs = msg.diffs ? msg.diffs.slice() : [];
  if (!diffs.length && (msg.docUpdated || (msg.tools && msg.tools.some(function(t){ return t.name === "generate_doc" || t.name === "edit_doc"; })))) {
    var title = (msg.docTitle || "document").replace(/[^a-zA-Z0-9_\-\.]/g, "_") + ".html";
    diffs.push({
      file: title,
      add: 120,
      lines: [
        "+ <h1>" + (msg.docTitle || "Academic Assignment") + "</h1>",
        "+ <h2>1. Theoretical Principles & Derivations</h2>",
        "+ <p>Core definitions, laws, equations, and SI units...</p>",
        "+ <h2>2. Step-by-Step Solved Numericals</h2>",
        "+ <p>Given data, formulas, substitutions, and verified results...</p>"
      ]
    });
  }
  return diffs;
}

IceCreamHarness.prototype.appendAssistantResponse = function(msg) {
  var self = this;
  var msgWrap = document.createElement("div");
  msgWrap.className = "lz-assistant-msg";

  // 1. ToolChips / Thinking / Actions at TOP
  var toolList = (msg.tools || []).filter(Boolean);
  var rows = buildChipRows(msg);

  if (toolList.length > 0 && window.AIWidgets && window.AIWidgets.ToolChips) {
    var diffs = buildDiffsForMsg(msg);
    var tc = window.AIWidgets.ToolChips.create({
      reveal: "instant",
      open: true,
      calls: toolList.length,
      messages: 1,
      rows: rows,
      diffs: diffs
    });
    msgWrap.appendChild(tc.el);
  } else if (msg.think) {
    var thinkEl = P.createThinkingState({
      variant: "Reasoning",
      doneTitle: "Thought for a few moments",
      think: msg.think,
      isDone: true,
      expanded: false
    });
    msgWrap.appendChild(thinkEl.el);
  }

  // 2. Text content BELOW tools
  if (msg.content) {
    var mdDiv = document.createElement("div");
    mdDiv.className = "lz-markdown-body";
    mdDiv.innerHTML = parseMarkdown(msg.content || "");
    this.bindCodeCopy(mdDiv);
    msgWrap.appendChild(mdDiv);
  }

  // 3. Document preview pill
  var hasDoc = msg.docUpdated || (msg.tools && msg.tools.some(function(t){
    return t.name === "generate_doc" || t.name === "edit_doc" || t.name === "append_section";
  }));

  if (hasDoc) {
    var docPill = document.createElement("button");
    docPill.type = "button";
    docPill.className = "lz-doc-preview-pill";
    docPill.innerHTML = I.doc({ size: 13 }) + "<span>Open Document Preview</span>";
    docPill.addEventListener("click", function() {
      self.openArtifactPane();
    });
    msgWrap.appendChild(docPill);
  }

  if (msg.model) {
    var modelBadge = document.createElement("div");
    modelBadge.className = "lz-model-badge";
    modelBadge.textContent = "via " + msg.model;
    modelBadge.title = msg.model;
    msgWrap.appendChild(modelBadge);
  }

  this.threadWrap.appendChild(msgWrap);
  this.scrollToBottom();
};

IceCreamHarness.prototype.bindCodeCopy = function(el) {
  el.querySelectorAll(".code-copy").forEach(function(btn) {
    btn.addEventListener("click", function() {
      var pre = btn.closest(".code-block").querySelector("pre");
      navigator.clipboard.writeText(pre.textContent.trim()).then(function() {
        btn.querySelector("span").textContent = "Copied!";
        setTimeout(function() { btn.querySelector("span").textContent = "Copy"; }, 1400);
      });
    });
  });
};

IceCreamHarness.prototype.uploadFile = function(file, cb) {
  var fd = new FormData();
  fd.append("file", file);
  api("/ajax/lazy/upload/", { method: "POST", body: fd }).then(function(d) {
    if (cb) cb({ name: file.name, token: d.token, type: file.type });
    toast("File attached: " + file.name);
  }).catch(function(err) {
    toast((err && err.error) || "Upload failed", true);
  });
};

IceCreamHarness.prototype.handleUserPrompt = function(payload) {
  var self = this;
  if (this.streaming) return;

  // Clear empty state
  if (this.threadWrap.querySelector(".lz-empty-state")) {
    this.threadWrap.innerHTML = "";
  }

  this.appendUserBubble(payload.text, payload.attachments);

  var msgWrap = document.createElement("div");
  msgWrap.className = "lz-assistant-msg";

  // Container 1: ToolChips and thinking AT TOP
  var toolsHolder = document.createElement("div");
  toolsHolder.className = "lz-tools-holder";
  msgWrap.appendChild(toolsHolder);

  // Container 2: Markdown body BELOW tools
  var mdHolder = document.createElement("div");
  mdHolder.className = "lz-markdown-body";
  msgWrap.appendChild(mdHolder);

  var loader = null;
  if (window.AIWidgets && window.AIWidgets.PixelLoader) {
    loader = window.AIWidgets.PixelLoader({ label: "Thinking…", variant: "dots" });
    toolsHolder.appendChild(loader.el);
  }

  this.threadWrap.appendChild(msgWrap);
  this.scrollToBottom();

  this.streaming = true;
  this.promptBar.setStreaming(true);
  this.abortController = new AbortController();

  var liveBuf = "";
  var liveThink = "";
  var liveTools = [];
  var liveDiffs = [];
  var liveModel = "";

  var sidPromise = this.activeSessionId ? Promise.resolve(this.activeSessionId) : api("/ajax/lazy/sessions/create/", { method: "POST", body: "{}" }).then(function(d) {
    self.activeSessionId = d.session.id;
    self.sessions.set(d.session.id, d.session);
    self.tabs.push(d.session);
    self.renderTabs();
    return d.session.id;
  });

  sidPromise.then(function(sid) {
    return fetch("/ajax/lazy/sessions/" + sid + "/chat/", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrf() },
      body: JSON.stringify(payload),
      signal: self.abortController.signal
    }).then(function(resp) {
      if (!resp.ok) return resp.json().catch(function(){ return {}; }).then(function(j){ throw j; });
      var reader = resp.body.getReader(), dec = new TextDecoder(), buf = "";
      function pump() {
        return reader.read().then(function(r) {
          if (r.done) return finalize();
          buf += dec.decode(r.value, { stream: true });
          var parts = buf.split("\n\n");
          buf = parts.pop();
          for (var i = 0; i < parts.length; i++) {
            handleFrame(parts[i]);
          }
          return pump();
        });
      }
      return pump();
    });
  }).catch(function(err) {
    if (err && err.name === "AbortError") {
      liveBuf += "\n\n*(generation stopped)*";
    } else {
      toast((err && (err.error || err.message)) || "Generation failed", true);
    }
    finalize();
  });

  function handleFrame(line) {
    line = line.trim();
    if (!line || line.indexOf("data:") !== 0) return;
    var data = line.slice(5).trim();
    if (data === "[DONE]") return;
    var f; try { f = JSON.parse(data); } catch(e) { return; }

    if (f.type === "model") {
      liveModel = f.model || f.content || "";
    } else if (f.type === "think") {
      liveThink += (f.content || "");
      if (loader) {
        var cleanSnippet = (f.content || "").replace(/[\n\r]+/g, " ").trim();
        if (cleanSnippet) {
          loader.setLabel(cleanSnippet.slice(0, 32) + "…");
        }
      }
    } else if (f.type === "status") {
      liveTools.push({ name: f.tool || "tool", summary: f.label || f.tool || "Working…" });
      if (loader) {
        loader.setLabel((f.label || "Working…").slice(0, 32));
      }
    } else if (f.type === "delta") {
      if (loader) { loader.destroy(); loader = null; }
      liveBuf += f.content;
      mdHolder.innerHTML = parseMarkdown(liveBuf) + '<span class="stream-caret"></span>';
      self.bindCodeCopy(mdHolder);
      self.scrollToBottom();
    } else if (f.type === "approval") {
      if (loader) { loader.destroy(); loader = null; }
      var approvalCard = P.createApprovalCard({
        questions: f.questions,
        onSubmitted: function(answers) {
          var chosen = [];
          Object.keys(answers).forEach(function(k) {
            var v = answers[k];
            if (v) chosen.push(v);
          });
          var promptText = "Draft the document with these confirmed preferences: " + chosen.join("; ") + ". Original topic: " + (f.originalPrompt || payload.text);
          self.handleUserPrompt({ text: promptText });
        }
      });
      msgWrap.appendChild(approvalCard);
      self.scrollToBottom();
    } else if (f.type === "error") {
      if (loader) { loader.destroy(); loader = null; }
      liveBuf = (liveBuf ? liveBuf + "\n\n" : "") + "*(Generation notice: " + (f.message || "Unable to complete request") + ")*";
      mdHolder.innerHTML = parseMarkdown(liveBuf);
    } else if (f.type === "doc") {
      self.openArtifactPane(f.html, f.title || "Document");
    } else if (f.type === "done") {
      if (loader) { loader.destroy(); loader = null; }
      if (f.model) liveModel = f.model;

      var toolList = (f.tools || liveTools || []).filter(Boolean);
      var turnMsg = {
        content: liveBuf,
        think: liveThink,
        tools: toolList,
        docUpdated: f.docUpdated,
        docTitle: f.docTitle,
        diffs: liveDiffs,
        model: f.model || liveModel || ""
      };

      var rows = buildChipRows(turnMsg);
      toolsHolder.innerHTML = "";
      if (toolList.length > 0 && window.AIWidgets && window.AIWidgets.ToolChips) {
        var diffs = buildDiffsForMsg(turnMsg);
        var tc = window.AIWidgets.ToolChips.create({
          reveal: "instant",
          open: true,
          calls: toolList.length,
          messages: 1,
          rows: rows,
          diffs: diffs
        });
        toolsHolder.appendChild(tc.el);
      } else if (turnMsg.think) {
        var thinkEl = P.createThinkingState({
          variant: "Reasoning",
          doneTitle: "Thought for a few moments",
          think: turnMsg.think,
          isDone: true,
          expanded: false
        });
        toolsHolder.appendChild(thinkEl.el);
      }

      // Final render for markdown text without caret
      if (liveBuf) {
        mdHolder.innerHTML = parseMarkdown(liveBuf);
        mdHolder.style.display = "block";
        self.bindCodeCopy(mdHolder);
      }

      if (f.docUpdated) {
        if (!msgWrap.querySelector(".lz-doc-preview-pill")) {
          var docPill = document.createElement("button");
          docPill.type = "button";
          docPill.className = "lz-doc-preview-pill";
          docPill.innerHTML = I.doc({ size: 13 }) + "<span>Open Document Preview</span>";
          docPill.addEventListener("click", function() {
            self.openArtifactPane();
          });
          msgWrap.appendChild(docPill);
        }
      }
      if (f.credits) {
        self.credits = f.credits;
        self.buildSidebar();
      }
      var displayModel = (turnMsg.model || f.model || liveModel || "").trim();
      if (displayModel) {
        var modelBadge = document.createElement("div");
        modelBadge.className = "lz-model-badge";
        modelBadge.textContent = "via " + displayModel;
        modelBadge.title = displayModel;
        msgWrap.appendChild(modelBadge);
      }
    }
  }

  function finalize() {
    self.streaming = false;
    self.promptBar.setStreaming(false);
    if (loader) {
      loader.destroy();
      loader = null;
    }
    var c = mdHolder.querySelector(".stream-caret");
    if (c) c.remove();
    if (liveBuf) {
      mdHolder.innerHTML = parseMarkdown(liveBuf);
      mdHolder.style.display = "";
      self.bindCodeCopy(mdHolder);
    } else if (liveTools.length || msgWrap.querySelector(".ai-chips") || msgWrap.querySelector(".lz-doc-preview-pill")) {
      mdHolder.style.display = "none";
    } else {
      mdHolder.innerHTML = parseMarkdown("*(No response generated)*");
      mdHolder.style.display = "";
    }
    self.scrollToBottom();
  }
};

IceCreamHarness.prototype.stopStreaming = function() {
  if (this.abortController) {
    this.abortController.abort();
    this.abortController = null;
  }
};

window.LazyHarness = IceCreamHarness;
})(window);
