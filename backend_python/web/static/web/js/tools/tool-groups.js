(function () {
  "use strict";

  var ICONS = {
    pointer: '<path d="M7.2 3.2 L7.2 20.2 L11.1 16.1 L14.8 23.2 L17.4 21.9 L13.6 14.7 L19.6 14.4 Z"/>',
    hand: '<path d="M9.2 12.2 V6.6 c0-1 .8-1.7 1.7-1.7s1.7.7 1.7 1.7V11 M12.6 11.2 V5.4 c0-1 .8-1.8 1.8-1.8s1.8.8 1.8 1.8V11.4 M16.2 11.6 V7.4 c0-.9.7-1.6 1.6-1.6s1.6.7 1.6 1.6v7.2 c0 3.4-2.2 6.4-6.2 6.4 h-.6 c-3.2 0-5.8-2-6.8-4.8 L6.4 13.2 c-.4-.8.1-1.8 1-1.8.4 0 .8.2 1 .6 l1 2.2"/>',
    pen: '<path d="M15.4 4.8 l3.8 3.8-10.4 10.4 H5 v-3.8 Z"/><path d="M13.8 6.4 l3.8 3.8"/>',
    highlighter: '<path d="M7.2 16.8 h9.6 l2.2-4.4-4.8-4.8-7 4.8 Z"/><path d="M8.4 17.2 v2.4"/>',
    rect: '<rect x="5.2" y="6.4" width="13.6" height="11.2" rx="1.4"/>',
    ellipse: '<ellipse cx="12" cy="12" rx="7.2" ry="5.4"/>',
    line: '<path d="M5 18 L19 6"/>',
    arrow: '<path d="M5 18 L18 6"/><path d="M12.2 6.2 H18 V12"/>',
    eraser: '<path d="M8 16.4 L15.6 8.8 a2 2 0 0 1 2.8 0 l1 1 a2 2 0 0 1 0 2.8 L11.8 20.2 H8 Z"/><path d="M8 16.4 L11.8 20.2"/>',
    lasso: '<path d="M7.4 14.6 c-1.8-2.2-.4-6.8 3.4-7.6 3.8-.8 6.8 2 6.4 5.2-.4 2.8-3 4-5.2 3.2"/><circle cx="9.4" cy="17.8" r="1.4"/>',
    text: '<path d="M6.2 7.2 H17.8 M12 7.2 V18.4 M8.4 18.4 H15.6"/>',
    sticky: '<path d="M7 5.6 h8.4 l3.6 3.6 V18.4 H7 Z"/><path d="M15.2 5.6 V9.4 H19"/>',
    image: '<rect x="4.8" y="6.2" width="14.4" height="11.6" rx="1.6"/><circle cx="9" cy="10.4" r="1.3"/><path d="M5.6 16.2 L10.2 12.4 L13.2 15 L15.6 13.2 L19 16.2"/>',
    file: '<path d="M8 4.8 h5.4 L18 9.4 V19.2 H8 Z"/><path d="M13.4 4.8 V9.4 H18"/>',
    table: '<rect x="5" y="6" width="14" height="12" rx="1.4"/><path d="M5 10.2 H19 M5 14.2 H19 M10 6 V18"/>',
    grid: '<rect x="5" y="5.5" width="14" height="13" rx="1.4"/><path d="M5 9.5 H19 M5 14 H19 M12 5.5 V18.5"/>',
    flow: '<rect x="7" y="4.2" width="10" height="6" rx="1.4"/><rect x="7" y="13.8" width="10" height="6" rx="1.4"/><path d="M12 10.2 V13.8"/>',
    chart: '<path d="M5 17 V7 M5 17 H19"/><path d="M8 13 l3-3 3 2 4-5"/>',
    tune: '<path d="M6 8 H18 M6 12 H18 M6 16 H18"/><circle cx="10" cy="8" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/><circle cx="9" cy="16" r="1.5" fill="currentColor"/>',
    spark: '<path d="M12 3.5 l1.6 5 5.2.2-4.1 3.2 1.5 5L12 14.2 8 16.9l1.5-5-4.1-3.2 5.2-.2 Z"/>',
    quiz: '<circle cx="12" cy="12" r="8"/><path d="M8.6 12.2 l2.3 2.3 4.6-4.8"/>',
    flash: '<rect x="6.2" y="5" width="11.6" height="14" rx="1.6"/><path d="M9 9 h6 M9 12.5 h4.5"/>',
    time: '<path d="M12 5 v14 M7 8 h10 M7 16 h10"/><circle cx="12" cy="8" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/><circle cx="12" cy="16" r="1.3" fill="currentColor"/>',
    poll: '<path d="M7 16 V11 M12 16 V7 M17 16 V9"/><path d="M5 18 H19"/>',
    blocks: '<rect x="5" y="5" width="6.2" height="6.2" rx="1.2"/><rect x="12.8" y="5" width="6.2" height="6.2" rx="1.2"/><rect x="5" y="12.8" width="6.2" height="6.2" rx="1.2"/><rect x="12.8" y="12.8" width="6.2" height="6.2" rx="1.2"/>'
  };

  function svgIcon(name, size) {
    size = size || 18;
    var body = ICONS[name] || ICONS.pointer;
    return '<svg viewBox="0 0 24 24" width="' + size + '" height="' + size + '" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + "</svg>";
  }

  function defaultGroups() {
    return [
      { id: "select", title: "Select", icon: "pointer" },
      { id: "pan", title: "Hand", icon: "hand" },
      {
        id: "pen",
        title: "Draw",
        icon: "pen",
        items: [
          { id: "pen", title: "Pen", icon: "pen" },
          { id: "highlighter", title: "Highlighter", icon: "highlighter" }
        ]
      },
      {
        id: "rect",
        title: "Shape",
        icon: "rect",
        items: [
          { id: "rect", title: "Rectangle", icon: "rect" },
          { id: "ellipse", title: "Ellipse", icon: "ellipse" },
          { id: "line", title: "Line", icon: "line" },
          { id: "arrow", title: "Arrow", icon: "arrow" }
        ]
      },
      {
        id: "eraser",
        title: "Erase",
        icon: "eraser",
        items: [
          { id: "eraser", title: "Eraser", icon: "eraser" },
          { id: "lasso", title: "Lasso", icon: "lasso" }
        ]
      },
      {
        id: "insert",
        title: "Insert",
        icon: "sticky",
        items: [
          { id: "text", title: "Text", icon: "text" },
          { id: "sticky", title: "Sticky", icon: "sticky" },
          { id: "image", title: "Image", icon: "image" },
          { id: "file", title: "File / PDF", icon: "file" }
        ]
      },
      {
        id: "blocks",
        title: "Blocks",
        icon: "blocks",
        items: [
          { id: "w-filter", title: "Filter table", icon: "table" },
          { id: "w-records", title: "Records", icon: "grid" },
          { id: "w-flow", title: "Flow", icon: "flow" },
          { id: "w-insights", title: "Insights", icon: "chart" },
          { id: "w-tune", title: "Fine-tune", icon: "tune" },
          { id: "w-selbar", title: "Selection AI", icon: "spark" }
        ]
      },
      {
        id: "learn",
        title: "Learn",
        icon: "quiz",
        items: [
          { id: "w-quiz", title: "Quiz", icon: "quiz" },
          { id: "w-flash", title: "Flashcards", icon: "flash" },
          { id: "w-timeline", title: "Timeline", icon: "time" },
          { id: "w-poll", title: "Poll", icon: "poll" }
        ]
      }
    ];
  }

  function groupOf(groups, id) {
    for (var i = 0; i < groups.length; i++) {
      var g = groups[i];
      if (g.id === id) return g;
      var items = g.items || [];
      for (var j = 0; j < items.length; j++) if (items[j].id === id) return g;
    }
    return null;
  }

  function itemIcon(group, id) {
    var items = group.items || [];
    for (var i = 0; i < items.length; i++) if (items[i].id === id) return items[i].icon;
    return group.icon;
  }

  function ToolGroups(opts) {
    this.host = opts.host;
    this.groups = opts.groups || defaultGroups();
    this.active = opts.active || "select";
    this.onChange = opts.onChange || function () {};
    this.bare = !!opts.bare;
    this._open = null;
    this._hideTimer = 0;
    this._last = {};
    this._onDoc = this._onDoc.bind(this);
    this._onKey = this._onKey.bind(this);
    this.mount();
  }

  ToolGroups.prototype.mount = function () {
    if (!this.host) return;
    this.host.classList.add("tg-host");
    if (this.bare) this.host.classList.add("tg-bare");
    this.host.innerHTML =
      '<div class="tg-bar" role="toolbar" aria-label="Canvas tools"></div>' +
      '<div class="tg-dock" hidden></div>';
    this._bar = this.host.querySelector(".tg-bar");
    this._dock = this.host.querySelector(".tg-dock");
    this._fly = document.createElement("div");
    this._fly.className = "tg-fly";
    this._fly.hidden = true;
    document.body.appendChild(this._fly);
    this._renderBar();
    this._bar.addEventListener("click", this._onBarClick.bind(this));
    this._bar.addEventListener("pointerover", this._onBarEnter.bind(this));
    this._bar.addEventListener("pointerout", this._onBarLeave.bind(this));
    this._fly.addEventListener("pointerenter", this._cancelHide.bind(this));
    this._fly.addEventListener("pointerleave", this._scheduleHide.bind(this));
    this._fly.addEventListener("click", this._onFlyClick.bind(this));
    document.addEventListener("pointerdown", this._onDoc);
    document.addEventListener("keydown", this._onKey);
  };

  ToolGroups.prototype._renderBar = function () {
    var html = "";
    for (var i = 0; i < this.groups.length; i++) {
      var g = this.groups[i];
      if (i === 2) html += '<span class="tg-sep" aria-hidden="true"></span>';
      var has = g.items && g.items.length > 1;
      var on = groupOf(this.groups, this.active) === g;
      var icon = on && has ? itemIcon(g, this.active) : g.icon;
      html +=
        '<button type="button" class="tg-btn' +
        (on ? " is-on" : "") +
        (has ? " has-items" : "") +
        '" data-tg="' +
        g.id +
        '" title="' +
        g.title +
        '" aria-haspopup="' +
        (has ? "true" : "false") +
        '" aria-expanded="' +
        (this._open === g.id ? "true" : "false") +
        '">' +
        svgIcon(icon, 18) +
        (has ? '<i class="tg-caret" aria-hidden="true"></i>' : "") +
        "</button>";
    }
    this._bar.innerHTML = html;
  };

  ToolGroups.prototype._onBarClick = function (e) {
    var btn = e.target.closest("[data-tg]");
    if (!btn) return;
    var id = btn.getAttribute("data-tg");
    var g = groupOf(this.groups, id);
    if (!g) return;
    if (g.items && g.items.length > 1) {
      if (this._open === g.id) {
        if (window.matchMedia("(hover: none)").matches) this.closeFly();
        return;
      }
      this._showFly(g, btn);
      return;
    }
    this.closeFly();
    this.select(g.id);
  };

  ToolGroups.prototype._onBarEnter = function (e) {
    if (window.matchMedia("(hover: none)").matches) return;
    var btn = e.target.closest("[data-tg]");
    if (!btn || !this._bar.contains(btn)) return;
    var from = e.relatedTarget;
    if (from && btn.contains(from)) return;
    var g = groupOf(this.groups, btn.getAttribute("data-tg"));
    if (!g || !g.items || g.items.length < 2) {
      this._scheduleHide();
      return;
    }
    this._cancelHide();
    this._showFly(g, btn);
  };

  ToolGroups.prototype._onBarLeave = function (e) {
    if (this._bar.contains(e.relatedTarget) || this._fly.contains(e.relatedTarget)) return;
    this._scheduleHide();
  };

  ToolGroups.prototype._onFlyClick = function (e) {
    var btn = e.target.closest("[data-tg-id]");
    if (!btn) return;
    this.select(btn.getAttribute("data-tg-id"));
    this.closeFly();
  };

  ToolGroups.prototype._showFly = function (g, btn) {
    this._open = g.id;
    var html = "";
    var items = g.items || [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      html +=
        '<button type="button" class="tg-fly-item' +
        (it.id === this.active ? " is-on" : "") +
        '" data-tg-id="' +
        it.id +
        '">' +
        svgIcon(it.icon, 16) +
        "<span>" +
        it.title +
        "</span></button>";
    }
    this._fly.innerHTML = html;
    this._fly.hidden = false;
    this._placeFly(btn);
    var buttons = this._bar.querySelectorAll("[data-tg]");
    for (var b = 0; b < buttons.length; b++) {
      buttons[b].setAttribute("aria-expanded", buttons[b].getAttribute("data-tg") === g.id ? "true" : "false");
    }
  };

  ToolGroups.prototype._placeFly = function (btn) {
    var fly = this._fly;
    var r = btn.getBoundingClientRect();
    fly.style.left = "0px";
    fly.style.top = "0px";
    var fr = fly.getBoundingClientRect();
    var gap = 8;
    var below = window.innerHeight - r.bottom;
    var above = r.top;
    var placeBelow = below >= fr.height + gap || below >= above;
    var top = placeBelow ? r.bottom + gap : r.top - fr.height - gap;
    var left = r.right - fr.width;
    if (left < 8) left = r.left;
    left = Math.max(8, Math.min(left, window.innerWidth - fr.width - 8));
    top = Math.max(8, Math.min(top, window.innerHeight - fr.height - 8));
    fly.style.left = left + "px";
    fly.style.top = top + "px";
    fly.dataset.side = placeBelow ? "below" : "above";
  };

  ToolGroups.prototype._scheduleHide = function () {
    var self = this;
    this._cancelHide();
    this._hideTimer = setTimeout(function () {
      self.closeFly();
    }, 120);
  };

  ToolGroups.prototype._cancelHide = function () {
    if (this._hideTimer) {
      clearTimeout(this._hideTimer);
      this._hideTimer = 0;
    }
  };

  ToolGroups.prototype.closeFly = function () {
    this._cancelHide();
    this._open = null;
    this._fly.hidden = true;
    this._fly.innerHTML = "";
    var buttons = this._bar ? this._bar.querySelectorAll("[data-tg]") : [];
    for (var b = 0; b < buttons.length; b++) buttons[b].setAttribute("aria-expanded", "false");
  };

  ToolGroups.prototype.select = function (id, silent) {
    if (!id) return;
    var g = groupOf(this.groups, id);
    if (g) this._last[g.id] = id;
    this.active = id;
    this._renderBar();
    if (!silent) this.onChange(id);
  };

  ToolGroups.prototype.setActive = function (id) {
    this.select(id, true);
  };

  ToolGroups.prototype.setDock = function (html) {
    if (!this._dock) return;
    if (!html) {
      this._dock.hidden = true;
      this._dock.innerHTML = "";
      return;
    }
    this._dock.innerHTML = html;
    this._dock.hidden = false;
  };

  ToolGroups.prototype._onDoc = function (e) {
    if (!this._open) return;
    if (this.host.contains(e.target) || this._fly.contains(e.target)) return;
    this.closeFly();
  };

  ToolGroups.prototype._onKey = function (e) {
    var tag = (e.target && e.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || e.metaKey || e.ctrlKey || e.altKey) return;
    var map = { v: "select", h: "pan", p: "pen", r: "rect", e: "eraser", t: "text" };
    var id = map[e.key && e.key.toLowerCase()];
    if (id) {
      e.preventDefault();
      this.select(id);
      this.closeFly();
    }
    if (e.key === "Escape") this.closeFly();
  };

  ToolGroups.prototype.destroy = function () {
    document.removeEventListener("pointerdown", this._onDoc);
    document.removeEventListener("keydown", this._onKey);
    this.closeFly();
    if (this._fly && this._fly.parentNode) this._fly.parentNode.removeChild(this._fly);
    if (this.host) this.host.innerHTML = "";
  };

  ToolGroups.svgIcon = svgIcon;
  ToolGroups.defaultGroups = defaultGroups;
  ToolGroups.ICONS = ICONS;

  window.ToolGroups = ToolGroups;
  window.RadialWheel = ToolGroups;
})();
