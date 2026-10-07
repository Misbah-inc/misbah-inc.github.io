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
