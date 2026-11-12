(function () {
  var wrap = document.getElementById('sch-docs');
  var add = document.getElementById('sch-add-doc');
  if (!wrap || !add) return;
  var max = parseInt(wrap.getAttribute('data-max'), 10) || 6;

  function bind(row) {
    var input = row.querySelector('input[type="file"]');
    var label = row.querySelector('.sch-file');
    var name = row.querySelector('.sch-file-name');
    var remove = row.querySelector('.sch-doc-remove');
    input.addEventListener('change', function () {
      var f = input.files && input.files[0];
      name.textContent = f ? f.name : name.getAttribute('data-empty');
      label.classList.toggle('has-file', !!f);
    });
    remove.addEventListener('click', function () {
      row.remove();
      sync();
    });
  }

  function sync() {
    var rows = wrap.querySelectorAll('.sch-doc');
    add.hidden = rows.length >= max;
    rows.forEach(function (r, i) {
      r.querySelector('.sch-doc-remove').hidden = rows.length === 1 || i === 0;
    });
  }

  bind(wrap.querySelector('.sch-doc'));
  add.addEventListener('click', function () {
    var rows = wrap.querySelectorAll('.sch-doc');
    if (rows.length >= max) return;
    var copy = rows[0].cloneNode(true);
    copy.querySelector('input[type="file"]').value = '';
    var name = copy.querySelector('.sch-file-name');
    name.textContent = name.getAttribute('data-empty');
    copy.querySelector('.sch-file').classList.remove('has-file');
    copy.querySelector('select').selectedIndex = 0;
    wrap.appendChild(copy);
    bind(copy);
    sync();
  });
  sync();
})();
