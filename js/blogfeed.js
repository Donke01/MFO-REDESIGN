/* Lani's blog: newer posts from mfolanisblog.wordpress.com slot in before the posts that are part of this site.
   If WordPress can't be reached, the page simply keeps the posts it already shows. */
(function () {
  var boxes = document.querySelectorAll('.posts[data-feed]');
  if (!boxes.length || !window.fetch) return;
  var API = 'https://public-api.wordpress.com/rest/v1.1/sites/mfolanisblog.wordpress.com/posts/?number=12&fields=title,date,URL,excerpt,content';
  var KEY = 'mfoLaniFeed1';
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  function text(h) { var d = document.createElement('div'); d.innerHTML = h || ''; return (d.textContent || '').replace(/\s+/g, ' ').trim(); }
  function words(t, n) { var w = t.split(' '); return w.length > n ? w.slice(0, n).join(' ').replace(/[,;:.]$/, '') + '…' : t; }
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

  function card(p) {
    var a = el('a', 'post-card'); a.href = p.url; a.setAttribute('data-date', p.date.slice(0, 10)); a.setAttribute('data-wp', '1');
    var im = el('img'); im.src = p.img || 'assets/img/boys.webp'; im.alt = ''; im.loading = 'lazy'; im.width = 1400; im.height = 698;
    im.addEventListener('load', function () { im.classList.add('mo-ok'); }); im.addEventListener('error', function () { im.classList.add('mo-ok'); });
    var d = new Date(p.date.slice(0, 10) + 'T12:00:00');
    a.appendChild(im);
    a.appendChild(el('span', 'pc-date', d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear()));
    a.appendChild(el('h3', null, p.title));
    a.appendChild(el('p', null, p.excerpt));
    var by = el('span', 'byline-s'); var f = el('img'); f.src = 'assets/img/lani.webp'; f.alt = ''; f.width = 32; f.height = 32; by.appendChild(f); by.appendChild(document.createTextNode('Mama Lani')); a.appendChild(by);
    return a;
  }

  function show(posts) {
    boxes.forEach(function (box) {
      var cards = Array.prototype.slice.call(box.querySelectorAll('.post-card'));
      var have = {}; cards.forEach(function (c) { var u = c.getAttribute('data-src'); if (u) have[u.replace(/\/$/, '')] = 1; });
      posts.forEach(function (p) { if (!have[p.url.replace(/\/$/, '')]) cards.push(card(p)); }); // posts already copied into this site are skipped
      cards.sort(function (x, y) { return y.getAttribute('data-date') < x.getAttribute('data-date') ? -1 : 1; });
      var n = box.getAttribute('data-feed') === 'all' ? cards.length : parseInt(box.getAttribute('data-feed'), 10) || 3;
      box.textContent = '';
      cards.slice(0, n).forEach(function (c) { box.appendChild(c); });
    });
  }

  function tidy(list) {
    return list.filter(function (p) { return !/^hello world/i.test(text(p.title)); }).map(function (p) {
      var m = /<img[^>]+src="([^"]+)"/i.exec(p.content || '');
      return { title: text(p.title), date: p.date, url: p.URL, excerpt: words(text(p.excerpt).replace(/\[…\]|\[\.\.\.\]/g, '').trim(), 24), img: m ? m[1].split('?')[0] + '?w=800' : '' };
    });
  }

  try { var c = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (c && Date.now() - c.t < 3600e3) { show(c.p); return; } } catch (e) {}
  fetch(API).then(function (r) { if (!r.ok) throw r.status; return r.json(); }).then(function (j) {
    var p = tidy(j.posts || []);
    try { sessionStorage.setItem(KEY, JSON.stringify({ t: Date.now(), p: p })); } catch (e) {}
    show(p);
  }).catch(function () { /* keep the posts already on the page */ });
})();
