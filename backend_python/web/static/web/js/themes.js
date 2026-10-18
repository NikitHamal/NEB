// Season card: closing it keeps it closed for this theme (until the next festival).
(function () {
  var card = document.querySelector('[data-st-card]');
  if (!card) return;
  var key = 'st-card-closed:' + card.getAttribute('data-st-card') + ':' + new Date().getFullYear();
  try { if (localStorage.getItem(key)) { card.hidden = true; return; } } catch (e) {}
  var close = card.querySelector('[data-st-close]');
  if (!close) return;
  close.addEventListener('click', function () {
    try { localStorage.setItem(key, '1'); } catch (e) {}
    card.classList.add('is-leaving');
    setTimeout(function () { card.hidden = true; }, 320);
  });
})();
