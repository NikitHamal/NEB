/* Lazy workspace — transport helpers and shared formatting.
 *
 * Every network call the workspace makes lives here so the controller stays
 * about state and rendering. Exposed on window.LazyApi.
 */

(() => {
  'use strict';

  const config = () => window.LAZY_AGENT_CONFIG || {};

  const csrf = () =>
    config().csrfToken || document.querySelector('meta[name="csrf-token"]')?.content || '';

  async function request(url, options = {}) {
    const res = await fetch(url, {
      credentials: 'same-origin',
      ...options,
      headers: {
        'X-CSRFToken': csrf(),
        ...(options.headers || {}),
      },
    });
    const text = await res.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : {};
    } catch (err) {
      data = { ok: res.ok, raw: text };
    }
    if (!res.ok) {
      const error = new Error((data && data.error) || `Request failed (${res.status})`);
      error.status = res.status;
      error.payload = data;
      throw error;
    }
    return data;
  }

  function jsonPost(url, body) {
    return request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {}),
    });
  }

  const endpoints = () => config().endpoints || {};

  const api = {
    csrf,
    request,
    jsonPost,

    startRun({ goal, sessionId, modelKey, sources }) {
      return jsonPost(endpoints().run, {
        goal,
        title: goal.slice(0, 80),
        sessionId: sessionId || null,
        modelKey: modelKey || 'neby-pro',
        sources: sources || [],
      });
    },

    cancelRun(runId) {
      return jsonPost((endpoints().cancel || '').replace('__ID__', runId), {});
    },

    runDetail(runId) {
      return request((endpoints().detail || '').replace('__ID__', runId));
    },

    runFiles(runId) {
      return request((endpoints().files || '').replace('__ID__', runId));
    },

    sessionHistory(sessionId) {
      return request((endpoints().history || '').replace('__ID__', sessionId));
    },

    upload(file) {
      const form = new FormData();
      form.append('file', file);
      return request(endpoints().upload, { method: 'POST', body: form });
    },

    streamUrl(runId) {
      return (endpoints().stream || '').replace('__ID__', runId);
    },

    artifactUrl(runId, path) {
      return `${endpoints().artifact}${String(path || '')
        .split('/')
        .map(encodeURIComponent)
        .join('/')}`.replace('__RID__', runId);
    },
  };

  // ------------------------------------------------------------------
  // Formatting
  // ------------------------------------------------------------------

  function formatSize(bytes) {
    const n = Number(bytes) || 0;
    if (!n) return '—';
    const units = ['B', 'KB', 'MB', 'GB'];
    let value = n;
    let unit = 0;
    while (value >= 1024 && unit < units.length - 1) {
      value /= 1024;
      unit += 1;
    }
    return `${value < 10 ? value.toFixed(1) : Math.round(value)} ${units[unit]}`;
  }

  function formatClock(ms) {
    if (!ms) return '—';
    const d = new Date(Number(ms));
    if (Number.isNaN(d.getTime())) return '—';
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function formatDay(ms) {
    if (!ms) return '';
    const d = new Date(Number(ms));
    if (Number.isNaN(d.getTime())) return '';
    const today = new Date();
    if (d.toDateString() === today.toDateString()) {
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    const yesterday = new Date(today.getTime() - 86400000);
    if (d.toDateString() === yesterday.toDateString()) return 'Yesterday';
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
  }

  function formatDuration(ms) {
    const value = Number(ms) || 0;
    if (value < 1000) return `${Math.round(value)}ms`;
    const seconds = value / 1000;
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ${Math.round(seconds % 60)}s`;
  }

  /** Short human label for a tool's arguments, for the activity feed. */
  function summariseArgs(args) {
    if (!args || typeof args !== 'object') return '';
    const keys = ['name', 'query', 'url', 'path', 'brief', 'title', 'goal', 'command', 'code', 'html', 'spec'];
    const ordered = [
      ...keys.filter((k) => k in args),
      ...Object.keys(args).filter((k) => !keys.includes(k)),
    ].slice(0, 3);
    return ordered
      .map((k) => {
        let v = args[k];
        if (typeof v === 'string') {
          if (v.length > 60) v = `${v.slice(0, 60)}…`;
        } else if (v && typeof v === 'object') {
          const inner = Array.isArray(v) ? `${v.length} item${v.length === 1 ? '' : 's'}` : Object.keys(v).join(', ');
          v = `{${inner.slice(0, 50)}}`;
        } else {
          v = String(v);
        }
        return `${k}=${v}`;
      })
      .join('  ');
  }

  /** Human sentence for a tool call, so the feed reads like narration. */
  function toolLabel(name, args) {
    const a = args || {};
    switch (name) {
      case 'web_search': return `Searching the web for “${a.query || 'sources'}”`;
      case 'web_fetch': return `Reading ${hostOf(a.url)}`;
      case 'build_document': return 'Writing the document';
      case 'create_document': return 'Rendering the document to .docx';
      case 'create_pdf': return 'Rendering the document to .pdf';
      case 'create_slides': return 'Building the presentation';
      case 'create_spreadsheet': return 'Building the spreadsheet';
      case 'create_diagram': return 'Drawing a diagram';
      case 'create_chart': return 'Plotting a chart';
      case 'write_file': return `Writing ${a.path || 'a file'}`;
      case 'read_file': return `Reading ${a.path || 'a file'}`;
      case 'read_upload': return `Reading the attachment ${a.path || ''}`.trim();
      case 'list_files': return 'Checking the workspace';
      case 'run_python': return 'Running Python';
      case 'run_command': return `Running ${a.command || 'a command'}`;
      case 'zip_files': return 'Packaging the files';
      case 'pdf_tool': return 'Working on the PDF';
      case 'analyze_data': return `Analysing ${a.path || 'the data'}`;
      case 'humanize_text': return 'Humanising the wording';
      case 'translate_text': return `Translating to ${a.language || 'another language'}`;
      case 'spawn_subagents': return 'Researching in parallel';
      case 'save_preview': return 'Updating the preview';
      default: return name.replace(/_/g, ' ');
    }
  }

  function hostOf(url) {
    try {
      return new URL(String(url)).hostname.replace(/^www\./, '');
    } catch (err) {
      return String(url || 'a page').slice(0, 40);
    }
  }

  function extensionOf(name) {
    const parts = String(name || '').split('.');
    return parts.length > 1 ? `.${parts.pop().toLowerCase()}` : '';
  }

  function kindOf(name, mime) {
    const ext = extensionOf(name);
    if (['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'].includes(ext)) return 'image';
    if (ext === '.pdf') return 'pdf';
    if (['.docx', '.doc'].includes(ext)) return 'doc';
    if (['.pptx', '.ppt'].includes(ext)) return 'slides';
    if (['.xlsx', '.xls', '.csv'].includes(ext)) return 'sheet';
    if (ext === '.zip') return 'archive';
    if (['.html', '.htm'].includes(ext)) return 'html';
    if (['.py', '.js', '.ts', '.json', '.md', '.txt', '.css', '.xml', '.yml', '.yaml'].includes(ext)) return 'code';
    if (String(mime || '').startsWith('image/')) return 'image';
    return 'file';
  }

  api.fmt = { formatSize, formatClock, formatDay, formatDuration, summariseArgs, toolLabel, extensionOf, kindOf, hostOf };
  window.LazyApi = api;
})();
