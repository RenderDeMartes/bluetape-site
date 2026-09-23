/* Bluetape Rigging Studio — shared behaviour. No dependencies. */
(function () {
  'use strict';

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav. */
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav__toggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* Email is assembled in the browser so scrapers never see it in the HTML. */
  var mail = ['hello', 'bluetaperigging.com'].join('@');
  Array.prototype.forEach.call(document.querySelectorAll('[data-mail]'), function (el) {
    el.href = 'mailto:' + mail;
    if (!el.textContent.trim()) el.textContent = mail;
  });

  /* Click-to-play trailers. No request to YouTube until someone asks. */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('.play');
    if (!btn) return;
    var fig = btn.parentNode;
    var frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + btn.getAttribute('data-yt') + '?autoplay=1&rel=0';
    frame.title = btn.getAttribute('data-title') || 'Trailer';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    frame.allowFullscreen = true;
    fig.innerHTML = '';
    fig.appendChild(frame);
  });

  /* The brief form writes an email; there is no server behind it. */
  var form = document.querySelector('#brief');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var subject = 'Rigging enquiry' + (f.studio.value ? ' — ' + f.studio.value : '');
      var body = [
        'Name: ' + f.name.value,
        'Studio: ' + f.studio.value,
        'Need: ' + f.need.value,
        'Deadline: ' + f.deadline.value,
        '',
        f.scope.value
      ].join('\n');
      window.location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }

  /* Section reveals. */
  var targets = document.querySelectorAll('[data-reveal]');
  if (reduced || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(targets, function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.style.transitionDelay = (parseFloat(el.getAttribute('data-reveal')) || 0) + 'ms';
      el.classList.add('is-in');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
})();
