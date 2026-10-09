/* ============================================================
   MISBAH INC. — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Mobile Hamburger ──────────────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open);
    });

    // Close menu when a nav link is clicked (mobile)
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', false);
      });
    });
  }

  /* ── Dropdown Menus (click on mobile, hover+delay on desktop) ── */
  document.querySelectorAll('.nav-dropdown').forEach(dd => {
    const trigger = dd.querySelector('.nav-link');
    const panel   = dd.querySelector('.dropdown-panel');
    const arrow   = dd.querySelector('.dropdown-arrow');
    let closeTimer;

    const openDd = () => {
      clearTimeout(closeTimer);
      dd.classList.add('open');
      if (arrow) arrow.classList.add('up');
    };
    const scheduleDdClose = () => {
      closeTimer = setTimeout(() => {
        dd.classList.remove('open');
        if (arrow) arrow.classList.remove('up');
      }, 200);
    };

    // Desktop: hover with delay so diagonal mouse movement works
    dd.addEventListener('mouseenter', openDd);
    dd.addEventListener('mouseleave', scheduleDdClose);
    if (panel) {
      panel.addEventListener('mouseenter', () => clearTimeout(closeTimer));
      panel.addEventListener('mouseleave', scheduleDdClose);
    }

    // Mobile: click to toggle
    if (trigger) {
      trigger.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          const open = dd.classList.toggle('open');
          if (arrow) arrow.classList.toggle('up', open);
        }
      });
    }
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.open').forEach(dd => {
        dd.classList.remove('open');
        const arrow = dd.querySelector('.dropdown-arrow');
        if (arrow) arrow.classList.remove('up');
      });
    }
  });

  /* ── Sticky nav shadow on scroll ─────────────────────── */
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.style.boxShadow = window.scrollY > 10
        ? '0 2px 24px rgba(0,0,0,0.45)'
        : '0 2px 16px rgba(0,0,0,0.35)';
    }, { passive: true });
  }

  /* ── Social Channel Dropdowns (WhatsApp / Telegram) ─── */
  document.querySelectorAll('.social-dropdown').forEach(dd => {
    const btn  = dd.querySelector('.social-btn');
    const menu = dd.querySelector('.social-menu');
    if (!btn || !menu) return;
    let closeTimer;
    const openMenu  = () => { clearTimeout(closeTimer); menu.classList.add('open'); btn.setAttribute('aria-expanded', true); };
    const scheduleClose = () => {
      closeTimer = setTimeout(() => {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', false);
      }, 400);
    };
    dd.addEventListener('mouseenter', openMenu);
    dd.addEventListener('mouseleave', scheduleClose);
    // Keep open while hovering the menu itself (it overflows the container)
    menu.addEventListener('mouseenter', () => clearTimeout(closeTimer));
    menu.addEventListener('mouseleave', scheduleClose);
    // Also support tap on mobile
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.social-menu.open').forEach(m => {
      m.classList.remove('open');
      m.closest('.social-dropdown')?.querySelector('.social-btn')?.setAttribute('aria-expanded', false);
    });
  });

  /* ── Smooth anchor scroll ─────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = document.querySelector('.site-header')?.offsetHeight || 64;
        window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
      }
    });
  });

  /* ── Active language highlight (by hreflang: the links point at the same page in each language) ── */
  const pathLang = ['ar', 'fa', 'ur'].indexOf(location.pathname.split('/')[1]) >= 0 ? location.pathname.split('/')[1] : 'en';
  document.querySelectorAll('.lang-sw a').forEach(a => {
    a.classList.toggle('active', a.getAttribute('hreflang') === pathLang);
  });


  /* ── Topics slider ───────────────────────────────────── */
  document.querySelectorAll('[data-carousel]').forEach(function (c) {
    var track = c.querySelector('.topic-track'), prev = c.querySelector('.tc-prev'), next = c.querySelector('.tc-next'), dots = c.querySelector('.tc-dots');
    var cards = track.children, rtl = getComputedStyle(track).direction === 'rtl';
    function gap() { return parseFloat(getComputedStyle(track).columnGap) || 24; }
    function step() { return cards[0].offsetWidth + gap(); }
    function visible() { return Math.max(1, Math.round((track.clientWidth + gap()) / step())); }
    function pos() { return Math.abs(track.scrollLeft); }
    function max() { return track.scrollWidth - track.clientWidth; }
    function pages() { return Math.max(1, Math.ceil(cards.length / visible())); }
    function build() {
      dots.innerHTML = '';
      for (var i = 0; i < pages(); i++) (function (i) {
        var b = document.createElement('button'); b.type = 'button'; b.tabIndex = -1;
        b.addEventListener('click', function () { track.scrollTo({ left: (rtl ? -1 : 1) * Math.min(i * visible() * step(), max()), behavior: 'smooth' }); });
        dots.appendChild(b);
      })(i);
    }
    function update() {
      var over = max() > 4;
      c.classList.toggle('has-overflow', over);
      if (!over) return;
      prev.disabled = pos() <= 4; next.disabled = pos() >= max() - 4;
      var n = dots.children.length, k = max() ? Math.round(pos() / max() * (n - 1)) : 0;
      for (var i = 0; i < n; i++) dots.children[i].classList.toggle('on', i === k);
    }
    function go(dir) { track.scrollBy({ left: (rtl ? -1 : 1) * dir * visible() * step(), behavior: 'smooth' }); }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', function () { build(); update(); });
    // which cards are on screen (dims the rest) and the first-visit hint on the "next" button
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.target.classList.toggle('in-view', e.intersectionRatio >= 0.6); });
        c.classList.add('io-ready');     // dim only once we know which cards are visible (no flash on load)
      }, { root: track, threshold: [0, 0.6, 1] });
      Array.prototype.forEach.call(cards, function (el) { io.observe(el); });
    } else { Array.prototype.forEach.call(cards, function (el) { el.classList.add('in-view'); }); }
    function stopPulse() { next.classList.remove('pulse'); }
    next.classList.add('pulse');
    next.addEventListener('click', stopPulse); prev.addEventListener('click', stopPulse);
    track.addEventListener('scroll', function () { if (pos() > 8) stopPulse(); }, { passive: true });
    build(); update();
  });

  /* ── Liquid glass: refraction filters (Chromium-class engines; other browsers keep the plain frosted look) ── */
  try {
    if (window.CSS && CSS.supports && CSS.supports('backdrop-filter', 'url(#glass-lens) blur(2px)')) {
      var svg = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' +
        '<filter id="glass-lens" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.018 0.03" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter>' +
        '<filter id="glass-lens-soft" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.006 0.012" numOctaves="2" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="26" xChannelSelector="R" yChannelSelector="G"/></filter></svg>';
      document.body.insertAdjacentHTML('afterbegin', svg);
      document.documentElement.classList.add('glass-lens');
    }
  } catch (e) {}

  /* ── Liquid glass bar: refraction at the rim (Chromium), a moving highlight, and a body that reacts to scrolling ─────────────
     The bar is a lens: content passing underneath bends near its edge (an SVG displacement map drawn to the bar's exact size, used
     as a backdrop filter — only Chromium-based browsers allow that; Safari/Firefox keep the frosted blur). On top of that, in
     every browser: a specular highlight that follows the pointer / scroll position, and a small elastic squash-and-stretch when you
     scroll fast, as on iOS. Everything is skipped for visitors who asked for reduced motion. */
  (function () {
    var bar = document.querySelector('.site-header');
    if (!bar) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var lens = document.documentElement.classList.contains('glass-lens');

    /* 1. refraction map for the bar's current size */
    var svgNS = 'http://www.w3.org/2000/svg', filt = null, feImg = null, feDisp = null, lastKey = '';
    function mapFor(w, h, radius, bezel) {
      var c = document.createElement('canvas'); c.width = w; c.height = h;
      var g = c.getContext('2d'), img = g.createImageData(w, h), d = img.data, hw = w / 2, hh = h / 2;
      for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) {
        var px = x + 0.5 - hw, py = y + 0.5 - hh;
        var qx = Math.abs(px) - (hw - radius), qy = Math.abs(py) - (hh - radius);
        var ox = Math.max(qx, 0), oy = Math.max(qy, 0);
        var dist = Math.sqrt(ox * ox + oy * oy) + Math.min(Math.max(qx, qy), 0) - radius;   // < 0 inside
        var depth = -dist, i = (y * w + x) * 4, dx = 0, dy = 0;
        if (depth < bezel && depth >= 0) {
          var t = 1 - depth / bezel, m = t * t * (3 - 2 * t);                               // strongest at the very edge
          var nx, ny;
          if (qx > 0 || qy > 0) { var l = Math.sqrt(ox * ox + oy * oy) || 1; nx = Math.sign(px) * ox / l; ny = Math.sign(py) * oy / l; }
          else if (qx > qy) { nx = Math.sign(px); ny = 0; } else { nx = 0; ny = Math.sign(py); }
          dx = -nx * m; dy = -ny * m;                                                        // pull content in from inside the rim
        }
        d[i] = 128 + 127 * dx; d[i + 1] = 128 + 127 * dy; d[i + 2] = 128; d[i + 3] = 255;
      }
      g.putImageData(img, 0, 0); return c.toDataURL('image/png');
    }
    function buildFilter() {
      if (!lens) return;
      var r = bar.getBoundingClientRect(), w = Math.round(r.width), h = Math.round(r.height);
      if (!w || !h) return;
      var radius = parseFloat(getComputedStyle(bar).borderTopLeftRadius) || h / 2, key = w + 'x' + h + 'x' + radius;
      if (key === lastKey) return; lastKey = key;
      if (!filt) {
        var svg = document.createElementNS(svgNS, 'svg'); svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true');
        svg.style.position = 'absolute';
        filt = document.createElementNS(svgNS, 'filter'); filt.setAttribute('id', 'lg-bar'); filt.setAttribute('filterUnits', 'userSpaceOnUse'); filt.setAttribute('primitiveUnits', 'userSpaceOnUse');
        filt.setAttribute('color-interpolation-filters', 'sRGB');
        feImg = document.createElementNS(svgNS, 'feImage'); feImg.setAttribute('preserveAspectRatio', 'none'); feImg.setAttribute('result', 'map'); feImg.setAttribute('x', '0'); feImg.setAttribute('y', '0');
        feDisp = document.createElementNS(svgNS, 'feDisplacementMap'); feDisp.setAttribute('in', 'SourceGraphic'); feDisp.setAttribute('in2', 'map'); feDisp.setAttribute('xChannelSelector', 'R'); feDisp.setAttribute('yChannelSelector', 'G');
        filt.appendChild(feImg); filt.appendChild(feDisp); svg.appendChild(filt); document.body.appendChild(svg);
      }
      filt.setAttribute('x', '0'); filt.setAttribute('y', '0'); filt.setAttribute('width', w); filt.setAttribute('height', h);
      feImg.setAttribute('width', w); feImg.setAttribute('height', h);
      var bezel = Math.min(26, h * 0.42);
      feImg.setAttribute('href', mapFor(w, h, Math.min(radius, h / 2), bezel));
      feDisp.setAttribute('scale', String(Math.round(bezel * 1.7)));
      bar.classList.add('lg-ready');
    }
    buildFilter();
    var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(buildFilter, 150); });

    /* 2. scrolled state + elastic body + highlight angle */
    var lastY = window.scrollY, sx = 1, sy = 1, tx = 1, ty = 1, raf = 0;
    function frame() {
      sx += (tx - sx) * 0.18; sy += (ty - sy) * 0.18;
      bar.style.setProperty('--lg-sx', sx.toFixed(4)); bar.style.setProperty('--lg-sy', sy.toFixed(4));
      tx += (1 - tx) * 0.12; ty += (1 - ty) * 0.12;                      // relax back to rest
      if (Math.abs(sx - 1) > 0.0005 || Math.abs(sy - 1) > 0.0005 || Math.abs(tx - 1) > 0.0005) raf = requestAnimationFrame(frame); else { raf = 0; bar.style.removeProperty('--lg-sx'); bar.style.removeProperty('--lg-sy'); }
    }
    window.addEventListener('scroll', function () {
      var y = window.scrollY, v = y - lastY; lastY = y;
      bar.classList.toggle('is-scrolled', y > 8);
      bar.style.setProperty('--lg-shine', ((y / 5) % 100).toFixed(1) + '%');           // the highlight drifts as the page moves
      if (reduce) return;
      var k = Math.min(Math.abs(v) / 60, 1);                                              // fast scroll -> stretch wider, squash lower
      tx = 1 + 0.012 * k; ty = 1 - 0.05 * k;
      if (!raf) raf = requestAnimationFrame(frame);
    }, { passive: true });
    bar.classList.toggle('is-scrolled', window.scrollY > 8);

    /* 3. pointer-following specular highlight */
    if (!reduce) bar.addEventListener('pointermove', function (e) {
      var r = bar.getBoundingClientRect();
      bar.style.setProperty('--lg-mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
      bar.style.setProperty('--lg-my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
    }, { passive: true });
  })();

});
