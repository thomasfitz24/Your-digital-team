/* Shoreline 911 — header + menu behaviour */
(function () {
  'use strict';

  var header   = document.getElementById('site-header');
  var toggle   = document.getElementById('menu-toggle');
  var label    = toggle.querySelector('.menu-toggle__label');
  var menu     = document.getElementById('site-menu');
  var backdrop = document.getElementById('menu-backdrop');
  var isOpen   = false;

  /* ---------- Menu drawer ---------- */
  function openMenu() {
    if (isOpen) return;
    isOpen = true;
    menu.hidden = false;
    backdrop.hidden = false;
    // next frame so the transition runs from the hidden state
    requestAnimationFrame(function () {
      menu.classList.add('is-open');
      backdrop.classList.add('is-visible');
    });
    toggle.setAttribute('aria-expanded', 'true');
    label.textContent = label.dataset.close;
    document.body.classList.add('menu-open');
    showHeader();
    var first = menu.querySelector('a');
    if (first) first.focus({ preventScroll: true });
  }

  function closeMenu(returnFocus) {
    if (!isOpen) return;
    isOpen = false;
    menu.classList.remove('is-open');
    backdrop.classList.remove('is-visible');
    toggle.setAttribute('aria-expanded', 'false');
    label.textContent = label.dataset.open;
    document.body.classList.remove('menu-open');
    var done = function () {
      if (!isOpen) { menu.hidden = true; backdrop.hidden = true; }
      menu.removeEventListener('transitionend', done);
    };
    menu.addEventListener('transitionend', done);
    setTimeout(done, 500); // safety if transitionend never fires (reduced motion)
    if (returnFocus !== false) toggle.focus({ preventScroll: true });
  }

  toggle.addEventListener('click', function () { isOpen ? closeMenu() : openMenu(); });
  backdrop.addEventListener('click', function () { closeMenu(); });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) closeMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen) closeMenu();
    // keep Tab inside the drawer while it is open
    if (e.key === 'Tab' && isOpen) {
      var focusables = [toggle].concat([].slice.call(menu.querySelectorAll('a[href]')));
      var first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------- Header sits at the top of the page; transparent over the hero, solid when the menu is open ---------- */
  var ticking = false;

  function showHeader() { header.classList.remove('is-hidden'); }

  var hero = document.getElementById('hero');

  function onScroll() {
    var y = window.scrollY;
    // transparent while the header sits over the hero, solid grey once past it
    var overHero = hero ? y < hero.offsetHeight - header.offsetHeight : false;
    header.classList.toggle('is-transparent', overHero);
    header.classList.toggle('is-scrolled', !overHero && y > 4);
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Page turns dark from the Builds section down ---------- */
  var builds = document.querySelector('.builds');
  if (builds) {
    var darkTick = false;
    function checkDark() {
      // only once the section has actually arrived at the top of the screen
      var top = builds.getBoundingClientRect().top;
      document.body.classList.toggle('is-dark', top <= window.innerHeight * 0.12);
      darkTick = false;
    }
    window.addEventListener('scroll', function () {
      if (!darkTick) { requestAnimationFrame(checkDark); darkTick = true; }
    }, { passive: true });
    window.addEventListener('resize', checkDark);
    checkDark();
  }

  /* ---------- Builds carousel arrows ---------- */
  var track = document.getElementById('builds-track');
  if (track) {
    var arrows = document.querySelectorAll('.builds__arrow');
    function step() { var li = track.querySelector('li'); return li ? li.getBoundingClientRect().width + 24 : 600; }
    function updateArrows() {
      var max = track.scrollWidth - track.clientWidth - 2;
      arrows.forEach(function (b) {
        var dir = +b.dataset.dir;
        b.disabled = dir < 0 ? track.scrollLeft <= 2 : track.scrollLeft >= max;
      });
    }
    arrows.forEach(function (b) {
      b.addEventListener('click', function () {
        track.scrollBy({ left: +b.dataset.dir * step(), behavior: 'smooth' });
      });
    });
    track.addEventListener('scroll', updateArrows, { passive: true });
    window.addEventListener('resize', updateArrows);
    updateArrows();
  }
})();
