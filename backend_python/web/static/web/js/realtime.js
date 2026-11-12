/* NEBians realtime client.
 *
 * Transport: Server-Sent Events straight to Ably (no SDK, no tunnel, and this
 * server holds no socket). The server only hands out a short-lived subscribe
 * token from /api/realtime/config/ and publishes events over HTTPS.
 *
 *   WS.subscribe('forum.public');  WS.subscribe('post.<id>');  WS.subscribe('user');
 *   WS.on('post.<id>:reply.created', fn);  WS.on('user:notification.new', fn);
 *
 * What keeps it light:
 *   - no channels subscribed -> no connection and no request at all
 *   - subscribe calls made in the same tick share ONE connection
 *   - a tab that is hidden for 30s drops its stream (Ably free plan counts
 *     concurrent connections) and resumes, with lastEventId, when it is back
 *   - token renewed at ~80% of its life, reconnect backoff with jitter
 *
 * `WS_CONFIG.url` / WS_PUBLIC_URL still selects the old self-hosted WebSocket.
 */
(function (global) {
  'use strict';

  var STATE = { DISCONNECTED: 'disconnected', CONNECTING: 'connecting', CONNECTED: 'connected', CLOSED: 'closed' };
  var HIDDEN_GRACE = 30000;
  var RESYNC_AFTER = 110000;
  var MIN_DELAY = 1500;
  var MAX_DELAY = 60000;

  var state = STATE.CLOSED;
  var channels = new Set();
  var handlers = Object.create(null);
  var healthListeners = new Set();
  var cfg = null;
  var es = null;
  var ws = null;
  var lastEventId = '';
  var lastSeen = 0;
  var delay = MIN_DELAY;
  var timers = { connect: null, renew: null, hidden: null, reopen: null };
  var starting = false;
  var shard = null;      // Ably app index in use (several free apps share the load)
  var openFails = 0;     // errors since the last successful open
  var wantOpen = false;

  function now() { return Date.now(); }
  function clearTimer(name) { if (timers[name]) { clearTimeout(timers[name]); timers[name] = null; } }

  function setState(s) {
    if (state === s) return;
    state = s;
    if (document.body) document.body.setAttribute('data-ws-state', s);
    healthListeners.forEach(function (fn) { try { fn(s); } catch (e) { /* ignore */ } });
  }

  // ----- public API ----------------------------------------------------------

  function subscribe(channel) {
    if (!channel || channels.has(channel)) return;
    channels.add(channel);
    wantOpen = true;
    if (cfg && cfg.transport === 'ws') {
      if (ws && ws.readyState === 1) sendRaw({ action: 'subscribe', channel: channel });
      return;
    }
    scheduleReopen();
  }

  function unsubscribe(channel) {
    if (!channel || !channels.delete(channel)) return;
    if (cfg && cfg.transport === 'ws') {
      if (ws && ws.readyState === 1) sendRaw({ action: 'unsubscribe', channel: channel });
      return;
    }
    if (!channels.size) closeStream(); else scheduleReopen();
  }

  function on(key, fn) {
    if (!key || typeof fn !== 'function') return function () {};
    var bucket = handlers[key] || (handlers[key] = new Set());
    bucket.add(fn);
    return function () { bucket.delete(fn); };
  }

  function off(key, fn) {
    if (!handlers[key]) return;
    if (fn) handlers[key].delete(fn); else delete handlers[key];
  }

  function onHealth(fn) {
    healthListeners.add(fn);
    try { fn(state); } catch (e) { /* ignore */ }
    return function () { healthListeners.delete(fn); };
  }

  function isOpen() { return state === STATE.CONNECTED; }
  function getState() { return state; }

  function start() {
    wantOpen = true;
    if (state === STATE.CONNECTING || state === STATE.CONNECTED || starting) return;
    boot();
  }

  function stop() {
    wantOpen = false;
    clearTimer('connect'); clearTimer('renew'); clearTimer('reopen'); clearTimer('hidden');
    closeStream();
    setState(STATE.CLOSED);
  }

  // ----- config + connect ----------------------------------------------------

  function fetchConfig(done) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/realtime/config/' + (shard === null ? '' : '?shard=' + shard), true);
    xhr.withCredentials = true;
    xhr.onload = function () {
      var data = null;
      if (xhr.status >= 200 && xhr.status < 300) {
        try { data = JSON.parse(xhr.responseText); } catch (e) { data = null; }
      }
      done(data, xhr.status);
    };
    xhr.onerror = function () { done(null, 0); };
    xhr.send();
  }

  function boot() {
    if (!wantOpen || !channels.size) return;
    starting = true;
    setState(STATE.CONNECTING);
    var explicit = (global.WS_CONFIG && global.WS_CONFIG.url) || '';
    fetchConfig(function (data, status) {
      starting = false;
      if (!wantOpen) return;
      if (!data || (data.transport !== 'ably-sse' && data.transport !== 'ws' && !explicit)) {
        // Nothing to connect to (or server unreachable): stay quiet, look again later.
        setState(STATE.DISCONNECTED);
        retry(status === 429 ? 120000 : 300000);
        return;
      }
      cfg = data;
      if (typeof data.shard === 'number') shard = data.shard;
      if (data.transport !== 'ably-sse') {
        cfg = { transport: 'ws', url: data.ws_url || explicit };
        openWebSocket();
        return;
      }
      openStream();
    });
  }

  function retry(ms) {
    clearTimer('connect');
    var wait = ms || Math.min(delay, MAX_DELAY);
    wait += Math.random() * wait * 0.3;
    timers.connect = setTimeout(function () {
      timers.connect = null;
      delay = Math.min(delay * 2, MAX_DELAY);
      boot();
    }, wait);
  }

  function ablyChannelList() {
    var list = [];
    channels.forEach(function (ch) {
      if (ch === 'user') { if (cfg.user_channel) list.push(cfg.user_channel); return; }
      if (ch.indexOf('user.') === 0 && ch !== cfg.user_channel) return; // private: not ours
      if (/^(forum\.public|post\.|resource\.|resource_request\.|user\.)/.test(ch)) list.push(ch);
    });
    return list;
  }

  function openStream() {
    closeStream(true);
    var list = ablyChannelList();
    if (!list.length || !cfg || !cfg.token || typeof EventSource === 'undefined') {
      setState(STATE.DISCONNECTED);
      return;
    }
    var url = cfg.sse_url + '?v=1.2&accessToken=' + encodeURIComponent(cfg.token) +
      '&channels=' + list.map(encodeURIComponent).join(',') +
      (lastEventId ? '&lastEvent=' + encodeURIComponent(lastEventId) : '');
    setState(STATE.CONNECTING);
    var source = new EventSource(url);
    es = source;
    source.onopen = function () {
      if (es !== source) return;
      if (lastSeen && now() - lastSeen > RESYNC_AFTER) {
        try { global.dispatchEvent(new CustomEvent('neb:realtime-resync')); } catch (e) { /* ignore */ }
      }
      lastSeen = now();
      delay = MIN_DELAY;
      openFails = 0;
      setState(STATE.CONNECTED);
    };
    source.onmessage = function (ev) {
      if (es !== source) return;
      lastSeen = now();
      if (ev.lastEventId) lastEventId = ev.lastEventId;
      handleAbly(ev.data);
    };
    source.onerror = function () {
      if (es !== source) return;
      // EventSource retries on its own for network blips; a CLOSED stream is an
      // auth or quota failure, so fetch a fresh token and start over.
      openFails += 1;
      if (source.readyState === 2) {
        source.close();
        es = null;
        setState(STATE.DISCONNECTED);
        rotateShard();
        if (wantOpen && !document.hidden) retry();
      } else if (openFails >= 3 && cfg && cfg.shards > 1) {
        // This Ably app keeps failing (quota, outage): move to the next one.
        source.close();
        es = null;
        rotateShard();
        if (wantOpen && !document.hidden) retry(MIN_DELAY); else setState(STATE.DISCONNECTED);
      } else {
        setState(STATE.CONNECTING);
      }
    };
    clearTimer('renew');
    var life = (cfg.expires_in || 3600) * 800;
    timers.renew = setTimeout(renewToken, life);
  }

  function rotateShard() {
    if (!cfg || !(cfg.shards > 1)) return;
    shard = ((typeof cfg.shard === 'number' ? cfg.shard : 0) + 1) % cfg.shards;
    openFails = 0;
    cfg = null; // forces a fresh token for the other app
  }

  function renewToken() {
    timers.renew = null;
    if (!wantOpen || !es) return;
    fetchConfig(function (data) {
      if (data && data.token) { cfg = data; openStream(); }
      else retry(30000);
    });
  }

  function closeStream(keepState) {
    clearTimer('renew');
    if (es) { try { es.close(); } catch (e) { /* ignore */ } es = null; }
    if (ws) { try { ws.close(1000, 'client'); } catch (e) { /* ignore */ } ws = null; }
    if (!keepState && state !== STATE.CLOSED) setState(STATE.DISCONNECTED);
  }

  function scheduleReopen() {
    clearTimer('reopen');
    timers.reopen = setTimeout(function () {
      timers.reopen = null;
      if (!wantOpen || !channels.size || document.hidden) return;
      if (!cfg) { if (!starting) boot(); return; }
      openStream();
    }, 120);
  }

  // ----- Ably message -> page event -------------------------------------------

  function handleAbly(raw) {
    var msg;
    try { msg = JSON.parse(raw); } catch (e) { return; }
    if (!msg || typeof msg !== 'object') return;
    var items = Array.isArray(msg) ? msg : [msg];
    items.forEach(function (m) {
      if (!m || !m.name || !m.channel) return;
      var data = m.data;
      if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { /* keep string */ } }
      var channel = m.channel;
      if (cfg && cfg.user_channel && channel === cfg.user_channel) {
        dispatch('user', m.name, data);
        if (channels.has(channel)) dispatch(channel, m.name, data);
      } else {
        dispatch(channel, m.name, data);
      }
    });
  }

  function dispatch(channel, event, data) {
    fire(handlers[channel + ':' + event], data, channel, event);
    fire(handlers[channel + ':*'], data, channel, event);
    fire(handlers['*:' + event], data, channel, event);
    fire(handlers['*'], data, channel, event);
  }

  function fire(bucket, data, channel, event) {
    if (!bucket) return;
    bucket.forEach(function (fn) {
      try { fn(data, channel, event); } catch (e) { console.error('[realtime] handler error:', e); }
    });
  }

  // ----- self-hosted WebSocket (only when WS_PUBLIC_URL is configured) --------

  function sendRaw(obj) {
    if (!ws || ws.readyState !== 1) return false;
    try { ws.send(JSON.stringify(obj)); return true; } catch (e) { return false; }
  }

  function openWebSocket() {
    closeStream(true);
    if (!cfg || !cfg.url || typeof WebSocket === 'undefined') { setState(STATE.DISCONNECTED); return; }
    var sock;
    try { sock = new WebSocket(cfg.url); } catch (e) { setState(STATE.DISCONNECTED); retry(); return; }
    ws = sock;
    sock.onopen = function () {
      delay = MIN_DELAY;
      setState(STATE.CONNECTED);
      channels.forEach(function (ch) { sendRaw({ action: 'subscribe', channel: ch }); });
    };
    sock.onmessage = function (ev) {
      var msg;
      try { msg = JSON.parse(ev.data); } catch (e) { return; }
      if (!msg) return;
      if (msg.type === 'ping') sendRaw({ action: 'pong' });
      else if (msg.type === 'event') dispatch(msg.channel, msg.event, msg.data);
    };
    sock.onclose = function () {
      if (ws !== sock) return;
      ws = null;
      setState(STATE.DISCONNECTED);
      if (wantOpen && !document.hidden) retry();
    };
  }

  // ----- tab lifecycle ---------------------------------------------------------

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      clearTimer('hidden');
      timers.hidden = setTimeout(function () {
        timers.hidden = null;
        if (document.hidden) { clearTimer('connect'); closeStream(); }
      }, HIDDEN_GRACE);
      return;
    }
    clearTimer('hidden');
    if (wantOpen && channels.size && state !== STATE.CONNECTED && state !== STATE.CONNECTING) {
      if (cfg) openStream(); else boot();
    }
  });

  global.addEventListener('pagehide', function () { clearTimer('connect'); closeStream(); });
  global.addEventListener('pageshow', function (ev) {
    if (ev.persisted && wantOpen && channels.size) { cfg ? openStream() : boot(); }
  });

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
