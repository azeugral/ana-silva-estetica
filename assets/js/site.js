(() => {
  const doc = document.documentElement;
  doc.classList.add('js');
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const WA = 'https://wa.me/message/MENNVN7SM6MRM1';

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

  // Hero
  const hero = document.querySelector('.hero');
  requestAnimationFrame(() => hero.classList.add('pronto'));

  // Pedido de marcação
  const form = document.getElementById('pedido');
  const sens = document.getElementById('f-sens');
  const nota = document.getElementById('pedido-nota');
  const val = n => (form.querySelector(`input[name="${n}"]:checked`) || {}).value || '';
  const atualizaSens = () => { sens.hidden = val('trat') !== 'Branqueamento dentário'; };
  form.addEventListener('change', atualizaSens); atualizaSens();

  // "Marcar" nos tratamentos pré-seleciona o tratamento
  document.querySelectorAll('[data-trat]').forEach(a => a.addEventListener('click', () => {
    const r = form.querySelector(`input[name="trat"][value="${a.dataset.trat}"]`);
    if (r) { r.checked = true; atualizaSens(); }
  }));

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const nome = form.nome.value.trim();
    if (!nome) { form.nome.classList.add('erro'); form.nome.focus(); return; }
    form.nome.classList.remove('erro');
    const linhas = [
      `Olá Ana! Chamo-me ${nome} e gostava de marcar uma avaliação.`,
      `Tratamento: ${val('trat')}`,
    ];
    if (!sens.hidden) linhas.push(`Sensibilidade nos dentes: ${val('sens')}`);
    const dia = form.dia.value.trim();
    linhas.push(`Preferência: ${dia ? dia + ', ' : ''}${val('per').toLowerCase()}`);
    const obs = form.obs.value.trim();
    if (obs) linhas.push(`Nota: ${obs}`);
    const msg = linhas.join('\n');
    let copiou = false;
    try { await navigator.clipboard.writeText(msg); copiou = true; } catch (_) {}
    nota.textContent = copiou
      ? 'Mensagem copiada. No WhatsApp, cola e envia.'
      : 'Copia esta mensagem e envia no WhatsApp: ' + msg.replace(/\n/g, ' · ');
    nota.classList.add('ok');
    window.open(WA, '_blank', 'noopener');
  });
  form.nome.addEventListener('input', () => form.nome.classList.remove('erro'));

  // Entradas: subida leve
  const els = document.querySelectorAll('.sobe');
  if (reduz || !('IntersectionObserver' in window)) { els.forEach(e => e.classList.add('visto')); return; }
  const io = new IntersectionObserver(ents => ents.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  els.forEach(e => io.observe(e));
})();
