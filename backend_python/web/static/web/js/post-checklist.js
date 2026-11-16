/* To-do lines in a post (`- [ ] text`, `- [x] text`) become boxes the reader can tick.
   The author's text never changes; a reader's ticks stay in this browser, per post. */
(function () {
  'use strict';
  var CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.55 18 3.85 12.3l1.43-1.42 4.27 4.27 9.17-9.17 1.43 1.42z"/></svg>';
  var MARK = /^\s*\[( |x|X)\]\s+/;

  function firstText(li) {
    var n = li.firstChild;
    while (n && n.nodeType === 1 && n.tagName === 'P') n = n.firstChild;
    return n && n.nodeType === 3 ? n : null;
  }

  function run(root) {
    var id = (root.id || '').replace('post-content-', '') || location.pathname;
    var key = 'neb-post-ticks:' + id;
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(key) || '{}') || {}; } catch (e) { saved = {}; }
    var lists = root.querySelectorAll('ul');
    var idx = 0;
    for (var u = 0; u < lists.length; u++) {
      var ul = lists[u], tasks = [];
      var items = ul.children;
      for (var i = 0; i < items.length; i++) {
        var li = items[i];
        if (li.tagName !== 'LI') continue;
        var t = firstText(li);
        var m = t && MARK.exec(t.nodeValue);
        if (!m) continue;
        t.nodeValue = t.nodeValue.slice(m[0].length);
        var n = idx++;
        var done = saved[n] !== undefined ? !!saved[n] : m[1] !== ' ';
        var box = document.createElement('button');
        box.type = 'button';
        box.className = 'nb-task-box';
        box.setAttribute('role', 'checkbox');
        box.innerHTML = CHECK;
        li.classList.add('nb-task');
        li.insertBefore(box, li.firstChild);
        tasks.push(li);
        (function (li, box, n) {
          function set(v) {
            li.classList.toggle('is-done', v);
            box.setAttribute('aria-checked', v ? 'true' : 'false');
          }
          set(done);
          li.addEventListener('click', function (e) {
            if (e.target.closest && e.target.closest('a')) return;
            var v = !li.classList.contains('is-done');
            set(v);
            saved[n] = v;
            try { localStorage.setItem(key, JSON.stringify(saved)); } catch (err) { /* private mode */ }
          });
        })(li, box, n);
      }
      if (tasks.length) ul.classList.add('nb-tasks');
    }
  }

  function start() {
    var root = document.querySelector('.fp-post-body');
    if (root) run(root);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
