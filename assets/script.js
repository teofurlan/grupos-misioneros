/* ============================================================
   Grupos misioneros con niños — comportamiento de la página
   JS vanilla, sin dependencias. Todo es progresivo: si esto
   no carga, la página se sigue leyendo entera.
   ============================================================ */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Barra de progreso de lectura ---------------------- */
  var bar = document.getElementById('progressBar');
  var topbar = document.querySelector('.topbar');
  var ticking = false;

  function onScroll() {
    var scrolled = window.scrollY;
    var max = document.documentElement.scrollHeight - window.innerHeight;

    if (bar) {
      bar.style.width = (max > 0 ? (scrolled / max) * 100 : 0) + '%';
    }
    if (topbar) {
      topbar.classList.toggle('is-stuck', scrolled > 8);
    }
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScroll);
    }
  }, { passive: true });

  onScroll();

  /* ---- Índice desplegable -------------------------------- */
  var toggle = document.getElementById('navToggle');
  var index = document.getElementById('navIndex');

  function closeIndex() {
    if (!index || !toggle) return;
    index.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
  }

  if (toggle && index) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = index.hidden;
      index.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
    });

    // Cerrar al elegir una sección, al clickear afuera o con Escape.
    index.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeIndex();
    });
    document.addEventListener('click', function (e) {
      if (!index.hidden && !index.contains(e.target) && e.target !== toggle) closeIndex();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeIndex();
    });
  }

  /* ---- Aparición de secciones al entrar en pantalla ------- */
  var sections = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    // Sin animación: se muestran todas de una.
    sections.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // una sola vez por sección
      }
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

  sections.forEach(function (el) { observer.observe(el); });
})();
