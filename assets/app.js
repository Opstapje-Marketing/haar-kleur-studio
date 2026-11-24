// Haar Kleur Studio – kleine interacties
(function () {
  // Header schaduw bij scrollen
  var header = document.querySelector('.site-header');
  var onScroll = function () { if (header) header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobiel menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Sluiten' : 'Menu';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.textContent = 'Menu'; }
    });
  }

  // Voor/na: tijdens het scrollen schuift het eindresultaat over de voor-foto.
  // Zelf slepen kan altijd; daarna neemt de bezoeker het over.
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bas = [];
  document.querySelectorAll('.ba').forEach(function (el) {
    var input = el.querySelector('input');
    if (!input) return;
    var item = { el: el, input: input, manual: false };
    var set = function (v) { input.value = v; el.style.setProperty('--pos', v + '%'); el.classList.toggle('ba-edge', v <= 1 || v >= 99); el.setAttribute('data-side', v > 50 ? 'voor' : 'na'); };
    item.set = set;
    input.addEventListener('input', function () { item.manual = true; el.classList.remove('ba-edge'); el.style.setProperty('--pos', input.value + '%'); });
    input.addEventListener('pointerdown', function () { item.manual = true; });
    set(reduce ? 50 : 100);
    bas.push(item);
  });
  if (!reduce && bas.length) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var vh = window.innerHeight;
      bas.forEach(function (it) {
        if (it.manual || it.el.offsetParent === null) return;
        var sec = it.el.closest('.hero-scroll');
        var pin = sec && sec.querySelector('.hero-pin');
        if (pin && getComputedStyle(pin).position === 'sticky') {
          var sr = sec.getBoundingClientRect();
          var span = sec.offsetHeight - pin.offsetHeight;
          var q = span > 0 ? (-sr.top) / span : 0;
          q = Math.max(0, Math.min(1, (q - 0.06) / 0.8));
          q = q * q * (3 - 2 * q);
          sec.classList.toggle('done', q > 0.9);
          it.set(Math.round((1 - q) * 1000) / 10);
          return;
        }
        var r = it.el.getBoundingClientRect();
        if (sec) {
          // Hero op mobiel: overgang start pas als je begint te scrollen
          var hq = window.scrollY / Math.max(1, r.height * 1.05);
          hq = Math.max(0, Math.min(1, hq)); hq = hq * hq * (3 - 2 * hq);
          it.set(Math.round((1 - hq) * 1000) / 10);
          return;
        }
        if (r.bottom < 0 || r.top > vh) return;
        // 0 = net in beeld (voor), 1 = in het bovenste deel van het scherm (na)
        var p = (vh * 0.9 - r.top) / (vh * 0.55);
        p = Math.max(0, Math.min(1, p));
        p = p * p * (3 - 2 * p); // zachte in- en uitloop
        it.set(Math.round((1 - p) * 1000) / 10);
      });
    };
    var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    update();
  }

  // Portfolio-filter
  var filterBtns = document.querySelectorAll('.filters button');
  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      document.querySelectorAll('[data-cat]').forEach(function (item) {
        item.hidden = !(f === 'alle' || item.getAttribute('data-cat').split(' ').indexOf(f) > -1);
      });
    });
  });

  // Zachte fade-in
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
})();
