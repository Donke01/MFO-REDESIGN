/* Missions for Orphans motion: a green-to-red scroll line, cards that rise in once, numbers that count up,
   photos that shimmer until they arrive, a soft light under the pointer, and a quick fade between pages.
   Everything here is decoration: with reduced motion, or if this file fails, the pages look and work the same. */
(function () {
  var html = document.documentElement;
  // photos: stop the shimmer once each one has arrived
  function ok(im) { if (im.complete) im.classList.add('mo-ok'); }
  document.addEventListener('load', function (e) { if (e.target.tagName === 'IMG') e.target.classList.add('mo-ok'); }, true);
  document.addEventListener('error', function (e) { if (e.target.tagName === 'IMG') e.target.classList.add('mo-ok'); }, true);

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { document.querySelectorAll('img').forEach(function (im) { im.classList.add('mo-ok'); }); return; }
  html.classList.add('mo');
  document.querySelectorAll('img').forEach(ok);

  // quick fade to the next page (same-site links only)
  addEventListener('pageshow', function () { html.classList.remove('mo-leave'); });
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]'); if (!a || (a.target && a.target !== '_self') || a.hasAttribute('download')) return;
    var u; try { u = new URL(a.getAttribute('href'), location.href); } catch (x) { return; }
    if (u.origin !== location.origin || u.pathname === location.pathname) return;
    e.preventDefault(); html.classList.add('mo-leave');
    try { sessionStorage.setItem('moNav', '1'); } catch (x) {}
    setTimeout(function () { location.href = u.href; }, 170);
  });

  // scroll line
  var bar = document.createElement('div'); bar.className = 'mo-line'; bar.setAttribute('aria-hidden', 'true'); bar.innerHTML = '<i></i>';
  document.body.appendChild(bar);
  var fill = bar.firstChild, tick = false;
  function prog() { tick = false; var h = document.documentElement.scrollHeight - innerHeight; fill.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, Math.max(0, scrollY / h)) : 0) + ')'; }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(prog); } }, { passive: true });
  addEventListener('resize', prog); prog();

  // cards rise in, a little after each other
  var CARDS = '.fund,.gift,.news,.home-cta,.grow-row figure,.steps li,.pcard,.ways > div,.post-card,.tcard,.mcard,.program,.contact .block';
  var queue = [], busy = false;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); queue.push(e.target); } });
    if (!busy) { busy = true; requestAnimationFrame(flush); }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  function flush() {
    busy = false;
    queue.sort(function (a, b) { var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return (ra.top - rb.top) || (ra.left - rb.left); });
    queue.forEach(function (el, i) { el.style.setProperty('--mo-d', Math.min(i, 6) * 70 + 'ms'); el.classList.add('mo-in'); });
    queue = [];
  }
  document.querySelectorAll(CARDS).forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < innerHeight * 0.92 && r.bottom > 0) return; // already on screen: leave it
    el.classList.add('mo-pre'); io.observe(el);
  });

  // numbers count up when they come into view ($1,600, 506 widows, 190 families …)
  var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { nio.unobserve(e.target); count(e.target); } }); }, { threshold: 0.6 });
  function count(el) {
    var m = /^([^\d]*)([\d,]+)(.*)$/.exec(el.textContent); if (!m) return;
    var target = parseFloat(m[2].replace(/,/g, '')); if (!(target > 9)) return;
    var t0 = null, dur = 1100, comma = m[2].indexOf(',') >= 0;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = m[1] + (comma ? v.toLocaleString('en-US') : String(v)) + m[3];
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  document.querySelectorAll('.gift b, .program .fact b, .tally b, .stat b, .mon-cost li b').forEach(function (el) {
    var r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) return;
    nio.observe(el);
  });

  // a soft light follows the pointer over cards (mouse and trackpad)
  if (matchMedia('(hover: hover)').matches) {
    document.addEventListener('pointermove', function (e) {
      var c = e.target.closest && e.target.closest('.fund,.item,.post-card,.faces > div,.ways > div'); if (!c) return;
      var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }
})();
