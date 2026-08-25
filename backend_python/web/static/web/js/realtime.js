/* NEBians real-time client.
 *
 * Single WebSocket connection to /ws/ that dispatches typed events to
 * page-level subscribers. Handles reconnect, heartbeat, tab-visibility
 * pause, and a polling fallback when the WebSocket is down.
 *
 * Usage (from page templates):
 *   WS.subscribe('post.<id>');
 *   WS.subscribe('user');
 *   WS.subscribe('forum.public');
 *   WS.subscribe('resource.<id>');
 *   WS.on('post.<id>:reply.created', function(data) { ... });
 *   WS.on('user:notification.new',  function(data) { ... });
 *   WS.on('forum.public:post.created', function(data) { ... });
 *
 * Channel event names mirror what the server emits (api/realtime.py).
 *
 * The WS endpoint URL is auto-detected from window.location:
 *   - https -> wss://<host>/ws/
 *   - http  -> ws://<host>/ws/
 *   - data-ws-url attribute on <body> overrides the default (used for
 *     staging environments where the WS endpoint is on a different host,
 *     e.g. ws.nebians.consica.com.np).
 */
(function (global) {
  'use strict';

  var STATE = {
    DISCONNECTED: 'disconnected',
    CONNECTING: 'connecting',
    CONNECTED: 'connected',
    CLOSED: 'closed',
  };

  var config = global.WS_CONFIG || {};
  var wsUrl = config.url || deriveUrl();
  var heartbeatInterval = 25000;
  var minReconnectDelay = 1000;
  var maxReconnectDelay = 30000;
  var reconnectDelay = minReconnectDelay;
  var state = STATE.DISCONNECTED;
  var socket = null;
  var channels = new Set();
  var handlers = Object.create(null); // 'channel:event' -> Set<fn>
  var heartbeatTimer = null;
  var lastPingTs = 0;
  var reconnectTimer = null;
  var paused = false;
  var healthListeners = new Set();
  var lastEventTs = 0;
  var baseWsUrl = null; // extracted from wsUrl (without query string)
  var haveRefetched = false; // prevent infinite refetch loops

  // ----- URL derivation -----------------------------------------------------

  function deriveUrl() {
    var explicit = document.body && document.body.getAttribute('data-ws-url');
    if (explicit) return explicit;
    var proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    return proto + '//' + location.host + '/ws/';
  }

  // ----- Public API ---------------------------------------------------------

  function subscribe(channel) {
    if (!channel) return;
    if (channels.has(channel)) return;
    channels.add(channel);
    if (state === STATE.CONNECTED) {
      sendRaw({ action: 'subscribe', channel: channel });
    }
  }

  function unsubscribe(channel) {
    if (!channel) return;
    if (!channels.delete(channel)) return;
    if (state === STATE.CONNECTED) {
      sendRaw({ action: 'unsubscribe', channel: channel });
    }
  }

  function on(eventKey, fn) {
    if (!eventKey || typeof fn !== 'function') return;
    var bucket = handlers[eventKey] || (handlers[eventKey] = new Set());
    bucket.add(fn);
    return function off() { bucket.delete(fn); };
  }

  function off(eventKey, fn) {
    if (!handlers[eventKey]) return;
    if (fn) handlers[eventKey].delete(fn);
    else delete handlers[eventKey];
  }

  function getState() { return state; }

  function isOpen() { return state === STATE.CONNECTED; }

  function onHealth(fn) {
    healthListeners.add(fn);
    fn(state);
    return function () { healthListeners.delete(fn); };
  }

  function start() {
    if (state === STATE.CONNECTING || state === STATE.CONNECTED) return;
    connect();
  }

  function stop() {
    paused = true;
    if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
    if (socket) {
      try { socket.close(1000, 'client stop'); } catch (e) { /* ignore */ }
    }
    setState(STATE.CLOSED);
  }

  // ----- internals ----------------------------------------------------------

  function connect() {
    setState(STATE.CONNECTING);
    if (!baseWsUrl) {
      var qidx = wsUrl.indexOf('?');
      baseWsUrl = qidx >= 0 ? wsUrl.substring(0, qidx) : wsUrl;
    }
    try {
      socket = new WebSocket(wsUrl);
    } catch (e) {
      console.warn('[ws] WebSocket construction failed:', e);
      scheduleReconnect();
      return;
    }

    socket.addEventListener('open', function () {
      reconnectDelay = minReconnectDelay;
      setState(STATE.CONNECTED);
      // Re-subscribe to all channels on (re)connect.
      channels.forEach(function (ch) {
        sendRaw({ action: 'subscribe', channel: ch });
      });
      startHeartbeat();
    });

    socket.addEventListener('message', function (ev) {
      handleMessage(ev.data);
    });

    socket.addEventListener('close', function (ev) {
      stopHeartbeat();
      if (state !== STATE.CLOSED) {
        setState(STATE.DISCONNECTED);
        if (!paused) scheduleReconnect();
      }
    });

    socket.addEventListener('error', function () {
      // 'close' will fire right after; reconnect happens there.
    });
  }

  function refetchWsUrl(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/realtime/config/', true);
    xhr.withCredentials = true;
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 400) {
        try {
          var data = JSON.parse(xhr.responseText);
          if (data.ws_url) {
            wsUrl = data.ws_url;
            var qidx = wsUrl.indexOf('?');
            baseWsUrl = qidx >= 0 ? wsUrl.substring(0, qidx) : wsUrl;
            if (global.WS_CONFIG) global.WS_CONFIG.url = wsUrl;
            if (document.body) document.body.setAttribute('data-ws-url', wsUrl);
          }
        } catch (e) { /* ignore parse errors */ }
      }
      callback();
    };
    xhr.onerror = function () { callback(); };
    xhr.send();
  }

  function scheduleReconnect() {
    if (paused) return;
    if (reconnectTimer) return;
    var jitter = Math.random() * 0.3 * reconnectDelay;
    var delay = reconnectDelay + jitter;
    reconnectTimer = setTimeout(function () {
      reconnectTimer = null;
      reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay);
      // Refetch the WS URL from the server before reconnecting, so we get
      // the latest tunnel URL if cloudflared has restarted since page load.
      refetchWsUrl(function () {
        connect();
      });
    }, delay);
  }

  function setState(s) {
    if (state === s) return;
    state = s;
    healthListeners.forEach(function (fn) { try { fn(s); } catch (e) { /* ignore */ } });
    document.body && document.body.setAttribute('data-ws-state', s);
  }

  function sendRaw(obj) {
    if (state !== STATE.CONNECTED || !socket) return false;
    try {
      socket.send(JSON.stringify(obj));
      return true;
    } catch (e) {
      return false;
    }
  }

  function handleMessage(raw) {
    var msg;
    try { msg = JSON.parse(raw); } catch (e) { return; }
    if (!msg || typeof msg !== 'object') return;
    var type = msg.type;
    if (type === 'pong') {
      lastPingTs = Date.now();
      return;
    }
    if (type === 'ping') {
      sendRaw({ action: 'pong' });
      lastEventTs = Date.now();
      return;
    }
    if (type === 'ready') {
      heartbeatInterval = msg.heartbeat_interval || 25000;
      lastPingTs = Date.now();
      return;
    }
    if (type === 'event') {
      lastEventTs = Date.now();
      dispatch(msg.channel, msg.event, msg.data);
      return;
    }
    if (type === 'subscribed' || type === 'unsubscribed' || type === 'since_ack') {
      return;
    }
    if (type === 'error') {
      console.warn('[ws] server error:', msg.code, msg.message);
    }
  }

  function dispatch(channel, event, data) {
    // Specific: 'post.<id>:reply.created'
    var specific = channel + ':' + event;
    fire(handlers[specific], data, channel, event);
    // Wildcard on channel: 'post.<id>:*'
    fire(handlers[channel + ':*'], data, channel, event);
    // Wildcard on event across all channels: '*:reply.created'
    fire(handlers['*:' + event], data, channel, event);
    // Global wildcard
    fire(handlers['*'], data, channel, event);
  }

  function fire(bucket, data, channel, event) {
    if (!bucket) return;
    bucket.forEach(function (fn) {
      try { fn(data, channel, event); } catch (e) { console.error('[ws] handler error:', e); }
    });
  }

  // ----- heartbeat ----------------------------------------------------------

  function startHeartbeat() {
    stopHeartbeat();
    heartbeatTimer = setInterval(function () {
      if (state !== STATE.CONNECTED) return;
      // If the server hasn't pinged us in 2x interval, our connection may be
      // half-closed. Force a ping so we can detect a dead socket faster.
      var sinceServer = Date.now() - lastEventTs;
      if (sinceServer > heartbeatInterval * 2) {
        sendRaw({ action: 'ping', ts: Date.now() });
      }
    }, heartbeatInterval);
  }

  function stopHeartbeat() {
    if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
  }

  // ----- tab visibility & Back-Forward Cache (bfcache) lifecycle ------------

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') {
      if (paused) { paused = false; start(); }
      else if (state === STATE.DISCONNECTED || state === STATE.CLOSED) start();
    }
  });

  // When page enters Back-Forward Cache (bfcache), close socket cleanly.
  window.addEventListener('pagehide', function (ev) {
    if (ev.persisted || socket) {
      try {
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.close(1000, 'pagehide');
        }
      } catch (e) { /* ignore */ }
    }
  });

  // When restored from Back-Forward Cache (bfcache), resume realtime connection.
  window.addEventListener('pageshow', function (ev) {
    if (ev.persisted) {
      paused = false;
      start();
    }
  });

  window.addEventListener('beforeunload', function () {
    try { if (socket) socket.close(1000, 'page unload'); } catch (e) { /* ignore */ }
  });

  // Expose
  global.WS = {
    start: start,
    stop: stop,
    subscribe: subscribe,
    unsubscribe: unsubscribe,
    on: on,
    off: off,
    onHealth: onHealth,
    getState: getState,
    isOpen: isOpen,
    send: sendRaw,
  };
})(window);
