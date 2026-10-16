// Tema claro/oscuro compartido por las páginas institucionales.
// Aplica la preferencia guardada de inmediato (sin parpadeo) y conecta el botón #theme.
(function () {
  try {
    var s = localStorage.getItem('piva-theme');
    if (s) document.documentElement.setAttribute('data-theme', s);
  } catch (e) {}
  function wire() {
    var b = document.getElementById('theme');
    if (!b) return;
    b.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme');
      var isDark = cur ? cur === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
      var next = isDark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('piva-theme', next); } catch (e) {}
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
  else wire();
})();
