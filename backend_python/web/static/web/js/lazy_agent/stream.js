/* Lazy workspace — SSE consumer.
 *
 * Wraps EventSource with a small state machine: it reconnects while a run is
 * still in flight, gives up cleanly once the server publishes a terminal
 * frame, and never leaves the UI stuck on "running".
 */

(() => {
  'use strict';

  const MAX_RETRIES = 3;
  const SILENCE_MS = 120000;

  class RunStream {
    /**
     * @param {string} runId
     * @param {(frame: object) => void} onFrame
     * @param {{ onOpen?: Function, onClose?: Function, onError?: Function }} hooks
     */
    constructor(runId, onFrame, hooks = {}) {
      this.runId = runId;
      this.onFrame = onFrame;
      this.hooks = hooks;
      this.source = null;
      this.retries = 0;
      this.closed = false;
      this.lastFrameAt = Date.now();
      this.seen = new Set();
      this._timer = null;
    }

    open() {
      if (this.closed) return;
      const url = window.LazyApi.streamUrl(this.runId);
      const es = new EventSource(url, { withCredentials: true });
      this.source = es;

      es.onopen = () => {
        this.retries = 0;
        this.lastFrameAt = Date.now();
        this.hooks.onOpen && this.hooks.onOpen();
      };

      es.onmessage = (event) => {
        this.lastFrameAt = Date.now();
        if (!event.data) return;
        let frame;
        try {
          frame = JSON.parse(event.data);
        } catch (err) {
          return;
        }
        if (!frame || !frame.type) return;
        this.onFrame(frame);
        if (frame.type === 'done' || frame.type === 'error') {
          this.close();
        }
      };

      es.onerror = () => {
        // EventSource reconnects on its own; only intervene when it is futile.
        if (this.closed) return;
        if (this.source !== es) return;
        this.retries += 1;
        if (this.retries > MAX_RETRIES) {
          this.close();
          this.hooks.onError && this.hooks.onError(new Error('Lost connection to the agent.'));
        }
      };

      this._timer = setInterval(() => this._watchdog(), 15000);
    }

    /** Guard against a server that stops sending without closing the socket. */
    _watchdog() {
      if (this.closed) return;
      if (Date.now() - this.lastFrameAt > SILENCE_MS) {
        this.close();
        this.hooks.onError && this.hooks.onError(new Error('The agent stopped responding.'));
      }
    }

    close() {
      if (this.closed) return;
      this.closed = true;
      if (this._timer) clearInterval(this._timer);
      if (this.source) {
        try {
          this.source.close();
        } catch (err) { /* noop */ }
        this.source = null;
      }
      this.hooks.onClose && this.hooks.onClose();
    }
  }

  window.LazyStream = { RunStream };
})();
