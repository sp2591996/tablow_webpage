// Progressive enhancement only: every page is readable and crawlable without JS.
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var inr = function (n) { return '₹' + n.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); };
  var inr2 = function (n) { return '₹' + n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };

  // Sticky offsets follow the real header height (it wraps on phones)
  var head = $('.site-head');
  function setTop() { if (head) document.documentElement.style.setProperty('--head-h', head.offsetHeight + 'px'); }
  setTop(); addEventListener('resize', setTop);

  // Section nav: highlight the section in view and keep its pill visible
  var nav = $('.secnav-in'), links = $$('.secnav a');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) { map[a.hash.slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = map[en.target.id]; if (!a) return;
        links.forEach(function (l) { l.classList.remove('active'); });
        a.classList.add('active');
        var x = a.offsetLeft - nav.clientWidth / 2 + a.clientWidth / 2;
        nav.scrollTo({ left: Math.max(0, x), behavior: 'smooth' });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  // Mobile buy bar appears once the main CTA scrolls away (hidden on desktop by CSS)
  var bar = $('.buybar'), hero = $('[data-hero]');
  if (bar && hero) {
    var onScroll = function () { bar.classList.toggle('show', hero.getBoundingClientRect().bottom < 0); };
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  // Toast
  var toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); toast.setAttribute('aria-live', 'polite'); document.body.appendChild(toast);
  function say(t) { toast.textContent = t; toast.classList.add('show'); clearTimeout(say.t); say.t = setTimeout(function () { toast.classList.remove('show'); }, 2000); }

  // Pack + quantity (substitute page)
  var buy = $('[data-buy]');
  var qty = 1;
  function refresh() {
    if (!buy) return;
    var p = $('input[name=pack]:checked', buy); if (!p) return;
    var packs = +p.value, unitPrice = +buy.dataset.packprice, mrp = +buy.dataset.brandpack;
    $('[data-total]', buy).textContent = inr2(unitPrice * packs * qty);
    var s = $('[data-save]', buy); if (s) s.textContent = inr2((mrp - unitPrice) * packs * qty);
  }
  if (buy) {
    $$('input[name=pack]', buy).forEach(function (r) { r.addEventListener('change', refresh); });
    $$('[data-step]', buy).forEach(function (b) {
      b.addEventListener('click', function () {
        qty = Math.max(1, Math.min(10, qty + (+b.dataset.step)));
        $('output', buy).textContent = qty; refresh();
      });
    });
    var pinBtn = $('[data-pin]', buy);
    if (pinBtn) pinBtn.addEventListener('click', function () {
      var v = ($('#pincode').value || '').trim(), msg = $('.pin-msg', buy), ok = /^[1-9][0-9]{5}$/.test(v);
      msg.textContent = ok ? 'Delivery available. Usually 2–4 days from a licensed partner pharmacy.' : 'Enter a valid 6-digit pincode.';
      msg.style.color = ok ? '' : 'var(--danger)';
    });
    refresh();
  }

  // Add to cart (prototype)
  // Add to cart never blocks (a Tablow doctor calls after the order for prescription medicines)
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-add]'); if (!b || b.disabled) return;
    say(b.dataset.add + ' added to cart');
  });
  // Brand option: enabled only after the shopper ticks the extra-cost acknowledgement
  Array.prototype.forEach.call(document.querySelectorAll('.keep-brand'), function (k) {
    var cb = k.querySelector('[data-kb]'), btn = k.querySelector('[data-kb-btn]');
    cb.addEventListener('change', function () { btn.disabled = !cb.checked; });
  });

  // Savings calculator
  $$('[data-calc]').forEach(function (c) {
    var r = $('input[type=range]', c), diff = +c.dataset.diff, kind = c.dataset.kind;
    function upd() {
      var n = +r.value;
      $('[data-n]', c).textContent = n;
      if (kind === 'course') {
        $('[data-main]', c).textContent = inr(diff * n);
        $('[data-a]', c).textContent = inr(diff * n * 3);
      } else if (kind === 'year') {
        $('[data-main]', c).textContent = inr(diff * n);
        $('[data-a]', c).textContent = inr(diff * n / 12);
    } else {
        $('[data-main]', c).textContent = inr(diff * n * 12);
        $('[data-a]', c).textContent = inr(diff * n);
      }
    }
    r.addEventListener('input', upd); upd();
  });
})();

// Savings calculator v6: one input, saving per year
(function () {
  var fmt = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };
  Array.prototype.forEach.call(document.querySelectorAll('[data-calc2]'), function (c) {
    var q = function (s) { return c.querySelector(s); }, D = c.dataset;
    var out = q('[data-dose]'), mx = +q('[data-max]').value, dose = +out.textContent;
    function upd() {
      var packs, bt, st, n, txt;
      if (D.per === 'course') {            // short courses: you buy whole packs
        packs = dose * +D.ppc; bt = packs * +D.bp; st = packs * +D.sp; n = packs * +D.units;
        txt = 'at ' + dose + ' course' + (dose > 1 ? 's' : '') + ' a year';
      } else {
        n = D.per === 'month' ? dose * 12 : dose * 365;
        bt = n * +D.bu; st = n * +D.su; packs = Math.ceil(n / +D.units - 1e-9);
        txt = 'at ' + dose + ' ' + D.unit + (dose > 1 ? 's' : '') + (D.per === 'month' ? ' a month' : ' a day');
      }
      q('[data-save]').textContent = fmt(bt - st);
      q('[data-spantxt]').textContent = txt;
      q('[data-bt]').textContent = fmt(bt) + ' a year'; q('[data-st]').textContent = fmt(st) + ' a year';
      q('[data-sb]').style.width = Math.max(6, Math.round(st / bt * 100)) + '%';
      q('[data-need]').textContent = (+D.units > 1 ? Math.round(n) + ' ' + D.unit + 's, ' : '') + packs + ' ' + D.pack + (packs > 1 ? 's' : '');
      q('[data-pm]').textContent = fmt((bt - st) / 12);
    }
    Array.prototype.forEach.call(c.querySelectorAll('[data-d]'), function (b) {
      b.addEventListener('click', function () { dose = Math.max(1, Math.min(mx, dose + (+b.dataset.d))); out.textContent = dose; upd(); });
    });
    upd();
  });
})();

// "Want the brand instead?" link opens the brand option and scrolls to it
document.addEventListener('click', function (e) {
  var a = e.target.closest('[data-open-kb]'); if (!a) return;
  var k = document.getElementById('keep-brand'); if (k) k.open = true;
});
