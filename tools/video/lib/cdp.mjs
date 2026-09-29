import { EventEmitter } from 'node:events';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export class Connection extends EventEmitter {
  constructor(wsUrl) {
    super();
    this.wsUrl = wsUrl;
    this.seq = 0;
    this.pending = new Map();
    this.closed = false;
    this.ws = null;
  }

  open() {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(this.wsUrl);
      this.ws = ws;
      ws.addEventListener('open', () => resolve(this), { once: true });
      ws.addEventListener('error', () => reject(new Error(`cannot open ${this.wsUrl}`)), { once: true });
      ws.addEventListener('message', (event) => this.dispatch(event.data));
      ws.addEventListener('close', () => this.shutdown(new Error('devtools socket closed')));
    });
  }

  dispatch(data) {
    const message = JSON.parse(data);
    if (message.id !== undefined) {
      const entry = this.pending.get(message.id);
      if (!entry) return;
      this.pending.delete(message.id);
      clearTimeout(entry.timer);
      if (message.error) entry.reject(new Error(`${entry.method} failed: ${message.error.message}`));
      else entry.resolve(message.result);
      return;
    }
    const key = message.sessionId ? `${message.sessionId}:${message.method}` : message.method;
    this.emit(key, message.params);
  }

  send(method, params = {}, sessionId = undefined, timeout = 60_000) {
    if (this.closed) return Promise.reject(new Error('devtools connection closed'));
    const id = ++this.seq;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`${method} timed out after ${timeout}ms`));
      }, timeout);
      this.pending.set(id, { resolve, reject, method, timer });
      const payload = { id, method, params };
      if (sessionId) payload.sessionId = sessionId;
      this.ws.send(JSON.stringify(payload));
    });
  }

  shutdown(error) {
    if (this.closed) return;
    this.closed = true;
    for (const entry of this.pending.values()) {
      clearTimeout(entry.timer);
      entry.reject(error);
    }
    this.pending.clear();
    this.emit('close');
  }

  close() {
    try {
      this.ws?.close();
    } catch {
      this.shutdown(new Error('closed'));
    }
    this.shutdown(new Error('closed'));
  }
}

export class Page {
  constructor(connection, sessionId, targetId) {
    this.connection = connection;
    this.sessionId = sessionId;
    this.targetId = targetId;
    this.logs = [];
    this.errors = [];
    const on = (event, handler) => connection.on(`${sessionId}:${event}`, handler);
    on('Runtime.consoleAPICalled', (p) => {
      const text = p.args.map((a) => a.value ?? a.description ?? a.type).join(' ');
      this.logs.push({ type: p.type, text });
      if (p.type === 'error') this.errors.push(text);
    });
    on('Runtime.exceptionThrown', (p) => {
      const d = p.exceptionDetails;
      this.errors.push(`${d.exception?.description ?? d.text} (${d.url ?? ''}:${d.lineNumber ?? '?'})`);
    });
    on('Log.entryAdded', (p) => {
      if (p.entry.level === 'error') this.errors.push(`${p.entry.text} ${p.entry.url ?? ''}`.trim());
    });
  }

  send(method, params, timeout) {
    return this.connection.send(method, params, this.sessionId, timeout);
  }

  waitFor(event, timeout = 60_000) {
    return new Promise((resolve, reject) => {
      const key = `${this.sessionId}:${event}`;
      const handler = (params) => {
        clearTimeout(timer);
        resolve(params);
      };
      const timer = setTimeout(() => {
        this.connection.off(key, handler);
        reject(new Error(`timed out waiting for ${event}`));
      }, timeout);
      this.connection.once(key, handler);
    });
  }

  async setViewport({ width, height, deviceScaleFactor = 1, mobile = false }) {
    await this.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor, mobile });
  }

  async goto(url, { timeout = 60_000 } = {}) {
    const loaded = this.waitFor('Page.loadEventFired', timeout);
    const nav = await this.send('Page.navigate', { url }, timeout);
    if (nav.errorText) throw new Error(`navigation to ${url} failed: ${nav.errorText}`);
    await loaded;
  }

  async idle({ quiet = 900, timeout = 30_000 } = {}) {
    let inflight = 0;
    let last = Date.now();
    const bump = () => {
      last = Date.now();
    };
    const start = () => {
      inflight += 1;
      bump();
    };
    const finish = () => {
      inflight = Math.max(0, inflight - 1);
      bump();
    };
    const s = this.sessionId;
    const c = this.connection;
    c.on(`${s}:Network.requestWillBeSent`, start);
    c.on(`${s}:Network.loadingFinished`, finish);
    c.on(`${s}:Network.loadingFailed`, finish);
    const deadline = Date.now() + timeout;
    try {
      while (Date.now() < deadline) {
        if (inflight <= 0 && Date.now() - last >= quiet) return true;
        await sleep(100);
      }
      return false;
    } finally {
      c.off(`${s}:Network.requestWillBeSent`, start);
      c.off(`${s}:Network.loadingFinished`, finish);
      c.off(`${s}:Network.loadingFailed`, finish);
    }
  }

  async evaluate(expression, { awaitPromise = true, timeout = 120_000 } = {}) {
    const result = await this.send(
      'Runtime.evaluate',
      { expression, awaitPromise, returnByValue: true, userGesture: true },
      timeout,
    );
    if (result.exceptionDetails) {
      const d = result.exceptionDetails;
      throw new Error(d.exception?.description ?? d.text ?? 'evaluation failed');
    }
    return result.result.value;
  }

  async screenshot({ format = 'png', quality = 92, clip = undefined, fast = false, beyond = false } = {}) {
    const params = { format, fromSurface: true, captureBeyondViewport: beyond };
    if (format === 'jpeg') params.quality = quality;
    if (clip) params.clip = { scale: 1, ...clip };
    if (fast) params.optimizeForSpeed = true;
    const { data } = await this.send('Page.captureScreenshot', params);
    return Buffer.from(data, 'base64');
  }

  async close() {
    try {
      await this.connection.send('Target.closeTarget', { targetId: this.targetId }, undefined, 5_000);
    } catch {
      return;
    }
  }
}

export { sleep };
