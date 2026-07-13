(function(){
  'use strict';

  var COLLAB_COLORS = [
    '#E53E3E','#DD6B20','#38A169','#319795','#3182CE','#5A67D8','#805AD5','#D53F8C',
    '#F56565','#ED8936','#48BB78','#38B2AC','#4299E1','#667EEA','#9F7AEA','#ED64A6',
  ];

  function arrayToBase64(uint8) {
    var bin = '';
    for (var i = 0; i < uint8.length; i++) bin += String.fromCharCode(uint8[i]);
    return btoa(bin);
  }

  function base64ToArray(b64) {
    var bin = atob(b64);
    var u8 = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    return u8;
  }

  function pickColor(userId) {
    var hash = 0;
    for (var i = 0; i < userId.length; i++) {
      hash = ((hash << 5) - hash) + userId.charCodeAt(i);
      hash |= 0;
    }
    return COLLAB_COLORS[Math.abs(hash) % COLLAB_COLORS.length];
  }

  var _inst = null;

  function SSYjs() {
    this.doc = null;
    this.ytext = null;
    this.ws = null;
    this.spaceId = null;
    this.userId = null;
    this.userName = '';
    this.color = '';
    this._onRemoteChange = null;
    this._onSave = null;
    this._reconnectTimer = null;
    this._cursorTimer = null;
    this._awarenessTimer = null;
    this._remoteCursors = {};
    this._onRemoteCursor = null;
    this._connected = false;
    this._pendingUpdates = [];
    this._boundTextarea = null;
    this._boundFns = { input: null, mouseup: null, keyup: null };
  }

  SSYjs.prototype.init = function(spaceId, initialContent, userName) {
    var self = this;
    this.spaceId = spaceId;
    this.userName = userName || 'Anonymous';
    this.doc = new Y.Doc();
    this.ytext = this.doc.getText('content');

    if (initialContent && this.ytext.toString() === '') {
      this.doc.transact(function() {
        self.ytext.insert(0, initialContent);
      }, 'init');
    }

    this.doc.on('update', function(update, origin) {
      if (origin === 'remote' || origin === 'init') return;
      self._sendUpdate(update);
    });

    this.ytext.observe(function(evt, tr) {
      if (tr.origin === 'remote' || tr.origin === 'init') return;
      if (tr.origin && tr.origin.localEdit) return;
      if (self._onRemoteChange) {
        self._onRemoteChange(self.ytext.toString());
      }
    });

    if (typeof window.Y === 'undefined') {
      console.warn('SSYjs: Yjs library not loaded');
      return;
    }

    this.connectWS();
  };

  SSYjs.prototype.connectWS = function() {
    var self = this;
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) return;
    if (this._reconnectTimer) { clearTimeout(this._reconnectTimer); this._reconnectTimer = null; }

    var wsUrl = (window.WS_CONFIG && window.WS_CONFIG.url) || '';
    if (!wsUrl) {
      var p = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      wsUrl = p + '//' + window.location.host + '/ws/';
    }

    try {
      this.ws = new WebSocket(wsUrl);
    } catch(e) { return; }

    this.ws.onopen = function() {
      // Wait for the server's `subscribed` ack before treating the transport as
      // usable. Messages sent before group_add completes can be dropped by the
      // consumer because it intentionally only relays updates to joined groups.
      self._connected = false;
      try {
        self.ws.send(JSON.stringify({ action: 'subscribe', channel: 'studyspace.' + self.spaceId }));
      } catch(e) {}
      self.color = pickColor(self.userId || self.spaceId);
    };

    this.ws.onmessage = function(e) {
      try {
        var msg = JSON.parse(e.data);
        if (msg.type === 'ping') {
          // The Django Channels consumer uses an application-level heartbeat.
          // If we don't answer, the server closes the socket after ~30s, which
          // makes collaboration appear to work briefly and then only update
          // after refresh/HTTP save.
          try { self.ws.send(JSON.stringify({ action: 'pong' })); } catch(_) {}
          return;
        }
        if (msg.type === 'ready') {
          self.userId = msg.user_id;
          self.color = pickColor(self.userId || self.spaceId);
        } else if (msg.type === 'subscribed') {
          self._connected = true;
          if (self._pendingUpdates.length) {
            var pending = self._pendingUpdates.splice(0, self._pendingUpdates.length);
            pending.forEach(function(updateB64) {
              try {
                self.ws.send(JSON.stringify({
                  action: 'yjs_update',
                  spaceId: self.spaceId,
                  update: updateB64,
                }));
              } catch(_) {}
            });
          }
        } else if (msg.type === 'event') {
          self._handleEvent(msg);
        }
      } catch(err) {}
    }; 

    this.ws.onclose = function() {
      self._connected = false;
      if (self._reconnectTimer) return;
      self._reconnectTimer = setTimeout(function() {
        self._reconnectTimer = null;
        self.connectWS();
      }, 3000);
    };

    this.ws.onerror = function() {
      self._connected = false;
    };
  };

  SSYjs.prototype.disconnect = function() {
    if (this._reconnectTimer) { clearTimeout(this._reconnectTimer); this._reconnectTimer = null; }
    if (this._awarenessTimer) { clearTimeout(this._awarenessTimer); this._awarenessTimer = null; }
    if (this._cursorTimer) { clearTimeout(this._cursorTimer); this._cursorTimer = null; }
    if (this.ws) { try { this.ws.close(); } catch(e) {} this.ws = null; }
    this._connected = false;
    this._unbindTextarea();
    if (this.doc) { this.doc.destroy(); this.doc = null; }
    this.ytext = null;
  };

  SSYjs.prototype._handleEvent = function(msg) {
    var self = this;

    function processUpdate(data) {
      if (!data || data.senderId === self.userId) return;
      try {
        var update = base64ToArray(data.update);
        Y.applyUpdate(self.doc, update, 'remote');
      } catch(e) {}
    }

    function processAwareness(data, senderId) {
      var s = data.state || {};
      if (s.cursorStart === undefined || s.cursorEnd === undefined) {
        delete self._remoteCursors[senderId];
      } else {
        self._remoteCursors[senderId] = {
          start: s.cursorStart,
          end: s.cursorEnd,
          name: s.name || 'Someone',
          color: s.color || pickColor(senderId),
        };
      }
    }

    if (msg.event === 'yjs_update' && msg.data) {
      if (msg.batched && Array.isArray(msg.data)) {
        msg.data.forEach(processUpdate);
      } else {
        processUpdate(msg.data);
      }
      if (this._boundTextarea) {
        this._boundTextarea.value = this.ytext.toString();
      }
      if (this._onRemoteChange) {
        this._onRemoteChange(this.ytext.toString());
      }
    }
    if (msg.event === 'yjs_awareness' && msg.data) {
      if (msg.batched && Array.isArray(msg.data)) {
        msg.data.forEach(function(item) {
          if (item && item.senderId !== self.userId) {
            processAwareness(item, item.senderId);
          }
        });
      } else {
        if (msg.data.senderId !== this.userId) {
          processAwareness(msg.data, msg.data.senderId);
        }
      }
      if (this._onRemoteCursor) {
        this._onRemoteCursor(this._remoteCursors);
      }
    }
  };

  SSYjs.prototype._sendUpdate = function(update) {
    var updateB64 = arrayToBase64(update);
    if (!this._connected || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
      // Keep a small offline/early-subscribe buffer so fast first strokes or
      // short reconnects don't vanish. Yjs updates are idempotent; duplicates
      // are safe, but we cap the queue to avoid unbounded memory use.
      this._pendingUpdates.push(updateB64);
      if (this._pendingUpdates.length > 200) this._pendingUpdates.shift();
      return;
    }
    try {
      this.ws.send(JSON.stringify({
        action: 'yjs_update',
        spaceId: this.spaceId,
        update: updateB64,
      }));
    } catch(e) {
      this._pendingUpdates.push(updateB64);
      if (this._pendingUpdates.length > 200) this._pendingUpdates.shift();
    }
  };

  SSYjs.prototype._sendAwareness = function(start, end) {
    if (!this._connected || !this.ws) return;
    try {
      this.ws.send(JSON.stringify({
        action: 'yjs_awareness',
        spaceId: this.spaceId,
        state: {
          cursorStart: start,
          cursorEnd: end,
          name: this.userName,
          color: this.color,
        },
      }));
    } catch(e) {}
  };

  SSYjs.prototype.bindTextarea = function(textarea) {
    var self = this;
    if (!textarea) return;
    this._unbindTextarea();
    this._boundTextarea = textarea;

    var isFromYjs = false;

    var onInput = function() {
      if (isFromYjs) return;
      var oldVal = self.ytext.toString();
      var newVal = textarea.value;
      if (oldVal === newVal) return;

      var start = 0;
      while (start < oldVal.length && start < newVal.length && oldVal[start] === newVal[start]) start++;

      var oldEnd = oldVal.length;
      var newEnd = newVal.length;
      while (oldEnd > start && newEnd > start && oldVal[oldEnd - 1] === newVal[newEnd - 1]) {
        oldEnd--;
        newEnd--;
      }

      self.doc.transact(function() {
        if (oldEnd > start) self.ytext.delete(start, oldEnd - start);
        if (newEnd > start) self.ytext.insert(start, newVal.slice(start, newEnd));
      }, { localEdit: true });
    };

    var onMouseUp = function() {
      if (self._cursorTimer) clearTimeout(self._cursorTimer);
      self._cursorTimer = setTimeout(function() {
        self._cursorTimer = null;
        self._sendAwareness(textarea.selectionStart, textarea.selectionEnd);
      }, 80);
    };

    var onKeyUp = function() {
      if (self._cursorTimer) clearTimeout(self._cursorTimer);
      self._cursorTimer = setTimeout(function() {
        self._cursorTimer = null;
        self._sendAwareness(textarea.selectionStart, textarea.selectionEnd);
      }, 80);
    };

    textarea.addEventListener('input', onInput);
    textarea.addEventListener('mouseup', onMouseUp);
    textarea.addEventListener('keyup', onKeyUp);

    this._boundFns = { input: onInput, mouseup: onMouseUp, keyup: onKeyUp };
  };

  SSYjs.prototype._unbindTextarea = function() {
    if (this._boundTextarea && this._boundFns) {
      this._boundTextarea.removeEventListener('input', this._boundFns.input);
      this._boundTextarea.removeEventListener('mouseup', this._boundFns.mouseup);
      this._boundTextarea.removeEventListener('keyup', this._boundFns.keyup);
    }
    this._boundTextarea = null;
    this._boundFns = { input: null, mouseup: null, keyup: null };
  };

  SSYjs.prototype.getContent = function() {
    return this.ytext ? this.ytext.toString() : '';
  };

  SSYjs.prototype.getYtext = function() {
    return this.ytext;
  };

  SSYjs.prototype.getDoc = function() {
    return this.doc;
  };

  SSYjs.prototype.getArray = function(name) {
    return this.doc ? this.doc.getArray(name) : null;
  };

  SSYjs.prototype.getMap = function(name) {
    return this.doc ? this.doc.getMap(name) : null;
  };

  window.SSYjs = SSYjs;
})();
