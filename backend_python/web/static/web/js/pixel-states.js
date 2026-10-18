// Empty states get the app's pixel art: each one already shows a Material icon naming its
// situation (cloud_off, search_off, bookmark...), so the matching sprite is picked from that name,
// exactly as the Android app's PixelStates does. Content loaded later is handled too.
(function () {
  var RULES = [
    [/^(cloud_off|wifi_off|error|error_outline|sync_problem|warning)$/, 'rainCloud'],
    [/^(search|search_off|manage_search|find_in_page|travel_explore)$/, 'magnifier'],
    [/^notifications/, 'sleepyBell'],
    [/^bookmark/, 'ribbon'],
    [/^(download|download_done|cloud_download|file_download|downloading)$/, 'downloadTray'],
    [/^(forum|chat|chat_bubble|chat_bubble_outline|question_answer|comment|comments_disabled|mode_comment)$/, 'typing'],
    [/^(menu_book|auto_stories|library_books|description|picture_as_pdf|folder_off|book|import_contacts)$/, 'bookLoader'],
    [/^(inbox|hourglass_empty|hourglass_top|schedule|bedtime)$/, 'nebySleep'],
    [/^(lock|lock_outline|shield|key|vpn_key)$/, 'padlock'],
    [/^(newspaper|article|feed|campaign|announcement)$/, 'newspaper'],
    [/^(payments|paid|account_balance|account_balance_wallet|toll|savings|wallet|receipt_long|credit_card)$/, 'coin'],
    [/^(push_pin|keep)$/, 'pushPin'],
    [/^(storefront|store|shopping_bag|sell|dashboard_customize|local_mall)$/, 'storefront'],
    [/^(emoji_events|leaderboard|insights|bar_chart|analytics|military_tech|workspace_premium)$/, 'trophy'],
  ];
  var SEL = '.empty-state > .material-symbols-outlined, .notif-empty-state > .material-symbols-outlined, .fp-empty > .material-symbols-outlined, ' +
    '.notif-empty-icon > .material-symbols-outlined, .bookmarks-empty-icon > .material-symbols-outlined, .request-empty > .material-symbols-outlined, ' +
    '.empty-leaderboard > .material-symbols-outlined, .follow-list-empty > .material-symbols-outlined, .credits-empty > .material-symbols-outlined';
  var HOSTS = '.empty-state, .notif-empty-state, .fp-empty, .bookmarks-empty, .request-empty, .empty-leaderboard, .follow-list-empty, .credits-empty';

  function spriteFor(name) {
    for (var i = 0; i < RULES.length; i++) if (RULES[i][0].test(name)) return RULES[i][1];
    return 'nebyIdle';
  }
  function upgrade(root) {
    var icons = (root.querySelectorAll ? root.querySelectorAll(SEL) : []);
    for (var i = 0; i < icons.length; i++) {
      var icon = icons[i];
      if (icon.getAttribute('data-px')) continue;
      var sprite = document.createElement('span');
      sprite.className = 'px-sprite px-' + spriteFor((icon.textContent || '').trim());
      sprite.setAttribute('aria-hidden', 'true');
      sprite.setAttribute('data-px', '1');
      icon.replaceWith(sprite);
    }
  }
  function start() {
    upgrade(document);
    if (!('MutationObserver' in window)) return;
    new MutationObserver(function (list) {
      for (var i = 0; i < list.length; i++) for (var j = 0; j < list[i].addedNodes.length; j++) {
        var n = list[i].addedNodes[j];
        if (n.nodeType === 1 && (n.matches && (n.matches(HOSTS) || n.querySelector(HOSTS)))) upgrade(n.parentNode || n);
      }
    }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
