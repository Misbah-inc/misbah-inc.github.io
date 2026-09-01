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

  /* ── Dropdown Menus (click on mobile, hover on desktop) ── */
  document.querySelectorAll('.nav-dropdown').forEach(dd => {
    const trigger = dd.querySelector('.nav-link');
    const arrow   = dd.querySelector('.dropdown-arrow');

    if (trigger) {
      trigger.addEventListener('click', (e) => {
        // Only use click behaviour on mobile (nav-links is open)
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

  /* ── Donation Frequency Tabs ──────────────────────────── */
  const freqTabs = document.querySelectorAll('.freq-tab');
  freqTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      freqTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      updateDonateBtn();
    });
  });

  /* ── Donation Amount Buttons ──────────────────────────── */
  const amtBtns      = document.querySelectorAll('.amt-btn');
  const customInput  = document.getElementById('custom-amount');
  const donateBtn    = document.getElementById('donate-btn');

  let selectedAmt = 50; // default

  amtBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      amtBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedAmt = parseInt(btn.dataset.amount, 10);
      if (customInput) customInput.value = '';
      updateDonateBtn();
    });
  });

  if (customInput) {
    customInput.addEventListener('input', () => {
      amtBtns.forEach(b => b.classList.remove('active'));
      selectedAmt = parseInt(customInput.value, 10) || 0;
      updateDonateBtn();
    });
  }

  function updateDonateBtn() {
    if (!donateBtn) return;
    const freq    = document.querySelector('.freq-tab.active')?.textContent?.trim() || 'One Time';
    const amount  = customInput?.value || selectedAmt;
    const label   = isNaN(amount) || amount <= 0 ? 'Donate' : `Donate $${amount} — ${freq}`;
    donateBtn.textContent = label;
  }

  // Set default active amount button
  const defaultBtn = document.querySelector('.amt-btn[data-amount="50"]');
  if (defaultBtn) defaultBtn.classList.add('active');
  updateDonateBtn();

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
      }, 280);
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

  /* ── Prayer Times ────────────────────────────────────── */
  (function () {
    const locBtn      = document.getElementById('prayer-locate-btn');
    const locLabel    = document.getElementById('prayer-locate-label');
    const cityEl      = document.getElementById('prayer-city');
    const grid        = document.getElementById('prayer-grid');
    const methodSel   = document.getElementById('prayer-method-select');
    if (!locBtn || !grid) return;
    let _lastLat = null, _lastLon = null;

    const PRAYERS = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];
    const NEXT_CANDIDATES = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

    function toMin(t) {
      const parts = (t || '').split(':');
      return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
    }

    function fmt12(t) {
      const parts = (t || '').split(':');
      let h = parseInt(parts[0], 10), m = parseInt(parts[1], 10);
      const ampm = h >= 12 ? 'PM' : 'AM';
      h = h % 12 || 12;
      return h + ':' + String(m).padStart(2, '0') + ' ' + ampm;
    }

    function renderTimes(timings, city) {
      const now = new Date();
      const nowMin = now.getHours() * 60 + now.getMinutes();
      let nextKey = null;
      for (const k of NEXT_CANDIDATES) {
        if (toMin(timings[k]) > nowMin) { nextKey = k; break; }
      }
      if (!nextKey) nextKey = 'Fajr';

      const html = PRAYERS.map(k => {
        const isNext = k === nextKey;
        return `<div class="prayer-card${isNext ? ' next-prayer' : ''}">
          <div class="prayer-name">${k}</div>
          <div class="prayer-time">${fmt12(timings[k])}</div>
          ${isNext ? '<div class="prayer-next-tag">▲ Next</div>' : ''}
        </div>`;
      }).join('');

      grid.innerHTML = `<div class="prayer-grid-times">${html}</div>`;
      if (cityEl && city) cityEl.textContent = city;
    }

    function loadTimes(lat, lon) {
      _lastLat = lat; _lastLon = lon;
      const method = methodSel ? methodSel.value : '0';
      // Fetch prayer times and reverse-geocode city name in parallel
      Promise.all([
        fetch('https://api.aladhan.com/v1/timings?latitude=' + lat + '&longitude=' + lon + '&method=' + method).then(r => r.json()),
        fetch('https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=' + lat + '&longitude=' + lon + '&localityLanguage=en').then(r => r.json()).catch(() => ({}))
      ]).then(([prayer, geo]) => {
        if (prayer.code === 200) {
          const city = geo.locality || geo.city || geo.principalSubdivision || '';
          renderTimes(prayer.data.timings, city);
          locLabel.textContent = 'Update Location';
        } else {
          locLabel.textContent = 'Try Again';
        }
      }).catch(() => { locLabel.textContent = 'Try Again'; });
    }

    function requestLocation() {
      if (!navigator.geolocation) return;
      locLabel.textContent = 'Detecting…';
      navigator.geolocation.getCurrentPosition(
        pos => {
          const { latitude: lat, longitude: lon } = pos.coords;
          try { localStorage.setItem('misbah_lat', lat); localStorage.setItem('misbah_lon', lon); } catch(e) {}
          loadTimes(lat, lon);
        },
        () => {
          locLabel.textContent = 'Detect Location';
        }
      );
    }

    locBtn.addEventListener('click', requestLocation);

    // Auto-load on page open: use cached coords instantly, then refresh
    try {
      const lat = parseFloat(localStorage.getItem('misbah_lat'));
      const lon = parseFloat(localStorage.getItem('misbah_lon'));
      if (lat && lon) loadTimes(lat, lon);
    } catch(e) {}
    // Always re-request in background to keep times fresh
    requestLocation();

    if (methodSel) {
      methodSel.addEventListener('change', () => {
        if (_lastLat !== null) loadTimes(_lastLat, _lastLon);
      });
    }
  })();

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

  /* ── Active language highlight ────────────────────────── */
  const langLinks = document.querySelectorAll('.lang-sw a');
  const pathLang  = location.pathname.split('/')[1]; // '' | 'ar' | 'fa' | 'ur'
  langLinks.forEach(a => {
    const href = a.getAttribute('href');
    const isActive = (pathLang === '' && href === '/') ||
                     (pathLang !== '' && href === '/' + pathLang + '/');
    a.classList.toggle('active', isActive);
  });

});
