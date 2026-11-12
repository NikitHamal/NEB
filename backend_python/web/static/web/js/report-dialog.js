/* Report dialog. One dialog for every page: window.openReportDialog(targetType, targetId).
   Built on the shared NebUI scrim/dialog (bottom sheet on phones, keyboard-aware), reasons are a
   radio group of chips, details are a plain field. No native select, no inline styles.
   Callers: forum, forum_post, home, search, subject_page (they all go through window.openReportDialog). */
(function () {
  'use strict';

  var REASONS = [
    ['spam', 'Spam', 'block'],
    ['abuse', 'Abuse or harassment', 'report'],
    ['inappropriate', 'Inappropriate', 'visibility_off'],
    ['misinformation', 'Misinformation', 'fact_check'],
    ['other', 'Other', 'more_horiz']
  ];

  var scrim = null, target = null, reason = 'other', busy = false;

  function csrf() {
    var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    if (m) return decodeURIComponent(m[1]);
    return typeof window.CSRF_TOKEN === 'string' ? window.CSRF_TOKEN : '';
  }

  function build() {
    if (scrim) return scrim;
    scrim = document.createElement('div');
    scrim.className = 'neb-scrim';
    scrim.id = 'global-report-modal';
    scrim.hidden = true;
    scrim.innerHTML =
      '<div class="neb-dialog fp-dialog rp-dialog" role="dialog" aria-modal="true" aria-labelledby="rpTitle">' +
        '<div class="neb-dialog-head"><h2 class="neb-dialog-title" id="rpTitle">Report</h2></div>' +
        '<div class="fp-dialog-body">' +
          '<div class="rp-reasons" role="radiogroup" aria-labelledby="rpTitle">' +
            REASONS.map(function (r) {
              return '<button type="button" class="rp-reason" role="radio" aria-checked="false" data-reason="' + r[0] + '">' +
                '<span class="material-symbols-outlined" aria-hidden="true">' + r[2] + '</span>' + r[1] + '</button>';
            }).join('') +
          '</div>' +
          '<textarea id="global-report-description" data-neb-skip="1" maxlength="1600" rows="4" aria-label="Details" placeholder="Details"></textarea>' +
          '<p class="rp-error" id="global-report-error" role="alert" hidden></p>' +
        '</div>' +
        '<div class="neb-dialog-actions">' +
          '<button type="button" class="md-btn md-btn-text" data-neb-close>Cancel</button>' +
          '<button type="button" class="md-btn md-btn-error" id="global-report-submit" data-rp-submit>Report</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(scrim);
    scrim.addEventListener('click', function (e) {
      if (e.target === scrim || e.target.closest('[data-neb-close]')) { close(); return; }
      var chip = e.target.closest('.rp-reason');
      if (chip) { choose(chip.getAttribute('data-reason')); return; }
      if (e.target.closest('[data-rp-submit]')) submit();
    });
    return scrim;
  }

  function choose(key) {
    reason = key;
    scrim.querySelectorAll('.rp-reason').forEach(function (c) {
      c.setAttribute('aria-checked', String(c.getAttribute('data-reason') === key));
    });
  }

  function showError(msg) {
    var el = document.getElementById('global-report-error');
    el.textContent = msg || 'Could not send the report.';
    el.hidden = false;
  }

  function open(targetType, targetId) {
    target = { targetType: targetType, targetId: targetId };
    build();
    choose('other');
    document.getElementById('global-report-description').value = '';
    document.getElementById('global-report-error').hidden = true;
    if (window.NebUI) window.NebUI.open(scrim); else scrim.hidden = false;
  }

  function close() {
    if (!scrim) return;
    if (window.NebUI) window.NebUI.close(scrim); else scrim.hidden = true;
    target = null;
  }

  function submit() {
    if (!target || busy) return;
    var btn = document.getElementById('global-report-submit');
    busy = true; btn.disabled = true; btn.textContent = 'Sending';
    fetch('/ajax/report/', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({
        target_type: target.targetType,
        target_id: target.targetId,
        reason: reason,
        description: document.getElementById('global-report-description').value.trim(),
        context_path: location.pathname + location.search + location.hash
      })
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        if (!res.ok || res.d.error) throw new Error(res.d.error || 'Could not send the report.');
        close();
        if (typeof window.showSnackbar === 'function') window.showSnackbar('Report sent');
      })
      .catch(function (err) { showError(err && err.message); })
      .then(function () { busy = false; btn.disabled = false; btn.textContent = 'Report'; });
  }

  window.openReportDialog = open;
  window.closeReportDialog = close;
  window.reportContent = open;
})();
