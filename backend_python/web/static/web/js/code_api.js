(function () {
  'use strict';

  function NebyCodeAPI(boot) {
    this.csrf = (boot || {}).csrf || '';
  }

  NebyCodeAPI.prototype.request = function (method, url, body) {
    var options = {
      method: method,
      credentials: 'same-origin',
      headers: { 'X-CSRFToken': this.csrf },
    };
    if (body !== undefined) {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(body);
    }
    return fetch(url, options).then(function (response) {
      return response.json().catch(function () { return {}; }).then(function (data) {
        if (!response.ok) {
          var error = new Error(data.error || response.statusText || 'Request failed');
          error.code = data.code || '';
          error.status = response.status;
          error.data = data.data;
          throw error;
        }
        return data;
      });
    });
  };

  NebyCodeAPI.prototype.sessions = function () {
    return this.request('GET', '/ajax/code/sessions/');
  };

  NebyCodeAPI.prototype.createSession = function (values) {
    return this.request('POST', '/ajax/code/sessions/create/', values || {});
  };

  NebyCodeAPI.prototype.session = function (id) {
    return this.request('GET', '/ajax/code/sessions/' + encodeURIComponent(id) + '/detail/');
  };

  NebyCodeAPI.prototype.updateSession = function (id, values) {
    return this.request('POST', '/ajax/code/sessions/' + encodeURIComponent(id) + '/update/', values || {});
  };

  NebyCodeAPI.prototype.send = function (id, values) {
    return this.request('POST', '/ajax/code/sessions/' + encodeURIComponent(id) + '/send/', values || {});
  };

  NebyCodeAPI.prototype.cancel = function (id) {
    return this.request('POST', '/ajax/code/sessions/' + encodeURIComponent(id) + '/cancel/', {});
  };

  NebyCodeAPI.prototype.deleteSession = function (id) {
    return this.request('POST', '/ajax/code/sessions/' + encodeURIComponent(id) + '/delete/', {});
  };

  NebyCodeAPI.prototype.status = function () {
    return this.request('GET', '/ajax/code/status/');
  };

  NebyCodeAPI.prototype.connection = function () {
    return this.request('GET', '/ajax/code/token/');
  };

  NebyCodeAPI.prototype.fs = function (op, values) {
    var body = Object.assign({ op: op }, values || {});
    return this.request('POST', '/ajax/code/fs/', body).then(function (result) { return result.data; });
  };

  NebyCodeAPI.prototype.fsList = function (path) {
    return this.fs('list', { path: path || '.' });
  };

  NebyCodeAPI.prototype.fsTree = function (depth) {
    return this.fs('tree', { path: '.', depth: depth || 4 });
  };

  NebyCodeAPI.prototype.fsRead = function (path) {
    return this.fs('read', { path: path });
  };

  NebyCodeAPI.prototype.fsWrite = function (path, content) {
    return this.fs('write', { path: path, content: content });
  };

  NebyCodeAPI.prototype.fsMkdir = function (path) {
    return this.fs('mkdir', { path: path });
  };

  NebyCodeAPI.prototype.fsDelete = function (path, recursive) {
    return this.fs('delete', { path: path, recursive: !!recursive });
  };

  NebyCodeAPI.prototype.fsMove = function (source, destination) {
    return this.fs('move', { source: source, destination: destination });
  };

  NebyCodeAPI.prototype.git = function (op, values) {
    var body = Object.assign({ op: op }, values || {});
    return this.request('POST', '/ajax/code/git/', body).then(function (result) { return result.data; });
  };

  NebyCodeAPI.prototype.term = function (sessionId, command, timeout) {
    return this.request('POST', '/ajax/code/term/', {
      session_id: sessionId || '',
      command: command,
      timeout_sec: timeout || 900,
    });
  };

  window.NebyCodeAPI = NebyCodeAPI;
})();
