(function(window){
"use strict";

var I = window.LazyIcons;

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function(c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

var SOURCES = [
  { key: "attach", name: "Add files & docs", desc: "Upload .docx, .pdf, or images", icon: "clip" },
  { key: "neb", name: "NEB Syllabus & Notes", desc: "Access curriculum resources", icon: "doc" },
  { key: "web", name: "Web Search", desc: "Live research and citations", icon: "globe" }
];

var COMMANDS = [
  { key: "write", name: "/write", desc: "Draft a new document or essay" },
  { key: "rewrite", name: "/rewrite", desc: "Polish, rephrase or condense" },
  { key: "summarize", name: "/summarize", desc: "Create a structured study digest" },
  { key: "outline", name: "/outline", desc: "Generate chapter or report outline" },
  { key: "table", name: "/table", desc: "Organize data into an AI table" }
];

var MODELS = [
  { key: "neby-pro", name: "Neby Pro (Smart)", tag: "Recommended" },
  { key: "neby-fast", name: "Neby Fast (Speed)", tag: "Instant" }
];

function PromptBar(container, opts) {
  opts = opts || {};
  this.container = container;
  this.onSend = opts.onSend;
  this.onStop = opts.onStop;
  this.onUpload = opts.onUpload;
  this.placeholder = opts.placeholder || "Ask Lazy to write, research or structure anything…";

  this.attachments = [];
  this.model = MODELS[0];
  this.streaming = false;

  this.init();
}

PromptBar.prototype.init = function() {
  var self = this;
  this.container.innerHTML = "";

  var shell = document.createElement("div");
  shell.className = "lz-promptbar-shell";

  var wrap = document.createElement("div");
  wrap.className = "lz-promptbar-wrap";

  var bar = document.createElement("div");
  bar.className = "lz-promptbar";

  // Attachments container
  this.attRow = document.createElement("div");
  this.attRow.className = "lz-promptbar-attachments";
  this.attRow.style.display = "none";
  bar.appendChild(this.attRow);

  // Input
  this.input = document.createElement("textarea");
  this.input.className = "lz-promptbar-input";
  this.input.placeholder = this.placeholder;
  this.input.rows = 1;
  bar.appendChild(this.input);

  // Controls Row
  var ctrl = document.createElement("div");
  ctrl.className = "lz-promptbar-controls";

  var left = document.createElement("div");
  left.className = "lz-promptbar-left";

  this.attachBtn = document.createElement("button");
  this.attachBtn.type = "button";
  this.attachBtn.className = "lz-btn-icon";
  this.attachBtn.title = "Attach file";
  this.attachBtn.innerHTML = I.plus({ size: 16 });
  left.appendChild(this.attachBtn);

  this.modelBtn = document.createElement("button");
  this.modelBtn.type = "button";
  this.modelBtn.className = "lz-model-picker-btn";
  this.modelBtn.innerHTML = I.sparkle({ size: 13, className: "text-accent" }) +
    '<span class="lz-model-name">' + esc(this.model.name) + '</span>' +
    I.chevronDown({ size: 12 });
  left.appendChild(this.modelBtn);

  ctrl.appendChild(left);

  var right = document.createElement("div");
  right.className = "lz-promptbar-right";

  this.sendBtn = document.createElement("button");
  this.sendBtn.type = "button";
  this.sendBtn.className = "lz-btn-send";
  this.sendBtn.title = "Send message";
  this.sendBtn.disabled = true;
  this.sendBtn.innerHTML = I.send({ size: 15 });
  right.appendChild(this.sendBtn);

  this.stopBtn = document.createElement("button");
  this.stopBtn.type = "button";
  this.stopBtn.className = "lz-btn-stop";
  this.stopBtn.title = "Stop generating";
  this.stopBtn.style.display = "none";
  this.stopBtn.innerHTML = I.stop({ size: 14 });
  right.appendChild(this.stopBtn);

  ctrl.appendChild(right);
  bar.appendChild(ctrl);

  // Popup Menu (@ and / autocomplete)
  this.popup = document.createElement("div");
  this.popup.className = "lz-popup-menu";
  this.popup.style.display = "none";
  wrap.appendChild(this.popup);

  // Model Menu Popover
  this.modelMenu = document.createElement("div");
  this.modelMenu.className = "lz-popup-menu";
  this.modelMenu.style.display = "none";
  this.modelMenu.style.width = "220px";
  MODELS.forEach(function(m) {
    var mItem = document.createElement("button");
    mItem.type = "button";
    mItem.className = "lz-menu-item";
    mItem.innerHTML = '<span>' + esc(m.name) + '</span><span class="lz-menu-item-sub">' + esc(m.tag) + '</span>';
    mItem.addEventListener("click", function() {
      self.model = m;
      self.modelBtn.querySelector(".lz-model-name").textContent = m.name;
      self.modelMenu.style.display = "none";
    });
    self.modelMenu.appendChild(mItem);
  });
  wrap.appendChild(this.modelMenu);

  // Hidden File Input
  this.fileInput = document.createElement("input");
  this.fileInput.type = "file";
  this.fileInput.accept = ".docx,.pdf,.txt,.png,.jpg,.jpeg,.webp";
  this.fileInput.style.display = "none";
  wrap.appendChild(this.fileInput);

  wrap.appendChild(bar);
  shell.appendChild(wrap);
  this.container.appendChild(shell);

  this.bindEvents();
};

PromptBar.prototype.bindEvents = function() {
  var self = this;

  this.input.addEventListener("input", function() {
    self.autosize();
    self.updateSendState();
    self.checkAutocomplete();
  });

  this.input.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!self.sendBtn.disabled && !self.streaming) {
        self.submit();
      }
    }
  });

  this.sendBtn.addEventListener("click", function() {
    self.submit();
  });

  this.stopBtn.addEventListener("click", function() {
    if (self.onStop) self.onStop();
  });

  this.attachBtn.addEventListener("click", function() {
    self.fileInput.click();
  });

  this.fileInput.addEventListener("change", function(e) {
    var file = e.target.files && e.target.files[0];
    if (!file) return;
    if (self.onUpload) {
      self.onUpload(file, function(att) {
        self.addAttachment(att);
      });
    }
    self.fileInput.value = "";
  });

  this.modelBtn.addEventListener("click", function(e) {
    e.stopPropagation();
    var isShown = self.modelMenu.style.display === "block";
    self.modelMenu.style.display = isShown ? "none" : "block";
    self.popup.style.display = "none";
  });

  document.addEventListener("click", function(e) {
    if (!self.container.contains(e.target)) {
      self.popup.style.display = "none";
      self.modelMenu.style.display = "none";
    }
  });
};

PromptBar.prototype.autosize = function() {
  this.input.style.height = "auto";
  this.input.style.height = Math.min(this.input.scrollHeight, 180) + "px";
};

PromptBar.prototype.updateSendState = function() {
  var hasText = Boolean(this.input.value.trim());
  var hasAtts = this.attachments.length > 0;
  this.sendBtn.disabled = !(hasText || hasAtts);
};

PromptBar.prototype.checkAutocomplete = function() {
  var val = this.input.value;
  var match = /(^|\s)([@/])([\w-]*)$/.exec(val);
  if (!match) {
    this.popup.style.display = "none";
    return;
  }
  var type = match[2];
  var query = (match[3] || "").toLowerCase();
  var items = (type === "@")
    ? SOURCES.filter(function(s){ return s.name.toLowerCase().indexOf(query) !== -1; })
    : COMMANDS.filter(function(c){ return c.name.toLowerCase().indexOf(query) !== -1; });

  if (!items.length) {
    this.popup.style.display = "none";
    return;
  }

  var self = this;
  this.popup.innerHTML = "";
  items.forEach(function(it) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "lz-menu-item";
    btn.innerHTML = '<span>' + esc(it.name) + '</span><span class="lz-menu-item-sub">' + esc(it.desc) + '</span>';
    btn.addEventListener("click", function() {
      if (it.key === "attach") {
        self.fileInput.click();
      } else {
        self.input.value = val.replace(/([@/])[\w-]*$/, it.name + " ");
        self.input.focus();
        self.autosize();
      }
      self.popup.style.display = "none";
    });
    self.popup.appendChild(btn);
  });

  this.popup.style.display = "block";
};

PromptBar.prototype.addAttachment = function(att) {
  var self = this;
  this.attachments.push(att);
  this.renderAttachments();
  this.updateSendState();
};

PromptBar.prototype.removeAttachment = function(idx) {
  this.attachments.splice(idx, 1);
  this.renderAttachments();
  this.updateSendState();
};

PromptBar.prototype.renderAttachments = function() {
  var self = this;
  if (!this.attachments.length) {
    this.attRow.style.display = "none";
    this.attRow.innerHTML = "";
    return;
  }
  this.attRow.style.display = "flex";
  this.attRow.innerHTML = "";
  this.attachments.forEach(function(att, idx) {
    var chip = document.createElement("div");
    chip.className = "lz-att-chip";
    chip.innerHTML = I.doc({ size: 12 }) +
      '<span>' + esc(att.name) + '</span>' +
      '<button type="button" class="lz-att-remove" aria-label="Remove attachment">' + I.close({ size: 11 }) + '</button>';
    chip.querySelector(".lz-att-remove").addEventListener("click", function() {
      self.removeAttachment(idx);
    });
    self.attRow.appendChild(chip);
  });
};

PromptBar.prototype.submit = function() {
  var text = this.input.value.trim();
  if (!text && !this.attachments.length) return;
  var payload = {
    text: text || "(see attached files)",
    attachments: this.attachments.slice(),
    model: this.model.key
  };
  this.input.value = "";
  this.attachments = [];
  this.renderAttachments();
  this.autosize();
  this.updateSendState();
  if (this.onSend) this.onSend(payload);
};

PromptBar.prototype.setStreaming = function(streaming) {
  this.streaming = streaming;
  this.sendBtn.style.display = streaming ? "none" : "inline-flex";
  this.stopBtn.style.display = streaming ? "inline-flex" : "none";
};

window.LazyPromptBar = PromptBar;
})(window);
