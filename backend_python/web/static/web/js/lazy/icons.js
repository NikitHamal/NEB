(function(window){
"use strict";

var Icons = {
  svg: function(content, opts) {
    opts = opts || {};
    var size = opts.size || 16;
    var sw = opts.strokeWidth || 1.8;
    var cls = opts.className ? ' class="' + opts.className + '"' : '';
    var fill = opts.fill || "none";
    var stroke = opts.stroke || "currentColor";
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="' + fill + '" stroke="' + stroke + '" stroke-width="' + sw + '" stroke-linecap="round" stroke-linejoin="round"' + cls + ' aria-hidden="true">' + content + '</svg>';
  },
  home: function(o){ return Icons.svg('<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>', o); },
  chat: function(o){ return Icons.svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', o); },
  plus: function(o){ return Icons.svg('<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>', o); },
  search: function(o){ return Icons.svg('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>', o); },
  chevronDown: function(o){ return Icons.svg('<polyline points="6 9 12 15 18 9"/>', o); },
  chevronRight: function(o){ return Icons.svg('<polyline points="9 18 15 12 9 6"/>', o); },
  chevronLeft: function(o){ return Icons.svg('<polyline points="15 18 9 12 15 6"/>', o); },
  close: function(o){ return Icons.svg('<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>', o); },
  trash: function(o){ return Icons.svg('<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>', o); },
  send: function(o){ return Icons.svg('<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>', o); },
  stop: function(o){ return Icons.svg('<rect x="6" y="6" width="12" height="12" rx="2"/>', Object.assign({fill:"currentColor"}, o)); },
  clip: function(o){ return Icons.svg('<path d="m21.4 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>', o); },
  sparkle: function(o){ return Icons.svg('<path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/>', Object.assign({fill:"currentColor"}, o)); },
  doc: function(o){ return Icons.svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>', o); },
  table: function(o){ return Icons.svg('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>', o); },
  check: function(o){ return Icons.svg('<polyline points="20 6 9 17 4 12"/>', o); },
  copy: function(o){ return Icons.svg('<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>', o); },
  download: function(o){ return Icons.svg('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>', o); },
  sidebarToggle: function(o){ return Icons.svg('<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/>', o); },
  user: function(o){ return Icons.svg('<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>', o); },
  shuffle: function(o){ return Icons.svg('<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/>', o); },
  globe: function(o){ return Icons.svg('<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>', o); },
  tasks: function(o){ return Icons.svg('<path d="M11 6h9M11 12h9M11 18h9M4 6l1.5 1.5L8 5M4 12l1.5 1.5L8 11M4 18l1.5 1.5L8 17"/>', o); },
  terminal: function(o){ return Icons.svg('<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>', o); },
  edit: function(o){ return Icons.svg('<path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/>', o); },
  filter: function(o){ return Icons.svg('<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>', o); },
  refresh: function(o){ return Icons.svg('<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>', o); },
  menu: function(o){ return Icons.svg('<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>', o); },
  sun: function(o){ return Icons.svg('<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>', o); },
  moon: function(o){ return Icons.svg('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>', o); }
};

window.LazyIcons = Icons;
})(window);
