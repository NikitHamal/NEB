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
/* festival decor pauses whenever it is off screen */
(function () {
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.parentElement && e.target.parentElement.classList.toggle('is-paused', !e.isIntersecting); }); });
  document.querySelectorAll('.st-decor').forEach(function (d) { io.observe(d); });
})();
