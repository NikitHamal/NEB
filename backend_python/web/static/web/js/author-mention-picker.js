(function() {
  'use strict';

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str == null ? '' : String(str);
    return div.innerHTML;
  }

  function avatarMarkup(photoUrl, name) {
    var letter = (name || '?').trim().charAt(0).toUpperCase() || '?';
    if (photoUrl) {
      return '<img src="' + escapeHtml(photoUrl) + '" alt="" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'\';"><span style="display:none">' + escapeHtml(letter) + '</span>';
    }
    return '<span>' + escapeHtml(letter) + '</span>';
  }

  function initMentionField(input) {
    var wrap = document.createElement('div');
    wrap.className = 'mention-wrap';
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);

    var dropdown = document.createElement('div');
    dropdown.className = 'mention-dropdown';
    dropdown.style.display = 'none';
    wrap.appendChild(dropdown);

    var query = '';
    var queryStart = 0;
    var results = [];
    var activeIdx = -1;
    var debounceTimer = null;

    function detectMention() {
      var value = input.value;
      var caret = input.selectionStart;
      var before = value.substring(0, caret);
      var match = before.match(/@([A-Za-z0-9_.]*)$/);
      if (match) {
        query = match[1];
        queryStart = match.index;
        return true;
      }
      return false;
    }

    function renderDropdown() {
      if (!results.length) {
        hideDropdown();
        return;
      }
      dropdown.innerHTML = results.map(function(u, i) {
        var cls = 'mention-result' + (i === activeIdx ? ' active' : '');
        return '<button type="button" class="' + cls + '" data-idx="' + i + '">' +
          '<span class="mention-result-avatar">' + avatarMarkup(u.photoUrl, u.displayName) + '</span>' +
          '<span class="mention-result-info">' +
            '<span class="mention-result-name">' + escapeHtml(u.displayName || u.username) + '</span>' +
            '<span class="mention-result-handle">@' + escapeHtml(u.username) + '</span>' +
          '</span>' +
        '</button>';
      }).join('');
      dropdown.style.display = '';
      dropdown.querySelectorAll('.mention-result').forEach(function(btn) {
        btn.addEventListener('mousedown', function(e) {
          e.preventDefault();
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          insertMention(idx);
        });
      });
    }

    function hideDropdown() {
      dropdown.style.display = 'none';
      activeIdx = -1;
    }

    function insertMention(idx) {
      if (idx < 0 || idx >= results.length) return;
      var u = results[idx];
      var before = input.value.substring(0, queryStart);
      var after = input.value.substring(queryStart + 1 + query.length);
      var insert = '@' + u.username + ' ';
      input.value = before + insert + after;
      var newCaret = (before + insert).length;
      input.focus();
      try { input.setSelectionRange(newCaret, newCaret); } catch (e) {}
      hideDropdown();
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function fetchResults(q) {
      fetch('/ajax/user-search/?q=' + encodeURIComponent(q), { credentials: 'same-origin' })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          results = data || [];
          activeIdx = results.length ? 0 : -1;
          renderDropdown();
        })
        .catch(function() { hideDropdown(); });
    }

    input.addEventListener('input', function() {
      if (detectMention()) {
        if (query.length < 1) {
          hideDropdown();
          return;
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() { fetchResults(query); }, 200);
      } else {
        hideDropdown();
      }
    });

    input.addEventListener('keydown', function(e) {
      if (dropdown.style.display === 'none') return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIdx = Math.min(activeIdx + 1, results.length - 1);
        renderDropdown();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIdx = Math.max(activeIdx - 1, 0);
        renderDropdown();
      } else if (e.key === 'Enter' || e.key === 'Tab') {
        if (activeIdx >= 0) {
          e.preventDefault();
          insertMention(activeIdx);
        }
      } else if (e.key === 'Escape') {
        hideDropdown();
      }
    });

    input.addEventListener('blur', function() {
      setTimeout(hideDropdown, 150);
    });
  }

  function initAll() {
    document.querySelectorAll('input[data-mention-user="1"]:not([data-mention-ready])').forEach(function(input) {
      input.setAttribute('data-mention-ready', '1');
      initMentionField(input);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
