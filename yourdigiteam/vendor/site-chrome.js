/* ══════════════════════════════════════════════════════════════════
   SITE CHROME — shared header + footer for every yourdigitalteam page
   Include on a page with:
     <link rel="stylesheet" href="vendor/site-chrome.css">
     <script src="vendor/site-chrome.js" defer></script>
   Everything below is driven by the NAV / SERVICES / COMPANY maps —
   add a page there and it appears in the menu and the footer at once.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── the site map, in one place ── */
  var SERVICES = [
    { href: 'seo.html',            label: 'SEO' },
    { href: 'ppc.html',            label: 'PPC' },
    { href: 'social.html',         label: 'Social Media' },
    { href: 'email.html',          label: 'Email Marketing' },
    { href: 'content.html',        label: 'Content' },
    { href: 'index.html#foundation', label: 'Web Development' }
  ];
  var MENU = [
    { href: 'index.html',            label: 'Home' },
    { href: 'services.html',         label: 'All Services' },
    { href: 'about.html',            label: 'About' },
    { href: 'index.html#process',    label: 'Our Process' },
    { href: 'index.html#foundation', label: 'Website Builder' },
    { href: 'contact.html',          label: 'Contact' }
  ];
  var PILL_NAV = [
    { href: 'index.html#services', label: 'Services' },
    { href: 'index.html#process',  label: 'Our Process' },
    { href: 'contact.html',        label: 'Contact' }
  ];
  var COMPANY = [
    { href: 'index.html',         label: 'Home' },
    { href: 'about.html',         label: 'About' },
    { href: 'services.html',      label: 'All Services' },
    { href: 'index.html#process', label: 'Our Process' },
    { href: 'contact.html',       label: 'Contact' },
    { href: 'privacy.html',       label: 'Privacy' }
  ];

  /* Sole trader, not a limited company. UK business-names rules still require
     the proprietor's name and an address for service to be shown. */
  var TRADING_NAME = 'Your Digital Team';
  var PROPRIETOR = '';          /* TODO: your full legal name */
  var SERVICE_ADDRESS = '';     /* TODO: an address where documents can be served */
  var SOCIALS = [
    { label: 'Facebook',  href: '#', path: 'M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.8 3.7-3.8 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z' },
    { label: 'Instagram', href: '#', path: 'M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.8s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2-.1-1.3-.1-1.7-.1-4.9s0-3.5.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4 1.3-.1 1.7-.1 4.9-.1zm0 3.2A6.6 6.6 0 1 0 18.6 12 6.6 6.6 0 0 0 12 5.4zm0 10.9A4.3 4.3 0 1 1 16.3 12 4.3 4.3 0 0 1 12 16.3zm8.4-11.2a1.5 1.5 0 1 1-1.5-1.5 1.5 1.5 0 0 1 1.5 1.5z' },
    { label: 'X',         href: '#', path: 'M18.2 2.3h3.3l-7.2 8.2L22.8 22h-6.6l-5.2-6.8L5.1 22H1.8l7.7-8.8L1.5 2.3h6.8l4.7 6.2 5.2-6.2zm-1.2 17.7h1.8L7.1 4.2H5.2L17 20z' },
    { label: 'YouTube',   href: '#', path: 'M23 7.6a2.9 2.9 0 0 0-2-2.1C19.1 5 12 5 12 5s-7.1 0-8.9.5a2.9 2.9 0 0 0-2.1 2.1A30 30 0 0 0 .5 12a30 30 0 0 0 .5 4.4 2.9 2.9 0 0 0 2.1 2.1c1.8.5 8.9.5 8.9.5s7.1 0 8.9-.5a2.9 2.9 0 0 0 2.1-2.1 30 30 0 0 0 .5-4.4 30 30 0 0 0-.5-4.4zM9.8 15.3V8.7l5.7 3.3z' },
    { label: 'TikTok',    href: '#', path: 'M16.6 5.8a4.8 4.8 0 0 1-1.2-3.2h-3.3v13.1a2.7 2.7 0 1 1-1.9-2.6V9.7a5.9 5.9 0 1 0 5.2 5.9V9.2A8 8 0 0 0 20 10.7V7.5a4.8 4.8 0 0 1-3.4-1.7z' },
    { label: 'LinkedIn',  href: '#', path: 'M20.4 20.4h-3.5v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9v5.7H9.4V9h3.3v1.6h.1a3.7 3.7 0 0 1 3.3-1.8c3.6 0 4.3 2.3 4.3 5.4v6.2zM5.3 7.4a2.1 2.1 0 1 1 2.1-2.1 2.1 2.1 0 0 1-2.1 2.1zm1.8 13H3.6V9h3.5v11.4zM22.2 0H1.8A1.8 1.8 0 0 0 0 1.8v20.4A1.8 1.8 0 0 0 1.8 24h20.4a1.8 1.8 0 0 0 1.8-1.8V1.8A1.8 1.8 0 0 0 22.2 0z' }
  ];
  var EMAIL = 'thomas@yourdigiteam.com';

  /* ── which page are we on ── */
  var HERE = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  if (HERE === '') HERE = 'index.html';

  /* A link written as "index.html#services" becomes a bare "#services" when
     we are already on the home page, so in-page scrolling and the underline
     spy keep working instead of reloading the document. */
  function resolve(href) {
    var hash = href.indexOf('#');
    if (hash < 0) return href;
    var file = href.slice(0, hash).toLowerCase();
    return (file === HERE || (file === 'index.html' && HERE === 'index.html'))
      ? href.slice(hash)
      : href;
  }
  function isCurrent(href) {
    var file = href.split('#')[0].toLowerCase();
    return file !== '' && file === HERE && href.indexOf('#') < 0;
  }
  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function linkAttrs(item) {
    return 'href="' + esc(resolve(item.href)) + '"' + (isCurrent(item.href) ? ' aria-current="page"' : '');
  }

  /* ══════════ MARKUP ══════════ */
  function headerHTML() {
    return '' +
    '<div class="ydt-header__shell">' +
      '<div class="ydt-header__pill" id="ydtPill">' +
        '<div class="ydt-header__row">' +
          '<a href="' + esc(resolve('index.html#top')) + '" class="ydt-header__logo" aria-label="yourdigitalteam home">yourdigitalteam.</a>' +

          '<nav class="ydt-header__nav" aria-label="Primary navigation">' +
            '<div class="ydt-header__underline" id="ydtUnderline" aria-hidden="true"></div>' +
            PILL_NAV.map(function (n) {
              return '<a ' + linkAttrs(n) + ' class="ydt-header__nav-link">' + esc(n.label) + '</a>';
            }).join('') +
          '</nav>' +

          '<div class="ydt-header__controls">' +
            '<button class="ydt-header__grid-btn" id="ydtGridBtn" aria-expanded="false" aria-controls="ydtDropdown" aria-label="Open menu">' +
              '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
                '<rect x="2" y="2" width="8.5" height="8.5" rx="1.4"/>' +
                '<rect x="13.5" y="2" width="8.5" height="8.5" rx="1.4"/>' +
                '<rect x="2" y="13.5" width="8.5" height="8.5" rx="1.4"/>' +
                '<rect x="13.5" y="13.5" width="8.5" height="8.5" rx="1.4"/>' +
              '</svg>' +
            '</button>' +
            '<button class="ydt-header__burger" id="ydtBurger" aria-expanded="false" aria-controls="ydtDropdown" aria-label="Toggle menu">' +
              '<div class="ydt-header__icon-wrap">' +
                '<span class="ydt-header__icon ydt-header__icon--open" aria-hidden="true">' +
                  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>' +
                '</span>' +
                '<span class="ydt-header__icon ydt-header__icon--close" aria-hidden="true">' +
                  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
                '</span>' +
              '</div>' +
            '</button>' +
          '</div>' +
        '</div>' +

        '<div class="ydt-header__dropdown" id="ydtDropdown" role="menu" aria-label="Site pages">' +
          '<div class="ydt-header__dropdown-inner">' +
            '<div class="ydt-header__dropdown-links">' +
              MENU.map(function (m) {
                return '<div class="ydt-header__dropdown-item" role="none">' +
                  '<a ' + linkAttrs(m) + ' class="ydt-header__dropdown-btn" role="menuitem">' +
                    '<span class="ydt-header__dropdown-label">' + esc(m.label) + '</span>' +
                  '</a></div>';
              }).join('') +
            '</div>' +
            '<div class="ydt-header__dropdown-social" aria-label="Social links">' +
              SOCIALS.map(function (s) {
                return '<a href="' + esc(s.href) + '" class="ydt-header__social-link" aria-label="' + esc(s.label) + '">' +
                  '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="' + s.path + '"/></svg></a>';
              }).join('') +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function footerHTML() {
    function list(items) {
      return '<ul class="site-footer__list">' + items.map(function (i) {
        return '<li><a ' + linkAttrs(i) + '>' + esc(i.label) + '</a></li>';
      }).join('') + '</ul>';
    }
    return '' +
    '<div class="site-footer__inner">' +
      '<div class="site-footer__cols">' +
        '<div>' +
          '<a href="' + esc(resolve('index.html#top')) + '" class="site-footer__brand-mark">yourdigitalteam.</a>' +
          '<p class="site-footer__brand-line">Growth marketing built on measurement, not guesswork. Search, paid, social, email and content, run as one system.</p>' +
          '<a href="mailto:' + EMAIL + '" class="site-footer__mail">' + EMAIL + '</a>' +
        '</div>' +
        '<div><h2 class="site-footer__heading">Services</h2>' + list(SERVICES) + '</div>' +
        '<div><h2 class="site-footer__heading">Company</h2>' + list(COMPANY) + '</div>' +
        '<div><h2 class="site-footer__heading">Follow</h2>' +
          '<ul class="site-footer__list">' + SOCIALS.slice(0, 4).map(function (s) {
            return '<li><a href="' + esc(s.href) + '">' + esc(s.label) + '</a></li>';
          }).join('') + '</ul>' +
        '</div>' +
      '</div>' +
      '<div class="site-footer__bar">' +
        '<span class="site-footer__copy">© ' + new Date().getFullYear() + ' yourdigitalteam. ' +
          (PROPRIETOR ? esc(PROPRIETOR) + ' trading as ' + esc(TRADING_NAME) + '. ' : '') +
          (SERVICE_ADDRESS ? esc(SERVICE_ADDRESS) + '. ' : '') +
          'All rights reserved.</span>' +
        '<div class="site-footer__socials">' +
          SOCIALS.map(function (s) {
            return '<a href="' + esc(s.href) + '" aria-label="' + esc(s.label) + '">' +
              '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="' + s.path + '"/></svg></a>';
          }).join('') +
        '</div>' +
      '</div>' +
    '</div>';
  }

  /* ══════════ MOUNT ══════════ */
  function mount() {
    if (document.getElementById('ydtHeader')) return;   /* page ships its own */

    var backdrop = document.createElement('div');
    backdrop.className = 'ydt-backdrop';
    backdrop.id = 'ydtBackdrop';
    backdrop.setAttribute('aria-hidden', 'true');

    var header = document.createElement('header');
    header.className = 'ydt-header';
    header.id = 'ydtHeader';
    header.setAttribute('role', 'banner');
    header.innerHTML = headerHTML();

    document.body.insertBefore(header, document.body.firstChild);
    document.body.insertBefore(backdrop, header);

    var footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML = footerHTML();
    var slot = document.querySelector('[data-site-footer]');
    if (slot) slot.parentNode.replaceChild(footer, slot);
    else document.body.appendChild(footer);

    wire(header, backdrop);
    consentBanner();
  }

  /* ══════════ BEHAVIOUR ══════════ */
  function wire(header, backdrop) {
    var pill = header.querySelector('#ydtPill');
    var gridBtn = header.querySelector('#ydtGridBtn');
    var burger = header.querySelector('#ydtBurger');
    var dropdown = header.querySelector('#ydtDropdown');
    var underline = header.querySelector('#ydtUnderline');
    var navEl = header.querySelector('.ydt-header__nav');
    var navLinks = header.querySelectorAll('.ydt-header__nav-link');
    var isOpen = false;

    function openDropdown() {
      isOpen = true;
      header.classList.add('ydt-header--dropdown-open');
      gridBtn.setAttribute('aria-expanded', 'true');
      gridBtn.setAttribute('aria-label', 'Close menu');
      burger.setAttribute('aria-expanded', 'true');
      dropdown.style.maxHeight = dropdown.scrollHeight + 'px';
      backdrop.classList.add('ydt-backdrop--visible');
      document.body.style.overflow = 'hidden';
    }
    function closeDropdown() {
      isOpen = false;
      header.classList.remove('ydt-header--dropdown-open');
      gridBtn.setAttribute('aria-expanded', 'false');
      gridBtn.setAttribute('aria-label', 'Open menu');
      burger.setAttribute('aria-expanded', 'false');
      dropdown.style.maxHeight = '0px';
      backdrop.classList.remove('ydt-backdrop--visible');
      document.body.style.removeProperty('overflow');
    }
    function toggleDropdown() { isOpen ? closeDropdown() : openDropdown(); }

    gridBtn.addEventListener('click', toggleDropdown);
    burger.addEventListener('click', toggleDropdown);
    backdrop.addEventListener('click', closeDropdown);
    document.addEventListener('mousedown', function (e) {
      if (isOpen && !pill.contains(e.target)) closeDropdown();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen) closeDropdown();
    });
    dropdown.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeDropdown);
    });

    /* the underline rests on the section you're in and follows the cursor on hover */
    var activeNavLink = null;
    var navHovered = false;

    function placeUnderline(link) {
      if (!link || !navEl) { underline.style.opacity = '0'; return; }
      var rect = link.getBoundingClientRect();
      var navRect = navEl.getBoundingClientRect();
      underline.style.left = (rect.left - navRect.left) + 'px';
      underline.style.width = rect.width + 'px';
      underline.style.opacity = '1';
    }
    function setActiveNav(hash) {
      activeNavLink = null;
      navLinks.forEach(function (l) {
        if (l.getAttribute('href') === hash) activeNavLink = l;
      });
      if (!navHovered) placeUnderline(activeNavLink);
    }

    navLinks.forEach(function (link) {
      link.addEventListener('mouseenter', function () { navHovered = true; placeUnderline(link); });
    });
    if (navEl) {
      navEl.addEventListener('mouseleave', function () { navHovered = false; placeUnderline(activeNavLink); });
    }
    window.addEventListener('resize', function () {
      placeUnderline(navHovered ? null : activeNavLink);
      if (isOpen) dropdown.style.maxHeight = dropdown.scrollHeight + 'px';
    });

    /* ── track the section in view so the underline follows ── */
    function trackSections() {
      var targets = [];
      navLinks.forEach(function (l) {
        var href = l.getAttribute('href');
        if (!href || href.charAt(0) !== '#') return;
        var el = document.querySelector(href);
        if (el) targets.push({ el: el, hash: href });
      });
      if (!targets.length || !('IntersectionObserver' in window)) return;
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          for (var i = 0; i < targets.length; i++) {
            if (targets[i].el === entry.target) { setActiveNav(targets[i].hash); return; }
          }
        });
      }, { rootMargin: '-45% 0px -45% 0px' });
      targets.forEach(function (t) { obs.observe(t.el); });
    }
    trackSections();
  }

  /* ══════════════════════════════════════════════════════════════
     ANALYTICS + CONSENT

     Paste your GA4 measurement ID into GA_ID below (looks like
     "G-XXXXXXXXXX") and analytics switches on. Leave it empty and
     nothing loads and no banner appears — the site stays entirely
     cookie-free, which is why it ships that way.

     GA4 sets cookies, so under UK GDPR / PECR it may not run until
     the visitor agrees. Nothing is loaded before "Accept" is
     clicked, and the choice is remembered in localStorage. Decline
     is as easy as accept, which is the part most banners get wrong.

     If you would rather not have a banner at all, a cookieless
     analytics tool (Plausible, Fathom) needs no consent — swap the
     loadAnalytics body for their one-line script and delete the
     banner call.
     ══════════════════════════════════════════════════════════════ */
  var GA_ID = '';                       /* e.g. 'G-XXXXXXXXXX' */
  var CONSENT_KEY = 'ydt-consent';

  function loadAnalytics() {
    if (!GA_ID || window.__ydtAnalytics) return;
    window.__ydtAnalytics = true;
    var s1 = document.createElement('script');
    s1.async = true;
    s1.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s1);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
  }

  function consentBanner() {
    if (!GA_ID) return;                                  /* nothing to consent to */
    var stored = null;
    try { stored = localStorage.getItem(CONSENT_KEY); } catch (e) {}
    if (stored === 'granted') { loadAnalytics(); return; }
    if (stored === 'denied') return;

    var el = document.createElement('div');
    el.className = 'ydt-consent';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', 'Cookies');
    el.innerHTML =
      '<p>We would like to use analytics cookies to see which pages are useful. ' +
      'Nothing loads unless you agree, and you can change your mind any time. ' +
      '<a href="privacy.html">How we handle data</a>.</p>' +
      '<div class="ydt-consent__row">' +
        '<button type="button" class="ydt-consent__yes">Accept</button>' +
        '<button type="button" class="ydt-consent__no">Decline</button>' +
      '</div>';
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('is-in'); });

    function choose(value) {
      try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
      if (value === 'granted') loadAnalytics();
      el.classList.remove('is-in');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 500);
    }
    el.querySelector('.ydt-consent__yes').addEventListener('click', function () { choose('granted'); });
    el.querySelector('.ydt-consent__no').addEventListener('click', function () { choose('denied'); });
  }

  /* let the privacy page offer a way back out */
  window.ydtResetConsent = function () {
    try { localStorage.removeItem(CONSENT_KEY); } catch (e) {}
    location.reload();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
