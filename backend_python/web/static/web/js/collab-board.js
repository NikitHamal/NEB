(function(){
  'use strict';

  var COLORS = [
    '#1f1f1f','#e53e3e','#dd6b20','#d69e2e','#38a169',
    '#319795','#3182ce','#5a67d8','#805ad5','#d53f8c',
    '#ffffff','#f56565','#ed8936','#ecc94b','#48bb78',
    '#38b2ac','#4299e1','#667eea','#9f7aea','#ed64a6'
  ];
  var STROKE_WIDTHS = [2, 4, 8, 14];
  var STICKY_COLORS = ['#fff9c4','#c8e6c9','#bbdefb','#f8bbd0','#e1bee7','#ffe0b2'];
  var MIN_ZOOM = 0.1;
  var MAX_ZOOM = 5;
  var GRID_SIZE = 40;

  var _board = null;

  function CollabBoard() {
    this.canvas = null;
    this.ctx = null;
    this.container = null;
    this.elements = [];
    this.camera = { x: 0, y: 0, zoom: 1 };
    this.tool = 'select';
    this.color = '#1f1f1f';
    this.strokeWidth = 4;
    this.stickyColor = '#fff9c4';
    this.selected = null;
    this.selectedIdx = -1;
    this.dragState = null;
    this.drawing = false;
    this.currentPath = [];
    this.shapeStart = null;
    this.dirty = true;
    this.rafId = null;
    this.spaceId = null;
    this.yjsInst = null;
    this.yarray = null;
    this._saveTimer = null;
    this._cursorTimer = null;
    this._textInput = null;
    this._editingIdx = -1;
    this._resizeHandle = null;
    this._spaceHeld = false;
    this._panning = false;
    this._panStart = null;
    this._panCameraStart = null;
    this._lastPinchDist = 0;
    this._imageCache = {};
    this._remoteCursors = {};
    this._boundHandlers = {};
  }

  CollabBoard.prototype.init = function(spaceId, yjsInst, savedContent) {
    var self = this;
    this.spaceId = spaceId;
    this.yjsInst = yjsInst;
    this.container = document.getElementById('cbContainer');
    this.canvas = document.getElementById('cbCanvas');
    if (!this.canvas || !this.container) return;
    this.ctx = this.canvas.getContext('2d');

    if (savedContent) {
      try {
        var parsed = JSON.parse(savedContent);
        if (Array.isArray(parsed.elements)) this.elements = parsed.elements;
        if (parsed.camera) this.camera = parsed.camera;
      } catch(e) {}
    }

    if (yjsInst && yjsInst.doc) {
      this.yarray = yjsInst.doc.getArray('board_elements');
      if (this.yarray.length > 0) {
        this.elements = [];
        for (var i = 0; i < this.yarray.length; i++) {
          try { this.elements.push(JSON.parse(JSON.stringify(this.yarray.get(i)))); } catch(e) {}
        }
      } else if (this.elements.length > 0) {
        yjsInst.doc.transact(function() {
          for (var j = 0; j < self.elements.length; j++) {
            self.yarray.push([JSON.parse(JSON.stringify(self.elements[j]))]);
          }
        }, 'init');
      }
      this.yarray.observe(function(evt, tr) {
        if (tr.origin === 'local' || tr.origin === 'init') return;
        self.elements = [];
        for (var k = 0; k < self.yarray.length; k++) {
          try { self.elements.push(JSON.parse(JSON.stringify(self.yarray.get(k)))); } catch(e) {}
        }
        self.dirty = true;
      });

      if (yjsInst._onRemoteCursor) {
        var origCb = yjsInst._onRemoteCursor;
        yjsInst._onRemoteCursor = function(cursors) {
          self._handleRemoteCursors(cursors);
          origCb(cursors);
        };
      } else {
        yjsInst._onRemoteCursor = function(cursors) {
          self._handleRemoteCursors(cursors);
        };
      }
    }

    this._resize();
    this._bindEvents();
    this._buildToolbar();
    this._startLoop();
    this.dirty = true;
  };

  CollabBoard.prototype.destroy = function() {
    if (this.rafId) cancelAnimationFrame(this.rafId);
    this.rafId = null;
    if (this._saveTimer) clearTimeout(this._saveTimer);
    if (this._cursorTimer) clearTimeout(this._cursorTimer);
    this._unbindEvents();
    this._removeTextInput();
    this._remoteCursors = {};
    var cc = document.getElementById('cbCursors');
    if (cc) cc.innerHTML = '';
    _board = null;
  };

  CollabBoard.prototype.serialize = function() {
    return JSON.stringify({ elements: this.elements, camera: this.camera });
  };

  // ── Rendering ──

  CollabBoard.prototype._startLoop = function() {
    var self = this;
    function loop() {
      self.rafId = requestAnimationFrame(loop);
      if (self.dirty) {
        self._render();
        self.dirty = false;
      }
    }
    loop();
  };

  CollabBoard.prototype._render = function() {
    var ctx = this.ctx;
    var w = this.canvas.width;
    var h = this.canvas.height;
    var cam = this.camera;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, w, h);

    this._drawGrid(ctx, w, h, cam);

    ctx.setTransform(cam.zoom, 0, 0, cam.zoom, cam.x, cam.y);

    for (var i = 0; i < this.elements.length; i++) {
      this._drawElement(ctx, this.elements[i], i === this.selectedIdx);
    }

    if (this.drawing && this.tool === 'pen' && this.currentPath.length > 1) {
      ctx.strokeStyle = this.color;
      ctx.lineWidth = this.strokeWidth / cam.zoom;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(this.currentPath[0].x, this.currentPath[0].y);
      for (var p = 1; p < this.currentPath.length; p++) {
        ctx.lineTo(this.currentPath[p].x, this.currentPath[p].y);
      }
      ctx.stroke();
    }

    if (this.drawing && this.shapeStart && (this.tool === 'rect' || this.tool === 'ellipse' || this.tool === 'line' || this.tool === 'arrow')) {
      this._drawShapePreview(ctx);
    }
  };

  CollabBoard.prototype._drawGrid = function(ctx, w, h, cam) {
    var gs = GRID_SIZE * cam.zoom;
    if (gs < 8) return;
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--md-outline-variant') || 'rgba(0,0,0,0.06)';
    ctx.lineWidth = 0.5;
    var ox = cam.x % gs;
    var oy = cam.y % gs;
    ctx.beginPath();
    for (var x = ox; x < w; x += gs) { ctx.moveTo(x, 0); ctx.lineTo(x, h); }
    for (var y = oy; y < h; y += gs) { ctx.moveTo(0, y); ctx.lineTo(w, y); }
    ctx.stroke();
  };

  CollabBoard.prototype._drawElement = function(ctx, el, isSelected) {
    if (!el) return;
    ctx.save();
    switch (el.type) {
      case 'pen': this._drawPen(ctx, el); break;
      case 'rect': this._drawRect(ctx, el); break;
      case 'ellipse': this._drawEllipse(ctx, el); break;
      case 'line': this._drawLine(ctx, el); break;
      case 'arrow': this._drawArrow(ctx, el); break;
      case 'sticky': this._drawSticky(ctx, el); break;
      case 'text': this._drawText(ctx, el); break;
      case 'image': this._drawImage(ctx, el); break;
    }
    if (isSelected) this._drawSelectionBox(ctx, el);
    ctx.restore();
  };

  CollabBoard.prototype._drawPen = function(ctx, el) {
    if (!el.points || el.points.length < 2) return;
    ctx.strokeStyle = el.color || '#1f1f1f';
    ctx.lineWidth = el.lineWidth || 4;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(el.points[0].x, el.points[0].y);
    for (var i = 1; i < el.points.length; i++) ctx.lineTo(el.points[i].x, el.points[i].y);
    ctx.stroke();
  };

  CollabBoard.prototype._drawRect = function(ctx, el) {
    if (el.fill && el.fill !== 'transparent') {
      ctx.fillStyle = el.fill;
      ctx.beginPath();
      ctx.roundRect(el.x, el.y, el.w, el.h, 4);
      ctx.fill();
    }
    ctx.strokeStyle = el.stroke || '#1f1f1f';
    ctx.lineWidth = el.lineWidth || 2;
    ctx.beginPath();
    ctx.roundRect(el.x, el.y, el.w, el.h, 4);
    ctx.stroke();
  };

  CollabBoard.prototype._drawEllipse = function(ctx, el) {
    var cx = el.x + el.w / 2;
    var cy = el.y + el.h / 2;
    var rx = Math.abs(el.w / 2);
    var ry = Math.abs(el.h / 2);
    ctx.beginPath();
    ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
    if (el.fill && el.fill !== 'transparent') { ctx.fillStyle = el.fill; ctx.fill(); }
    ctx.strokeStyle = el.stroke || '#1f1f1f';
    ctx.lineWidth = el.lineWidth || 2;
    ctx.stroke();
  };

  CollabBoard.prototype._drawLine = function(ctx, el) {
    ctx.strokeStyle = el.stroke || '#1f1f1f';
    ctx.lineWidth = el.lineWidth || 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(el.x1, el.y1);
    ctx.lineTo(el.x2, el.y2);
    ctx.stroke();
  };

  CollabBoard.prototype._drawArrow = function(ctx, el) {
    ctx.strokeStyle = el.stroke || '#1f1f1f';
    ctx.lineWidth = el.lineWidth || 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(el.x1, el.y1);
    ctx.lineTo(el.x2, el.y2);
    ctx.stroke();
    var angle = Math.atan2(el.y2 - el.y1, el.x2 - el.x1);
    var headLen = Math.max(12, (el.lineWidth || 2) * 4);
    ctx.fillStyle = el.stroke || '#1f1f1f';
    ctx.beginPath();
    ctx.moveTo(el.x2, el.y2);
    ctx.lineTo(el.x2 - headLen * Math.cos(angle - 0.4), el.y2 - headLen * Math.sin(angle - 0.4));
    ctx.lineTo(el.x2 - headLen * Math.cos(angle + 0.4), el.y2 - headLen * Math.sin(angle + 0.4));
    ctx.closePath();
    ctx.fill();
  };

  CollabBoard.prototype._drawSticky = function(ctx, el) {
    var w = el.w || 160;
    var h = el.h || 120;
    ctx.fillStyle = el.bgColor || '#fff9c4';
    ctx.shadowColor = 'rgba(0,0,0,0.10)';
    ctx.shadowBlur = 8;
    ctx.shadowOffsetY = 2;
    ctx.beginPath();
    ctx.roundRect(el.x, el.y, w, h, 6);
    ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.strokeStyle = 'rgba(0,0,0,0.08)';
    ctx.lineWidth = 1;
    ctx.stroke();
    if (el.text) {
      ctx.fillStyle = '#1f1f1f';
      ctx.font = '13px Poppins, sans-serif';
      ctx.textBaseline = 'top';
      this._wrapText(ctx, el.text, el.x + 10, el.y + 10, w - 20, 18);
    }
  };

  CollabBoard.prototype._drawText = function(ctx, el) {
    ctx.fillStyle = el.color || '#1f1f1f';
    ctx.font = (el.fontSize || 16) + 'px Poppins, sans-serif';
    ctx.textBaseline = 'top';
    var lines = (el.text || '').split('\n');
    var lh = (el.fontSize || 16) * 1.4;
    for (var i = 0; i < lines.length; i++) {
      ctx.fillText(lines[i], el.x, el.y + i * lh);
    }
  };

  CollabBoard.prototype._drawImage = function(ctx, el) {
    var self = this;
    var img = this._imageCache[el.src];
    if (!img) {
      img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = function() { self.dirty = true; };
      img.src = el.src;
      this._imageCache[el.src] = img;
    }
    if (img.complete && img.naturalWidth) {
      ctx.drawImage(img, el.x, el.y, el.w || img.naturalWidth, el.h || img.naturalHeight);
    } else {
      ctx.fillStyle = 'rgba(0,0,0,0.05)';
      ctx.fillRect(el.x, el.y, el.w || 200, el.h || 150);
      ctx.fillStyle = '#999';
      ctx.font = '12px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('Loading...', el.x + (el.w || 200) / 2, el.y + (el.h || 150) / 2);
      ctx.textAlign = 'start';
    }
  };

  CollabBoard.prototype._drawShapePreview = function(ctx) {
    var s = this.shapeStart;
    var e = this._lastMouse || s;
    ctx.strokeStyle = this.color;
    ctx.lineWidth = this.strokeWidth / this.camera.zoom;
    ctx.setLineDash([6 / this.camera.zoom, 4 / this.camera.zoom]);
    if (this.tool === 'rect') {
      ctx.strokeRect(Math.min(s.x, e.x), Math.min(s.y, e.y), Math.abs(e.x - s.x), Math.abs(e.y - s.y));
    } else if (this.tool === 'ellipse') {
      var cx = (s.x + e.x) / 2;
      var cy = (s.y + e.y) / 2;
      ctx.beginPath();
      ctx.ellipse(cx, cy, Math.abs(e.x - s.x) / 2, Math.abs(e.y - s.y) / 2, 0, 0, Math.PI * 2);
      ctx.stroke();
    } else if (this.tool === 'line' || this.tool === 'arrow') {
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(e.x, e.y);
      ctx.stroke();
    }
    ctx.setLineDash([]);
  };

  CollabBoard.prototype._drawSelectionBox = function(ctx, el) {
    var b = this._getBounds(el);
    if (!b) return;
    var pad = 6 / this.camera.zoom;
    ctx.strokeStyle = '#1a73e8';
    ctx.lineWidth = 2 / this.camera.zoom;
    ctx.setLineDash([4 / this.camera.zoom, 3 / this.camera.zoom]);
    ctx.strokeRect(b.x - pad, b.y - pad, b.w + pad * 2, b.h + pad * 2);
    ctx.setLineDash([]);
    var hs = 6 / this.camera.zoom;
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#1a73e8';
    ctx.lineWidth = 1.5 / this.camera.zoom;
    var corners = [
      [b.x - pad, b.y - pad],
      [b.x + b.w + pad - hs, b.y - pad],
      [b.x - pad, b.y + b.h + pad - hs],
      [b.x + b.w + pad - hs, b.y + b.h + pad - hs]
    ];
    for (var i = 0; i < corners.length; i++) {
      ctx.fillRect(corners[i][0], corners[i][1], hs, hs);
      ctx.strokeRect(corners[i][0], corners[i][1], hs, hs);
    }
  };

  CollabBoard.prototype._wrapText = function(ctx, text, x, y, maxW, lineH) {
    var words = text.split(' ');
    var line = '';
    var cy = y;
    for (var i = 0; i < words.length; i++) {
      var test = line + words[i] + ' ';
      if (ctx.measureText(test).width > maxW && line) {
        ctx.fillText(line.trim(), x, cy);
        line = words[i] + ' ';
        cy += lineH;
      } else {
        line = test;
      }
    }
    if (line.trim()) ctx.fillText(line.trim(), x, cy);
  };

  // ── Coordinate helpers ──

  CollabBoard.prototype._screenToWorld = function(sx, sy) {
    return {
      x: (sx - this.camera.x) / this.camera.zoom,
      y: (sy - this.camera.y) / this.camera.zoom
    };
  };

  CollabBoard.prototype._worldToScreen = function(wx, wy) {
    return {
      x: wx * this.camera.zoom + this.camera.x,
      y: wy * this.camera.zoom + this.camera.y
    };
  };

  CollabBoard.prototype._getBounds = function(el) {
    if (!el) return null;
    switch (el.type) {
      case 'pen': {
        if (!el.points || !el.points.length) return null;
        var mnx = Infinity, mny = Infinity, mxx = -Infinity, mxy = -Infinity;
        for (var i = 0; i < el.points.length; i++) {
          if (el.points[i].x < mnx) mnx = el.points[i].x;
          if (el.points[i].y < mny) mny = el.points[i].y;
          if (el.points[i].x > mxx) mxx = el.points[i].x;
          if (el.points[i].y > mxy) mxy = el.points[i].y;
        }
        return { x: mnx, y: mny, w: mxx - mnx, h: mxy - mny };
      }
      case 'rect': case 'ellipse': case 'sticky': case 'image':
        return { x: el.x, y: el.y, w: el.w || 160, h: el.h || 120 };
      case 'text': {
        var tw = (el.text || '').length * (el.fontSize || 16) * 0.6;
        var th = ((el.text || '').split('\n').length) * (el.fontSize || 16) * 1.4;
        return { x: el.x, y: el.y, w: Math.max(tw, 40), h: Math.max(th, 24) };
      }
      case 'line': case 'arrow':
        return {
          x: Math.min(el.x1, el.x2), y: Math.min(el.y1, el.y2),
          w: Math.abs(el.x2 - el.x1), h: Math.abs(el.y2 - el.y1)
        };
    }
    return null;
  };

  CollabBoard.prototype._hitTest = function(wx, wy) {
    for (var i = this.elements.length - 1; i >= 0; i--) {
      var b = this._getBounds(this.elements[i]);
      if (!b) continue;
      var pad = 8;
      if (wx >= b.x - pad && wx <= b.x + b.w + pad &&
          wy >= b.y - pad && wy <= b.y + b.h + pad) {
        return i;
      }
    }
    return -1;
  };

  // ── Event binding ──

  CollabBoard.prototype._bindEvents = function() {
    var self = this;

    this._boundHandlers.mousedown = function(e) { self._onPointerDown(e); };
    this._boundHandlers.mousemove = function(e) { self._onPointerMove(e); };
    this._boundHandlers.mouseup = function(e) { self._onPointerUp(e); };
    this._boundHandlers.wheel = function(e) { self._onWheel(e); };
    this._boundHandlers.keydown = function(e) { self._onKeyDown(e); };
    this._boundHandlers.keyup = function(e) { self._onKeyUp(e); };
    this._boundHandlers.resize = function() { self._resize(); self.dirty = true; };
    this._boundHandlers.touchstart = function(e) { self._onTouchStart(e); };
    this._boundHandlers.touchmove = function(e) { self._onTouchMove(e); };
    this._boundHandlers.touchend = function(e) { self._onTouchEnd(e); };

    this.canvas.addEventListener('mousedown', this._boundHandlers.mousedown);
    this.canvas.addEventListener('mousemove', this._boundHandlers.mousemove);
    this.canvas.addEventListener('mouseup', this._boundHandlers.mouseup);
    this.canvas.addEventListener('wheel', this._boundHandlers.wheel, { passive: false });
    this.canvas.addEventListener('touchstart', this._boundHandlers.touchstart, { passive: false });
    this.canvas.addEventListener('touchmove', this._boundHandlers.touchmove, { passive: false });
    this.canvas.addEventListener('touchend', this._boundHandlers.touchend);
    window.addEventListener('keydown', this._boundHandlers.keydown);
    window.addEventListener('keyup', this._boundHandlers.keyup);
    window.addEventListener('resize', this._boundHandlers.resize);
  };

  CollabBoard.prototype._unbindEvents = function() {
    if (!this.canvas) return;
    this.canvas.removeEventListener('mousedown', this._boundHandlers.mousedown);
    this.canvas.removeEventListener('mousemove', this._boundHandlers.mousemove);
    this.canvas.removeEventListener('mouseup', this._boundHandlers.mouseup);
    this.canvas.removeEventListener('wheel', this._boundHandlers.wheel);
    this.canvas.removeEventListener('touchstart', this._boundHandlers.touchstart);
    this.canvas.removeEventListener('touchmove', this._boundHandlers.touchmove);
    this.canvas.removeEventListener('touchend', this._boundHandlers.touchend);
    window.removeEventListener('keydown', this._boundHandlers.keydown);
    window.removeEventListener('keyup', this._boundHandlers.keyup);
    window.removeEventListener('resize', this._boundHandlers.resize);
  };

  CollabBoard.prototype._resize = function() {
    if (!this.canvas || !this.container) return;
    var dpr = window.devicePixelRatio || 1;
    var r = this.container.getBoundingClientRect();
    this.canvas.width = r.width * dpr;
    this.canvas.height = r.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.canvas.style.width = r.width + 'px';
    this.canvas.style.height = r.height + 'px';
    this.dirty = true;
  };

  // ── Pointer handlers ──

  CollabBoard.prototype._getCanvasXY = function(e) {
    var r = this.canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  };

  CollabBoard.prototype._onPointerDown = function(e) {
    if (e.button === 1 || (e.button === 0 && this._spaceHeld)) {
      this._panning = true;
      this._panStart = { x: e.clientX, y: e.clientY };
      this._panCameraStart = { x: this.camera.x, y: this.camera.y };
      this.canvas.classList.add('cb-cursor-grabbing');
      e.preventDefault();
      return;
    }
    if (e.button !== 0) return;
    var pos = this._getCanvasXY(e);
    var wp = this._screenToWorld(pos.x, pos.y);

    this._removeTextInput();

    switch (this.tool) {
      case 'select':
        var idx = this._hitTest(wp.x, wp.y);
        if (idx >= 0) {
          this.selectedIdx = idx;
          this.selected = this.elements[idx];
          var b = this._getBounds(this.selected);
          this.dragState = { startX: wp.x, startY: wp.y, origEl: JSON.parse(JSON.stringify(this.selected)) };
        } else {
          this.selectedIdx = -1;
          this.selected = null;
        }
        this.dirty = true;
        break;
      case 'pen':
        this.drawing = true;
        this.currentPath = [{ x: wp.x, y: wp.y }];
        break;
      case 'rect': case 'ellipse': case 'line': case 'arrow':
        this.drawing = true;
        this.shapeStart = { x: wp.x, y: wp.y };
        this._lastMouse = { x: wp.x, y: wp.y };
        break;
      case 'sticky':
        this._addElement({
          type: 'sticky', x: wp.x - 80, y: wp.y - 60,
          w: 160, h: 120, text: '', bgColor: this.stickyColor, id: this._uid()
        });
        this.selectedIdx = this.elements.length - 1;
        this.selected = this.elements[this.selectedIdx];
        this.dirty = true;
        this._startTextEdit(this.selectedIdx);
        break;
      case 'text':
        this._addElement({
          type: 'text', x: wp.x, y: wp.y, text: '',
          fontSize: 18, color: this.color, id: this._uid()
        });
        this.selectedIdx = this.elements.length - 1;
        this.selected = this.elements[this.selectedIdx];
        this.dirty = true;
        this._startTextEdit(this.selectedIdx);
        break;
      case 'image':
        this._promptImage(wp.x, wp.y);
        break;
      case 'eraser':
        var eidx = this._hitTest(wp.x, wp.y);
        if (eidx >= 0) {
          this._removeElement(eidx);
          this.selectedIdx = -1;
          this.selected = null;
          this.dirty = true;
        }
        break;
    }
  };

  CollabBoard.prototype._onPointerMove = function(e) {
    var pos = this._getCanvasXY(e);

    if (this._panning && this._panStart) {
      this.camera.x = this._panCameraStart.x + (e.clientX - this._panStart.x);
      this.camera.y = this._panCameraStart.y + (e.clientY - this._panStart.y);
      this.dirty = true;
      return;
    }

    var wp = this._screenToWorld(pos.x, pos.y);

    if (this._cursorTimer) clearTimeout(this._cursorTimer);
    var self = this;
    this._cursorTimer = setTimeout(function() {
      if (self.yjsInst) self.yjsInst._sendAwareness(Math.round(wp.x), Math.round(wp.y));
    }, 60);

    if (this.drawing && this.tool === 'pen') {
      this.currentPath.push({ x: wp.x, y: wp.y });
      this.dirty = true;
    }

    if (this.drawing && this.shapeStart) {
      this._lastMouse = { x: wp.x, y: wp.y };
      this.dirty = true;
    }

    if (this.dragState && this.selected && this.tool === 'select') {
      var dx = wp.x - this.dragState.startX;
      var dy = wp.y - this.dragState.startY;
      var orig = this.dragState.origEl;
      if (this.selected.type === 'line' || this.selected.type === 'arrow') {
        this.selected.x1 = orig.x1 + dx;
        this.selected.y1 = orig.y1 + dy;
        this.selected.x2 = orig.x2 + dx;
        this.selected.y2 = orig.y2 + dy;
      } else if (this.selected.type === 'pen') {
        for (var i = 0; i < this.selected.points.length; i++) {
          this.selected.points[i].x = orig.points[i].x + dx;
          this.selected.points[i].y = orig.points[i].y + dy;
        }
      } else {
        this.selected.x = orig.x + dx;
        this.selected.y = orig.y + dy;
      }
      this.dirty = true;
    }

    if (this.tool === 'select' && !this.dragState) {
      var hi = this._hitTest(wp.x, wp.y);
      this.canvas.classList.toggle('cb-cursor-move', hi >= 0);
      this.canvas.classList.toggle('cb-cursor-default', hi < 0);
    }
  };

  CollabBoard.prototype._onPointerUp = function(e) {
    if (this._panning) {
      this._panning = false;
      this._panStart = null;
      this.canvas.classList.remove('cb-cursor-grabbing');
      return;
    }

    if (this.drawing && this.tool === 'pen' && this.currentPath.length > 1) {
      this._addElement({
        type: 'pen', points: this.currentPath.slice(),
        color: this.color, lineWidth: this.strokeWidth, id: this._uid()
      });
    }

    if (this.drawing && this.shapeStart && this._lastMouse) {
      var s = this.shapeStart;
      var e2 = this._lastMouse;
      if (Math.abs(e2.x - s.x) > 4 || Math.abs(e2.y - s.y) > 4) {
        var newEl = null;
        if (this.tool === 'rect') {
          newEl = {
            type: 'rect', x: Math.min(s.x, e2.x), y: Math.min(s.y, e2.y),
            w: Math.abs(e2.x - s.x), h: Math.abs(e2.y - s.y),
            fill: 'transparent', stroke: this.color, lineWidth: this.strokeWidth, id: this._uid()
          };
        } else if (this.tool === 'ellipse') {
          newEl = {
            type: 'ellipse', x: Math.min(s.x, e2.x), y: Math.min(s.y, e2.y),
            w: Math.abs(e2.x - s.x), h: Math.abs(e2.y - s.y),
            fill: 'transparent', stroke: this.color, lineWidth: this.strokeWidth, id: this._uid()
          };
        } else if (this.tool === 'line') {
          newEl = { type: 'line', x1: s.x, y1: s.y, x2: e2.x, y2: e2.y, stroke: this.color, lineWidth: this.strokeWidth, id: this._uid() };
        } else if (this.tool === 'arrow') {
          newEl = { type: 'arrow', x1: s.x, y1: s.y, x2: e2.x, y2: e2.y, stroke: this.color, lineWidth: this.strokeWidth, id: this._uid() };
        }
        if (newEl) this._addElement(newEl);
      }
    }

    if (this.dragState && this.selectedIdx >= 0) {
      this._updateElement(this.selectedIdx, this.elements[this.selectedIdx]);
    }

    this.drawing = false;
    this.currentPath = [];
    this.shapeStart = null;
    this._lastMouse = null;
    this.dragState = null;
    this.dirty = true;
  };

  // ── Touch handlers ──

  CollabBoard.prototype._onTouchStart = function(e) {
    if (e.touches.length === 2) {
      this._lastPinchDist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      e.preventDefault();
      return;
    }
    if (e.touches.length === 1) {
      var t = e.touches[0];
      this._onPointerDown({ button: 0, clientX: t.clientX, clientY: t.clientY, preventDefault: function() {} });
      e.preventDefault();
    }
  };

  CollabBoard.prototype._onTouchMove = function(e) {
    if (e.touches.length === 2) {
      var dist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      if (this._lastPinchDist > 0) {
        var scale = dist / this._lastPinchDist;
        var midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        var midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        var r = this.canvas.getBoundingClientRect();
        this._zoomAt(midX - r.left, midY - r.top, scale);
      }
      this._lastPinchDist = dist;
      e.preventDefault();
      return;
    }
    if (e.touches.length === 1) {
      var t = e.touches[0];
      this._onPointerMove({ clientX: t.clientX, clientY: t.clientY });
      e.preventDefault();
    }
  };

  CollabBoard.prototype._onTouchEnd = function(e) {
    this._lastPinchDist = 0;
    this._onPointerUp({});
  };

  // ── Zoom ──

  CollabBoard.prototype._onWheel = function(e) {
    e.preventDefault();
    var pos = this._getCanvasXY(e);
    var factor = e.deltaY < 0 ? 1.08 : 0.92;
    this._zoomAt(pos.x, pos.y, factor);
  };

  CollabBoard.prototype._zoomAt = function(sx, sy, factor) {
    var newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, this.camera.zoom * factor));
    var wp = this._screenToWorld(sx, sy);
    this.camera.zoom = newZoom;
    this.camera.x = sx - wp.x * newZoom;
    this.camera.y = sy - wp.y * newZoom;
    this.dirty = true;
    this._updateZoomLabel();
  };

  CollabBoard.prototype._updateZoomLabel = function() {
    var label = document.getElementById('cbZoomLabel');
    if (label) label.textContent = Math.round(this.camera.zoom * 100) + '%';
  };

  // ── Keyboard ──

  CollabBoard.prototype._onKeyDown = function(e) {
    if (this._textInput) return;
    if (e.key === ' ' && !this._spaceHeld) {
      this._spaceHeld = true;
      this.canvas.classList.add('cb-cursor-grab');
      e.preventDefault();
    }
    if ((e.key === 'Delete' || e.key === 'Backspace') && this.selectedIdx >= 0) {
      this._removeElement(this.selectedIdx);
      this.selectedIdx = -1;
      this.selected = null;
      this.dirty = true;
      e.preventDefault();
    }
    if (e.key === 'Escape') {
      this.selectedIdx = -1;
      this.selected = null;
      this._removeTextInput();
      this.dirty = true;
    }
  };

  CollabBoard.prototype._onKeyUp = function(e) {
    if (e.key === ' ') {
      this._spaceHeld = false;
      this.canvas.classList.remove('cb-cursor-grab');
    }
  };

  // ── Element CRUD (synced via Yjs) ──

  CollabBoard.prototype._uid = function() {
    return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  };

  CollabBoard.prototype._addElement = function(el) {
    this.elements.push(el);
    if (this.yarray) {
      var self = this;
      this.yjsInst.doc.transact(function() {
        self.yarray.push([JSON.parse(JSON.stringify(el))]);
      }, 'local');
    }
    this._scheduleSave();
    this.dirty = true;
  };

  CollabBoard.prototype._updateElement = function(idx, el) {
    this.elements[idx] = el;
    if (this.yarray && idx < this.yarray.length) {
      var self = this;
      this.yjsInst.doc.transact(function() {
        self.yarray.delete(idx, 1);
        self.yarray.insert(idx, [JSON.parse(JSON.stringify(el))]);
      }, 'local');
    }
    this._scheduleSave();
    this.dirty = true;
  };

  CollabBoard.prototype._removeElement = function(idx) {
    this.elements.splice(idx, 1);
    if (this.yarray && idx < this.yarray.length) {
      var self = this;
      this.yjsInst.doc.transact(function() {
        self.yarray.delete(idx, 1);
      }, 'local');
    }
    this._scheduleSave();
    this.dirty = true;
  };

  CollabBoard.prototype._scheduleSave = function() {
    if (this._saveTimer) clearTimeout(this._saveTimer);
    var self = this;
    this._saveTimer = setTimeout(function() {
      self._saveToServer();
    }, 3000);
  };

  CollabBoard.prototype._saveToServer = function() {
    if (!this.spaceId) return;
    var content = this.serialize();
    var csrfEl = document.querySelector('meta[name="csrf-token"]');
    var csrf = csrfEl ? csrfEl.content : '';
    fetch('/ajax/study-space/' + this.spaceId + '/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
      body: JSON.stringify({ content: content })
    }).catch(function() {});
    var statusEl = document.getElementById('cbStatusText');
    if (statusEl) statusEl.textContent = 'Saved';
    setTimeout(function() { if (statusEl) statusEl.textContent = 'Synced'; }, 2000);
  };

  // ── Text editing ──

  CollabBoard.prototype._startTextEdit = function(idx) {
    var el = this.elements[idx];
    if (!el || (el.type !== 'sticky' && el.type !== 'text')) return;
    this._removeTextInput();
    this._editingIdx = idx;

    var b = this._getBounds(el);
    if (!b) return;
    var sp = this._worldToScreen(b.x, b.y);

    var input = document.createElement('textarea');
    input.className = 'cb-text-input';
    input.value = el.text || '';
    input.style.left = sp.x + 'px';
    input.style.top = sp.y + 'px';
    input.style.width = Math.max(b.w * this.camera.zoom, 60) + 'px';
    input.style.height = Math.max(b.h * this.camera.zoom, 28) + 'px';
    input.style.fontSize = ((el.fontSize || 13) * this.camera.zoom) + 'px';
    if (el.type === 'sticky') {
      input.style.background = el.bgColor || '#fff9c4';
      input.style.color = '#1f1f1f';
    }
    this.container.appendChild(input);
    this._textInput = input;
    input.focus();

    var self = this;
    input.addEventListener('blur', function() {
      self._commitTextEdit();
    });
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') { self._commitTextEdit(); e.preventDefault(); }
      e.stopPropagation();
    });
  };

  CollabBoard.prototype._commitTextEdit = function() {
    if (!this._textInput || this._editingIdx < 0) return;
    var el = this.elements[this._editingIdx];
    if (el) {
      el.text = this._textInput.value;
      if (!el.text && (el.type === 'text' || el.type === 'sticky')) {
        this._removeElement(this._editingIdx);
        this.selectedIdx = -1;
        this.selected = null;
      } else {
        this._updateElement(this._editingIdx, el);
      }
    }
    this._removeTextInput();
    this.dirty = true;
  };

  CollabBoard.prototype._removeTextInput = function() {
    if (this._textInput && this._textInput.parentNode) {
      this._textInput.parentNode.removeChild(this._textInput);
    }
    this._textInput = null;
    this._editingIdx = -1;
  };

  // ── Image upload ──

  CollabBoard.prototype._promptImage = function(wx, wy) {
    var inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = 'image/*';
    var self = this;
    inp.onchange = function() {
      if (!inp.files || !inp.files.length) return;
      var file = inp.files[0];
      var fd = new FormData();
      fd.append('file', file);
      var csrfEl = document.querySelector('meta[name="csrf-token"]');
      var csrf = csrfEl ? csrfEl.content : '';
      fetch('/ajax/study-space/' + self.spaceId + '/upload/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
        body: fd
      })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.error) { if (typeof window.showSnackbar === 'function') window.showSnackbar(data.error); return; }
        var url = data.fileUrl || data.file_url || '';
        if (!url) return;
        self._addElement({
          type: 'image', x: wx - 100, y: wy - 75,
          w: 200, h: 150, src: url, id: self._uid()
        });
      })
      .catch(function() {
        if (typeof window.showSnackbar === 'function') window.showSnackbar('Image upload failed');
      });
    };
    inp.click();
  };

  // ── Remote cursors ──

  CollabBoard.prototype._handleRemoteCursors = function(cursors) {
    var cc = document.getElementById('cbCursors');
    if (!cc) return;
    var keys = Object.keys(cursors);
    if (!keys.length) { cc.innerHTML = ''; return; }
    var html = '';
    for (var i = 0; i < keys.length; i++) {
      var c = cursors[keys[i]];
      var sp = this._worldToScreen(c.start || 0, c.end || 0);
      var col = c.color || '#e53e3e';
      var name = (c.name || 'Someone');
      if (name.length > 14) name = name.slice(0, 14) + '\u2026';
      html += '<div class="cb-remote-cursor" style="left:' + sp.x + 'px;top:' + sp.y + 'px;--cur-color:' + col + '">' +
        '<div class="cb-remote-cursor-arrow" style="border-top-color:' + col + '"></div>' +
        '<div class="cb-remote-cursor-name" style="background:' + col + '">' + name + '</div>' +
      '</div>';
    }
    cc.innerHTML = html;
  };

  // ── Toolbar builder ──

  CollabBoard.prototype._buildToolbar = function() {
    var tb = document.getElementById('cbToolbar');
    if (!tb) return;
    var self = this;

    var tools = [
      { id: 'select', icon: 'near_me', title: 'Select / Move' },
      { sep: true },
      { id: 'pen', icon: 'draw', title: 'Pen' },
      { id: 'rect', icon: 'rectangle', title: 'Rectangle' },
      { id: 'ellipse', icon: 'circle', title: 'Ellipse' },
      { id: 'line', icon: 'horizontal_rule', title: 'Line' },
      { id: 'arrow', icon: 'arrow_right_alt', title: 'Arrow' },
      { sep: true },
      { id: 'sticky', icon: 'sticky_note_2', title: 'Sticky Note' },
      { id: 'text', icon: 'text_fields', title: 'Text' },
      { id: 'image', icon: 'image', title: 'Image' },
      { sep: true },
      { id: 'eraser', icon: 'ink_eraser', title: 'Eraser' },
      { sep: true },
      { id: 'color', icon: 'palette', title: 'Color' },
      { id: 'stroke', icon: 'line_weight', title: 'Stroke Width' },
    ];

    var html = '';
    for (var i = 0; i < tools.length; i++) {
      var t = tools[i];
      if (t.sep) { html += '<div class="cb-toolbar-sep"></div>'; continue; }
      var active = t.id === this.tool ? ' cb-active' : '';
      html += '<button class="cb-tool-btn' + active + '" data-tool="' + t.id + '" title="' + t.title + '">' +
        '<span class="material-symbols-outlined">' + t.icon + '</span></button>';
    }

    html += '<div class="cb-color-picker" id="cbColorPicker">';
    for (var c = 0; c < COLORS.length; c++) {
      var act = COLORS[c] === this.color ? ' cb-swatch-active' : '';
      html += '<div class="cb-color-swatch' + act + '" data-color="' + COLORS[c] + '" style="background:' + COLORS[c] + '"></div>';
    }
    html += '</div>';

    html += '<div class="cb-stroke-picker" id="cbStrokePicker">';
    for (var s = 0; s < STROKE_WIDTHS.length; s++) {
      var sa = STROKE_WIDTHS[s] === this.strokeWidth ? ' cb-stroke-active' : '';
      html += '<div class="cb-stroke-opt' + sa + '" data-width="' + STROKE_WIDTHS[s] + '"><span style="width:' + Math.min(STROKE_WIDTHS[s] * 2, 20) + 'px;height:' + STROKE_WIDTHS[s] + 'px"></span></div>';
    }
    html += '</div>';

    tb.innerHTML = html;

    tb.addEventListener('click', function(e) {
      var btn = e.target.closest('[data-tool]');
      if (btn) {
        var tid = btn.dataset.tool;
        if (tid === 'color') {
          var cp = document.getElementById('cbColorPicker');
          if (cp) cp.classList.toggle('cb-open');
          var sp = document.getElementById('cbStrokePicker');
          if (sp) sp.classList.remove('cb-open');
          return;
        }
        if (tid === 'stroke') {
          var sp2 = document.getElementById('cbStrokePicker');
          if (sp2) sp2.classList.toggle('cb-open');
          var cp2 = document.getElementById('cbColorPicker');
          if (cp2) cp2.classList.remove('cb-open');
          return;
        }
        self.tool = tid;
        self.selectedIdx = -1;
        self.selected = null;
        self.dirty = true;
        tb.querySelectorAll('.cb-tool-btn').forEach(function(b) {
          b.classList.toggle('cb-active', b.dataset.tool === tid);
        });
        document.getElementById('cbColorPicker')?.classList.remove('cb-open');
        document.getElementById('cbStrokePicker')?.classList.remove('cb-open');
        self._updateCanvasCursor();
      }

      var swatch = e.target.closest('[data-color]');
      if (swatch) {
        self.color = swatch.dataset.color;
        tb.querySelectorAll('.cb-color-swatch').forEach(function(s) {
          s.classList.toggle('cb-swatch-active', s.dataset.color === self.color);
        });
      }

      var strokeOpt = e.target.closest('[data-width]');
      if (strokeOpt) {
        self.strokeWidth = parseInt(strokeOpt.dataset.width, 10);
        tb.querySelectorAll('.cb-stroke-opt').forEach(function(s) {
          s.classList.toggle('cb-stroke-active', parseInt(s.dataset.width, 10) === self.strokeWidth);
        });
      }
    });
  };

  CollabBoard.prototype._updateCanvasCursor = function() {
    this.canvas.className = '';
    switch (this.tool) {
      case 'select': this.canvas.classList.add('cb-cursor-default'); break;
      case 'text': this.canvas.classList.add('cb-cursor-text'); break;
      default: break;
    }
  };

  // ── Zoom controls ──

  CollabBoard.prototype.zoomIn = function() {
    var cx = this.canvas.width / (window.devicePixelRatio || 1) / 2;
    var cy = this.canvas.height / (window.devicePixelRatio || 1) / 2;
    this._zoomAt(cx, cy, 1.2);
  };

  CollabBoard.prototype.zoomOut = function() {
    var cx = this.canvas.width / (window.devicePixelRatio || 1) / 2;
    var cy = this.canvas.height / (window.devicePixelRatio || 1) / 2;
    this._zoomAt(cx, cy, 0.8);
  };

  CollabBoard.prototype.zoomFit = function() {
    this.camera = { x: 0, y: 0, zoom: 1 };
    this.dirty = true;
    this._updateZoomLabel();
  };

  // ── Static entry points ──

  window.CollabBoard = {
    init: function(spaceId, yjsInst, savedContent) {
      if (_board) _board.destroy();
      _board = new CollabBoard();
      _board.init(spaceId, yjsInst, savedContent);
    },
    destroy: function() {
      if (_board) {
        _board._saveToServer();
        _board.destroy();
        _board = null;
      }
    },
    serialize: function() {
      return _board ? _board.serialize() : '';
    },
    zoomIn: function() { if (_board) _board.zoomIn(); },
    zoomOut: function() { if (_board) _board.zoomOut(); },
    zoomFit: function() { if (_board) _board.zoomFit(); },
    getInstance: function() { return _board; }
  };
})();
