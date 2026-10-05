(function () {
  // Hero rotation
  var figs = [].slice.call(document.querySelectorAll('#stage figure'));
  var dots = [].slice.call(document.querySelectorAll('#stage .dots button'));
  if (figs.length) {
    var i = 0, timer = null;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var show = function (n) {
      i = (n + figs.length) % figs.length;
      figs.forEach(function (f, k) { f.classList.toggle('on', k === i); f.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      dots.forEach(function (d, k) { d.setAttribute('aria-current', k === i ? 'true' : 'false'); });
    };
    var start = function () { if (reduce) return; if (timer) clearInterval(timer); timer = setInterval(function () { show(i + 1); }, 5200); };
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); start(); }); });
    show(0); start();
  }

  // Reservation / inquiry forms (tribute site: nothing is sent anywhere)
  [].slice.call(document.querySelectorAll('form.res')).forEach(function (form) {
    var dateEl = form.querySelector('input[type="date"]');
    if (dateEl) {
      var t = new Date(); var min = t.toISOString().slice(0, 10);
      t.setDate(t.getDate() + 1);
      dateEl.min = min; if (!dateEl.value) dateEl.value = t.toISOString().slice(0, 10);
    }
    var box = form.querySelector('.confirm');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var nameEl = form.querySelector('[name="name"]');
      var name = nameEl ? nameEl.value.trim() : '';
      box.hidden = false; box.textContent = '';
      var s = document.createElement('strong');
      var p = document.createElement('span');
      var sm = document.createElement('small');
      if (!name) {
        s.textContent = 'Add a name for the reservation.';
        p.textContent = 'Luigi likes to know who he is cooking for.';
        box.append(s, p); nameEl && nameEl.focus(); return;
      }
      var kind = form.getAttribute('data-kind') || 'table';
      var d = dateEl && dateEl.value ? new Date(dateEl.value + 'T12:00:00') : null;
      var when = d ? d.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' }) : 'your date';
      if (kind === 'event') {
        var size = form.querySelector('[name="size"]').value;
        s.textContent = 'Grazie, ' + name + '. Your event inquiry for ' + when + ' (' + size + ') is in.';
        p.textContent = 'Our events team will call you back. Chef Luigi has already started thinking about the menu.';
      } else {
        var party = form.querySelector('[name="party"]').value;
        var time = form.querySelector('[name="time"]').value;
        s.textContent = 'Grazie, ' + name + '. Table for ' + party + ' on ' + when + ' at ' + time + '.';
        p.textContent = 'Chef Luigi has been told. He is very excited and definitely exists.';
      }
      sm.textContent = 'Terrezano’s is a tribute site, so nothing was actually booked.';
      box.append(s, p, sm);
      box.focus && box.focus();
    });
  });

  // Copy phone
  [].slice.call(document.querySelectorAll('[data-copy]')).forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.getElementById(btn.getAttribute('data-copy'));
      var label = btn.textContent;
      var fallback = function () {
        var r = document.createRange(); r.selectNodeContents(el);
        var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        btn.textContent = 'Selected';
      };
      try { navigator.clipboard.writeText(el.textContent).then(function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = label; }, 1800); }, fallback); }
      catch (err) { fallback(); }
    });
  });
})();
