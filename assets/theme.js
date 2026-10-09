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
