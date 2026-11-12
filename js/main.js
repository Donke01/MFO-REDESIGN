// Missions for Orphans — site behaviour (no dependencies)

// Mobile menu: opens an indigo panel under the floating bar; X, Escape or a link closes it
const toggle = document.querySelector('.menu-toggle');
const nav = document.getElementById('site-nav');
if (toggle && nav) {
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    document.documentElement.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  toggle.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); toggle.focus(); } });
  matchMedia('(min-width: 1081px)').addEventListener('change', (e) => { if (e.matches) setMenu(false); });
  addEventListener('pageshow', () => setMenu(false));
  document.addEventListener('click', (e) => { if (nav.classList.contains('open') && !nav.contains(e.target) && !toggle.contains(e.target)) setMenu(false); });
}

// Photo lightbox for mission galleries
const box = document.querySelector('.lightbox');
if (box) {
  const img = box.querySelector('img');
  document.querySelectorAll('.gallery button, .mc-ph').forEach((btn) => {
    btn.addEventListener('click', () => {
      const thumb = btn.querySelector('img');
      img.src = btn.dataset.full || thumb.src;
      img.alt = thumb.alt;
      box.showModal();
    });
  });
  box.querySelector('button').addEventListener('click', () => box.close());
  box.addEventListener('click', (e) => { if (e.target === box) box.close(); });
}

// YouTube: load the player only when someone presses play
document.querySelectorAll('.video-frame[data-youtube]').forEach((frame) => {
  const btn = frame.querySelector('button');
  btn.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${frame.dataset.youtube}?autoplay=1&rel=0`;
    iframe.title = btn.getAttribute('aria-label') || 'Video';
    iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    frame.replaceChildren(iframe);
  });
});

// Contact form: posts to the endpoint set in data-endpoint (e.g. Formspree or a WordPress handler)
const form = document.querySelector('.form[data-endpoint]');
if (form) {
  const status = form.querySelector('.form-status');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const endpoint = form.dataset.endpoint;
    if (!endpoint) {
      status.textContent = 'This form is not connected yet. Please call 602-616-5557.';
      return;
    }
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    status.textContent = 'Sending…';
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form),
      });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      status.textContent = 'Message sent. We will get back to you soon.';
    } catch {
      status.textContent = 'Your message did not send. Check your connection and try again, or call 602-616-5557.';
    } finally {
      btn.disabled = false;
    }
  });
}

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
