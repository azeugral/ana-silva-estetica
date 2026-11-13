(() => {
  const doc = document.documentElement;
  doc.classList.add('js');
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav: linha ao rolar
  const nav = document.querySelector('.nav');
  const marca = () => nav.classList.toggle('rolou', scrollY > 8);
  addEventListener('scroll', marca, { passive: true }); marca();

  // Menu do celular
  const btn = document.querySelector('.nav-menu');
  const menu = document.getElementById('menu');
  const fecha = () => { menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); btn.firstElementChild.textContent = 'Menu'; };
  btn.addEventListener('click', () => {
    const abre = menu.hidden;
    menu.hidden = !abre; btn.setAttribute('aria-expanded', String(abre));
    btn.firstElementChild.textContent = abre ? 'Fechar' : 'Menu';
  });
  menu.addEventListener('click', e => { if (e.target.closest('a')) fecha(); });

  // Hero + escala de cor: o cursor vai do A3,5 ao 0M1 em ~1,3 s
  const hero = document.querySelector('.hero');
  const cursor = document.querySelector('.escala-cursor');
  const tabs = [...document.querySelectorAll('.escala-svg .tab')];
  const pos = i => `calc((${i}*84 + 42) / 672 * 100%)`;
  const ativa = i => tabs.forEach((t, k) => {
    t.classList.toggle('ativo', k === i);
    t.querySelector('path').style.filter = k === i ? 'drop-shadow(0 6px 8px rgba(43,26,20,.18))' : '';
  });
  if (!reduz && cursor) {
    cursor.style.transition = 'none';
    cursor.style.left = pos(0); ativa(0);
    void cursor.offsetWidth;
    requestAnimationFrame(() => {
      hero.classList.add('pronto');
      setTimeout(() => {
        cursor.style.transition = '';
        cursor.style.left = pos(tabs.length - 1);
        const passo = 1250 / (tabs.length - 1);
        tabs.forEach((_, i) => setTimeout(() => ativa(i), i * passo));
      }, 380);
    });
  } else {
    hero.classList.add('pronto'); ativa(tabs.length - 1);
  }

  // Entradas: subida leve
  const els = document.querySelectorAll('.sobe');
  if (reduz || !('IntersectionObserver' in window)) { els.forEach(e => e.classList.add('visto')); return; }
  const io = new IntersectionObserver(ents => ents.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  els.forEach(e => io.observe(e));
})();
