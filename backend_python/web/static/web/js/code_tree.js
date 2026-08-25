(function (global) {
  'use strict';

  var THEMES = ['theme-orange', 'theme-blue', 'theme-purple', 'theme-emerald', 'theme-rose', 'theme-cyan', 'theme-amber'];

  function resolveTheme(index, label) {
    if (typeof index === 'number') {
      return THEMES[index % THEMES.length];
    }
    var hash = 0;
    var str = String(label || '');
    for (var i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return THEMES[Math.abs(hash) % THEMES.length];
  }

  function resolveIcon(session) {
    var name = String(session.name || '').toLowerCase();
    var status = session.status || 'idle';
    if (status === 'running' || status === 'queued') return 'progress_activity';
    if (status === 'error') return 'error';
    if (name.indexOf('api') >= 0 || name.indexOf('send') >= 0) return 'near_me';
    if (name.indexOf('react') >= 0 || name.indexOf('component') >= 0 || name.indexOf('atom') >= 0) return 'token';
    if (name.indexOf('hook') >= 0 || name.indexOf('event') >= 0 || name.indexOf('stream') >= 0) return 'hub';
    if (name.indexOf('metric') >= 0 || name.indexOf('chart') >= 0 || name.indexOf('stat') >= 0) return 'trending_up';
    if (name.indexOf('click') >= 0 || name.indexOf('engage') >= 0 || name.indexOf('touch') >= 0) return 'touch_app';
    if (name.indexOf('bounce') >= 0 || name.indexOf('diagnos') >= 0 || name.indexOf('warn') >= 0) return 'warning';
    if (name.indexOf('ai') >= 0 || name.indexOf('template') >= 0 || name.indexOf('prompt') >= 0) return 'auto_awesome';
    if (name.indexOf('edit') >= 0 || name.indexOf('code') >= 0 || name.indexOf('editor') >= 0) return 'terminal';
    if (name.indexOf('version') >= 0 || name.indexOf('history') >= 0 || name.indexOf('time') >= 0) return 'history';
    if (name.indexOf('test') >= 0 || name.indexOf('check') >= 0) return 'verified';
    if (name.indexOf('fix') >= 0 || name.indexOf('bug') >= 0) return 'build';
    if (name.indexOf('doc') >= 0 || name.indexOf('readme') >= 0) return 'description';
    if (name.indexOf('db') >= 0 || name.indexOf('model') >= 0 || name.indexOf('migrat') >= 0) return 'database';
    return 'terminal';
  }

  function esc(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function NebyWorkspaceTree(options) {
    this.options = Object.assign({
      mount: null,
      workspaces: [],
      activeWorkspaceId: '',
      activeSessionId: '',
      filter: '',
      onSelectSession: function () {},
      onSelectWorkspace: function () {},
      onCreateSession: function () {},
      onDeleteSession: function () {},
      onCreateWorkspace: function () {},
    }, options || {});

    this.mount = typeof this.options.mount === 'string'
      ? document.querySelector(this.options.mount)
      : this.options.mount;

    this.workspaces = this.options.workspaces || [];
    this.activeWorkspaceId = this.options.activeWorkspaceId || '';
    this.activeSessionId = this.options.activeSessionId || '';
    this.filter = this.options.filter || '';
    this.expandedWorkspaces = new Set();

    if (this.mount) {
      this._init();
    }
  }

  NebyWorkspaceTree.prototype._init = function () {
    this.mount.innerHTML = '';
    this.container = document.createElement('div');
    this.container.className = 'nc-tree-container';

    this.railTrack = document.createElement('div');
    this.railTrack.className = 'nc-tree-rail-track';
    this.container.appendChild(this.railTrack);

    this.indicator = document.createElement('div');
    this.indicator.className = 'nc-tree-indicator';
    this.container.appendChild(this.indicator);

    this.groupsContainer = document.createElement('div');
    this.groupsContainer.className = 'nc-tree-groups-wrap';
    this.container.appendChild(this.groupsContainer);

    this.mount.appendChild(this.container);

    if (this.activeWorkspaceId) {
      this.expandedWorkspaces.add(this.activeWorkspaceId);
    } else if (this.workspaces.length) {
      this.activeWorkspaceId = this.workspaces[0].id;
      this.expandedWorkspaces.add(this.workspaces[0].id);
    }

    this.render();
  };

  NebyWorkspaceTree.prototype.setData = function (data) {
    if (data.workspaces) this.workspaces = data.workspaces;
    if (data.activeWorkspaceId !== undefined) this.activeWorkspaceId = data.activeWorkspaceId;
    if (data.activeSessionId !== undefined) this.activeSessionId = data.activeSessionId;
    if (data.filter !== undefined) this.filter = data.filter;

    if (this.activeWorkspaceId) {
      this.expandedWorkspaces.add(this.activeWorkspaceId);
    } else if (this.workspaces.length && !this.expandedWorkspaces.size) {
      this.activeWorkspaceId = this.workspaces[0].id;
      this.expandedWorkspaces.add(this.workspaces[0].id);
    }

    this.render();
  };

  NebyWorkspaceTree.prototype.setActiveSession = function (sessionId, workspaceId) {
    this.activeSessionId = sessionId;
    if (workspaceId) {
      this.activeWorkspaceId = workspaceId;
      this.expandedWorkspaces.add(workspaceId);
    }
    this.render();
  };

  NebyWorkspaceTree.prototype.setActiveWorkspace = function (workspaceId) {
    this.activeWorkspaceId = workspaceId;
    this.expandedWorkspaces.add(workspaceId);
    this.render();
  };

  NebyWorkspaceTree.prototype.setFilter = function (query) {
    this.filter = (query || '').trim().toLowerCase();
    this.render();
  };

  NebyWorkspaceTree.prototype.render = function () {
    var self = this;
    if (!this.groupsContainer) return;

    var filterQuery = (this.filter || '').trim().toLowerCase();
    this.groupsContainer.innerHTML = '';

    if (!this.workspaces.length) {
      this.indicator.classList.remove('visible');
      return;
    }

    var activeGroupHeaderEl = null;

    this.workspaces.forEach(function (workspace, index) {
      var wsId = workspace.id || 'ws-' + index;
      var wsLabel = workspace.label || workspace.name || 'Workspace';
      var themeClass = workspace.theme || resolveTheme(index, wsLabel);
      var sessions = workspace.sessions || [];

      if (filterQuery) {
        sessions = sessions.filter(function (s) {
          return String(s.name || '').toLowerCase().indexOf(filterQuery) >= 0;
        });
      }

      var isExpanded = self.expandedWorkspaces.has(wsId) || filterQuery.length > 0;
      var isActiveWs = self.activeWorkspaceId === wsId;

      var groupEl = document.createElement('div');
      groupEl.className = 'nc-tree-group ' + themeClass + (isExpanded ? ' expanded' : '');
      groupEl.setAttribute('data-workspace-id', wsId);

      var headerEl = document.createElement('div');
      headerEl.className = 'nc-tree-group-header';
      headerEl.innerHTML =
        '<span class="nc-tree-group-title">' + esc(wsLabel) + '</span>' +
        '<div class="nc-tree-group-actions">' +
          '<button type="button" class="nc-tree-iconbtn nc-tree-add-btn" title="New session in ' + esc(wsLabel) + '"><span class="material-symbols-outlined">add</span></button>' +
        '</div>';

      headerEl.addEventListener('click', function (e) {
        if (e.target.closest('.nc-tree-add-btn')) {
          e.stopPropagation();
          self.options.onCreateSession(wsId, workspace);
          return;
        }

        if (self.expandedWorkspaces.has(wsId)) {
          self.expandedWorkspaces.delete(wsId);
        } else {
          self.expandedWorkspaces.clear();
          self.expandedWorkspaces.add(wsId);
          self.activeWorkspaceId = wsId;
        }

        self.options.onSelectWorkspace(wsId, workspace);
        self.render();
      });

      var addBtn = headerEl.querySelector('.nc-tree-add-btn');
      if (addBtn) {
        addBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          self.options.onCreateSession(wsId, workspace);
        });
      }

      groupEl.appendChild(headerEl);

      if (isActiveWs) {
        activeGroupHeaderEl = headerEl;
      }

      var bodyEl = document.createElement('div');
      bodyEl.className = 'nc-tree-group-body';

      var innerEl = document.createElement('div');
      innerEl.className = 'nc-tree-group-inner';

      var svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svgEl.setAttribute('class', 'nc-tree-svg-branches');
      innerEl.appendChild(svgEl);

      var itemsListEl = document.createElement('div');
      itemsListEl.className = 'nc-tree-items-list';

      var renderedRowEls = [];

      sessions.forEach(function (session) {
        var sessionId = session.id;
        var isSessionActive = self.activeSessionId === sessionId;
        var iconName = resolveIcon(session);

        var itemEl = document.createElement('div');
        itemEl.className = 'nc-tree-item' + (isSessionActive ? ' active' : '');
        itemEl.setAttribute('data-session-id', sessionId);

        var dotHtml = '';
        if (session.status === 'running' || session.status === 'queued') {
          dotHtml = '<span class="nc-tree-item-dot"></span>';
        }

        itemEl.innerHTML =
          '<span class="material-symbols-outlined nc-tree-item-icon">' + iconName + '</span>' +
          '<span class="nc-tree-item-label">' + esc(session.name || 'New session') + '</span>' +
          dotHtml +
          '<button type="button" class="nc-tree-item-del" title="Delete session"><span class="material-symbols-outlined">delete</span></button>';

        itemEl.addEventListener('click', function (e) {
          if (e.target.closest('.nc-tree-item-del')) return;
          self.activeSessionId = sessionId;
          self.activeWorkspaceId = wsId;
          self.options.onSelectSession(sessionId, wsId, session);
          self.render();
        });

        var delBtn = itemEl.querySelector('.nc-tree-item-del');
        if (delBtn) {
          delBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            self.options.onDeleteSession(sessionId, wsId, session);
          });
        }

        itemsListEl.appendChild(itemEl);
        renderedRowEls.push({ el: itemEl, isActive: isSessionActive });
      });

      var newRowEl = document.createElement('div');
      newRowEl.className = 'nc-tree-new-row';
      newRowEl.innerHTML = '<span class="material-symbols-outlined">add</span><span>New session</span>';
      newRowEl.addEventListener('click', function (e) {
        e.stopPropagation();
        self.options.onCreateSession(wsId, workspace);
      });
      itemsListEl.appendChild(newRowEl);
      renderedRowEls.push({ el: newRowEl, isActive: false });

      innerEl.appendChild(itemsListEl);
      bodyEl.appendChild(innerEl);
      groupEl.appendChild(bodyEl);
      self.groupsContainer.appendChild(groupEl);

      if (isExpanded) {
        requestAnimationFrame(function () {
          self._drawSvgBranches(innerEl, svgEl, renderedRowEls);
        });
      }
    });

    self._updateIndicator(activeGroupHeaderEl);
  };

  NebyWorkspaceTree.prototype._drawSvgBranches = function (innerEl, svgEl, rows) {
    if (!innerEl || !svgEl || !rows.length) return;
    var innerRect = innerEl.getBoundingClientRect();
    if (!innerRect.height) return;

    var startX = 2;
    var endX = 20;
    var radius = 7;
    var pathsHtml = '';

    var activeCenterY = null;
    var lastCenterY = null;

    rows.forEach(function (row) {
      var rowRect = row.el.getBoundingClientRect();
      var centerY = Math.round(rowRect.top - innerRect.top + (rowRect.height / 2));
      lastCenterY = centerY;

      if (row.isActive) {
        activeCenterY = centerY;
      }
    });

    // 1. Draw inactive background tree
    if (lastCenterY !== null) {
      var dMain = 'M ' + startX + ' 0 L ' + startX + ' ' + (lastCenterY - radius);
      pathsHtml += '<path d="' + dMain + '" class="branch-inactive" />';
    }

    rows.forEach(function (row) {
      var rowRect = row.el.getBoundingClientRect();
      var centerY = Math.round(rowRect.top - innerRect.top + (rowRect.height / 2));
      var branchD = 'M ' + startX + ' ' + Math.max(0, centerY - radius) +
                    ' Q ' + startX + ' ' + centerY + ' ' + (startX + radius) + ' ' + centerY +
                    ' L ' + endX + ' ' + centerY;
      pathsHtml += '<path d="' + branchD + '" class="branch-inactive" />';
    });

    // 2. Draw active highlight branch
    if (activeCenterY !== null) {
      var dActive = 'M ' + startX + ' 0 L ' + startX + ' ' + Math.max(0, activeCenterY - radius) +
                    ' Q ' + startX + ' ' + activeCenterY + ' ' + (startX + radius) + ' ' + activeCenterY +
                    ' L ' + endX + ' ' + activeCenterY;
      pathsHtml += '<path d="' + dActive + '" class="branch-active" />';
    }

    svgEl.setAttribute('height', Math.max(10, innerRect.height) + 'px');
    svgEl.innerHTML = pathsHtml;
  };

  NebyWorkspaceTree.prototype._updateIndicator = function (targetHeaderEl) {
    var self = this;
    if (!this.indicator || !this.container) return;

    if (!targetHeaderEl && this.groupsContainer) {
      targetHeaderEl = this.groupsContainer.querySelector('.nc-tree-group.expanded > .nc-tree-group-header') ||
                       this.groupsContainer.querySelector('.nc-tree-group-header');
    }

    if (!targetHeaderEl) {
      this.indicator.classList.remove('visible');
      return;
    }

    requestAnimationFrame(function () {
      var containerRect = self.container.getBoundingClientRect();
      var headerRect = targetHeaderEl.getBoundingClientRect();

      var top = Math.round(headerRect.top - containerRect.top + (headerRect.height - 24) / 2);
      var height = 24;

      var parentGroup = targetHeaderEl.closest('.nc-tree-group');
      if (parentGroup) {
        var computedStyle = getComputedStyle(parentGroup);
        var accent = computedStyle.getPropertyValue('--nc-accent').trim();
        if (accent) self.indicator.style.backgroundColor = accent;
      }

      self.indicator.style.transform = 'translateY(' + top + 'px)';
      self.indicator.style.height = height + 'px';
      self.indicator.classList.add('visible');
    });
  };

  NebyWorkspaceTree.prototype.destroy = function () {
    if (this.mount) this.mount.innerHTML = '';
  };

  global.NebyWorkspaceTree = NebyWorkspaceTree;
})(typeof window !== 'undefined' ? window : this);
