(function(){
"use strict";

var ICONS = {
  pointer: '<path d="M7.2 3.2 L7.2 20.2 L11.1 16.1 L14.8 23.2 L17.4 21.9 L13.6 14.7 L19.6 14.4 Z"/>',
  pointerFill: '<path d="M7.2 3.2 L7.2 20.2 L11.1 16.1 L14.8 23.2 L17.4 21.9 L13.6 14.7 L19.6 14.4 Z" fill="currentColor" stroke="none"/>',
  hand: '<path d="M9.2 12.2 V6.6 c0-1 .8-1.7 1.7-1.7s1.7.7 1.7 1.7V11 M12.6 11.2 V5.4 c0-1 .8-1.8 1.8-1.8s1.8.8 1.8 1.8V11.4 M16.2 11.6 V7.4 c0-.9.7-1.6 1.6-1.6s1.6.7 1.6 1.6v7.2 c0 3.4-2.2 6.4-6.2 6.4 h-.6 c-3.2 0-5.8-2-6.8-4.8 L6.4 13.2 c-.4-.8.1-1.8 1-1.8.4 0 .8.2 1 .6 l1 2.2"/>',
  scissors: '<path d="M8.2 8.2 a2.4 2.4 0 1 1 0 .2 Z M8.2 18.4 a2.4 2.4 0 1 1 0 .2 Z"/><path d="M10.2 9.6 L19.4 17.8 M10.2 16.8 L19.4 8.6"/>',
  ruler: '<path d="M5.4 16.6 L15.2 6.8 l3.6 3.6 L9 20.2 Z"/><path d="M8.2 13.8 l1.2-1.2 M10.2 11.8 l1.2-1.2 M12.2 9.8 l1.2-1.2"/>',
  marker: '<path d="M14.8 5.2 l4 4-9.6 9.6 H5.2 v-4 Z"/><path d="M13.2 6.8 l4 4"/><path d="M5.2 18.8 h4"/>',
  pen: '<path d="M15.4 4.8 l3.8 3.8-10.4 10.4 H5 v-3.8 Z"/><path d="M13.8 6.4 l3.8 3.8"/>',
  highlighter: '<path d="M7.2 16.8 h9.6 l2.2-4.4-4.8-4.8-7 4.8 Z"/><path d="M8.4 17.2 v2.4"/>',
  rect: '<rect x="5.2" y="6.4" width="13.6" height="11.2" rx="1.4"/>',
  ellipse: '<ellipse cx="12" cy="12" rx="7.2" ry="5.4"/>',
  line: '<path d="M5 18 L19 6"/>',
  arrow: '<path d="M5 18 L18 6"/><path d="M12.2 6.2 H18 V12"/>',
  eraser: '<path d="M8 16.4 L15.6 8.8 a2 2 0 0 1 2.8 0 l1 1 a2 2 0 0 1 0 2.8 L11.8 20.2 H8 Z"/><path d="M8 16.4 L11.8 20.2"/>',
  text: '<path d="M6.2 7.2 H17.8 M12 7.2 V18.4 M8.4 18.4 H15.6"/>',
  sticky: '<path d="M7 5.6 h8.4 l3.6 3.6 V18.4 H7 Z"/><path d="M15.2 5.6 V9.4 H19"/>',
  image: '<rect x="4.8" y="6.2" width="14.4" height="11.6" rx="1.6"/><circle cx="9" cy="10.4" r="1.3"/><path d="M5.6 16.2 L10.2 12.4 L13.2 15 L15.6 13.2 L19 16.2"/>',
  file: '<path d="M8 4.8 h5.4 L18 9.4 V19.2 H8 Z"/><path d="M13.4 4.8 V9.4 H18"/>',
  lasso: '<path d="M7.4 14.6 c-1.8-2.2-.4-6.8 3.4-7.6 3.8-.8 6.8 2 6.4 5.2-.4 2.8-3 4-5.2 3.2"/><circle cx="9.4" cy="17.8" r="1.4"/>',
  pdf: '<path d="M8 4.8 h5.4 L18 9.4 V19.2 H8 Z"/><path d="M13.4 4.8 V9.4 H18"/><path d="M10 13.6 h4 M10 16 h2.8"/>'
};

function svgIcon(name, size){
  size = size || 22;
  var body = ICONS[name] || ICONS.pointer;
  return '<svg viewBox="0 0 24 24" width="'+size+'" height="'+size+'" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+body+'</svg>';
}

function defaultTools(){
  return [
    { id: "rect", key: "R", title: "Shape", icon: "ruler",
      variants: [
        { id: "rect", title: "Rectangle", icon: "rect" },
        { id: "ellipse", title: "Ellipse", icon: "ellipse" },
        { id: "line", title: "Line", icon: "line" },
        { id: "arrow", title: "Arrow", icon: "arrow" }
      ]
    },
    { id: "eraser", key: "S", title: "Cut", icon: "scissors",
      variants: [
        { id: "eraser", title: "Eraser", icon: "eraser" },
        { id: "lasso", title: "Lasso", icon: "lasso" }
      ]
    },
    { id: "select", key: "P", title: "Select", icon: "pointer",
      variants: [
        { id: "select", title: "Select", icon: "pointer" },
        { id: "text", title: "Text", icon: "text" },
        { id: "sticky", title: "Sticky", icon: "sticky" },
        { id: "image", title: "Image", icon: "image" },
        { id: "file", title: "File / PDF", icon: "file" }
      ]
    },
    { id: "pan", key: "H", title: "Hand", icon: "hand" },
    { id: "pen", key: "G", title: "Draw", icon: "marker",
      variants: [
        { id: "pen", title: "Pen", icon: "pen" },
        { id: "highlighter", title: "Highlighter", icon: "highlighter" },
        { id: "marker", title: "Marker", icon: "marker" }
      ]
    }
  ];
}

function findTool(tools, id){
  for (var i = 0; i < tools.length; i++){
    if (tools[i].id === id) return tools[i];
    var vars = tools[i].variants || [];
    for (var j = 0; j < vars.length; j++){
      if (vars[j].id === id){
        return { parent: tools[i], tool: vars[j], index: i };
      }
    }
  }
  return null;
}

function iconFor(tools, id){
  for (var i = 0; i < tools.length; i++){
    if (tools[i].id === id) return tools[i].icon;
    var vars = tools[i].variants || [];
    for (var j = 0; j < vars.length; j++){
      if (vars[j].id === id) return vars[j].icon;
    }
  }
  return "pointer";
}

function keyFor(tools, id){
  for (var i = 0; i < tools.length; i++){
    var vars = tools[i].variants || [];
    for (var j = 0; j < vars.length; j++){
      if (vars[j].id === id) return tools[i].key;
    }
    if (tools[i].id === id) return tools[i].key;
  }
  return "";
}

function RadialWheel(opts){
  opts = opts || {};
  this.host = typeof opts.host === "string" ? document.querySelector(opts.host) : (opts.host || null);
  this.tools = opts.tools && opts.tools.length ? opts.tools : defaultTools();
  this.active = opts.active || "select";
  this.onChange = typeof opts.onChange === "function" ? opts.onChange : function(){};
  this.onOpen = typeof opts.onOpen === "function" ? opts.onOpen : function(){};
  this.onClose = typeof opts.onClose === "function" ? opts.onClose : function(){};
  this.open = false;
  this.hoverIndex = -1;
  this._flyTimer = null;
  this._root = null;
  this._boundKey = this._onKey.bind(this);
  this._boundDoc = this._onDocPointer.bind(this);
  this.mount();
}

RadialWheel.prototype.mount = function(){
  if (!this.host){
    this.host = document.createElement("div");
    this.host.className = "rw-host";
    document.body.appendChild(this.host);
  }
  this.host.classList.add("rw-host");
  this.host.innerHTML =
    '<div class="rw-root" data-open="false">' +
      '<div class="rw-arc" aria-hidden="true"></div>' +
      '<div class="rw-keys" aria-hidden="true"></div>' +
      '<div class="rw-items"></div>' +
      '<div class="rw-flyout" hidden></div>' +
      '<button type="button" class="rw-fab" aria-label="Tools" aria-expanded="false"></button>' +
      '<div class="rw-key" hidden></div>' +
      '<div class="rw-dock" hidden></div>' +
    '</div>';
  this._root = this.host.querySelector(".rw-root");
  this._fab = this._root.querySelector(".rw-fab");
  this._items = this._root.querySelector(".rw-items");
  this._keys = this._root.querySelector(".rw-keys");
  this._fly = this._root.querySelector(".rw-flyout");
  this._key = this._root.querySelector(".rw-key");
  this._dock = this._root.querySelector(".rw-dock");
  this._renderItems();
  this._paintFab();
  var self = this;
  this._fab.addEventListener("pointerdown", function(e){
    e.preventDefault();
    e.stopPropagation();
    self.toggle();
  });
  this._items.addEventListener("pointerover", function(e){
    var btn = e.target.closest("[data-rw-index]");
    if (!btn || !self.open) return;
    self._hover(parseInt(btn.dataset.rwIndex, 10));
  });
  this._items.addEventListener("pointerdown", function(e){
    var btn = e.target.closest("[data-rw-index]");
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    var tool = self.tools[parseInt(btn.dataset.rwIndex, 10)];
    if (!tool) return;
    if (tool.variants && tool.variants.length && self.hoverIndex === parseInt(btn.dataset.rwIndex, 10) && !self._fly.hidden){
      return;
    }
    self.select(tool.id);
  });
  this._fly.addEventListener("pointerdown", function(e){
    var btn = e.target.closest("[data-rw-id]");
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    self.select(btn.dataset.rwId);
  });
  document.addEventListener("pointerdown", this._boundDoc, true);
  document.addEventListener("keydown", this._boundKey);
};

RadialWheel.prototype._itemAngle = function(i, n){
  return Math.PI - (n === 1 ? 0 : i * Math.PI / (n - 1));
};

RadialWheel.prototype._renderItems = function(){
  var n = this.tools.length;
  var html = "";
  var keys = "";
  for (var i = 0; i < n; i++){
    var t = this.tools[i];
    var angle = this._itemAngle(i, n);
    var r = 118;
    var x = Math.cos(angle) * r;
    var y = -Math.sin(angle) * r;
    html += '<button type="button" class="rw-item" data-rw-index="'+i+'" data-rw-id="'+t.id+'" title="'+t.title+' ('+t.key+')" style="--rw-x:'+x+'px;--rw-y:'+y+'px;--rw-i:'+i+'">' +
      svgIcon(t.icon, 22) +
    '</button>';
    var kx = Math.cos(angle) * 68;
    var ky = -Math.sin(angle) * 68;
    keys += '<span class="rw-item-key" style="--rw-x:'+kx+'px;--rw-y:'+ky+'px;--rw-i:'+i+'">'+t.key+'</span>';
  }
  this._items.innerHTML = html;
  if (this._keys) this._keys.innerHTML = keys;
};

RadialWheel.prototype._paintFab = function(){
  var icon = iconFor(this.tools, this.active);
  this._fab.innerHTML = svgIcon(icon === "pointer" ? "pointer" : icon, 24);
  this._fab.setAttribute("aria-label", "Tool: " + this.active);
  var k = keyFor(this.tools, this.active);
  if (k && !this.open){
    this._key.hidden = false;
    this._key.textContent = k;
  } else {
    this._key.hidden = true;
  }
  var items = this._items.querySelectorAll(".rw-item");
  for (var i = 0; i < items.length; i++){
    var t = this.tools[i];
    var on = t.id === this.active;
    if (!on && t.variants){
      for (var j = 0; j < t.variants.length; j++){
        if (t.variants[j].id === this.active) on = true;
      }
    }
    items[i].classList.toggle("is-active", on);
  }
};

RadialWheel.prototype._hover = function(index){
  if (this.hoverIndex === index) return;
  this.hoverIndex = index;
  var items = this._items.querySelectorAll(".rw-item");
  for (var i = 0; i < items.length; i++) items[i].classList.toggle("is-hover", i === index);
  clearTimeout(this._flyTimer);
  var self = this;
  var tool = this.tools[index];
  if (!tool || !tool.variants || tool.variants.length < 2){
    this._hideFly();
    return;
  }
  this._flyTimer = setTimeout(function(){ self._showFly(index); }, 80);
};

RadialWheel.prototype._showFly = function(index){
  var tool = this.tools[index];
  if (!tool || !tool.variants) { this._hideFly(); return; }
  var n = this.tools.length;
  var angle = this._itemAngle(index, n);
  var r = 176;
  var x = Math.cos(angle) * r;
  var y = -Math.sin(angle) * r;
  var rot = -(angle * 180 / Math.PI - 90);
  var html = "";
  for (var i = 0; i < tool.variants.length; i++){
    var v = tool.variants[i];
    html += '<button type="button" class="rw-fly-item'+(v.id===this.active?" is-active":"")+'" data-rw-id="'+v.id+'" title="'+v.title+'">'+svgIcon(v.icon, 20)+'</button>';
  }
  this._fly.innerHTML = html;
  this._fly.hidden = false;
  this._fly.style.setProperty("--rw-x", x + "px");
  this._fly.style.setProperty("--rw-y", y + "px");
  this._fly.style.setProperty("--rw-rot", rot + "deg");
  this._fly.classList.add("is-in");
};

RadialWheel.prototype._hideFly = function(){
  this._fly.hidden = true;
  this._fly.classList.remove("is-in");
  this._fly.innerHTML = "";
};

RadialWheel.prototype.toggle = function(){
  if (this.open) this.closeWheel();
  else this.openWheel();
};

RadialWheel.prototype.openWheel = function(){
  if (this.open) return;
  this.open = true;
  this.hoverIndex = -1;
  this._root.dataset.open = "true";
  this._fab.setAttribute("aria-expanded", "true");
  this._key.hidden = true;
  this._hideFly();
  this.onOpen();
};

RadialWheel.prototype.closeWheel = function(){
  if (!this.open) return;
  this.open = false;
  this.hoverIndex = -1;
  this._root.dataset.open = "false";
  this._fab.setAttribute("aria-expanded", "false");
  this._hideFly();
  this._paintFab();
  this.onClose();
};

RadialWheel.prototype.select = function(id, silent){
  if (!id) return;
  this.active = id;
  this._paintFab();
  this.closeWheel();
  if (!silent) this.onChange(id, iconFor(this.tools, id));
};

RadialWheel.prototype.setActive = function(id){
  this.active = id;
  this._paintFab();
};

RadialWheel.prototype.setDock = function(html){
  if (!html){ this._dock.hidden = true; this._dock.innerHTML = ""; return; }
  this._dock.hidden = false;
  this._dock.innerHTML = html;
};

RadialWheel.prototype._onDocPointer = function(e){
  if (!this.open) return;
  if (this.host.contains(e.target)) return;
  this.closeWheel();
};

RadialWheel.prototype._onKey = function(e){
  var tag = (e.target && e.target.tagName) || "";
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || (e.target && e.target.isContentEditable)) return;
  if (e.key === "Escape"){
    if (this.open){ e.preventDefault(); this.closeWheel(); }
    return;
  }
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  var k = String(e.key || "").toUpperCase();
  for (var i = 0; i < this.tools.length; i++){
    if (this.tools[i].key === k){
      e.preventDefault();
      if (this.open) this.select(this.tools[i].id);
      else {
        var current = this.tools[i];
        if (current.variants && current.variants.length){
          var idx = -1;
          for (var j = 0; j < current.variants.length; j++){
            if (current.variants[j].id === this.active) idx = j;
          }
          var next = current.variants[(idx + 1) % current.variants.length];
          this.select(next.id);
        } else {
          this.select(current.id);
        }
      }
      return;
    }
  }
};

RadialWheel.prototype.destroy = function(){
  document.removeEventListener("pointerdown", this._boundDoc, true);
  document.removeEventListener("keydown", this._boundKey);
  if (this.host) this.host.innerHTML = "";
};

RadialWheel.svgIcon = svgIcon;
RadialWheel.defaultTools = defaultTools;
RadialWheel.ICONS = ICONS;
RadialWheel.findTool = findTool;

window.RadialWheel = RadialWheel;
})();
