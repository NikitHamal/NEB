(function () {
  'use strict';
  function init(root) {
    root.querySelectorAll('[data-syllabus-search]:not([data-ready])').forEach(function (input) {
      input.dataset.ready = 'true';
      input.addEventListener('input', function () {
        var query = input.value.trim().toLocaleLowerCase();
        var catalogue = input.closest('.syllabus-catalogue');
        var count = 0;
        catalogue.querySelectorAll('[data-syllabus-grade]').forEach(function (grade) {
          var visible = 0;
          grade.querySelectorAll('[data-syllabus-subject]').forEach(function (subject) {
            subject.hidden = !subject.dataset.search.toLocaleLowerCase().includes(query);
            if (!subject.hidden) visible++;
          });
          grade.hidden = visible === 0;
          count += visible;
        });
        catalogue.querySelector('[data-syllabus-empty]').hidden = count > 0;
      });
    });
    var tools = Array.from(root.querySelectorAll('[data-study-chapter]:not([data-ready])'));
    if (!tools.length) return;
    var key = 'nebians.syllabus.v1.' + tools[0].dataset.studySubject;
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(key) || '{}'); } catch (_) {}
    if (!saved || typeof saved !== 'object' || Array.isArray(saved)) saved = {};
    function refresh() {
      var count = tools.filter(function (tool) { return saved[tool.dataset.studyChapter] === true; }).length;
      tools.forEach(function (tool) {
        var done = saved[tool.dataset.studyChapter] === true;
        tool.querySelector('[data-study-done]').checked = done;
        tool.querySelector('progress').value = count * 100 / tools.length;
        var label = count + ' / ' + tools.length + (tool.lang === 'ne' ? ' पाठ' : ' chapters');
        if (tool.lang === 'ne') label = label.replace(/[0-9]/g, function (n) { return '०१२३४५६७८९'[n]; });
        tool.querySelector('[data-study-count]').textContent = label;
        document.querySelectorAll('.sidebar-nav-item').forEach(function (nav) {
          if (nav.dataset.chapterId === tool.dataset.studyChapter) nav.dataset.revised = String(done);
        });
      });
    }
    tools.forEach(function (tool, index) {
      tool.dataset.ready = 'true';
      tool.querySelector('input').addEventListener('change', function (e) {
        saved[tool.dataset.studyChapter] = e.target.checked;
        try { localStorage.setItem(key, JSON.stringify(saved)); } catch (_) {}
        refresh();
      });
      var pane = tool.closest('.chapter-content-pane');
      function navigate(offset) {
        var next = tools[index + offset];
        if (!next) return;
        var nav = Array.from(document.querySelectorAll('.sidebar-nav-item')).find(function (n) { return n.dataset.chapterId === next.dataset.studyChapter; });
        if (nav) { nav.click(); document.querySelector('.subject-viewer').scrollIntoView({block: 'start'}); }
      }
      pane.querySelector('[data-study-prev]').disabled = index === 0;
      pane.querySelector('[data-study-next]').disabled = index === tools.length - 1;
      pane.querySelector('[data-study-prev]').addEventListener('click', function () { navigate(-1); });
      pane.querySelector('[data-study-next]').addEventListener('click', function () { navigate(1); });
    });
    refresh();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(document); });
  else init(document);
  document.addEventListener('htmx:afterSwap', function () { init(document); });
}());
