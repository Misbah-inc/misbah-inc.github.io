(function () {
  var KEY = 'misbah-theme';
  var root = document.documentElement;

  function apply(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem(KEY, t); } catch (e) {}
    document.querySelectorAll('.theme-toggle').forEach(function (btn) {
      btn.setAttribute('aria-label', t === 'light' ? 'Switch to dark mode' : 'Switch to light mode');
    });
  }

  // Apply saved preference immediately (before paint)
  var saved = '';
  try { saved = localStorage.getItem(KEY) || ''; } catch (e) {}
  if (saved === 'light' || saved === 'dark') apply(saved);
  else {                                   // no saved choice: the page's own default (light) stays; just keep the button label right
    var cur = root.getAttribute('data-theme') || 'light', labels = function () {
      document.querySelectorAll('.theme-toggle').forEach(function (b) { b.setAttribute('aria-label', cur === 'light' ? 'Switch to dark mode' : 'Switch to light mode'); });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', labels); else labels();
  }

  // Toggle on click
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.theme-toggle');
    if (!btn) return;
    apply(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
  });
})();

/* Text size: A− / A+ beside the theme button on every page. The page content scales (CSS zoom on <main>; the header and footer keep their size so the bar never overflows), the choice is remembered. */
(function () {
  var KEY = 'misbah-fs', STEPS = [0.9, 1, 1.12, 1.25, 1.4, 1.6], root = document.documentElement;
  var LBL = { en: ['Smaller text', 'Larger text'], ar: ['تصغير الخط', 'تكبير الخط'], fa: ['کوچک‌تر کردن متن', 'بزرگ‌تر کردن متن'], ur: ['متن چھوٹا کریں', 'متن بڑا کریں'] };
  function maxStep() { return window.innerWidth < 768 ? STEPS.length - 2 : STEPS.length - 1; }   // on a phone 160% would push the page wider than the screen
  var i = 1;
  try { var s = parseInt(localStorage.getItem(KEY), 10); if (s >= 0 && s < STEPS.length) i = Math.min(s, top()); } catch (e) {}
  function apply() { root.style.setProperty('--fs', STEPS[i]); try { localStorage.setItem(KEY, i); } catch (e) {} sync(); }
  function sync() {
    document.querySelectorAll('.fs-ctl').forEach(function (c) {
      c.querySelector('[data-fs="-1"]').disabled = i === 0; c.querySelector('[data-fs="1"]').disabled = i >= top();
    });
  }
  if (i !== 1) root.style.setProperty('--fs', STEPS[i]);
  function build() {
    var l = LBL[root.getAttribute('lang')] || LBL.en;
    document.querySelectorAll('.theme-toggle').forEach(function (t) {
      if (t.nextElementSibling && t.nextElementSibling.classList.contains('fs-ctl')) return;
      var c = document.createElement('span'); c.className = 'fs-ctl'; c.setAttribute('role', 'group');
      c.innerHTML = '<button type="button" data-fs="-1" aria-label="' + l[0] + '">A<small>−</small></button><button type="button" data-fs="1" aria-label="' + l[1] + '">A<small>+</small></button>';
      t.parentNode.insertBefore(c, t.nextSibling);
    });
    sync();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.fs-ctl button'); if (!b) return;
    i = Math.max(0, Math.min(top(), i + parseInt(b.getAttribute('data-fs'), 10))); apply();
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
