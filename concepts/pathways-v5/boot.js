/* Pathways v5 boot: builds the rail and bottom bar, then renders the first route. */
(function () {
  'use strict';
  var V = window.V, M = V.ms;
  var item = function (n) { return '<button data-go="' + n[0] + '" data-nav="' + n[0] + '" aria-current="false"><span class="pill">' + M(n[2]) + '</span>' + n[1] + '</button>'; };
  V.$('#rail').innerHTML = '<a class="mk" href="#/home" aria-label="Home">' + M('alt_route') + '</a>' + V.NAV.slice(0, 9).map(item).join('') + '<span class="sp"></span>' + V.NAV.slice(9).map(item).join('');
  V.$('#bnav').innerHTML = V.NAV.slice(0, 5).map(item).join('') + '<button data-act="more" aria-label="More"><span class="pill">' + M('apps') + '</span>More</button>';
  V.$('#themeIc').textContent = document.documentElement.dataset.theme === 'dark' ? 'light_mode' : 'dark_mode';
  V.badge();
  V.render();
})();
