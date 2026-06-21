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

  function showSelection(picker, user) {
    var selection = picker.querySelector('.behalf-selection');
    var searchRow = picker.querySelector('.behalf-search-row');
    var results = picker.querySelector('.behalf-results');
    picker.querySelector('#behalf-username').value = user.username;
    picker.querySelector('.behalf-avatar').innerHTML = avatarMarkup(user.photoUrl, user.displayName);
    picker.querySelector('.behalf-name').textContent = user.displayName || user.username;
    picker.querySelector('.behalf-handle').textContent = '@' + user.username;
    selection.style.display = '';
    searchRow.style.display = 'none';
    results.style.display = 'none';
    var clearFlag = picker.querySelector('#clear-behalf');
    if (clearFlag) clearFlag.value = '';
  }

  function showSearch(picker) {
    var selection = picker.querySelector('.behalf-selection');
    var searchRow = picker.querySelector('.behalf-search-row');
    var searchInput = picker.querySelector('.behalf-search-input');
    var results = picker.querySelector('.behalf-results');
    selection.style.display = 'none';
    searchRow.style.display = '';
    results.style.display = 'none';
    picker.querySelector('#behalf-username').value = '';
    var clearFlag = picker.querySelector('#clear-behalf');
    if (clearFlag) clearFlag.value = '1';
    if (searchInput) searchInput.focus();
  }

  function renderResults(picker, users) {
    var results = picker.querySelector('.behalf-results');
    if (!users.length) {
      results.innerHTML = '<div class="behalf-empty">No users found.</div>';
      results.style.display = '';
      return;
    }
    results.innerHTML = users.map(function(u, i) {
      return '<button type="button" class="behalf-result" data-idx="' + i + '">' +
        '<span class="behalf-result-avatar">' + avatarMarkup(u.photoUrl, u.displayName) + '</span>' +
        '<span class="behalf-result-info">' +
          '<span class="behalf-result-name">' + escapeHtml(u.displayName || u.username) + '</span>' +
          '<span class="behalf-result-handle">@' + escapeHtml(u.username) + '</span>' +
        '</span>' +
      '</button>';
    }).join('');
    results.style.display = '';
    var cached = users;
    results.querySelectorAll('.behalf-result').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        var idx = parseInt(btn.getAttribute('data-idx'), 10);
        showSelection(picker, cached[idx]);
      });
    });
  }

  function initBehalfPicker(picker) {
    var searchInput = picker.querySelector('.behalf-search-input');
    var clearBtn = picker.querySelector('.behalf-clear');
    var results = picker.querySelector('.behalf-results');
    var debounceTimer = null;

    var initialUsername = picker.getAttribute('data-initial-username');
    var initialName = picker.getAttribute('data-initial-name');
    var initialPhoto = picker.getAttribute('data-initial-photo');
    if (initialUsername) {
      showSelection(picker, { username: initialUsername, displayName: initialName || initialUsername, photoUrl: initialPhoto || '' });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', function(e) {
        e.preventDefault();
        showSearch(picker);
      });
    }

    if (searchInput) {
      searchInput.addEventListener('input', function() {
        var q = searchInput.value.trim();
        clearTimeout(debounceTimer);
        if (q.length < 2) {
          results.style.display = 'none';
          return;
        }
        debounceTimer = setTimeout(function() {
          fetch('/ajax/user-search/?q=' + encodeURIComponent(q), { credentials: 'same-origin' })
            .then(function(r) { return r.json(); })
            .then(function(data) { renderResults(picker, data || []); })
            .catch(function() { results.style.display = 'none'; });
        }, 250);
      });

      searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          results.style.display = 'none';
        }
      });
    }

    document.addEventListener('click', function(e) {
      if (!picker.contains(e.target)) {
        results.style.display = 'none';
      }
    });
  }

  document.querySelectorAll('.behalf-picker').forEach(initBehalfPicker);
})();
