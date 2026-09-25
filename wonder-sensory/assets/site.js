/* ==========================================================================
   Wonder Sensory — shared behaviour
   Every block checks for its own elements first, so a page that has a header
   but no timetable (cafe.html, contact.html) runs cleanly.
   ========================================================================== */
(function () {
  'use strict';

  var BOOK = 'https://bookaby.me/wondersensory';

  /* ---------------------------------------------------------------- header */
  (function header() {
    var el = document.querySelector('.header');
    if (!el) return;
    var onScroll = function () { el.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  })();

  /* ----------------------------------------------------------- mobile menu */
  (function mobileMenu() {
    var menu = document.getElementById('mobileMenu');
    var openBtn = document.getElementById('menuOpen');
    var closeBtn = document.getElementById('menuClose');
    if (!menu || !openBtn || !closeBtn) return;

    // everything that must be hidden from keyboard and screen readers while open
    var behind = ['.header', 'main', '.footer', '.announce']
      .map(function (s) { return document.querySelector(s); })
      .filter(Boolean);

    var FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

    function visibleItems() {
      return Array.prototype.filter.call(
        menu.querySelectorAll(FOCUSABLE),
        function (n) { return n.offsetParent !== null; }
      );
    }

    function setMenu(open) {
      menu.classList.toggle('open', open);
      openBtn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
      behind.forEach(function (n) {
        if (open) { n.setAttribute('inert', ''); } else { n.removeAttribute('inert'); }
      });
      if (!open) { openBtn.focus(); return; }
      // focus the close button, or the first thing that is actually visible if it is not
      var items = visibleItems();
      var target = (closeBtn.offsetParent !== null) ? closeBtn : items[0];
      if (target) target.focus();
    }

    openBtn.addEventListener('click', function () { setMenu(true); });
    if (window.matchMedia) {
      window.matchMedia('(min-width:1001px)').addEventListener('change', function (e) {
        if (e.matches && menu.classList.contains('open')) setMenu(false);
      });
    }
    closeBtn.addEventListener('click', function () { setMenu(false); });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });

    document.addEventListener('keydown', function (e) {
      if (!menu.classList.contains('open')) return;
      if (e.key === 'Escape') { setMenu(false); return; }
      if (e.key !== 'Tab') return;
      // keep focus inside the dialog
      var items = visibleItems();
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  })();

  /* ------------------------------------------------------------- timetable */
  /* --------------------------------------------------------------------
     EDIT THE WEEKS BELOW TO KEEP THE TIMETABLE CURRENT.

     Session types:  P = Pre-Walking Playtime   O = 0+ Open Sensory Play
                     V = Private Hire           null = no session in that slot

     Each day() takes: (day name, date number, time list, types, sold-out slots)
       - time list is WD for weekdays (09:30 start) or WE for weekends (10:00)
       - the fifth argument lists the *positions* that are sold out, counting
         from 0. So [0,2] marks the first and third sessions of that day full.

     UPDATED tells visitors when this was last checked. Change it whenever you
     edit the weeks, otherwise the page claims to be fresher than it is.
     -------------------------------------------------------------------- */
  var UPDATED = '24 September 2026';

  (function timetable() {
    var grid = document.getElementById('ttGrid');
    var list = document.getElementById('ttList');
    var tabs = document.getElementById('dayTabs');
    var weekLabel = document.getElementById('weekLabel');
    var themeText = document.getElementById('themeText');
    var themePill = document.getElementById('themePill');
    var prev = document.getElementById('prevWeek');
    var next = document.getElementById('nextWeek');
    if (!grid || !list || !tabs || !weekLabel || !prev || !next) return;

    var NAMES = { pre: 'Pre-Walking Playtime', open: '0+ Open Sensory Play', private: 'Private Hire' };
    var SHORT = { pre: 'Pre-Walking', open: 'Open Play', private: 'Private Hire' };
    var WD = ['09:30', '10:45', '12:00', '13:15', '14:30'];
    var WE = ['10:00', '11:15', '12:30', '13:45', '15:00'];
    var P = 'pre', O = 'open', V = 'private';

    function day(label, num, times, types, full) {
      return {
        label: label, num: num,
        slots: types.map(function (t, i) {
          return t ? { time: times[i], type: t, full: !!(full && full.indexOf(i) > -1) } : null;
        }).filter(Boolean)
      };
    }

    var WEEKS = [
      { start: '2026-09-07', label: '7 – 13 September', theme: 'Wild West theme week · £15 per child', themed: true, days: [
        day('Mon', 7, WD, [P, O, O, O, P], [0]), day('Tue', 8, WD, [P, P, O, P, O]),
        day('Wed', 9, WD, [O, P, O, O, P]),      day('Thu', 10, WD, [O, P, O, P, P]),
        day('Fri', 11, WD, [P, O, P, O, P], [1]), day('Sat', 12, WE, [O, O, P, P, O], [0, 1]),
        day('Sun', 13, WE, [P, P, O, O, P], [0])
      ] },
      { start: '2026-09-14', label: '14 – 20 September', theme: 'Standard sessions · £10 per child', themed: false, days: [
        day('Mon', 14, WD, [O, V, O, P, O]), day('Tue', 15, WD, [P, O, O, P, P]),
        day('Wed', 16, WD, [O, P, O, O, P]), day('Thu', 17, WD, [P, O, O, P, O]),
        day('Fri', 18, WD, [O, P, P, O, O]), day('Sat', 19, WE, [P, O, V, null, P]),
        day('Sun', 20, WE, [O, P, O, P, O])
      ] },
      { start: '2026-09-21', label: '21 – 27 September', theme: 'Standard sessions · £10 per child', themed: false, days: [
        day('Mon', 21, WD, [O, P, O, P, O]), day('Tue', 22, WD, [P, O, O, P, P]),
        day('Wed', 23, WD, [O, P, P, O, P]), day('Thu', 24, WD, [P, O, O, P, O]),
        day('Fri', 25, WD, [O, P, P, O, O]), day('Sat', 26, WE, [P, O, O, P, P]),
        day('Sun', 27, WE, [V, null, null, null, null])
      ] },
      { start: '2026-09-28', label: '28 Sep – 4 October', theme: 'Space theme from Thu 1 Oct · £15 per child (£10 Mon–Wed)', themed: true, days: [
        day('Mon', 28, WD, [O, P, O, P, O]), day('Tue', 29, WD, [P, O, O, P, P]),
        day('Wed', 30, WD, [O, P, null, null, null]), day('Thu', 1, WD, [O, P, O, P, O]),
        day('Fri', 2, WD, [O, O, P, P, O]), day('Sat', 3, WE, [P, O, O, P, P]),
        day('Sun', 4, WE, [O, P, O, P, O])
      ] }
    ];

    // open on the week that contains today (last week if all are past, first if all are future)
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var DAY = 864e5;
    function weekStart(w) { var d = new Date(w.start + 'T00:00:00'); return d; }
    var wk = 0, filter = 'all', activeDay = 0;
    for (var i = 0; i < WEEKS.length; i++) {
      var st = weekStart(WEEKS[i]);
      if (today >= st) wk = i;
      if (today >= st && today < new Date(st.getTime() + 7 * DAY)) {
        activeDay = Math.round((today - st) / DAY);
        break;
      }
    }
    function isPast(w, di) { return new Date(weekStart(w).getTime() + di * DAY) < today; }

    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

    function slotHTML(s, compact, past) {
      var N = compact ? SHORT : NAMES;
      if (filter !== 'all' && filter !== s.type) return '';
      var cls = 'slot ' + s.type + (s.full || past ? ' full' : '');
      var sub = past ? 'Gone' : s.full ? 'Fully booked'
        : (s.type === 'private' ? (compact ? 'Booked out' : 'Exclusive use · booked')
                                : (compact ? 'Spaces available' : '1 hour · spaces available'));
      var label = NAMES[s.type] + ' at ' + s.time + (s.full ? ', fully booked' : '');
      var inner = '<time>' + s.time + '</time><b>' + N[s.type] + '</b><small>' + sub + '</small>';
      if (past || s.full || s.type === 'private') {
        return '<div class="' + cls + '">' + inner + '</div>';
      }
      return '<a class="' + cls + '" href="' + BOOK + '" target="_blank" rel="noopener"' +
             ' aria-label="Book ' + esc(label) + ' (opens the booking site in a new tab)">' + inner + '</a>';
    }

    function emptyMsg(suffix) {
      return '<p class="tt-empty">No ' + (NAMES[filter] || '') + ' sessions' + (suffix || '') + '</p>';
    }

    function render() {
      var w = WEEKS[wk];
      weekLabel.textContent = w.label;
      if (themeText) themeText.textContent = w.theme;
      if (themePill) themePill.classList.toggle('plain', !w.themed);
      prev.disabled = wk === 0;
      next.disabled = wk === WEEKS.length - 1;
      if (document.activeElement === next && next.disabled) prev.focus();
      if (document.activeElement === prev && prev.disabled) next.focus();

      grid.innerHTML = w.days.map(function (d, di) {
        var visible = d.slots.filter(function (s) { return filter === 'all' || filter === s.type; });
        var past = isPast(w, di);
        var body = d.slots.map(function (s) { return slotHTML(s, true, past); }).join('') +
                   (visible.length ? '' : emptyMsg());
        return '<div class="tt-day"><div class="dh"><b>' + d.label + '</b><span>' + d.num + '</span></div>' + body + '</div>';
      }).join('');

      tabs.innerHTML = w.days.map(function (d, i) {
        return '<button type="button" role="tab" id="daytab-' + i + '" aria-controls="ttList"' +
               ' aria-selected="' + (i === activeDay) + '" tabindex="' + (i === activeDay ? '0' : '-1') + '"' +
               ' data-i="' + i + '">' + d.label + '<span>' + d.num + '</span></button>';
      }).join('');

      var d = w.days[activeDay];
      var vis = d.slots.filter(function (s) { return filter === 'all' || filter === s.type; });
      list.setAttribute('aria-labelledby', 'daytab-' + activeDay);
      list.innerHTML = d.slots.map(function (s) { return slotHTML(s, false, isPast(w, activeDay)); }).join('') +
                       (vis.length ? '' : emptyMsg(' on ' + d.label));
    }

    prev.addEventListener('click', function () { if (wk > 0) { wk--; activeDay = 0; render(); } });
    next.addEventListener('click', function () { if (wk < WEEKS.length - 1) { wk++; activeDay = 0; render(); } });

    tabs.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      activeDay = +b.dataset.i;
      render();
    });
    // arrow keys move between day tabs, which is what role="tab" promises
    tabs.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft' && e.key !== 'Home' && e.key !== 'End') return;
      var count = WEEKS[wk].days.length;
      e.preventDefault();
      if (e.key === 'Home') activeDay = 0;
      else if (e.key === 'End') activeDay = count - 1;
      else activeDay = (activeDay + (e.key === 'ArrowRight' ? 1 : count - 1)) % count;
      render();
      var t = tabs.querySelector('[aria-selected="true"]');
      if (t) t.focus();
    });

    document.querySelectorAll('.chip[data-filter]').forEach(function (c) {
      c.addEventListener('click', function () {
        filter = c.dataset.filter;
        document.querySelectorAll('.chip[data-filter]').forEach(function (x) {
          x.setAttribute('aria-pressed', String(x === c));
        });
        render();
      });
    });

    var stamp = document.getElementById('ttUpdated');
    if (stamp) stamp.textContent = UPDATED;

    render();
  })();

  /* ------------------------------------------------------------ enquiry form */
  (function enquiryForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;
    var statusBox = document.getElementById('formStatus');
    var summary = document.getElementById('errorSummary');
    var summaryList = document.getElementById('errorSummaryList');
    var send = document.getElementById('sendBtn');

    // Pre-select the enquiry topic when arriving from a "Get a quote" style link
    var topic = new URLSearchParams(location.search).get('topic');
    var select = form.querySelector('#f-topic');
    if (topic && select) {
      Array.prototype.forEach.call(select.options, function (o) {
        if (o.value.toLowerCase() === topic.toLowerCase()) select.value = o.value;
      });
    }

    var fields = Array.prototype.slice.call(form.querySelectorAll('input[required],textarea[required],input[type="email"]'));

    function messageFor(el) {
      if (el.validity.valueMissing) {
        return el.tagName === 'TEXTAREA' ? 'Tell us what you would like to ask.'
          : 'Enter your ' + (el.dataset.label || el.name) + '.';
      }
      if (el.validity.typeMismatch && el.type === 'email') {
        return 'Enter an email address in the format name@example.com.';
      }
      return 'Check this field.';
    }

    function showError(el, msg) {
      var slot = document.getElementById(el.id + '-err');
      el.setAttribute('aria-invalid', 'true');
      if (slot) {
        slot.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">' +
          '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg><span>' + msg + '</span>';
      }
    }
    function clearError(el) {
      var slot = document.getElementById(el.id + '-err');
      el.removeAttribute('aria-invalid');
      if (slot) slot.textContent = '';
      if (summaryList) {
        var item = summaryList.querySelector('a[href="#' + el.id + '"]');
        if (item && item.parentNode) item.parentNode.parentNode.removeChild(item.parentNode);
        if (summary && !summaryList.children.length) summary.classList.remove('show');
      }
    }
    function validate(el) {
      if (el.checkValidity()) { clearError(el); return null; }
      var msg = messageFor(el);
      showError(el, msg);
      return msg;
    }

    // validate on blur, not on every keystroke
    fields.forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value !== '') validate(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid')) validate(el); });
    });

    form.addEventListener('submit', function (e) {
      var problems = [];
      if (statusBox) statusBox.className = 'form-status';
      fields.forEach(function (el) {
        var msg = validate(el);
        if (msg) problems.push({ id: el.id, label: el.dataset.label || el.name, msg: msg });
      });

      if (problems.length) {
        e.preventDefault();
        if (summary && summaryList) {
          summaryList.innerHTML = problems.map(function (p) {
            return '<li><a href="#' + p.id + '">' + p.msg + '</a></li>';
          }).join('');
          summary.classList.add('show');
          summary.focus();
        }
        return;
      }
      if (summary) summary.classList.remove('show');

      // With no endpoint configured yet, do not pretend the message was sent.
      if (!form.getAttribute('action')) {
        e.preventDefault();
        if (statusBox) {
          statusBox.className = 'form-status show warn';
          statusBox.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">' +
            '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>' +
            '<span>This form is not connected yet, so nothing has been sent. Please message us on ' +
            '<a href="https://www.facebook.com/behindthemagicdooruk" target="_blank" rel="noopener">Facebook</a> or ' +
            '<a href="https://www.instagram.com/behindthemagicdooruk/" target="_blank" rel="noopener">Instagram</a> in the meantime.</span>';
          statusBox.focus();
        }
        return;
      }
      if (send) { send.disabled = true; send.textContent = 'Sending…'; }
    });
  })();

  /* ----------------------------------------------- external link announcement */
  (function externalLinks() {
    document.querySelectorAll('a[target="_blank"]').forEach(function (a) {
      if (a.querySelector('.vh') || a.getAttribute('aria-label')) return;
      var s = document.createElement('span');
      s.className = 'vh';
      s.textContent = ' (opens in a new tab)';
      a.appendChild(s);
    });
  })();
})();
