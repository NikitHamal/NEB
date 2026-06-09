(function() {
  var actions = {};

  function getActionEl(el) {
    var current = el;
    while (current && current !== document.body) {
      if (current.dataset) {
        // data-action-stop must be checked first so modal/sheet cards can
        // prevent backdrop actions from intercepting nested links, radio
        // buttons, and follower cards.
        if (current.dataset.actionStop !== undefined) return null;
        if (current.dataset.action && current.tagName !== 'FORM') return current;
      }
      current = current.parentElement;
    }
    return null;
  }

  document.addEventListener('click', function(e) {
    var el = getActionEl(e.target);
    if (!el) return;
    var action = el.dataset.action;
    if (actions[action]) {
      e.preventDefault();
      actions[action](el, e);
    }
  });

  document.addEventListener('submit', function(e) {
    var form = e.target;
    if (form && form.dataset && form.dataset.action) {
      var action = form.dataset.action;
      if (actions[action]) {
        e.preventDefault();
        actions[action](form, e);
      }
    }
  });

  document.addEventListener('keydown', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.keydownAction) {
      var action = el.dataset.keydownAction;
      if (actions[action]) {
        actions[action](el, e);
      }
    }
  });

  document.addEventListener('change', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.changeAction) {
      var action = el.dataset.changeAction;
      if (actions[action]) {
        actions[action](el, e);
      }
    }
  });

  document.addEventListener('focusin', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.focusAction) {
      var action = el.dataset.focusAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('focusout', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.blurAction) {
      var action = el.dataset.blurAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('mousedown', function(e) {
    var el = getActionEl(e.target);
    if (!el) return;
    var action = el.dataset.mousedownAction;
    if (action && actions[action]) {
      actions[action](el, e);
    }
  });

  document.addEventListener('mouseover', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.hoverAction) {
      var action = el.dataset.hoverAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('error', function(e) {
    var img = e.target;
    if (img && img.tagName === 'IMG' && img.dataset.fallback) {
      img.style.display = 'none';
      var next = img.nextElementSibling;
      if (next) next.style.display = img.dataset.fallback || 'inline-flex';
    }
  }, true);

  window.registerAction = function(name, fn) {
    actions[name] = fn;
  };

  window.registerActions = function(map) {
    for (var key in map) {
      if (map.hasOwnProperty(key)) actions[key] = map[key];
    }
  };
})();