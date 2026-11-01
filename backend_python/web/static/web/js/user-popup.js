/* Author hover card. Any element marked data-user-popup="<username>" gets it,
   and the thread page's author links keep working through the .fp-post /
   .fp-thread-reply selectors. The card is created here, not in a template, so
   every page that shows a name gets the same preview. */
(function () {
  'use strict';

  var SHOW_DELAY = 320;
  var HIDE_DELAY = 240;
  var SKELETON_DELAY = 140;
  var cache = {};
  var card = null;
  var currentAnchor = null;
  var showTimer = null;
  var hideTimer = null;
  var skeletonTimer = null;
  var requestSeq = 0;
  var overCard = false;

  var PROFILE_LINK = 'a[href*="/app/profile/"]';

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function signedIn() {
    return typeof IS_AUTHENTICATED !== 'undefined' && !!IS_AUTHENTICATED;
  }

  function ensureCard() {
    if (card && document.body.contains(card)) return card;
    card = document.createElement('div');
    card.className = 'fp-user-popup';
    card.id = 'nebUserPopup';
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-label', 'Profile preview');
    document.body.appendChild(card);
    card.addEventListener('mouseenter', function () {
      overCard = true;
      clearTimeout(hideTimer);
      clearTimeout(showTimer);
    });
    card.addEventListener('mouseleave', function () {
      overCard = false;
      scheduleHide();
    });
    return card;
  }

  function findAnchor(target) {
    if (!target || target.nodeType !== 1) return null;
    var el = target.closest('[data-user-popup]');
    if (!el) {
      var thread = target.closest('.fp-post, .fp-thread-reply, .fp-reply');
      if (thread) el = target.closest(PROFILE_LINK);
    }
    if (!el) return null;
    if (el.closest('.fp-user-popup')) return null;
    return el;
  }

  function usernameFor(el) {
    var explicit = el.getAttribute('data-user-popup');
    if (explicit) return explicit;
    var href = el.getAttribute('href') || '';
    var match = href.match(/\/profile\/([^/]+)\//);
    return match ? decodeURIComponent(match[1]) : null;
  }

  function skeletonHtml() {
    return '<div class="fp-user-popup-header">' +
        '<div class="fp-user-popup-avatar fp-sk fp-sk-avatar"></div>' +
        '<div class="fp-user-popup-id">' +
          '<div class="fp-sk fp-sk-line" style="width:58%"></div>' +
          '<div class="fp-sk fp-sk-line fp-sk-line-sm" style="width:36%;margin-top:7px"></div>' +
        '</div>' +
      '</div>' +
      '<div class="fp-sk fp-sk-line fp-sk-line-sm" style="width:52%;margin-top:10px"></div>';
  }

  function renderSkeleton(anchor) {
    var el = ensureCard();
    el.innerHTML = skeletonHtml();
    el.setAttribute('aria-busy', 'true');
    el.classList.add('visible');
    position(anchor);
  }

  function countLabel(value, word) {
    var n = Number(value) || 0;
    return n + ' ' + word + (n === 1 ? '' : 's');
  }

  function render(data, anchor) {
    var el = ensureCard();
    var name = data.displayName || data.username || '';
    var initial = name.charAt(0) || '?';
    var profileHref = '/app/profile/' + encodeURIComponent(data.username) + '/';
    var avatarHtml = data.photoUrl
      ? '<img src="' + esc(data.photoUrl) + '" alt="" data-fallback="flex"><span class="fp-user-popup-avatar-letter" style="display:none;">' + esc(initial) + '</span>'
      : '<span class="fp-user-popup-avatar-letter">' + esc(initial) + '</span>';
    var followBtn = (!data.isSelf && signedIn())
      ? '<button class="follow-btn-inline ' + (data.isFollowing ? 'following' : 'not-following') + '" data-action="toggle-follow" data-user-id="' + esc(data.id) + '">' + (data.isFollowing ? 'Following' : 'Follow') + '</button>'
      : '';

    var html = '<div class="fp-user-popup-header">' +
      '<a class="fp-user-popup-avatar" href="' + profileHref + '" aria-label="View ' + esc(name) + '\'s profile">' + avatarHtml + '</a>' +
      '<div class="fp-user-popup-id">' +
        '<div class="fp-user-popup-name-row">' +
          '<a class="fp-user-popup-name" href="' + profileHref + '">' +
            '<span class="fp-user-popup-name-text">' + esc(name) + '</span>' +
          '</a>' +
          (data.badgeInfo ? '<span class="role-badge role-badge-' + esc(data.badgeInfo.type) + '" title="' + esc(data.badgeInfo.label) + '"><span class="material-symbols-outlined">' + esc(data.badgeInfo.icon) + '</span></span>' : '') +
        '</div>' +
        '<div class="fp-user-popup-username">@' + esc(data.username) + '</div>' +
      '</div>' +
      followBtn +
    '</div>';

    if (data.bio) {
      html += '<div class="fp-user-popup-bio">' + esc(data.bio) + '</div>';
    }
    if (!data.isLocked) {
      html += '<div class="fp-user-popup-meta">' +
        '<span>' + esc(countLabel(data.postCount, 'post')) + '</span>' +
        '<span class="fp-user-popup-dot">·</span>' +
        '<span>' + esc(countLabel(data.replyCount, 'reply')) + '</span>' +
        '<span class="fp-user-popup-dot">·</span>' +
        '<span>' + esc(countLabel(data.followerCount, 'follower')) + '</span>' +
      '</div>';
    }

    el.innerHTML = html;
    el.removeAttribute('aria-busy');
    el.classList.add('visible');
    position(anchor);
  }

  function position(anchor) {
    if (!anchor || !card || !card.classList.contains('visible')) return;
    var rect = anchor.getBoundingClientRect();
    var width = card.offsetWidth || 252;
    var height = card.offsetHeight || 120;
    var top = rect.bottom + 8;
    var left = rect.left + rect.width / 2 - width / 2;
    if (left + width > window.innerWidth - 12) left = window.innerWidth - width - 12;
    if (left < 12) left = 12;
    if (top + height > window.innerHeight - 12) top = rect.top - height - 8;
    if (top < 12) top = 12;
    card.style.top = top + 'px';
    card.style.left = left + 'px';
  }

  function hideNow() {
    clearTimeout(showTimer);
    clearTimeout(skeletonTimer);
    if (card) {
      card.classList.remove('visible');
      card.removeAttribute('aria-busy');
    }
    currentAnchor = null;
    overCard = false;
  }

  function scheduleHide() {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function () {
      if (!overCard) hideNow();
    }, HIDE_DELAY);
  }

  function openFor(username, anchor) {
    ensureCard();
    currentAnchor = anchor;
    clearTimeout(skeletonTimer);
    clearTimeout(hideTimer);

    if (cache[username]) {
      render(cache[username], anchor);
      return;
    }

    var seq = ++requestSeq;
    skeletonTimer = setTimeout(function () {
      if (seq === requestSeq) renderSkeleton(anchor);
    }, SKELETON_DELAY);

    fetch('/ajax/user-popup/' + encodeURIComponent(username) + '/', {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(function (response) { return response.ok ? response.json() : null; })
      .then(function (data) {
        clearTimeout(skeletonTimer);
        if (seq !== requestSeq) return;
        if (!data || !data.username) {
          hideNow();
          return;
        }
        cache[username] = data;
        render(data, anchor);
      })
      .catch(function () {
        clearTimeout(skeletonTimer);
        if (seq === requestSeq) hideNow();
      });
  }

  document.addEventListener('mouseenter', function (event) {
    var anchor = findAnchor(event.target);
    if (!anchor) return;
    var username = usernameFor(anchor);
    if (!username) return;
    overCard = false;
    clearTimeout(hideTimer);
    clearTimeout(showTimer);
    currentAnchor = anchor;
    showTimer = setTimeout(function () {
      openFor(username, anchor);
    }, SHOW_DELAY);
  }, true);

  document.addEventListener('mouseleave', function (event) {
    var anchor = findAnchor(event.target);
    if (!anchor || anchor !== currentAnchor) return;
    clearTimeout(showTimer);
    scheduleHide();
  }, true);

  document.addEventListener('scroll', hideNow, true);

  window.addEventListener('resize', function () {
    position(currentAnchor);
  }, { passive: true });
})();
