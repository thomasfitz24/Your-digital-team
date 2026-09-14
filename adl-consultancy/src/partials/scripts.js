/* ADL Consultancy — progressive enhancement only.
   Every feature below upgrades markup that already works without JavaScript:
   the hero shows its poster frame, the standards panels render stacked, the
   nav renders as a plain list. Nothing here is required to read or navigate
   the site — which matters because WordPress editors often strip inline
   <script> from pasted content. */
(function () {
  'use strict';

  var page = document.querySelector('.adl-page');
  if (!page) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- current year in the footer ------------------------------------- */
  var yr = document.getElementById('adlYear');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- sticky header shadow ------------------------------------------- */
  var header = document.getElementById('adlHeader');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- standards dropdown --------------------------------------------- */
  var ddBtn = document.getElementById('adlStdToggle');
  var ddMenu = document.getElementById('adlStdMenu');
  if (ddBtn && ddMenu) {
    var hoverOpened = false;
    var hoverTimer;
    var setDd = function (open) {
      ddMenu.classList.toggle('open', open);
      ddBtn.setAttribute('aria-expanded', String(open));
      if (!open) hoverOpened = false;
    };
    // A click must not close a menu the pointer only just hover-opened.
    ddBtn.addEventListener('click', function () {
      var open = ddMenu.classList.contains('open');
      if (open && hoverOpened) { hoverOpened = false; return; }
      setDd(!open);
    });
    var li = ddBtn.parentNode;
    li.addEventListener('mouseenter', function () {
      clearTimeout(hoverTimer);
      if (!ddMenu.classList.contains('open')) { setDd(true); hoverOpened = true; }
    });
    li.addEventListener('mouseleave', function () {
      hoverTimer = setTimeout(function () { if (hoverOpened) setDd(false); }, 160);
    });
    document.addEventListener('click', function (e) {
      if (!ddBtn.contains(e.target) && !ddMenu.contains(e.target)) setDd(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ddMenu.classList.contains('open')) { setDd(false); ddBtn.focus(); }
    });
  }

  /* ---- mobile menu ------------------------------------------------------ */
  var burger = document.getElementById('adlMenuToggle');
  var mobile = document.getElementById('adlMobileMenu');
  if (burger && mobile) {
    var setMenu = function (open) {
      page.classList.toggle('menu-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) { mobile.hidden = false; }
      else {
        setTimeout(function () {
          if (!page.classList.contains('menu-open')) mobile.hidden = true;
        }, 340);
      }
    };
    mobile.hidden = true; // only hide it once JS is available to bring it back
    burger.addEventListener('click', function () {
      setMenu(!page.classList.contains('menu-open'));
    });
    mobile.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && page.classList.contains('menu-open')) { setMenu(false); burger.focus(); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1140 && page.classList.contains('menu-open')) setMenu(false);
    });
  }

  /* ---- standards: upgrade stacked panels into a tablist ----------------- */
  var tablist = document.querySelector('.tabs[role="tablist"]');
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var panels = tabs
      .map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); })
      .filter(Boolean);

    if (tabs.length && panels.length === tabs.length) {
      tablist.classList.add('is-live'); // CSS keeps the tab strip hidden until now
      var select = function (tab, focus) {
        tabs.forEach(function (t) {
          var on = t === tab;
          var panel = document.getElementById(t.getAttribute('aria-controls'));
          t.setAttribute('aria-selected', String(on));
          t.setAttribute('tabindex', on ? '0' : '-1');
          if (panel) panel.hidden = !on;
        });
        if (focus) tab.focus();
      };
      tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { select(tab, false); });
        tab.addEventListener('keydown', function (e) {
          var next = null;
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = tabs[(i + 1) % tabs.length];
          else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = tabs[(i - 1 + tabs.length) % tabs.length];
          else if (e.key === 'Home') next = tabs[0];
          else if (e.key === 'End') next = tabs[tabs.length - 1];
          if (next) { e.preventDefault(); select(next, true); }
        });
      });
      select(tabs[0], false);
    }
  }

  /* ---- hero: swap the poster for a muted looping video ------------------ */
  var media = document.querySelector('.hero-media[data-video]');
  if (media && !reduced && window.innerWidth >= 860) {
    var id = media.getAttribute('data-video');
    if (id) {
      var frame = document.createElement('iframe');
      frame.setAttribute('title', 'ADL Consultancy background video');
      frame.setAttribute('aria-hidden', 'true');
      frame.setAttribute('tabindex', '-1');
      frame.setAttribute('allow', 'autoplay; encrypted-media');
      frame.setAttribute('frameborder', '0');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&mute=1&loop=1&playlist=' + id +
        '&controls=0&showinfo=0&rel=0&modestbranding=1&playsinline=1&disablekb=1';
      media.appendChild(frame);
    }
  }

  /* ---- video modal: the same film, with sound --------------------------- */
  var modal = document.getElementById('adlVideoModal');
  if (modal) {
    var modalFrame = modal.querySelector('iframe');
    var lastFocus = null;
    var openModal = function (id) {
      lastFocus = document.activeElement;
      modalFrame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1';
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      var closeBtn = modal.querySelector('.close');
      if (closeBtn) closeBtn.focus();
    };
    var closeModal = function () {
      modal.classList.remove('open');
      // about:blank, not '' — an empty src resolves to the current document URL,
      // which would reload the whole page inside the hidden iframe.
      modalFrame.src = 'about:blank'; // stops playback
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    };
    document.querySelectorAll('[data-play]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        openModal(btn.getAttribute('data-play'));
      });
    });
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target.closest('.close')) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });
  }
})();
