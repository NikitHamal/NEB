(function () {
  'use strict';
  var UI = window.CodeUI;

  var KEYWORDS = {
    js: 'const let var function return if else for while class new extends import export from default async await try catch finally throw typeof instanceof this super null undefined true false switch case break continue do delete void yield static get set of in as type interface implements enum public private protected readonly declare namespace',
    py: 'def return if elif else for while class import from as with try except finally raise lambda None True False and or not in is pass break continue global nonlocal yield async await assert del match case self',
    css: 'important media supports keyframes import from to and not only',
    go: 'func package import return if else for range switch case break continue defer chan go select struct interface map type var const nil true false',
    rs: 'fn let mut pub use mod struct enum impl trait for while loop if else match return Some None Ok Err self crate dyn where unsafe async await move ref',
    sh: 'if then else fi for do done while case esac function exit return local echo cd export set unset source alias',
  };

  function langOf(path) {
    var ext = (String(path || '').split('.').pop() || '').toLowerCase();
    if (['js', 'mjs', 'cjs', 'jsx', 'ts', 'tsx', 'json'].indexOf(ext) >= 0) return 'js';
    if (ext === 'py') return 'py';
    if (['css', 'scss', 'less'].indexOf(ext) >= 0) return 'css';
    if (ext === 'go') return 'go';
    if (ext === 'rs') return 'rs';
    if (['sh', 'bash', 'ps1', 'bat'].indexOf(ext) >= 0) return 'sh';
    if (['yml', 'yaml', 'toml', 'ini', 'env', 'conf'].indexOf(ext) >= 0) return 'conf';
    return '';
  }

  function highlight(code, path) {
    var lang = langOf(path);
    var source = String(code == null ? '' : code);
    if (!lang || source.length > 400000) return UI.esc(source);
    if (lang === 'conf') {
      return source.split('\n').map(function (line) {
        if (/^\s*[#;]/.test(line)) return '<span class="tk-com">' + UI.esc(line) + '</span>';
        return UI.esc(line).replace(/^([\w.-]+)(=)/, '<span class="tk-key">$1</span>$2');
      }).join('\n');
    }
    var keywords = (KEYWORDS[lang] || '').split(' ');
    var out = '';
    var index = 0;
    var strRe = /^("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)/;
    var commentRe = (lang === 'py' || lang === 'sh') ? /^#.*/ : /^(?:\/\/.*|\/\*[\s\S]*?\*\/)/;
    while (index < source.length) {
      var rest = source.slice(index);
      var match = strRe.exec(rest);
      if (match) {
        out += '<span class="tk-str">' + UI.esc(match[0]) + '</span>';
        index += match[0].length;
        continue;
      }
      match = commentRe.exec(rest);
      if (match) {
        out += '<span class="tk-com">' + UI.esc(match[0]) + '</span>';
        index += match[0].length;
        continue;
      }
      var ch = source[index];
      if (/[A-Za-z_$]/.test(ch)) {
        var word = /^[$A-Za-z_][$\w]*/.exec(rest)[0];
        if (keywords.indexOf(word) >= 0) out += '<span class="tk-key">' + word + '</span>';
        else if (source[index + word.length] === '(' || /^[A-Z]/.test(word)) out += '<span class="tk-fn">' + word + '</span>';
        else out += UI.esc(word);
        index += word.length;
        continue;
      }
      if (/\d/.test(ch) && !/[\w$]/.test(source[index - 1] || '')) {
        match = /^(?:0[xXbBoO]?[\da-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(rest);
        if (match) {
          out += '<span class="tk-num">' + match[0] + '</span>';
          index += match[0].length;
          continue;
        }
      }
      out += UI.esc(ch);
      index += 1;
    }
    return out;
  }

  function withNums(html) {
    return String(html || '').split('\n').map(function (line, index) {
      return '<span class="ncu-line"><span class="ncu-ln">' + (index + 1) + '</span><span class="ncu-lcode">' + (line || ' ') + '</span></span>';
    }).join('');
  }

  var FILE_ICONS = {
    js: 'javascript', ts: 'javascript', jsx: 'javascript', tsx: 'javascript', py: 'terminal',
    html: 'html', css: 'css', scss: 'css', json: 'data_object', yml: 'data_object',
    yaml: 'data_object', toml: 'data_object', md: 'description', txt: 'description',
    sh: 'terminal', bash: 'terminal', ps1: 'terminal', svg: 'image', png: 'image',
  };

  function iconForFile(path) {
    var ext = (String(path || '').split('.').pop() || '').toLowerCase();
    return FILE_ICONS[ext] || 'draft';
  }

  function isDir(node) {
    return node && (node.is_dir === true || node.type === 'dir' || node.type === 'folder');
  }

  function Tree(opts) {
    var root = UI.el('div', 'ncu-tree ncu-code');
    var selected = '';
    var expanded = {};

    function renderRows(parent, entries, depth) {
      (entries || []).forEach(function (entry) {
        var row = document.createElement('button');
        var folder = isDir(entry);
        row.type = 'button';
        row.className = 'ncu-tree-row ' + (folder ? 'dir' : 'file') + (selected === entry.path ? ' sel' : '');
        row.style.paddingLeft = (8 + depth * 14) + 'px';
        row.innerHTML = UI.icon(folder ? (expanded[entry.path] ? 'folder_open' : 'folder') : iconForFile(entry.name || entry.path)) + '<span class="tname">' + UI.esc(entry.name || entry.path) + '</span>';
        parent.appendChild(row);
        if (folder) {
          var children = document.createElement('div');
          children.hidden = !expanded[entry.path];
          parent.appendChild(children);
          row.addEventListener('click', function () {
            expanded[entry.path] = !expanded[entry.path];
            children.hidden = !expanded[entry.path];
            row.querySelector('.material-symbols-outlined').textContent = expanded[entry.path] ? 'folder_open' : 'folder';
            if (expanded[entry.path] && !children.dataset.loaded) {
              opts.api.fsList(entry.path).then(function (data) {
                children.dataset.loaded = '1';
                renderRows(children, data.entries || [], depth + 1);
              }).catch(opts.onError);
            }
          });
        } else {
          row.addEventListener('click', function () {
            selected = entry.path;
            root.querySelectorAll('.ncu-tree-row.sel').forEach(function (item) { item.classList.remove('sel'); });
            row.classList.add('sel');
            opts.onOpenFile(entry.path);
          });
        }
      });
    }

    function refresh() {
      root.innerHTML = '';
      return opts.api.fsList('.').then(function (data) {
        renderRows(root, data.entries || [], 0);
        return data;
      });
    }

    return { el: root, refresh: refresh, render: function (entries) { root.innerHTML = ''; renderRows(root, entries || [], 0); } };
  }

  function Editor(opts) {
    var root = UI.el('div', 'ncu-editor ncu-code');
    root.innerHTML = '<div class="ncu-edtabs"></div><div class="ncu-edempty">Open a file from the workspace</div><div class="ncu-edmain" hidden><div class="ncu-edbar"><span class="ncu-edpath"></span><span style="flex:1"></span></div><div class="ncu-edwrap"><pre class="ncu-edpre"><code></code></pre><textarea class="ncu-edta" spellcheck="false" hidden></textarea></div></div>';
    var tabs = root.querySelector('.ncu-edtabs');
    var empty = root.querySelector('.ncu-edempty');
    var main = root.querySelector('.ncu-edmain');
    var pathEl = root.querySelector('.ncu-edpath');
    var pre = root.querySelector('.ncu-edpre');
    var code = root.querySelector('code');
    var textarea = root.querySelector('.ncu-edta');
    var bar = root.querySelector('.ncu-edbar');
    var files = [];
    var active = '';
    var editing = false;
    var editButton = UI.IconButton({ icon: 'edit', title: 'Edit file', sm: true, onClick: startEdit });
    var saveButton = UI.IconButton({ icon: 'save', title: 'Save file', sm: true, onClick: save });
    saveButton.el.hidden = true;
    bar.appendChild(editButton.el);
    bar.appendChild(saveButton.el);

    function activeFile() {
      return files.find(function (item) { return item.path === active; });
    }

    function renderTabs() {
      tabs.innerHTML = '';
      files.forEach(function (file) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'ncu-edtab' + (file.path === active ? ' on' : '');
        button.innerHTML = UI.icon(iconForFile(file.path)) + '<span>' + UI.esc(file.path.split('/').pop()) + '</span>';
        button.title = file.path;
        button.addEventListener('click', function () { activate(file.path); });
        var close = document.createElement('span');
        close.className = 'material-symbols-outlined';
        close.textContent = 'close';
        close.addEventListener('click', function (event) {
          event.stopPropagation();
          files = files.filter(function (item) { return item.path !== file.path; });
          if (active === file.path) {
            active = files.length ? files[files.length - 1].path : '';
            if (active) activate(active);
            else {
              empty.hidden = false;
              main.hidden = true;
            }
          }
          renderTabs();
        });
        button.appendChild(close);
        tabs.appendChild(button);
      });
    }

    function paint() {
      var file = activeFile();
      if (!file) return;
      var source = file.content.length > 500000 ? file.content.slice(0, 500000) + '\n… file preview truncated …' : file.content;
      code.innerHTML = withNums(highlight(source, file.path));
    }

    function activate(path) {
      active = path;
      editing = false;
      empty.hidden = true;
      main.hidden = false;
      pathEl.textContent = path;
      pathEl.title = path;
      textarea.hidden = true;
      pre.hidden = false;
      editButton.el.hidden = false;
      saveButton.el.hidden = true;
      paint();
      renderTabs();
    }

    function startEdit() {
      var file = activeFile();
      if (!file) return;
      editing = true;
      textarea.value = file.content;
      textarea.hidden = false;
      pre.hidden = true;
      editButton.el.hidden = true;
      saveButton.el.hidden = false;
      textarea.focus();
    }

    function save() {
      var file = activeFile();
      if (!file || !editing) return;
      saveButton.el.disabled = true;
      Promise.resolve(opts.onSave(file.path, textarea.value)).then(function () {
        file.content = textarea.value;
        editing = false;
        textarea.hidden = true;
        pre.hidden = false;
        editButton.el.hidden = false;
        saveButton.el.hidden = true;
        paint();
        UI.toast('Saved ' + file.path.split('/').pop());
        if (opts.onSaved) opts.onSaved(file.path);
      }).catch(opts.onError).finally(function () { saveButton.el.disabled = false; });
    }

    textarea.addEventListener('keydown', function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
        event.preventDefault();
        save();
      }
      if (event.key === 'Tab') {
        event.preventDefault();
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;
        textarea.value = textarea.value.slice(0, start) + '  ' + textarea.value.slice(end);
        textarea.selectionStart = textarea.selectionEnd = start + 2;
      }
    });

    return {
      el: root,
      open: function (path, content) {
        var file = files.find(function (item) { return item.path === path; });
        if (file) file.content = String(content || '');
        else files.push({ path: path, content: String(content || '') });
        activate(path);
      },
      activePath: function () { return active; },
      setContent: function (path, content) {
        var file = files.find(function (item) { return item.path === path; });
        if (file && (!editing || active !== path)) {
          file.content = String(content || '');
          if (active === path) paint();
        }
      },
    };
  }

  function Terminal(opts) {
    var root = UI.el('div', 'ncu-terminal');
    root.innerHTML = '<div class="ncu-term-header"><span class="ncu-term-title"><span class="material-symbols-outlined">terminal</span>Local shell</span><button type="button" class="ncu-iconbtn sm ncu-term-clear" title="Clear terminal"><span class="material-symbols-outlined">delete_sweep</span></button></div><div class="ncu-termlog ncu-code"><div class="ncu-termmuted">Commands run in your connected local workspace.</div></div><form class="ncu-termform"><span class="ncu-term-prompt">❯</span><input autocomplete="off" spellcheck="false" placeholder="Run a command…"><button type="submit" class="ncu-iconbtn sm" title="Run"><span class="material-symbols-outlined">arrow_upward</span></button></form>';
    var log = root.querySelector('.ncu-termlog');
    var form = root.querySelector('form');
    var input = root.querySelector('input');
    var history = [];
    var historyIndex = 0;

    function line(text, cls) {
      var row = document.createElement('div');
      row.className = 'ncu-termline' + (cls ? ' ' + cls : '');
      row.textContent = text;
      log.appendChild(row);
      while (log.childNodes.length > 1400) log.removeChild(log.firstChild);
      log.scrollTop = log.scrollHeight;
      return row;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var command = input.value.trim();
      if (!command) return;
      input.value = '';
      history.push(command);
      historyIndex = history.length;
      line('$ ' + command, 'cmd');
      opts.onRun(command);
    });

    input.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (historyIndex > 0) historyIndex -= 1;
        input.value = history[historyIndex] || '';
      } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (historyIndex < history.length - 1) historyIndex += 1;
        else historyIndex = history.length;
        input.value = history[historyIndex] || '';
      }
    });

    root.querySelector('.ncu-term-clear').addEventListener('click', function () { log.innerHTML = ''; });

    return {
      el: root,
      line: line,
      appendChunk: function (chunk, stream) {
        if (!chunk) return;
        line(String(chunk).replace(/\r\n/g, '\n').replace(/\n$/, ''), stream === 'err' ? 'err' : '');
      },
      finish: function (code, ms) {
        if (code != null) line('Process exited with code ' + code + (ms ? ' · ' + (ms / 1000).toFixed(1) + 's' : ''), code === 0 ? '' : 'err');
      },
      focus: function () { input.focus(); },
    };
  }

  function ChangesList(opts) {
    var root = UI.el('div', 'ncu-changes');
    var head = UI.el('div', 'ncu-chghead');
    var list = UI.el('div', 'ncu-chglist');
    root.appendChild(head);
    root.appendChild(list);

    function render(files) {
      files = files || [];
      head.innerHTML = '<span class="ncu-chgcount">' + files.length + ' change' + (files.length === 1 ? '' : 's') + '</span><span style="flex:1"></span>';
      list.innerHTML = '';
      files.forEach(function (file) {
        var row = document.createElement('button');
        row.type = 'button';
        row.className = 'ncu-chgrow' + (file.path === opts.getActive() ? ' sel' : '');
        var icon = file.kind === 'delete' ? 'delete' : (file.kind === 'new' ? 'note_add' : (file.kind === 'rename' ? 'drive_file_rename_outline' : 'edit_note'));
        row.innerHTML = UI.icon(icon) + '<span class="t-path">' + UI.esc(file.path) + '</span>' + (file.kind === 'new' ? '<span class="ncu-badge new">New</span>' : '');
        row.addEventListener('click', function () { opts.onOpen(file.path); });
        list.appendChild(row);
      });
      if (!files.length) list.innerHTML = '<div class="ncu-termmuted" style="padding:14px 10px">Working tree clean.</div>';
    }

    return { el: root, render: render };
  }

  window.CodePanels = {
    highlight: highlight,
    withNums: withNums,
    langOf: langOf,
    Tree: Tree,
    Editor: Editor,
    Terminal: Terminal,
    ChangesList: ChangesList,
  };
})();
