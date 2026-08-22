(function(){
  'use strict';

  var scene = null;
  var overlays = new Map();
  var frame = 0;
  var activeBoard = null;
  var lastSignature = '';
  var lastFrameAt = 0;

  function ext(url) {
    var clean = String(url || '').split('?')[0].split('#')[0].toLowerCase();
    var index = clean.lastIndexOf('.');
    return index >= 0 ? clean.slice(index + 1) : '';
  }

  function mediaKind(url, title, mime) {
    var e = ext(url || title);
    var m = String(mime || '').toLowerCase();
    if (m.indexOf('video/') === 0 || /^(mp4|webm|mov|m4v|ogv)$/.test(e)) return 'video';
    if (m.indexOf('audio/') === 0 || /^(mp3|wav|ogg|m4a|aac|flac|opus)$/.test(e)) return 'audio';
    if (m === 'application/pdf' || e === 'pdf') return 'pdf';
    return '';
  }

  function normalizeMedia(el) {
    if (!el || el.type !== 'document_card') return el;
    var kind = mediaKind(el.url, el.title, el.mimeType);
    if (!kind) return el;
    return {
      type: 'media', kind: kind, x: el.x, y: el.y,
      w: kind === 'audio' ? 420 : 480,
      h: kind === 'audio' ? 96 : 300,
      title: el.title, url: el.url, id: el.id
    };
  }

  function boardSignature(board) {
    var parts = [board.camera.x, board.camera.y, board.camera.zoom, board.selectedIdx, board.elements.length];
    for (var i = 0; i < board.elements.length; i++) {
      var el = board.elements[i];
      if (el && el.type === 'media') parts.push(el.id, el.x, el.y, el.w, el.h, el.url);
    }
    return parts.join('|');
  }

  function initThree(container) {
    if (!window.THREE || !container) return null;
    var canvas = document.createElement('canvas');
    canvas.className = 'cb-three-scene';
    container.insertBefore(canvas, container.firstChild);
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: false, antialias: false, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    var s = new THREE.Scene();
    var camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    var material = new THREE.ShaderMaterial({
      uniforms: {
        uResolution: { value: new THREE.Vector2(1, 1) },
        uCamera: { value: new THREE.Vector3(0, 0, 1) },
        uTheme: { value: 0 }
      },
      vertexShader: 'void main(){gl_Position=vec4(position,1.0);}',
      fragmentShader: [
        'precision mediump float;',
        'uniform vec2 uResolution;',
        'uniform vec3 uCamera;',
        'uniform float uTheme;',
        'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
        'void main(){',
        'vec2 uv=gl_FragCoord.xy/uResolution.xy;',
        'vec2 world=(gl_FragCoord.xy-uResolution*.5)/max(uCamera.z,.001)-uCamera.xy*.18;',
        'float grain=hash(floor(world*1.7))*0.035+hash(floor(world*0.23))*0.025;',
        'float scratch=step(.995,hash(vec2(floor(world.x*.05),floor(world.y*.7))))*.035;',
        'vec3 dark=vec3(.055,.058,.062);',
        'vec3 green=vec3(.035,.145,.105);',
        'vec3 blue=vec3(.045,.105,.19);',
        'vec3 base=mix(dark,mix(green,blue,.18),uTheme);',
        'float vignette=smoothstep(.95,.15,distance(uv,vec2(.5)));',
        'gl_FragColor=vec4(base+grain+scratch+vignette*.018,1.0);',
        '}'
      ].join('')
    });
    var mesh = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), material);
    s.add(mesh);
    var ro = new ResizeObserver(function(entries) {
      var r = entries[0].contentRect;
      renderer.setSize(Math.max(1, r.width), Math.max(1, r.height), false);
      material.uniforms.uResolution.value.set(Math.max(1, r.width) * renderer.getPixelRatio(), Math.max(1, r.height) * renderer.getPixelRatio());
      renderer.render(s, camera);
    });
    ro.observe(container);
    return { canvas: canvas, renderer: renderer, scene: s, camera: camera, material: material, observer: ro };
  }

  function updateThree(board) {
    if (!scene || !board) return;
    scene.material.uniforms.uCamera.value.set(board.camera.x, board.camera.y, board.camera.zoom);
    var theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 0 : 1;
    scene.material.uniforms.uTheme.value = theme;
    scene.renderer.render(scene.scene, scene.camera);
  }

  function createOverlay(board, el) {
    var node = document.createElement('div');
    node.className = 'cb-media-frame';
    node.dataset.elementId = el.id;
    var head = document.createElement('div');
    head.className = 'cb-media-head';
    var title = document.createElement('span');
    title.textContent = el.title || (el.kind === 'pdf' ? 'PDF document' : el.kind === 'audio' ? 'Audio' : 'Video');
    var open = document.createElement('a');
    open.href = el.url;
    open.target = '_blank';
    open.rel = 'noopener';
    open.className = 'material-symbols-outlined';
    open.textContent = 'open_in_new';
    head.appendChild(title);
    head.appendChild(open);
    head.addEventListener('pointerdown', function(event) {
      if (event.button !== 0 || event.target.closest('a')) return;
      var index = board.elements.findIndex(function(item) { return item && item.id === el.id; });
      if (index < 0) return;
      event.preventDefault();
      event.stopPropagation();
      head.setPointerCapture(event.pointerId);
      board.selectedIdx = index;
      board.selected = board.elements[index];
      var startX = event.clientX;
      var startY = event.clientY;
      var originX = board.elements[index].x;
      var originY = board.elements[index].y;
      function move(moveEvent) {
        var current = board.elements[index];
        if (!current) return;
        current.x = originX + (moveEvent.clientX - startX) / board.camera.zoom;
        current.y = originY + (moveEvent.clientY - startY) / board.camera.zoom;
        board.selected = current;
        board.dirty = true;
        syncOverlays(board);
      }
      function end() {
        head.removeEventListener('pointermove', move);
        head.removeEventListener('pointerup', end);
        head.removeEventListener('pointercancel', end);
        var current = board.elements[index];
        if (current) board._updateElement(index, Object.assign({}, current));
      }
      head.addEventListener('pointermove', move);
      head.addEventListener('pointerup', end);
      head.addEventListener('pointercancel', end);
    });
    node.appendChild(head);
    if (el.kind === 'video') {
      var video = document.createElement('video');
      video.src = el.url;
      video.controls = true;
      video.preload = 'metadata';
      video.playsInline = true;
      node.appendChild(video);
    } else if (el.kind === 'audio') {
      var audio = document.createElement('audio');
      audio.src = el.url;
      audio.controls = true;
      audio.preload = 'metadata';
      node.appendChild(audio);
    } else {
      var embed = document.createElement('iframe');
      embed.src = el.url + (String(el.url).indexOf('#') >= 0 ? '' : '#toolbar=1&navpanes=0');
      embed.loading = 'lazy';
      embed.title = el.title || 'PDF';
      node.appendChild(embed);
    }
    board.container.appendChild(node);
    overlays.set(el.id, node);
    return node;
  }

  function syncOverlays(board) {
    if (!board || !board.container) return;
    var live = new Set();
    board.elements.forEach(function(el) {
      if (!el || el.type !== 'media') return;
      live.add(el.id);
      var node = overlays.get(el.id) || createOverlay(board, el);
      var x = el.x * board.camera.zoom + board.camera.x;
      var y = el.y * board.camera.zoom + board.camera.y;
      var w = (el.w || 420) * board.camera.zoom;
      var h = (el.h || 260) * board.camera.zoom;
      node.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
      node.style.width = Math.max(180, w) + 'px';
      node.style.height = Math.max(el.kind === 'audio' ? 92 : 150, h) + 'px';
      node.style.display = board.camera.zoom < .22 ? 'none' : '';
      var selected = board.selectedIdx >= 0 ? board.elements[board.selectedIdx] : null;
      node.classList.toggle('cb-media-selected', selected && selected.id === el.id);
    });
    overlays.forEach(function(node, id) {
      if (!live.has(id)) {
        node.remove();
        overlays.delete(id);
      }
    });
  }

  function loop(now) {
    frame = requestAnimationFrame(loop);
    if (!activeBoard || now - lastFrameAt < 32) return;
    lastFrameAt = now;
    var signature = boardSignature(activeBoard);
    if (signature === lastSignature) return;
    lastSignature = signature;
    if (scene) updateThree(activeBoard);
    syncOverlays(activeBoard);
  }

  function smooth(points) {
    if (!points || points.length < 3) return points || [];
    var out = [points[0]];
    for (var i = 1; i < points.length - 1; i++) {
      var a = points[i - 1];
      var b = points[i];
      var c = points[i + 1];
      out.push({ x: (a.x + b.x * 2 + c.x) / 4, y: (a.y + b.y * 2 + c.y) / 4, p: b.p || 0.5 });
    }
    out.push(points[points.length - 1]);
    return out;
  }

  function install(board) {
    if (!board || board.__proInstalled) return;
    board.__proInstalled = true;
    activeBoard = board;
    scene = null;
    var normalized = false;
    for (var initialIndex = 0; initialIndex < board.elements.length; initialIndex++) {
      var converted = normalizeMedia(board.elements[initialIndex]);
      if (converted !== board.elements[initialIndex]) {
        board.elements[initialIndex] = converted;
        normalized = true;
      }
    }
    if (normalized && board.yarray) {
      board.yjsInst.doc.transact(function() {
        board.yarray.delete(0, board.yarray.length);
        board.elements.forEach(function(item) {
          board.yarray.push([JSON.parse(JSON.stringify(item))]);
        });
      }, 'local');
      board._scheduleSave();
    }

    var originalGetXY = board._getCanvasXY.bind(board);
    board._getCanvasXY = function(e) {
      var r = board.canvas.getBoundingClientRect();
      if (!r.width || !r.height) return originalGetXY(e);
      return {
        x: (e.clientX - r.left) * (board._viewportWidth / r.width),
        y: (e.clientY - r.top) * (board._viewportHeight / r.height)
      };
    };

    var originalAdd = board._addElement.bind(board);
    board._addElement = function(el) {
      if (el && el.type === 'pen') {
        el.brush = el.brush || board.brush || 'pen';
        el.points = smooth(el.points);
      }
      el = normalizeMedia(el);
      originalAdd(el);
      lastSignature = '';
    };

    var originalDrawPen = board._drawPen.bind(board);
    board._drawPen = function(ctx, el) {
      if (!el || el.brush === 'pen' || !el.brush) return originalDrawPen(ctx, el);
      var points = el.points || [];
      if (points.length < 2) return;
      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      if (el.brush === 'pencil') {
        ctx.globalAlpha = .72;
        ctx.strokeStyle = el.color;
        ctx.lineWidth = Math.max(.8, (el.lineWidth || 2) * .55);
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (var p = 1; p < points.length; p++) ctx.lineTo(points[p].x, points[p].y);
        ctx.stroke();
      } else {
        ctx.strokeStyle = el.color || '#f6f0dc';
        ctx.globalAlpha = .82;
        ctx.lineWidth = el.lineWidth || 4;
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (var i = 1; i < points.length; i++) ctx.lineTo(points[i].x, points[i].y);
        ctx.stroke();
        ctx.globalAlpha = .18;
        for (var n = 0; n < 3; n++) {
          ctx.lineWidth = Math.max(1, (el.lineWidth || 4) * (.35 + n * .12));
          ctx.beginPath();
          ctx.moveTo(points[0].x + n - 1, points[0].y - n + 1);
          for (var j = 1; j < points.length; j++) ctx.lineTo(points[j].x + n - 1, points[j].y - n + 1);
          ctx.stroke();
        }
      }
      ctx.restore();
    };

    var originalDrawElement = board._drawElement.bind(board);
    board._drawElement = function(ctx, el, selected) {
      if (el && el.type === 'media') {
        if (selected) {
          ctx.save();
          ctx.strokeStyle = '#8b5cf6';
          ctx.lineWidth = 2 / board.camera.zoom;
          ctx.setLineDash([8 / board.camera.zoom, 5 / board.camera.zoom]);
          ctx.strokeRect(el.x, el.y, el.w || 480, el.h || 300);
          ctx.restore();
        }
        return;
      }
      originalDrawElement(ctx, el, selected);
    };

    var originalBounds = board._getBounds.bind(board);
    board._getBounds = function(el) {
      if (el && el.type === 'media') return { x: el.x, y: el.y, w: el.w || 480, h: el.h || 300 };
      return originalBounds(el);
    };

    var toolbar = document.getElementById('cbToolbar');
    if (toolbar) {
      toolbar.querySelectorAll('.cb-color-swatch').forEach(function(item) {
        item.classList.toggle('cb-swatch-active', item.dataset.color === '#ffffff');
      });
      var pen = toolbar.querySelector('[data-tool="pen"]');
      if (pen) {
        pen.title = 'Pen';
      }
    }

    board.canvas.addEventListener('pointermove', function(e) {
      if (!board.drawing || board.tool !== 'pen' || !e.getCoalescedEvents) return;
      var events = e.getCoalescedEvents();
      if (events.length < 2) return;
      var last = board.currentPath[board.currentPath.length - 1];
      events.forEach(function(point) {
        var pos = board._getCanvasXY(point);
        var wp = board._screenToWorld(pos.x, pos.y);
        if (!last || Math.hypot(wp.x - last.x, wp.y - last.y) > .55) {
          board.currentPath.push({ x: wp.x, y: wp.y, p: point.pressure || .5 });
          last = wp;
        }
      });
      board.dirty = true;
    }, { passive: true });

    var originalRemove = board._removeElement.bind(board);
    board._removeElement = function(idx) {
      var target = this.elements[idx];
      originalRemove(idx);
      if (target && overlays.has(target.id)) {
        var dead = overlays.get(target.id);
        if (dead && dead.parentNode) dead.parentNode.removeChild(dead);
        overlays.delete(target.id);
      }
    };

    var originalClear = board.clearAll ? board.clearAll.bind(board) : null;
    board.clearAll = function() {
      var ok = originalClear ? originalClear() : false;
      if (ok) {
        overlays.forEach(function(node) { if (node && node.parentNode) node.parentNode.removeChild(node); });
        overlays.clear();
      }
      return ok;
    };

    lastSignature = '';
    if (!frame) frame = requestAnimationFrame(loop);
  }

  function patchInit() {
    if (!window.CollabBoard || window.CollabBoard.__proPatched) return;
    var original = window.CollabBoard.init;
    window.CollabBoard.init = function(spaceId, bridge, saved) {
      original(spaceId, bridge, saved);
      install(window.CollabBoard.getInstance());
    };
    window.CollabBoard.__proPatched = true;
  }

  document.addEventListener('DOMContentLoaded', patchInit);
  patchInit();
})();
